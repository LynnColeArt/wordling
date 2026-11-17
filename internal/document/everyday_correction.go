package document

import (
	"bytes"
	"encoding/binary"
)

func validEverydayTabStop(column int) bool {
	return column >= 5 && column <= 65 && column%5 == 0
}

func validTabColumn(column int) bool { return column >= -10 && column <= 75 }

func everydayTabOwner(column int) []byte {
	absolute := uint16(column + 10)
	advance := absolute * 120
	raw := []byte{0xc1, 2, 0, 0, 0, 0, 0, 0, 0xc1}
	binary.LittleEndian.PutUint16(raw[2:4], advance)
	binary.LittleEndian.PutUint16(raw[4:6], advance)
	binary.LittleEndian.PutUint16(raw[6:8], absolute)
	return raw
}

func matchedEverydayTab(raw []byte) bool {
	if len(raw) != 9 {
		return false
	}
	column := int(binary.LittleEndian.Uint16(raw[6:8])) - 10
	return validTabColumn(column) && bytes.Equal(raw, everydayTabOwner(column))
}

// InsertEverydayTab writes the complete default-profile Tab owner for a
// zero-based text stop calculated by the formatter.
func (d *Document) InsertEverydayTab(c Cursor, targetColumn int) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if !validEverydayTabStop(targetColumn) {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	return d.InsertTab(c, everydayTabOwner(targetColumn))
}

