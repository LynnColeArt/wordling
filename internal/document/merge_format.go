package document

// MergeFieldFormatting tracks the independent native Bold and Underline
// switches in an explicit data field.
type MergeFieldFormatting struct {
	bold, underline bool
}

// Apply accepts only a complete, alternating attribute owner.
func (f *MergeFieldFormatting) Apply(raw []byte) bool {
	active := &f.bold
	kind := identify(raw)
	switch kind {
	case BoldOn, BoldOff:
	case UnderlineOn, UnderlineOff:
		active = &f.underline
	default:
		return false
	}
	on := kind == BoldOn || kind == UnderlineOn
	if *active == on {
		return false
	}
	*active = on
	return true
}

func (f MergeFieldFormatting) Active() bool { return f.bold || f.underline }

// ToggleMergeFieldAttribute appends an attribute owner at the end of the
// current explicit value. End Field requires both switches to be closed.
func (d *Document) ToggleMergeFieldAttribute(c Cursor, attribute Attribute) (EditResult, error) {
	return d.editMergeOwners(c, false, false, func(body mergeAuthoringBody, at mergeAuthoringGap) (int, []byte, int, error) {
		if !body.secondary || c.gap != d.TokenCount() {
			return 0, nil, 0, failure(UnsupportedBoldContext, c.gap, noSpan)
		}
		switch attribute {
		case BoldAttribute:
			if at.format.bold {
				return 0, []byte(nativeBoldOff), 1, nil
			}
			return 0, []byte(nativeBoldOn), 1, nil
		case UnderlineAttribute:
			if at.format.underline {
				return 0, []byte(nativeUnderlineOff), 1, nil
			}
			return 0, []byte(nativeUnderlineOn), 1, nil
		default:
			return 0, nil, 0, failure(UnsupportedBoldContext, c.gap, noSpan)
		}
	})
}

// ApplyMergeFieldAttribute formats a block within one explicit field. The
// logical selection can cross automatic wraps, but cannot consume merge codes.
func (d *Document) ApplyMergeFieldAttribute(anchor, end Cursor, attribute Attribute) (EditResult, error) {
	start, stop := anchor, end
	if start.gap > stop.gap {
		start, stop = stop, start
	}
	if !d.valid() || anchor.state != d.state || end.state != d.state || start.gap < 0 || start.gap == stop.gap || stop.gap > d.TokenCount() {
		return unchangedEdit(d, end), failure(UnsupportedBoldContext, end.gap, noSpan)
	}
	var on, off Kind
	var begin, finish string
	switch attribute {
	case BoldAttribute:
		on, off, begin, finish = BoldOn, BoldOff, nativeBoldOn, nativeBoldOff
	case UnderlineAttribute:
		on, off, begin, finish = UnderlineOn, UnderlineOff, nativeUnderlineOn, nativeUnderlineOff
	default:
		return unchangedEdit(d, end), failure(UnsupportedBoldContext, end.gap, noSpan)
	}
	active := func(f MergeFieldFormatting) bool {
		if attribute == BoldAttribute {
			return f.bold
		}
		return f.underline
	}
	caret := start.gap
	edit, err := d.editMergeOwners(start, false, false, func(body mergeAuthoringBody, at mergeAuthoringGap) (int, []byte, int, error) {
		if !body.secondary || !body.gaps[stop.gap].editable {
			return 0, nil, 0, failure(UnsupportedBoldContext, start.gap, noSpan)
		}
		var raw []byte
		count, visible := 0, false
		if !active(at.format) {
			raw = append(raw, begin...)
			count++
		}
		for i := start.gap; i < stop.gap; i++ {
			token, _ := d.Token(i)
			switch token.Kind {
			case on, off:
				continue
			case ASCII, ExtendedCharacter:
				visible = true
			case BoldOn, BoldOff, UnderlineOn, UnderlineOff, SoftReturn, DeletedSoftReturn:
			case EndOfPage:
				next, _ := d.Token(i + 1)
				if next.Kind != SoftPage && next.Kind != DeletedSoftPage {
					return 0, nil, 0, failure(UnsupportedBoldContext, i, token.Span)
				}
			case SoftPage, DeletedSoftPage:
			default:
				return 0, nil, 0, failure(UnsupportedBoldContext, i, token.Span)
			}
			raw = append(raw, token.Raw...)
			count++
		}
		if !visible {
			return 0, nil, 0, failure(UnsupportedBoldContext, start.gap, noSpan)
		}
		caret += count
		if !active(body.gaps[stop.gap].format) {
			raw = append(raw, finish...)
			count++
		}
		return stop.gap - start.gap, raw, count, nil
	})
	if err != nil {
		return unchangedEdit(d, end), err
	}
	if end.gap == stop.gap {
		edit.Cursor.gap = caret
	}
	edit.merge.cursor = edit.Cursor
	return edit, nil
}

// deleteMergeFieldAttribute removes both boundaries of the selected Reveal
// code while preserving the text, the other attribute, and page owners.
func (d *Document) deleteMergeFieldAttribute(c Cursor, target int, attribute Attribute) (EditResult, error) {
	if !d.valid() || !c.reveal || c.state != d.state || target < 0 || target >= d.TokenCount() {
		return unchangedEdit(d, c), failure(UnsupportedBoldContext, target, noSpan)
	}
	on, off := d.pairAt(target, attribute)
	if on < 0 {
		return unchangedEdit(d, c), failure(UnsupportedBoldContext, target, noSpan)
	}
	start, _ := d.CursorAt(on)
	start.reveal = true
	edit, err := d.editMergeOwners(start, false, false, func(body mergeAuthoringBody, _ mergeAuthoringGap) (int, []byte, int, error) {
		if !body.secondary {
			return 0, nil, 0, failure(UnsupportedBoldContext, target, noSpan)
		}
		raw := d.state.image.Export()
		return off - on + 1, raw[d.state.gaps[on+1]:d.state.gaps[off]], off - on - 1, nil
	})
	if err != nil {
		return unchangedEdit(d, c), err
	}
	edit.Cursor.gap = c.gap
	if c.gap > on {
		edit.Cursor.gap--
	}
	if c.gap > off {
		edit.Cursor.gap--
	}
	edit.merge.cursor = edit.Cursor
	return edit, nil
}
