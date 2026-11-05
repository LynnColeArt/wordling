package editor_test

import (
	"bytes"
	"errors"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
)

func freshNew(t testing.TB) (editor.Session, *storage.Directory, string) {
	t.Helper()
	path := t.TempDir()
	dir, err := storage.OpenDirectory(path)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = dir.Close() })
	s, err := editor.New(editor.Config{Locations: []editor.Location{{Directory: dir}}})
	if err != nil {
		t.Fatal(err)
	}
	return s, dir, path
}
func firstRequest(t *testing.T, s editor.Session, dir *storage.Directory, name string) (editor.Session, *editor.Intent) {
	t.Helper()
	s = key(t, s, editor.Save)
	s = text(t, s, name)
	s, observe := submit(t, s)
	if observe.Kind != editor.Observe {
		t.Fatal(observe.Kind)
	}
	dst, err := dir.Observe(name)
	if err != nil {
		t.Fatal(err)
	}
	s, pub := done(t, s, editor.Result{Operation: observe.Operation, Revision: observe.Revision, Kind: observe.Kind, Destination: dst})
	if pub == nil || pub.Kind != editor.PublishNewBuffer || !pub.RequestKey().Valid() {
		t.Fatal("missing sealed source-less request")
	}
	return s, pub
}
func finishFirst(t *testing.T, s editor.Session, i *editor.Intent) editor.Session {
	t.Helper()
	s, read := done(t, s, editor.ExecuteNewPublication(i))
	if read == nil || read.Kind != editor.BindNewSource || s.Source() != nil || s.Snapshot().Name != "" || !s.Snapshot().Dirty || s.Snapshot().SaveState == editor.NewNamePublished {
		t.Fatal("publication fabricated a clean/source state")
	}
	s, _ = done(t, s, editor.ExecuteFirstRead(read))
	if s.Snapshot().NewPhase != editor.NewAnchored || s.Source() == nil || s.Snapshot().Dirty {
		t.Fatalf("bind %+v", s.Snapshot())
	}
	return s
}
func TestNewActualStartupPublishReadPreservesBirthAndOriginalAbsence(t *testing.T) {
	for _, body := range []string{"", "ASCII"} {
		t.Run(body, func(t *testing.T) {
			s, d, path := freshNew(t)
			origin := s.Document().Birth()
			if !origin.IsNew() || s.Snapshot().Dirty || s.Snapshot().SavedRevision != (document.Revision{}) {
				t.Fatal("genesis vs saved")
			}
			if body != "" {
				s = text(t, s, body)
			}
			before := s.Snapshot()
			raw, _ := s.Document().Export()
			s, p := firstRequest(t, s, d, "FIRST")
			s = finishFirst(t, s, p)
			if s.Document().Birth() != origin || s.Document().Revision() != before.NativeRevision || s.Snapshot().Gap != before.Gap || s.Snapshot().SavedRevision != before.NativeRevision {
				t.Fatal("first Read replaced native/cursor")
			}
			_, err := s.Document().OriginalExport()
			var failure *document.Failure
			if !errors.As(err, &failure) || failure.Category != document.NoLoadedOriginal {
				t.Fatal("New became Loaded")
			}
			actual, err := os.ReadFile(filepath.Join(path, "FIRST"))
			if err != nil || !bytes.Equal(actual, raw) || s.Source().Identity() != s.Snapshot().FirstPublication.Result.Outcome.Identity {
				t.Fatal("actual41 source identity")
			}
			source := s.Source()
			*s.Source() = storage.Document{}
			*s.Document() = document.Document{}
			if s.Source().Identity() != source.Identity() || s.Document().Birth() != origin {
				t.Fatal("getters retargeted source")
			}
		})
	}
}
func TestNewNameCancellationAndClearRemainContextSpecific(t *testing.T) {
	s, _, _ := freshNew(t)
	s = text(t, s, "ASCII")
	base := s.Document().Revision()
	s = key(t, s, editor.Save)
	s = text(t, s, "CANCEL")
	s = key(t, s, editor.F1)
	if s.Document().Revision() != base || s.Source() != nil || s.Snapshot().Name != "" {
		t.Fatal("draft cancel changed native")
	}
	s = key(t, s, editor.F7)
	s = key(t, s, editor.F1)
	if s.Document().Revision() != base {
		t.Fatal("Save question F1")
	}
	s = key(t, s, editor.F7)
	s = key(t, s, editor.No)
	s = key(t, s, editor.No)
	if s.Document() != nil {
		t.Fatal("unqualified F7 clear minted New")
	}
	expectRefusal(t, s, editor.Event{Command: editor.Text, Text: "X"})
}
func TestNewPendingAuthorityForksAndMirrorsCannotRedirect(t *testing.T) {
	base, d, path := freshNew(t)
	base = text(t, base, "A")
	s, p := firstRequest(t, base, d, "A")
	fork, q := firstRequest(t, base, d, "B")
	if p.Operation != q.Operation || p.Revision != q.Revision || p.RequestKey() == q.RequestKey() {
		t.Fatal("same-counter forks share authority")
	}
	copy := *p
	if copy.RequestKey() != p.RequestKey() {
		t.Fatal("copy key")
	}
	other, err := storage.OpenDirectory(path)
	if err != nil {
		t.Fatal(err)
	}
	defer other.Close()
	fake := *p
	fake.Directory = other
	if editor.ExecuteNewPublication(&fake).Err == nil {
		t.Fatal("independent same-path root accepted")
	}
	for _, mutation := range []func(*editor.Intent){func(i *editor.Intent) { i.Operation++ }, func(i *editor.Intent) { i.Screen++ }, func(i *editor.Intent) { i.NativeRevision = document.Revision{} }, func(i *editor.Intent) { i.Candidate[0] ^= 1 }, func(i *editor.Intent) { *i.Destination = storage.Destination{} }, func(i *editor.Intent) { i.Name = "OTHER" }} {
		fake = *s.Snapshot().Pending
		mutation(&fake)
		if editor.ExecuteNewPublication(&fake).Err == nil {
			t.Fatal("mutated wrapper executed")
		}
	}
	if _, err = os.Stat(filepath.Join(path, "A")); !os.IsNotExist(err) {
		t.Fatal("forgery IO")
	}
	before := s.Snapshot()
	for _, c := range []editor.Command{editor.Text, editor.Save, editor.F7, editor.Macro, editor.SwitchDocument, editor.Retrieve} {
		expectRefusal(t, s, editor.Event{Command: c, Text: map[editor.Command]string{editor.Text: "X"}[c]})
	}
	genuine := editor.ExecuteNewPublication(p)
	forged := genuine
	forged.Outcome.Identity.ID.Inode++
	if next, _, err := s.Reduce(editor.Event{Command: editor.Complete, Result: &forged}); err == nil || next.Snapshot().Pending == nil || next.Snapshot().NewPhase != editor.AwaitPublish {
		t.Fatal("forged result consumed pending")
	}
	if next, _, err := fork.Reduce(editor.Event{Command: editor.Complete, Result: &genuine}); err == nil || next.Snapshot().Pending == nil {
		t.Fatal("foreign same-counter reply")
	}
	s, read := done(t, s, genuine)
	if s.Snapshot().NativeRevision != before.NativeRevision {
		t.Fatal("native changed while pending")
	}
	accepted := editor.ExecuteFirstRead(read)
	fakeRead := accepted
	*fakeRead.Document = storage.Document{}
	if _, _, err := s.Reduce(editor.Event{Command: editor.Complete, Result: &fakeRead}); err == nil {
		t.Fatal("rebound result document")
	}
	s, _ = done(t, s, editor.ExecuteFirstRead(read))
	bound := s.Snapshot()
	s, _ = done(t, s, genuine)
	if s.Snapshot().NativeRevision != bound.NativeRevision || s.Snapshot().Name != bound.Name || s.Snapshot().Detached.Applied {
		t.Fatal("duplicate/late reply")
	}
}
func TestNewActualReadRefusalsRetryNeverRepublishes(t *testing.T) {
	for _, variant := range []string{"missing", "same-bytes-new-inode", "changed-bytes", "metadata", "close"} {
		t.Run(variant, func(t *testing.T) {
			s, d, path := freshNew(t)
			s = text(t, s, "X")
			s, p := firstRequest(t, s, d, "FIRST")
			s, read := done(t, s, editor.ExecuteNewPublication(p))
			raw, _ := s.Document().Export()
			file := filepath.Join(path, "FIRST")
			switch variant {
			case "missing":
				if err := os.Rename(file, file+".retained"); err != nil {
					t.Fatal(err)
				}
			case "same-bytes-new-inode":
				os.Rename(file, file+".retained")
				if err := os.WriteFile(file, raw, 0600); err != nil {
					t.Fatal(err)
				}
			case "changed-bytes":
				if err := os.WriteFile(file, []byte("changed"), 0600); err != nil {
					t.Fatal(err)
				}
			case "metadata":
				if err := os.Chmod(file, 0644); err != nil {
					t.Fatal(err)
				}
			case "close":
				copy := *d
				if err := copy.Close(); err != nil {
					t.Fatal(err)
				}
			}
			result := editor.ExecuteFirstRead(read)
			s, _ = done(t, s, result)
			if s.Snapshot().NewPhase != editor.PublishedUnbound || s.Source() != nil || !s.Snapshot().Dirty || s.Snapshot().Name != "" {
				t.Fatal("bad Read falsely bound")
			}
			for _, c := range []editor.Command{editor.Save, editor.F7, editor.Retrieve, editor.Text} {
				expectRefusal(t, s, editor.Event{Command: c, Text: map[editor.Command]string{editor.Text: "Y"}[c]})
			}
			next, retry, err := s.Reduce(editor.Event{Command: editor.RetryFirstRead})
			if err != nil || retry.Kind != editor.BindNewSource || retry.RequestKey() == read.RequestKey() {
				t.Fatal("retry is not fresh Read-only")
			}
			if variant == "missing" {
				if err = os.Rename(file+".retained", file); err != nil {
					t.Fatal(err)
				}
			}
			next, _ = done(t, next, editor.ExecuteFirstRead(retry))
			// Even restoring the same inode via rename changes ctime: conservative refusal.
			if next.Snapshot().NewPhase != editor.PublishedUnbound {
				t.Fatal("changed identity rehabilitated")
			}
			after, _ := next.Document().Export()
			if !bytes.Equal(after, raw) {
				t.Fatal("refusal lost native")
			}
		})
	}
}
func TestNewReadOnlyRetryAfterCancelledReadAndUncertainPublishCannotReconcile(t *testing.T) {
	for _, publication := range []bool{false, true} {
		t.Run(map[bool]string{false: "read-only retry", true: "uncertain publication"}[publication], func(t *testing.T) {
			s, d, _ := freshNew(t)
			s, p := firstRequest(t, s, d, "FIRST")
			result := editor.ExecuteNewPublication(p)
			if !publication {
				s, p = done(t, s, result)
			}
			s = key(t, s, editor.CancelOperation)
			if publication {
				if s.Snapshot().NewPhase != editor.PublicationUncertain || !s.Snapshot().Dirty {
					t.Fatal("cancel proved absence")
				}
				s, _ = done(t, s, result)
				expectRefusal(t, s, editor.Event{Command: editor.RetryFirstRead})
				expectRefusal(t, s, editor.Event{Command: editor.F7})
			} else {
				next, retry, err := s.Reduce(editor.Event{Command: editor.RetryFirstRead})
				if err != nil {
					t.Fatal(err)
				}
				next, _ = done(t, next, editor.ExecuteFirstRead(retry))
				if next.Snapshot().NewPhase != editor.NewAnchored {
					t.Fatal("same exact receipt Read retry failed")
				}
			}
		})
	}
}
func TestNewActualTargetRaceAndSharedCloseAreDefiniteBeforePublication(t *testing.T) {
	for _, closed := range []bool{false, true} {
		s, d, path := freshNew(t)
		s, p := firstRequest(t, s, d, "FIRST")
		if closed {
			alias := *d
			alias.Close()
		} else {
			os.WriteFile(filepath.Join(path, "FIRST"), []byte("foreign"), 0600)
		}
		result := editor.ExecuteNewPublication(p)
		if result.Err == nil {
			t.Fatal("expected actual41 refusal")
		}
		s, _ = done(t, s, result)
		if s.Snapshot().NewPhase != editor.NewUnpublished || s.Source() != nil || s.Snapshot().SaveState != editor.SaveFailed {
			t.Fatal("definite failure lied about publication")
		}
	}
}

