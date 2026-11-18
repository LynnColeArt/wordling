package editor

import (
	"bytes"
	"context"
	"crypto/sha256"
	"errors"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/storage"
)

// Positive receivers and acquisitions are reached through actual constructors,
// reductions and rooted reads. Only the negative variants mutate private facts.
func pendingNewNested(t *testing.T) (Session, *MacroExecution, *Intent, *storage.Directory, string) {
	t.Helper()
	root := t.TempDir()
	dir, err := storage.OpenDirectory(root)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = dir.Close() })
	pins := map[string]string{"PARENT": "92971022af3838c7c7ab3ae4f00bbefa94f429e610fb487cb520b0fdfc131b40", "CHILD": "2d893c406ad84e122800d6b0611eee539627d4fe3851746989222f91d0bd6f1e"}
	for name, pin := range pins {
		raw, err := os.ReadFile("../../docs/research/reference-runs/2026-10-29-history-02/CMD51-212/" + name + ".WPM")
		if err != nil || fmt.Sprintf("%x", sha256.Sum256(raw)) != pin {
			t.Fatal("original source", name, err)
		}
		if err = os.WriteFile(filepath.Join(root, name+".WPM"), raw, 0600); err != nil {
			t.Fatal(err)
		}
	}
	s, err := New(Config{Locations: []Location{{Directory: dir}, {Prefix: `C:\OUT\`, Directory: dir}}})
	if err != nil {
		t.Fatal(err)
	}
	var intent *Intent
	for _, event := range []Event{{Command: Macro}, {Command: Text, Text: "PARENT"}, {Command: Enter}} {
		s, intent, err = s.Reduce(event)
		if err != nil {
			t.Fatal(err)
		}
	}
	result := ExecuteMacroRead(intent)
	s, _, err = s.Reduce(Event{Command: Complete, Result: &result})
	if err != nil {
		t.Fatal(err)
	}
	s, run, err := s.StartMacro(vm.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	for n := 0; n < 4096; n++ {
		s, intent, _, err = run.Step(context.Background(), s, 1)
		if err != nil {
			t.Fatal(err)
		}
		if intent != nil {
			return s, run, intent, dir, root
		}
		if run.Snapshot().Terminal {
			t.Fatal("New target never issued genuine child read", run.Snapshot())
		}
	}
	t.Fatal("child request bound")
	return Session{}, nil, nil, nil, ""
}

func assertNewNestedRefusal(t *testing.T, s Session, run *MacroExecution, result Result) {
	t.Helper()
	before := run.Snapshot()
	raw, _ := s.Document().Export()
	next, _, err := run.Resume(s, result)
	after, _ := next.Document().Export()
	p := run.Snapshot()
	if err == nil || !bytes.Equal(raw, after) || next.Document().Birth() != s.Document().Birth() || next.Snapshot().Dirty != s.Snapshot().Dirty || p.Pending == nil || p.Pending.Operation != before.Pending.Operation || p.AppliedWords != before.AppliedWords || p.ReceiptCount != before.ReceiptCount || p.TotalSteps != before.TotalSteps || p.TotalWords != before.TotalWords {
		t.Fatalf("forged read consumed authority/effects: %v %+v", err, p)
	}
}

func finishNewNestedInternal(t *testing.T, s Session, run *MacroExecution) Session {
	t.Helper()
	for n := 0; !run.Snapshot().Terminal; n++ {
		if n >= 4096 {
			t.Fatal("bounded real continuation")
		}
		next, intent, _, err := run.Step(context.Background(), s, 16)
		if err != nil {
			t.Fatal(err)
		}
		s = next
		if intent != nil {
			s, _, err = run.Resume(s, ExecuteMacroRead(intent))
			if err != nil {
				t.Fatal(err)
			}
		}
	}
	if run.Snapshot().State != "complete" {
		t.Fatal(run.Snapshot())
	}
	return s
}

func TestNewNestedRequestAndResultProvenance(t *testing.T) {
	s, run, intent, _, _ := pendingNewNested(t)
	foreign, foreignRun, foreignIntent, foreignDir, _ := pendingNewNested(t)
	_ = foreign
	_ = foreignRun
	requestChanges := map[string]func(*Intent){
		"operation": func(i *Intent) { i.Operation++ }, "revision": func(i *Intent) { i.Revision++ }, "run": func(i *Intent) { i.MacroRun++ }, "request": func(i *Intent) { i.MacroRequest++ }, "parent": func(i *Intent) { i.MacroParent[0] ^= 1 }, "screen": func(i *Intent) { i.Screen = 2 }, "name": func(i *Intent) { i.Name = "PARENT.WPM" }, "root": func(i *Intent) { i.Directory = foreignDir },
	}
	for label, change := range requestChanges {
		t.Run("request-"+label, func(t *testing.T) {
			bad := *intent
			change(&bad)
			assertNewNestedRefusal(t, s, run, ExecuteMacroRead(&bad))
		})
	}
	actual := ExecuteMacroRead(intent)
	if actual.Err != nil {
		t.Fatal(actual.Err)
	}
	resultChanges := map[string]func(*Result){
		"operation": func(r *Result) { r.Operation++ }, "revision": func(r *Result) { r.Revision++ }, "kind": func(r *Result) { r.Kind = Observe }, "source": func(r *Result) { r.Macro = &storage.Macro{} }, "synthetic-missing": func(r *Result) { r.Err = fs.ErrNotExist }, "unrelated-document": func(r *Result) { r.Document = &storage.Document{} }, "unrelated-destination": func(r *Result) { r.Destination = &storage.Destination{} },
	}
	for label, change := range resultChanges {
		t.Run("result-"+label, func(t *testing.T) { bad := actual; change(&bad); assertNewNestedRefusal(t, s, run, bad) })
	}
	assertNewNestedRefusal(t, s, run, ExecuteMacroRead(foreignIntent))
	assertNewNestedRefusal(t, s, run, Result{Kind: ReadMacro, Operation: intent.Operation, Revision: intent.Revision, Err: fs.ErrNotExist})
	var err error
	s, _, err = run.Resume(s, actual)
	if err != nil {
		t.Fatal("authentic result no longer usable", err)
	}
	if _, _, err = run.Resume(s, actual); err == nil {
		t.Fatal("duplicate child accepted")
	}
	s = finishNewNestedInternal(t, s, run)
	if s.Snapshot().Gap != len("PCHILDRPARENT") || s.Document().TokenCount() != len("PCHILDRPARENT") {
		t.Fatal("handler control flow changed", s.Snapshot())
	}
}

func TestNewNestedPendingRetainsCurrentNewTargetAndTransition(t *testing.T) {
	s, run, intent, _, _ := pendingNewNested(t)
	actual := ExecuteMacroRead(intent)
	other, _, _, _, _ := pendingNewNested(t)
	changes := map[string]func(*Session){
		"owner": func(s *Session) { s.macroOwner = other.macroOwner }, "buffer": func(s *Session) { s.bufferID = other.bufferID }, "screen": func(s *Session) { s.screen = 2 }, "target": func(s *Session) { s.newMacro = other.newMacro }, "genesis": func(s *Session) { s.genesis = document.Revision{} }, "phase": func(s *Session) { s.newPhase = NewAnchored }, "source": func(s *Session) { s.source = &storage.Document{} }, "name": func(s *Session) { s.name = "FORGED" }, "publication": func(s *Session) { s.publishedRevision = s.native.Revision() },
	}
	for label, change := range changes {
		t.Run(label, func(t *testing.T) { bad := s; change(&bad); assertNewNestedRefusal(t, bad, run, actual) })
	}
	stale := s
	var err error
	s, _, _, err = run.Step(context.Background(), s, 1)
	if err != nil {
		t.Fatal(err)
	}
	if s.Snapshot().Revision != stale.Snapshot().Revision || s.Document().Revision() != stale.Document().Revision() {
		t.Fatal("waiting transition must preserve equal counters")
	}
	assertNewNestedRefusal(t, stale, run, actual)
	s, _, err = run.Resume(s, actual)
	if err != nil {
		t.Fatal(err)
	}
	_ = finishNewNestedInternal(t, s, run)
}

func TestNewNestedRealHostFailureAndPendingCancellation(t *testing.T) {
	for _, mode := range []string{"closed-root", "host-stop", "cancel-context"} {
		t.Run(mode, func(t *testing.T) {
			s, run, intent, dir, _ := pendingNewNested(t)
			before := s.Snapshot()
			history := s.History().Revision()
			birth := s.Document().Birth()
			raw, _ := s.Document().Export()
			prior := run.Snapshot()
			var late Result
			var err error
			if mode == "closed-root" {
				if err = dir.Close(); err != nil {
					t.Fatal(err)
				}
				late = ExecuteMacroRead(intent)
				if late.Err == nil {
					t.Fatal("actual closed directory accepted")
				}
				s, _, err = run.Resume(s, late)
				var failure *vm.Failure
				if !errors.As(err, &failure) || failure.Code != "HostFailure" {
					t.Fatal("host error became ON ERROR condition", err)
				}
			} else {
				late = ExecuteMacroRead(intent)
				if mode == "host-stop" {
					s, _, err = run.HostStop(s, "pending child stopped by host")
				} else {
					ctx, cancel := context.WithCancel(context.Background())
					cancel()
					s, _, _, err = run.Step(ctx, s, 1)
				}
				if err != nil {
					t.Fatal(err)
				}
			}
			p := run.Snapshot()
			after, _ := s.Document().Export()
			if !p.Terminal || p.State == "complete" || p.Pending != nil || p.AppliedWords != prior.AppliedWords || p.ReceiptCount != prior.ReceiptCount || !bytes.Equal(raw, after) || s.Document().Birth() != birth || s.Snapshot().NativeRevision != before.NativeRevision || s.History().Revision() != history || !s.Snapshot().Dirty || s.Source() != nil || s.Snapshot().Name != "" || s.Snapshot().NewPhase != NewUnpublished || s.Snapshot().Mode != Editing {
				t.Fatal("partial New truth lost", p, s.Snapshot())
			}
			if _, _, err = run.Resume(s, late); err == nil {
				t.Fatal("late child completion accepted")
			}
			next, _, err := s.Reduce(Event{Command: Text, Text: "Z"})
			if err != nil || next.Document().TokenCount() != s.Document().TokenCount()+1 {
				t.Fatal("terminal owner not released", err)
			}
		})
	}
}

func TestNewNestedOutOfOrderAuthenticReadsDoNotStealHandlers(t *testing.T) {
	s, run, intent, _, _ := pendingNewNested(t)
	older := ExecuteMacroRead(intent)
	var err error
	s, _, err = run.Resume(s, older)
	if err != nil {
		t.Fatal(err)
	}
	for read := 0; read < 2; read++ {
		var pending *Intent
		for n := 0; pending == nil; n++ {
			if n >= 4096 {
				t.Fatal("nested missing bound")
			}
			s, pending, _, err = run.Step(context.Background(), s, 1)
			if err != nil {
				t.Fatal(err)
			}
		}
		assertNewNestedRefusal(t, s, run, older)
		actual := ExecuteMacroRead(pending)
		if actual.Err == nil || actual.macroObservation == nil || !actual.macroObservation.missing || actual.macroObservation.proof != pending.macroProof {
			t.Fatal("missing condition was not an actual rooted absence", actual.Err)
		}
		s, _, err = run.Resume(s, actual)
		if err != nil {
			t.Fatal(err)
		}
		older = actual
	}
	s = finishNewNestedInternal(t, s, run)
	raw, _ := s.Document().Export()
	if string(raw[324:]) != "PCHILDRPARENT" {
		t.Fatal("child/parent handler scope changed")
	}
}
