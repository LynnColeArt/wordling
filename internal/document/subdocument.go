package document

import (
	"encoding/binary"
	"fmt"
	"strings"
)

func subdocumentName(raw []byte) (string, bool) {
	if len(raw) < 13 || len(raw) > 139 || raw[0] != 0xd7 || raw[1] != 9 || raw[6] != 1 {
		return "", false
	}
	stop := len(raw) - 4
	if int(binary.LittleEndian.Uint16(raw[2:4])) != stop || !sameRecordTrailer(raw, stop) || raw[stop-1] != 0 || raw[len(raw)-1] != 0xd7 {
		return "", false
	}
	name := string(raw[7 : stop-1])
	return name, validSubdocumentName(name)
}

func validSubdocumentName(name string) bool {
	return len(name) > 0 && len(name) <= 127 && strings.TrimSpace(name) == name &&
		strings.IndexFunc(name, func(ch rune) bool { return ch < 32 || ch > 126 }) < 0
}

func isSubdocument(raw []byte) bool {
	_, ok := subdocumentName(raw)
	return ok
}

func (t Token) Subdocument() (string, bool) {
	if t.Kind != Subdocument {
		return "", false
	}
	return subdocumentName(t.Raw)
}

func (d *Document) InsertSubdocument(c Cursor, name string, column int) (EditResult, error) {
	if !validSubdocumentName(name) {
		return unchangedEdit(d, c), fmt.Errorf("enter a DOS subdocument filename")
	}
	if column < 0 || column > 0xffff {
		return unchangedEdit(d, c), failure(InvalidPosition, c.gap, noSpan)
	}
	raw := []byte{0xd7, 9, 0, 0, byte(column), byte(column >> 8), 1}
	raw = append(raw, strings.ToUpper(name)...)
	raw = append(raw, 0)
	n := len(raw)
	binary.LittleEndian.PutUint16(raw[2:4], uint16(n))
	return d.editTokens(c, append(raw, byte(n), byte(n>>8), 9, 0xd7))
}
