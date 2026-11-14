package tui

import (
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

type commentUI struct {
	stage  int
	caret  int
	draft  string
	notice string
}

const (
	commentClosed = iota
	commentChoices
	commentEditor
)

func (m Model) openComment() Model {
	m.closeMenus()
	m.comment = commentUI{stage: commentChoices}
	return m
}

func (m Model) commentPress(key input.Key) (tea.Model, tea.Cmd) {
	c := &m.comment
	if key.IsRepeat || key.Mod & ^(tea.ModShift|tea.ModCapsLock) != 0 {
		return m, nil
	}
	if key.Code == tea.KeyEscape || key.Code == tea.KeyF1 {
		m.comment = commentUI{}
		return m, nil
	}
	if c.stage == commentChoices {
		switch key.Code {
		case '1':
			c.stage = commentEditor
		case tea.KeyF7:
			m.comment = commentUI{}
		}
		return m, nil
	}
	c.notice = ""
	switch key.Code {
	case tea.KeyF7:
		next, err := m.session.InsertComment(c.draft)
		if err != nil {
			c.notice = err.Error()
		} else {
			m.session, m.comment = next, commentUI{}
		}
	case tea.KeyHome:
		c.caret = 0
	case tea.KeyEnd:
		c.caret = len(c.draft)
	case tea.KeyLeft:
		c.caret = max(0, c.caret-1)
	case tea.KeyRight:
		c.caret = min(len(c.draft), c.caret+1)
	case tea.KeyBackspace:
		if c.caret > 0 {
			c.draft = c.draft[:c.caret-1] + c.draft[c.caret:]
			c.caret--
		}
	case tea.KeyDelete:
		if c.caret < len(c.draft) {
			c.draft = c.draft[:c.caret] + c.draft[c.caret+1:]
		}
	default:
		if len(c.draft)+len(key.Text) <= 1024 && strings.IndexFunc(key.Text, func(ch rune) bool { return ch < 32 || ch > 126 }) < 0 {
			c.draft = c.draft[:c.caret] + key.Text + c.draft[c.caret:]
			c.caret += len(key.Text)
		}
	}
	return m, nil
}

func commentBox(text string, width int) []string {
	if width < 5 {
		return []string{clip(text, width)}
	}
	inside := width - 4
	rows := []string{"╔" + strings.Repeat("═", width-2) + "╗"}
	for len(text) > inside {
		rows = append(rows, "║ "+text[:inside]+" ║")
		text = text[inside:]
	}
	rows = append(rows, "║ "+text+strings.Repeat(" ", inside-len(text))+" ║")
	return append(rows, "╚"+strings.Repeat("═", width-2)+"╝")
}

func (m Model) commentView() tea.View {
	c := m.comment
	if c.stage == commentChoices {
		view := m.historicView()
		lines := strings.Split(view.Content, "\n")
		lines[len(lines)-1] = clip("1 Create; 2 Edit; 3 Convert to Text: 0", m.width)
		view.Content = strings.Join(lines, "\n")
		return view
	}
	width := max(5, m.width-1)
	rows := append([]string{"Document Comment"}, commentBox(c.draft, width)...)
	view := m.historicModalView(rows, "Press Exit when done", c.notice)
	cells := max(1, width-4)
	view.Cursor = tea.NewCursor(min(m.width-1, 2+c.caret%cells), min(max(0, m.height-2), 2+c.caret/cells))
	return view
}
