package tui

import (
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

// MenuBar is copied HOST display diagnostic data, never command or native authority.
type MenuBar struct {
	Visible, Available bool
	Reason             string
}
type menuDisplay struct {
	shown      bool
	diagnostic string
}

const menuUnsupported = "Menu bar display only; Alt+= hides; action unsupported"

func menuKey(k input.Key) bool {
	return k.Code == '=' && k.Mod == tea.ModAlt && !k.IsRepeat && (k.Text == "" || k.Text == "=")
}

// Availability observes the real constructor genesis and existing IO/UI owners.
// It never claims a token, creates a document or changes reducer history.
func (m Model) menuReason() string {
	if m.runtime == nil {
		return "Menu bar unavailable: uninitialized runtime"
	}
	if m.width != 80 || m.height != 25 {
		return "Menu bar unavailable: requires 80x25"
	}
	if m.macro != nil || m.macroTicket != nil || m.macroCPU || m.macroDeferred != nil || m.macroFrozen != nil || m.macroStatus.Active || m.macroStatus.WorkerPending || m.macroStatus.DisplaySuppressed {
		return "Menu bar unavailable: macro display or work"
	}
	if len(m.unsettled) != 0 || m.firstPending != nil {
		return "Menu bar unavailable: pending IO"
	}
	m.runtime.mu.Lock()
	idle := !m.runtime.stopping && m.uiAuthority != nil && m.runtime.uiAuthority == m.uiAuthority && m.runtime.macro == nil && m.runtime.issued == 0 && len(m.runtime.results) == 0 && len(m.runtime.firstTickets) == 0
	m.runtime.mu.Unlock()
	if !idle {
		return "Menu bar unavailable: stale, closed or busy runtime"
	}
	s := m.session.Snapshot()
	d := m.session.Document()
	if d == nil || m.session.Source() != nil || d.TokenCount() != 0 || s.GenesisRevision == (document.Revision{}) || s.GenesisRevision != s.NativeRevision || s.Revision != 1 || s.Gap != 0 || s.Provenance != 0 {
		return "Menu bar unavailable: requires pristine startup document"
	}
	if s.Screen != 1 || s.Mode != editor.Editing || s.NewPhase != editor.NewUnpublished || s.Typeover || s.Reveal || s.Selection || s.MacroRun != 0 || s.MacroRepeat != 1 || m.repeatEntry {
		return "Menu bar unavailable: requires idle Doc1 Insert"
	}
	if s.Pending != nil || s.Name != "" || s.Draft != "" || s.OriginalName != "" || s.Prompt != "" || s.Notice != "" || m.notice != "" || m.reconcile != "" || s.PublishedName != "" || s.SaveState != editor.NotSaved || s.PublishedRevision != (document.Revision{}) || s.SavedRevision != (document.Revision{}) || s.FirstPublication != (editor.Receipt{}) || s.Published != (editor.Receipt{}) || s.Last != (editor.Receipt{}) || s.Detached != (editor.Receipt{}) {
		return "Menu bar unavailable: application state"
	}
	return ""
}
func (m Model) menuState() MenuBar {
	reason := m.menuReason()
	return MenuBar{Visible: m.menu.shown && reason == "", Available: reason == "", Reason: reason}
}
func (m *Model) invalidateMenu() {
	if m.menu.shown && m.menuReason() != "" {
		m.menu = menuDisplay{}
	}
}
func (m Model) menuPress(k input.Key) (Model, bool) {
	state := m.menuState()
	if state.Visible {
		if menuKey(k) {
			m.menu = menuDisplay{}
		} else {
			m.menu.diagnostic = menuUnsupported
		}
		return m, true
	}
	if menuKey(k) {
		if state.Available {
			m.menu = menuDisplay{shown: true}
		} else {
			m.menu = menuDisplay{diagnostic: state.Reason}
		}
		return m, true
	}
	return m, false
}
func (m Model) menuPrompt(s editor.Snapshot, prompt string) string {
	if m.menu.diagnostic == "" || s.Mode != editor.Editing || s.Reveal || prompt != "" || s.Notice != "" || m.notice != "" || m.reconcile != "" || m.repeatEntry || m.macroFrozen != nil || m.macroStatus.DisplaySuppressed {
		return prompt
	}
	return m.menu.diagnostic
}
func renderMenuBar() string {
	text := "File Edit Search Layout Mark Tools Font Graphics Help        (Press F3 for Help)"
	var out strings.Builder
	previous := 0
	for i, c := range text {
		role := 0x71
		if i < 4 {
			role = 0x47
		}
		switch i {
		case 5, 10, 17, 24, 29, 36, 40, 49:
			role = 0x74
		}
		if role != previous {
			switch role {
			case 0x47:
				out.WriteString("\x1b[22;37;41m")
			case 0x74:
				out.WriteString("\x1b[22;31;47m")
			case 0x71:
				out.WriteString("\x1b[22;34;47m")
			}
			previous = role
		}
		out.WriteRune(c)
	}
	out.WriteString("\x1b[0m")
	return out.String()
}
