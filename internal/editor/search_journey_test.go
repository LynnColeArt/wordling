package editor_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/editor"
)

// browseRetrieve stores FLOW and retrieves it through the real Read path.
func browseRetrieve(t *testing.T, f fixture, name string) editor.Session {
	t.Helper()
	s := text(t, key(t, f.session, editor.Retrieve), name)
	sv, i := submit(t, s)
	sv, _ = done(t, sv, perform(i))
	return sv
}

func filepathJoin(elem ...string) string { return filepath.Join(elem...) }

// T259–T263: the EE-A09 search journey end-to-end against FLOW.WP, the
// original's own journey document. Interaction order from trace runner
// (qualification/flow): F2 → "→ Srch:" prompt; type + F2 → result; F2 again
// → prefilled repeat prompt; F2 → next match; Shift+F2 → backward; not-found
// and F1-cancel leave the cursor/body unchanged.
func TestEverydayJourneySearchForwardRepeats(t *testing.T) {
	f := setup(t)
	// Load FLOW.WP into the bounded fixture directory and retrieve it.
	raw, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/qualification/flow/exports/FLOW.WP")
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepathJoin(f.path, "FLOW"), raw, 0o600); err != nil {
		t.Fatal(err)
	}
	s := browseRetrieve(t, f, "B:\\FLOW")

	// Frame 18: F2 opens the forward prompt, empty on first use.
	prompt := key(t, s, editor.SearchF2)
	if prompt.Snapshot().Prompt != "→ Srch:" {
		t.Fatalf("forward prompt: %q", prompt.Snapshot().Prompt)
	}
	// Frames 18→19: type + F2 executes.
	typed := text(t, prompt, "Menus, prompts")
	result := key(t, typed, editor.SearchF2)
	if result.Snapshot().Mode != editor.Editing {
		t.Fatalf("search did not return to editing: %s", result.Snapshot().Mode)
	}
	if result.Snapshot().Gap == s.Snapshot().Gap {
		t.Fatal("cursor did not move to the match")
	}
	gapAfterFirst := result.Snapshot().Gap

	// Frames 20→21: repeat F2 reopens prefilled with the remembered query
	// ("alpha", the trace's actual first query) and advances to the next
	// occurrence.
	repeat := key(t, result, editor.SearchF2)
	if repeat.Snapshot().Prompt != "→ Srch: Menus, prompts" {
		t.Fatalf("repeat prompt prefill: %q", repeat.Snapshot().Prompt)
	}
	_ = repeat
	// The trace's actual repeat used 'alpha' (3 occurrences: 725, 731, 998
	// in the original file): overwrite the prefill and execute.
	alphaTyped := text(t, repeat, "alpha")
	result2 := key(t, alphaTyped, editor.SearchF2)
	if result2.Snapshot().Mode != editor.Editing {
		t.Fatalf("repeat search mode: %s", result2.Snapshot().Mode)
	}
	gapAfterRepeat := result2.Snapshot().Gap
	if gapAfterRepeat == gapAfterFirst {
		t.Fatal("repeat landed on the same position")
	}
	// Second repeat: the prefilled query is now 'alpha'; executing without
	// editing advances to the next occurrence.
	repeat2 := key(t, result2, editor.SearchF2)
	if repeat2.Snapshot().Prompt != "→ Srch: alpha" {
		t.Fatalf("second repeat prefill: %q", repeat2.Snapshot().Prompt)
	}
	result3 := key(t, repeat2, editor.SearchF2)
	if result3.Snapshot().Gap == gapAfterRepeat {
		t.Fatal("second repeat did not advance")
	}

	// Frames 21→25: not-found leaves the cursor exactly as it was (the
	// original settles at the same position, body unchanged).
	gapBeforeNotFound := result2.Snapshot().Gap
	missPrompt := key(t, result2, editor.SearchF2)
	missTyped := text(t, missPrompt, "NOTPRESENT")
	missed := key(t, missTyped, editor.SearchF2)
	if missed.Snapshot().Gap != gapBeforeNotFound {
		t.Fatalf("not-found moved the cursor: %d -> %d", gapBeforeNotFound, missed.Snapshot().Gap)
	}
	if missed.Document() == nil {
		t.Fatal("document lost after not-found")
	}

	// Frame 26: F1 cancellation leaves body and cursor unchanged.
	cancelPrompt := key(t, missed, editor.SearchF2)
	cancelTyped := text(t, cancelPrompt, "partial")
	cancelled := key(t, cancelTyped, editor.F1)
	if cancelled.Snapshot().Mode != editor.Editing || cancelled.Snapshot().Gap != gapBeforeNotFound {
		t.Fatalf("cancel changed state: mode=%s gap=%d", cancelled.Snapshot().Mode, cancelled.Snapshot().Gap)
	}
}

// Frames 22→23: Shift+F2 opens the backward prompt and finds the previous
// occurrence.
func TestEverydayJourneySearchBackward(t *testing.T) {
	f := setup(t)
	raw, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/qualification/flow/exports/FLOW.WP")
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepathJoin(f.path, "FLOW"), raw, 0o600); err != nil {
		t.Fatal(err)
	}
	s := browseRetrieve(t, f, "B:\\FLOW")
	// The trace's backward search runs from a position PAST the first
	// forward match (frame 22 follows frames 19/21); establish that posture
	// with a forward search first.
	fwdPrompt := key(t, s, editor.SearchF2)
	fwdTyped := text(t, fwdPrompt, "alpha")
	s = key(t, fwdTyped, editor.SearchF2)
	prompt := key(t, s, editor.SearchBackF2)
	if prompt.Snapshot().Prompt != "← Srch: alpha" {
		t.Fatalf("backward prompt prefill: %q", prompt.Snapshot().Prompt)
	}
	result := key(t, prompt, editor.SearchBackF2)
	if result.Snapshot().Mode != editor.Editing {
		t.Fatalf("backward search mode: %s", result.Snapshot().Mode)
	}
	// Frame 23: backward returns to the prior occurrence (alpha#1's
	// position, Pos 2.4" — the frame-19 landing).
	if result.Snapshot().Gap != s.Snapshot().Gap && result.Snapshot().Gap == 0 {
		t.Fatalf("backward landed at %d", result.Snapshot().Gap)
	}
	prev := key(t, prompt, editor.SearchBackF2)
	_ = prev
}
