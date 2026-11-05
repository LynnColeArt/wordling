package editor

import (
	"bytes"
	"os"
	"path/filepath"
	"reflect"
	"runtime"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/storage"
)

const (
	boldOnTest  = "\xc3\x0c\xc3"
	boldOffTest = "\xc4\x0c\xc4"
)

func boldFixture(t *testing.T) (Session, *storage.Directory, string) {
	t.Helper()
	path := t.TempDir()
	dir, err := storage.OpenDirectory(path)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = dir.Close() })
	s, err := New(Config{Locations: []Location{{Directory: dir}}})
	if err != nil {
		t.Fatal(err)
	}
	return s, dir, path
}

func boldApply(t *testing.T, s Session, e Event) (Session, *Intent) {
	t.Helper()
	next, intent, err := s.Reduce(e)
	if err != nil {
		t.Fatalf("command %v: %v", e.Command, err)
	}
	return next, intent
}

func boldKey(t *testing.T, s Session, c Command) Session {
	t.Helper()
	next, i := boldApply(t, s, Event{Command: c})
	if i != nil {
		t.Fatalf("unexpected intent %v for command %v", i.Kind, c)
	}
	return next
}

func boldType(t *testing.T, s Session, text string) Session {
	t.Helper()
	next, i := boldApply(t, s, Event{Command: Text, Text: text})
	if i != nil {
		t.Fatal("unexpected text intent")
	}
	return next
}

func boldNative(t *testing.T, s Session) []byte {
	t.Helper()
	b, err := s.Document().Export()
	if err != nil {
		t.Fatal(err)
	}
	return b
}

func boldBody(t *testing.T, s Session) string {
	t.Helper()
	c, err := s.Document().CursorAt(0)
	if err != nil {
		t.Fatal(err)
	}
	off, err := c.Offset()
	if err != nil {
		t.Fatal(err)
	}
	return string(boldNative(t, s)[off:])
}

func boldAssertRefusal(t *testing.T, s, next Session, intent *Intent, err error) {
	t.Helper()
	if err == nil || intent != nil || next.transition != s.transition ||
		next.History().Revision() != s.History().Revision() ||
		next.Snapshot().NativeRevision != s.Snapshot().NativeRevision ||
		!reflect.DeepEqual(s, next) {
		t.Fatalf("expected complete session refusal, got intent %v and error %v", intent, err)
	}
}

func boldRefused(t *testing.T, s Session, e Event) error {
	t.Helper()
	next, i, err := s.Reduce(e)
	boldAssertRefusal(t, s, next, i, err)
	return err
}

func boldActiveSession(t *testing.T, s Session) Session {
	t.Helper()
	return boldType(t, boldKey(t, s, Bold), "BC")
}

func boldClosedSession(t *testing.T, s Session) Session {
	t.Helper()
	return boldKey(t, boldActiveSession(t, s), Bold)
}

func boldIsActive(s Session) bool {
	_, active := s.History().ActiveBold(s.Document())
	return active
}

func boldNoFiles(t *testing.T, path string) {
	t.Helper()
	files, err := os.ReadDir(path)
	if err != nil || len(files) != 0 {
		t.Fatalf("unexpected filesystem effect: %v %v", files, err)
	}
}

func boldExecute(t *testing.T, i *Intent) Result {
	t.Helper()
	if i == nil {
		t.Fatal("missing genuine intent")
	}
	r := Result{Kind: i.Kind, Operation: i.Operation, Revision: i.Revision}
	switch i.Kind {
	case Observe:
		r.Destination, r.Err = i.Directory.Observe(i.Name)
	case Read:
		r.Document, r.Err = i.Directory.Read(i.Name)
	case PublishNewBuffer:
		return ExecuteNewPublication(i)
	case BindNewSource:
		return ExecuteFirstRead(i)
	case WriteSnapshot:
		r.Outcome, r.Err = i.Directory.Save(i.Document, i.Destination, i.Decision)
	default:
		t.Fatalf("unexpected intent kind %v", i.Kind)
	}
	return r
}

func boldCompleteIO(t *testing.T, s Session, i *Intent) (Session, *Intent) {
	t.Helper()
	r := boldExecute(t, i)
	return boldApply(t, s, Event{Command: Complete, Result: &r})
}

