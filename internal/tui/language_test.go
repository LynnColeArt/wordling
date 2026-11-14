package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestLanguageCodeMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, textKey("Before"), tea.Key{Code: tea.KeyF8, Mod: tea.ModShift},
		textKey("4"), textKey("4"), textKey("uk"), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7), textKey("After"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-language/LANGUAGE.WP"); got != want {
		t.Fatalf("got %x, want %x: %s", got, want, m.notice)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if view := ansi.Strip(m.View().Content); !strings.Contains(view, "Before[Lang:UK]After") {
		t.Fatal(view)
	}
}
