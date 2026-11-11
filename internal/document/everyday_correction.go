package document

import (
	"bytes"
	"encoding/binary"
)

func validEverydayTabStop(column int) bool {
	return column >= 5 && column <= 65 && column%5 == 0
}

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
	return validEverydayTabStop(column) && bytes.Equal(raw, everydayTabOwner(column))
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
	return token.Kind == ASCII || token.Kind == HardReturn ||
		token.Kind == Tab && matchedEverydayTab(token.Raw)
}

// DeleteEveryday erases one complete native character owner and records its
// qualified Undelete group. Existing pair operations retain their own rules.
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
	if !everydayCharacter(token) {
		switch token.Kind {
		case BoldOn, BoldOff, UnderlineOn, UnderlineOff:
			return d.Delete(c, direction, h)
		default:
			return unchanged, failure(UnsupportedDeletion, target, token.Span)
		}
	}
	s := *unchanged.state
	s.everyday, s.kind, s.direction, s.target = true, CharacterDeletion, direction, target
	s.blockStart, s.blockEnd = target, target+1
	return d.completeEverydayDeletion(s, h)
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

func (d *Document) completeEverydayDeletion(s deletionState, h History) (Deletion, error) {
	unchanged := unchangedDeletion(d, s.cursor, h)
	if err := d.checkEverydayDeletion(s.cursor, h); err != nil {
		return unchanged, err
	}
	first, last := s.blockStart, s.blockEnd
	raw := d.state.image.Export()
	begin := int(d.state.gaps[0])
	body := make([]byte, 0, len(raw)-begin)
	body = append(body, raw[begin:d.state.gaps[first]]...)
	body = append(body, raw[d.state.gaps[last]:]...)
	edit, err := d.publishBody(s.cursor, body, d.TokenCount()-(last-first), first, false)
	if err != nil {
		return unchanged, err
	}
	next, err := h.record(s, d.fragment(first, last), edit.Document.state)
	if err != nil {
		return unchanged, err
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
