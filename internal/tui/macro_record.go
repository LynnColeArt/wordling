package tui

import (
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
	"github.com/lynncoleart/wordling/internal/storage"
)

const (
	recordName = iota + 1
	recordExisting
	recordReplace
	recordDescription
	recordEditDescription
	recordInspect
	recordKeys
)

type macroRecording struct {
	stage                   int
	draft, description      string
	target                  *storage.MacroRecordingTarget
	replace                 bool
	keys                    []uint16
	image                   *wpm.Image
	action                  []uint16
	editable                bool
	actionGap, descrGap     int
	literalCommand, discard bool
}

func isRecordKey(k input.Key) bool {
	return k.Code == tea.KeyF10 && k.Mod&^tea.ModCapsLock == tea.ModCtrl && !k.IsRepeat
}

func (m Model) openMacroRecording() Model {
	s := m.session.Snapshot()
	if m.runtime.workspaceRoot == nil || m.macro != nil || m.runtime.activeMacro() != nil ||
		m.reconcile != "" || m.firstPending != nil || len(m.unsettled) != 0 ||
		s.Mode != editor.Editing || s.MacroRepeat != 1 || s.Selection || s.Reveal || s.Typeover || s.HomePrefix != 0 {
		m.notice = "Define macro requires ordinary editing"
		return m
	}
	m.closeMenus()
	m.recording = macroRecording{stage: recordName}
	m.notice = ""
	return m
}

func (m Model) recordPress(k input.Key) (tea.Model, tea.Cmd) {
	r := &m.recording
	if k.IsRepeat {
		return m, nil
	}
	if r.stage == recordInspect {
		return m.macroActionPress(k), nil
	}
	if r.stage == recordEditDescription {
		return m.macroDescriptionPress(k), nil
	}
	if k.Mod&^tea.ModCapsLock == 0 && (k.Code == tea.KeyF1 || k.Code == tea.KeyEscape) {
		m.recording, m.notice = macroRecording{}, ""
		return m, nil
	}
	if (r.stage == recordExisting || r.stage == recordReplace) && k.Mod&^(tea.ModShift|tea.ModCapsLock) != 0 {
		return m, nil
	}
	if r.stage == recordExisting {
		switch k.Text {
		case "1":
			r.stage = recordReplace
		case "2", "3":
			m = m.openExistingMacro(k.Text == "3")
		}
		return m, nil
	}
	if r.stage == recordReplace {
		switch {
		case strings.EqualFold(k.Text, "y"):
			r.stage, r.replace, m.notice = recordDescription, true, ""
		case strings.EqualFold(k.Text, "n"), k.Code == tea.KeyEnter:
			r.stage, m.notice = recordExisting, ""
		}
		return m, nil
	}
	if r.stage != recordKeys {
		if k.Mod&^(tea.ModShift|tea.ModCapsLock) != 0 {
			return m, nil
		}
		switch k.Code {
		case tea.KeyEnter:
			if r.stage == recordName {
				target, err := m.runtime.workspaceRoot.ObserveMacroRecording(r.draft)
				if err != nil {
					m.notice = err.Error()
					return m, nil
				}
				r.target, r.stage, r.draft = target, recordDescription, ""
				if target.Exists() {
					r.stage = recordExisting
				}
			} else {
				r.description, r.stage, r.draft = r.draft, recordKeys, ""
			}
			m.notice = ""
		case tea.KeyBackspace:
			if len(r.draft) > 0 {
				r.draft = r.draft[:len(r.draft)-1]
			}
		default:
			if k.Mod&^(tea.ModShift|tea.ModCapsLock) == 0 && len(r.draft)+len(k.Text) <= 79 && printableMacroText(k.Text) {
				r.draft += k.Text
			}
		}
		return m, nil
	}
	if isRecordKey(k) {
		err := r.target.Publish(r.description, r.keys, r.replace)
		m.recording, m.notice = macroRecording{}, ""
		if err != nil {
			m.notice = err.Error()
		}
		return m, nil
	}
	var keys []uint16
	var event editor.Event
	switch {
	case k.Mod&^tea.ModCapsLock == 0 && k.Code == tea.KeyEnter:
		keys, event.Command = []uint16{wpm.RecordedEnter}, editor.Enter
	case k.Mod&^tea.ModCapsLock == 0 && k.Code == tea.KeyLeft:
		keys, event = []uint16{wpm.RecordedLeft}, editor.Event{Command: editor.Left, ViewportColumns: m.width}
	case k.Mod&^(tea.ModShift|tea.ModCapsLock) == 0 && k.Text != "" && printableMacroText(k.Text) && !strings.ContainsRune(k.Text, '~'):
		for i := range len(k.Text) {
			keys = append(keys, uint16(k.Text[i]))
		}
		event = editor.Event{Command: editor.Text, Text: k.Text}
	default:
		m.notice = "Recordable keys: printable text, Enter and Left"
		return m, nil
	}
	if len(r.keys)+len(keys) > wpm.MaxRecordedKeys {
		m.notice = "Macro key limit reached; Ctrl+F10 saves the recording"
		return m, nil
	}
	next, intent, err := m.session.Reduce(event)
	switch {
	case err != nil:
		m.notice = err.Error()
	case intent != nil || next.Snapshot().Mode != editor.Editing:
		m.notice = "Recordable keys must stay in ordinary editing"
	default:
		m.session, m.notice = next, ""
		r.keys = append(append([]uint16(nil), r.keys...), keys...)
	}
	return m, nil
}

func printableMacroText(s string) bool {
	return strings.IndexFunc(s, func(c rune) bool { return c < 32 || c > 126 }) == -1
}

func (m Model) macroRecordingView(view tea.View) tea.View {
	if m.recording.stage == recordInspect {
		return m.macroActionView()
	}
	prompt := "Recording macro; Ctrl+F10 to finish"
	switch m.recording.stage {
	case recordName:
		prompt = "Define macro: " + m.recording.draft
	case recordExisting:
		prompt = m.recording.target.Path() + " Already Exists: 1 Replace; 2 Edit; 3 Description: 0"
	case recordReplace:
		prompt = "Replace " + m.recording.target.Path() + "? No (Yes)"
	case recordDescription, recordEditDescription:
		prompt = "Description: " + safeMacroDescription([]byte(m.recording.draft))
	}
	rows := strings.Split(view.Content, "\n")
	y := len(rows) - 1
	rows[y] = clip(prompt, m.width)
	if m.notice != "" && y > 0 {
		rows[y-1] = clip(m.notice, m.width)
	}
	view.Content = strings.Join(rows, "\n")
	if m.recording.stage != recordKeys {
		column := len(prompt)
		if m.recording.stage == recordEditDescription {
			column = len("Description: ") + m.recording.descrGap
		}
		view.Cursor = tea.NewCursor(min(m.width-1, column), y)
	}
	return view
}

func safeMacroDescription(desc []byte) string {
	return strings.Map(func(c rune) rune {
		if c < 32 || c > 126 {
			return '?'
		}
		return c
	}, string(desc))
}
