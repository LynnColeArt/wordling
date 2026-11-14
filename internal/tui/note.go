package tui

import (
	"fmt"
	"math"
	"strconv"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/input"
)

type noteUI struct {
	stage          int
	end, replacing bool
	index, number  int
	caret          int
	draft, notice  string
}

const (
	noteClosed = iota
	noteMenu
	noteChoices
	noteEditor
	noteNumber
	noteOptions
	noteKeep
)

func (m Model) openNotes(stage int, end bool) Model {
	m.closeMenus()
	m.note = noteUI{stage: stage, end: end}
	if stage == noteNumber {
		m.note.number = max(1, m.session.NextNoteNumber(end)-1)
	}
	return m
}

func (m Model) notePress(key input.Key) (tea.Model, tea.Cmd) {
	note := &m.note
	if key.IsRepeat || key.Mod & ^tea.ModShift != 0 {
		return m, nil
	}
	if key.Code == tea.KeyF1 || key.Code == tea.KeyEscape {
		m.note = noteUI{}
		return m, nil
	}
	note.notice = ""
	switch note.stage {
	case noteMenu:
		if key.Code == '1' || key.Code == '2' {
			note.stage, note.end = noteChoices, key.Code == '2'
		}
	case noteChoices:
		if key.Code == '1' {
			note.stage = noteEditor
		} else if key.Code == '2' {
			note.stage = noteNumber
			note.number = max(1, m.session.NextNoteNumber(note.end)-1)
		} else if key.Code == '4' && !note.end {
			note.stage = noteOptions
		}
	case noteOptions:
		if key.Code == '2' {
			note.stage = noteKeep
		} else if key.Code == tea.KeyF7 {
			m.note = noteUI{}
		}
	case noteKeep:
		switch key.Code {
		case tea.KeyEnter:
			value := m.session.FootnoteKeep()
			if note.draft != "" {
				n, err := strconv.ParseFloat(strings.TrimSuffix(note.draft, "\""), 64)
				if err != nil || n < 0 || n > 10 {
					note.notice = "Enter a note amount from 0 to 10 inches"
					return m, nil
				}
				value = int(math.Round(n * document.UnitsPerInch))
			}
			next, err := m.session.SetFootnoteKeep(value)
			if err != nil {
				note.notice = err.Error()
			} else {
				m.session = next
				note.stage = noteOptions
				note.draft = ""
			}
		case tea.KeyBackspace:
			if n := len(note.draft); n > 0 {
				note.draft = note.draft[:n-1]
			}
		case tea.KeyF7:
			note.stage = noteOptions
			note.draft = ""
		default:
			if len(note.draft)+len(key.Text) <= 10 && strings.Trim(key.Text, "0123456789.\"") == "" {
				note.draft += key.Text
			}
		}
	case noteNumber:
		switch key.Code {
		case tea.KeyEnter:
			number := note.number
			if note.draft != "" {
				number, _ = strconv.Atoi(note.draft)
			}
			index, record, ok := m.session.FindNote(number, note.end)
			if !ok {
				note.notice = "Note number not found"
				return m, nil
			}
			note.stage, note.replacing = noteEditor, true
			note.index, note.number, note.draft = index, record.Number, record.Text
		case tea.KeyBackspace:
			if n := len(note.draft); n > 0 {
				note.draft = note.draft[:n-1]
			}
		default:
			if len(note.draft)+len(key.Text) <= 5 && strings.Trim(key.Text, "0123456789") == "" {
				note.draft += key.Text
			}
		}
	case noteEditor:
		switch key.Code {
		case tea.KeyEnter:
			if !note.end && len(note.draft) < 360 {
				note.draft = note.draft[:note.caret] + "\n" + note.draft[note.caret:]
				note.caret++
			}
		case tea.KeyHome:
			note.caret = strings.LastIndexByte(note.draft[:note.caret], '\n') + 1
		case tea.KeyEnd:
			if n := strings.IndexByte(note.draft[note.caret:], '\n'); n >= 0 {
				note.caret += n
			} else {
				note.caret = len(note.draft)
			}
		case tea.KeyLeft:
			note.caret = max(0, note.caret-1)
		case tea.KeyRight:
			note.caret = min(len(note.draft), note.caret+1)
		case tea.KeyBackspace:
			if note.caret > 0 {
				note.draft = note.draft[:note.caret-1] + note.draft[note.caret:]
				note.caret--
			}
		case tea.KeyDelete:
			if note.caret < len(note.draft) {
				note.draft = note.draft[:note.caret] + note.draft[note.caret+1:]
			}
		case tea.KeyF7:
			next, err := m.session, error(nil)
			if note.replacing {
				next, err = m.session.EditNote(note.index, note.draft)
			} else {
				next, err = m.session.CreateNote(note.draft, note.end)
			}
			if err != nil {
				note.notice = err.Error()
			} else {
				m.session, m.note = next, noteUI{}
			}
		default:
			if len(note.draft)+len(key.Text) <= 360 && strings.IndexFunc(key.Text, func(ch rune) bool {
				return ch < 32 || ch > 126
			}) == -1 {
				note.draft = note.draft[:note.caret] + key.Text + note.draft[note.caret:]
				note.caret += len(key.Text)
			}
		}
	}
	return m, nil
}

