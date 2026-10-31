package document_test

import (
	"bytes"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"errors"
	"os"
	"reflect"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
)

const pairedPath = "../../docs/research/reference-runs/2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5"

func fixture(t testing.TB) []byte {
	t.Helper()
	b, e := os.ReadFile(pairedPath)
	if e != nil {
		t.Fatal(e)
	}
	h := sha256.Sum256(b)
	if len(b) != 334 || hex.EncodeToString(h[:]) != "c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d" {
		t.Fatal("changed original fixture")
	}
	return b
}

// Synthetic body substitution keeps the original prefix, deliberately labelled
// synthetic and used only to test API refusal/preservation, never as an oracle.
func synthetic(t testing.TB, body []byte) []byte {
	b := fixture(t)
	n := int(binary.LittleEndian.Uint32(b[4:8]))
	return append(bytes.Clone(b[:n]), body...)
}
func exact(t testing.TB, d *document.Document, want []byte) {
	t.Helper()
	got, e := d.Export()
	if e != nil || !bytes.Equal(got, want) {
		t.Fatalf("export mismatch: %v", e)
	}
	if sha256.Sum256(got) != sha256.Sum256(want) {
		t.Fatal("hash mismatch")
	}
}
func category(t testing.TB, e error, k document.Category) {
	t.Helper()
	var f *document.Failure
	if !errors.As(e, &f) || f.Category != k {
		t.Fatalf("wanted %s; got %v", k, e)
	}
}

func TestOriginalGapsAndSharedViews(t *testing.T) {
	b := fixture(t)
	saved := bytes.Clone(b)
	d, e := document.Parse(b)
	if e != nil {
		t.Fatal(e)
	}
	if d.TokenCount() != 6 {
		t.Fatal(d.TokenCount())
	}
	offsets := []int{324, 325, 328, 329, 330, 333, 334}
	c, e := d.CursorAt(0)
	if e != nil {
		t.Fatal(e)
	}
	for gap, off := range offsets {
		if c.Gap() != gap {
			t.Fatal(c.Gap())
		}
		got, e := c.Offset()
		if e != nil || got != off {
			t.Fatalf("gap %d offset %d %v", gap, got, e)
		}
		exact(t, d, saved)
		if gap < 6 {
			next, e := c.Move(1)
			if e != nil {
				t.Fatal(e)
			}
			if c.Gap() != gap {
				t.Fatal("cursor mutated")
			}
			c = next
		}
	}
	for i := 5; i >= 0; i-- {
		c, e = c.Move(-1)
		if e != nil || c.Gap() != i {
			t.Fatal(i, e)
		}
	}
	normal, e := c.Present(0, 6)
	if e != nil {
		t.Fatal(e)
	}
	reveal := c.WithReveal(true)
	shown, e := reveal.Present(0, 6)
	if e != nil {
		t.Fatal(e)
	}
	var n, r strings.Builder
	for i, x := range normal.Elements {
		n.WriteString(x.Text)
		r.WriteString(shown.Elements[i].Text)
		if x.Span != shown.Elements[i].Span || x.TokenIndex != i {
			t.Fatal("view coordinate drift")
		}
	}
	if n.String() != "ABCD" || r.String() != "A[BOLD]BC[bold]D" {
		t.Fatal(n.String(), r.String())
	}
	if normal.CursorGap != shown.CursorGap || c.Reveal() || !reveal.Reveal() || reveal.Gap() != c.Gap() {
		t.Fatal("toggle changed shared cursor")
	}
	if !reflect.DeepEqual(c, reveal.WithReveal(false)) {
		t.Fatal("toggle did not restore view state")
	}
	exact(t, d, saved)
	if !bytes.Equal(b, saved) {
		t.Fatal("input changed")
	}
}

