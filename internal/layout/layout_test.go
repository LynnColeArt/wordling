package layout_test

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"math"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
)

func TestProjectSimpleParagraph(t *testing.T) {
	s := layout.Settings{
		PageWidthInches: 8.5, PageHeightInches: 11,
		MarginLeftInches: 1, MarginRightInches: 1,
		MarginTopInches: 1, MarginBottomInches: 1,
		CPI: 10, LineSpacing: 1, HyphenationNo: true, FullJustification: true, RelativeTabSet: true,
	}
	tokens := make([]document.Token, 0, 80)
	for i := 0; i < 80; i++ {
		tokens = append(tokens, document.Token{Kind: document.ASCII, Raw: []byte("A")})
	}
	out := layout.Project(tokens, s)
	if len(out.Lines) < 2 {
		t.Fatalf("expected wrapped lines, got %d", len(out.Lines))
	}
	if out.Lines[0].Page != 1 || len(out.Lines[0].Tokens) == 0 {
		t.Fatalf("bad first line %v", out.Lines[0])
	}
}

func TestProjectExplicitPageOnce(t *testing.T) {
	s := layout.Settings{
		PageWidthInches: 8.5, PageHeightInches: 11,
		MarginLeftInches: 1, MarginRightInches: 1,
		MarginTopInches: 1, MarginBottomInches: 1,
		CPI: 10, LineSpacing: 1, HyphenationNo: true,
	}
	// A hard page token should begin a new page, even with no other text.
	tokens := []document.Token{
		{Kind: document.ASCII},
		{Kind: document.HardPage},
		{Kind: document.ASCII},
	}
	out := layout.Project(tokens, s)
	if len(out.Lines) != 2 || out.Lines[0].Page != 1 || out.Lines[1].Page != 2 {
		t.Fatalf("one explicit page boundary = %+v", out.Lines)
	}
}

func matchedSettings() layout.Settings {
	return layout.Settings{
		PageWidthInches: 8.5, PageHeightInches: 11,
		MarginLeftInches: 1, MarginRightInches: 1,
		MarginTopInches: 1, MarginBottomInches: 1,
		CPI: 10, LineSpacing: 1, HyphenationNo: true,
		FullJustification: true, RelativeTabSet: true,
	}
}

const refDir = "../../docs/research/everyday-contract-2026-11-05/"

func original(t *testing.T, path string) (*document.Document, []byte) {
	t.Helper()
	raw, err := os.ReadFile(refDir + path)
	if err != nil {
		t.Fatal(err)
	}
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	return d, raw
}

func parseBody(t *testing.T, body []byte) *document.Document {
	t.Helper()
	_, raw := original(t, "r3/EVERY.WP")
	d, err := document.Parse(append(bytes.Clone(raw[:324]), body...))
	if err != nil {
		t.Fatal(err)
	}
	return d
}

func body(t *testing.T, d *document.Document) []byte {
	t.Helper()
	var out []byte
	for i := 0; i < d.TokenCount(); i++ {
		token, err := d.Token(i)
		if err != nil {
			t.Fatal(err)
		}
		out = append(out, token.Raw...)
	}
	return out
}

func applyFlow(t *testing.T, d *document.Document, gap int) document.EditResult {
	t.Helper()
	c, err := d.CursorAt(gap)
	if err != nil {
		t.Fatal(err)
	}
	p, err := layout.PlanReflow(d, matchedSettings())
	if err != nil {
		t.Fatal(err)
	}
	out, err := d.AdoptReflow(c, p)
	if err != nil {
		t.Fatal(err)
	}
	return out
}

