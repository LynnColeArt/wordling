package editor

import "github.com/lynncoleart/wordling/internal/document"

const (
	ReplaceConfirmMode Mode = "ReplaceConfirm"
	ReplaceFindMode    Mode = "ReplaceFind"
	ReplaceWithMode    Mode = "ReplaceWith"
	ReplaceMatchMode   Mode = "ReplaceMatch"
)

// backwardPageSave binds a deferred formatter record to the edited revision.
type backwardPageSave struct {
	revision document.Revision
	record   int
}

type replaceState struct {
	query     string
	direction SearchKind
	confirm   bool
	match     FindResult
}

func IsReplacePrompt(mode Mode) bool {
	return mode == ReplaceFindMode || mode == ReplaceWithMode
}

func (s Session) replaceInput(event Event) (Session, *Intent, error) {
	if event.Command == F1 || event.Command == Escape {
		if s.mode == ReplaceMatchMode {
			s.backwardPageSave = backwardPageSave{}
		}
		s.mode, s.draft, s.caret, s.replacing = Editing, "", 0, replaceState{}
		return s, nil, nil
	}
	switch s.mode {
	case ReplaceConfirmMode:
		if event.Command != Yes && event.Command != No && event.Command != Enter {
			return s, nil, refuse("choose Yes or No")
		}
		s.mode = ReplaceFindMode
		s.replacing = replaceState{confirm: event.Command == Yes, direction: Forward}
		s.draft, s.caret, s.touched = "", 0, false
	case ReplaceFindMode, ReplaceWithMode:
		switch event.Command {
		case Up, Down:
			if s.mode != ReplaceFindMode {
				return s, nil, refuse("enter replacement text")
			}
			s.replacing.direction = Forward
			if event.Command == Up {
				s.replacing.direction = Backward
			}
		case SearchF2:
			if s.mode == ReplaceFindMode {
				if s.draft == "" {
					return s, nil, refuse("enter a search string")
				}
				s.replacing.query = s.draft
				s.mode, s.draft, s.caret, s.touched = ReplaceWithMode, "", 0, false
			} else {
				next, err := s.runReplace(s.cursor.Gap())
				return next, nil, err
			}
		case Bold, Underline, Text, ComposeCharacter, Backspace, Left, Right:
			return s.reduceSearch(event)
		default:
			return s, nil, refuse("use F2 to continue Replace")
		}
	case ReplaceMatchMode:
		if event.Command != Yes && event.Command != No && event.Command != Enter {
			return s, nil, refuse("choose Yes or No")
		}
		match := s.replacing.match
		gap := match.EndGap
		if event.Command == Yes {
			next, err := s.replaceMatch(match)
			if err != nil {
				return s, nil, err
			}
			s = next
			gap = s.cursor.Gap()
		}
		if s.replacing.direction == Backward {
			gap = match.TokenIndex
		}
		next, err := s.runReplace(gap)
		return next, nil, err
	}
	return s, nil, nil
}

func (s Session) replaceMatch(match FindResult) (Session, error) {
	cursor, err := s.native.CursorAt(match.TokenIndex)
	if err != nil {
		return s, err
	}
	edit, err := s.native.ReplaceSearchSpan(cursor.WithReveal(s.cursor.Reveal()), match.EndGap, []byte(s.draft))
	if err != nil {
		return s, err
	}
	next, err := s.adoptEverydayEdit(edit)
	if err != nil {
		return s, err
	}
	if !edit.Changed || s.replacing.direction != Backward || !s.replacing.confirm {
		return next, nil
	}
	crossedPage := false
	for i := match.TokenIndex; i < match.EndGap; i++ {
		token, _ := s.native.Token(i)
		crossedPage = crossedPage || token.Kind == document.SoftPage || token.Kind == document.DeletedSoftPage
	}
	if crossedPage {
		for i := match.TokenIndex; i < next.cursor.Gap(); i++ {
			token, _ := next.native.Token(i)
			transition, _ := next.native.Token(i + 1)
			if token.Kind == document.EndOfPage && (transition.Kind == document.SoftPage || transition.Kind == document.DeletedSoftPage) {
				next.backwardPageSave = backwardPageSave{revision: next.native.Revision(), record: i}
				break
			}
		}
	}
	return next, nil
}

func (s Session) runReplace(gap int) (Session, error) {
	// Bound the synchronous command. Reduce keeps the original session if it fails.
	for count := 0; count < 4096; count++ {
		projection, err := projectSearch(s.native)
		if err != nil {
			return s, err
		}
		if gap < 0 || gap >= len(projection.gaps) {
			return s, refuse("replacement position is invalid")
		}
		match, ok := projection.find(projection.gaps[gap], []byte(s.replacing.query), s.replacing.direction)
		if !ok {
			if count == 0 && s.mode == ReplaceWithMode {
				s.notice = "NOT FOUND"
			}
			s.mode, s.draft, s.caret, s.replacing = Editing, "", 0, replaceState{}
			return s, nil
		}
		if s.replacing.confirm {
			cursor, err := s.native.CursorAt(match.TokenIndex)
			if err != nil {
				return s, err
			}
			s.cursor = cursor.WithReveal(s.cursor.Reveal())
			s.mode, s.replacing.match = ReplaceMatchMode, match
			return s, nil
		}
		s, err = s.replaceMatch(match)
		if err != nil {
			return s, err
		}
		gap = s.cursor.Gap()
		if s.replacing.direction == Backward {
			gap = match.TokenIndex
		}
	}
	return s, refuse("replacement count exceeds its bound")
}

func (s Session) beginReplace() (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || s.mergeSource || s.proof != nil {
		return s, nil, refuse("Replace requires an ordinary editable document")
	}
	if _, table := s.native.SimpleTable(); table {
		return s, nil, refuse("Replace in tables is unavailable")
	}
	if err := s.native.CheckMutation(); err != nil {
		return s, nil, err
	}
	s.mode, s.notice = ReplaceConfirmMode, ""
	return s, nil, nil
}
