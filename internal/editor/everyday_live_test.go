package editor_test

import (
	"bytes"
	"errors"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
)

func liveWorkspace(t *testing.T, path string) (*storage.Workspace, *storage.WorkspaceDirectory, editor.Session) {
	t.Helper()
	w, err := storage.OpenWorkspace(path)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = w.Close() })
	d, err := w.Root()
	if err != nil {
		t.Fatal(err)
	}
	s, err := editor.New(editor.Config{Workspace: w, OriginalBackup: storage.OriginalBackupOn})
	if err != nil {
		t.Fatal(err)
	}
	return w, d, s
}

func liveEvent(t *testing.T, s editor.Session, e editor.Event) (editor.Session, *editor.Intent) {
	t.Helper()
	next, i, err := s.Reduce(e)
	if err != nil {
		t.Fatalf("command %v in %s: %v", e.Command, s.Snapshot().Mode, err)
	}
	return next, i
}

func liveKeys(t *testing.T, s editor.Session, commands ...editor.Command) editor.Session {
	t.Helper()
	for _, c := range commands {
		var i *editor.Intent
		s, i = liveEvent(t, s, editor.Event{Command: c})
		if i != nil {
			t.Fatalf("unexpected intent %s", i.Kind)
		}
	}
	return s
}

func liveText(t *testing.T, s editor.Session, text string) editor.Session {
	t.Helper()
	next, i := liveEvent(t, s, editor.Event{Command: editor.Text, Text: text})
	if i != nil {
		t.Fatalf("unexpected text intent %s", i.Kind)
	}
	return next
}

func liveDispatch(t *testing.T, s editor.Session, i *editor.Intent) (editor.Session, *editor.Intent) {
	t.Helper()
	if i == nil {
		t.Fatal("no live request")
	}
	r := editor.ExecuteEveryday(i)
	return liveEvent(t, s, editor.Event{Command: editor.Complete, Result: &r})
}

func liveSave(t *testing.T, s editor.Session, name string, replace bool) editor.Session {
	t.Helper()
	if name != "" {
		s = liveText(t, s, name)
	}
	s, i := liveEvent(t, s, editor.Event{Command: editor.Enter})
	if i == nil || i.Kind != editor.ObserveWorkspace {
		t.Fatal("missing workspace observe")
	}
	s, i = liveDispatch(t, s, i)
	if replace {
		if i != nil || s.Snapshot().Mode != editor.ReplaceQuestion {
			t.Fatalf("expected overwrite prompt: %v %v", s.Snapshot().Mode, i)
		}
		s, i = liveEvent(t, s, editor.Event{Command: editor.Yes})
	}
	if i == nil || i.Kind != editor.PublishEveryday {
		t.Fatalf("missing workspace save in %v: %v", s.Snapshot().Mode, i)
	}
	s, i = liveDispatch(t, s, i)
	if i != nil || s.Snapshot().Last.Result.Err != nil || s.Snapshot().Dirty {
		t.Fatalf("publication did not bind: %+v", s.Snapshot())
	}
	return s
}

func liveReadBytes(t *testing.T, path string) []byte {
	t.Helper()
	b, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	return b
}

func liveBody(t *testing.T, s editor.Session) []byte {
	t.Helper()
	body, err := s.Document().Export()
	if err != nil {
		t.Fatal(err)
	}
	start := int(body[4]) | int(body[5])<<8 | int(body[6])<<16 | int(body[7])<<24
	return body[start:]
}