func TestIsolationAndRefusalCoordinates(t *testing.T) {
	b := fixture(t)
	saved := bytes.Clone(b)
	d, e := document.Parse(b)
	if e != nil {
		t.Fatal(e)
	}
	b[0] = 0
	exact(t, d, saved)
	out, _ := d.Export()
	out[0] = 0
	tok, e := d.Token(1)
	if e != nil || tok.Kind != document.BoldOn || tok.Span != (wp51.Span{Offset: 325, Length: 3}) {
		t.Fatal(tok, e)
	}
	tok.Raw[1] = 0
	again, _ := d.Token(1)
	if !bytes.Equal(again.Raw, []byte{0xc3, 0x0c, 0xc3}) {
		t.Fatal("token bytes alias")
	}
	tok.Span.Offset = 0
	c, _ := d.CursorAt(2)
	p, e := c.Present(0, 6)
	if e != nil {
		t.Fatal(e)
	}
	p.Elements[0].Text = "changed"
	p.Elements[0].Span.Offset = 0
	p2, _ := c.Present(0, 6)
	if p2.Elements[0].Text != "A" || p2.Elements[0].Span.Offset != 324 {
		t.Fatal("presentation aliases")
	}
	for _, gap := range []int{-1, 7, int(^uint(0) >> 1)} {
		_, e = d.CursorAt(gap)
		category(t, e, document.InvalidPosition)
	}
	for _, i := range []int{-1, 6} {
		_, e = d.Token(i)
		category(t, e, document.InvalidPosition)
	}
	for _, dir := range []int{-2, 0, 2, int(^uint(0) >> 1)} {
		next, e := c.Move(dir)
		category(t, e, document.InvalidDirection)
		if next != c {
			t.Fatal("failed move changed cursor")
		}
	}
	first, _ := d.CursorAt(0)
	next, e := first.Move(-1)
	category(t, e, document.InvalidPosition)
	if next != first {
		t.Fatal("boundary mutated")
	}
	last, _ := d.CursorAt(6)
	_, e = last.Move(1)
	category(t, e, document.InvalidPosition)
	for _, args := range [][2]int{{-1, 1}, {0, -1}, {7, 0}, {6, 1}, {1, int(^uint(0) >> 1)}} {
		_, e = c.Present(args[0], args[1])
		if e == nil {
			t.Fatal("bad window accepted", args)
		}
	}
	p, e = c.Present(6, 0)
	if e != nil || len(p.Elements) != 0 || p.StartGap != 6 || p.EndGap != 6 {
		t.Fatal(p, e)
	}
	exact(t, d, saved)
}

func TestOpaqueIdentitiesArePreservedButNotTraversedOrRendered(t *testing.T) {
	opaque := [][]byte{{0x80}, {0x1b}, {0xc0, 0x24, 1, 0xc0}, {0xc3, 0x0d, 0xc3}, {0xc4, 0x0d, 0xc4}, {0xd0, 1, 4, 0, 4, 0, 1, 0xd0}}
	for _, raw := range opaque {
		t.Run(hex.EncodeToString(raw), func(t *testing.T) {
			b := synthetic(t, append(append([]byte{'A'}, raw...), 'B'))
			d, e := document.Parse(b)
			if e != nil {
				t.Fatal(e)
			}
			if d.TokenCount() != 3 {
				t.Fatal(d.TokenCount())
			}
			tok, _ := d.Token(1)
			if tok.Kind != document.Opaque || !bytes.Equal(tok.Raw, raw) {
				t.Fatal(tok)
			}
			c, _ := d.CursorAt(1)
			next, e := c.Move(1)
			category(t, e, document.UnsupportedToken)
			if next != c {
				t.Fatal("opaque crossing changed cursor")
			}
			after, _ := d.CursorAt(2)
			next, e = after.Move(-1)
			category(t, e, document.UnsupportedToken)
			if next != after {
				t.Fatal("reverse opaque crossing changed cursor")
			}
			for _, r := range []bool{false, true} {
				p, e := c.WithReveal(r).Present(0, 3)
				category(t, e, document.UnsupportedToken)
				if len(p.Elements) != 0 {
					t.Fatal("partial opaque presentation")
				}
			}
			p, e := c.Present(2, 1)
			if e != nil || p.Elements[0].Text != "B" {
				t.Fatal(p, e)
			}
			exact(t, d, b)
		})
	}
}

func TestNativeErrorsAndTruncations(t *testing.T) {
	b := fixture(t)
	for n := 0; n < len(b); n++ {
		input := bytes.Clone(b[:n])
		before := bytes.Clone(input)
		native, ne := wp51.Parse(input)
		d, de := document.Parse(input)
		if (ne == nil) != (de == nil) {
			t.Fatalf("native acceptance changed %d: %v %v", n, ne, de)
		}
		if ne != nil {
			var f *wp51.Failure
			if !errors.As(de, &f) || d != nil {
				t.Fatal("native typed failure lost", de)
			}
		} else {
			if !bytes.Equal(native.Export(), input) {
				t.Fatal("native changed")
			}
			exact(t, d, input)
		}
		if !bytes.Equal(before, input) {
			t.Fatal("refusal mutated source")
		}
	}
	for _, body := range [][]byte{{0xc3, 0xc}, {0xc3, 0xc, 0xc4}, {0xd0, 0, 3, 0, 3, 0, 0, 0xd0}, {0}, {0x7f}} {
		_, e := document.Parse(synthetic(t, body))
		var f *wp51.Failure
		if !errors.As(e, &f) {
			t.Fatal("malformed accepted", body, e)
		}
	}
	_, e := document.Parse(make([]byte, wp51.MaxInputBytes+1))
	var nf *wp51.Failure
	if !errors.As(e, &nf) || nf.Category != wp51.InputLimit {
		t.Fatal(e)
	}
	var zero document.Document
	_, e = zero.Export()
	category(t, e, document.InvalidDocument)
	_, e = zero.CursorAt(0)
	category(t, e, document.InvalidDocument)
	var cursor document.Cursor
	_, e = cursor.Present(0, 0)
	category(t, e, document.InvalidDocument)
	_, e = cursor.Offset()
	category(t, e, document.InvalidDocument)
}

