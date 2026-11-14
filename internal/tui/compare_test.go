package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestCompareScreenAndDiskMatchesDOS(t *testing.T) {
	m, root := everydayUI(t)
	source := filepath.Join(root, "BEFORE.WP")
	raw, err := os.ReadFile("../../docs/research/reference-runs/mission1-document-compare/BEFORE.WP")
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(source, raw, 0600); err != nil {
		t.Fatal(err)
	}
	altF5 := tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, textKey("Alpha new tail"), altF5, textKey("6"), textKey("2"),
		textKey("MISSING.WP"), enter)
	if m.notice == "" || hBoldBody(t, m) != "Alpha new tail" {
		t.Fatalf("missing source changed current text: %q", m.notice)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF1), altF5, textKey("6"), textKey("2"), textKey("BEFORE.WP"), enter)
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-document-compare/COMPARE.WP"); got != want {
		t.Fatalf("native compare differs:\ngot  %x\nwant %x\n%s", got, want, m.notice)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	view := ansi.Strip(m.View().Content)
	if !strings.Contains(view, "[REDLN]Alpha new tail[redln][STKOUT]Alpha old tail[stkout]") {
		t.Fatal(view)
	}
	after, err := os.ReadFile(source)
	if err != nil || !bytes.Equal(after, raw) {
		t.Fatalf("comparison changed disk version: %v", err)
	}
}

func TestComparePreservesUnchangedParagraphs(t *testing.T) {
	m, root := everydayUI(t)
	raw, err := os.ReadFile("../../docs/research/reference-runs/mission1-document-compare/MULBEFR.WP")
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(root, "MULBEFR.WP"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, textKey("Overview"), enter, textKey("Alpha new tail"), enter, textKey("Closing"),
		tea.Key{Code: tea.KeyF5, Mod: tea.ModAlt}, textKey("6"), textKey("2"), textKey("MULBEFR.WP"), enter)
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-document-compare/MULTI.WP"); got != want {
		t.Fatalf("native compare differs:\ngot  %x\nwant %x\n%s", got, want, m.notice)
	}
}
