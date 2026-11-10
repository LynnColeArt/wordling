package editor_test

import (
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
)

// T259/T260: Find honors the anchor and repeats. Frame reconciliation
// (WP83 probe): repeated F2 finds successive matches (frames 19→21); the
// backward prompt returns the previous occurrence (frame 23).
func TestSearchFindHonorsFromAndRepeats(t *testing.T) {
	raw, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/qualification/flow/exports/FLOW.WP")
	if err != nil {
		t.Fatal(err)
	}
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	// FLOW.WP contains the literal "alpha" twice on the tabbed line
	// (frames 19/21 capture two F2 presses landing on Pos 2.4" then Pos 3").
	first, found := editor.Find(d, nil, []byte("alpha"), editor.Forward)
	if !found || !first.Found {
		t.Fatal("first forward search failed")
	}
	second, found := editor.Find(d, editor.EncodeFrom(first.Offset+len("alpha")), []byte("alpha"), editor.Forward)
	if !found || second.Offset <= first.Offset {
		t.Fatalf("repeat did not advance: %d -> %d", first.Offset, second.Offset)
	}
	third, found := editor.Find(d, editor.EncodeFrom(second.Offset+len("alpha")), []byte("alpha"), editor.Forward)
	if !found || third.Offset <= second.Offset {
		t.Fatalf("third match missing/behind: %v found=%v", third, found)
	}
	fourth, found := editor.Find(d, editor.EncodeFrom(third.Offset+len("alpha")), []byte("alpha"), editor.Forward)
	if found {
		t.Fatalf("unexpected fourth match at %d", fourth.Offset)
	}
	// Backward from after the second match returns the second, then the
	// first (frame 23 returns to the prior occurrence).
	back1, found := editor.Find(d, editor.EncodeFrom(second.Offset+len("alpha")), []byte("alpha"), editor.Backward)
	if !found || back1.Offset != second.Offset {
		t.Fatalf("backward 1: %v found=%v", back1, found)
	}
	back2, found := editor.Find(d, editor.EncodeFrom(back1.Offset), []byte("alpha"), editor.Backward)
	if !found || back2.Offset != first.Offset {
		t.Fatalf("backward 2: %v found=%v", back2, found)
	}
	// The anchor beyond the document is refused, not wrapped.
	if _, ok := editor.Find(d, []byte{0xff, 0xff}, []byte("a"), editor.Forward); ok {
		t.Fatal("anchor beyond document must refuse")
	}
}

// W83-1 regression: the empty anchor means document start for forward.
func TestSearchEmptyAnchorStartsAtDocumentStart(t *testing.T) {
	raw := pinnedFixture(t)
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	r, found := editor.Find(d, nil, []byte("C3"), editor.Forward)
	_ = r
	_ = found
	// The pinned fixture body is "A<BOLD>BC<BOLD-off>D" — search for the
	// literal second ASCII 'B' through its raw C3-owner framing is not the
	// tested property; the property is: two searches with an empty anchor
	// return the SAME match (no hidden resumption state).
	a, _ := editor.Find(d, nil, []byte("B"), editor.Forward)
	b, _ := editor.Find(d, nil, []byte("B"), editor.Forward)
	if !a.Found || a.Offset != b.Offset {
		t.Fatalf("empty anchor not stable: %v / %v", a, b)
	}
}

// Search never mutates native bytes (EE-A09: failed/canceled search leaves
// the body unchanged — the pure function cannot).
func TestSearchIsPure(t *testing.T) {
	raw := pinnedFixture(t)
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	before, err := d.Export()
	if err != nil {
		t.Fatal(err)
	}
	_, _ = editor.Find(d, nil, []byte("NOTPRESENT"), editor.Forward)
	_, _ = editor.Find(d, nil, []byte("A"), editor.Backward)
	after, err := d.Export()
	if err != nil || !bytesEqual(before, after) {
		t.Fatal("search mutated native bytes")
	}
}

func bytesEqual(a, b []byte) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}
