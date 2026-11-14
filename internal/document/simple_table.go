package document

import (
	"bytes"
	"encoding/binary"
	"encoding/hex"
	"strings"
)

// SimpleTable describes the default standalone Letter table.
type TableCell struct {
	Start, End  int
	Text        string
	Hidden      string
	overflow    []string
	formula     *tableFormula
	joined      bool
	joinedRight string
}

type SimpleTable struct {
	Cells      []TableCell
	Widths     []int
	PageStarts []int
}

type tableProfile struct {
	widths                                        []int
	header, first, middle, later, last, cell, end string
}

var tableProfiles = map[int]tableProfile{
	2: {widths: []int{31, 31},
		header: "d20b4f00000a03000100000064006400780000000000000000000000000000000000000000000000000000000a02002100b004640064007800000000000000010000003c0f3c0f00000000202000004f000bd2",
		first:  "dc0116000370018412000a100370018412000a100000160001dc",
		middle: "dc0116000370018412000a1003500184110009100000160001dc",
		later:  "dc0116000370018412000a1003500184110009100000160001dc",
		last:   "dc011600035001841100091003800184110209127001160001dc",
		cell:   "dc000f0000000101000000000000200f0000dc",
		end:    "dc02130003800184110209120200c002000002130002dc",
	},
	3: {widths: []int{20, 21, 20},
		header: "d20b5400000a03000100000064006400780000000000000000000000000000000000000000000000000000000a03002100b00464006400780000000000000001000000280a280a280a000000000000202020000054000bd2",
		first:  "dc011a000370018612000a000a100370018612000a000a1000001a0001dc",
		middle: "dc011a000370018612000a000a100350018611000900091000001a0001dc",
		later:  "dc011a000370018612000a000a100350018611000900091000001a0001dc",
		last:   "dc011a00035001861100090009100380018611020902091270011a0001dc",
		cell:   "dc000f0000000101000000000000200f0000dc",
		end:    "dc021500038001861102090209120200c002000003150002dc",
	},
	4: {widths: []int{15, 15, 15, 15},
		header: "d20b5900000a03000100000064006400780000000000000000000000000000000000000000000000000000000a04002100b004640064007800000000000000010000009e079e079e079e07000000000000000020202020000059000bd2",
		first:  "dc011e0003700188120002800a000a1003700188120002800a000a1000001e0001dc",
		middle: "dc011e0003700188120002800a000a1003500188110002800900091000001e0001dc",
		later:  "dc011e0003500188110002800900091003500188110002800900091070011e0001dc",
		last:   "dc011e00035001881100028009000910038001881102028009020912c0021e0001dc",
		cell:   "dc000f0000000101000000000000200f0000dc",
		end:    "dc02170003800188110202800902091203001004000004170002dc",
	},
}

const MaxTableRows = 128

const tablePageHeight = 10800

// WordPerfect 5.1 paginates at row boundaries.
const TableRowTooTall Category = "TableRowTooTall"

func tableRowBaseHeight(row, rows int) int {
	switch row {
	case 0:
		return 368
	case rows - 1:
		return 384
	default:
		return 336
	}
}

var tableEndPages = []byte{0xd4, 3, 6, 0, 1, 0, 6, 0, 3, 0xd4}

func tableOwner(encoded string) []byte {
	raw, _ := hex.DecodeString(encoded)
	return raw
}

