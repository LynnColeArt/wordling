package document

import (
	"encoding/binary"
	"slices"
	"strings"
)

// D4/04 stores nondisplayable cell text. DOS may nest records after
// successive edits. The toolkit permits a zero hash on write.
const maxTableHiddenText = 2000

func decodeTableOverflow(raw []byte) ([]string, bool) {
	var parts []string
	total := 0
	for len(raw) != 0 {
		if len(raw) < 11 || raw[0] != 0xd4 || raw[1] != 4 ||
			int(binary.LittleEndian.Uint16(raw[2:])) != len(raw)-4 ||
			raw[len(raw)-2] != 4 || raw[len(raw)-1] != 0xd4 ||
			binary.LittleEndian.Uint16(raw[2:]) != binary.LittleEndian.Uint16(raw[len(raw)-4:]) {
			return nil, false
		}
		payload := raw[6 : len(raw)-4]
		i := 0
		for i < len(payload) && payload[i] != 0xd4 {
			b := payload[i]
			if b == 0xc0 && i+4 <= len(payload) && identify(payload[i:i+4]) == ExtendedCharacter {
				i += 4
				continue
			}
			if b != hardReturnByte && (b < 32 || b > 126) {
				return nil, false
			}
			i++
		}
		if i == 0 || total+i > maxTableHiddenText {
			return nil, false
		}
		parts = append(parts, string(payload[:i]))
		total += i
		raw = payload[i:]
	}
	return parts, total != 0
}

func encodeTableOverflow(cell TableCell) []byte {
	if cell.Hidden == "" {
		return nil
	}
	parts := cell.overflow
	if len(parts) == 0 {
		parts = []string{cell.Hidden}
		if strings.Trim(cell.Hidden, "\n") == "" {
			parts = make([]string, len(cell.Hidden))
			for i := range parts {
				parts[i] = "\n"
			}
		}
	}
	record := make([]byte, len(cell.Hidden)+10*len(parts))
	start, end := 0, len(record)
	for _, part := range parts {
		writeTableOverflow(record[start:end], part)
		start, end = start+6+len(part), end-4
	}
	return record
}

// spillTableLine moves the last word or the overlong run out of the
// visible line. In either case the break itself is hidden with the text.
func spillTableLine(line []rune) int {
	if space := lastTableSpace(line[1:]); space >= 0 {
		return space + 1
	}
	return len(line) - 1
}

func (cell *TableCell) setOverflow(parts []string) {
	cell.overflow = parts
	cell.Hidden = strings.Join(parts, "")
}

func writeTableOverflow(record []byte, text string) {
	record[0], record[1] = 0xd4, 4
	copy(record[6:], text)
	end := len(record)
	record[end-2], record[end-1] = 4, 0xd4
	size := uint16(end - 4)
	binary.LittleEndian.PutUint16(record[2:], size)
	binary.LittleEndian.PutUint16(record[end-4:], size)
}

const tableVisibleBreaks = 52

func editTableText(cell TableCell, logical []rune, first, last int, text []rune, width int) (TableCell, int, bool) {
	atEnd := first == last && last == len(logical)
	if atEnd && len(text) != 0 && !slices.Contains(text, '\n') &&
		strings.Count(cell.DisplayText(), "\n") == tableVisibleBreaks {
		// DOS allows the cursor in the last column. It wraps on the
		// following keystroke and returns the cursor to the visible prefix.
		for i := range len(text) {
			owners := tableOwners(cell.Text)
			lineStart := tableLineStart(owners)
			line := owners[lineStart:]
			if len(line) < width {
				if len(line) < width-1 && len(cell.overflow) > 1 && cell.Hidden[0] != hardReturnByte {
					cell.setOverflow([]string{cell.Hidden})
				}
				cell.Text += tableBytes(text[i : i+1])
				continue
			}
			cut := spillTableLine(line)
			cell.setOverflow(append([]string{tableBytes(line[cut:]) + tableBytes(text[i:i+1])}, cell.overflow...))
			cell.Text = tableBytes(owners[:lineStart+cut])
		}
		return cell, len(tableOwners(cell.Text)), len(cell.Hidden) <= maxTableHiddenText
	}

	edited := append(append(append([]rune(nil), logical[:first]...), text...), logical[last:]...)
	wrapped, position := wrapTableText(edited, width-1, first+len(text))
	visible, tail, breaks := splitTableOverflow(wrapped, tableVisibleBreaks)
	if tail != "" {
		if !atEnd {
			return cell, 0, false
		}
		cell.setOverflow(append([]string{tail}, cell.overflow...))
		wrapped = visible
	} else if breaks < tableVisibleBreaks && cell.Hidden != "" {
		reflow, _ := wrapTableText(append(edited, tableOwners(cell.Hidden)...), width-1, first+len(text))
		wrapped, tail, _ = splitTableOverflow(reflow, tableVisibleBreaks)
		var parts []string
		for strings.HasPrefix(tail, "\n") {
			parts = append(parts, "\n")
			tail = tail[1:]
		}
		if tail != "" {
			parts = append(parts, tail)
		}
		cell.setOverflow(parts)
	}
	cell.Text = tableBytes(wrapped)
	return cell, min(position, len(wrapped)), len(cell.Hidden) <= maxTableHiddenText
}

// FinalizeTableOverflow applies DOS's save-time wrap to a character still
// occupying the last column. It leaves the live cursor and revision untouched.
func (d *Document) FinalizeTableOverflow() (*Document, error) {
	table, ok := d.SimpleTable()
	if !ok {
		return d, nil
	}
	changed := false
	for i, cell := range table.Cells {
		if strings.Count(cell.DisplayText(), "\n") != tableVisibleBreaks {
			continue
		}
		width := table.Widths[i%len(table.Widths)]
		owners := tableOwners(cell.Text)
		lineStart := tableLineStart(owners)
		line := owners[lineStart:]
		if len(line) != width {
			continue
		}
		cut := spillTableLine(line)
		parts := append([]string(nil), cell.overflow...)
		if len(parts) == 0 {
			parts = []string{tableBytes(line[cut:])}
		} else {
			parts[0] = tableBytes(line[cut:]) + parts[0]
		}
		cell.setOverflow(parts)
		cell.Text = tableBytes(owners[:lineStart+cut])
		table.Cells[i] = cell
		changed = true
	}
	if !changed {
		return d, nil
	}
	body, ok := tableProfiles[len(table.Widths)].body(table.Cells)
	if !ok {
		return nil, failure(UnsupportedBody, -1, noSpan)
	}
	raw := d.state.image.Export()
	return parseRevision(append(raw[:d.state.gaps[0]], body...), d.state.birth)
}

func tableLineStart(owners []rune) int {
	for i := len(owners) - 1; i >= 0; i-- {
		switch owners[i] {
		case hardReturnByte, softReturnByte, deletedSoftReturn:
			return i + 1
		}
	}
	return 0
}
