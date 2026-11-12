package editor

import (
	"bytes"
	"errors"
	"io/fs"
	"strings"
	"sync/atomic"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
	"github.com/lynncoleart/wordling/internal/merge"
	"github.com/lynncoleart/wordling/internal/storage"
)

type everydayRequest struct {
	intent         Intent
	workspace      *storage.Workspace
	directory      *storage.WorkspaceDirectory
	mergeInput     *mergePrimaryState
	insert         bool
	backup         storage.OriginalBackup
	purgesFastSave bool
	used           atomic.Bool
}

type everydayObservation struct {
	request     *everydayRequest
	directory   *storage.WorkspaceDirectory
	result      Result
	mergeOutput merge.Evaluation
}

func copySelection(p *storage.EntrySelection) *storage.EntrySelection {
	if p == nil {
		return nil
	}
	copy := *p
	return &copy
}

func sameWrapper[T comparable](a, b *T) bool {
	if a == nil || b == nil {
		return a == b
	}
	return *a == *b
}

func (p *everydayRequest) matches(i *Intent) bool {
	if p == nil || i == nil {
		return false
	}
	want := p.intent
	return i.Operation == want.Operation && i.Revision == want.Revision &&
		i.Kind == want.Kind && i.Name == want.Name && i.Screen == want.Screen &&
		i.Decision == want.Decision && i.NativeRevision == want.NativeRevision &&
		bytes.Equal(i.Candidate, want.Candidate) && sameWrapper(i.Selection, want.Selection) &&
		sameWrapper(i.Document, want.Document) && sameWrapper(i.Destination, want.Destination) &&
		sameWrapper(i.Directory, want.Directory)
}

// EverydayIntentOwnedBy checks the authenticated request against the runtime's
// live workspace. The executor independently checks its own pinned authority.
func EverydayIntentOwnedBy(i *Intent, w *storage.Workspace) bool {
	return i != nil && i.everydayProof.matches(i) && w.OwnsDirectory(i.everydayProof.directory)
}

func everydayResult(p *everydayRequest, d *storage.WorkspaceDirectory, r Result) Result {
	r.Operation, r.Revision, r.Kind = p.intent.Operation, p.intent.Revision, p.intent.Kind
	issued := copyResult(r)
	issued.everydayObservation = &everydayObservation{request: p, directory: d, result: copyResult(r)}
	return issued
}

func invalidEveryday(i *Intent, reason string) Result {
	r := Result{Err: refuse(reason)}
	if i != nil {
		r.Operation, r.Revision, r.Kind = i.Operation, i.Revision, i.Kind
	}
	return r
}

// RefuseEveryday settles a genuine undispatched request without filesystem I/O.
func RefuseEveryday(i *Intent, err error) Result {
	if i == nil || !i.everydayProof.matches(i) || err == nil ||
		!i.everydayProof.used.CompareAndSwap(false, true) {
		return invalidEveryday(i, "invalid or previously dispatched workspace refusal")
	}
	return everydayResult(i.everydayProof, nil, Result{Err: err})
}

// ExecuteEveryday performs exactly one authorized operation outside Reduce.
func ExecuteEveryday(i *Intent) Result {
	if i == nil || !i.everydayProof.matches(i) || !i.everydayProof.used.CompareAndSwap(false, true) {
		return invalidEveryday(i, "invalid or previously dispatched workspace request")
	}
	p := i.everydayProof
	if !p.workspace.OwnsDirectory(p.directory) {
		return everydayResult(p, nil, Result{Err: refuse("workspace directory is no longer live")})
	}
	r, d := p.execute()
	var output merge.Evaluation
	if p.intent.Kind == ReadMergeSecondary && r.Err == nil {
		output, r.Err = p.mergeInput.evaluate(r.Document, d)
	}
	result := everydayResult(p, d, r)
	result.everydayObservation.mergeOutput = output
	return result
}

