package document_test

import (
	"github.com/lynncoleart/wordling/internal/document"
	"os"
	"testing"
)

// Consumer-visible admission errors remain distinct from broad native framing
// success. These are API contracts for WP26/27, not generic native corruption.
func TestMutationFailureCategories(t *testing.T) {
	for _, tc := range []struct {
		name     string
		raw      []byte
		category document.Category
	}{
		{"opaque", synthetic(t, []byte{0x80}), document.UnsupportedBody},
		{"unmatched", synthetic(t, []byte{0xc4, 12, 0xc4}), document.UnsupportedBody},
		{"resource", func() []byte { b := fixture(t); b[66] = 'D'; return b }(), document.UnsupportedResource},
		{"metadata", func() []byte { b := fixture(t); b[264] = 0; return b }(), document.UnsupportedMetadata},
	} {
		t.Run(tc.name, func(t *testing.T) {
			d, e := document.Parse(tc.raw)
			if e != nil {
				t.Fatal(e)
			}
			category(t, d.CheckMutation(), tc.category)
			c, _ := d.CursorAt(0)
			r, e := d.InsertASCII(c, []byte("X"))
			category(t, e, tc.category)
			if r.Document != d || r.Cursor != c || r.Changed {
				t.Fatal("failed edit consumed revision")
			}
			exact(t, d, tc.raw)
		})
	}
	raw, e := os.ReadFile("../../docs/research/continuation/native-edits/runs/wp23-a-modes-r1/N0003.WP5")
	if e != nil {
		t.Fatal(e)
	}
	d, e := document.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	category(t, d.CheckMutation(), document.UnsupportedPrefix)
	exact(t, d, raw)
	d, _ = document.Parse(fixture(t))
	c, _ := d.CursorAt(1)
	_, e = d.TypeoverASCII(c, []byte{'X', 0x1b})
	category(t, e, document.InvalidASCII)
	var nilDocument *document.Document
	category(t, nilDocument.CheckMutation(), document.InvalidDocument)
}
