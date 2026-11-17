package document_test

import (
	"bytes"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

// Original WP23 boundary-{view}-{mode}-g{1,2,4,5} and no-navigation
// XY witnesses establish each character command, not a glyph/cell position.
func TestASCIICommandSequenceAndRevision(t *testing.T) {
	for _, reveal := range []bool{false, true} {
		for _, over := range []bool{false, true} {
			for _, gap := range []int{1, 2, 4, 5, 6} {
				d, e := document.Parse(fixture(t))
				if e != nil {
					t.Fatal(e)
				}
				c, _ := d.CursorAt(gap)
				c = c.WithReveal(reveal)
				var r document.EditResult
				if over {
					r, e = d.TypeoverASCII(c, []byte("XY"))
				} else {
					r, e = d.InsertASCII(c, []byte("XY"))
				}
				if e != nil {
					t.Fatal(e)
				}
				want := fixture(t)
				off, _ := c.Offset()
				end := off
				if over {
					for g := gap; g < d.TokenCount() && g < gap+2; g++ {
						tok, _ := d.Token(g)
						if tok.Kind != document.ASCII {
							break
						}
						end += tok.Span.Length
					}
				}
				want = append(append(bytes.Clone(want[:off]), []byte("XY")...), want[end:]...)
				want[256] |= 8
				exact(t, r.Document, want)
				exact(t, d, fixture(t))
				if !r.Changed || r.Cursor.Gap() != gap+2 || r.Cursor.Reveal() != reveal || r.Document.Revision() == d.Revision() || r.Cursor.Revision() != r.Document.Revision() {
					t.Fatal("revision/gap/view", r)
				}
				failed, e := r.Document.InsertASCII(c, []byte("Z"))
				category(t, e, document.RevisionMismatch)
				if failed.Document != r.Document || failed.Cursor != c || failed.Changed {
					t.Fatal("failed edit changed result")
				}
				original, e := r.Document.OriginalExport()
				if e != nil || !bytes.Equal(original, fixture(t)) {
					t.Fatal("original image lost", e)
				}
			}
		}
	}
}

func TestMutationRefusalIsAtomic(t *testing.T) {
	d, _ := document.Parse(fixture(t))
	c, _ := d.CursorAt(2)
	for _, text := range [][]byte{{'X', 0x1b}, {'X', '\r'}, {'X', 0xc3, 12, 0xc3}, bytes.Repeat([]byte{'x'}, document.MaxMutationTokens+1)} {
		r, e := d.InsertASCII(c, text)
		if e == nil || r.Document != d || r.Cursor != c || r.Changed {
			t.Fatal("non-atomic refusal", r, e)
		}
		exact(t, d, fixture(t))
	}
	for _, body := range [][]byte{{0xc3, 12, 0xc3}, {0xc4, 12, 0xc4}, {0x80}, {0xd0, 1, 4, 0, 4, 0, 1, 0xd0}, {0xc3, 12, 0xc3, 0xc3, 12, 0xc3, 0xc4, 12, 0xc4, 0xc4, 12, 0xc4}, bytes.Repeat([]byte{0xc3, 12, 0xc3, 0xc4, 12, 0xc4}, 3)} {
		raw := synthetic(t, body)
		p, e := document.Parse(raw)
		if e != nil {
			t.Fatal(e)
		}
		if p.CheckMutation() == nil {
			t.Fatal("unsafe body admitted", body)
		}
		pc, _ := p.CursorAt(0)
		r, e := p.InsertASCII(pc, []byte("X"))
		if e == nil || r.Document != p || r.Cursor != pc {
			t.Fatal("unsafe mutation", r, e)
		}
		exact(t, p, raw)
	}
}

func TestTwoPairsLiteralEmptyPairAndNoEdit(t *testing.T) {
	body := []byte{0xc3, 12, 0xc3, 0xc4, 12, 0xc4, 0xc3, 12, 0xc3, 'B', 0xc4, 12, 0xc4}
	d, e := document.Parse(synthetic(t, body))
	if e != nil || d.CheckMutation() != nil {
		t.Fatal(e)
	}
	c, _ := d.CursorAt(3)
	r, e := d.InsertASCII(c, []byte("X"))
	if e != nil {
		t.Fatal(e)
	}
	got, _ := r.Document.Export()
	if !bytes.Equal(got[324:], append(append(bytes.Clone(body[:9]), 'X'), body[9:]...)) {
		t.Fatal("empty pair collapsed")
	}
	unchanged, e := d.InsertASCII(c, nil)
	if e != nil || unchanged.Document != d || unchanged.Cursor != c || unchanged.Changed {
		t.Fatal(unchanged, e)
	}
}
