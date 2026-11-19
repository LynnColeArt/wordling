package wp51_test

import (
	"bytes"
	"encoding/hex"
	"errors"
	"testing"

	"github.com/lynncoleart/wordling/internal/wp51"
)

func TestOuterFraming(t *testing.T) {
	widths := []int{4, 9, 11, 3, 3, 5, 6, 7, 4, 5, 6, 6, 8, 10, 10, 12}
	for i, width := range widths {
		code := byte(0xc0 + i)
		token := bytes.Repeat([]byte{0}, width)
		token[0] = code
		token[width-1] = code
		if _, err := wp51.Parse(simple(token)); err != nil {
			t.Fatal(err)
		}
		for n := 1; n < width; n++ {
			checkError(t, simple(token[:n]), wp51.MalformedBody)
		}
		token[width-1] ^= 1
		checkError(t, simple(token), wp51.MalformedBody)
	}
	for code := 0xd0; code <= 0xff; code++ {
		for _, length := range []int{4, 5, 28, 65535} {
			token := make([]byte, length+4)
			token[0] = byte(code)
			token[1] = 0xf7
			put16(token, 2, uint16(length))
			put16(token, length, uint16(length))
			token[length+2] = 0xf7
			token[length+3] = byte(code)
			// Even 00/7F/FF payload bytes are opaque; there is no generic nested decoder.
			if length > 4 {
				token[4] = 0x7f
			}
			image, err := wp51.Parse(simple(token))
			if err != nil {
				t.Fatal(err)
			}
			if image.Inspect().OuterTokenCount != 1 {
				t.Fatal("payload was recursively traversed")
			}
			if length == 4 {
				for n := 1; n < len(token); n++ {
					checkError(t, simple(token[:n]), wp51.MalformedBody)
				}
			}
			for _, off := range []int{length, length + 2, length + 3} {
				bad := bytes.Clone(token)
				bad[off] ^= 1
				checkError(t, simple(bad), wp51.MalformedBody)
			}
			checkError(t, simple(token[:len(token)-1]), wp51.MalformedBody)
		}
	}
	for length := 0; length < 4; length++ {
		b := []byte{0xde, 0x36, byte(length), 0, 4, 0, 0x36, 0xde}
		checkError(t, simple(b), wp51.MalformedBody)
	}
	for _, token := range [][]byte{{1}, {0x1f}, {' '}, {'~'}, {0x80}, {0xbf}, {0xde, 0x36, 4, 0, 4, 0, 0x36, 0xde}, {0xde, 0x31, 4, 0, 4, 0, 0x31, 0xde}} {
		if _, err := wp51.Parse(simple(token)); err != nil {
			t.Fatal(err)
		}
	}
}

