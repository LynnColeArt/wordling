package layout

import (
	"encoding/binary"
	"errors"
	"math"
	"sort"

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
	HyphenationNo                       bool
	FullJustification                   bool
	RelativeTabSet                      bool
}

type Layout struct {
	Settings Settings
	Lines    []Line
	gaps     []position
}

type Line struct {
	Page, Row               int
	StartGap, EndGap        int
	TopInches, BottomInches float64
	LeftInches, RightInches float64
	WidthInches             float64
	Tokens                  []TokenPosition
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
	if end {
		g, valid := measure(l.Settings)
		if !valid {
			return 0, false
		}
		column = g.cols
	}
	return l.GapAt(line, column)
}

// atom is a layout decision point over existing native owners. In a reflow
// pass a soft return represents a space, and a deletable break represents
// no separator. The existing span is retained for revision-bound plan edits.
type atom struct {
	start, end int
	kind       document.Kind
	space      bool
}

type boundary uint8

const (
	wrapWord boundary = iota + 1
	wrapAtSpace
	returnLine
	explicitPage
)

type rowBreak struct {
	index int // native owner or the gap preceding an overflowing word
	kind  boundary
	page  int
	row   int
}

// rowsFor is used by pure projection and by the reflow planner. On overflow
// the most recent ordinary space belongs to the previous row as a zero-width
// separator. Only an unbroken run is split at the right margin.
func rowsFor(a []atom, g geometry) []rowBreak {
	var breaks []rowBreak
	page, row, col, lastSpace, start := 1, 0, 0, -1, 0
	advance := func(at int, kind boundary) {
		breaks = append(breaks, rowBreak{at, kind, page, row})
		if kind == explicitPage || row == g.rows-1 {
			page++
			row = 0
		} else {
			row++
		}
		col, lastSpace = 0, -1
	}
	for i := 0; i < len(a); {
		item := a[i]
		switch item.kind {
		case document.HardReturn:
			advance(item.start, returnLine)
			i++
			start = i
		case document.HardPage:
			advance(item.start, explicitPage)
			i++
			start = i
		case document.Tab:
			col = g.tabAfter(col)
			i++
		case document.ASCII:
			if item.space && col > 0 {
				lastSpace = i
			}
			if col < g.cols {
				col++
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
	before, after, skipSpace := physicalBreaks(tokens, g)
	out.gaps = make([]position, len(tokens)+1)
	page, row, col := 1, 0, 0
	qualified := true
	left := settings.MarginLeftInches
	width := float64(g.cols) / settings.CPI
	makeLine := func(start int) Line {
		top := settings.MarginTopInches + float64(row)*g.lineHeight
		return Line{Page: page, Row: row, StartGap: start, EndGap: start, TopInches: top,
			BottomInches: top + g.lineHeight, LeftInches: left, RightInches: left + width, WidthInches: width}
	}
	out.Lines = append(out.Lines, makeLine(0))
	advance := func(start int, forcePage bool) {
		if forcePage || row == g.rows-1 {
			page++
			row = 0
		} else {
			row++
		}
		col = 0
		out.Lines = append(out.Lines, makeLine(start))
	}
	for i, t := range tokens {
		if b, ok := before[i]; ok {
			advance(i, b.page)
		}
		line := &out.Lines[len(out.Lines)-1]
		line.EndGap = i
		editable := !insidePageGroup(tokens, i)
		out.gaps[i] = position{len(out.Lines) - 1, col, qualified, editable}
		cells, text := 0, ""
		switch t.Kind {
		case document.ASCII:
			if !skipSpace[i] {
				cells = 1
				text = string(t.Raw)
			}
		case document.Tab:
			cells, text = g.tabAfter(col)-col, "\t"
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
			advance(i+1, b.page)
		}
	}
	last := &out.Lines[len(out.Lines)-1]
	last.EndGap = len(tokens)
	out.gaps[len(tokens)] = position{len(out.Lines) - 1, col, qualified, true}
	return out
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

func physicalBreaks(tokens []Token, g geometry) (before, after map[int]physicalBreak, skip map[int]bool) {
	before, after, skip = map[int]physicalBreak{}, map[int]physicalBreak{}, map[int]bool{}
	start := 0
	addImplicit := func(end int) {
		a := make([]atom, 0, end-start)
		for i := start; i < end; i++ {
			t := tokens[i]
			a = append(a, atom{i, i + 1, t.Kind, isSpace(t)})
		}
		for _, b := range rowsFor(a, g) {
			switch b.kind {
			case wrapWord:
				before[b.index] = physicalBreak{}
			case wrapAtSpace:
				after[b.index] = physicalBreak{}
				skip[b.index] = true
			}
		}
	}
	for i, t := range tokens {
		switch t.Kind {
		case document.SoftReturn, document.DeletedSoftReturn, document.HardReturn:
			addImplicit(i)
			after[i] = physicalBreak{}
			start = i + 1
		case document.HardPage, document.HardReturnSoftPage, document.SoftPage, document.DeletedSoftPage:
			addImplicit(i)
			after[i] = physicalBreak{page: true}
			start = i + 1
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
	tokens, err := TokensFromDocument(d)
	if err != nil {
		return document.ReflowPlan{}, err
	}
	a, obsolete := semanticAtoms(tokens)
	g, _ := measure(settings)
	breaks := rowsFor(a, g)
	desired := make(map[int]rowBreak, len(breaks))
	for _, b := range breaks {
		desired[b.index] = b
	}

	var changes []document.ReflowChange
	for _, item := range a {
		b, exists := desired[item.start]
		if item.space || item.kind == document.HardReturn || item.kind == document.HardPage {
			if op, ok := separatorChange(tokens, item, b, exists, g.rows); ok {
				changes = append(changes, op)
			}
		}
		if exists && b.kind == wrapWord {
			// A stored break can be on either side of adjacent zero-width
			// formatting. Keep its native side if it occupies this cell.
			gap, prior, found := nearbyWordBreak(tokens, obsolete, item.start)
			op, ok := wordBreakChange(tokens, item.start, prior, found, b, g.rows)
			if ok {
				changes = append(changes, op)
			}
			if found {
				delete(obsolete, gap)
			}
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
func semanticAtoms(tokens []Token) ([]atom, map[int]int) {
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
				end++
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
		a = append(a, atom{i, end, kind, space})
		i = end
	}
	return a, derived
}

func separatorChange(tokens []Token, item atom, b rowBreak, exists bool, rows int) (document.ReflowChange, bool) {
	at := item.start
	original := tokens[at].Kind
	op := document.ReflowChange{At: at}
	isPage := exists && b.row == rows-1
	if item.kind == document.HardPage {
		if original == document.EndOfPage && samePageRecord(tokens[at], b.page, b.row) {
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
			return op, !samePageRecord(tokens[at], b.page, b.row)
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
	case document.BoldOn, document.BoldOff, document.UnderlineOn, document.UnderlineOff:
		return true
	default:
		return false
	}
}

func wordBreakChange(tokens []Token, at, prior int, found bool, b rowBreak, rows int) (document.ReflowChange, bool) {
	op := document.ReflowChange{At: at}
	if found {
		op.At = prior
	}
	if b.row == rows-1 {
		op.Page = uint16(b.page)
		if !found {
			op.Kind = document.InsertDeletedSoftPage
			return op, true
		}
		if tokens[prior].Kind == document.EndOfPage {
			op.Kind = document.RenumberSoftPage
			return op, !samePageRecord(tokens[prior], b.page, b.row)
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

func samePageRecord(t Token, page, row int) bool {
	// These are interpreted positions in an admitted owner, not a serialized
	// page record. Native field creation and validation belong to document.
	return len(t.Raw) >= 10 && int(binary.LittleEndian.Uint16(t.Raw[6:8])) == row*200 &&
		int(binary.LittleEndian.Uint16(t.Raw[8:10])) == page
}
