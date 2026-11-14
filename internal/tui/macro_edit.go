package tui

import (
	"fmt"
	"slices"
	"strings"
	"unicode/utf8"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

func (m Model) openExistingMacro(description bool) Model {
	r := &m.recording
	image, err := r.target.ReadExisting()
	if err != nil {
		m.notice = err.Error()
		return m
	}
	r.image, r.stage, m.notice = image, recordInspect, ""
	r.action, r.editable = image.RecordingKeys()
	r.description = originalMacroDescription(image)
	r.actionGap = -1 // Before the initial Display Off command in the original.
	if description {
		if len(r.description) > wpm.MaxEditedDescription || !printableMacroText(r.description) {
			r.stage, m.notice = recordExisting, "This macro description cannot be edited"
			return m
		}
		r.stage, r.draft, r.descrGap = recordEditDescription, r.description, 0
	}
	return m
}

func originalMacroDescription(image *wpm.Image) string {
	desc := image.Description()
	return string(desc[:len(desc)-1])
}

func (m Model) macroDescriptionPress(k input.Key) Model {
	if k.Mod&^(tea.ModShift|tea.ModCapsLock) != 0 {
		return m
	}
	r := &m.recording
	switch k.Code {
	case tea.KeyF1, tea.KeyEscape:
		r.stage, m.notice = recordExisting, ""
	case tea.KeyEnter:
		if _, err := r.image.Edit(r.draft, nil, false); err != nil {
			m.notice = err.Error()
		} else {
			r.description, r.stage, m.notice = r.draft, recordInspect, ""
		}
	case tea.KeyHome:
		r.descrGap = 0
	case tea.KeyEnd:
		r.descrGap = len(r.draft)
	case tea.KeyLeft:
		r.descrGap = max(0, r.descrGap-1)
	case tea.KeyRight:
		r.descrGap = min(len(r.draft), r.descrGap+1)
	case tea.KeyBackspace:
		if r.descrGap > 0 {
			r.draft = r.draft[:r.descrGap-1] + r.draft[r.descrGap:]
			r.descrGap--
		}
	case tea.KeyDelete:
		if r.descrGap < len(r.draft) {
			r.draft = r.draft[:r.descrGap] + r.draft[r.descrGap+1:]
		}
	default:
		if len(r.draft)+len(k.Text) <= wpm.MaxEditedDescription && printableMacroText(k.Text) {
			r.draft = r.draft[:r.descrGap] + k.Text + r.draft[r.descrGap:]
			r.descrGap += len(k.Text)
		}
	}
	return m
}

func (r macroRecording) actionChanged() bool {
	if !r.editable {
		return false
	}
	original, _ := r.image.RecordingKeys()
	return !slices.Equal(r.action, original)
}

func (m Model) macroActionPress(k input.Key) Model {
	r := &m.recording
	if r.discard {
		switch {
		case strings.EqualFold(k.Text, "y") && k.Mod&^(tea.ModShift|tea.ModCapsLock) == 0:
			m.recording, m.notice = macroRecording{}, ""
		case strings.EqualFold(k.Text, "n") || k.Code == tea.KeyF1 || k.Code == tea.KeyEscape || k.Code == tea.KeyEnter:
			r.discard = false
		}
		return m
	}
	if k.Mod == 0 {
		switch k.Code {
		case tea.KeyF7:
			actionChanged := r.actionChanged()
			var err error
			if actionChanged || r.description != originalMacroDescription(r.image) {
				err = r.target.PublishEdit(r.image, r.description, r.action, actionChanged)
			} // An unchanged exit has no publication.
			if err != nil {
				m.notice = err.Error()
			} else {
				m.recording, m.notice = macroRecording{}, ""
			}
			return m
		case tea.KeyEscape, tea.KeyF1:
			if r.actionChanged() || r.description != originalMacroDescription(r.image) {
				r.discard = true
				m.notice = ""
			} else {
				m.recording, m.notice = macroRecording{}, ""
			}
			return m
		}
	}
	if !r.editable {
		m.notice = "This WPM's action is available for inspection only"
		return m
	}
	m.notice = ""
	if k.Mod == tea.ModCtrl && k.Code == 'v' {
		r.literalCommand = true
		return m
	}
	insert := func(keys []uint16) {
		if r.actionGap < 0 {
			m.notice = "Move right past Display Off before editing"
			return
		}
		if len(r.action)+len(keys) > wpm.MaxRecordedKeys {
			m.notice = "Macro key limit reached"
			return
		}
		r.action = slices.Insert(slices.Clone(r.action), r.actionGap, keys...)
		r.actionGap += len(keys)
	}
	if r.literalCommand {
		r.literalCommand = false
		switch {
		case k.Mod == 0 && k.Code == tea.KeyLeft:
			insert([]uint16{wpm.RecordedLeft})
		default:
			m.notice = "Command insertion supports Left"
		}
		return m
	}
	if k.Mod == 0 {
		switch k.Code {
		case tea.KeyEnter:
			insert([]uint16{wpm.ActionReturn})
			return m
		case tea.KeyLeft:
			r.actionGap = max(-1, r.actionGap-1)
			return m
		case tea.KeyRight:
			r.actionGap = min(len(r.action), r.actionGap+1)
			return m
		case tea.KeyHome:
			r.actionGap = -1
			return m
		case tea.KeyEnd:
			r.actionGap = len(r.action)
			return m
		case tea.KeyBackspace:
			if r.actionGap > 0 {
				r.action = slices.Delete(slices.Clone(r.action), r.actionGap-1, r.actionGap)
				r.actionGap--
			}
			return m
		case tea.KeyDelete:
			if r.actionGap >= 0 && r.actionGap < len(r.action) {
				r.action = slices.Delete(slices.Clone(r.action), r.actionGap, r.actionGap+1)
			}
			return m
		}
	}
	if k.Mod&^(tea.ModShift|tea.ModCapsLock) == 0 && k.Text != "" && printableMacroText(k.Text) && !strings.ContainsRune(k.Text, '~') {
		keys := make([]uint16, len(k.Text))
		for i := range keys {
			keys[i] = uint16(k.Text[i])
		}
		insert(keys)
	}
	return m
}

func (m Model) macroActionView() tea.View {
	r := m.recording
	lines := []string{""}
	x, y := 0, 0
	width := max(1, min(m.width-7, 71))
	add := func(word uint16, gap bool) {
		label, newline := macroWordLabel(word)
		if len(label) <= width && utf8.RuneCountInString(lines[len(lines)-1])+utf8.RuneCountInString(label) > width {
			lines = append(lines, "")
		}
		if gap {
			x, y = utf8.RuneCountInString(lines[len(lines)-1]), len(lines)-1
		}
		lines[len(lines)-1] += label
		if newline {
			lines = append(lines, "")
		}
	}
	if r.editable {
		add(0xfc0c, r.actionGap < 0)
		for i, word := range r.action {
			add(word, r.actionGap == i)
		}
		if r.actionGap == len(r.action) {
			x, y = utf8.RuneCountInString(lines[len(lines)-1]), len(lines)-1
		}
	} else {
		follower := false
		for _, word := range r.image.WordPreview(4096) {
			if word.Value == 0 {
				break
			}
			if follower && word.Value == wpm.EnterFollower {
				follower = false
				continue
			}
			add(word.Value, false)
			follower = word.Value == wpm.RecordedEnter
		}
	}
	body := []string{"Macro: Action", "", "     File             " + r.target.Path(), "",
		"     Description      " + safeMacroDescription([]byte(r.description)), ""}
	box := m.width >= 11 && m.height >= 10
	if box {
		body = append(body, "     ╔"+strings.Repeat("═", width)+"╗")
		rows := m.height - 10
		top := max(0, y-rows+1)
		for i := top; i < top+rows; i++ {
			line := ""
			if i < len(lines) {
				line = clip(lines[i], width)
			}
			body = append(body, "     ║"+line+strings.Repeat(" ", width-utf8.RuneCountInString(line))+"║")
		}
		body = append(body, "     ╚"+strings.Repeat("═", width)+"╝", "Ctrl-V to Insert next key as command;")
		y -= top
	}
	footer := "Press Exit when done"
	if r.discard {
		footer = "Cancel changes? No (Yes)"
	} else if r.literalCommand {
		footer = "Insert next key as command"
	}
	view := m.historicModalView(body, footer, m.notice)
	if box && m.height > 10 && !r.discard && !r.literalCommand && r.editable {
		view.Cursor = tea.NewCursor(min(m.width-1, 6+x), 7+y)
	}
	return view
}

func macroWordLabel(word uint16) (string, bool) {
	switch word {
	case 0xfc0c:
		return "{DISPLAY OFF}", false
	case wpm.RecordedEnter:
		return "{Enter}", true
	case wpm.ActionReturn:
		return "", true
	case wpm.RecordedLeft:
		return "{Left}", false
	case ' ':
		return "·", false
	}
	if word >= 32 && word <= 126 {
		return string(rune(word)), false
	}
	return fmt.Sprintf("{%04X}", word), false
}
