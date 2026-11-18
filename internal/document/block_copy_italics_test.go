package document_test

import (
	"bytes"
	"crypto/sha256"
	"fmt"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

// Independent mirrors of the pinned original native owners, not style flags.
var bciOn = []byte{0xc3, 0x08, 0xc3}
var bciOff = []byte{0xc4, 0x08, 0xc4}

type bciWant struct {
	body  []byte
	kinds []document.Kind
}

func bciPlain(s string) bciWant { return bciWant{[]byte(s), bciASCII(len(s))} }
func bciASCII(n int) []document.Kind {
	out := make([]document.Kind, n)
	for i := range out {
		out[i] = document.ASCII
	}
	return out
}
func bciKinds(parts ...[]document.Kind) []document.Kind {
	var out []document.Kind
	for _, p := range parts {
		out = append(out, p...)
	}
	return out
}
func bciRun(prefix, text, suffix string) bciWant {
	return bciWant{cat([]byte(prefix), bciOn, []byte(text), bciOff, []byte(suffix)), bciKinds(bciASCII(len(prefix)), []document.Kind{document.ItalicsOn}, bciASCII(len(text)), []document.Kind{document.ItalicsOff}, bciASCII(len(suffix)))}
}
func bciParse(t *testing.T, body []byte) *document.Document {
	t.Helper()
	d, e := document.Parse(synthetic(t, body))
	if e != nil {
		t.Fatal(e)
	}
	return d
}
func bciPrefix(t *testing.T) []byte {
	t.Helper()
	d, e := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if e != nil {
		t.Fatal(e)
	}
	raw, e := d.Export()
	if e != nil {
		t.Fatal(e)
	}
	return raw
}
func bciAssert(t *testing.T, d *document.Document, first, last int, want bciWant) *document.Document {
	t.Helper()
	raw, e := d.Export()
	if e != nil {
		t.Fatal(e)
	}
	rev, birth := d.Revision(), d.Birth()
	a, e := d.CursorAt(first)
	if e != nil {
		t.Fatal(e)
	}
	b, e := d.CursorAt(last)
	if e != nil {
		t.Fatal(e)
	}
	a, b = a.WithReveal(true), b.WithReveal(true)
	fragment, e := d.CopyEverydayBlock(a, b)
	if e != nil {
		t.Fatalf("native Italics producer refused selected owners: %v", e)
	}
	if got := everydayBody(t, fragment); !bytes.Equal(got, want.body) {
		t.Fatalf("native Copy omitted/misordered required Italics edge owners: actual %x expected %x", got, want.body)
	}
	if fragment.TokenCount() != len(want.kinds) {
		t.Fatalf("fragment owner count %d expected %d", fragment.TokenCount(), len(want.kinds))
	}
	for i, k := range want.kinds {
		tok, e := fragment.Token(i)
		if e != nil || tok.Kind != k {
			t.Fatalf("fragment actual Kind at %d=%v expected %v: %v", i, tok.Kind, k, e)
		}
	}
	expected := cat(bciPrefix(t), want.body)
	exact(t, fragment, expected)
	if e := fragment.CheckMutation(); e != nil {
		t.Fatal("fragment not self-contained", e)
	}
	original, e := fragment.OriginalExport()
	if e != nil || !bytes.Equal(original, expected) || fragment.Birth() == birth {
		t.Fatal("fragment imported source provenance/birth")
	}
	exact(t, d, raw)
	if d.Revision() != rev || d.Birth() != birth || a.Gap() != first || b.Gap() != last || a.Revision() != rev || b.Revision() != rev {
		t.Fatal("Copy changed source/cursors")
	}
	exported, _ := fragment.Export()
	clear(exported)
	if fragment.TokenCount() > 0 {
		tok, _ := fragment.Token(0)
		clear(tok.Raw)
	}
	exact(t, fragment, expected)
	exact(t, d, raw)
	reopened, e := document.Parse(expected)
	if e != nil {
		t.Fatal(e)
	}
	exact(t, reopened, expected)
	return fragment
}
func bciRefuse(t *testing.T, d *document.Document, a, b document.Cursor, want document.Category) {
	t.Helper()
	raw, e := d.Export()
	if e != nil {
		t.Fatal(e)
	}
	rev, birth := d.Revision(), d.Birth()
	fragment, e := d.CopyEverydayBlock(a, b)
	category(t, e, want)
	if fragment != nil || d.Revision() != rev || d.Birth() != birth {
		t.Fatal("refusal returned partial fragment or changed source")
	}
	exact(t, d, raw)
}

func TestBlockCopyItalicsOriginalEncodingAndDetachedPrefix(t *testing.T) {
	raw, e := os.ReadFile("../../docs/research/reference-runs/mission1-appearance/ITALICS.WP")
	if e != nil {
		t.Fatal(e)
	}
	if fmt.Sprintf("%x", sha256.Sum256(raw)) != "24470a1f57bf84cd38527041d8e2d99b0f4330f5a8d442ce43230b334299f7c7" {
		t.Fatal("original encoding pin")
	}
	d, e := document.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	on, _ := d.Token(0)
	off, _ := d.Token(6)
	if on.Kind != document.ItalicsOn || off.Kind != document.ItalicsOff || !bytes.Equal(on.Raw, bciOn) || !bytes.Equal(off.Raw, bciOff) {
		t.Fatal("literal08 does not mirror actual original Kind/owners")
	}
	bciAssert(t, d, 0, 7, bciRun("", "alpha", ""))
	bciAssert(t, d, 1, 6, bciRun("", "alpha", ""))
	exact(t, d, raw)
	// A distinct already-admitted prefix/hash/flag variant must stay with source.
	source := synthetic(t, cat(bciOn, []byte("AB"), bciOff))
	source[256] = 8
	copy(source[101:103], []byte{0x11, 0x72})
	custom, e := document.Parse(source)
	if e != nil || custom.CheckMutation() != nil {
		t.Fatal("qualified source prefix setup", e)
	}
	fragment := bciAssert(t, custom, 1, 3, bciRun("", "AB", ""))
	out, _ := fragment.Export()
	if bytes.Equal(out[:324], source[:324]) {
		t.Fatal("detached copy imported source prefix")
	}
	exact(t, custom, source)
}

func TestBlockCopyItalicsEveryBoundaryAndReverse(t *testing.T) {
	source := cat([]byte("L"), bciOn, []byte("AB"), bciOff, []byte("R"))
	cases := []struct {
		first, last int
		want        bciWant
	}{
		{0, 1, bciPlain("L")}, {0, 2, bciRun("L", "", "")}, {0, 3, bciRun("L", "A", "")}, {0, 4, bciRun("L", "AB", "")}, {0, 5, bciRun("L", "AB", "")}, {0, 6, bciRun("L", "AB", "R")},
		{1, 2, bciRun("", "", "")}, {1, 3, bciRun("", "A", "")}, {1, 4, bciRun("", "AB", "")}, {1, 5, bciRun("", "AB", "")}, {1, 6, bciRun("", "AB", "R")},
		{2, 3, bciRun("", "A", "")}, {2, 4, bciRun("", "AB", "")}, {2, 5, bciRun("", "AB", "")}, {2, 6, bciRun("", "AB", "R")},
		{3, 4, bciRun("", "B", "")}, {3, 5, bciRun("", "B", "")}, {3, 6, bciRun("", "B", "R")}, {4, 5, bciRun("", "", "")}, {4, 6, bciRun("", "", "R")}, {5, 6, bciPlain("R")}}
	for _, tc := range cases {
		for _, reverse := range []bool{false, true} {
			t.Run(fmt.Sprintf("g%d-g%d/reverse%v", tc.first, tc.last, reverse), func(t *testing.T) {
				first, last := tc.first, tc.last
				if reverse {
					first, last = last, first
				}
				bciAssert(t, bciParse(t, source), first, last, tc.want)
			})
		}
	}
}

func TestBlockCopyItalicsIndependentStylesAndRuns(t *testing.T) {
	three := cat(boldOn, underlineOn, bciOn, []byte("AB"), bciOff, underlineOf, boldOff)
	threeKinds := bciKinds([]document.Kind{document.BoldOn, document.UnderlineOn, document.ItalicsOn}, bciASCII(2), []document.Kind{document.ItalicsOff, document.UnderlineOff, document.BoldOff})
	cases := []struct {
		name        string
		source      []byte
		first, last int
		want        bciWant
	}{
		{"all-three-interior", three, 3, 5, bciWant{three, threeKinds}},
		{"all-three-whole", three, 0, 8, bciWant{three, threeKinds}},
		{"bold-italic-edges", cat(boldOn, bciOn, []byte("AB"), bciOff, boldOff), 2, 4, bciWant{cat(boldOn, bciOn, []byte("AB"), bciOff, boldOff), bciKinds([]document.Kind{document.BoldOn, document.ItalicsOn}, bciASCII(2), []document.Kind{document.ItalicsOff, document.BoldOff})}},
		{"underline-italic-edges", cat(underlineOn, bciOn, []byte("AB"), bciOff, underlineOf), 2, 4, bciWant{cat(underlineOn, bciOn, []byte("AB"), bciOff, underlineOf), bciKinds([]document.Kind{document.UnderlineOn, document.ItalicsOn}, bciASCII(2), []document.Kind{document.ItalicsOff, document.UnderlineOff})}},
		{"crossing-keeps-selected-order", cat(boldOn, bciOn, []byte("A"), boldOff, []byte("B"), bciOff), 2, 5, bciWant{cat(boldOn, bciOn, []byte("A"), boldOff, []byte("B"), bciOff), []document.Kind{document.BoldOn, document.ItalicsOn, document.ASCII, document.BoldOff, document.ASCII, document.ItalicsOff}}},
		{"multiple-runs", cat(bciOn, []byte("A"), bciOff, []byte("-"), bciOn, []byte("B"), bciOff), 1, 6, bciWant{cat(bciOn, []byte("A"), bciOff, []byte("-"), bciOn, []byte("B"), bciOff), []document.Kind{document.ItalicsOn, document.ASCII, document.ItalicsOff, document.ASCII, document.ItalicsOn, document.ASCII, document.ItalicsOff}}},
		{"plain-leading-trailing", cat([]byte("pre"), bciOn, []byte("I"), bciOff, []byte("post")), 0, 10, bciRun("pre", "I", "post")},
		{"empty-pair", cat(bciOn, bciOff), 0, 2, bciRun("", "", "")},
		{"legacy-bold", cat(boldOn, []byte("AB"), boldOff), 1, 3, bciWant{cat(boldOn, []byte("AB"), boldOff), []document.Kind{document.BoldOn, document.ASCII, document.ASCII, document.BoldOff}}},
		{"legacy-underline", cat(underlineOn, []byte("AB"), underlineOf), 1, 3, bciWant{cat(underlineOn, []byte("AB"), underlineOf), []document.Kind{document.UnderlineOn, document.ASCII, document.ASCII, document.UnderlineOff}}},
		{"literal-label", []byte("[ITALC]"), 0, 7, bciPlain("[ITALC]")}}
	for _, tc := range cases {
		for _, reverse := range []bool{false, true} {
			t.Run(fmt.Sprintf("%s/reverse%v", tc.name, reverse), func(t *testing.T) {
				first, last := tc.first, tc.last
				if reverse {
					first, last = last, first
				}
				bciAssert(t, bciParse(t, tc.source), first, last, tc.want)
			})
		}
	}
}

func TestBlockCopyItalicsLegacyFloorSixWrappersAndLimits(t *testing.T) {
	for _, n := range []int{document.MaxMutationTokens - 4, document.MaxMutationTokens - 3} {
		t.Run(fmt.Sprintf("legacy-plain-%d", n), func(t *testing.T) {
			d := bciParse(t, bytes.Repeat([]byte("x"), n))
			a, _ := d.CursorAt(0)
			b, _ := d.CursorAt(n)
			if n+4 > document.MaxMutationTokens {
				bciRefuse(t, d, a, b, document.MutationLimit)
			} else {
				bciAssert(t, d, 0, n, bciWant{bytes.Repeat([]byte("x"), n), bciASCII(n)})
			}
		})
	}
	for _, styles := range []int{2, 3} {
		t.Run(fmt.Sprintf("exact-limit-%dstyles", styles), func(t *testing.T) {
			n := document.MaxMutationTokens - 2*styles
			on, off := cat(boldOn, underlineOn), cat(underlineOf, boldOff)
			kindsOn, kindsOff := []document.Kind{document.BoldOn, document.UnderlineOn}, []document.Kind{document.UnderlineOff, document.BoldOff}
			if styles == 3 {
				on = cat(on, bciOn)
				off = cat(bciOff, off)
				kindsOn = append(kindsOn, document.ItalicsOn)
				kindsOff = append([]document.Kind{document.ItalicsOff}, kindsOff...)
			}
			body := cat(on, bytes.Repeat([]byte("x"), n), off)
			fragment := bciAssert(t, bciParse(t, body), styles, styles+n, bciWant{body, bciKinds(kindsOn, bciASCII(n), kindsOff)})
			if fragment.TokenCount() != document.MaxMutationTokens {
				t.Fatal("actual synthesized wrappers not counted")
			}
		})
	}
	for name, body := range map[string][]byte{"source-token-limit": bytes.Repeat([]byte("x"), document.MaxMutationTokens+1), "source-byte-limit": bytes.Repeat(observedTab, document.MaxMutationBytes/9+1)} {
		t.Run(name, func(t *testing.T) {
			d := bciParse(t, body)
			a, _ := d.CursorAt(0)
			b, _ := d.CursorAt(1)
			bciRefuse(t, d, a, b, document.MutationLimit)
		})
	}
	// An otherwise-admitted byte-bound source retains full Tab owners and wrapper
	// bytes, with no source body/prefix limit increase.
	n := (document.MaxMutationBytes - 324 - 18) / 9
	body := cat(boldOn, underlineOn, bciOn, bytes.Repeat(observedTab, n), bciOff, underlineOf, boldOff)
	wantKinds := bciKinds([]document.Kind{document.BoldOn, document.UnderlineOn, document.ItalicsOn})
	for range n {
		wantKinds = append(wantKinds, document.Tab)
	}
	wantKinds = append(wantKinds, document.ItalicsOff, document.UnderlineOff, document.BoldOff)
	bciAssert(t, bciParse(t, body), 3, n+3, bciWant{body, wantKinds})
}

func TestBlockCopyItalicsRefusalsCursorAndSourceSafety(t *testing.T) {
	for name, body := range map[string][]byte{"duplicate-on": cat(bciOn, bciOn, []byte("i"), bciOff, bciOff), "unmatched-off": bciOff, "unclosed": cat(bciOn, []byte("i")), "opaque": {0x80, 'A'}, "unsafe-page": {0x8c, 'A'}, "unowned-redline": {0xc3, 0x0a, 0xc3, 'A', 0xc4, 0x0a, 0xc4}} {
		t.Run(name, func(t *testing.T) {
			d := bciParse(t, body)
			if name == "unowned-redline" {
				tok, _ := d.Token(0)
				if tok.Kind != document.RedlineOn || d.CheckMutation() != nil {
					t.Fatal("actual admitted Redline negative control setup")
				}
			}
			a, _ := d.CursorAt(0)
			b, _ := d.CursorAt(d.TokenCount())
			bciRefuse(t, d, a, b, document.UnsupportedBody)
		})
	}
	d := bciParse(t, cat(bciOn, []byte("AB"), bciOff))
	a, _ := d.CursorAt(1)
	b, _ := d.CursorAt(3)
	bciRefuse(t, d, a, a, document.InvalidPosition)
	other := bciParse(t, []byte("OTHER"))
	foreign, _ := other.CursorAt(1)
	bciRefuse(t, d, a, foreign, document.RevisionMismatch)
	bciRefuse(t, d, foreign, b, document.InvalidPosition)
	edit, e := d.InsertASCII(a, []byte("X"))
	if e != nil {
		t.Fatal(e)
	}
	fresh, _ := edit.Document.CursorAt(2)
	bciRefuse(t, edit.Document, a, fresh, document.InvalidPosition)
	bciRefuse(t, edit.Document, fresh, b, document.RevisionMismatch)
	var zero document.Document
	fragment, e := zero.CopyEverydayBlock(document.Cursor{}, document.Cursor{})
	category(t, e, document.InvalidDocument)
	if fragment != nil {
		t.Fatal("zero source produced fragment")
	}
}

func TestBlockCopyItalicsCheckedInsertionSeamUnchanged(t *testing.T) {
	source := bciParse(t, cat(bciOn, []byte("AB"), bciOff))
	fragment := bciAssert(t, source, 1, 3, bciRun("", "AB", ""))
	for _, copy := range []bool{false, true} {
		t.Run(fmt.Sprintf("copy%v", copy), func(t *testing.T) {
			receiver := bciParse(t, []byte("LR"))
			c, _ := receiver.CursorAt(1)
			var edit document.EditResult
			var e error
			if copy {
				edit, e = receiver.InsertBlockCopy(c, fragment)
			} else {
				edit, e = receiver.InsertDocument(c, fragment)
			}
			if e != nil {
				t.Fatal(e)
			}
			want := cat([]byte("L"), bciOn, []byte("AB"), bciOff, []byte("R"))
			if !bytes.Equal(everydayBody(t, edit.Document), want) {
				t.Fatal("producer fragment did not reach ordinary checked insertion")
			}
			gap := 5
			if copy {
				gap = 1
			}
			if edit.Cursor.Gap() != gap {
				t.Fatal("insertion API caret changed")
			}
			active := bciParse(t, cat(bciOn, []byte("LR"), bciOff))
			at, _ := active.CursorAt(2)
			before, _ := active.Export()
			if copy {
				edit, e = active.InsertBlockCopy(at, fragment)
			} else {
				edit, e = active.InsertDocument(at, fragment)
			}
			category(t, e, document.UnsupportedBody)
			if edit.Document != active || edit.Cursor != at || edit.Changed {
				t.Fatal("active receiver refusal weakened")
			}
			exact(t, active, before)
		})
	}
}
