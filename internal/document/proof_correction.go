package document

import "strings"

// MaxProofWordBytes bounds one checked spelling correction. The original
// processes at most 64 characters of the witnessed unbroken-word suspect.
const MaxProofWordBytes = 64

// ReplaceProofWord replaces the exact spelling within an owned token range.
// The range starts and ends with glyph owners. Enclosing attribute owners
// remain outside it; interior attribute owners move to the replacement's end
// in native order. No ordinary whitespace or explicit page is consumed.
func (d *Document) ReplaceProofWord(start, end Cursor, expected, replacement string) (EditResult, error) {
	if err := d.checkProofRange(start, end); err != nil {
		return unchangedEdit(d, start), err
	}
	if !validProofWord(expected) || !validProofWord(replacement) {
		return unchangedEdit(d, start), failure(InvalidASCII, start.gap, noSpan)
	}
	if a, _ := d.Token(start.gap); a.Kind != ASCII {
		return unchangedEdit(d, start), failure(UnsupportedBody, start.gap, a.Span)
	}
	if z, _ := d.Token(end.gap - 1); z.Kind != ASCII {
		return unchangedEdit(d, start), failure(UnsupportedBody, end.gap-1, z.Span)
	}
	var attributes []int
	letter := 0
	for i := start.gap; i < end.gap; i++ {
		t, _ := d.Token(i)
		switch t.Kind {
		case ASCII:
			if letter >= len(expected) || t.Raw[0] != expected[letter] {
				return unchangedEdit(d, start), failure(UnsupportedBody, i, t.Span)
			}
			letter++
		case BoldOn, BoldOff, UnderlineOn, UnderlineOff:
			attributes = append(attributes, i)
		case DeletedSoftReturn:
			// A derived line boundary does not separate the word.
		case EndOfPage:
			group, ok := d.matchedPageGroup(i)
			if !ok || group.kind != DeletedSoftPage || i+group.tokens > end.gap {
				return unchangedEdit(d, start), failure(UnsupportedBody, i, t.Span)
			}
			i += group.tokens - 1
		default:
			return unchangedEdit(d, start), failure(UnsupportedBody, i, t.Span)
		}
	}
	if letter != len(expected) {
		return unchangedEdit(d, start), failure(UnsupportedBody, start.gap, noSpan)
	}
	// A proof range owns a complete word, except for the original first-64
	// processing cap. Even a capped range must begin at the real word start.
	if d.proofContinues(start.gap-1, -1) ||
		len(expected) < MaxProofWordBytes && d.proofContinues(end.gap, 1) {
		return unchangedEdit(d, start), failure(UnsupportedBody, start.gap, noSpan)
	}
	if replacement == expected {
		return d.everydayNoOp(start, proofEdit), nil
	}
	return d.publishProofCorrection(start, start.gap, end.gap, replacement, attributes)
}

// DeleteProofDuplicate implements the observed plain Double Word correction.
// It checks both complete spellings and the run of ASCII spaces between them.
// It removes the second word and the nearest preceding space, leaving all
// other spaces and surrounding owners in their original order.
func (d *Document) DeleteProofDuplicate(start, end Cursor, previous, expected string) (EditResult, error) {
	if err := d.checkProofRange(start, end); err != nil {
		return unchangedEdit(d, start), err
	}
	if !validProofWord(previous) || !validProofWord(expected) || !strings.EqualFold(previous, expected) {
		return unchangedEdit(d, start), failure(InvalidASCII, start.gap, noSpan)
	}
	separation := start.gap
	for separation > 0 {
		token, _ := d.Token(separation - 1)
		if token.Kind != ASCII || token.Raw[0] != ' ' {
			break
		}
		separation--
	}
	before := separation - len(previous)
	if separation == start.gap || before < 0 || end.gap-start.gap != len(expected) ||
		!d.proofBoundary(before-1) || !d.proofBoundary(end.gap) {
		return unchangedEdit(d, start), failure(UnsupportedBody, start.gap, noSpan)
	}
	for _, part := range []struct {
		start int
		word  string
	}{{before, previous}, {start.gap, expected}} {
		for offset := range len(part.word) {
			i := part.start + offset
			t, _ := d.Token(i)
			if t.Kind != ASCII || t.Raw[0] != part.word[offset] {
				return unchangedEdit(d, start), failure(UnsupportedBody, i, t.Span)
			}
		}
	}
	return d.publishProofCorrection(start, start.gap-1, end.gap, "", nil)
}

