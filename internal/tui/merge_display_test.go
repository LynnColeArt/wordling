package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
)

func TestOriginalMergeOwnersDisplayWithoutMutationAuthority(t *testing.T) {
	cases := []struct {
		file          string
		normal, codes map[int]string
	}{
		{"PRIMARY.WP5", map[int]string{1: "Hello {FIELD}1~", 2: "========"}, map[int]string{13: "Hello [Mrg:FIELD]1~[HPg]"}},
		{"SECOND.WP5", map[int]string{1: "Alice{END FIELD}", 2: "{END RECORD}", 3: "========", 4: "Bob{END FIELD}"}, map[int]string{13: "Alice[Mrg:END FIELD][HRt]", 14: "[Mrg:END RECORD][HPg]", 15: "Bob[Mrg:END FIELD][HRt]"}},
	}
	for _, tc := range cases {
		t.Run(tc.file, func(t *testing.T) {
			m, root := everydayUI(t)
			raw, err := os.ReadFile(filepath.Join("../../docs/research/reference-runs/2026-10-29-extended-04/CMD51-134", tc.file))
			if err != nil {
				t.Fatal(err)
			}
			if err := os.WriteFile(filepath.Join(root, tc.file), raw, 0600); err != nil {
				t.Fatal(err)
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey(tc.file), everydayKey(tea.KeyEnter))
			assertScreenRows(t, m, tc.normal)
			if err := m.Session().Document().CheckMutation(); err == nil {
				t.Fatal("recognized merge display owners acquired mutation authority")
			} else if f, ok := err.(*document.Failure); !ok || f.Category != document.UnsupportedBody {
				t.Fatalf("unexpected mutation refusal: %v", err)
			}
			m = inputKeys(t, m, everydayKey(tea.KeyF11))
			assertScreenRows(t, m, tc.codes)
			if !bytes.Equal(hBoldNative(t, m), raw) {
				t.Fatal("merge display changed native bytes")
			}
		})
	}
}
