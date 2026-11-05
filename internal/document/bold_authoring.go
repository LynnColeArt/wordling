package document

import "github.com/lynncoleart/wordling/internal/wp51"

const (
	UnsupportedBoldContext Category = "UnsupportedBoldContext"
	EmptyBoldSpan          Category = "EmptyBoldSpan"
	InvalidBoldResult      Category = "InvalidBoldResult"
	InvalidBoldSpan        Category = "InvalidBoldSpan"
)

const (
	nativeBoldOn  = "\xc3\x0c\xc3"
	nativeBoldOff = "\xc4\x0c\xc4"
	boldPairBytes = len(nativeBoldOn) + len(nativeBoldOff)
)

type boldPhase uint8

const (
	boldPristine boldPhase = iota + 1
	boldActive
	boldClosed
)

// boldState is copied on every change. Its nonzero-size allocation gives each
// active span its own identity, including after an ASCII receipt advances Off.
type boldState struct {
	owner    *revisionState
	phase    boldPhase
	on, off  int
	inserted int
}

// BoldSpan is the immutable active formatting authority from History.ActiveBold.
type BoldSpan struct{ state *boldState }

type boldOperation uint8

const (
	openBold boldOperation = iota + 1
	closeBold
)

type boldReceipt struct {
	before, after *revisionState
	cursor        Cursor
	operation     boldOperation
	priorPairs    int
	active        *boldState
}

// BoldResult is an immutable candidate transition. History.AfterBold admits its
// private receipt before a caller adopts the new native and history state.
type BoldResult struct {
	native  *revisionState
	cursor  Cursor
	receipt *boldReceipt
}

func (r BoldResult) Document() *Document {
	if r.native == nil {
		return nil
	}
	return &Document{r.native}
}
func (r BoldResult) Cursor() Cursor { return r.cursor }
func (r BoldResult) Changed() bool  { return r.receipt != nil && r.receipt.before != r.native }

func (d *Document) boldRefusal(c Cursor) BoldResult {
	if !d.valid() {
		return BoldResult{cursor: c}
	}
	return BoldResult{native: d.state, cursor: c}
}

func (d *Document) boldOrigin(flagOffset int) *boldState {
	if !d.Birth().IsNew() || d.TokenCount() != 0 {
		return nil
	}
	flag, ok := d.state.image.Bytes(wp51.Span{Offset: flagOffset, Length: 1})
	// New has a clear format-change bit. The existing publisher sets it on
	// every body change, including an edit that later returns to empty.
	if !ok || flag[0]&8 != 0 {
		return nil
	}
	return &boldState{owner: d.state, phase: boldPristine}
}

