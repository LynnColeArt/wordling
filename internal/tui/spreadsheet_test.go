package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/document"
)

func TestSpreadsheetImportAndRefreshMatchesDOS(t *testing.T) {
	const reference = "../../docs/research/reference-runs/mission1-spreadsheet/"
	read := func(name string) []byte {
		t.Helper()
		b, err := os.ReadFile(reference + name)
		if err != nil {
			t.Fatal(err)
		}
		return b
	}
	ctrlF5 := tea.Key{Code: tea.KeyF5, Mod: tea.ModCtrl}
	enter := everydayKey(tea.KeyEnter)
	for _, command := range []string{"1", "2"} {
		t.Run(command, func(t *testing.T) {
			m, root := everydayUI(t)
			worksheet := filepath.Join(root, "OUT", "RANGE.WK1")
			if err := os.Mkdir(filepath.Dir(worksheet), 0700); err != nil {
				t.Fatal(err)
			}
			write := func(raw []byte) {
				t.Helper()
				if err := os.WriteFile(worksheet, raw, 0600); err != nil {
					t.Fatal(err)
				}
			}
			raw := read("RANGE.WK1")
			write(raw)
			link, err := document.Parse(read("LINK.WP"))
			if err != nil {
				t.Fatal(err)
			}
			fixture, ok := link.SpreadsheetTable()
			if !ok || fixture.Link == nil {
				t.Fatal("DOS link fixture was not recognized")
			}
			ts := fixture.Link.Modified
			if err := os.Chtimes(worksheet, ts, ts); err != nil {
				t.Fatal(err)
			}
			m = inputKeys(t, m, ctrlF5, textKey("5"), textKey(command), textKey("1"),
				textKey("C:\\OUT\\RANGE.WK1"), enter, textKey("2"), textKey("A1..B2"), enter, textKey("4"))
			name := "IMPORT.WP"
			if command == "2" {
				name = "LINK.WP"
			}
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-spreadsheet/"+name); got != want {
				t.Fatalf("native %s differs:\ngot  %x\nwant %x\n%s", name, got, want, m.notice)
			}
			screen := ansi.Strip(m.View().Content)
			if !strings.Contains(screen, "Amber") || !strings.Contains(screen, "│       7 ") || strings.Contains(screen, "Outside") {
				t.Fatal(screen)
			}
			if command == "1" {
				return
			}
			// A broken source must leave both the cache and the native link intact.
			write(raw[:10])
			before := hBoldNative(t, m)
			m = inputKeys(t, m, ctrlF5, textKey("5"), textKey("4"), textKey("3"))
			if m.notice == "" || !bytes.Equal(before, hBoldNative(t, m)) {
				t.Fatalf("failed refresh changed cache: %q", m.notice)
			}
			at := bytes.Index(raw, []byte{13, 0, 7, 0, 255, 1, 0, 1, 0, 7, 0})
			if at < 0 {
				t.Fatal("fixture has no integer 7 at B2")
			}
			raw[at+9] = 19
			write(raw)
			if !bytes.Equal(before, hBoldNative(t, m)) {
				t.Fatal("changing the source changed the cached table")
			}
			m = inputKeys(t, m, textKey("3"))
			got, want := []byte(hBoldBody(t, m)), []byte(lineFormatBody(t, "mission1-spreadsheet/UPDATED.WP"))
			if len(got) < 12 || len(want) < 12 || !bytes.Equal(got[:8], want[:8]) || !bytes.Equal(got[12:], want[12:]) {
				t.Fatalf("refreshed native body differs:\ngot  %x\nwant %x\n%s", got, want, m.notice)
			}
			after, err := os.ReadFile(worksheet)
			if err != nil || !bytes.Equal(after, raw) {
				t.Fatalf("refresh changed worksheet bytes: %v", err)
			}
		})
	}
}

func TestSpreadsheetOffsetRangeAndSignedIntegers(t *testing.T) {
	m, root := everydayUI(t)
	raw, err := os.ReadFile("../../docs/research/reference-runs/mission1-spreadsheet/OFFSET.WK1")
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(root, "OFFSET.WK1"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF5, Mod: tea.ModCtrl}, textKey("5"),
		textKey("1"), textKey("1"), textKey("OFFSET.WK1"), everydayKey(tea.KeyEnter),
		textKey("2"), textKey("b2:c3"), everydayKey(tea.KeyEnter), textKey("4"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-spreadsheet/OFFSET.WP"); got != want {
		t.Fatalf("offset native range differs:\ngot  %x\nwant %x\n%s", got, want, m.notice)
	}
	screen := ansi.Strip(m.View().Content)
	if !strings.Contains(screen, "║     -19  │      91 ║") || !strings.Contains(screen, "║      25  │      42 ║") {
		t.Fatal(screen)
	}
}