func TestNewLaterSaveAsKeepsFirstAnchorAndBirth(t *testing.T) {
	s, d, path := freshNew(t)
	s = text(t, s, "A")
	s, p := firstRequest(t, s, d, "FIRST")
	s = finishFirst(t, s, p)
	birth := s.Document().Birth()
	anchor := s.Source().Identity()
	first := s.Snapshot().FirstPublication
	s = text(t, s, "B")
	s = text(t, key(t, s, editor.Save), "SECOND")
	s, i := submit(t, s)
	s, i = done(t, s, perform(i))
	if i.Kind != editor.PublishCandidate {
		t.Fatal("did not use existing sourced path")
	}
	s, _ = done(t, s, perform(i))
	if s.Source().Identity() != anchor || s.Source().Name() != "FIRST" || s.Document().Birth() != birth || s.Snapshot().FirstPublication.Result.Outcome != first.Result.Outcome || s.Snapshot().Name != "SECOND" {
		t.Fatal("SaveAs rebased birth/source/first receipt")
	}
	if err := os.WriteFile(filepath.Join(path, "FIRST"), []byte("external"), 0600); err != nil {
		t.Fatal(err)
	}
	s = text(t, key(t, s, editor.Save), "THIRD")
	s, i = submit(t, s)
	s, i = done(t, s, perform(i))
	s, _ = done(t, s, perform(i))
	if s.Snapshot().SaveState != editor.SaveFailed || s.Snapshot().Name != "SECOND" {
		t.Fatal("first source guard bypass")
	}
	if _, err := os.Stat(filepath.Join(path, "THIRD")); !os.IsNotExist(err) {
		t.Fatal("published after first source changed")
	}
}
func TestNewHistoryBirthAndSuspensionSurviveFirstBinding(t *testing.T) {
	s, d, _ := freshNew(t)
	s = text(t, s, "AB")
	s = key(t, s, editor.Left)
	s = key(t, s, editor.Delete)
	h := s.History()
	birth := s.Document().Birth()
	count := h.Count()
	s, p := firstRequest(t, s, d, "FIRST")
	rev := s.Document().Revision()
	gap := s.Snapshot().Gap
	s = finishFirst(t, s, p)
	if s.Document().Birth() != birth || s.Document().Revision() != rev || s.Snapshot().Gap != gap || s.History().Count() != count {
		t.Fatal("binding reset history/native")
	}
	// The actual history state/eligibility is delegated to document, never rebuilt.
	if h.Count() != count {
		t.Fatal("old history fork mutated")
	}
}
func TestNewForgedZeroUnexecutedReplyAndDefiniteFailureFreshOperation(t *testing.T) {
	s, d, path := freshNew(t)
	s, p := firstRequest(t, s, d, "FIRST")
	fake := editor.Result{Operation: p.Operation, Revision: p.Revision, Kind: p.Kind, Outcome: storage.Outcome{State: storage.Published}}
	if n, _, e := s.Reduce(editor.Event{Command: editor.Complete, Result: &fake}); e == nil || n.Snapshot().Pending == nil {
		t.Fatal("unexecuted public receipt accepted")
	}
	if (editor.Intent{}).RequestKey().Valid() {
		t.Fatal("zero key")
	}
	os.WriteFile(filepath.Join(path, "FIRST"), []byte("foreign"), 0600)
	s, _ = done(t, s, editor.ExecuteNewPublication(p))
	os.Remove(filepath.Join(path, "FIRST"))
	next, q := firstRequest(t, s, d, "FIRST")
	if q.Operation <= p.Operation || q.RequestKey() == p.RequestKey() {
		t.Fatal("definite failure reused request")
	}
	_ = finishFirst(t, next, q)
}
func FuzzFirstBindingAuthority(f *testing.F) {
	f.Add([]byte{0, 1, 2, 3, 4, 5})
	f.Add([]byte{8, 9, 10, 11})
	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) > 64 {
			return
		}
		s, d, _ := freshNew(t)
		s, p := firstRequest(t, s, d, "FIRST")
		raw, _ := s.Document().Export()
		original := s
		for _, b := range data {
			fake := *original.Snapshot().Pending
			switch b % 7 {
			case 0:
				fake.Operation++
			case 1:
				fake.Revision++
			case 2:
				fake.Screen++
			case 3:
				fake.Name = "OTHER"
			case 4:
				fake.NativeRevision = document.Revision{}
			case 5:
				fake.Candidate[0] ^= 1
			case 6:
				*fake.Directory = storage.Directory{}
			}
			r := editor.ExecuteNewPublication(&fake)
			if r.Err == nil {
				t.Fatal("forged wrapper executed")
			}
			n, _, _ := original.Reduce(editor.Event{Command: editor.Complete, Result: &r})
			got, _ := n.Document().Export()
			if !bytes.Equal(got, raw) || n.Source() != nil || n.Snapshot().Name != "" {
				t.Fatal("authority refusal mutated")
			}
		}
		_ = finishFirst(t, s, p)
	})
}

