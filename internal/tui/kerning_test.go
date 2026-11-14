package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestKerningCodeMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, textKey("AV "), tea.Key{Code: tea.KeyF8, Mod: tea.ModShift},
		textKey("4"), textKey("6"), textKey("1"), textKey("y"), everydayKey(tea.KeyF7), textKey("AV"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-kerning/KERN.WP"); got != want {
		t.Fatalf("got %x, want %x: %s", got, want, m.notice)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if view := ansi.Strip(m.View().Content); !strings.Contains(view, "AV [Kern:On]AV") {
		t.Fatal(view)
	}
}
