package layout

import (
	"encoding/binary"
	"errors"
	"math"
	"sort"
	"time"

	"github.com/lynncoleart/wordling/internal/document"
)

type Document interface {
	TokenCount() int
	Token(index int) (document.Token, error)
}

type Token = document.Token

type Settings struct {
	PageWidthInches, PageHeightInches   float64
	MarginLeftInches, MarginRightInches float64
	MarginTopInches, MarginBottomInches float64
	CPI                                 float64
	LineSpacing                         float64
	InitialLineSpacing                  int
	HyphenationNo                       bool
	FullJustification                   bool
	RelativeTabSet                      bool
	Date                                time.Time
}

type Layout struct {
	Settings       Settings
	Lines          []Line
	gaps           []position
	alignment      map[int]int
	tabSets        []tabSetChange
	decimalAnchors map[int]int
}

type Line struct {
	Page, Row               int
	StartGap, EndGap        int
	TopInches, BottomInches float64
	LeftInches, RightInches float64
	WidthInches             float64
	Tokens                  []TokenPosition
	FullJustification       bool
	Justification           document.Justification
}

type TokenPosition struct {
	Index       int
	Token       Token
	LeftInches  float64
	WidthInches float64
	Text        string
}

type position struct {
	line, column int
	qualified    bool
	editable     bool
}

var (
	errNoDocument = errors.New("layout: no document")
	errSettings   = errors.New("layout: invalid or unqualified paper settings")
	errOwner      = errors.New("layout: cannot reflow an unsupported native owner")
)

func FromDocument(d Document, settings Settings) (Layout, error) {
	if _, ok := measure(settings); !ok {
		return Layout{}, errSettings
	}
	tokens, err := TokensFromDocument(d)
	if err != nil {
		return Layout{}, err
	}
	if native, ok := d.(*document.Document); ok {
		settings.InitialLineSpacing, _ = native.InitialLineSpacing()
	}
	return Project(tokens, settings), nil
}

func TokensFromDocument(d Document) ([]Token, error) {
	if d == nil {
		return nil, errNoDocument
	}
	n := d.TokenCount()
	if n < 0 || n > document.MaxTokens {
		return nil, errOwner
	}
	tokens := make([]Token, n)
	for i := range tokens {
		tok, err := d.Token(i)
		if err != nil {
			return nil, err
		}
		tokens[i] = tok
	}
	return tokens, nil
}

type geometry struct {
	cols, rows, tab int
	lineHeight      float64
}

func layoutDate(settings Settings) string {
	if settings.Date.IsZero() {
		return document.FormatDate(time.Now())
	}
	return document.FormatDate(settings.Date)
}

func measure(settings Settings) (geometry, bool) {
	width := settings.PageWidthInches - settings.MarginLeftInches - settings.MarginRightInches
	height := settings.PageHeightInches - settings.MarginTopInches - settings.MarginBottomInches
	lineHeight := settings.LineSpacing / 6
	cols := math.Floor(width*settings.CPI + 1e-9)
	rows := math.Floor(height/lineHeight + 1e-9)
	if !(cols >= 1 && cols <= 10000 && rows >= 1 && rows <= 10000) ||
		!(settings.CPI > 0 && settings.CPI <= 10000) {
		return geometry{}, false
	}
	return geometry{int(cols), int(rows), max(1, int(math.Round(settings.CPI/2))), lineHeight}, true
}

// NextTabColumn returns the next relative half-inch stop in zero-based text
// columns. The stored Tab owner's display cache does not determine geometry.
func (settings Settings) NextTabColumn(column int) (int, bool) {
	g, ok := measure(settings)
	if !ok || !settings.RelativeTabSet || column < 0 || column > g.cols {
		return 0, false
	}
	return g.tabAfter(column), true
}

func (g geometry) tabAfter(column int) int {
	return min(g.cols, (column/g.tab+1)*g.tab)
}

func (l Layout) PositionAt(gap int) (line, column int, ok bool) {
	if gap < 0 || gap >= len(l.gaps) || !l.gaps[gap].qualified {
		return 0, 0, false
	}
	p := l.gaps[gap]
	return p.line, p.column, true
}

// GapAt finds a native insertion gap nearest a requested column on a physical
// row. Tabs expose their two real edges, not fake interior insertion points.
// Duplicate zero-width columns favor the last editable native gap.
func (l Layout) GapAt(line, column int) (int, bool) {
	if line < 0 || line >= len(l.Lines) || column < 0 {
		return 0, false
	}
	row := l.Lines[line]
	best, distance := -1, math.MaxInt
	for i := row.StartGap; i <= row.EndGap && i < len(l.gaps); i++ {
		p := l.gaps[i]
		if !p.qualified || !p.editable || p.line != line {
			continue
		}
		d := p.column - column
		if d < 0 {
			d = -d
		}
		if d <= distance {
			best, distance = i, d
		}
	}
	return best, best >= 0
}

// VerticalGap preserves the caller's desired column across short physical rows.
// The session owns the desired column and resets it after nonvertical movement.
func (l Layout) VerticalGap(gap, desiredColumn, delta int) (int, bool) {
	line, _, ok := l.PositionAt(gap)
	if !ok || delta != -1 && delta != 1 {
		return 0, false
	}
	return l.GapAt(line+delta, desiredColumn)
}

// PageGap returns the first editable gap on the adjacent physical page.
func (l Layout) PageGap(gap, delta int) (int, bool) {
	line, _, ok := l.PositionAt(gap)
	if !ok || delta != -1 && delta != 1 {
		return 0, false
	}
	target := l.Lines[line].Page + delta
	i := sort.Search(len(l.Lines), func(i int) bool { return l.Lines[i].Page >= target })
	if target < 1 || i >= len(l.Lines) || l.Lines[i].Page != target {
		return 0, false
	}
	return l.GapAt(i, 0)
}

