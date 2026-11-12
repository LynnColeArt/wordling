package document

import "testing"

func TestClosedEncoderBoundsAndRepresentations(t *testing.T) {
	for _, args := range [][6]int{{1979, 3, 9, 12, 4, 20}, {1992, 0, 9, 12, 4, 20}, {1992, 2, 30, 12, 4, 20}, {1992, 3, 9, 24, 4, 20}, {1992, 3, 9, 12, 60, 20}, {1992, 3, 9, 12, 4, 21}} {
		if _, _, ok := cachedDosStamp(args[0], args[1], args[2], args[3], args[4], args[5]); ok {
			t.Fatal("invalid DOS stamp", args)
		}
	}
	date, clock, ok := cachedDosStamp(1992, 3, 9, 12, 4, 20)
	if !ok || date != 0x1869 || clock != 0x608a {
		t.Fatal("scoped cached DOS fields")
	}
	for _, mode := range []int{0, 1, 2} {
		w := newEncoder{}
		switch mode {
		case 0:
			w.add(make([]byte, MaxNewPrefixBytes)...)
			w.u8(1)
		case 1:
			w.nul("unbounded", 2)
		case 2:
			w.u24(1 << 23)
		}
		if !w.err || len(w.bytes) > MaxNewPrefixBytes {
			t.Fatal("encoder did not refuse boundedly")
		}
	}
	w := newEncoder{}
	encodeDescriptor(&w, nativeDescriptor{italic: -2})
	if w.err || w.bytes[10] != 0xfe || w.bytes[11] != 0xff {
		t.Fatal("signed little endian representation")
	}
}
