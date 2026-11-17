package document

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"strconv"
)

const (
	centerAlignmentByte      = 0xe0
	rightAlignmentByte       = 0x60
	decimalAlignmentByte     = 0x40
	softDecimalAlignmentByte = 0x42
	endAlignmentByte         = 0x83
	inlineAlignmentByte      = 0x8f
)

func alignmentOwner(kind Kind, position, anchor int) []byte {
	mode := byte(centerAlignmentByte)
	if kind == FlushRight {
		mode = rightAlignmentByte
	} else if kind == ContentsLeader {
		mode = 0x70
	} else if kind == DecimalTab {
		mode = decimalAlignmentByte
	} else if kind == SoftDecimalTab {
		mode = softDecimalAlignmentByte
	}
	raw := []byte{0xc1, mode, 0, 0, 0, 0, 0, 0, 0xc1}
	binary.LittleEndian.PutUint16(raw[2:4], uint16(position))
	binary.LittleEndian.PutUint16(raw[4:6], uint16(anchor))
	binary.LittleEndian.PutUint16(raw[6:8], uint16((position+60)/120))
	return raw
}

func alignmentKind(raw []byte) Kind {
	if len(raw) != 9 || raw[0] != 0xc1 {
		return Opaque
	}
	var kind Kind
	switch raw[1] {
	case centerAlignmentByte:
		kind = CenterLine
	case 0x70:
		kind = ContentsLeader
	case rightAlignmentByte:
		kind = FlushRight
	case decimalAlignmentByte:
		kind = DecimalTab
	case softDecimalAlignmentByte:
		kind = SoftDecimalTab
	default:
		return Opaque
	}
	position := int(binary.LittleEndian.Uint16(raw[2:4]))
	anchor := int(binary.LittleEndian.Uint16(raw[4:6]))
	if position <= anchor && anchor <= 10200 && bytes.Equal(raw, alignmentOwner(kind, position, anchor)) {
		return kind
	}
	return Opaque
}

func (d *Document) InsertAlignment(c Cursor, kind Kind) (EditResult, error) {
	if kind != CenterLine && kind != FlushRight && kind != DecimalTab && kind != SoftDecimalTab {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	raw := append(alignmentOwner(kind, 0, 0), endAlignmentByte)
	if (kind == DecimalTab || kind == SoftDecimalTab) && d.BeforeDecimalAlignmentEnd(c.gap) {
		c.gap++
	}
	return d.insertNamedTokensAt(c, raw, 2, 1)
}

// EndLineAlignment replaces the active alignment terminator or inserts a
// paragraph return immediately after it.
func (d *Document) EndLineAlignment(c Cursor, inline bool) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if !d.BeforeAutomaticAlignmentEnd(c.Gap()) {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	if !inline {
		return d.InsertHardReturn(Cursor{state: c.state, gap: c.gap + 1, reveal: c.reveal})
	}
	body := d.state.image.Export()[d.state.gaps[0]:]
	body[int(d.state.gaps[c.gap]-d.state.gaps[0])] = inlineAlignmentByte
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
	}
	return d.publishEveryday(c, body, d.TokenCount(), c.gap+1, mapping, blockFormatEdit)
}

func (d *Document) BeforeAutomaticAlignmentEnd(gap int) bool {
	owner, err := d.Token(gap)
	return err == nil && owner.Kind == EndAlignment && owner.Raw[0] == endAlignmentByte
}

func (d *Document) BeforeDecimalAlignmentEnd(gap int) bool {
	if !d.BeforeAutomaticAlignmentEnd(gap) {
		return false
	}
	for i := gap - 1; i >= 0; i-- {
		t, _ := d.Token(i)
		switch t.Kind {
		case DecimalTab, SoftDecimalTab:
			return true
		case CenterLine, FlushRight, EndAlignment, HardReturn, HardPage, Tab:
			return false
		}
	}
	return false
}

