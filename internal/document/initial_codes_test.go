package document_test

import (
	"bytes"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

func TestInitialCodesFastSaveRefusesChangedRetiredResources(t *testing.T) {
	captured, err := os.ReadFile("../../docs/research/reference-runs/mission1-initial-codes/LOADEDY.WP")
	if err != nil {
		t.Fatal(err)
	}
	original, err := document.Parse(captured)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := original.CompactFastSave(); err != nil {
		t.Fatal(err)
	}
	for _, position := range []int{78, 96, 166, 496, 509} {
		candidate := bytes.Clone(captured)
		candidate[position] ^= 1
		doc, err := document.Parse(candidate)
		if err != nil {
			t.Fatal(err)
		}
		if _, err := doc.CompactFastSave(); err == nil {
			t.Fatalf("admitted a changed retired byte at %d", position)
		}
		if raw, err := doc.Export(); err != nil || !bytes.Equal(raw, candidate) {
			t.Fatalf("read-only export changed the bytes at %d", position)
		}
	}
}
