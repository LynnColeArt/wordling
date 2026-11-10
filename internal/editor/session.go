// Package editor implements a pure, revision-bound session reducer. Native edits
// and history use document; filesystem execution stays with the host adapter.
package editor

import (
	"bytes"
	"crypto/sha256"
	"errors"
	"fmt"
	"io/fs"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/storage"
)

type Mode string

const (
	Editing          Mode = "Editing"
	RetrieveName     Mode = "RetrieveName"
	SaveName         Mode = "SaveName"
	ReplaceQuestion  Mode = "ReplaceQuestion"
	ExitSaveQuestion Mode = "ExitSaveQuestion"
	ExitQuestion     Mode = "ExitQuestion"
	// ExitDocQuestion is the per-document exit question the original asks
	// after saving on exit when a second screen exists (EE-A12 frames
	// corrections/08 + corrections/30: "Exit doc 2?" / "Exit doc 1?").
	ExitDocQuestion Mode = "ExitDocQuestion"
	// Proofreading modes (Ctrl+F2 flow, frames spelling/proof 01–09).
	ProofMenuMode  Mode = "ProofMenu"
	ProofAskMode   Mode = "ProofAsk"
	ProofAckMode   Mode = "ProofAck"
	Waiting        Mode = "Waiting"
	Exited         Mode = "Exited"
	DeleteQuestion Mode = "DeleteQuestion"
	HistoryPreview Mode = "HistoryPreview"
	MacroName      Mode = "MacroName"
	MacroReady     Mode = "MacroReady"
	MacroRunning   Mode = "MacroRunning"
)

const MacroError Mode = "MacroError"

type Command uint8

const (
	Text     Command = iota
	Retrieve         // Original Shift+F10.
	Save             // Original F10.
	Reveal           // Original Alt+F3.
	F1
	Escape
	F7
	Home
	Up
	Right
	Left
	Backspace
	Enter
	Yes
	No
	Complete
	CancelOperation // Host safety operation; not an original key alias.
	Insert          // Original Insert mode toggle.
	Delete
	Block          // Original Alt+F4 selection start.
	Previous       // Original Undelete numeric 2.
	Restore        // Original Undelete numeric 1.
	Macro          // Original Alt+F10.
	SwitchDocument // Original Shift+F3; bounded two-screen context.
	RetryFirstRead // Explicit Linux host-safety retry; no original-key alias.
	Bold           // Native Bold authoring in the bounded New cohort.
	End            // Original End, to the end of the current line.
	Down           // Completes Original Home, Home, Down.
	SearchF2       // Original F2 (search execute / open forward prompt).
	SearchBackF2   // Original Shift+F2 (backward search prompt/execute).
	ProofCtrlF2    // Original Ctrl+F2 (proofreading Check menu).
	ProofDigit     // Menu digit / Not Found action digit payload via Text.
	ProofSkipOnce  // Not Found 1 Skip Once.
	ProofSkip      // Not Found 2 Skip (rest of pass).
	ProofAdd       // Not Found 3 Add (provider dictionary write, WP87 owner).
	ProofAdvance   // Any-key acknowledgement of word count (frame 09 'spc').
)

type IntentKind string

const (
	Read             IntentKind = "Read"
	Observe          IntentKind = "Observe"
	WriteSnapshot    IntentKind = "WriteSnapshot"
	PublishCandidate IntentKind = "PublishCandidate"
	ReadMacro        IntentKind = "ReadMacro"
)

// Location is a declared rooted profile, not DOS path emulation. Empty Prefix
// accepts flat basenames only. A nonempty exact Prefix is for a separately
// declared comparison/profile binding; it never resolves arbitrary host paths.
type Location struct {
	Prefix    string
	Directory *storage.Directory
}
type Config struct{ Locations []Location }

// Intent is an immutable request value. Host code performs the actual dependency
// call and returns the same Operation, Revision and Kind in its Result.
type Intent struct {
	firstProof             *firstRequest
	macroProof             *macroReadProof
	Operation, Revision    uint64
	Kind                   IntentKind
	Directory              *storage.Directory
	Name                   string
	Document               *storage.Document
	Destination            *storage.Destination
	Decision               storage.Decision
	Candidate              []byte
	NativeRevision         document.Revision
	MacroRun, MacroRequest uint64
	MacroParent            [32]byte
	Repeat                 uint32
	Screen                 uint8
}
type Result struct {
	firstObservation    *firstObservation
	macroMissing        bool
	macroProof          *macroReadProof
	macroObservation    *macroReadObservation
	Operation, Revision uint64
	Kind                IntentKind
	Document            *storage.Document
	Macro               *storage.Macro
	Destination         *storage.Destination
	Outcome             storage.Outcome
	Err                 error
}
type Event struct {
	Command Command
	Text    string
	Result  *Result
}

type SaveState string

const (
	NotSaved         SaveState = "NotSaved"
	SameFileNoOp     SaveState = "SameFileNoOp"
	NewNamePublished SaveState = "NewNamePublished"
	SaveFailed       SaveState = "SaveFailed"
	SaveUncertain    SaveState = "SaveUncertain"
)

