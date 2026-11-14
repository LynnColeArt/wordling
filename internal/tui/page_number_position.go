package tui

import (
	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

func (m Model) pageNumberPress(key input.Key) Model {
	f := &m.lineFormat
	f.error = ""
	switch key.Code {
	case tea.KeyF1, tea.KeyEscape, tea.KeyF7:
		switch f.screen {
		case formatPageNumberPosition:
			f.screen = formatPageNumbering
		case formatPageSuppressNumber:
			f.screen = formatPageSuppress
		default:
			f.screen = formatClosed
		}
		return m
	}
	var apply func() (editor.Session, error)
	target := formatPageNumbering
	switch f.screen {
	case formatPageNumbering:
		if key.Code == '4' {
			f.screen = formatPageNumberPosition
		}
	case formatPageNumberPosition:
		if key.Code == '2' || key.Code == '7' {
			apply = func() (editor.Session, error) { return m.session.SetPageNumberPosition(int(key.Code - '0')) }
		}
	case formatPageSuppress:
		if key.Code == '4' {
			f.screen = formatPageSuppressNumber
		}
	case formatPageSuppressNumber:
		if key.Code == 'y' || key.Code == 'Y' {
			apply = m.session.SuppressPageNumber
			target = formatPageSuppress
		} else if key.Code == 'n' || key.Code == 'N' || key.Code == tea.KeyEnter {
			f.screen = formatPageSuppress
		}
	}
	if apply != nil {
		next, err := apply()
		if err != nil {
			f.error = err.Error()
		} else {
			m.session, f.screen = next, target
		}
	}
	return m
}

func (m Model) pageNumberView() tea.View {
	f := m.lineFormat
	switch f.screen {
	case formatPageNumbering:
		return m.historicModalView([]string{"Format: Page Numbering", "", "     1 - New Page Number      1", "", "     2 - Page Number Style    ^B", "",
			"     3 - Insert Page Number", "", "     4 - Page Number Position " + document.PageNumberPositionName(m.session.PageNumberPosition())}, "Selection: 0", f.error)
	case formatPageNumberPosition:
		return m.historicModalView([]string{"Format: Page Number Position", "", "     2 - Top Center", "", "     7 - Bottom Right"}, "Selection: 0", f.error)
	default:
		number := "No"
		if m.session.PageNumberSuppressed() {
			number = "Yes"
		}
		prompt := "Selection: 0"
		if f.screen == formatPageSuppressNumber {
			prompt = "Suppress Page Numbering? No (Yes)"
		}
		return m.historicModalView([]string{"Format: Suppress (this page only)", "", "     4 - Suppress Page Numbering             " + number}, prompt, f.error)
	}
}