func (p *everydayRequest) execute() (r Result, directory *storage.WorkspaceDirectory) {
	i := p.intent
	d := p.directory
	if isWorkspaceRead(i.Kind) && i.Selection != nil {
		if !p.workspace.OwnsSelection(i.Selection) {
			return Result{Err: refuse("foreign or unavailable file selection")}, nil
		}
		d = i.Selection.Directory()
		return readWorkspaceSelection(i.Selection), d
	}
	if i.Kind == PublishEveryday {
		return p.publish(), d
	}
	d, name, err := resolveWorkspaceName(d, i.Name)
	if err != nil {
		return Result{Err: err}, nil
	}
	if i.Kind == ObserveWorkspace {
		r.Destination, r.Err = d.Observe(name)
		return r, d
	}
	if isWorkspaceRead(i.Kind) {
		return readWorkspaceName(d, name), d
	}
	return Result{Err: refuse("unqualified workspace operation")}, nil
}

func readWorkspaceName(d *storage.WorkspaceDirectory, name string) Result {
	l, err := d.List(name)
	if err != nil {
		return Result{Err: err}
	}
	for index, entry := range l.Entries() {
		if entry.DOSName != name || entry.Mode.IsDir() {
			continue
		}
		selection, err := l.Select(index)
		if err != nil {
			return Result{Err: err}
		}
		return readWorkspaceSelection(selection)
	}
	return Result{Err: &storage.Failure{Kind: storage.ReadFailed, Stage: "workspace retrieve", Name: name, Cause: fs.ErrNotExist}}
}

func readWorkspaceSelection(selection *storage.EntrySelection) Result {
	doc, err := selection.Read()
	if err == nil && !selection.MatchesDocument(doc) {
		return Result{Err: refuse("selected native acquisition does not match its observation")}
	}
	return Result{Document: doc, Err: err}
}

func resolveWorkspaceName(base *storage.WorkspaceDirectory, draft string) (*storage.WorkspaceDirectory, string, error) {
	if strings.ContainsAny(draft, "/\x00") {
		return nil, "", refuse("workspace filename requires a DOS path")
	}
	leaf := draft
	dir := base
	if i := strings.LastIndexByte(draft, '\\'); i >= 0 {
		var err error
		dir, err = base.Navigate(draft[:i+1])
		if err != nil {
			return nil, "", err
		}
		leaf = draft[i+1:]
	} else if len(draft) >= 2 && draft[1] == ':' {
		var err error
		dir, err = base.Navigate(draft[:2])
		if err != nil {
			return nil, "", err
		}
		leaf = draft[2:]
	}
	name, err := storage.DOSName(leaf)
	return dir, name, err
}

func (p *everydayRequest) publish() Result {
	i := p.intent
	d := p.directory.Directory()
	id := storage.PublicationID{Operation: i.Operation, Revision: i.Revision}
	var save storage.SaveResult
	var err error
	if i.Document == nil {
		prepared, prepErr := d.PrepareNewSave(i.Destination, i.Candidate, i.Decision, p.backup, id)
		if prepErr != nil {
			return Result{Err: prepErr}
		}
		save, err = d.PublishNewSave(prepared, id)
	} else if prior, exists := i.Destination.Identity(); exists && prior.ID == i.Document.Identity().ID &&
		i.Destination.Name() == i.Document.Name() && i.Destination.DirectoryID() == i.Document.DirectoryID() &&
		bytes.Equal(i.Document.Export(), i.Candidate) {
		out, err := d.Save(i.Document, i.Destination, i.Decision)
		return Result{Document: i.Document, Outcome: out, Err: err}
	} else {
		prepared, prepErr := d.PrepareSave(i.Document, i.Destination, i.Candidate, i.Decision, p.backup, id)
		if prepErr != nil {
			return Result{Err: prepErr}
		}
		save, err = d.PublishSave(prepared, id)
	}
	if err != nil {
		return Result{Err: err}
	}
	if save.ID != id || save.Document == nil || !bytes.Equal(save.Document.Export(), i.Candidate) ||
		save.Outcome.Name != i.Destination.Name() || save.Outcome.Identity != save.Document.Identity() {
		return Result{Err: &storage.Failure{Kind: storage.PublicationUncertain, Stage: "workspace save receipt", Name: i.Name, DestinationMayExist: true}}
	}
	return Result{Document: save.Document, Outcome: save.Outcome}
}

