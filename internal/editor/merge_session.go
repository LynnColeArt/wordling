package editor

import (
	"errors"
	"io/fs"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/merge"
	"github.com/lynncoleart/wordling/internal/storage"
)

const (
	MergeMenuMode      Mode = "MergeMenu"
	MergePrimaryName   Mode = "MergePrimaryName"
	MergeSecondaryName Mode = "MergeSecondaryName"
)

type mergePrimaryState struct {
	plan             merge.Primary
	profile          document.MergeSaveProfile
	source           *storage.Document
	directory        *storage.WorkspaceDirectory
	workingDirectory *storage.WorkspaceDirectory
}

type mergeResultState struct {
	merged   document.Revision
	profile  document.MergeSaveProfile
	occupied bool
	atEnd    bool
}

func (m mergeResultState) active() bool {
	return m.merged != (document.Revision{})
}

func (s Session) exportMergeResult() ([]byte, error) {
	return s.native.ExportMergeResult(s.mergeResult.profile, document.MergeSaveOptions{
		FastSave: !s.fastSaveDisabled,
		Occupied: s.mergeResult.occupied,
		AtEnd:    s.mergeResult.atEnd,
		Edited:   s.mergeResult.merged != s.native.Revision(),
		Purged:   s.fastSavePurged,
	})
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

func (s Session) completeMergeRead(result Result, directory *storage.WorkspaceDirectory, fragment *document.Document) (Session, error) {
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
		s.mergePrimary = &mergePrimaryState{plan: plan, profile: profile, source: copySource(result.Document), directory: directory, workingDirectory: s.workspaceBase}
		return s.filename(MergeSecondaryName), nil
	}
	if result.Kind != ReadMergeSecondary || s.mode != MergeSecondaryName || s.mergePrimary == nil || fragment == nil {
		return s, refuse("merge completion does not match its role")
	}
	next, err := s.insertEverydayDocument(fragment)
	if err != nil {
		return s, err
	}
	next.mergePrimary = nil
	if next.native.Revision() == s.native.Revision() {
		return next, nil
	}
	occupied := s.native.TokenCount() != 0
	// Refuse incompatible resources before publishing the result in the buffer.
	next.mergeResult = mergeResultState{
		merged: next.native.Revision(), profile: s.mergePrimary.profile, occupied: occupied,
		atEnd: occupied && s.cursor.Gap() == s.native.TokenCount(),
	}
	if _, err := next.exportMergeResult(); err != nil {
		return s, err
	}
	return next, nil
}

func mergeSourceID(d *storage.WorkspaceDirectory, name string) string {
	return strings.TrimSuffix(d.DOSPath(), "\\") + "\\" + strings.ToUpper(name)
}

func (p *mergePrimaryState) evaluate(secondary *storage.Document, directory *storage.WorkspaceDirectory) (*document.Document, error) {
	if p == nil || p.source == nil || p.directory == nil || p.workingDirectory == nil || secondary == nil || directory == nil {
		return nil, refuse("missing authenticated merge source")
	}
	primaryID := mergeSourceID(p.directory, p.source.Name())
	second := merge.Source{ID: mergeSourceID(directory, secondary.Name()), Bytes: secondary.Export()}
	pinned := map[string]merge.Source{primaryID: {ID: primaryID, Bytes: p.source.Export()}, second.ID: second}
	resolve := func(_, name string) (merge.Source, error) {
		dir, leaf, err := resolveWorkspaceName(p.workingDirectory, name)
		if err != nil {
			return merge.Source{}, err
		}
		id := mergeSourceID(dir, leaf)
		if source, ok := pinned[id]; ok {
			return source, nil
		}
		result := readWorkspaceName(dir, leaf)
		if result.Err != nil {
			var failure *storage.Failure
			if errors.As(result.Err, &failure) && failure.Kind == storage.ReadFailed &&
				failure.Stage == "workspace retrieve" && errors.Is(failure, fs.ErrNotExist) {
				return merge.Source{}, &merge.MissingSource{Name: name}
			}
			return merge.Source{}, result.Err
		}
		source := merge.Source{ID: id, Bytes: result.Document.Export()}
		pinned[id] = source
		return source, nil
	}
	return merge.EvaluateWithSources(p.plan, primaryID, second, resolve)
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
