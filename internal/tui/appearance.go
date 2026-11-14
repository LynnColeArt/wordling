package tui

import (
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

const (
	appearanceFont = iota + 1
	appearanceAttributes
)

func (m Model) appearancePress(k input.Key) (tea.Model, tea.Cmd) {
	if k.IsRepeat || k.Mod != 0 {
		return m, nil
	}
	switch k.Code {
	case tea.KeyF1, tea.KeyEscape:
		m.appearance--
		return m, nil
	case tea.KeyF7:
		m.appearance = 0
		return m, nil
	}
	if m.appearance == appearanceFont && k.Code == '2' {
		m.appearance = appearanceAttributes
		return m, nil
	}
	if m.appearance != appearanceAttributes {
		return m, nil
	}
	switch k.Code {
	case '1':
		m.appearance = 0
		return m.reduce(editor.Event{Command: editor.Bold})
	case '2':
		m.appearance = 0
		return m.reduce(editor.Event{Command: editor.Underline})
	case '4':
		return m.applyItalics(), nil
	default:
		return m, nil
	}
}

func (m Model) applyItalics() Model {
	m.closeMenus()
	m.appearance = 0
	next, err := m.session.ToggleItalics()
	m.notice = ""
	if err != nil {
		m.notice = err.Error()
	} else {
		m.session = next
	}
	return m
}

func (m Model) appearanceView(view tea.View) tea.View {
	prompt := "1 Size; 2 Appearance; 3 Normal; 4 Base Font; 5 Print Color: 0"
	if m.appearance == appearanceAttributes {
		prompt = "1 Bold 2 Undln 3 Dbl Und 4 Italc 5 Outln 6 Shadw 7 Sm Cap 8 Redln 9 Stkout: 0"
	}
	lines := strings.Split(view.Content, "\n")
	y := len(lines) - 1
	lines[y] = clip(prompt, m.width)
	view.Content = strings.Join(lines, "\n")
	view.Cursor = tea.NewCursor(min(m.width-1, len(prompt)), y)
	return view
}