// LineBoundary returns the first or last editable position on a physical row.
func (l Layout) LineBoundary(gap int, end bool) (int, bool) {
	line, _, ok := l.PositionAt(gap)
	if !ok {
		return 0, false
	}
	column := 0
	row := l.Lines[line]
	if end {
		column = int(math.Round((row.RightInches - l.Settings.MarginLeftInches) * l.Settings.CPI))
	}
	return l.GapAt(line, column)
}

// atom is a layout decision point over existing native owners. In a reflow
// pass a soft return represents a space, and a deletable break represents
// no separator. The existing span is retained for revision-bound plan edits.
type atom struct {
	start, end  int
	kind        document.Kind
	space       bool
	indent      int
	width       int
	left        int
	top, bottom int
	spacing     int
	height      int
	cells       int
	tabs        *document.TabSet
	keepLines   int
	keepNote    int
	noteLines   int
	pageNumber  int
	pageText    document.PageText
}

type boundary uint8

const (
	wrapWord boundary = iota + 1
	wrapAtSpace
	returnLine
	explicitPage
)

type rowBreak struct {
	index          int // native owner or the gap preceding an overflowing word
	kind           boundary
	page           int
	row            int
	top, bottom    int
	last           bool
	vertical       int
	header, footer bool
	oddHeader      bool
	conditional    bool
	pendingWidow   bool
	noteReserve    int
	pageNumber     int
	suppressNumber bool
}

// rowsFor is used by pure projection and by the reflow planner. On overflow
// the most recent ordinary space belongs to the previous row as a zero-width
// separator. Only an unbroken run is split at the right margin.
func rowsFor(a []atom, g geometry, settings Settings, protected map[int]bool) []rowBreak {
	var breaks []rowBreak
	page, row, col, lastSpace, start := 1, 0, 0, -1, 0
	indent := 0
	rightIndent := 0
	spacing := max(1, settings.InitialLineSpacing)
	height, vertical := 200, 0
	keepLines := 0
	top, bottom := defaultPageMargins(settings)
	left := int(math.Round((settings.MarginLeftInches - 1) * settings.CPI))
	var pageText [4]int
	numberPosition, suppressNumber := 0, false
	var tabs *document.TabSet
	advance := func(at int, kind boundary) {
		header, footer := pageText[0] != 0 || pageText[1] != 0, pageText[2] != 0 || pageText[3] != 0
		oddHeader := footer && pageText[0] != 1 && pageText[1] != 1 && (pageText[0] == 2 || pageText[1] == 2)
		pageHeight := pageBodyHeight(settings, top, bottom, header, footer)
		conditional := protected[at] || kind == returnLine && keepLines > 0 && keepLines*200 <= pageHeight &&
			vertical+height*spacing+keepLines*200 > pageHeight
		last := conditional || vertical+height*spacing+height > pageHeight
		breaks = append(breaks, rowBreak{at, kind, page, row, top, bottom, last, vertical, header, footer, oddHeader, conditional, false, 0, numberPosition, suppressNumber})
		keepLines = 0
		if kind == explicitPage || last {
			page++
			suppressNumber = false
			row, vertical = 0, 0
		} else {
			vertical += height * spacing
			row = vertical / 200
		}
		col, lastSpace = indent, -1
	}
	for i := 0; i < len(a); {
		item := a[i]
		switch item.kind {
		case document.TabSetCode:
			tabs = item.tabs
			i++
		case document.ConditionalPage:
			keepLines = max(keepLines, item.keepLines)
			i++
		case document.PageNumberPosition:
			numberPosition = item.pageNumber
			i++
		case document.SuppressPageNumber:
			suppressNumber = true
			i++
		case document.PageTextCode:
			pageText[item.pageText.Slot] = item.pageText.Pages
			i++
		case document.LineHeight:
			height = item.height
			if height == 0 {
				height = 200
			}
			i++
		case document.LineSpacing:
			spacing = item.spacing
			i++
		case document.PageMargins:
			top, bottom = item.top, item.bottom
			i++
		case document.LineMargins:
			if item.width > 0 {
				g.cols = item.width
			}
			left = item.left
			indent, rightIndent, col, lastSpace = 0, 0, 0, -1
			i++
			start = i
		case document.HardReturn:
			indent, rightIndent = 0, 0
			advance(item.start, returnLine)
			i++
			start = i
		case document.HardPage:
			indent, rightIndent = 0, 0
			advance(item.start, explicitPage)
			i++
			start = i
		case document.Indent, document.DoubleIndent:
			indentColumn := max(0, item.indent-left)
			if item.kind == document.DoubleIndent {
				rightIndent += max(0, indentColumn-indent)
			}
			indent, col, lastSpace = indentColumn, indentColumn, -1
			i++
			start = i
		case document.MarginRelease:
			col = max(0, item.indent-left)
			i++
		case document.Tab:
			col = layoutTab(g, tabs, (left+10)*120, col, g.cols-rightIndent)
			i++
		case document.ASCII, document.ExtendedCharacter, document.HardSpace, document.DOSControl, document.Footnote, document.Endnote, document.DateCode, document.PageReference, document.OutlineNumber:
			if item.space && col > 0 {
				lastSpace = i
			}
			cells := max(1, item.cells)
			limit := max(indent+1, g.cols-rightIndent)
			if col+cells <= limit || col == indent && cells > limit-indent {
				col += cells
				i++
				continue
			}
			if lastSpace >= start {
				next := lastSpace + 1
				advance(a[lastSpace].start, wrapAtSpace)
				i, start = next, next
				continue
			}
			advance(item.start, wrapWord)
			start = i
		default:
			i++
		}
	}
	return breaks
}

