package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestDefaultOutlineLevelsMatchDOS(t *testing.T) {
	m, _ := everydayUI(t)
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF5, Mod: tea.ModShift}, textKey("4"), textKey("1"),
		enter, textKey("First"), enter, everydayKey(tea.KeyTab), textKey("Child"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-outline/OUTLINE.WP"); got != want {
		t.Fatalf("outline body %x, want %x: %s", got, want, m.notice)
	}
	if s := ansi.Strip(m.View().Content); !strings.Contains(s, "I.First") || !strings.Contains(s, "     A.Child") {
		t.Fatal(s)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if s := ansi.Strip(m.View().Content); !strings.Contains(s, "[Outline On]") || strings.Count(s, "[Par Num:Auto]") != 2 {
		t.Fatal(s)
	}
}
