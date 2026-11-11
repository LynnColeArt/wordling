package tui

import (
	"fmt"
	"math"
	"sort"
	"strings"

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
	revision   document.Revision
	layout     layout.Layout
	ready      bool
	visualRows []int
	top        [2]int
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
		p, err := layout.FromDocument(d, editor.EverydaySettings())
		v.revision, v.layout, v.ready = s.NativeRevision, p, err == nil
		v.visualRows = visualRows(p)
	}
	if !v.ready || s.Screen < 1 || s.Screen > 2 {
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
	if !v.ready || s.Screen < 1 || s.Screen > 2 {
		return
	}
	line, _, ok := v.layout.PositionAt(s.Gap)
	if ok && line >= 0 && line < len(v.visualRows) {
		v.top[s.Screen-1] = v.visualRows[line]
	}
}

// The dashed page separator is an upper-pane screen row. It is never a
// physical document line or a native owner.
func visualRows(p layout.Layout) []int {
	rows := make([]int, len(p.Lines))
	row := 0
	for i, line := range p.Lines {
		if i > 0 && p.Lines[i-1].Page != line.Page {
			row++
		}
		rows[i] = row
		row++
	}
	return rows
}

const (
	underlined    = "\x1b[22;34;47m" // Original 0x71.
	boldUnderline = "\x1b[22;97;47m" // Original 0x7F.
)

func projectEveryday(d *document.Document, gap, width, rows int) (everydayFrame, error) {
	p, err := layout.FromDocument(d, editor.EverydaySettings())
	if err != nil {
		return everydayFrame{}, err
	}
	return paintEveryday(d, nil, p, visualRows(p), gap, false, -1, -1, width, 0, rows, 0)
}

func paintEveryday(d *document.Document, preview []string, p layout.Layout, visual []int, gap int, reveal bool, blockStart, blockEnd, width, top, normalRows, codeRows int) (everydayFrame, error) {
	y, x, ok := p.PositionAt(gap)
	if !ok || y < 0 || y >= len(visual) {
		return everydayFrame{}, fmt.Errorf("cursor is outside the qualified layout")
	}
	f := everydayFrame{row: visual[y] - top, column: x, normal: make([]string, normalRows)}
	// The original lower pane centers the active line at its fourth row
	// once possible, independently of the upper viewport's scroll.
	codeTop := 0
	codeEnd := 0
	if reveal && codeRows > 0 {
		codeTop = max(0, y-min(3, codeRows-1))
		codeEnd = min(len(p.Lines), codeTop+codeRows)
		f.codes = make([]string, codeEnd-codeTop)
	}
	normalStart := sort.SearchInts(visual, top)
	normalEnd := sort.SearchInts(visual, top+normalRows)
	blockLo, blockHi := min(blockStart, blockEnd), max(blockStart, blockEnd)
	bold, underline := false, false
	for row, line := range p.Lines[:max(normalEnd, codeEnd)] {
		paintNormal := row >= normalStart && row < normalEnd
		paintCode := codeEnd > 0 && row >= codeTop && row < codeEnd
		var normal, codes []revealRun
		col, codeCells, activeCode := 0, 0, -1
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
			}
			if !paintNormal && !paintCode {
				continue
			}
			selected := i >= blockLo && i < blockHi
			if paintNormal && (token.Kind == document.ASCII || token.Kind == document.Tab) {
				role := revealBase
				switch {
				case selected:
					role = revealActive
				case underline && bold:
					role = boldUnderline
				case underline:
					role = underlined
				case bold:
					role = revealCode
				}
				start := int(math.Round((pos.LeftInches - p.Settings.MarginLeftInches) * p.Settings.CPI))
				if start > col {
					normal = append(normal, revealRun{strings.Repeat(" ", start-col), revealBase})
					col = start
				}
				display := pos.Text
				if token.Kind == document.Tab {
					display = strings.Repeat(" ", max(0, int(math.Round(pos.WidthInches*p.Settings.CPI))))
				}
				normal = append(normal, revealRun{display, role})
				col += len(display)
			}
			if paintCode {
				var label string
				if preview != nil {
					label = preview[i]
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
				if token.Kind == document.ASCII {
					role = revealBase
				}
				if selected && preview == nil {
					role = revealActive
				}
				if i == gap && preview == nil {
					role, activeCode = revealActive, codeCells
					if label == "" {
						label = " "
					}
				}
				codes = append(codes, revealRun{label, role})
				codeCells += len(label)
			}
		}
		if paintNormal {
			left := 0
			if row == y && x >= width {
				left = x - width + 1
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
			f.codes[row-codeTop] = renderReveal(codes, max(0, activeCode-width+1), width)
		}
	}
	for row := max(1, normalStart); row < min(len(visual), normalEnd+1); row++ {
		if visual[row]-visual[row-1] > 1 {
			screen := visual[row] - top - 1
			if screen >= 0 && screen < len(f.normal) {
				f.normal[screen] = strings.Repeat("-", width)
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
	p := layout.Project(tokens, editor.EverydaySettings())
	visual := visualRows(p)
	line, _, ok := p.PositionAt(overlay.CursorGap)
	if !ok {
		return everydayFrame{}, fmt.Errorf("preview cursor is outside the qualified layout")
	}
	top := max(0, visual[line]-max(1, normalRows)+1)
	if screen := m.session.Snapshot().Screen; screen >= 1 && int(screen) <= len(m.everyday.top) {
		top = max(top, min(visual[line], m.everyday.top[screen-1]))
	}
	return paintEveryday(nil, labels, p, visual, overlay.CursorGap, overlay.Reveal,
		overlay.FragmentStart, overlay.FragmentEnd, m.width, top, normalRows, codeRows)
}

func previewCode(entry document.OverlayElement) string {
	switch entry.Kind {
	case document.ASCII:
		return string(entry.Raw)
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
	var ruler strings.Builder
	interval, hasTabs := settings.NextTabColumn(0)
	margin := int(math.Round((settings.PageWidthInches - settings.MarginLeftInches - settings.MarginRightInches) * settings.CPI))
	for i := 0; i < width; i++ {
		switch {
		case i == 0:
			ruler.WriteByte('{')
		case i == margin:
			ruler.WriteByte('}')
		case hasTabs && interval > 0 && i%interval == 0:
			ruler.WriteRune('▲')
		default:
			ruler.WriteByte(' ')
		}
	}
	return revealActive + ruler.String() + screenReset
}
