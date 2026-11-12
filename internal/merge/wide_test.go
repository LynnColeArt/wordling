package merge_test

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/merge"
)

func wideFixture(t *testing.T, variant, name string) []byte {
	t.Helper()
	path := filepath.Join("../../docs/research/everyday-contract-2026-11-05/native-merge/wide", variant, name+".WP5")
	raw, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	return raw
}

func TestWideSecondaryRequiresExactCountAndPageOwners(t *testing.T) {
	primary, err := merge.CompilePrimary(wideFixture(t, "53", "PRIMARY"))
	if err != nil {
		t.Fatal(err)
	}
	secondary := wideFixture(t, "53", "SECOND")
	if result, err := merge.Evaluate(primary, secondary); result == nil || err != nil {
		t.Fatalf("native 53-field data refused: %v", err)
	}
	firstRecord := bytes.Index(secondary, []byte{0xde, 0x34, 6, 0, 54, 0, 6, 0, 0x34, 0xde})
	if firstRecord < 0 {
		t.Fatal("missing 53-field record delimiter")
	}
	for _, offset := range []int{firstRecord + 4, firstRecord + 16} {
		malformed := bytes.Clone(secondary)
		malformed[offset] ^= 1
		if result, err := merge.Evaluate(primary, malformed); result != nil || err == nil {
			t.Fatalf("unverified secondary owner accepted at %d", offset)
		}
	}
}

func TestSecondaryPageBreakRequiresExactFieldSeparator(t *testing.T) {
	primary, err := merge.CompilePrimary(wideFixture(t, "60", "PRIMARY"))
	if err != nil {
		t.Fatal(err)
	}
	secondary := wideFixture(t, "60", "SECOND")
	if result, err := merge.Evaluate(primary, secondary); result == nil || err != nil {
		t.Fatalf("native two-page data refused: %v", err)
	}
	page := bytes.Index(secondary, []byte{0xd4, 0, 0x1c, 0, 0, 0x16, 0x68, 0x29})
	if page < 0 || secondary[page+32] != 0x8c {
		t.Fatal("missing automatic field page separator")
	}
	for _, offset := range []int{page + 6, page + 8, page + 32} {
		malformed := bytes.Clone(secondary)
		malformed[offset] ^= 1
		if result, err := merge.Evaluate(primary, malformed); result != nil || err == nil {
			t.Fatalf("unverified field page separator accepted at %d", offset)
		}
	}
}
