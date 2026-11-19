package editor_test

import (
	"bytes"
	"crypto/sha256"
	"errors"
	"fmt"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
	"io"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
)

func TestGivenBlankSessionWhenNormalF1ThenUndeleteUnsupported(t *testing.T) {
	s, err := editor.New(editor.Config{})
	if err != nil {
		t.Fatal(err)
	}
	next, intent, err := s.Reduce(editor.Event{Command: editor.F1})
	if err == nil || intent != nil || next.Snapshot().Mode != editor.Editing {
		t.Fatal("read-only F1 must refuse Undelete")
	}
}

type fixture struct {
	dir     *storage.Directory
	path    string
	raw     []byte
	session editor.Session
}

func setup(t *testing.T) fixture {
	t.Helper()
	raw, err := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if err != nil {
		t.Fatal(err)
	}
	if fmt.Sprintf("%x", sha256.Sum256(raw)) != "c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d" {
		t.Fatal("original fixture identity")
	}
	path := t.TempDir()
	if err = os.WriteFile(filepath.Join(path, "ORIGIN"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	dir, err := storage.OpenDirectory(path)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = dir.Close() })
	s, err := editor.New(editor.Config{Locations: []editor.Location{{Prefix: "B:\\", Directory: dir}, {Prefix: "C:\\OUT\\", Directory: dir}}})
	if err != nil {
		t.Fatal(err)
	}
	return fixture{dir, path, raw, s}
}
func key(t *testing.T, s editor.Session, c editor.Command) editor.Session {
	t.Helper()
	next, i, e := s.Reduce(editor.Event{Command: c})
	if e != nil || i != nil {
		t.Fatalf("command %d: %v, intent=%v", c, e, i)
	}
	return next
}
func text(t *testing.T, s editor.Session, value string) editor.Session {
	t.Helper()
	next, i, e := s.Reduce(editor.Event{Command: editor.Text, Text: value})
	if e != nil || i != nil {
		t.Fatalf("text: %v", e)
	}
	return next
}
func submit(t *testing.T, s editor.Session) (editor.Session, *editor.Intent) {
	t.Helper()
	next, i, e := s.Reduce(editor.Event{Command: editor.Enter})
	if e != nil || i == nil {
		t.Fatalf("submit: %v", e)
	}
	return next, i
}

// Host adapter in tests: calls the real approved APIs; reducer never executes IO.
func perform(i *editor.Intent) editor.Result {
	r := editor.Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind}
	switch i.Kind {
	case editor.Read:
		r.Document, r.Err = i.Directory.Read(i.Name)
	case editor.Observe:
		r.Destination, r.Err = i.Directory.Observe(i.Name)
	case editor.PublishCandidate:
		p, err := i.Directory.PreparePublication(i.Document, i.Destination, i.Candidate, storage.PublicationID{Operation: i.Operation, Revision: i.Revision})
		r.Err = err
		if err == nil {
			r.Outcome, r.Err = i.Directory.Publish(p, p.ID())
		}
	case editor.WriteSnapshot:
		r.Outcome, r.Err = i.Directory.Save(i.Document, i.Destination, i.Decision)
	}
	return r
}
func done(t *testing.T, s editor.Session, r editor.Result) (editor.Session, *editor.Intent) {
	t.Helper()
	next, i, e := s.Reduce(editor.Event{Command: editor.Complete, Result: &r})
	if e != nil {
		t.Fatal(e)
	}
	return next, i
}
func load(t *testing.T, f fixture) editor.Session {
	t.Helper()
	s := key(t, f.session, editor.Retrieve)
	s = text(t, s, "B:\\ORIGIN")
	s, i := submit(t, s)
	s, next := done(t, s, perform(i))
	if next != nil {
		t.Fatal("unexpected intent")
	}
	return s
}
func expectRefusal(t *testing.T, s editor.Session, event editor.Event) {
	t.Helper()
	next, i, err := s.Reduce(event)
	if err == nil || i != nil {
		t.Fatal("expected explicit refusal")
	}
	a, b := s.Snapshot(), next.Snapshot()
	if a.Mode != b.Mode || a.Name != b.Name || a.Gap != b.Gap || a.Revision != b.Revision {
		t.Fatal("refusal changed document state")
	}
}
func unchanged(t *testing.T, s editor.Session, raw []byte) {
	t.Helper()
	a, e := s.Document().Export()
	if e != nil || !bytes.Equal(a, raw) {
		t.Fatal("native changed")
	}
}

