package editor_test

import (
	"context"
	"github.com/lynncoleart/wordling/internal/editor"
	"os"
	"path/filepath"
	"testing"
)

func TestAcceptedSameRevisionForksCannotRetargetMacro(t *testing.T) {
	ready, f := readyMacro(t)
	base := key(t, ready, editor.CancelOperation)
	cursor := key(t, base, editor.Right)
	view := key(t, base, editor.Reveal)
	mode := key(t, base, editor.Save)
	screen := key(t, base, editor.SwitchDocument)
	if cursor.Document().Revision() != view.Document().Revision() || cursor.Snapshot().Revision != view.Snapshot().Revision || cursor.Snapshot().Gap == view.Snapshot().Gap || cursor.Snapshot().Reveal == view.Snapshot().Reveal {
		t.Fatal("test did not make two accepted same-count/native-revision divergent forks")
	}
	active, run := openMacro(t, cursor, "B:\\M38")
	otherActive, otherRun := openMacro(t, view, "B:\\M38")
	_ = otherRun
	for label, foreign := range map[string]editor.Session{"cursor-view-fork": otherActive, "wrong-mode": mode, "wrong-active-buffer": screen} {
		t.Run(label, func(t *testing.T) {
			before := run.Snapshot()
			native := foreign.Document().Revision()
			next, _, _, e := run.Step(context.Background(), foreign, 1)
			if e == nil || run.Snapshot().TotalSteps != before.TotalSteps || run.Snapshot().ReceiptCount != before.ReceiptCount || next.Document().Revision() != native {
				t.Fatal("divergent fork reached macro effects")
			}
		})
	}
	active = runMacro(t, active, run)
	if active.Snapshot().Gap != 4 {
		t.Fatal("authoritative cursor was not retained")
	}
	raw, e := os.ReadFile(filepath.Join(f.path, "M38.WPM"))
	if e != nil || len(raw) == 0 {
		t.Fatal("source changed")
	}
}
func TestPendingChildRequiresExactUniqueTransitionNotSameCounters(t *testing.T) {
	root := "../../docs/research/continuation/macro-quit/runs/wp39-nested-02"
	s, f := twoBuffers(t, root, "nested-1")
	s = key(t, s, editor.SwitchDocument)
	for _, name := range []string{"Q39P", "Q39C"} {
		raw, e := os.ReadFile(root + "/input/" + name + ".WPM")
		if e != nil {
			t.Fatal(e)
		}
		if e = os.WriteFile(filepath.Join(f.path, name+".WPM"), raw, 0600); e != nil {
			t.Fatal(e)
		}
	}
	s, run := openMacro(t, s, "B:\\Q39P")
	var pending *editor.Intent
	var e error
	for pending == nil {
		s, pending, _, e = run.Step(context.Background(), s, 16)
		if e != nil {
			t.Fatal(e)
		}
	}
	stale := s
	prior := run.Snapshot()
	native := s.Document().Revision()
	for _, command := range []editor.Command{editor.Right, editor.Reveal, editor.SwitchDocument, editor.Save} {
		next, _, e := s.Reduce(editor.Event{Command: command})
		if e == nil || next.Document().Revision() != native || next.Snapshot().Gap != s.Snapshot().Gap || next.Snapshot().Reveal != s.Snapshot().Reveal || next.Snapshot().Mode != s.Snapshot().Mode || next.Snapshot().Screen != s.Snapshot().Screen {
			t.Fatal("ordinary command forked an active macro target")
		}
	}
	// A waiting Step performs zero VM/native work but accepts a distinct driver
	// transition. The two concurrently live tokens must still differ: their
	// non-zero-sized allocation cannot be coalesced like Go's new(struct{}).
	s, _, current, e := run.Step(context.Background(), s, 1)
	if e != nil {
		t.Fatal(e)
	}
	if current.TotalSteps != prior.TotalSteps || current.TotalWords != prior.TotalWords || s.Document().Revision() != native || s.Snapshot().Revision != stale.Snapshot().Revision {
		t.Fatal("test did not preserve all numeric/native counters")
	}
	result := perform(pending)
	if _, _, e = run.Resume(stale, result); e == nil || run.Snapshot().Pending == nil || run.Snapshot().ReceiptCount != prior.ReceiptCount || run.Snapshot().AppliedWords != prior.AppliedWords {
		t.Fatal("wrong transition consumed child read or caused effects")
	}
	s, _, e = run.Resume(s, result)
	if e != nil {
		t.Fatal(e)
	}
	s = runMacro(t, s, run)
	if asciiText(t, s) != "D1SENT DIRTY1P39C39" {
		t.Fatal("wrong child target")
	}
}