func TestTokenAndWindowBudgets(t *testing.T) {
	b := synthetic(t, bytes.Repeat([]byte{'x'}, document.MaxTokens))
	d, e := document.Parse(b)
	if e != nil || d.TokenCount() != document.MaxTokens {
		t.Fatal(e)
	}
	c, _ := d.CursorAt(document.MaxTokens)
	off, e := c.Offset()
	if e != nil || off != len(b) {
		t.Fatal(off, e)
	}
	exact(t, d, b)
	_, e = document.Parse(synthetic(t, bytes.Repeat([]byte{'x'}, document.MaxTokens+1)))
	category(t, e, document.TokenLimit)
	_, e = c.Present(0, document.MaxWindowTokens+1)
	category(t, e, document.WindowLimit)
	p, e := c.Present(0, document.MaxWindowTokens)
	if e != nil || len(p.Elements) != document.MaxWindowTokens {
		t.Fatal(len(p.Elements), e)
	}
	// A long opaque token consumes one index entry, not one entry per byte.
	body := make([]byte, 65539)
	body[0] = 0xd0
	body[1] = 1
	binary.LittleEndian.PutUint16(body[2:], 65535)
	binary.LittleEndian.PutUint16(body[65535:], 65535)
	body[65537] = 1
	body[65538] = 0xd0
	long := synthetic(t, body)
	d, e = document.Parse(long)
	if e != nil || d.TokenCount() != 1 {
		t.Fatal(e)
	}
	tok, e := d.Token(0)
	if e != nil || len(tok.Raw) != len(body) {
		t.Fatal(e)
	}
	exact(t, d, long)
}

func FuzzReadOnlyDocument(f *testing.F) {
	f.Add(fixture(f))
	for _, body := range [][]byte{{'A'}, {0x80}, {0xc0, 0x24, 1, 0xc0}, {0xc3, 12, 0xc3}, {0xd0, 1, 4, 0, 4, 0, 1, 0xd0}, {0xc3}} {
		f.Add(synthetic(f, body))
	}
	f.Fuzz(func(t *testing.T, input []byte) {
		before := bytes.Clone(input)
		d, e := document.Parse(input)
		if !bytes.Equal(before, input) {
			t.Fatal("parse mutated")
		}
		if e != nil {
			return
		}
		exact(t, d, input)
		if d.TokenCount() > document.MaxTokens {
			t.Fatal("unbounded index")
		}
		count := min(d.TokenCount(), 32)
		for i := 0; i < count; i++ {
			tok, e := d.Token(i)
			if e != nil || tok.Span.Length <= 0 {
				t.Fatal(e)
			}
			c, e := d.CursorAt(i)
			if e != nil {
				t.Fatal(e)
			}
			offset, _ := c.Offset()
			if offset != tok.Span.Offset {
				t.Fatal("gap inside token")
			}
			next, e := c.Move(1)
			if tok.Kind == document.Opaque {
				if e == nil || next != c {
					t.Fatal("opaque crossed")
				}
			} else {
				if e != nil || next.Gap() != i+1 {
					t.Fatal(e)
				}
			}
			a, e := c.Present(i, 1)
			b, e2 := c.WithReveal(true).Present(i, 1)
			if (e == nil) != (e2 == nil) {
				t.Fatal("view support drift")
			}
			if e == nil && (a.Elements[0].Span != b.Elements[0].Span || a.CursorGap != b.CursorGap) {
				t.Fatal("view mapping drift")
			}
		}
		end, e := d.CursorAt(d.TokenCount())
		if e != nil {
			t.Fatal(e)
		}
		offset, _ := end.Offset()
		if offset != len(input) {
			t.Fatal("tail lost")
		}
		exact(t, d, input)
	})
}
func BenchmarkParseTokenLimit(b *testing.B) {
	input := synthetic(b, bytes.Repeat([]byte{'x'}, document.MaxTokens))
	b.ReportAllocs()
	b.SetBytes(int64(len(input)))
	b.ResetTimer()
	for b.Loop() {
		d, e := document.Parse(input)
		if e != nil || d.TokenCount() != document.MaxTokens {
			b.Fatal(e)
		}
	}
}
func BenchmarkPresentWindow(b *testing.B) {
	d, e := document.Parse(synthetic(b, bytes.Repeat([]byte{'x'}, document.MaxTokens)))
	if e != nil {
		b.Fatal(e)
	}
	c, _ := d.CursorAt(0)
	b.ReportAllocs()
	b.ResetTimer()
	for b.Loop() {
		if _, e := c.Present(0, document.MaxWindowTokens); e != nil {
			b.Fatal(e)
		}
	}
}

