package tui

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
	"github.com/lynncoleart/wordling/internal/storage"
)

// CancelPendingMsg is an explicit host operation, never an original key alias.
// Disk IO continues; commands are held until the late receipt is reconciled.
type CancelPendingMsg struct{}
type operation struct {
	id, revision uint64
	kind         editor.IntentKind
}
type Model struct {
	runtime           *Runtime
	session           editor.Session
	width, height     int
	notice, reconcile string
	unsettled         []operation
	macro             *macroFlow
	macroTicket       *macroTicket
	macroCPU          bool
	macroStatus       MacroStatus
	macroFrozen       *macroPane
	repeatEntry       bool
	uiAuthority       *uiTransition
	macroDeferred     *macroIOReceipt
}
type State struct {
	Session                   editor.Snapshot
	Width, Height             int
	Notice, Reconciliation    string
	PendingIO                 int
	PhysicalDeliveryQualified bool
	Macro                     MacroStatus
	Profile                   string
}

func (m Model) State() State {
	profile := ""
	if m.runtime != nil {
		profile = m.runtime.profile
	}
	return State{Profile: profile, Session: m.session.Snapshot(), Width: m.width, Height: m.height, Notice: m.notice, Reconciliation: m.reconcile, PendingIO: len(m.unsettled), Macro: m.macroStatus}
}

// Session returns an immutable value for measurements/inspection. Never fork it
// to execute independent intents: this Model owns the sole authoritative chain.
func (m Model) Session() editor.Session { return m.session }
func (m Model) Init() tea.Cmd           { return nil }
func (m Model) reduce(event editor.Event) (tea.Model, tea.Cmd) {
	previousMode := m.session.Snapshot().Mode
	next, intent, err := m.session.Reduce(event)
	m.session = next
	if err == nil && next.Snapshot().Mode == editor.MacroName && previousMode != editor.MacroName {
		m.macroStatus = MacroStatus{}
		m.macroFrozen = nil
	}
	m.notice = ""
	if err != nil {
		m.notice = err.Error()
	}
	if intent != nil {
		m.unsettled = append(append([]operation(nil), m.unsettled...), operation{intent.Operation, intent.Revision, intent.Kind})
		return m, m.runtime.command(*intent)
	}
	if next.Snapshot().Mode == editor.Exited {
		return m, tea.Quit
	}
	return m, nil
}
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	if m.runtime == nil {
		m.notice = "Uninitialized host runtime"
		return m, nil
	}
	token, valid := m.runtime.claimUI(m.uiAuthority)
	if !valid {
		m.notice = "Stale UI transition refused; authentic model retains authority"
		return m, nil
	}
	m.uiAuthority = token
	return m.update(msg)
}
func (m Model) update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch v := msg.(type) {
	case macroIOReply:
		return m.macroIO(v.receipt)
	case macroReply:
		return m.macroReply(v)
	case macroDuplicateMsg:
		m.notice = "Duplicate macro dispatch refused; authentic continuation retained"
		return m, nil
	case macroReadRefusedMsg:
		return m.macroReadRefused(v)
	case HostStopMacroMsg:
		return m.hostStopMacro(v.Reason)
	}
	if _, ok := msg.(duplicateDispatchMsg); ok {
		m.notice = "Duplicate IO dispatch refused; no additional operation executed"
		return m, nil
	}
	if reply, ok := msg.(resultMsg); ok {
		result := reply.result
		if result.Kind == editor.ReadMacro {
			m.notice = "Unbound macro IO payload refused; authentic receipt retained"
			return m, nil
		}
		remaining := make([]operation, 0, len(m.unsettled))

		for _, op := range m.unsettled {
			if op == (operation{result.Operation, result.Revision, result.Kind}) {

			} else {
				remaining = append(remaining, op)
			}
		}
		m.unsettled = remaining
		if warning := Reconciliation(result); warning != "" {
			m.reconcile = warning
		}
		pending := m.session.Snapshot().Pending
		attached := pending != nil && pending.Operation == result.Operation && pending.Revision == result.Revision && pending.Kind == result.Kind
		if !attached && result.Err == nil && result.Outcome.State == storage.Published {
			m.reconcile = "Detached save published a destination; filesystem reconciliation required"
		}
		return m.reduce(editor.Event{Command: editor.Complete, Result: &result})
	}
	if _, ok := msg.(CancelPendingMsg); ok {
		return m.reduce(editor.Event{Command: editor.CancelOperation})
	}
	event := input.Translate(msg)
	if event.Kind == input.Resize {
		m.width = max(1, min(event.Width, 4096))
		m.height = max(1, min(event.Height, 4096))
		return m, nil
	}
	if event.Kind != input.Press {
		switch event.Kind {
		case input.Paste, input.PasteStart, input.PasteEnd, input.Unknown:
			m.notice = "Unsupported event: " + string(event.Kind) + " (" + event.SourceType + ")"
		}
		return m, nil
	}
	if m.reconcile != "" {
		m.notice = "Resolve filesystem uncertainty before further commands"
		return m, nil
	}
	if len(m.unsettled) > 0 && m.session.Snapshot().Mode != editor.Waiting {
		m.notice = "Detached IO still pending; awaiting its actual receipt"
		return m, nil
	}
	k := event.Key
	if k.IsRepeat {
		m.notice = "Unsupported repeated key event"
		return m, nil
	}
	if next, cmd, handled := m.macroKey(k.Code, k.Mod, k.Text); handled {
		return next, cmd
	}
	command, ok := resolve(*k, m.session.Snapshot().Mode)
	if !ok {
		m.notice = "Unsupported key (physical delivery unqualified)"
		return m, nil
	}
	return m.reduce(command)
}
func resolve(k input.Key, mode editor.Mode) (editor.Event, bool) {
	// Delivered text keeps its identity. No q/CtrlQ/CtrlS command aliases.
	if k.Mod&^(tea.ModShift|tea.ModCapsLock) == 0 && k.Text != "" {
		switch mode {
		case editor.RetrieveName, editor.SaveName, editor.MacroName, editor.Editing, editor.Waiting:
			return editor.Event{Command: editor.Text, Text: k.Text}, true
		case editor.ReplaceQuestion, editor.ExitSaveQuestion, editor.ExitQuestion, editor.DeleteQuestion:
			if k.Text == "y" || k.Text == "Y" {
				return editor.Event{Command: editor.Yes}, true
			}
			if k.Text == "n" || k.Text == "N" {
				return editor.Event{Command: editor.No}, true
			}
		case editor.HistoryPreview:
			if k.Text == "1" {
				return editor.Event{Command: editor.Restore}, true
			}
			if k.Text == "2" {
				return editor.Event{Command: editor.Previous}, true
			}
		}
	}
	event := editor.Event{}
	switch {
	case k.Code == tea.KeyF10 && k.Mod == tea.ModAlt:
		event.Command = editor.Macro
	case k.Code == tea.KeyF3 && k.Mod == tea.ModShift:
		event.Command = editor.SwitchDocument
	case k.Code == tea.KeyF10 && k.Mod == tea.ModShift:
		event.Command = editor.Retrieve
	case k.Code == tea.KeyF3 && k.Mod == tea.ModAlt:
		event.Command = editor.Reveal
	case k.Code == tea.KeyF4 && k.Mod == tea.ModAlt:
		event.Command = editor.Block
	case k.Mod != 0:
		return event, false
	default:
		switch k.Code {
		case tea.KeyF10:
			event.Command = editor.Save
		case tea.KeyF1:
			event.Command = editor.F1
		case tea.KeyF7:
			event.Command = editor.F7
		case tea.KeyEscape:
			event.Command = editor.Escape
		case tea.KeyHome:
			event.Command = editor.Home
		case tea.KeyUp:
			event.Command = editor.Up
		case tea.KeyRight:
			event.Command = editor.Right
		case tea.KeyLeft:
			event.Command = editor.Left
		case tea.KeyBackspace:
			event.Command = editor.Backspace
		case tea.KeyDelete:
			event.Command = editor.Delete
		case tea.KeyInsert:
			event.Command = editor.Insert
		case tea.KeyEnter:
			event.Command = editor.Enter
		default:
			return event, false
		}
	}
	return event, true
}