type physicalBreak struct {
	page bool
}

// Project keeps existing explicit owner boundaries visible and fills in wraps
// for editable text before native reflow. It never modifies source tokens.
func Project(tokens []Token, settings Settings) Layout {
	out := Layout{Settings: settings}
	g, ok := measure(settings)
	if !ok {
		return out
	}
	before, after, skipSpace := physicalBreaks(tokens, g, settings)
	out.gaps = make([]position, len(tokens)+1)
	page, row, col := 1, 0, 0
	indent := 0
	rightIndent := 0
	spacing := max(1, settings.InitialLineSpacing)
	height, vertical := g.lineHeight, 0.0
	qualified := true
	full := settings.FullJustification
	justification := document.JustifyLeft
	if full {
		justification = document.JustifyFull
	}
	left := settings.MarginLeftInches
	pageTop, pageBottom := defaultPageMargins(settings)
	var pageText [4]bool
	var tabs *document.TabSet
	width := float64(g.cols) / settings.CPI
	makeLine := func(start int) Line {
		top := float64(pageTop)/document.UnitsPerInch + vertical
		if pageText[0] || pageText[1] {
			top += 1.0 / 3
		}
		return Line{Page: page, Row: row, StartGap: start, EndGap: start, TopInches: top,
			BottomInches: top + float64(spacing)*height, LeftInches: left, RightInches: left + width - float64(rightIndent)/settings.CPI, WidthInches: width,
			FullJustification: full, Justification: justification}
	}
	out.Lines = append(out.Lines, makeLine(0))
	advance := func(start int, forcePage bool) {
		header, footer := pageText[0] || pageText[1], pageText[2] || pageText[3]
		bodyHeight := float64(pageBodyHeight(settings, pageTop, pageBottom, header, footer)) / document.UnitsPerInch
		if forcePage || vertical+float64(spacing+1)*height > bodyHeight+1e-9 {
			page++
			row, vertical = 0, 0
		} else {
			vertical += float64(spacing) * height
			row = int(math.Floor(vertical*6 + 1e-9))
		}
		col = indent
		out.Lines = append(out.Lines, makeLine(start))
	}
	for i, t := range tokens {
		if b, ok := before[i]; ok {
			advance(i, b.page)
		}
		line := &out.Lines[len(out.Lines)-1]
		line.EndGap = i
		editable := !insidePageGroup(tokens, i)
		base := int(math.Round((left - settings.MarginLeftInches) * settings.CPI))
		out.gaps[i] = position{len(out.Lines) - 1, base + col, qualified, editable}
		cells, text := 0, ""
		switch t.Kind {
		case document.TabSetCode:
			if ruler, ok := t.Tabs(); ok {
				tabs = &ruler
				out.tabSets = append(out.tabSets, tabSetChange{i, tabs})
			}
		case document.PageTextCode:
			text, ok := t.PageText()
			if ok {
				before := pageText[0] || pageText[1]
				pageText[text.Slot] = text.Pages != 0
				after := pageText[0] || pageText[1]
				if !before && after {
					line.TopInches += 1.0 / 3
					line.BottomInches += 1.0 / 3
				} else if before && !after {
					line.TopInches -= 1.0 / 3
					line.BottomInches -= 1.0 / 3
				}
			}
		case document.ParagraphJustification:
			justification, _ = t.Justification()
			full = justification == document.JustifyFull
			line.FullJustification, line.Justification = full, justification
		case document.LineHeight:
			height = g.lineHeight
			if value := t.LineHeight(); value != 0 {
				height = float64(value) / document.UnitsPerInch
			}
			line.BottomInches = line.TopInches + float64(spacing)*height
		case document.LineSpacing:
			spacing = t.LineSpacing()
			line.BottomInches = line.TopInches + float64(spacing)*height
		case document.PageMargins:
			pageTop, pageBottom, _ = t.PageMargins()
			line.TopInches = float64(pageTop)/document.UnitsPerInch + vertical
			line.BottomInches = line.TopInches + float64(spacing)*height
		case document.LineMargins:
			left, g.cols = marginGeometry(t, settings, left, g.cols)
			width = float64(g.cols) / settings.CPI
			line.LeftInches, line.RightInches, line.WidthInches = left, left+width, width
			col, indent, rightIndent = 0, 0, 0
		case document.ASCII, document.ExtendedCharacter, document.HardSpace:
			if !skipSpace[i] {
				cells = 1
				text = t.CharacterText()
			}
		case document.DOSControl:
			cells, text = 2, string([]byte{'^', t.Raw[0] + '@'})
		case document.DateCode:
			text = layoutDate(settings)
			cells = len(text)
		case document.MathSubtotal:
			text, cells = "+", 1
		case document.OutlineNumber:
			text = t.OutlineText()
			cells = len(text)
		case document.PageReference:
			ref, _ := t.CrossReference()
			text, cells = ref.Value, len(ref.Value)
		case document.Footnote, document.Endnote:
			text = t.NoteNumber()
			cells = len(text)
		case document.Indent, document.DoubleIndent:
			target := t.IndentColumn() - base
			if t.Kind == document.DoubleIndent {
				rightIndent += max(0, target-indent)
				line.RightInches = left + width - float64(rightIndent)/settings.CPI
			}
			indent, cells = target, target-col
		case document.MarginRelease:
			cells = t.MarginReleaseColumn() - base - col
		case document.EndIndent, document.HardReturn, document.HardReturnSoftPage, document.HardPage:
			indent, rightIndent = 0, 0
		case document.Tab:
			cells, text = layoutTab(g, tabs, int(math.Round(left*document.UnitsPerInch)), col, g.cols-rightIndent)-col, "\t"
		case document.MergeField, document.MergeEndField, document.MergeEndRecord, document.MergePageOff, document.MergePageOn, document.MergeNestPrimary, document.MergeNestSecondary, document.MergeIfBlank, document.MergeElse, document.MergeEndIf, document.MergeBreak:
			// The original shows labels in the editor without advancing
			// the printed position for these native owners.
			text = t.Kind.MergeLabel(false)
		case document.Opaque:
			qualified = false
		}
		line.Tokens = append(line.Tokens, TokenPosition{i, t, left + float64(col)/settings.CPI,
			float64(cells) / settings.CPI, text})
		col += cells
		if b, ok := after[i]; ok {
			if t.Kind != document.DormantHardReturn {
				advance(i+1, b.page)
			}
		}
	}
	last := &out.Lines[len(out.Lines)-1]
	last.EndGap = len(tokens)
	base := int(math.Round((left - settings.MarginLeftInches) * settings.CPI))
	out.gaps[len(tokens)] = position{len(out.Lines) - 1, base + col, qualified, true}
	out.applyAlignment()
	return out
}