func boldStartSave(t *testing.T, s Session, name string) (Session, *Intent) {
	t.Helper()
	s = boldType(t, boldKey(t, s, Save), name)
	s, i := boldApply(t, s, Event{Command: Enter})
	if i == nil || i.Kind != Observe {
		t.Fatal("save did not issue real Observe")
	}
	return s, i
}

func TestBoldSessionLifecycle(t *testing.T) {
	if RetryFirstRead != 24 || Bold != RetryFirstRead+1 {
		t.Fatal("Bold must follow the unchanged existing command values")
	}
	s, _, path := boldFixture(t)
	s = boldType(t, s, "A")
	start := s
	open := boldKey(t, s, Bold)
	if !boldIsActive(open) || open.Snapshot().HistoryQualified || open.Snapshot().HistoryCountKnown ||
		open.Snapshot().HistoryCount != 0 || open.revision != start.revision+1 ||
		open.sequence != start.sequence || open.transition == start.transition ||
		open.provenance != Bold || open.native.Birth() != start.native.Birth() ||
		boldBody(t, open) != "A"+boldOnTest+boldOffTest || open.cursor.Gap() != 2 {
		t.Fatal("begin did not adopt actual E receipt and unknown history atomically")
	}
	boldRefused(t, open, Event{Command: Bold})
	visible := boldKey(t, open, Reveal)
	if visible.native.Revision() != open.native.Revision() || visible.History().Revision() != open.History().Revision() {
		t.Fatal("Reveal altered native or active history")
	}
	active := boldType(t, visible, "BC")
	if active.cursor.Gap() != 4 || !boldIsActive(active) || !active.cursor.Reveal() ||
		active.revision != open.revision+1 || boldBody(t, active) != "A"+boldOnTest+"BC"+boldOffTest {
		t.Fatal("actual Text did not advance active Off")
	}
	closed := boldKey(t, active, Bold)
	if boldIsActive(closed) || closed.revision != active.revision ||
		closed.native.Revision() != active.native.Revision() || closed.history.Revision() == active.history.Revision() ||
		closed.cursor.Gap() != 5 || !closed.cursor.Reveal() || closed.provenance != Bold ||
		closed.transition == active.transition || closed.History().CountKnown() {
		t.Fatal("close did not adopt genuine cursor-only result")
	}
	closed = boldType(t, boldKey(t, closed, Reveal), "D")
	if boldBody(t, closed) != "A"+boldOnTest+"BC"+boldOffTest+"D" {
		t.Fatal("wrong native body after plain suffix")
	}
	nonEOF := boldKey(t, closed, Left)
	boldRefused(t, nonEOF, Event{Command: Bold})
	s = boldClosedSession(t, boldKey(t, nonEOF, Right))
	if boldBody(t, s) != "A"+boldOnTest+"BC"+boldOffTest+"D"+boldOnTest+"BC"+boldOffTest {
		t.Fatal("wrong second genuine pair")
	}
	boldRefused(t, s, Event{Command: Bold})
	boldNoFiles(t, path)
}

func TestBoldActiveRefusals(t *testing.T) {
	s, _, path := boldFixture(t)
	s = boldKey(t, s, Bold)
	for _, key := range []Command{Save, Left, Right, Home, Up, Insert, Block, Delete, Backspace,
		F1, Enter, Escape, Macro, SwitchDocument, Restore, Previous} {
		boldRefused(t, s, Event{Command: key})
	}
	for _, input := range []string{"", "é", "\n", "\xc3\x0c\xc3"} {
		boldRefused(t, s, Event{Command: Text, Text: input})
	}
	s = boldKey(t, boldType(t, s, "R"), Bold)
	if boldBody(t, s) != boldOnTest+"R"+boldOffTest {
		t.Fatal("refusal consumed active recovery path")
	}
	boldNoFiles(t, path)
}

