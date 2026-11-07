package editor

import (
	"bytes"

	"github.com/lynncoleart/wordling/internal/document"
)

// SearchKind selects the bounded original search direction.
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

// Result is an immutable search result or bounded no-match state.
type Result struct {
	Found      bool
	TokenIndex int
	Offset     int
}

// Find locates the first match on raw document tokens without inventing display
// text. It is intentionally independent of terminal presentation.
func Find(doc *document.Document, from, query []byte, direction SearchKind) ([]int, bool) {
	var matches []int
	if len(query) == 0 {
		return matches, false
	}
	count := doc.TokenCount()
	if count == 0 {
		return matches, false
	}
	raw := make([]byte, 0, count)
	spans := make([]int, 0, count+1)
	for i := 0; i < count; i++ {
		tok, err := doc.Token(i)
		if err != nil {
			return nil, false
		}
		spans = append(spans, len(raw))
		raw = append(raw, tok.Raw...)
	}
	spans = append(spans, len(raw))
	if direction == Forward {
		start := 0
		for i := 0; i <= len(raw)-len(query); i++ {
			index := i + start
			if index+len(query) > len(raw) {
				continue
			}
			if bytes.Equal(raw[index:index+len(query)], query) {
				matches = append(matches, indexOf(spans, index))
				break
			}
		}
		return matches, len(matches) > 0
	}
	for i := len(raw) - len(query); i >= 0; i-- {
		if bytes.Equal(raw[i:i+len(query)], query) {
			matches = append(matches, indexOf(spans, i))
			break
		}
	}
	return matches, len(matches) > 0
}

func indexOf(spans []int, offset int) int {
	for i := 0; i < len(spans)-1; i++ {
		if offset >= spans[i] && offset < spans[i+1] {
			return i
		}
	}
	if offset == spans[len(spans)-1] {
		return len(spans) - 2
	}
	return -1
}
