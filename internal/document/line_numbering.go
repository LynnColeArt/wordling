package document

import "bytes"

func lineNumberOwner(enabled bool) []byte {
	raw := []byte{0xd3, 5, 14, 0, 0x21, 0xd0, 2, 1, 0, 0x21, 0xd0, 2, 1, 0, 14, 0, 5, 0xd3}
	if enabled {
		raw[9] = 0xa1
	}
	return raw
}

func lineNumberKind(raw []byte) bool {
	return len(raw) == 18 && raw[0] == 0xd3 && raw[1] == 5 && bytes.Equal(raw, lineNumberOwner(raw[9] == 0xa1))
}

func (t Token) EnablesLineNumbering() bool {
	return t.Kind == LineNumbering && len(t.Raw) == 18 && t.Raw[9] == 0xa1
}

func (d *Document) SetLineNumbering(c Cursor, enabled bool) (EditResult, error) {
	return d.editTokens(c, lineNumberOwner(enabled))
}