func TestNewRepeatedReadFailuresRetainOriginalReceiptAndNative(t *testing.T) {
	s, d, _ := freshNew(t)
	s, p := firstRequest(t, s, d, "FIRST")
	s, read := done(t, s, editor.ExecuteNewPublication(p))
	first := s.Snapshot().FirstPublication
	native := s.Document().Revision()
	birth := s.Document().Birth()
	d.Close()
	s, _ = done(t, s, editor.ExecuteFirstRead(read))
	operation := read.Operation
	for n := 0; n < 100; n++ {
		next, q, err := s.Reduce(editor.Event{Command: editor.RetryFirstRead})
		if err != nil || q.Operation <= operation {
			t.Fatal("retry token/counter")
		}
		operation = q.Operation
		s, _ = done(t, next, editor.ExecuteFirstRead(q))
		snap := s.Snapshot()
		if snap.FirstPublication.Result.Outcome != first.Result.Outcome || snap.NativeRevision != native || s.Document().Birth() != birth || snap.Name != "" || snap.NewPhase != editor.PublishedUnbound {
			t.Fatal("retry lost original receipt/native")
		}
	}
}

func TestNewCapturedDirectorySurvivesCallerWrapperReplacement(t *testing.T) {
	s, d, original := freshNew(t)
	keep := *d
	defer keep.Close()
	s, p := firstRequest(t, s, d, "FIRST")
	otherPath := t.TempDir()
	other, err := storage.OpenDirectory(otherPath)
	if err != nil {
		t.Fatal(err)
	}
	defer other.Close()
	*d = *other
	s = finishFirst(t, s, p)
	if s.Source() == nil {
		t.Fatal("missing first anchor")
	}
	if _, err = os.Stat(filepath.Join(original, "FIRST")); err != nil {
		t.Fatal("accepted root lost")
	}
	if _, err = os.Stat(filepath.Join(otherPath, "FIRST")); !os.IsNotExist(err) {
		t.Fatal("caller rebound root")
	}
}

