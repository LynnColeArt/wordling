package document

// Original command identities; these are semantic commands, not terminal keys.
type DeleteDirection uint8

const (
	ForwardDelete DeleteDirection = iota + 1
	Backspace
)

type DeleteAnswer uint8

const (
	Yes DeleteAnswer = iota + 1
	No
	F1
	Escape
)

type DeletionKind uint8

const (
	NoDeletion DeletionKind = iota
	CharacterDeletion
	PairDeletion
	OpeningRepair
	ClosingRepair
	AttributedDeletion
	Restoration
)
const (
	UnsupportedDeletion        Category = "UnsupportedDeletion"
	UnsupportedHistoryEffect   Category = "UnsupportedHistoryEffect"
	InvalidHistory             Category = "InvalidHistory"
	HistoryMismatch            Category = "HistoryMismatch"
	InvalidDeletionState       Category = "InvalidDeletionState"
	InvalidAnswer              Category = "InvalidAnswer"
	InvalidEditResult          Category = "InvalidEditResult"
	InvalidPreview             Category = "InvalidPreview"
	HistoryEmpty               Category = "HistoryEmpty"
	UnsupportedHistoryBoundary Category = "UnsupportedHistoryBoundary"
)

// Deletion is an immutable command result/question. Accessors return copied
// handles or values; no accepted object retains an exported mutable wrapper.
type Deletion struct{ state *deletionState }
type deletionState struct {
	before, after                                       *revisionState
	beforeHistory, afterHistory                         *historyState
	cursor                                              Cursor
	kind                                                DeletionKind
	direction                                           DeleteDirection
	target, on, off                                     int
	blockStart, blockEnd                                int
	pending, block, applied, bodyChanged, nativeChanged bool
}

func (r Deletion) Document() *Document {
	if r.state == nil {
		return nil
	}
	return &Document{state: r.state.after}
}
func (r Deletion) Cursor() Cursor {
	if r.state == nil {
		return Cursor{}
	}
	return r.state.cursor
}
func (r Deletion) History() History {
	if r.state == nil {
		return History{}
	}
	return History{state: r.state.afterHistory}
}
func (r Deletion) Pending() bool       { return r.state != nil && r.state.pending }
func (r Deletion) BlockActive() bool   { return r.state != nil && r.state.block }
func (r Deletion) Applied() bool       { return r.state != nil && r.state.applied }
func (r Deletion) BodyChanged() bool   { return r.state != nil && r.state.bodyChanged }
func (r Deletion) NativeChanged() bool { return r.state != nil && r.state.nativeChanged }
func (r Deletion) Kind() DeletionKind {
	if r.state == nil {
		return NoDeletion
	}
	return r.state.kind
}
func (r Deletion) BlockRange() (int, int, bool) {
	if !r.BlockActive() {
		return 0, 0, false
	}
	return r.state.blockStart, r.state.blockEnd, true
}
func (r Deletion) Prompt() string {
	if !r.Pending() {
		return ""
	}
	if r.state.block {
		return "Delete Block? No (Yes)"
	}
	if r.state.target == r.state.on {
		return "Delete [BOLD]? No (Yes)"
	}
	return "Delete [bold]? No (Yes)"
}
func unchangedDeletion(d *Document, c Cursor, h History) Deletion {
	var state *revisionState
	if d != nil {
		state = d.state
	}
	return Deletion{&deletionState{before: state, after: state, beforeHistory: h.state, afterHistory: h.state, cursor: c}}
}
func (d *Document) checkDeletion(c Cursor, h History) error {
	if !d.valid() {
		return failure(InvalidDocument, -1, noSpan)
	}
	if c.state != d.state {
		return failure(RevisionMismatch, c.gap, noSpan)
	}
	if e := h.check(d); e != nil {
		return e
	}
	return d.CheckMutation()
}
func (d *Document) pairAt(index int) (int, int) {
	on := -1
	raw := d.state.image.Export()
	for i := 0; i < d.TokenCount(); i++ {
		s := d.span(i)
		switch identify(raw[s.Offset : s.Offset+s.Length]) {
		case BoldOn:
			on = i
		case BoldOff:
			if on == index || i == index {
				return on, i
			}
			on = -1
		}
	}
	return -1, -1
}

