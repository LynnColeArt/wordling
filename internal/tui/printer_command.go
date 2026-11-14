package tui

import (
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

func (m Model) printerFunctionsPress(key input.Key) Model {
	form := &m.lineFormat
	switch key.Code {
	case tea.KeyEscape, tea.KeyF1:
		if form.screen == formatPrinterFunctions {
			return m.openLineFormat(formatOther)
		}
		form.screen, form.draft, form.error = formatPrinterFunctions, "", ""
		return m
	case tea.KeyF7:
		if form.screen == formatPrinterLiteral && form.draft != "" {
			// The original filename editor can be left without committing.
			return m.openLineFormat(formatOther)
		}
		m.lineFormat = lineFormatUI{}
		return m
	}
	switch form.screen {
	case formatPrinterFunctions:
		if key.Code == '1' {
			form.screen = formatKerning
		} else if key.Code == '2' {
			form.screen = formatPrinterCommand
		}
	case formatKerning:
		if key.Code == 'y' || key.Code == 'Y' || key.Code == 'n' || key.Code == 'N' || key.Code == tea.KeyEnter {
			enabled := key.Code == 'y' || key.Code == 'Y' || key.Code == tea.KeyEnter && m.session.Kerning()
			next, err := m.session.SetKerning(enabled)
			if err != nil {
				form.error = err.Error()
			} else {
				m.session = next
				form.screen, form.error = formatPrinterFunctions, ""
			}
		}
	case formatPrinterCommand:
		if key.Code == '1' {
			form.screen = formatPrinterLiteral
		}
	case formatPrinterLiteral:
		switch key.Code {
		case tea.KeyBackspace:
			if len(form.draft) != 0 {
				form.draft = form.draft[:len(form.draft)-1]
			}
		case tea.KeyEnter:
			next, err := m.session.InsertPrinterCommand(form.draft)
			if err != nil {
				form.error = err.Error()
			} else {
				m.session = next
				form.screen, form.draft, form.error = formatPrinterFunctions, "", ""
			}
		default:
			if len(form.draft)+len(key.Text) <= 1275 && strings.IndexFunc(key.Text, func(r rune) bool { return r < 32 || r > 126 }) < 0 {
				form.draft += key.Text
			}
		}
	}
	return m
}

func (m Model) printerFunctionsView() tea.View {
	form, footer := m.lineFormat, "Selection: 0"
	if form.screen == formatPrinterCommand {
		footer = "Printer Command: 1 Command; 2 Filename: 0"
	} else if form.screen == formatPrinterLiteral {
		footer = "Command: " + form.draft
	}
	kerning := "No"
	if m.session.Kerning() {
		kerning = "Yes"
	}
	if form.screen == formatKerning {
		footer = "Selection: 1"
		if kerning == "No" {
			kerning += " (Yes)"
		} else {
			kerning += " (No)"
		}
	}
	return m.historicModalView([]string{"Format: Printer Functions", "", "     1 - Kerning                                  " + kerning, "",
		"     2 - Printer Command", "", "     3 - Word Spacing                             Optimal", "         Letter Spacing                           Optimal", "",
		"     4 - Word Spacing Justification Limits", "", "     5 - Baseline Placement for Typesetters       No", "", "     6 - Leading Adjustment"}, footer, form.error)
}