func TestBoldExitRoutes(t *testing.T) {
	s, _, path := boldFixture(t)
	active := boldActiveSession(t, s)
	question := boldKey(t, active, F7)
	if question.mode != ExitSaveQuestion || !boldIsActive(question) ||
		question.native.Revision() != active.native.Revision() || question.history.Revision() != active.history.Revision() {
		t.Fatal("F7 lost active ownership")
	}
	for _, cmd := range []Command{Escape, Yes, Save} {
		boldRefused(t, question, Event{Command: cmd})
	}
	if s := boldKey(t, question, F1); s.mode != Editing || !boldIsActive(s) {
		t.Fatal("F1 did not return to active editing")
	}
	exit := boldKey(t, question, No)
	if exit.mode != ExitQuestion || !boldIsActive(exit) {
		t.Fatal("No did not keep the real exit question")
	}
	if s := boldKey(t, exit, F1); s.mode != Editing || !boldIsActive(s) {
		t.Fatal("exit-question F1 did not preserve active ownership")
	}
	if s := boldKey(t, exit, Yes); s.mode != Exited || s.native != nil {
		t.Fatal("no-save exit failed")
	}
	for _, cmd := range []Command{No, Escape} {
		cleared := boldKey(t, exit, cmd)
		if cleared.mode != Editing || cleared.native != nil || boldIsActive(cleared) ||
			cleared.history.Revision() != active.history.Revision() {
			t.Fatal("clear lost retained history or remained active")
		}
		retrieve := boldKey(t, cleared, Retrieve)
		if retrieve.mode != RetrieveName {
			t.Fatal("legacy Retrieve stopped working after clear")
		}
	}
	boldNoFiles(t, path)
	if err := os.WriteFile(filepath.Join(path, "RETURN"), boldNative(t, s), 0600); err != nil {
		t.Fatal(err)
	}
	retrieve := boldType(t, boldKey(t, boldKey(t, exit, No), Retrieve), "RETURN")
	retrieve, i := boldApply(t, retrieve, Event{Command: Enter})
	retrieve, i = boldCompleteIO(t, retrieve, i)
	if i != nil || retrieve.source == nil || boldIsActive(retrieve) {
		t.Fatal("actual legacy retrieval after discard failed")
	}
}

func TestBoldClosedSaveWaiver(t *testing.T) {
	s, _, path := boldFixture(t)
	s = boldClosedSession(t, s)
	beforeHistory := s.history.Revision()
	s = boldKey(t, boldKey(t, s, Save), F1)
	if s.historyValid || s.history.Revision() != beforeHistory || s.source != nil || s.sequence != 0 {
		t.Fatal("closed Save did not use the inherited waiver")
	}
	boldRefused(t, s, Event{Command: Bold})
	s = boldType(t, s, "D")
	if s.history.Revision() != beforeHistory || boldBody(t, s) != boldOnTest+"BC"+boldOffTest+"D" {
		t.Fatal("legacy post-waiver Text repaired or lost history")
	}
	if _, ok := boldRefused(t, s, Event{Command: Bold}).(*Refusal); !ok {
		t.Fatal("post-waiver Bold reached E instead of the early session refusal")
	}
	if !boldKey(t, s, Reveal).cursor.Reveal() {
		t.Fatal("legacy Reveal refused after waiver")
	}
	boldNoFiles(t, path)
}