// Delete interprets only a complete admitted ASCII/Bold token. Normal Bold
// deletion returns its exact code question; Reveal bypasses that question.
// Unsupported history effects remain atomic prerequisites, never guessed entries.
func (d *Document) Delete(c Cursor, direction DeleteDirection, h History) (Deletion, error) {
	unchanged := unchangedDeletion(d, c, h)
	if e := d.checkDeletion(c, h); e != nil {
		return unchanged, e
	}
	if direction != ForwardDelete && direction != Backspace {
		return unchanged, failure(InvalidDirection, c.gap, noSpan)
	}
	target := c.gap
	if direction == Backspace {
		target--
	}
	if target < 0 || target >= d.TokenCount() {
		return unchanged, failure(InvalidPosition, target, noSpan)
	}
	token, _ := d.Token(target)
	s := *unchanged.state
	s.direction = direction
	s.target = target
	if token.Kind == ASCII {
		s.kind = CharacterDeletion
		return d.completeDeletion(s, h)
	}
	if token.Kind != BoldOn && token.Kind != BoldOff {
		return unchanged, failure(UnsupportedDeletion, target, token.Span)
	}
	s.kind = PairDeletion
	s.on, s.off = d.pairAt(target)
	if s.on < 0 {
		return unchanged, failure(UnsupportedBody, target, token.Span)
	}
	if !c.reveal {
		s.pending = true
		return Deletion{&s}, nil
	}
	return d.completeDeletion(s, h)
}

// DeleteBlock qualifies forward selections of exactly one opening boundary, one
// closing boundary, or a complete attributed span in Reveal Codes. Empty,
// reversed, normal-view and other partial selections are explicitly unqualified.
func (d *Document) DeleteBlock(anchor, end Cursor, h History) (Deletion, error) {
	unchanged := unchangedDeletion(d, end, h)
	if e := d.checkDeletion(end, h); e != nil {
		return unchanged, e
	}
	if anchor.state != d.state {
		return unchanged, failure(RevisionMismatch, anchor.gap, noSpan)
	}
	if !anchor.reveal || !end.reveal || anchor.gap >= end.gap {
		return unchanged, failure(UnsupportedDeletion, anchor.gap, noSpan)
	}
	s := *unchanged.state
	s.blockStart = anchor.gap
	s.blockEnd = end.gap
	s.block = true
	s.pending = true
	s.on, s.off = d.pairAt(anchor.gap)
	if s.on < 0 {
		return unchanged, failure(UnsupportedDeletion, anchor.gap, noSpan)
	}
	switch {
	case anchor.gap == s.on && end.gap == s.on+1:
		s.kind = OpeningRepair
	case anchor.gap == s.off && end.gap == s.off+1:
		s.kind = ClosingRepair
	case anchor.gap == s.on && end.gap == s.off+1:
		s.kind = AttributedDeletion
	default:
		return unchanged, failure(UnsupportedDeletion, anchor.gap, noSpan)
	}
	return Deletion{&s}, nil
}
func (d *Document) AnswerDeletion(h History, pending Deletion, answer DeleteAnswer) (Deletion, error) {
	unchanged := unchangedDeletion(d, pending.Cursor(), h)
	if pending.state == nil || !pending.Pending() {
		return unchanged, failure(InvalidDeletionState, -1, noSpan)
	}
	if e := d.checkDeletion(pending.Cursor(), h); e != nil {
		return unchanged, e
	}
	if pending.state.beforeHistory != h.state || pending.state.before != d.state {
		return unchanged, failure(HistoryMismatch, -1, noSpan)
	}
	if answer < Yes || answer > Escape {
		return pending, failure(InvalidAnswer, -1, noSpan)
	}
	s := *pending.state
	if answer == Yes {
		return d.completeDeletion(s, h)
	}
	if h.state.count > 0 {
		return pending, failure(UnsupportedHistoryEffect, -1, noSpan)
	}
	s.pending = false
	if !s.block {
		if s.direction == ForwardDelete {
			s.cursor.gap++
		} else {
			s.cursor.gap--
		}
	}
	next := *h.state
	next.groupOpen = false
	s.afterHistory = &next
	return Deletion{&s}, nil
}