func (s Session) beginEveryday(kind IntentKind, selection *storage.EntrySelection, name string, insert bool, decision storage.Decision) (Session, *Intent, error) {
	if s.workspace == nil || s.workspaceBase == nil {
		return s, nil, refuse("command requires a configured workspace")
	}
	d := s.workspaceBase
	i := Intent{Operation: s.sequence + 1, Revision: s.revision, Kind: kind, Screen: s.screen,
		Name: name, Decision: decision, NativeRevision: s.native.Revision(), Selection: copySelection(selection)}
	switch kind {
	case ReadSelection, ReadMergePrimary, ReadMergeSecondary:
		if selection != nil {
			if !s.workspace.OwnsSelection(selection) {
				return s, nil, refuse("foreign or unavailable file selection")
			}
			d = selection.Directory()
			i.Name = selection.Name()
		}
	case PublishEveryday:
		d = s.workspaceTarget
		if d == nil || s.target == nil || s.native == nil {
			return s, nil, refuse("workspace save needs an observed target and document")
		}
		var err error
		switch {
		case s.source != nil && s.native.Revision() == s.saved:
			// A loaded or published Fast Save image can have a different
			// wire prefix from the current editing revision. Keep that
			// exact source for every unchanged save, including Save As.
			i.Candidate = s.source.Export()
		case s.mergeResult.active():
			i.Candidate, err = s.exportMergeResult()
		case !s.fastSaveDisabled && !s.fastSavePurged && s.native.Birth().IsLoaded():
			i.Candidate, err = s.native.ExportFastSave()
		case s.mergeSource:
			i.Candidate, err = s.native.ExportFormattedMergeSource()
		case s.native.Birth().IsLoaded():
			i.Candidate, err = s.native.ExportCompactFastSave(!s.fastSaveDisabled)
		default:
			i.Candidate, err = s.native.Export()
		}
		if err != nil {
			return s, nil, err
		}
		i.Name, i.Document, i.Destination = s.target.Name(), s.source, s.target
	}
	i.Directory = d.Directory()
	p := &everydayRequest{intent: *copyIntent(&i), workspace: s.workspace, directory: d, insert: insert, backup: s.originalBackup}
	if kind == ReadMergeSecondary {
		p.mergeInput = s.mergePrimary
	}
	if kind == PublishEveryday && s.fastSaveDisabled &&
		(s.native.Birth().IsLoaded() || s.mergeResult.active() && !s.mergeResult.occupied) &&
		s.native.Revision() != s.saved {
		p.purgesFastSave = true
	}
	i.everydayProof = p
	s.pending = copyIntent(&i)
	s.sequence++
	s.resume, s.mode = s.mode, Waiting
	s.notice = ""
	return s, copyIntent(s.pending), nil
}

func (s Session) requestWorkspaceRetrieve(selection *storage.EntrySelection, name string) (Session, *Intent, error) {
	if s.workspace == nil || s.selection || s.homes != 0 || (selection == nil && name == "") {
		return s, nil, refuse("workspace retrieve needs a valid name or selection")
	}
	if selection != nil && !s.workspace.OwnsSelection(selection) {
		return s, nil, refuse("foreign or unavailable file selection")
	}
	if s.native != nil && s.native.TokenCount() > 0 {
		s.resume, s.mode = s.mode, RetrieveInsertQuestion
		s.retrieveSelection, s.retrieveDraft = copySelection(selection), name
		return s, nil, nil
	}
	return s.beginEveryday(ReadSelection, selection, name, false, storage.NoOverwrite)
}

func (s Session) answerRetrieveInsertion(command Command) (Session, *Intent, error) {
	switch command {
	case Yes, No, F1, Escape, Enter:
	default:
		return s, nil, refuse("answer the retrieve insertion question")
	}
	selection, name := s.retrieveSelection, s.retrieveDraft
	s.mode, s.retrieveSelection, s.retrieveDraft = s.resume, nil, ""
	if command == Yes {
		return s.beginEveryday(ReadSelection, selection, name, true, storage.NoOverwrite)
	}
	return s, nil, nil
}

