package document

import (
	"bytes"
	"fmt"
)

func tocMarkKind(raw []byte) bool {
	return len(raw) == 9 && raw[0] == 0xd7 && raw[1] <= 1 && raw[2] == 5 && raw[3] == 0 &&
		raw[4] <= 4 && raw[5] == 5 && raw[6] == 0 && raw[7] == raw[1] && raw[8] == 0xd7
}

func tocMarkLabel(raw []byte) string {
	mark := "Mark"
	if raw[1] == 1 {
		mark = "End Mark"
	}
	return fmt.Sprintf("[%s:ToC,%d]", mark, raw[4]+1)
}

func tocOwner(end, level byte) []byte { return []byte{0xd7, end, 5, 0, level - 1, 5, 0, end, 0xd7} }

func (d *Document) MarkContents(anchor, cursor Cursor, level int) (EditResult, error) {
	if err := d.checkEverydayCursor(anchor); err != nil {
		return unchangedEdit(d, cursor), err
	}
	if err := d.checkEverydayCursor(cursor); err != nil {
		return unchangedEdit(d, cursor), err
	}
	lo, hi := min(anchor.gap, cursor.gap), max(anchor.gap, cursor.gap)
	if lo == hi || level < 1 || level > 5 {
		return unchangedEdit(d, cursor), failure(InvalidPosition, lo, noSpan)
	}
	for i := lo; i < hi; i++ {
		t, _ := d.Token(i)
		if !t.Kind.IsCharacter() {
			return unchangedEdit(d, cursor), failure(UnsupportedBody, i, t.Span)
		}
	}
	image := d.state.image.Export()
	a, b := d.state.gaps[lo], d.state.gaps[hi]
	body := append([]byte(nil), image[d.state.gaps[0]:a]...)
	body = append(body, tocOwner(0, byte(level))...)
	body = append(body, image[a:b]...)
	body = append(body, tocOwner(1, byte(level))...)
	body = append(body, image[b:]...)
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
		if i >= lo {
			mapping[i]++
		}
		if i >= hi {
			mapping[i]++
		}
	}
	return d.publishEveryday(cursor, body, d.TokenCount()+2, hi+2, mapping, blockFormatEdit)
}

// ContentsEntry holds the text owners and resolved page label of a marked heading.
type ContentsEntry struct {
	Text  string
	Page  string
	Level int
}

var contentsDefinition = [...]byte{0xd7, 2, 10, 0, 0, 4, 4, 4, 4, 4, 10, 0, 2, 0xd7}

func contentsDefinitionLevels(raw []byte) int {
	if len(raw) != len(contentsDefinition) || raw[4] >= 2 ||
		!bytes.Equal(raw[:4], contentsDefinition[:4]) || !bytes.Equal(raw[5:], contentsDefinition[5:]) {
		return 0
	}
	return int(raw[4]) + 1
}

func (d *Document) ContentsLevels() int {
	for i := 0; i < d.TokenCount(); i++ {
		t, _ := d.Token(i)
		if t.Kind == ContentsDefinition {
			return contentsDefinitionLevels(t.Raw)
		}
	}
	return 0
}

func (d *Document) DefineContents(c Cursor, levels int) (EditResult, error) {
	if d.ContentsLevels() > 0 {
		return unchangedEdit(d, c), fmt.Errorf("a table of contents is already defined")
	}
	if levels < 1 || levels > 2 {
		return unchangedEdit(d, c), fmt.Errorf("choose one or two contents levels")
	}
	template := contentsDefinition
	template[4] = byte(levels - 1)
	return d.editTokens(c, template[:])
}

