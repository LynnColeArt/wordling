package tui

import (
	"fmt"
	"math"
	"sort"
	"strings"
	"unicode/utf8"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/layout"
)

type everydayFrame struct {
	normal, codes []string
	row, column   int
}

// The positions and semantic owners come from one immutable native revision.
// Terminal dimensions only select its visible window.
type everydayViewport struct {
	revision    document.Revision
	layout      layout.Layout
	ready       bool
	visualRows  []int
	visualWidth int
	top         [editor.MaxDocumentScreens]int
}

func (m *Model) prepareEverydayViewport() {
	if m.runtime == nil || !m.runtime.editorChrome ||
		!m.showEditorChrome() && (m.historic.menu || m.historic.files) {
		return
	}
	s := m.session.Snapshot()
	d := m.session.Document()
	v := &m.everyday
	if d == nil {
		v.ready = false
		return
	}
	if !v.ready || v.revision != s.NativeRevision {
		settings := editor.EverydaySettings()
		settings.Date = m.runtime.now()
		p, err := layout.FromDocument(d, settings)
		v.revision, v.layout, v.ready = s.NativeRevision, p, err == nil
		v.visualRows = nil
	}
	if v.ready && (v.visualRows == nil || v.visualWidth != m.width) {
		v.visualRows = visualRows(v.layout, m.width)
		v.visualWidth = m.width
	}
	if !v.ready || s.Screen < 1 || s.Screen > editor.MaxDocumentScreens || m.proofModal() {
		return
	}
	line, _, ok := v.layout.PositionAt(s.Gap)
	if !ok || line < 0 || line >= len(v.visualRows) {
		return
	}
	row := v.visualRows[line]
	top := &v.top[s.Screen-1]
	if row < *top {
		*top = row
	} else if height := m.documentRows(s.Reveal); row >= *top+height {
		*top = row - height + 1
	}
}

// Original PageUp/PageDown bring the first line of the new page to the
// top of the editing viewport; an ordinary editing wrap scrolls only as
// needed to expose the caret. The projection's page membership is unchanged.
func (m *Model) scrollPageToCaret() {
	v := &m.everyday
	s := m.session.Snapshot()
	if !v.ready || s.Screen < 1 || s.Screen > editor.MaxDocumentScreens {
		return
	}
	line, _, ok := v.layout.PositionAt(s.Gap)
	if ok && line >= 0 && line < len(v.visualRows) {
		v.top[s.Screen-1] = v.visualRows[line]
	}
}

// The dashed page separator is an upper-pane screen row. It is never a
// physical document line or a native owner.
func lineCommentRows(line layout.Line, width int) []string {
	var rows []string
	for _, t := range line.Tokens {
		if text, ok := t.Token.Comment(); ok {
			rows = append(rows, commentBox(text, width)...)
		} else if name, ok := t.Token.Subdocument(); ok {
			rows = append(rows, commentBox("Subdoc: "+name, width)...)
		}
	}
	return rows
}

func visualRows(p layout.Layout, width int) []int {
	rows := make([]int, len(p.Lines))
	row := 0
	for i, line := range p.Lines {
		if i > 0 && p.Lines[i-1].Page != line.Page {
			row++
		}
		rows[i] = row + len(lineCommentRows(line, width))
		row = rows[i] + 1
	}
	return rows
}

const (
	underlined    = "\x1b[22;34;47m" // Original 0x71.
	boldUnderline = "\x1b[22;97;47m" // Original 0x7F.
	redlineText   = "\x1b[22;31;47m" // Original 0x74.
	strikeoutText = "\x1b[22;30;46m" // Original 0x30.
	italicText    = "\x1b[22;93;44m" // Original 0x1E.
)

func projectEveryday(d *document.Document, gap, width, rows int) (everydayFrame, error) {
	p, err := layout.FromDocument(d, editor.EverydaySettings())
	if err != nil {
		return everydayFrame{}, err
	}
	return paintEveryday(d, nil, p, visualRows(p, width), gap, false, -1, -1, width, 0, rows, 0)
}