func TestBoldRootedPublication(t *testing.T) {
	s, dir, _ := boldFixture(t)
	s = boldType(t, boldClosedSession(t, boldType(t, s, "A")), "D")
	raw := boldNative(t, s)
	before := s
	s, observe := boldStartSave(t, s, "FIRST")
	s, publish := boldCompleteIO(t, s, observe)
	if publish == nil || publish.Kind != PublishNewBuffer {
		t.Fatal("missing New publication intent")
	}
	s, read := boldCompleteIO(t, s, publish)
	if read == nil || read.Kind != BindNewSource {
		t.Fatal("missing first read binding")
	}
	s, next := boldCompleteIO(t, s, read)
	if next != nil || s.newPhase != NewAnchored || s.source == nil || s.name != "FIRST" ||
		s.saved != before.native.Revision() || s.historyValid || s.history.Revision() != before.history.Revision() ||
		!s.published.Applied || !s.last.Applied || s.publishedName != "FIRST" {
		t.Fatal("first publication did not retain source/name/unknown-history invariants")
	}
	boldRefused(t, s, Event{Command: Bold})
	anchor := s.Source().Identity()
	s, observe = boldStartSave(t, s, "SECOND")
	s, write := boldCompleteIO(t, s, observe)
	if write == nil || write.Kind != WriteSnapshot {
		t.Fatal("no-edit Save As did not use the actual snapshot path")
	}
	s, next = boldCompleteIO(t, s, write)
	if next != nil || s.name != "SECOND" || s.publishedName != "SECOND" ||
		s.Source().Identity() != anchor || s.Source().Name() != "FIRST" || s.historyValid ||
		s.lastSave != NewNamePublished || !s.published.Applied || s.native.Revision() != before.native.Revision() {
		t.Fatal("no-edit publication changed authoritative first binding")
	}
	for _, name := range []string{"FIRST", "SECOND"} {
		stored, err := dir.Read(name)
		if err != nil || !bytes.Equal(stored.Export(), raw) {
			t.Fatalf("rooted %s readback differs: %v", name, err)
		}
		native, err := document.Parse(stored.Export())
		if err != nil || native.TokenCount() != 6 {
			t.Fatalf("actual native readback invalid: %v", err)
		}
	}
	question := boldKey(t, boldKey(t, s, F7), Escape)
	if question.mode != SaveName || !question.fromExit {
		t.Fatal("closed Save-on-exit route changed")
	}
	boldRefused(t, question, Event{Command: Enter})
	s = boldKey(t, question, F1)
	existing, existingObserve := boldStartSave(t, s, "SECOND")
	existing, next = boldCompleteIO(t, existing, existingObserve)
	if next != nil || existing.mode != ReplaceQuestion {
		t.Fatal("existing destination did not enter the inherited replacement question")
	}
	boldRefused(t, existing, Event{Command: Yes})
	if back := boldKey(t, existing, No); back.mode != SaveName || back.target != nil {
		t.Fatal("existing replacement No route changed")
	}
	second, err := dir.Read("SECOND")
	if err != nil || !bytes.Equal(second.Export(), raw) {
		t.Fatal("replacement refusal changed the rooted destination")
	}
	s = boldType(t, s, "E")
	if s.history.Revision() != before.history.Revision() {
		t.Fatal("post-publication Text reset retained history")
	}
	boldRefused(t, s, Event{Command: Bold})
}

func TestBoldActualFailedPublicationAndReadRetry(t *testing.T) {
	for _, failWrite := range []bool{true, false} {
		s, _, path := boldFixture(t)
		s = boldClosedSession(t, s)
		before := s
		s, i := boldStartSave(t, s, "FIRST")
		s, i = boldCompleteIO(t, s, i)
		file := filepath.Join(path, "FIRST")
		if failWrite {
			if err := os.WriteFile(file, []byte("foreign"), 0600); err != nil {
				t.Fatal(err)
			}
			s, i = boldCompleteIO(t, s, i)
			if i != nil || s.newPhase != NewUnpublished || s.lastSave != SaveFailed || s.historyValid {
				t.Fatal("actual failed New publication lost its inherited status")
			}
			raw, err := os.ReadFile(file)
			if err != nil || string(raw) != "foreign" {
				t.Fatal("failed save modified existing target")
			}
			s = boldType(t, s, "X")
			boldRefused(t, s, Event{Command: Bold})
		} else {
			s, i = boldCompleteIO(t, s, i)
			if i == nil || i.Kind != BindNewSource {
				t.Fatal("missing genuine BindNewSource")
			}
			late := boldExecute(t, i)
			s = boldKey(t, s, CancelOperation)
			if s.newPhase != PublishedUnbound {
				t.Fatal("cancelled binding did not preserve uncertainty")
			}
			s, next := boldApply(t, s, Event{Command: Complete, Result: &late})
			if next != nil || s.detached.Applied || s.detached.Result.Kind != BindNewSource {
				t.Fatal("actual late read did not detach")
			}
			boldRefused(t, s, Event{Command: Bold})
			s, i = boldApply(t, s, Event{Command: RetryFirstRead})
			if i == nil || i.Kind != BindNewSource {
				t.Fatal("read-only retry did not issue binding")
			}
			s, i = boldCompleteIO(t, s, i)
			if i != nil || s.newPhase != NewAnchored || s.source == nil {
				t.Fatal("actual read retry failed")
			}
		}
		if s.history.Revision() != before.history.Revision() {
			t.Fatal("save route repaired retained history")
		}
	}
}

