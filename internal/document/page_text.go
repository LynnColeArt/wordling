package document

import (
	"bytes"
	"encoding/binary"
	"fmt"
)

type PageText struct {
	Slot, Pages int
	Text        string
}

func (p PageText) Footer() bool { return p.Slot >= 2 }

func (p PageText) Label() string {
	label := "Header"
	if p.Footer() {
		label = "Footer"
	}
	return fmt.Sprintf("%s %c", label, 'A'+rune(p.Slot%2))
}

func (p PageText) Applies(page int) bool {
	return p.Pages == 1 || p.Pages == 2 && page%2 == 1 || p.Pages == 4 && page%2 == 0
}

func (t Token) PageText() (PageText, bool) {
	if t.Kind != PageTextCode {
		return PageText{}, false
	}
	return readPageText(t.Raw)
}

func readPageText(raw []byte) (PageText, bool) {
	if len(raw) == 22 && raw[0] == 0xd5 && raw[1] <= 3 && bytes.Equal(raw, pageTextOwner(PageText{Slot: int(raw[1])})) {
		return PageText{Slot: int(raw[1])}, true
	}
	if len(raw) < 27 || len(raw) > 86 || raw[0] != 0xd5 || raw[1] > 3 ||
		raw[len(raw)-2] != raw[1] || raw[len(raw)-1] != 0xd5 || raw[12] != 200 || raw[13] != 0 {
		return PageText{}, false
	}
	pages := int(raw[11])
	stop := len(raw) - 4
	if int(binary.LittleEndian.Uint16(raw[2:4])) != stop || !sameRecordTrailer(raw, stop) {
		return PageText{}, false
	}
	if pages != 1 && pages != 2 && pages != 4 {
		return PageText{}, false
	}
	for _, value := range raw[4:11] {
		if value != 0 {
			return PageText{}, false
		}
	}
	for _, value := range raw[15:20] {
		if value != 0 {
			return PageText{}, false
		}
	}
	if raw[14] > raw[1]/2 {
		return PageText{}, false
	}
	for _, value := range raw[22 : len(raw)-4] {
		if value < 32 || value > 126 {
			return PageText{}, false
		}
	}
	return PageText{Slot: int(raw[1]), Pages: pages, Text: string(raw[22 : len(raw)-4])}, true
}

func pageTextOwner(p PageText) []byte {
	return pageTextOwnerWithHeader(p, false)
}

func pageTextOwnerWithHeader(p PageText, header bool) []byte {
	if p.Pages == 0 {
		return []byte{0xd5, byte(p.Slot), 18, 0, 1, 200, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 18, 0, 18, 0, byte(p.Slot), 0xd5}
	}
	raw := make([]byte, 22)
	raw[0], raw[1], raw[11], raw[12] = 0xd5, byte(p.Slot), byte(p.Pages), 200
	raw[20], raw[21] = 0x13, 0x8f
	if p.Footer() && header {
		raw[14] = 1
		if p.Slot == 2 {
			raw[21] = 0xa1
		} else {
			raw[20], raw[21] = 0x59, 0x5c
		}
	}
	raw = append(raw, p.Text...)
	length := len(raw)
	binary.LittleEndian.PutUint16(raw[2:4], uint16(length))
	return append(raw, byte(length), byte(length>>8), byte(p.Slot), 0xd5)
}

func (d *Document) InsertPageText(c Cursor, text PageText) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if text.Slot < 0 || text.Slot > 3 {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	var headers [2]bool
	for i := 0; i < c.gap; i++ {
		token, _ := d.Token(i)
		if text, ok := token.PageText(); ok && !text.Footer() {
			headers[text.Slot] = text.Pages != 0
		}
	}
	raw := pageTextOwnerWithHeader(text, headers[0] || headers[1])
	if _, ok := readPageText(raw); !ok {
		return unchangedEdit(d, c), fmt.Errorf("enter 1 to 60 printable characters for the header or footer")
	}
	return d.editTokens(c, raw)
}

func pageTextLabel(raw []byte) string {
	text, ok := readPageText(raw)
	if !ok {
		return ""
	}
	pages := "Every page"
	if text.Pages == 0 {
		return "[" + text.Label() + ":Discontinue]"
	} else if text.Pages == 2 {
		pages = "Odd pages"
	} else if text.Pages == 4 {
		pages = "Even pages"
	}
	return fmt.Sprintf("[%s:%s;%s]", text.Label(), pages, text.Text)
}
