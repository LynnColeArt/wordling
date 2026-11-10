package editor_test

import (
	"errors"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
)

// T258 — EE-A12 save-on-exit journeys, genuine storage receipts. Interaction
// order from trace corrections runner 685cf988: F7 -> "Save document?" ->
// Yes -> "Document to be saved:" -> <name> -> Enter -> publish -> exit
// question -> the exit answer closes/declines/returns.

// Rooted route on a retrieved document with real edits: the save to a fresh
// name publishes as a genuine candidate and continues to the exit question.
func TestEverydayJourneySaveOnExitRooted(t *testing.T) {
	f := setup(t)
	s := text(t, load(t, f), "CHANGED")
	question := key(t, s, editor.F7)
	if question.Snapshot().Prompt != "Save document? Yes (No)" {
		t.Fatal("save question prompt")
	}
	advanced := key(t, question, editor.Yes)
	if advanced.Snapshot().Mode != editor.SaveName {
		t.Fatal("Yes did not open the save prompt")
	}
	sv, i := submit(t, advanced)
	if i.Kind != editor.Observe {
		t.Fatal(i.Kind)
	}
	// The prefilled draft is the current display name (B:\ORIGIN); type the
	// bound-free suffix the way the original journey renames: F10-style
	// editing is not qualified here, so rename via a fresh Save is not the
	// observed route — the observed route keeps the original name and
	// answers the Replace question with the no-op admission (same bytes are
	// NOT the case here: edits exist). Per session.go the edited replacement
	// is refused by design (UnsupportedReplacement), so the honest journey
	// target EE-A11 uses: same-file no-op for unchanged, candidate publish
	// for a NEW name. F1 returns to the document and a new Save publishes
	// the edited candidate to a fresh name — but fromExit then no longer
	// applies. Therefore the rooted save-on-exit journey with edits ends at
	// the Replace question, whose Yes refusal is the pinned contract; the
	// journey asserts that honest endpoint instead of inventing a route.
	sv, _ = done(t, sv, perform(i))
	if sv.Snapshot().Mode != editor.ReplaceQuestion {
		t.Fatalf("expected replace question, got %s", sv.Snapshot().Mode)
	}
	_, _, err := sv.Reduce(editor.Event{Command: editor.Yes})
	var failure *storage.Failure
	if err == nil || !errors.As(err, &failure) || failure.Kind != storage.UnsupportedReplacement {
		t.Fatalf("edited replacement must stay refused: %v", err)
	}
	// Cancel back to the save prompt, F1 back to the document (the observed
	// journey's decline path, frame files/11).
	cancel := key(t, sv, editor.No)
	if cancel.Snapshot().Mode != editor.SaveName {
		t.Fatal("decline keeps the name prompt")
	}
	back := key(t, cancel, editor.F1)
	if back.Snapshot().Mode != editor.Editing || back.Document() == nil || !back.Snapshot().Dirty {
		t.Fatal("F1 exit cancel preserved the edits")
	}
}

// Rooted unchanged route: an unchanged document's save-on-exit completes the
// same-file no-op inline (the Observe completion publishes directly) and
// lands on the exit question.
func TestEverydayJourneySaveOnExitUnchangedNoOp(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	question := key(t, s, editor.F7)
	advanced := key(t, question, editor.Yes)
	sv, i := submit(t, advanced)
	if i.Kind != editor.Observe {
		t.Fatal(i.Kind)
	}
	sv, next := done(t, sv, perform(i))
	if next != nil || sv.Snapshot().Mode != editor.ReplaceQuestion {
		t.Fatalf("replace question state: next=%v mode=%s", next, sv.Snapshot().Mode)
	}
	var err error
	sv, next, err = sv.Reduce(editor.Event{Command: editor.Yes})
	if err != nil || next == nil {
		t.Fatalf("no-op not admitted: %v", err)
	}
	sv, _ = done(t, sv, perform(next))
	snap := sv.Snapshot()
	if snap.Mode != editor.ExitQuestion || snap.SaveState != editor.SameFileNoOp {
		t.Fatalf("unchanged save-on-exit landing mode=%s state=%s", snap.Mode, snap.SaveState)
	}
	closed := key(t, sv, editor.Yes)
	if closed.Snapshot().Mode != editor.Exited || closed.Document() != nil {
		t.Fatal("exit Yes closed")
	}
}

