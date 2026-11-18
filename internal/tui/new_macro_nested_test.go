package tui

import (
	"bytes"
	"crypto/sha256"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
)

type nestedRuntimeSample struct {
	id, run, root, output string
	sources               map[string][]byte
	reads                 int
}

func nestedRuntimeSamples(t *testing.T) []nestedRuntimeSample {
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
	reads := map[string]int{"CMD51-210": 2, "CMD51-212": 4, "CMD51-213": 3, "CMD51-230": 2}
	var samples []nestedRuntimeSample
	for _, c := range corpus.Cases {
		want, ok := outputs[c.ID]
		if !ok {
			continue
		}
		for _, run := range []string{c.Run, c.Repeat} {
			sample := nestedRuntimeSample{id: c.ID, run: run, root: c.Root, output: want, reads: reads[c.ID], sources: map[string][]byte{}}
			for _, export := range corpus.Exports {
				if export.ID != c.ID || export.Run != run {
					continue
				}
				data, err := os.ReadFile("../../" + export.Path)
				if err != nil || fmt.Sprintf("%x", sha256.Sum256(data)) != export.SHA256 {
					t.Fatal("original source binding", export.Path, err)
				}
				sample.sources[filepath.Base(export.Path)] = data
			}
			if sample.sources[sample.root] == nil || (sample.id != "CMD51-210" && sample.sources["CHILD.WPM"] == nil) {
				t.Fatal("missing authentic programs", sample.id)
			}
			samples = append(samples, sample)
		}
	}
	if len(samples) != 8 {
		t.Fatal("source repetitions", len(samples))
	}
	return samples
}

func nestedRuntime(t *testing.T, sample nestedRuntimeSample, edited bool) (*Runtime, Model, string, []byte) {
	t.Helper()
	root := t.TempDir()
	r, m, err := Open(Config{Root: root, Profile: MacroCOUT, EditorChrome: edited})
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() {
		if err := r.Close(); err != nil {
			t.Error(err)
		}
	})
	for name, raw := range sample.sources {
		if err = os.WriteFile(filepath.Join(root, name), raw, 0600); err != nil {
			t.Fatal(err)
		}
	}
	var other []byte
	if edited {
		// Both screens are genuinely created through public keyboard input.
		m = key(t, m, tea.KeyF3, tea.ModShift, "")
		if m.Session().Snapshot().Screen != 2 {
			t.Fatal("Doc2 setup", m.State())
		}
		m = key(t, m, 'O', 0, "OTHER SCREEN")
		m = key(t, m, tea.KeyF3, tea.ModShift, "")
		doc, err := m.Session().NativeOnScreen(2)
		if err != nil {
			t.Fatal(err)
		}
		other, _ = doc.Export()
		m = key(t, m, 'L', 0, "LEFTRIGHT")
		for range 5 {
			m = key(t, m, tea.KeyLeft, 0, "")
		}
		if m.Session().Snapshot().Gap != 4 || !m.Session().CanRunWorkspaceMacro() {
			t.Fatal("edited New admission", m.State())
		}
	}
	return r, m, root, other
}

func drainNestedRuntime(t *testing.T, m Model, c tea.Cmd) (Model, *editor.MacroExecution) {
	t.Helper()
	var driver *editor.MacroExecution
	for n := 0; c != nil; n++ {
		if n >= 4096 {
			t.Fatal("bounded public runtime")
		}
		if m.macro != nil && m.macro.driver != nil {
			driver = m.macro.driver
		}
		pending := m.Session().Snapshot().Pending
		actual := c()
		if pending != nil && pending.Kind == editor.ReadMacro && pending.MacroRequest != 0 {
			before, _ := m.Session().Document().Export()
			completed := len(m.runtime.Completed())
			next, stray := m.Update(c())
			m = next.(Model)
			after, _ := m.Session().Document().Export()
			if stray != nil || !bytes.Equal(before, after) || len(m.runtime.Completed()) != completed || m.Session().Snapshot().Pending == nil || m.Session().Snapshot().Pending.Operation != pending.Operation {
				t.Fatal("duplicate settled/applied a child", m.State())
			}
		}
		next, follow := m.Update(actual)
		m = next.(Model)
		c = follow
		if m.macro != nil && m.macro.driver != nil {
			driver = m.macro.driver
		}
	}
	return m, driver
}

