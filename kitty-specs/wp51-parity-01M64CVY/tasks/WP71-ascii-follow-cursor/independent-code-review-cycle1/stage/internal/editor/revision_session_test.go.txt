package editor_test

import (
	"bytes"
	"crypto/sha256"
	"errors"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"path/filepath"
	"testing"
)

func queued(t *testing.T, s editor.Session, name string) (editor.Session, *editor.Intent) {
	t.Helper()
	s = text(t, key(t, s, editor.Save), "B:\\"+name)
	s, i := submit(t, s)
	return done(t, s, perform(i))
}
func TestCandidateSaveBindsCurrentRevisionAndOriginalGuard(t *testing.T) {
	f := setup(t)
	s := text(t, load(t, f), "X")
	source := s.Source().Identity()
	native := s.Document().Revision()
	if !s.Snapshot().Dirty {
		t.Fatal("edit not dirty")
	}
	s, i := queued(t, s, "FIRST")
	if i.Kind != editor.PublishCandidate {
		t.Fatal("edited save routed snapshot")
	}
	candidate := append([]byte(nil), i.Candidate...)
	s, _ = done(t, s, perform(i))
	x := s.Snapshot()
	if x.Dirty || x.SavedRevision != native || x.PublishedRevision != native || x.Name != "B:\\FIRST" || s.Source().Identity() != source {
		t.Fatalf("saved identities: %+v", x)
	}
	disk, _ := os.ReadFile(filepath.Join(f.path, "FIRST"))
	if !bytes.Equal(disk, candidate) {
		t.Fatal("candidate publication")
	}
	s = text(t, s, "Y")
	s, i = queued(t, s, "SECOND")
	if i.Document.Identity() != source {
		t.Fatal("source guard silently rebased")
	}
	if err := os.WriteFile(filepath.Join(f.path, "ORIGIN"), append(f.raw, 'Q'), 0600); err != nil {
		t.Fatal(err)
	}
	r := perform(i)
	var failure *storage.Failure
	if !errors.As(r.Err, &failure) || failure.Kind != storage.StaleSource {
		t.Fatalf("original source freshness: %v", r.Err)
	}
	s, _ = done(t, s, r)
	if !s.Snapshot().Dirty || s.Snapshot().Name != "B:\\FIRST" || s.Snapshot().PublishedRevision != native {
		t.Fatal("failed second save cleared dirty/name/receipt")
	}
	if _, err := os.Stat(filepath.Join(f.path, "SECOND")); !errors.Is(err, os.ErrNotExist) {
		t.Fatal("stale source published")
	}
}
func TestPendingCandidateNewerTypingAndDetachedCompletion(t *testing.T) {
	f := setup(t)
	s := text(t, load(t, f), "X")
	s, i := queued(t, s, "COPY")
	candidate := append([]byte(nil), i.Candidate...)
	s = text(t, s, "Y")
	rev := s.Document().Revision()
	r := perform(i)
	s, _ = done(t, s, r)
	x := s.Snapshot()
	if !x.Dirty || x.Name != "B:\\ORIGIN" || x.SavedRevision == rev || x.Detached.Applied || !x.Detached.DestinationMayExist || x.Pending != nil {
		t.Fatalf("late revision: %+v", x)
	}
	disk, _ := os.ReadFile(filepath.Join(f.path, "COPY"))
	if !bytes.Equal(disk, candidate) {
		t.Fatal("actual earlier effects lost")
	}
	s, _ = done(t, s, r)
	if s.Document().Revision() != rev || !s.Snapshot().Dirty {
		t.Fatal("duplicate cleared edit")
	}
}
func TestPublicIntentAndResultIsolation(t *testing.T) {
	f := setup(t)
	s := key(t, f.session, editor.Retrieve)
	s = text(t, s, "B:\\ORIGIN")
	s, i := submit(t, s)
	r := perform(i)
	s, _ = done(t, s, r)
	*r.Document = storage.Document{}
	if s.Source().Identity().Size == 0 {
		t.Fatal("accepted result wrapper borrowed")
	}
	s = text(t, s, "X")
	s, i = queued(t, s, "FIRST")
	good := s.Snapshot().Pending
	clear(i.Candidate)
	*i.Document = storage.Document{}
	*i.Directory = storage.Directory{}
	*i.Destination = storage.Destination{}
	snap := s.Snapshot()
	clear(snap.Pending.Candidate)
	*snap.Pending.Document = storage.Document{}
	*snap.Pending.Directory = storage.Directory{}
	*snap.Pending.Destination = storage.Destination{}
	actual := perform(good)
	s, _ = done(t, s, actual)
	if s.Snapshot().Dirty || s.Snapshot().SaveState != editor.NewNamePublished {
		t.Fatal("returned intent retargeted internal request")
	}
	last := s.Snapshot().Last
	last.Result.Outcome.Identity.Size = 0
	if s.Snapshot().Last.Result.Outcome.Identity.Size == 0 {
		t.Fatal("receipt retargeted")
	}
}
func TestDirectoryConfigurationCopyAndRealClose(t *testing.T) {
	f := setup(t)
	original := *f.dir
	*f.dir = storage.Directory{} // Config must already own its wrapper.
	s := load(t, f)
	if s.Source().Identity().Size != int64(len(f.raw)) {
		t.Fatal("location alias")
	}
	if err := original.Close(); err != nil {
		t.Fatal(err)
	}
	s = text(t, s, "X")
	s = text(t, key(t, s, editor.Save), "B:\\FIRST")
	s, i := submit(t, s)
	r := perform(i)
	if r.Err == nil {
		t.Fatal("private wrapper copy bypassed actual lifetime")
	}
	s, _ = done(t, s, r)
	if !s.Snapshot().Dirty {
		t.Fatal("closed save became clean")
	}
}
func TestMalformedCandidateResultsNeverSave(t *testing.T) {
	for _, mutation := range []string{"hash", "size", "name", "root", "inode", "kind", "revision", "operation"} {
		t.Run(mutation, func(t *testing.T) {
			f := setup(t)
			s := text(t, load(t, f), "X")
			s, i := queued(t, s, "COPY")
			r := editor.Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind, Outcome: storage.Outcome{State: storage.Published, Name: i.Name, DirectoryID: i.Directory.ID(), Identity: storage.Identity{Size: int64(len(i.Candidate)), SHA256: sha256.Sum256(i.Candidate), ID: storage.FileID{Inode: 42}}}}
			switch mutation {
			case "hash":
				r.Outcome.Identity.SHA256[0] ^= 1
			case "size":
				r.Outcome.Identity.Size++
			case "name":
				r.Outcome.Name = "OTHER"
			case "root":
				r.Outcome.DirectoryID = storage.FileID{}
			case "inode":
				r.Outcome.Identity.ID = storage.FileID{}
			case "kind":
				r.Kind = editor.Read
			case "revision":
				r.Revision++
			case "operation":
				r.Operation++
			}
			next, _, _ := s.Reduce(editor.Event{Command: editor.Complete, Result: &r})
			if !next.Snapshot().Dirty || next.Snapshot().Name != "B:\\ORIGIN" || next.Snapshot().SaveState == editor.NewNamePublished {
				t.Fatal("forged envelope saved revision")
			}
			if _, err := os.Stat(filepath.Join(f.path, "COPY")); !errors.Is(err, os.ErrNotExist) {
				t.Fatal("reducer performed IO")
			}
		})
	}
}
func TestUncertainDetachedAndMatchingFailuresKeepEffects(t *testing.T) {
	for _, detach := range []bool{false, true} {
		t.Run(map[bool]string{true: "detached", false: "matching"}[detach], func(t *testing.T) {
			f := setup(t)
			s := text(t, load(t, f), "X")
			s, i := queued(t, s, "COPY")
			if detach {
				s = key(t, s, editor.CancelOperation)
			}
			failure := &storage.Failure{Kind: storage.PublicationUncertain, Stage: "post-link witness", DestinationMayExist: true, Candidate: ".wordling-candidate-witness"}
			r := editor.Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind, Err: failure}
			s, _ = done(t, s, r)
			failure.DestinationMayExist = false
			x := s.Snapshot()
			receipt := x.Last
			if detach {
				receipt = x.Detached
			} else if x.SaveState != editor.SaveUncertain {
				t.Fatal("uncertainty hidden")
			}
			if !x.Dirty || !receipt.DestinationMayExist || receipt.Candidate == "" {
				t.Fatal("possible effects/dirty lost")
			}
			if e, ok := receipt.Result.Err.(*storage.Failure); ok {
				e.Candidate = "changed"
			}
			x = s.Snapshot()
			if !detach && x.Last.Candidate == "changed" {
				t.Fatal("failure getter alias")
			}
		})
	}
}
func TestDirtyExitAndReplacementNeverFalseSuccess(t *testing.T) {
	f := setup(t)
	s := text(t, load(t, f), "CHANGED")
	question := key(t, s, editor.F7)
	if question.Snapshot().Notice == "(Text was not modified)" {
		t.Fatal("dirty notice false")
	}
	if key(t, question, editor.F1).Document().Revision() != s.Document().Revision() {
		t.Fatal("F1 lost edits")
	}
	advance := key(t, question, editor.Escape)
	if advance.Snapshot().Mode != editor.SaveName {
		t.Fatal("Esc was generic cancel")
	}
	expectRefusal(t, advance, editor.Event{Command: editor.Enter})
	exit := key(t, question, editor.No)
	if key(t, exit, editor.F1).Document().Revision() != s.Document().Revision() {
		t.Fatal("exit F1")
	}
	if key(t, exit, editor.Escape).Document() != nil {
		t.Fatal("exit Esc did not clear")
	}
	save := key(t, s, editor.Save)
	save, i := submit(t, save)
	save, _ = done(t, save, perform(i))
	expectRefusal(t, save, editor.Event{Command: editor.Yes})
	if !save.Snapshot().Dirty {
		t.Fatal("replacement refusal lost dirty")
	}
}