func (s Session) answerWorkspaceReplacement(command Command) (Session, *Intent, error) {
	switch command {
	case Yes:
		s.mode = SaveName
		return s.beginEveryday(PublishEveryday, nil, s.target.Name(), false, storage.AllowOverwrite)
	case No, Enter:
		s.mode, s.caret, s.touched = SaveName, 0, false
		s.target, s.workspaceTarget = nil, nil
		return s, nil, nil
	case F1, Escape:
		s.mode, s.fromExit = Editing, false
		s.target, s.workspaceTarget = nil, nil
		return s, nil, nil
	default:
		return s, nil, refuse("answer the replacement question")
	}
}

func (s Session) completeEveryday(result Result) (Session, *Intent, error) {
	o := result.everydayObservation
	if o == nil {
		return s, nil, refuse("unauthenticated workspace completion")
	}
	p := o.request
	if result.Operation != p.intent.Operation || result.Revision != p.intent.Revision || result.Kind != p.intent.Kind {
		return s, nil, refuse("workspace completion envelope mismatch")
	}
	result = copyResult(o.result)
	if s.pending == nil || s.pending.everydayProof != p {
		s.detached = receipt(result, false)
		return s, nil, nil
	}
	if s.screen != p.intent.Screen || s.revision != p.intent.Revision || s.native.Revision() != p.intent.NativeRevision {
		s.pending, s.mode = nil, s.resume
		s.detached = receipt(result, false)
		s.notice = "Older revision completed; current edits and name retained"
		return s, nil, nil
	}
	s = s.advanced()
	s.pending, s.mode = nil, s.resume
	s.last = receipt(result, true)
	if result.Err != nil && o.mergeOutput.Fragment == nil {
		s.notice = result.Err.Error()
		if !isWorkspaceRead(result.Kind) {
			s.lastSave = SaveFailed
			if s.last.DestinationMayExist {
				s.lastSave = SaveUncertain
			}
		}
		return s, nil, nil
	}
	switch result.Kind {
	case ReadMergePrimary, ReadMergeSecondary:
		next, err := s.completeMergeRead(result, o.directory, o.mergeOutput)
		if err != nil {
			s.notice = err.Error()
			s.last.Result.Err = err
			return s, nil, nil
		}
		if result.Err != nil {
			next.notice = result.Err.Error()
		}
		return next, nil, nil
	case ReadSelection:
		next, err := s.adoptWorkspaceRead(result.Document, o.directory, p.insert)
		if err != nil {
			s.notice = err.Error()
			s.last.Result.Err = err
			return s, nil, nil
		}
		return next, nil, nil
	case ObserveWorkspace:
		s.target, s.workspaceTarget = copyDestination(result.Destination), o.directory
		if s.target.Exists() {
			s.mode = ReplaceQuestion
			return s, nil, nil
		}
		return s.beginEveryday(PublishEveryday, nil, s.target.Name(), false, storage.NoOverwrite)
	case PublishEveryday:
		s.fastSavePurged = s.fastSavePurged || p.purgesFastSave
		s.source, s.workspaceBase = copySource(result.Document), o.directory
		s.name, s.saved = result.Document.Name(), p.intent.NativeRevision
		s.publishedRevision, s.publishedName = s.saved, s.name
		s.published = receipt(result, true)
		if s.newPhase == NewUnpublished {
			s.newPhase = NewAnchored
		}
		s.lastSave = NewNamePublished
		if result.Outcome.State == storage.Unchanged {
			s.lastSave = SameFileNoOp
		}
		s.mode, s.notice = Editing, ""
		if s.historyValid && s.history.Qualified() {
			h, err := s.history.Separate(document.SavedBoundary)
			if err == nil {
				s.history = h
			} else {
				s.historyValid = false
			}
		}
		if s.fromExit {
			s.mode, s.fromExit = s.exitPromptMode(), false
		}
		return s, nil, nil
	default:
		return s, nil, refuse("unknown workspace completion")
	}
}

