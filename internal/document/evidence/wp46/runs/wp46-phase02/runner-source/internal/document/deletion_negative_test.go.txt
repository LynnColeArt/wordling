package document_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/document"
	"testing"
)

func TestDeletionRefusalsPreserveAllInputs(t *testing.T) {
	d, _ := document.Parse(fixture(t))
	h, _ := document.NewHistory(d)
	c, _ := d.CursorAt(0)
	before, _ := d.Export()
	for _, direction := range []document.DeleteDirection{0, 255, document.Backspace} {
		r, e := d.Delete(c, direction, h)
		if e == nil || r.History().Revision() != h.Revision() || r.Cursor() != c {
			t.Fatal("failed command changed inputs")
		}
		exact(t, r.Document(), before)
	}
	other, _ := document.Parse(fixture(t))
	foreign, _ := other.CursorAt(1)
	r, e := d.Delete(foreign, document.ForwardDelete, h)
	category(t, e, document.RevisionMismatch)
	if r.History().Revision() != h.Revision() {
		t.Fatal("foreign cursor consumed history")
	}
	exact(t, d, before)
	for _, span := range [][2]int{{1, 1}, {5, 1}, {0, 1}, {1, 3}, {2, 4}, {0, 6}} {
		a, _ := d.CursorAt(span[0])
		b, _ := d.CursorAt(span[1])
		r, e := d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), h)
		category(t, e, document.UnsupportedDeletion)
		if r.History().Revision() != h.Revision() || r.Cursor() != b.WithReveal(true) {
			t.Fatal("bad selection changed state")
		}
		exact(t, r.Document(), before)
	}
	a, _ := d.CursorAt(1)
	b, _ := d.CursorAt(2)
	_, e = d.DeleteBlock(a, b, h)
	category(t, e, document.UnsupportedDeletion)
	pending, e := d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), h)
	if e != nil {
		t.Fatal(e)
	}
	invalid, e := d.AnswerDeletion(h, pending, 255)
	category(t, e, document.InvalidAnswer)
	if invalid.History().Revision() != h.Revision() || !invalid.Pending() {
		t.Fatal("invalid answer changed question")
	}
	_, e = d.CancelBlock(h, pending)
	category(t, e, document.InvalidDeletionState)
	var zero document.History
	_, e = d.Delete(c, document.ForwardDelete, zero)
	category(t, e, document.InvalidHistory)
	var noQuestion document.Deletion
	_, e = d.AnswerDeletion(h, noQuestion, document.Yes)
	category(t, e, document.InvalidDeletionState)
}

func TestUnsafeRestoreDestinationsAndLimitsAreAtomic(t *testing.T) {
	d, _ := document.Parse(fixture(t))
	h, _ := document.NewHistory(d)
	a, _ := d.CursorAt(1)
	b, _ := d.CursorAt(2)
	q, _ := d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), h)
	repaired, e := d.AnswerDeletion(h, q, document.Yes)
	if e != nil {
		t.Fatal(e)
	}
	outside, _ := repaired.Document().CursorAt(0)
	p, _ := repaired.History().Open(outside)
	before, _ := repaired.Document().Export()
	r, e := repaired.Document().Restore(repaired.History(), p)
	category(t, e, document.UnsupportedBody)
	if r.History().Revision() != repaired.History().Revision() || r.Cursor() != outside {
		t.Fatal("unsafe restoration changed inputs")
	}
	exact(t, r.Document(), before)
	// A maximum admitted body remains bounded through delete/restore/repeat.
	source := synthetic(t, bytes.Repeat([]byte{'x'}, document.MaxMutationTokens))
	large, _ := document.Parse(source)
	history, _ := document.NewHistory(large)
	at, _ := large.CursorAt(0)
	large, at, history = deleteForward(t, large, at, history)
	preview, _ := history.Open(at)
	restored, e := large.Restore(history, preview)
	if e != nil {
		t.Fatal(e)
	}
	again, _ := restored.History().Open(restored.Cursor())
	raw, _ := restored.Document().Export()
	bad, e := restored.Document().Restore(restored.History(), again)
	category(t, e, document.MutationLimit)
	if bad.History().Revision() != restored.History().Revision() || bad.Cursor() != restored.Cursor() {
		t.Fatal("limit changed state")
	}
	exact(t, bad.Document(), raw)
}

func TestLiteralLabelsAndOpaqueLookalikesRemainDifferentIdentities(t *testing.T) {
	base := plainOriginal(t)
	c, _ := base.CursorAt(0)
	setup, e := base.TypeoverASCII(c, []byte("[BOLD]"))
	if e != nil {
		t.Fatal(e)
	}
	d := setup.Document
	c, _ = d.CursorAt(0)
	h, _ := document.NewHistory(d)
	for range 6 {
		d, c, h = deleteForward(t, d, c, h)
	}
	info, _ := h.Entry(0)
	if !bytes.Equal(info.Native, []byte("[BOLD]")) {
		t.Fatal("literal labels became native codes")
	}
	p, _ := h.Open(c)
	view, e := p.Present(0, 6, true)
	if e != nil {
		t.Fatal(e)
	}
	for _, element := range view.Elements {
		if element.Kind != document.ASCII {
			t.Fatal("display label reinterpreted")
		}
	}
	restored, e := d.Restore(h, p)
	if e != nil {
		t.Fatal(e)
	}
	raw, _ := restored.Document().Export()
	if !bytes.Equal(raw[324:], []byte("[BOLD]")) {
		t.Fatal("literal bytes changed")
	}
	opaque := synthetic(t, []byte{0xd0, 1, 7, 0, 0xc3, 12, 0xc3, 7, 0, 1, 0xd0})
	image, e := document.Parse(opaque)
	if e != nil {
		t.Fatal(e)
	}
	_, e = document.NewHistory(image)
	category(t, e, document.UnsupportedBody)
	exact(t, image, opaque)
}
