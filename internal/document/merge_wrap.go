package document

import (
	"bytes"
	"slices"
)

const mergeLineColumns = 65

// reflowMergeSecondary regenerates the physical separators of explicit data.
// End Field and End Record remain the logical boundaries even across pages.
func (d *Document) reflowMergeSecondary(caret int) (*Document, int, error) {
	raw := d.state.image.Export()
	bodyStart := int(d.state.gaps[0])
	out := append([]byte(nil), raw[:bodyStart]...)
	var line []byte
	page, row := uint16(1), uint16(0)
	position, lineCaret := -1, -1
	lineBreak := func(lineCode, pageCode byte) {
		if row == lastEverydayPageRow {
			out = append(out, everydayPageRecord(page, row)...)
			out = append(out, pageCode)
			page++
			row = 0
			return
		}
		out = append(out, lineCode)
		row++
	}
	flush := func() {
		for len(line) > mergeLineColumns {
			split := bytes.LastIndexByte(line[:mergeLineColumns+1], ' ')
			consumed := mergeLineColumns
			if split > 0 {
				consumed = split + 1
			} else {
				split = mergeLineColumns
			}
			if lineCaret >= 0 && lineCaret < consumed {
				position = len(out) + lineCaret
				lineCaret = -1
			}
			out = append(out, line[:split]...)
			if consumed > split {
				lineBreak(softReturnByte, softPageByte)
			} else {
				lineBreak(deletedSoftReturn, deletedSoftPage)
			}
			line = line[consumed:]
			if lineCaret >= 0 {
				lineCaret -= consumed
			}
		}
		if lineCaret >= 0 {
			position = len(out) + lineCaret
			lineCaret = -1
		}
		out = append(out, line...)
		line = line[:0]
	}
	for i := 0; i < d.TokenCount(); i++ {
		if i == caret {
			lineCaret = len(line)
		}
		token, _ := d.Token(i)
		kind := token.Kind
		if kind == EndOfPage {
			transition, err := d.Token(i + 1)
			if err != nil {
				return nil, 0, failure(UnsupportedBody, i, token.Span)
			}
			kind = transition.Kind
			i++
		}
		switch kind {
		case ASCII:
			line = append(line, token.Raw[0])
		case SoftReturn, SoftPage:
			line = append(line, ' ')
		case DeletedSoftReturn, DeletedSoftPage:
		case MergeEndField, MergeEndRecord, MergePageOff, MergePageOn:
			flush()
			out = append(out, token.Raw...)
		case HardReturn, HardReturnSoftPage:
			flush()
			lineBreak(hardReturnByte, hardReturnPageByte)
		case HardPage:
			flush()
			out = append(out, everydayPageRecord(page, row)...)
			out = append(out, hardPageByte)
			page++
			row = 0
		default:
			return nil, 0, failure(UnsupportedBody, i, token.Span)
		}
	}
	if caret == d.TokenCount() {
		lineCaret = len(line)
	}
	flush()
	if len(out) > MaxMutationBytes {
		return nil, 0, failure(MutationLimit, caret, noSpan)
	}
	next, err := parseRevision(out, d.state.birth)
	if err != nil {
		return nil, 0, err
	}
	gap, ok := slices.BinarySearch(next.state.gaps, uint32(position))
	if position < 0 || !ok {
		return nil, 0, failure(InvalidPosition, caret, noSpan)
	}
	return next, gap, nil
}
