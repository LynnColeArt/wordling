package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestJoinTopTableCellsMatchesDOS(t *testing.T) {
	m := newTwoByTwoTable(t)
	tab := everydayKey(tea.KeyTab)
	m = inputKeys(t, m, textKey("ALPHA"), tab, textKey("BETA"), tab, textKey("GAMMA"), tab, textKey("DELTA"),
		everydayKey(tea.KeyUp), everydayKey(tea.KeyHome), everydayKey(tea.KeyLeft), tableF7)
	block := tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt}
	right := everydayKey(tea.KeyRight)
	selectRow := func(m Model) Model {
		return inputKeys(t, m, block, right, textKey("7"))
	}
	m = selectRow(m)
	if !strings.Contains(ansi.Strip(m.View().Content), "Join cells? No (Yes)") {
		t.Fatal(m.View().Content)
	}
	prior := m.session.Snapshot().NativeRevision
	m = inputKeys(t, m, textKey("n"))
	if m.session.Snapshot().NativeRevision != prior {
		t.Fatal("declining changed the table")
	}
	m = inputKeys(t, m, everydayKey(tea.KeyHome), everydayKey(tea.KeyLeft))
	m = selectRow(m)
	m = inputKeys(t, m, textKey("y"), everydayKey(tea.KeyF7))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-table-join/ROWJOIN.WP"); got != want {
		t.Fatalf("joined body %x, want %x: %s", got, want, m.notice)
	}
	if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, "║ALPHA                           BETA") ||
		!strings.Contains(screen, "║GAMMA                          │DELTA") {
		t.Fatal(screen)
	}
	m = inputKeys(t, m, tab)
	if !strings.Contains(ansi.Strip(m.View().Content), "Cell A2") {
		t.Fatal("Tab did not skip the covered cell")
	}
}