func (d *Document) InsertPositionedTab(c Cursor, targetColumn int) (EditResult, error) {
	if !validTabColumn(targetColumn) {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	if d.BeforeDecimalAlignmentEnd(c.gap) {
		c.gap++
	}
	return d.InsertTab(c, everydayTabOwner(targetColumn))
}

func (d *Document) checkEverydayDeletion(c Cursor, h History) error {
	if err := d.checkEverydayCursor(c); err != nil {
		return err
	}
	if err := h.check(d); err != nil {
		return err
	}
	if h.state.observed != nil {
		return failure(UnsupportedHistoryEffect, c.gap, noSpan)
	}
	if h.state.groupUnknown {
		return failure(UnsupportedHistoryBoundary, c.gap, noSpan)
	}
	return nil
}

func everydayCharacter(token Token) bool {
	return token.Kind.IsCharacter() || token.Kind == DOSControl || token.Kind == HardReturn || token.Kind == Indent ||
		token.Kind == Tab && (matchedEverydayTab(token.Raw) || bytes.Equal(token.Raw, dosTextTab))
}

// DeleteEveryday erases one complete native character owner and records its
// qualified Undelete group, or removes the exact code owners of a qualified
// pair or trailing formatter boundary.
func (d *Document) DeleteEveryday(c Cursor, direction DeleteDirection, h History) (Deletion, error) {
	unchanged := unchangedDeletion(d, c, h)
	if err := d.checkEverydayDeletion(c, h); err != nil {
		return unchanged, err
	}
	target := c.gap
	switch direction {
	case Backspace:
		target--
	case ForwardDelete:
	default:
		return unchanged, failure(InvalidDirection, c.gap, noSpan)
	}
	token, err := d.Token(target)
	if err != nil {
		return unchanged, err
	}
	s := *unchanged.state
	s.everyday, s.direction, s.target = true, direction, target
	if everydayCharacter(token) {
		s.kind = CharacterDeletion
		s.blockStart, s.blockEnd = target, target+1
		return d.completeEverydayDeletion(s, h)
	}
	switch token.Kind {
	case BoldOn, BoldOff, UnderlineOn, UnderlineOff:
		if direction == Backspace {
			return d.Delete(c, direction, h)
		}
		s.kind, s.attribute = PairDeletion, BoldAttribute
		if token.Kind == UnderlineOn || token.Kind == UnderlineOff {
			s.attribute = UnderlineAttribute
		}
		s.on, s.off = d.pairAt(target, s.attribute)
		if s.on < 0 {
			return unchanged, failure(UnsupportedBody, target, token.Span)
		}
		if !c.reveal {
			s.pending = true
			return Deletion{&s}, nil
		}
		return d.completeEverydayPair(s, h)
	case DeletedSoftReturn:
		if direction == Backspace && d.isTrailingEverydayWrap(target) {
			s.kind = formatterBoundaryDeletion
			s.blockStart, s.blockEnd = target, target+1
			return d.completeEverydayDeletion(s, h)
		}
	}
	return unchanged, failure(UnsupportedDeletion, target, token.Span)
}

// The observed trailing DSRt is the final owner after a full, unbroken
// default-profile text row. Other soft returns remain formatter-owned.
func (d *Document) isTrailingEverydayWrap(index int) bool {
	const rowWidth = 65
	if index != d.TokenCount()-1 || index < rowWidth {
		return false
	}
	for i := index - rowWidth; i < index; i++ {
		token, _ := d.Token(i)
		if token.Kind != ASCII || token.Raw[0] == ' ' {
			return false
		}
	}
	if index == rowWidth {
		return true
	}
	prior, _ := d.Token(index - rowWidth - 1)
	return prior.Kind == HardReturn
}

// DeleteEverydayBlock captures the native half-open range in either direction.
// The displayed caret is independent of the endpoints and survives a refusal.
func (d *Document) DeleteEverydayBlock(current, anchor, end Cursor, h History) (Deletion, error) {
	unchanged := unchangedDeletion(d, current, h)
	for _, c := range []Cursor{current, anchor, end} {
		if err := d.checkEverydayDeletion(c, h); err != nil {
			return unchanged, err
		}
		if c.reveal != current.reveal {
			return unchanged, failure(InvalidPosition, c.gap, noSpan)
		}
	}
	first, last := min(anchor.gap, end.gap), max(anchor.gap, end.gap)
	if first == last {
		return unchanged, failure(UnsupportedDeletion, first, noSpan)
	}
	if current.gap < first || current.gap > last {
		return unchanged, failure(InvalidPosition, current.gap, noSpan)
	}
	var bold, underline int
	for i := first; i < last; i++ {
		t, _ := d.Token(i)
		switch t.Kind {
		case BoldOn:
			bold++
		case BoldOff:
			bold--
		case UnderlineOn:
			underline++
		case UnderlineOff:
			underline--
		case SoftReturn, DeletedSoftReturn:
		default:
			if !everydayCharacter(t) {
				return unchanged, failure(UnsupportedDeletion, i, t.Span)
			}
		}
		if bold < 0 || underline < 0 {
			return unchanged, failure(UnsupportedDeletion, i, t.Span)
		}
	}
	if bold != 0 || underline != 0 {
		return unchanged, failure(UnsupportedDeletion, first, noSpan)
	}
	s := *unchanged.state
	s.everyday, s.kind, s.block, s.pending = true, EverydayBlockDeletion, true, true
	s.blockStart, s.blockEnd = first, last
	return Deletion{&s}, nil
}

// DeleteEverydayRange deletes word text as one Undelete entry, retaining formatting.
func (d *Document) DeleteEverydayRange(current, start, end Cursor, h History, direction DeleteDirection) (Deletion, error) {
	return d.deleteEverydayRange(current, start, end, h, false, true, direction)
}

// ConfirmEverydayPageDeletion asks before deleting up to the page boundary.
func (d *Document) ConfirmEverydayPageDeletion(current, end Cursor, h History) (Deletion, error) {
	return d.deleteEverydayRange(current, current, end, h, true, true, 0)
}

// DeleteEverydayLine removes complete formatting pairs inside the deleted range.
func (d *Document) DeleteEverydayLine(current, end Cursor, h History) (Deletion, error) {
	var before, after [2]bool
	for i := 0; i < end.gap; i++ {
		if i == current.gap {
			before = after
		}
		t, err := d.Token(i)
		if err != nil {
			return unchangedDeletion(d, current, h), err
		}
		switch t.Kind {
		case BoldOn:
			after[0] = true
		case BoldOff:
			after[0] = false
		case UnderlineOn:
			after[1] = true
		case UnderlineOff:
			after[1] = false
		}
	}
	if before != after {
		return d.deleteSplitFormattedLine(current, end, h, before, after)
	}
	return d.deleteEverydayRange(current, current, end, h, false, false, 0)
}

// A deleted formatted fragment gets its own opening and closing codes.
// The text left on either side keeps the attributes it had before deletion.
func (d *Document) deleteSplitFormattedLine(current, end Cursor, h History, before, after [2]bool) (Deletion, error) {
	unchanged := unchangedDeletion(d, current, h)
	for _, c := range []Cursor{current, end} {
		if err := d.checkEverydayDeletion(c, h); err != nil {
			return unchanged, err
		}
	}
	if current.gap >= end.gap || current.reveal != end.reveal {
		return unchanged, failure(InvalidPosition, current.gap, noSpan)
	}
	for i := current.gap; i < end.gap; i++ {
		token, _ := d.Token(i)
		switch token.Kind {
		case BoldOn, BoldOff, UnderlineOn, UnderlineOff, SoftReturn, DeletedSoftReturn:
		default:
			if !everydayCharacter(token) {
				return unchanged, failure(UnsupportedDeletion, i, token.Span)
			}
		}
	}
	fragment := d.fragment(current.gap, end.gap)
	raw := d.state.image.Export()
	body := append([]byte(nil), raw[d.state.gaps[0]:d.state.gaps[current.gap]]...)
	gap := current.gap
	var wrapper []byte
	var opening, closing []Kind
	for i, attr := range []byte{0x0c, 0x0e} {
		if before[i] == after[i] {
			continue
		}
		on, off := BoldOn, BoldOff
		if i == 1 {
			on, off = UnderlineOn, UnderlineOff
		}
		if before[i] {
			body = append(body, 0xc4, attr, 0xc4)
			wrapper = append(wrapper, 0xc3, attr, 0xc3)
			opening = append(opening, on)
		} else {
			body = append(body, 0xc3, attr, 0xc3)
			fragment.native += string([]byte{0xc4, attr, 0xc4})
			closing = append(closing, off)
		}
		gap++
	}
	fragment.native = string(wrapper) + fragment.native
	fragment.kinds = append(append(opening, fragment.kinds...), closing...)
	fragment.offsets = fragment.offsets[:0]
	for at := 0; at < len(wrapper); at += 3 {
		fragment.offsets = append(fragment.offsets, uint32(at))
	}
	for i := current.gap; i < end.gap; i++ {
		fragment.offsets = append(fragment.offsets, uint32(len(wrapper)+int(d.state.gaps[i]-d.state.gaps[current.gap])))
	}
	for i := len(closing); i > 0; i-- {
		fragment.offsets = append(fragment.offsets, uint32(len(fragment.native)-i*3))
	}
	fragment.offsets = append(fragment.offsets, uint32(len(fragment.native)))
	body = append(body, raw[d.state.gaps[end.gap]:]...)
	edit, err := d.publishBody(current, body, d.TokenCount()-(end.gap-current.gap)+gap-current.gap, gap, false)
	if err != nil {
		return unchanged, err
	}
	state := *unchanged.state
	state.everyday, state.kind = true, EverydayBlockDeletion
	next, err := h.record(state, fragment, edit.Document.state)
	if err != nil {
		return unchanged, err
	}
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
		if i >= end.gap {
			mapping[i] += gap - end.gap
		} else if i >= current.gap {
			mapping[i] = -1
		}
	}
	remapFormats(next.state, d.state, edit.Document.state, mapping)
	state.after, state.cursor, state.afterHistory = edit.Document.state, edit.Cursor, next.state
	state.applied, state.bodyChanged, state.nativeChanged = true, true, true
	return Deletion{&state}, nil
}

