package tui

import (
	"bytes"
	"github.com/charmbracelet/x/ansi"
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
)

func TestHistoricMenuExitUsesSessionConfirmations(t *testing.T) {
	runtime, m, err := Open(Config{Root: t.TempDir(), Profile: LocalFlat, EditorChrome: true})
	if err != nil {
		t.Fatal(err)
	}
	defer runtime.Close()
	m, _ = press(m, '=', tea.ModAlt, "=")
	m, _ = press(m, tea.KeyEnter, 0, "")
	m, _ = press(m, 'e', 0, "e")
	if m.session.Snapshot().Mode != editor.ExitSaveQuestion {
		t.Fatal("File Exit must use save confirmation")
	}
	m, _ = press(m, 'n', 0, "n")
	if m.session.Snapshot().Mode != editor.ExitQuestion {
		t.Fatal("missing exit confirmation")
	}
	var cmd tea.Cmd
	m, cmd = press(m, 'y', 0, "y")
	if cmd == nil || m.session.Snapshot().Mode != editor.Exited {
		t.Fatal("exit failed")
	}
}

func TestEditorLineNavigation(t *testing.T) {
	runtime, m, err := Open(Config{Root: t.TempDir(), Profile: LocalFlat, EditorChrome: true})
	if err != nil {
		t.Fatal(err)
	}
	defer runtime.Close()
	key := func(code rune) { m, _ = press(m, code, 0, "") }
	write := func(text string) {
		for _, r := range text {
			m, _ = press(m, r, 0, string(r))
		}
	}
	gap := func(want int) {
		t.Helper()
		s := m.session.Snapshot()
		if s.Gap != want || s.HomePrefix != 0 {
			t.Fatalf("gap = %d, Home prefix = %d; want gap %d and no prefix", s.Gap, s.HomePrefix, want)
		}
	}
	write("first")
	key(tea.KeyEnter)
	write("second")
	key(tea.KeyLeft)
	key(tea.KeyHome)
	if !strings.Contains(m.View().Content, "Esc cancels") {
		t.Fatal("Home prefix hint missing")
	}
	key(tea.KeyEscape)
	gap(11)

	key(tea.KeyHome)
	key(tea.KeyHome)
	key(tea.KeyLeft)
	gap(6)
	key(tea.KeyEnd)
	gap(12)

	key(tea.KeyHome)
	key(tea.KeyHome)
	key(tea.KeyUp)
	key(tea.KeyEnd)
	gap(5)
	key(tea.KeyHome)
	key(tea.KeyHome)
	key(tea.KeyDown)
	gap(12)

	if body := hBoldBody(t, m); body != "first\nsecond" {
		t.Fatalf("navigation changed native body to %q", body)
	}
}

func TestHistoricFileListRetrievesNativeFile(t *testing.T) {
	root := t.TempDir()
	runtime, m, err := Open(Config{Root: root, Profile: LocalFlat, EditorChrome: true})
	if err != nil {
		t.Fatal(err)
	}
	defer runtime.Close()
	native := hBoldNative(t, m)
	if err := os.WriteFile(filepath.Join(root, "SAMPLE"), native, 0600); err != nil {
		t.Fatal(err)
	}
	m, _ = press(m, tea.KeyF5, 0, "")
	if !m.historic.files || len(m.historic.entries) != 1 {
		t.Fatal("F5 did not list file")
	}
	before := m.session.Snapshot()
	m, _ = press(m, tea.KeyF7, 0, "")
	if m.session.Snapshot() != before {
		t.Fatal("leaving List Files changed document")
	}
	m, _ = press(m, tea.KeyF5, 0, "")
	var cmd tea.Cmd
	m, cmd = press(m, tea.KeyEnter, 0, "")
	m = drain(m, cmd)
	if m.session.Snapshot().Name != "SAMPLE" || m.historic.files {
		t.Fatalf("retrieve failed: %+v", m.State())
	}
	if !bytes.Equal(hBoldNative(t, m), native) {
		t.Fatal("retrieval changed native bytes")
	}
}

func TestHistoricMenuPreservesTextAndBacksOut(t *testing.T) {
	runtime, m, err := Open(Config{Root: t.TempDir(), Profile: LocalFlat, EditorChrome: true})
	if err != nil {
		t.Fatal(err)
	}
	defer runtime.Close()
	m, _ = press(m, 'a', 0, "a")
	before := hBoldNative(t, m)
	m, _ = press(m, '=', tea.ModAlt, "=")
	m, _ = press(m, 't', 0, "t")
	m, _ = press(m, 'm', 0, "m")
	if m.historic.sub != "Tools/Macro" {
		t.Fatal("Macro submenu did not open")
	}
	m, _ = press(m, tea.KeyF1, 0, "")
	if m.historic.sub != "" || !m.historic.drop {
		t.Fatal("F1 did not back up one level")
	}
	m, _ = press(m, tea.KeyF7, 0, "")
	if m.historic.menu || !bytes.Equal(before, hBoldNative(t, m)) {
		t.Fatal("menus changed document or failed to close")
	}
	view := ansi.Strip(m.View().Content)
	lines := strings.Split(view, "\n")
	if len(lines) != 25 || lines[1] != "a" || !strings.HasSuffix(lines[24], "Doc 1 Pg -- Ln -- Pos --") {
		t.Fatalf("historical screen geometry: %q", view)
	}
	if strings.Contains(view, "Ctrl+") || strings.Contains(view, "Wordling 5.2") {
		t.Fatal("modern chrome remains")
	}
}

func TestHistoricStartupMenuAndBoundaryKeys(t *testing.T) {
	runtime, m, err := Open(Config{Root: t.TempDir(), Profile: LocalFlat, EditorChrome: true})
	if err != nil {
		t.Fatal(err)
	}
	defer runtime.Close()
	for _, size := range []tea.WindowSizeMsg{{Width: 80, Height: 25}, {Width: 283, Height: 82}} {
		next, _ := m.Update(size)
		m = next.(Model)
		view := m.View()
		if !strings.HasPrefix(ansi.Strip(view.Content), "File Edit Search Layout") || view.Cursor == nil || view.Cursor.Y != 1 {
			t.Fatal("startup menu or document focus missing")
		}
	}
	original := hBoldNative(t, m)
	for _, key := range []rune{tea.KeyLeft, tea.KeyBackspace, tea.KeyRight, tea.KeyDelete} {
		m, _ = press(m, key, 0, "")
		if m.notice != "" || m.session.Snapshot().Gap != 0 || !bytes.Equal(original, hBoldNative(t, m)) {
			t.Fatalf("empty boundary key %v failed: %s", key, m.notice)
		}
	}
	m, _ = press(m, 'a', 0, "a")
	if hBoldBody(t, m) != "a" {
		t.Fatal("visible menu swallowed typing")
	}
	next, _ := m.Update(tea.MouseClickMsg{X: 1, Y: 0, Button: tea.MouseLeft})
	m = next.(Model)
	if !m.historic.menu || !m.historic.drop {
		t.Fatal("File click did not open menu")
	}
	m, _ = press(m, tea.KeyF7, 0, "")
	if m.historic.menu || !m.historic.bar {
		t.Fatal("closing menu lost bar or kept focus")
	}
	m, _ = press(m, 'b', 0, "b")
	if hBoldBody(t, m) != "ab" {
		t.Fatal("typing did not resume")
	}
}
