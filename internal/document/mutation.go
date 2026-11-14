package document

import (
	"bytes"
)

// Mutation qualification policies, NOT original format limits. Read-only Parse
// retains WP02's 16MiB and WP15's MaxTokens; admission is deliberately narrower.
const (
	MaxMutationBytes  = 65536
	MaxMutationTokens = 16384
	MaxBoldPairs      = 2
)

const (
	RevisionMismatch    Category = "RevisionMismatch"
	MutationLimit       Category = "MutationLimit"
	UnsupportedPrefix   Category = "UnsupportedPrefix"
	UnsupportedResource Category = "UnsupportedResource"
	UnsupportedMetadata Category = "UnsupportedMetadata"
	UnsupportedBody     Category = "UnsupportedBody"
	InvalidASCII        Category = "InvalidASCII"
)

// Revision is an opaque comparable identity, not a content hash. Even separately
// parsed equal bytes have distinct revisions. Its zero value identifies no image.
type Revision struct{ state *revisionState }

func (d *Document) Revision() Revision {
	if !d.valid() {
		return Revision{}
	}
	return Revision{d.state}
}
func (c Cursor) Revision() Revision {
	if !c.state.valid() {
		return Revision{}
	}
	return Revision{c.state}
}

// OriginalExport copies the immutable initially loaded image across all edits.
// New returns explicit NoLoadedOriginal for its entire lifetime. Export instead
// returns this revision's native candidate. Neither performs IO.
func (d *Document) OriginalExport() ([]byte, error) {
	if !d.valid() {
		return nil, failure(InvalidDocument, -1, noSpan)
	}
	if d.state.birth.kind == newBirth {
		return nil, failure(NoLoadedOriginal, -1, noSpan)
	}
	return d.state.birth.originalImage.Export(), nil
}

// EditResult preserves the receiver and incoming cursor on every refusal. No
// partial revision is published. Changed describes a native body change; a
// same-byte typeover only moves its cursor and does not invent metadata dirtiness.
type EditResult struct {
	Document *Document
	Cursor   Cursor
	Changed  bool
	receipt  *asciiEditReceipt
	everyday *everydayReceipt
	merge    *mergeEditReceipt
}

// The receipt is completed before publication and never points at exported
// mutable handles. History can validate actual ASCII transitions without trusting
// fabricated/rebound public result fields or retaining document ancestry chains.
type asciiEditReceipt struct {
	before, after         *revisionState
	cursor                Cursor
	changed               bool
	replaced, inputLength int
}

// CheckMutation checks the full reviewed WP23 prefix/resource/paired-body schema.
// Native parsing alone, a matching prefix size or a fixture digest is insufficient.
func (d *Document) CheckMutation() error { _, e := d.mutationAdmission(); return e }

// InsertASCII receives explicit insert semantics; session mode/key delivery is
// outside this package. Input is WP printable ASCII identity, not Unicode text.
func (d *Document) InsertASCII(c Cursor, text []byte) (EditResult, error) {
	return d.editCharacters(c, text, false, false)
}

// TypeoverASCII is repeated original character typeover: replace the next printable
// token, insert before a code, append at EOF; advance one resulting token gap per
// character. Encountering a code keeps subsequent characters before that code.
func (d *Document) TypeoverASCII(c Cursor, text []byte) (EditResult, error) {
	return d.editCharacters(c, text, true, false)
}

// InsertHardReturn inserts the native paragraph separator at the current gap.
// InsertSoftReturn inserts the observed soft-wrap boundary owner. The layout
// owns decisions about when to create one; this API never synthesizes display text.
func (d *Document) InsertSoftReturn(c Cursor) (EditResult, error) {
	return d.editTokens(c, []byte{softReturnByte})
}

func (d *Document) InsertHardSpace(c Cursor) (EditResult, error) {
	return d.editTokens(c, []byte{0xa0})
}