func (l *Layout) applyParagraphAlignment(row int) {
	line := &l.Lines[row]
	if line.Justification != document.JustifyCenter && line.Justification != document.JustifyRight {
		return
	}
	width, first := 0.0, -1
	for i, item := range line.Tokens {
		if item.WidthInches > 0 {
			if first < 0 {
				first = i
			}
			width += item.WidthInches
		}
	}
	if first < 0 {
		return
	}
	start := line.RightInches - width
	if line.Justification == document.JustifyCenter {
		start = (line.LeftInches + start) / 2
	}
	shift := max(0, start-line.Tokens[first].LeftInches)
	cells := int(math.Floor(shift*l.Settings.CPI + 1e-9))
	for i := range line.Tokens {
		token := &line.Tokens[i]
		l.shiftAlignedGap(token.Index, token.LeftInches+shift, cells)
		token.LeftInches += shift
	}
	last := line.Tokens[len(line.Tokens)-1]
	if line.EndGap > last.Index && l.gaps[line.EndGap].line == row {
		l.shiftAlignedGap(line.EndGap, last.LeftInches+last.WidthInches, cells)
	}
}

// ParagraphPositionChanges refreshes the formatter's start-position records
// after the document's physical line breaks have been resolved.
func (l Layout) ParagraphPositionChanges() []document.ReflowChange {
	var changes []document.ReflowChange
	for _, line := range l.Lines {
		aligned := line.Justification == document.JustifyCenter || line.Justification == document.JustifyRight
		record, first := -1, -1
		position := (line.LeftInches + line.RightInches) / 2
		for _, token := range line.Tokens {
			if token.Token.Kind == document.ParagraphJustification {
				record = -1
			}
			if token.Token.Kind == document.ParagraphPosition {
				record = token.Index
			}
			if first == -1 && token.WidthInches > 0 {
				first, position = token.Index, token.LeftInches
			}
		}
		at, kind := first, document.InsertParagraphPosition
		switch {
		case aligned && record >= 0:
			at, kind = record, document.RefreshParagraphPosition
		case !aligned && record >= 0:
			at, kind = record, document.RemoveParagraphPosition
			position = 0
		}
		// DOS retains a blank centered row as a cache-only paragraph.
		if aligned && at < 0 && line.Justification == document.JustifyCenter {
			at = line.EndGap
		}
		if at >= 0 && (aligned || record >= 0) {
			changes = append(changes, document.ReflowChange{
				At: at, Kind: kind, Position: uint16(math.Round(position * document.UnitsPerInch)),
			})
		}
	}
	return changes
}

// PrintedColumn returns the horizontal cursor position in inches. Centered
// text can occupy half cells in the formatter and still use whole screen cells.
func (l Layout) PrintedColumn(gap int) (float64, bool) {
	_, col, ok := l.PositionAt(gap)
	if !ok {
		return 0, false
	}
	pos := l.Settings.MarginLeftInches + float64(col)/l.Settings.CPI
	if units, ok := l.alignment[gap]; ok {
		pos = float64(units) / document.UnitsPerInch
	}
	return pos, true
}

func (l Layout) NextTabColumnAt(gap int) (int, bool) {
	target, _, ok := l.NextTabStopAt(gap)
	return target, ok
}

func (l Layout) NextTabStopAt(gap int) (target int, decimal, ok bool) {
	row, column, ok := l.PositionAt(gap)
	if !ok || !l.Settings.RelativeTabSet {
		return 0, false, false
	}
	line := l.Lines[row]
	origin := int(math.Round((line.LeftInches - l.Settings.MarginLeftInches) * l.Settings.CPI))
	width := int(math.Round(line.WidthInches * l.Settings.CPI))
	step := max(1, int(math.Round(l.Settings.CPI/2)))
	margin := int(math.Round(line.LeftInches * document.UnitsPerInch))
	target, decimal = layoutTabStop(geometry{cols: width, tab: step}, l.tabsAt(gap), margin, max(0, column-origin), width)
	return origin + target, decimal, true
}

func (l Layout) AtLineStart(gap int) bool {
	row, _, ok := l.PositionAt(gap)
	return ok && l.Lines[row].StartGap == gap
}