func TestLiveWorkspaceSavesBackupsAndDoc2Continuation(t *testing.T) {
	path := t.TempDir()
	if err := os.Mkdir(filepath.Join(path, "letters"), 0700); err != nil {
		t.Fatal(err)
	}
	_, _, s := liveWorkspace(t, path)
	s = liveText(t, s, "FIRST")
	s = liveKeys(t, s, editor.Save)
	s = liveSave(t, s, `C:\LETTERS\DOC.WP`, false)
	docPath := filepath.Join(path, "letters", "DOC.WP")
	before := liveReadBytes(t, docPath)
	s = liveText(t, s, " CHANGE")
	s = liveKeys(t, s, editor.F7, editor.Yes)
	s = liveSave(t, s, "", true)
	if s.Snapshot().Mode != editor.ExitQuestion || !bytes.Equal(liveReadBytes(t, filepath.Join(path, "letters", "DOC.BK!")), before) {
		t.Fatal("edited F7 save did not rotate backup and continue to exit")
	}
	s = liveKeys(t, s, editor.F1, editor.SwitchDocument)
	if s.Snapshot().Screen != 2 || s.Document().TokenCount() != 0 {
		t.Fatal("Doc 2 did not start independently")
	}
	s = liveText(t, s, "SECOND")
	s = liveKeys(t, s, editor.F7, editor.Yes)
	s = liveSave(t, s, "DOC2.WP", false)
	if s.Snapshot().Mode != editor.ExitDocQuestion {
		t.Fatalf("new F7 save did not continue to the screen exit: %v", s.Snapshot().Mode)
	}
	s = liveKeys(t, s, editor.Yes)
	if s.Snapshot().Screen != 1 || string(liveBody(t, s)) != "FIRST CHANGE" || s.Source().Name() != "DOC.WP" {
		t.Fatal("closing Doc 2 did not restore Doc 1 source and content")
	}
	s = liveKeys(t, s, editor.Save)
	s = liveSave(t, s, "COPY.WP", false)
	if s.Source().Name() != "COPY.WP" || !bytes.Equal(liveReadBytes(t, docPath), liveReadBytes(t, filepath.Join(path, "letters", "COPY.WP"))) {
		t.Fatal("Save As did not preserve exact native bytes")
	}
}

func TestLiveWorkspaceNestedSelectionAndOccupiedRetrieve(t *testing.T) {
	path := t.TempDir()
	if err := os.Mkdir(filepath.Join(path, "letters"), 0700); err != nil {
		t.Fatal(err)
	}
	w, root, author := liveWorkspace(t, path)
	author = liveText(t, author, "FILE")
	author = liveKeys(t, author, editor.Save)
	author = liveSave(t, author, `C:\LETTERS\A.WP`, false)
	child, err := root.Navigate("letters")
	if err != nil {
		t.Fatal(err)
	}
	l, err := child.List("*.WP")
	if err != nil {
		t.Fatal(err)
	}
	selected, err := l.Select(l.Find("A.WP"))
	if err != nil {
		t.Fatal(err)
	}
	s, err := editor.New(editor.Config{Workspace: w})
	if err != nil {
		t.Fatal(err)
	}
	s, i := liveEvent(t, s, editor.Event{Command: editor.RetrieveSelection, Selection: selected})
	if !editor.EverydayIntentOwnedBy(i, w) {
		t.Fatal("selection request not authenticated")
	}
	s, _ = liveDispatch(t, s, i)
	if string(liveBody(t, s)) != "FILE" || s.Source().Name() != "A.WP" || s.Snapshot().Dirty {
		t.Fatalf("bad blank retrieval: %+v", s.Snapshot())
	}
	s = liveKeys(t, s, editor.End)
	prior := s.Source().Identity()
	s, i = liveEvent(t, s, editor.Event{Command: editor.RetrieveSelection, Selection: selected})
	if i != nil || s.Snapshot().Mode != editor.RetrieveInsertQuestion {
		t.Fatal("occupied retrieve acquired before confirmation")
	}
	s = liveKeys(t, s, editor.Enter)
	if string(liveBody(t, s)) != "FILE" || s.Snapshot().Dirty {
		t.Fatal("decline changed current document")
	}
	s, _ = liveEvent(t, s, editor.Event{Command: editor.RetrieveSelection, Selection: selected})
	s, i = liveEvent(t, s, editor.Event{Command: editor.Yes})
	s, _ = liveDispatch(t, s, i)
	if string(liveBody(t, s)) != "FILEFILE" || !s.Snapshot().Dirty || s.Source().Identity() != prior {
		t.Fatalf("occupied retrieval did not insert at caret with receiver identity: %+v", s.Snapshot())
	}
}

