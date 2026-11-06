package document_test

import (
	"bytes"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

// Observed everyday native shapes (WP78 r2/r3 EVERY.WP, REPORT.md):
// soft return 0D, hard return 0A, hard page 0C, attribute ON C3 <type> C3 and
// OFF C4 <type> C4 with type 0C Bold and 0E Underline, and the 9-byte Tab owner.
// The bodies below are synthetic substitutions over the real qualified prefix,
// used to exercise the API — never as an oracle for original output.
var (
	boldOn      = []byte{0xc3, 0x0c, 0xc3}
	boldOff     = []byte{0xc4, 0x0c, 0xc4}
	underlineOn = []byte{0xc3, 0x0e, 0xc3}
	underlineOf = []byte{0xc4, 0x0e, 0xc4}
	observedTab = []byte{0xc1, 0x02, 0x08, 0x07, 0x08, 0x07, 0x0f, 0x00, 0xc1}
)

func cat(a ...[]byte) []byte { return bytes.Join(a, nil) }

func TestEverydayCodesAdmittedAndLabelled(t *testing.T) {
	body := cat([]byte("AB"), underlineOn, []byte("UN"), underlineOf, []byte{0x0d},
		observedTab, []byte("CD"), []byte{0x0a}, []byte{0x0c})
	raw := synthetic(t, body)
	d, e := document.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	if e := d.CheckMutation(); e != nil {
		t.Fatalf("everyday body refused: %v", e)
	}
	exact(t, d, raw)

	kinds := []document.Kind{
		document.ASCII, document.ASCII,
		document.UnderlineOn, document.ASCII, document.ASCII, document.UnderlineOff,
		document.SoftReturn, document.Tab,
		document.ASCII, document.ASCII,
		document.HardReturn, document.HardPage,
	}
	if d.TokenCount() != len(kinds) {
		t.Fatalf("token count %d, want %d", d.TokenCount(), len(kinds))
	}
	for i, want := range kinds {
		tok, e := d.Token(i)
		if e != nil {
			t.Fatal(e)
		}
		if tok.Kind != want {
			t.Fatalf("token %d kind %d, want %d", i, tok.Kind, want)
		}
	}
	// The Tab owner is retained whole: nine native bytes, never split.
	tab, _ := d.Token(7)
	if tab.Span.Length != 9 || !bytes.Equal(tab.Raw, observedTab) {
		t.Fatalf("tab owner %v", tab)
	}

	// One label source feeds both views, and Reveal never becomes serializer input.
	c, _ := d.CursorAt(0)
	normal, e := c.Present(0, d.TokenCount())
	if e != nil {
		t.Fatal(e)
	}
	reveal, e := c.WithReveal(true).Present(0, d.TokenCount())
	if e != nil {
		t.Fatal(e)
	}
	wantNormal := []string{"A", "B", "", "U", "N", "", "\n", "\t", "C", "D", "\n", ""}
	wantReveal := []string{"A", "B", "[UND]", "U", "N", "[und]", "[SRt]", "[Tab]", "C", "D", "[HRt]", "[HPg]"}
	for i := range wantNormal {
		if normal.Elements[i].Text != wantNormal[i] {
			t.Fatalf("normal %d = %q, want %q", i, normal.Elements[i].Text, wantNormal[i])
		}
		if reveal.Elements[i].Text != wantReveal[i] {
			t.Fatalf("reveal %d = %q, want %q", i, reveal.Elements[i].Text, wantReveal[i])
		}
	}
	insp, e := document.InspectRevealCatalogue(d, d.Revision(), 0, d.TokenCount())
	if e != nil {
		t.Fatal(e)
	}
	for i := range wantReveal {
		if insp.Elements[i].Text != wantReveal[i] || insp.Elements[i].TokenIndex != i {
			t.Fatalf("catalogue %d = %v", i, insp.Elements[i])
		}
	}
	// Movement now crosses the everyday owners instead of refusing them.
	for gap := 0; gap < d.TokenCount(); gap++ {
		next, e := c.Move(1)
		if e != nil || next.Gap() != gap+1 {
			t.Fatalf("forward move at %d: %v", gap, e)
		}
		if back, e := next.Move(-1); e != nil || back.Gap() != gap {
			t.Fatalf("backward move at %d: %v", gap, e)
		}
		c = next
	}
	// Export stays byte-exact: neither view normalized the source.
	exact(t, d, raw)
}

func TestEverydayAttributeRefusalsRetained(t *testing.T) {
	for name, body := range map[string][]byte{
		"duplicate underline on":  cat([]byte("A"), underlineOn, underlineOn, []byte("B"), underlineOf, underlineOf),
		"unmatched underline off": cat([]byte("A"), underlineOf),
		"unterminated underline":  cat([]byte("A"), underlineOn, []byte("BC")),
		"duplicate bold on":       cat([]byte("A"), boldOn, boldOn, []byte("B"), boldOff, boldOff),
		"unmatched bold off":      cat([]byte("A"), boldOff),
	} {
		raw := synthetic(t, body)
		d, e := document.Parse(raw)
		if e != nil {
			t.Fatalf("%s: parse %v", name, e)
		}
		if e := d.CheckMutation(); e == nil {
			t.Fatalf("%s admitted", name)
		}
		c, _ := d.CursorAt(0)
		r, e := d.InsertASCII(c, []byte("X"))
		if e == nil || r.Document != d || r.Cursor != c {
			t.Fatalf("%s mutated", name)
		}
		exact(t, d, raw)
	}
}

func TestNestedAndRepeatedPairsAdmitted(t *testing.T) {
	// Bold inside Underline, and three sequential Bold pairs: the former
	// two-pair ceiling and flat attribute state were WP23 policies, not format
	// limits, and the original stores both shapes.
	body := cat(boldOn, underlineOn, []byte("NEST"), underlineOf, boldOff,
		boldOn, []byte("1"), boldOff, boldOn, []byte("2"), boldOff,
		boldOn, []byte("3"), boldOff, []byte("end"))
	raw := synthetic(t, body)
	d, e := document.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	if e := d.CheckMutation(); e != nil {
		t.Fatalf("nested/repeated attributes refused: %v", e)
	}
	exact(t, d, raw)
}

func TestUnnamedTabShapeStaysOpaque(t *testing.T) {
	// Same outer C1 width, different interior. The observed field bytes are
	// evidence, not constants, so the owner is left unnamed rather than labelled
	// Tab on a guess — and unnamed means mutation refuses it.
	tab := bytes.Clone(observedTab)
	tab[1] = 0x03
	raw := synthetic(t, cat([]byte("A"), tab))
	d, e := document.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	tok, e := d.Token(1)
	if e != nil {
		t.Fatal(e)
	}
	if tok.Kind != document.Opaque || tok.Span.Length != 9 {
		t.Fatalf("unnamed tab %v", tok)
	}
	if e := d.CheckMutation(); e == nil {
		t.Fatal("unnamed C1 payload admitted")
	}
	exact(t, d, raw)
}

func TestEverydayReturnAndTabLifecycle(t *testing.T) {
	// Loaded, then saved by two successful edits. The result remains an exact
	// WP51 body revision, not a private container.
	body := cat([]byte("AB"), observedTab, []byte("CD"), []byte{0x0a})
	raw := synthetic(t, body)
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	if err := d.CheckMutation(); err != nil {
		t.Fatal(err)
	}
	c, _ := d.CursorAt(2)
	r, err := d.InsertSoftReturn(c)
	if err != nil || !r.Changed || r.Cursor.Gap() != 3 {
		t.Fatal("soft return insertion", err)
	}
	loaded := r.Document
	if got := mustExport(t, loaded); !bytes.Equal(got[324:], cat([]byte("AB"), []byte{0x0d}, observedTab, []byte("CD"), []byte{0x0a})) {
		t.Fatal("soft return was not inserted byte-exactly")
	}
	c, _ = loaded.CursorAt(r.Cursor.Gap())
	r, err = loaded.InsertTab(c, observedTab)
	if err != nil || !r.Changed || r.Cursor.Gap() != 4 {
		t.Fatal("tab insertion", err)
	}
	saved := r.Document
	tok, _ := saved.Token(3)
	if tok.Kind != document.Tab || tok.Span.Length != len(observedTab) || !bytes.Equal(tok.Raw, observedTab) {
		t.Fatalf("saved tab %v", tok)
	}
	tok, _ = saved.Token(4)
	if tok.Kind != document.Tab || tok.Span.Length != len(observedTab) || !bytes.Equal(tok.Raw, observedTab) {
		t.Fatalf("saved second tab %v", tok)
	}
	c, _ = saved.CursorAt(6)
	over, err := saved.InsertHardReturn(c)
	if err != nil || !over.Changed || over.Cursor.Gap() != 7 {
		t.Fatal("hard return through saved everyday body", err)
	}
	exact(t, d, raw)
}

func mustExport(t testing.TB, d *document.Document) []byte {
	t.Helper()
	got, err := d.Export()
	if err != nil {
		t.Fatal(err)
	}
	return got
}
