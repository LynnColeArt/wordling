package document_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/document"
	"testing"
)

func TestASCIIReceiptOwnershipAndUnknownHistoryEffects(t *testing.T) {
	d := plainOriginal(t)
	h, _ := document.NewHistory(d)
	c, _ := d.CursorAt(0)
	edit, e := d.InsertASCII(c, []byte("X"))
	if e != nil {
		t.Fatal(e)
	}
	forged := document.EditResult{Document: edit.Document, Cursor: edit.Cursor, Changed: edit.Changed}
	bad, e := h.AfterEdit(forged)
	category(t, e, document.InvalidEditResult)
	if bad.Revision() != h.Revision() {
		t.Fatal("forged receipt changed history")
	}
	for _, mutate := range []func(*document.EditResult){func(r *document.EditResult) { r.Changed = !r.Changed }, func(r *document.EditResult) { r.Cursor = r.Cursor.WithReveal(!r.Cursor.Reveal()) }} {
		copy := edit
		mutate(&copy)
		bad, e = h.AfterEdit(copy)
		category(t, e, document.InvalidEditResult)
		if bad.Revision() != h.Revision() {
			t.Fatal("corrupted receipt changed history")
		}
	}
	next, e := h.AfterEdit(edit)
	if e != nil || !next.Qualified() || next.Count() != 0 {
		t.Fatal("fresh insertion", e)
	}
	stable := *edit.Document
	*edit.Document = *d
	p, e := next.Open(edit.Cursor)
	if e != nil || p.Active() {
		t.Fatal("accepted history followed public result replacement", e)
	}
	_, e = h.AfterEdit(edit)
	category(t, e, document.InvalidEditResult)
	// The accepted state remains usable through a copied handle of that state.
	r, e := stable.Delete(edit.Cursor, document.ForwardDelete, next)
	if e != nil || r.History().Count() != 1 {
		t.Fatal(e)
	}
	before, _ := r.History().Entry(0)
	insert, e := r.Document().InsertASCII(r.Cursor(), []byte("Y"))
	if e != nil {
		t.Fatal(e)
	}
	unknown, e := r.History().AfterEdit(insert)
	if e != nil || unknown.Qualified() {
		t.Fatal("unobserved insertion history claimed qualified", e)
	}
	preserved, e := unknown.Entry(0)
	if e != nil || preserved.Qualified || !bytes.Equal(before.Native, preserved.Native) {
		t.Fatal("earlier native fragment lost", e)
	}
	_, e = unknown.Open(insert.Cursor)
	category(t, e, document.UnsupportedHistoryEffect)
	failed, e := unknown.Separate(document.RightBoundary)
	category(t, e, document.UnsupportedHistoryEffect)
	if failed.Revision() != unknown.Revision() {
		t.Fatal("movement silently qualified/cleared unknown history")
	}
	fresh := plainOriginal(t)
	empty, _ := document.NewHistory(fresh)
	at, _ := fresh.CursorAt(0)
	typeover, e := fresh.TypeoverASCII(at, []byte("Z"))
	if e != nil {
		t.Fatal(e)
	}
	unqualified, e := empty.AfterEdit(typeover)
	if e != nil || unqualified.Qualified() {
		t.Fatal("typeover history invented", e)
	}
}

func TestHistoryPreviewAndQuestionSnapshots(t *testing.T) {
	d := plainOriginal(t)
	h, _ := document.NewHistory(d)
	c, _ := d.CursorAt(0)
	d, c, h = deleteForward(t, d, c, h)
	p, _ := h.Open(c)
	before := normalOverlay(t, p)
	retained := h
	h = document.History{}
	if normalOverlay(t, p) != before {
		t.Fatal("preview followed zeroed public history wrapper")
	}
	failed, e := d.Restore(h, p)
	category(t, e, document.InvalidHistory)
	if failed.History().Revision() != h.Revision() {
		t.Fatal("invalid history changed")
	}
	h, _ = document.NewHistory(d)
	failed, e = d.Restore(h, p)
	category(t, e, document.HistoryMismatch)
	if failed.History().Revision() != h.Revision() {
		t.Fatal("new wrapper retargeted old preview")
	}
	h = retained
	entries, _ := h.Entry(0)
	entries.Native[0] = 0
	if normalOverlay(t, p) != before {
		t.Fatal("entry aliases preview")
	}
	pendingDoc, _ := document.Parse(fixture(t))
	history, _ := document.NewHistory(pendingDoc)
	at, _ := pendingDoc.CursorAt(1)
	pending, e := pendingDoc.Delete(at, document.ForwardDelete, history)
	if e != nil {
		t.Fatal(e)
	}
	accepted := pending
	off, _ := pendingDoc.CursorAt(4)
	pending, _ = pendingDoc.Delete(off, document.ForwardDelete, history)
	answer, e := pendingDoc.AnswerDeletion(history, accepted, document.No)
	if e != nil || answer.Cursor().Gap() != 2 || pending.Prompt() != "Delete [bold]? No (Yes)" {
		t.Fatal("question snapshot retargeted", e)
	}
	stale, e := pendingDoc.AnswerDeletion(answer.History(), accepted, document.No)
	category(t, e, document.HistoryMismatch)
	if stale.History().Revision() != answer.History().Revision() {
		t.Fatal("answered question replay changed current history")
	}
}

