package document_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/document"
	"os"
	"testing"
)

func TestWrapperReplacementCannotRebindCursor(t *testing.T) {
	sameLength, e := os.ReadFile("../../docs/research/continuation/native-edits/runs/wp23-a-boundaries-r1/N0031.WP5")
	if e != nil {
		t.Fatal(e)
	}
	shorter, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/DELETED.WP5")
	if e != nil {
		t.Fatal(e)
	}
	for _, tc := range []struct {
		name string
		raw  []byte
		gap  int
	}{{"same-length-wrong-edit", sameLength, 2}, {"shorter-offset", shorter, 6}} {
		t.Run(tc.name, func(t *testing.T) {
			d, e := document.Parse(fixture(t))
			if e != nil {
				t.Fatal(e)
			}
			other, e := document.Parse(tc.raw)
			if e != nil || other.CheckMutation() != nil {
				t.Fatal("qualified replacement", e)
			}
			c, _ := d.CursorAt(tc.gap)
			revision := d.Revision()
			beforeOffset, _ := c.Offset()
			beforeView, _ := c.WithReveal(true).Present(0, 6)
			*d = *other // Legal public assignment, no reflection/unsafe/private access.
			// This must be refused even if token gap remains in range and files have
			// equal lengths: the incoming cursor belongs to the prior immutable state.
			r, e := d.InsertASCII(c, []byte("Q"))
			category(t, e, document.RevisionMismatch)
			if r.Document != d || r.Cursor != c || r.Changed {
				t.Fatal("replacement accepted stale cursor")
			}
			exact(t, d, tc.raw)
			if c.Revision() != revision || d.Revision() == revision {
				t.Fatal("revision follows mutable wrapper")
			}
			afterOffset, e := c.Offset()
			if e != nil || afterOffset != beforeOffset {
				t.Fatal("captured offset lost", afterOffset, e)
			}
			afterView, e := c.WithReveal(true).Present(0, 6)
			if e != nil || len(afterView.Elements) != len(beforeView.Elements) {
				t.Fatal("captured view lost", e)
			}
			for i, x := range beforeView.Elements {
				if x != afterView.Elements[i] {
					t.Fatal("view rebound to replacement")
				}
			}
		})
	}
}

func TestCursorOffsetSurvivesShorterWrapper(t *testing.T) {
	d, _ := document.Parse(fixture(t))
	c, _ := d.CursorAt(6)
	shorter, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/DELETED.WP5")
	if e != nil {
		t.Fatal(e)
	}
	other, _ := document.Parse(shorter)
	*d = *other
	defer func() {
		if v := recover(); v != nil {
			t.Fatalf("public wrapper replacement made Offset panic: %v", v)
		}
	}()
	offset, e := c.Offset()
	if e != nil || offset != 334 {
		t.Fatal(offset, e)
	}
}

func TestZeroRepeatedAndIndependentWrapperSnapshots(t *testing.T) {
	d, _ := document.Parse(fixture(t))
	alias := *d
	c, _ := d.CursorAt(2)
	revision := c.Revision()
	first, e := d.InsertASCII(c, []byte("X"))
	if e != nil {
		t.Fatal(e)
	}
	firstRevision := first.Cursor.Revision()
	firstBytes, _ := first.Document.Export()
	second, e := d.InsertASCII(c, []byte("Y"))
	if e != nil {
		t.Fatal(e)
	}
	secondBytes, _ := second.Document.Export()
	if firstRevision == second.Cursor.Revision() || bytes.Equal(firstBytes, secondBytes) {
		t.Fatal("independent revisions aliased")
	}
	for i := 0; i < 3; i++ {
		*d = document.Document{}
		offset, e := c.Offset()
		if e != nil || offset != 328 || c.Revision() != revision {
			t.Fatal("zeroing rebound cursor", e)
		}
		if d.Revision() == revision {
			t.Fatal("zeroing retained wrapper revision")
		}
		*d = *second.Document
		_, e = d.TypeoverASCII(c, []byte("Z"))
		category(t, e, document.RevisionMismatch)
		*d = alias // Copying the same immutable state deliberately restores identity.
		if d.Revision() != revision {
			t.Fatal("state copy lost identity")
		}
		again, _ := d.CursorAt(2)
		if again != c {
			t.Fatal("same immutable state/gap cursors differ")
		}
	}
	*first.Document = *second.Document
	if first.Cursor.Revision() != firstRevision {
		t.Fatal("result cursor rebound to replaced result wrapper")
	}
	shown, e := first.Cursor.Present(0, 7)
	if e != nil || shown.Elements[2].Text != "X" {
		t.Fatal("independent result snapshot changed", e)
	}
	_, e = first.Document.InsertASCII(first.Cursor, []byte("Q"))
	category(t, e, document.RevisionMismatch)
}
