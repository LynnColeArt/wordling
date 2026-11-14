package document

import "encoding/binary"

func validIndentPosition(raw []byte) bool {
	position := int(binary.LittleEndian.Uint16(raw))
	return position >= 1800 && position <= 9000 && (position-1200)%600 == 0
}

// InsertIndent writes the DOS left-indent owner for the Standard Printer.
func (d *Document) InsertIndent(c Cursor, previousMargin, column int) (EditResult, error) {
	return d.insertIndent(c, previousMargin, column, false)
}

func (d *Document) InsertDoubleIndent(c Cursor, previousMargin, column int) (EditResult, error) {
	return d.insertIndent(c, previousMargin, column, true)
}

func (d *Document) insertIndent(c Cursor, previousMargin, column int, double bool) (EditResult, error) {
	if !validEverydayTabStop(column) || previousMargin < 0 || previousMargin >= column {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	position := uint16(1200 + column*120)
	raw := []byte{0xc2, 0, 0, 0, 0, 0, 0, 0, byte(10 + column), 0, 0xc2}
	if double {
		raw[1] = 1
	}
	binary.LittleEndian.PutUint16(raw[2:], uint16((column-previousMargin)*120))
	binary.LittleEndian.PutUint16(raw[4:], position)
	binary.LittleEndian.PutUint16(raw[6:], position)
	return d.editTokens(c, raw)
}

// IndentColumn reports the stored absolute temporary left margin relative
// to the ordinary one-inch margin.
func (t Token) IndentColumn() int {
	if t.Kind != Indent && t.Kind != DoubleIndent {
		return 0
	}
	return (int(binary.LittleEndian.Uint16(t.Raw[6:8])) - 1200) / 120
}

func (d *Document) InsertMarginRelease(c Cursor, column int) (EditResult, error) {
	if column < 0 || column > 65 || column%5 != 0 {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	raw := []byte{0xc1, 0x80, 0, 0, 0, 0, byte(10 + column), 0, 0xc1}
	binary.LittleEndian.PutUint16(raw[2:4], uint16(1200+column*120))
	copy(raw[4:6], raw[2:4])
	return d.editTokens(c, raw)
}

func (t Token) MarginReleaseColumn() int {
	if t.Kind != MarginRelease {
		return 0
	}
	return int(t.Raw[6]) - 10
}

func (d *Document) InsertIndentedReturn(c Cursor, column int) (EditResult, error) {
	if !validEverydayTabStop(column) {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	raw := []byte{0xc6, 0x28, 0x23, 0, 0, 0xc6, hardReturnByte}
	for i := c.gap - 1; i >= 0; i-- {
		t, _ := d.Token(i)
		if t.Kind == DoubleIndent {
			binary.LittleEndian.PutUint16(raw[1:3], uint16(9000-column*120))
			break
		}
		if t.Kind == Indent || t.Kind == HardReturn || t.Kind == HardPage {
			break
		}
	}
	binary.LittleEndian.PutUint16(raw[3:], uint16(1200+column*120))
	return d.insertNamedTokens(c, raw, 2)
}
