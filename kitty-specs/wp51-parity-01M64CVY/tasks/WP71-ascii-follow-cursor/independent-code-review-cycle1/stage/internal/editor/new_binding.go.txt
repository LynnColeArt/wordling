package editor

import (
	"bytes"
	"crypto/sha256"
	"fmt"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/storage"
)

// NewPhase describes Linux host safety, not additional DOS prompts.
type NewPhase string

const (
	NewUnpublished       NewPhase = "NewUnpublished"
	AwaitPublish         NewPhase = "AwaitPublish"
	AwaitFirstRead       NewPhase = "AwaitFirstRead"
	PublishedUnbound     NewPhase = "PublishedUnbound"
	PublicationUncertain NewPhase = "PublicationUncertain"
	NewAnchored          NewPhase = "NewAnchored"
)
const (
	PublishNewBuffer IntentKind = "PublishNewBuffer"
	BindNewSource    IntentKind = "BindNewSource"
)

// RequestKey is an opaque issued-request identity for once-per-request host
// scheduling. It confers neither IO authority nor transaction idempotence.
type RequestKey struct{ proof *firstRequest }

func (k RequestKey) Valid() bool { return k.proof != nil }
func (i Intent) RequestKey() RequestKey {
	if !i.firstProof.matches(&i) {
		return RequestKey{}
	}
	return RequestKey{i.firstProof}
}

type firstRequest struct {
	transition          *transitionIdentity
	buffer              *bufferIdentity
	birth               document.Birth
	native              document.Revision
	operation, revision uint64
	screen              uint8
	kind                IntentKind
	directory           storage.Directory
	target              storage.Destination
	name, display       string
	candidate           []byte
	publication         *firstPublication
}
type firstPublication struct {
	request   *firstRequest
	result    Result
	possible  bool
	candidate string
}
type firstObservation struct {
	request   *firstRequest
	outcome   storage.Outcome
	source    *storage.Document
	err       *sealedError
	possible  bool
	candidate string
}

// sealedError owns diagnostic values. Unwrap returns fresh typed failures so
// errors.As on a public diagnostic cannot mutate the private observation.
type sealedError struct {
	message  string
	failures []storage.Failure
}

