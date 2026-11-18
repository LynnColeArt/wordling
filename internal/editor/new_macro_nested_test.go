package editor_test

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/editor"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/storage"
)

type newNestedSample struct {
	id, run, root, output string
	sources               map[string][]byte
}

func newNestedSamples(t *testing.T) []newNestedSample {
	t.Helper()
	raw, err := os.ReadFile("../macro/runtime/testdata/original-cases.json")
	if err != nil {
		t.Fatal(err)
	}
	var corpus struct {
		Cases []struct {
			ID          string `json:"case_id"`
			Run, Repeat string
			Root        string `json:"root_macro"`
			Expected    struct {
				Hex string `json:"expected_hex"`
			}
		} `json:"macro_cases"`
		Exports []struct {
			Path, Run, SHA256 string
			ID                string `json:"case_id"`
		} `json:"wpm_exports"`
	}
	if err = json.Unmarshal(raw, &corpus); err != nil {
		t.Fatal(err)
	}
	outputs := map[string]string{"CMD51-210": "HANDLED", "CMD51-212": "PCHILDRPARENT", "CMD51-213": "PCPARENT", "CMD51-230": "PCCHILDBADRDONE"}
	var samples []newNestedSample
	for _, c := range corpus.Cases {
		want, ok := outputs[c.ID]
		if !ok {
			continue
		}
		body, err := hex.DecodeString(c.Expected.Hex)
		if err != nil || string(body) != want {
			t.Fatal("original expectation", c.ID, err)
		}
		for _, run := range []string{c.Run, c.Repeat} {
			sample := newNestedSample{id: c.ID, run: run, root: c.Root, output: want, sources: map[string][]byte{}}
			for _, export := range corpus.Exports {
				if export.ID != c.ID || export.Run != run {
					continue
				}
				data, err := os.ReadFile("../../" + export.Path)
				if err != nil || fmt.Sprintf("%x", sha256.Sum256(data)) != export.SHA256 {
					t.Fatal("source identity", export.Path, err)
				}
				sample.sources[filepath.Base(export.Path)] = data
			}
			if sample.sources[c.Root] == nil || (c.ID != "CMD51-210" && sample.sources["CHILD.WPM"] == nil) {
				t.Fatal("incomplete original source pair", c.ID, run)
			}
			samples = append(samples, sample)
		}
	}
	if len(samples) != 8 {
		t.Fatal("four cases/two original repetitions", len(samples))
	}
	return samples
}

func stageNewNested(t *testing.T, root string, sample newNestedSample) {
	t.Helper()
	for name, raw := range sample.sources {
		if err := os.WriteFile(filepath.Join(root, name), raw, 0600); err != nil {
			t.Fatal(err)
		}
	}
}

