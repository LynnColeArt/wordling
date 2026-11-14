package document

import (
	"bytes"
	"fmt"
)

var joinedCellTab = []byte{0xc1, 4, 0x50, 0x14, 0x50, 0x14, 0x2b, 0, 0xc1}

func (c TableCell) JoinedRight() (string, bool) { return c.joinedRight, c.joined }
func (c TableCell) Covered() bool               { return c.Start < 0 }

func (t SimpleTable) joinedRow() bool {
	return len(t.Widths) == 2 && len(t.Cells) == 4 && t.Cells[0].joined && t.Cells[1].Covered()
}

func simpleJoinText(s string) bool {
	for i := range len(s) {
		if s[i] < 32 || s[i] > 126 {
			return false
		}
	}
	return true
}

// JoinTableTopRow admits the observed horizontal join in the first row of a
// default 2 by 2 table. The join stores the second value after a native Tab.
func (d *Document) JoinTableTopRow(c Cursor, first int) (EditResult, error) {
	table, ok := d.SimpleTable()
	last, inside := table.CellAt(c.gap)
	if !ok || !inside || min(first, last) != 0 || max(first, last) != 1 || len(table.Widths) != 2 || len(table.Cells) != 4 || table.joinedRow() {
		return unchangedEdit(d, c), fmt.Errorf("select the two top cells of a default two-by-two table")
	}
	for _, cell := range table.Cells {
		if !simpleJoinText(cell.Text) || cell.Hidden != "" || cell.formula != nil {
			return unchangedEdit(d, c), fmt.Errorf("joining this table requires single-line text cells")
		}
	}
	table.Cells[0].joined = true
	table.Cells[0].joinedRight = table.Cells[1].Text
	table.Cells[1] = TableCell{Start: -1, End: -1}
	body, ok := tableProfiles[2].body(table.Cells)
	if !ok {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	return d.publishSimpleTable(c, body, 0, false)
}

func (d *Document) publishSimpleTable(c Cursor, body []byte, index int, atEnd bool) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	if !d.valid() || c.state != d.state {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	if len(body)+int(d.state.gaps[0]) > MaxMutationBytes {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return unchanged, err
	}
	raw := d.state.image.Export()
	changed := !bytes.Equal(raw[d.state.gaps[0]:], body)
	next := d
	if changed {
		candidate := append(raw[:d.state.gaps[0]], body...)
		candidate[flags] |= 8
		next, err = parseRevision(candidate, d.state.birth)
		if err != nil {
			return unchanged, err
		}
	}
	updated, ok := next.SimpleTable()
	if !ok || next.TokenCount() > MaxMutationTokens || index >= len(updated.Cells) || updated.Cells[index].Covered() {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	c.gap = updated.Cells[index].Start
	if atEnd {
		c.gap = updated.Cells[index].End
	}
	c.state = next.state
	return EditResult{Document: next, Cursor: c, Changed: changed}, nil
}