func TestRepeatedCancelCannotQualifyUnknownGrouping(t *testing.T) {
	d := plainOriginal(t)
	h, _ := document.NewHistory(d)
	c, _ := d.CursorAt(0)
	d, c, h = deleteForward(t, d, c, h)
	for range 2 {
		p, _ := h.Open(c)
		var e error
		h, e = h.CancelPreview(p)
		if e != nil {
			t.Fatal(e)
		}
	}
	before, _ := d.Export()
	r, e := d.Delete(c, document.ForwardDelete, h)
	category(t, e, document.UnsupportedHistoryBoundary)
	if r.History().Revision() != h.Revision() || r.Cursor() != c {
		t.Fatal("failed continued grouping changed state")
	}
	exact(t, r.Document(), before)
	separated, e := h.Separate(document.SavedBoundary)
	if e != nil {
		t.Fatal(e)
	}
	_, e = d.Delete(c, document.ForwardDelete, separated)
	if e != nil {
		t.Fatal("observed separator did not resolve grouping", e)
	}
}

func TestKnownRestoreReopenThenMarkerUsesReceipt(t *testing.T) {
	d, _ := document.Parse(fixture(t))
	h, _ := document.NewHistory(d)
	a, _ := d.CursorAt(1)
	b, _ := d.CursorAt(2)
	pending, _ := d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), h)
	r, e := d.AnswerDeletion(h, pending, document.Yes)
	if e != nil {
		t.Fatal(e)
	}
	p, _ := r.History().Open(r.Cursor())
	cancelled, e := r.History().CancelPreview(p)
	if e != nil {
		t.Fatal(e)
	}
	p, _ = cancelled.Open(r.Cursor())
	restored, e := r.Document().Restore(cancelled, p)
	if e != nil {
		t.Fatal(e)
	}
	reopened, _ := restored.History().Open(restored.Cursor())
	view, e := reopened.Present(0, 10, true)
	if e != nil {
		t.Fatal(e)
	}
	var label string
	for _, element := range view.Elements {
		label += element.Text
	}
	if label != "A[BOLD][bold][BOLD][bold][BOLD]BC[bold]D" {
		t.Fatal("literal nonmutating above-pair preview", label)
	}
	// Actual trace reopens/cancels BEFORE X. Retention after X is unrun.
	history, e := restored.History().CancelPreview(reopened)
	if e != nil {
		t.Fatal(e)
	}
	marker, e := restored.Document().InsertASCII(restored.Cursor(), []byte("X"))
	if e != nil {
		t.Fatal(e)
	}
	after, e := history.AfterEdit(marker)
	if e != nil {
		t.Fatal("known native marker sequence rejected", e)
	}
	raw, _ := marker.Document.Export()
	want := []byte{'A', 0xc3, 12, 0xc3, 0xc4, 12, 0xc4, 0xc3, 12, 0xc3, 'X', 'B', 'C', 0xc4, 12, 0xc4, 'D'}
	if !bytes.Equal(raw[324:], want) || marker.Cursor.Gap() != 5 {
		t.Fatal("literal empty pair/marker/gap lost")
	}
	if after.Qualified() {
		t.Fatal("invented post-X original history observation")
	}
	_, e = after.Open(marker.Cursor)
	category(t, e, document.UnsupportedHistoryEffect)
}