func TestCandidateLateDestinationAndCancelledObservation(t *testing.T) {
	f := setup(t)
	s := text(t, load(t, f), "X")
	s, i := queued(t, s, "LATE")
	if err := os.WriteFile(filepath.Join(f.path, "LATE"), []byte("external"), 0600); err != nil {
		t.Fatal(err)
	}
	r := perform(i)
	if r.Err == nil {
		t.Fatal("late target accepted")
	}
	s, _ = done(t, s, r)
	if !s.Snapshot().Dirty || s.Snapshot().SaveState != editor.SaveFailed {
		t.Fatal("failed candidate became clean")
	}
	raw, _ := os.ReadFile(filepath.Join(f.path, "LATE"))
	if string(raw) != "external" {
		t.Fatal("external destination changed")
	}
	s = text(t, key(t, key(t, s, editor.F1), editor.Save), "B:\\OTHER")
	s, observe := submit(t, s)
	r = perform(observe)
	s = key(t, s, editor.CancelOperation)
	s, _ = done(t, s, r)
	if s.Snapshot().Pending != nil || s.Snapshot().Detached.Applied {
		t.Fatal("cancelled observation emitted publication")
	}
}
func TestMetadataOnlyRepairIsDirty(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	s = key(t, s, editor.Reveal)
	s = key(t, s, editor.Right)
	s = key(t, s, editor.Block)
	s = key(t, s, editor.Right)
	s = key(t, s, editor.Backspace)
	before := s.Document().Revision()
	number := s.Snapshot().Revision
	s = key(t, s, editor.Yes)
	if s.Document().Revision() == before || s.Snapshot().Revision != number+1 || !s.Snapshot().Dirty || s.Snapshot().Selection || s.Snapshot().Gap != 2 {
		t.Fatal("body-equal native repair lost metadata dirtiness")
	}
}

func TestOptimisticPublishedOutcomeWithHostFailureStaysUncertain(t *testing.T) {
	f := setup(t)
	s := text(t, load(t, f), "X")
	s, i := queued(t, s, "COPY")
	r := perform(i)
	if r.Err != nil {
		t.Fatal(r.Err)
	}
	r.Err = errors.New("host failed after real publication")
	s, _ = done(t, s, r)
	if !s.Snapshot().Last.DestinationMayExist || s.Snapshot().SaveState != editor.SaveUncertain || !s.Snapshot().Dirty {
		t.Fatal("published output plus host error hid possible effects")
	}
	if _, err := os.Stat(filepath.Join(f.path, "COPY")); err != nil {
		t.Fatal(err)
	}
}