func (l *Layout) applyAlignment() {
	for row := range l.Lines {
		l.applyParagraphAlignment(row)
		line := &l.Lines[row]
		for first := range line.Tokens {
			item := line.Tokens[first]
			kind := item.Token.Kind
			if kind != document.CenterLine && kind != document.FlushRight && kind != document.DecimalTab && kind != document.SoftDecimalTab && kind != document.ContentsLeader {
				continue
			}
			end := first + 1
			width := 0.0
			for end < len(line.Tokens) && line.Tokens[end].Token.Kind != document.EndAlignment &&
				line.Tokens[end].Token.Kind != document.CenterLine && line.Tokens[end].Token.Kind != document.FlushRight && line.Tokens[end].Token.Kind != document.DecimalTab && line.Tokens[end].Token.Kind != document.SoftDecimalTab {
				width += line.Tokens[end].WidthInches
				end++
			}
			anchor := line.RightInches
			if kind == document.ContentsLeader {
				// The generated page field sits at the document margin,
				// outside the title’s double indent.
				anchor = line.LeftInches + line.WidthInches
			}
			position := anchor - width
			if kind == document.CenterLine {
				anchor = (line.LeftInches + line.RightInches) / 2
				position = anchor - width/2
			} else if kind == document.DecimalTab || kind == document.SoftDecimalTab {
				origin := int(math.Round(line.LeftInches * document.UnitsPerInch))
				col := int(math.Round((item.LeftInches - line.LeftInches) * l.Settings.CPI))
				right := int(math.Round((line.RightInches - line.LeftInches) * l.Settings.CPI))
				target := layoutTab(geometry{cols: right, tab: 5}, l.tabsAt(item.Index), origin, col, right)
				anchor = line.LeftInches + float64(target)/l.Settings.CPI
				position = anchor - width
				if l.decimalAnchors == nil {
					l.decimalAnchors = make(map[int]int)
				}
				l.decimalAnchors[item.Index] = int(math.Round(anchor * document.UnitsPerInch))
			}
			decimal := kind == document.DecimalTab || kind == document.SoftDecimalTab
			shift := max(0, position-item.LeftInches)
			line.Tokens[first].LeftInches = item.LeftInches + shift
			if kind == document.ContentsLeader {
				line.Tokens[first].WidthInches = shift
			}
			cells := int(math.Floor(shift*l.Settings.CPI + 1e-9))
			for i := first + 1; i < len(line.Tokens); i++ {
				token := &line.Tokens[i]
				if !decimal && (token.Token.Kind == document.CenterLine || token.Token.Kind == document.FlushRight ||
					token.Token.Kind == document.DecimalTab || token.Token.Kind == document.SoftDecimalTab) {
					break
				}
				l.shiftAlignedGap(token.Index, token.LeftInches+shift, cells)
				token.LeftInches += shift
				if decimal && token.Token.Kind == document.Tab {
					origin := int(math.Round(line.LeftInches * document.UnitsPerInch))
					col := int(math.Round((token.LeftInches - line.LeftInches) * l.Settings.CPI))
					right := int(math.Round((line.RightInches - line.LeftInches) * l.Settings.CPI))
					next := layoutTab(geometry{cols: right, tab: 5}, l.tabsAt(token.Index), origin, col, right)
					updated := float64(next-col) / l.Settings.CPI
					shift += updated - token.WidthInches
					cells = int(math.Round(shift * l.Settings.CPI))
					token.WidthInches = updated
				}
				if i == len(line.Tokens)-1 && line.EndGap > token.Index {
					if l.gaps[line.EndGap].line == row {
						l.shiftAlignedGap(line.EndGap, token.LeftInches+token.WidthInches, cells)
					}
				}
			}
		}
	}
}

func (l *Layout) shiftAlignedGap(gap int, inches float64, cells int) {
	if l.alignment == nil {
		l.alignment = make(map[int]int)
	}
	l.gaps[gap].column += cells
	l.alignment[gap] = int(math.Round(inches * document.UnitsPerInch))
}

func insidePageGroup(tokens []Token, i int) bool {
	if i <= 0 || i >= len(tokens) {
		return false
	}
	switch tokens[i].Kind {
	case document.HardPage, document.HardReturnSoftPage, document.SoftPage, document.DeletedSoftPage:
		return tokens[i-1].Kind == document.EndOfPage
	case document.DormantHardReturn:
		return i > 1 && tokens[i-2].Kind == document.EndOfPage && tokens[i-1].Kind == document.HardReturnSoftPage
	default:
		return false
	}
}

