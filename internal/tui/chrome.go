package tui

import (
	"fmt"
	"image/color"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

type toolbarAction struct {
	label string
	key   input.Key
}

var toolbarActions = [...]toolbarAction{
	{" Shift+F10 Open ", input.Key{Code: tea.KeyF10, Mod: tea.ModShift}},
	{" F10 Save ", input.Key{Code: tea.KeyF10}},
	{" F6 Bold ", input.Key{Code: tea.KeyF6}},
	{" Alt+F3 Reveal Codes ", input.Key{Code: tea.KeyF3, Mod: tea.ModAlt}},
	{" F7 Exit ", input.Key{Code: tea.KeyF7}},
}

var exitSaveActions = [...]toolbarAction{
	{" Skip Save (N) ", input.Key{Code: 'n', Text: "n"}},
	{" Return (F1) ", input.Key{Code: tea.KeyF1}},
}
var exitConfirmActions = [...]toolbarAction{
	{" Exit (Y) ", input.Key{Code: 'y', Text: "y"}},
	{" Return (F1) ", input.Key{Code: tea.KeyF1}},
}

func actionsForMode(mode editor.Mode) []toolbarAction {
	switch mode {
	case editor.ExitSaveQuestion:
		return exitSaveActions[:]
	case editor.ExitQuestion:
		return exitConfirmActions[:]
	default:
		return toolbarActions[:]
	}
}

func (m Model) showEditorChrome() bool {
	return m.runtime != nil && m.runtime.editorChrome && m.height >= 12
}

func (m Model) documentRows(reveal bool) int {
	if m.showEditorChrome() {
		rows := m.height - 1
		if reveal {
			rows = m.height/2 - 1
		}
		if m.historic.bar {
			rows--
		}
		return max(1, rows)
	}
	return max(1, m.height-9)
}

func (m Model) toolbarKey(mouse *tea.Mouse) (input.Key, bool) {
	if mouse == nil || mouse.Button != tea.MouseLeft || mouse.Y != m.height-1 {
		return input.Key{}, false
	}
	x := 0
	for _, action := range actionsForMode(m.session.Snapshot().Mode) {
		end := x + len(action.label)
		if mouse.X >= x && mouse.X < end && end <= m.width {
			return action.key, true
		}
		x = end + 1
	}
	return input.Key{}, false
}

func (m Model) editorChromeLines(lines, reveal []string, s editor.Snapshot) []string {
	const bar = "\x1b[1;30;46m"
	const reset = "\x1b[0m"
	if !m.menuState().Visible {
		lines[0] = bar + " Wordling 5.2 " + reset
	}
	bodyHeight := m.height - 2
	if len(reveal) != 0 {
		bodyHeight = m.height / 2
	}
	lines = lines[:min(len(lines), bodyHeight)]
	for len(lines) < bodyHeight {
		lines = append(lines, "")
	}
	if len(reveal) != 0 {
		const divider = "\x1b[1;37;41m"
		lines = append(lines, divider+" Reveal Codes "+strings.Repeat(" ", max(0, m.width-14))+reset, reveal[1])
		for len(lines) < m.height-3 {
			lines = append(lines, "")
		}
		lines = append(lines, "Alt+F3 restores the full document view")
	}
	name := s.Name
	if name == "" {
		name = "Untitled"
	}
	if s.Dirty {
		name += " *"
	}
	mode := string(s.Mode)
	if s.Mode == editor.Editing {
		mode = "Insert"
		if s.Typeover {
			mode = "Typeover"
		}
	}
	status := fmt.Sprintf(" %s  |  Doc %d  |  %s", name, s.Screen, mode)
	if m.runtime.controlKeys {
		status += "  |  Ctrl+O Open  Ctrl+S Save  Ctrl+Q Exit"
	}
	var buttons []string
	for _, action := range actionsForMode(s.Mode) {
		buttons = append(buttons, bar+action.label+reset)
	}
	return append(lines, status, strings.Join(buttons, " "))
}

func applyEditorChrome(v *tea.View) {
	v.BackgroundColor = color.RGBA{R: 0, G: 0, B: 170, A: 255}
	v.ForegroundColor = color.RGBA{R: 238, G: 245, B: 255, A: 255}
	v.MouseMode = tea.MouseModeCellMotion
}
