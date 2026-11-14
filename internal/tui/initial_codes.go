package tui

import (
	"fmt"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

func (m Model) initialCodesPress(key input.Key) Model {
	form := &m.lineFormat
	if key.Code == tea.KeyF8 && key.Mod&tea.ModShift != 0 && form.screen == formatInitialCodes {
		form.screen = formatInitialFormat
		return m
	}
	if key.Mod&tea.ModShift != 0 {
		return m
	}
	form.error = ""
	if key.Code == tea.KeyF7 || key.Code == tea.KeyF1 || key.Code == tea.KeyEscape {
		switch form.screen {
		case formatDocument:
			m.lineFormat = lineFormatUI{}
		case formatInitialCodes:
			if key.Code == tea.KeyF7 {
				form.screen = formatDocument
			}
		case formatInitialFormat, formatInitialLine:
			form.screen = formatInitialCodes
		case formatInitialSpacing:
			form.screen = formatInitialLine
			form.spacing, _ = m.session.Document().InitialLineSpacing()
		}
		return m
	}
	switch form.screen {
	case formatDocument:
		if key.Code == '2' {
			spacing, present := m.session.Document().InitialLineSpacing()
			if present && spacing == 0 {
				form.error = "These Initial Codes are outside the supported format"
			} else {
				form.screen, form.spacing = formatInitialCodes, spacing
			}
		}
	case formatInitialFormat:
		if key.Code == '1' {
			form.screen = formatInitialLine
		}
	case formatInitialLine:
		if key.Code == '6' {
			form.screen = formatInitialSpacing
		}
	case formatInitialSpacing:
		switch key.Code {
		case '1', '2':
			form.spacing = int(key.Code - '0')
		case tea.KeyEnter:
			next, err := m.session.SetInitialLineSpacing(form.spacing)
			if err != nil {
				form.error = err.Error()
				return m
			}
			m.session = next
			form.screen = formatInitialLine
		}
	}
	return m
}

func (m Model) initialCodesView() tea.View {
	switch m.lineFormat.screen {
	case formatDocument:
		return m.historicModalView([]string{"Format: Document", "",
			"     1 - Display Pitch - Automatic Yes", "                         Width     0.1\"", "",
			"     2 - Initial Codes", "", "     3 - Initial Base Font         Courier 10cpi", "",
			"     4 - Redline Method            Printer Dependent", "", "     5 - Summary"},
			"Selection: 0", m.lineFormat.error)
	case formatInitialFormat:
		return m.historicModalView([]string{"Format: 1 Line; 2 Page; 3 Document; 4 Other"}, "Selection: 0", "")
	default:
		row := max(0, m.height/2-1)
		body := make([]string, row)
		body = append(body, "Initial Codes:  Press Exit when done                           Ln 1\" Pos 1\"",
			"{    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    }")
		if spacing, present := m.session.Document().InitialLineSpacing(); present {
			body = append(body, fmt.Sprintf("[Ln Spacing:%d]", spacing))
		}
		view := m.historicModalView(body, "", m.lineFormat.error)
		view.Cursor = tea.NewCursor(0, min(m.height-1, row+2))
		return view
	}
}
