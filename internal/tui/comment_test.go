package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestCreateCommentMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, textKey("Visible before"), everydayKey(tea.KeyEnter), tea.Key{Code: tea.KeyF5, Mod: tea.ModCtrl}, textKey("4"), textKey("1"))
	if !strings.Contains(ansi.Strip(m.View().Content), "Document Comment") {
		t.Fatal(m.View().Content)
	}
	m = inputKeys(t, m, textKey("Internal note"), everydayKey(tea.KeyF7), textKey("Visible after"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-comment/COMMENT.WP"); got != want {
		t.Fatalf("body %x, want %x", got, want)
	}
	screen := ansi.Strip(m.View().Content)
	if strings.Index(screen, "Internal note") < strings.Index(screen, "Visible before") ||
		strings.Index(screen, "Visible after") < strings.Index(screen, "Internal note") {
		t.Fatal(screen)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if !strings.Contains(ansi.Strip(m.View().Content), "[Comment]Visible after") {
		t.Fatal(m.View().Content)
	}
}