// Receipt preserves typed failures/residue, including detached late operations.
// Applied=false never means a filesystem action was rolled back or cancelled.
type Receipt struct {
	Result              Result
	Applied             bool
	DestinationMayExist bool
	Candidate           string
}

type Refusal struct{ Reason string }

func (r *Refusal) Error() string { return "editor: unsupported or invalid transition: " + r.Reason }
func refuse(reason string) error { return &Refusal{reason} }

// Session is a persistent value. All transitions return a copy; dependency
// documents/cursors are immutable. Call New; the zero Session is not initialized.
type Session struct {
	newPhase      NewPhase
	genesis       document.Revision
	first         *firstPublication
	initialized   bool
	transition    *transitionIdentity
	bufferID      *bufferIdentity
	screen        uint8
	other         *Session
	macroOwner    *macroIdentity
	macroDelivery bool
	macroReady    *macroAcquisition
	newMacro      *newMacroTarget
	// macroVisitedNew marks a New buffer that hosted an accepted macro run
	// (new_macro_test:156/193 pins: such a buffer owes the macro lifecycle
	// and must not switch away; the EE-A12 switch witness covers hand-typed
	// New only — the trace never switches after a macro). Set with the macro
	// owner; survives the terminal cleanup that clears newMacro/owner.
	macroVisitedNew           bool
	lastSearchQuery           string
	lastSearchEnd             int
	searchPending             bool
	proof                     *ProofreadingState
	genesisHistory            document.HistoryRevision
	macroRepeat               uint32
	locations                 []Location
	mode, resume              Mode
	source                    *storage.Document
	native                    *document.Document
	cursor                    document.Cursor
	revision, sequence        uint64
	name, draft, original     string
	caret, homes              int
	touched, fromExit         bool
	editedPrefill             bool
	pending                   *Intent
	target                    *storage.Destination
	targetDir                 *storage.Directory
	targetName                string
	lastSave                  SaveState
	published                 Receipt
	last, detached            Receipt
	notice                    string
	history                   document.History
	historyValid, historyUsed bool
	over                      bool
	selection                 bool
	anchor                    document.Cursor
	deletion                  document.Deletion
	preview                   document.Preview
	saved                     document.Revision
	publishedRevision         document.Revision
	publishedName             string
	provenance                Command
}

type Snapshot struct {
	NewPhase                                                        NewPhase
	GenesisRevision                                                 document.Revision
	FirstPublication                                                Receipt
	Screen                                                          uint8
	MacroRun                                                        uint64
	MacroRepeat                                                     uint32
	Mode                                                            Mode
	Prompt, Name, Draft, OriginalName, Notice                       string
	Caret, HomePrefix, Gap                                          int
	Reveal                                                          bool
	Revision                                                        uint64
	Pending                                                         *Intent
	SaveState                                                       SaveState
	Published                                                       Receipt
	Last, Detached                                                  Receipt
	Dirty, Typeover, Selection, HistoryQualified, HistoryCountKnown bool
	SelectionStart, SelectionEnd, HistoryCount, PreviewIndex        int
	SavedRevision, NativeRevision, PublishedRevision                document.Revision
	PublishedName                                                   string
	Provenance                                                      Command
}

