package tui

import (
	"strconv"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

type composeEntry struct {
	active, echo   bool
	value          string
	enterSeparator bool
}

func (c *composeEntry) begin(k input.Key) bool {
	if k.Mod != tea.ModCtrl || k.Code != '2' && k.Code != 'v' && k.Code != tea.KeySpace {
		return false
	}
	*c = composeEntry{active: true, echo: k.Code == 'v'}
	return true
}

func (c composeEntry) prompt() string {
	value := c.value
	if c.enterSeparator {
		value = strings.Replace(value, ",", " ", 1)
	}
	return "Key = " + value
}

// press returns a complete character or a diagnostic when the entry closes.
func (c *composeEntry) press(k input.Key) (composeCharacter, bool, string) {
	switch k.Code {
	case tea.KeyEscape, tea.KeyF1:
		*c = composeEntry{}
	case tea.KeyBackspace:
		if len(c.value) > 0 {
			c.value = c.value[:len(c.value)-1]
			if !strings.Contains(c.value, ",") {
				c.enterSeparator = false
			}
		}
	case tea.KeyEnter:
		left, right, comma := strings.Cut(c.value, ",")
		set, setErr := strconv.Atoi(left)
		if !comma && setErr == nil {
			c.value += ","
			c.enterSeparator = true
			return composeCharacter{}, false, ""
		}
		number, numberErr := strconv.Atoi(right)
		*c = composeEntry{}
		if setErr == nil && numberErr == nil && set >= 0 && set <= 255 && number >= 0 && number <= 255 &&
			len(document.CharacterBytes(byte(set), byte(number))) != 0 {
			return composeCharacter{byte(set), byte(number)}, true, ""
		}
		return composeCharacter{}, false, "Invalid WordPerfect character"
	default:
		for _, r := range k.Text {
			if r < 32 || r > 126 {
				continue
			}
			if len(c.value) < 7 {
				c.value += string(r)
			}
			if len(c.value) < 2 {
				continue
			}
			if left, _, comma := strings.Cut(c.value, ","); comma && left != "" {
				if _, err := strconv.Atoi(left); err == nil {
					continue
				}
			}
			if _, err := strconv.Atoi(c.value); err == nil {
				continue
			}
			result, ok := lookupComposePair(c.value)
			*c = composeEntry{}
			if !ok {
				return composeCharacter{}, false, ""
			}
			return result, true, ""
		}
	}
	return composeCharacter{}, false, ""
}

func (m Model) editorComposePress(k input.Key) (tea.Model, tea.Cmd) {
	character, ready, notice := m.compose.press(k)
	m.notice = notice
	if ready {
		return m.reduce(editor.Event{Command: editor.ComposeCharacter, Character: &editor.CharacterIdentity{Set: character.set, Number: character.number}})
	}
	return m, nil
}
