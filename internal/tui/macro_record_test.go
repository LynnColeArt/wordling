package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

func TestRecordAndReplayNativeWPM(t *testing.T) {
	ctrl := tea.Key{Code: tea.KeyF10, Mod: tea.ModCtrl}
	enter, left := everydayKey(tea.KeyEnter), everydayKey(tea.KeyLeft)
	const refs = "../../docs/research/reference-runs/"
	for _, tc := range []struct {
		name, description, fixture, single, doubled string
		run                                         []tea.Key
	}{
		{"TESTMAC", "Recorded test", refs + "2026-10-29-extended-04/CMD51-131/TESTMAC.WPM",
			"ABC", "ABCABC", []tea.Key{textKey("ABC")}},
		{"TYPED", "Keys and text", refs + "mission1-macro-recording/TYPED.WPM",
			"A B\nC", "A B\nA B\nCC", []tea.Key{textKey("A B"), enter, textKey("C"), left}},
	} {
		t.Run(tc.name, func(t *testing.T) {
			m, root := everydayUI(t)
			if err := os.Mkdir(filepath.Join(root, "OUT"), 0700); err != nil {
				t.Fatal(err)
			}
			path := filepath.Join(root, "OUT", tc.name+".WPM")
			source, err := os.ReadFile(tc.fixture)
			if err != nil {
				t.Fatal(err)
			}
			name := "C:\\OUT\\" + tc.name
			m = inputKeys(t, m, ctrl, textKey(name), enter, textKey(tc.description), enter)
			m = inputKeys(t, m, tc.run...)
			m = inputKeys(t, m, ctrl)
			got, err := os.ReadFile(path)
			if err != nil || !bytes.Equal(got, source) || hBoldBody(t, m) != tc.single {
				t.Fatalf("recorded %x (%v), body %q, notice %q", got, err, hBoldBody(t, m), m.notice)
			}
			m, cmd := press(m, tea.KeyF10, tea.ModAlt, "")
			m = inputKeys(t, m, textKey(name))
			m, cmd = press(m, tea.KeyEnter, 0, "")
			m, _ = drainNewMacro(t, m, cmd)
			if hBoldBody(t, m) != tc.doubled || m.macroStatus.State != "complete" {
				t.Fatalf("played %q, status %+v, notice %q", hBoldBody(t, m), m.macroStatus, m.notice)
			}
			// The default response to the original overwrite question refuses replacement.
			m = inputKeys(t, m, ctrl, textKey(name), enter, textKey("1"), enter)
			if m.recording.stage != recordExisting {
				t.Fatalf("default answer replaced the macro: %q", m.notice)
			}
			m = inputKeys(t, m, everydayKey(tea.KeyF1))
			after, err := os.ReadFile(path)
			if err != nil || !bytes.Equal(after, source) {
				t.Fatalf("collision did not preserve macro: %v %q", err, m.notice)
			}
			m = inputKeys(t, m, ctrl, textKey("CANCEL"), enter, textKey("Cancelled"), enter, textKey("Y"), everydayKey(tea.KeyF1))
			if _, err = os.Stat(filepath.Join(root, "CANCEL.WPM")); !os.IsNotExist(err) || m.recording.stage != 0 {
				t.Fatalf("cancelled recording exists: %v", err)
			}
		})
	}
}

