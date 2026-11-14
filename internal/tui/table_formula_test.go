package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

var tableF7 = tea.Key{Code: tea.KeyF7, Mod: tea.ModAlt}

func newTwoByTwoTable(t *testing.T) Model {
	t.Helper()
	m, _ := everydayUI(t)
	enter := everydayKey(tea.KeyEnter)
	return inputKeys(t, m, tableF7, textKey("2"), textKey("1"), textKey("2"), enter, textKey("2"), enter, everydayKey(tea.KeyF7))
}

func TestTableFormulaRecalculationMatchesDOS(t *testing.T) {
	m := newTwoByTwoTable(t)
	tab, enter, f7 := everydayKey(tea.KeyTab), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7)
	m = inputKeys(t, m, textKey("2"), tab, textKey("3"), tab, tableF7, textKey("5"), textKey("2"), textKey("A1+B1"), enter, f7)
	want := lineFormatBody(t, "mission1-table-math/INIT.WP")
	if got := hBoldBody(t, m); got != want {
		t.Fatalf("initial body %x, want %x: %s", got, want, m.notice)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyUp), everydayKey(tea.KeyHome), everydayKey(tea.KeyDelete), textKey("7"))
	if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, "5.00") || !strings.Contains(screen, "║7") {
		t.Fatal(screen)
	}
	m = inputKeys(t, m, tableF7, textKey("5"), textKey("1"), f7)
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-table-math/RECALC.WP"); got != want {
		t.Fatalf("recalculated body %x, want %x: %s", got, want, m.notice)
	}
}

func TestCopyTableFormulaToCellMatchesDOS(t *testing.T) {
	m := newTwoByTwoTable(t)
	tab, enter, f7 := everydayKey(tea.KeyTab), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7)
	m = inputKeys(t, m, tab, textKey("3"), tab, tab, textKey("5"), everydayKey(tea.KeyUp), everydayKey(tea.KeyLeft), everydayKey(tea.KeyLeft))
	m = inputKeys(t, m, tableF7, textKey("5"), textKey("2"), textKey("B1+B1"), enter)
	m = inputKeys(t, m, textKey("5"), textKey("3"), textKey("1"), everydayKey(tea.KeyDown), enter, f7)
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-table-math/COPY.WP"); got != want {
		t.Fatalf("copied body %x, want %x: %s", got, want, m.notice)
	}
}
