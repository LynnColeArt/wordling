package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/layout"
)

func TestDateTextMatchesDOSAndSurvivesRetrieval(t *testing.T) {
	m, root := everydayUI(t)
	m.runtime.now = func() time.Time { return time.Date(1992, time.March, 9, 12, 0, 0, 0, time.UTC) }
	m = inputKeys(t, m, textKey("Literal: "), tea.Key{Code: tea.KeyF5, Mod: tea.ModShift})
	if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, datePrompt) || !strings.Contains(screen, "Literal:") {
		t.Fatal(screen)
	}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, textKey("1"), enter)
	want := lineFormatBody(t, "mission1-dates/LITERAL.WP")
	if got := hBoldBody(t, m); got != want {
		t.Fatalf("native body = %q, want %q", got, want)
	}
	if err := os.WriteFile(filepath.Join(root, "LITERAL.WP"), hBoldNative(t, m), 0600); err != nil {
		t.Fatal(err)
	}
	m.runtime.now = func() time.Time { return time.Date(1992, time.March, 10, 12, 0, 0, 0, time.UTC) }
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModShift}, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift},
		textKey("LITERAL.WP"), enter)
	if got := hBoldBody(t, m); got != want || !strings.Contains(ansi.Strip(m.View().Content), "Literal: March 9, 1992") {
		t.Fatalf("retrieved body = %q, want %q\n%s", got, want, m.View().Content)
	}
}

func TestDateCodeMatchesDOSAndUpdatesOnRetrieval(t *testing.T) {
	m, root := everydayUI(t)
	clock := func(day int) func() time.Time {
		return func() time.Time { return time.Date(1992, time.March, day, 12, 0, 0, 0, time.UTC) }
	}
	m.runtime.now = clock(9)
	dateKey := tea.Key{Code: tea.KeyF5, Mod: tea.ModShift}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, textKey("Literal: "), dateKey, textKey("1"), enter, textKey("Dynamic: "), dateKey, textKey("2"))
	want := lineFormatBody(t, "mission1-dates/DATES.WP")
	original := hBoldNative(t, m)
	if got := hBoldBody(t, m); got != want || !strings.Contains(ansi.Strip(m.View().Content), "Dynamic: March 9, 1992") {
		t.Fatalf("native = %x, want %x\n%s", got, want, m.View().Content)
	}
	exported, err := m.session.Document().ExportDOSTextAt(m.runtime.now())
	plain, e := os.ReadFile("../../docs/research/reference-runs/mission1-dates/DATES.TXT")
	if e != nil || err != nil || !bytes.Equal(exported, plain) {
		t.Fatalf("DOS text = %q, want %q: %v %v", exported, plain, err, e)
	}
	settings := editor.EverydaySettings()
	settings.Date = m.runtime.now()
	pages, err := layout.StandardPages(m.session.Document(), settings)
	if err != nil {
		t.Fatal(err)
	}
	printed, err := os.ReadFile("../../docs/research/reference-runs/mission1-dates/DATES.PRN")
	if err != nil {
		t.Fatal(err)
	}
	if got := layout.StandardPrint(pages); !bytes.Equal(got, printed) {
		t.Fatalf("printer = %q, want %q", got, printed)
	}
	if err := os.WriteFile(filepath.Join(root, "DATES.WP"), original, 0600); err != nil {
		t.Fatal(err)
	}
	m.runtime.now = clock(10)
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModShift}, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey("DATES.WP"), enter)
	screen := ansi.Strip(m.View().Content)
	if got := hBoldBody(t, m); got != want || !strings.Contains(screen, "Literal: March 9, 1992") || !strings.Contains(screen, "Dynamic: March 10, 1992") {
		t.Fatalf("retrieved native = %x, want %x\n%s", got, want, screen)
	}
}
