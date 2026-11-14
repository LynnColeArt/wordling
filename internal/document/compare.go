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