func New(config Config) (Session, error) {
	locations := append([]Location(nil), config.Locations...)
	seen := map[string]bool{}
	for i, l := range locations {
		if l.Directory == nil || l.Directory.ID() == (storage.FileID{}) || seen[l.Prefix] {
			return Session{}, refuse("location requires unique prefix and pinned directory")
		}
		seen[l.Prefix] = true
		l.Directory = copyDirectory(l.Directory)
		locations[i] = l
	}
	native, err := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if err != nil {
		return Session{}, err
	}
	cursor, err := native.CursorAt(0)
	if err != nil {
		return Session{}, err
	}
	history, err := document.NewHistory(native)
	if err != nil {
		return Session{}, err
	}
	return Session{initialized: true, transition: &transitionIdentity{1}, bufferID: &bufferIdentity{1}, screen: 1, macroRepeat: 1, locations: locations, mode: Editing, lastSave: NotSaved, native: copyNative(native), cursor: cursor, history: history, historyValid: true, genesisHistory: history.Revision(), newPhase: NewUnpublished, genesis: native.Revision(), revision: 1}, nil
}
func (s Session) Snapshot() Snapshot {
	x := Snapshot{Mode: s.mode, Name: s.name, Draft: s.draft, OriginalName: s.original, Notice: s.notice, Caret: s.caret, HomePrefix: s.homes, Gap: s.cursor.Gap(), Reveal: s.cursor.Reveal(), Revision: s.revision, SaveState: s.lastSave, Last: cloneFirstReceipt(s.last), Detached: cloneFirstReceipt(s.detached)}
	x.NewPhase, x.GenesisRevision = s.newPhase, s.genesis
	if s.first != nil {
		x.FirstPublication = firstReceipt(s.first.result, true, s.first.possible, s.first.candidate)
	}
	x.Dirty = s.dirty()
	x.Typeover, x.Selection = s.over, s.selection
	x.SelectionStart, x.SelectionEnd = s.anchor.Gap(), s.cursor.Gap()
	x.HistoryQualified, x.HistoryCountKnown, x.HistoryCount = s.historyValid && s.history.Qualified(), s.historyValid && s.history.CountKnown(), s.history.Count()
	x.PreviewIndex = s.preview.Index()
	x.NativeRevision, x.SavedRevision, x.PublishedRevision = s.native.Revision(), s.saved, s.publishedRevision
	x.PublishedName, x.Provenance = s.publishedName, s.provenance
	x.Published = receipt(s.published.Result, s.published.Applied)
	x.Pending = copyIntent(s.pending)
	x.Screen = s.screen
	x.MacroRepeat = s.macroRepeat
	if s.macroOwner != nil {
		x.MacroRun = s.macroOwner.run
	}
	switch s.mode {
	case DeleteQuestion:
		x.Prompt = s.deletion.Prompt()
	case HistoryPreview:
		x.Prompt = s.preview.Prompt()
	case MacroName:
		x.Prompt = "Macro: " + s.draft
	case RetrieveName:
		x.Prompt = "Document to be retrieved: " + s.draft + " (List Files)"
	case SaveName:
		x.Prompt = "Document to be saved: " + s.draft
	case ReplaceQuestion:
		x.Prompt = "Replace " + s.draft + "? No (Yes)"
	case ExitSaveQuestion:
		x.Prompt = "Save document? Yes (No)"
		if !s.dirty() {
			x.Notice = "(Text was not modified)"
		}
	case SearchForwardMode:
		if s.draft == "" {
			x.Prompt = "→ Srch:"
		} else {
			x.Prompt = "→ Srch: " + s.draft
		}
	case SearchBackwardMode:
		if s.draft == "" {
			x.Prompt = "← Srch:"
		} else {
			x.Prompt = "← Srch: " + s.draft
		}
	case ExitQuestion:
		x.Prompt = "Exit WP? No (Yes) (Cancel to return to document)"
	case ExitDocQuestion:
		x.Prompt = fmt.Sprintf("Exit doc %d? No (Yes) (Cancel to return to document)", s.screen)
	}
	return x
}
func (s Session) Document() *document.Document { return copyNative(s.native) }
func (s Session) Source() *storage.Document    { return copySource(s.source) }
func (s Session) Present(start, count int) (document.Presentation, error) {
	if s.native == nil {
		return document.Presentation{}, refuse("no retrieved document")
	}
	return s.cursor.Present(start, count)
}
func (s Session) begin(kind IntentKind, dir *storage.Directory, name string) (Session, *Intent, error) {
	if err := s.boldWriteGuard(kind); err != nil {
		return s, nil, err
	}
	if kind == ReadMacro && s.native != nil && s.native.Birth().IsNew() && !s.newMacro.unedited(s) {
		return s, nil, refuse("New macro admission no longer owns naming target")
	}
	s.sequence++
	request := Intent{Operation: s.sequence, Revision: s.revision, Kind: kind, Directory: dir, Name: name, Document: s.source, Destination: s.target, Decision: storage.NoOverwrite}
	request.NativeRevision = s.native.Revision()
	if s.native != nil && kind != ReadMacro {
		request.Candidate, _ = s.native.Export()
	}
	if kind == ReadMacro {
		request.Document = nil
		request.Destination = nil
		request.MacroRun = request.Operation
		request.Repeat = s.macroRepeat
		request.Screen = s.screen
		request.macroProof = newMacroReadProof(request, s.bufferID)
		if s.newMacro != nil {
			request.macroProof.target = s.newMacro
			request.macroProof.issued = &transitionIdentity{1}
			request.macroProof.native = request.NativeRevision
		}
		s.macroRepeat = 1
	}
	s.pending = copyIntent(&request)
	s.resume = s.mode
	s.mode = Waiting
	s.notice = ""
	return s, copyIntent(s.pending), nil
}
func (s Session) resolve(name string) (*storage.Directory, string, error) {
	var best *Location
	for i := range s.locations {
		l := &s.locations[i]
		if strings.HasPrefix(name, l.Prefix) && (best == nil || len(l.Prefix) > len(best.Prefix)) {
			best = l
		}
	}
	if best == nil {
		return nil, "", refuse("filename is outside declared rooted locations")
	}
	leaf := strings.TrimPrefix(name, best.Prefix)
	if leaf == "" || leaf == "." || leaf == ".." || len(leaf) > storage.MaxNameBytes || strings.ContainsAny(leaf, "/\\:\x00") || strings.HasPrefix(leaf, ".wordling-candidate-") {
		return nil, "", refuse("only bounded flat basenames in a declared location")
	}
	return best.Directory, leaf, nil
}
func (s Session) filename(mode Mode) Session {
	s.mode = mode
	s.draft = s.name
	s.original = s.name
	s.caret = 0
	s.touched = false
	s.editedPrefill = false
	s.target = nil
	s.targetDir = nil
	s.targetName = ""
	s.notice = ""
	if mode == RetrieveName || mode == MacroName {
		s.draft = ""
		s.original = ""
	}
	return s
}