type historyPreviewDisplay struct {
	labels []string
	active int
}

func paintEveryday(d *document.Document, preview *historyPreviewDisplay, p layout.Layout, visual []int, gap int, reveal bool, blockStart, blockEnd, width, top, normalRows, codeRows int, highlighted ...proofRange) (everydayFrame, error) {
	y, x, ok := p.PositionAt(gap)
	if !ok || y < 0 || y >= len(visual) {
		return everydayFrame{}, fmt.Errorf("cursor is outside the qualified layout")
	}
	f := everydayFrame{row: visual[y] - top, column: x, normal: make([]string, normalRows)}
	// The original lower pane centers the active line at its fourth row
	// once possible, independently of the upper viewport's scroll.
	codeTop := 0
	codeEnd := 0
	revealGap := gap
	if reveal && codeRows > 0 {
		codeTop = max(0, y-min(3, codeRows-1))
		codeEnd = min(len(p.Lines), codeTop+codeRows)
		f.codes = make([]string, codeEnd-codeTop)
		if preview == nil {
			owner, err := d.Token(gap)
			if err == nil && owner.Kind == document.EndOfPage {
				next, err := d.Token(gap + 1)
				if err == nil && next.Kind == document.HardPage {
					// Reveal shows the page break at the hidden cache's gap.
					revealGap++
				}
			}
		}
	}
	normalStart := sort.Search(len(visual), func(i int) bool { return visual[i] >= top })
	normalEnd := sort.SearchInts(visual, top+normalRows)
	blockLo, blockHi := min(blockStart, blockEnd), max(blockStart, blockEnd)
	bold, underline := false, false
	redline, strikeout, italics := false, false, false
	for row, line := range p.Lines[:max(normalEnd, codeEnd)] {
		paintNormal := row >= normalStart && row < normalEnd
		paintCode := codeEnd > 0 && row >= codeTop && row < codeEnd
		var normal, codes []revealRun
		col, mergeCells, codeCells, activeCode := 0, 0, 0, -1
		activeCodeWidth := 1
		var labels []document.Element
		if paintCode && preview == nil && len(line.Tokens) != 0 {
			start := line.Tokens[0].Index
			for offset := 0; offset < len(line.Tokens); offset += document.MaxWindowTokens {
				count := min(len(line.Tokens)-offset, document.MaxWindowTokens)
				window, err := document.InspectRevealCatalogue(d, d.Revision(), start+offset, count)
				if err != nil {
					return everydayFrame{}, err
				}
				labels = append(labels, window.Elements...)
			}
		}
		for j, pos := range line.Tokens {
			token, i := pos.Token, pos.Index
			switch token.Kind {
			case document.Opaque:
				return everydayFrame{}, fmt.Errorf("unsupported native layout owner %d", i)
			case document.BoldOn:
				bold = true
			case document.BoldOff:
				bold = false
			case document.UnderlineOn:
				underline = true
			case document.UnderlineOff:
				underline = false
			case document.RedlineOn:
				redline = true
			case document.RedlineOff:
				redline = false
			case document.StrikeoutOn:
				strikeout = true
			case document.StrikeoutOff:
				strikeout = false
			case document.ItalicsOn:
				italics = true
			case document.ItalicsOff:
				italics = false
			}
			if !paintNormal && !paintCode {
				continue
			}
			selected := i >= blockLo && i < blockHi
			if paintNormal && token.Kind == document.ContentsLeader {
				end := int(math.Round((pos.LeftInches - p.Settings.MarginLeftInches) * p.Settings.CPI))
				if end > col {
					normal = append(normal, revealRun{dotLeader(end - col), revealBase})
					col = end
				}
			}
			if paintNormal && (pos.Text != "" || token.Kind == document.ASCII || token.Kind == document.Tab) {
				role := revealBase
				switch {
				case selected || proofHighlighted(highlighted, i):
					role = revealActive
				case strikeout:
					role = strikeoutText
				case redline:
					role = redlineText
				case underline && bold:
					role = boldUnderline
				case underline:
					role = underlined
				case bold:
					role = revealCode
				case italics:
					role = italicText
				}
				start := mergeCells + int(math.Floor((pos.LeftInches-p.Settings.MarginLeftInches)*p.Settings.CPI+1e-9))
				if start > col {
					normal = append(normal, revealRun{strings.Repeat(" ", start-col), revealBase})
					col = start
				}
				display := pos.Text
				if token.Kind == document.Tab {
					display = strings.Repeat(" ", max(0, int(math.Round(pos.WidthInches*p.Settings.CPI))))
				}
				normal = append(normal, revealRun{display, role})
				col += utf8.RuneCountInString(display)
				if token.Kind.MergeLabel(false) != "" {
					mergeCells += utf8.RuneCountInString(display)
					if row == y && i < gap {
						f.column += utf8.RuneCountInString(display)
					}
				}
			}
			if paintCode {
				var label string
				if preview != nil {
					label = preview.labels[i]
					if token.Kind == document.ASCII && pos.Text == "" {
						label = ""
					}
					if i == blockLo {
						codes = append(codes, revealRun{"[Block]", revealCode})
						codeCells += len("[Block]")
					}
				} else {
					label = labels[j].Text
				}
				role := revealCode
				if token.Kind.IsCharacter() {
					role = revealBase
				}
				if selected && preview == nil {
					role = revealActive
				}
				if preview != nil && i == preview.active || preview == nil && i == revealGap {
					role, activeCode = revealActive, codeCells
					if token.Kind == document.ExtendedCharacter {
						label = token.RevealCharacter()
						activeCodeWidth = utf8.RuneCountInString(label)
					}
					if label == "" {
						label = " "
					}
				}
				codes = append(codes, revealRun{label, role})
				codeCells += utf8.RuneCountInString(label)
			}
		}
		if paintNormal {
			left := 0
			if row == y && f.column >= width {
				left = layout.ScreenColumnOffset(f.column, width)
				f.column -= left
			}
			screen := visual[row] - top
			f.normal[screen] = renderReveal(normal, left, width)
		}
		if paintCode {
			if preview != nil && row+1 < len(p.Lines) && len(line.Tokens) != 0 {
				last := line.Tokens[len(line.Tokens)-1]
				if last.Token.Kind == document.ASCII {
					label := "[DSRt]"
					if last.Text == "" {
						label = "[SRt]"
					}
					codes = append(codes, revealRun{label, revealCode})
				}
			}
			if preview == nil && row == y && gap == d.TokenCount() {
				activeCode = codeCells
				codes = append(codes, revealRun{" ", revealActive})
			}
			f.codes[row-codeTop] = renderReveal(codes, max(0, activeCode-width+min(width, activeCodeWidth)), width)
		}
	}
	for row := max(0, normalStart); row <= normalEnd && row < len(visual); row++ {
		box := lineCommentRows(p.Lines[row], width)
		start := visual[row] - len(box) - top
		for j, line := range box {
			if screen := start + j; screen >= 0 && screen < len(f.normal) {
				f.normal[screen] = line
			}
		}
		if row > 0 && p.Lines[row].Page != p.Lines[row-1].Page {
			screen := start - 1
			if screen >= 0 && screen < len(f.normal) {
				separator := "-"
				previous := p.Lines[row-1].Tokens
				if len(previous) != 0 && previous[len(previous)-1].Token.Kind == document.HardPage {
					separator = "="
				}
				f.normal[screen] = strings.Repeat(separator, width)
			}
		}
	}
	return f, nil
}

