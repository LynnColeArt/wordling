// Package editor implements a bounded read-only session reducer. It has no
// terminal dependency, filesystem execution, semantic writer or dirty document.
package editor

import (
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
	Waiting          Mode = "Waiting"
	Exited           Mode = "Exited"
)

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
)

type IntentKind string

const (
	Read          IntentKind = "Read"
	Observe       IntentKind = "Observe"
	WriteSnapshot IntentKind = "WriteSnapshot"
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
	Operation, Revision uint64
	Kind                IntentKind
	Directory           *storage.Directory
	Name                string
	Document            *storage.Document
	Destination         *storage.Destination
	Decision            storage.Decision
}
type Result struct {
	Operation, Revision uint64
	Kind                IntentKind
	Document            *storage.Document
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
	initialized           bool
	locations             []Location
	mode, resume          Mode
	source                *storage.Document
	native                *document.Document
	cursor                document.Cursor
	revision, sequence    uint64
	name, draft, original string
	caret, homes          int
	touched, fromExit     bool
	editedPrefill         bool
	pending               *Intent
	target                *storage.Destination
	targetDir             *storage.Directory
	targetName            string
	lastSave              SaveState
	last, detached        Receipt
	notice                string
}

type Snapshot struct {
	Mode                                      Mode
	Prompt, Name, Draft, OriginalName, Notice string
	Caret, HomePrefix, Gap                    int
	Reveal                                    bool
	Revision                                  uint64
	Pending                                   *Intent
	SaveState                                 SaveState
	Last, Detached                            Receipt
}

func New(config Config) (Session, error) {
	locations := append([]Location(nil), config.Locations...)
	seen := map[string]bool{}
	for _, l := range locations {
		if l.Directory == nil || l.Directory.ID() == (storage.FileID{}) || seen[l.Prefix] {
			return Session{}, refuse("location requires unique prefix and pinned directory")
		}
		seen[l.Prefix] = true
	}
	return Session{initialized: true, locations: locations, mode: Editing, lastSave: NotSaved}, nil
}
func (s Session) Snapshot() Snapshot {
	x := Snapshot{Mode: s.mode, Name: s.name, Draft: s.draft, OriginalName: s.original, Notice: s.notice, Caret: s.caret, HomePrefix: s.homes, Gap: s.cursor.Gap(), Reveal: s.cursor.Reveal(), Revision: s.revision, SaveState: s.lastSave, Last: receipt(s.last.Result, s.last.Applied), Detached: receipt(s.detached.Result, s.detached.Applied)}
	if s.pending != nil {
		p := *s.pending
		x.Pending = &p
	}
	switch s.mode {
	case RetrieveName:
		x.Prompt = "Document to be retrieved: " + s.draft + " (List Files)"
	case SaveName:
		x.Prompt = "Document to be saved: " + s.draft
	case ReplaceQuestion:
		x.Prompt = "Replace " + s.draft + "? No (Yes)"
	case ExitSaveQuestion:
		x.Prompt = "Save document? Yes (No)"
		x.Notice = "(Text was not modified)"
	case ExitQuestion:
		x.Prompt = "Exit WP? No (Yes) (Cancel to return to document)"
	}
	return x
}
func (s Session) Document() *document.Document { return s.native }
func (s Session) Source() *storage.Document    { return s.source }
func (s Session) Present(start, count int) (document.Presentation, error) {
	if s.native == nil {
		return document.Presentation{}, refuse("no retrieved document")
	}
	return s.cursor.Present(start, count)
}
func (s Session) begin(kind IntentKind, dir *storage.Directory, name string) (Session, *Intent, error) {
	s.sequence++
	request := Intent{Operation: s.sequence, Revision: s.revision, Kind: kind, Directory: dir, Name: name, Document: s.source, Destination: s.target, Decision: storage.NoOverwrite}
	s.pending = &request
	s.resume = s.mode
	s.mode = Waiting
	s.notice = ""
	copy := request
	return s, &copy, nil
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
	if mode == RetrieveName {
		s.draft = ""
		s.original = ""
	}
	return s
}
func (s Session) clear() Session {
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
	s.fromExit = false
	s.target = nil
	s.notice = ""
	return s
}

