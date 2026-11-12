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