func TestBoldDefensiveFences(t *testing.T) {
	s, dir, path := boldFixture(t)
	active := boldActiveSession(t, s)
	// Supplemental private states retain actual E active ownership but are
	// unreachable through the public key policy. They prove the extra fences.
	for _, tc := range []struct {
		mode    Mode
		command Command
	}{{SaveName, Enter}, {ReplaceQuestion, Yes}} {
		private := active
		private.mode = tc.mode
		private.draft = "FIRST"
		private.lastSave = SaveFailed
		event := Event{Command: tc.command}
		if _, ok := boldRefused(t, private, event).(*Refusal); !ok {
			t.Fatal("active filename guard did not issue a Session refusal")
		}
		next, i, err := private.reduce(event)
		boldAssertRefusal(t, private, next, i, err)
	}
	for _, kind := range []IntentKind{Observe, WriteSnapshot, PublishCandidate} {
		next, i, err := active.begin(kind, dir, "FIRST")
		boldAssertRefusal(t, active, next, i, err)
	}
	target, err := dir.Observe("FIRST")
	if err != nil {
		t.Fatal(err)
	}
	private := active
	private.target = target
	next, i, err := private.firstIntent(PublishNewBuffer, dir, "FIRST", nil)
	boldAssertRefusal(t, private, next, i, err)
	// Close is cursor-only, so the retained earlier active history has the
	// exact same native owner as the genuine subsequently issued Observe.
	closed := boldKey(t, active, Bold)
	waiting, observe := boldStartSave(t, closed, "FIRST")
	waiting.history = active.history
	result := boldExecute(t, observe)
	next, i, err = waiting.Reduce(Event{Command: Complete, Result: &result})
	if err == nil || i != nil || next.pending != nil || !next.last.Applied ||
		next.last.Result.Kind != Observe || next.sequence != waiting.sequence || !boldIsActive(next) {
		t.Fatal("defensive write fence swallowed genuine Observe completion or issued a write")
	}
	late, i := boldApply(t, next, Event{Command: Complete, Result: &result})
	if i != nil || late.detached.Applied || late.detached.Result.Operation != result.Operation || !boldIsActive(late) {
		t.Fatal("late completion did not use inherited detached receipt path")
	}
	boldNoFiles(t, path)
	// Supplemental sourced completion takes the generic write path.
	waiting, observe = boldStartSave(t, closed, "FIRST")
	waiting, publish := boldCompleteIO(t, waiting, observe)
	waiting, read := boldCompleteIO(t, waiting, publish)
	anchored, i := boldCompleteIO(t, waiting, read)
	if i != nil || anchored.newPhase != NewAnchored {
		t.Fatal("expected genuine first binding")
	}
	waiting, observe = boldStartSave(t, anchored, "SECOND")
	waiting.history = active.history
	result = boldExecute(t, observe)
	next, i, err = waiting.Reduce(Event{Command: Complete, Result: &result})
	if err == nil || i != nil || next.pending != nil || !next.last.Applied ||
		next.last.Result.Kind != Observe || next.sequence != waiting.sequence || !boldIsActive(next) {
		t.Fatal("defensive generic fence swallowed genuine sourced Observe or issued a write")
	}
	if _, err := os.Stat(filepath.Join(path, "SECOND")); !os.IsNotExist(err) {
		t.Fatal("defensive sourced completion wrote a file")
	}
}

func TestBoldUnavailableCohorts(t *testing.T) {
	s, dir, path := boldFixture(t)
	typeover := boldKey(t, s, Insert)
	home := boldKey(t, s, Home)
	selection := boldKey(t, boldKey(t, boldType(t, s, "A"), Reveal), Block)
	macro := boldKey(t, s, Macro)
	typed := boldType(t, s, "A")
	deleted := boldKey(t, boldKey(t, typed, Left), Delete)
	unknown := boldType(t, boldKey(t, boldKey(t, typed, Left), Insert), "X")
	unknown = boldKey(t, unknown, Insert)
	for _, session := range []Session{{}, typeover, home, selection, macro, deleted, unknown, boldKey(t, s, Retrieve)} {
		boldRefused(t, session, Event{Command: Bold})
	}
	if err := os.WriteFile(filepath.Join(path, "SOURCE"), boldNative(t, typed), 0600); err != nil {
		t.Fatal(err)
	}
	loading := boldType(t, boldKey(t, s, Retrieve), "SOURCE")
	loading, i := boldApply(t, loading, Event{Command: Enter})
	loaded, i := boldCompleteIO(t, loading, i)
	if i != nil || loaded.source == nil {
		t.Fatal("real loaded fixture failed")
	}
	boldRefused(t, loaded, Event{Command: Bold})
	boldRefused(t, boldKey(t, loaded, SwitchDocument), Event{Command: Bold})
	repeat, err := loaded.WithMacroRepeat(3)
	if err != nil {
		t.Fatal(err)
	}
	boldRefused(t, repeat, Event{Command: Bold})
	// Defensive ownership mismatch. Neither a foreign source nor a cursor
	// on the wrong gap can act on a genuine active E span.
	active := boldActiveSession(t, s)
	badCursor := active
	badCursor.cursor, _ = active.native.CursorAt(0)
	boldRefused(t, badCursor, Event{Command: Bold})
	boldRefused(t, badCursor, Event{Command: Text, Text: "Z"})
	badSource := active
	badSource.source, err = dir.Read("SOURCE")
	if err != nil {
		t.Fatal(err)
	}
	boldRefused(t, badSource, Event{Command: Bold})
	boldRefused(t, badSource, Event{Command: Text, Text: "Z"})
}

