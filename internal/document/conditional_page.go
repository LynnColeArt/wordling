package document

import "errors"

func conditionalPageKind(raw []byte) bool {
	return len(raw) == 9 && raw[0] == 0xd9 && raw[1] == 1 && raw[2] == 5 &&
		raw[3] == 0 && raw[4] > 0 && raw[5] == 5 && raw[6] == 0 && raw[7] == 1 && raw[8] == 0xd9
}

func (t Token) ConditionalLines() int {
	if t.Kind == ConditionalPage && conditionalPageKind(t.Raw) {
		return int(t.Raw[4])
	}
	return 0
}

func (d *Document) InsertConditionalPage(c Cursor, lines int) (EditResult, error) {
	if lines < 1 || lines > 255 {
		return EditResult{}, errors.New("enter a line count from 1 to 255")
	}
	return d.editTokens(c, []byte{0xd9, 1, 5, 0, byte(lines), 5, 0, 1, 0xd9})
}

func (d *Document) SetWidowProtection(c Cursor, enabled bool) (EditResult, error) {
	code := byte(0x8b)
	if enabled {
		code = 0x8a
	}
	return d.editTokens(c, []byte{code})
}
