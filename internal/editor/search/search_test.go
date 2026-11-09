package editor

import (
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

func TestFindForward(t *testing.T) {
	raw, err := os.ReadFile("../../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if err != nil {
		t.Fatal(err)
	}
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	got, found := Find(d, nil, []byte("A"), Forward)
	if !found || len(got) == 0 {
		t.Fatalf("forward search failed: %v %v", got, found)
	}
}