func (d *Document) checkProofRange(start, end Cursor) error {
	if err := d.checkEverydayCursor(start); err != nil {
		return err
	}
	if end.state != start.state {
		return failure(RevisionMismatch, end.gap, noSpan)
	}
	if end.gap <= start.gap || end.gap > d.TokenCount() || end.reveal != start.reveal {
		return failure(InvalidPosition, end.gap, noSpan)
	}
	return nil
}

func proofLetter(c byte) bool {
	return c >= 'a' && c <= 'z' || c >= 'A' && c <= 'Z'
}

func validProofWord(word string) bool {
	if len(word) == 0 || len(word) > MaxProofWordBytes || !proofLetter(word[0]) || !proofLetter(word[len(word)-1]) {
		return false
	}
	for i := 1; i+1 < len(word); i++ {
		if !proofLetter(word[i]) && (word[i] != '\'' || !proofLetter(word[i-1]) || !proofLetter(word[i+1])) {
			return false
		}
	}
	return true
}

// proofNeighbor observes one lexical neighbor across formatting and derived
// no-separator boundaries. It never crosses a space-bearing or explicit page.
func (d *Document) proofNeighbor(index, step int) (byte, int) {
	for index >= 0 && index < d.TokenCount() {
		t, _ := d.Token(index)
		switch t.Kind {
		case ASCII:
			return t.Raw[0], index + step
		case BoldOn, BoldOff, UnderlineOn, UnderlineOff, DeletedSoftReturn, DeletedSoftPage:
			// These qualified native owners do not separate a word.
		case EndOfPage:
			group, ok := d.matchedPageGroup(index)
			if !ok || group.kind != DeletedSoftPage {
				return 0, index
			}
		default:
			return 0, index
		}
		index += step
	}
	return 0, index
}

func (d *Document) proofContinues(index, step int) bool {
	c, next := d.proofNeighbor(index, step)
	if proofLetter(c) || c >= '0' && c <= '9' {
		return true
	}
	if c == '\'' {
		// Only an internal apostrophe extends the word. A quote next to
		// the word, followed by a boundary or EOF, is punctuation.
		after, _ := d.proofNeighbor(next, step)
		return proofLetter(after)
	}
	return false
}

func (d *Document) proofBoundary(index int) bool {
	if index < 0 || index >= d.TokenCount() {
		return true
	}
	t, _ := d.Token(index)
	switch t.Kind {
	case HardReturn, SoftReturn, Tab, HardPage, SoftPage, HardReturnSoftPage:
		return true
	case ASCII:
		c := t.Raw[0]
		return !proofLetter(c) && c != '\'' && !(c >= '0' && c <= '9')
	default:
		return false
	}
}

func (d *Document) publishProofCorrection(c Cursor, start, end int, replacement string, attributes []int) (EditResult, error) {
	added := len(replacement) + len(attributes)
	count := d.TokenCount() - (end - start) + added
	raw := d.state.image.Export()
	bodyStart, lo, hi := int(d.state.gaps[0]), int(d.state.gaps[start]), int(d.state.gaps[end])
	attrBytes := 0
	for _, i := range attributes {
		attrBytes += int(d.state.gaps[i+1] - d.state.gaps[i])
	}
	size := len(raw) - (hi - lo) + len(replacement) + attrBytes
	if size > MaxMutationBytes || count > MaxMutationTokens {
		return unchangedEdit(d, c), failure(MutationLimit, start, noSpan)
	}

	// This map names only surviving owners. Interior format anchors retain
	// their exact code bytes and identity even when the spelling changes size.
	tokenMap := make([]int, d.TokenCount())
	for i := range tokenMap {
		switch {
		case i < start:
			tokenMap[i] = i
		case i >= end:
			tokenMap[i] = i + added - (end - start)
		default:
			tokenMap[i] = -1
		}
	}
	body := make([]byte, 0, size-bodyStart)
	body = append(body, raw[bodyStart:lo]...)
	body = append(body, replacement...)
	for j, i := range attributes {
		tokenMap[i] = start + len(replacement) + j
		body = append(body, raw[d.state.gaps[i]:d.state.gaps[i+1]]...)
	}
	body = append(body, raw[hi:]...)
	return d.publishEveryday(c, body, count, start+added, tokenMap, proofEdit)
}

// AfterProofCorrection advances only a genuine checked proof edit and keeps
// the existing Undelete entries. A correction is not itself a delete group.
func (h History) AfterProofCorrection(r EditResult) (History, error) {
	return h.afterEveryday(r, proofEdit)
}