func (m Model) noteView() tea.View {
	label := "Footnote"
	if m.note.end {
		label = "Endnote"
	}
	if m.note.stage == noteOptions || m.note.stage == noteKeep {
		keep := printedInches(float64(m.session.FootnoteKeep()) / document.UnitsPerInch)
		footer := "Selection: 0"
		if m.note.stage == noteKeep {
			footer = "Selection: 2"
			if m.note.draft != "" {
				keep = m.note.draft
			}
		}
		return m.historicModalView([]string{
			"Footnote Options", "", "     1 - Spacing Within Footnotes            1",
			"                 Between Footnotes           0.167\"", "",
			"     2 - Amount of Note to Keep Together     " + keep, "",
			"     3 - Style for Number in Text            [SUPRSCPT][Note Num][suprscpt]", "",
			"     4 - Style for Number in Note                 [SUPRSCPT][Note Num][suprscpt", "",
			"     5 - Footnote Numbering Method           Numbers", "",
			"     6 - Start Footnote Numbers each Page    No", "",
			"     7 - Line Separating Text and Footnotes  2-inch Line", "",
			"     8 - Print Continued Message             No", "",
			"     9 - Footnotes at Bottom of Page         Yes",
		}, footer, m.note.notice)
	}
	if m.note.stage != noteEditor {
		prompt := "1 Footnote; 2 Endnote; 3 Endnote Placement: 0"
		if m.note.stage == noteChoices {
			prompt = label + ": 1 Create; 2 Edit; 3 New Number; 4 Options: 0"
		}
		if m.note.stage == noteNumber {
			number := m.note.draft
			if number == "" {
				number = strconv.Itoa(m.note.number)
			}
			prompt = label + " number? " + number
		}
		view := m.historicView()
		lines := strings.Split(view.Content, "\n")
		lines[len(lines)-1] = clip(prompt, m.width)
		if m.note.notice != "" && len(lines) > 1 {
			lines[len(lines)-2] = clip(m.note.notice, m.width)
		}
		view.Content = strings.Join(lines, "\n")
		view.Cursor = tea.NewCursor(min(m.width-1, len(prompt)-1), len(lines)-1)
		return view
	}
	number := fmt.Sprint(m.session.NextNoteNumber(m.note.end))
	if m.note.replacing {
		number = strconv.Itoa(m.note.number)
	}
	if m.note.end {
		number += "."
	}
	lines := strings.Split(m.note.draft, "\n")
	lines[0] = number + lines[0]
	view := m.historicModalView(lines, label+":  Press Exit when done", m.note.notice)
	before := m.note.draft[:m.note.caret]
	row := strings.Count(before, "\n")
	col := len(before) - strings.LastIndexByte(before, '\n') - 1
	if row == 0 {
		col += len(number)
	}
	view.Cursor = tea.NewCursor(min(m.width-1, col), min(max(0, m.height-2), row))
	return view
}
