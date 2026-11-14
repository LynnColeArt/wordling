package document

import (
	"encoding/binary"
	"fmt"
)

func commentText(raw []byte) (string, bool) {
	if len(raw) < 12 || len(raw) > 1035 || raw[0] != 0xd9 || raw[1] != 2 || raw[4] != 10 || raw[5] != 0 || raw[6] != 1 {
		return "", false
	}
	stop := len(raw) - 4
	if int(binary.LittleEndian.Uint16(raw[2:4])) != stop || !sameRecordTrailer(raw, stop) || raw[len(raw)-1] != 0xd9 {
		return "", false
	}
	text := raw[7:stop]
	for _, b := range text {
		if b < 32 || b > 126 {
			return "", false
		}
	}
	return string(text), true
}

func (t Token) Comment() (string, bool) {
	if t.Kind != Comment {
		return "", false
	}
	return commentText(t.Raw)
}

func (d *Document) InsertComment(c Cursor, text string) (EditResult, error) {
	if len(text) == 0 || len(text) > 1024 {
		return unchangedEdit(d, c), fmt.Errorf("enter 1 to 1024 characters for the comment")
	}
	raw := append([]byte{0xd9, 2, 0, 0, 10, 0, 1}, text...)
	length := len(raw)
	binary.LittleEndian.PutUint16(raw[2:4], uint16(length))
	return d.editTokens(c, append(raw, byte(length), byte(length>>8), 2, 0xd9))
}
