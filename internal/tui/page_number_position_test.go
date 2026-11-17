package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestPageNumberPositionAndSuppressionMatchDOS(t *testing.T) {
	shiftF8 := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}
	page := tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl}
	f7 := everydayKey(tea.KeyF7)
	for _, tc := range []struct{ name, choice, expected string }{
		{"BOTTOM", "7", "[Pg Numbering:Bottom Right]Alpha"},
		{"TOP", "2", "[Pg Numbering:Top Center]Alpha"},
		{"TITLE", "7", "[Pg Numbering:Bottom Right][Suppress:PgNum]Alpha"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			m, _ := everydayUI(t)
			m = inputKeys(t, m, shiftF8, textKey("2"), textKey("6"), textKey("4"), textKey(tc.choice), f7)
			if tc.name == "TITLE" {
				m = inputKeys(t, m, shiftF8, textKey("2"), textKey("8"), textKey("4"), textKey("y"), f7)
			}
			m = inputKeys(t, m, textKey("Alpha"), page, textKey("Beta"), page, textKey("Gamma"))
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-page-number-position/"+tc.name+".WP"); got != want {
				t.Fatalf("got %x, want %x; %q", got, want, m.notice)
			}
			m = inputKeys(t, m, everydayKey(tea.KeyHome), everydayKey(tea.KeyHome), everydayKey(tea.KeyUp),
				tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
			if !strings.Contains(ansi.Strip(m.View().Content), tc.expected) {
				t.Fatal(ansi.Strip(m.View().Content))
			}
		})
	}
}