func runtimeNestedBody(t *testing.T, m Model) (string, []byte) {
	t.Helper()
	raw, err := m.Session().Document().Export()
	if err != nil || len(raw) < 8 {
		t.Fatal(err)
	}
	start := int(binary.LittleEndian.Uint32(raw[4:8]))
	if start < 0 || start > len(raw) {
		t.Fatal("native body boundary")
	}
	return string(raw[start:]), raw
}

func TestNewNestedRuntimeOriginalProgramsSaveAndReopen(t *testing.T) {
	for _, sample := range nestedRuntimeSamples(t) {
		for _, edited := range []bool{false, true} {
			t.Run(fmt.Sprintf("%s/%s/edited-%t", sample.id, sample.run, edited), func(t *testing.T) {
				r, m, root, otherBefore := nestedRuntime(t, sample, edited)
				before, birth := m.Session().Snapshot(), m.Session().Document().Birth()
				m, c := queuedMacro(t, m, `C:\OUT\`+strings.TrimSuffix(sample.root, ".WPM"))
				m, driver := drainNestedRuntime(t, m, c)
				if driver == nil {
					t.Fatal("no actual execution driver")
				}
				want := sample.output
				if edited {
					want = "LEFT" + want + "RIGHT"
				}
				body, raw := runtimeNestedBody(t, m)
				state, p := m.Session().Snapshot(), driver.Snapshot()
				if body != want || state.Gap != before.Gap+len(sample.output) || !state.Dirty || state.Name != "" || state.NewPhase != editor.NewUnpublished || m.Session().Source() != nil || m.Session().Document().Birth() != birth || state.GenesisRevision != before.GenesisRevision || m.State().PendingIO != 0 || m.State().Macro.Active || m.State().Macro.State != "complete" || m.State().Macro.Error != "" || m.State().Macro.AppliedWords != uint64(len(sample.output)) || p.Repeat != 1 || p.Completed != 1 || p.Pending != nil || p.DisplaySuppressed || len(r.Completed()) != sample.reads || len(r.CompletedMacros()) != 1 {
					t.Fatal("public New result/receipts", m.State(), p, body)
				}
				if p.Source != sha256.Sum256(sample.sources[sample.root]) {
					t.Fatal("root source identity")
				}
				known := map[[32]byte][]byte{}
				for _, data := range sample.sources {
					known[sha256.Sum256(data)] = data
				}
				receipts, err := driver.Receipts(0, p.ReceiptCount)
				if err != nil {
					t.Fatal(err)
				}
				for _, receipt := range receipts {
					source, ok := known[receipt.Effect.Source]
					if !ok || !receipt.Applied || receipt.Err != nil || len(receipt.Effect.Words) != 1 {
						t.Fatal("source receipt", receipt)
					}
					word := receipt.Effect.Words[0]
					offset := int(word.Span.Offset)
					if offset < 75 || offset+2 > len(source) || word.Span.Length != 2 || binary.LittleEndian.Uint16(source[offset:]) != word.Value {
						t.Fatal("original source span", receipt)
					}
				}
				if edited {
					other, err := m.Session().NativeOnScreen(2)
					if err != nil {
						t.Fatal(err)
					}
					otherAfter, _ := other.Export()
					if !bytes.Equal(otherBefore, otherAfter) {
						t.Fatal("nested execution edited Doc2")
					}
					m, c = press(m, tea.KeyF10, 0, "")
					if c != nil {
						t.Fatal("save name unexpectedly issued IO")
					}
					m = key(t, m, 'R', 0, "RESULT.WP")
					m, c = press(m, tea.KeyEnter, 0, "")
					if c == nil {
						t.Fatal("no real workspace save")
					}
					m = drain(m, c)
				} else {
					m, c = firstSave(t, m, "RESULT.WP")
					next, bind := m.Update(c())
					m = next.(Model)
					if bind == nil || m.Session().Snapshot().NewPhase != editor.AwaitFirstRead || m.Session().Source() != nil || !m.Session().Snapshot().Dirty || m.Session().Snapshot().Name != "" {
						t.Fatal("publish manufactured clean/source state", m.State())
					}
					m = drain(m, bind)
				}
				actual, err := os.ReadFile(filepath.Join(root, "RESULT.WP"))
				if err != nil || !bytes.Equal(actual, raw) || m.Session().Snapshot().Dirty || m.Session().Source() == nil || m.Session().Snapshot().Name != "RESULT.WP" || m.Session().Document().Birth() != birth || m.Session().Snapshot().NativeRevision != state.NativeRevision || m.Session().Snapshot().GenesisRevision != before.GenesisRevision || m.Session().Snapshot().Gap != state.Gap || m.State().PendingIO != 0 {
					t.Fatal("native publication/lineage", err, m.State())
				}
				if m.Session().Source().Identity().SHA256 != sha256.Sum256(actual) {
					t.Fatal("save receipt/source identity")
				}
				// Reopen through a fresh actual Runtime and public Retrieve commands.
				r2, reopened, err := Open(Config{Root: root, Profile: MacroCOUT, EditorChrome: edited})
				if err != nil {
					t.Fatal(err)
				}
				t.Cleanup(func() { _ = r2.Close() })
				reopened = key(t, reopened, tea.KeyF10, tea.ModShift, "")
				reopened = key(t, reopened, 'R', 0, "RESULT.WP")
				reopened, c = press(reopened, tea.KeyEnter, 0, "")
				reopened = drain(reopened, c)
				reopenedBody, reopenedRaw := runtimeNestedBody(t, reopened)
				if reopenedBody != want || !bytes.Equal(reopenedRaw, raw) || reopened.Session().Source() == nil || reopened.Session().Snapshot().Dirty || reopened.Session().Source().Identity().SHA256 != sha256.Sum256(actual) {
					t.Fatal("real native reopen changed content", reopened.State())
				}
				for name, original := range sample.sources {
					source, err := os.ReadFile(filepath.Join(root, name))
					if err != nil || !bytes.Equal(source, original) {
						t.Fatal("source WPM changed", name, err)
					}
				}
				if output := os.Getenv("WORDLING_WP100_EVIDENCE"); output != "" {
					if err = os.MkdirAll(output, 0700); err != nil {
						t.Fatal(err)
					}
					record := struct {
						Case, Run               string
						Edited                  bool
						Body                    string
						Before, Terminal, Saved editor.Snapshot
						Progress                editor.MacroProgress
						NativeSHA256            [32]byte
						Receipts                []editor.MacroReceipt
					}{sample.id, sample.run, edited, body, before, state, m.Session().Snapshot(), p, sha256.Sum256(raw), receipts}
					data, err := json.MarshalIndent(record, "", "  ")
					if err != nil {
						t.Fatal(err)
					}
					name := strings.ReplaceAll(t.Name(), "/", "_") + ".json"
					if err = os.WriteFile(filepath.Join(output, name), data, 0600); err != nil {
						t.Fatal(err)
					}
				}
			})
		}
	}
}

func TestNewNestedRuntimeActualChildHostFailure(t *testing.T) {
	sample := nestedRuntimeSamples(t)[2]
	r, m, root, _ := nestedRuntime(t, sample, false)
	m, c := queuedMacro(t, m, "PARENT")
	for n := 0; n < 4096; n++ {
		pending := m.Session().Snapshot().Pending
		if pending != nil && pending.Kind == editor.ReadMacro && pending.MacroRequest != 0 {
			before, _ := m.Session().Document().Export()
			// A directory at the declared child filename is an actual rooted I/O
			// failure, distinct from the original missing-file condition.
			child := filepath.Join(root, "CHILD.WPM")
			if err := os.Rename(child, child+".held"); err != nil {
				t.Fatal(err)
			}
			if err := os.Mkdir(child, 0700); err != nil {
				t.Fatal(err)
			}
			m, driver := drainNewMacro(t, m, c)
			after, _ := m.Session().Document().Export()
			if driver == nil || m.State().Macro.State != "failed" || !strings.Contains(m.State().Macro.Error, "HostFailure") || !bytes.Equal(before, after) || !m.Session().Snapshot().Dirty || m.Session().Source() != nil || m.State().PendingIO != 0 || m.State().Macro.Active || len(r.Completed()) != 2 {
				t.Fatal("real child host failure became handler or lost partial effects", m.State())
			}
			return
		}
		if c == nil {
			t.Fatal("no child work")
		}
		next, follow := m.Update(c())
		m = next.(Model)
		c = follow
	}
	t.Fatal("child IO bound")
}
