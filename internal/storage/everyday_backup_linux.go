package storage

import (
	"bytes"
	"crypto/sha256"
	"errors"
	"io/fs"
	"os"
	"strings"
	"sync/atomic"
	"syscall"

	"github.com/lynncoleart/wordling/internal/wp51"
	"golang.org/x/sys/unix"
)

// OriginalBackup controls only the original-document backup, not timed recovery.
type OriginalBackup uint8

const (
	OriginalBackupOff OriginalBackup = iota
	OriginalBackupOn
	// OriginalBackupPreserve publishes a native resource without consulting
	// or changing a sibling original-document backup.
	OriginalBackupPreserve
)

// PreparedSave and PreparedNewSave keep sourced and never-sourced buffers distinct.
// They are single-use. Cancel succeeds only before publication starts; once started,
// callers must consume the real result, even if their active document has changed.
type PreparedSave struct{ request *saveRequest }
type PreparedNewSave struct{ request *saveRequest }

func (p *PreparedSave) Cancel() bool {
	return p != nil && p.request != nil && p.request.state.CompareAndSwap(0, 2)
}
func (p *PreparedNewSave) Cancel() bool {
	return p != nil && p.request != nil && p.request.state.CompareAndSwap(0, 2)
}

type saveRequest struct {
	directory      *openedDirectory
	guard          sourceGuard
	target, backup *Destination
	old, oldBackup snapshot
	image          *wp51.Image
	id             PublicationID
	setting        OriginalBackup
	state          atomic.Uint32
}

// SaveResult includes the acquired new source for the next edit/save cycle. No
// caller-side reread or invented source identity is needed to save repeatedly.
type SaveResult struct {
	Outcome  Outcome
	Document *Document
	ID       PublicationID
}

func (d *Directory) PrepareSave(source *Document, target *Destination, data []byte, decision Decision, backup OriginalBackup, id PublicationID) (*PreparedSave, error) {
	if source == nil || source.image == nil || !source.origin.open() {
		return nil, failure(InvalidRequest, "prepare save source", "", nil)
	}
	src := *source
	r, err := d.prepareSave(sourceGuard{kind: guardLoaded, source: &src}, target, data, decision, backup, id)
	if err != nil {
		return nil, err
	}
	return &PreparedSave{r}, nil
}
func (d *Directory) PrepareNewSave(target *Destination, data []byte, decision Decision, backup OriginalBackup, id PublicationID) (*PreparedNewSave, error) {
	r, err := d.prepareSave(sourceGuard{kind: guardNew}, target, data, decision, backup, id)
	if err != nil {
		return nil, err
	}
	return &PreparedNewSave{r}, nil
}
func (d *Directory) prepareSave(guard sourceGuard, target *Destination, data []byte, decision Decision, backup OriginalBackup, id PublicationID) (*saveRequest, error) {
	cap := d.acquired()
	if err := receiver(cap, "prepare everyday save"); err != nil {
		return nil, err
	}
	if target == nil || target.directory != cap || id.Operation == 0 || id.Revision == 0 || (decision != NoOverwrite && decision != AllowOverwrite) || backup > OriginalBackupPreserve {
		return nil, failure(InvalidRequest, "prepare everyday save", "", nil)
	}
	dst := *target
	if dst.exists && decision != AllowOverwrite {
		return nil, failure(OverwriteRequired, "overwrite decision", dst.name, nil)
	}
	if _, err := DOSName(dst.name); err != nil {
		return nil, err
	}
	if len(data) > wp51.MaxInputBytes {
		return nil, failure(InputLimit, "candidate size", dst.name, nil)
	}
	img, err := wp51.Parse(data)
	if err != nil {
		return nil, failure(NativeRefused, "candidate framing", dst.name, err)
	}
	r := &saveRequest{directory: cap, guard: guard, target: &dst, image: img, id: id, setting: backup}
	if err = r.checkNames(); err != nil {
		return nil, err
	}
	if err = guard.check(); err != nil {
		return nil, err
	}
	if err = cap.checkDestination(&dst); err != nil {
		return nil, err
	}
	if dst.exists {
		r.old, err = cap.readStable(dst.name)
		if err != nil {
			return nil, err
		}
		if !sameStamp(r.old.identity, dst.identity) {
			return nil, failure(DestinationChanged, "prepare destination", dst.name, nil)
		}
	}
	if dst.exists && backup != OriginalBackupPreserve {
		name := strings.SplitN(strings.ToUpper(dst.name), ".", 2)[0] + ".BK!"
		if strings.EqualFold(name, dst.name) {
			return nil, failure(UnsafePath, "backup self collision (unqualified original case)", dst.name, nil)
		}
		actual, e := resolveDOS(cap, name)
		if e != nil {
			return nil, e
		}
		r.backup, err = cap.observe(actual)
		if err != nil {
			return nil, err
		}
		if r.backup.exists {
			r.oldBackup, err = cap.readStable(actual)
			if err != nil {
				return nil, err
			}
			if !sameStamp(r.backup.identity, r.oldBackup.identity) {
				return nil, failure(DestinationChanged, "prepare backup", actual, nil)
			}
			if r.oldBackup.identity.ID == r.old.identity.ID || (guard.source != nil && r.oldBackup.identity.ID == guard.source.identity.ID) {
				return nil, failure(UnsafePath, "backup aliases document", actual, nil)
			}
		}
	}
	if err = r.check(); err != nil {
		return nil, err
	}
	return r, nil
}
func (r *saveRequest) checkNames() error {
	for _, dst := range []*Destination{r.target, r.backup} {
		if dst == nil {
			continue
		}
		actual, err := resolveDOS(r.directory, dst.name)
		if err != nil {
			return err
		}
		if actual != dst.name {
			// A direct local-flat Observe may preserve lowercase for an absent
			// name. No existing case alias may be mistaken for that absence.
			if strings.EqualFold(actual, dst.name) {
				if _, e := r.directory.ops.Lstat(actual); errors.Is(e, fs.ErrNotExist) {
					continue
				}
			}
			return failure(DestinationChanged, "DOS alias changed", dst.name, nil)
		}
	}
	return nil
}
func (r *saveRequest) check() error {
	if err := r.guard.validate(r.directory, r.target); err != nil {
		return err
	}
	if err := r.guard.check(); err != nil {
		return err
	}
	if err := r.checkNames(); err != nil {
		return err
	}
	for _, pair := range []struct {
		d *Destination
		s snapshot
	}{{r.target, r.old}, {r.backup, r.oldBackup}} {
		if pair.d == nil {
			continue
		}
		if err := r.directory.checkDestination(pair.d); err != nil {
			return err
		}
		if pair.d.exists {
			now, err := r.directory.readStable(pair.d.name)
			if err != nil || !sameSnapshot(now.identity, pair.s.identity) {
				return failure(DestinationChanged, "save snapshot changed", pair.d.name, err)
			}
		}
	}
	return nil
}
func (d *Directory) PublishSave(p *PreparedSave, id PublicationID) (SaveResult, error) {
	if p == nil {
		return SaveResult{}, failure(InvalidRequest, "publish save", "", nil)
	}
	return d.publishEveryday(p.request, id, guardLoaded)
}
func (d *Directory) PublishNewSave(p *PreparedNewSave, id PublicationID) (SaveResult, error) {
	if p == nil {
		return SaveResult{}, failure(InvalidRequest, "publish new save", "", nil)
	}
	return d.publishEveryday(p.request, id, guardNew)
}