// exitPromptMode is the question the original asks after a completed
// save-on-exit: with a second screen present it asks "Exit doc N?" (EE-A12
// frames corrections/08 + corrections/30); a single-screen session asks
// "Exit WP?" (files/12). Both keep the F1-cancel / No / Yes semantics.
func (s Session) exitPromptMode() Mode {
	if s.other != nil {
		return ExitDocQuestion
	}
	return ExitQuestion
}

// renewed binds a usable fresh New document to this screen (T257; EE-A12
// frame corrections/03 types into the acquired screen, frame 33 into the
// post-close screen). Screen-acquisition-only; the exit-clear law (an
// unqualified clear mints no New) is untouched. Fresh buffer identity: the
// new document cannot alias the prior one's provenance.
func (s Session) renewed() (Session, error) {
	native, err := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if err != nil {
		return s, err
	}
	cursor, err := native.CursorAt(0)
	if err != nil {
		return s, err
	}
	history, err := document.NewHistory(native)
	if err != nil {
		return s, err
	}
	s.newPhase = NewUnpublished
	s.genesis = native.Revision()
	s.first = nil
	s.source = nil
	s.native = native
	s.cursor = cursor
	s.history = history
	s.historyValid = true
	s.historyUsed = false
	s.genesisHistory = history.Revision()
	s.revision++
	s.name = ""
	s.saved = document.Revision{}
	s.publishedRevision = document.Revision{}
	s.publishedName = ""
	s.lastSave = NotSaved
	s.mode = Editing
	return s, nil
}

func (s Session) clear() Session {
	s.newPhase = ""
	s.first = nil
	s.genesis = document.Revision{}
	s.source = nil
	s.native = nil
	s.cursor = document.Cursor{}
	s.name = ""
	s.draft = ""
	s.original = ""
	s.caret = 0
	s.homes = 0
	s.revision++
	s.mode = Editing
	s.lastSave = NotSaved
	s.historyValid = false
	s.saved = document.Revision{}
	s.selection = false
	s.deletion = document.Deletion{}
	s.preview = document.Preview{}
	s.fromExit = false
	s.macroVisitedNew = false
	s.target = nil
	s.notice = ""
	return s
}