// History preview has virtual token indices. Read the immutable overlay in
// bounded windows and project it without publishing or restoring anything.
func (m Model) paintEverydayPreview(normalRows, codeRows int) (everydayFrame, error) {
	overlay, err := m.session.Preview(0, 0)
	if err != nil {
		return everydayFrame{}, err
	}
	tokens := make([]document.Token, 0, overlay.TotalTokens)
	labels := make([]string, 0, overlay.TotalTokens)
	for start := 0; start < overlay.TotalTokens; start += document.MaxWindowTokens {
		window, err := m.session.Preview(start, min(overlay.TotalTokens-start, document.MaxWindowTokens))
		if err != nil {
			return everydayFrame{}, err
		}
		for _, entry := range window.Elements {
			tokens = append(tokens, document.Token{Kind: entry.Kind, Raw: entry.Raw, Span: entry.Span})
			labels = append(labels, previewCode(entry))
		}
	}
	settings := editor.EverydaySettings()
	settings.InitialLineSpacing, _ = m.session.Document().InitialLineSpacing()
	p := layout.Project(tokens, settings)
	visual := visualRows(p, m.width)
	line, _, ok := p.PositionAt(overlay.CursorGap)
	if !ok {
		return everydayFrame{}, fmt.Errorf("preview cursor is outside the qualified layout")
	}
	top := max(0, visual[line]-max(1, normalRows)+1)
	if screen := m.session.Snapshot().Screen; screen >= 1 && int(screen) <= len(m.everyday.top) {
		top = max(top, min(visual[line], m.everyday.top[screen-1]))
	}
	preview := &historyPreviewDisplay{labels: labels, active: -1}
	if overlay.Merge {
		for i := overlay.FragmentEnd; i < len(labels); i++ {
			if labels[i] != "" {
				preview.active = i
				break
			}
		}
	}
	return paintEveryday(nil, preview, p, visual, overlay.CursorGap, overlay.Reveal,
		overlay.FragmentStart, overlay.FragmentEnd, m.width, top, normalRows, codeRows)
}