func (d *Document) deleteEverydayRange(current, start, end Cursor, h History, pageRemainder, keepFormatting bool, direction DeleteDirection) (Deletion, error) {
	unchanged := unchangedDeletion(d, current, h)
	for _, cursor := range []Cursor{current, start, end} {
		if err := d.checkEverydayDeletion(cursor, h); err != nil {
			return unchanged, err
		}
		if cursor.reveal != current.reveal {
			return unchanged, failure(InvalidPosition, cursor.gap, noSpan)
		}
	}
	if start.gap >= end.gap || current.gap < start.gap || current.gap > end.gap {
		return unchanged, failure(InvalidPosition, current.gap, noSpan)
	}
	for i := start.gap; i < end.gap; i++ {
		token, _ := d.Token(i)
		switch token.Kind {
		case BoldOn, BoldOff, UnderlineOn, UnderlineOff, SoftReturn, DeletedSoftReturn:
		default:
			if !everydayCharacter(token) {
				return unchanged, failure(UnsupportedDeletion, i, token.Span)
			}
		}
	}
	state := *unchanged.state
	state.everyday, state.keepFormatting, state.kind = true, keepFormatting, EverydayBlockDeletion
	state.blockStart, state.blockEnd, state.wordDirection = start.gap, end.gap, direction
	if pageRemainder {
		state.pageRemainder, state.pending = true, true
		return Deletion{&state}, nil
	}
	return d.completeEverydayDeletion(state, h)
}