func (s Session) Reduce(event Event) (Session, *Intent, error) {
	if s.mode == Editing && s.macroRepeat != 1 && event.Command != Macro {
		return s, nil, refuse("qualified Macro repeat setup must be followed by Macro")
	}
	if s.macroOwner != nil && !s.macroDelivery {
		return s, nil, refuse("active macro owns delivery; use execution Step/Resume/HostStop")
	}

	next, intent, err := s.reduce(event)
	if err != nil && event.Command != Complete {
		return s, nil, err
	}
	if err == nil && event.Command != Complete {
		next.provenance = event.Command
		if intent != nil && intent.firstProof != nil {
			next.transition = intent.firstProof.transition
		} else if intent != nil && intent.macroProof != nil && intent.macroProof.target != nil {
			next.transition = intent.macroProof.issued
		} else {
			next = next.advanced()
		}
	}
	return next, intent, err
}
func (s Session) reduce(event Event) (Session, *Intent, error) {
	if !s.initialized {
		return s, nil, refuse("uninitialized session")
	}
	if event.Command == Complete {
		if event.Result == nil || event.Text != "" {
			return s, nil, refuse("completion requires result only")
		}
		return s.complete(*event.Result)
	}
	if event.Result != nil || (event.Command != Text && event.Text != "") {
		return s, nil, refuse("mixed event payload")
	}
	if s.newPhase == PublishedUnbound {
		if event.Command == RetryFirstRead {
			return s.retryFirstRead()
		}
		return s, nil, refuse("published New requires Read-only binding retry")
	}
	if s.newPhase == PublicationUncertain {
		return s, nil, refuse("New publication effect unresolved; host reconciliation required")
	}
	if err := s.boldActiveGuard(event); err != nil {
		return s, nil, err
	}
	if s.mode == Exited {
		return s, nil, refuse("session exited")
	}
	if s.mode == Waiting {
		if s.pending != nil && (s.pending.Kind == PublishCandidate || s.pending.Kind == WriteSnapshot) && editingCommand(event.Command) {
			old := s
			s.mode = Editing
			next, _, err := s.reduce(event)
			if err != nil {
				return old, nil, err
			}
			next.mode = Waiting
			return next, nil, nil
		}
		if event.Command != CancelOperation {
			return s, nil, refuse("operation pending; host cancellation is separate from original keys")
		}
		if s.pending != nil && s.pending.firstProof != nil {
			p := s.pending.firstProof
			if p.kind == PublishNewBuffer {
				s.newPhase = PublicationUncertain
				s.first = &firstPublication{request: p, result: Result{Kind: p.kind, Operation: p.operation, Revision: p.revision}, possible: true}
				s.lastSave = SaveUncertain
			} else {
				s.newPhase = PublishedUnbound
				s.lastSave = SaveUncertain
			}
		}
		s.pending = nil
		s.newMacro = nil
		s.mode = s.resume
		s.notice = "Operation detached; filesystem completion still requires reconciliation"
		return s, nil, nil
	}
	if s.mode == MacroError {
		if event.Command == F1 {
			s.mode = Editing
			s.notice = ""
			return s, nil, nil
		}
		return s, nil, refuse("missing macro recovery requires observed F1")
	}
	if s.mode == MacroReady && event.Command == CancelOperation {
		s.newMacro = nil
		s.mode = Editing
		s.notice = "Host discarded unstarted macro; source snapshot retained"
		return s, nil, nil
	}
	if event.Command == CancelOperation {
		return s, nil, refuse("no pending operation")
	}
	if s.mode == DeleteQuestion || s.mode == HistoryPreview {
		return s.edit(event)
	}
	if s.mode == RetrieveName || s.mode == SaveName || s.mode == MacroName {
		return s.editName(event)
	}
	if s.mode == SearchForwardMode || s.mode == SearchBackwardMode {
		return s.reduceSearch(event)
	}
	if s.mode == ProofMenuMode || s.mode == ProofAskMode || s.mode == ProofAckMode {
		return s.reduceProofEvent(event)
	}
	switch s.mode {
	case ReplaceQuestion:
		switch event.Command {
		case No:
			s.mode = SaveName
			s.caret = 0
			s.touched = false
			s.target = nil
			return s, nil, nil
		case Yes:
			if s.source == nil {
				return s, nil, &storage.Failure{Kind: storage.UnsupportedReplacement, Stage: "New replacement", Name: s.targetName}
			}

			raw, _ := s.native.Export()
			if !bytes.Equal(raw, s.source.Export()) {
				return s, nil, &storage.Failure{Kind: storage.UnsupportedReplacement, Stage: "edited replacement", Name: s.targetName}
			}
			identity, _ := s.target.Identity()
			if identity.ID != s.source.Identity().ID {
				return s, nil, &storage.Failure{Kind: storage.UnsupportedReplacement, Stage: "session replacement decision", Name: s.targetName}
			}
			next, _, err := s.begin(WriteSnapshot, s.targetDir, s.targetName)
			request := *next.pending
			request.Decision = storage.AllowOverwrite
			next.pending = &request
			return next, copyIntent(next.pending), err
		}
	case ExitSaveQuestion:
		switch event.Command {
		case F1:
			s.mode = Editing
			s.fromExit = false
			return s, nil, nil
		case Escape:
			s = s.filename(SaveName)
			s.fromExit = true
			return s, nil, nil
		case No:
			// EE-A12 trace (corrections runner 685cf988): with a second
			// screen present, even the declined save routes to "Exit doc
			// N?" (frame 32's route); single-screen goes to "Exit WP?".
			s.mode = s.exitPromptMode()
			s.fromExit = false
			return s, nil, nil
		case Yes:
			// EE-A12 trace (corrections runner 685cf988): F7 -> "Save
			// document? Yes(No)" -> 'y' -> "Document to be saved:" prompt.
			// Same route as Escape but from the affirmative default answer.
			s = s.filename(SaveName)
			s.fromExit = true
			return s, nil, nil
		}
	case ExitQuestion:
		switch event.Command {
		case F1:
			s.mode = Editing
			return s, nil, nil
		case No, Escape:
			return s.clear(), nil, nil
		case Yes:
			s = s.clear()
			s.mode = Exited
			return s, nil, nil
		}
	case ExitDocQuestion:
		// EE-A12 trace (corrections runner 685cf988), frames 31/32/34: F1
		// returns to the document; Yes closes this screen and restores the
		// sibling; No declines exit back to editing. "Exit doc N?" with No
		// returning to the document is the observed cancel shape (frame 31
		// waits 'Doc 1' after F1; the No answer keeps the screen editable).
		switch event.Command {
		case F1, No, Escape:
			s.mode = Editing
			return s, nil, nil
		case Yes:
			other := *s.other
			other.other = nil
			other.sequence = s.sequence
			other.transition = s.transition
			other.historyValid = false
			return other, nil, nil
		}
	case Editing:
		if s.selection && event.Command != Right && event.Command != Backspace && event.Command != F1 {
			return s, nil, refuse("only forward block movement/Backspace and qualified F1 cleanup")
		}
		if s.homes > 0 {
			switch event.Command {
			case Escape:
				s.homes = 0
				return s, nil, nil
			case Left:
				if s.homes == 2 {
					return s.moveToBoundary(-1, false)
				}
				return s, nil, refuse("use Home twice, then Left for line start")
			case Down:
				if s.homes == 2 {
					return s.moveToBoundary(1, true)
				}
				return s, nil, refuse("use Home twice, then Down for document end")
			case Home, Up:
			default:
				return s, nil, refuse("Home prefix pending. Press Escape to cancel")
			}
		}
		switch event.Command {
		case SwitchDocument:
			return s.switchDocument()
		case Macro:
			if s.native == nil || s.selection || s.homes != 0 {
				return s, nil, refuse("macro invocation requires qualified loaded editing context")
			}
			newTarget := s.native.Birth().IsNew()
			if newTarget && !s.pristineNewMacro() {
				return s, nil, refuse("macro requires pristine initial New Doc1")
			}
			if h, err := s.interrupted(); err != nil {
				return s, nil, err
			} else {
				s.history = h
			}
			if newTarget {
				s.newMacro = s.captureNewMacro()
			}
			return s.filename(MacroName), nil, nil
		case Retrieve:
			if s.source != nil || (s.native != nil && s.native.Revision() != s.genesis) {
				return s, nil, refuse("insertion into an existing buffer is unimplemented")
			}
			return s.filename(RetrieveName), nil, nil
		case Save:
			if s.source == nil && s.newPhase != NewUnpublished {
				return s, nil, refuse("new document writer unavailable")
			}
			next, err := s.saveHistoryInterleaving()
			if err != nil {
				return s, nil, err
			}
			s = next
			s.fromExit = false
			return s.filename(SaveName), nil, nil
		case F7:
			if h, err := s.interrupted(); err != nil {
				return s, nil, err
			} else {
				s.history = h
			}
			s.mode = ExitSaveQuestion
			return s, nil, nil
		case SearchF2, SearchBackF2:
			// EE-A09: F2 opens the forward prompt (empty on first use,
			// prefilled with the remembered query on repeats); Shift+F2
			// mirrors backward. The trace's frames 18/20/22.
			direction := Forward
			if event.Command == SearchBackF2 {
				direction = Backward
			}
			return s.beginSearch(direction), nil, nil
		case ProofCtrlF2:
			// Trace: ctrl-f2 → "Check: 1 Word; 2 Page; 3 Document; ..."
			// (frame 01). Requires a loaded document (the original runs from
			// ordinary editing).
			if s.native == nil {
				return s, nil, refuse("proofreading requires a loaded document")
			}
			if h, err := s.interrupted(); err != nil {
				return s, nil, err
			} else {
				s.history = h
			}
			next := s.beginProofreading()
			next.mode = ProofMenuMode
			return next, nil, nil
		case ProofSkipOnce:
			return s.proofSkip(true), nil, nil
		case ProofSkip:
			return s.proofSkip(false), nil, nil
		case ProofAdd:
			return s.proofAdd(), nil, nil
		case ProofAdvance:
			// Frame 09: any key on the word-count acknowledgement returns
			// to editing; a new pass resets transient decisions.
			st := s.proofreadState()
			if st.Phase == ProofCompleteAck {
				st.Corrections = map[string]string{}
				st.Skipped = map[string]struct{}{}
				st.Phase = ProofInactive
				st.Suspects = nil
				s.mode = Editing
				s.proof = st
			}
			return s, nil, nil
		case Bold:
			return s.authorBold()
		case Text, Enter, Insert, Delete, Backspace, Block, F1, Previous, Restore:
			return s.edit(event)
		case Reveal:
			if s.native == nil {
				return s, nil, refuse("Reveal requires retrieved document")
			}
			if s.selection {
				return s, nil, refuse("view change during block is unqualified")
			}
			if s.historyValid && s.history.Qualified() {
				h, err := s.history.InterruptGrouping()
				if err != nil {
					return s, nil, err
				}
				s.history = h
			}
			s.cursor = s.cursor.WithReveal(!s.cursor.Reveal())
			return s, nil, nil
		case Left, Right:
			if s.native == nil {
				return s, nil, refuse("cursor requires retrieved document")
			}
			direction := 1
			if event.Command == Left {
				direction = -1
			}
			cursor, err := s.cursor.Move(direction)
			if err != nil {
				return s, nil, err
			}
			if s.historyValid && s.history.Qualified() {
				var h document.History
				if event.Command == Right {
					h, err = s.history.Separate(document.RightBoundary)
				} else {
					h, err = s.history.InterruptGrouping()
				}
				if err != nil {
					return s, nil, err
				}
				s.history = h
			}
			s.cursor = cursor
			s.provenance = event.Command
			return s, nil, nil
		case End:
			return s.moveToBoundary(1, false)
		case Home:
			if s.native == nil || s.homes == 3 {
				return s, nil, refuse("Home prefix outside observed bounded sequence")
			}
			if h, err := s.interrupted(); err != nil {
				return s, nil, err
			} else {
				s.history = h
			}
			s.homes++
			return s, nil, nil
		case Up:
			if s.homes != 2 && s.homes != 3 {
				return s, nil, refuse("only Home2/3 Up endpoints observed")
			}
			gap := 0
			if s.native.TokenCount() > 0 {
				token, _ := s.native.Token(0)
				if token.Kind == document.Opaque {
					return s, nil, refuse("opaque initial code semantics unknown")
				}
				if s.homes == 2 && token.Kind == document.BoldOn {
					gap = 1
				}
			}
			cursor, err := s.native.CursorAt(gap)
			if err != nil {
				return s, nil, err
			}
			s.cursor = cursor.WithReveal(s.cursor.Reveal())
			s.homes = 0
			return s, nil, nil
		}
	}
	return s, nil, refuse(fmt.Sprintf("command %d in %s", event.Command, s.mode))
}