func (s Session) adoptWorkspaceRead(source *storage.Document, directory *storage.WorkspaceDirectory, insert bool) (Session, error) {
	previous := s
	native, err := document.Parse(source.Export())
	if err != nil {
		return s, err
	}
	if insert {
		return s.insertEverydayDocument(native)
	}
	// A qualified Fast Save image has a compact editing representation.
	// The source capability and original birth still own its exact wire
	// bytes, and every unchanged save uses those bytes.
	if compact, compactErr := native.CompactFastSave(); compactErr == nil {
		native = compact
	}
	cursor, err := native.CursorAt(0)
	if err != nil {
		return s, err
	}
	history, err := document.NewHistory(native)
	notice := ""
	mergeSource := false
	if err != nil {
		var failure *document.Failure
		if !errors.As(err, &failure) {
			return s, err
		}
		switch failure.Category {
		case document.UnsupportedPrefix, document.UnsupportedBody, document.UnsupportedMetadata, document.UnsupportedResource, document.MutationLimit:
			mergeSource = native.CheckMergeSource() == nil
			if mergeSource {
				history, err = document.NewMergeHistory(native)
			}
			if !mergeSource {
				notice = "Read-only native document: " + string(failure.Category)
			}
		default:
			return s, err
		}
	}
	s.native, s.cursor, s.history = native, cursor.WithReveal(s.cursor.Reveal()), history
	s.mergeSource, s.mergeResult = mergeSource, mergeResultState{}
	s.fastSavePurged = false
	s.historyValid, s.historyUsed = err == nil, err == nil
	s.source, s.workspaceBase = copySource(source), directory
	s.saved, s.name, s.mode = native.Revision(), source.Name(), Editing
	s.newPhase, s.first, s.genesis = "", nil, document.Revision{}
	s.publishedRevision, s.publishedName, s.published = document.Revision{}, "", Receipt{}
	s.lastSave, s.notice, s.homes = NotSaved, notice, 0
	s.selection, s.verticalRun = false, false
	s.deletion, s.preview = document.Deletion{}, document.Preview{}
	s.revision++
	return previous.carryMergeHistory(s)
}

func (s Session) insertEverydayDocument(native *document.Document) (Session, error) {
	edit, err := s.native.InsertDocument(s.cursor, native)
	if err != nil {
		return s, err
	}
	history := s.history
	if s.historyValid {
		history, err = history.AfterRetrieval(edit)
		if err != nil {
			return s, err
		}
	}
	next, err := s.finishEverydayEdit(edit, history)
	if err != nil {
		return s, err
	}
	next.mode, next.notice = Editing, ""
	return next, nil
}

func (s Session) adoptEverydayEdit(edit document.EditResult) (Session, error) {
	history := s.history
	var err error
	if s.historyValid {
		history, err = history.AfterEverydayEdit(edit)
		if err != nil {
			return s, err
		}
	}
	return s.finishEverydayEdit(edit, history)
}

func (s Session) finishEverydayEdit(edit document.EditResult, history document.History) (Session, error) {
	old := s.native.Revision()
	next := s
	var err error
	next.native, next.cursor, next.history = edit.Document, edit.Cursor, history
	if next.native.Revision() != old {
		next, err = next.reflowEveryday()
		if err != nil {
			return s, err
		}
		next.revision++
		next.lastSave = NotSaved
	}
	next.verticalRun = false
	return next, nil
}

func (s Session) reflowEveryday() (Session, error) {
	settings := EverydaySettings()
	plan, err := layout.PlanReflow(s.native, settings)
	if err != nil {
		return s, err
	}
	next, err := s.adoptLayoutPlan(plan)
	if err != nil {
		return s, err
	}
	physical, err := layout.FromDocument(next.native, settings)
	if err != nil {
		return s, err
	}
	var changes []document.ReflowChange
	for _, line := range physical.Lines {
		for _, item := range line.Tokens {
			if item.Token.Kind != document.Tab {
				continue
			}
			_, column, known := physical.PositionAt(item.Index)
			target, ok := settings.NextTabColumn(column)
			if !known || !ok {
				return s, refuse("Tab cache position is not qualified")
			}
			changes = append(changes, document.ReflowChange{
				At: item.Index, Kind: document.RefreshTabCache, Column: uint16(target),
			})
		}
	}
	if len(changes) == 0 {
		return next, nil
	}
	cache, err := document.NewReflowPlan(next.native, changes)
	if err != nil {
		return s, err
	}
	refreshed, err := next.adoptLayoutPlan(cache)
	if err != nil {
		return s, err
	}
	return refreshed, nil
}

