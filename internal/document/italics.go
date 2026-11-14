package document

// ToggleItalics inserts a balanced pair with the cursor inside it, or moves
// past the existing close owner when turning off a run just typed.
func (d *Document) ToggleItalics(c Cursor) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if t, err := d.Token(c.gap); err == nil && t.Kind == ItalicsOff {
		c.gap++
		return d.everydayNoOp(c, blockFormatEdit), nil
	}
	for i := c.gap - 1; i >= 0; i-- {
		t, _ := d.Token(i)
		if t.Kind == ItalicsOff {
			break
		}
		if t.Kind == ItalicsOn {
			return unchangedEdit(d, c), failure(UnsupportedBoldContext, c.gap, noSpan)
		}
	}
	raw := d.state.image.Export()
	at := int(d.state.gaps[c.gap])
	body := append([]byte(nil), raw[d.state.gaps[0]:at]...)
	body = append(body, attributeOn, 8, attributeOn, attributeOff, 8, attributeOff)
	body = append(body, raw[at:]...)
	return d.publishEveryday(c, body, d.TokenCount()+2, c.gap+1, insertionTokenMap(d.TokenCount(), c.gap, 2), blockFormatEdit)
}
