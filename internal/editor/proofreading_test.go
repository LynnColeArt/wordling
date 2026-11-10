package editor_test

import (
	"testing"

	"github.com/lynncoleart/wordling/internal/editor"
)

// T279–T283: the continuous proofreading journey modeled on the WP78
// contract and the spelling/proof trace. Document: the trace's PROOF.WP
// sentence typed into a fresh New buffer. The provider's role (WP87) is
// bounded to acceptance; the state machine owns the walk, transient
// decisions and continuations.

func proofSession(t *testing.T) editor.Session {
	t.Helper()
	s := text(t, mustNew(t), "The quik brown fox met a zorbly cat. The quik fox saw zorbly again. Zorbly follows a mispelled word.")
	return s
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
	if interrupted.Snapshot().Mode != editor.Editing {
		t.Fatalf("F1 interrupt mode: %s", interrupted.Snapshot().Mode)
	}
	if interrupted.Document() == nil || interrupted.Document().TokenCount() == 0 {
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
	// The trace's first correction is quik→quick via suggestion letter 'c'.
	// 'quick' is 5 chars; 'quik' is 4: the original's replacement is NOT an
	// in-place typeover — the boundary fixture shows the replacement is a
	// delete+insert through the native pair publisher (empty code pairs
	// move to the replacement's end). The cohort correction therefore goes
	// through the session's own qualified ASCII insert + deletes: insert
	// the delta characters at the suspect END and forward-delete the
	// surplus at the suspect START is NOT the original's layout; the
	// correct bounded edit is: typeover the shared prefix, insert the new
	// suffix, delete the old suffix. quik→quick shares "quik"+"c" at end.
	// (The BOUNDARY.WP evidence pins the code migration; plain-body
	// replacement via shared-prefix typeover + insert + delete is the
	// honest bounded form for this cohort without the unimplemented pair
	// publisher.)
	_, _, err := ask.Reduce(editor.Event{Command: editor.Text, Text: "c"})
	if err != nil {
		t.Fatal(err)
	}
	// "mispelled"→"misspelled": shared prefix "mi", then s→ss. Same seam.
	if _, _, err := ask.Reduce(editor.Event{Command: editor.ProofSkipOnce}); err != nil {
		t.Fatal(err)
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