// encode regenerates the default row height and position caches from the
// tallest preceding cell in each row and the tallest cell in each row.
func (p tableProfile) encode(cells []TableCell) ([][]byte, bool) {
	columns := len(p.widths)
	rows := len(cells) / columns
	joined := (SimpleTable{Widths: p.widths, Cells: cells}).joinedRow()
	owners := [][]byte{tableOwner(p.header)}
	rowStart, priorHeight, priorStart := 0, 0, 0
	page := uint16(1)
	overflowEndPosition := 0
	priorOverflow, hadOverflow := false, false
	for row := range rows {
		encoded := p.middle
		height := tableRowBaseHeight(row, rows)
		switch {
		case row == 0:
			encoded = p.first
		case row == rows-1:
			encoded = p.last
		case row >= 2:
			encoded = p.later
		}
		owner := tableOwner(encoded)
		binary.LittleEndian.PutUint16(owner[5:], uint16(priorHeight))
		if row == 0 {
			binary.LittleEndian.PutUint16(owner[5:], 368)
		}
		if row > 0 {
			predecessor := tableOwner(p.middle)
			if row == 1 {
				predecessor = tableOwner(p.first)
			}
			second := 12 + 2*(columns-2)
			copy(owner[7:second], predecessor[second+3:second+3+second-7])
		}
		binary.LittleEndian.PutUint16(owner[len(owner)-6:], uint16(priorStart))
		cellCacheOffset := 0
		if hadOverflow && row == 2 && rows == 3 && !priorOverflow && priorStart == 0 && rowStart == 336 {
			// DOS keeps the prior start from its provisional layout.
			binary.LittleEndian.PutUint16(owner[len(owner)-6:], 4368)
			cellCacheOffset = 4368
		}
		baseHeight := height
		for column := range columns {
			height = max(height, baseHeight+200*(len(cells[row*columns+column].Lines())-1))
		}
		overflow := false
		for column := range columns {
			overflow = overflow || cells[row*columns+column].Hidden != ""
		}
		hadOverflow = hadOverflow || overflow
		if overflow {
			overflowEndPosition = 4304
			if row == 0 && rows == 2 {
				overflowEndPosition = 4368
			}
		}
		if overflow && height != baseHeight+52*200 {
			return nil, false
		}
		if row == 0 && overflow {
			binary.LittleEndian.PutUint16(owner[5:], uint16(height-200))
		}
		if rowStart+height > tablePageHeight {
			if rowStart == 0 || height > tablePageHeight {
				return nil, false
			}
			pageRecord := everydayPageRecord(page, 0)
			binary.LittleEndian.PutUint16(pageRecord[6:], uint16(rowStart-200))
			if priorOverflow {
				y := 136
				if row == 1 {
					y = 168
					if cells[columns-1].Hidden != "" {
						y = rowStart - 200
					}
				}
				binary.LittleEndian.PutUint16(pageRecord[6:], uint16(y))
			} else if overflow {
				pageRecord[14] = 1
				if row == rows-1 && row > 1 {
					pageRecord[17] = 1
				}
			}
			owners = append(owners, pageRecord)
			owner[0], owner[len(owner)-1] = 0xdd, 0xdd
			page++
			priorStart = 0
			rowStart = 0
		}
		if joined {
			if row == 0 {
				owner[10], owner[18] = 2, 2
			} else if row == 1 {
				owner[10] = 2
			}
		}
		maxExtra := 0
		cellOwners := make([][]byte, 0, columns)
		for column := range columns {
			cell := cells[row*columns+column]
			if cell.Covered() {
				if !joined || row != 0 || column != 1 {
					return nil, false
				}
				continue
			}
			raw := tableOwner(p.cell)
			if cell.joined {
				if !joined || row != 0 || column != 0 || !simpleJoinText(cell.Text) || !simpleJoinText(cell.joinedRight) ||
					len(cell.joinedRight) > p.widths[1] || cell.Hidden != "" || cell.formula != nil {
					return nil, false
				}
				raw[6] = 2
			}
			raw[5] = byte(column)
			if column > 0 {
				raw[7] = 1
				binary.LittleEndian.PutUint16(raw[8:], uint16(rowStart+baseHeight+200*maxExtra)+uint16(cellCacheOffset))
				raw[10] = byte(maxExtra)
			}
			if len(cell.Text) > 2000 {
				return nil, false
			}
			lines := cell.Lines()
			for _, line := range lines {
				if len([]rune(line)) > p.widths[column] {
					return nil, false
				}
			}
			maxExtra = max(maxExtra, len(lines)-1)
			if cell.formula != nil {
				raw = cell.formula.attach(raw)
			}
			cellOwners = append(cellOwners, raw)
		}
		binary.LittleEndian.PutUint16(owner[13+2*(columns-2):], uint16(height))
		owners = append(owners, owner)
		owners = append(owners, cellOwners...)
		priorStart, rowStart = rowStart, rowStart+height
		priorHeight, priorOverflow = height, overflow
	}
	end := tableOwner(p.end)
	binary.LittleEndian.PutUint16(end[5:], uint16(priorHeight))
	i := 12 + 2*(columns-2)
	binary.LittleEndian.PutUint16(end[i:], uint16(rows-1))
	binary.LittleEndian.PutUint16(end[i+2:], uint16(priorStart))
	if priorOverflow {
		record := everydayPageRecord(page, 0)
		binary.LittleEndian.PutUint16(record[6:], 136)
		owners = append(owners, record)
		end[0], end[len(end)-1] = 0xdd, 0xdd
		clear(end[i+2 : i+6])
	} else if hadOverflow {
		binary.LittleEndian.PutUint16(end[i+2:], uint16(overflowEndPosition))
	}
	owners = append(owners, end)
	if page > 1 && !hadOverflow {
		owners = append(owners, tableEndPages)
	}
	return owners, true
}