func (d *Document) completeEverydayDeletion(s deletionState, h History) (Deletion, error) {
	unchanged := unchangedDeletion(d, s.cursor, h)
	if err := d.checkEverydayDeletion(s.cursor, h); err != nil {
		return unchanged, err
	}
	if s.kind == PairDeletion {
		return d.completeEverydayPair(s, h)
	}
	first, last := s.blockStart, s.blockEnd
	if s.keepFormatting {
		return d.completeTextRangeDeletion(s, h)
	}
	raw := d.state.image.Export()
	begin := int(d.state.gaps[0])
	body := make([]byte, 0, len(raw)-begin)
	body = append(body, raw[begin:d.state.gaps[first]]...)
	body = append(body, raw[d.state.gaps[last]:]...)
	edit, err := d.publishBody(s.cursor, body, d.TokenCount()-(last-first), first, false)
	if err != nil {
		return unchanged, err
	}
	var next History
	if s.kind == formatterBoundaryDeletion {
		state := *h.state
		state.document = edit.Document.state
		state.groupOpen = state.groupOpen && state.groupDirection == Backspace && state.groupGap == s.cursor.gap
		state.groupGap = edit.Cursor.gap
		next = History{&state}
	} else {
		next, err = h.record(s, d.fragment(first, last), edit.Document.state)
		if err != nil {
			return unchanged, err
		}
	}
	next.state.seedStage = seedUnqualified
	if next.state.bold != nil || next.state.underline != nil {
		mapping := make([]int, d.TokenCount())
		for i := range mapping {
			switch {
			case i < first:
				mapping[i] = i
			case i < last:
				mapping[i] = -1
			default:
				mapping[i] = i - (last - first)
			}
		}
		remapFormats(next.state, d.state, edit.Document.state, mapping)
	}
	s.after, s.cursor, s.afterHistory = edit.Document.state, edit.Cursor, next.state
	s.pending, s.block, s.applied = false, false, true
	s.bodyChanged, s.nativeChanged = edit.Changed, s.before != s.after
	return Deletion{&s}, nil
}

func (d *Document) completeTextRangeDeletion(s deletionState, h History) (Deletion, error) {
	unchanged := unchangedDeletion(d, s.cursor, h)
	raw := d.state.image.Export()
	start := int(d.state.gaps[0])
	lo, hi := s.blockStart, s.blockEnd
	body := append([]byte(nil), raw[start:d.state.gaps[lo]]...)
	removed := fragment{}
	var removedBytes []byte
	caret := lo
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
		if i < lo || i >= hi {
			mapping[i] -= len(removed.kinds)
			continue
		}
		token, _ := d.Token(i)
		switch token.Kind {
		case BoldOn, BoldOff, UnderlineOn, UnderlineOff:
			mapping[i] -= len(removed.kinds)
			body = append(body, token.Raw...)
			caret++
		default:
			mapping[i] = -1
			removed.offsets = append(removed.offsets, uint32(len(removedBytes)))
			removedBytes = append(removedBytes, token.Raw...)
			removed.kinds = append(removed.kinds, token.Kind)
		}
	}
	if len(removed.kinds) == 0 {
		s.pending = false
		return Deletion{&s}, nil
	}
	removedCount := len(removed.kinds)
	if s.wordDirection == Backspace {
		caret = lo
	}
	if s.wordDirection == ForwardDelete {
		// DOS prepends the opening codes of attributes closed by the
		// forward deletion, in reverse encounter order.
		var restoredBold, restoredUnderline bool
		for i := lo; i < hi; i++ {
			token, _ := d.Token(i)
			var kind Kind
			switch token.Kind {
			case BoldOff:
				if restoredBold {
					continue
				}
				restoredBold = true
				kind = BoldOn
			case UnderlineOff:
				if restoredUnderline {
					continue
				}
				restoredUnderline = true
				kind = UnderlineOn
			default:
				continue
			}
			removedBytes = append([]byte{0xc3, token.Raw[1], 0xc3}, removedBytes...)
			for j := range removed.offsets {
				removed.offsets[j] += 3
			}
			removed.offsets = append([]uint32{0}, removed.offsets...)
			removed.kinds = append([]Kind{kind}, removed.kinds...)
			removed.wordRestore = true
		}
	}

	body = append(body, raw[d.state.gaps[hi]:]...)
	removed.native = string(removedBytes)
	removed.offsets = append(removed.offsets, uint32(len(removedBytes)))
	edit, err := d.publishBody(s.cursor, body, d.TokenCount()-removedCount, caret, false)
	if err != nil {
		return unchanged, err
	}
	next, err := h.record(s, removed, edit.Document.state)
	if err != nil {
		return unchanged, err
	}
	remapFormats(next.state, d.state, edit.Document.state, mapping)
	s.after, s.cursor, s.afterHistory = edit.Document.state, edit.Cursor, next.state
	s.pending = false
	s.applied, s.bodyChanged, s.nativeChanged = true, edit.Changed, s.before != s.after
	return Deletion{&s}, nil
}

