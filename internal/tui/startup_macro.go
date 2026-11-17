package tui

import (
	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
)

type startupMacroMsg struct{ name string }

// WithStartupMacro configures a one-time startup invocation. The UI dispatches
// it after opening the workspace and checking for recovery documents.
func (m Model) WithStartupMacro(name string) Model {
	m.startupMacro = name
	return m
}

func (m Model) runStartupMacro(name string) (tea.Model, tea.Cmd) {
	if name == "" || name != m.startupMacro {
		return m, nil
	}
	m.startupMacro = ""
	if len(m.recovery.entries) != 0 {
		m.notice = "Startup macro skipped while recovering documents"
		return m, nil
	}
	if !m.newMacroHostIdle() || m.session.Snapshot().Mode != editor.Editing {
		m.notice = "Startup macro requires an untouched editing screen"
		return m, nil
	}
	next, _, err := m.session.Reduce(editor.Event{Command: editor.Macro})
	if err == nil {
		next, _, err = next.Reduce(editor.Event{Command: editor.Text, Text: name})
	}
	if err != nil {
		m.notice = err.Error()
		return m, nil
	}
	m.session = next
	return m.reduce(editor.Event{Command: editor.Enter})
}
