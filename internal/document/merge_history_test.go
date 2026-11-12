package document_test

import (
	"bytes"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

func TestMergeHistoryRequiresAuthenticTransitionsAndTarget(t *testing.T) {
	newDoc := newDocument(t)
	initial, err := document.NewHistory(newDoc)
	if err != nil {
		t.Fatal(err)
	}
	start, _ := newDoc.CursorAt(0)
	field, err := newDoc.InsertMergeCode(start, document.AuthorMergeField, "1")
	if err != nil {
		t.Fatal(err)
	}
	source, err := initial.AfterMergeEdit(field)
	if err != nil {
		t.Fatal(err)
	}
	at, _ := field.Document.CursorAt(0)
	deleted, err := field.Document.DeleteMergeCode(at.WithReveal(true), false)
	if err != nil {
		t.Fatal(err)
	}
	fabricated := deleted
	fabricated.Changed = false
	if _, err := source.AfterMergeEdit(fabricated); err == nil {
		t.Fatal("mutated public receipt adopted")
	}
	shared, err := source.AfterMergeEdit(deleted)
	if err != nil || shared.Count() != 1 {
		t.Fatalf("authentic structural deletion was not retained: %v", err)
	}
	if _, err := shared.AfterMergeEdit(deleted); err == nil {
		t.Fatal("stale edit replayed")
	}

	target := newDocument(t)
	targetHistory, err := document.NewHistory(target)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := shared.CarryHistory(field.Document, targetHistory, target); err == nil {
		t.Fatal("a stale source revision moved history")
	}
	foreign := newDocument(t)
	if _, err := shared.CarryHistory(deleted.Document, targetHistory, foreign); err == nil {
		t.Fatal("a foreign destination revision acquired history")
	}
	carried, err := shared.CarryHistory(deleted.Document, targetHistory, target)
	if err != nil || carried.Count() != 1 || targetHistory.Count() != 0 {
		t.Fatalf("authentic transfer changed the source history: %v", err)
	}
	targetCursor, _ := target.CursorAt(0)
	p, err := carried.Open(targetCursor.WithReveal(true))
	if err != nil || !p.Active() {
		t.Fatalf("no target overlay: %v", err)
	}
	if _, err := foreign.Restore(carried, p); err == nil {
		t.Fatal("a foreign document restored the target overlay")
	}
	r, err := target.Restore(carried, p)
	if err != nil {
		t.Fatal(err)
	}
	want := []byte{0xde, 0x36, 4, 0, 4, 0, 0x36, 0xde}
	if got := mergeCodeBody(t, r.Document()); !bytes.Equal(got, want) || r.Cursor().Gap() != 1 {
		t.Fatalf("authentic restore body %x, cursor %d", got, r.Cursor().Gap())
	}
	if got := mergeCodeBody(t, target); len(got) != 0 {
		t.Fatalf("preview/restore mutated the prior target: %x", got)
	}
}
