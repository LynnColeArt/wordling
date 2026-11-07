package document_test

import (
	"bytes"
	"errors"
	"runtime"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
)

const (
	boldOnBytes  = "\xc3\x0c\xc3"
	boldOffBytes = "\xc4\x0c\xc4"
)

func boldNew(t *testing.T) (*document.Document, document.History) {
	t.Helper()
	d, err := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if err != nil {
		t.Fatal(err)
	}
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	return d, h
}

func boldCursor(t *testing.T, d *document.Document, gap int) document.Cursor {
	t.Helper()
	c, err := d.CursorAt(gap)
	if err != nil {
		t.Fatal(err)
	}
	return c
}

func boldBytes(t *testing.T, d *document.Document) []byte {
	t.Helper()
	raw, err := d.Export()
	if err != nil {
		t.Fatal(err)
	}
	return raw
}

func boldBody(t *testing.T, d *document.Document) string {
	t.Helper()
	start, err := boldCursor(t, d, 0).Offset()
	if err != nil {
		t.Fatal(err)
	}
	return string(boldBytes(t, d)[start:])
}

func boldText(t *testing.T, d *document.Document, c document.Cursor, h document.History, text string) (document.EditResult, document.History) {
	t.Helper()
	r, err := d.InsertASCII(c, []byte(text))
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterEdit(r)
	if err != nil {
		t.Fatal(err)
	}
	return r, h
}

func boldBegin(t *testing.T, d *document.Document, h document.History) (document.BoldResult, document.History, document.BoldSpan) {
	t.Helper()
	r, err := d.BeginBold(boldCursor(t, d, d.TokenCount()))
	if err != nil {
		t.Fatalf("begin paired native Bold: %v", err)
	}
	h, err = h.AfterBold(r)
	if err != nil {
		t.Fatal(err)
	}
	s, ok := h.ActiveBold(r.Document())
	if !ok {
		t.Fatal("missing active span")
	}
	return r, h, s
}

func boldRejectHistory(t *testing.T, h document.History, r document.BoldResult) {
	t.Helper()
	next, err := h.AfterBold(r)
	if err == nil || next.Revision() != h.Revision() {
		t.Fatal("unowned/replayed Bold result advanced history")
	}
}

func TestBoldNativePair(t *testing.T) {
	for _, prefix := range []string{"", "A", "r2?"} {
		t.Run(prefix, func(t *testing.T) {
			d, h := boldNew(t)
			if prefix != "" {
				r, next := boldText(t, d, boldCursor(t, d, 0), h, prefix)
				d, h = r.Document, next
			}
			before := boldBytes(t, d)
			r, next, _ := boldBegin(t, d, h)
			got := r.Document()
			if body := boldBody(t, got); body != prefix+boldOnBytes+boldOffBytes {
				t.Fatalf("wrong balanced native pair: %x", body)
			}
			if !r.Changed() || got.Revision() == d.Revision() || got.Birth() != d.Birth() ||
				r.Cursor().Revision() != got.Revision() || !bytes.Equal(before, boldBytes(t, d)) {
				t.Fatal("begin did not conserve original and publish one immutable New revision")
			}
			if next.Qualified() || next.CountKnown() || next.Count() != 0 || !h.Qualified() || !h.CountKnown() {
				t.Fatal("Bold incorrectly qualified or changed stored history")
			}
			if next.Revision() == h.Revision() {
				t.Fatal("history owner did not advance")
			}
			copyDoc := r.Document()
			*copyDoc = document.Document{}
			if r.Document().Revision() != got.Revision() {
				t.Fatal("mutable wrapper retargeted BoldResult")
			}
		})
	}
}

func TestBoldBeginCursor(t *testing.T) {
	d, h := boldNew(t)
	first, h := boldText(t, d, boldCursor(t, d, 0), h, "p!")
	r, _, _ := boldBegin(t, first.Document, h)
	off, err := r.Document().Token(r.Cursor().Gap())
	if err != nil || off.Kind != document.BoldOff || r.Cursor().Gap() != 3 {
		t.Fatalf("cursor is not immediately before Off: gap=%d token=%v err=%v", r.Cursor().Gap(), off.Kind, err)
	}
}

