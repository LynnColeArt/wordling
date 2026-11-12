package merge_test

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/merge"
)

func source(t *testing.T, file string) []byte {
	t.Helper()
	b, err := os.ReadFile(filepath.Join("../../docs/research/reference-runs/2026-10-29-extended-04/CMD51-134", file+".WP5"))
	if err != nil {
		t.Fatal(err)
	}
	return b
}

func literalEdit(t *testing.T, raw []byte, letter byte) []byte {
	t.Helper()
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	c, err := d.CursorAt(0)
	if err != nil {
		t.Fatal(err)
	}
	edited, err := d.InsertMergeLiteral(c, []byte{letter})
	if err != nil {
		t.Fatal(err)
	}
	got, err := edited.Document.Export()
	if err != nil {
		t.Fatal(err)
	}
	at, _ := c.Offset()
	prefix := bytes.Clone(raw[:at])
	prefix[256] |= 8
	want := append(append(prefix, letter), raw[at:]...)
	if !bytes.Equal(got, want) {
		t.Fatal("edit did not preserve original owners")
	}
	if edited.Document.Birth() != d.Birth() || edited.Cursor.Gap() != 1 {
		t.Fatal("edit did not preserve lineage and cursor")
	}
	return got
}

func TestEditedSourcesEvaluateWithOriginalPageBoundaries(t *testing.T) {
	p := literalEdit(t, source(t, "PRIMARY"), 'X')
	s := literalEdit(t, source(t, "SECOND"), 'Z')
	plan, err := merge.CompilePrimary(p)
	if err != nil {
		t.Fatal(err)
	}
	d, err := merge.Evaluate(plan, s)
	if err != nil {
		t.Fatal(err)
	}
	at, _ := d.CursorAt(0)
	start, _ := at.Offset()
	got, _ := d.Export()
	if string(got[start:]) != "XHello ZAlice\f\fXHello Bob\f" {
		t.Fatalf("unexpected body %q", got[start:])
	}
}

func TestMergeLiteralRefusesOperandAndCache(t *testing.T) {
	d, err := document.Parse(source(t, "PRIMARY"))
	if err != nil {
		t.Fatal(err)
	}
	for gap := 7; gap <= d.TokenCount(); gap++ {
		cursor, _ := d.CursorAt(gap)
		edit, err := d.InsertMergeLiteral(cursor, []byte("X"))
		if err == nil || edit.Document.Revision() != d.Revision() || edit.Cursor != cursor {
			t.Fatalf("modified protected gap %d", gap)
		}
	}
	raw := source(t, "PRIMARY")
	raw[len(raw)-32+5] ^= 1
	if p, err := merge.CompilePrimary(raw); err == nil || p.Valid() {
		t.Fatal("compiled unqualified formatter owner")
	}
}
