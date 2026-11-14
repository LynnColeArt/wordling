package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestCustomTabsAndDecimalAlignmentMatchDOS(t *testing.T) {
	for _, absolute := range []bool{false, true} {
		name := "RELATIVE"
		if absolute {
			name = "ABSOLUTE"
		}
		t.Run(name, func(t *testing.T) {
			m, _ := everydayUI(t)
			tab, enter, f7 := everydayKey(tea.KeyTab), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7)
			format := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}
			decimal := tea.Key{Code: tea.KeyF6, Mod: tea.ModCtrl}
			m = inputKeys(t, m, textKey("Before"), tab, textKey("old"), enter, format, textKey("1"), textKey("8"))
			if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, "Ctrl-End (clear tabs)") {
				t.Fatal(screen)
			}
			if absolute {
				m = inputKeys(t, m, textKey("t"), textKey("1"), tea.Key{Code: tea.KeyEnd, Mod: tea.ModCtrl})
			}
			m = inputKeys(t, m, textKey("2.2"), enter, f7, f7, textKey("Some"), tab, textKey("regular"), enter)
			if absolute {
				m = inputKeys(t, m, tab, textKey("absolute"))
			} else {
				m = inputKeys(t, m, textKey("Custom"), tab, tab, tab, textKey("new"), enter, decimal)
				if m.notice != "" {
					t.Fatal(m.notice)
				}
				m = inputKeys(t, m, textKey("12.34"), enter, decimal, textKey("5"), textKey("."), textKey("67"), enter,
					decimal, textKey("123"), enter)
				screen := ansi.Strip(m.View().Content)
				for _, line := range []string{"\n   12.34", "\n    5.67", "\n  123"} {
					if !strings.Contains(screen, line) {
						t.Errorf("%s\nbody %x\nnotice %s", screen, hBoldBody(t, m), m.notice)
					}
				}
			}
			if !absolute {
				checkLineFormatTextExport(t, m, "mission1-custom-tabs/RELATIVE.TXT")
			}
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-custom-tabs/"+name+".WP"); got != want {
				t.Fatalf("body %x\nwant %x\n%s", got, want, m.notice)
			}
		})
	}
}

func TestRulerDecimalStopsMatchDOS(t *testing.T) {
	m, _ := everydayUI(t)
	tab, enter, f7 := everydayKey(tea.KeyTab), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7)
	format := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}
	m = inputKeys(t, m, textKey("Before"), tab, textKey("old"), enter, format, textKey("1"), textKey("8"),
		textKey("2.2"), enter, textKey("d"), f7, f7,
		tab, tab, tab, tab, tab, textKey("12.34"), enter, tab, tab, tab, tab, tab, textKey("5.67"))
	checkLineFormatTextExport(t, m, "mission1-custom-tabs/DECIMAL.TXT")
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-custom-tabs/DECIMAL.WP"); got != want {
		t.Fatalf("body %x\nwant %x\n%s", got, want, m.notice)
	}
}

func TestDecimalTabEndsAtNextTabMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	dec := tea.Key{Code: tea.KeyF6, Mod: tea.ModCtrl}
	m = inputKeys(t, m, dec, textKey("12"), everydayKey(tea.KeyTab), textKey("after tab"), everydayKey(tea.KeyEnter),
		dec, textKey("5"), dec, textKey("2.50"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-custom-tabs/CHAIN.WP"); got != want {
		t.Fatalf("body %x\nwant %x\n%s", got, want, m.notice)
	}
}
