package editor

import (
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
)

const (
	MergeChoicesMode Mode = "MergeChoices"
	MergeOperandMode Mode = "MergeOperand"
)

const mergeChoiceRows = 10

// Names and parameter guides follow the original Merge Codes More chooser.
var mergeChoices = [...]string{
	"{ASSIGN}var~expr~",
	"{BELL}",
	"{BREAK}",
	"{CALL}label~",
	"{CANCEL OFF}",
	"{CANCEL ON}",
	"{CASE}expr~cs1~lb1~...csN~lbN~~",
	"{CASE CALL}expr~cs1~lb1~...csN~lbN~~",
	"{CHAIN MACRO}macroname~           (^G)",
	"{CHAIN PRIMARY}filename~",
	"{CHAIN SECONDARY}filename~",
	"{CHAR}var~message~",
	"{COMMENT}comment~",
	"{CTON}character~",
	"{DATE}                            (^D)",
	"{DOCUMENT}filename~",
	"{ELSE}",
	"{END FIELD}                       (^R)",
	"{END FOR}",
	"{END IF}",
	"{END RECORD}                      (^E)",
	"{END WHILE}",
	"{FIELD}field~                     (^F)",
	"{FIELD NAMES}name1~...nameN~~",
	"{FOR}var~start~stop~step~",
	"{GO}label~",
	"{IF}expr~",
	"{IF BLANK}field~",
	"{IF EXISTS}var~",
	"{IF NOT BLANK}field~",
	"{INPUT}message~",
	"{KEYBOARD}                        (^C)",
	"{LABEL}label~",
	"{LEN}expr~",
	"{LOCAL}var~expr~",
	"{LOOK}var~",
	"{MID}expr~offset~count~",
	"{MRG CMND}codes{MRG CMND}         (^V)",
	"{NEST MACRO}macroname~",
	"{NEST PRIMARY}filename~           (^P)",
	"{NEST SECONDARY}filename~",
	"{NEXT}",
	"{NEXT RECORD}                     (^N)",
	"{NTOC}number~",
	"{ON CANCEL}action~",
	"{ON ERROR}action~",
	"{OTHERWISE}",
	"{PAGE OFF}",
	"{PAGE ON}",
	"{PRINT}                           (^T)",
	"{PROCESS}codes{PROCESS}",
	"{PROMPT}message~                  (^O)",
	"{QUIT}                            (^Q)",
	"{RETURN}",
	"{RETURN CANCEL}",
	"{RETURN ERROR}",
	"{REWRITE}                         (^U)",
	"{STATUS PROMPT}message~",
	"{STEP OFF}",
	"{STEP ON}",
	"{STOP}",
	"{SUBST PRIMARY}filename~",
	"{SUBST SECONDARY}filename~        (^S)",
	"{SYSTEM}sysvar~",
	"{TEXT}var~message~",
	"{VARIABLE}var~",
	"{WAIT}10ths second~",
	"{WHILE}expr~",
}

func mergeChoiceName(index int) string {
	line := mergeChoices[index]
	return line[1:strings.IndexByte(line, '}')]
}

func mergeChoiceKind(index int) document.Kind {
	switch mergeChoiceName(index) {
	case "PAGE OFF":
		return document.MergePageOff
	case "PAGE ON":
		return document.MergePageOn
	case "NEST PRIMARY":
		return document.MergeNestPrimary
	case "NEST SECONDARY":
		return document.MergeNestSecondary
	case "IF BLANK":
		return document.MergeIfBlank
	case "ELSE":
		return document.MergeElse
	case "END IF":
		return document.MergeEndIf
	case "BREAK":
		return document.MergeBreak
	default:
		return document.Opaque
	}
}

// MergeChoices exposes only a copied view of the active keyboard modal.
func (s Session) MergeChoices() (rows []string, selected int, operand bool) {
	if s.mode != MergeChoicesMode && s.mode != MergeOperandMode {
		return nil, 0, false
	}
	for _, line := range mergeChoices[s.mergeChoiceTop : s.mergeChoiceTop+mergeChoiceRows] {
		rows = append(rows, line)
	}
	return rows, s.mergeChoice - s.mergeChoiceTop, s.mode == MergeOperandMode
}

