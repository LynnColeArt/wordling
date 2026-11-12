package document_test

import (
	"bytes"
	"errors"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

const fastSaveFlowPath = "../../docs/research/everyday-contract-2026-11-05/qualification/flow/exports/FLOW.WP"

func readFastSaveFixture(t *testing.T, path string) []byte {
	t.Helper()
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	return data
}

func TestCompactFastSaveMatchesOriginalRewrite(t *testing.T) {
	originalCompact := readFastSaveFixture(t, "../tui/evidence/everyday/FLOW.WP")
	cases := []struct {
		name string
		path string
	}{
		{"first saved index", fastSaveFlowPath},
		{"relocated middle index", "../../docs/research/continuation/resaved-prefix/runs/w42-two-bold-baseline/r2/W42EDIT.WP5"},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			raw := readFastSaveFixture(t, tc.path)
			source, err := document.Parse(raw)
			if err != nil {
				t.Fatal(err)
			}
			compact, err := source.CompactFastSave()
			if err != nil {
				t.Fatal(err)
			}
			got, err := compact.Export()
			if err != nil {
				t.Fatal(err)
			}
			want := append(bytes.Clone(originalCompact[:324]), raw[564:]...)
			if !bytes.Equal(got, want) {
				t.Fatal("compaction changed native body or differs from the original compact prefix")
			}
			original, err := compact.OriginalExport()
			if err != nil || !compact.Birth().IsLoaded() || !bytes.Equal(original, raw) {
				t.Fatal("compaction lost original loaded bytes", err)
			}
			untouched, err := source.Export()
			if err != nil || !bytes.Equal(untouched, raw) || source.Revision() == compact.Revision() {
				t.Fatal("compaction modified the input revision", err)
			}
			cursor, err := compact.CursorAt(compact.TokenCount())
			if err != nil {
				t.Fatal(err)
			}
			result, err := compact.InsertASCII(cursor, []byte(" REEDIT"))
			if err != nil || !result.Changed {
				t.Fatal("compacted native revision did not admit a subsequent edit", err)
			}
			edited, err := result.Document.Export()
			if err != nil || !bytes.Equal(edited[324:], append(bytes.Clone(raw[564:]), []byte(" REEDIT")...)) {
				t.Fatal("subsequent edit did not preserve prior body owners", err)
			}
		})
	}
}

func TestCompactFastSaveRefusesUnqualifiedOwners(t *testing.T) {
	original := readFastSaveFixture(t, fastSaveFlowPath)
	cases := []struct {
		name     string
		change   func([]byte) []byte
		category document.Category
	}{
		{"unknown live entry", func(b []byte) []byte { b[56] = 9; return b }, document.UnsupportedPrefix},
		{"unknown deleted extent", func(b []byte) []byte { b[66] ^= 1; return b }, document.UnsupportedPrefix},
		{"nonzero unused index payload", func(b []byte) []byte { b[535] = 1; return b }, document.UnsupportedPrefix},
		{"unqualified body owner", func(b []byte) []byte { return append(b, 0xa9) }, document.UnsupportedBody},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			raw := tc.change(bytes.Clone(original))
			source, err := document.Parse(raw)
			if err != nil {
				t.Fatal(err)
			}
			compact, err := source.CompactFastSave()
			var failure *document.Failure
			if compact != nil || !errors.As(err, &failure) || failure.Category != tc.category {
				t.Fatalf("expected compaction refusal %s, got %v", tc.category, err)
			}
			untouched, err := source.Export()
			if err != nil || !bytes.Equal(untouched, raw) {
				t.Fatal("failed compaction changed original bytes", err)
			}
		})
	}
}
