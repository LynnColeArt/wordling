package editor

import "github.com/lynncoleart/wordling/internal/document"

const (
	MergeCodesMode Mode = "MergeCodes"
	MergeFieldMode Mode = "MergeField"
)

const mergeCodePrompt = "1 Field; 2 End Record; 3 Input; 4 Page Off; 5 Next Record; 6 More: 0"

func (s Session) beginMergeCodes() (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || s.selection || s.over || s.proof != nil {
		return s, nil, refuse("Merge Codes requires an editable workspace document")
	}
	s.mode, s.notice = MergeCodesMode, ""
	return s, nil, nil
}

func (s Session) mergeAuthoringInput(event Event) (Session, *Intent, error) {
	if event.Command == F1 || event.Command == Escape {
		s.mode, s.draft, s.caret, s.notice = Editing, "", 0, ""
		return s, nil, nil
	}
	if s.mode == MergeChoicesMode {
		return s.mergeChoiceInput(event)
	}
	if s.mode == MergeOperandMode {
		return s.mergeOperandInput(event)
	}
	if s.mode == MergeCodesMode {
		switch {
		case event.Command == Enter || event.Command == Text && event.Text == "0":
			s.mode = Editing
			return s, nil, nil
		case event.Command == Text && event.Text == "1":
			s.mode, s.draft, s.caret = MergeFieldMode, "", 0
			return s, nil, nil
		case event.Command == Text && event.Text == "2":
			return s.insertMergeCode(document.AuthorMergeEndRecord, "")
		case event.Command == Text && event.Text == "4":
			return s.insertNamedMergeCode(document.MergePageOff, "")
		case event.Command == Text && event.Text == "6":
			s.mode, s.draft, s.caret = MergeChoicesMode, "", 0
			s.mergeChoice, s.mergeChoiceTop = 0, 0
			return s, nil, nil
		default:
			return s, nil, refuse("This Merge Codes command is not yet implemented")
		}
	}
	switch event.Command {
	case Text:
		if len(event.Text) == 0 || len(s.draft)+len(event.Text) > document.MaxMergeOperandBytes {
			return s, nil, refuse("Field number exceeds its editing bound")
		}
		for _, digit := range event.Text {
			if digit < '0' || digit > '9' {
				return s, nil, refuse("Field number must contain decimal digits")
			}
		}
		s.draft += event.Text
		s.caret = len(s.draft)
	case Backspace:
		if len(s.draft) != 0 {
			s.draft = s.draft[:len(s.draft)-1]
			s.caret = len(s.draft)
		}
	case Enter:
		if s.draft == "" {
			return s, nil, refuse("Enter a field number")
		}
		return s.insertMergeCode(document.AuthorMergeField, s.draft)
	default:
		return s, nil, refuse("Enter a field number")
	}
	return s, nil, nil
}

func (s Session) insertMergeCode(code document.MergeCode, operand string) (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || s.selection || s.over || s.proof != nil {
		return s, nil, refuse("Merge code requires an editable workspace document")
	}
	edit, err := s.native.InsertMergeCode(s.cursor, code, operand)
	if err != nil {
		return s, nil, err
	}
	return s.adoptMergeAuthoring(edit)
}

func (s Session) adoptMergeAuthoring(edit document.EditResult) (Session, *Intent, error) {
	history := s.history
	if s.historyValid {
		var err error
		history, err = history.AfterMergeEdit(edit)
		if err != nil {
			return s, nil, err
		}
	}
	s.native, s.cursor = edit.Document, edit.Cursor
	s.mergeSource = s.native.IsAuthoredMergeSource()
	s.mergeResult = mergeResultState{}
	s.mode, s.notice, s.draft, s.caret = Editing, "", "", 0
	s.revision++
	s.lastSave, s.verticalRun = NotSaved, false
	s.history = history
	return s, nil, nil
}

func (s Session) deleteMergeCode(command Command) (Session, *Intent, error) {
	edit, err := s.native.DeleteAuthoredMergeText(s.cursor, command == Backspace)
	if err != nil {
		return s, nil, err
	}
	return s.adoptMergeAuthoring(edit)
}

func (s Session) insertAuthoredMergeText(text string) (Session, *Intent, error) {
	edit, err := s.native.InsertAuthoredMergeText(s.cursor, []byte(text))
	if err != nil {
		return s, nil, err
	}
	return s.adoptMergeAuthoring(edit)
}

// MergeField reports the active secondary data field for the status line.
func (s Session) MergeField() (int, bool) {
	if !s.mergeSource {
		return 0, false
	}
	return s.native.MergeFieldAt(s.cursor)
}

type mergeHistoryCarry struct {
	source  *document.Document
	history document.History
}

// Share the witnessed structural deletion ring without moving either
// document's format state, cursor or revision between screens. A read-only
// screen can hold custody, but cannot use the ring to mutate its document.
func (s Session) carryMergeHistory(next Session) (Session, error) {
	if s.workspace == nil {
		return next, nil
	}
	carry := s.parkedMergeHistory
	if s.historyValid && s.history.HasSharedMergeHistory() {
		carry = &mergeHistoryCarry{copyNative(s.native), s.history}
	}
	if carry == nil {
		return next, nil
	}
	next.parkedMergeHistory = carry
	if !next.historyValid || !next.history.CountKnown() {
		return next, nil
	}
	history, err := carry.history.CarryMergeHistory(carry.source, next.history, next.native)
	if err != nil {
		return next, err
	}
	next.history = history
	next.parkedMergeHistory = nil
	return next, nil
}