func (s Session) moveMergeChoice(index int) Session {
	s.mergeChoice = max(0, min(index, len(mergeChoices)-1))
	s.mergeChoiceTop = min(s.mergeChoiceTop, s.mergeChoice)
	s.mergeChoiceTop = max(s.mergeChoiceTop, s.mergeChoice-mergeChoiceRows+1)
	return s
}

func (s Session) searchMergeChoice(draft string) Session {
	s.draft, s.caret = draft, len(draft)
	if draft == "" {
		return s.moveMergeChoice(0)
	}
	for i := range mergeChoices {
		if strings.HasPrefix(mergeChoiceName(i), draft) {
			if i < s.mergeChoiceTop || i >= s.mergeChoiceTop+mergeChoiceRows {
				s.mergeChoiceTop = max(0, min(i-5, len(mergeChoices)-mergeChoiceRows))
			}
			return s.moveMergeChoice(i)
		}
	}
	return s
}

func (s Session) mergeChoiceInput(event Event) (Session, *Intent, error) {
	switch event.Command {
	case Up:
		s.draft, s.caret = "", 0
		s = s.moveMergeChoice(s.mergeChoice - 1)
	case Down:
		s.draft, s.caret = "", 0
		s = s.moveMergeChoice(s.mergeChoice + 1)
	case PageUp:
		s.draft, s.caret = "", 0
		s = s.moveMergeChoice(s.mergeChoice - mergeChoiceRows)
	case PageDown:
		s.draft, s.caret = "", 0
		s = s.moveMergeChoice(s.mergeChoice + mergeChoiceRows)
	case Text:
		if len(s.draft)+len(event.Text) <= 25 {
			s = s.searchMergeChoice(s.draft + strings.ToUpper(event.Text))
		}
	case Backspace:
		if s.draft != "" {
			s = s.searchMergeChoice(s.draft[:len(s.draft)-1])
		}
	case Enter:
		if !strings.HasPrefix(mergeChoiceName(s.mergeChoice), s.draft) {
			return s, nil, refuse("No merge code matches that name")
		}
		kind := mergeChoiceKind(s.mergeChoice)
		switch mergeChoiceName(s.mergeChoice) {
		case "FIELD":
			s.mode, s.draft, s.caret = MergeFieldMode, "", 0
			return s, nil, nil
		case "END FIELD":
			return s.insertMergeCode(document.AuthorMergeEndField, 0)
		case "END RECORD":
			return s.insertMergeCode(document.AuthorMergeEndRecord, 0)
		}
		switch kind {
		case document.MergeNestPrimary, document.MergeNestSecondary, document.MergeIfBlank:
			s.mode, s.draft, s.caret = MergeOperandMode, "", 0
			return s, nil, nil
		case document.Opaque:
			return s, nil, refuse("This Merge Codes command is not yet implemented")
		default:
			return s.insertNamedMergeCode(kind, "")
		}
	default:
		return s, nil, refuse("Use Name Search, arrows or Enter")
	}
	return s, nil, nil
}

func (s Session) mergeOperandPrompt() string {
	if mergeChoiceKind(s.mergeChoice) == document.MergeIfBlank {
		return "Enter Field: "
	}
	return "Enter Filename: "
}

func (s Session) mergeOperandInput(event Event) (Session, *Intent, error) {
	switch event.Command {
	case Text:
		if len(s.draft)+len(event.Text) > 63 {
			return s, nil, refuse("Merge operand exceeds its editing bound")
		}
		s.draft += strings.ToUpper(event.Text)
		s.caret = len(s.draft)
	case Backspace:
		if s.draft != "" {
			s.draft = s.draft[:len(s.draft)-1]
			s.caret = len(s.draft)
		}
	case Enter:
		return s.insertNamedMergeCode(mergeChoiceKind(s.mergeChoice), s.draft)
	default:
		return s, nil, refuse("Enter a merge operand")
	}
	return s, nil, nil
}

func (s Session) insertNamedMergeCode(kind document.Kind, operand string) (Session, *Intent, error) {
	edit, err := s.native.InsertNamedMergeCode(s.cursor, kind, operand)
	if err != nil {
		return s, nil, err
	}
	return s.adoptMergeAuthoring(edit), nil, nil
}
