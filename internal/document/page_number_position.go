package document

import (
	"bytes"
	"encoding/binary"
	"fmt"
)

// The captured Standard Printer choices use the default 1/6-inch spacing.
const (
	PageNumberTopCenter   = 2
	PageNumberBottomRight = 7
)

func pageNumberPositionOwner(position byte) []byte {
	return []byte{0xd0, 8, 10, 0, 0, 0xc8, 0, position, 0xc8, 0, 10, 0, 8, 0xd0}
}

func pageNumberPositionKind(raw []byte) bool {
	return len(raw) == 14 && (raw[7] == PageNumberTopCenter || raw[7] == PageNumberBottomRight) &&
		bytes.Equal(raw, pageNumberPositionOwner(raw[7]))
}

var suppressPageNumberOwner = []byte{0xd0, 7, 6, 0, 0, 1, 6, 0, 7, 0xd0}

func (t Token) PageNumberPosition() int {
	if t.Kind == PageNumberPosition {
		return int(t.Raw[7])
	}
	return 0
}

func PageNumberPositionName(position int) string {
	switch position {
	case PageNumberTopCenter:
		return "Top Center"
	case PageNumberBottomRight:
		return "Bottom Right"
	}
	return "No page numbering"
}

func (d *Document) SetPageNumberPosition(c Cursor, position int) (EditResult, error) {
	if position != PageNumberTopCenter && position != PageNumberBottomRight {
		return unchangedEdit(d, c), fmt.Errorf("supported page numbering positions are Top Center and Bottom Right")
	}
	return d.editTokens(c, pageNumberPositionOwner(byte(position)))
}

func (d *Document) SuppressPageNumber(c Cursor) (EditResult, error) {
	return d.editTokens(c, suppressPageNumberOwner)
}

func (d *Document) pageNumberBeforeBreak(index int) (number int, suppressed bool) {
	pastPage := false
	for i := index - 1; i >= 0; i-- {
		t, _ := d.Token(i)
		if t.Kind == HardPage || t.Kind == SoftPage || t.Kind == HardReturnSoftPage || t.Kind == DeletedSoftPage {
			pastPage = true
		}
		if t.Kind == SuppressPageNumber && !pastPage {
			suppressed = true
		}
		if p := t.PageNumberPosition(); number == 0 && p != 0 {
			number = p
		}
		if pastPage && number != 0 {
			break
		}
	}
	return number, suppressed
}

func reservePageNumber(raw []byte, position int, suppressed, header, footer bool) {
	if suppressed {
		raw[15] |= 1
		return
	}
	switch position {
	case PageNumberTopCenter:
		if !header {
			reservePageText(raw, true, footer, false)
		}
	case PageNumberBottomRight:
		sub := func(index int) {
			n := binary.LittleEndian.Uint16(raw[index:])
			binary.LittleEndian.PutUint16(raw[index:], n-400)
		}
		sub(20)
		if !footer {
			sub(22)
		}
	}
}