func TestOriginalCorpusAndCompleteSpans(t *testing.T) {
	cases := []struct {
		path, hash string
		size       int
	}{
		{"2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5", "a42b87e3441dc422c5a348e5b6838e5949a3dabedddf49e947f784408db0dff6", 337},
		{"2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5", "c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d", 334},
		{"2026-10-29-extended-04/CMD51-131/TESTMAC.WPM", "e0e71258e6dc4c678b27773831105f0e7fca0b0803d451fb58b80ac02bc20b4e", 80},
		{"2026-10-29-extended-04/CMD51-134/PRIMARY.WP5", "635a545c0bd722194f5aa8fa300e384732428ee2c39c64fbeb99c6e32cc2ccb4", 373},
		{"2026-10-29-extended-04/CMD51-134/SECOND.WP5", "8938b5d63f74f88238aded933922eb6239696312b91151d05f62248b00fee302", 436},
		{"2026-10-29-extended-04/CMD51-134/MERGED.WP5", "8a2782895e3605538f56f656499df83c0e460fb25458b6cccbaee9aeb6b96bd3", 683},
	}
	for _, tc := range cases {
		t.Run(tc.path, func(t *testing.T) {
			input, e := os.ReadFile("../../docs/research/reference-runs/" + tc.path)
			if e != nil {
				t.Fatal(e)
			}
			sum := sha256.Sum256(input)
			if len(input) != tc.size || hex.EncodeToString(sum[:]) != tc.hash {
				t.Fatal("fixture identity changed")
			}
			d, e := document.Parse(input)
			if strings.HasSuffix(tc.path, ".WPM") {
				var f *wp51.Failure
				if !errors.As(e, &f) || f.Category != wp51.UnsupportedFileType || d != nil {
					t.Fatal("companion falsely accepted", e)
				}
				return
			}
			if e != nil {
				t.Fatal(e)
			}
			start := int(binary.LittleEndian.Uint32(input[4:8]))
			next := start
			var body []byte
			for i := 0; i < d.TokenCount(); i++ {
				tok, e := d.Token(i)
				if e != nil || tok.Span.Offset != next || len(tok.Raw) != tok.Span.Length {
					t.Fatal(i, tok, e)
				}
				body = append(body, tok.Raw...)
				next += tok.Span.Length
				exact(t, d, input)
			}
			if next != len(input) || !bytes.Equal(body, input[start:]) {
				t.Fatal("opaque span/tail lost")
			}
		})
	}
}

func TestAllFramedWidthsAndMaximumNativeInput(t *testing.T) {
	widths := []int{4, 9, 11, 3, 3, 5, 6, 7, 4, 5, 6, 6, 8, 10, 10, 12}
	for n, width := range widths {
		raw := make([]byte, width)
		raw[0] = byte(0xc0 + n)
		raw[width-1] = raw[0]
		input := synthetic(t, raw)
		d, e := document.Parse(input)
		if e != nil || d.TokenCount() != 1 {
			t.Fatal(n, e)
		}
		tok, e := d.Token(0)
		if e != nil || tok.Kind != document.Opaque || !bytes.Equal(tok.Raw, raw) {
			t.Fatal(n, tok, e)
		}
		c, _ := d.CursorAt(1)
		offset, _ := c.Offset()
		if offset != len(input) {
			t.Fatal("fixed token split")
		}
		exact(t, d, input)
	}
	prefix := synthetic(t, nil)
	body := make([]byte, 0, wp51.MaxInputBytes-len(prefix))
	large := make([]byte, 65539)
	large[0] = 0xd0
	large[1] = 1
	binary.LittleEndian.PutUint16(large[2:], 65535)
	binary.LittleEndian.PutUint16(large[65535:], 65535)
	large[65537] = 1
	large[65538] = 0xd0
	for len(body)+len(large) <= cap(body) {
		body = append(body, large...)
	}
	body = append(body, bytes.Repeat([]byte{'x'}, cap(body)-len(body))...)
	input := append(prefix, body...)
	if len(input) != wp51.MaxInputBytes {
		t.Fatal(len(input))
	}
	d, e := document.Parse(input)
	if e != nil {
		t.Fatal(e)
	}
	exact(t, d, input)
}
