package editor_test

import (
	"bytes"
	"context"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"path/filepath"
	"testing"
)

func BenchmarkMacroOrdinaryCommands(b *testing.B) {
	for _, large := range []bool{false, true} {
		name := "small"
		if large {
			name = "near-mutation-token-cap"
		}
		b.Run(name, func(b *testing.B) {
			raw, e := os.ReadFile("../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01/run-doc1-1/D1BASE.WP5")
			if e != nil {
				b.Fatal(e)
			}
			if large {
				d, e := document.Parse(raw)
				if e != nil {
					b.Fatal(e)
				}
				c, _ := d.CursorAt(0)
				r, e := d.InsertASCII(c, bytes.Repeat([]byte("X"), document.MaxMutationTokens-3-d.TokenCount()))
				if e != nil {
					b.Fatal(e)
				}
				raw, e = r.Document.Export()
				if e != nil {
					b.Fatal(e)
				}
			}
			root := b.TempDir()
			if e = os.WriteFile(filepath.Join(root, "ORIGIN"), raw, 0600); e != nil {
				b.Fatal(e)
			}
			macro, e := os.ReadFile("../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
			if e != nil {
				b.Fatal(e)
			}
			if e = os.WriteFile(filepath.Join(root, "M38.WPM"), macro, 0600); e != nil {
				b.Fatal(e)
			}
			dir, e := storage.OpenDirectory(root)
			if e != nil {
				b.Fatal(e)
			}
			defer dir.Close()
			s, e := editor.New(editor.Config{Locations: []editor.Location{{Directory: dir}}})
			if e != nil {
				b.Fatal(e)
			}
			for _, event := range []editor.Event{{Command: editor.Retrieve}, {Command: editor.Text, Text: "ORIGIN"}} {
				s, _, e = s.Reduce(event)
				if e != nil {
					b.Fatal(e)
				}
			}
			s, i, e := s.Reduce(editor.Event{Command: editor.Enter})
			if e != nil {
				b.Fatal(e)
			}
			result := perform(i)
			s, _, e = s.Reduce(editor.Event{Command: editor.Complete, Result: &result})
			if e != nil {
				b.Fatal(e)
			}
			s, _, e = s.Reduce(editor.Event{Command: editor.Macro})
			if e != nil {
				b.Fatal(e)
			}
			s, _, e = s.Reduce(editor.Event{Command: editor.Text, Text: "M38"})
			if e != nil {
				b.Fatal(e)
			}
			s, i, e = s.Reduce(editor.Event{Command: editor.Enter})
			if e != nil {
				b.Fatal(e)
			}
			result = perform(i)
			s, _, e = s.Reduce(editor.Event{Command: editor.Complete, Result: &result})
			if e != nil {
				b.Fatal(e)
			}
			b.ReportAllocs()
			b.ResetTimer()
			for range b.N {
				current, run, e := s.StartMacro(vm.DefaultLimits())
				if e != nil {
					b.Fatal(e)
				}
				for !run.Snapshot().Terminal {
					current, _, _, e = run.Step(context.Background(), current, 16)
					if e != nil {
						b.Fatal(e)
					}
				}
				if run.Snapshot().State != "complete" || run.Snapshot().AppliedWords != 3 {
					b.Fatal("benchmark actual command refusal")
				}
			}
		})
	}
}