func (s Session) editName(event Event) (Session, *Intent, error) {
	switch event.Command {
	case Macro:
		if s.mode == SaveName {
			return s, nil, nil
		}
		return s, nil, refuse("macro nesting in this filename prompt unqualified")
	case F1:
		s.newMacro = nil
		s.mode = Editing
		s.fromExit = false
		s.notice = ""
		return s, nil, nil
	case Escape:
		if s.mode == RetrieveName {
			s.mode = Editing
			s.notice = ""
			return s, nil, nil
		}
	case Text:
		if len(event.Text) > storage.MaxNameBytes {
			return s, nil, refuse("filename draft safety bound")
		}
		if event.Text == "" {
			return s, nil, refuse("empty filename text")
		}
		for _, r := range event.Text {
			if r < 0x20 || r > 0x7e {
				return s, nil, refuse("filename requires explicit ASCII profile")
			}
		}
		draft, caret := s.draft, s.caret
		if !s.touched {
			s.editedPrefill = false
			draft = ""
			caret = 0
		}
		if len(draft)+len(event.Text) > storage.MaxNameBytes {
			return s, nil, refuse("filename draft safety bound")
		}
		s.draft = draft[:caret] + event.Text + draft[caret:]
		s.caret = caret + len(event.Text)
		s.touched = true
		return s, nil, nil
	case Right:
		if s.mode == RetrieveName || s.mode == MacroName {
			return s, nil, refuse("Retrieve filename editing unobserved")
		}
		if s.caret >= len(s.draft) {
			return s, nil, refuse("filename caret boundary")
		}
		if !s.touched && s.draft != "" {
			s.editedPrefill = true
		}
		s.caret++
		s.touched = true
		return s, nil, nil
	case Backspace:
		if s.mode == RetrieveName || s.mode == MacroName {
			return s, nil, refuse("Retrieve filename editing unobserved")
		}
		if s.caret == 0 {
			return s, nil, refuse("filename caret boundary")
		}
		s.draft = s.draft[:s.caret-1] + s.draft[s.caret:]
		s.caret--
		s.touched = true
		return s, nil, nil
	case Enter:
		if s.mode == SaveName && s.editedPrefill {
			return s, nil, refuse("prefilled filename edit has only cancel evidence")
		}
		resolve := s.resolve
		if s.mode == MacroName {
			resolve = s.resolveMacro
		}
		dir, name, err := resolve(s.draft)
		if err != nil {
			return s, nil, err
		}
		if s.mode == MacroName {
			return s.begin(ReadMacro, dir, name)
		}
		if s.mode == RetrieveName {
			return s.begin(Read, dir, name)
		}
		if s.source == nil && s.newPhase != NewUnpublished {
			return s, nil, refuse("new document writer unavailable")
		}
		s.lastSave = NotSaved
		return s.begin(Observe, dir, name)
	}
	return s, nil, refuse("unobserved filename command")
}

