package tui

import (
	"strings"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

const datePrompt = "1 Date Text; 2 Date Code; 3 Date Format; 4 Outline; 5 Para Num; 6 Define: 0"

func (m Model) datePress(key input.Key) (tea.Model, tea.Cmd) {
	if key.IsRepeat || key.Mod != 0 {
		return m, nil
	}
	if m.outlineMenu {
		switch key.Code {
		case tea.KeyF1, tea.KeyF7, tea.KeyEscape:
			m.outlineMenu, m.dateMenu = false, false
		case '1':
			next, err := m.session.StartOutline()
			if err != nil {
				m.notice = err.Error()
			} else {
				m.session, m.notice = next, ""
				m.outlineMenu, m.dateMenu = false, false
			}
		}
		return m, nil
	}
	switch key.Code {
	case '4':
		m.outlineMenu = true
	case tea.KeyF1, tea.KeyF7, tea.KeyEscape:
		m.dateMenu = false
	case '1':
		return m.insertDateText(m.runtime.now()), nil
	case '2':
		return m.insertDateCode(), nil
	}
	return m, nil
}

func (m Model) insertDateText(now time.Time) Model {
	m.closeMenus()
	m.dateMenu = false
	next, err := m.session.InsertDateText(now)
	if err != nil {
		m.notice = err.Error()
		return m
	}
	m.session, m.notice = next, ""
	return m
}

func (m Model) dateView(view tea.View) tea.View {
	lines := strings.Split(view.Content, "\n")
	status := len(lines) - 1
	prompt := datePrompt
	if m.outlineMenu {
		prompt = "Outline: 1 On; 2 Off; 3 Move Family; 4 Copy Family; 5 Delete Family: 0"
	}
	lines[status] = clip(prompt, m.width)
	view.Content = strings.Join(lines, "\n")
	view.Cursor = tea.NewCursor(min(m.width-1, len(prompt)-1), status)
	return view
}

func (m Model) insertDateCode() Model {
	m.closeMenus()
	m.dateMenu = false
	next, err := m.session.InsertDateCode()
	if err != nil {
		m.notice = err.Error()
		return m
	}
	m.session, m.notice = next, ""
	return m
}
