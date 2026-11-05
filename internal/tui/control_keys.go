package tui

import (
	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

// Translate opt-in host shortcuts before the normal function-key dispatch so
// menus, pending I/O and modal editing apply the same rules to either key.
func controlKey(k input.Key) input.Key {
	if k.Mod != tea.ModCtrl {
		return k
	}
	switch k.Code {
	case 'b':
		k.Code, k.Mod = tea.KeyF6, 0
	case 'r':
		k.Code, k.Mod = tea.KeyF3, tea.ModAlt
	case 's':
		k.Code, k.Mod = tea.KeyF10, 0
	case 'o':
		k.Code, k.Mod = tea.KeyF10, tea.ModShift
	case 'q':
		k.Code, k.Mod = tea.KeyF7, 0
	default:
		return k
	}
	k.Text = ""
	return k
}