func TestNewExistingTargetNeverEnablesReplacement(t *testing.T) {
	s, d, path := freshNew(t)
	raw, _ := s.Document().Export()
	os.WriteFile(filepath.Join(path, "FIRST"), []byte("foreign"), 0600)
	s = text(t, key(t, s, editor.Save), "FIRST")
	s, i := submit(t, s)
	target, err := d.Observe("FIRST")
	if err != nil {
		t.Fatal(err)
	}
	s, _ = done(t, s, editor.Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind, Destination: target})
	if s.Snapshot().Mode != editor.ReplaceQuestion {
		t.Fatal("expected existing-target prompt")
	}
	next, _, err := s.Reduce(editor.Event{Command: editor.Yes})
	var failure *storage.Failure
	if !errors.As(err, &failure) || failure.Kind != storage.UnsupportedReplacement {
		t.Fatal("New replacement not explicitly refused")
	}
	got, _ := next.Document().Export()
	file, _ := os.ReadFile(filepath.Join(path, "FIRST"))
	if !bytes.Equal(got, raw) || string(file) != "foreign" || next.Source() != nil {
		t.Fatal("replacement refusal changed data")
	}
}

func TestNewRealPermissionFailureThenUserFreshTransaction(t *testing.T) {
	if os.Geteuid() == 0 {
		t.Skip("root bypasses this real directory permission qualification")
	}
	s, d, path := freshNew(t)
	s = text(t, s, "X")
	s, p := firstRequest(t, s, d, "FIRST")
	raw, _ := s.Document().Export()
	if err := os.Chmod(path, 0500); err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = os.Chmod(path, 0700) })
	result := editor.ExecuteNewPublication(p)
	var failure *storage.Failure
	if !errors.As(result.Err, &failure) || failure.Kind != storage.CandidateFailed {
		t.Fatalf("actual create permission failure: %v", result.Err)
	}
	s, _ = done(t, s, result)
	if s.Snapshot().NewPhase != editor.NewUnpublished || s.Source() != nil || s.Snapshot().Name != "" {
		t.Fatal("permission failure claimed save")
	}
	got, _ := s.Document().Export()
	if !bytes.Equal(got, raw) {
		t.Fatal("permission failure lost native")
	}
	if err := os.Chmod(path, 0700); err != nil {
		t.Fatal(err)
	}
	next, q := firstRequest(t, s, d, "FIRST")
	if q.RequestKey() == p.RequestKey() {
		t.Fatal("reused failed request")
	}
	_ = finishFirst(t, next, q)
}