func newNestedReceiver(t *testing.T, edited bool) (editor.Session, *storage.Directory, string) {
	t.Helper()
	root := t.TempDir()
	dir, err := storage.OpenDirectory(root)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = dir.Close() })
	config := editor.Config{Locations: []editor.Location{{Directory: dir}, {Prefix: `C:\OUT\`, Directory: dir}}}
	if edited {
		workspace, err := storage.OpenWorkspace(root)
		if err != nil {
			t.Fatal(err)
		}
		t.Cleanup(func() { _ = workspace.Close() })
		config.Workspace = workspace
	}
	s, err := editor.New(config)
	if err != nil {
		t.Fatal(err)
	}
	if edited {
		s = liveText(t, s, "LEFTRIGHT")
		for range 5 {
			s = liveKeys(t, s, editor.Left)
		}
		if s.Snapshot().Gap != 4 || !s.CanRunWorkspaceMacro() {
			t.Fatal("real edited New receiver", s.Snapshot())
		}
	}
	return s, dir, root
}

func startNewNested(t *testing.T, s editor.Session, name string) (editor.Session, *editor.MacroExecution) {
	t.Helper()
	s = key(t, s, editor.Macro)
	s = text(t, s, `C:\OUT\`+strings.TrimSuffix(name, ".WPM"))
	s, intent := submit(t, s)
	if intent == nil || intent.Kind != editor.ReadMacro {
		t.Fatal("root acquisition")
	}
	s, _ = done(t, s, editor.ExecuteMacroRead(intent))
	s, run, err := s.StartMacro(vm.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	return s, run
}

// Unlike the root-only historical helper, this drives real child acquisition.
func runNewNested(t *testing.T, s editor.Session, run *editor.MacroExecution, quota uint32) editor.Session {
	t.Helper()
	for n := 0; !run.Snapshot().Terminal; n++ {
		if n >= 4096 {
			t.Fatal("bounded child-aware driver")
		}
		before := run.Snapshot().TotalSteps
		next, intent, p, err := run.Step(context.Background(), s, quota)
		if err != nil || p.TotalSteps-before > uint64(quota) {
			t.Fatalf("nested step: %v %+v", err, p)
		}
		s = next
		if intent != nil {
			if intent.Kind != editor.ReadMacro || intent.MacroRequest == 0 || intent.MacroRun != p.Run {
				t.Fatal("child authority", intent, p)
			}
			s, _, err = run.Resume(s, editor.ExecuteMacroRead(intent))
			if err != nil {
				t.Fatal("nested resume", err)
			}
		}
	}
	if run.Snapshot().State != "complete" {
		t.Fatalf("nested execution: %+v", run.Snapshot())
	}
	return s
}

func checkNewNestedReceipts(t *testing.T, run *editor.MacroExecution, sample newNestedSample, gap int) {
	t.Helper()
	p := run.Snapshot()
	receipts, err := run.Receipts(0, p.ReceiptCount)
	if err != nil {
		t.Fatal(err)
	}
	sources := map[[32]byte][]byte{}
	for _, raw := range sample.sources {
		sources[sha256.Sum256(raw)] = raw
	}
	childSeen := false
	applied := 0
	for _, receipt := range receipts {
		raw, ok := sources[receipt.Effect.Source]
		if !ok || !receipt.Applied || receipt.Err != nil || !receipt.Result.MayHaveEffects || len(receipt.Effect.Words) != 1 || receipt.Screen != 1 {
			t.Fatal("effect provenance", receipt)
		}
		word := receipt.Effect.Words[0]
		at := int(word.Span.Offset)
		if word.Span.Length != 2 || at < 75 || at+2 > len(raw) || binary.LittleEndian.Uint16(raw[at:]) != word.Value {
			t.Fatal("original source span", receipt)
		}
		if receipt.Effect.Source == sha256.Sum256(sample.sources["CHILD.WPM"]) {
			childSeen = true
		}
		if receipt.Effect.Kind == "display-off" {
			if receipt.Before != receipt.After || receipt.BeforeGap != receipt.AfterGap {
				t.Fatal("display mutated native", receipt)
			}
		} else {
			if receipt.BeforeGap != gap+applied || receipt.AfterGap != gap+applied+1 || receipt.After != receipt.Before+1 {
				t.Fatal("actual caret/revision receipt", receipt)
			}
			applied++
		}
	}
	if applied != len(sample.output) || p.AppliedWords != uint64(applied) || (sample.id != "CMD51-210" && !childSeen) {
		t.Fatal("parent/child applications", p, childSeen)
	}
}

func TestNewNestedOriginalPrograms(t *testing.T) {
	for _, sample := range newNestedSamples(t) {
		for _, edited := range []bool{false, true} {
			for _, quota := range []uint32{1, 16} {
				t.Run(fmt.Sprintf("%s/%s/edited-%t/q%d", sample.id, sample.run, edited, quota), func(t *testing.T) {
					s, dir, root := newNestedReceiver(t, edited)
					stageNewNested(t, root, sample)
					before, birth := s.Snapshot(), s.Document().Birth()
					s, run := startNewNested(t, s, sample.root)
					s = runNewNested(t, s, run, quota)
					want := sample.output
					if edited {
						want = "LEFT" + want + "RIGHT"
					}
					state, p := s.Snapshot(), run.Snapshot()
					if asciiText(t, s) != want || state.Gap != before.Gap+len(sample.output) || !state.Dirty || state.Name != "" || s.Source() != nil || state.NewPhase != editor.NewUnpublished || state.GenesisRevision != before.GenesisRevision || s.Document().Birth() != birth || p.Repeat != 1 || p.Completed != 1 || p.Pending != nil || p.DisplaySuppressed {
						t.Fatalf("New receiver/result %+v %+v body%q", state, p, asciiText(t, s))
					}
					checkNewNestedReceipts(t, run, sample, before.Gap)
					if _, _, err := run.Resume(s, editor.Result{}); err == nil {
						t.Fatal("terminal duplicate accepted")
					}
					if !edited {
						raw, err := s.Document().Export()
						if err != nil {
							t.Fatal(err)
						}
						s, publish := firstRequest(t, s, dir, "RESULT.WP")
						s = finishFirst(t, s, publish)
						actual, err := os.ReadFile(filepath.Join(root, "RESULT.WP"))
						if err != nil || !bytes.Equal(actual, raw) || s.Document().Birth() != birth || s.Snapshot().NativeRevision != state.NativeRevision || s.Snapshot().Gap != state.Gap {
							t.Fatal("first publication provenance", err, s.Snapshot())
						}
					}
					for name, original := range sample.sources {
						actual, err := os.ReadFile(filepath.Join(root, name))
						if err != nil || !bytes.Equal(actual, original) {
							t.Fatal("WPM source modified", name, err)
						}
					}
				})
			}
		}
	}
}