func TestLiveWorkspaceRejectsForgedForeignAndStaleCompletions(t *testing.T) {
	path := t.TempDir()
	w, _, s := liveWorkspace(t, path)
	foreign, _, other := liveWorkspace(t, path)
	s = liveKeys(t, liveText(t, s, "FIRST"), editor.Save)
	other = liveKeys(t, liveText(t, other, "OTHER"), editor.Save)
	s = liveText(t, s, "A.WP")
	other = liveText(t, other, "A.WP")
	s, i := liveEvent(t, s, editor.Event{Command: editor.Enter})
	_, j := liveEvent(t, other, editor.Event{Command: editor.Enter})
	if !editor.EverydayIntentOwnedBy(i, w) || editor.EverydayIntentOwnedBy(i, foreign) {
		t.Fatal("same path does not imply same workspace authority")
	}
	forged := editor.Result{Kind: i.Kind, Operation: i.Operation, Revision: i.Revision}
	if _, _, err := s.Reduce(editor.Event{Command: editor.Complete, Result: &forged}); err == nil {
		t.Fatal("forged completion accepted")
	}
	wrong := editor.ExecuteEveryday(j)
	s, _ = liveEvent(t, s, editor.Event{Command: editor.Complete, Result: &wrong})
	if s.Snapshot().Mode != editor.Waiting {
		t.Fatal("foreign genuine result consumed the request")
	}
	s, i = liveDispatch(t, s, i)
	s = liveKeys(t, s, editor.CancelOperation)
	late := editor.ExecuteEveryday(i)
	s, _ = liveEvent(t, s, editor.Event{Command: editor.Complete, Result: &late})
	if !s.Snapshot().Dirty || s.Source() != nil || !s.Snapshot().Detached.DestinationMayExist {
		t.Fatal("late save rebound the active document or hid its filesystem effect")
	}
}

func TestLiveWorkspaceLayoutUnderlineAndSearch(t *testing.T) {
	_, _, s := liveWorkspace(t, t.TempDir())
	s = liveText(t, s, strings.Repeat("x", 63))
	s = liveKeys(t, s, editor.Tab)
	s = liveText(t, s, "y")
	if !bytes.Contains(liveBody(t, s), []byte{0xc1, 2, 0x28, 0x23, 0x28, 0x23, 75, 0, 0xc1, 0x90, 'y'}) {
		t.Fatalf("Tab-edge native bytes: %x", liveBody(t, s))
	}
	s = liveKeys(t, s, editor.Enter)
	s = liveText(t, s, "short")
	s = liveKeys(t, s, editor.Enter, editor.Underline)
	s = liveText(t, s, "find")
	s = liveKeys(t, s, editor.Underline, editor.Home, editor.Home, editor.Up, editor.End)
	p, err := s.EverydayPosition()
	if err != nil || p.Page != 1 || p.Line != 1 || p.Pos != 66 {
		t.Fatalf("physical first line end: %+v %v", p, err)
	}
	s = liveKeys(t, s, editor.Down, editor.Down, editor.Down)
	p, err = s.EverydayPosition()
	if err != nil || p.Line != 4 || p.Pos != 5 {
		t.Fatalf("desired-column navigation: %+v %v", p, err)
	}
	s = liveKeys(t, s, editor.Home, editor.Home, editor.Up, editor.SearchF2, editor.Underline)
	if got := s.Snapshot().Prompt; !strings.HasSuffix(got, "[UND]") {
		t.Fatalf("underline search prompt %q", got)
	}
	before := liveBody(t, s)
	s = liveKeys(t, s, editor.SearchF2)
	token, err := s.Document().Token(s.Snapshot().Gap - 1)
	if err != nil || token.Kind != document.UnderlineOn || !bytes.Equal(before, liveBody(t, s)) {
		t.Fatalf("format search did not find exact native owner: %v %v", token.Kind, err)
	}
}

