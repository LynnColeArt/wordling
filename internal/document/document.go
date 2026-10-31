// Package document exposes immutable native revisions and shared normal/Reveal
// token gaps. Semantic writes require the narrower WP23 mutation admission.
package document

import (
	"encoding/binary"
	"fmt"

	"github.com/lynncoleart/wordling/internal/wp51"
)

// Safety policies, not original application limits. The gap index is at most
// (MaxTokens+1)*4 bytes; a presentation allocates at most MaxWindowTokens elements.
const (
	MaxTokens       = 1 << 20
	MaxWindowTokens = 4096
)

type Category string

const (
	InvalidDocument  Category = "InvalidDocument"
	InvalidPosition  Category = "InvalidPosition"
	InvalidDirection Category = "InvalidDirection"
	TokenLimit       Category = "TokenLimit"
	WindowLimit      Category = "WindowLimit"
	UnsupportedToken Category = "UnsupportedToken"
)

// Failure identifies a document refusal. Native-reader errors pass through with
// their original *wp51.Failure type. A negative index/span denotes no token.
type Failure struct {
	Category   Category
	TokenIndex int
	Span       wp51.Span
}

func (e *Failure) Error() string {
	return fmt.Sprintf("document: %s at token %d, span %d+%d", e.Category, e.TokenIndex, e.Span.Offset, e.Span.Length)
}
func failure(k Category, index int, span wp51.Span) error { return &Failure{k, index, span} }

var noSpan = wp51.Span{Offset: -1}

type Kind uint8

const (
	Opaque Kind = iota
	ASCII
	BoldOn
	BoldOff
)

// Token is an independent inspection value. Raw always retains the exact native
// bytes, even for an opaque token whose movement/presentation is unsupported.
type Token struct {
	Kind Kind
	Span wp51.Span
	Raw  []byte
}

// Document must be constructed by Parse or New. It retains one immutable dependency
// image and a compact private absolute-gap index, with no mutable document state.
type Document struct{ state *revisionState }

// A caller may copy or replace the exported Document wrapper. Cursor and
// Revision capture this private immutable state, never that mutable wrapper.
// No state pointer, image pointer or gap slice is exposed to callers.
type revisionState struct {
	image *wp51.Image
	gaps  []uint32
	birth *birthLineage
}

func (s *revisionState) valid() bool {
	return s != nil && s.image != nil && s.birth != nil && len(s.gaps) > 0
}

// Parse delegates all native validity decisions to the approved reader. The
// following indexing pass only locates already-validated token spans; it does not
// decode opaque payloads, nested text, paired-code relationships or edit safety.
func Parse(input []byte) (*Document, error) { return parseRevision(input, nil) }

// One native parser/indexer. A nil birth means an explicit Loaded acquisition;
// internal validation and New supply their captured immutable lineage.
func parseRevision(input []byte, birth *birthLineage) (*Document, error) {
	image, err := wp51.Parse(input)
	if err != nil {
		return nil, err
	}
	info := image.Inspect()
	if info.OuterTokenCount > MaxTokens {
		return nil, failure(TokenLimit, -1, info.Body)
	}
	body, _ := image.Bytes(info.Body)
	gaps := make([]uint32, info.OuterTokenCount+1)
	offset := 0
	for i := 0; i < info.OuterTokenCount; i++ {
		gaps[i] = uint32(info.Body.Offset + offset)
		offset += framedWidth(body[offset:])
	}
	gaps[len(gaps)-1] = uint32(info.Body.Offset + len(body))
	if birth == nil {
		birth = &birthLineage{kind: loadedBirth, originalImage: image}
	}
	return &Document{state: &revisionState{image: image, gaps: gaps, birth: birth}}, nil
}

// These SDK WP51 outer-width facts are used only after wp51.Parse has checked
// every delimiter/length/bound. Reusing their span lengths is not another native
// validator or permission to interpret payloads. In particular C0 remains opaque.
func framedWidth(raw []byte) int {
	lead := raw[0]
	if lead < 0xc0 {
		return 1
	}
	if lead < 0xd0 {
		return [...]int{4, 9, 11, 3, 3, 5, 6, 7, 4, 5, 6, 6, 8, 10, 10, 12}[lead-0xc0]
	}
	return int(binary.LittleEndian.Uint16(raw[2:4])) + 4
}
func identify(raw []byte) Kind {
	if len(raw) == 1 && raw[0] >= 0x20 && raw[0] <= 0x7e {
		return ASCII
	}
	if len(raw) == 3 && raw[1] == 0x0c && raw[0] == raw[2] {
		if raw[0] == 0xc3 {
			return BoldOn
		}
		if raw[0] == 0xc4 {
			return BoldOff
		}
	}
	return Opaque
}
func (d *Document) valid() bool { return d != nil && d.state.valid() }
func (d *Document) TokenCount() int {
	if !d.valid() {
		return 0
	}
	return len(d.state.gaps) - 1
}
func (d *Document) Export() ([]byte, error) {
	if !d.valid() {
		return nil, failure(InvalidDocument, -1, noSpan)
	}
	return d.state.image.Export(), nil
}
func (d *Document) span(index int) wp51.Span {
	return wp51.Span{Offset: int(d.state.gaps[index]), Length: int(d.state.gaps[index+1] - d.state.gaps[index])}
}
func (d *Document) Token(index int) (Token, error) {
	if !d.valid() {
		return Token{}, failure(InvalidDocument, index, noSpan)
	}
	if index < 0 || index >= d.TokenCount() {
		return Token{}, failure(InvalidPosition, index, noSpan)
	}
	span := d.span(index)
	raw, _ := d.state.image.Bytes(span)
	return Token{Kind: identify(raw), Span: span, Raw: raw}, nil
}

