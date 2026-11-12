package editor

import (
	"strings"

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

const searchUnderline = "\xc3\x0e\xc3"

func searchDisplay(raw string) string {
	return strings.ReplaceAll(raw, searchUnderline, "[UND]")
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
	case Underline:
		if s.workspace == nil {
			return s, nil, refuse("attribute search requires qualified workspace editing")
		}
		event.Text = searchUnderline
		fallthrough
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
		width := 1
		if strings.HasSuffix(s.draft, searchUnderline) {
			width = len(searchUnderline)
		}
		s.draft = s.draft[:len(s.draft)-width]
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

// executeSearch begins at the current native caret. Backward excludes a
// match ending at that caret. Both directions land after the matched owners.
func (s Session) executeSearch(direction SearchKind) (Session, *Intent, error) {
	if s.native == nil {
		return s, nil, refuse("search requires a loaded document")
	}
	projected, err := projectSearch(s.native)
	if err != nil {
		return s, nil, err
	}
	gap := s.cursor.Gap()
	if gap < 0 || gap >= len(projected.gaps) {
		return s, nil, refuse("search caret is outside the native document")
	}
	seed := projected.gaps[gap]
	if direction == Backward {
		seed--
	}
	result, found := projected.find(seed, []byte(s.draft), direction)
	s.lastSearchQuery = s.draft
	s.searchPending = false
	s.mode = Editing
	if !found {
		s.notice = "NOT FOUND"
		return s, nil, nil
	}
	s.notice = ""
	cursor, err := s.native.CursorAt(result.EndGap)
	if err != nil {
		return s, nil, err
	}
	if s.workspace != nil && cursor.Gap() != s.cursor.Gap() {
		s.history, err = s.interrupted()
		if err != nil {
			return s, nil, err
		}
	}
	s.cursor = cursor.WithReveal(s.cursor.Reveal())
	return s, nil, nil
}