func TestLiveWorkspaceHostRefusalSettlesAuthenticatedWait(t *testing.T) {
	_, _, s := liveWorkspace(t, t.TempDir())
	s = liveKeys(t, liveText(t, s, "FIRST"), editor.Save)
	s = liveText(t, s, "NO.WP")
	s, i := liveEvent(t, s, editor.Event{Command: editor.Enter})
	refusal := errors.New("host refused before I/O")
	r := editor.RefuseEveryday(i, refusal)
	s, _ = liveEvent(t, s, editor.Event{Command: editor.Complete, Result: &r})
	if s.Snapshot().Mode != editor.SaveName || !errors.Is(s.Snapshot().Last.Result.Err, refusal) || !s.Snapshot().Dirty {
		t.Fatal("refusal did not return to the save prompt without changing data")
	}
}

func TestLiveWorkspaceBackwardSearchRepeatAndFilenameDefaults(t *testing.T) {
	path := t.TempDir()
	w, _, s := liveWorkspace(t, path)
	s = liveText(t, s, "alpha beta alpha")
	s = liveKeys(t, s, editor.F7, editor.Enter)
	if s.Snapshot().Mode != editor.SaveName {
		t.Fatal("save-on-exit Enter did not choose Yes")
	}
	s = liveSave(t, s, "FIRST.WP", false)
	s = liveKeys(t, s, editor.F1, editor.SearchBackF2)
	s = liveText(t, s, "alpha")
	s = liveKeys(t, s, editor.SearchBackF2)
	if s.Snapshot().Gap != 5 {
		t.Fatalf("first backward search must skip the match ending at the starting caret: %d", s.Snapshot().Gap)
	}
	s = liveKeys(t, s, editor.SearchBackF2, editor.SearchBackF2)
	if s.Snapshot().Gap != 5 || s.Snapshot().Notice != "NOT FOUND" {
		t.Fatalf("backward repeat with no earlier match must retain the caret: %+v", s.Snapshot())
	}

	fresh, err := editor.New(editor.Config{Workspace: w})
	if err != nil {
		t.Fatal(err)
	}
	fresh = liveKeys(t, fresh, editor.Retrieve)
	fresh = liveText(t, fresh, `C:\FIRST.WP`)
	fresh, i := liveEvent(t, fresh, editor.Event{Command: editor.Enter})
	fresh, _ = liveDispatch(t, fresh, i)
	if !bytes.Equal(liveBody(t, fresh), []byte("alpha beta alpha")) {
		t.Fatal("typed workspace Retrieve did not acquire exact file")
	}
	fresh = liveText(t, fresh, "edit ")
	fresh = liveKeys(t, fresh, editor.Save)
	fresh, i = liveEvent(t, fresh, editor.Event{Command: editor.Enter})
	fresh, _ = liveDispatch(t, fresh, i)
	fresh = liveKeys(t, fresh, editor.Enter)
	if fresh.Snapshot().Mode != editor.SaveName || !fresh.Snapshot().Dirty ||
		string(liveBody(t, fresh)) != "edit alpha beta alpha" {
		t.Fatal("default No did not retain unsaved editing")
	}
	fresh = liveKeys(t, fresh, editor.F1)
	if fresh.Snapshot().Mode != editor.Editing {
		t.Fatal("F1 did not cancel save naming")
	}
}

