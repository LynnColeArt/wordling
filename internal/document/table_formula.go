package document

import (
	"encoding/binary"
	"fmt"
	"math"
	"strconv"
	"strings"
)

type tableAddress struct{ row, col int }
type tableFormula struct{ left, right tableAddress }

func tableCoordinate(index, columns int) tableAddress {
	return tableAddress{row: index / columns, col: index % columns}
}

func tableFormulaRecord(raw []byte) (*tableFormula, bool) {
	if len(raw) == 19 {
		return nil, true
	}
	if len(raw) != 32 || raw[4] != 0x20 || raw[15] != 1 || raw[16] != 11 ||
		raw[17] != 0xa6 || raw[22] != 0xa6 || raw[27] != 1 {
		return nil, false
	}
	read := func(offset int) tableAddress {
		return tableAddress{
			row: int(int16(binary.LittleEndian.Uint16(raw[offset:]))),
			col: int(int16(binary.LittleEndian.Uint16(raw[offset+2:]))),
		}
	}
	f := &tableFormula{left: read(18), right: read(23)}
	for _, ref := range [...]tableAddress{f.left, f.right} {
		if ref.row <= -MaxTableRows || ref.row >= MaxTableRows || ref.col < -3 || ref.col > 3 {
			return nil, false
		}
	}
	return f, true
}

func (f tableFormula) attach(owner []byte) []byte {
	raw := append([]byte(nil), owner[:15]...)
	raw[4] = 0x20
	raw = append(raw, 1, 11)
	for _, ref := range [...]tableAddress{f.left, f.right} {
		raw = append(raw, 0xa6, byte(ref.row), byte(ref.row>>8), byte(ref.col), byte(ref.col>>8))
	}
	raw = append(raw, 1) // addition, after its two operands
	binary.LittleEndian.PutUint16(raw[2:4], uint16(len(raw)))
	return append(raw, byte(len(raw)), 0, 0, 0xdc)
}

func (ref tableAddress) resolve(source tableAddress, columns int) int {
	col, row := source.col+ref.col, source.row+ref.row
	if col < 0 || col >= columns || row < 0 {
		return -1
	}
	return row*columns + col
}

func (cell TableCell) Formula(index, columns int) string {
	if cell.formula == nil {
		return ""
	}
	name := func(ref tableAddress) string {
		target := ref.resolve(tableCoordinate(index, columns), columns)
		if target < 0 {
			return "?"
		}
		at := tableCoordinate(target, columns)
		return fmt.Sprintf("%c%d", 'A'+at.col, 1+at.row)
	}
	return name(cell.formula.left) + "+" + name(cell.formula.right)
}

func (t SimpleTable) formula(index int, text string) (*tableFormula, error) {
	left, right, ok := strings.Cut(strings.ToUpper(text), "+")
	if !ok {
		return nil, fmt.Errorf("enter two cell names joined by +, such as A1+B1")
	}
	source := tableCoordinate(index, len(t.Widths))
	parse := func(s string) (tableAddress, bool) {
		s = strings.TrimSpace(s)
		if len(s) < 2 || s[0] < 'A' || int(s[0]-'A') >= len(t.Widths) {
			return tableAddress{}, false
		}
		row, err := strconv.Atoi(s[1:])
		if err != nil || row < 1 || row > len(t.Cells)/len(t.Widths) {
			return tableAddress{}, false
		}
		return tableAddress{row - 1 - source.row, int(s[0]-'A') - source.col}, true
	}
	a, aok := parse(left)
	b, bok := parse(right)
	if !aok || !bok {
		return nil, fmt.Errorf("enter two existing table cells")
	}
	return &tableFormula{left: a, right: b}, nil
}

func (t SimpleTable) calculate(all bool, index int) {
	values, states := make([]float64, len(t.Cells)), make([]byte, len(t.Cells))
	var eval func(int) (float64, bool)
	eval = func(i int) (float64, bool) {
		if i < 0 || i >= len(t.Cells) || states[i] == 1 || states[i] == 3 {
			return 0, false
		}
		if states[i] == 2 {
			return values[i], true
		}
		states[i] = 1
		cell := t.Cells[i]
		n := 0.0
		ok := false
		if cell.formula != nil && (all || i == index) {
			at := tableCoordinate(i, len(t.Widths))
			left, foundLeft := eval(cell.formula.left.resolve(at, len(t.Widths)))
			right, foundRight := eval(cell.formula.right.resolve(at, len(t.Widths)))
			n, ok = left+right, foundLeft && foundRight
		} else {
			text := strings.TrimSpace(cell.DisplayText())
			text = strings.ReplaceAll(text[strings.LastIndexByte(text, '\n')+1:], " ", "")
			var err error
			n, err = strconv.ParseFloat(text, 64)
			ok = err == nil
		}
		ok = ok && !math.IsNaN(n) && !math.IsInf(n, 0) && math.Abs(n) < 1e10
		states[i] = 3
		if ok {
			states[i], values[i] = 2, n
		}
		return n, ok
	}
	for i := range t.Cells {
		if t.Cells[i].formula != nil && (all || i == index) {
			value, ok := eval(i)
			t.Cells[i].Text = "??"
			if ok {
				if value == 0 {
					value = 0 // Normalize negative zero.
				}
				t.Cells[i].Text = strconv.FormatFloat(value, 'f', 2, 64)
			}
		}
	}
}

func (d *Document) TableMath(c Cursor, formula string, source int, recalculate bool) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	if !d.valid() || c.state != d.state {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	table, ok := d.SimpleTable()
	index, inside := table.CellAt(c.gap)
	if !ok || !inside || table.joinedRow() {
		return unchanged, fmt.Errorf("move inside the table before using Math")
	}
	if !recalculate {
		if table.Cells[index].formula == nil && table.Cells[index].Text != "" {
			return unchanged, fmt.Errorf("choose an empty cell for this formula")
		}
		f := table.Cells[index].formula
		if source >= 0 {
			if source >= len(table.Cells) || table.Cells[source].formula == nil {
				return unchanged, fmt.Errorf("select a cell containing a formula to copy")
			}
			f = table.Cells[source].formula
		} else {
			var err error
			f, err = table.formula(index, formula)
			if err != nil {
				return unchanged, err
			}
		}
		table.Cells[index].formula = f
	}
	table.calculate(recalculate, index)
	body, ok := tableProfiles[len(table.Widths)].body(table.Cells)
	if !ok {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	return d.publishSimpleTable(c, body, index, !recalculate)
}