func (d *Document) SimpleTable() (SimpleTable, bool) {
	if !d.valid() {
		return SimpleTable{}, false
	}
	header, err := d.Token(0)
	if err != nil || header.Kind != Opaque || len(header.Raw) < 46 || header.Raw[0] != 0xd2 || header.Raw[1] != 0x0b {
		return SimpleTable{}, false
	}
	p, ok := tableProfiles[int(header.Raw[45])]
	if !ok || !bytes.Equal(header.Raw, tableOwner(p.header)) {
		return SimpleTable{}, false
	}
	table := SimpleTable{Widths: append([]int(nil), p.widths...)}
	owners := [][]byte{header.Raw}
	gap := 1
	for gap < d.TokenCount() && len(table.Cells) < MaxTableRows*len(p.widths) {
		row, _ := d.Token(gap)
		if len(row.Raw) == 32 && row.Raw[0] == 0xd4 && row.Raw[1] == 0 {
			owners = append(owners, row.Raw)
			gap++
			row, _ = d.Token(gap)
			if len(row.Raw) >= 2 && row.Raw[1] == 1 {
				table.PageStarts = append(table.PageStarts, len(table.Cells))
			}
		}
		if len(row.Raw) < 2 || (row.Raw[0] != 0xdc && row.Raw[0] != 0xdd) || row.Raw[1] != 1 {
			break
		}
		owners = append(owners, row.Raw)
		gap++
		for column := range p.widths {
			if column == 1 && len(table.Cells) == 1 && table.Cells[0].joined {
				table.Cells = append(table.Cells, TableCell{Start: -1, End: -1})
				continue
			}
			cell, err := d.Token(gap)
			if err != nil || len(cell.Raw) < 19 || cell.Raw[0] != 0xdc || cell.Raw[1] != 0 {
				return SimpleTable{}, false
			}
			formula, ok := tableFormulaRecord(cell.Raw)
			if !ok {
				return SimpleTable{}, false
			}
			owners = append(owners, cell.Raw)
			gap++
			start := gap
			var content strings.Builder
		contentTokens:
			for gap < d.TokenCount() {
				token, _ := d.Token(gap)
				switch token.Kind {
				case ASCII, ExtendedCharacter, HardReturn, SoftReturn, DeletedSoftReturn:
					content.Write(token.Raw)
				default:
					break contentTokens
				}
				if content.Len() > 2000 {
					return SimpleTable{}, false
				}
				gap++
			}
			parsed := TableCell{Start: start, End: gap, Text: content.String(), formula: formula}
			if cell.Raw[6] == 2 {
				if len(table.Cells) != 0 || column != 0 || len(p.widths) != 2 {
					return SimpleTable{}, false
				}
				tab, err := d.Token(gap)
				if err != nil || !bytes.Equal(tab.Raw, joinedCellTab) {
					return SimpleTable{}, false
				}
				parsed.joined = true
				gap++
				var right strings.Builder
				for gap < d.TokenCount() && right.Len() <= p.widths[1] {
					char, _ := d.Token(gap)
					if char.Kind != ASCII {
						break
					}
					right.Write(char.Raw)
					gap++
				}
				parsed.joinedRight = right.String()
			}
			if hidden, err := d.Token(gap); err == nil && len(hidden.Raw) >= 2 && hidden.Raw[0] == 0xd4 && hidden.Raw[1] == 4 {
				if strings.Count(parsed.DisplayText(), "\n") != 52 {
					return SimpleTable{}, false
				}
				parts, ok := decodeTableOverflow(hidden.Raw)
				if !ok {
					return SimpleTable{}, false
				}
				parsed.setOverflow(parts)
				gap++
			}
			table.Cells = append(table.Cells, parsed)
		}
	}
	if gap >= d.TokenCount() || len(table.Cells) < 2*len(p.widths) {
		return SimpleTable{}, false
	}
	end, _ := d.Token(gap)
	owners = append(owners, end.Raw)
	gap++
	if extra, err := d.Token(gap); err == nil && bytes.Equal(extra.Raw, tableEndPages) {
		owners = append(owners, extra.Raw)
		gap++
	}
	if gap != d.TokenCount() {
		return SimpleTable{}, false
	}
	expected, ok := p.encode(table.Cells)
	if !ok || len(expected) != len(owners) {
		return SimpleTable{}, false
	}
	// DOS can refresh the first row's leading height when saving an edit.
	if len(owners[1]) == len(expected[1]) && bytes.Equal(owners[1][5:7], expected[1][13+2*(len(p.widths)-2):15+2*(len(p.widths)-2)]) {
		copy(expected[1][5:7], owners[1][5:7])
	}
	for i, raw := range owners {
		if !bytes.Equal(raw, expected[i]) {
			return SimpleTable{}, false
		}
	}
	return table, true
}

