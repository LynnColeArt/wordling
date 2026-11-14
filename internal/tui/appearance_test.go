package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestFontAppearanceItalicsMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	font := tea.Key{Code: tea.KeyF8, Mod: tea.ModCtrl}
	m = inputKeys(t, m, font, textKey("2"), textKey("4"), textKey("alpha"),
		font, textKey("2"), textKey("4"), textKey("beta"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-appearance/ITALICS.WP"); got != want {
		t.Fatalf("got %x, want %x (%s)", got, want, m.notice)
	}
	if !strings.Contains(m.View().Content, italicText+"alpha") {
		t.Fatal("missing DOS italics color")
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt},
		everydayKey(tea.KeyHome), everydayKey(tea.KeyHome), everydayKey(tea.KeyUp))
	if !strings.Contains(ansi.Strip(m.View().Content), "[ITALC]alpha[italc]beta") {
		t.Fatal(ansi.Strip(m.View().Content))
	}
}
