package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestSubdocumentLinkMatchesDOS(t *testing.T) {
	for _, tc := range []struct {
		before, file, name, fixture string
	}{
		{"Chapter ", "CHAPTER.WP", "CHAPTER.WP", "MASTER.WP"},
		{"", "rich.wp", "RICH.WP", "BEGIN.WP"},
	} {
		t.Run(tc.fixture, func(t *testing.T) {
			m, _ := everydayUI(t)
			if tc.before != "" {
				m = inputKeys(t, m, textKey(tc.before))
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}, textKey("2"))
			if !strings.Contains(ansi.Strip(m.View().Content), "Subdoc Filename:") {
				t.Fatal(m.View().Content)
			}
			m = inputKeys(t, m, textKey(tc.file), everydayKey(tea.KeyEnter), textKey(" end"))
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-subdocuments/"+tc.fixture); got != want {
				t.Fatalf("body %x, want %x: %s", got, want, m.notice)
			}
			if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, "Subdoc: "+tc.name) || !strings.Contains(screen, "Doc 1 Pg 1") {
				t.Fatal(screen)
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
			if !strings.Contains(ansi.Strip(m.View().Content), "[Subdoc:"+tc.name+"]") {
				t.Fatal(m.View().Content)
			}
		})
	}
}
