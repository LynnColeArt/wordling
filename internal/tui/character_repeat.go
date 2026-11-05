package tui

import (
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

// Value state carries observations, never a document or a reusable authority.
type characterRepeat struct {
	active          bool
	count           uint8
	native, genesis document.Revision
	revision        uint64
	screen          uint8
	gap             int
}

func (m Model) characterContext() bool {
	if m.runtime == nil || m.width != 80 || m.height != 25 || m.repeatEntry || m.notice != "" || m.reconcile != "" || m.menu.shown || m.menu.diagnostic != "" || len(m.unsettled) != 0 || m.firstPending != nil || m.macro != nil || m.macroTicket != nil || m.macroCPU || m.macroDeferred != nil || m.macroFrozen != nil || m.macroStatus != (MacroStatus{}) {
		return false
	}
	s := m.session.Snapshot()
	d := m.session.Document()
	if d == nil || !d.Birth().IsNew() || m.session.Source() != nil || d.TokenCount() != 0 || s.GenesisRevision == (document.Revision{}) || s.GenesisRevision != s.NativeRevision || s.Revision != 1 || s.Gap != 0 || s.Provenance != 0 || s.HomePrefix != 0 || !s.HistoryQualified || !s.HistoryCountKnown || s.HistoryCount != 0 {
		return false
	}
	if s.Screen != 1 || s.Mode != editor.Editing || s.NewPhase != editor.NewUnpublished || s.Typeover || s.Reveal || s.Selection || s.MacroRun != 0 || s.MacroRepeat != 1 {
		return false
	}
	if s.Pending != nil || s.Name != "" || s.Draft != "" || s.OriginalName != "" || s.Prompt != "" || s.Notice != "" || s.PublishedName != "" || s.SaveState != editor.NotSaved || s.PublishedRevision != (document.Revision{}) || s.SavedRevision != (document.Revision{}) || s.FirstPublication != (editor.Receipt{}) || s.Published != (editor.Receipt{}) || s.Last != (editor.Receipt{}) || s.Detached != (editor.Receipt{}) {
		return false
	}
	p := m.characterRepeat
	if p.active && (p.native != s.NativeRevision || p.genesis != s.GenesisRevision || p.revision != s.Revision || p.screen != s.Screen || p.gap != s.Gap) {
		return false
	}
	m.runtime.mu.Lock()
	defer m.runtime.mu.Unlock()
	return !m.runtime.stopping && m.uiAuthority != nil && m.uiAuthority == m.runtime.uiAuthority && m.runtime.macro == nil && m.runtime.issued == 0 && len(m.runtime.results) == 0 && len(m.runtime.executed) == 0 && len(m.runtime.firstTickets) == 0 && len(m.runtime.macroResults) == 0
}

func bareCharacterCommand(k input.Key, code rune) bool {
	return k.Code == code && k.Mod == 0 && k.Text == "" && !k.IsRepeat
}

func (m Model) beginCharacterRepeat(k input.Key) (Model, bool) {
	if !bareCharacterCommand(k, tea.KeyEscape) || !m.characterContext() {
		return m, false
	}
	s := m.session.Snapshot()
	m.characterRepeat = characterRepeat{active: true, native: s.NativeRevision, genesis: s.GenesisRevision, revision: s.Revision, screen: s.Screen, gap: s.Gap}
	return m, true
}

func (m Model) characterPress(k input.Key) (tea.Model, tea.Cmd) {
	valid := m.characterContext()
	p := m.characterRepeat
	m.characterRepeat = characterRepeat{}
	if !valid {
		m.notice = "Character Repeat context unavailable (host policy)"
		return m, nil
	}
	if bareCharacterCommand(k, tea.KeyEscape) || bareCharacterCommand(k, tea.KeyF1) {
		m.notice = "Character Repeat cancelled (host policy)"
		return m, nil
	}
	if !k.IsRepeat && k.Mod&^(tea.ModShift|tea.ModCapsLock) == 0 && len(k.Text) == 1 && k.Code >= 0x21 && k.Code <= 0x7e {
		c := k.Text[0]
		if p.count == 0 && c >= '1' && c <= '9' {
			p.count = c - '0'
			m.characterRepeat = p
			return m, nil
		}
		if p.count >= 1 && p.count <= 9 && c >= 0x21 && c <= 0x7e && (c < '0' || c > '9') {
			d := m.session.Document()
			total := d.TokenCount()
			native, err := d.Export()
			if err == nil && total == 0 && total <= document.MaxMutationTokens && int(p.count) <= document.MaxMutationTokens-total && int(p.count) <= document.MaxMutationBytes && len(native) <= document.MaxMutationBytes-int(p.count) {
				return m.reduce(editor.Event{Command: editor.Text, Text: characterPayload(c, p.count)})
			}
		}
	}
	m.notice = "Unsupported character Repeat input (host policy)"
	return m, nil
}

// Called only after grammar, owner and downstream capacity checks.
func characterPayload(c byte, count uint8) string {
	return strings.Repeat(string([]byte{c}), int(count))
}

func (m *Model) invalidateCharacterMessage(msg tea.Msg) {
	if !m.characterRepeat.active {
		return
	}
	switch msg.(type) {
	case tea.EnvMsg, tea.ColorProfileMsg:
		return
	}
	switch input.Translate(msg).Kind {
	case input.Press, input.Release, input.KeyboardCapabilities, input.Capability, input.TerminalVersion:
		return
	}
	m.characterRepeat = characterRepeat{}
}
