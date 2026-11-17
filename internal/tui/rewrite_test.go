package tui

import (
	"reflect"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestScreenRewriteMatchesDOSWithoutMutation(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, textKey("Rewrite keeps this text."), everydayKey(tea.KeyLeft), everydayKey(tea.KeyLeft))
	before, screen, caret := m.session.Snapshot(), m.View().Content, m.View().Cursor
	keys := tea.Key{Code: tea.KeyF3, Mod: tea.ModCtrl}
	m = inputKeys(t, m, keys)
	if !strings.Contains(ansi.Strip(m.View().Content), screenPrompt) {
		t.Fatal(m.View().Content)
	}
	m = inputKeys(t, m, textKey("3"))
	if !reflect.DeepEqual(m.session.Snapshot(), before) || m.View().Content != screen || !reflect.DeepEqual(m.View().Cursor, caret) {
		t.Fatal("rewrite changed document or cursor")
	}
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-rewrite/REWRITE.WP"); got != want {
		t.Fatalf("native %q, want %q", got, want)
	}
}
