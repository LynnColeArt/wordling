package document

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
	var bold, underline bool
	for i := 0; i < last; i++ {
		if i == first {
			if bold {
				body = append(body, attributeOn, boldAttribute, attributeOn)
			}
			if underline {
				body = append(body, attributeOn, underlineAttr, attributeOn)
			}
		}
		t, _ := d.Token(i)
		switch t.Kind {
		case BoldOn, BoldOff:
			bold = t.Kind == BoldOn
		case UnderlineOn, UnderlineOff:
			underline = t.Kind == UnderlineOn
		}
		if i >= first {
			switch t.Kind {
			case ASCII, ExtendedCharacter, HardSpace, DOSControl, Tab, HardReturn, HardPage,
				SoftReturn, DeletedSoftReturn, BoldOn, BoldOff, UnderlineOn, UnderlineOff:
				body = append(body, t.Raw...)
			default:
				return nil, failure(UnsupportedBody, i, t.Span)
			}
		}
	}
	if underline {
		body = append(body, attributeOff, underlineAttr, attributeOff)
	}
	if bold {
		body = append(body, attributeOff, boldAttribute, attributeOff)
	}
	if len(body) > MaxMutationBytes || last-first+4 > MaxMutationTokens {
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