func (s Session) Reduce(event Event) (Session, *Intent, error) {
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
	if s.mode == Exited {
		return s, nil, refuse("session exited")
	}
	if s.mode == Waiting {
		if event.Command != CancelOperation {
			return s, nil, refuse("operation pending; host cancellation is separate from original keys")
		}
		s.pending = nil
		s.mode = s.resume
		s.notice = "Operation detached; filesystem completion still requires reconciliation"
		return s, nil, nil
	}
	if event.Command == CancelOperation {
		return s, nil, refuse("no pending operation")
	}
	if s.mode == RetrieveName || s.mode == SaveName {
		return s.editName(event)
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
				return s, nil, refuse("new document writer unavailable")
			}
			identity, _ := s.target.Identity()
			if identity.ID != s.source.Identity().ID {
				return s, nil, &storage.Failure{Kind: storage.UnsupportedReplacement, Stage: "session replacement decision", Name: s.targetName}
			}
			next, _, err := s.begin(WriteSnapshot, s.targetDir, s.targetName)
			request := *next.pending
			request.Decision = storage.AllowOverwrite
			next.pending = &request
			copy := request
			return next, &copy, err
		}
	case ExitSaveQuestion:
		switch event.Command {
		case F1:
			s.mode = Editing
			return s, nil, nil
		case Escape:
			s = s.filename(SaveName)
			s.fromExit = true
			return s, nil, nil
		case No:
			s.mode = ExitQuestion
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
	case Editing:
		if s.homes > 0 && event.Command != Home && event.Command != Up {
			return s, nil, refuse("unobserved Home-prefix interruption")
		}
		switch event.Command {
		case Retrieve:
			if s.source != nil {
				return s, nil, refuse("insertion into an existing buffer is unimplemented")
			}
			return s.filename(RetrieveName), nil, nil
		case Save:
			if s.source == nil {
				return s, nil, refuse("new document writer unavailable")
			}
			s.fromExit = false
			return s.filename(SaveName), nil, nil
		case F7:
			s.mode = ExitSaveQuestion
			return s, nil, nil
		case Reveal:
			if s.native == nil {
				return s, nil, refuse("Reveal requires retrieved document")
			}
			s.cursor = s.cursor.WithReveal(!s.cursor.Reveal())
			return s, nil, nil
		case Right:
			if s.native == nil {
				return s, nil, refuse("cursor requires retrieved document")
			}
			cursor, err := s.cursor.Move(1)
			if err != nil {
				return s, nil, err
			}
			s.cursor = cursor
			return s, nil, nil
		case Home:
			if s.native == nil || s.homes == 3 {
				return s, nil, refuse("Home prefix outside observed bounded sequence")
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
	return s, nil, refuse(fmt.Sprintf("command %d in %s (read-only scope)", event.Command, s.mode))
}

func (s Session) editName(event Event) (Session, *Intent, error) {
	switch event.Command {
	case F1:
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
		if s.mode == RetrieveName {
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
		if s.mode == RetrieveName {
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
		if s.fromExit {
			return s, nil, refuse("save-on-exit completion not observed; F1 can return to document")
		}
		dir, name, err := s.resolve(s.draft)
		if err != nil {
			return s, nil, err
		}
		if s.mode == RetrieveName {
			return s.begin(Read, dir, name)
		}
		if s.source == nil {
			return s, nil, refuse("new document writer unavailable")
		}
		s.lastSave = NotSaved
		return s.begin(Observe, dir, name)
	}
	return s, nil, refuse("unobserved filename command")
}

func receipt(result Result, applied bool) Receipt {
	record := Receipt{Result: result, Applied: applied, DestinationMayExist: !applied && result.Outcome.State == storage.Published}
	var failure *storage.Failure
	if errors.As(result.Err, &failure) {
		copy := *failure
		record.Result.Err = &copy
		record.DestinationMayExist = failure.DestinationMayExist
		record.Candidate = failure.Candidate
	}
	return record
}
func (s Session) complete(result Result) (Session, *Intent, error) {
	if s.pending == nil || result.Operation != s.pending.Operation || result.Revision != s.pending.Revision || result.Revision != s.revision || result.Kind != s.pending.Kind {
		s.detached = receipt(result, false)
		return s, nil, nil
	}
	request := *s.pending
	s.pending = nil
	s.mode = s.resume
	s.last = receipt(result, true)
	if result.Err != nil {
		s.notice = result.Err.Error()
		if request.Kind == Read && errors.Is(result.Err, fs.ErrNotExist) {
			s.notice = "ERROR: File not found -- " + s.draft
			s.touched = false
			s.caret = 0
		}
		if request.Kind == WriteSnapshot || request.Kind == Observe {
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
		if request.Kind == WriteSnapshot || request.Kind == Observe {
			s.lastSave = SaveFailed
		}
		return s, nil, refuse(reason)
	}
	switch request.Kind {
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
		s.source = result.Document
		s.native = native
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
		s.target = target
		s.targetDir = request.Directory
		s.targetName = request.Name
		if target.Exists() {
			s.mode = ReplaceQuestion
			return s, nil, nil
		}
		return s.begin(WriteSnapshot, request.Directory, request.Name)
	case WriteSnapshot:
		out := result.Outcome
		if out.Name != request.Name || out.DirectoryID != request.Directory.ID() || out.Identity.Size != s.source.Identity().Size || out.Identity.SHA256 != s.source.Identity().SHA256 {
			return invalid("save result identity mismatch")
		}
		switch out.State {
		case storage.Unchanged:
			if request.Decision != storage.AllowOverwrite || !request.Destination.Exists() || out.Identity.ID != s.source.Identity().ID {
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
		s.notice = ""
	default:
		return invalid("unknown operation result")
	}
	return s, nil, nil
}
