package editor

import (
	"bytes"
	"errors"
	"io/fs"
	"math"
	"sort"
	"strconv"
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
	if i.Kind == AppendWorkspace {
		return appendWorkspaceBlock(d, name, i), d
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
	case AppendWorkspace:
		var err error
		i.Candidate, err = s.blockCopy.Export()
		if err != nil {
			return s, nil, err
		}
	case PublishEveryday:
		d = s.workspaceTarget
		if d == nil || s.target == nil || s.native == nil {
			return s, nil, refuse("workspace save needs an observed target and document")
		}
		native := s.native
		var err error
		if s.native.Revision() != s.saved {
			native, err = native.FinalizeTableOverflow()
			if err != nil {
				return s, nil, err
			}
		}
		_, initialCodes := native.InitialLineSpacing()
		switch {
		case s.source != nil && s.native.Revision() == s.saved:
			// A loaded or published Fast Save image can have a different
			// wire prefix from the current editing revision. Keep that
			// exact source for every unchanged save, including Save As.
			i.Candidate = s.source.Export()
		case initialCodes:
			i.Candidate, err = native.ExportInitialCodesSave(!s.fastSaveDisabled && !s.fastSavePurged)
		case native.UsesSummaryPrefix():
			i.Candidate, err = native.ExportSummarySave(!s.fastSaveDisabled && !s.fastSavePurged)
		case s.mergeResult.active():
			i.Candidate, err = s.exportMergeResult()
		case !s.fastSaveDisabled && !s.fastSavePurged && s.native.Birth().IsLoaded():
			if s.mergeSource {
				if err = s.native.CheckMergeSource(); err != nil {
					return s, nil, err
				}
			}
			i.Candidate, err = native.ExportFastSave()
		case s.mergeSource:
			i.Candidate, err = native.ExportFormattedMergeSource()
		case s.native.Birth().IsLoaded():
			i.Candidate, err = native.ExportCompactFastSave(!s.fastSaveDisabled)
		default:
			i.Candidate, err = native.Export()
		}
		if err != nil {
			return s, nil, err
		}
		deferred := s.backwardPageSave
		if s.native.Revision() != s.saved && deferred.revision == s.native.Revision() &&
			s.cursor.Gap() <= deferred.record {
			i.Candidate, err = native.OmitDeferredPageRecord(i.Candidate, deferred.record)
			if err != nil {
				return s, nil, err
			}
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
		if !isWorkspaceRead(result.Kind) && result.Kind != AppendWorkspace {
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
	case AppendWorkspace:
		s.blockCopy, s.mode, s.notice = nil, Editing, ""
		return s, nil, nil
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

// A lone soft-page owner at the normal page boundary is the DOS deferred
// save form. Restore its cache for editing while retaining the acquired source.
func restoreDeferredPageOnRead(native *document.Document) *document.Document {
	index := -1
	previous := document.Opaque
	for i := 0; i < native.TokenCount(); i++ {
		token, _ := native.Token(i)
		if (token.Kind == document.SoftPage || token.Kind == document.DeletedSoftPage) && previous != document.EndOfPage {
			if index >= 0 {
				return native
			}
			index = i
		}
		previous = token.Kind
	}
	if index < 0 {
		return native
	}
	projected, err := layout.FromDocument(native, EverydaySettings())
	if err != nil {
		return native
	}
	line, _, ok := projected.PositionAt(index)
	if !ok {
		return native
	}
	physical := projected.Lines[line]
	if physical.Row != 53 || physical.Page < 1 || physical.Page > 65535 {
		return native
	}
	restored, err := native.RestoreDeferredSoftPage(index, uint16(physical.Page))
	if err != nil {
		return native
	}
	return restored
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
	native = restoreDeferredPageOnRead(native)
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
			_, sheet := native.SpreadsheetTable()
			if _, table := native.SimpleTable(); !mergeSource && !table && !sheet {
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
	return previous.carryEverydayHistory(s)
}

func (s Session) importDOSText(name string, softReturns bool) (Session, error) {
	if s.workspaceBase == nil || s.native == nil || s.selection || s.homes != 0 {
		return s, refuse("DOS text retrieval requires an editable workspace document")
	}
	raw, err := s.workspaceBase.ReadDOSBytes(name)
	if err != nil {
		return s, err
	}
	edit, err := s.native.InsertDOSText(s.cursor, raw, softReturns)
	if err != nil {
		return s, err
	}
	if s.historyValid {
		history, err := s.history.AfterRetrieval(edit)
		if err != nil {
			return s, err
		}
		s.history = history
	}
	s.native, s.cursor = edit.Document, edit.Cursor
	s.verticalRun, s.notice = false, ""
	if edit.Changed {
		s.revision++
		s.lastSave = NotSaved
	}
	return s, nil
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
	changes := physical.ParagraphPositionChanges()
	for _, line := range physical.Lines {
		for _, item := range line.Tokens {
			if item.Token.Kind == document.CenterLine || item.Token.Kind == document.FlushRight || item.Token.Kind == document.DecimalTab || item.Token.Kind == document.SoftDecimalTab {
				anchor := line.RightInches
				if item.Token.Kind == document.CenterLine {
					anchor = (line.LeftInches + line.RightInches) / 2
				} else if item.Token.Kind == document.DecimalTab || item.Token.Kind == document.SoftDecimalTab {
					anchor = float64(physical.DecimalAnchor(item.Index)) / document.UnitsPerInch
				}
				changes = append(changes, document.ReflowChange{
					At: item.Index, Kind: document.RefreshAlignmentCache,
					Position: uint16(math.Round(item.LeftInches * document.UnitsPerInch)),
					Anchor:   uint16(math.Round(anchor * document.UnitsPerInch)),
				})
				continue
			}
			if item.Token.Kind != document.Tab || item.Token.OutlineIndent() {
				continue
			}
			target := int(math.Round((item.LeftInches + item.WidthInches - settings.MarginLeftInches) * settings.CPI))
			if target < 0 || target > 75 {
				return s, refuse("Tab cache position is not qualified")
			}
			changes = append(changes, document.ReflowChange{
				At: item.Index, Kind: document.RefreshTabCache, Column: uint16(target), CustomTab: target%5 != 0 || target > 65 || target == 0,
			})
		}
	}
	if len(changes) == 0 {
		return next, nil
	}
	sort.Slice(changes, func(i, j int) bool { return changes[i].At < changes[j].At })
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
	return err == nil && last.Kind.IsCharacter() && previous.Kind == document.DeletedSoftReturn
}

// WithOriginalBackup applies the observed document backup setting to both
// document screens. Resource writes use their separate storage policy.
func (s Session) WithOriginalBackup(backup storage.OriginalBackup) (Session, error) {
	if s.workspace == nil || (backup != storage.OriginalBackupOff && backup != storage.OriginalBackupOn) ||
		s.mode != Editing || s.pending != nil {
		return s, refuse("original backup preference requires idle workspace editing")
	}
	s.originalBackup = backup
	for i, screen := range s.screens {
		if screen != nil {
			copy := *screen
			copy.originalBackup = backup
			s.screens[i] = &copy
		}
	}
	if s.other != nil {
		other := *s.other
		other.originalBackup = backup
		s.other = &other
	}
	return s, nil
}

func (s Session) indentColumn() int {
	for i := s.cursor.Gap() - 1; i >= 0; i-- {
		t, _ := s.native.Token(i)
		switch t.Kind {
		case document.Indent, document.DoubleIndent:
			return t.IndentColumn()
		case document.EndIndent, document.HardReturn, document.HardPage, document.HardReturnSoftPage:
			return 0
		}
	}
	return 0
}

func (s Session) everydayTab(command Command) (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || s.selection {
		return s, nil, refuse("Tab requires qualified workspace editing")
	}
	lay, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return s, nil, err
	}
	target, decimal, ok := lay.NextTabStopAt(s.cursor.Gap())
	if !ok {
		return s, nil, refuse("Tab position is not qualified")
	}
	var edit document.EditResult
	switch command {
	case Indent:
		edit, err = s.native.InsertIndent(s.cursor, s.indentColumn(), target)
	case DoubleIndent:
		edit, err = s.native.InsertDoubleIndent(s.cursor, s.indentColumn(), target)
	case MarginRelease:
		line, column, known := lay.PositionAt(s.cursor.Gap())
		if !known {
			return s, nil, refuse("Margin release requires a known cursor position")
		}
		margin := int(math.Round((lay.Lines[line].LeftInches - lay.Settings.MarginLeftInches) * lay.Settings.CPI))
		if column <= margin {
			return s, nil, nil
		}
		target = margin + (column-margin-1)/5*5
		edit, err = s.native.InsertMarginRelease(s.cursor, target)
	default:
		if decimal || s.ColumnMathActive() {
			edit, err = s.native.InsertAlignment(s.cursor, document.SoftDecimalTab)
		} else {
			edit, err = s.native.InsertPositionedTab(s.cursor, target)
		}
	}
	if err != nil {
		return s, nil, err
	}
	next, err := s.adoptEverydayEdit(edit)
	return next, nil, err
}

func (s Session) everydayAttribute(underline bool) (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || !s.historyValid {
		return s, nil, refuse("attribute requires qualified workspace editing")
	}
	attribute := document.BoldAttribute
	active, activeOK := s.history.ActiveBold(s.native)
	if underline {
		attribute = document.UnderlineAttribute
		active, activeOK = s.history.ActiveUnderline(s.native)
	}
	if s.mergeSource {
		var edit document.EditResult
		var err error
		if s.selection {
			edit, err = s.native.ApplyMergeFieldAttribute(s.anchor, s.cursor, attribute)
		} else {
			edit, err = s.native.ToggleMergeFieldAttribute(s.cursor, attribute)
		}
		if err != nil {
			return s, nil, err
		}
		next, intent, err := s.adoptMergeAuthoring(edit)
		if err == nil {
			next.selection, next.blockMoved = false, false
			next.anchor = document.Cursor{}
		}
		return next, intent, err
	}
	if s.selection {
		edit, err := s.native.ApplyEverydayBlockFormat(s.anchor, s.cursor, attribute)
		if err != nil {
			return s, nil, err
		}
		next, err := s.adoptEverydayEdit(edit)
		if err != nil {
			return s, nil, err
		}
		next.selection, next.blockMoved = false, false
		next.anchor = document.Cursor{}
		return next, nil, nil
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
	s.blockMoved = s.blockMoved || s.selection && cursor.Gap() != current
	s.cursor = cursor.WithReveal(s.cursor.Reveal())
	return s, nil, nil
}

func (s Session) everydayScreenEdge(right bool, width int) (Session, *Intent, error) {
	if width <= 0 {
		if right {
			return s.everydayMove(End)
		}
		return s.everydayMove(Home)
	}
	projected, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return s, nil, err
	}
	line, column, ok := projected.PositionAt(s.cursor.Gap())
	if !ok {
		return s, nil, refuse("cursor is outside the layout")
	}
	// Use the same scroll position as the displayed editing row.
	target := layout.ScreenColumnOffset(column, width)
	if right {
		target += width - 1
	}
	gap, ok := projected.GapAt(line, target)
	s.homes, s.verticalRun = 0, false
	if !ok || gap == s.cursor.Gap() {
		return s, nil, nil
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

func (s Session) everydayWordMove(command Command) (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil {
		return s, nil, refuse("word motion requires a workspace document")
	}
	count := s.native.TokenCount()
	direction, index := 1, s.cursor.Gap()
	if command == WordLeft {
		direction, index = -1, index-1
	}

	// Formatting codes do not split words or receive the destination caret.
	// WordPerfect includes punctuation embedded between spaces in one word.
	cursor := s.cursor
	seenText, seenSeparator := false, false
	target := 0
	if direction > 0 {
		target = count
	}
	for index >= 0 && index < count {
		token, err := s.native.Token(index)
		if err != nil {
			return s, nil, err
		}
		separator := false
		switch token.Kind {
		case document.ASCII:
			separator = token.Raw[0] == ' '
		case document.ExtendedCharacter, document.DOSControl:
		case document.HardSpace, document.HardReturn, document.SoftReturn, document.SoftPage, document.HardPage, document.HardReturnSoftPage, document.Tab, document.Indent:
			separator = true
		default:
			cursor, err = cursor.Move(direction)
			if err != nil {
				return s, nil, err
			}
			index += direction
			continue
		}
		if direction < 0 {
			if separator && seenText {
				break
			}
			if !separator {
				target = index
			}
		} else if !separator && seenSeparator {
			target = index
			break
		}
		seenText = seenText || !separator
		seenSeparator = seenSeparator || separator
		cursor, err = cursor.Move(direction)
		if err != nil {
			return s, nil, err
		}
		index += direction
	}
	s.homes, s.verticalRun = 0, false
	if target == s.cursor.Gap() {
		return s, nil, nil
	}
	next, err := s.native.CursorAt(target)
	if err != nil {
		return s, nil, err
	}
	history, err := s.interrupted()
	if err != nil {
		return s, nil, err
	}
	s.history, s.cursor = history, next.WithReveal(s.cursor.Reveal())
	s.blockMoved = s.blockMoved || s.selection
	return s, nil, nil
}

func (s Session) deleteEverydaySpan(command Command) (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || s.selection {
		return s, nil, refuse("word or line deletion requires workspace editing")
	}
	original := s
	s.homes, s.verticalRun = 0, false
	gap, count := s.cursor.Gap(), s.native.TokenCount()
	first, last := gap, gap
	if command == DeleteToLineEnd {
		projected, err := layout.FromDocument(s.native, EverydaySettings())
		if err != nil {
			return original, nil, err
		}
		if end, ok := projected.LineBoundary(gap, true); ok {
			last = end
		}
	} else {
		// A word has no punctuation boundary. Hard returns are retained,
		// including when Delete Word is pressed at the end of a paragraph.
		classify := func(index int) (space, boundary, format bool) {
			token, _ := s.native.Token(index)
			switch token.Kind {
			case document.ASCII:
				return token.Raw[0] == ' ', false, false
			case document.Tab, document.SoftReturn, document.SoftPage:
				return true, false, false
			case document.ExtendedCharacter, document.DOSControl, document.DeletedSoftReturn:
				return false, false, false
			case document.BoldOn, document.BoldOff, document.UnderlineOn, document.UnderlineOff:
				return false, false, true
			default:
				return false, true, false
			}
		}
		if command != Backspace {
			seenSpace := false
			for last < count {
				space, boundary, format := classify(last)
				if boundary || !format && !space && seenSpace {
					break
				}
				if format && seenSpace {
					break
				}
				seenSpace = seenSpace || space
				last++
			}
		}
		if command != Delete {
			for first > 0 {
				space, boundary, _ := classify(first - 1)
				if space || boundary {
					break
				}
				first--
			}
		}
	}
	if first >= last {
		return s, nil, nil
	}
	start, _ := s.native.CursorAt(first)
	end, _ := s.native.CursorAt(last)
	reveal := s.cursor.Reveal()
	var result document.Deletion
	var err error
	if command == DeleteToLineEnd {
		result, err = s.native.DeleteEverydayLine(s.cursor, end.WithReveal(reveal), s.history)
	} else {
		var direction document.DeleteDirection
		if command == Backspace {
			direction = document.Backspace
		}
		if command == Delete {
			direction = document.ForwardDelete
		}
		result, err = s.native.DeleteEverydayRange(s.cursor, start.WithReveal(reveal), end.WithReveal(reveal), s.history, direction)
	}
	if err != nil {
		return original, nil, err
	}
	return s.settleDeletion(result, command)
}

func (s Session) deletePageRemainder() (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || s.selection || !s.historyValid || s.mergeSource {
		return s, nil, refuse("Delete Remainder of page requires an ordinary editable document")
	}
	physical, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return s, nil, err
	}
	gap := s.cursor.Gap()
	end := s.native.TokenCount()
	if line, _, known := physical.PositionAt(gap); known {
		page := physical.Lines[line].Page
		for i := line + 1; i < len(physical.Lines); i++ {
			if physical.Lines[i].Page > page {
				end = physical.Lines[i].StartGap - 2
				// Automatic pages can put the first physical gap before
				// the dormant hard return. Back up to the record owner.
				if token, err := s.native.Token(end); err == nil && token.Kind == document.HardReturnSoftPage {
					end--
				}
				break
			}
		}
	} else {
		return s, nil, refuse("Delete Remainder of page needs a qualified cursor position")
	}
	if end != s.native.TokenCount() {
		boundary, err := s.native.Token(end)
		if err != nil || boundary.Kind != document.EndOfPage {
			return s, nil, refuse("Delete Remainder of page needs a qualified page boundary")
		}
		transition, _ := s.native.Token(end + 1)
		if transition.Kind != document.HardPage && transition.Kind != document.HardReturnSoftPage &&
			transition.Kind != document.SoftPage && transition.Kind != document.DeletedSoftPage {
			return s, nil, refuse("Delete Remainder of page needs a qualified page boundary")
		}
	}
	if end <= gap {
		return s, nil, nil
	}
	cursor, err := s.native.CursorAt(end)
	if err != nil {
		return s, nil, err
	}
	result, err := s.native.ConfirmEverydayPageDeletion(s.cursor, cursor.WithReveal(s.cursor.Reveal()), s.history)
	if err != nil {
		return s, nil, err
	}
	return s.applyDeletion(result, DeletePageRemainder), nil, nil
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
	if err == nil && s.mergeSource {
		// The page-cache owner has no visible position in either view.
		index := min(cursor.Gap(), s.cursor.Gap())
		if token, tokenErr := s.native.Token(index); tokenErr == nil && token.Kind == document.EndOfPage {
			cursor, err = cursor.Move(delta)
		}
		if delta < 0 && err == nil {
			if token, tokenErr := s.native.Token(cursor.Gap() - 1); tokenErr == nil && token.Kind == document.EndOfPage {
				cursor, err = cursor.Move(delta)
			}
		}
	}
	if err == nil {
		s.cursor = cursor
		s.blockMoved = true
		s.history, err = s.interrupted()
	}
	return s, nil, err
}

func (s Session) seekBlock(event Event) (Session, *Intent, error) {
	if event.Command == Text && len(event.Text) != 1 {
		return s, nil, nil
	}
	cursor, err := s.seekCharacterOrReturn(event)
	if err != nil {
		return s, nil, err
	}
	if cursor != s.cursor {
		s.cursor, s.blockMoved = cursor, true
	}
	return s, nil, nil
}

func (s Session) seekCharacterOrReturn(event Event) (document.Cursor, error) {
	cursor := s.cursor
	for cursor.Gap() < s.native.TokenCount() {
		token, err := s.native.Token(cursor.Gap())
		if err != nil {
			return s.cursor, err
		}
		cursor, err = cursor.Move(1)
		if err != nil {
			return s.cursor, err
		}
		if event.Command == Enter && (token.Kind == document.HardReturn || token.Kind == document.HardReturnSoftPage) ||
			event.Command == Text && token.Kind.IsCharacter() && token.CharacterText() == event.Text {
			return cursor, nil
		}
	}
	return s.cursor, nil
}

func (s Session) gotoPress(event Event) (Session, *Intent, error) {
	original := s
	if event.Command == F1 || event.Command == Escape {
		s.mode, s.draft = Editing, ""
		return s, nil, nil
	}
	if event.Command == Backspace {
		s.draft = s.draft[:max(0, len(s.draft)-1)]
		return s, nil, nil
	}
	if event.Command == Text && event.Text != "" && strings.Trim(event.Text, "0123456789") == "" {
		if len(s.draft+event.Text) <= 6 {
			s.draft += event.Text
		}
		return s, nil, nil
	}
	if event.Command != Enter && (event.Command != Text || len(event.Text) != 1 || s.draft != "") {
		return s, nil, nil
	}
	cursor := s.cursor
	var err error
	if s.draft != "" {
		page, _ := strconv.Atoi(s.draft)
		projected, err := layout.FromDocument(s.native, EverydaySettings())
		if err != nil {
			return original, nil, err
		}
		for i, line := range projected.Lines {
			if line.Page == page {
				if gap, ok := projected.GapAt(i, 0); ok {
					cursor, err = s.native.CursorAt(gap)
					if err != nil {
						return original, nil, err
					}
				}
				break
			}
		}
	} else {
		cursor, err = s.seekCharacterOrReturn(event)
		if err != nil {
			return original, nil, err
		}
	}
	s.history, err = s.interrupted()
	if err != nil {
		return original, nil, err
	}
	s.cursor = cursor.WithReveal(s.cursor.Reveal())
	s.mode, s.draft, s.verticalRun = Editing, "", false
	return s, nil, nil
}

func (s Session) switchEverydayDocument(target uint8, create bool) (Session, *Intent, error) {
	if s.mode != Editing || s.pending != nil || s.selection || s.homes != 0 || s.macroOwner != nil || s.macroRepeat != 1 || s.macroVisitedNew {
		return s, nil, refuse("document switch outside qualified workspace editing")
	}
	if create {
		for i, screen := range s.screens {
			if screen == nil && uint8(i+1) != s.screen {
				return s.changeScreen(uint8(i+1), true, false)
			}
		}
		return s, nil, refuse("six documents are already open")
	}
	if target == 0 {
		target = s.nextScreen()
		if target == 0 {
			return s.switchEverydayDocument(0, true)
		}
	}
	return s.changeScreen(target, false, false)
}

func (s Session) nextScreen() uint8 {
	for offset := uint8(1); offset < MaxDocumentScreens; offset++ {
		index := (s.screen - 1 + offset) % MaxDocumentScreens
		if s.screens[index] != nil {
			return index + 1
		}
	}
	return 0
}

func (s Session) changeScreen(target uint8, create, closeCurrent bool) (Session, *Intent, error) {
	if target == s.screen {
		return s, nil, nil
	}
	if target < 1 || target > MaxDocumentScreens {
		return s, nil, refuse("document screen is not open")
	}
	var next Session
	if existing := s.screens[target-1]; existing != nil {
		next = *existing
	} else if create {
		seed := Session{initialized: true, locations: s.locations, workspace: s.workspace,
			workspaceBase: s.workspaceBase, originalBackup: s.originalBackup, mode: Editing,
			bufferID: &bufferIdentity{target}, screen: target, macroRepeat: 1}
		var err error
		next, err = seed.renewed()
		if err != nil {
			return s, nil, err
		}
	} else {
		return s, nil, refuse("document screen is not open")
	}
	next.screens = s.screens
	next.screens[target-1] = nil
	if !closeCurrent {
		current := s
		current.screens = [MaxDocumentScreens]*Session{}
		next.screens[s.screen-1] = &current
	}
	next.sequence, next.transition = s.sequence, s.transition
	next.proofResources = s.proofResources
	next, err := s.carryEverydayHistory(next)
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
