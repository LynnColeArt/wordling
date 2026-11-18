package document

const blockCopyItalicsAttribute byte = 0x08

// CopyEverydayBlock prepares a self-contained fragment for retrieval. The
// fragment includes the formatting active at either edge of the selection.
func (d *Document) CopyEverydayBlock(anchor, end Cursor) (*Document, error) {
	if err := d.checkEverydayCursor(end); err != nil {
		return nil, err
	}
	if anchor.state != d.state || anchor.gap < 0 || anchor.gap > d.TokenCount() {
		return nil, failure(InvalidPosition, anchor.gap, noSpan)
	}
	first, last := min(anchor.gap, end.gap), max(anchor.gap, end.gap)
	if first == last {
		return nil, failure(InvalidPosition, first, noSpan)
	}
	var body []byte
	var bold, underline, italics bool
	wrappers := 0
	for i := 0; i < last; i++ {
		if i == first {
			if bold {
				body = append(body, attributeOn, boldAttribute, attributeOn)
				wrappers++
			}
			if underline {
				body = append(body, attributeOn, underlineAttr, attributeOn)
				wrappers++
			}
			if italics {
				body = append(body, attributeOn, blockCopyItalicsAttribute, attributeOn)
				wrappers++
			}
		}
		t, _ := d.Token(i)
		switch t.Kind {
		case BoldOn, BoldOff:
			bold = t.Kind == BoldOn
		case UnderlineOn, UnderlineOff:
			underline = t.Kind == UnderlineOn
		case ItalicsOn, ItalicsOff:
			italics = t.Kind == ItalicsOn
		}
		if i >= first {
			switch t.Kind {
			case ASCII, ExtendedCharacter, HardSpace, DOSControl, Tab, HardReturn, HardPage,
				SoftReturn, DeletedSoftReturn, BoldOn, BoldOff, UnderlineOn, UnderlineOff, ItalicsOn, ItalicsOff:
				body = append(body, t.Raw...)
			default:
				return nil, failure(UnsupportedBody, i, t.Span)
			}
		}
	}
	if italics {
		body = append(body, attributeOff, blockCopyItalicsAttribute, attributeOff)
		wrappers++
	}
	if underline {
		body = append(body, attributeOff, underlineAttr, attributeOff)
		wrappers++
	}
	if bold {
		body = append(body, attributeOff, boldAttribute, attributeOff)
		wrappers++
	}
	if len(body) > MaxMutationBytes || last-first+max(4, wrappers) > MaxMutationTokens {
		return nil, failure(MutationLimit, first, noSpan)
	}
	// Retrieval uses only these owners. Keep the source's metadata out of
	// the detached copy, including Summary and Fast Save packets.
	prefix, err := encodeHistoricalProfile()
	if err != nil {
		return nil, err
	}
	return Parse(append(prefix, body...))
}
