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
type Revision struct{ document *Document }

func (d *Document) Revision() Revision {
	if !d.valid() {
		return Revision{}
	}
	return Revision{d}
}
func (c Cursor) Revision() Revision { return c.document.Revision() }

// OriginalExport copies the immutable initially loaded image across all edits.
// Export instead returns this revision's native candidate. Neither performs IO.
func (d *Document) OriginalExport() ([]byte, error) {
	if !d.valid() {
		return nil, failure(InvalidDocument, -1, noSpan)
	}
	return d.original.Export(), nil
}

// EditResult preserves the receiver and incoming cursor on every refusal. No
// partial revision is published. Changed describes a native body change; a
// same-byte typeover only moves its cursor and does not invent metadata dirtiness.
type EditResult struct {
	Document *Document
	Cursor   Cursor
	Changed  bool
}

// CheckMutation checks the full reviewed WP23 prefix/resource/paired-body schema.
// Native parsing alone, a matching prefix size or a fixture digest is insufficient.
func (d *Document) CheckMutation() error { _, e := d.mutationAdmission(); return e }

// InsertASCII receives explicit insert semantics; session mode/key delivery is
// outside this package. Input is WP printable ASCII identity, not Unicode text.
func (d *Document) InsertASCII(c Cursor, text []byte) (EditResult, error) {
	return d.editASCII(c, text, false)
}

// TypeoverASCII is repeated original character typeover: replace the next ASCII
// token, insert before a code, append at EOF; advance one resulting token gap per
// character. Encountering a code keeps subsequent characters before that code.
func (d *Document) TypeoverASCII(c Cursor, text []byte) (EditResult, error) {
	return d.editASCII(c, text, true)
}

func (d *Document) editASCII(c Cursor, text []byte, over bool) (EditResult, error) {
	unchanged := EditResult{Document: d, Cursor: c}
	if !d.valid() {
		return unchanged, failure(InvalidDocument, -1, noSpan)
	}
	if c.document != d {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	// Cursor fields are private, but retain explicit checks before indexing.
	if c.gap < 0 || c.gap > d.TokenCount() {
		return unchanged, failure(InvalidPosition, c.gap, noSpan)
	}
	flags, e := d.mutationAdmission()
	if e != nil {
		return unchanged, e
	}
	if len(text) > MaxMutationTokens {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	for i, b := range text {
		if b < 0x20 || b > 0x7e {
			return unchanged, failure(InvalidASCII, i, noSpan)
		}
	}
	if len(text) == 0 {
		return unchanged, nil
	}
	raw := d.image.Export()
	start := int(d.gaps[c.gap])
	end := start
	replaced := 0
	if over {
		for replaced < len(text) && c.gap+replaced < d.TokenCount() {
			span := d.span(c.gap + replaced)
			if identify(raw[span.Offset:span.Offset+span.Length]) != ASCII {
				break
			}
			end += span.Length
			replaced++
		}
	}
	// Subtraction precedes addition, with input text already bounded.
	size := len(raw) - (end - start) + len(text)
	count := d.TokenCount() - replaced + len(text)
	if size > MaxMutationBytes || count > MaxMutationTokens {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	cursor := c
	cursor.gap += len(text)
	if bytes.Equal(raw[start:end], text) {
		return EditResult{d, cursor, false}, nil
	}
	candidate := make([]byte, 0, size)
	candidate = append(candidate, raw[:start]...)
	candidate = append(candidate, text...)
	candidate = append(candidate, raw[end:]...)
	candidate[flags] |= 8 // checked indexed packet6 bit3 only; owned input prefix.
	next, e := Parse(candidate)
	if e != nil {
		return unchanged, e
	}
	if e = next.CheckMutation(); e != nil {
		return unchanged, e
	}
	next.original = d.original
	cursor.document = next
	return EditResult{next, cursor, true}, nil
}
