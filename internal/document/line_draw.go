package document

import "fmt"

// ExtendHorizontalDrawing writes the start and end caps used by the pinned
// line draw profile. The caret follows DOS to the left of the final cap.
func (d *Document) ExtendHorizontalDrawing(c Cursor, start, steps int, double bool) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if steps < 1 || steps > 65 || start < 0 || start > d.TokenCount() {
		return unchangedEdit(d, c), fmt.Errorf("draw within one fixed-pitch line")
	}
	first, middle, last := byte(50), byte(8), byte(48)
	if double {
		first, middle, last = 54, 19, 52
	}
	stop := start
	if steps > 1 {
		stop = start + steps
		if stop > d.TokenCount() || c.gap != stop-1 {
			return unchangedEdit(d, c), fmt.Errorf("the drawing changed while Line Draw was active")
		}
		for i := start; i < stop; i++ {
			t, _ := d.Token(i)
			want := middle
			if i == start {
				want = first
			} else if i == stop-1 {
				want = last
			}
			if t.Kind != ExtendedCharacter || t.Raw[1] != want || t.Raw[2] != 3 {
				return unchangedEdit(d, c), fmt.Errorf("the drawing changed while Line Draw was active")
			}
		}
	}
	raw := d.state.image.Export()
	body := append([]byte(nil), raw[d.state.gaps[0]:d.state.gaps[start]]...)
	body = append(body, CharacterBytes(3, first)...)
	for range steps - 1 {
		body = append(body, CharacterBytes(3, middle)...)
	}
	body = append(body, CharacterBytes(3, last)...)
	body = append(body, raw[d.state.gaps[stop]:]...)
	delta := steps + 1 - (stop - start)
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
		if i >= stop {
			mapping[i] += delta
		} else if i >= start {
			mapping[i] = -1
		}
	}
	return d.publishEveryday(c, body, d.TokenCount()+delta, start+steps, mapping, blockFormatEdit)
}
