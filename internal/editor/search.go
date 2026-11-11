package editor

import (
	"bytes"
	"sort"

	"github.com/lynncoleart/wordling/internal/document"
)

// SearchKind selects the bounded original search direction (EE-A09: F2
// forward, Shift+F2 backward).
type SearchKind uint8

const (
	Forward SearchKind = iota + 1
	Backward
)

// Search is a bounded session-owned search target. It never searches rendered
// ANSI strings and never edits native bytes.
type Search struct {
	Query []byte
	Kind  SearchKind
}

// FindResult is an immutable search result or bounded no-match state. (Named
// FindResult: the parent package's `Result` is the session IO receipt type.)
type FindResult struct {
	Found      bool
	TokenIndex int
	Offset     int
}

// Find locates query matches on raw document tokens without inventing display
// text. It returns the first match strictly at or after `from` (forward) /
// strictly before `from` (backward), where `from` is a byte offset into the
// concatenated raw token stream; nil/empty `from` means document start
// (forward) / end (backward). Soft returns (0x0D) are transparent filler —
// the original searches across the screen wrap (EE-A09 "Search crosses SRt",
// frame 27 "Menus, prompts" matching over the SRt). W83-1/W83-2 fixed: the
// anchor parameter is honored, and repetition is the caller re-issuing Find
// with the previous Offset — the original's repeated-F2 semantics (frames
// 19→21).
func Find(doc *document.Document, from []byte, query []byte, direction SearchKind) (FindResult, bool) {
	var zero FindResult
	if len(query) == 0 {
		return zero, false
	}
	count := doc.TokenCount()
	if count == 0 {
		return zero, false
	}
	raw := make([]byte, 0, count)
	spans := make([]int, 0, count+1)
	for i := 0; i < count; i++ {
		tok, err := doc.Token(i)
		if err != nil {
			return zero, false
		}
		spans = append(spans, len(raw))
		if tok.Kind == document.SoftReturn {
			// The soft return matches a query SPACE: the screen renders the
			// wrap as a line break, and the trace's cross-wrap query
			// "Menus, prompts" (frame 27) matches over the single 0x0d.
			raw = append(raw, ' ')
			continue
		}
		raw = append(raw, tok.Raw...)
	}
	spans = append(spans, len(raw))
	start := 0
	if len(from) > 0 {
		start = decodeFrom(from)
		if start < 0 || start > len(raw) {
			return zero, false
		}
	}
	match := func(index int) bool {
		at := spans[index]
		end := at + len(query)
		if end > len(raw) || !bytes.Equal(raw[at:end], query) {
			return false
		}
		boundary := sort.SearchInts(spans, end)
		return boundary < len(spans) && spans[boundary] == end
	}
	if direction == Forward {
		for i := sort.SearchInts(spans, start); i < count; i++ {
			if match(i) {
				return FindResult{Found: true, TokenIndex: i, Offset: spans[i]}, true
			}
		}
		return zero, false
	}
	for i := sort.SearchInts(spans, start-len(query)+1) - 1; i >= 0; i-- {
		if match(i) {
			return FindResult{Found: true, TokenIndex: i, Offset: spans[i]}, true
		}
	}
	return zero, false
}

// EncodeFrom preserves the anchor across session turns: the byte offset is
// carried verbatim as the caller's next `from` value.
func EncodeFrom(offset int) []byte { return []byte{byte(offset >> 8), byte(offset)} }

func decodeFrom(from []byte) int {
	if len(from) < 2 {
		return 0
	}
	return int(from[0])<<8 | int(from[1])
}
