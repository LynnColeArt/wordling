package editor

import (
	"strings"
	"unicode/utf8"

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

const (
	searchUnderline = "\xc3\x0e\xc3"
	searchNotFound  = "NOT FOUND"
)

var searchFormats = map[string]string{
	"\xc3\x0c\xc3": "[BOLD]", "\xc4\x0c\xc4": "[bold]",
	searchUnderline: "[UND]", "\xc4\x0e\xc4": "[und]",
}

func searchFormat(raw string) string {
	if len(raw) < 3 {
		return ""
	}
	return searchFormats[raw[:3]]
}

func searchDisplay(raw string) string {
	var display strings.Builder
	for len(raw) > 0 {
		switch {
		case searchFormat(raw) != "":
			display.WriteString(searchFormat(raw))
			raw = raw[3:]
		case len(raw) >= 4 && document.IsExtendedCharacter([]byte(raw[:4])):
			display.WriteString(document.CharacterGlyph(raw[2], raw[1]))
			raw = raw[4:]
		default:
			display.WriteByte(raw[0])
			raw = raw[1:]
		}
	}
	return display.String()
}

func searchCaret(display string) int { return utf8.RuneCountInString(display) }

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
	case ComposeCharacter:
		if s.workspace == nil {
			return s, nil, refuse("Compose requires workspace search")
		}
		raw := document.CharacterBytes(event.Character.Set, event.Character.Number)
		if len(raw) == 0 {
			return s, nil, refuse("invalid WordPerfect character")
		}
		event.Text = string(raw)
		fallthrough
	case Text:
		return s.appendSearchText(event.Text)
	case Bold, Underline:
		return s.toggleSearchAttribute(event.Command)
	case Left, Right, Backspace:
		at := s.caret
		if event.Command == Right {
			if at < len(s.draft) {
				s.caret += searchOwnerWidth(s.draft[at:])
			}
		} else if at > 0 {
			previous := 0
			for next := searchOwnerWidth(s.draft); next < at; next += searchOwnerWidth(s.draft[next:]) {
				previous = next
			}
			if event.Command == Backspace {
				s.draft = s.draft[:previous] + s.draft[at:]
			}
			s.caret = previous
		}
		s.touched = true
		return s, nil, nil
	case SearchF2, F7:
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

func searchOwnerWidth(raw string) int {
	if searchFormat(raw) != "" {
		return 3
	}
	if len(raw) >= 4 && document.IsExtendedCharacter([]byte(raw[:4])) {
		return 4
	}
	return 1
}

func (s Session) toggleSearchAttribute(command Command) (Session, *Intent, error) {
	if s.workspace == nil {
		return s, nil, refuse("attribute search requires qualified workspace editing")
	}
	attribute := byte(0x0c)
	if command == Underline {
		attribute = 0x0e
	}
	on := string([]byte{0xc3, attribute, 0xc3})
	off := string([]byte{0xc4, attribute, 0xc4})
	active := false
	if s.touched {
		for prefix := s.draft[:s.caret]; len(prefix) > 0; {
			width := searchOwnerWidth(prefix)
			switch prefix[:width] {
			case on:
				active = true
			case off:
				active = false
			}
			prefix = prefix[width:]
		}
	}
	if active {
		return s.appendSearchText(off)
	}
	return s.appendSearchText(on)
}

func (s Session) appendSearchText(text string) (Session, *Intent, error) {
	draft, at := s.draft, s.caret
	if !s.touched {
		draft, at = "", 0
	}
	if len(draft)+len(text) > storage.MaxNameBytes {
		return s, nil, refuse("search query safety bound")
	}
	s.draft = draft[:at] + text + draft[at:]
	s.caret = at + len(text)
	s.touched = true
	return s, nil, nil
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
		s.notice = searchNotFound
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
	s.blockMoved = s.blockMoved || s.selection && cursor.Gap() != s.cursor.Gap()
	s.cursor = cursor.WithReveal(s.cursor.Reveal())
	return s, nil, nil
}
