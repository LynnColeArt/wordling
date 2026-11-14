package document

import (
	"bytes"
	"encoding/binary"
	"fmt"
)

var outlineStart = [...]byte{0xd9, 4, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 4, 0xd9}
var outlineIndent = [...]byte{0xc1, 0, 8, 7, 8, 7, 15, 0, 0xc1}

type outlineNumber struct {
	level    int
	previous [2]int
	text     string
}

func outlineNumberFields(raw []byte) (outlineNumber, bool) {
	if len(raw) < 27 || raw[0] != 0xd8 || raw[1] != 1 || raw[4] > 1 || raw[len(raw)-1] != 0xd8 {
		return outlineNumber{}, false
	}
	stop := len(raw) - 4
	if int(binary.LittleEndian.Uint16(raw[2:4])) != stop || !sameRecordTrailer(raw, stop) {
		return outlineNumber{}, false
	}
	for _, b := range raw[9:21] {
		if b != 0 {
			return outlineNumber{}, false
		}
	}
	o := outlineNumber{
		level:    int(raw[4]),
		previous: [2]int{int(binary.LittleEndian.Uint16(raw[5:7])), int(binary.LittleEndian.Uint16(raw[7:9]))},
		text:     string(raw[21:stop]),
	}
	want, ok := outlineLabel(o.level, o.previous[o.level]+1)
	return o, ok && o.text == want
}

func outlineLabel(level, ordinal int) (string, bool) {
	if level == 1 && ordinal >= 1 && ordinal <= 26 {
		return string(rune('A'+ordinal-1)) + ".", true
	}
	roman := [...]string{"", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"}
	if level == 0 && ordinal >= 1 && ordinal < len(roman) {
		return roman[ordinal] + ".", true
	}
	return "", false
}

func (t Token) OutlineText() string {
	if t.Kind != OutlineNumber {
		return ""
	}
	o, _ := outlineNumberFields(t.Raw)
	return o.text
}

func outlineNumberOwner(level int, previous [2]int) ([]byte, error) {
	text, ok := outlineLabel(level, previous[level]+1)
	if !ok {
		return nil, fmt.Errorf("outline number is outside the captured default range")
	}
	raw := make([]byte, 21)
	raw[0], raw[1], raw[4] = 0xd8, 1, byte(level)
	binary.LittleEndian.PutUint16(raw[5:7], uint16(previous[0]))
	binary.LittleEndian.PutUint16(raw[7:9], uint16(previous[1]))
	raw = append(raw, text...)
	raw[2] = byte(len(raw))
	return append(raw, raw[2], 0, 1, 0xd8), nil
}

func (d *Document) StartOutline(c Cursor) (EditResult, error) {
	if c.gap != 0 || d.TokenCount() != 0 {
		return unchangedEdit(d, c), fmt.Errorf("start this outline in a blank document")
	}
	return d.editTokens(c, outlineStart[:])
}

func (d *Document) OutlineAt(c Cursor) bool {
	t, err := d.Token(0)
	return err == nil && t.Kind == OutlineOn && c.gap > 0
}

func (d *Document) NextOutline(c Cursor, changeLevel bool) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if c.gap != d.TokenCount() || !d.OutlineAt(c) {
		return unchangedEdit(d, c), fmt.Errorf("continue the outline at the end of the document")
	}
	level, last := 0, -1
	var previous [2]int
	if c.gap > 1 {
		for i := c.gap - 1; i > 0; i-- {
			t, _ := d.Token(i)
			if t.Kind == OutlineNumber {
				o, _ := outlineNumberFields(t.Raw)
				level, previous, last = o.level, o.previous, i
				break
			}
		}
	}
	if changeLevel {
		if last != c.gap-1 || level != 0 || previous[0] < 1 {
			return unchangedEdit(d, c), fmt.Errorf("Tab changes a new top-level outline item to the second level")
		}
		raw := d.state.image.Export()
		body := append([]byte(nil), raw[d.state.gaps[0]:d.state.gaps[last]]...)
		body = append(body, outlineIndent[:]...)
		next, err := outlineNumberOwner(1, previous)
		if err != nil {
			return unchangedEdit(d, c), err
		}
		body = append(body, next...)
		mapping := make([]int, d.TokenCount())
		for i := range mapping {
			mapping[i] = i
		}
		mapping[last] = -1
		return d.publishEveryday(c, body, d.TokenCount()+1, c.gap+1, mapping, blockFormatEdit)
	}
	body := []byte{hardReturnByte}
	count := 2
	if last >= 0 {
		previous[level]++
	}
	if level == 1 {
		body = append(body, outlineIndent[:]...)
		count++
	}
	next, err := outlineNumberOwner(level, previous)
	if err != nil {
		return unchangedEdit(d, c), err
	}
	return d.insertNamedTokens(c, append(body, next...), count)
}

func isOutlineStart(raw []byte) bool { return bytes.Equal(raw, outlineStart[:]) }

func (t Token) OutlineIndent() bool { return t.Kind == Tab && bytes.Equal(t.Raw, outlineIndent[:]) }
