package editor_test

import (
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"sync"
	"testing"
)

func TestSameByteTypeoverRemainsCleanAndModeToggleIsAtomic(t *testing.T) {
	f := setup(t)
	s := key(t, load(t, f), editor.Insert)
	before := s.Document().Revision()
	s = text(t, s, "A")
	if s.Snapshot().Dirty || s.Document().Revision() != before || s.Snapshot().Gap != 1 {
		t.Fatal("same-byte typeover invented dirty revision")
	}
	// Native mode/view/navigation remain available without promoting history.
	s = key(t, s, editor.Insert)
	if s.Snapshot().Typeover || s.Snapshot().HistoryQualified {
		t.Fatal("mode toggle invented history qualification")
	}
	s = text(t, s, "Q")
	s = key(t, s, editor.Reveal)
	s = key(t, s, editor.Right)
	if !s.Snapshot().Dirty {
		t.Fatal("insertion after typeover did not edit")
	}
	expectRefusal(t, s, editor.Event{Command: editor.F1})
}
func TestImmutableSessionConcurrentObservers(t *testing.T) {
	f := setup(t)
	s := text(t, load(t, f), "X")
	s, _ = queued(t, s, "COPY")
	var wg sync.WaitGroup
	for range 8 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for range 40 {
				p := s.Snapshot()
				clear(p.Pending.Candidate)
				*p.Pending.Document = storage.Document{}
				*s.Document() = *s.Document()
				_, _ = s.Present(0, s.Document().TokenCount())
				_, _, _ = s.Reduce(editor.Event{Command: editor.Text, Text: "Y"})
			}
		}()
	}
	wg.Wait()
	if !s.Snapshot().Dirty || s.Snapshot().Pending.Document.Identity().Size == 0 {
		t.Fatal("observer changed authority")
	}
}
func BenchmarkReducerInsertion(b *testing.B) {
	raw, err := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if err != nil {
		b.Fatal(err)
	}
	root := b.TempDir()
	if err = os.WriteFile(root+"/ORIGIN", raw, 0600); err != nil {
		b.Fatal(err)
	}
	dir, err := storage.OpenDirectory(root)
	if err != nil {
		b.Fatal(err)
	}
	defer dir.Close()
	s, err := editor.New(editor.Config{Locations: []editor.Location{{Directory: dir}}})
	if err != nil {
		b.Fatal(err)
	}
	s, _, _ = s.Reduce(editor.Event{Command: editor.Retrieve})
	s, _, _ = s.Reduce(editor.Event{Command: editor.Text, Text: "ORIGIN"})
	s, i, _ := s.Reduce(editor.Event{Command: editor.Enter})
	r := perform(i)
	s, _, err = s.Reduce(editor.Event{Command: editor.Complete, Result: &r})
	if err != nil {
		b.Fatal(err)
	}
	b.ReportAllocs()
	b.ResetTimer()
	for range b.N {
		_, _, err := s.Reduce(editor.Event{Command: editor.Text, Text: "X"})
		if err != nil {
			b.Fatal(err)
		}
	}
}

func TestModeAndNavigationPreserveEarlierUnknownHistory(t *testing.T) {
	f := setup(t)
	s := key(t, load(t, f), editor.Delete)
	entry, err := s.History().Entry(0)
	if err != nil {
		t.Fatal(err)
	}
	s = key(t, s, editor.Insert)
	s = text(t, s, "Q")
	old := s.Document().Revision()
	s = key(t, s, editor.Insert)
	s = text(t, s, "R")
	s = key(t, s, editor.Reveal)
	s = key(t, s, editor.Right)
	after, err := s.History().Entry(0)
	if err != nil {
		t.Fatal(err)
	}
	if string(entry.Native) != string(after.Native) || s.History().Count() != 1 || s.Snapshot().HistoryQualified || s.Document().Revision() == old {
		t.Fatal("mode/navigation cleared earlier effects or invented history")
	}
	expectRefusal(t, s, editor.Event{Command: editor.F1})
}
