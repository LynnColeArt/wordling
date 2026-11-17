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

func TestPairedBoldStyleCanBeSavedAndReopened(t *testing.T) {
	m, root := everydayUI(t)
	f7, enter, f6 := everydayKey(tea.KeyF7), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF6)
	styles := tea.Key{Code: tea.KeyF8, Mod: tea.ModAlt}
	m = inputKeys(t, m, styles, textKey("3"), textKey("1"), textKey("EMPHASIS"), enter, textKey("4"), f6, f7, f7)
	if len(m.session.Document().NamedStyles()) != 1 {
		t.Fatal(m.View().Content)
	}
	m = inputKeys(t, m, textKey("3"), textKey("1"), textKey("emphasis"), enter)
	if !strings.Contains(ansi.Strip(m.View().Content), "Style name already exists") {
		t.Fatal(m.View().Content)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF1), everydayKey(tea.KeyF1), textKey("1"), textKey("Styled text"))
	want := lineFormatBody(t, "mission1-style-authoring/BOLD.WP")
	got := hBoldBody(t, m)
	normalize := func(body string) []byte {
		raw := []byte(body)
		for i := 0; i+4 < len(raw); i++ {
			if raw[i] != 0xdb || raw[i+1] > 1 {
				continue
			}
			field := i + 14
			if raw[i+1] == 1 {
				field = i + 20
			}
			if field+1 >= len(raw) {
				break
			}
			raw[field], raw[field+1] = 0, 0
			i += int(raw[i+2]) + 3
		}
		return raw
	}
	if !bytes.Equal(normalize(got), normalize(want)) {
		t.Fatalf("got %x, want %x: %s", got, want, m.notice)
	}
	dos, err := os.ReadFile("../../docs/research/reference-runs/mission1-style-authoring/BOLD.WP")
	if err != nil {
		t.Fatal(err)
	}
	d, err := document.Parse(dos)
	if err != nil {
		t.Fatal(err)
	}
	if err = d.CheckMutation(); err != nil {
		t.Fatalf("DOS styled save not writable: %v", err)
	}
	if err = os.WriteFile(filepath.Join(root, "BOLD.WP"), dos, 0600); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModShift}, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey("BOLD.WP"), enter)
	if m.notice != "" || hBoldBody(t, m) != want {
		t.Fatalf("retrieve: %s", m.notice)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyEnd), textKey(" more"))
	if m.notice != "" || !strings.Contains(hBoldBody(t, m), "more") {
		t.Fatalf("edit: %s", m.notice)
	}
}