// CMD51-237/238 and239: original blank Retrieve cancel and missing-name retry.
func TestGivenRetrieveDraftWhenContextualCancelOrMissingThenBlankOrRetry(t *testing.T) {
	f := setup(t)
	for _, cancel := range []editor.Command{editor.F1, editor.Escape} {
		s := text(t, key(t, f.session, editor.Retrieve), "B:\\MISSING")
		s = key(t, s, cancel)
		if s.Snapshot().Mode != editor.Editing || s.Source() != nil {
			t.Fatal("cancel retrieve")
		}
	}
	s := text(t, key(t, f.session, editor.Retrieve), "B:\\MISSING")
	s, i := submit(t, s)
	s, _ = done(t, s, perform(i))
	if s.Snapshot().Mode != editor.RetrieveName || s.Snapshot().Notice != "ERROR: File not found -- B:\\MISSING" || s.Snapshot().Draft != "B:\\MISSING" {
		t.Fatalf("retry: %+v", s.Snapshot())
	}
	s = text(t, s, "B:\\ORIGIN")
	s, i = submit(t, s)
	s, _ = done(t, s, perform(i))
	if s.Snapshot().Name != "B:\\ORIGIN" || s.Snapshot().Gap != 0 {
		t.Fatal("retrieve identity")
	}
	unchanged(t, s, f.raw)
	expectRefusal(t, s, editor.Event{Command: editor.Retrieve})
}

func TestGivenUndecodedOrEditingCommandsWhenReadOnlyThenExplicitUnsupported(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	for _, c := range []editor.Command{editor.Escape, editor.Left, editor.Backspace, editor.Up, editor.Yes} {
		expectRefusal(t, s, editor.Event{Command: c})
	}
	expectRefusal(t, s, editor.Event{Command: editor.Text, Text: "\x80"})
	expectRefusal(t, f.session, editor.Event{Command: editor.Save})
	expectRefusal(t, s, editor.Event{Command: editor.Save, Text: "mixed"})
	unchanged(t, s, f.raw)
}

// CMD51-049 and048: one immutable cursor supplies both projections.
func TestGivenBoldGapsWhenRightAndRevealThenSharedNativeCoordinates(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	base := s
	offsets := []int{324, 325, 328, 329, 330, 333, 334}
	for gap, want := range offsets {
		if s.Snapshot().Gap != gap {
			t.Fatal("gap")
		}
		p, e := s.Present(0, 6)
		if e != nil {
			t.Fatal(e)
		}
		var normal string
		for _, v := range p.Elements {
			normal += v.Text
		}
		if normal != "ABCD" {
			t.Fatal(normal)
		}
		s = key(t, s, editor.Reveal)
		r, e := s.Present(0, 6)
		if e != nil || r.CursorGap != gap {
			t.Fatal(e)
		}
		var reveal string
		for _, v := range r.Elements {
			reveal += v.Text
		}
		if reveal != "A[BOLD]BC[bold]D" {
			t.Fatal(reveal)
		}
		s = key(t, s, editor.Reveal)
		cursor, _ := s.Document().CursorAt(gap)
		offset, _ := cursor.Offset()
		if offset != want {
			t.Fatalf("offset%d !=%d", offset, want)
		}
		if gap < 6 {
			s = key(t, s, editor.Right)
		}
	}
	expectRefusal(t, s, editor.Event{Command: editor.Right})
	if base.Snapshot().Gap != 0 {
		t.Fatal("prior value mutated")
	}
	unchanged(t, s, f.raw)
}

