package document

import (
	"bytes"

	"github.com/lynncoleart/wordling/internal/merge/explicit"
	"github.com/lynncoleart/wordling/internal/merge/native"
)

// MatchMergePrimaryPageCache checks the exact cached Standard Printer owner
// witnessed in the one-line, hard-page merge primary.
func MatchMergePrimaryPageCache(raw []byte) bool {
	return bytes.Equal(raw, everydayPageRecord(1, 0))
}

// NewMergeFragment constructs an ordinary native body from evaluated merge
// text and logical breaks. The destination formatter generates its page caches.
func NewMergeFragment(body []byte) (*Document, error) {
	d, err := New(NewConfig{Profile: HistoricalUS51DosTextStandardPrinter})
	if err != nil {
		return nil, err
	}
	if len(body) > MaxMutationTokens {
		return nil, failure(MutationLimit, -1, noSpan)
	}
	for _, b := range body {
		if !mergeLiteralByte(b) && b != hardPageByte && b != hardReturnByte {
			return nil, failure(InvalidASCII, -1, noSpan)
		}
	}
	cursor, err := d.CursorAt(0)
	if err != nil {
		return nil, err
	}
	result, err := d.publishBody(cursor, body, len(body), len(body), false)
	return result.Document, err
}

func mergeLiteralByte(b byte) bool { return b >= 0x20 && b <= 0x7e }
func editableMergeLiteral(raw []byte) bool {
	for _, b := range raw {
		if !mergeLiteralByte(b) || b == '~' {
			return false
		}
	}
	return true
}

// mergeLiteralSpan recognizes the exact literal ownership of the observed
// one-line primary and explicit-data secondary. It never selects a merge code,
// an operand, an inter-field separator, or a page-cache owner.
func (d *Document) mergeLiteralSpan(raw []byte, at int) (start, end int, ok bool) {
	first := int(d.state.gaps[0])
	body := raw[first:]
	primaryTail := []byte{0xde, 0x36, 4, 0, 4, 0, 0x36, 0xde, '1', '~'}
	if len(body) > len(primaryTail)+33 {
		literal := len(body) - len(primaryTail) - 33
		page := len(body) - 33
		if at >= first && at <= first+literal && bytes.Equal(body[literal:page], primaryTail) &&
			MatchMergePrimaryPageCache(body[page:len(body)-1]) && body[len(body)-1] == hardPageByte &&
			editableMergeLiteral(body[:literal]) {
			return first, first + literal, true
		}
	}
	image, err := native.Parse(raw, native.DefaultLimits())
	if err != nil {
		return 0, 0, false
	}
	view, err := image.View(native.Secondary)
	if err != nil {
		return 0, 0, false
	}
	data, err := explicit.Admit(view, image.Source())
	if err != nil {
		return 0, 0, false
	}
	info, _ := data.Inspect()
	for _, record := range info.Records {
		// The observed editable secondary uses one field per physical line.
		// The explicitly delimited two-field form uses separate lines too.
		for _, field := range record.Fields {
			span, valid := field.Content.Bounds()
			if valid && at >= span.Offset && at <= span.Offset+span.Length &&
				editableMergeLiteral(raw[span.Offset:span.Offset+span.Length]) {
				return span.Offset, span.Offset + span.Length, true
			}
		}
	}
	return 0, 0, false
}

// CheckMergeSource admits the supported merge source for literal editing
// and source-preserving native publication only.
func (d *Document) CheckMergeSource() error {
	if _, err := d.prefixMutationAdmission(); err != nil {
		return err
	}
	raw := d.state.image.Export()
	if _, _, ok := d.mergeLiteralSpan(raw, int(d.state.gaps[0])); !ok && !d.IsAuthoredMergeSource() {
		return failure(UnsupportedBody, -1, noSpan)
	}
	return nil
}

// ExportFormattedMergeSource rewrites the checked resource index exactly as
// the original Fast Save No did for the edited merge sources.
func (d *Document) ExportFormattedMergeSource() ([]byte, error) {
	if err := d.CheckMergeSource(); err != nil {
		return nil, err
	}
	if d.Birth().IsNew() {
		// An original first save keeps the New printer/font packet order
		// and clears the pending-format bit in its current document state.
		flags, err := d.prefixMutationAdmission()
		if err != nil {
			return nil, err
		}
		raw := d.state.image.Export()
		raw[flags] &^= 8
		return raw, nil
	}
	return compactFastSaveCandidate(d.state.image, fastSaveLivePackets(d.state.image)), nil
}