// completeEverydayPair removes the selected pair's two complete owners
// without placing formatting-only deletion on the original Undelete stack.
func (d *Document) completeEverydayPair(s deletionState, h History) (Deletion, error) {
	unchanged := unchangedDeletion(d, s.cursor, h)
	raw := d.state.image.Export()
	start := int(d.state.gaps[0])
	on, off := d.span(s.on), d.span(s.off)
	body := make([]byte, 0, len(raw)-start-on.Length-off.Length)
	body = append(body, raw[start:on.Offset]...)
	body = append(body, raw[on.Offset+on.Length:off.Offset]...)
	body = append(body, raw[off.Offset+off.Length:]...)
	gap := s.target
	if s.target == s.off {
		gap--
	}
	edit, err := d.publishBody(s.cursor, body, d.TokenCount()-2, gap, false)
	if err != nil {
		return unchanged, err
	}
	next := *h.state
	next.document, next.groupOpen, next.seedStage = edit.Document.state, false, seedUnqualified
	if next.bold != nil || next.underline != nil {
		mapping := make([]int, d.TokenCount())
		for i := range mapping {
			switch {
			case i == s.on || i == s.off:
				mapping[i] = -1
			case i > s.off:
				mapping[i] = i - 2
			case i > s.on:
				mapping[i] = i - 1
			default:
				mapping[i] = i
			}
		}
		remapFormats(&next, d.state, edit.Document.state, mapping)
	}
	s.after, s.cursor, s.afterHistory = edit.Document.state, edit.Cursor, &next
	s.pending, s.applied = false, true
	s.bodyChanged, s.nativeChanged = edit.Changed, s.before != s.after
	return Deletion{&s}, nil
}

func insertionTokenMap(count, gap, added int) []int {
	mapping := make([]int, count)
	for i := range mapping {
		mapping[i] = i
		if i >= gap {
			mapping[i] += added
		}
	}
	return mapping
}

func remapFormats(h *historyState, before, after *revisionState, tokenMap []int) {
	r := everydayReceipt{before: before, after: after, tokenMap: tokenMap}
	h.bold = remapFormat(h.bold, &r)
	h.underline = remapFormat(h.underline, &r)
}

// ConvertEverydayBlockCase modifies ASCII letters within the native selection.
// The sentence context comes from punctuation included in the selection.
func (d *Document) ConvertEverydayBlockCase(anchor, cursor Cursor, uppercase bool) (EditResult, error) {
	unchanged := unchangedEdit(d, cursor)
	for _, c := range []Cursor{anchor, cursor} {
		if err := d.checkEverydayCursor(c); err != nil {
			return unchanged, err
		}
	}
	lo, hi := min(anchor.gap, cursor.gap), max(anchor.gap, cursor.gap)
	body := bytes.Clone(d.state.image.Export()[d.state.gaps[0]:])
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
	}
	sentence, wordStart := false, true
	for i := lo; i < hi; i++ {
		token, _ := d.Token(i)
		if token.Kind != ASCII {
			if token.Kind == HardReturn || token.Kind == SoftReturn || token.Kind == Tab {
				wordStart = true
			}
			continue
		}
		c := token.Raw[0]
		index := token.Span.Offset - int(d.state.gaps[0])
		switch {
		case c >= 'a' && c <= 'z':
			if uppercase {
				body[index] = c - ('a' - 'A')
			}
			wordStart, sentence = false, false
		case c >= 'A' && c <= 'Z':
			keepI := false
			if c == 'I' && wordStart && i+1 < hi {
				next, _ := d.Token(i + 1)
				keepI = next.Kind == ASCII && next.Raw[0] == '\''
			}
			if !uppercase && !sentence && !keepI {
				body[index] = c + ('a' - 'A')
			}
			wordStart, sentence = false, false
		case c == '.' || c == '!' || c == '?':
			wordStart, sentence = true, true
		default:
			wordStart = c == ' ' || c == '"' || c == '('
		}
	}
	return d.publishEveryday(cursor, body, d.TokenCount(), cursor.gap, mapping, blockCaseEdit)
}

