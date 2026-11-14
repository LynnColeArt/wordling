package tui

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestSortSecondaryMergeRecordsMatchesDOS(t *testing.T) {
	m, root := everydayUI(t)
	raw, err := os.ReadFile("../../docs/research/reference-runs/mission1-sort/BEFORE.WP")
	if err != nil {
		t.Fatal(err)
	}
	if err = os.WriteFile(filepath.Join(root, "BEFORE.WP"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey("BEFORE.WP"), enter,
		tea.Key{Code: tea.KeyF9, Mod: tea.ModCtrl}, textKey("2"), enter, enter, textKey("7"), textKey("1"))
	if view := ansi.Strip(m.View().Content); !strings.Contains(view, "Sort Secondary Merge File") || !strings.Contains(view, "Ascending") {
		t.Fatal(view, m.notice)
	}
	m = inputKeys(t, m, textKey("1"))
	if want, got := lineFormatBody(t, "mission1-sort/SORTED.WP"), hBoldBody(t, m); want != got {
		t.Fatalf("sorted %x, want %x: %s", got, want, m.notice)
	}
	if view := ansi.Strip(m.View().Content); strings.Index(view, "Amber") >= strings.Index(view, "Zebra") || !strings.Contains(view, "Keep A") {
		t.Fatal(view)
	}
}
