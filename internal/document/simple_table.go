package document

import (
	"bytes"
	"encoding/binary"
	"encoding/hex"
	"strings"
)

// SimpleTable describes the default standalone Letter table.
type TableCell struct {
	Start, End int
	Text       string
}

type SimpleTable struct {
	Cells  []TableCell
	Widths []int
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

const MaxTableRows = 20

func tableOwner(encoded string) []byte {
	raw, _ := hex.DecodeString(encoded)
	return raw
}

// encode regenerates the default row height and position caches from the
// tallest preceding cell in each row and the tallest cell in each row.
func (p tableProfile) encode(cells []TableCell) ([][]byte, bool) {
	columns := len(p.widths)
	rows := len(cells) / columns
	owners := [][]byte{tableOwner(p.header)}
	rowStart, priorHeight, priorStart := 0, 0, 0
	for row := range rows {
		encoded := p.middle
		height := 336
		switch {
		case row == 0:
			encoded, height = p.first, 368
		case row == rows-1:
			encoded, height = p.last, 384
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
		maxExtra := 0
		cellOwners := make([][]byte, 0, columns)
		for column := range columns {
			cell := cells[row*columns+column]
			raw := tableOwner(p.cell)
			raw[5] = byte(column)
			if column > 0 {
				raw[7] = 1
				binary.LittleEndian.PutUint16(raw[8:], uint16(rowStart+height+200*maxExtra))
				raw[10] = byte(maxExtra)
			}
			lines := strings.Split(cell.Text, "\n")
			for _, line := range lines {
				if len(line) > p.widths[column] {
					return nil, false
				}
			}
			maxExtra = max(maxExtra, len(lines)-1)
			cellOwners = append(cellOwners, raw)
		}
		height += 200 * maxExtra
		binary.LittleEndian.PutUint16(owner[13+2*(columns-2):], uint16(height))
		owners = append(owners, owner)
		owners = append(owners, cellOwners...)
		priorStart, rowStart = rowStart, rowStart+height
		priorHeight = height
		if rowStart > 10000 {
			return nil, false
		}
	}
	end := tableOwner(p.end)
	binary.LittleEndian.PutUint16(end[5:], uint16(priorHeight))
	i := 12 + 2*(columns-2)
	binary.LittleEndian.PutUint16(end[i:], uint16(rows-1))
	binary.LittleEndian.PutUint16(end[i+2:], uint16(priorStart))
	owners = append(owners, end)
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
		if len(row.Raw) < 2 || row.Raw[0] != 0xdc || row.Raw[1] != 1 {
			break
		}
		owners = append(owners, row.Raw)
		gap++
		for range p.widths {
			cell, err := d.Token(gap)
			if err != nil || len(cell.Raw) != 19 || cell.Raw[0] != 0xdc || cell.Raw[1] != 0 {
				return SimpleTable{}, false
			}
			owners = append(owners, cell.Raw)
			gap++
			start := gap
			var content strings.Builder
			for gap < d.TokenCount() {
				token, _ := d.Token(gap)
				if token.Kind == HardReturn {
					content.WriteByte('\n')
				} else if token.Kind == ASCII {
					content.WriteByte(token.Raw[0])
				} else {
					break
				}
				if content.Len() > 2000 {
					return SimpleTable{}, false
				}
				gap++
			}
			table.Cells = append(table.Cells, TableCell{Start: start, End: gap, Text: content.String()})
		}
	}
	if gap+1 != d.TokenCount() || len(table.Cells) < 2*len(p.widths) {
		return SimpleTable{}, false
	}
	end, _ := d.Token(gap)
	owners = append(owners, end.Raw)
	expected, ok := p.encode(table.Cells)
	if !ok {
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
	if start < cell.Start || end < start || end > cell.End {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	for i := range len(text) {
		if text[i] != '\n' && (text[i] < 32 || text[i] > 126) {
			return unchanged, failure(InvalidASCII, c.gap, noSpan)
		}
	}
	if d.TokenCount()-(end-start)+len(text) > MaxMutationTokens ||
		int(d.state.gaps[d.TokenCount()])-(end-start)+len(text) > MaxMutationBytes {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return unchanged, err
	}
	raw := d.state.image.Export()
	from, to := d.state.gaps[start], d.state.gaps[end]
	c.gap = start + len(text)
	if bytes.Equal(raw[from:to], []byte(text)) {
		return EditResult{Document: d, Cursor: c}, nil
	}
	table.Cells[index].Text = cell.Text[:start-cell.Start] + text + cell.Text[end-cell.Start:]
	body, ok := tableProfiles[len(table.Widths)].body(table.Cells)
	if !ok {
		return unchanged, failure(UnsupportedBody, start, noSpan)
	}
	candidate := append(raw[:d.state.gaps[0]], body...)
	candidate[flags] |= 8
	next, err := parseRevision(candidate, d.state.birth)
	if err != nil {
		return unchanged, err
	}
	c.state = next.state
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