func (p tableProfile) body(cells []TableCell) ([]byte, bool) {
	owners, ok := p.encode(cells)
	if !ok {
		return nil, false
	}
	var body []byte
	index := 0
	for _, owner := range owners {
		body = append(body, owner...)
		if owner[0] == 0xdc && owner[1] == 0 {
			body = append(body, cells[index].Text...)
			if cells[index].joined {
				body = append(body, joinedCellTab...)
				body = append(body, cells[index].joinedRight...)
				index++ // The next logical cell is covered by this native owner.
			}
			body = append(body, encodeTableOverflow(cells[index])...)
			index++
		}
	}
	return body, true
}

func (t SimpleTable) CellAt(gap int) (int, bool) {
	for i, cell := range t.Cells {
		if gap >= cell.Start && gap <= cell.End {
			return i, true
		}
	}
	return 0, false
}

// EditTableCell replaces text inside one cell and updates the row caches.
func (d *Document) EditTableCell(c Cursor, start, end int, text string) (EditResult, error) {
	for i := range len(text) {
		if text[i] != '\n' && (text[i] < 32 || text[i] > 126) {
			return unchangedEdit(d, c), failure(InvalidASCII, c.gap, noSpan)
		}
	}
	return d.editTableCell(c, start, end, []rune(text))
}

// WriteTableCharacter inserts or types over one complete native cell character.
func (d *Document) WriteTableCharacter(c Cursor, set, number byte, over bool) (EditResult, error) {
	raw := CharacterBytes(set, number)
	if len(raw) == 0 {
		return unchangedEdit(d, c), failure(InvalidASCII, c.gap, noSpan)
	}
	end := c.gap
	if over {
		table, _ := d.SimpleTable()
		if index, ok := table.CellAt(c.gap); ok && end < table.Cells[index].End {
			end++
		}
	}
	return d.editTableCell(c, c.gap, end, tableOwners(string(raw)))
}

