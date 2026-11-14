package document

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

func (d *Document) ColumnMathAt(c Cursor) bool {
	if !d.valid() || c.state != d.state {
		return false
	}
	for i := c.gap - 1; i >= 0; i-- {
		token, _ := d.Token(i)
		switch token.Kind {
		case MathOn:
			return true
		case MathOff:
			return false
		}
	}
	return false
}

func (d *Document) SetColumnMath(c Cursor, enabled bool) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if enabled == d.ColumnMathAt(c) {
		return unchangedEdit(d, c), fmt.Errorf("Math is already %s", map[bool]string{true: "on", false: "off"}[enabled])
	}
	b := byte(0xa8)
	if enabled {
		b = 0xa7
	}
	return d.editTokens(c, []byte{b})
}

// InsertColumnSubtotal places the native subtotal owner after the decimal
// field's hidden terminator. Calculate later fills the field before it.
func (d *Document) InsertColumnSubtotal(c Cursor) (EditResult, error) {
	if !d.ColumnMathAt(c) || !d.BeforeDecimalAlignmentEnd(c.gap) {
		return unchangedEdit(d, c), fmt.Errorf("use a Math decimal tab before the subtotal")
	}
	c.gap++
	return d.insertNamedTokens(c, []byte{0xa1}, 1)
}

func (d *Document) CalculateColumnSubtotal(c Cursor) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if !d.ColumnMathAt(c) {
		return unchangedEdit(d, c), fmt.Errorf("turn on Math before calculating")
	}
	start := c.gap - 1
	for start >= 0 {
		t, _ := d.Token(start)
		if t.Kind == MathOn {
			break
		}
		start--
	}
	total := 0.0
	values := 0
	field, closing := -1, -1
	bodyStart, bodyEnd := -1, -1
	newText := ""
	for i := start + 1; i < d.TokenCount(); i++ {
		t, _ := d.Token(i)
		switch t.Kind {
		case MathOff, MathOn:
			i = d.TokenCount()
		case SoftDecimalTab:
			if field >= 0 {
				return unchangedEdit(d, c), fmt.Errorf("this calculation supports one Math column")
			}
			field, closing = i, -1
		case EndAlignment:
			closing = i
		case MathSubtotal:
			if bodyStart >= 0 || field < 0 || closing <= field || values == 0 {
				return unchangedEdit(d, c), fmt.Errorf("enter numbers and a single subtotal in the same Math column")
			}
			bodyStart, bodyEnd = field+1, i
			newText = strconv.FormatFloat(total, 'f', 2, 64)
			if math.Abs(total) >= 1e8 {
				return unchangedEdit(d, c), fmt.Errorf("subtotal is outside the supported range")
			}
		case HardReturn:
			if field >= 0 && bodyStart < 0 {
				if closing != i-1 {
					return unchangedEdit(d, c), fmt.Errorf("enter a whole number in each Math row")
				}
				raw := d.state.image.Export()
				text := string(raw[d.state.gaps[field+1]:d.state.gaps[closing]])
				value, err := strconv.ParseInt(text, 10, 32)
				if err != nil {
					return unchangedEdit(d, c), fmt.Errorf("enter a whole number in each Math row")
				}
				total += float64(value)
				values++
			}
			field, closing = -1, -1
		}
	}
	if bodyStart < 0 {
		return unchangedEdit(d, c), fmt.Errorf("add a subtotal (+) in the Math column")
	}
	period := strings.IndexByte(newText, '.')
	insert := append([]byte(newText[:period]), endAlignmentByte)
	insert = append(insert, newText[period:]...)
	raw := d.state.image.Export()
	body := append([]byte(nil), raw[d.state.gaps[0]:d.state.gaps[bodyStart]]...)
	body = append(body, insert...)
	body = append(body, raw[d.state.gaps[bodyEnd]:]...)
	delta := len(insert) - (bodyEnd - bodyStart)
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
		if i >= bodyStart && i < bodyEnd {
			mapping[i] = -1
		} else if i >= bodyEnd {
			mapping[i] += delta
		}
	}
	return d.publishEveryday(c, body, d.TokenCount()+delta, bodyEnd+delta+1, mapping, blockFormatEdit)
}