func TestLiveWorkspaceStaleTargetLeavesUnsavedDocumentAndBackup(t *testing.T) {
	path := t.TempDir()
	_, _, s := liveWorkspace(t, path)
	s = liveKeys(t, liveText(t, s, "original"), editor.Save)
	s = liveSave(t, s, "A.WP", false)
	target := filepath.Join(path, "A.WP")
	backup := filepath.Join(path, "A.BK!")
	prior := liveReadBytes(t, target)
	if err := os.WriteFile(backup, []byte("unchanged backup"), 0600); err != nil {
		t.Fatal(err)
	}
	s = liveKeys(t, liveText(t, s, " edited"), editor.F7, editor.Yes)
	s, i := liveEvent(t, s, editor.Event{Command: editor.Enter})
	s, _ = liveDispatch(t, s, i)
	if s.Snapshot().Mode != editor.ReplaceQuestion {
		t.Fatal("missing overwrite question")
	}
	external := append(bytes.Clone(prior), []byte(" external")...)
	if err := os.WriteFile(target, external, 0600); err != nil {
		t.Fatal(err)
	}
	s, i = liveEvent(t, s, editor.Event{Command: editor.Yes})
	s, _ = liveDispatch(t, s, i)
	if s.Snapshot().Mode != editor.SaveName || !s.Snapshot().Dirty ||
		s.Snapshot().SaveState != editor.SaveFailed || s.Snapshot().Last.Result.Err == nil ||
		string(liveBody(t, s)) != "original edited" {
		t.Fatalf("stale publication changed the session or continued exit: %+v", s.Snapshot())
	}
	if !bytes.Equal(liveReadBytes(t, target), external) || string(liveReadBytes(t, backup)) != "unchanged backup" {
		t.Fatal("stale target refusal changed target or backup bytes")
	}
}

func TestLiveWorkspaceLoadedBackspaceAndMotionHistory(t *testing.T) {
	path := t.TempDir()
	w, _, author := liveWorkspace(t, path)
	author = liveText(t, author, "ABC")
	author = liveKeys(t, author, editor.Enter)
	author = liveText(t, author, "DEF")
	author = liveKeys(t, author, editor.Save)
	_ = liveSave(t, author, "BACK.WP", false)

	s, err := editor.New(editor.Config{Workspace: w})
	if err != nil {
		t.Fatal(err)
	}
	s = liveKeys(t, s, editor.Retrieve)
	s = liveText(t, s, "BACK.WP")
	s, i := liveEvent(t, s, editor.Event{Command: editor.Enter})
	s, _ = liveDispatch(t, s, i)
	s = liveKeys(t, s, editor.Delete, editor.Home, editor.Home, editor.Down,
		editor.Backspace, editor.Up, editor.Down, editor.Backspace)
	if string(liveBody(t, s)) != "BC\nD" || !s.Snapshot().HistoryQualified {
		t.Fatal("loaded text or history did not survive ordinary Backspace")
	}
	for index, want := range []string{"E", "F", "A"} {
		entry, err := s.History().Entry(index)
		if err != nil || string(entry.Native) != want {
			t.Fatalf("history %d: %q, %v, want %q", index, entry.Native, err, want)
		}
	}
	s = liveKeys(t, s, editor.Home, editor.Home, editor.Up, editor.Down, editor.Backspace)
	if string(liveBody(t, s)) != "BCD" {
		t.Fatal("loaded Backspace did not join the paragraphs")
	}
	s = liveKeys(t, s, editor.F1, editor.Restore)
	if string(liveBody(t, s)) != "BC\nD" {
		t.Fatal("Undelete did not restore the native hard return")
	}
}

func TestLiveWorkspaceBackwardBlockDefaultsAndUndelete(t *testing.T) {
	_, _, s := liveWorkspace(t, t.TempDir())
	s = liveKeys(t, liveText(t, s, "ABC"), editor.Block, editor.Left)
	if x := s.Snapshot(); x.Gap != 3 || x.SelectionStart != 3 || x.SelectionEnd != 3 {
		t.Fatal("first Left at EOF changed the selection before the original does")
	}
	s = liveKeys(t, s, editor.Left, editor.Left, editor.Delete)
	if x := s.Snapshot(); x.Mode != editor.DeleteQuestion || x.Prompt != "Delete Block? No (Yes)" ||
		x.SelectionStart != 3 || x.SelectionEnd != 1 {
		t.Fatalf("backward block confirmation: %+v", x)
	}
	s = liveKeys(t, s, editor.Enter)
	if !s.Snapshot().Selection || string(liveBody(t, s)) != "ABC" {
		t.Fatal("default No did not preserve the active block")
	}
	s = liveKeys(t, s, editor.Delete, editor.Yes)
	if s.Snapshot().Selection || string(liveBody(t, s)) != "A" {
		t.Fatal("confirmed backward block did not delete the exact native span")
	}
	s = liveKeys(t, s, editor.F1, editor.Restore)
	if string(liveBody(t, s)) != "ABC" {
		t.Fatal("block Undelete did not restore original bytes")
	}
}

