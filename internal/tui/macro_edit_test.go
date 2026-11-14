package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
)

func TestEditExistingMacroMatchesDOS(t *testing.T) {
	const ref = "../../docs/research/reference-runs/"
	read := func(p string) []byte {
		t.Helper()
		raw, err := os.ReadFile(p)
		if err != nil {
			t.Fatal(err)
		}
		return raw
	}
	original := read(ref + "mission1-macro-recording/TYPED.WPM")
	ctrl := tea.Key{Code: tea.KeyF10, Mod: tea.ModCtrl}
	enter, f7, f1 := everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7), everydayKey(tea.KeyF1)
	right, left := everydayKey(tea.KeyRight), everydayKey(tea.KeyLeft)
	insertCommand := tea.Key{Code: 'v', Mod: tea.ModCtrl}
	for _, scenario := range []string{"action", "description", "cancel", "stale", "reverted"} {
		t.Run(scenario, func(t *testing.T) {
			m, root := everydayUI(t)
			path := filepath.Join(root, "TYPED.WPM")
			if err := os.WriteFile(path, original, 0600); err != nil {
				t.Fatal(err)
			}
			m = inputKeys(t, m, textKey("Document untouched"), ctrl, textKey("TYPED"), enter)
			doc := hBoldNative(t, m)
			var want []byte
			if scenario == "description" {
				m = inputKeys(t, m, textKey("3"), everydayKey(tea.KeyEnd))
				if !strings.Contains(m.View().Content, "Description: Keys and text") {
					t.Fatal(m.View().Content)
				}
				for range len("Keys and text") {
					m = inputKeys(t, m, everydayKey(tea.KeyBackspace))
				}
				m = inputKeys(t, m, textKey("Revised"), enter)
				if !strings.Contains(m.View().Content, "Description      Revised") {
					t.Fatal(m.View().Content)
				}
				want = read(ref + "mission1-macro-edit/DESCR.WPM")
			} else {
				m = inputKeys(t, m, textKey("2"), right, textKey("Z"))
				if scenario == "reverted" {
					m = inputKeys(t, m, everydayKey(tea.KeyBackspace))
					want = original
				} else {
					m = inputKeys(t, m, everydayKey(tea.KeyDelete))
					want = read(ref + "mission1-macro-edit/ACTION.WPM")
					if !strings.Contains(m.View().Content, "{DISPLAY OFF}Z·B{Enter}") {
						t.Fatal(m.View().Content)
					}
				}
			}
			if !bytes.Equal(read(path), original) || !bytes.Equal(doc, hBoldNative(t, m)) {
				t.Fatal("macro editing committed changes too early")
			}
			switch scenario {
			case "cancel":
				m = inputKeys(t, m, f1, enter)
				if m.recording.stage != recordInspect || m.recording.discard {
					t.Fatal("default answer should keep the editor open")
				}
				m = inputKeys(t, m, f1, textKey("y"))
				want = original
			case "stale":
				want = read(ref + "mission1-macro-recording/REPLACED.WPM")
				newer := filepath.Join(root, "NEWER.WPM")
				if err := os.WriteFile(newer, want, 0600); err != nil {
					t.Fatal(err)
				}
				if err := os.Rename(newer, path); err != nil {
					t.Fatal(err)
				}
				m = inputKeys(t, m, f7)
				if m.notice == "" || m.recording.stage != recordInspect {
					t.Fatal("stale editor should retain the unsaved buffer and report a conflict")
				}
			case "reverted":
				before, err := os.Stat(path)
				if err != nil {
					t.Fatal(err)
				}
				m = inputKeys(t, m, f7)
				after, err := os.Stat(path)
				if err != nil || !os.SameFile(before, after) {
					t.Fatalf("reverted edit rewrote the source: %v", err)
				}
			default:
				m = inputKeys(t, m, f7)
			}
			if got := read(path); !bytes.Equal(got, want) {
				t.Fatalf("got %x, want %x; notice %q", got, want, m.notice)
			}
			if !bytes.Equal(doc, hBoldNative(t, m)) {
				t.Fatal("macro edit changed the document")
			}
		})
	}

	t.Run("insert-command", func(t *testing.T) {
		m, root := everydayUI(t)
		path := filepath.Join(root, "TYPED.WPM")
		if err := os.WriteFile(path, original, 0600); err != nil {
			t.Fatal(err)
		}
		m = inputKeys(t, m, ctrl, textKey("TYPED"), enter, textKey("2"), right, right, insertCommand, left, f7)
		if got, want := read(path), read(ref+"mission1-macro-edit/LEFT.WPM"); !bytes.Equal(got, want) {
			t.Fatalf("got %x, want %x; notice %q", got, want, m.notice)
		}
	})
}
