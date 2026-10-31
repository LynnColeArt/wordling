package editor_test

import (
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"reflect"
	"testing"
)

// This is reducer event-boundary fuzz, not another binary codec or original run.
// At most256 events, text at most8 bytes/event, inherited mutation/native limits.
func FuzzReducerAtomicRefusals(f *testing.F) {
	raw, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if e != nil {
		f.Fatal(e)
	}
	root := f.TempDir()
	if e = os.WriteFile(root+"/ORIGIN", raw, 0600); e != nil {
		f.Fatal(e)
	}
	dir, e := storage.OpenDirectory(root)
	if e != nil {
		f.Fatal(e)
	}
	defer dir.Close()
	base, e := editor.New(editor.Config{Locations: []editor.Location{{Directory: dir}}})
	if e != nil {
		f.Fatal(e)
	}
	base, _, _ = base.Reduce(editor.Event{Command: editor.Retrieve})
	base, _, _ = base.Reduce(editor.Event{Command: editor.Text, Text: "ORIGIN"})
	base, i, _ := base.Reduce(editor.Event{Command: editor.Enter})
	r := perform(i)
	base, _, e = base.Reduce(editor.Event{Command: editor.Complete, Result: &r})
	if e != nil {
		f.Fatal(e)
	}
	for _, v := range [][]byte{{0}, {2, 4, 12, 13}, {1, 1, 3, 5, 8}, {255, 0, 17, 8}} {
		f.Add(v)
	}
	commands := []editor.Command{editor.Text, editor.Insert, editor.Right, editor.Left, editor.Delete, editor.Backspace, editor.Reveal, editor.Block, editor.F1, editor.Previous, editor.Restore, editor.Yes, editor.No, editor.Escape, editor.F7, editor.Save, editor.Home, editor.Up, editor.CancelOperation, editor.Enter}
	f.Fuzz(func(t *testing.T, input []byte) {
		if len(input) > 256 {
			t.Skip()
		}
		s := base
		for pos, v := range input {
			before := s.Snapshot()
			rev := s.Document().Revision()
			event := editor.Event{Command: commands[int(v)%len(commands)]}
			if event.Command == editor.Text {
				end := pos + 8
				if end > len(input) {
					end = len(input)
				}
				event.Text = string(input[pos:end])
			}
			next, _, err := s.Reduce(event)
			if err != nil {
				if !reflect.DeepEqual(before, next.Snapshot()) || next.Document().Revision() != rev {
					t.Fatal("refusal partially changed session")
				}
			}
			s = next
		}
		source := base.Source().Export()
		if !reflect.DeepEqual(source, raw) {
			t.Fatal("persistent original mutated")
		}
	})
}
