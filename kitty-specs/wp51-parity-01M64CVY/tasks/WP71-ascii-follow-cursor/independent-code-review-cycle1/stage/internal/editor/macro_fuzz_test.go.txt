package editor_test

import (
	"context"
	"github.com/lynncoleart/wordling/internal/editor"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"path/filepath"
	"testing"
)

// Adapter budget: at most64 operations/16 charged units per slice, work256 and
// output32 per run (shared over repeat3). No binary decoder or VM budget change.
func FuzzMacroAdapterContinuations(f *testing.F) {
	root := f.TempDir()
	doc, e := os.ReadFile("../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01/run-doc1-1/D1BASE.WP5")
	if e != nil {
		f.Fatal(e)
	}
	macro, e := os.ReadFile("../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
	if e != nil {
		f.Fatal(e)
	}
	for name, data := range map[string][]byte{"ORIGIN": doc, "M38.WPM": macro} {
		if e = os.WriteFile(filepath.Join(root, name), data, 0600); e != nil {
			f.Fatal(e)
		}
	}
	dir, e := storage.OpenDirectory(root)
	if e != nil {
		f.Fatal(e)
	}
	defer dir.Close()
	base, e := editor.New(editor.Config{Locations: []editor.Location{{Prefix: "B:\\", Directory: dir}}})
	if e != nil {
		f.Fatal(e)
	}
	base, _, _ = base.Reduce(editor.Event{Command: editor.Retrieve})
	base, _, _ = base.Reduce(editor.Event{Command: editor.Text, Text: "B:\\ORIGIN"})
	base, i, _ := base.Reduce(editor.Event{Command: editor.Enter})
	r := perform(i)
	base, _, e = base.Reduce(editor.Event{Command: editor.Complete, Result: &r})
	if e != nil {
		f.Fatal(e)
	}
	for _, seed := range [][]byte{{0, 1, 2, 3, 4, 5, 6, 7}, {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}, {3, 1, 5, 8, 13, 21, 34}, {255, 0, 7, 4, 9, 2}} {
		f.Add(seed)
	}
	f.Fuzz(func(t *testing.T, input []byte) {
		if len(input) > 64 {
			t.Skip()
		}
		s := base
		var execution *editor.MacroExecution
		var old editor.Session
		limits := vm.DefaultLimits()
		limits.Steps = 256
		limits.OutputWords = 32
		limits.SliceSteps = 16
		for _, v := range input {
			before := s.Document().Revision()
			var err error
			if execution != nil && !execution.Snapshot().Terminal {
				switch v % 5 {
				case 0:
					_, _, _, err = execution.Step(context.Background(), old, 1)
					if err == nil {
						t.Fatal("stale/foreign session accepted")
					}
				case 1:
					old = s
					s, _, _, err = execution.Step(context.Background(), s, 1+uint32(v%16))
				case 2:
					old = s
					s, _, err = execution.HostStop(s, "generated host containment")
				case 3:
					_, _, err = execution.OriginalCancel(s)
					if err == nil {
						t.Fatal("unqualified operator Cancel admitted")
					}
				case 4:
					_, _, err = s.Reduce(editor.Event{Command: editor.SwitchDocument})
					if err == nil {
						t.Fatal("active macro changed buffer")
					}
				}
			} else {
				execution = nil
				switch s.Snapshot().Mode {
				case editor.MacroName:
					if v%3 == 0 {
						s, _, err = s.Reduce(editor.Event{Command: editor.F1})
					} else {
						s, _, err = s.Reduce(editor.Event{Command: editor.Text, Text: "B:\\M38"})
						if err == nil {
							s, _, err = s.Reduce(editor.Event{Command: editor.Enter})
						}
					}
				case editor.Waiting:
					pending := s.Snapshot().Pending
					if pending != nil && pending.Kind == editor.ReadMacro {
						result := editor.ExecuteMacroRead(pending)
						if v%3 == 0 {
							result.Operation++
						}
						s, _, err = s.Reduce(editor.Event{Command: editor.Complete, Result: &result})
					}
				case editor.MacroReady:
					old = s
					s, execution, err = s.StartMacro(limits)
				case editor.MacroError:
					s, _, err = s.Reduce(editor.Event{Command: editor.F1})
				case editor.Editing:
					switch v % 5 {
					case 0:
						s, _, err = s.Reduce(editor.Event{Command: editor.Text, Text: "x"})
					case 1:
						s, _, err = s.Reduce(editor.Event{Command: editor.Macro})
					case 2:
						s, _, err = s.Reduce(editor.Event{Command: editor.Right})
					case 3:
						s, err = s.WithMacroRepeat(3)
					case 4:
						s, _, err = s.Reduce(editor.Event{Command: editor.SwitchDocument})
					}
				}
			}
			if err != nil && s.Document().Revision() != before {
				t.Fatal("refusal changed native revision")
			}
			if execution != nil {
				p := execution.Snapshot()
				if p.TotalSteps > limits.Steps || p.TotalWords > limits.OutputWords {
					t.Fatal("adapter broadened total VM budget")
				}
				if p.AppliedWords > p.TotalWords || p.ReceiptCount > int(p.TotalWords) {
					t.Fatal("invented/duplicated effect receipts")
				}
			}
		}
	})
}