// linked builds synthetic consistent blocks with bounded zero-length opaque packets.
func linked(n int) []byte {
	b := make([]byte, 16+50*n)
	copy(b, simple(nil)[:16])
	put32(b, 4, uint32(len(b)))
	for j := 0; j < n; j++ {
		o := 16 + 50*j
		put16(b, o, 0xfffb)
		put16(b, o+2, 5)
		put16(b, o+4, 50)
		if j+1 < n {
			put32(b, o+6, uint32(o+50))
		}
		for k := 1; k < 5; k++ {
			put16(b, o+10*k, 9)
			put32(b, o+10*k+6, uint32(len(b)))
		}
	}
	return b
}
func TestPrefixTraversalAndOpaquePackets(t *testing.T) {
	b := linked(2)
	put32(b, 72, 16)
	checkError(t, b, wp51.MalformedPrefix) // two-block cycle
	b = linked(1)
	put32(b, 22, 16)
	checkError(t, b, wp51.MalformedPrefix)
	for _, next := range []uint32{1, 15, 66, 67, 0xffffffff} {
		b = linked(1)
		put32(b, 22, next)
		checkError(t, b, wp51.MalformedPrefix)
	}
	// A type 0 terminator ignores malicious next pointers and unused entry garbage.
	b = simple([]byte("tail"))
	put32(b, 22, 0xffffffff)
	copy(b[36:66], bytes.Repeat([]byte{0xff}, 30))
	image, err := wp51.Parse(b)
	if err != nil || !bytes.Equal(b, image.Export()) {
		t.Fatalf("early terminator: %v", err)
	}
	b = linked(1)
	if _, err = wp51.Parse(b); err != nil {
		t.Fatalf("zero next without terminator: %v", err)
	}
	for _, kind := range []uint16{9, 0xfffc, 0xfffd, 0xfffe, 0xffff} {
		b = simple([]byte("body"))
		b = append(b[:66], append([]byte{0, 0x7f, 0xff}, b[66:]...)...)
		put32(b, 4, 69)
		put16(b, 26, kind)
		put32(b, 28, 3)
		put32(b, 32, 66)
		image, err = wp51.Parse(b)
		if err != nil {
			t.Fatal(err)
		}
		if !bytes.Equal(b, image.Export()) {
			t.Fatal("opaque packet changed")
		}
	}
	// Nonempty aliases and partial packet overlaps are explicit unvalidated structures.
	for _, pos := range []uint32{66, 67} {
		b = make([]byte, 70)
		copy(b, simple(nil))
		put32(b, 4, 70)
		for _, entry := range []int{26, 36} {
			put16(b, entry, 9)
			put32(b, entry+2, 2)
			put32(b, entry+6, 66)
		}
		put32(b, 42, pos)
		checkError(t, b, wp51.UnsupportedStructure)
	}
	// A second complete block physically overlaps the first without overlapping headers.
	b = make([]byte, 100)
	copy(b, linked(1))
	put32(b, 4, 100)
	put32(b, 22, 46)
	put16(b, 26, 0) // terminator prevents following it, so replace with entries.
	for _, entry := range []int{26, 36, 46, 56} {
		put16(b, entry, 9)
		put32(b, entry+2, 0)
		put32(b, entry+6, 100)
	}
	put16(b, 46, 0xfffb)
	put16(b, 48, 5)
	put16(b, 50, 50)
	put32(b, 52, 0)
	put16(b, 56, 0)
	// The overlapping header occupies a general index in block 1 and is refused.
	checkError(t, b, wp51.UnsupportedStructure)
	// Two individually complete index headers overlap. The aliased packet span
	// is also outside the validated non-overlap subset; neither interpretation
	// authorizes an accepted image.
	b = make([]byte, 400000)
	copy(b, linked(1))
	put32(b, 4, uint32(len(b)))
	put32(b, 22, 58)
	for _, entry := range []int{26, 36, 46, 56} {
		put16(b, entry, 9)
		put32(b, entry+2, 0)
		put32(b, entry+6, uint32(len(b)))
	}
	put16(b, 58, 0xfffb)
	put16(b, 60, 5)
	put16(b, 62, 50)
	put32(b, 64, 0)
	checkError(t, b, wp51.UnsupportedStructure)
}
func TestGraphicsException(t *testing.T) {
	graphic := func() []byte {
		b := make([]byte, 68)
		copy(b, simple(nil))
		put32(b, 4, 68)
		put16(b, 26, 8)
		put32(b, 28, 2)
		put32(b, 32, 66)
		return b
	}
	b := graphic()
	image, err := wp51.Parse(b)
	if err != nil || !bytes.Equal(b, image.Export()) {
		t.Fatal(err)
	}
	b = graphic()
	put16(b, 66, 1)
	checkError(t, b, wp51.UnsupportedStructure)
	for _, n := range []uint32{0, 1, 3} {
		b = graphic()
		put32(b, 28, n)
		checkError(t, b, wp51.MalformedPrefix)
	}
	b = graphic()
	put16(b, 36, 9)
	put32(b, 42, 68)
	checkError(t, b, wp51.UnsupportedStructure)
	b = graphic()
	put32(b, 32, 67)
	checkError(t, b, wp51.MalformedPrefix)
}
func TestResourceBoundaries(t *testing.T) {
	b := simple(nil)
	b = append(b, bytes.Repeat([]byte{'x'}, wp51.MaxInputBytes-len(b))...)
	image, err := wp51.Parse(b)
	if err != nil {
		t.Fatal(err)
	}
	if image.Inspect().OuterTokenCount != len(b)-66 || !bytes.Equal(b, image.Export()) {
		t.Fatal("max-size bytes/token count changed")
	}
	checkError(t, append(b, 'x'), wp51.InputLimit)
	b = linked(wp51.MaxIndexBlocks)
	image, err = wp51.Parse(b)
	if err != nil {
		t.Fatal(err)
	}
	info := image.Inspect()
	if len(info.Blocks) != 4096 || len(info.Packets) != 16384 {
		t.Fatal("boundary traversal incomplete")
	}
	checkError(t, linked(wp51.MaxIndexBlocks+1), wp51.TraversalLimit)
}
func FuzzNativeFraming(f *testing.F) {
	fixtures, recipes := corpus(f)
	seeds := map[string][]byte{}
	for _, fixture := range fixtures {
		b := readFixture(f, fixture)
		seeds[fixture.ID] = b
		f.Add(b)
	}
	for _, r := range recipes {
		suffix, err := hex.DecodeString(r.Append)
		if err != nil {
			f.Fatal(err)
		}
		f.Add(append(bytes.Clone(seeds[r.Seed]), suffix...))
	}
	for _, b := range [][]byte{nil, {}, simple(nil), simple([]byte{0}), simple([]byte{0x7f}), simple([]byte{0xff}), simple([]byte{0xde, 0x36, 3, 0, 4, 0, 0x36, 0xde})} {
		f.Add(b)
	}
	cycle := linked(2)
	put32(cycle, 72, 16)
	f.Add(cycle)
	huge := linked(1)
	put32(huge, 28, 0xffffffff)
	f.Add(huge)
	f.Fuzz(func(t *testing.T, b []byte) {
		before := bytes.Clone(b)
		image, err := wp51.Parse(b)
		if !bytes.Equal(b, before) {
			t.Fatal("input mutation")
		}
		if err != nil {
			var e *wp51.Failure
			if image != nil || !errors.As(err, &e) || e.Offset < 0 || e.Field == "" {
				t.Fatalf("untyped refusal: %v", err)
			}
			return
		}
		out := image.Export()
		if len(out) != len(b) || !bytes.Equal(out, b) || sha256Sum(out) != sha256Sum(b) {
			t.Fatal("non-identical export")
		}
		if len(b) > 0 {
			b[0] ^= 0xff
			out[0] ^= 0x01
			if !bytes.Equal(image.Export(), before) {
				t.Fatal("buffer isolation")
			}
		}
	})
}
func sha256Sum(b []byte) string { return hash(b) }
func BenchmarkMaxBody(b *testing.B) {
	input := simple(nil)
	input = append(input, bytes.Repeat([]byte{'x'}, wp51.MaxInputBytes-len(input))...)
	b.SetBytes(int64(len(input)))
	b.ReportAllocs()
	b.ResetTimer()
	for n := 0; n < b.N; n++ {
		if _, err := wp51.Parse(input); err != nil {
			b.Fatal(err)
		}
	}
}
func BenchmarkMaxPrefix(b *testing.B) {
	input := linked(wp51.MaxIndexBlocks)
	b.SetBytes(int64(len(input)))
	b.ReportAllocs()
	b.ResetTimer()
	for n := 0; n < b.N; n++ {
		if _, err := wp51.Parse(input); err != nil {
			b.Fatal(err)
		}
	}
}