func physicalBreaks(tokens []Token, g geometry, settings Settings) (before, after map[int]physicalBreak, skip map[int]bool) {
	before, after, skip = map[int]physicalBreak{}, map[int]physicalBreak{}, map[int]bool{}
	start, indent := 0, 0
	indentKind := document.Indent
	nextKind := indentKind
	left := int(math.Round((settings.MarginLeftInches - 1) * settings.CPI))
	var tabs *document.TabSet
	addImplicit := func(end int) {
		a := make([]atom, 0, end-start+1)
		if tabs != nil {
			a = append(a, atom{kind: document.TabSetCode, tabs: tabs})
		}
		if left != 0 {
			a = append(a, atom{kind: document.LineMargins, width: g.cols, left: left})
		}
		if indent != 0 {
			a = append(a, atom{kind: indentKind, indent: indent})
		}
		for i := start; i < end; i++ {
			t := tokens[i]
			_, width := marginGeometry(t, settings, 0, 0)
			top, bottom, _ := t.PageMargins()
			a = append(a, tokenAtom(t, i, i+1, t.Kind, isSpace(t), width, top, bottom, settings))
		}
		for _, b := range rowsFor(a, g, settings, nil) {
			switch b.kind {
			case wrapWord:
				before[b.index] = physicalBreak{}
			case wrapAtSpace:
				after[b.index] = physicalBreak{}
				skip[b.index] = true
			}
		}
	}
	nextIndent := indent
	for i, t := range tokens {
		switch t.Kind {
		case document.Indent, document.DoubleIndent:
			nextIndent = t.IndentColumn()
			nextKind = t.Kind
		case document.EndIndent:
			nextIndent = 0
		case document.SoftReturn, document.DeletedSoftReturn, document.HardReturn,
			document.HardPage, document.HardReturnSoftPage, document.SoftPage, document.DeletedSoftPage:
			addImplicit(i)
			page := t.Kind == document.HardPage || t.Kind == document.HardReturnSoftPage ||
				t.Kind == document.SoftPage || t.Kind == document.DeletedSoftPage
			after[i] = physicalBreak{page: page}
			if t.Kind == document.HardReturn || t.Kind == document.HardPage || t.Kind == document.HardReturnSoftPage {
				nextIndent = 0
			}
			for _, owner := range tokens[start:i] {
				if ruler, ok := owner.Tabs(); ok {
					tabs = &ruler
				}
				_, g.cols = marginGeometry(owner, settings, 0, g.cols)
				if value, _, ok := owner.LineMargins(); ok {
					left = int(math.Round(float64(value)*settings.CPI/document.UnitsPerInch - settings.CPI))
				}
			}
			start, indent = i+1, nextIndent
			indentKind = nextKind
		}
	}
	addImplicit(len(tokens))
	return before, after, skip
}

func isSpace(token Token) bool {
	return token.Kind == document.ASCII && len(token.Raw) == 1 && token.Raw[0] == ' '
}

// PlanReflow computes native owner changes after a semantic edit. Projection
// and window resize never call this writer-facing operation. The returned plan
// is bound by document to this exact revision and has no serialized view text.
func PlanReflow(d *document.Document, settings Settings) (document.ReflowPlan, error) {
	if d == nil {
		return document.ReflowPlan{}, errNoDocument
	}
	if !matchedProfile(settings) {
		return document.ReflowPlan{}, errSettings
	}
	if err := d.CheckMutation(); err != nil {
		return document.ReflowPlan{}, err
	}
	settings.InitialLineSpacing, _ = d.InitialLineSpacing()
	tokens, err := TokensFromDocument(d)
	if err != nil {
		return document.ReflowPlan{}, err
	}
	a, obsolete := semanticAtoms(tokens, settings)
	g, _ := measure(settings)
	breaks := rowsFor(a, g, settings, nil)
	// A protected block that fits on a page moves at the preceding hard
	// return. Recalculate subsequent page positions after each such move.
	for i, item := range a {
		if item.kind != document.BlockProtectOn || i == 0 {
			continue
		}
		rows := int(binary.LittleEndian.Uint16(tokens[item.start].Raw[2:4])) / 200
		preceding := i - 1
		for preceding >= 0 && a[preceding].kind != document.HardReturn && a[preceding].kind != document.HardPage {
			preceding--
		}
		if preceding < 0 || a[preceding].kind != document.HardReturn {
			continue
		}
		prev := a[preceding].start
		for _, br := range breaks {
			if br.index != prev {
				continue
			}
			if br.row+1 < g.rows && br.row+1+rows > g.rows {
				a[preceding].kind = document.HardPage
				breaks = rowsFor(a, g, settings, nil)
			}
			break
		}
	}
	breaks = protectWidowRows(a, g, settings, breaks)
	breaks, noteSplits := noteFlow(a, g, settings, breaks)
	desired := make(map[int]rowBreak, len(breaks))
	for _, b := range breaks {
		desired[b.index] = b
	}

	changes := noteFlowChanges(a, noteSplits, tokens)
	for _, item := range a {
		b, exists := desired[item.start]
		if exists && b.conditional && item.kind == document.HardReturn {
			if tokens[item.start].Kind != document.EndOfPage || tokens[item.start].Raw[14] != b.protectedMarker() || !samePageRecord(tokens[item.start], b) {
				op := document.ReflowChange{At: item.start, Kind: document.PromoteProtectedReturn, Page: uint16(b.page), Row: uint16(b.row)}
				applyPageGeometry(&op, b)
				changes = append(changes, op)
			}
			continue
		}
		if exists && item.kind == document.HardPage &&
			(tokens[item.start].Kind == document.HardReturn || tokens[item.start].Kind == document.EndOfPage &&
				item.end > item.start+1 && tokens[item.start+1].Kind == document.HardReturnSoftPage) {
			if tokens[item.start].Kind != document.EndOfPage || tokens[item.start].Raw[14] != 1 || !samePageRecord(tokens[item.start], b) {
				op := document.ReflowChange{At: item.start, Kind: document.PromoteProtectedReturn, Page: uint16(b.page), Row: uint16(b.row)}
				applyPageGeometry(&op, b)
				changes = append(changes, op)
			}
			continue
		}
		if item.space || item.kind == document.HardReturn || item.kind == document.HardPage {
			if op, ok := separatorChange(tokens, item, b, exists); ok {
				applyPageGeometry(&op, b)
				if item.space {
					op.PageProtection = b.spaceProtection()
				}
				changes = append(changes, op)
			}
		}
		if exists && b.kind == wrapWord {
			// A stored break can be on either side of adjacent zero-width
			// formatting. Keep its native side if it occupies this cell.
			gap, prior, found := nearbyWordBreak(tokens, obsolete, item.start)
			op, ok := wordBreakChange(tokens, item.start, prior, found, b)
			if ok {
				applyPageGeometry(&op, b)
				changes = append(changes, op)
			}
			if found {
				delete(obsolete, gap)
			}
		}
	}
	for i := 3; i < len(tokens); i++ {
		if tokens[i].Kind != document.DormantHardReturn || tokens[i-3].Kind != document.BlockProtectOff ||
			tokens[i-2].Kind != document.EndOfPage || tokens[i-1].Kind != document.HardReturnSoftPage {
			continue
		}
		b, kept := desired[i-2]
		if kept && b.last && samePageRecord(tokens[i-2], b) {
			changes = append(changes, document.ReflowChange{At: i, Kind: document.OmitProtectedDormantReturn})
		}
	}
	for _, i := range obsolete {
		kind := document.RemoveDeletedSoftReturn
		if tokens[i].Kind == document.EndOfPage {
			kind = document.DemoteSoftPage
		}
		changes = append(changes, document.ReflowChange{At: i, Kind: kind})
	}
	sort.Slice(changes, func(i, j int) bool { return changes[i].At < changes[j].At })
	return document.NewReflowPlan(d, changes)
}