func receipt(result Result, applied bool) Receipt {
	result = copyResult(result)
	record := Receipt{Result: result, Applied: applied, DestinationMayExist: (!applied || result.Err != nil) && result.Outcome.State == storage.Published}
	var failure *storage.Failure
	if errors.As(result.Err, &failure) {
		copy := *failure
		record.Result.Err = &copy
		// A typed storage failure is authoritative about its transaction stage.
		record.DestinationMayExist = failure.DestinationMayExist
		record.Candidate = failure.Candidate
	}
	return record
}
func (s Session) complete(result Result) (Session, *Intent, error) {
	result = copyResult(result)
	if s.pending != nil && s.pending.firstProof != nil {
		if result.Operation != s.pending.Operation || result.Revision != s.pending.Revision || result.Kind != s.pending.Kind {
			s.detached = receipt(result, false)
			return s, nil, nil
		}
		return s.completeFirst(result)
	}
	if s.pending == nil || result.Operation != s.pending.Operation || result.Revision != s.pending.Revision || result.Kind != s.pending.Kind {
		if s.newMacro != nil && s.pending != nil && s.pending.Kind == ReadMacro {
			return s, nil, refuse("foreign New macro root result")
		}
		s = s.advanced()
		s.newMacro = nil
		s.detached = receipt(result, false)
		return s, nil, nil
	}
	request := *s.pending
	if request.Kind == ReadMacro {
		if s.newMacro != nil || (request.macroProof != nil && request.macroProof.target != nil) {
			if !s.validNewMacroRead(&request) {
				return s, nil, refuse("New macro root is stale or foreign")
			}
		}
		var err error
		result, err = acceptedMacroResult(&request, result, s.bufferID)
		if err != nil {
			return s, nil, err
		}
	}
	if result.Revision != s.revision {
		s.pending = nil
		s.mode = Editing
		s = s.advanced()
		s.detached = receipt(result, false)
		s.notice = "Older revision completed; current edits and name retained"
		return s, nil, nil
	}
	s = s.advanced()
	s.pending = nil
	s.mode = s.resume
	s.last = receipt(result, true)
	if result.Err != nil {
		s.notice = result.Err.Error()
		if request.Kind == ReadMacro {
			s.newMacro = nil
			s.mode = Editing
			s.notice = "Macro acquisition failed: " + result.Err.Error()
			if result.macroMissing {
				display := s.draft
				if !strings.HasSuffix(display, ".WPM") {
					display += ".WPM"
				}
				s.mode = MacroError
				s.notice = "ERROR: File not found -- " + display
			}
		}
		if request.Kind == Read && errors.Is(result.Err, fs.ErrNotExist) {
			s.notice = "ERROR: File not found -- " + s.draft
			s.touched = false
			s.caret = 0
		}
		if (request.Kind == WriteSnapshot || request.Kind == PublishCandidate) || request.Kind == Observe {
			s.lastSave = SaveFailed
			if s.last.DestinationMayExist {
				s.lastSave = SaveUncertain
			}
		}
		return s, nil, nil
	}
	invalid := func(reason string) (Session, *Intent, error) {
		s.notice = reason
		result.Err = refuse(reason)
		s.last = receipt(result, true)
		if (request.Kind == WriteSnapshot || request.Kind == PublishCandidate) || request.Kind == Observe {
			s.lastSave = SaveFailed
		}
		return s, nil, refuse(reason)
	}
	switch request.Kind {
	case ReadMacro:
		macro := result.Macro
		if macro == nil || macro.Name() != request.Name || macro.DirectoryID() != request.Directory.ID() || macro.Image() == nil || macro.Image().SHA256() != macro.Identity().SHA256 {
			return invalid("macro result identity mismatch")
		}
		s.macroReady = &macroAcquisition{request: *copyIntent(&request), source: copyMacro(macro), ready: s.transition, observation: result.macroObservation}
		s.mode = MacroReady
		s.notice = ""
	case Read:
		if result.Document == nil || result.Document.Name() != request.Name || result.Document.DirectoryID() != request.Directory.ID() {
			return invalid("read result identity mismatch")
		}
		native, err := document.Parse(result.Document.Export())
		if err != nil {
			s.notice = err.Error()
			result.Err = err
			s.last = receipt(result, true)
			return s, nil, err
		}
		cursor, err := native.CursorAt(0)
		if err != nil {
			return s, nil, err
		}
		s.newPhase = ""
		s.first = nil
		s.genesis = document.Revision{}
		s.source = copySource(result.Document)
		s.native = copyNative(native)
		if !s.historyUsed {
			h, err := document.NewHistory(native)
			if err == nil {
				s.history = h
				s.historyValid = true
			}
		}
		s.historyUsed = true
		s.saved = native.Revision()
		s.publishedRevision = document.Revision{}
		s.published = Receipt{}
		s.publishedName = ""
		s.cursor = cursor
		s.name = s.draft
		s.mode = Editing
		s.revision++
		s.homes = 0
		s.notice = ""
		s.lastSave = NotSaved
	case Observe:
		target := result.Destination
		if target == nil || target.Name() != request.Name || target.DirectoryID() != request.Directory.ID() {
			return invalid("destination result identity mismatch")
		}
		s.target = copyDestination(target)
		s.targetDir = copyDirectory(request.Directory)
		s.targetName = request.Name
		if target.Exists() {
			s.mode = ReplaceQuestion
			return s, nil, nil
		}
		if s.newPhase == NewUnpublished {
			return s.firstIntent(PublishNewBuffer, request.Directory, request.Name, nil)
		}
		kind := WriteSnapshot
		if s.native != nil {
			raw, _ := s.native.Export()
			if !bytes.Equal(raw, s.source.Export()) {
				kind = PublishCandidate
			}
		}
		return s.begin(kind, request.Directory, request.Name)
	case WriteSnapshot, PublishCandidate:
		out := result.Outcome
		if out.Name != request.Name || out.DirectoryID != request.Directory.ID() || out.Identity.Size != int64(len(request.Candidate)) || out.Identity.SHA256 != sha256.Sum256(request.Candidate) {
			return invalid("save result identity mismatch")
		}
		switch out.State {
		case storage.Unchanged:
			if request.Kind != WriteSnapshot || request.Decision != storage.AllowOverwrite || !request.Destination.Exists() || out.Identity.ID != s.source.Identity().ID {
				return invalid("invalid same-file no-op result")
			}
			s.lastSave = SameFileNoOp
		case storage.Published:
			// A real published candidate has an inode. Device zero can be valid;
			// this structural check cannot authenticate arbitrary host IO claims.
			if out.Identity.ID.Inode == 0 {
				return invalid("published destination has no inode identity")
			}
			if request.Destination.Exists() {
				return invalid("existing destination cannot be published")
			}
			s.lastSave = NewNamePublished
		default:
			return invalid("unknown save outcome")
		}
		s.mode = Editing
		s.name = s.draft
		s.saved = request.NativeRevision
		s.publishedRevision, s.publishedName = request.NativeRevision, s.name
		s.published = receipt(result, true)
		if s.historyValid {
			h, err := s.history.Separate(document.SavedBoundary)
			if err != nil {
				// Publication already happened. Preserve its receipt and native
				// revision, but never retain permission after a failed barrier.
				s.historyValid = false
				s.notice = err.Error()
				return s, nil, err
			}
			s.history = h
		}
		s.notice = ""
		if s.fromExit {
			// EE-A12 trace (corrections runner 685cf988): after a completed
			// save-on-exit publication, the original continues to "Exit doc
			// N?"/"Exit WP?" rather than returning to editing. F1 at the exit
			// question still returns to the document (frame 07-cancel route).
			s.fromExit = false
			s.mode = s.exitPromptMode()
			return s, nil, nil
		}
	default:
		return invalid("unknown operation result")
	}
	return s, nil, nil
}
