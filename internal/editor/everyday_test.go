package editor_test

import (
	"bytes"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
)

// pinnedFixture reads the WP01-pinned ORIGIN.WP5 (334 bytes, sha256
// c6cffd…c34aa3d, see internal/document README) from the reference run tree.
func pinnedFixture(t *testing.T) []byte {
	t.Helper()
	const want = "c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d"
	raw, err := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5")
	if err != nil {
		t.Fatal(err)
	}
	sum := sha256.Sum256(raw)
	if got := hex.EncodeToString(sum[:]); got != want {
		t.Fatalf("fixture hash %s, want %s", got, want)
	}
	return raw
}

// synthBody substitutes the body after the pinned prefix, the same sanctioned
// document_test pattern (synthetic evidence for API behavior, never an oracle
// for original output).
func synthBody(t *testing.T, raw, body []byte) []byte {
	t.Helper()
	if len(raw) < 8 {
		t.Fatal("fixture too short")
	}
	n := int(binary.LittleEndian.Uint32(raw[4:8]))
	if n <= 0 || n > len(raw) {
		t.Fatalf("bad prefix length %d", n)
	}
	return append(bytes.Clone(raw[:n]), body...)
}

// T254: the printed-geometry seam is qualified only for explicit HardPage
// structure. Line/Pos stay unqualified while GAP-1 (WP81 layout amendment) is
// open; unknown values are never synthesized.
func TestCursorPositionOfHardPageBoundary(t *testing.T) {
	raw := pinnedFixture(t)
	body := append([]byte("A"), 0xc3, 0x0c, 0xc3) // A [BOLD on
	body = append(body, "BC"...)                  // BC
	body = append(body, 0xc4, 0x0c, 0xc4)         // bold off]
	body = append(body, 'D', 0x0a, 0x0a, 0x0c)    // D HRt HRt HPg
	body = append(body, 'E')                      // E on page 2
	d, err := document.Parse(synthBody(t, raw, body))
	if err != nil {
		t.Fatal(err)
	}
	total := d.TokenCount()
	hp := -1
	for i := total - 1; i >= 0; i-- {
		tok, err := d.Token(i)
		if err != nil {
			t.Fatal(err)
		}
		if tok.Kind == document.HardPage {
			hp = i
			break
		}
	}
	if hp < 0 {
		t.Fatalf("synthetic body has no HardPage (%d tokens)", total)
	}
	pos := func(gap int) editor.Position {
		t.Helper()
		p, err := editor.CursorPositionOf(d, gap)
		if err != nil {
			t.Fatalf("gap %d: %v", gap, err)
		}
		return p
	}
	if got := pos(0); got.Page != 1 {
		t.Fatalf("gap 0 page = %d, want 1", got.Page)
	}
	if _, line, posFlag := pos(0).Qualified(); line || posFlag {
		t.Fatal("Line/Pos qualified while GAP-1 unresolved")
	}
	if got := pos(hp + 1); got.Page != 2 {
		t.Fatalf("gap after HPg page = %d, want 2", got.Page)
	}
	if got := pos(total); got.Page != 2 {
		t.Fatalf("end-of-doc gap past HPg page = %d, want 2", got.Page)
	}
	_, err = editor.CursorPositionOf(d, total+1)
	if err == nil {
		t.Fatal("gap beyond TokenCount must refuse, not synthesize")
	}
}

// EverydayPosition routes the same mapping through the live session cursor.
func TestEverydayPositionSessionRouted(t *testing.T) {
	s, err := editor.New(editor.Config{})
	if err != nil {
		t.Fatal(err)
	}
	p, err := s.EverydayPosition()
	if err != nil {
		t.Fatal(err)
	}
	if p.Page != 1 {
		t.Fatalf("empty New Doc 1 page = %d, want 1", p.Page)
	}
	if _, line, pos := p.Qualified(); line || pos {
		t.Fatal("Line/Pos qualified without a qualified layout engine")
	}
}