// CMD51-019/020: body-leading Bold witness is not all document Initial Codes.
func TestGivenLeadingBoldWhenHome2VersusHome3ThenDifferentTokenGap(t *testing.T) {
	f := setup(t)
	raw, e := os.ReadFile("../../docs/research/continuation/session1/runs/2026-10-31-session1-b01-r1/CMD51-049/LEAD.WP5")
	if e != nil {
		t.Fatal(e)
	}
	if fmt.Sprintf("%x", sha256.Sum256(raw)) != "62eab679536fbd23e03f4c609ee2b9bf0672fddb83129681aacce194f4efce7a" {
		t.Fatal("LEAD identity")
	}
	if e = os.WriteFile(filepath.Join(f.path, "ORIGIN"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	original := load(t, f)
	for _, reveal := range []bool{false, true} {
		for homes := 2; homes <= 3; homes++ {
			s := original
			if reveal {
				s = key(t, s, editor.Reveal)
			}
			for range homes {
				s = key(t, s, editor.Home)
			}
			s = key(t, s, editor.Up)
			want := 0
			if homes == 2 {
				want = 1
			}
			if s.Snapshot().Gap != want || s.Snapshot().Reveal != reveal || s.Snapshot().HomePrefix != 0 {
				t.Fatal("home endpoint")
			}
			s = key(t, s, editor.Right)
			if s.Snapshot().Gap != want+1 {
				t.Fatal("Right witness")
			}
			unchanged(t, s, raw)
		}
	}
	pending := key(t, original, editor.Home)
	expectRefusal(t, pending, editor.Event{Command: editor.Reveal})
}

// CMD51-069 (edit and cancel only),070 (character-first name) and149 (FC-002).
func TestGivenPrefilledFilenameWhenEditOrCharacterFirstThenCaretOrNewName(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	start := s
	s = key(t, s, editor.Save)
	if s.Snapshot().Caret != 0 || s.Snapshot().OriginalName != "B:\\ORIGIN" {
		t.Fatal("prefilled caret")
	}
	for range 5 {
		s = key(t, s, editor.Right)
	}
	s = key(t, s, editor.Backspace)
	s = text(t, s, "X")
	expectRefusal(t, s, editor.Event{Command: editor.Enter})
	if s.Snapshot().Draft != "B:\\OXIGIN" {
		t.Fatal(s.Snapshot().Draft)
	}
	s = key(t, s, editor.F1)
	if s.Snapshot().Name != start.Snapshot().Name {
		t.Fatal("draft renamed source")
	}
	s = text(t, key(t, s, editor.Save), "C:\\OUT\\CHARFST")
	if s.Snapshot().Draft != "C:\\OUT\\CHARFST" {
		t.Fatal("first character appended")
	}
	s, observe := submit(t, s)
	if observe.Kind != editor.Observe {
		t.Fatal("observe before save")
	}
	s, save := done(t, s, perform(observe))
	if save.Kind != editor.WriteSnapshot || save.Decision != storage.NoOverwrite {
		t.Fatal("absent destination")
	}
	s, _ = done(t, s, perform(save))
	if s.Snapshot().SaveState != editor.NewNamePublished || s.Snapshot().Mode != editor.Editing || s.Snapshot().Name != "C:\\OUT\\CHARFST" {
		t.Fatal("publication")
	}
	disk, e := os.ReadFile(filepath.Join(f.path, "CHARFST"))
	if e != nil || !bytes.Equal(disk, f.raw) {
		t.Fatal("FC002")
	}
	unchanged(t, s, f.raw)
	old, e := os.ReadFile(filepath.Join(f.path, "ORIGIN"))
	if e != nil || !bytes.Equal(old, f.raw) {
		t.Fatal("source changed")
	}
}

func TestGivenExistingDestinationWhenNoOrExplicitSameFileYesThenRefusalOrNoOp(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	s, i := submit(t, key(t, s, editor.Save))
	s, _ = done(t, s, perform(i))
	if s.Snapshot().Prompt != "Replace B:\\ORIGIN? No (Yes)" {
		t.Fatal(s.Snapshot().Prompt)
	}
	refused := key(t, s, editor.No)
	if refused.Snapshot().Mode != editor.SaveName || refused.Snapshot().Draft != "B:\\ORIGIN" {
		t.Fatal("refusal loses name")
	}
	refused = key(t, refused, editor.F1)
	unchanged(t, refused, f.raw)
	s, save, err := s.Reduce(editor.Event{Command: editor.Yes})
	if err != nil || save == nil || save.Decision != storage.AllowOverwrite {
		t.Fatal(err)
	}
	s, _ = done(t, s, perform(save))
	if s.Snapshot().SaveState != editor.SameFileNoOp {
		t.Fatal("same-file no-op must be distinct")
	}
	if err = os.WriteFile(filepath.Join(f.path, "OTHER"), f.raw, 0600); err != nil {
		t.Fatal(err)
	}
	s = text(t, key(t, s, editor.Save), "B:\\OTHER")
	s, i = submit(t, s)
	s, _ = done(t, s, perform(i))
	next, save, err := s.Reduce(editor.Event{Command: editor.Yes})
	var failure *storage.Failure
	if !errors.As(err, &failure) || failure.Kind != storage.UnsupportedReplacement || save != nil || next.Snapshot().Mode != editor.ReplaceQuestion {
		t.Fatal("actual replacement not refused")
	}
}

// CMD51-240..244/087: read-only supports clean named and fresh empty contexts.
func TestGivenCleanContextsWhenF7DecisionsThenContextualPreserveClearOrExit(t *testing.T) {
	f := setup(t)
	for _, base := range []editor.Session{f.session, load(t, f)} {
		save := key(t, base, editor.F7)
		if save.Snapshot().Prompt != "Save document? Yes (No)" || save.Snapshot().Notice != "(Text was not modified)" {
			t.Fatal("save question")
		}
		returned := key(t, save, editor.F1)
		if !sameSource(returned.Source(), base.Source()) {
			t.Fatal("F1 Save context lost source")
		}
		advanced := key(t, save, editor.Escape)
		if advanced.Snapshot().Mode != editor.SaveName {
			t.Fatal("Esc should advance")
		}
		expectRefusal(t, advanced, editor.Event{Command: editor.Enter})
		returned = key(t, advanced, editor.F1)
		if !sameSource(returned.Source(), base.Source()) {
			t.Fatal("F1 filename lost source")
		}
		confirm := key(t, save, editor.No)
		if confirm.Snapshot().Prompt != "Exit WP? No (Yes) (Cancel to return to document)" {
			t.Fatal("exit question")
		}
		returned = key(t, confirm, editor.F1)
		if !sameSource(returned.Source(), base.Source()) {
			t.Fatal("F1 Exit context lost source")
		}
		for _, c := range []editor.Command{editor.No, editor.Escape} {
			clear := key(t, confirm, c)
			if clear.Source() != nil || clear.Snapshot().Name != "" || clear.Snapshot().Mode != editor.Editing {
				t.Fatal("No/Esc must clear")
			}
		}
		exited := key(t, confirm, editor.Yes)
		if exited.Snapshot().Mode != editor.Exited {
			t.Fatal("F7 n y")
		}
		expectRefusal(t, exited, editor.Event{Command: editor.Save})
	}
}

func TestGivenPendingReadWhenCancelledAndLateThenNeverReplacesNewOperation(t *testing.T) {
	f := setup(t)
	s := text(t, key(t, f.session, editor.Retrieve), "B:\\ORIGIN")
	s, old := submit(t, s)
	result := perform(old)
	s = key(t, s, editor.CancelOperation)
	s = key(t, s, editor.F1)
	s = text(t, key(t, s, editor.Retrieve), "B:\\MISSING")
	s, current := submit(t, s)
	next, _ := done(t, s, result)
	if next.Source() != nil || next.Snapshot().Pending.Operation != current.Operation || next.Snapshot().Detached.Applied {
		t.Fatal("late read hijacked new operation")
	}
	for _, alter := range []func(*editor.Result){func(r *editor.Result) { r.Operation++ }, func(r *editor.Result) { r.Revision++ }, func(r *editor.Result) { r.Kind = editor.Observe }} {
		wrong := perform(current)
		alter(&wrong)
		next, _ = done(t, s, wrong)
		if next.Snapshot().Pending.Operation != current.Operation {
			t.Fatal("mismatched receipt consumed pending")
		}
	}
	next, _ = done(t, next, perform(current))
	if next.Snapshot().Mode != editor.RetrieveName || next.Source() != nil {
		t.Fatal("missing retry")
	}
}

func TestGivenCancelledPublicationWhenLateSuccessThenReconcileWithoutSaveSuccess(t *testing.T) {
	f := setup(t)
	s := text(t, key(t, load(t, f), editor.Save), "B:\\LATE")
	s, i := submit(t, s)
	s, save := done(t, s, perform(i))
	s = key(t, s, editor.CancelOperation)
	r := perform(save)
	if r.Err != nil {
		t.Fatal(r.Err)
	}
	s, _ = done(t, s, r)
	if s.Snapshot().Mode != editor.SaveName || s.Snapshot().SaveState != editor.NotSaved || s.Snapshot().Name != "B:\\ORIGIN" || !s.Snapshot().Detached.DestinationMayExist || s.Snapshot().Detached.Applied {
		t.Fatal("late publication is not user-visible success")
	}
	actual, e := os.ReadFile(filepath.Join(f.path, "LATE"))
	if e != nil || !bytes.Equal(actual, f.raw) {
		t.Fatal("test must exercise actual side effect")
	}
}

func TestGivenStorageFailuresWhenCompletionThenNoFalseSuccessAndResiduePreserved(t *testing.T) {
	f := setup(t)
	base := load(t, f)
	for _, kind := range []storage.Kind{storage.StaleSource, storage.DestinationChanged, storage.CandidateFailed, storage.PublicationFailed, storage.PublicationUncertain, storage.CleanupFailed} {
		t.Run(string(kind), func(t *testing.T) {
			s := text(t, key(t, base, editor.Save), "B:\\FAIL")
			s, i := submit(t, s)
			s, save := done(t, s, perform(i))
			failure := &storage.Failure{Kind: kind, Stage: "injected completion boundary", Name: save.Name, Candidate: "candidate-residue", DestinationMayExist: kind == storage.PublicationUncertain || kind == storage.CleanupFailed, Cause: io.ErrShortWrite}
			result := editor.Result{Operation: save.Operation, Revision: save.Revision, Kind: save.Kind, Err: failure, Outcome: storage.Outcome{State: storage.Published}}
			s, _ = done(t, s, result)
			snap := s.Snapshot()
			want := editor.SaveFailed
			if failure.DestinationMayExist {
				want = editor.SaveUncertain
			}
			if snap.Mode != editor.SaveName || snap.SaveState != want || snap.Last.Candidate != "candidate-residue" || snap.Name != "B:\\ORIGIN" || !errors.Is(snap.Last.Result.Err, io.ErrShortWrite) {
				t.Fatal("failure details/success")
			}
			snap.Last.Result.Err.(*storage.Failure).Candidate = "tampered"
			if s.Snapshot().Last.Candidate != "candidate-residue" || s.Snapshot().Last.Result.Err.(*storage.Failure).Candidate != "candidate-residue" {
				t.Fatal("snapshot failure alias")
			}
			unchanged(t, s, f.raw)
		})
	}
}

func TestGivenActualStaleSourceOrDestinationRaceThenStorageRefusalSurvivesReducer(t *testing.T) {
	for _, race := range []string{"source", "destination"} {
		t.Run(race, func(t *testing.T) {
			f := setup(t)
			s := text(t, key(t, load(t, f), editor.Save), "B:\\TARGET")
			s, i := submit(t, s)
			s, save := done(t, s, perform(i))
			name := "TARGET"
			want := storage.DestinationChanged
			if race == "source" {
				name = "ORIGIN"
				want = storage.StaleSource
			}
			if e := os.WriteFile(filepath.Join(f.path, name), f.raw, 0600); e != nil {
				t.Fatal(e)
			}
			r := perform(save)
			var failure *storage.Failure
			if !errors.As(r.Err, &failure) || failure.Kind != want {
				t.Fatalf("real storage refusal: %v", r.Err)
			}
			s, _ = done(t, s, r)
			if s.Snapshot().SaveState != editor.SaveFailed || s.Snapshot().Mode == editor.Exited {
				t.Fatal("false success")
			}
			unchanged(t, s, f.raw)
		})
	}
}

func TestGivenWrongSuccessIdentityThenNoSuccessfulSave(t *testing.T) {
	f := setup(t)
	s := text(t, key(t, load(t, f), editor.Save), "B:\\TARGET")
	s, i := submit(t, s)
	s, save := done(t, s, perform(i))
	r := editor.Result{Operation: save.Operation, Revision: save.Revision, Kind: save.Kind, Outcome: storage.Outcome{State: storage.Published, Name: "foreign"}}
	next, intent, err := s.Reduce(editor.Event{Command: editor.Complete, Result: &r})
	if err == nil || intent != nil || next.Snapshot().SaveState != editor.SaveFailed || next.Snapshot().Mode != editor.SaveName {
		t.Fatal("unbound success accepted")
	}
}

func TestGivenInvalidFilenameOrConfigurationThenNoIntent(t *testing.T) {
	f := setup(t)
	for _, value := range []string{"/tmp/foreign", "B:\\..", "B:\\sub\\file", "Z:\\UNKNOWN", "B:\\.wordling-candidate-forged"} {
		s := text(t, key(t, f.session, editor.Retrieve), value)
		expectRefusal(t, s, editor.Event{Command: editor.Enter})
	}
	s := key(t, f.session, editor.Retrieve)
	expectRefusal(t, s, editor.Event{Command: editor.Text, Text: "é"})
	expectRefusal(t, s, editor.Event{Command: editor.Text, Text: "\x1b"})
	expectRefusal(t, s, editor.Event{Command: editor.Text, Text: strings.Repeat("x", 256)})
	if _, e := editor.New(editor.Config{Locations: []editor.Location{{Prefix: "B:\\", Directory: f.dir}, {Prefix: "B:\\", Directory: f.dir}}}); e == nil {
		t.Fatal("ambiguous binding")
	}
	if _, err := editor.New(editor.Config{Locations: []editor.Location{{Directory: &storage.Directory{}}}}); err == nil {
		t.Fatal("zero directory accepted")
	}
	var zero editor.Session
	expectRefusal(t, zero, editor.Event{Command: editor.F7})
}

func TestGivenSharedImmutableSessionWhenConcurrentProjectionsThenNoMutation(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	var wg sync.WaitGroup
	for range 16 {
		wg.Go(func() {
			for range 100 {
				next, _, err := s.Reduce(editor.Event{Command: editor.Reveal})
				if err != nil {
					t.Error(err)
					return
				}
				if _, err = next.Present(0, 6); err != nil {
					t.Error(err)
				}
				if s.Snapshot().Reveal {
					t.Error("shared source mutated")
				}
			}
		})
	}
	wg.Wait()
	unchanged(t, s, f.raw)
}

func TestGivenPendingOrCompletedValuesWhenCallerMutatesCopiesThenBindingsRemain(t *testing.T) {
	f := setup(t)
	s := text(t, key(t, f.session, editor.Retrieve), "B:\\ORIGIN")
	s, i := submit(t, s)
	operation := i.Operation
	i.Operation++
	snap := s.Snapshot()
	snap.Pending.Revision++
	snap.Pending.Name = "forged"
	original := s.Snapshot().Pending
	if original.Operation != operation || original.Revision != 0 || original.Name != "ORIGIN" {
		t.Fatal("intent alias")
	}
	r := perform(original)
	s, _ = done(t, s, r)
	revision := s.Snapshot().Revision
	s, _ = done(t, s, r)
	if s.Snapshot().Revision != revision || s.Snapshot().Detached.Applied || s.Source() == nil {
		t.Fatal("duplicate load reapplied")
	}
	exported := s.Source().Export()
	exported[0] ^= 1
	semantic, _ := s.Document().Export()
	semantic[0] ^= 1
	unchanged(t, s, f.raw)
}

func TestGivenDeclaredRootWhenFlatNameThenNoInventedDriveMapping(t *testing.T) {
	f := setup(t)
	s, err := editor.New(editor.Config{Locations: []editor.Location{{Directory: f.dir}}})
	if err != nil {
		t.Fatal(err)
	}
	forbidden := text(t, key(t, s, editor.Retrieve), "B:\\ORIGIN")
	expectRefusal(t, forbidden, editor.Event{Command: editor.Enter})
	s = text(t, key(t, s, editor.Retrieve), "ORIGIN")
	s, i := submit(t, s)
	s, _ = done(t, s, perform(i))
	if s.Snapshot().Name != "ORIGIN" {
		t.Fatal("flat-name profile")
	}
	unchanged(t, s, f.raw)
}

func TestGivenSeparatePinnedDirectoriesWhenPublishThenTargetIdentityAndSourceRemain(t *testing.T) {
	f := setup(t)
	targetPath := t.TempDir()
	target, err := storage.OpenDirectory(targetPath)
	if err != nil {
		t.Fatal(err)
	}
	defer target.Close()
	s, err := editor.New(editor.Config{Locations: []editor.Location{{Prefix: "B:\\", Directory: f.dir}, {Prefix: "C:\\OUT\\", Directory: target}}})
	if err != nil {
		t.Fatal(err)
	}
	f.session = s
	s = text(t, key(t, load(t, f), editor.Save), "C:\\OUT\\COPY")
	s, i := submit(t, s)
	if i.Directory.ID() != target.ID() {
		t.Fatal("directory binding")
	}
	s, save := done(t, s, perform(i))
	s, _ = done(t, s, perform(save))
	if s.Snapshot().Last.Result.Outcome.DirectoryID != target.ID() || s.Source().DirectoryID() != f.dir.ID() {
		t.Fatal("source rebound to destination")
	}
	raw, err := os.ReadFile(filepath.Join(targetPath, "COPY"))
	if err != nil || !bytes.Equal(raw, f.raw) {
		t.Fatal("cross-directory exact snapshot")
	}
}

func TestGivenOpaqueNativeTokenWhenNavigationRefusedThenExactSnapshotSurvives(t *testing.T) {
	f := setup(t)
	opaque := append([]byte(nil), f.raw...)
	opaque[324] = 0x80 // Synthetic refusal case, not an original glyph claim.
	if err := os.WriteFile(filepath.Join(f.path, "ORIGIN"), opaque, 0600); err != nil {
		t.Fatal(err)
	}
	s := load(t, f)
	expectRefusal(t, s, editor.Event{Command: editor.Right})
	if _, err := s.Present(0, 6); err == nil {
		t.Fatal("opaque presented as empty glyph")
	}
	home := key(t, key(t, s, editor.Home), editor.Home)
	expectRefusal(t, home, editor.Event{Command: editor.Up})
	unchanged(t, s, opaque)
}

// I1: a matching IO envelope/fingerprint cannot make an impossible inode a save.
// This is a structural receipt check, not filesystem-side-effect authentication.
func TestGivenMatchingPublishedReceiptWithoutInodeThenFailedSavePreservesSession(t *testing.T) {
	for _, id := range []storage.FileID{{}, {Device: 17}} {
		t.Run(fmt.Sprintf("device%d", id.Device), func(t *testing.T) {
			f := setup(t)
			base := load(t, f)
			base = key(t, base, editor.Right)
			base = key(t, base, editor.Reveal)
			s := text(t, key(t, base, editor.Save), "B:\\TARGET")
			s, i := submit(t, s)
			s, write := done(t, s, perform(i))
			if _, err := os.Stat(filepath.Join(f.path, "TARGET")); !errors.Is(err, os.ErrNotExist) {
				t.Fatal("target must still be absent; no Save executed")
			}
			identity := write.Document.Identity()
			identity.ID = id
			forged := editor.Result{Operation: write.Operation, Revision: write.Revision, Kind: write.Kind, Outcome: storage.Outcome{State: storage.Published, Name: write.Name, DirectoryID: write.Directory.ID(), Identity: identity}}
			next, intent, err := s.Reduce(editor.Event{Command: editor.Complete, Result: &forged})
			if err == nil {
				t.Fatalf("zero inode was falsely successful: %+v", next.Snapshot())
			}
			snap := next.Snapshot()
			if intent != nil || snap.SaveState != editor.SaveFailed || snap.Mode != editor.SaveName || snap.Pending != nil || snap.Last.Result.Err == nil {
				t.Fatal("matching malformed receipt must complete as explicit failed attempt")
			}
			if snap.Name != base.Snapshot().Name || snap.Revision != base.Snapshot().Revision || snap.Gap != base.Snapshot().Gap || snap.Reveal != base.Snapshot().Reveal || !sameSource(next.Source(), base.Source()) || next.Document().Revision() != base.Document().Revision() {
				t.Fatal("malformed receipt changed source/document/name/cursor/view")
			}
			if s.Snapshot().Pending.Operation != write.Operation {
				t.Fatal("previous immutable waiting value mutated")
			}
			if _, err = os.Stat(filepath.Join(f.path, "TARGET")); !errors.Is(err, os.ErrNotExist) {
				t.Fatal("reducer performed IO")
			}
			unchanged(t, next, f.raw)
			// Retrying must acquire a new observation; a duplicate old receipt cannot win.
			next, observe := submit(t, next)
			if observe.Kind != editor.Observe || observe.Operation == write.Operation {
				t.Fatal("retry reused failed operation")
			}
			detached, _, err := next.Reduce(editor.Event{Command: editor.Complete, Result: &forged})
			if err != nil || detached.Snapshot().Pending.Operation != observe.Operation || detached.Snapshot().Detached.Applied || detached.Snapshot().Name != base.Snapshot().Name {
				t.Fatal("stale malformed receipt consumed retry")
			}
		})
	}
}

func TestGivenValidPublishedShapeWithDeviceZeroThenDeviceAloneDoesNotRefuse(t *testing.T) {
	f := setup(t)
	s := text(t, key(t, load(t, f), editor.Save), "B:\\TARGET")
	s, i := submit(t, s)
	s, write := done(t, s, perform(i))
	actual := perform(write)
	if actual.Err != nil || actual.Outcome.Identity.ID.Inode == 0 {
		t.Fatalf("real publication identity: %+v", actual)
	}
	// Device 0 is a structurally valid Linux device number. The IO boundary remains
	// trusted: this shape test does not claim that our actual target has device0.
	actual.Outcome.Identity.ID.Device = 0
	s, _ = done(t, s, actual)
	if s.Snapshot().SaveState != editor.NewNamePublished || s.Snapshot().Name != "B:\\TARGET" {
		t.Fatal("device zero was incorrectly treated as absent identity")
	}
}

func sameSource(a, b *storage.Document) bool {
	if a == nil || b == nil {
		return a == b
	}
	return a.Identity() == b.Identity() && a.Name() == b.Name() && a.DirectoryID() == b.DirectoryID()
}