func (d *Document) editTableCell(c Cursor, start, end int, text []rune) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	if !d.valid() || c.state != d.state {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	table, valid := d.SimpleTable()
	index, inside := table.CellAt(c.gap)
	if !valid || !inside {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	cell := table.Cells[index]
	if cell.formula != nil || cell.joined {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	if start < cell.Start || end < start || end > cell.End {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	if d.TokenCount()-(end-start)+len(text) > MaxMutationTokens ||
		int(d.state.gaps[d.TokenCount()])-int(d.state.gaps[end]-d.state.gaps[start])+len(tableBytes(text)) > MaxMutationBytes {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return unchanged, err
	}
	raw := d.state.image.Export()
	logical, first := logicalTableText(cell.Text, start-cell.Start)
	_, last := logicalTableText(cell.Text, end-cell.Start)
	if first == last && len(text) == 0 {
		// A deleted soft return has no character to remove.
		c.gap = start
		if start == unchanged.Cursor.gap {
			c.gap = end
		}
		return EditResult{Document: d, Cursor: c}, nil
	}
	width := table.Widths[index%len(table.Widths)]
	updatedCell, position, ok := editTableText(cell, logical, first, last, text, width)
	if !ok {
		return unchanged, failure(TableRowTooTall, start, noSpan)
	}
	if updatedCell.Text == cell.Text && updatedCell.Hidden == cell.Hidden {
		c.gap = cell.Start + position
		return EditResult{Document: d, Cursor: c}, nil
	}
	table.Cells[index] = updatedCell

	body, ok := tableProfiles[len(table.Widths)].body(table.Cells)
	if !ok {
		return unchanged, failure(UnsupportedBody, start, noSpan)
	}
	if len(body)+int(d.state.gaps[0]) > MaxMutationBytes {
		return unchanged, failure(MutationLimit, start, noSpan)
	}
	candidate := append(raw[:d.state.gaps[0]], body...)
	candidate[flags] |= 8
	next, err := parseRevision(candidate, d.state.birth)
	if err != nil {
		return unchanged, err
	}
	if next.TokenCount() > MaxMutationTokens {
		return unchanged, failure(MutationLimit, start, noSpan)
	}
	updated, ok := next.SimpleTable()
	if !ok {
		return unchanged, failure(UnsupportedBody, start, noSpan)
	}
	c.state, c.gap = next.state, updated.Cells[index].Start+position
	return EditResult{Document: next, Cursor: c, Changed: true}, nil
}

// CreateSimpleTable creates the default table in an empty document.
func (d *Document) CreateSimpleTable(c Cursor, columns, rows int) (EditResult, error) {
	if !d.valid() || c.state != d.state || d.TokenCount() != 0 || c.gap != 0 {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return unchangedEdit(d, c), err
	}
	raw := d.state.image.Export()
	raw[flags] |= 8
	profile, ok := tableProfiles[columns]
	if !ok || rows < 2 || rows > MaxTableRows {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	body, ok := profile.body(make([]TableCell, columns*rows))
	if !ok {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	raw = append(raw, body...)
	next, err := parseRevision(raw, d.state.birth)
	if err != nil {
		return unchangedEdit(d, c), err
	}
	c.state, c.gap = next.state, 3
	return EditResult{Document: next, Cursor: c, Changed: true}, nil
}

// tableOwners represents each native owner as one rune during layout.
// Extended identities occupy a private internal range and are decoded on write.
func tableOwners(raw string) []rune {
	owners := make([]rune, 0, len(raw))
	for len(raw) > 0 {
		if raw[0] == 0xc0 && len(raw) >= 4 {
			owners = append(owners, 0x10000+rune(raw[2])*256+rune(raw[1]))
			raw = raw[4:]
		} else {
			owners = append(owners, rune(raw[0]))
			raw = raw[1:]
		}
	}
	return owners
}

func tableBytes(owners []rune) string {
	var raw strings.Builder
	for _, owner := range owners {
		if owner >= 0x10000 {
			raw.Write(CharacterBytes(byte((owner-0x10000)/256), byte(owner)))
		} else {
			raw.WriteByte(byte(owner))
		}
	}
	return raw.String()
}

// DisplayText gives one screen glyph per native owner.
func (c TableCell) DisplayText() string { return c.display(false, -1) }

func (c TableCell) display(reveal bool, active int) string {
	var display strings.Builder
	for i, owner := range tableOwners(c.Text) {
		switch {
		case owner >= 0x10000:
			set, number := byte((owner-0x10000)/256), byte(owner)
			if reveal && c.Start+i == active {
				display.WriteString((Token{Kind: ExtendedCharacter, Raw: CharacterBytes(set, number)}).RevealCharacter())
			} else {
				display.WriteString(CharacterGlyph(set, number))
			}
		case reveal && owner == hardReturnByte:
			display.WriteString("[HRt]")
		case reveal && owner == softReturnByte:
			display.WriteString("[SRt]")
		case reveal && owner == deletedSoftReturn:
			display.WriteString("[DSRt]")
		case owner == softReturnByte || owner == deletedSoftReturn:
			display.WriteByte('\n')
		default:
			display.WriteRune(owner)
		}
	}
	return display.String()
}

// RevealParts keeps the highlighted owner separate from adjacent cells.
func (c TableCell) RevealParts(gap int) (string, string, string) {
	owners := tableOwners(c.Text)
	offset := gap - c.Start
	before := TableCell{Text: tableBytes(owners[:offset])}
	if offset == len(owners) {
		return before.RevealText(-1), "", ""
	}
	active := TableCell{Start: gap, Text: tableBytes(owners[offset : offset+1])}
	after := TableCell{Text: tableBytes(owners[offset+1:])}
	return before.RevealText(-1), active.RevealText(gap), after.RevealText(-1)
}

func (c TableCell) RevealText(gap int) string { return c.display(true, gap) }

func (c TableCell) Lines() []string { return strings.Split(c.DisplayText(), "\n") }

func logicalTableText(raw string, gap int) ([]rune, int) {
	var text []rune
	position := 0
	for i, owner := range tableOwners(raw) {
		switch owner {
		case softReturnByte:
			owner = ' '
		case deletedSoftReturn:
			continue
		}
		text = append(text, owner)
		if i < gap {
			position++
		}
	}
	return text, position
}

func wrapTableText(text []rune, width, gap int) ([]rune, int) {
	var output []rune
	position := gap
	for i := 0; i < len(text); {
		end := i
		for end < len(text) && text[end] != '\n' && end-i <= width {
			end++
		}
		if end-i <= width {
			stop := min(len(text), end+1)
			output = append(output, text[i:stop]...)
			i = stop
			continue
		}
		if space := lastTableSpace(text[i+1 : i+width+1]); space >= 0 {
			stop := i + 1 + space
			output = append(output, text[i:stop]...)
			output = append(output, softReturnByte)
			i = stop + 1
		} else {
			output = append(output, text[i:i+width]...)
			output = append(output, deletedSoftReturn)
			i += width
			if i <= gap {
				position++
			}
		}
	}
	return output, position
}

func splitTableOverflow(wrapped []rune, limit int) ([]rune, string, int) {
	lines := 0
	for i, owner := range wrapped {
		switch owner {
		case hardReturnByte, softReturnByte, deletedSoftReturn:
			lines++
			if lines > limit {
				tail, _ := logicalTableText(tableBytes(wrapped[i:]), 0)
				return wrapped[:i], tableBytes(tail), lines
			}
		}
	}
	return wrapped, "", lines
}

func lastTableSpace(line []rune) int {
	for i := len(line) - 1; i >= 0; i-- {
		if line[i] == ' ' {
			return i
		}
	}
	return -1
}
