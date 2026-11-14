package document

import (
	"encoding/binary"
	"fmt"
	"strconv"
	"strings"
)

func embeddedPrinterCommand(raw []byte) ([]byte, bool) {
	if len(raw) < 10 || len(raw) > 264 || raw[0] != 0xd9 || raw[1] != 0 || raw[4] != 0 || raw[len(raw)-1] != 0xd9 {
		return nil, false
	}
	stop := len(raw) - 4
	return raw[5:stop], int(binary.LittleEndian.Uint16(raw[2:4])) == stop && sameRecordTrailer(raw, stop)
}

func isPrinterCommand(raw []byte) bool {
	_, ok := embeddedPrinterCommand(raw)
	return ok
}

func (t Token) PrinterBytes() []byte {
	if t.Kind != PrinterCommand {
		return nil
	}
	data, _ := embeddedPrinterCommand(t.Raw)
	return data
}

func printerCommandLabel(raw []byte) string {
	data, _ := embeddedPrinterCommand(raw)
	var text strings.Builder
	for _, b := range data {
		if b < 32 || b > 126 {
			fmt.Fprintf(&text, "<%d>", b)
		} else {
			text.WriteByte(b)
		}
	}
	return "[Ptr Cmnd:" + text.String() + "]"
}

func (d *Document) InsertPrinterCommand(c Cursor, text string) (EditResult, error) {
	var data []byte
	for pos := 0; pos < len(text); pos++ {
		b := text[pos]
		if b == '<' {
			end := strings.IndexByte(text[pos+1:], '>')
			if end < 1 || end > 3 {
				return unchangedEdit(d, c), fmt.Errorf("enter printer byte values in angle brackets, such as <27>")
			}
			digits := text[pos+1 : pos+1+end]
			value, err := strconv.Atoi(digits)
			if err != nil || value < 0 || value > 255 || strings.Trim(digits, "0123456789") != "" {
				return unchangedEdit(d, c), fmt.Errorf("printer byte values must be between 0 and 255")
			}
			b = byte(value)
			pos += end + 1
		} else if b < 32 || b > 126 {
			return unchangedEdit(d, c), fmt.Errorf("use printable ASCII or an angle-bracket byte value")
		}
		data = append(data, b)
	}
	if len(data) == 0 || len(data) > 255 {
		return unchangedEdit(d, c), fmt.Errorf("enter 1 to 255 printer bytes")
	}
	raw := append([]byte{0xd9, 0, 0, 0, 0}, data...)
	n := len(raw)
	binary.LittleEndian.PutUint16(raw[2:4], uint16(n))
	return d.editTokens(c, append(raw, byte(n), byte(n>>8), 0, 0xd9))
}
