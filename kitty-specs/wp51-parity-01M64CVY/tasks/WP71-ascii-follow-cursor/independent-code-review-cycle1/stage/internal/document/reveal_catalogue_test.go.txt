package document_test

import (
	"bytes"
	"encoding/binary"
	"go/ast"
	"go/parser"
	"go/token"
	"math"
	"os"
	"reflect"
	"sync"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

func catalogueParse(t testing.TB, body []byte) *document.Document {
	t.Helper()
	d, e := document.Parse(synthetic(t, body))
	if e != nil {
		t.Fatal(e)
	}
	return d
}
func catalogueVariable(total int) []byte {
	b := bytes.Repeat([]byte{0x55}, total)
	b[0] = 0xd0
	b[1] = 1
	binary.LittleEndian.PutUint16(b[2:4], uint16(total-4))
	binary.LittleEndian.PutUint16(b[total-4:total-2], uint16(total-4))
	b[total-2] = 1
	b[total-1] = 0xd0
	return b
}
func TestCatalogueOriginalPairsAndUnknownOwnership(t *testing.T) {
	for _, spec := range []struct {
		kind, label   string
		index, offset int
	}{{"L1-HR", "[HRt]", 14, 692}, {"L2-HP", "[HPg]", 16, 725}} {
		for _, rep := range []string{"01", "02"} {
			t.Run(spec.kind+rep, func(t *testing.T) {
				path := "../../docs/research/continuation/text-layout/runs/wp14-r" + rep + "-" + spec.kind + "/BASEA.WP5"
				raw, e := os.ReadFile(path)
				if e != nil {
					t.Fatal(e)
				}
				d, e := document.Parse(raw)
				if e != nil {
					t.Fatal(e)
				}
				rev := d.Revision()
				birth := d.Birth()
				c, _ := d.CursorAt(0)
				p, e := document.InspectRevealCatalogue(d, rev, 0, d.TokenCount())
				if e != nil {
					t.Fatal(e)
				}
				if p.Revision != rev || p.TotalTokens != d.TokenCount() || len(p.Elements) != d.TokenCount() || !p.TrueEOF {
					t.Fatal(p)
				}
				found := 0
				unknown := 0
				for i, v := range p.Elements {
					token, e := d.Token(i)
					if e != nil {
						t.Fatal(e)
					}
					if v.TokenIndex != i || v.Span != token.Span || v.Kind != token.Kind {
						t.Fatal("lost owner", i, v, token)
					}
					if v.Text == spec.label {
						found++
						if i != spec.index || v.Span.Offset != spec.offset || v.Span.Length != 1 || v.Kind != document.Opaque {
							t.Fatal(v)
						}
					}
					if token.Kind == document.Opaque && i != spec.index {
						unknown++
						if v.Text != "" {
							t.Fatal("decoded unknown payload", v)
						}
					}
				}
				if found != 1 || unknown < 9 {
					t.Fatal(found, unknown)
				}
				if _, e := c.Move(1); e == nil {
					t.Fatal("inspection enabled movement")
				}
				if _, e := c.Present(0, d.TokenCount()); e == nil {
					t.Fatal("inspection enabled Present")
				}
				if e := d.CheckMutation(); e == nil {
					t.Fatal("inspection admitted original")
				}
				if _, e := document.NewHistory(d); e == nil {
					t.Fatal("inspection qualified history")
				}
				if _, e := d.Delete(c, document.ForwardDelete, document.History{}); e == nil {
					t.Fatal("inspection enabled delete")
				}
				if _, e := d.Restore(document.History{}, document.Preview{}); e == nil {
					t.Fatal("inspection enabled Restore")
				}
				if (document.History{}).CountKnown() {
					t.Fatal("invented count")
				}
				exact(t, d, raw)
				orig, e := d.OriginalExport()
				if e != nil || !bytes.Equal(orig, raw) || d.Revision() != rev || d.Birth() != birth || c.Gap() != 0 {
					t.Fatal("inspection changed native identity")
				}
			})
		}
	}
}
func TestCatalogueWholeOwnersNotBytesOrLabelText(t *testing.T) {
	opaque := catalogueVariable(12)
	opaque[4] = 0x0a
	opaque[5] = 0x0c
	body := append([]byte("[HRt]"), opaque...)
	body = append(body, 0xc3, 0x0c, 0xc3, 0x0a, 0x0c, 0xc4, 0x0c, 0xc4)
	d := catalogueParse(t, body)
	p, e := document.InspectRevealCatalogue(d, d.Revision(), 0, d.TokenCount())
	if e != nil {
		t.Fatal(e)
	}
	want := []string{"[", "H", "R", "t", "]", "", "[BOLD]", "[HRt]", "[HPg]", "[bold]"}
	if len(p.Elements) != len(want) {
		t.Fatal(p)
	}
	for i, v := range p.Elements {
		if v.Text != want[i] {
			t.Fatal(i, v)
		}
	}
	if p.Elements[7].Kind != document.Opaque || p.Elements[8].Kind != document.Opaque {
		t.Fatal("new native kind")
	}
	// A forged public Token is only caller inspection data, never an API input.
	fake, _ := d.Token(5)
	fake.Raw = []byte{0x0a}
	fake.Kind = document.ASCII
	fake.Span.Length = 1
	p2, e := document.InspectRevealCatalogue(d, d.Revision(), 5, 1)
	if e != nil || p2.Elements[0].Text != "" || p2.Elements[0].Span.Length != 12 {
		t.Fatal("forged Token retargeted source", p2, e)
	}
	for _, rep := range []string{"01", "02"} {
		raw, e := os.ReadFile("../../docs/research/continuation/text-layout/runs/wp14-r" + rep + "-L4-ABS/BASEA.WP5")
		if e != nil {
			t.Fatal(e)
		}
		tab, e := document.Parse(raw)
		if e != nil {
			t.Fatal(e)
		}
		v, e := document.InspectRevealCatalogue(tab, tab.Revision(), 0, tab.TokenCount())
		if e != nil {
			t.Fatal(e)
		}
		for i, x := range v.Elements {
			token, _ := tab.Token(i)
			if token.Raw[0] == 0xc1 && x.Text != "" {
				t.Fatal("guessed Tab", x)
			}
		}
	}
}
func TestCatalogueRevisionCopiesAndImmutableForks(t *testing.T) {
	d := catalogueParse(t, []byte("AB"))
	same := catalogueParse(t, []byte("AB"))
	rev := d.Revision()
	if _, e := document.InspectRevealCatalogue(d, same.Revision(), 0, 1); e == nil {
		t.Fatal("equal-byte foreign revision")
	}
	if _, e := document.InspectRevealCatalogue(d, document.Revision{}, 0, 1); e == nil {
		t.Fatal("zero revision")
	}
	old := *d
	p, e := document.InspectRevealCatalogue(d, rev, 0, 2)
	if e != nil {
		t.Fatal(e)
	}
	p.Elements[0].Text = "forged"
	p.Elements[0].Span.Offset = 0
	p.Revision = same.Revision()
	again, _ := document.InspectRevealCatalogue(d, rev, 0, 2)
	if again.Elements[0].Text != "A" || again.Elements[0].Span.Offset == 0 {
		t.Fatal("result alias")
	}
	*d = *same
	if _, e := document.InspectRevealCatalogue(d, rev, 0, 2); e == nil {
		t.Fatal("wrapper replacement followed")
	}
	v, e := document.InspectRevealCatalogue(&old, rev, 0, 2)
	if e != nil || v.Elements[0].Text != "A" {
		t.Fatal("old capture lost", e)
	}
	c, _ := old.CursorAt(1)
	r, e := old.InsertASCII(c, []byte("X"))
	if e != nil {
		t.Fatal(e)
	}
	if _, e := document.InspectRevealCatalogue(r.Document, rev, 0, 2); e == nil {
		t.Fatal("stale edit revision")
	}
	if _, e := document.InspectRevealCatalogue(&old, rev, 0, 2); e != nil {
		t.Fatal(e)
	}
}
func TestCatalogueBoundsEOFAndPrecopyBudget(t *testing.T) {
	d := catalogueParse(t, []byte("ABC"))
	for _, v := range [][2]int{{-1, 1}, {0, -1}, {4, 0}, {1, math.MaxInt}, {math.MaxInt, 1}, {0, 4}} {
		if _, e := document.InspectRevealCatalogue(d, d.Revision(), v[0], v[1]); e == nil {
			t.Fatal("range admitted", v)
		}
	}
	var nilDoc *document.Document
	for _, bad := range []*document.Document{nilDoc, {}} {
		if _, e := document.InspectRevealCatalogue(bad, document.Revision{}, 0, 0); e == nil {
			t.Fatal("invalid document")
		}
	}
	for _, v := range []struct {
		start, count int
		eof          bool
	}{{0, 0, false}, {0, 2, false}, {2, 1, true}, {3, 0, true}} {
		p, e := document.InspectRevealCatalogue(d, d.Revision(), v.start, v.count)
		if e != nil || p.TrueEOF != v.eof || p.StartGap != v.start || p.EndGap != v.start+v.count {
			t.Fatal(v, p, e)
		}
	}
	huge := catalogueParse(t, bytes.Repeat(catalogueVariable(65536), 4))
	p, e := document.InspectRevealCatalogue(huge, huge.Revision(), 0, 4)
	if e != nil || len(p.Elements) != 4 {
		t.Fatal("exact raw budget", e)
	}
	over := catalogueParse(t, append(bytes.Repeat(catalogueVariable(65536), 4), 'X'))
	if _, e := document.InspectRevealCatalogue(over, over.Revision(), 0, 5); e == nil {
		t.Fatal("raw budget")
	}
	bench := testing.Benchmark(func(b *testing.B) {
		for i := 0; i < b.N; i++ {
			_, _ = document.InspectRevealCatalogue(over, over.Revision(), 0, 5)
		}
	})
	if bench.AllocedBytesPerOp() > 1024 {
		t.Fatal("copied oversized owner window before refusal", bench.AllocedBytesPerOp())
	}
	maxOwner := catalogueParse(t, catalogueVariable(65539))
	p, e = document.InspectRevealCatalogue(maxOwner, maxOwner.Revision(), 0, 1)
	if e != nil || p.Elements[0].Span.Length != 65539 || p.Elements[0].Text != "" {
		t.Fatal("split max owner", p, e)
	}
	codes := catalogueParse(t, bytes.Repeat([]byte{0xc3, 0x0c, 0xc3}, 4097))
	p, e = document.InspectRevealCatalogue(codes, codes.Revision(), 0, 4096)
	if e != nil || p.TrueEOF {
		t.Fatal(e)
	}
	n := 0
	for _, x := range p.Elements {
		n += len(x.Text)
	}
	if n != 24576 || n > document.MaxCatalogueTextBytes {
		t.Fatal(n)
	}
	if _, e := document.InspectRevealCatalogue(codes, codes.Revision(), 0, 4097); e == nil {
		t.Fatal("token cap")
	}
}
func TestCatalogueRetainsHistoryAndBirthContracts(t *testing.T) {
	d, e := document.Parse(fixture(t))
	if e != nil {
		t.Fatal(e)
	}
	c, _ := d.CursorAt(0)
	h, e := document.NewHistory(d)
	if e != nil {
		t.Fatal(e)
	}
	deleted, e := d.Delete(c, document.ForwardDelete, h)
	if e != nil {
		t.Fatal(e)
	}
	before := deleted.History()
	_, e = document.InspectRevealCatalogue(deleted.Document(), deleted.Document().Revision(), 0, deleted.Document().TokenCount())
	if e != nil {
		t.Fatal(e)
	}
	if before.Revision() != deleted.History().Revision() || before.CountKnown() != deleted.History().CountKnown() || before.Count() != deleted.History().Count() {
		t.Fatal("history mutated")
	}
	entry1, _ := before.Entry(0)
	entry2, _ := deleted.History().Entry(0)
	if !reflect.DeepEqual(entry1, entry2) {
		t.Fatal("fragments changed")
	}
	n, e := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if e != nil {
		t.Fatal(e)
	}
	rev := n.Revision()
	b := n.Birth()
	if _, e := document.InspectRevealCatalogue(n, rev, 0, 0); e != nil {
		t.Fatal(e)
	}
	if n.Birth() != b || n.Revision() != rev || !b.IsNew() {
		t.Fatal("birth lost")
	}
	if _, e := n.OriginalExport(); e == nil {
		t.Fatal("invented Loaded birth")
	}
}

func TestCatalogueUnknownHistoryAndVirtualPreviewRemainUnknown(t *testing.T) {
	d, c, h := wp40Setup(t, "direct-reveal-delete-on", "r1", true)
	r, e := d.Delete(c, document.ForwardDelete, h)
	if e != nil {
		t.Fatal(e)
	}
	d, c, h = r.Document(), r.Cursor(), r.History()
	if h.CountKnown() {
		t.Fatal("fixture must model unknown count")
	}
	saved := h
	before, e := h.Open(c)
	if e != nil {
		t.Fatal(e)
	}
	overlay, e := before.Present(0, 0, true)
	if e != nil {
		t.Fatal(e)
	}
	if _, e := document.InspectRevealCatalogue(d, d.Revision(), 0, d.TokenCount()); e != nil {
		t.Fatal(e)
	}
	after, e := before.Present(0, 0, true)
	if e != nil || !reflect.DeepEqual(overlay, after) || h.Revision() != saved.Revision() || h.CountKnown() {
		t.Fatal("catalogue changed virtual history", e)
	}
	_, e = h.Open(c.WithReveal(false))
	category(t, e, document.UnsupportedHistoryEffect)
	_, e = h.Separate(document.RightBoundary)
	category(t, e, document.UnsupportedHistoryEffect)
}
func TestCatalogueMalformedNativeStillRefuses(t *testing.T) {
	body := catalogueVariable(12)
	raw := synthetic(t, body)
	for _, b := range [][]byte{raw[:len(raw)-1], synthetic(t, []byte{0}), synthetic(t, []byte{0x7f})} {
		if _, e := document.Parse(b); e == nil {
			t.Fatal("malformed native accepted")
		}
	}
}

// Structural source ownership invariant, not an unsynchronized wrapper-race test.
func TestCatalogueCapturesWrapperOnce(t *testing.T) {
	f, e := parser.ParseFile(token.NewFileSet(), "reveal_catalogue.go", nil, 0)
	if e != nil {
		t.Fatal(e)
	}
	reads := 0
	ast.Inspect(f, func(n ast.Node) bool {
		v, ok := n.(*ast.SelectorExpr)
		if ok {
			x, ok := v.X.(*ast.Ident)
			if ok && x.Name == "d" && v.Sel.Name == "state" {
				reads++
			}
		}
		return true
	})
	if reads != 1 {
		t.Fatal("caller wrapper must be captured once", reads)
	}
}
func TestCatalogueConcurrentImmutableReaders(t *testing.T) {
	d := catalogueParse(t, []byte("ABC"))
	rev := d.Revision()
	var wg sync.WaitGroup
	for range 16 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for range 20 {
				p, e := document.InspectRevealCatalogue(d, rev, 0, 3)
				if e != nil || p.Elements[0].Text != "A" {
					t.Error("read identity", e)
					return
				}
				p.Elements[0].Text = "local"
			}
		}()
	}
	wg.Wait()
}

func BenchmarkCatalogueMaxWindow(b *testing.B) {
	d := catalogueParse(b, bytes.Repeat([]byte{0xc3, 0x0c, 0xc3}, 4096))
	rev := d.Revision()
	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		if _, e := document.InspectRevealCatalogue(d, rev, 0, 4096); e != nil {
			b.Fatal(e)
		}
	}
}
func BenchmarkCatalogueRefusedRawWindow(b *testing.B) {
	d := catalogueParse(b, append(bytes.Repeat(catalogueVariable(65536), 4), 'X'))
	rev := d.Revision()
	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		if _, e := document.InspectRevealCatalogue(d, rev, 0, 5); e == nil {
			b.Fatal("budget bypass")
		}
	}
}
