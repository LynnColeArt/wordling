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
	EndGap     int
	Offset     int
}

// Find locates a whole-owner query at or after the supplied byte anchor
// (forward) or ending at or before it (backward). An empty anchor is zero.
// Both returned gaps are native token boundaries.
func Find(doc *document.Document, from []byte, query []byte, direction SearchKind) (FindResult, bool) {
	if len(query) == 0 {
		return FindResult{}, false
	}
	projection, err := projectSearch(doc)
	if err != nil {
		return FindResult{}, false
	}
	return projection.find(decodeFrom(from), query, direction)
}

type searchProjection struct {
	raw  []byte
	gaps []int
}

func projectSearch(doc *document.Document) (searchProjection, error) {
	count := doc.TokenCount()
	p := searchProjection{raw: make([]byte, 0, count), gaps: make([]int, 0, count+1)}
	for i := 0; i < count; i++ {
		token, err := doc.Token(i)
		if err != nil {
			return searchProjection{}, err
		}
		p.gaps = append(p.gaps, len(p.raw))
		if token.Kind == document.SoftReturn {
			// Original "Menus, prompts" matches across the single SRt.
			p.raw = append(p.raw, ' ')
		} else {
			p.raw = append(p.raw, token.Raw...)
		}
	}
	p.gaps = append(p.gaps, len(p.raw))
	return p, nil
}

func (p searchProjection) find(start int, query []byte, direction SearchKind) (FindResult, bool) {
	if len(query) == 0 || start < 0 || start > len(p.raw) {
		return FindResult{}, false
	}
	match := func(index int) (FindResult, bool) {
		at := p.gaps[index]
		end := at + len(query)
		if end > len(p.raw) || !bytes.Equal(p.raw[at:end], query) {
			return FindResult{}, false
		}
		endGap := sort.SearchInts(p.gaps, end)
		if endGap == len(p.gaps) || p.gaps[endGap] != end {
			return FindResult{}, false
		}
		return FindResult{Found: true, TokenIndex: index, EndGap: endGap, Offset: at}, true
	}
	if direction == Forward {
		for i := sort.SearchInts(p.gaps, start); i < len(p.gaps)-1; i++ {
			if result, found := match(i); found {
				return result, true
			}
		}
	} else {
		for i := sort.SearchInts(p.gaps, start-len(query)+1) - 1; i >= 0; i-- {
			if result, found := match(i); found {
				return result, true
			}
		}
	}
	return FindResult{}, false
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