// ApplyEverydayBlockFormat sets one attribute over the selected text. Existing
// coverage is unioned with the selection, preserving the other attribute.
func (d *Document) ApplyEverydayBlockFormat(anchor, cursor Cursor, attribute Attribute) (EditResult, error) {
	unchanged := unchangedEdit(d, cursor)
	for _, c := range []Cursor{anchor, cursor} {
		if err := d.checkEverydayCursor(c); err != nil {
			return unchanged, err
		}
	}
	lo, hi := min(anchor.gap, cursor.gap), max(anchor.gap, cursor.gap)
	if lo == hi {
		return d.everydayNoOp(cursor, blockFormatEdit), nil
	}
	on, off, begin, finish := BoldOn, BoldOff, nativeBoldOn, nativeBoldOff
	if attribute == UnderlineAttribute {
		on, off, begin, finish = UnderlineOn, UnderlineOff, nativeUnderlineOn, nativeUnderlineOff
	} else if attribute != BoldAttribute {
		return unchanged, failure(UnsupportedBoldContext, lo, noSpan)
	}

	oldActive, active := false, false
	var body []byte
	var count, gap int
	visible := false
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		token, _ := d.Token(i)
		selected := i >= lo && i < hi
		if token.Kind == on || token.Kind == off {
			if i == cursor.gap {
				gap = count
			}
			oldActive = token.Kind == on
			mapping[i] = -1
			if !selected && oldActive != active {
				mapping[i] = count
				body = append(body, token.Raw...)
				count++
				active = oldActive
			}
			continue
		}
		visible = visible || selected && token.Kind.IsCharacter()
		if desired := oldActive || selected; desired != active {
			if desired {
				body = append(body, begin...)
			} else {
				body = append(body, finish...)
			}
			count++
			active = desired
		}
		if i == cursor.gap {
			gap = count
		}
		mapping[i] = count
		body = append(body, token.Raw...)
		count++
	}
	if !visible {
		return d.everydayNoOp(cursor, blockFormatEdit), nil
	}
	if cursor.gap == d.TokenCount() {
		gap = count
	}
	if active {
		body = append(body, finish...)
		count++
	}
	return d.publishEveryday(cursor, body, count, gap, mapping, blockFormatEdit)
}

// BeginEverydayFormat inserts an exact pair at an editable native position.
func (d *Document) BeginEverydayFormat(c Cursor, attribute Attribute) (BoldResult, error) {
	return d.beginFormat(c, attribute, true)
}