// InsertDecimalText closes a hard decimal tab before the first period.
func (d *Document) InsertDecimalText(c Cursor, text []byte) (EditResult, error) {
	at := bytes.IndexByte(text, '.')
	if at < 0 || !d.BeforeDecimalAlignmentEnd(c.gap) {
		return d.InsertASCII(c, text)
	}
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	for _, b := range text {
		if b < 32 || b > 126 {
			return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
		}
	}
	image := d.state.image.Export()
	offset := int(d.state.gaps[c.gap])
	body := append([]byte(nil), image[d.state.gaps[0]:offset]...)
	body = append(body, text[:at]...)
	body = append(body, endAlignmentByte)
	body = append(body, text[at:]...)
	body = append(body, image[offset+1:]...)
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
		if i == c.gap {
			mapping[i] += at
		} else if i > c.gap {
			mapping[i] += len(text)
		}
	}
	return d.publishEveryday(c, body, d.TokenCount()+len(text), c.gap+len(text)+1, mapping, blockFormatEdit)
}

const UnitsPerInch = 1200

type Justification byte

const (
	JustifyLeft Justification = iota
	JustifyFull
	JustifyCenter
	JustifyRight
)

func (j Justification) String() string {
	if j > JustifyRight {
		return ""
	}
	return [...]string{"Left", "Full", "Center", "Right"}[j]
}

func justificationKind(raw []byte) bool {
	return len(raw) == 10 && raw[0] == 0xd0 && raw[1] == 6 && raw[2] == 6 && raw[3] == 0 &&
		raw[4] <= 3 && raw[5] <= 3 && raw[6] == 6 && raw[7] == 0 && raw[8] == 6 && raw[9] == 0xd0
}

func (t Token) Justification() (Justification, bool) {
	if t.Kind != ParagraphJustification || !justificationKind(t.Raw) {
		return 0, false
	}
	return Justification(t.Raw[5]), true
}

