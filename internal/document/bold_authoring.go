package document

import "github.com/lynncoleart/wordling/internal/wp51"

type Attribute uint8

const (
	BoldAttribute Attribute = iota + 1
	UnderlineAttribute
)

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

	// The WP78 corrected-source capture stores Underline in its own balanced
	// three-byte pair. Bold and Underline flags are independent.
	nativeUnderlineOn  = "\xc3\x0e\xc3"
	nativeUnderlineOff = "\xc4\x0e\xc4"
	underlinePairBytes = len(nativeUnderlineOn) + len(nativeUnderlineOff)
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
	owner     *revisionState
	attribute Attribute
	phase     boldPhase
	on, off   int
	inserted  int
}

// Attribute identifies the one native paired format this state owns.
func (s *boldState) attributeKind() (Kind, Kind) {
	switch s.attribute {
	case BoldAttribute:
		return BoldOn, BoldOff
	case UnderlineAttribute:
		return UnderlineOn, UnderlineOff
	}
	return Opaque, Opaque
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
	attribute     Attribute
	active        *boldState
	everyday      bool
	tokenMap      []int
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
	return d.formatOrigin(flagOffset, BoldAttribute)
}

func (d *Document) formatOrigin(flagOffset int, attribute Attribute) *boldState {
	if !d.Birth().IsNew() || d.TokenCount() != 0 {
		return nil
	}
	flag, ok := d.state.image.Bytes(wp51.Span{Offset: flagOffset, Length: 1})
	// New has a clear format-change bit. The existing publisher sets it on
	// every body change, including an edit that later returns to empty.
	if !ok || flag[0]&8 != 0 {
		return nil
	}
	return &boldState{owner: d.state, attribute: attribute, phase: boldPristine}
}

// BeginBold appends one balanced native pair and leaves the cursor before Off.
// History separately qualifies the constructor or prior closed-span lineage.
func (d *Document) BeginBold(c Cursor) (BoldResult, error) {
	return d.beginFormat(c, BoldAttribute, false)
}

func (d *Document) CloseBold(c Cursor, active BoldSpan) (BoldResult, error) {
	return d.closeFormat(c, active, BoldAttribute)
}

func (h History) ActiveBold(d *Document) (BoldSpan, bool) {
	return h.activeFormat(d, BoldAttribute)
}

func (h History) AfterBold(r BoldResult) (History, error) {
	return h.afterFormat(r)
}

// BeginUnderline/CloseUnderline use the same immutable native pair semantics as
// Bold. The two attributed flags have independent state and may overlap.
func (d *Document) BeginUnderline(c Cursor) (BoldResult, error) {
	return d.beginFormat(c, UnderlineAttribute, false)
}

func (d *Document) CloseUnderline(c Cursor, active BoldSpan) (BoldResult, error) {
	return d.closeFormat(c, active, UnderlineAttribute)
}

func (h History) ActiveUnderline(d *Document) (BoldSpan, bool) {
	return h.activeFormat(d, UnderlineAttribute)
}

func (h History) AfterUnderline(r BoldResult) (History, error) {
	return h.afterFormat(r)
}