func previewCode(entry document.OverlayElement) string {
	if label := entry.Kind.MergeLabel(true); label != "" {
		return label
	}
	switch entry.Kind {
	case document.ASCII, document.ExtendedCharacter, document.DOSControl:
		return entry.Text
	case document.HardSpace:
		return "[ ]"
	case document.BoldOn:
		return "[BOLD]"
	case document.BoldOff:
		return "[bold]"
	case document.UnderlineOn:
		return "[UND]"
	case document.UnderlineOff:
		return "[und]"
	case document.Tab:
		return "[Tab]"
	case document.HardReturn:
		return "[HRt]"
	case document.SoftReturn:
		return "[SRt]"
	case document.DeletedSoftReturn, document.DeletedSoftPage:
		return "[DSRt]"
	case document.HardPage:
		return "[HPg]"
	case document.SoftPage:
		return "[SPg]"
	case document.HardReturnSoftPage:
		return "[HRt-SPg]"
	case document.DormantHardReturn:
		return "[Dorm HRt]"
	}
	return ""
}

func everydayRuler(width int, settings layout.Settings) string {
	return tabRuler(width, settings, nil, 1200, 1200)
}

func tabRuler(width int, settings layout.Settings, rulerSet *document.TabSet, left, right int) string {
	var ruler strings.Builder
	interval, hasTabs := settings.NextTabColumn(0)
	margin := int(math.Round((settings.PageWidthInches - float64(left+right)/document.UnitsPerInch) * settings.CPI))
	stops := map[int]bool{}
	if rulerSet != nil {
		for _, pos := range rulerSet.Positions(left) {
			stops[int(math.Round(float64(pos-left)/120))] = true
		}
	}
	for i := 0; i < width; i++ {
		switch {
		case i == 0:
			ruler.WriteByte('{')
		case i == margin:
			ruler.WriteByte('}')
		case rulerSet != nil && stops[i] || rulerSet == nil && hasTabs && interval > 0 && i%interval == 0:
			ruler.WriteRune('▲')
		default:
			ruler.WriteByte(' ')
		}
	}
	return revealActive + ruler.String() + screenReset
}

func dotLeader(n int) string { return (strings.Repeat(" .", (n+1)/2))[:n] }
