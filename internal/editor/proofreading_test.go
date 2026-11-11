package editor_test

import (
	"bytes"
	"testing"

	"github.com/lynncoleart/wordling/internal/editor"
)

func proofSession(t *testing.T) editor.Session {
	t.Helper()
	s, _ := proofLive(t, t.TempDir())
	return proofType(t, s, "The quik brown fox met a zorbly cat. The quik fox saw zorbly again. Zorbly follows a mispelled word.")
}

func mustNew(t *testing.T) editor.Session {
	t.Helper()
	s, err := editor.New(editor.Config{})
	if err != nil {
		t.Fatal(err)
	}
	return s
}

// ctrl-f2 opens the Check menu (frame 01); digit 3 (Document) starts the
// questioning walk whose first suspect is the first "quik".
func TestProofreadingMenuAndFirstQuestion(t *testing.T) {
	s := proofSession(t)
	menu := key(t, s, editor.ProofCtrlF2)
	if menu.Snapshot().Mode != editor.ProofMenuMode {
		t.Fatalf("after Ctrl+F2: %s", menu.Snapshot().Mode)
	}
	ask, _, err := menu.Reduce(editor.Event{Command: editor.Text, Text: "3"})
	if err != nil {
		t.Fatal(err)
	}
	if ask.Snapshot().Mode != editor.ProofAskMode {
		t.Fatalf("after digit 3: %s", ask.Snapshot().Mode)
	}
	pw, ok := ask.ProofSnapshot()
	if !ok || pw.Word != "quik" {
		t.Fatalf("first suspect: %+v ok=%v", pw, ok)
	}
}

// Skip applies to the rest of the pass (frame 05): skipping both "quik"
// occurrences means a later third "quik" would not be questioned — but this
// document has exactly two, so the walk advances "zorbly" next, and the
// skipped word is not re-asked.
func TestProofreadingSkipRestAdvances(t *testing.T) {
	s := proofSession(t)
	menu := key(t, s, editor.ProofCtrlF2)
	ask, _, _ := menu.Reduce(editor.Event{Command: editor.Text, Text: "3"})
	// Skip the current suspect once (Not Found 1); next suspect arrives.
	next, _, err := ask.Reduce(editor.Event{Command: editor.ProofSkipOnce})
	if err != nil {
		t.Fatal(err)
	}
	pw, ok := next.ProofSnapshot()
	if !ok || pw.Word != "zorbly" {
		t.Fatalf("after Skip Once: %+v ok=%v", pw, ok)
	}
	// Skip-for-pass (2): "zorbly" never questioned again.
	rest, _, _ := next.Reduce(editor.Event{Command: editor.ProofSkip})
	pw2, ok2 := rest.ProofSnapshot()
	if !ok2 || pw2.Word == "zorbly" {
		t.Fatalf("Skip did not suppress the word: %+v ok=%v", pw2, ok2)
	}
}

// The walk ends in the word-count acknowledgement mode and ProofAdvance
// (any key, frame 09 'spc') returns to editing; a new pass (Ctrl+F2 again)
// re-questions the same words because transient decisions reset (frame 10).
func TestProofreadingCompletionReset(t *testing.T) {
	s := proofSession(t)
	menu := key(t, s, editor.ProofCtrlF2)
	ask, _, _ := menu.Reduce(editor.Event{Command: editor.Text, Text: "3"})
	// Skip once repeatedly until the walk drains (each call advances one).
	cur := ask
	for i := 0; i < 12; i++ {
		snap := cur.Snapshot()
		if snap.Mode == editor.ProofAckMode {
			break
		}
		var err error
		cur, _, err = cur.Reduce(editor.Event{Command: editor.ProofSkipOnce})
		if err != nil {
			t.Fatalf("step %d: %v", i, err)
		}
	}
	if cur.Snapshot().Mode != editor.ProofAckMode {
		t.Fatalf("walk did not complete: %s", cur.Snapshot().Mode)
	}
	back, _, _ := cur.Reduce(editor.Event{Command: editor.ProofAdvance})
	if back.Snapshot().Mode != editor.Editing {
		t.Fatalf("after acknowledgement: %s", back.Snapshot().Mode)
	}
	// New pass re-questions "quik" (transient decisions were reset).
	menu2 := key(t, back, editor.ProofCtrlF2)
	ask2, _, _ := menu2.Reduce(editor.Event{Command: editor.Text, Text: "3"})
	pw, ok := ask2.ProofSnapshot()
	if !ok || pw.Word != "quik" {
		t.Fatalf("new pass first suspect: %+v ok=%v", pw, ok)
	}
}

// F1 interrupts checking and returns to editing (spell study: F1 produces
// "the interrupted word's" return; an unconditional exit is insufficient).
func TestProofreadingInterruptF1(t *testing.T) {
	s := proofSession(t)
	menu := key(t, s, editor.ProofCtrlF2)
	ask, _, _ := menu.Reduce(editor.Event{Command: editor.Text, Text: "3"})
	interrupted, _, err := ask.Reduce(editor.Event{Command: editor.F1})
	if err != nil {
		t.Fatal(err)
	}
	if interrupted.Snapshot().Mode != editor.ProofAckMode || !interrupted.ProofStatus().Partial {
		t.Fatalf("F1 interrupt mode: %s", interrupted.Snapshot().Mode)
	}
	interrupted = proofKey(t, interrupted, editor.ProofAdvance)
	if interrupted.Snapshot().Mode != editor.Editing || interrupted.Document() == nil || interrupted.Document().TokenCount() == 0 {
		t.Fatal("interrupt lost the document")
	}
}

// Correction through the real native path: choose a replacement for the
// first "quik" via the suggestion seam; the document body must contain
// "quick" and the surrounding words unchanged (T280: approved document
// operations only; no rendering-side string replacement).
func TestProofreadingCorrectionPreservesBody(t *testing.T) {
	s := proofSession(t)
	menu := key(t, s, editor.ProofCtrlF2)
	ask, _, _ := menu.Reduce(editor.Event{Command: editor.Text, Text: "3"})
	corrected := proofChooseSuggestion(t, ask, "quick")
	if !bytes.Contains(proofLiveBytes(t, corrected), []byte("The quick brown fox")) ||
		corrected.ProofStatus().Word != "zorbly" {
		t.Fatal("the visible suggestion did not replace the native word and advance")
	}
}

func TestProofreadingRequiresAdmittedLexicon(t *testing.T) {
	s := mustNew(t)
	before := s.Snapshot()
	got, intent, err := s.Reduce(editor.Event{Command: editor.ProofCtrlF2})
	if err == nil || intent != nil || got.Snapshot().NativeRevision != before.NativeRevision ||
		got.Snapshot().Mode != before.Mode {
		t.Fatal("missing lexicon must refuse without changing the editor")
	}
}

func countOf(b []byte, sub string) int {
	n := 0
	sub_ := []byte(sub)
	for i := 0; i+len(sub_) <= len(b); i++ {
		ok := true
		for j := range sub_ {
			if b[i+j] != sub_[j] {
				ok = false
				break
			}
		}
		if ok {
			n++
		}
	}
	return n
}