func (s Session) adoptLayoutPlan(plan document.ReflowPlan) (Session, error) {
	edit, err := s.native.AdoptReflow(s.cursor, plan)
	if err != nil {
		return s, err
	}
	if edit.Document.Revision() == s.native.Revision() {
		return s, nil
	}
	if s.historyValid {
		s.history, err = s.history.AfterReflow(edit)
		if err != nil {
			return s, err
		}
	}
	s.native, s.cursor = edit.Document, edit.Cursor
	return s, nil
}

func (s Session) settleDeletion(result document.Deletion, command Command) (Session, *Intent, error) {
	next := s.applyDeletion(result, command)
	if s.workspace != nil && next.native.Revision() != s.native.Revision() {
		if command == Restore && (s.mergeSource || next.native.IsAuthoredMergeSource()) {
			next.mergeSource = next.native.IsAuthoredMergeSource()
			next.verticalRun = false
			return next, nil, nil
		}
		if s.preserveTrailingWrapAfterBackspace(next, command) {
			return next, nil, nil
		}
		reflowed, err := next.reflowEveryday()
		if err != nil {
			return s, nil, err
		}
		return reflowed, nil, nil
	}
	return next, nil, nil
}

// At EOF the original first removes the glyph and leaves its DSRt. The next
// Backspace removes the boundary alone. Immediate reflow would collapse that
// two-keystroke transition and delete the preceding glyph too soon.
func (s Session) preserveTrailingWrapAfterBackspace(next Session, command Command) bool {
	count := s.native.TokenCount()
	if command != Backspace || s.selection || s.cursor.Gap() != count || count < 2 ||
		next.native.TokenCount() != count-1 {
		return false
	}
	last, err := s.native.Token(count - 1)
	if err != nil {
		return false
	}
	if last.Kind == document.DeletedSoftReturn {
		return true
	}
	previous, err := s.native.Token(count - 2)
	return err == nil && last.Kind == document.ASCII && previous.Kind == document.DeletedSoftReturn
}

// WithOriginalBackup applies the observed document backup setting to both
// document screens. Resource writes use their separate storage policy.
func (s Session) WithOriginalBackup(backup storage.OriginalBackup) (Session, error) {
	if s.workspace == nil || (backup != storage.OriginalBackupOff && backup != storage.OriginalBackupOn) ||
		s.mode != Editing || s.pending != nil {
		return s, refuse("original backup preference requires idle workspace editing")
	}
	s.originalBackup = backup
	if s.other != nil {
		other := *s.other
		other.originalBackup = backup
		s.other = &other
	}
	return s, nil
}

func (s Session) everydayTab() (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || s.selection {
		return s, nil, refuse("Tab requires qualified workspace editing")
	}
	lay, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return s, nil, err
	}
	_, col, known := lay.PositionAt(s.cursor.Gap())
	target, ok := lay.Settings.NextTabColumn(col)
	if !known || !ok {
		return s, nil, refuse("Tab position is not qualified")
	}
	edit, err := s.native.InsertEverydayTab(s.cursor, target)
	if err != nil {
		return s, nil, err
	}
	next, err := s.adoptEverydayEdit(edit)
	return next, nil, err
}

func (s Session) everydayAttribute(underline bool) (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || !s.historyValid || s.selection {
		return s, nil, refuse("attribute requires qualified workspace editing")
	}
	attribute := document.BoldAttribute
	active, activeOK := s.history.ActiveBold(s.native)
	if underline {
		attribute = document.UnderlineAttribute
		active, activeOK = s.history.ActiveUnderline(s.native)
	}
	var result document.BoldResult
	var err error
	if activeOK {
		result, err = s.native.CloseEverydayFormat(s.cursor, active, attribute)
	} else {
		result, err = s.native.BeginEverydayFormat(s.cursor, attribute)
	}
	if err != nil {
		return s, nil, err
	}
	history, err := s.history.AfterEverydayFormat(result)
	if err != nil {
		return s, nil, err
	}
	s.native, s.cursor, s.history = result.Document(), result.Cursor(), history
	if result.Changed() {
		s.revision++
		s.lastSave = NotSaved
	}
	return s, nil, nil
}

