package merge_test

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
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

func TestFormattedWrappedFieldsKeepNativeAttributes(t *testing.T) {
	primary, err := merge.CompilePrimary(wideFixture(t, "formatted", "PRIMARY"))
	if err != nil {
		t.Fatal(err)
	}
	secondary := wideFixture(t, "formatted", "EDITED")
	result, err := merge.Evaluate(primary, secondary)
	if err != nil {
		t.Fatal(err)
	}
	raw, err := result.Export()
	if err != nil {
		t.Fatal(err)
	}
	for _, span := range [][]byte{
		[]byte("\xc3\x0c\xc3A alphaXXXX " + string(bytes.Repeat([]byte("beta gamma delta alpha "), 3)) + "beta gamma delta end\xc4\x0c\xc4"),
		[]byte("\xc3\x0e\xc3Bunderlined\xc4\x0e\xc4"),
	} {
		if !bytes.Contains(raw, span) {
			t.Fatalf("missing native formatted span %q", span)
		}
	}
	// A well framed but unknown attribute and an unmatched supported
	// attribute must both be refused instead of leaking into the result.
	for _, change := range [][2][]byte{
		{{0xc3, 0x0c, 0xc3}, {0xc3, 0x01, 0xc3}},
		{{0xc4, 0x0c, 0xc4}, {' ', ' ', ' '}},
	} {
		malformed := bytes.Replace(secondary, change[0], change[1], 1)
		if d, err := merge.Evaluate(primary, malformed); d != nil || err == nil {
			t.Fatalf("accepted invalid formatting %x", change[1])
		}
	}
}

func TestOverlappingAttributesAcrossSecondaryPage(t *testing.T) {
	primary, err := merge.CompilePrimary(wideFixture(t, "overlap-page", "PRIMARY"))
	if err != nil {
		t.Fatal(err)
	}
	source := wideFixture(t, "overlap-page", "SECOND")
	d, err := merge.Evaluate(primary, source)
	if err != nil {
		t.Fatal(err)
	}
	raw, err := d.Export()
	if err != nil {
		t.Fatal(err)
	}
	span := "\xc3\x0c\xc3BoldStart \xc3\x0e\xc3" +
		strings.Repeat("A alpha beta gamma delta ", 4) +
		"\xc4\x0c\xc4UnderTail\xc4\x0e\xc4 PlainEnd"
	if !bytes.Contains(raw, []byte(span)) {
		t.Fatal("merge did not carry both attributes across the removed source page separator")
	}

	page := bytes.Index(source, []byte{0xd4, 0, 0x1c, 0, 0, 0x16, 0x68, 0x29})
	if page < 0 || source[page+32] != 0x0b {
		t.Fatal("missing source soft page boundary")
	}
	source[page+8] ^= 1
	if d, err := merge.Evaluate(primary, source); d != nil || err == nil {
		t.Fatal("accepted an invalid page cache inside overlapping attributes")
	}
}