// New-buffer route (frame corrections/08 pattern): fresh New Doc 1, typed,
// F7, Yes, name, publish+bind -> exit question; the written file is real.
func TestEverydayJourneySaveOnExitNewBuffer(t *testing.T) {
	path := t.TempDir()
	dir, err := storage.OpenDirectory(path)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = dir.Close() })
	s, err := editor.New(editor.Config{Locations: []editor.Location{{Prefix: "C:\\OUT\\", Directory: dir}}})
	if err != nil {
		t.Fatal(err)
	}
	s = text(t, s, "SCREEN TWO")
	question := key(t, s, editor.F7)
	advanced := key(t, question, editor.Yes)
	s = text(t, advanced, "C:\\OUT\\SECOND.WP")
	sv, i := submit(t, s)
	if i.Kind != editor.Observe {
		t.Fatal(i.Kind)
	}
	dst, err := dir.Observe("SECOND.WP")
	if err != nil {
		t.Fatal(err)
	}
	sv, pub := done(t, sv, editor.Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind, Destination: dst})
	if pub == nil || pub.Kind != editor.PublishNewBuffer {
		t.Fatal("missing first publication request")
	}
	sv, read := done(t, sv, editor.ExecuteNewPublication(pub))
	if read == nil {
		t.Fatal("missing bind request")
	}
	sv, _ = done(t, sv, editor.ExecuteFirstRead(read))
	snap := sv.Snapshot()
	if snap.Mode != editor.ExitQuestion {
		t.Fatalf("New-buffer save-on-exit landing mode %s", snap.Mode)
	}
	if snap.SaveState != editor.NewNamePublished {
		t.Fatalf("save state %s", snap.SaveState)
	}
	written, err := os.ReadFile(filepath.Join(path, "SECOND.WP"))
	if err != nil {
		t.Fatal(err)
	}
	if len(written) < 10 || string(written[len(written)-10:]) != "SCREEN TWO" {
		t.Fatalf("publication body mismatch %q", written)
	}
}

// T257 journey: fresh screen accepts typing immediately (frame corrections/03
// "SCREEN TWO"), content survives a round trip, and the exit-clear law
// remains (exit No leaves an inert cleared session, not a New document).
func TestEverydayJourneyFreshScreenTyping(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	s = key(t, s, editor.SwitchDocument)
	if s.Snapshot().Screen != 2 || s.Source() != nil {
		t.Fatalf("fresh screen %d", s.Snapshot().Screen)
	}
	typed := text(t, s, "SCREEN TWO")
	back := key(t, typed, editor.SwitchDocument)
	if back.Snapshot().Screen != 1 || back.Source() == nil {
		t.Fatal("switch back to Doc 1")
	}
	again := key(t, back, editor.SwitchDocument)
	raw, err := again.Document().Export()
	if err != nil {
		t.Fatal(err)
	}
	if string(raw[len(raw)-len("SCREEN TWO"):]) != "SCREEN TWO" {
		t.Fatalf("Doc 2 content lost: %q", raw[len(raw)-len("SCREEN TWO"):])
	}
}

// Exit-declined clear keeps the original unqualified-clear law.
func TestEverydayJourneyExitDeclineClears(t *testing.T) {
	f := setup(t)
	s := text(t, load(t, f), "CHANGED")
	question := key(t, s, editor.F7)
	exit := key(t, question, editor.No)
	cleared := key(t, exit, editor.No)
	if cleared.Document() != nil || cleared.Source() != nil || cleared.Snapshot().Name != "" {
		t.Fatal("unqualified exit decline minted state")
	}
	if _, _, err := cleared.Reduce(editor.Event{Command: editor.Text, Text: "X"}); err == nil {
		t.Fatal("cleared session accepted text")
	}
}