// panes uses only document presentations. It never interprets native bytes,
// wraps original pages, computes printed positions or serializes view text.
func (m Model) panes() (normal, reveal string, x int, err error) {
	d := m.session.Document()
	if d == nil {
		return "", "", 0, nil
	}
	s := m.session.Snapshot()
	gap := s.Gap
	if gap > document.MaxWindowTokens {
		return "", "", 0, fmt.Errorf("cursor beyond bounded %d-token presentation", document.MaxWindowTokens)
	}
	count := min(d.TokenCount(), document.MaxWindowTokens)
	p, err := m.session.Present(0, count)
	if err != nil {
		return "", "", 0, err
	}
	elements := p.Elements
	blockStart, blockEnd := -1, -1
	if s.Selection {
		blockStart, blockEnd = s.SelectionStart, s.SelectionEnd
	}
	if s.Mode == editor.HistoryPreview {
		info, e := m.session.Preview(0, 0)
		if e != nil {
			return "", "", 0, e
		}
		if info.TotalTokens > document.MaxWindowTokens {
			return "", "", 0, fmt.Errorf("preview exceeds bounded %d-token presentation", document.MaxWindowTokens)
		}
		overlay, e := m.session.Preview(0, info.TotalTokens)
		if e != nil {
			return "", "", 0, e
		}
		elements = make([]document.Element, len(overlay.Elements))
		for i, v := range overlay.Elements {
			elements[i] = document.Element{TokenIndex: i, Kind: v.Kind, Text: v.Text}
		}
		blockStart, blockEnd = overlay.FragmentStart, overlay.FragmentEnd
	}
	var n, r strings.Builder
	nx, rx := 0, 0
	for i := 0; i <= len(elements); i++ {
		if i == blockStart {
			n.WriteString("[Block]")
			r.WriteString("[Block]")
			if i < gap {
				nx += 7
				rx += 7
			}
		}
		if i == blockEnd {
			n.WriteString("[Block]")
			r.WriteString("[Block]")
			if i < gap {
				nx += 7
				rx += 7
			}
		}
		if i == len(elements) {
			break
		}
		e := elements[i]
		rt := e.Text
		switch e.Kind {
		case document.BoldOn:
			n.WriteString("\x1b[1m")
			rt = "[BOLD]"
		case document.BoldOff:
			n.WriteString("\x1b[22m")
			rt = "[bold]"
		case document.ASCII:
			n.WriteString(e.Text)
			if i < gap {
				nx += len(e.Text)
			}
		default:
			return "", "", 0, fmt.Errorf("unsupported token presentation")
		}
		r.WriteString(rt)
		if i < gap {
			rx += len(rt)
		}
	}
	// Terminal cell scrolling is view-only, never original pagination or Pos.
	ns, rs := max(0, nx-max(1, m.width/2)), max(0, rx-max(1, m.width/2))
	x = nx - ns
	return ansi.TruncateLeft(n.String()+"\x1b[0m", ns, ""), ansi.TruncateLeft(r.String(), rs, ""), x, nil
}
func clip(s string, width int) string { return ansi.Truncate(s, width, "") }
func (m Model) View() tea.View {
	s := m.session.Snapshot()
	normal, reveal, x, err := m.panes()
	if m.macroStatus.DisplaySuppressed && m.macroFrozen != nil {
		normal, reveal, x, err = m.macroFrozen.normal, m.macroFrozen.reveal, m.macroFrozen.x, m.macroFrozen.err
	}
	lines := []string{"Wordling 5.2 | bounded native editing", normal}
	if err != nil {
		lines[1] = "Unsupported document presentation: " + err.Error()
	}
	if s.Reveal {
		lines = append(lines, "Press Reveal Codes to restore screen", reveal)
	}
	prompt := s.Prompt
	if m.repeatEntry {
		prompt = "Repeat Value = "
	} else if s.Mode == editor.Editing && s.MacroRepeat == 3 {
		prompt = "Repeat Value = 3"
	}
	lines = append(lines, prompt, s.Notice)
	if line := m.macroLine(); line != "" {
		lines = append(lines, line)
	}
	if s.Screen == 2 {
		lines = append(lines, "Doc2")
	}
	if s.Mode == editor.Waiting {
		lines = append(lines, "Filesystem operation pending")
	}
	if m.notice != "" {
		lines = append(lines, m.notice)
	}
	if m.reconcile != "" {
		lines = append(lines, m.reconcile)
	}
	history := "unknown"
	if s.HistoryCountKnown {
		history = fmt.Sprint(s.HistoryCount)
	}
	typing := ""
	if s.Typeover {
		typing = "Typeover "
	}
	profileLabel := "local-flat: ASCII basenames only; physical key delivery UNQUALIFIED"
	if m.runtime != nil && m.runtime.profile == MacroCOUT {
		profileLabel = "macro-cout: exact C:\\OUT\\ and flat names; physical key delivery UNQUALIFIED"
	}
	lines = append(lines, fmt.Sprintf("%s | %s | gap %d | %s", s.Mode, s.Name, s.Gap, s.SaveState),
		fmt.Sprintf("%sDirty=%t Block=%t revision=%d history=%s qualified=%t", typing, s.Dirty, s.Selection, s.Revision, history, s.HistoryQualified), profileLabel)
	for i := range lines {
		lines[i] = clip(lines[i], m.width)
	}
	if len(lines) > m.height {
		lines = lines[:m.height]
	}
	v := tea.NewView(strings.Join(lines, "\n"))
	v.AltScreen = true
	v.KeyboardEnhancements = tea.KeyboardEnhancements{ReportEventTypes: true, ReportAlternateKeys: true, ReportAllKeysAsEscapeCodes: true, ReportAssociatedText: true}
	if (s.Mode == editor.Editing || s.Mode == editor.DeleteQuestion || s.Mode == editor.HistoryPreview || s.Mode == editor.Waiting) && err == nil && m.height > 1 {
		y := 1
		if y < m.height {
			v.Cursor = tea.NewCursor(min(x, m.width-1), y)
		}
	}
	// Prompt caret refers to the original reducer draft, not document position.
	if (s.Mode == editor.RetrieveName || s.Mode == editor.SaveName || s.Mode == editor.MacroName) && len(lines) > 2 {
		prefix := "Document to be retrieved: "
		if s.Mode == editor.SaveName {
			prefix = "Document to be saved: "
		} else if s.Mode == editor.MacroName {
			prefix = "Macro: "
		}
		y := 2
		if s.Reveal {
			y = 4
		}
		if y < m.height {
			v.Cursor = tea.NewCursor(min(len(prefix)+s.Caret, m.width-1), y)
		}
	}
	if (m.repeatEntry || s.Mode == editor.Editing && s.MacroRepeat == 3) && m.height > 2 {
		x := len("Repeat Value = ")
		if !m.repeatEntry {
			x++
		}
		v.Cursor = tea.NewCursor(min(x, m.width-1), 2)
	}
	return v
}
