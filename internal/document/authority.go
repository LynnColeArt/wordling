package document

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"strings"
)

func plainAuthority(text string) bool {
	return len(text) > 0 && len(text) <= 255 &&
		strings.IndexFunc(text, func(c rune) bool { return c < 32 || c > 126 }) == -1
}

func authorityFields(raw []byte) (section int, short, full string, ok bool) {
	if len(raw) < 13 || raw[0] != 0xd7 || raw[1] != 4 || raw[4] > 15 || raw[5] != 0 || raw[len(raw)-1] != 0xd7 {
		return
	}
	stop := len(raw) - 4
	if int(binary.LittleEndian.Uint16(raw[2:4])) != stop || !sameRecordTrailer(raw, stop) {
		return
	}
	n := bytes.IndexByte(raw[6:stop], 0)
	if n == -1 {
		return
	}
	short, full = string(raw[6:6+n]), string(raw[7+n:stop])
	return int(raw[4]) + 1, short, full, plainAuthority(short) && plainAuthority(full)
}

func isAuthority(raw []byte) bool {
	_, _, _, ok := authorityFields(raw)
	return ok
}

func (d *Document) AuthoritySelection(anchor, c Cursor) (string, error) {
	if err := d.checkEverydayCursor(anchor); err != nil {
		return "", err
	}
	if err := d.checkEverydayCursor(c); err != nil {
		return "", err
	}
	first, last := min(anchor.gap, c.gap), max(anchor.gap, c.gap)
	if first == last || last-first > 255 {
		return "", fmt.Errorf("select a citation of 1 to 255 text characters")
	}
	var text strings.Builder
	for i := first; i < last; i++ {
		t, _ := d.Token(i)
		if t.Kind != ASCII || !plainAuthority(string(t.Raw)) {
			return "", fmt.Errorf("this citation requires a single line of plain text")
		}
		text.Write(t.Raw)
	}
	return text.String(), nil
}

func (d *Document) MarkAuthority(anchor, c Cursor, section int, short, full string) (EditResult, error) {
	if _, err := d.AuthoritySelection(anchor, c); err != nil {
		return unchangedEdit(d, c), err
	}
	if section < 1 || section > 16 || !plainAuthority(short) || !plainAuthority(full) {
		return unchangedEdit(d, c), fmt.Errorf("enter a section from 1 to 16 and both citation forms")
	}
	for i := 0; i < d.TokenCount(); i++ {
		t, _ := d.Token(i)
		if t.Kind == AuthorityMark {
			_, existing, _, _ := authorityFields(t.Raw)
			if strings.EqualFold(existing, short) {
				return unchangedEdit(d, c), fmt.Errorf("that short form already identifies an authority")
			}
		}
	}
	raw := append([]byte{0xd7, 4, 0, 0, byte(section - 1), 0}, short...)
	raw = append(raw, 0)
	raw = append(raw, full...)
	size := len(raw)
	binary.LittleEndian.PutUint16(raw[2:4], uint16(size))
	raw = append(raw, byte(size), byte(size>>8), 4, 0xd7)
	at := c
	at.gap = min(anchor.gap, c.gap)
	receipt, err := d.insertNamedTokensAt(at, raw, 1, 0)
	if err != nil {
		return unchangedEdit(d, c), err
	}
	return receipt, nil
}
