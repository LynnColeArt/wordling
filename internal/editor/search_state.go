package editor

import (
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/storage"
)

// EE-A09 session search state (T259-T263). The original's search lives in a
// prompt mode with a draft query, direction-bound execution, and a remembered
// last query for repetition (frames: F2 → "→ Srch:", type + F2 → result,
// F2 again → "→ Srch: alpha" prefilled, F2 → next match; Shift+F2 mirrored).
// Search never edits native bytes: cancellation/not-found settle at the
// pre-search position (frames 24/25/26 return to Pos 2.4").

const (
	SearchForwardMode  Mode = "SearchForward"
	SearchBackwardMode Mode = "SearchBackward"
)

// beginSearch opens the prompt in the given direction. The draft prefill is
// the remembered direction-scoped last query (frame 20/22 show the query
// already present in the prompt for repeats; first invocation is empty).
func (s Session) beginSearch(direction SearchKind) Session {
	s.mode = searchPromptMode(direction)
	s.draft = s.lastSearchQuery
	s.original = s.lastSearchQuery
	s.caret = len(s.draft)
	s.touched = false
	s.editedPrefill = false
	s.notice = ""
	s.searchPending = true
	return s
}

func searchPromptMode(direction SearchKind) Mode {
	if direction == Backward {
		return SearchBackwardMode
	}
	return SearchForwardMode
}

// reduceSearch handles prompt-mode events: typing, cancellation (F1), and
// execution (F2 in the same direction — the original terminates and runs).
func (s Session) reduceSearch(event Event) (Session, *Intent, error) {
	switch event.Command {
	case F1:
		// Frame 26: F1 cancels; body and cursor unchanged.
		s.mode = Editing
		s.draft = ""
		s.searchPending = false
		s.fromExit = false
		return s, nil, nil
	case Text:
		if len(event.Text) > storage.MaxNameBytes {
			return s, nil, refuse("search query safety bound")
		}
		draft := s.draft
		if !s.touched {
			draft = ""
		}
		if len(draft)+len(event.Text) > storage.MaxNameBytes {
			return s, nil, refuse("search query safety bound")
		}
		s.draft = draft + event.Text
		s.caret = len(s.draft)
		s.touched = true
		return s, nil, nil
	case Backspace:
		if s.caret == 0 {
			return s, nil, refuse("search caret boundary")
		}
		s.draft = s.draft[:len(s.draft)-1]
		s.caret = len(s.draft)
		s.touched = true
		return s, nil, nil
	case SearchF2:
		// Execute. The prompt's direction is authoritative (frames pair F2
		// with the forward prompt, Shift+F2 with the backward one; the
		// backward flow re-executes via Shift+F2, frame 23).
		return s.executeSearch(s.promptDirection(s.mode))
	case SearchBackF2:
		return s.executeSearch(Backward)
	case Enter:
		// The original's Enter on the search prompt is unobserved (the trace
		// always terminates with F2 in the prompt's direction); keep the
		// bounded refusal rather than inventing an alias.
		return s, nil, refuse("search executes with F2 in the prompt's direction")
	default:
		return s, nil, refuse("unobserved search prompt command")
	}
}

func (s Session) promptDirection(mode Mode) SearchKind {
	if mode == SearchBackwardMode {
		return Backward
	}
	return Forward
}

// executeSearch runs Find from the cursor's token-stream offset. On repeat
// execution (same query as the last successful match) the seed is the last
// match's end so the search advances; a fresh query seeds from the cursor.
// It moves the cursor to the match, remembers the query + match end, and
// returns to Editing. Not-found leaves the cursor exactly as it was (frames
// 24/25) and surfaces the failure notice.
func (s Session) executeSearch(direction SearchKind) (Session, *Intent, error) {
	if s.native == nil {
		return s, nil, refuse("search requires a loaded document")
	}
	total := s.native.TokenCount()
	// Concatenate raw bytes with span indexing (the same bounded walk Find
	// uses, with transparent soft returns), then seed `from`: after the last
	// match when repeating the same query, else from the cursor's token gap.
	raw := make([]byte, 0, total)
	spans := make([]int, 0, total+1)
	rawGap := 0
	for i := 0; i < total; i++ {
		tok, err := s.native.Token(i)
		if err != nil {
			return s, nil, err
		}
		spans = append(spans, len(raw))
		if tok.Kind == document.SoftReturn {
			raw = append(raw, ' ') // SRt matches a query space (frame 27)
			continue
		}
		raw = append(raw, tok.Raw...)
	}
	spans = append(spans, len(raw))
	gap := s.cursor.Gap()
	if gap > total {
		gap = total
	}
	if gap < len(spans) {
		rawGap = spans[gap]
	} else {
		rawGap = spans[len(spans)-1]
	}
	seed := rawGap
	if s.lastSearchQuery == s.draft && s.lastSearchEnd > 0 {
		seed = s.lastSearchEnd
		if seed > len(raw) {
			seed = len(raw)
		}
	}
	result, found := Find(s.native, EncodeFrom(seed), []byte(s.draft), direction)
	s.lastSearchQuery = s.draft
	s.searchPending = false
	s.mode = Editing
	if !found {
		s.notice = "NOT FOUND"
		return s, nil, nil
	}
	s.notice = ""
	s.lastSearchEnd = result.Offset + len(s.draft)
	cursor, err := s.native.CursorAt(result.TokenIndex)
	if err != nil {
		return s, nil, err
	}
	s.cursor = cursor
	return s, nil, nil
}

// The session carries direction-scoped last queries for prefill (frames
// 20/22: the prompt reopens with the query already present).
