package document

import "encoding/binary"

// The D4/04 record holds text DOS cannot display in a cell. The toolkit
// permits a zero hash on write. Read the original hashes without interpreting
// them. DOS nests these records when another Enter is pressed at the limit.
const maxTableHiddenReturns = 100

func decodeTableOverflow(raw []byte) (string, bool) {
	count := 0
	for len(raw) != 0 {
		if count == maxTableHiddenReturns || len(raw) < 11 || raw[0] != 0xd4 || raw[1] != 4 ||
			int(binary.LittleEndian.Uint16(raw[2:])) != len(raw)-4 ||
			raw[6] != hardReturnByte || raw[len(raw)-2] != 4 || raw[len(raw)-1] != 0xd4 ||
			binary.LittleEndian.Uint16(raw[2:]) != binary.LittleEndian.Uint16(raw[len(raw)-4:]) {
			return "", false
		}
		count++
		raw = raw[7 : len(raw)-4]
	}
	text := make([]byte, count)
	for i := range text {
		text[i] = hardReturnByte
	}
	return string(text), count != 0
}

func encodeTableOverflow(text string) []byte {
	if text == "" {
		return nil
	}
	record := make([]byte, 11*len(text))
	for start, end := 0, len(record); start < end; start, end = start+7, end-4 {
		record[start], record[start+1] = 0xd4, 4
		record[start+6] = hardReturnByte
		record[end-2], record[end-1] = 4, 0xd4
		size := uint16(end - start - 4)
		binary.LittleEndian.PutUint16(record[start+2:], size)
		binary.LittleEndian.PutUint16(record[end-4:], size)
	}
	return record
}
