package tui

import (
	"bytes"
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/wp51"
)

func macroModel(t *testing.T, profile string, raw []byte) (*Runtime, Model, string) {
	t.Helper()
	root := t.TempDir()
	if e := os.WriteFile(filepath.Join(root, "ORIGIN"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	r, m, e := Open(Config{Root: root, Profile: profile})
	if e != nil {
		t.Fatal(e)
	}
	t.Cleanup(func() { _ = r.Close() })
	return r, retrieve(m), root
}
func actualMacroSave(t *testing.T, m Model, root, name string) (Model, []byte) {
	t.Helper()
	m, c := queueEdited(t, m, name)
	m = drain(m, c)
	raw, e := os.ReadFile(filepath.Join(root, name))
	if e != nil || m.Session().Snapshot().Dirty || m.Session().Snapshot().SaveState != editor.NewNamePublished {
		t.Fatal("actual macro native publication", e, m.State())
	}
	return m, raw
}
func macroNative(t *testing.T, got, want []byte) {
	t.Helper()
	image, e := wp51.Parse(want)
	if e != nil {
		t.Fatal(e)
	}
	flag := -1
	for _, p := range image.Inspect().Packets {
		if p.Type == 6 {
			if flag >= 0 {
				t.Fatal("multiple flag owners")
			}
			flag = p.Data.Offset
		}
	}
	if flag < 0 || len(got) != len(want) {
		t.Fatal("native length/framing differs")
	}
	differences := 0
	for i, b := range got {
		if b != want[i] {
			if i != flag || b != want[i]|8 {
				t.Fatalf("unexplained native byte %d: %02x/%02x", i, b, want[i])
			}
			differences++
		}
	}
	t.Logf("actual native sha%x original sha%x length%d indexed-policy-differences%d", sha256.Sum256(got), sha256.Sum256(want), len(got), differences)
	if dir := os.Getenv("WORDLING_WP37_NATIVE"); dir != "" {
		if e := os.MkdirAll(dir, 0700); e != nil {
			t.Fatal(e)
		}
		hash := sha256.Sum256(got)
		name := strings.ReplaceAll(t.Name(), "/", "_") + fmt.Sprintf("-%x.WP5", hash[:8])
		if e := os.WriteFile(filepath.Join(dir, name), got, 0600); e != nil {
			t.Fatal(e)
		}
	}
}
func macroEnd(t *testing.T, m Model) Model {
	t.Helper()
	for m.Session().Snapshot().Gap < m.Session().Document().TokenCount() {
		m = key(t, m, tea.KeyRight, 0, "")
	}
	return m
}
func TestMacroOriginal09AllContextsUseLiveInputRuntimeAndPublication(t *testing.T) {
	raw, e := os.ReadFile("../../internal/macro/runtime/testdata/original-cases.json")
	if e != nil {
		t.Fatal(e)
	}
	var corpus struct {
		Cases []struct {
			ID      string `json:"case_id"`
			Root    string `json:"root_macro"`
			Results []struct {
				Path string `json:"path"`
			} `json:"native_results"`
		} `json:"macro_cases"`
		Exports []struct {
			Path, Run string
			ID        string `json:"case_id"`
		} `json:"wpm_exports"`
	}
	if e = json.Unmarshal(raw, &corpus); e != nil {
		t.Fatal(e)
	}
	if len(corpus.Cases) != 20 || len(corpus.Exports) != 46 {
		t.Fatal("approved corpus identity")
	}
	for _, c := range corpus.Cases {
		for _, result := range c.Results {
			t.Run(c.ID+filepath.Base(filepath.Dir(filepath.Dir(result.Path))), func(t *testing.T) {
				original, e := os.ReadFile("../../" + result.Path)
				if e != nil {
					t.Fatal(e)
				}
				_, m, root := macroModel(t, MacroCOUT, original)
				source := m.Session().Source().Identity()
				count := m.Session().Document().TokenCount()
				if c.ID == "CMD51-131" {
					count -= 3
				}
				for range count {
					m = key(t, m, tea.KeyDelete, 0, "")
				}
				if c.ID == "CMD51-131" {
					m = macroEnd(t, m)
				}
				if c.ID == "CMD51-132" {
					m = key(t, m, tea.KeyEscape, 0, "")
					m = key(t, m, '3', 0, "3")
				}
				for _, p := range corpus.Exports {
					if p.ID == c.ID && strings.Contains(result.Path, "/"+p.Run+"/") {
						macroFile(t, root, filepath.Base(p.Path), p.Path)
					}
				}
				before := m.Session().Document().Revision()
				m, cmd := queuedMacro(t, m, strings.TrimSuffix(c.Root, ".WPM"))
				m = drain(m, cmd)
				if c.ID == "CMD51-178" || c.ID == "CMD51-206" {
					if m.Session().Document().Revision() != before || m.State().Macro.State != "refused" || m.State().Macro.AppliedWords != 0 {
						t.Fatal("search was faked", m.State())
					}
					t.Log("unavailable search path remains explicit refusal")
					return
				}
				if m.State().Macro.Error != "" || !m.State().Macro.Terminal {
					t.Fatal("real macro did not finish", m.State())
				}
				m, candidate := actualMacroSave(t, m, root, "OUTPUT")
				macroNative(t, candidate, original)
				if m.Session().Source().Identity() != source || !bytes.Equal(m.Session().Source().Export(), original) {
					t.Fatal("macro save rebased original source")
				}
			})
		}
	}
}
func twoMacroBuffers(t *testing.T, base, sample string) (*Runtime, Model, string) {
	t.Helper()
	raw, e := os.ReadFile("../../" + base + "/" + sample + "/D1BASE.WP5")
	if e != nil {
		t.Fatal(e)
	}
	r, m, root := macroModel(t, MacroCOUT, raw)
	m = macroEnd(t, m)
	m = key(t, m, 'D', 0, "DIRTY1")
	m = key(t, m, tea.KeyF3, tea.ModShift, "")
	macroFile(t, root, "SECOND", base+"/"+sample+"/D2BASE.WP5")
	m = key(t, m, tea.KeyF10, tea.ModShift, "")
	m = key(t, m, 'S', 0, "SECOND")
	m, c := press(m, tea.KeyEnter, 0, "")
	m = drain(m, c)
	m = macroEnd(t, m)
	m = key(t, m, 'D', 0, "DIRTY2")
	return r, m, root
}
func TestMacroOriginal38RunRepeatDoc2ThroughActualIO(t *testing.T) {
	for _, kind := range []string{"run-doc1", "repeat-doc2"} {
		for n := 1; n <= 2; n++ {
			t.Run(fmt.Sprintf("%s-%d", kind, n), func(t *testing.T) {
				run := "wp38-run-doc1-01"
				if kind == "repeat-doc2" {
					run = "wp38-repeat-doc2-02"
				}
				base := "docs/research/continuation/macro-session/runs/" + run
				sample := fmt.Sprintf("%s-%d", kind, n)
				_, m, root := twoMacroBuffers(t, base, sample)
				macroFile(t, root, "M38.WPM", base+"/input/M38.WPM")
				if kind == "run-doc1" {
					m = key(t, m, tea.KeyF3, tea.ModShift, "")
				} else {
					m = key(t, m, tea.KeyEscape, 0, "")
					if !strings.Contains(m.View().Content, "Repeat Value = ") {
						t.Fatal("repeat prompt")
					}
					m = key(t, m, '3', 0, "3")
				}
				m, c := queuedMacro(t, m, "M38")
				m = drain(m, c)
				target := m.Session().Snapshot().Screen
				name := "D1OUT"
				expected := "D1AFTER.WP5"
				other := "D2AFTER.WP5"
				if target == 2 {
					name = "D2OUT"
					expected = "D2AFTER.WP5"
					other = "D1AFTER.WP5"
				}
				m, got := actualMacroSave(t, m, root, name)
				want, e := os.ReadFile("../../" + base + "/" + sample + "/" + expected)
				if e != nil {
					t.Fatal(e)
				}
				macroNative(t, got, want)
				m = key(t, m, tea.KeyF3, tea.ModShift, "")
				m, got = actualMacroSave(t, m, root, "OTHEROUT")
				want, e = os.ReadFile("../../" + base + "/" + sample + "/" + other)
				if e != nil {
					t.Fatal(e)
				}
				macroNative(t, got, want)
			})
		}
	}
}
func TestMacroOriginal39RootAndChildStopAndManualReady(t *testing.T) {
	for _, kind := range []string{"root", "nested"} {
		for n := 1; n <= 2; n++ {
			t.Run(fmt.Sprintf("%s-%d", kind, n), func(t *testing.T) {
				base := "docs/research/continuation/macro-quit/runs/wp39-" + kind + "-02"
				sample := fmt.Sprintf("%s-%d", kind, n)
				_, m, root := twoMacroBuffers(t, base, sample)
				m = key(t, m, tea.KeyF3, tea.ModShift, "")
				name := "Q39R"
				if kind == "nested" {
					name = "Q39P"
					macroFile(t, root, "Q39C.WPM", base+"/input/Q39C.WPM")
				}
				macroFile(t, root, name+".WPM", base+"/input/"+name+".WPM")
				m, c := queuedMacro(t, m, name)
				m = drain(m, c)
				if m.State().Macro.State != "complete" || m.State().Macro.Error != "" {
					t.Fatal("qualified normal QUIT did not complete invocation", m.State())
				}
				m, got := actualMacroSave(t, m, root, "BEFORE")
				want, e := os.ReadFile("../../" + base + "/" + sample + "/QBEFORE.WP5")
				if e != nil {
					t.Fatal(e)
				}
				macroNative(t, got, want)
				m = key(t, m, 'R', 0, "READY")
				m, got = actualMacroSave(t, m, root, "AFTER")
				want, e = os.ReadFile("../../" + base + "/" + sample + "/QAFTER.WP5")
				if e != nil {
					t.Fatal(e)
				}
				macroNative(t, got, want)
			})
		}
	}
}