func (e *sealedError) Error() string { return e.message }
func (e *sealedError) Unwrap() []error {
	out := make([]error, len(e.failures))
	for i, f := range e.failures {
		v := f
		out[i] = &v
	}
	return out
}
func freezeFirstError(err error, invoked bool) (*sealedError, bool, string) {
	if err == nil {
		return nil, false, ""
	}
	out := &sealedError{}
	possible, candidate := false, ""
	budget := 64
	var walk func(error, bool)
	walk = func(e error, covered bool) {
		if e == nil {
			return
		}
		budget--
		if budget < 0 {
			possible = true
			return
		}
		if f, ok := e.(*storage.Failure); ok && f != nil {
			v := *f
			v.Cause = nil
			out.failures = append(out.failures, v)
			out.message += fmt.Sprintf("storage: %s during %s (%q); ", v.Kind, v.Stage, v.Name)
			if candidate == "" {
				candidate = v.Candidate
			}
			switch v.Kind {
			case storage.InvalidRequest, storage.UnsafePath, storage.ReadFailed, storage.InputLimit, storage.NativeRefused, storage.StaleSource, storage.DestinationChanged, storage.OverwriteRequired, storage.UnsupportedReplacement, storage.CandidateFailed, storage.PublicationFailed, storage.CleanupFailed:
			default:
				possible = true
			}
			possible = possible || v.DestinationMayExist
			walk(f.Cause, true)
			return
		}
		if many, ok := e.(interface{ Unwrap() []error }); ok {
			for _, child := range many.Unwrap() {
				walk(child, covered)
			}
			return
		}
		if one, ok := e.(interface{ Unwrap() error }); ok {
			walk(one.Unwrap(), covered)
			return
		}
		if !covered {
			possible = true
		}
		out.message += e.Error() + "; "
	}
	walk(err, false)
	if !invoked {
		possible = false
	}
	return out, possible, candidate
}
func (p *firstRequest) matches(i *Intent) bool {
	if p == nil || i == nil || i.firstProof != p || i.Directory == nil {
		return false
	}
	if i.Kind != p.kind || i.Operation != p.operation || i.Revision != p.revision || i.NativeRevision != p.native || i.Screen != p.screen || *i.Directory != p.directory || i.Name != p.name || i.Document != nil || i.Decision != storage.NoOverwrite || i.MacroRun != 0 || i.MacroRequest != 0 || i.MacroParent != ([32]byte{}) || i.Repeat != 0 || i.macroProof != nil {
		return false
	}
	if !bytes.Equal(i.Candidate, p.candidate) {
		return false
	}
	if p.kind == PublishNewBuffer {
		return i.Destination != nil && *i.Destination == p.target
	}
	return i.Destination == nil
}
func (s Session) firstIntent(kind IntentKind, directory *storage.Directory, name string, pub *firstPublication) (Session, *Intent, error) {
	if s.native == nil || !s.native.Birth().IsNew() {
		return s, nil, refuse("first publication requires actual New birth")
	}
	raw, err := s.native.Export()
	if err != nil {
		return s, nil, err
	}
	if s.sequence == ^uint64(0) || s.revision == 0 {
		return s, nil, refuse("first request counter exhausted or invalid")
	}
	s.sequence++
	p := &firstRequest{transition: &transitionIdentity{1}, buffer: s.bufferID, birth: s.native.Birth(), native: s.native.Revision(), operation: s.sequence, revision: s.revision, screen: s.screen, kind: kind, directory: *directory, name: name, display: s.draft, candidate: append([]byte(nil), raw...), publication: pub}
	var target *storage.Destination
	if kind == PublishNewBuffer {
		if s.target == nil || s.target.Exists() {
			return s, nil, refuse("requires observed absent target")
		}
		p.target = *s.target
		target = copyDestination(s.target)
		s.newPhase = AwaitPublish
	} else {
		s.newPhase = AwaitFirstRead
		p.display = pub.request.display
	}
	i := &Intent{firstProof: p, Operation: p.operation, Revision: p.revision, Kind: kind, Directory: copyDirectory(directory), Name: name, Destination: target, Candidate: append([]byte(nil), raw...), NativeRevision: p.native, Screen: p.screen}
	s.transition = p.transition
	s.pending = copyIntent(i)
	s.resume = Editing
	s.mode = Waiting
	return s, copyIntent(i), nil
}
func firstResult(i *Intent, kind IntentKind) (Result, *firstRequest) {
	r := Result{Kind: kind}
	if i == nil {
		r.Err = refuse("nil first request")
		return r, nil
	}
	r.Operation, r.Revision = i.Operation, i.Revision
	p := i.firstProof
	if !p.matches(i) || p.kind != kind {
		r.Err = refuse("first request wrapper differs from accepted authority")
		return r, nil
	}
	return r, p
}

// ExecuteNewPublication performs actual41 IO outside Reduce, on the captured
// opened capability. Public wrapper values can refuse but never redirect IO.
func ExecuteNewPublication(i *Intent) Result {
	r, p := firstResult(i, PublishNewBuffer)
	if p == nil {
		return r
	}
	id := storage.PublicationID{Operation: p.operation, Revision: p.revision}
	prepared, err := p.directory.PrepareNewPublication(&p.target, p.candidate, id)
	invoked := false
	if err == nil {
		invoked = true
		r.Outcome, err = p.directory.PublishNew(prepared, id)
	}
	frozen, possible, candidate := freezeFirstError(err, invoked)
	if r.Outcome.State == storage.Published && err != nil {
		possible = true
	}
	o := &firstObservation{request: p, outcome: r.Outcome, err: frozen, possible: possible, candidate: candidate}
	r.firstObservation = o
	if frozen != nil {
		r.Err = frozen
	}
	return r
}

