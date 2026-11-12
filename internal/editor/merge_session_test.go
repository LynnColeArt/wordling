package editor_test

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
)

func mergeWorkspace(t *testing.T) (string, editor.Session) {
	t.Helper()
	path := t.TempDir()
	for _, name := range []string{"PRIMARY.WP5", "SECOND.WP5"} {
		raw := liveReadBytes(t, filepath.Join("../../docs/research/reference-runs/2026-10-29-extended-04/CMD51-134", name))
		if err := os.WriteFile(filepath.Join(path, name), raw, 0600); err != nil {
			t.Fatal(err)
		}
	}
	_, _, s := liveWorkspace(t, path)
	return path, s
}

func openMergePrimary(t *testing.T, s editor.Session) editor.Session {
	t.Helper()
	return liveText(t, liveKeys(t, s, editor.MergeCtrlF9), "1")
}

func requestMergeName(t *testing.T, s editor.Session, name string, kind editor.IntentKind) (editor.Session, *editor.Intent) {
	t.Helper()
	s, request := liveEvent(t, liveText(t, s, name), editor.Event{Command: editor.Enter})
	if request == nil || request.Kind != kind {
		t.Fatalf("expected %s request", kind)
	}
	return s, request
}

func TestWorkspaceMergeRetainsAuthenticatedPrimaryAtCaret(t *testing.T) {
	path, s := mergeWorkspace(t)
	s = liveText(t, s.WithFastSaveDisabled(true), "BEFOREAFTER")
	s = liveKeys(t, s, editor.Left, editor.Left, editor.Left, editor.Left, editor.Left)
	s, request := requestMergeName(t, openMergePrimary(t, s), "PRIMARY.WP5", editor.ReadMergePrimary)
	s, _ = liveDispatch(t, s, request)
	if s.Snapshot().Mode != editor.MergeSecondaryName {
		t.Fatalf("primary did not settle: %+v", s.Snapshot())
	}
	primary := filepath.Join(path, "PRIMARY.WP5")
	if err := os.WriteFile(primary, []byte("replacement outside the session"), 0600); err != nil {
		t.Fatal(err)
	}
	s, request = requestMergeName(t, s, "SECOND.WP5", editor.ReadMergeSecondary)
	s, _ = liveDispatch(t, s, request)
	if s.Snapshot().Mode != editor.Editing || !s.Snapshot().Dirty {
		t.Fatalf("merge did not settle: %+v", s.Snapshot())
	}
	doc := s.Document()
	raw, _ := doc.Export()
	caret, _ := doc.CursorAt(s.Snapshot().Gap)
	at, _ := caret.Offset()
	if !bytes.HasSuffix(raw[:at], []byte{0xd4, 0x0c}) || string(raw[at:]) != "AFTER" {
		t.Fatalf("merge caret did not stop before suffix: %d", at)
	}
	if !bytes.Contains(raw, []byte("BEFOREHello Alice")) || !bytes.Contains(raw, []byte("Hello Bob")) {
		t.Fatal("pinned primary or destination text was lost")
	}
}

func TestWorkspaceMergeF1DetachesPendingRead(t *testing.T) {
	_, s := mergeWorkspace(t)
	s = liveText(t, s, "KEEP")
	revision := s.Document().Revision()
	s, request := requestMergeName(t, openMergePrimary(t, s), "PRIMARY.WP5", editor.ReadMergePrimary)
	s = liveKeys(t, s, editor.F1)
	s, _ = liveDispatch(t, s, request)
	if s.Snapshot().Mode != editor.Editing || s.Document().Revision() != revision {
		t.Fatalf("cancelled merge returned to a source or changed the buffer: %+v", s.Snapshot())
	}
	if got := s.Snapshot().Detached; got.Applied || got.Result.Kind != editor.ReadMergePrimary {
		t.Fatalf("missing detached merge receipt: %+v", got)
	}
}

func TestWorkspaceMergeDoesNotEnableStructuralSourceEdits(t *testing.T) {
	_, s := mergeWorkspace(t)
	s = liveText(t, liveKeys(t, s, editor.Retrieve), "PRIMARY.WP5")
	s, request := liveEvent(t, s, editor.Event{Command: editor.Enter})
	s, _ = liveDispatch(t, s, request)
	s = liveText(t, s, "X")
	if !s.Snapshot().Dirty || s.Document().CheckMutation() == nil {
		t.Fatal("literal edit should leave structural mutation restricted")
	}
	if _, _, err := s.Reduce(editor.Event{Command: editor.Enter}); err == nil {
		t.Fatal("accepted structural source edit")
	}
	if _, err := document.NewHistory(s.Document()); err == nil {
		t.Fatal("invented ordinary undo history for a merge source")
	}
}

func TestWorkspaceMergeOriginalPlainAndConditionalResults(t *testing.T) {
	for _, id := range []string{"207", "209"} {
		t.Run(id, func(t *testing.T) {
			fixtures := filepath.Join("../../docs/research/reference-runs/2026-10-29-advanced-03", "CMD51-"+id)
			path := t.TempDir()
			for _, name := range []string{"PRIMARY.WP5", "SECOND.WP5"} {
				if err := os.WriteFile(filepath.Join(path, name), liveReadBytes(t, filepath.Join(fixtures, name)), 0600); err != nil {
					t.Fatal(err)
				}
			}
			_, _, s := liveWorkspace(t, path)
			s, request := requestMergeName(t, openMergePrimary(t, s), "PRIMARY.WP5", editor.ReadMergePrimary)
			s, _ = liveDispatch(t, s, request)
			s, request = requestMergeName(t, s, "SECOND.WP5", editor.ReadMergeSecondary)
			s, _ = liveDispatch(t, s, request)
			if s.Snapshot().Mode != editor.Editing || !s.Snapshot().Dirty {
				t.Fatalf("original merge failed: %+v", s.Snapshot())
			}
			liveSave(t, liveKeys(t, s, editor.Save), "MERGED.WP5", false)
			got := liveReadBytes(t, filepath.Join(path, "MERGED.WP5"))
			want := liveReadBytes(t, filepath.Join(fixtures, "MERGED.WP5"))
			if !bytes.Equal(got, want) {
				t.Fatalf("published merge differs from DOS: %d versus %d bytes", len(got), len(want))
			}
		})
	}
}
