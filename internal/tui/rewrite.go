package tui

import (
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

type lineDrawUI struct {
	stage, start, steps int
}

const screenPrompt = "1 Window; 2 Line Draw; 3 Rewrite: 3"

func (m Model) screenPress(key input.Key) (tea.Model, tea.Cmd) {
	if key.IsRepeat || key.Mod != 0 {
		return m, nil
	}
	if m.lineDraw.stage != 0 {
		return m.drawLinePress(key)
	}
	switch key.Code {
	case '2':
		m.lineDraw.stage = 1
	case tea.KeyF1, tea.KeyEscape, tea.KeyF7:
		m.screenMenu = false
	case '3', tea.KeyEnter:
		m.screenMenu = false
		m.notice = ""
		m.everyday.ready = false
		m.prepareEverydayViewport()
	}
	return m, nil
}

func (m Model) screenView(view tea.View) tea.View {
	lines := strings.Split(view.Content, "\n")
	row := len(lines) - 1
	prompt := screenPrompt
	if m.lineDraw.stage != 0 {
		prompt = "1 │; 2 ║; 3 *; 4 Change; 5 Erase; 6 Move: 1"
		if m.lineDraw.stage == 3 {
			prompt = "1 │; 2 ║; 3 *; 4 Change; 5 Erase; 6 Move: 2"
		}
	}
	if m.lineDraw.stage != 0 && m.notice != "" && row > 0 {
		lines[row-1] = clip(m.notice, m.width)
	}
	lines[row] = clip(prompt, m.width)
	view.Content = strings.Join(lines, "\n")
	view.Cursor = tea.NewCursor(min(m.width-1, len(prompt)-1), row)
	return view
}

func (m Model) drawLinePress(key input.Key) (tea.Model, tea.Cmd) {
	switch key.Code {
	case tea.KeyF1, tea.KeyF7, tea.KeyEscape:
		m.lineDraw, m.screenMenu, m.notice = lineDrawUI{}, false, ""
		return m, nil
	}
	if m.lineDraw.stage == 1 {
		if key.Code == '1' || key.Code == '2' {
			m.lineDraw.stage = 2
			if key.Code == '2' {
				m.lineDraw.stage = 3
			}
			m.lineDraw.start = m.session.Snapshot().Gap
			m.notice = ""
		}
		return m, nil
	}
	if key.Code != tea.KeyRight {
		return m, nil
	}
	next, err := m.session.ExtendHorizontalDrawing(m.lineDraw.start, m.lineDraw.steps+1, m.lineDraw.stage == 3)
	if err != nil {
		m.notice = err.Error()
	} else {
		m.session, m.notice = next, ""
		m.lineDraw.steps++
	}
	return m, nil
}
