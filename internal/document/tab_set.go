package document

import (
	"encoding/binary"
	"fmt"
	"maps"
	"slices"
	"strings"
)

const maxTabStops = 40

// TabSet stores positions in WordPerfect units measured from the left edge
// at the time the ruler was set. Relative rulers move with the left margin.
type TabSet struct {
	Stops    []int
	Margin   int
	Absolute bool
	Decimal  map[int]bool
}

func DefaultTabSet() TabSet {
	stops := make([]int, 29)
	for i := range stops {
		stops[i] = i * 600
	}
	return TabSet{Stops: stops, Margin: 1200}
}

func unpackTabSet(raw []byte, margin int) (TabSet, bool) {
	out := TabSet{Margin: margin}
	if margin == 65535 {
		out.Absolute = true
		out.Margin = 0
	}
	for i := range maxTabStops {
		v := int(binary.LittleEndian.Uint16(raw[i*2:]))
		if v == 65535 {
			continue
		}
		if v > 16800 || len(out.Stops) > 0 && v <= out.Stops[len(out.Stops)-1] || len(out.Stops) != i {
			return TabSet{}, false
		}
		out.Stops = append(out.Stops, v)
	}
	for i := range maxTabStops {
		v := raw[80+i/2]
		if i%2 == 0 {
			v >>= 4
		} else {
			v &= 15
		}
		if v == 0 {
			continue
		}
		if v != 3 || i >= len(out.Stops) {
			return TabSet{}, false
		}
		if out.Decimal == nil {
			out.Decimal = make(map[int]bool)
		}
		out.Decimal[out.Stops[i]] = true
	}
	return out, true
}

func decodeTabSet(raw []byte) (old, next TabSet, ok bool) {
	if len(raw) != 212 || raw[0] != 0xd0 || raw[1] != 4 || raw[2] != 208 ||
		raw[3] != 0 || raw[208] != 208 || raw[209] != 0 || raw[210] != 4 || raw[211] != 0xd0 {
		return
	}
	before := int(binary.LittleEndian.Uint16(raw[204:206]))
	after := int(binary.LittleEndian.Uint16(raw[206:208]))
	if before > 10200 && before != 65535 || after > 10200 && after != 65535 {
		return
	}
	old, ok = unpackTabSet(raw[4:104], before)
	if ok {
		next, ok = unpackTabSet(raw[104:204], after)
	}
	return
}

func tabSetKind(raw []byte) bool {
	_, _, ok := decodeTabSet(raw)
	return ok
}

func (t Token) Tabs() (TabSet, bool) {
	if t.Kind != TabSetCode {
		return TabSet{}, false
	}
	_, next, ok := decodeTabSet(t.Raw)
	return next, ok
}

func (s TabSet) Positions(left int) []int {
	stops := slices.Clone(s.Stops)
	if !s.Absolute {
		for i := range stops {
			stops[i] += left - s.Margin
		}
	}
	return stops
}

func packTabSet(dst []byte, ruler TabSet) {
	stops := ruler.Stops
	for i := range maxTabStops {
		v := 65535
		if i < len(stops) {
			v = stops[i]
		}
		binary.LittleEndian.PutUint16(dst[i*2:], uint16(v))
		if ruler.Decimal[v] {
			shift := uint((1 - i%2) * 4)
			dst[80+i/2] |= 3 << shift
		}
	}
}

func (d *Document) InsertTabSet(c Cursor, old, next TabSet) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if len(old.Stops) > maxTabStops || len(next.Stops) > maxTabStops {
		return unchangedEdit(d, c), fmt.Errorf("tab ruler requires up to %d left stops", maxTabStops)
	}
	if old.Absolute == next.Absolute && old.Margin == next.Margin && slices.Equal(old.Stops, next.Stops) && maps.Equal(old.Decimal, next.Decimal) {
		return d.everydayNoOp(c, blockFormatEdit), nil
	}
	raw := make([]byte, 212)
	copy(raw, []byte{0xd0, 4, 208, 0})
	copy(raw[208:], []byte{208, 0, 4, 0xd0})
	packTabSet(raw[4:104], old)
	packTabSet(raw[104:204], next)
	for i, ruler := range []TabSet{old, next} {
		value := ruler.Margin
		if ruler.Absolute {
			value = 65535
		}
		binary.LittleEndian.PutUint16(raw[204+i*2:], uint16(value))
	}
	return d.editTokens(c, raw)
}

func tabSetLabel(raw []byte) string {
	_, next, _ := decodeTabSet(raw)
	var stops []string
	for _, n := range next.Stops {
		stops = append(stops, fmt.Sprintf("%g\"", float64(n-next.Margin)/UnitsPerInch))
	}
	mode := "Rel"
	if next.Absolute {
		mode = "Abs"
	}
	return "[Tab Set:" + mode + "; " + strings.Join(stops, ", ") + "]"
}