// InsertTab inserts one complete named Tab owner supplied as exact native bytes.
// It is not a display-string serializer; the caller may not pass arbitrary text.
func (d *Document) InsertTab(c Cursor, owner []byte) (EditResult, error) {
	if identify(owner) != Tab {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	return d.editTokens(c, owner)
}

// InsertHardPage inserts a page boundary. Everyday reflow fills its page cache.
func (d *Document) InsertHardPage(c Cursor) (EditResult, error) {
	return d.editTokens(c, []byte{hardPageByte})
}

func (d *Document) InsertHardReturn(c Cursor) (EditResult, error) {
	return d.editTokens(c, []byte{hardReturnByte})
}

// editTokens appends only a complete already-identified native token. It shares
// the publisher/admission path with character edits so both have the same
// bounds, atomic refusal, prefix policy and format-change receipt.
func (d *Document) editTokens(c Cursor, tokens []byte) (EditResult, error) {
	if identify(tokens) == Opaque {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	return d.insertNamedTokens(c, tokens, 1)
}

func (d *Document) insertNamedTokens(c Cursor, tokens []byte, inserted int) (EditResult, error) {
	return d.insertNamedTokensAt(c, tokens, inserted, inserted)
}

func (d *Document) insertNamedTokensAt(c Cursor, tokens []byte, inserted, advance int) (EditResult, error) {
	unchanged := EditResult{Document: d, Cursor: c}
	if !d.valid() {
		return unchanged, failure(InvalidDocument, -1, noSpan)
	}
	if c.state != d.state {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	if c.gap < 0 || c.gap > d.TokenCount() {
		return unchanged, failure(InvalidPosition, c.gap, noSpan)
	}
	if len(tokens) > MaxMutationTokens {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	_, e := d.mutationAdmission()
	if e != nil {
		return unchanged, e
	}
	raw := d.state.image.Export()
	at := int(d.state.gaps[c.gap])
	start := int(d.state.gaps[0])
	size := len(raw) + len(tokens)
	count := d.TokenCount() + inserted
	if size > MaxMutationBytes || count > MaxMutationTokens {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	body := make([]byte, 0, size-start)
	body = append(body, raw[start:at]...)
	body = append(body, tokens...)
	body = append(body, raw[at:]...)
	edit, e := d.publishBody(c, body, count, c.gap+advance, false)
	if e == nil {
		edit.receipt = &asciiEditReceipt{before: d.state, after: edit.Document.state, cursor: edit.Cursor, changed: edit.Changed, replaced: 0, inputLength: inserted}
	}
	return edit, e
}

func (d *Document) editCharacters(c Cursor, text []byte, over, allowReturn bool) (EditResult, error) {
	unchanged := EditResult{Document: d, Cursor: c}
	if !d.valid() {
		return unchanged, failure(InvalidDocument, -1, noSpan)
	}
	if c.state != d.state {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	// Cursor fields are private, but retain explicit checks before indexing.
	if c.gap < 0 || c.gap > d.TokenCount() {
		return unchanged, failure(InvalidPosition, c.gap, noSpan)
	}
	_, e := d.mutationAdmission()
	if e != nil {
		return unchanged, e
	}
	if len(text) > MaxMutationTokens {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	for i, b := range text {
		if (b < 0x20 || b > 0x7e) && !(allowReturn && b == hardReturnByte) {
			return unchanged, failure(InvalidASCII, i, noSpan)
		}
	}
	if len(text) == 0 {
		unchanged.receipt = &asciiEditReceipt{before: d.state, after: d.state, cursor: c}
		return unchanged, nil
	}
	return d.writeCharacters(c, text, len(text), over)
}

// WriteCharacter inserts or types over one printable native character.
func (d *Document) WriteCharacter(c Cursor, set, number byte, over bool) (EditResult, error) {
	raw := CharacterBytes(set, number)
	if len(raw) == 0 {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	if len(raw) == 1 {
		return d.editCharacters(c, raw, over, false)
	}
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	return d.writeCharacters(c, raw, 1, over)
}

func (d *Document) writeCharacters(c Cursor, text []byte, inputCount int, over bool) (EditResult, error) {
	replaced := 0
	if over {
		for replaced < inputCount && c.gap+replaced < d.TokenCount() {
			token, _ := d.Token(c.gap + replaced)
			if !token.Kind.IsCharacter() {
				break
			}
			replaced++
		}
	}
	return d.replaceCharacters(c, text, inputCount, replaced)
}

// ReplaceSearchSpan replaces printable text and balanced attribute spans.
func (d *Document) ReplaceSearchSpan(c Cursor, end int, text []byte) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	if err := d.checkEverydayCursor(c); err != nil {
		return unchanged, err
	}
	if end <= c.gap || end > d.TokenCount() {
		return unchanged, failure(InvalidPosition, end, noSpan)
	}
	if end == c.gap+1 && len(text) == 0 {
		token, _ := d.Token(c.gap)
		switch token.Kind {
		case BoldOn, BoldOff:
			return d.removeSearchPair(c, BoldAttribute)
		case UnderlineOn, UnderlineOff:
			return d.removeSearchPair(c, UnderlineAttribute)
		}
	}
	var removed, inserted MergeFieldFormatting
	for i := c.gap; i < end; i++ {
		t, _ := d.Token(i)
		switch t.Kind {
		case SoftReturn, DeletedSoftReturn:
			continue
		case EndOfPage:
			group, ok := d.matchedPageGroup(i)
			if ok && (group.kind == SoftPage || group.kind == DeletedSoftPage) && i+group.tokens <= end {
				i += group.tokens - 1
				continue
			}
		}
		if !t.Kind.IsCharacter() && !removed.Apply(t.Raw) {
			return unchanged, failure(UnsupportedBody, i, t.Span)
		}
	}
	if removed.Active() {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	count := 0
	for at := 0; at < len(text); count++ {
		switch {
		case text[at] >= 32 && text[at] <= 126:
			at++
		case at+4 <= len(text) && IsExtendedCharacter(text[at:at+4]):
			at += 4
		case at+3 <= len(text) && inserted.Apply(text[at:at+3]):
			at += 3
		default:
			return unchanged, failure(UnsupportedBody, c.gap, noSpan)
		}
	}
	if inserted.Active() {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	edit, err := d.replaceCharacters(c, text, count, end-c.gap)
	if err == nil {
		if err = edit.Document.CheckMutation(); err != nil {
			return unchanged, err
		}
	}
	return edit, err
}

func (d *Document) replaceCharacters(c Cursor, text []byte, inputCount, replaced int) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	raw := d.state.image.Export()
	start, end := int(d.state.gaps[c.gap]), int(d.state.gaps[c.gap+replaced])
	// Subtraction precedes addition, with input text already bounded.
	size := len(raw) - (end - start) + len(text)
	count := d.TokenCount() - replaced + inputCount
	if size > MaxMutationBytes || count > MaxMutationTokens {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	bodyStart := int(d.state.gaps[0])
	body := make([]byte, 0, size-bodyStart)
	body = append(body, raw[bodyStart:start]...)
	body = append(body, text...)
	body = append(body, raw[end:]...)
	r, e := d.publishBody(c, body, count, c.gap+inputCount, false)
	if e == nil {
		r.receipt = &asciiEditReceipt{before: d.state, after: r.Document.state, cursor: r.Cursor, changed: r.Changed, replaced: replaced, inputLength: inputCount}
	}
	return r, e
}

// The sole semantic candidate publisher. Only domain commands call it, after
// whole-token edits. forceFormat is authorized for confirmed blocked-pair repair;
// no-edit/decline/preview paths never call it. It preserves the owned input prefix
// and applies only checked indexed packet6 bit3, never a template or relocation.
func (d *Document) publishBody(c Cursor, body []byte, tokens, gap int, forceFormat bool) (EditResult, error) {
	return d.publishBodyWithWordRestore(c, body, tokens, gap, forceFormat, false)
}

func (d *Document) publishBodyWithWordRestore(c Cursor, body []byte, tokens, gap int, forceFormat, wordRestore bool) (EditResult, error) {
	unchanged := EditResult{Document: d, Cursor: c}
	if !d.valid() {
		return unchanged, failure(InvalidDocument, -1, noSpan)
	}
	if c.state != d.state {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	flags, e := d.mutationAdmission()
	if e != nil {
		return unchanged, e
	}
	start := int(d.state.gaps[0])
	if tokens < 0 || tokens > MaxMutationTokens || len(body) > MaxMutationBytes-start {
		return unchanged, failure(MutationLimit, gap, noSpan)
	}
	if gap < 0 || gap > tokens {
		return unchanged, failure(InvalidPosition, gap, noSpan)
	}
	raw := d.state.image.Export()
	changed := !bytes.Equal(raw[start:], body)
	cursor := c
	cursor.gap = gap
	if !changed && (!forceFormat || raw[flags]&8 != 0) {
		return EditResult{Document: d, Cursor: cursor}, nil
	}
	candidate := make([]byte, 0, start+len(body))
	candidate = append(candidate, raw[:start]...)
	candidate = append(candidate, body...)
	candidate[flags] = candidate[flags]&^0x10 | 8
	next, e := parseRevision(candidate, d.state.birth)
	if e != nil {
		return unchanged, e
	}
	if next.TokenCount() != tokens {
		return unchanged, failure(InvalidDocument, -1, noSpan)
	}
	if next.needsInitialGeneration() {
		candidate[flags] |= 0x10
		next, e = parseRevision(candidate, d.state.birth)
		if e != nil {
			return unchanged, e
		}
	}
	next.state.openWordRestore = d.state.openWordRestore || wordRestore
	if e = next.CheckMutation(); e != nil {
		return unchanged, e
	}
	cursor.state = next.state
	return EditResult{Document: next, Cursor: cursor, Changed: changed}, nil
}

// removeSearchPair preserves the text and other codes between matching owners.
func (d *Document) removeSearchPair(c Cursor, attribute Attribute) (EditResult, error) {
	on, off := d.pairAt(c.gap, attribute)
	if on < 0 || off <= on {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	raw := d.state.image.Export()
	start := int(d.state.gaps[0])
	body := append([]byte(nil), raw[start:d.state.gaps[on]]...)
	body = append(body, raw[d.state.gaps[on+1]:d.state.gaps[off]]...)
	body = append(body, raw[d.state.gaps[off+1]:]...)
	mapping := make([]int, d.TokenCount())
	next := 0
	for i := range mapping {
		if i == on || i == off {
			mapping[i] = -1
			continue
		}
		mapping[i] = next
		next++
	}
	gap := c.gap
	if gap == off {
		gap--
	}
	return d.publishEveryday(c, body, next, gap, mapping, searchPairEdit)
}