func (d *Document) InsertJustification(c Cursor, old, next Justification) (EditResult, error) {
	if old > JustifyRight || next > JustifyRight {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	raw := []byte{0xd0, 6, 6, 0, byte(old), byte(next), 6, 0, 6, 0xd0}
	return d.editTokens(c, raw)
}

func justificationCache(raw []byte) bool {
	if len(raw) != 12 || raw[0] != 0xd4 || raw[1] != 5 || raw[2] != 8 || raw[3] != 0 ||
		raw[8] != 8 || raw[9] != 0 || raw[10] != 5 || raw[11] != 0xd4 {
		return false
	}
	position := binary.LittleEndian.Uint16(raw[6:8])
	return position <= 10200 && binary.LittleEndian.Uint16(raw[4:6]) == position/120
}

func paragraphPositionOwner(position uint16) []byte {
	raw := []byte{0xd4, 5, 8, 0, 0, 0, 0, 0, 8, 0, 5, 0xd4}
	binary.LittleEndian.PutUint16(raw[4:6], position/120)
	binary.LittleEndian.PutUint16(raw[6:8], position)
	return raw
}

func spacingKind(raw []byte) bool {
	return len(raw) == 12 && raw[0] == 0xd0 && raw[1] == 2 && raw[2] == 8 && raw[3] == 0 &&
		raw[4] == 0 && raw[5] >= 1 && raw[5] <= 9 && raw[6] == 0 && raw[7] >= 1 && raw[7] <= 9 &&
		raw[8] == 8 && raw[9] == 0 && raw[10] == 2 && raw[11] == 0xd0
}

func (t Token) LineSpacing() int {
	if t.Kind != LineSpacing || !spacingKind(t.Raw) {
		return 0
	}
	return int(t.Raw[7])
}

func (d *Document) InsertLineSpacing(c Cursor, prior, spacing int) (EditResult, error) {
	if prior < 1 || prior > 9 || spacing < 1 || spacing > 9 {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	raw := []byte{0xd0, 2, 8, 0, 0, byte(prior), 0, byte(spacing), 8, 0, 2, 0xd0}
	return d.editTokens(c, raw)
}

func lineHeightKind(raw []byte) bool {
	return len(raw) == 12 && raw[0] == 0xd0 && raw[1] == 0 && raw[2] == 8 && raw[3] == 0 &&
		binary.LittleEndian.Uint16(raw[4:6]) <= 12000 && binary.LittleEndian.Uint16(raw[6:8]) <= 12000 &&
		raw[8] == 8 && raw[9] == 0 && raw[10] == 0 && raw[11] == 0xd0
}

func (t Token) LineHeight() int {
	if t.Kind != LineHeight || !lineHeightKind(t.Raw) {
		return 0
	}
	return int(binary.LittleEndian.Uint16(t.Raw[6:8]))
}

func (d *Document) InsertLineHeight(c Cursor, prior, height int) (EditResult, error) {
	if prior < 0 || prior > 12000 || height < 0 || height > 12000 {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	raw := []byte{0xd0, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0xd0}
	binary.LittleEndian.PutUint16(raw[4:6], uint16(prior))
	binary.LittleEndian.PutUint16(raw[6:8], uint16(height))
	return d.editTokens(c, raw)
}

func ValidLineMargins(left, right int) bool {
	return left >= 0 && right >= 0 && left <= 8*UnitsPerInch && right <= 8*UnitsPerInch &&
		left+right <= 8*UnitsPerInch
}

func (t Token) LineMargins() (left, right int, ok bool) {
	if t.Kind != LineMargins {
		return 0, 0, false
	}
	return t.marginValues()
}

func (t Token) PageMargins() (top, bottom int, ok bool) {
	if t.Kind != PageMargins {
		return 0, 0, false
	}
	return t.marginValues()
}

func (t Token) marginValues() (first, second int, ok bool) {
	if marginKind(t.Raw) != t.Kind {
		return 0, 0, false
	}
	return int(binary.LittleEndian.Uint16(t.Raw[8:10])), int(binary.LittleEndian.Uint16(t.Raw[10:12])), true
}

func marginKind(raw []byte) Kind {
	if len(raw) != 16 || raw[0] != 0xd0 || raw[2] != 12 || raw[3] != 0 ||
		raw[12] != 12 || raw[13] != 0 || raw[14] != raw[1] || raw[15] != 0xd0 {
		return Opaque
	}
	kind, valid := LineMargins, ValidLineMargins
	switch raw[1] {
	case 1:
	case 5:
		kind, valid = PageMargins, ValidPageMargins
	default:
		return Opaque
	}
	for _, i := range []int{4, 8} {
		if !valid(int(binary.LittleEndian.Uint16(raw[i:i+2])), int(binary.LittleEndian.Uint16(raw[i+2:i+4]))) {
			return Opaque
		}
	}
	return kind
}

func ValidPageMargins(top, bottom int) bool {
	// The Standard Printer formatter uses 200 WordPerfect units per row.
	return top >= 0 && bottom >= 0 && top <= 13000 && bottom <= 13000 && top+bottom <= 13000
}

func (d *Document) InsertPageMargins(c Cursor, oldTop, oldBottom, top, bottom int) (EditResult, error) {
	if !ValidPageMargins(oldTop, oldBottom) || !ValidPageMargins(top, bottom) {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	return d.editTokens(c, marginOwner(5, oldTop, oldBottom, top, bottom))
}

func (d *Document) InsertLineMargins(c Cursor, oldLeft, oldRight, left, right int, startLine bool) (EditResult, error) {
	if !ValidLineMargins(oldLeft, oldRight) || !ValidLineMargins(left, right) {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	owner := marginOwner(1, oldLeft, oldRight, left, right)
	if startLine {
		return d.insertNamedTokens(c, append([]byte{hardReturnByte}, owner...), 2)
	}
	return d.editTokens(c, owner)
}

func marginOwner(function byte, first, second, newFirst, newSecond int) []byte {
	owner := []byte{0xd0, function, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, function, 0xd0}
	for i, value := range []int{first, second, newFirst, newSecond} {
		binary.LittleEndian.PutUint16(owner[4+i*2:], uint16(value))
	}
	return owner
}

func marginLabel(kind Kind, raw []byte) string {
	first, second, _ := (Token{Kind: kind, Raw: raw}).marginValues()
	inches := func(value int) string {
		return strconv.FormatFloat(float64(value)/UnitsPerInch, 'f', -1, 64)
	}
	axes := "L/R"
	if kind == PageMargins {
		axes = "T/B"
	}
	return fmt.Sprintf("[%s Mar:%s\",%s\"]", axes, inches(first), inches(second))
}