func matchedProfile(s Settings) bool {
	return s.PageWidthInches == 8.5 && s.PageHeightInches == 11 &&
		s.MarginLeftInches == 1 && s.MarginRightInches == 1 &&
		s.MarginTopInches == 1 && s.MarginBottomInches == 1 &&
		s.CPI == 10 && s.LineSpacing == 1 && s.HyphenationNo &&
		s.FullJustification && s.RelativeTabSet
}

// semanticAtoms collapses a page group to the underlying separator. A derived
// DSRt/DSPg has no separator; its exact native position is retained so the
// planner can conserve or replace it without touching adjacent native owners.
func semanticAtoms(tokens []Token, settings Settings) ([]atom, map[int]int) {
	a := make([]atom, 0, len(tokens))
	derived := map[int]int{}
	for i := 0; i < len(tokens); {
		kind := tokens[i].Kind
		end := i + 1
		space := isSpace(tokens[i])
		if kind == document.EndOfPage {
			// CheckMutation has already established the complete group.
			kind = tokens[end].Kind
			end++
			if kind == document.HardReturnSoftPage {
				kind = document.HardReturn
				if end < len(tokens) && tokens[end].Kind == document.DormantHardReturn {
					end++
				}
			}
		}
		switch kind {
		case document.SoftPage, document.SoftReturn:
			kind, space = document.ASCII, true
		case document.DeletedSoftPage, document.DeletedSoftReturn:
			derived[end] = i
			i = end
			continue
		}
		_, width := marginGeometry(tokens[i], settings, 0, 0)
		top, bottom, _ := tokens[i].PageMargins()
		a = append(a, tokenAtom(tokens[i], i, end, kind, space, width, top, bottom, settings))
		i = end
	}
	return a, derived
}

func tokenAtom(token Token, start, end int, kind document.Kind, space bool, width, top, bottom int, settings Settings) atom {
	indent := token.IndentColumn()
	if kind == document.MarginRelease {
		indent = token.MarginReleaseColumn()
	}
	cells := len(token.NoteNumber()) + len(token.OutlineText())
	if ref, ok := token.CrossReference(); ok {
		cells = len(ref.Value)
	}
	if kind == document.DateCode {
		cells = len(layoutDate(settings))
	}
	if kind == document.DOSControl {
		cells = 2
	}
	pageText, _ := token.PageText()
	left := 0
	if units, _, ok := token.LineMargins(); ok {
		left = units/120 - 10
	}
	var ruler *document.TabSet
	if value, ok := token.Tabs(); ok {
		ruler = &value
	}
	keep, _ := token.FootnoteKeep()
	return atom{start: start, end: end, kind: kind, tabs: ruler, space: space, indent: indent, width: width, left: left,
		top: top, bottom: bottom, spacing: token.LineSpacing(), height: token.LineHeight(), cells: cells,
		keepLines: token.ConditionalLines(), keepNote: keep, noteLines: footnoteLineCount(token), pageText: pageText, pageNumber: token.PageNumberPosition()}
}

func marginGeometry(token Token, settings Settings, left float64, width int) (float64, int) {
	nextLeft, nextRight, ok := token.LineMargins()
	if !ok {
		return left, width
	}
	left = float64(nextLeft) / document.UnitsPerInch
	right := float64(nextRight) / document.UnitsPerInch
	columns := int(math.Floor((settings.PageWidthInches-left-right)*settings.CPI + 1e-9))
	return left, max(1, columns)
}

func defaultPageMargins(settings Settings) (int, int) {
	return int(math.Round(settings.MarginTopInches * document.UnitsPerInch)),
		int(math.Round(settings.MarginBottomInches * document.UnitsPerInch))
}

func printableHeight(settings Settings, top, bottom int) int {
	return int(math.Round(settings.PageHeightInches*document.UnitsPerInch)) - top - bottom
}

func pageBodyHeight(settings Settings, top, bottom int, header, footer bool) int {
	height := printableHeight(settings, top, bottom)
	if header {
		height -= 400
	}
	if footer {
		height -= 400
	}
	return max(200, height)
}

func applyPageGeometry(change *document.ReflowChange, b rowBreak) {
	if change.Page != 0 && (b.header || b.footer || b.top != document.UnitsPerInch || b.bottom != document.UnitsPerInch ||
		b.last && b.vertical != 10600 || b.vertical%200 != 0 || b.spaceProtection() != 0 ||
		change.Kind == document.RefreshHardPage && (b.pageNumber != 0 || b.suppressNumber)) {
		change.Row, change.Top, change.Bottom = uint16(b.row), uint16(b.top), uint16(b.bottom)
		change.Vertical = uint16(b.vertical)
		change.CustomPage = true
		change.Header, change.Footer = b.header, b.footer
		change.OddHeader = b.oddHeader
		change.NoteReserve = uint16(b.noteReserve)
		if change.Kind == document.RefreshHardPage {
			change.PageNumberPosition, change.PageNumberSuppressed = uint8(b.pageNumber), b.suppressNumber
		}
	}
}