// CancelBlock is the separately observed F1 cleanup after a declined block
// question. It is not a global Escape/No/cancel-exit rule or an Undelete action.
func (d *Document) CancelBlock(h History, r Deletion) (Deletion, error) {
	unchanged := unchangedDeletion(d, r.Cursor(), h)
	if e := d.checkDeletion(r.Cursor(), h); e != nil {
		return unchanged, e
	}
	if r.state == nil || r.Pending() || !r.BlockActive() || r.state.after != d.state || r.state.afterHistory != h.state {
		return unchanged, failure(InvalidDeletionState, -1, noSpan)
	}
	s := *r.state
	s.block = false
	s.kind = NoDeletion
	s.before = s.after
	s.beforeHistory = h.state
	next := *h.state
	next.groupOpen = false
	s.afterHistory = &next
	return Deletion{&s}, nil
}
func (d *Document) completeDeletion(s deletionState, h History) (Deletion, error) {
	unchanged := Deletion{&s}
	if h.state.groupUnknown {
		return unchanged, failure(UnsupportedHistoryBoundary, -1, noSpan)
	}
	// Approved WP40 qualifies only its structural command context and bounded
	// observations; no general record/skip/clear/count rule is inferred.
	if (s.kind == PairDeletion || s.kind == ClosingRepair) && !h.wp40Target(s) {
		return unchanged, failure(UnsupportedHistoryEffect, s.target, noSpan)
	}
	if h.state.count > 0 && (s.kind == OpeningRepair || s.kind == AttributedDeletion) {
		return unchanged, failure(UnsupportedHistoryEffect, s.target, noSpan)
	}
	if h.state.observed != nil || (s.kind == CharacterDeletion && s.direction == Backspace) {
		return unchanged, failure(UnsupportedHistoryEffect, s.target, noSpan)
	}
	raw := d.state.image.Export()
	bodyStart := int(d.state.gaps[0])
	body := make([]byte, 0, len(raw)-bodyStart)
	gap := s.cursor.gap
	tokens := d.TokenCount()
	var remembered fragment
	switch s.kind {
	case CharacterDeletion:
		span := d.span(s.target)
		body = append(body, raw[bodyStart:span.Offset]...)
		body = append(body, raw[span.Offset+span.Length:]...)
		remembered = d.fragment(s.target, s.target+1)
		tokens--
		gap = s.target
	case PairDeletion:
		on, off := d.span(s.on), d.span(s.off)
		body = append(body, raw[bodyStart:on.Offset]...)
		body = append(body, raw[on.Offset+on.Length:off.Offset]...)
		body = append(body, raw[off.Offset+off.Length:]...)
		tokens -= 2
		gap = s.target
		if s.target == s.off {
			gap--
		}
	case ClosingRepair:
		body = append(body, raw[bodyStart:]...)
		remembered = joinFragments(d.fragment(s.on, s.on+1), d.fragment(s.off, s.off+1))
		gap = s.blockEnd
	case OpeningRepair:
		body = append(body, raw[bodyStart:]...)
		remembered = joinFragments(d.fragment(s.off, s.off+1), d.fragment(s.on, s.on+1))
		gap = s.blockEnd
	case AttributedDeletion:
		start, end := int(d.state.gaps[s.blockStart]), int(d.state.gaps[s.blockEnd])
		body = append(body, raw[bodyStart:start]...)
		body = append(body, raw[end:]...)
		remembered = d.fragment(s.blockStart, s.blockEnd)
		tokens -= s.blockEnd - s.blockStart
		gap = s.blockStart
	default:
		return unchanged, failure(UnsupportedDeletion, -1, noSpan)
	}
	edit, e := d.publishBody(s.cursor, body, tokens, gap, (s.kind == OpeningRepair || s.kind == ClosingRepair))
	if e != nil {
		return unchanged, e
	}
	var next History
	if s.kind == PairDeletion || s.kind == ClosingRepair {
		next = h.observeTarget(s, remembered, edit.Document.state)
	} else {
		next, e = h.record(s, remembered, edit.Document.state)
	}
	if e != nil {
		return unchanged, e
	}
	s.after = edit.Document.state
	s.cursor = edit.Cursor
	s.afterHistory = next.state
	s.pending = false
	s.block = false
	s.applied = true
	s.bodyChanged = edit.Changed
	s.nativeChanged = s.before != s.after
	return Deletion{&s}, nil
}