// rename changes ctime even when bytes and inode are conserved. Transaction
// checks deliberately ignore only ctime after its own namespace mutations.
func sameMoved(a, b snapshot) bool {
	return a.identity.ID == b.identity.ID && a.identity.Size == b.identity.Size && a.identity.Mode == b.identity.Mode && a.identity.Modified.Equal(b.identity.Modified) && a.identity.SHA256 == b.identity.SHA256 && bytes.Equal(a.data, b.data)
}

// A step retains the displaced inode under its private candidate name until both
// names are committed and synced. It can undo only while its own entries remain.
type saveStep struct {
	cap            *openedDirectory
	target         *Destination
	old            snapshot
	staged         candidate
	stagedSnapshot snapshot
	oldPin         file
	remove         bool
	applied        bool
}

func (s *saveStep) verify(name string, expected snapshot) error {
	got, err := s.cap.readStable(name)
	if err != nil || !sameMoved(got, expected) {
		return errors.Join(err, errors.New("transaction entry changed: "+name))
	}
	return nil
}
func (s *saveStep) apply() error {
	if err := s.cap.checkDestination(s.target); err != nil {
		return err
	}
	if s.target.exists {
		if err := s.verify(s.target.name, s.old); err != nil {
			return err
		}
	}
	if s.remove {
		// Empty staging reservation has already been removed; NOREPLACE prevents
		// clobbering a concurrent entry at this private recovery name.
		if err := s.cap.ops.Rename(s.target.name, s.staged.name, unix.RENAME_NOREPLACE); err != nil {
			return err
		}
		s.applied = true
		return s.verify(s.staged.name, s.old)
	}
	if err := s.verify(s.staged.name, s.stagedSnapshot); err != nil {
		return err
	}
	if s.target.exists {
		if err := s.cap.ops.Rename(s.staged.name, s.target.name, unix.RENAME_EXCHANGE); err != nil {
			return err
		}
	} else {
		if err := s.cap.ops.Link(s.staged.name, s.target.name); err != nil {
			return err
		}
	}
	s.applied = true
	if err := s.verify(s.target.name, s.stagedSnapshot); err != nil {
		return err
	}
	if s.target.exists {
		return s.verify(s.staged.name, s.old)
	}
	return nil
}
func (s *saveStep) undo() error {
	if !s.applied {
		return nil
	}
	if s.remove {
		if err := s.verify(s.staged.name, s.old); err != nil {
			return err
		}
		// Never overwrite a new backup supplied by another writer.
		if err := s.cap.ops.Rename(s.staged.name, s.target.name, unix.RENAME_NOREPLACE); err != nil {
			return err
		}
	} else {
		if err := s.verify(s.target.name, s.stagedSnapshot); err != nil {
			return err
		}
		if s.target.exists {
			if err := s.verify(s.staged.name, s.old); err != nil {
				return err
			}
			if err := s.cap.ops.Rename(s.staged.name, s.target.name, unix.RENAME_EXCHANGE); err != nil {
				return err
			}
		} else if err := s.cap.ops.Remove(s.target.name); err != nil {
			return err
		}
	}
	s.applied = false
	if s.target.exists {
		return s.verify(s.target.name, s.old)
	}
	_, err := s.cap.ops.Lstat(s.target.name)
	if !errors.Is(err, fs.ErrNotExist) {
		return errors.Join(err, errors.New("absent destination not restored"))
	}
	return nil
}
func (s *saveStep) cleanup() error {
	// If applied, the private name holds the old destination; otherwise the new
	// staged file. In either case cleanup refuses substituted or modified entries.
	expected := s.stagedSnapshot
	if s.applied && s.target.exists {
		expected = s.old
	}
	if s.remove && !s.applied {
		return nil
	}
	if err := s.verify(s.staged.name, expected); err != nil {
		return err
	}
	return s.cap.cleanup(candidate{name: s.staged.name, id: expected.identity.ID})
}
func (s *saveStep) close() error {
	var errs []error
	if s.staged.file != nil {
		errs = append(errs, s.staged.file.Close())
	}
	if s.staged.pin != nil {
		errs = append(errs, s.staged.pin.Close())
	}
	if s.oldPin != nil {
		errs = append(errs, s.oldPin.Close())
	}
	return errors.Join(errs...)
}
func (cap *openedDirectory) prepareStep(dst *Destination, old snapshot, data []byte, remove bool) (*saveStep, error) {
	s := &saveStep{cap: cap, target: dst, old: old, remove: remove}
	if dst.exists {
		var err error
		s.oldPin, err = cap.ops.OpenFile(dst.name, os.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_NONBLOCK, 0)
		if err != nil {
			return nil, err
		}
		info, err := s.oldPin.Stat()
		if err != nil {
			return nil, errors.Join(err, s.close())
		}
		id, err := identity(info)
		if err != nil || !sameStamp(id, old.identity) {
			return nil, errors.Join(err, errors.New("displaced file pin changed"), s.close())
		}
	}
	var err error
	s.staged, _, err = cap.stageCandidate(data, sha256.Sum256(data), true)
	if err != nil {
		cleanupErr := cap.cleanup(s.staged)
		residue := ""
		if cleanupErr != nil {
			residue = s.staged.name
		}
		return nil, &Failure{Kind: CandidateFailed, Stage: "stage save candidate", Name: dst.name, Candidate: residue, Cause: errors.Join(err, cleanupErr, s.close())}
	}
	s.stagedSnapshot, err = cap.readStable(s.staged.name)
	if err != nil {
		cleanupErr := cap.cleanup(s.staged)
		residue := ""
		if cleanupErr != nil {
			residue = s.staged.name
		}
		return nil, &Failure{Kind: CandidateFailed, Stage: "stage save candidate", Name: dst.name, Candidate: residue, Cause: errors.Join(err, cleanupErr, s.close())}
	}
	if remove {
		if err = cap.cleanup(s.staged); err != nil {
			return nil, errors.Join(err, s.close())
		}
	}
	return s, nil
}
func (d *Directory) publishEveryday(r *saveRequest, id PublicationID, kind guardKind) (result SaveResult, resultErr error) {
	cap := d.acquired()
	if err := receiver(cap, "publish everyday save"); err != nil {
		return result, err
	}
	if r == nil || r.directory != cap || r.id != id || r.guard.kind != kind || !r.state.CompareAndSwap(0, 1) {
		return result, failure(InvalidRequest, "prepared save identity or consumed request", "", nil)
	}
	cap.transaction.Lock()
	defer cap.transaction.Unlock()
	if err := r.check(); err != nil {
		return result, err
	}
	steps := []*saveStep{}
	defer func() {
		for _, s := range steps {
			if err := s.close(); err != nil {
				result = SaveResult{}
				resultErr = errors.Join(resultErr, &Failure{Kind: CleanupFailed, Stage: "save pin close", Name: r.target.name, DestinationMayExist: true, Cause: err})
			}
		}
	}()
	fail := func(cause error) (SaveResult, error) {
		var rollbackErr, cleanupErr error
		for i := len(steps) - 1; i >= 0; i-- {
			rollbackErr = errors.Join(rollbackErr, steps[i].undo())
		}
		if rollbackErr == nil {
			for _, s := range steps {
				cleanupErr = errors.Join(cleanupErr, s.cleanup())
			}
		}
		syncErr := cap.ops.SyncDirectory()
		kind := PublicationFailed
		if rollbackErr != nil || cleanupErr != nil || syncErr != nil {
			kind = PublicationUncertain
		}
		residues := []string{}
		var underlying *Failure
		if errors.As(cause, &underlying) && underlying.Candidate != "" {
			residues = append(residues, underlying.Candidate)
		}
		for _, s := range steps {
			if _, e := cap.ops.Lstat(s.staged.name); e == nil {
				residues = append(residues, s.staged.name)
			}
		}
		return SaveResult{}, &Failure{Kind: kind, Stage: "everyday save rollback", Name: r.target.name, Candidate: strings.Join(residues, ","), DestinationMayExist: kind == PublicationUncertain, Cause: errors.Join(cause, rollbackErr, cleanupErr, syncErr)}
	}
	main, err := cap.prepareStep(r.target, r.old, r.image.Export(), false)
	if err != nil {
		return result, err
	}
	steps = append(steps, main)
	if r.backup != nil && (r.setting == OriginalBackupOn || r.backup.exists) {
		step, e := cap.prepareStep(r.backup, r.oldBackup, r.old.data, r.setting == OriginalBackupOff)
		if e != nil {
			return fail(e)
		}
		steps = append(steps, step)
	}
	if err = r.check(); err != nil {
		return fail(err)
	}
	for _, s := range steps {
		if err = s.apply(); err != nil {
			return fail(err)
		}
	}
	if err = cap.ops.SyncDirectory(); err != nil {
		return fail(err)
	}
	// After this durable namespace checkpoint, cleanup failures cannot safely be
	// called refusal. Keep recovery residues and report the committed uncertainty.
	for _, s := range steps {
		if err = s.cleanup(); err != nil {
			return result, &Failure{Kind: CleanupFailed, Stage: "committed save cleanup", Name: r.target.name, Candidate: s.staged.name, DestinationMayExist: true, Cause: err}
		}
	}
	if err = cap.ops.SyncDirectory(); err != nil {
		return result, &Failure{Kind: PublicationUncertain, Stage: "save cleanup durability", Name: r.target.name, DestinationMayExist: true, Cause: err}
	}
	now, err := cap.readStable(r.target.name)
	if err != nil || !sameMoved(now, main.stagedSnapshot) {
		return result, &Failure{Kind: PublicationUncertain, Stage: "final saved document", Name: r.target.name, DestinationMayExist: true, Cause: errors.Join(err, errors.New("saved document changed"))}
	}
	if err = r.checkNames(); err != nil {
		return result, &Failure{Kind: PublicationUncertain, Stage: "final DOS alias", Name: r.target.name, DestinationMayExist: true, Cause: err}
	}
	// Verify the final backup too; cleanup may have exposed a concurrent writer.
	if r.backup != nil {
		if r.setting == OriginalBackupOn {
			backup, e := cap.readStable(r.backup.name)
			if e != nil || !sameMoved(backup, steps[1].stagedSnapshot) {
				return result, &Failure{Kind: PublicationUncertain, Stage: "final original backup", Name: r.target.name, DestinationMayExist: true, Cause: errors.Join(e, errors.New("backup changed"))}
			}
		} else if _, e := cap.ops.Lstat(r.backup.name); !errors.Is(e, fs.ErrNotExist) {
			return result, &Failure{Kind: PublicationUncertain, Stage: "final removed backup", Name: r.target.name, DestinationMayExist: true, Cause: errors.Join(e, errors.New("backup reappeared"))}
		}
	}
	result = SaveResult{Outcome: Outcome{State: Published, Name: r.target.name, DirectoryID: cap.id, Identity: now.identity}, Document: &Document{image: r.image, origin: cap, name: r.target.name, identity: now.identity}, ID: r.id}
	return result, nil
}
