package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestHorizontalLineDrawMatchesDOS(t *testing.T) {
	for _, tc := range []struct{ choice, file, glyph string }{
		{"1", "SINGLE.WP", "───"}, {"2", "DOUBLE.WP", "═══"},
	} {
		t.Run(tc.file, func(t *testing.T) {
			m, _ := everydayUI(t)
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModCtrl}, textKey("2"), textKey(tc.choice))
			for range 4 {
				m = inputKeys(t, m, everydayKey(tea.KeyRight))
			}
			m = inputKeys(t, m, everydayKey(tea.KeyF7))
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-line-draw/"+tc.file); got != want {
				t.Fatalf("body %x, want %x: %s", got, want, m.notice)
			}
			if view := ansi.Strip(m.View().Content); !strings.Contains(view, tc.glyph) || strings.Contains(view, "Erase; 6 Move") {
				t.Fatal(view)
			}
		})
	}
}
