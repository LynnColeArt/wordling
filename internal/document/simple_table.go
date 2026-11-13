package document

import (
	"bytes"
	"encoding/hex"
)

// The supported layout is the default two-by-two Letter table with single-line
// printable ASCII cells. The observed row, cell and end caches remain valid
// while edits fit the original 31-column cell interior.
const TableCellWidth = 31

type TableCell struct {
	Start, End int
	Text       string
}

type SimpleTable struct {
	Cells [4]TableCell
}

var simpleTableOwners = func() [][]byte {
	encoded := [...]string{
		"d20b4f00000a03000100000064006400780000000000000000000000000000000000000000000000000000000a02002100b004640064007800000000000000010000003c0f3c0f00000000202000004f000bd2",
		"dc0116000370018412000a100370018412000a100000160001dc",
		"dc000f0000000101000000000000200f0000dc",
		"dc000f0000010101700100000000200f0000dc",
		"dc0116000370018412000a1003800184110209120000160001dc",
		"dc000f0000000101000000000000200f0000dc",
		"dc000f0000010101f00200000000200f0000dc",
		"dc021300038001841102091201007001000002130002dc",
	}
	owners := make([][]byte, len(encoded))
	for i, owner := range encoded {
		owners[i], _ = hex.DecodeString(owner)
	}
	return owners
}()

func (d *Document) SimpleTable() (SimpleTable, bool) {
	var table SimpleTable
	if !d.valid() {
		return table, false
	}
	gap, cell := 0, 0
	for index, owner := range simpleTableOwners {
		token, err := d.Token(gap)
		if err != nil || !bytes.Equal(token.Raw, owner) {
			return SimpleTable{}, false
		}
		gap++
		switch index {
		case 2, 3, 5, 6:
			start := gap
			var content []byte
			for gap < d.TokenCount() {
				token, _ := d.Token(gap)
				if token.Kind != ASCII {
					break
				}
				if len(content) == TableCellWidth {
					return SimpleTable{}, false
				}
				content = append(content, token.Raw[0])
				gap++
			}
			table.Cells[cell] = TableCell{Start: start, End: gap, Text: string(content)}
			cell++
		}
	}
	return table, gap == d.TokenCount()
}

func (t SimpleTable) CellAt(gap int) (int, bool) {
	for i, cell := range t.Cells {
		if gap >= cell.Start && gap <= cell.End {
			return i, true
		}
	}
	return 0, false
}

// EditTableCell replaces a range inside a single cell, preserving all owners.
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
	if start < cell.Start || end < start || end > cell.End ||
		cell.End-cell.Start-(end-start)+len(text) > TableCellWidth {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	for i := range len(text) {
		if text[i] < 32 || text[i] > 126 {
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
	candidate := append(bytes.Clone(raw[:from]), text...)
	candidate = append(candidate, raw[to:]...)
	candidate[flags] |= 8
	next, err := parseRevision(candidate, d.state.birth)
	if err != nil {
		return unchanged, err
	}
	c.state = next.state
	return EditResult{Document: next, Cursor: c, Changed: true}, nil
}
