package tui

import (
	"math"
	"strconv"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/input"
)

func (m Model) advancePress(key input.Key) Model {
	form := &m.lineFormat
	form.error = ""
	switch key.Code {
	case tea.KeyF7, tea.KeyF1, tea.KeyEscape:
		if form.screen == formatAdvanceValue {
			form.screen = formatAdvance
		} else {
			form.screen = formatOther
		}
		return m
	}
	if form.screen == formatAdvance {
		switch key.Code {
		case '2':
			form.advanceMode = document.AdvanceDown
		case '5':
			form.advanceMode = document.AdvanceRight
		case '6':
			form.advanceMode = document.AdvancePosition
		case '1', '3', '4':
			form.error = "This Advance option is unavailable"
			return m
		default:
			return m
		}
		form.screen, form.draft = formatAdvanceValue, ""
		return m
	}
	switch key.Code {
	case tea.KeyEnter:
		inches, err := strconv.ParseFloat(strings.TrimSuffix(form.draft, "\""), 64)
		units := math.Round(inches * document.UnitsPerInch)
		if err != nil || math.IsNaN(units) || units < 0 || units > 65535 {
			form.error = "Enter a valid distance in inches"
			return m
		}
		next, err := m.session.InsertAdvance(form.advanceMode, int(units))
		if err != nil {
			form.error = err.Error()
			return m
		}
		m.session = next
		form.screen = formatOther
	case tea.KeyBackspace:
		if len(form.draft) > 0 {
			form.draft = form.draft[:len(form.draft)-1]
		}
	default:
		if len(form.draft)+len(key.Text) <= 12 && strings.Trim(key.Text, "0123456789.\"") == "" {
			form.draft += key.Text
		}
	}
	return m
}

func (m Model) advanceView() tea.View {
	form := m.lineFormat
	menu := "Advance: 1 Up; 2 Down; 3 Line; 4 Left; 5 Right; 6 Position"
	if form.screen == formatAdvance {
		return m.historicModalView([]string{"Format: Other"}, menu+": 0", form.error)
	}
	label := "Position"
	if form.advanceMode == document.AdvanceRight {
		label = "Right"
	} else if form.advanceMode == document.AdvanceDown {
		label = "Down"
	}
	return m.historicModalView([]string{"Format: Other", "", menu}, "Advance "+label+": "+form.draft, form.error)
}
