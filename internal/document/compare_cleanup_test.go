package document_test

import (
	"bytes"
	"encoding/binary"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

func compareCleanupDocument(t *testing.T, body []byte) *document.Document {
	t.Helper()
	raw, err := os.ReadFile("../../docs/research/reference-runs/mission1-document-compare/BEFORE.WP")
	if err != nil {
		t.Fatal(err)
	}
	raw = append(raw[:binary.LittleEndian.Uint32(raw[4:8]):binary.LittleEndian.Uint32(raw[4:8])], body...)
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	return d
}
func cleanupBody(t *testing.T, d *document.Document) []byte {
	t.Helper()
	raw, err := d.Export()
	if err != nil {
		t.Fatal(err)
	}
	return raw[binary.LittleEndian.Uint32(raw[4:8]):]
}
func TestRemoveComparisonMarksBoundedSemantics(t *testing.T) {
	const ron = "\xc3\x0a\xc3"
	const roff = "\xc4\x0a\xc4"
	const son = "\xc3\x0d\xc3"
	const soff = "\xc4\x0d\xc4"
	cases := []struct {
		name, body, want string
		changed          bool
	}{
		{"plain", "plain\ntext", "plain\ntext", false},
		{"empty", "", "", false},
		{"redline", ron + "new" + roff, "new", true},
		{"strikeout", son + "old" + soff, "", true},
		{"replacement", ron + "new\n" + roff + son + "old\n" + soff, "new\n", true},
		{"manual marks and disjoint spans", "a" + ron + "b" + roff + "c" + son + "d" + soff + "e" + ron + "f" + roff + son + "g" + soff, "abcef", true},
		{"redline inside strikeout", son + "a" + ron + "b" + roff + "c" + soff, "", true},
		{"strikeout inside redline", ron + "a" + son + "b" + soff + "c" + roff, "ac", true},
		{"overlapping marks", ron + "a" + son + "b" + roff + "c" + soff + "d", "ad", true},
		{"removed hard return", "a" + son + "\nb\n" + soff + "c", "ac", true},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			for _, reveal := range []bool{false, true} {
				d := compareCleanupDocument(t, []byte(tc.body))
				before, _ := d.Export()
				c, _ := d.CursorAt(0)
				c = c.WithReveal(reveal)
				edit, err := d.RemoveComparisonMarks(c)
				if err != nil {
					t.Fatal(err)
				}
				if !bytes.Equal(cleanupBody(t, edit.Document), []byte(tc.want)) || edit.Changed != tc.changed || edit.Cursor.Gap() != edit.Document.TokenCount() || edit.Cursor.Reveal() != reveal {
					t.Fatalf("result %q changed=%v cursor=%d", cleanupBody(t, edit.Document), edit.Changed, edit.Cursor.Gap())
				}
				after, _ := d.Export()
				if !bytes.Equal(before, after) {
					t.Fatal("input revision mutated")
				}
				again, err := edit.Document.RemoveComparisonMarks(edit.Cursor)
				if err != nil || again.Changed || again.Document.Revision() != edit.Document.Revision() {
					t.Fatal("cleanup not idempotent", err)
				}
			}
		})
	}
}
func TestRemoveComparisonMarksOriginalDOSInputs(t *testing.T) {
	for _, tc := range []struct{ file, want string }{{"COMPARE.WP", "Alpha new tail"}, {"MULTI.WP", "Overview\nAlpha new tail\nClosing"}} {
		raw, err := os.ReadFile("../../docs/research/reference-runs/mission1-document-compare/" + tc.file)
		if err != nil {
			t.Fatal(err)
		}
		d, err := document.Parse(raw)
		if err != nil {
			t.Fatal(err)
		}
		c, _ := d.CursorAt(0)
		edit, err := d.RemoveComparisonMarks(c)
		if err != nil || string(cleanupBody(t, edit.Document)) != tc.want {
			t.Fatalf("%s: %v", tc.file, err)
		}
	}
}
func TestRemoveComparisonMarksRefusesWithoutPartialEdit(t *testing.T) {
	for _, body := range []string{"\xc3\x0d\xc3THE FOLLOWING TEXT WAS MOVED\xc4\x0d\xc4", "\xc3\x0c\xc3bold\xc4\x0c\xc4", "\xc3\x0a\xc3new\xc4\x0a\xc4\t", "\xc3\x0a\xc3new\xc4\x0a\xc4THE FOLLOWING TEXT WAS MOVED"} {
		d := compareCleanupDocument(t, []byte(body))
		c, _ := d.CursorAt(0)
		before, _ := d.Export()
		edit, err := d.RemoveComparisonMarks(c)
		if err == nil || edit.Document != d || edit.Cursor != c || edit.Changed {
			t.Fatal("unsupported body was changed", err)
		}
		after, _ := d.Export()
		if !bytes.Equal(before, after) {
			t.Fatal("refusal mutated input")
		}
	}
	d := compareCleanupDocument(t, []byte("\xc3\x0a\xc3new\xc4\x0a\xc4"))
	other := compareCleanupDocument(t, []byte("other"))
	foreign, _ := other.CursorAt(0)
	edit, err := d.RemoveComparisonMarks(foreign)
	if err == nil || edit.Document != d || edit.Changed {
		t.Fatal("foreign cursor admitted")
	}
}