func TestOriginalFlowPhysicalRowsAndCaret(t *testing.T) {
	d, raw := original(t, "qualification/flow/exports/FLOW.WP")
	p, err := layout.FromDocument(d, matchedSettings())
	if err != nil {
		t.Fatal(err)
	}
	if len(p.Lines) != 116 || p.Lines[54].Page != 2 || p.Lines[108].Page != 3 {
		t.Fatalf("physical layout pages/rows: count=%d last=%+v", len(p.Lines), p.Lines[len(p.Lines)-1])
	}
	if line, column, ok := p.PositionAt(d.TokenCount()); !ok || line != 115 || column != 25 {
		t.Fatalf("Pg3 Ln2.17 Pos3.5: row=%d col=%d ok=%v", line, column, ok)
	}
	if ln := p.Lines[115].TopInches; math.Abs(ln-(1+7.0/6)) > 1e-9 {
		t.Fatalf("printed Ln=%v", ln)
	}
	n := 0
	for i, line := range p.Lines {
		for _, item := range line.Tokens {
			if item.Index != n {
				t.Fatalf("native owner %d appears out of order on row %d: %d", n, i, item.Index)
			}
			n++
		}
	}
	if n != d.TokenCount() {
		t.Fatalf("mapped %d of %d native owners", n, d.TokenCount())
	}
	if tok := p.Lines[54].Tokens[0].Token.Kind; tok != document.DormantHardReturn {
		t.Fatalf("original Reveal row begins with Dorm HRt, got %v", tok)
	}
	tab := p.Lines[4].Tokens[0]
	if tab.Token.Kind != document.Tab || tab.WidthInches != .5 || tab.LeftInches != 1 {
		t.Fatalf("original Tab row: %+v", tab)
	}
	firstEnd, ok := p.LineBoundary(0, true)
	if !ok {
		t.Fatal("missing first-line End")
	}
	_, desired, _ := p.PositionAt(firstEnd)
	if desired != 63 {
		t.Fatalf("original End Pos7.3 = col63, got %d", desired)
	}
	gap := firstEnd
	for _, want := range []int{58, 0, 17, 20} {
		gap, ok = p.VerticalGap(gap, desired, 1)
		if !ok {
			t.Fatal("downward movement refused")
		}
		_, actual, _ := p.PositionAt(gap)
		if actual != want {
			t.Fatalf("down desired=%d actual=%d want=%d", desired, actual, want)
		}
	}
	gap, ok = p.PageGap(0, 1)
	line, col, known := p.PositionAt(gap)
	if !ok || !known || line != 54 || col != 0 {
		t.Fatalf("page down expected Pg2 row0 cell0: %d %d %v", line, col, ok)
	}
	if token, _ := d.Token(gap); token.Kind == document.DormantHardReturn {
		t.Fatal("page down targeted an unsafe gap inside the compound owner")
	}
	gap, ok = p.PageGap(gap, 1)
	line, col, known = p.PositionAt(gap)
	if !ok || !known || line != 108 || col != 0 {
		t.Fatalf("second page down expected Pg3 row0 cell0: %d %d %v", line, col, ok)
	}
	gap, ok = p.PageGap(gap, -1)
	line, _, _ = p.PositionAt(gap)
	if !ok || line != 54 {
		t.Fatalf("PageUp did not reach page 2: %d %v", line, ok)
	}
	got, _ := d.Export()
	if !bytes.Equal(got, raw) {
		t.Fatal("layout projection or navigation changed original bytes")
	}
}

func TestOriginalProfileLiveTabsAndBlankRows(t *testing.T) {
	// These are the actual owner bytes from TABONE.WP at the start of a line.
	// Inserting six Xs before the owner changes the live stop to column 10.
	staleTab := []byte{0xc1, 2, 8, 7, 8, 7, 0x0f, 0, 0xc1}
	d := parseBody(t, bytes.Join([][]byte{[]byte("XXXXXX"), staleTab, []byte("ABC\n\n")}, nil))
	p, err := layout.FromDocument(d, matchedSettings())
	if err != nil {
		t.Fatal(err)
	}
	line, column, ok := p.PositionAt(7)
	if !ok || line != 0 || column != 10 || p.Lines[0].Tokens[6].WidthInches != .4 {
		t.Fatalf("real relative tab stop depends on stale cache: %d %d %v", line, column, ok)
	}
	if len(p.Lines) != 3 || len(p.Lines[2].Tokens) != 0 {
		t.Fatal("missing physical blank/final row")
	}
	if _, x, ok := p.PositionAt(d.TokenCount()); !ok || x != 0 {
		t.Fatal("end gap lost on blank final row")
	}
	next, ok := matchedSettings().NextTabColumn(6)
	if !ok || next != 10 {
		t.Fatalf("Tab target = %d %v", next, ok)
	}
}

