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
	// GAP-1 narrowed 11-09 (tracer design-decisions-3204c4f2e908):
	// explicit-boundary lines now QUALIFY Line/Pos; the old unqualified
	// assertion was a T254-era conservative rule, superseded by the reconciled
	// EE-A05 frames. Only Tab payloads (GAP-1b) and opaque structure
	// disqualify.
	if _, lineOK, posOK := pos(0).Qualified(); !lineOK || !posOK {
		t.Fatalf("explicit-boundary Line/Pos must qualify after GAP-1 narrowing: %+v", pos(0))
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

// T254/T255: the printed-geometry seam is frame-reconciled against the
// original-produced EE-A05 journey document (FLOW.WP + its 80x25 frames,
// qualification/flow/exports). Expected values are the documented original
// status lines, cited per case; values the WP82 walker cannot qualify report
// zero and are asserted as unknown, never synthesized.
func TestEverydayPositionReconcilesEHA05Frames(t *testing.T) {
	raw, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/qualification/flow/exports/FLOW.WP")
	if err != nil {
		t.Fatal(err)
	}
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	// FLOW.WP native census (WP82 probe): 253 ASCII, 111 HRt, 1 SRt,
	// 5 page-structure tokens, 1 Tab, 1 Underline pair, 2 DSRt.
	census := map[document.Kind]int{}
	for i := 0; i < d.TokenCount(); i++ {
		tok, err := d.Token(i)
		if err != nil {
			t.Fatal(err)
		}
		census[tok.Kind]++
	}
	if census[document.HardReturn] != 111 ||
		census[document.SoftReturn] != 1 || census[document.Tab] != 1 ||
		census[document.UnderlineOn] != 1 {
		t.Fatalf("FLOW.WP census drifted: %v", census)
	}

	// Frame 06 (line 1 end): "A faithful reconstruction needs more than a blue
	// screen. Menus," = 63 chars; native line 0 ends in the SRt at gap 63
	// (probe: first break at 63). Cursor at gap 63 → Pos 1.0+63/10 = 7.3",
	// Ln 1.0" (Pg 1) — original frame: Pg 1 Ln 1" Pos 7.3".
	p, err := editor.CursorPositionOf(d, 63)
	if err != nil {
		t.Fatal(err)
	}
	if _, line, posFlag := p.Qualified(); !line || !posFlag {
		t.Fatalf("line 0 cursor lost qualification: %+v", p)
	}
	if p.Page != 1 || p.Line != 1 || p.Pos != 64 {
		t.Fatalf("frame 06 = %+v, want Ln row1 Pos col 64 (65th cell)", p)
	}
	ln, posIn := p.Printed()
	if ln != 1.0 || posIn != 7.3 { // 1+63/10
		t.Fatalf("frame 06 printed = %.2f/%.2f, want 1.00/7.30", ln, posIn)
	}

	// Frame 07 (Down after End): desired horizontal = 63 clipped to the next
	// line's 58 cells → Pos 6.8". The seam maps cursor gaps only; the Down
	// key's 58-cell landing is asserted by finding the HRt gap.
	body58 := 58
	hr2 := 122 + body58 - 58 // probe: HRt at 122 after 58 more ASCII
	_ = hr2
	hp, err := editor.CursorPositionOf(d, 122)
	if err != nil {
		t.Fatal(err)
	}
	if hp.Pos != 59 || hp.Line != 2 {
		t.Fatalf("frame 07 landing = %+v, want line2 col 59 (58 cells + 1)", hp)
	}
	ln, posIn = hp.Printed()
	if ln != 1.1666666666666667 || posIn != 6.8 {
		t.Fatalf("frame 07 printed = %.2f/%.2f, want 1.17/6.80", ln, posIn)
	}

	// Frame 08 (Down to empty line): Ln 1.33" Pos 1.
	pos08, err := editor.CursorPositionOf(d, 123)
	if err != nil {
		t.Fatal(err)
	}
	if pos08.Line != 3 || pos08.Pos != 1 {
		t.Fatalf("frame 08 = %+v, want Ln row 3 Pos 1", pos08)
	}

	// Frame 16 (document end): Pg 3 qualified via the two composite breaks.
	// Ln 2.17" Pos 3" in the original frame are NOT reproducible by WP82: the
	// Tab at gap 144 precedes the end, and GAP-1b (tab-stop decode plus the
	// tabbed-line cursor-validity model behind frames 10/11/12) is WP81-owned.
	// Unknown is expected here; it is evidence, not failure.
	lastGap := d.TokenCount()
	pos16, err := editor.CursorPositionOf(d, lastGap)
	if err != nil {
		t.Fatal(err)
	}
	if pageOK, _, _ := pos16.Qualified(); !pageOK || pos16.Page != 3 {
		t.Fatalf("document end page = %+v, want Pg 3", pos16)
	}
	if _, lineOK, posOK := pos16.Qualified(); lineOK || posOK {
		t.Fatalf("Line/Pos past an undecoded Tab must stay unknown, got %+v", pos16)
	}
}

// The Tab line (frame 10: Pos 3.0" on Ln 1.67") is GAP-1b: the walker
// disqualifies Line/Pos rather than guessing the relative stop.
func TestEverydayPositionTabDisqualifies(t *testing.T) {
	raw := pinnedFixture(t)
	body := append([]byte("A"), 0x0a, 0x0a)                                   // A HRt
	body = append(body, 0xc1, 0x02, 0x08, 0x07, 0x08, 0x07, 0x0f, 0x00, 0xc1) // Tab
	body = append(body, 'X')
	d, err := document.Parse(synthBody(t, raw, body))
	if err != nil {
		t.Fatal(err)
	}
	p, err := editor.CursorPositionOf(d, d.TokenCount())
	if err != nil {
		t.Fatal(err)
	}
	if pageOK, lineOK, posOK := p.Qualified(); !pageOK || lineOK || posOK {
		t.Fatalf("tabbed line must disqualify Line/Pos, got %+v", p)
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
	// GAP-1 narrowed 11-09: boundary-only structures (this empty document) are
	// fully qualified; see the supersession note in
	// TestCursorPositionOfHardPageBoundary.
	if _, lineOK, posOK := p.Qualified(); !lineOK || !posOK {
		t.Fatalf("empty-document Line/Pos must qualify: %+v", p)
	}
	if p.Line != 1 || p.Pos != 1 {
		t.Fatalf("empty document must read Ln 1 Pos 1: %+v", p)
	}
}