func TestBoldPresentationLimitAndAllocation(t *testing.T) {
	s, _, path := boldFixture(t)
	within := boldType(t, s, strings.Repeat("X", 4093))
	over := boldType(t, s, strings.Repeat("X", 4094))
	open := boldKey(t, within, Bold)
	boldRefused(t, open, Event{Command: Bold})
	boldRefused(t, open, Event{Command: Text, Text: "ab"})
	active := boldType(t, open, "R")
	closed := boldKey(t, active, Bold)
	if closed.native.TokenCount() != 4096 || boldIsActive(closed) {
		t.Fatal("recovery character did not reach the exact presentation owner bound")
	}
	boldRefused(t, over, Event{Command: Bold})
	for _, tc := range []struct {
		name    string
		s       Session
		refused bool
	}{
		{"begin", within, false}, {"close", active, false}, {"begin-owner-refusal", over, true},
	} {
		var peak uint64
		for range 8 {
			var before, after runtime.MemStats
			runtime.ReadMemStats(&before)
			_, i, err := tc.s.Reduce(Event{Command: Bold})
			runtime.ReadMemStats(&after)
			if (err != nil) != tc.refused || i != nil {
				t.Fatalf("%s returned %v", tc.name, err)
			}
			peak = max(peak, after.TotalAlloc-before.TotalAlloc)
		}
		if peak > 20<<20 {
			t.Fatalf("%s allocated %d", tc.name, peak)
		}
		t.Logf("%s peak=%d bound=%d samples=8", tc.name, peak, 20<<20)
	}
	boldNoFiles(t, path)
}

func TestBoldDefensiveUnboundReadRetry(t *testing.T) {
	s, dir, path := boldFixture(t)
	active := boldActiveSession(t, s)
	closed := boldKey(t, active, Bold)
	waiting, observe := boldStartSave(t, closed, "FIRST")
	waiting, publish := boldCompleteIO(t, waiting, observe)
	waiting, read := boldCompleteIO(t, waiting, publish)
	if read == nil || read.Kind != BindNewSource {
		t.Fatal("missing genuine post-publication read intent")
	}
	unbound := boldKey(t, waiting, CancelOperation)
	if unbound.newPhase != PublishedUnbound || unbound.historyValid || unbound.pending != nil {
		t.Fatal("expected genuine unbound read-retry state")
	}

	// Supplemental only: close changed the cursor but kept the exact native
	// revision, so the earlier immutable active history can still match.
	unbound.history = active.history
	if !boldIsActive(unbound) {
		t.Fatal("supplement did not retain active history on the real native owner")
	}
	retrying, i := boldApply(t, unbound, Event{Command: RetryFirstRead})
	if i == nil || i.Kind != BindNewSource || retrying.sequence != unbound.sequence+1 {
		t.Fatal("read-only retry was swallowed or became a write")
	}
	bound, next := boldCompleteIO(t, retrying, i)
	if next != nil || bound.newPhase != NewAnchored || bound.source == nil ||
		bound.history.Revision() != active.history.Revision() || bound.historyValid ||
		!bound.last.Applied || bound.last.Result.Kind != BindNewSource {
		t.Fatal("genuine retry receipt did not bind or changed retained history")
	}
	stored, err := dir.Read("FIRST")
	if err != nil || !bytes.Equal(stored.Export(), boldNative(t, closed)) {
		t.Fatal("verification retry changed the previously published bytes")
	}
	files, err := os.ReadDir(path)
	if err != nil || len(files) != 1 || files[0].Name() != "FIRST" {
		t.Fatal("read-only retry produced an unexpected filesystem effect")
	}
}