// ExecuteFirstRead observes the same retained capability/name. It cannot
// publish, re-Observe, choose another root or replace the live native object.
func ExecuteFirstRead(i *Intent) Result {
	r, p := firstResult(i, BindNewSource)
	if p == nil {
		return r
	}
	source, err := p.directory.Read(p.name)
	frozen, _, candidate := freezeFirstError(err, false)
	o := &firstObservation{request: p, source: copySource(source), err: frozen, candidate: candidate}
	r.firstObservation = o
	r.Document = copySource(source)
	if frozen != nil {
		r.Err = frozen
	}
	return r
}
func firstReceipt(r Result, applied, possible bool, candidate string) Receipt {
	return Receipt{Result: copyResult(r), Applied: applied, DestinationMayExist: possible, Candidate: candidate}
}
func cloneFirstReceipt(r Receipt) Receipt { r.Result = copyResult(r.Result); return r }
func (s Session) completeFirst(r Result) (Session, *Intent, error) {
	i := s.pending
	p := i.firstProof
	o := r.firstObservation
	invalid := func() (Session, *Intent, error) {
		return s, nil, refuse("first completion lacks exact current private observation")
	}
	if p == nil || !p.matches(i) || p.transition != s.transition || p.buffer != s.bufferID || p.birth != s.native.Birth() || p.native != s.native.Revision() || p.revision != s.revision || p.screen != s.screen || o == nil || o.request != p || r.Operation != p.operation || r.Revision != p.revision || r.Kind != p.kind || r.Macro != nil || r.Destination != nil || r.macroProof != nil || r.macroObservation != nil || r.Outcome != o.outcome {
		return invalid()
	}
	if o.err == nil {
		if r.Err != nil {
			return invalid()
		}
	} else {
		e, ok := r.Err.(*sealedError)
		if !ok || e != o.err {
			return invalid()
		}
	}
	if (r.Document == nil) != (o.source == nil) {
		return invalid()
	}
	if r.Document != nil && *r.Document != *o.source {
		return invalid()
	}
	s.pending = nil
	s.mode = Editing
	s = s.advanced()
	s.last = firstReceipt(r, true, o.possible, o.candidate)
	if p.kind == PublishNewBuffer {
		if o.err != nil {
			s.notice = o.err.Error()
			s.lastSave = SaveFailed
			s.newPhase = NewUnpublished
			if o.possible {
				s.newPhase = PublicationUncertain
				s.lastSave = SaveUncertain
				s.first = &firstPublication{p, copyResult(r), true, o.candidate}
			}
			return s, nil, nil
		}
		outcome := o.outcome
		if outcome.State != storage.Published || outcome.Name != p.name || outcome.DirectoryID != p.directory.ID() || outcome.Identity.ID.Inode == 0 || outcome.Identity.Size != int64(len(p.candidate)) || outcome.Identity.SHA256 != sha256.Sum256(p.candidate) {
			s.newPhase = PublicationUncertain
			s.lastSave = SaveUncertain
			s.notice = "Invalid publication observation; destination effect unresolved"
			s.first = &firstPublication{p, copyResult(r), true, o.candidate}
			return s, nil, refuse(s.notice)
		}
		s.first = &firstPublication{p, copyResult(r), false, ""}
		s.lastSave = NotSaved
		return s.firstIntent(BindNewSource, &p.directory, p.name, s.first)
	}
	// No Parse: acquisition provides only the permanent first guard.
	pub := p.publication
	if pub == nil || s.first != pub {
		return invalid()
	}
	source := o.source
	if o.err != nil || source == nil || source.Name() != p.name || source.DirectoryID() != p.directory.ID() || source.Identity() != pub.result.Outcome.Identity || !bytes.Equal(source.Export(), p.candidate) {
		s.newPhase = PublishedUnbound
		s.lastSave = SaveUncertain
		s.notice = "Published but first rooted Read did not bind; explicit Read-only retry required"
		return s, nil, nil
	}
	s.source = copySource(source)
	s.newPhase = NewAnchored
	s.saved = p.native
	s.name = pub.request.display
	s.publishedName = s.name
	s.publishedRevision = p.native
	s.published = firstReceipt(pub.result, true, false, "")
	s.lastSave = NewNamePublished
	s.notice = ""
	if s.historyValid {
		h, err := s.history.Separate(document.SavedBoundary)
		if err != nil {
			s.historyValid = false
		} else {
			s.history = h
		}
	}
	return s, nil, nil
}
func (s Session) retryFirstRead() (Session, *Intent, error) {
	if s.newPhase != PublishedUnbound || s.first == nil || s.pending != nil {
		return s, nil, refuse("no published-unbound receipt to retry")
	}
	p := s.first.request
	return s.firstIntent(BindNewSource, &p.directory, p.name, s.first)
}