func (d *Document) beginFormat(c Cursor, attribute Attribute, everyday bool) (BoldResult, error) {

	unchanged := d.boldRefusal(c)
	if !d.valid() || c.state != d.state ||
		c.gap < 0 || c.gap > d.TokenCount() || c.reveal && !everyday {
		return unchanged, failure(UnsupportedBoldContext, c.gap, noSpan)
	}
	if err := d.CheckMutation(); err != nil {
		return unchanged, err
	}
	count := d.TokenCount()
	end := int(d.state.gaps[count])
	pairBytes := boldPairBytes
	var on, off string
	switch attribute {
	case BoldAttribute:
		on, off = nativeBoldOn, nativeBoldOff
	case UnderlineAttribute:
		on, off = nativeUnderlineOn, nativeUnderlineOff
		pairBytes = underlinePairBytes
	default:
		return unchanged, failure(UnsupportedBoldContext, c.gap, noSpan)
	}
	if count > MaxMutationTokens-2 || end > MaxMutationBytes-pairBytes {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	at := int(d.state.gaps[c.gap])
	raw := d.state.image.Export()
	prior, err := d.formatOpenPairs(raw, attribute)
	if err != nil {
		return unchanged, err
	}
	body := make([]byte, 0, end-int(d.state.gaps[0])+pairBytes)
	body = append(body, raw[d.state.gaps[0]:at]...)
	body = append(body, on...)
	body = append(body, off...)
	body = append(body, raw[at:]...)
	edit, err := d.publishBody(c, body, count+2, c.gap+1, false)
	if err != nil {
		return unchanged, err
	}
	receipt := &boldReceipt{before: d.state, after: edit.Document.state, cursor: edit.Cursor,
		operation: openBold, priorPairs: prior, attribute: attribute, everyday: everyday}
	if everyday {
		receipt.tokenMap = insertionTokenMap(count, c.gap, 2)
	}
	return BoldResult{native: receipt.after, cursor: receipt.cursor, receipt: receipt}, nil
}

func (d *Document) boldOpenPairs(raw []byte) (int, error) {
	return d.formatOpenPairs(raw, BoldAttribute)
}

func (d *Document) formatOpenPairs(raw []byte, attribute Attribute) (int, error) {
	pairs := 0
	on := BoldOn
	if attribute == UnderlineAttribute {
		on = UnderlineOn
	}
	for i := range d.TokenCount() {
		span := d.span(i)
		if identify(raw[span.Offset:span.Offset+span.Length]) == on {
			pairs++
		}
	}
	return pairs, nil
}

// closeFormat crosses the existing Off for the supplied attribute. The file,
// native revision and bytes remain identical. Only History.afterFormat records
// consumption of this span.
func (d *Document) closeFormat(c Cursor, active BoldSpan, attribute Attribute) (BoldResult, error) {
	unchanged := d.boldRefusal(c)
	if !d.valid() || c.state != d.state {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	s := active.state
	if !s.matches(d.state) || s.attribute != attribute {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	if c.gap != s.off || s.on < 0 || s.on >= s.off ||
		s.inserted != s.off-s.on-1 {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	if err := d.CheckMutation(); err != nil {
		return unchanged, err
	}
	on, _ := d.Token(s.on)
	off, _ := d.Token(s.off)
	wantOn, wantOff := s.attributeKind()
	if on.Kind != wantOn || off.Kind != wantOff {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	if s.inserted == 0 {
		return unchanged, failure(EmptyBoldSpan, c.gap, noSpan)
	}
	c.gap++
	receipt := &boldReceipt{before: d.state, after: d.state, cursor: c, operation: closeBold, active: s, attribute: attribute}
	return BoldResult{native: d.state, cursor: c, receipt: receipt}, nil
}

func (h History) activeFormat(d *Document, attribute Attribute) (BoldSpan, bool) {
	if h.state == nil || !d.valid() || h.state.document != d.state {
		return BoldSpan{}, false
	}
	s := h.state.format(attribute)
	if !s.matches(d.state) || s.attribute != attribute {
		return BoldSpan{}, false
	}
	return BoldSpan{s}, true
}

func (h History) afterFormat(r BoldResult) (History, error) {
	a := r.receipt
	if h.state == nil || a == nil || a.everyday || !r.native.valid() ||
		r.native != a.after || r.cursor != a.cursor || h.state.document != a.before {
		return h, failure(InvalidBoldResult, -1, noSpan)
	}
	var format boldState
	next := *h.state
	switch a.operation {
	case openBold:
		current := next.format(a.attribute)
		if !h.canOpenFormat(a.priorPairs, current) {
			return h, failure(InvalidBoldResult, -1, noSpan)
		}
		format = boldState{owner: a.after, attribute: a.attribute, phase: boldActive, on: r.cursor.gap - 1, off: r.cursor.gap}
		next.setFormat(a.attribute, &format)
	case closeBold:
		current := next.format(a.attribute)
		if !current.matches(a.before) || current != a.active || current.attribute != a.attribute {
			return h, failure(InvalidBoldResult, -1, noSpan)
		}
		format = *a.active
		format.phase = boldClosed
		next.setFormat(a.attribute, &format)
	default:
		return h, failure(InvalidBoldResult, -1, noSpan)
	}
	next.document = a.after
	next.effectUnqualified = true
	next.groupOpen = false
	next.groupUnknown = false
	next.seedStage = seedUnqualified
	if a.operation == openBold {
		for _, attribute := range []Attribute{BoldAttribute, UnderlineAttribute} {
			if attribute == a.attribute {
				continue // The newly opened pair owns this format; do not shift it.
			}
			state := next.format(attribute)
			if state != nil && state.owner == a.before {
				fresh := *state
				fresh.owner = a.after
				if state.phase == boldActive {
					fresh.off += 2
					fresh.inserted += 2
				}
				next.setFormat(attribute, &fresh)
			}
		}
	}
	return History{&next}, nil
}

func (h History) canOpenFormat(priorPairs int, current *boldState) bool {
	s := h.state
	doc := &Document{state: s.document}
	if current != nil {
		if current.owner != nil && current.owner != s.document || current.phase == boldActive ||
			current.phase == boldPristine && (s.count != 0 || s.observed != nil || s.groupOpen ||
				s.groupUnknown) {
			return false
		}
	}
	if s.count != 0 || s.observed != nil || s.groupOpen || s.groupUnknown {
		return false
	}
	// Loaded/saved documents may start an untracked pair at EOF. A New lineage is
	// not implicitly rearmable after deletion and retains the closed-state rule.
	if current == nil {
		if !doc.Birth().IsNew() {
			return h.Qualified() && h.CountKnown()
		}
		return false
	}
	// A closed pair may become an unqualified prior pair for repeated authoring.
	return true
}

func (s *boldState) matches(owner *revisionState) bool {
	return s != nil && s.phase == boldActive && s.owner == owner
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
	shiftToken := len(a.after.gaps) - len(a.before.gaps)
	if shiftToken != a.inputLength {
		return s, failure(InvalidBoldSpan, a.cursor.gap, noSpan)
	}
	originalGap := a.cursor.gap - shiftToken
	if originalGap >= s.on && originalGap <= s.off {
		next := *s
		next.owner = a.after
		next.off += shiftToken
		next.inserted += shiftToken
		return &next, nil
	}
	return nil, nil
}
