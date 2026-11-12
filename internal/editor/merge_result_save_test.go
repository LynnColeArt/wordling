package editor_test

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/editor"
)

func startOriginalMergeResult(t *testing.T, s editor.Session) editor.Session {
	t.Helper()
	s, request := requestMergeName(t, openMergePrimary(t, s), "PRIMARY.WP5", editor.ReadMergePrimary)
	s, _ = liveDispatch(t, s, request)
	s, request = requestMergeName(t, s, "SECOND.WP5", editor.ReadMergeSecondary)
	s, _ = liveDispatch(t, s, request)
	if s.Snapshot().Mode != editor.Editing || !s.Snapshot().Dirty {
		t.Fatalf("merge did not settle: %+v", s.Snapshot())
	}
	return s
}

func compareOriginalMergeResult(t *testing.T, path, name string, s editor.Session) editor.Session {
	t.Helper()
	s = liveSave(t, liveKeys(t, s, editor.Save), name, false)
	got := liveReadBytes(t, filepath.Join(path, name))
	want := liveReadBytes(t, filepath.Join("testdata/merge_result_save", name))
	if !bytes.Equal(got, want) {
		first := 0
		for first < len(got) && first < len(want) && got[first] == want[first] {
			first++
		}
		t.Errorf("%s differs from original at byte %d (%d versus %d bytes)", name, first, len(got), len(want))
	}
	return s
}

func TestWorkspaceSaveEditedMergeResultMatchesDOS(t *testing.T) {
	for _, setting := range []struct {
		name, prefix string
		disabled     bool
	}{{"yes", "Y", false}, {"no", "N", true}} {
		t.Run(setting.name, func(t *testing.T) {
			path, s := mergeWorkspace(t)
			s = startOriginalMergeResult(t, s.WithFastSaveDisabled(setting.disabled))
			top := func(s editor.Session) editor.Session {
				return liveKeys(t, s, editor.Home, editor.Home, editor.Up)
			}
			compare := func(s editor.Session, suffix string) editor.Session {
				t.Helper()
				return compareOriginalMergeResult(t, path, setting.prefix+suffix+".WP5", s)
			}
			s = compare(liveText(t, top(s), "EDIT "), "FIRST")
			s = compare(liveText(t, s, "MORE "), "AGAIN")
			s = liveKeys(t, s, editor.SwitchDocument)
			s, request := liveEvent(t, liveText(t, liveKeys(t, s, editor.Retrieve), setting.prefix+"FIRST.WP5"), editor.Event{Command: editor.Enter})
			s, _ = liveDispatch(t, s, request)
			s = compare(liveText(t, top(s), "OPEN "), "OPEN")
			compare(liveText(t, s, "NEXT "), "NEXT")
		})
	}
}

func TestWorkspaceEditedMergeKeepsPurgedIndexAfterToggle(t *testing.T) {
	for _, first := range []string{"N", "Y"} {
		t.Run(first, func(t *testing.T) {
			path, s := mergeWorkspace(t)
			s = startOriginalMergeResult(t, s.WithFastSaveDisabled(first == "N"))
			s = liveText(t, liveKeys(t, s, editor.Home, editor.Home, editor.Up), "EDIT ")
			s = compareOriginalMergeResult(t, path, first+"FIRST.WP5", s)
			s = liveText(t, s.WithFastSaveDisabled(first == "Y"), "OTHER ")
			s = compareOriginalMergeResult(t, path, first+"OTHER.WP5", s)
			if first == "Y" {
				s = liveKeys(t, s.WithFastSaveDisabled(false), editor.Home, editor.Home, editor.Up)
				for range 5 {
					s = liveKeys(t, s, editor.Right)
				}
				compareOriginalMergeResult(t, path, "YBACK.WP5", liveText(t, s, "BACK "))
			}
		})
	}
}

func TestWorkspaceLoadedPlainDocumentKeepsCompactOrderAfterToggle(t *testing.T) {
	path := t.TempDir()
	_, _, s := liveWorkspace(t, path)
	s = s.WithFastSaveDisabled(true)
	source := liveReadBytes(t, "../document/testdata/fast_save_yes/SECOND.WP")
	if err := os.WriteFile(filepath.Join(path, "INPUT.WP"), source, 0600); err != nil {
		t.Fatal(err)
	}
	s, request := liveEvent(t, liveText(t, liveKeys(t, s, editor.Retrieve), "INPUT.WP"), editor.Event{Command: editor.Enter})
	s, _ = liveDispatch(t, s, request)
	s = liveText(t, s, "EDIT ")
	s = liveSave(t, liveKeys(t, s, editor.Save), "PLAIN.WP5", false)
	s = liveKeys(t, s.WithFastSaveDisabled(false), editor.Home, editor.Home, editor.Up)
	s = liveText(t, s, "BACK ")
	liveSave(t, liveKeys(t, s, editor.Save), "BACK.WP5", false)
	for _, name := range []string{"PLAIN.WP5", "BACK.WP5"} {
		got := liveReadBytes(t, filepath.Join(path, name))
		want := liveReadBytes(t, filepath.Join("../../docs/research/continuation/edited-merge-result-save/loaded-no", name))
		if !bytes.Equal(got, want) {
			t.Errorf("%s publication differs from original", name)
		}
	}
	if !bytes.Equal(liveReadBytes(t, filepath.Join(path, "INPUT.WP")), source) {
		t.Fatal("loaded save changed its source")
	}
}
