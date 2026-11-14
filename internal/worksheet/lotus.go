// Package worksheet reads the original Lotus 1-2-3 record format.
package worksheet

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"strconv"
	"strings"
)

type Range struct {
	Left, Top, Right, Bottom uint16
}

type Cell struct {
	Text    string
	Integer bool
}

func columnName(column uint16) string {
	s := ""
	for n := int(column) + 1; n > 0; n = (n - 1) / 26 {
		s = string(rune('A'+(n-1)%26)) + s
	}
	return s
}

func (r Range) String() string {
	return fmt.Sprintf("%s%d..%s%d", columnName(r.Left), int(r.Top)+1, columnName(r.Right), int(r.Bottom)+1)
}

func ParseRange(text string) (Range, error) {
	bad := fmt.Errorf("enter a worksheet range such as A1..B2")
	parts := strings.Split(strings.NewReplacer("..", ":", ".", ":").Replace(strings.ToUpper(strings.TrimSpace(text))), ":")
	if len(parts) != 2 {
		return Range{}, bad
	}
	address := func(s string) (uint16, uint16, bool) {
		n, col := 0, 0
		for n < len(s) && s[n] >= 'A' && s[n] <= 'Z' {
			col = col*26 + int(s[n]-'A'+1)
			if col > 256 {
				return 0, 0, false
			}
			n++
		}
		if n == 0 || n == len(s) || strings.Trim(s[n:], "0123456789") != "" {
			return 0, 0, false
		}
		row, err := strconv.Atoi(s[n:])
		return uint16(col - 1), uint16(row - 1), err == nil && row >= 1 && row <= 8192
	}
	l, t, ok := address(parts[0])
	r, b, ok2 := address(parts[1])
	if !ok || !ok2 || l > r || t > b {
		return Range{}, bad
	}
	return Range{l, t, r, b}, nil
}

// ReadWK1 extracts two columns from the US WK1 label and integer profile.
// Unknown records outside the selected range do not affect the result.
func ReadWK1(raw []byte, r Range) ([]Cell, error) {
	if r.Right <= r.Left || r.Right-r.Left != 1 || r.Bottom <= r.Top || r.Bottom-r.Top != 1 || r.Right > 255 || r.Bottom >= 8192 {
		return nil, fmt.Errorf("select a two-by-two worksheet range")
	}
	if len(raw) < 10 || !bytes.Equal(raw[:6], []byte{0, 0, 2, 0, 6, 4}) {
		return nil, fmt.Errorf("incompatible worksheet: expected Lotus WK1")
	}
	cells := make([]Cell, 2*(int(r.Bottom-r.Top)+1))
	seen := make([]bool, len(cells))
	for raw = raw[6:]; len(raw) >= 4; {
		kind, size := binary.LittleEndian.Uint16(raw), int(binary.LittleEndian.Uint16(raw[2:]))
		raw = raw[4:]
		if size > len(raw) {
			break
		}
		data := raw[:size]
		raw = raw[size:]
		if kind == 1 && size == 0 && len(raw) == 0 {
			return cells, nil
		}
		switch kind {
		case 12, 13, 14, 15, 16:
		default:
			continue
		}
		if len(data) < 5 {
			break
		}
		col, row := binary.LittleEndian.Uint16(data[1:]), binary.LittleEndian.Uint16(data[3:])
		if col < r.Left || col > r.Right || row < r.Top || row > r.Bottom {
			continue
		}
		i := int(row-r.Top)*2 + int(col-r.Left)
		if seen[i] {
			return nil, fmt.Errorf("duplicate worksheet cell %s%d", columnName(col), row+1)
		}
		seen[i] = true
		if data[0] != 0xff {
			return nil, fmt.Errorf("worksheet cell %s%d has unsupported formatting", columnName(col), row+1)
		}
		switch {
		case kind == 12 && len(data) == 5:
		case kind == 13 && len(data) == 7:
			cells[i] = Cell{Text: strconv.Itoa(int(int16(binary.LittleEndian.Uint16(data[5:])))), Integer: true}
		case kind == 15 && len(data) >= 7 && data[5] == '\'' && data[len(data)-1] == 0:
			label := data[6 : len(data)-1]
			for _, b := range label {
				if b < 32 || b > 126 {
					return nil, fmt.Errorf("worksheet labels require printable ASCII")
				}
			}
			cells[i] = Cell{Text: string(label)}
		default:
			return nil, fmt.Errorf("worksheet cell %s%d has an unsupported value or alignment", columnName(col), row+1)
		}
	}
	return nil, fmt.Errorf("worksheet record stream is incomplete")
}
