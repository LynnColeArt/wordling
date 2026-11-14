package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestMarkContentsLevelsMatchDOS(t *testing.T) {
	for _, level := range []string{"1", "5"} {
		t.Run(level, func(t *testing.T) {
			m, _ := everydayUI(t)
			m = inputKeys(t, m, textKey("Overview"))
			for range len("Overview") {
				m = inputKeys(t, m, everydayKey(tea.KeyLeft))
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt}, everydayKey(tea.KeyEnd),
				tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}, textKey("1"))
			if !strings.Contains(ansi.Strip(m.View().Content), "ToC Level:") {
				t.Fatal(m.View().Content)
			}
			m = inputKeys(t, m, textKey(level), everydayKey(tea.KeyEnter))
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-toc-mark/LEVEL"+level+".WP"); got != want || m.session.Snapshot().Selection {
				t.Fatalf("body %x, want %x: %s", got, want, m.notice)
			}
		})
	}
}

func TestGenerateContentsMatchesDOSAndCanBeDeclined(t *testing.T) {
	m, _ := everydayUI(t)
	mark := tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}
	f7 := everydayKey(tea.KeyF7)
	m = inputKeys(t, m, mark, textKey("5"), textKey("1"), f7)
	m = markHeading(t, m, "Overview")
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-toc-generation/DEFIN.WP"); got != want {
		t.Fatalf("definition %x, want %x", got, want)
	}
	m = inputKeys(t, m, mark, textKey("6"), textKey("5"))
	if !strings.Contains(ansi.Strip(m.View().Content), "Existing tables, lists, and indexes will be replaced.") {
		t.Fatal(m.View().Content)
	}
	revision := m.session.Snapshot().NativeRevision
	m = inputKeys(t, m, textKey("n"))
	if m.session.Snapshot().NativeRevision != revision {
		t.Fatal("declining changed the document")
	}
	m = inputKeys(t, m, mark, textKey("6"), textKey("5"), textKey("y"))
	want := lineFormatBody(t, "mission1-toc-generation/GEN.WP")
	if got := hBoldBody(t, m); got != want {
		t.Fatalf("generated %x, want %x: %s", got, want, m.notice)
	}
	if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, "Overview . . . .") {
		t.Fatal(screen)
	}
	m = inputKeys(t, m, mark, textKey("6"), textKey("5"), textKey("y"))
	if got := hBoldBody(t, m); got != want {
		t.Fatalf("regenerated %x, want %x: %s", got, want, m.notice)
	}
}

func markHeading(t *testing.T, m Model, heading string, level ...string) Model {
	t.Helper()
	m = inputKeys(t, m, textKey(heading))
	for range len(heading) {
		m = inputKeys(t, m, everydayKey(tea.KeyLeft))
	}
	n := "1"
	if len(level) != 0 {
		n = level[0]
	}
	return inputKeys(t, m, tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt}, everydayKey(tea.KeyEnd),
		tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}, textKey("1"), textKey(n), everydayKey(tea.KeyEnter))
}

func TestGenerateTwoPageContentsMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	mark := tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}
	m = inputKeys(t, m, mark, textKey("5"), textKey("1"), everydayKey(tea.KeyF7))
	m = markHeading(t, m, "Overview")
	m = inputKeys(t, m, tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl})
	m = markHeading(t, m, "Results")
	if want, got := lineFormatBody(t, "mission1-toc-generation/TWODEF.WP"), hBoldBody(t, m); want != got {
		t.Fatalf("definition %x, want %x: %s", got, want, m.notice)
	}
	m = inputKeys(t, m, mark, textKey("6"), textKey("5"), textKey("y"))
	if want, got := lineFormatBody(t, "mission1-toc-generation/TWOGEN.WP"), hBoldBody(t, m); want != got {
		t.Fatalf("generated %x, want %x: %s", got, want, m.notice)
	}
}

func TestGenerateTwoLevelContentsMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	mark := tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}
	m = inputKeys(t, m, mark, textKey("5"), textKey("1"), textKey("1"), textKey("2"), everydayKey(tea.KeyF7))
	m = markHeading(t, m, "Overview")
	m = inputKeys(t, m, tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl})
	m = markHeading(t, m, "Results", "2")
	if want, got := lineFormatBody(t, "mission1-toc-generation/LVLDEF.WP"), hBoldBody(t, m); want != got {
		t.Fatalf("definition %x, want %x: %s", got, want, m.notice)
	}
	m = inputKeys(t, m, mark, textKey("6"), textKey("5"), textKey("y"))
	if want, got := lineFormatBody(t, "mission1-toc-generation/LVLGEN.WP"), hBoldBody(t, m); want != got {
		t.Fatalf("generated %x, want %x: %s", got, want, m.notice)
	}
	if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, "     Results . .") {
		t.Fatal(screen)
	}
}
