package document

import (
	"bytes"
	"fmt"
)

// ComparePlainText marks one changed line between two plain-text versions.
// Each corresponding line must have an ordinary hard return or end at EOF.
func (d *Document) ComparePlainText(c Cursor, other *Document) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	if err := d.checkEverydayCursor(c); err != nil {
		return unchanged, err
	}
	read := func(doc *Document) ([][]byte, bool) {
		if !doc.valid() || doc.TokenCount() < 1 || doc.TokenCount() > MaxMutationTokens {
			return nil, false
		}
		b, ok := doc.state.image.Bytes(doc.state.image.Inspect().Body)
		if !ok || len(b) != doc.TokenCount() {
			return nil, false
		}
		lines := bytes.SplitAfter(b, []byte{hardReturnByte})
		for _, line := range lines {
			if plain := bytes.TrimSuffix(line, []byte{hardReturnByte}); len(plain) > 65 || !simpleJoinText(string(plain)) {
				return nil, false
			}
		}
		return lines, true
	}
	screen, ok := read(d)
	disk, diskOK := read(other)
	unsupported := fmt.Errorf("Document Compare requires plain text versions with one changed line")
	if !ok || !diskOK || len(screen) != len(disk) {
		return unchanged, unsupported
	}
	start, changed := 0, -1
	for i := range screen {
		if !bytes.Equal(screen[i], disk[i]) {
			if changed != -1 || len(screen[i]) == 0 || len(disk[i]) == 0 {
				return unchanged, unsupported
			}
			changed = i
		}
		if changed == -1 {
			start += len(screen[i])
		}
	}
	if changed == -1 {
		return d.everydayNoOp(c, blockFormatEdit), nil
	}
	current, past := screen[changed], disk[changed]
	if (current[len(current)-1] == hardReturnByte) != (past[len(past)-1] == hardReturnByte) ||
		current[len(current)-1] != hardReturnByte && len(current)+len(past) > 65 {
		return unchanged, unsupported
	}
	body := make([]byte, 0, d.TokenCount()+len(past)+12)
	for _, line := range screen[:changed] {
		body = append(body, line...)
	}
	body = append(body, attributeOn, 10, attributeOn)
	body = append(body, current...)
	body = append(body, attributeOff, 10, attributeOff, attributeOn, 13, attributeOn)
	body = append(body, past...)
	body = append(body, attributeOff, 13, attributeOff)
	for _, line := range screen[changed+1:] {
		body = append(body, line...)
	}

	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
		switch {
		case i >= start+len(current):
			mapping[i] += len(past) + 4
		case i >= start:
			mapping[i]++
		}
	}
	return d.publishEveryday(c, body, d.TokenCount()+len(past)+4, 0, mapping, blockFormatEdit)
}

// RemoveComparisonMarks implements the bounded plain-text cleanup described in
// REF51 printed pp. 130 and 549: keep redlined text, discard strikeout text and
// both attributes' codes, then leave the cursor at the document end. It applies
// to pre-existing marks too, not only marks created by ComparePlainText.
// Other formatting, subdocuments and moved-phrase annotations are not admitted.
func (d *Document) RemoveComparisonMarks(c Cursor) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	if err := d.checkEverydayCursor(c); err != nil {
		return unchanged, err
	}
	unsupported := fmt.Errorf("comparison cleanup requires plain ASCII text with balanced Redline and Strikeout only; moved phrases and other formatting are not supported")
	if d.TokenCount() > MaxMutationTokens {
		return unchanged, failure(MutationLimit, -1, noSpan)
	}
	var body, originalText []byte
	mapping := make([]int, d.TokenCount())
	redline, strikeout, marked := false, false, false
	count := 0
	for i := range d.TokenCount() {
		token, err := d.Token(i)
		if err != nil {
			return unchanged, err
		}
		mapping[i] = -1
		switch token.Kind {
		case RedlineOn, RedlineOff, StrikeoutOn, StrikeoutOff:
			active := &redline
			if token.Kind == StrikeoutOn || token.Kind == StrikeoutOff {
				active = &strikeout
			}
			on := token.Kind == RedlineOn || token.Kind == StrikeoutOn
			if *active == on {
				return unchanged, unsupported
			}
			*active, marked = on, true
		case ASCII, HardReturn:
			originalText = append(originalText, token.Raw...)
			if !strikeout {
				mapping[i] = count
				count++
				body = append(body, token.Raw...)
			}
		default:
			return unchanged, unsupported
		}
	}
	if redline || strikeout || bytes.Contains(originalText, []byte("THE FOLLOWING TEXT WAS MOVED")) || bytes.Contains(originalText, []byte("THE PRECEDING TEXT WAS MOVED")) {
		return unchanged, unsupported
	}
	if !marked {
		end, err := d.CursorAt(d.TokenCount())
		if err != nil {
			return unchanged, err
		}
		return d.everydayNoOp(end.WithReveal(c.Reveal()), blockFormatEdit), nil
	}
	return d.publishEveryday(c, body, count, count, mapping, blockFormatEdit)
}