func TestOriginalDerivedNativePageAndTabEdges(t *testing.T) {
	page := []byte{
		0xd4, 0, 0x1c, 0, 0, 0x16, 0x68, 0x29, 1, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0x30, 0x2a, 0x30, 0x2a, 0x30, 0x2a, 0xb0, 4, 0xb0, 4, 0x1c, 0, 0, 0xd4,
	}
	tab := []byte{0xc1, 2, 0x28, 0x23, 0x28, 0x23, 0x4b, 0, 0xc1}
	concat := func(parts ...[]byte) []byte { return bytes.Join(parts, nil) }
	bottom := bytes.Repeat([]byte{0x0a}, 53)
	for _, tc := range []struct {
		name, hash  string
		plain, want []byte
		page, col   int
	}{
		{"long-word-page", "d9329e2d9f84df55f042b622e93cc8d9dc6ffaf6d9b7017ba5a77080aad6a710",
			concat(bottom, bytes.Repeat([]byte("Q"), 66)), concat(bottom, bytes.Repeat([]byte("Q"), 65), page, []byte{0x91, 'Q'}), 2, 1},
		{"space-page", "36fc35c978038bc442b9cdfcbd0e4a8d2237bbb3c65f0761827a77fb78205f61",
			concat(bottom, bytes.Repeat([]byte("X"), 61), []byte(" alpha")), concat(bottom, bytes.Repeat([]byte("X"), 61), page, []byte{0x0b}, []byte("alpha")), 2, 5},
		{"tab-edge", "426c12a60c6a53ead446cd2a554fbb3f687dc6a829506f2a91348b9ecab7ac99",
			concat(bytes.Repeat([]byte("X"), 63), tab, []byte("Y")), concat(bytes.Repeat([]byte("X"), 63), tab, []byte{0x90, 'Y'}), 1, 1},
	} {
		t.Run(tc.name, func(t *testing.T) {
			d := parseBody(t, tc.plain)
			_, originalPrefix := original(t, "r3/EVERY.WP")
			wantHash := sha256.Sum256(concat(originalPrefix[:324], tc.want))
			if hex.EncodeToString(wantHash[:]) != tc.hash {
				t.Fatal("original capture identity mismatch")
			}
			out := applyFlow(t, d, d.TokenCount())
			if !out.Changed || !bytes.Equal(body(t, out.Document), tc.want) {
				t.Fatalf("original native body differs: %x", body(t, out.Document))
			}
			p, err := layout.FromDocument(out.Document, matchedSettings())
			if err != nil {
				t.Fatal(err)
			}
			line, col, ok := p.PositionAt(out.Cursor.Gap())
			if !ok || p.Lines[line].Page != tc.page || col != tc.col {
				t.Fatalf("original page edge position: line %d column %d ok %v", line, col, ok)
			}
			stable := applyFlow(t, out.Document, out.Cursor.Gap())
			if stable.Changed || stable.Document.Revision() != out.Document.Revision() {
				t.Fatal("already qualified layout does not converge")
			}
		})
	}
}

func TestReflowMovesDerivedBreakAfterShortening(t *testing.T) {
	d := parseBody(t, append(bytes.Repeat([]byte("A"), 65), []byte(" word")...))
	out := applyFlow(t, d, d.TokenCount())
	want := append(bytes.Repeat([]byte("A"), 65), []byte{0x0d, 'w', 'o', 'r', 'd'}...)
	if !bytes.Equal(body(t, out.Document), want) {
		t.Fatal("missing lexical-space wrap")
	}
	// Candidate from an ordinary edit upstream of an existing SRt.
	short := parseBody(t, want[5:])
	clean := applyFlow(t, short, short.TokenCount())
	if bytes.Contains(body(t, clean.Document), []byte{0x0d}) ||
		!bytes.HasSuffix(body(t, clean.Document), []byte(" word")) {
		t.Fatal("stale soft return did not become its lexical space")
	}
}

func TestReflowOriginalNativeFirstSaveIsStable(t *testing.T) {
	d, raw := original(t, "qualification/flow/exports/FIRST.WP")
	result := applyFlow(t, d, d.TokenCount())
	got, _ := result.Document.Export()
	if result.Changed || !bytes.Equal(got, raw) {
		t.Fatal("reflow changed the matched original layout")
	}
}
