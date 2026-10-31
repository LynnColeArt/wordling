package document_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
	"os"
	"testing"
)

func FuzzNativeMutation(f *testing.F) {
	f.Add(fixture(f), []byte("XY"), uint16(1), true)
	two, e := os.ReadFile("../../docs/research/continuation/native-edits/runs/wp23-b-history-follow-repair-restore-r1/N0001.WP5")
	if e != nil {
		f.Fatal(e)
	}
	f.Add(two, []byte("X"), uint16(4), false)
	for _, body := range [][]byte{{'A'}, {0x80}, {0xc3, 12, 0xc3}, {0xd0, 1, 4, 0, 4, 0, 1, 0xd0}, bytes.Repeat([]byte{0xc3, 12, 0xc3, 0xc4, 12, 0xc4}, 3)} {
		f.Add(synthetic(f, body), []byte("X\r"), uint16(0), false)
	}
	f.Add(synthetic(f, bytes.Repeat([]byte{'x'}, document.MaxMutationTokens)), []byte("X"), uint16(0), false)
	f.Fuzz(func(t *testing.T, input, text []byte, gap uint16, over bool) {
		before := bytes.Clone(input)
		d, e := document.Parse(input)
		if !bytes.Equal(input, before) {
			t.Fatal("caller changed")
		}
		if e != nil {
			return
		}
		exact(t, d, before)
		c, e := d.CursorAt(int(gap))
		if e != nil {
			return
		}
		var r document.EditResult
		if over {
			r, e = d.TypeoverASCII(c, text)
		} else {
			r, e = d.InsertASCII(c, text)
		}
		exact(t, d, before)
		if e != nil {
			if r.Document != d || r.Cursor != c || r.Changed {
				t.Fatal("partial edit on refusal")
			}
			return
		}
		if e = r.Document.CheckMutation(); e != nil {
			t.Fatal("unsafe successful result", e)
		}
		raw, e := r.Document.Export()
		if e != nil {
			t.Fatal(e)
		}
		if len(raw) > document.MaxMutationBytes || r.Document.TokenCount() > document.MaxMutationTokens {
			t.Fatal("mutation budgets")
		}
		image, e := wp51.Parse(raw)
		if e != nil || !bytes.Equal(image.Export(), raw) {
			t.Fatal("invalid candidate", e)
		}
		source, e := r.Document.OriginalExport()
		if e != nil || !bytes.Equal(source, before) {
			t.Fatal("original source lost", e)
		}
		if r.Cursor.Gap() != c.Gap()+len(text) || r.Cursor.Reveal() != c.Reveal() {
			t.Fatal("wrong cursor")
		}
		info := image.Inspect()
		flag := -1
		for _, p := range info.Packets {
			if p.Type == 6 {
				flag = p.Data.Offset
			}
		}
		for i, b := range raw[:info.Body.Offset] {
			want := before[i]
			if i == flag && r.Changed {
				want |= 8
			}
			if b != want {
				t.Fatal("unrelated prefix byte changed", i)
			}
		}
		if r.Changed && r.Document.Revision() == d.Revision() {
			t.Fatal("revision reused")
		}
		if !r.Changed && !bytes.Equal(raw, before) {
			t.Fatal("no-change altered bytes")
		}
		// Returned token/candidate buffers cannot mutate the accepted revision.
		if len(raw) > 0 {
			raw[0] ^= 1
		}
		again, _ := r.Document.Export()
		if again[0] != 0xff {
			t.Fatal("export alias")
		}
		// Legal public wrapper replacement must not rebind old cursor state.
		// The labelled synthetic shorter body retains this admitted prefix;
		// it is a safety fixture, never a product new-document writer.
		oldRevision := c.Revision()
		oldOffset, _ := c.Offset()
		window := min(d.TokenCount(), 16)
		oldView, _ := c.Present(0, window)
		replacementBytes := append(bytes.Clone(before[:info.Body.Offset]), 'A')
		replacement, e := document.Parse(replacementBytes)
		if e != nil {
			t.Fatal(e)
		}
		*d = *replacement
		if c.Revision() != oldRevision || d.Revision() == oldRevision {
			t.Fatal("wrapper rebound revision")
		}
		if offset, e := c.Offset(); e != nil || offset != oldOffset {
			t.Fatal("wrapper rebound gap", e)
		}
		view, e := c.Present(0, window)
		if e != nil {
			t.Fatal(e)
		}
		for i, element := range oldView.Elements {
			if element != view.Elements[i] {
				t.Fatal("wrapper rebound view")
			}
		}
		refused, e := d.InsertASCII(c, []byte("X"))
		category(t, e, document.RevisionMismatch)
		if refused.Document != d || refused.Cursor != c || refused.Changed {
			t.Fatal("stale cursor consumed state")
		}
		exact(t, d, replacementBytes)
	})
}

func BenchmarkMutationAdmission(b *testing.B) {
	d, _ := document.Parse(synthetic(b, bytes.Repeat([]byte{'x'}, document.MaxMutationTokens)))
	b.ReportAllocs()
	b.ResetTimer()
	for b.Loop() {
		if e := d.CheckMutation(); e != nil {
			b.Fatal(e)
		}
	}
}
func BenchmarkMutationAtLimit(b *testing.B) {
	d, _ := document.Parse(synthetic(b, bytes.Repeat([]byte{'x'}, document.MaxMutationTokens)))
	c, _ := d.CursorAt(0)
	b.ReportAllocs()
	b.ResetTimer()
	for b.Loop() {
		if _, e := d.TypeoverASCII(c, []byte("Y")); e != nil {
			b.Fatal(e)
		}
	}
}