func TestLiveWorkspaceOverlappingAttributesAndNativeTabRefresh(t *testing.T) {
	_, _, s := liveWorkspace(t, t.TempDir())
	s = liveText(t, s, "X")
	s = liveKeys(t, s, editor.Backspace, editor.Bold)
	s = liveText(t, s, "B")
	s = liveKeys(t, s, editor.Underline)
	s = liveText(t, s, "C")
	s = liveKeys(t, s, editor.Bold)
	s = liveText(t, s, "D")
	s = liveKeys(t, s, editor.Underline)
	want := []byte{0xc3, 0x0c, 0xc3, 'B', 0xc3, 0x0e, 0xc3, 'C',
		0xc4, 0x0c, 0xc4, 'D', 0xc4, 0x0e, 0xc4}
	if !bytes.Equal(liveBody(t, s), want) {
		t.Fatalf("overlapping format bytes: %x", liveBody(t, s))
	}
	entry, err := s.History().Entry(0)
	if err != nil || string(entry.Native) != "X" || !s.Snapshot().HistoryQualified {
		t.Fatalf("formatting discarded earlier Undelete: %q, %v", entry.Native, err)
	}

	_, _, tabbed := liveWorkspace(t, t.TempDir())
	tabbed = liveKeys(t, tabbed, editor.Tab)
	tabbed = liveText(t, tabbed, "ABC")
	tabbed = liveKeys(t, tabbed, editor.Home, editor.Home, editor.Up)
	tabbed = liveText(t, tabbed, "XXXXXX")
	want = append([]byte("XXXXXX"), 0xc1, 2, 0x60, 0x09, 0x60, 0x09, 0x14, 0, 0xc1)
	want = append(want, 'A', 'B', 'C')
	if !bytes.Equal(liveBody(t, tabbed), want) {
		t.Fatalf("original TABTWO live cache: %x", liveBody(t, tabbed))
	}
}

func TestLiveWorkspaceTrailingDeletableWrapBackspace(t *testing.T) {
	_, _, s := liveWorkspace(t, t.TempDir())
	line := strings.Repeat("X", 64)
	s = liveText(t, s, line+"YZ")
	if got := liveBody(t, s); !bytes.Equal(got, append([]byte(line+"Y"), 0x90, 'Z')) {
		t.Fatalf("initial native wrap: %x", got)
	}
	s = liveKeys(t, s, editor.Backspace)
	if got := liveBody(t, s); !bytes.Equal(got, append([]byte(line+"Y"), 0x90)) {
		t.Fatalf("first Backspace must leave DSRt: %x", got)
	}
	if p, err := s.EverydayPosition(); err != nil || p.Line != 2 || p.Pos != 1 {
		t.Fatalf("trailing DSRt position: %+v, %v", p, err)
	}
	s = liveKeys(t, s, editor.Backspace)
	if got := liveBody(t, s); string(got) != line+"Y" {
		t.Fatalf("second Backspace must remove only DSRt: %x", got)
	}
	if p, err := s.EverydayPosition(); err != nil || p.Line != 1 || p.Pos != 66 {
		t.Fatalf("after DSRt position: %+v, %v", p, err)
	}
	s = liveKeys(t, s, editor.Backspace)
	if got := liveBody(t, s); string(got) != line {
		t.Fatalf("third Backspace removes preceding glyph: %x", got)
	}
	entry, err := s.History().Entry(0)
	if err != nil || string(entry.Native) != "YZ" {
		t.Fatalf("derived boundary entered history: %q, %v", entry.Native, err)
	}
}