// Cursor is a value: view and movement operations return a new cursor, preserving
// the caller's previous cursor on failure. Its document remains immutable.
type Cursor struct {
	state  *revisionState
	gap    int
	reveal bool
}

// CursorAt constructs a valid token-gap coordinate, not an original GoTo/Home
// command. Zero and TokenCount are the body boundaries, never byte positions.
func (d *Document) CursorAt(gap int) (Cursor, error) {
	if !d.valid() {
		return Cursor{}, failure(InvalidDocument, -1, noSpan)
	}
	if gap < 0 || gap > d.TokenCount() {
		return Cursor{}, failure(InvalidPosition, gap, noSpan)
	}
	return Cursor{state: d.state, gap: gap}, nil
}
func (c Cursor) Gap() int                    { return c.gap }
func (c Cursor) Reveal() bool                { return c.reveal }
func (c Cursor) WithReveal(show bool) Cursor { c.reveal = show; return c }
func (c Cursor) Offset() (int, error) {
	if !c.state.valid() {
		return 0, failure(InvalidDocument, -1, noSpan)
	}
	return int(c.state.gaps[c.gap]), nil
}
func (c Cursor) Move(direction int) (Cursor, error) {
	d := &Document{state: c.state}
	if !c.state.valid() {
		return c, failure(InvalidDocument, -1, noSpan)
	}
	if direction != -1 && direction != 1 {
		return c, failure(InvalidDirection, c.gap, noSpan)
	}
	target := c.gap + direction
	if target < 0 || target > d.TokenCount() {
		return c, failure(InvalidPosition, target, noSpan)
	}
	index := c.gap
	if direction < 0 {
		index--
	}
	token, _ := d.Token(index)
	if token.Kind == Opaque {
		return c, failure(UnsupportedToken, index, token.Span)
	}
	c.gap = target
	return c, nil
}

// Element preserves source/token identity in both views, including the empty
// normal text of Bold codes. Text is derived display, never native serialization.
type Element struct {
	TokenIndex int
	Kind       Kind
	Span       wp51.Span
	Text       string
}
type Presentation struct {
	StartGap, EndGap, CursorGap int
	Reveal                      bool
	Elements                    []Element
}

// Present renders a bounded token window, refusing an opaque token before
// returning any elements. It does not wrap, count terminal cells or infer layout.
func (c Cursor) Present(start, count int) (Presentation, error) {
	d := &Document{state: c.state}
	if !d.valid() {
		return Presentation{}, failure(InvalidDocument, -1, noSpan)
	}
	if start < 0 || start > d.TokenCount() || count < 0 || count > d.TokenCount()-start {
		return Presentation{}, failure(InvalidPosition, start, noSpan)
	}
	if count > MaxWindowTokens {
		return Presentation{}, failure(WindowLimit, start, noSpan)
	}
	// Acquire only the requested contiguous window, not the full body. Indexes
	// already identify valid complete-token spans, so this remains input bounded.
	window := wp51.Span{Offset: int(d.state.gaps[start]), Length: int(d.state.gaps[start+count] - d.state.gaps[start])}
	raw, _ := d.state.image.Bytes(window)
	for i := start; i < start+count; i++ {
		span := d.span(i)
		local := span.Offset - window.Offset
		if identify(raw[local:local+span.Length]) == Opaque {
			return Presentation{}, failure(UnsupportedToken, i, span)
		}
	}
	p := Presentation{StartGap: start, EndGap: start + count, CursorGap: c.gap, Reveal: c.reveal, Elements: make([]Element, count)}
	for i := start; i < start+count; i++ {
		span := d.span(i)
		local := span.Offset - window.Offset
		token := raw[local : local+span.Length]
		kind := identify(token)
		text := ""
		if kind == ASCII {
			text = string(token)
		} else if c.reveal {
			if kind == BoldOn {
				text = "[BOLD]"
			} else {
				text = "[bold]"
			}
		}
		p.Elements[i-start] = Element{TokenIndex: i, Kind: kind, Span: span, Text: text}
	}
	return p, nil
}
