package document

import "bytes"

// AdoptReflow publishes one validated layout boundary change to the same native
// document.  It is intentionally narrower than the generic editor body publisher:
// the caller may not create arbitrary body bytes and must derive them from an
// approved layout plan.  This preserves unrelated opaque prefix/body data.
func (d *Document) AdoptReflow(c Cursor, body []byte) (EditResult, error) {
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
	if _, e := d.mutationAdmission(); e != nil {
		return unchanged, e
	}
	start := int(d.state.gaps[0])
	if len(body) > MaxMutationBytes-start || len(body) < 0 {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	// The layout caller owns the current line/page plan.  The publisher owns only
	// the native body bytes: it preserves the prefix and does not invent or
	// serialize display text.
	return d.publishBody(c, bytes.Clone(body), d.TokenCount(), c.gap, false)
}