func TestFailureDetailsAndSpanBounds(t *testing.T) {
	cycle := linked(1)
	put32(cycle, 22, 16)
	for _, tt := range []struct {
		input  []byte
		offset int
		detail string
	}{{cycle, 16, "Cycle"}, {simple([]byte{0xc3, 1, 0xc4}), 68, "DelimiterMismatch"}, {simple([]byte{0xde, 0x36, 4, 0, 5, 0, 0x36, 0xde}), 70, "DelimiterMismatch"}} {
		_, err := wp51.Parse(tt.input)
		var failure *wp51.Failure
		if !errors.As(err, &failure) || failure.Offset != tt.offset || failure.Detail != tt.detail {
			t.Fatalf("want offset %d detail %s, got %v", tt.offset, tt.detail, err)
		}
	}
	image, err := wp51.Parse(simple([]byte("text")))
	if err != nil {
		t.Fatal(err)
	}
	for _, span := range []wp51.Span{{Offset: 0, Length: -1}, {Offset: 1, Length: int(^uint(0) >> 1)}, {Offset: int(^uint(0) >> 1), Length: 2}} {
		if _, ok := image.Bytes(span); ok {
			t.Fatalf("invalid span accepted: %v", span)
		}
	}
	data, ok := image.Bytes(image.Inspect().Body)
	if !ok || string(data) != "text" {
		t.Fatal("body span copy mismatch")
	}
}