// InsertMergeLiteral inserts printable characters only inside a qualified
// literal. It preserves the exact owned prefix, controls, and formatter caches.
func (d *Document) InsertMergeLiteral(c Cursor, text []byte) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	if !d.valid() {
		return unchanged, failure(InvalidDocument, -1, noSpan)
	}
	if c.state != d.state {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	if c.gap < 0 || c.gap > d.TokenCount() {
		return unchanged, failure(InvalidPosition, c.gap, noSpan)
	}
	if len(text) > MaxMutationTokens {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	if len(text) == 0 || !editableMergeLiteral(text) {
		return unchanged, failure(InvalidASCII, c.gap, noSpan)
	}
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return unchanged, err
	}
	raw := d.state.image.Export()
	if len(text) > MaxMutationBytes-len(raw) || len(text) > MaxMutationTokens-d.TokenCount() {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	at := int(d.state.gaps[c.gap])
	start, end, ok := d.mergeLiteralSpan(raw, at)
	if !ok {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	// Keep the source line and its inline code within the standard
	// 65-column text area so the owned formatter record stays valid.
	const literalColumns = 65 - len("{END FIELD}")
	if end-start+len(text) > literalColumns {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	candidate := make([]byte, 0, len(raw)+len(text))
	candidate = append(candidate, raw[:at]...)
	candidate = append(candidate, text...)
	candidate = append(candidate, raw[at:]...)
	candidate[flags] |= 8
	next, err := parseRevision(candidate, d.state.birth)
	if err != nil {
		return unchanged, err
	}
	if _, _, ok := next.mergeLiteralSpan(candidate, at+len(text)); !ok || next.TokenCount() != d.TokenCount()+len(text) {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	c.gap += len(text)
	c.state = next.state
	return EditResult{Document: next, Cursor: c, Changed: true}, nil
}

// MergeSaveProfile retains the immutable primary's exact prefix ownership.
// Body semantics are checked by the merge compiler before this is acquired.
type MergeSaveProfile struct {
	primary *revisionState
	middle  int
}

type MergeSaveOptions struct {
	FastSave bool
	Occupied bool
	AtEnd    bool
	Edited   bool
	Purged   bool
}

func (d *Document) MergeSaveProfile() (MergeSaveProfile, error) {
	if !d.valid() {
		return MergeSaveProfile{}, failure(InvalidDocument, -1, noSpan)
	}
	compact := d
	info := d.state.image.Inspect()
	middle := 272
	switch info.Prefix.Length {
	case compactFastSavePrefixBytes:
		if len(info.Packets) != 0 && info.Packets[0].Type == 7 {
			middle = 270
		}
	case fastSavePrefixBytes:
		var err error
		compact, err = d.compactFastSavePrefix()
		if err != nil {
			return MergeSaveProfile{}, err
		}
	default:
		return MergeSaveProfile{}, failure(UnsupportedPrefix, -1, info.Prefix)
	}
	if _, err := compact.prefixMutationAdmission(); err != nil {
		return MergeSaveProfile{}, err
	}
	return MergeSaveProfile{primary: d.state, middle: middle}, nil
}

// ExportMergeResult applies the primary's observed Fast Save generation to
// the checked receiver's ordinary body. The receiver owns the output body,
// and the primary contributes only matching Standard Printer resources.
func (d *Document) ExportMergeResult(profile MergeSaveProfile, options MergeSaveOptions) ([]byte, error) {
	if err := d.CheckMutation(); err != nil {
		return nil, err
	}
	if !profile.primary.valid() {
		return nil, failure(InvalidDocument, -1, noSpan)
	}
	image := d.state.image
	live, prior := fastSaveLivePackets(image), fastSaveLivePackets(profile.primary.image)
	if err := checkFastSaveResources(live, prior, image.Inspect().Prefix); err != nil {
		return nil, err
	}
	// In the original, insertion at EOF completes the formatting pass
	// immediately. Insertion before existing text leaves that work pending.
	formatted := options.AtEnd && !options.Edited
	if options.Purged {
		return compactFastSaveResult(image, live, options.FastSave && !formatted), nil
	}
	if options.Occupied && d.Birth().IsNew() {
		// Inserting into an occupied New buffer keeps its live packet
		// order, including the active format state when still pending.
		raw := image.Export()
		if !options.FastSave || formatted {
			flags, err := d.prefixMutationAdmission()
			if err != nil {
				return nil, err
			}
			raw[flags] &^= 8
		}
		return raw, nil
	}
	if !options.FastSave {
		return compactFastSaveCandidate(image, live), nil
	}
	if options.Occupied {
		return d.exportLoadedFastSave(true, formatted)
	}
	active := bytes.Clone(prior[6])
	active[0] &^= 8
	if options.Edited {
		active[0] |= live[6][0] & 8
	}
	return d.encodeFastSave(live, prior, profile.middle, active)
}
