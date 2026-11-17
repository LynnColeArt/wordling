package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestMarkFullAuthorityMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	citation := "Sample v. Example"
	m = inputKeys(t, m, textKey(citation))
	for range len(citation) {
		m = inputKeys(t, m, everydayKey(tea.KeyLeft))
	}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt}, everydayKey(tea.KeyEnd),
		tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}, textKey("4"), textKey("1"), enter)
	if !strings.Contains(ansi.Strip(m.View().Content), "ToA Full Form:") {
		t.Fatal(m.View().Content)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF7))
	if !strings.Contains(ansi.Strip(m.View().Content), "Short Form: "+citation) {
		t.Fatal(m.View().Content)
	}
	m = inputKeys(t, m, enter, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-authorities/CITE.WP"); got != want {
		t.Fatalf("body %x, want %x: %s", got, want, m.notice)
	}
	if !strings.Contains(ansi.Strip(m.View().Content), "[ToA:1;"+citation+";Full Form]") {
		t.Fatal(m.View().Content)
	}
}
