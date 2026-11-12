package editor

import (
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/merge"
	"github.com/lynncoleart/wordling/internal/merge/body"
	"github.com/lynncoleart/wordling/internal/storage"
)

const (
	MergeMenuMode      Mode = "MergeMenu"
	MergePrimaryName   Mode = "MergePrimaryName"
	MergeSecondaryName Mode = "MergeSecondaryName"
)

type mergePrimaryState struct {
	plan    body.Plan
	profile document.MergeSaveProfile
}

type mergeResultState struct {
	revision document.Revision
	profile  document.MergeSaveProfile
	occupied bool
}

func isMergeRead(kind IntentKind) bool {
	return kind == ReadMergePrimary || kind == ReadMergeSecondary
}

func isWorkspaceRead(kind IntentKind) bool {
	return kind == ReadSelection || isMergeRead(kind)
}

func (s Session) beginMerge() (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || s.selection || s.proof != nil {
		return s, nil, refuse("Merge requires an editable workspace document")
	}
	if err := s.native.CheckMutation(); err != nil {
		return s, nil, err
	}
	s.mode, s.notice = MergeMenuMode, ""
	return s, nil, nil
}

func (s Session) cancelMerge() (Session, *Intent, error) {
	s.mergePrimary = nil
	s.pending = nil
	s.mode, s.notice = Editing, ""
	return s, nil, nil
}

// mergeInput receives the same pinned workspace selection used by Retrieve,
// but only for the current merge role, and never adopts the source as Doc 1/2.
func (s Session) mergeInput(event Event) (Session, *Intent, error) {
	if event.Command == F1 {
		return s.cancelMerge()
	}
	if s.mode == MergeMenuMode {
		if event.Command == Enter || event.Command == Text && event.Text == "0" {
			return s.cancelMerge()
		}
		if event.Command == Text && event.Text == "1" {
			return s.filename(MergePrimaryName), nil, nil
		}
		return s, nil, refuse("Merge menu supports 1 Merge")
	}
	kind := ReadMergePrimary
	if s.mode == MergeSecondaryName {
		kind = ReadMergeSecondary
	}
	switch event.Command {
	case Enter:
		return s.beginEveryday(kind, nil, s.draft, false, storage.NoOverwrite)
	case RetrieveSelection:
		if event.Selection == nil {
			return s, nil, refuse("missing merge file selection")
		}
		return s.beginEveryday(kind, event.Selection, "", false, storage.NoOverwrite)
	default:
		return s.editName(event)
	}
}

func (s Session) completeMergeRead(result Result) (Session, error) {
	if result.Document == nil {
		return s, refuse("missing authenticated merge source")
	}
	if result.Kind == ReadMergePrimary && s.mode == MergePrimaryName {
		raw := result.Document.Export()
		plan, err := merge.CompilePrimary(raw)
		if err != nil {
			return s, err
		}
		primary, err := document.Parse(raw)
		if err != nil {
			return s, err
		}
		profile, err := primary.MergeSaveProfile()
		if err != nil {
			return s, err
		}
		s.mergePrimary = &mergePrimaryState{plan: plan, profile: profile}
		return s.filename(MergeSecondaryName), nil
	}
	if result.Kind != ReadMergeSecondary || s.mode != MergeSecondaryName || s.mergePrimary == nil {
		return s, refuse("merge completion does not match its role")
	}
	fragment, err := merge.Evaluate(s.mergePrimary.plan, result.Document.Export())
	if err != nil {
		return s, err
	}
	next, err := s.insertEverydayDocument(fragment)
	if err != nil {
		return s, err
	}
	occupied := s.native.TokenCount() != 0
	// Refuse incompatible resources before publishing the result in the buffer.
	if _, err := next.native.ExportMergeResult(s.mergePrimary.profile, !s.fastSaveDisabled, occupied); err != nil {
		return s, err
	}
	next.mergeResult = mergeResultState{revision: next.native.Revision(), profile: s.mergePrimary.profile, occupied: occupied}
	next.mergePrimary = nil
	return next, nil
}

func (s Session) editMergeLiteral(text string) (Session, *Intent, error) {
	edit, err := s.native.InsertMergeLiteral(s.cursor, []byte(text))
	if err != nil {
		return s, nil, err
	}
	s.native, s.cursor = edit.Document, edit.Cursor
	s.revision++
	s.lastSave, s.notice, s.verticalRun = NotSaved, "", false
	return s, nil, nil
}