func (b rowBreak) protectedMarker() byte {
	if b.noteReserve != 0 {
		return 0
	}
	return 1
}

func (b rowBreak) spaceProtection() uint8 {
	if b.conditional {
		return 1
	}
	if b.pendingWidow {
		return 2
	}
	return 0
}

func separatorChange(tokens []Token, item atom, b rowBreak, exists bool) (document.ReflowChange, bool) {
	at := item.start
	original := tokens[at].Kind
	op := document.ReflowChange{At: at}
	isPage := exists && b.last
	if item.kind == document.HardPage {
		if original == document.EndOfPage && samePageRecord(tokens[at], b) {
			return op, false
		}
		op.Kind, op.Page, op.Row = document.RefreshHardPage, uint16(b.page), uint16(b.row)
		return op, true
	}
	if isPage {
		op.Page = uint16(b.page)
		switch original {
		case document.EndOfPage:
			op.Kind = document.RenumberSoftPage
			return op, !samePageRecord(tokens[at], b) || item.space && tokens[at].Raw[14] != b.spaceProtection()
		case document.HardReturn:
			op.Kind = document.PromoteHardReturn
		default:
			op.Kind = document.WrapSpaceToPage
		}
		return op, true
	}
	if original == document.EndOfPage {
		op.Kind = document.DemoteSoftPage
		if item.space && exists {
			op.Kind = document.SoftenPageBreak
		}
		return op, true
	}
	if !item.space {
		return op, false
	}
	if exists && original == document.ASCII {
		op.Kind = document.WrapSpace
		return op, true
	}
	if !exists && original == document.SoftReturn {
		op.Kind = document.UnwrapSpace
		return op, true
	}
	return op, false
}

func nearbyWordBreak(tokens []Token, stored map[int]int, at int) (gap, prior int, found bool) {
	for gap = at; ; gap-- {
		if prior, found = stored[gap]; found {
			return gap, prior, true
		}
		if gap == 0 || !isAttribute(tokens[gap-1].Kind) {
			return 0, 0, false
		}
	}
}

func isAttribute(kind document.Kind) bool {
	switch kind {
	case document.BoldOn, document.BoldOff, document.UnderlineOn, document.UnderlineOff,
		document.RedlineOn, document.RedlineOff, document.StrikeoutOn, document.StrikeoutOff, document.ItalicsOn, document.ItalicsOff:
		return true
	default:
		return false
	}
}

func wordBreakChange(tokens []Token, at, prior int, found bool, b rowBreak) (document.ReflowChange, bool) {
	op := document.ReflowChange{At: at}
	if found {
		op.At = prior
	}
	if b.last {
		op.Page = uint16(b.page)
		if !found {
			op.Kind = document.InsertDeletedSoftPage
			return op, true
		}
		if tokens[prior].Kind == document.EndOfPage {
			op.Kind = document.RenumberSoftPage
			return op, !samePageRecord(tokens[prior], b)
		}
		op.Kind = document.PromoteDeletedSoftReturn
		return op, true
	}
	if !found {
		op.Kind = document.InsertDeletedSoftReturn
		return op, true
	}
	if tokens[prior].Kind == document.EndOfPage {
		op.Kind = document.SoftenPageBreak
		return op, true
	}
	return op, false
}

func samePageRecord(t Token, b rowBreak) bool {
	// These are interpreted positions in an admitted owner, not a serialized
	// page record. Native field creation and validation belong to document.
	header, footer := 0, 0
	if b.header {
		header = 400
	}
	if b.footer {
		footer = 400
	}
	height := 13200 - b.top - b.bottom
	second, third := height-header, height-header-footer
	bottomReference := header
	if b.oddHeader {
		second, third, bottomReference = height-800, height-400, 0
	}
	if b.kind == explicitPage && !b.suppressNumber {
		switch b.pageNumber {
		case document.PageNumberTopCenter:
			if !b.header {
				header, bottomReference = 400, 400
				second, third = second-400, third-400
			}
		case document.PageNumberBottomRight:
			second -= 400
			if !b.footer {
				third -= 400
			}
		}
	}
	suppressed := byte(0)
	if b.kind == explicitPage && b.suppressNumber {
		suppressed = 1
	}
	return len(t.Raw) == 32 && t.Raw[15] == suppressed && int(binary.LittleEndian.Uint16(t.Raw[6:8])) == b.vertical &&
		int(binary.LittleEndian.Uint16(t.Raw[8:10])) == b.page &&
		int(binary.LittleEndian.Uint16(t.Raw[10:12])) == b.noteReserve &&
		int(binary.LittleEndian.Uint16(t.Raw[24:26])) == b.top+header &&
		int(binary.LittleEndian.Uint16(t.Raw[26:28])) == b.top+bottomReference &&
		int(binary.LittleEndian.Uint16(t.Raw[18:20])) == height &&
		int(binary.LittleEndian.Uint16(t.Raw[20:22])) == second &&
		int(binary.LittleEndian.Uint16(t.Raw[22:24])) == third
}

// ScreenColumnOffset follows DOS text-mode horizontal scrolling in quarter-screen steps.
func ScreenColumnOffset(column, width int) int {
	if width <= 0 || column < width {
		return 0
	}
	step := max(1, width/4)
	return ((column-width)/step + 1) * step
}
