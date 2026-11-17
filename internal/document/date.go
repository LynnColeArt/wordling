package document

import (
	"bytes"
	"time"
)

const defaultDateFormat = "3 1, 4"

func dateCodeOwner() []byte {
	raw := make([]byte, 72)
	copy(raw, []byte{0xd8, 0, 68, 0})
	copy(raw[4:], defaultDateFormat)
	copy(raw[68:], []byte{68, 0, 0, 0xd8})
	return raw
}

func dateCodeKind(raw []byte) bool {
	return len(raw) == 72 && raw[0] == 0xd8 && bytes.Equal(raw, dateCodeOwner())
}

func (d *Document) InsertDateCode(c Cursor) (EditResult, error) {
	return d.editTokens(c, dateCodeOwner())
}

func FormatDate(now time.Time) string { return now.Format("January 2, 2006") }