func TestBoldCloseRequiresText(t *testing.T) {
	d, h := boldNew(t)
	open, h, s := boldBegin(t, d, h)
	old := boldBytes(t, open.Document())
	closed, err := open.Document().CloseBold(open.Cursor(), s)
	var failure *document.Failure
	if !errors.As(err, &failure) || failure.Category != document.EmptyBoldSpan {
		t.Fatalf("empty Bold span should refuse: %v", err)
	}
	if closed.Changed() || closed.Cursor() != open.Cursor() || !bytes.Equal(old, boldBytes(t, closed.Document())) {
		t.Fatal("empty close did not conserve native state")
	}
	boldRejectHistory(t, h, closed)
	text, h := boldText(t, open.Document(), open.Cursor().WithReveal(true), h, "z3")
	s, ok := h.ActiveBold(text.Document)
	if !ok {
		t.Fatal("typing did not recover")
	}
	closed, err = text.Document.CloseBold(text.Cursor, s)
	if err != nil || closed.Changed() || closed.Cursor().Gap() != text.Document.TokenCount() ||
		!closed.Cursor().Reveal() || closed.Document().Revision() != text.Document.Revision() ||
		!bytes.Equal(boldBytes(t, closed.Document()), boldBytes(t, text.Document)) {
		t.Fatalf("close did not cross Off on same native revision: %v", err)
	}
	next, err := h.AfterBold(closed)
	if err != nil || next.Qualified() || next.CountKnown() || next.Count() != 0 {
		t.Fatalf("close did not preserve unknown history: %v", err)
	}
	if _, ok := next.ActiveBold(text.Document); ok {
		t.Fatal("closed span remained active")
	}
	boldRejectHistory(t, next, closed)
}

func TestBoldStaleSpan(t *testing.T) {
	d, h := boldNew(t)
	open, h, stale := boldBegin(t, d, h)
	text, h := boldText(t, open.Document(), open.Cursor(), h, "x")
	if r, err := text.Document.CloseBold(text.Cursor, stale); err == nil || r.Changed() {
		t.Fatal("stale active span closed current revision")
	}
	current, ok := h.ActiveBold(text.Document)
	if !ok {
		t.Fatal("missing advanced span")
	}
	if _, err := text.Document.CloseBold(boldCursor(t, text.Document, 0), current); err == nil {
		t.Fatal("non-Off gap closed active span")
	}
	if _, err := text.Document.CloseBold(text.Cursor, document.BoldSpan{}); err == nil {
		t.Fatal("zero span closed active span")
	}
	other, _ := boldNew(t)
	foreign, err := document.Parse(boldBytes(t, text.Document))
	if err != nil {
		t.Fatal(err)
	}
	for _, wrong := range []*document.Document{nil, {}, other, foreign, open.Document()} {
		if _, ok := h.ActiveBold(wrong); ok {
			t.Fatal("foreign document acquired active history")
		}
	}
}

func TestBoldAuthenticHistory(t *testing.T) {
	d, h := boldNew(t)
	r, err := d.BeginBold(boldCursor(t, d, 0))
	if err != nil {
		t.Fatal(err)
	}
	zero := document.BoldResult{}
	if zero.Document() != nil || zero.Cursor() != (document.Cursor{}) || zero.Changed() {
		t.Fatal("wrong zero result accessors")
	}
	boldRejectHistory(t, h, zero)
	_, foreign := boldNew(t)
	boldRejectHistory(t, foreign, r)
	boldRejectHistory(t, document.History{}, r)
	typed, owned := boldText(t, d, boldCursor(t, d, 0), h, "A")
	fresh, err := document.NewHistory(typed.Document)
	if err != nil {
		t.Fatal(err)
	}
	begin, err := typed.Document.BeginBold(typed.Cursor)
	if err != nil {
		t.Fatal(err)
	}
	boldRejectHistory(t, fresh, begin)
	over, err := typed.Document.TypeoverASCII(boldCursor(t, typed.Document, 0), []byte("Q"))
	if err != nil {
		t.Fatal(err)
	}
	unknown, err := owned.AfterEdit(over)
	if err != nil || unknown.Qualified() || unknown.CountKnown() || unknown.Count() != 0 {
		t.Fatalf("expected ordinary unqualified history: %v", err)
	}
	begin, err = over.Document.BeginBold(over.Cursor)
	if err != nil {
		t.Fatal(err)
	}
	boldRejectHistory(t, unknown, begin)
}

func removedTestBoldActiveRejectsOtherEdits(t *testing.T) {
	d, h := boldNew(t)
	start, h := boldText(t, d, boldCursor(t, d, 0), h, "P")
	r, h, s := boldBegin(t, start.Document, h)
	for _, edit := range []struct {
		gap  int
		text string
		over bool
	}{{0, "K", false}, {0, "Q", true}, {r.Document().TokenCount(), "z", false}, {r.Cursor().Gap(), "", false}} {
		apply := r.Document().InsertASCII
		if edit.over {
			apply = r.Document().TypeoverASCII
		}
		candidate, err := apply(boldCursor(t, r.Document(), edit.gap), []byte(edit.text))
		if err != nil {
			t.Fatal(err)
		}
		next, err := h.AfterEdit(candidate)
		if err != nil {
			t.Fatal(err)
		}
		_ = next
		observed, ok := h.ActiveBold(r.Document())
		if !ok || observed != s {
			t.Fatal("rejected edit changed active span")
		}
	}
}

