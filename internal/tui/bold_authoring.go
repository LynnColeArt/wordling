package tui

import (
	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

// boldKey runs after the existing count, menu and macro dispatch. An F6 with
// associated text still belongs here so resolve cannot reinterpret it as Text.
func (m Model) boldKey(k input.Key) (tea.Model, tea.Cmd, bool) {
	if k.Code != tea.KeyF6 {
		return m, nil, false
	}
	if k.Mod != 0 || k.Text != "" || k.IsRepeat {
		m.notice = "Bold requires an ordinary bare F6 press"
		return m, nil, true
	}
	if !m.boldHostIdle() {
		m.notice = "Bold requires the current idle application context"
		return m, nil, true
	}
	next, cmd := m.reduce(editor.Event{Command: editor.Bold})
	return next, cmd, true
}

func (m Model) boldHostIdle() bool {
	if m.runtime == nil || m.characterRepeat.active || m.repeatEntry || m.menu.shown ||
		m.reconcile != "" || len(m.unsettled) != 0 || m.firstPending != nil ||
		m.macro != nil || m.macroTicket != nil || m.macroCPU || m.macroDeferred != nil ||
		m.macroFrozen != nil || m.macroStatus != (MacroStatus{}) {
		return false
	}
	// Host diagnostics are observations. Actual owner, receipts and G's
	// session admission decide whether a subsequent legitimate F6 can run.
	r := m.runtime
	r.mu.Lock()
	defer r.mu.Unlock()
	return !r.stopping && m.uiAuthority != nil && m.uiAuthority == r.uiAuthority &&
		r.macro == nil && r.issued == 0 && len(r.results) == 0 && len(r.executed) == 0 &&
		len(r.firstTickets) == 0 && len(r.macroResults) == 0
}