func TestMacroRecordingReplacementMatchesDOSAndRejectsStaleTarget(t *testing.T) {
	const refs = "../../docs/research/reference-runs/mission1-macro-recording/"
	m, root := everydayUI(t)
	path := filepath.Join(root, "TYPED.WPM")
	read := func(name string) []byte {
		t.Helper()
		b, err := os.ReadFile(name)
		if err != nil {
			t.Fatal(err)
		}
		return b
	}
	source := read(refs + "TYPED.WPM")
	if err := os.WriteFile(path, source, 0600); err != nil {
		t.Fatal(err)
	}
	ctrl := tea.Key{Code: tea.KeyF10, Mod: tea.ModCtrl}
	enter := everydayKey(tea.KeyEnter)
	start := func(m Model) Model {
		return inputKeys(t, m, ctrl, textKey("TYPED"), enter, textKey("1"), textKey("y"),
			textKey("New description"), enter, textKey("Q"))
	}
	m = start(m)
	if !bytes.Equal(read(path), source) {
		t.Fatal("replacement published before recording ended")
	}
	m = inputKeys(t, m, ctrl)
	want := read(refs + "REPLACED.WPM")
	if got := read(path); !bytes.Equal(got, want) {
		t.Fatalf("got %x, want %x (%s)", got, want, m.notice)
	}
	m = start(m)
	rename := filepath.Join(root, "NEWER.WPM")
	if err := os.WriteFile(rename, source, 0600); err != nil {
		t.Fatal(err)
	}
	if err := os.Rename(rename, path); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, ctrl)
	if !bytes.Equal(read(path), source) || m.notice == "" {
		t.Fatalf("stale confirm replaced a newer WPM: %q", m.notice)
	}
	m = inputKeys(t, m, ctrl, textKey("EMPTY"), enter, enter, textKey("Q"), ctrl)
	if got, want := read(filepath.Join(root, "EMPTY.WPM")), read(refs+"EMPTY.WPM"); !bytes.Equal(got, want) {
		t.Fatalf("empty description: got %x, want %x", got, want)
	}
}

func TestF1StopsOrdinaryEditorMacroAndKeepsPartialEdits(t *testing.T) {
	m, root := everydayUI(t)
	keys := make([]uint16, 250)
	for i := range keys {
		keys[i] = 'X'
	}
	raw, err := wpm.EncodeRecording("Long text", keys)
	if err != nil {
		t.Fatal(err)
	}
	if err = os.WriteFile(filepath.Join(root, "LONG.WPM"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	m, cmd := queuedMacro(t, m, "LONG")
	for i := 0; i < 20 && cmd != nil && m.macroStatus.AppliedWords == 0; i++ {
		next, pending := m.Update(cmd())
		m, cmd = next.(Model), pending
	}
	if cmd == nil || !m.macroStatus.Active || m.macroStatus.AppliedWords == 0 {
		t.Fatalf("macro never reached a partial run: %+v", m.macroStatus)
	}
	partial := hBoldNative(t, m)
	m, stop := press(m, tea.KeyF1, 0, "")
	if stop != nil {
		t.Fatal("an admitted worker already exists")
	}
	m, _ = drainNewMacro(t, m, cmd)
	if m.macroStatus.State != "stopped" || m.macroStatus.Active || !bytes.Equal(hBoldNative(t, m), partial) {
		t.Fatalf("stop lost or added edits: %+v", m.macroStatus)
	}
	m = inputKeys(t, m, textKey("Y"))
	if bytes.Equal(hBoldNative(t, m), partial) {
		t.Fatal("manual editing did not resume")
	}
}

func TestInspectAndCloseOriginalWPMKeepsBytes(t *testing.T) {
	m, root := everydayUI(t)
	fixture, err := os.ReadFile("../../docs/research/reference-runs/mission1-macro-recording/TYPED.WPM")
	if err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(root, "TYPED.WPM")
	if err := os.WriteFile(path, fixture, 0600); err != nil {
		t.Fatal(err)
	}
	ctrl := tea.Key{Code: tea.KeyF10, Mod: tea.ModCtrl}
	m = inputKeys(t, m, ctrl, textKey("TYPED"), everydayKey(tea.KeyEnter), textKey("2"))
	for _, cue := range []string{"Macro: Action", "Keys and text", "{DISPLAY OFF}A·B{Enter}", "C{Left}"} {
		if !strings.Contains(m.View().Content, cue) {
			t.Fatal(m.View().Content)
		}
	}
	info, err := os.Stat(path)
	if err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF7))
	after, err := os.Stat(path)
	if err != nil || !os.SameFile(info, after) || after.ModTime() != info.ModTime() || m.recording.stage != 0 {
		t.Fatalf("closing untouched WPM changed the file: %v %s", err, m.notice)
	}
	if got, err := os.ReadFile(path); err != nil || !bytes.Equal(got, fixture) {
		t.Fatalf("closing changed original WPM bytes: %v", err)
	}
}