func boldComplete(t *testing.T, d *document.Document, h document.History, text string) (document.BoldResult, document.History) {
	t.Helper()
	open, h, _ := boldBegin(t, d, h)
	insert, h := boldText(t, open.Document(), open.Cursor(), h, text)
	span, ok := h.ActiveBold(insert.Document)
	if !ok {
		t.Fatal("missing span after insertion")
	}
	closed, err := insert.Document.CloseBold(insert.Cursor, span)
	if err != nil {
		t.Fatal(err)
	}
	next, err := h.AfterBold(closed)
	if err != nil {
		t.Fatal(err)
	}
	return closed, next
}

func TestBoldClosedLineage(t *testing.T) {
	d, h := boldNew(t)
	prefix, h := boldText(t, d, boldCursor(t, d, 0), h, "A")
	r, h := boldComplete(t, prefix.Document, h, "BC")
	suffix, h := boldText(t, r.Document(), r.Cursor(), h, "D")
	if body := boldBody(t, suffix.Document); body != "A"+boldOnBytes+"BC"+boldOffBytes+"D" {
		t.Fatalf("completed original-backed body: %x", body)
	}
	r, h = boldComplete(t, suffix.Document, h, "7?")
	if body := boldBody(t, r.Document()); body != "A"+boldOnBytes+"BC"+boldOffBytes+"D"+boldOnBytes+"7?"+boldOffBytes {
		t.Fatalf("second completed pair: %x", body)
	}
	// WP80 makes repeated Bold pairs an explicitly supported edit. The same
	// closed lineage can continue after a saved/typed separator.
	if _, err := r.Document().BeginBold(r.Cursor()); err != nil {
		t.Fatalf("repeated Bold begin after completed pair: %v", err)
	}
}

func TestBoldClosedLineageRejectsNonAppend(t *testing.T) {
	for _, over := range []bool{false, true} {
		d, h := boldNew(t)
		initial, h := boldText(t, d, boldCursor(t, d, 0), h, "p")
		r, h := boldComplete(t, initial.Document, h, "RT")
		apply := r.Document().InsertASCII
		if over {
			apply = r.Document().TypeoverASCII
		}
		edited, err := apply(boldCursor(t, r.Document(), 0), []byte("p"))
		if err != nil {
			t.Fatal(err)
		}
		next, err := h.AfterEdit(edited)
		if err != nil || next.CountKnown() || next.Qualified() {
			t.Fatalf("normal closed edit should preserve unknown history: %v", err)
		}
		r2, err := edited.Document.BeginBold(boldCursor(t, edited.Document, edited.Document.TokenCount()))
		if err != nil {
			t.Fatal(err)
		}
		boldRejectHistory(t, next, r2)
	}
}

func removedTestBoldBeginRefusals(t *testing.T) {
	d, h := boldNew(t)
	text, h := boldText(t, d, boldCursor(t, d, 0), h, "a")
	foreign, _ := boldNew(t)
	loaded, err := document.Parse(boldBytes(t, text.Document))
	if err != nil {
		t.Fatal(err)
	}
	for _, tc := range []struct {
		d *document.Document
		c document.Cursor
	}{
		{text.Document, boldCursor(t, text.Document, 0)},
		{text.Document, text.Cursor.WithReveal(true)},
		{text.Document, boldCursor(t, foreign, 0)},
	} {
		r, err := tc.d.BeginBold(tc.c)
		if err == nil || r.Changed() || r.Cursor() != tc.c || r.Document().Revision() != tc.d.Revision() {
			t.Fatalf("begin refusal failed conservation: %v", err)
		}
		boldRejectHistory(t, h, r)
	}

	loaded, lerr := document.Parse(boldBytes(t, text.Document))
	if lerr != nil {
		t.Fatal(lerr)
	}
	loadedResult, lerr2 := loaded.BeginBold(boldCursor(t, loaded, loaded.TokenCount()))
	if lerr2 != nil || !loadedResult.Changed() {
		t.Fatalf("loaded Bold begin: %v", lerr2)
	}
	boldRejectHistory(t, h, loadedResult)
}

func TestBoldHistoryCannotRearmAfterDeletion(t *testing.T) {
	d, h := boldNew(t)
	typed, h := boldText(t, d, boldCursor(t, d, 0), h, "A")
	deleted, err := typed.Document.Delete(boldCursor(t, typed.Document, 0), document.ForwardDelete, h)
	if err != nil || !deleted.Applied() || deleted.Document().TokenCount() != 0 {
		t.Fatalf("expected actual deletion back to empty: %v", err)
	}
	r, err := deleted.Document().BeginBold(deleted.Cursor())
	if err != nil {
		t.Fatal(err)
	}
	boldRejectHistory(t, deleted.History(), r)
	fresh, err := document.NewHistory(deleted.Document())
	if err != nil {
		t.Fatal(err)
	}
	boldRejectHistory(t, fresh, r)
}

