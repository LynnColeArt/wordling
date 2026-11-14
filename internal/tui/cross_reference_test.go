package tui

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestPageReferencesMatchDOS(t *testing.T) {
	m, _ := everydayUI(t)
	menu := tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, textKey("See page "), menu, textKey("1"), textKey("1"), textKey("1"), textKey("Mixed"), enter)
	if !strings.Contains(ansi.Strip(m.View().Content), "See page ?") {
		t.Fatal(m.View().Content)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl}, textKey("Chapter"), menu, textKey("1"), textKey("2"), textKey("mixed"), enter)
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-cross-references/BEFORE.WP"); got != want {
		t.Fatalf("marked %x, want %x: %s", got, want, m.notice)
	}
	for range 2 {
		m = inputKeys(t, m, menu, textKey("6"), textKey("5"), textKey("y"))
		if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-cross-references/AFTER.WP"); got != want {
			t.Fatalf("generated %x, want %x: %s", got, want, m.notice)
		}
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if s := ansi.Strip(m.View().Content); !strings.Contains(s, "See page 2") || !strings.Contains(s, "[Ref(MIXED):Pg 2]") {
		t.Fatal(s)
	}
}

func TestMarkPageReferenceAndTargetMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	menu := tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, textKey("See page Chapter"))
	for range len("Chapter") {
		m = inputKeys(t, m, everydayKey(tea.KeyLeft))
	}
	m = inputKeys(t, m, menu, textKey("1"), textKey("3"), textKey("1"))
	if !strings.Contains(ansi.Strip(m.View().Content), "Move to page; Press Enter.") {
		t.Fatal(m.View().Content)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyEnd), enter, textKey("Joint"), enter)
	for range 2 {
		if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-cross-references/BOTH.WP"); got != want {
			t.Fatalf("got %x, want %x: %s", got, want, m.notice)
		}
		m = inputKeys(t, m, menu, textKey("6"), textKey("5"), textKey("y"))
	}
}

func TestPageReferenceUsesRenumberedPage(t *testing.T) {
	for _, prefix := range []string{"NUM", "ROM"} {
		t.Run(prefix, func(t *testing.T) {
			m, root := everydayUI(t)
			name := prefix + "DEF.WP"
			raw, err := os.ReadFile("../../docs/research/reference-runs/mission1-cross-references/" + name)
			if err != nil {
				t.Fatal(err)
			}
			if err := os.WriteFile(filepath.Join(root, name), raw, 0600); err != nil {
				t.Fatal(err)
			}
			menu := tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey(name), everydayKey(tea.KeyEnter))
			m = inputKeys(t, m, menu, textKey("6"), textKey("5"), textKey("y"))
			if want, got := lineFormatBody(t, "mission1-cross-references/"+prefix+"GEN.WP"), hBoldBody(t, m); got != want {
				t.Fatalf("got %x, want %x: %s", got, want, m.notice)
			}
		})
	}
}
