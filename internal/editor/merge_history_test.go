package editor_test

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/editor"
)

func TestWorkspaceReadOnlyScreenParksAuthenticatedMergeHistory(t *testing.T) {
	path, s := mergeWorkspace(t)
	file := filepath.Join(path, "READONLY.WP")
	original := liveReadBytes(t, "../../docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5")
	// Append one framed native owner outside the editing admission. The
	// workspace may display this file but may not use it as an Undo receiver.
	readOnly := append(bytes.Clone(original), 0xa9)
	if err := os.WriteFile(file, readOnly, 0600); err != nil {
		t.Fatal(err)
	}
	retrieve := func(s editor.Session, name string) editor.Session {
		s = liveText(t, liveKeys(t, s, editor.Retrieve), name)
		s, request := liveEvent(t, s, editor.Event{Command: editor.Enter})
		s, _ = liveDispatch(t, s, request)
		return s
	}
	s = retrieve(s, "PRIMARY.WP5")
	s = liveKeys(t, s, editor.Reveal, editor.Right, editor.Right, editor.Right,
		editor.Right, editor.Right, editor.Right, editor.Delete, editor.SwitchDocument)
	s = retrieve(s, "READONLY.WP")
	if s.Snapshot().HistoryQualified {
		t.Fatal("read-only screen received mutation history")
	}
	if _, _, err := s.Reduce(editor.Event{Command: editor.F1}); err == nil {
		t.Fatal("read-only target accepted Undelete")
	}
	if raw, err := s.Document().Export(); err != nil || !bytes.Equal(raw, readOnly) {
		t.Fatal("read-only target changed")
	}
	s = liveKeys(t, s, editor.F7, editor.No, editor.Yes)
	s = liveKeys(t, s, editor.F1)
	if s.Snapshot().Mode != editor.HistoryPreview {
		t.Fatal("the authenticated ring did not return from the read-only screen")
	}
}