func TestBoldPrefixAndRejectedNativeShapes(t *testing.T) {
	d, h := boldNew(t)
	before := boldBytes(t, d)
	r, _, _ := boldBegin(t, d, h)
	after := boldBytes(t, r.Document())
	image, err := wp51.Parse(before)
	if err != nil {
		t.Fatal(err)
	}
	meta := image.Inspect()
	if meta.Body.Offset != 324 || len(after) != len(before)+6 {
		t.Fatal("unexpected genuine New layout or body delta")
	}
	want := bytes.Clone(before)
	for _, packet := range meta.Packets {
		if packet.Type == 6 {
			want[packet.Data.Offset] |= 8
		}
	}
	if !bytes.Equal(want, after[:meta.Body.Offset]) {
		t.Fatal("begin changed unrelated native prefix bytes")
	}
	for _, body := range []string{boldOffBytes, boldOnBytes + boldOnBytes + "x" + boldOffBytes + boldOffBytes, "\x01"} {
		image := append(bytes.Clone(before), body...)
		bad, err := document.Parse(image)
		if err != nil {
			t.Fatal(err)
		}
		if err := bad.CheckMutation(); err == nil {
			t.Fatalf("malformed native body admitted: %x", body)
		}
		c := boldCursor(t, bad, bad.TokenCount())
		refused, err := bad.BeginBold(c)
		if err == nil || refused.Changed() || refused.Cursor() != c || !bytes.Equal(boldBytes(t, refused.Document()), image) {
			t.Fatal("rejected native body changed")
		}
	}
}

func TestBoldOwnerCeiling(t *testing.T) {
	for _, slack := range []int{2, 1} {
		d, h := boldNew(t)
		r, h := boldText(t, d, boldCursor(t, d, 0), h, string(bytes.Repeat([]byte{'s'}, document.MaxMutationTokens-slack)))
		out, err := r.Document.BeginBold(r.Cursor)
		if slack == 2 {
			if err != nil || out.Document().TokenCount() != document.MaxMutationTokens {
				t.Fatalf("reachable exact owner ceiling refused: %v", err)
			}
			if _, err := h.AfterBold(out); err != nil {
				t.Fatal(err)
			}
		} else {
			var failure *document.Failure
			if !errors.As(err, &failure) || failure.Category != document.MutationLimit ||
				out.Changed() || out.Document().Revision() != r.Document.Revision() {
				t.Fatalf("overflow did not refuse before publication: %v", err)
			}
		}
	}
}

func TestBoldAllocationBounds(t *testing.T) {
	overflowDoc, overflowHistory := boldNew(t)
	overflow, _ := boldText(t, overflowDoc, boldCursor(t, overflowDoc, 0), overflowHistory,
		string(bytes.Repeat([]byte{'x'}, document.MaxMutationTokens-1)))
	d, h := boldNew(t)
	initial, h := boldText(t, d, boldCursor(t, d, 0), h, string(bytes.Repeat([]byte{'m'}, document.MaxMutationTokens-3)))
	open, active, _ := boldBegin(t, initial.Document, h)
	text, active := boldText(t, open.Document(), open.Cursor(), active, "p")
	s, ok := active.ActiveBold(text.Document)
	if !ok {
		t.Fatal("missing active span")
	}
	for _, tc := range []struct {
		name string
		max  uint64
		run  func() error
	}{
		{"begin-at-limit", 16 << 20, func() error { _, e := initial.Document.BeginBold(initial.Cursor); return e }},
		{"begin-over-owner-limit", 16 << 20, func() error {
			refused, err := overflow.Document.BeginBold(overflow.Cursor)
			var failure *document.Failure
			if !errors.As(err, &failure) || failure.Category != document.MutationLimit ||
				refused.Changed() || refused.Document().Revision() != overflow.Document.Revision() ||
				refused.Cursor() != overflow.Cursor {
				return errors.New("owner overflow did not refuse without changing native state")
			}
			return nil
		}},
		{"close-at-limit", 8 << 20, func() error { _, e := text.Document.CloseBold(text.Cursor, s); return e }},
		{"history", 32 << 10, func() error { _, e := h.AfterBold(open); return e }},
	} {
		var peak uint64
		for range 8 {
			var before, after runtime.MemStats
			runtime.ReadMemStats(&before)
			if err := tc.run(); err != nil {
				t.Fatal(err)
			}
			runtime.ReadMemStats(&after)
			peak = max(peak, after.TotalAlloc-before.TotalAlloc)
		}
		if peak > tc.max {
			t.Fatalf("%s allocated %d bytes, limit %d", tc.name, peak, tc.max)
		}
		t.Logf("%s peak=%d bound=%d samples=8", tc.name, peak, tc.max)
	}
}