func (d *Document) GenerateContents(c Cursor, entries []ContentsEntry) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	start, end, err := d.contentsBounds()
	if err != nil {
		return unchangedEdit(d, c), err
	}
	if start < 0 {
		return unchangedEdit(d, c), fmt.Errorf("define a table of contents before generating it")
	}
	if len(entries) == 0 {
		return unchangedEdit(d, c), fmt.Errorf("mark a heading within the selected contents levels")
	}
	if end == -1 {
		end = start
	}
	raw := d.state.image.Export()
	body := append([]byte(nil), raw[d.state.gaps[0]:d.state.gaps[start+1]]...)
	body = append(body, hardReturnByte)
	added := 2 // Opening return and End Definition.
	for i, e := range entries {
		if i > 0 && e.Level == 1 {
			body = append(body, hardReturnByte)
			added++
		}
		if e.Level < 1 || e.Level > 2 || len(e.Text) == 0 || len(e.Text) > 54-5*(e.Level-1) || len(e.Page) == 0 || len(e.Page) > 5 {
			return unchangedEdit(d, c), fmt.Errorf("contents entry does not fit the default single-line format")
		}
		for _, ch := range []byte(e.Text + e.Page) {
			if ch < 32 || ch > 126 {
				return unchangedEdit(d, c), fmt.Errorf("contents entries require printable ASCII")
			}
		}
		// The original one-level template uses a half-inch double
		// indent, releases the left margin for the title, then inserts
		// the dot-leader flush-right field for the page number.
		body = append(body, 0xc2, 1, 0x58, 2, 8, 7, 8, 7, 15, 0, 0xc2)
		if e.Level == 1 {
			body = append(body, 0xc1, 0x80, 0xb0, 4, 0xb0, 4, 10, 0, 0xc1)
		} else {
			body = append(body, 0xc2, 0, 0x58, 2, 0x60, 9, 0x60, 9, 20, 0, 0xc2)
			body = append(body, 0xc1, 0x80, 8, 7, 8, 7, 15, 0, 0xc1)
			added++
		}
		body = append(body, e.Text...)
		if e.Level == 1 {
			body = append(body, 0xc6, 0xd0, 0x20, 8, 7, 0xc6)
		} else {
			body = append(body, 0xc6, 0xd0, 0x20, 0x60, 9, 0xc6)
		}
		body = append(body, alignmentOwner(ContentsLeader, 9000-(len(e.Page)+2)*120, 9000)...)
		body = append(body, ' ', ' ')
		body = append(body, e.Page...)
		body = append(body, endAlignmentByte, hardReturnByte)
		added += 8 + len(e.Text) + len(e.Page)
	}
	body = append(body, 0x9b)
	body = append(body, raw[d.state.gaps[end+1]:]...)
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
		if i > start && i <= end {
			mapping[i] = -1
		} else if i > end {
			mapping[i] += added - (end - start)
		}
	}
	return d.publishEveryday(c, body, d.TokenCount()+added-(end-start), start+1, mapping, blockFormatEdit)
}

// contentsBounds identifies the only replaceable generated region. A
// heading inside it makes the region ambiguous and must not be discarded.
func (d *Document) contentsBounds() (int, int, error) {
	start, end := -1, -1
	for i := 0; i < d.TokenCount(); i++ {
		t, _ := d.Token(i)
		switch t.Kind {
		case ContentsDefinition:
			if start != -1 {
				return -1, -1, fmt.Errorf("only one contents definition is supported")
			}
			start = i
		case ContentsEnd:
			if start == -1 || end != -1 {
				return -1, -1, fmt.Errorf("unpaired contents definition")
			}
			end = i
		}
	}
	if end >= 0 {
		for i := start + 1; i < end; i++ {
			t, _ := d.Token(i)
			if t.Kind == ContentsMark || t.Kind == ReferenceTarget || t.Kind == PageReference || t.Kind == Subdocument || t.Kind == AuthorityMark {
				return -1, -1, fmt.Errorf("contents definition overlaps other document marks")
			}
		}
	}
	return start, end, nil
}

type ContentsHeading struct {
	Gap   int
	Text  string
	Level int
}

// ContentsHeadings skips generated text, including a definition inserted
// just inside an existing heading's opening mark.
func (d *Document) ContentsHeadings(levels int) ([]ContentsHeading, error) {
	var out []ContentsHeading
	var text []byte
	level, gap := -1, -1
	start, end, err := d.contentsBounds()
	if err != nil {
		return nil, err
	}
	for i := 0; i < d.TokenCount(); i++ {
		if i == start {
			if end >= 0 {
				i = end
			}
			continue
		}
		t, _ := d.Token(i)
		if t.Kind == ContentsMark {
			if t.Raw[1] == 0 {
				if level >= 0 {
					return nil, fmt.Errorf("nested contents marks are not supported")
				}
				level, gap, text = int(t.Raw[4]), -1, nil
			} else {
				if level != int(t.Raw[4]) {
					return nil, fmt.Errorf("unpaired contents heading mark")
				}
				if level < levels && gap >= 0 {
					out = append(out, ContentsHeading{gap, string(text), level + 1})
				}
				level = -1
			}
			continue
		}
		if level >= 0 && level < levels {
			if t.Kind != ASCII {
				return nil, fmt.Errorf("only single-line ASCII contents headings are supported")
			}
			if gap < 0 {
				gap = i
			}
			text = append(text, t.Raw[0])
		}
	}
	if level >= 0 {
		return nil, fmt.Errorf("unpaired contents heading mark")
	}
	return out, nil
}
