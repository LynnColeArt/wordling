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
}
type State struct {
	Session                   editor.Snapshot
	Width, Height             int
	Notice, Reconciliation    string
	PendingIO                 int
	PhysicalDeliveryQualified bool
}

func (m Model) State() State {
	return State{Session: m.session.Snapshot(), Width: m.width, Height: m.height, Notice: m.notice, Reconciliation: m.reconcile, PendingIO: len(m.unsettled)}
}

// Session returns an immutable value for measurements/inspection. Never fork it
// to execute independent intents: this Model owns the sole authoritative chain.
func (m Model) Session() editor.Session { return m.session }
func (m Model) Init() tea.Cmd           { return nil }
func (m Model) reduce(event editor.Event) (tea.Model, tea.Cmd) {
	next, intent, err := m.session.Reduce(event)
	m.session = next
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
	if _, ok := msg.(duplicateDispatchMsg); ok {
		m.notice = "Duplicate IO dispatch refused; no additional operation executed"
		return m, nil
	}
	if reply, ok := msg.(resultMsg); ok {
		result := reply.result
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
	command, ok := resolve(*k, m.session.Snapshot().Mode)
	if !ok {
		m.notice = "Unsupported key (physical delivery unqualified)"
		return m, nil
	}
	return m.reduce(command)
}
func resolve(k input.Key, mode editor.Mode) (editor.Event, bool) {
	event := editor.Event{}
	// Shift/CapsLock are text modifiers, not command aliases. Preserve the
	// delivered Text verbatim in filename contexts, including uppercase ASCII.
	if k.Mod&^(tea.ModShift|tea.ModCapsLock) == 0 && k.Text != "" {
		if mode == editor.RetrieveName || mode == editor.SaveName {
			return editor.Event{Command: editor.Text, Text: k.Text}, true
		}
		if mode == editor.ReplaceQuestion || mode == editor.ExitSaveQuestion || mode == editor.ExitQuestion {
			if k.Text == "y" || k.Text == "Y" {
				return editor.Event{Command: editor.Yes}, true
			}
			if k.Text == "n" || k.Text == "N" {
				return editor.Event{Command: editor.No}, true
			}
		}
	}
	switch {
	case k.Code == tea.KeyF10 && k.Mod == tea.ModShift:
		event.Command = editor.Retrieve
	case k.Code == tea.KeyF3 && k.Mod == tea.ModAlt:
		event.Command = editor.Reveal
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
		case tea.KeyEnter:
			event.Command = editor.Enter
		default:
			if mode == editor.ReplaceQuestion || mode == editor.ExitSaveQuestion || mode == editor.ExitQuestion {
				switch k.Text {
				case "y", "Y":
					event.Command = editor.Yes
				case "n", "N":
					event.Command = editor.No
				default:
					return event, false
				}
			} else if mode == editor.RetrieveName || mode == editor.SaveName {
				if k.Text == "" {
					return event, false
				}
				event.Command = editor.Text
				event.Text = k.Text
			} else {
				return event, false
			}
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
	gap := m.session.Snapshot().Gap
	start := 0
	if gap > document.MaxWindowTokens {
		return "", "", 0, fmt.Errorf("cursor beyond bounded %d-token presentation", document.MaxWindowTokens)
	}
	count := min(d.TokenCount()-start, document.MaxWindowTokens)
	p, err := m.session.Present(start, count)
	if err != nil {
		return "", "", 0, err
	}
	var n, r strings.Builder
	for _, e := range p.Elements {
		text := e.Text
		if e.Kind == document.BoldOn {
			n.WriteString("\x1b[1m")
		}
		if e.Kind == document.BoldOff {
			n.WriteString("\x1b[22m")
		}
		if e.Kind == document.ASCII {
			n.WriteString(text)
		}
		if e.TokenIndex < gap && e.Kind == document.ASCII {
			x += len(text)
		}
		switch e.Kind {
		case document.BoldOn:
			r.WriteString("[BOLD]")
		case document.BoldOff:
			r.WriteString("[bold]")
		default:
			r.WriteString(text)
		}
	}
	scroll := max(0, x-max(1, m.width/2))
	return ansi.TruncateLeft(n.String()+"\x1b[0m", scroll, ""), r.String(), x - scroll, nil
}
func clip(s string, width int) string { return ansi.Truncate(s, width, "") }
func (m Model) View() tea.View {
	s := m.session.Snapshot()
	normal, reveal, x, err := m.panes()
	lines := []string{"Wordling 5.2 | bounded read-only session", normal}
	if err != nil {
		lines[1] = "Unsupported document presentation: " + err.Error()
	}
	if s.Reveal {
		lines = append(lines, "Press Reveal Codes to restore screen", reveal)
	}
	lines = append(lines, s.Prompt, s.Notice)
	if s.Mode == editor.Waiting {
		lines = append(lines, "Filesystem operation pending")
	}
	if m.notice != "" {
		lines = append(lines, m.notice)
	}
	if m.reconcile != "" {
		lines = append(lines, m.reconcile)
	}
	lines = append(lines, fmt.Sprintf("%s | %s | gap %d | %s", s.Mode, s.Name, s.Gap, s.SaveState), "local-flat: ASCII basenames only; physical key delivery UNQUALIFIED")
	for i := range lines {
		lines[i] = clip(lines[i], m.width)
	}
	if len(lines) > m.height {
		lines = lines[:m.height]
	}
	v := tea.NewView(strings.Join(lines, "\n"))
	v.AltScreen = true
	v.KeyboardEnhancements = tea.KeyboardEnhancements{ReportEventTypes: true, ReportAlternateKeys: true, ReportAllKeysAsEscapeCodes: true, ReportAssociatedText: true}
	if s.Mode == editor.Editing && err == nil && m.height > 1 {
		v.Cursor = tea.NewCursor(min(x, m.width-1), 1)
	}
	// Prompt caret refers to the original reducer draft, not document position.
	if (s.Mode == editor.RetrieveName || s.Mode == editor.SaveName) && len(lines) > 2 {
		prefix := "Document to be retrieved: "
		if s.Mode == editor.SaveName {
			prefix = "Document to be saved: "
		}
		y := 2
		if s.Reveal {
			y = 4
		}
		if y < m.height {
			v.Cursor = tea.NewCursor(min(len(prefix)+s.Caret, m.width-1), y)
		}
	}
	return v
}
