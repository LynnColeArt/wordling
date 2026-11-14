package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestColumnMathScopeMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	enter, tab := everydayKey(tea.KeyEnter), everydayKey(tea.KeyTab)
	m = inputKeys(t, m, tableF7, textKey("3"), textKey("1"), textKey("2"), tab, textKey("3"), enter,
		textKey("4"), tab, textKey("5"), enter, tableF7, textKey("3"), textKey("2"), textKey("After"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-column-math/MATH.WP"); got != want {
		t.Fatalf("body %x, want %x: %s", got, want, m.notice)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if view := ansi.Strip(m.View().Content); !strings.Contains(view, "[Math On]") || !strings.Contains(view, "[Math Off]After") {
		t.Fatal(view)
	}
}

func TestColumnMathSubtotalMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	enter, tab := everydayKey(tea.KeyEnter), everydayKey(tea.KeyTab)
	m = inputKeys(t, m, tableF7, textKey("3"), textKey("1"), textKey("N"), tab, textKey("3"), enter,
		textKey("S"), tab, textKey("5"), enter, textKey("T"), tab, textKey("+"))
	if view := ansi.Strip(m.View().Content); !strings.Contains(view, "+") || strings.Contains(view, "8.00") {
		t.Fatal(view)
	}
	m = inputKeys(t, m, tableF7, textKey("3"), textKey("4"))
	if view := ansi.Strip(m.View().Content); !strings.Contains(view, "8.00+") {
		t.Fatal(view, m.notice)
	}
	m = inputKeys(t, m, enter, tableF7, textKey("3"), textKey("2"), textKey("After"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-column-math/TOTAL.WP"); got != want {
		t.Fatalf("body %x, want %x: %s", got, want, m.notice)
	}
}