// BeginBold appends one balanced native pair and leaves the cursor before Off.
// History separately qualifies the constructor or prior closed-span lineage.
func (d *Document) BeginBold(c Cursor) (BoldResult, error) {
	unchanged := d.boldRefusal(c)
	if !d.valid() || !d.Birth().IsNew() || c.state != d.state ||
		c.gap != d.TokenCount() || c.reveal {
		return unchanged, failure(UnsupportedBoldContext, c.gap, noSpan)
	}
	if err := d.CheckMutation(); err != nil {
		return unchanged, err
	}
	count := d.TokenCount()
	end := int(d.state.gaps[count])
	if count > MaxMutationTokens-2 || end > MaxMutationBytes-boldPairBytes {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	raw := d.state.image.Export()
	prior, err := d.boldOpenPairs(raw)
	if err != nil {
		return unchanged, err
	}
	body := make([]byte, 0, end-int(d.state.gaps[0])+boldPairBytes)
	body = append(body, raw[d.state.gaps[0]:end]...)
	body = append(body, nativeBoldOn...)
	body = append(body, nativeBoldOff...)
	edit, err := d.publishBody(c, body, count+2, count+1, false)
	if err != nil {
		return unchanged, err
	}
	receipt := &boldReceipt{before: d.state, after: edit.Document.state, cursor: edit.Cursor,
		operation: openBold, priorPairs: prior}
	return BoldResult{native: receipt.after, cursor: receipt.cursor, receipt: receipt}, nil
}

func (d *Document) boldOpenPairs(raw []byte) (int, error) {
	pairs := 0
	previous := ASCII
	for i := range d.TokenCount() {
		span := d.span(i)
		kind := identify(raw[span.Offset : span.Offset+span.Length])
		if kind == BoldOn {
			pairs++
		}
		if pairs >= MaxBoldPairs || kind == BoldOff && previous == BoldOn {
			return 0, failure(UnsupportedBoldContext, i, span)
		}
		previous = kind
	}
	return pairs, nil
}

func (s *boldState) matches(owner *revisionState) bool {
	return s != nil && s.phase == boldActive && s.owner == owner
}

// CloseBold crosses the existing Off. The document, native revision and bytes
// remain identical. Only History.AfterBold records consumption of this span.
func (d *Document) CloseBold(c Cursor, active BoldSpan) (BoldResult, error) {
	unchanged := d.boldRefusal(c)
	if !d.valid() || !d.Birth().IsNew() || c.state != d.state {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	s := active.state
	if !s.matches(d.state) {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	if c.gap != s.off || s.off != d.TokenCount()-1 || s.on < 0 ||
		s.on >= s.off || s.inserted != s.off-s.on-1 {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	if err := d.CheckMutation(); err != nil {
		return unchanged, err
	}
	on, _ := d.Token(s.on)
	off, _ := d.Token(s.off)
	if on.Kind != BoldOn || off.Kind != BoldOff {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	if s.inserted == 0 {
		return unchanged, failure(EmptyBoldSpan, c.gap, noSpan)
	}
	c.gap++
	receipt := &boldReceipt{before: d.state, after: d.state, cursor: c, operation: closeBold, active: s}
	return BoldResult{native: d.state, cursor: c, receipt: receipt}, nil
}

// ActiveBold reports active formatting only for the supplied native owner.
func (h History) ActiveBold(d *Document) (BoldSpan, bool) {
	if h.state == nil || !d.valid() || h.state.document != d.state || !h.state.bold.matches(d.state) {
		return BoldSpan{}, false
	}
	return BoldSpan{h.state.bold}, true
}

// AfterBold binds an authentic native operation to the current history owner.
// Stored fragments survive, while their actual stack effect becomes unknown.
func (h History) AfterBold(r BoldResult) (History, error) {
	a := r.receipt
	if h.state == nil || a == nil || !r.native.valid() ||
		r.native != a.after || r.cursor != a.cursor || h.state.document != a.before {
		return h, failure(InvalidBoldResult, -1, noSpan)
	}
	var format boldState
	switch a.operation {
	case openBold:
		if !h.canOpenBold(a.priorPairs) {
			return h, failure(InvalidBoldResult, -1, noSpan)
		}
		format = boldState{owner: a.after, phase: boldActive, on: r.cursor.gap - 1, off: r.cursor.gap}
	case closeBold:
		if !h.state.bold.matches(a.before) || h.state.bold != a.active {
			return h, failure(InvalidBoldResult, -1, noSpan)
		}
		format = *a.active
		format.phase = boldClosed
	default:
		return h, failure(InvalidBoldResult, -1, noSpan)
	}
	next := *h.state
	next.document = a.after
	next.bold = &format
	next.effectUnqualified = true
	next.groupOpen = false
	next.groupUnknown = false
	next.seedStage = seedUnqualified
	return History{&next}, nil
}

func (h History) canOpenBold(priorPairs int) bool {
	s := h.state
	if s.bold == nil || s.bold.owner != s.document || s.count != 0 || s.observed != nil ||
		s.groupOpen || s.groupUnknown {
		return false
	}
	if priorPairs == 0 {
		return s.bold.phase == boldPristine && h.Qualified() && h.CountKnown()
	}
	return priorPairs == 1 && s.bold.phase == boldClosed && s.effectUnqualified
}

func (s *boldState) afterASCII(a *asciiEditReceipt) (*boldState, error) {
	if s == nil {
		return nil, nil
	}
	if s.phase == boldActive {
		return s.advanceActive(a)
	}
	if s.owner != a.before || a.replaced != 0 {
		return nil, nil
	}
	if s.phase == boldClosed && a.cursor.gap != len(a.after.gaps)-1 {
		return nil, nil
	}
	next := *s
	next.owner = a.after
	return &next, nil
}

func (s *boldState) advanceActive(a *asciiEditReceipt) (*boldState, error) {
	if !s.matches(a.before) || a.replaced != 0 || a.inputLength == 0 ||
		!a.changed || a.cursor.state != a.after {
		return s, failure(InvalidBoldSpan, -1, noSpan)
	}
	nextOff := s.off + a.inputLength
	if a.cursor.gap != nextOff || len(a.after.gaps)-2 != nextOff ||
		len(a.after.gaps)-len(a.before.gaps) != a.inputLength {
		return s, failure(InvalidBoldSpan, a.cursor.gap, noSpan)
	}
	next := *s
	next.owner = a.after
	next.off = nextOff
	next.inserted += a.inputLength
	return &next, nil
}