// CloseEverydayFormat consumes the exact active pair. Its Off owner may move
// ahead of another attribute's Off when two active formats overlap.
func (d *Document) CloseEverydayFormat(c Cursor, active BoldSpan, attribute Attribute) (BoldResult, error) {
	unchanged := d.boldRefusal(c)
	if err := d.checkEverydayCursor(c); err != nil {
		return unchanged, err
	}
	s := active.state
	if !s.matches(d.state) || s.attribute != attribute || c.gap <= s.on || c.gap > s.off {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	on, off := d.pairAt(s.on, attribute)
	if on != s.on || off != s.off {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	if c.gap == s.on+1 {
		return unchanged, failure(EmptyBoldSpan, c.gap, noSpan)
	}
	receipt := &boldReceipt{before: d.state, after: d.state, operation: closeBold,
		attribute: attribute, active: s, everyday: true}
	gap := c.gap
	c.gap++
	receipt.cursor = c
	if gap != off {
		raw := d.state.image.Export()
		start, at := int(d.state.gaps[0]), int(d.state.gaps[gap])
		from, to := int(d.state.gaps[off]), int(d.state.gaps[off+1])
		body := make([]byte, 0, len(raw)-start)
		body = append(body, raw[start:at]...)
		body = append(body, raw[from:to]...)
		body = append(body, raw[at:from]...)
		body = append(body, raw[to:]...)
		edit, err := d.publishBody(c, body, d.TokenCount(), c.gap, false)
		if err != nil {
			return unchanged, err
		}
		receipt.after, receipt.cursor = edit.Document.state, edit.Cursor
		receipt.tokenMap = insertionTokenMap(d.TokenCount(), gap, 0)
		for i := gap; i < off; i++ {
			receipt.tokenMap[i] = i + 1
		}
		receipt.tokenMap[off] = gap
	}
	return BoldResult{native: receipt.after, cursor: receipt.cursor, receipt: receipt}, nil
}

// AfterEverydayFormat adopts only an authentic everyday pair receipt against a
// qualified history, preserving earlier Undelete groups and the other format.
func (h History) AfterEverydayFormat(r BoldResult) (History, error) {
	a := r.receipt
	if h.state == nil || a == nil || !a.everyday || !r.native.valid() ||
		r.native != a.after || r.cursor != a.cursor || h.state.document != a.before {
		return h, failure(InvalidBoldResult, -1, noSpan)
	}
	if h.state.effectUnqualified || h.state.observed != nil || h.state.groupUnknown {
		return h, failure(UnsupportedHistoryEffect, -1, noSpan)
	}
	current := h.state.format(a.attribute)
	var state boldState
	switch a.operation {
	case openBold:
		if current.matches(a.before) {
			return h, failure(InvalidBoldResult, -1, noSpan)
		}
		state = boldState{owner: a.after, attribute: a.attribute, phase: boldActive, on: r.cursor.gap - 1, off: r.cursor.gap}
	case closeBold:
		if current != a.active || !current.matches(a.before) {
			return h, failure(InvalidBoldResult, -1, noSpan)
		}
		state = *current
		state.owner, state.phase, state.off = a.after, boldClosed, r.cursor.gap-1
	default:
		return h, failure(InvalidBoldResult, -1, noSpan)
	}
	next := *h.state
	if a.before != a.after {
		remapFormats(&next, a.before, a.after, a.tokenMap)
	}
	next.setFormat(a.attribute, &state)
	next.document = a.after
	next.groupOpen = false
	next.seedStage = seedUnqualified
	return History{&next}, nil
}

// ProtectEverydayBlock inserts the native pair around the selected text.
func (d *Document) ProtectEverydayBlock(anchor, cursor Cursor, rows int) (EditResult, error) {
	if err := d.checkEverydayCursor(anchor); err != nil {
		return unchangedEdit(d, cursor), err
	}
	if err := d.checkEverydayCursor(cursor); err != nil {
		return unchangedEdit(d, cursor), err
	}
	lo, hi := min(anchor.gap, cursor.gap), max(anchor.gap, cursor.gap)
	if lo == hi || rows < 1 || rows > lastEverydayPageRow+1 {
		return unchangedEdit(d, cursor), failure(InvalidPosition, lo, noSpan)
	}
	active := false
	for i := 0; i < hi; i++ {
		token, _ := d.Token(i)
		switch token.Kind {
		case BlockProtectOn, BlockProtectOff:
			if i >= lo {
				return unchangedEdit(d, cursor), failure(UnsupportedBody, i, token.Span)
			}
			active = token.Kind == BlockProtectOn
		case HardPage:
			if i >= lo {
				return unchangedEdit(d, cursor), failure(UnsupportedBody, i, token.Span)
			}
		}
	}
	if active {
		return unchangedEdit(d, cursor), failure(UnsupportedBody, lo, noSpan)
	}
	raw := d.state.image.Export()
	a, b := d.state.gaps[lo], d.state.gaps[hi]
	body := append([]byte(nil), raw[d.state.gaps[0]:a]...)
	units := rows * 200
	body = append(body, 0xc5, 0, byte(units), byte(units>>8), 0xc5)
	body = append(body, raw[a:b]...)
	body = append(body, 0xc5, 1, byte(units), byte(units>>8), 0xc5)
	body = append(body, raw[b:]...)
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
	return d.publishEveryday(cursor, body, d.TokenCount()+2, cursor.gap+1, mapping, blockCaseEdit)
}