func (s Session) everydayMove(command Command) (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil {
		return s, nil, refuse("motion requires a workspace document")
	}
	lay, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return s, nil, err
	}
	current := s.cursor.Gap()
	_, column, known := lay.PositionAt(current)
	if !known {
		return s, nil, refuse("physical cursor position is not qualified")
	}
	var gap int
	var ok bool
	switch command {
	case Up, Down:
		if !s.verticalRun {
			s.desiredColumn = column
		}
		s.verticalRun = true
		delta := 1
		if command == Up {
			delta = -1
		}
		gap, ok = lay.VerticalGap(current, s.desiredColumn, delta)
	case PageUp:
		gap, ok = lay.PageGap(current, -1)
	case PageDown:
		gap, ok = lay.PageGap(current, 1)
	case Home, End:
		gap, ok = lay.LineBoundary(current, command == End)
	}
	s.homes = 0
	if !ok {
		return s, nil, nil
	}
	// Original Reveal page movement highlights the dormant return at the
	// next page's top; the ordinary caret remains at the first editable gap.
	if s.cursor.Reveal() && (command == PageUp || command == PageDown) && gap > 0 {
		if token, tokenErr := s.native.Token(gap - 1); tokenErr == nil && token.Kind == document.DormantHardReturn {
			gap--
		}
	}
	cursor, err := s.native.CursorAt(gap)
	if err != nil {
		return s, nil, err
	}
	s.history, err = s.interrupted()
	if err != nil {
		return s, nil, err
	}
	s.cursor = cursor.WithReveal(s.cursor.Reveal())
	return s, nil, nil
}

func (s Session) everydayBlockMove(command Command) (Session, *Intent, error) {
	delta := 1
	if command == Left {
		delta = -1
		// WP78 history-repeat frames 15–18: the first Left at
		// normal-view EOF leaves the selection cursor at the anchor.
		if !s.blockMoved && !s.cursor.Reveal() && s.cursor.Gap() == s.native.TokenCount() {
			s.blockMoved = true
			return s, nil, nil
		}
	}
	if (delta < 0 && s.cursor.Gap() == 0) || (delta > 0 && s.cursor.Gap() == s.native.TokenCount()) {
		return s, nil, nil
	}
	cursor, err := s.cursor.Move(delta)
	if err == nil {
		s.cursor = cursor
		s.blockMoved = true
		s.history, err = s.interrupted()
	}
	return s, nil, err
}

func (s Session) switchEverydayDocument() (Session, *Intent, error) {
	if s.mode != Editing || s.pending != nil || s.selection || s.homes != 0 || s.macroOwner != nil || s.macroRepeat != 1 || s.macroVisitedNew {
		return s, nil, refuse("document switch outside qualified workspace editing")
	}
	current := s
	current.other = nil
	var next Session
	if s.other == nil {
		number := uint8(1)
		if s.screen == 1 {
			number = 2
		}
		seed := Session{initialized: true, locations: s.locations, workspace: s.workspace,
			workspaceBase: s.workspaceBase, originalBackup: s.originalBackup, mode: Editing,
			bufferID: &bufferIdentity{number}, screen: number, macroRepeat: 1}
		var err error
		next, err = seed.renewed()
		if err != nil {
			return s, nil, err
		}
	} else {
		next = *s.other
	}
	next.other, next.sequence, next.transition = &current, s.sequence, s.transition
	next, err := s.carryMergeHistory(next)
	if err != nil {
		return s, nil, err
	}
	return next, nil, nil
}

// WithFastSaveDisabled selects the original compact-save setting for this
// workspace session. Unchanged saves retain the acquired or published bytes.
func (s Session) WithFastSaveDisabled(disabled bool) Session {
	s.fastSaveDisabled = disabled
	return s
}
