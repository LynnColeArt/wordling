package editor_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/editor"
	"os"
	"reflect"
	"testing"
)

// Public semantic commands retain their original identity: selected Backspace
// invokes DeleteBlock; selected forward Delete is not an unobserved alias.
func TestSelectedBlockBackspaceQuestionsAndDeclines(t *testing.T) {
	for _, span := range []struct {
		name       string
		start, end int
	}{{"opening", 1, 2}, {"closing", 4, 5}, {"whole", 1, 5}} {
		for _, answer := range []editor.Command{editor.No, editor.F1, editor.Escape} {
			t.Run(span.name+string(rune('A'+answer)), func(t *testing.T) {
				f := setup(t)
				base := load(t, f)
				normal := key(t, base, editor.Right)
				expectRefusal(t, normal, editor.Event{Command: editor.Block}) // normal selection remains unqualified
				s := key(t, base, editor.Reveal)
				for range span.start {
					s = key(t, s, editor.Right)
				}
				s = key(t, s, editor.Block)
				for j := span.start; j < span.end; j++ {
					s = key(t, s, editor.Right)
				}
				selected := s.Snapshot()
				revision := s.Document().Revision()
				history := s.History().Revision()
				forward, _, err := s.Reduce(editor.Event{Command: editor.Delete})
				if err == nil || !reflect.DeepEqual(forward.Snapshot(), selected) {
					t.Fatal("unobserved selected Delete gained parity")
				}
				s = key(t, s, editor.Backspace)
				q := s.Snapshot()
				if q.Mode != editor.DeleteQuestion || q.Prompt != "Delete Block? No (Yes)" || q.Gap != span.end || !q.Selection || q.Dirty || q.SelectionStart != span.start || q.SelectionEnd != span.end {
					t.Fatalf("question fields: %+v", q)
				}
				raw, _ := s.Document().Export()
				if !bytes.Equal(raw, f.raw) || s.Document().Revision() != revision || s.History().Revision() != history {
					t.Fatal("question changed native/history")
				}
				s = key(t, s, answer)
				d := s.Snapshot()
				raw, _ = s.Document().Export()
				if d.Mode != editor.Editing || !d.Selection || d.Gap != span.end || d.Dirty || !bytes.Equal(raw, f.raw) || s.Document().Revision() != revision {
					t.Fatal("decline changed selection/native/revision")
				}
				s = key(t, s, editor.F1)
				if s.Snapshot().Selection || s.Snapshot().Gap != span.end || s.Snapshot().Dirty {
					t.Fatal("separate F1 cleanup")
				}
				// Earlier immutable selected/question values cannot be consumed by later state.
				if !selected.Selection || q.Mode != editor.DeleteQuestion {
					t.Fatal("prior values changed")
				}
			})
		}
	}
}

func TestOriginal23RepairRestoreBackspaceReplay(t *testing.T) {
	for _, repeat := range []string{"r1", "r2"} {
		t.Run(repeat, func(t *testing.T) {
			root := "../../docs/research/continuation/native-edits/runs/wp23-b-history-follow-repair-restore-" + repeat
			raw, err := os.ReadFile(root + "/N0000.WP5")
			if err != nil {
				t.Fatal(err)
			}
			s, _ := loadNative(t, raw)
			for _, c := range []editor.Command{editor.Reveal, editor.Right, editor.Block, editor.Right, editor.Backspace, editor.Yes} {
				s = key(t, s, c)
			}
			if s.Snapshot().Selection || s.Snapshot().Gap != 2 || !s.Snapshot().Dirty {
				t.Fatal("repair endpoint")
			}
			s = browse(t, s, 1)
			s = key(t, key(t, s, editor.F1), editor.Restore)
			s = browse(t, s, 1)
			s = text(t, s, "X")
			got, err := s.Document().Export()
			if err != nil {
				t.Fatal(err)
			}
			want, err := os.ReadFile(root + "/N0001.WP5")
			if err != nil {
				t.Fatal(err)
			}
			if !bytes.Equal(got, want) || s.Snapshot().Gap != 5 {
				t.Fatal("actual23 native Backspace/repair/Restore marker mismatch")
			}
		})
	}
}
func TestOrdinaryNormalBackspaceQuestionStillDirectional(t *testing.T) {
	for _, answer := range []editor.Command{editor.No, editor.F1, editor.Escape} {
		t.Run(string(rune('A'+answer)), func(t *testing.T) {
			f := setup(t)
			s := key(t, key(t, load(t, f), editor.Right), editor.Right)
			s = key(t, s, editor.Backspace)
			if s.Snapshot().Prompt != "Delete [BOLD]? No (Yes)" {
				t.Fatal("ordinary Backspace became block deletion")
			}
			s = key(t, s, answer)
			raw, _ := s.Document().Export()
			if !bytes.Equal(raw, f.raw) || s.Snapshot().Gap != 1 || s.Snapshot().Dirty || s.Snapshot().Selection {
				t.Fatal("ordinary directional decline changed")
			}
		})
	}
}
