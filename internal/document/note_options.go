package document

import (
	"bytes"
	"encoding/binary"
	"fmt"
)

const DefaultNoteKeep = 600

// This profile admits only a change to the keep amount. The other
// fields identify the pinned Standard Printer's ordinary footnote options.
func footnoteOptions(dst []byte, keep int) {
	dst[1] = 1
	binary.LittleEndian.PutUint16(dst[2:4], 200)
	binary.LittleEndian.PutUint16(dst[4:6], uint16(keep))
	binary.LittleEndian.PutUint16(dst[6:8], 304)
	dst[8] = '1'
	number := []byte{0xc3, 5, 0xc3, 0x8d, 0xc4, 5, 0xc4}
	copy(dst[18:], number)
	copy(dst[38:], "     ")
	copy(dst[43:], number)
	binary.LittleEndian.PutUint16(dst[58:60], 1200)
	binary.LittleEndian.PutUint16(dst[60:62], 1200)
}

func footnoteOptionsOwner(old, next int) []byte {
	raw := make([]byte, 164)
	copy(raw, []byte{0xd2, 3, 160, 0})
	footnoteOptions(raw[4:82], old)
	footnoteOptions(raw[82:160], next)
	copy(raw[160:], []byte{160, 0, 3, 0xd2})
	return raw
}

func footnoteOptionsKind(raw []byte) bool {
	if len(raw) != 164 || raw[0] != 0xd2 || raw[1] != 3 {
		return false
	}
	old := int(binary.LittleEndian.Uint16(raw[8:10]))
	next := int(binary.LittleEndian.Uint16(raw[86:88]))
	return old <= 12000 && next <= 12000 && bytes.Equal(raw, footnoteOptionsOwner(old, next))
}

func (t Token) FootnoteKeep() (int, bool) {
	if t.Kind != FootnoteOptions || !footnoteOptionsKind(t.Raw) {
		return 0, false
	}
	return int(binary.LittleEndian.Uint16(t.Raw[86:88])), true
}

func (d *Document) SetFootnoteKeep(c Cursor, old, next int) (EditResult, error) {
	if old < 0 || next < 0 || old > 12000 || next > 12000 {
		return unchangedEdit(d, c), fmt.Errorf("enter a note amount from 0 to 10 inches")
	}
	return d.editTokens(c, footnoteOptionsOwner(old, next))
}
