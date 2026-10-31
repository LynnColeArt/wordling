package editor_test

import (
	"bytes"
	"encoding/json"
	"github.com/lynncoleart/wordling/internal/editor"
	"os"
	"path/filepath"
	"testing"
)

func loadNative(t *testing.T, raw []byte) (editor.Session, fixture) {
	t.Helper()
	f := setup(t)
	if err := os.WriteFile(filepath.Join(f.path, "ORIGIN"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	return load(t, f), f
}
func browse(t *testing.T, s editor.Session, n int) editor.Session {
	t.Helper()
	s = key(t, s, editor.F1)
	for range n {
		s = key(t, s, editor.Previous)
	}
	return key(t, s, editor.F1)
}
func originalRows(t *testing.T, name, repeat, label string) []string {
	t.Helper()
	raw, err := os.ReadFile("../../docs/research/continuation/code-pair-history/observations.json")
	if err != nil {
		t.Fatal(err)
	}
	var ledger struct {
		Observations struct {
			Cases []struct {
				Plan struct {
					ID string `json:"id"`
				} `json:"plan"`
				Samples []struct {
					RunID string `json:"run_id"`
					Menus []struct {
						Label string   `json:"label"`
						Rows  []string `json:"whole_overlaid_rows"`
					} `json:"menus"`
				} `json:"samples"`
			} `json:"cases"`
		} `json:"observations"`
	}
	if err = json.Unmarshal(raw, &ledger); err != nil {
		t.Fatal(err)
	}
	for _, c := range ledger.Observations.Cases {
		if c.Plan.ID != name {
			continue
		}
		for _, sample := range c.Samples {
			if sample.RunID != "wp40-"+name+"-"+repeat {
				continue
			}
			for _, menu := range sample.Menus {
				if menu.Label == label {
					return menu.Rows
				}
			}
		}
	}
	t.Fatal("missing original rows")
	return nil
}
func TestActualWP40CommandsThroughSession(t *testing.T) {
	for _, view := range []string{"normal", "reveal"} {
		for _, direction := range []string{"delete", "backspace"} {
			for _, target := range []string{"on", "off"} {
				for _, repeat := range []string{"r1", "r2"} {
					name := "direct-" + view + "-" + direction + "-" + target
					t.Run(name+"-"+repeat, func(t *testing.T) { replay40(t, name, repeat, view, direction, target) })
				}
			}
		}
	}
	for _, r := range []string{"r1", "r2"} {
		t.Run("closing-"+r, func(t *testing.T) { replay40(t, "closing-block-repair-yes", r, "reveal", "block", "off") })
	}
}
func replay40(t *testing.T, name, repeat, view, direction, target string) {
	t.Helper()
	root := "../../docs/research/continuation/code-pair-history/runs/wp40-" + name + "-" + repeat
	raw, err := os.ReadFile(root + "/N0000.WP5")
	if err != nil {
		t.Fatal(err)
	}
	s, _ := loadNative(t, raw)
	if view == "reveal" {
		s = key(t, s, editor.Reveal)
	}
	s = key(t, s, editor.Delete)
	s = browse(t, s, 3)
	gap := 1
	if target == "off" {
		gap = 4
	}
	if direction == "backspace" {
		gap++
	}
	for s.Snapshot().Gap < gap {
		s = key(t, s, editor.Right)
	}
	if direction == "block" {
		s = key(t, s, editor.Block)
		s = key(t, s, editor.Right)
	}
	command := editor.Delete
	if direction == "backspace" {
		command = editor.Backspace
	}
	s = key(t, s, command)
	if s.Snapshot().Mode == editor.DeleteQuestion {
		s = key(t, s, editor.Yes)
	}
	if s.Snapshot().HistoryCountKnown {
		t.Fatal("unknown count promoted to actual count")
	}
	// Closing preview adds two code tokens; normal projection ignores both.
	s = matchPreview40(t, s, originalRows(t, name, repeat, "immediate-target-history"))
	s = key(t, key(t, s, editor.F1), editor.Restore)
	s = matchPreview40(t, s, originalRows(t, name, repeat, "post-restore-history"))
	s = text(t, s, "X")
	got, _ := s.Document().Export()
	want, err := os.ReadFile(root + "/N0001.WP5")
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(got, want) {
		t.Fatal("actual session native output differs from original")
	}
	if s.Snapshot().HistoryQualified {
		t.Fatal("post-marker history invented")
	}
}
func matchPreview40(t *testing.T, s editor.Session, rows []string) editor.Session {
	t.Helper()
	s = key(t, s, editor.F1)
	for i, row := range rows {
		// The public overlay reports total size independently of stored stack count.
		first, err := s.Preview(0, 0)
		if err != nil {
			t.Fatal(err)
		}
		p, err := s.Preview(0, first.TotalTokens)
		if err != nil {
			t.Fatal(err)
		}
		got := ""
		for _, v := range p.Elements {
			if len(v.Raw) == 1 {
				got += string(v.Raw)
			}
		}
		if got != row {
			t.Fatalf("whole original overlay%q !=%q", got, row)
		}
		if i < 3 {
			s = key(t, s, editor.Previous)
		}
	}
	expectRefusal(t, s, editor.Event{Command: editor.Previous})
	return key(t, s, editor.F1)
}
func TestNormalQuestionAndRevealBlockDeclines(t *testing.T) {
	for _, view := range []bool{false, true} {
		for _, answer := range []editor.Command{editor.No, editor.F1, editor.Escape} {
			t.Run(string(rune('A'+answer))+map[bool]string{true: "block", false: "normal"}[view], func(t *testing.T) {
				f := setup(t)
				s := load(t, f)
				if view {
					s = key(t, s, editor.Reveal)
				}
				s = key(t, s, editor.Right)
				if view {
					s = key(t, s, editor.Block)
					s = key(t, s, editor.Right)
				}
				s = key(t, s, editor.Delete)
				if s.Snapshot().Mode != editor.DeleteQuestion {
					t.Fatal("question absent")
				}
				s = key(t, s, answer)
				raw, _ := s.Document().Export()
				if !bytes.Equal(raw, f.raw) || s.Snapshot().Gap != 2 || s.Snapshot().Dirty {
					t.Fatal("decline altered bytes/cursor")
				}
				if s.Snapshot().Selection != view {
					t.Fatal("decline selection")
				}
				if view {
					s = key(t, s, editor.F1)
					if s.Snapshot().Selection {
						t.Fatal("separate F1 block cleanup")
					}
				}
			})
		}
	}
}
func TestUnbrowsedPairAndUnknownHistoryStayRefused(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	s = key(t, key(t, s, editor.Reveal), editor.Right)
	expectRefusal(t, s, editor.Event{Command: editor.Delete})
	s = key(t, key(t, key(t, s, editor.F7), editor.No), editor.Escape)
	s = text(t, key(t, s, editor.Retrieve), "B:\\ORIGIN")
	s, i := submit(t, s)
	s, _ = done(t, s, perform(i))
	expectRefusal(t, s, editor.Event{Command: editor.F1})
	if s.Snapshot().HistoryCountKnown {
		t.Fatal("cross-document history silently reset")
	}
}

func TestWholeAttributedBlockRestoreThroughSession(t *testing.T) {
	f := setup(t)
	s := key(t, load(t, f), editor.Reveal)
	s = key(t, s, editor.Right)
	s = key(t, s, editor.Block)
	for range 4 {
		s = key(t, s, editor.Right)
	}
	s = key(t, key(t, s, editor.Delete), editor.Yes)
	if s.Document().TokenCount() != 2 || s.Snapshot().Gap != 1 || s.Snapshot().Selection {
		t.Fatal("whole block not deleted")
	}
	s = key(t, key(t, s, editor.F1), editor.Restore)
	if s.Document().TokenCount() != 6 || s.Snapshot().Gap != 5 {
		t.Fatal("attributed restore gap")
	}
	for i := range 6 {
		got, _ := s.Document().Token(i)
		want, _ := load(t, f).Document().Token(i)
		if !bytes.Equal(got.Raw, want.Raw) {
			t.Fatal("actual attributed bytes lost")
		}
	}
	expectRefusal(t, s, editor.Event{Command: editor.F1})
}
