package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestLiteralPrinterCommandMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, textKey("Before"), tea.Key{Code: tea.KeyF8, Mod: tea.ModShift},
		textKey("4"), textKey("6"), textKey("2"), textKey("1"))
	if !strings.Contains(ansi.Strip(m.View().Content), "Command:") {
		t.Fatal(m.View().Content)
	}
	m = inputKeys(t, m, textKey("<36>TEST"), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7), textKey("After"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-printer-command/PRTCMD.WP"); got != want {
		t.Fatalf("got %x, want %x: %s", got, want, m.notice)
	}
	if view := ansi.Strip(m.View().Content); !strings.Contains(view, "BeforeAfter") || strings.Contains(view, "$TEST") {
		t.Fatal(view)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if !strings.Contains(ansi.Strip(m.View().Content), "[Ptr Cmnd:$TEST]") {
		t.Fatal(m.View().Content)
	}
}
