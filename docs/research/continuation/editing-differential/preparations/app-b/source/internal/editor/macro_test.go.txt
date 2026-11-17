package editor_test

import (
	"bytes"
	"context"
	"crypto/sha256"
	"fmt"
	"github.com/lynncoleart/wordling/internal/editor"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/wp51"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestActualMacroRootLoadAndOrdinaryReducer(t *testing.T) {
	for _, sample := range []string{"run-doc1-1", "run-doc1-2"} {
		t.Run(sample, func(t *testing.T) {
			root := "../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01"
			s, f := twoBuffers(t, root, sample)
			s = key(t, s, editor.SwitchDocument)
			other, _ := s.NativeOnScreen(2)
			before2, _ := other.Export()
			macro, e := os.ReadFile(root + "/input/M38.WPM")
			if e != nil {
				t.Fatal(e)
			}
			if e = os.WriteFile(filepath.Join(f.path, "M38.WPM"), macro, 0600); e != nil {
				t.Fatal(e)
			}
			s, run := openMacro(t, s, "B:\\M38")
			s = runMacro(t, s, run)
			got, _ := s.Document().Export()
			want, e := os.ReadFile(root + "/" + sample + "/D1AFTER.WP5")
			if e != nil {
				t.Fatal(e)
			}
			compareMacroNative(t, got, want)
			other, _ = s.NativeOnScreen(2)
			after2, _ := other.Export()
			if !bytes.Equal(before2, after2) || !s.Snapshot().Dirty || run.Snapshot().AppliedWords != 3 {
				t.Fatal("macro target/ordinary document/dirty state")
			}
		})
	}
}

// Original Save may clear the must-format flag. Wordling's independently
// approved25 candidate policy sets only indexed packet6 bit3. Keep both raw
// images literal and account for this one permitted difference, never normalize.
func compareMacroNative(t *testing.T, got, want []byte) {
	t.Helper()
	image, err := wp51.Parse(want)
	if err != nil {
		t.Fatal(err)
	}
	flag := -1
	for _, p := range image.Inspect().Packets {
		if p.Type == 6 {
			flag = p.Data.Offset
		}
	}
	if flag < 0 || len(got) != len(want) {
		t.Fatalf("native framing/length %d/%d", len(got), len(want))
	}
	differences := 0
	for i, b := range got {
		if b == want[i] {
			continue
		}
		if i != flag || b != want[i]|8 {
			t.Fatalf("unexplained native difference at%d: Go%02x original%02x", i, b, want[i])
		}
		differences++
	}
	t.Logf("actual native len%d sha%x; original sha%x; permitted indexed must-format differences%d", len(got), sha256.Sum256(got), sha256.Sum256(want), differences)
	if dir := os.Getenv("WORDLING_WP36_CANDIDATES"); dir != "" {
		if err := os.MkdirAll(dir, 0700); err != nil {
			t.Fatal(err)
		}
		digest := sha256.Sum256(got)
		name := strings.ReplaceAll(t.Name(), "/", "_") + fmt.Sprintf("-%x.WP5", digest[:8])
		if err := os.WriteFile(filepath.Join(dir, name), got, 0600); err != nil {
			t.Fatal(err)
		}
	}
}
func openMacro(t *testing.T, s editor.Session, name string) (editor.Session, *editor.MacroExecution) {
	t.Helper()
	s = key(t, s, editor.Macro)
	s = text(t, s, name)
	s, i := submit(t, s)
	s, _ = done(t, s, perform(i))
	next, run, err := s.StartMacro(vm.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	return next, run
}
func runMacro(t *testing.T, s editor.Session, run *editor.MacroExecution) editor.Session {
	t.Helper()
	for n := 0; !run.Snapshot().Terminal; n++ {
		if n > 1000000 {
			t.Fatal("test bound")
		}
		before := run.Snapshot().TotalSteps
		next, i, p, err := run.Step(context.Background(), s, 16)
		if err != nil {
			t.Fatal(err)
		}
		s = next
		if p.TotalSteps-before > 16 {
			t.Fatal("adapter reset per-slice work")
		}
		if i != nil {
			result := perform(i)
			s, _, err = run.Resume(s, result)
			if err != nil {
				t.Fatal(err)
			}
		}
	}
	if run.Snapshot().State != "complete" {
		t.Fatalf("macro result: %+v", run.Snapshot())
	}
	return s
}
func end(t *testing.T, s editor.Session) editor.Session {
	t.Helper()
	for range s.Document().TokenCount() {
		s = key(t, s, editor.Right)
	}
	return s
}
func twoBuffers(t *testing.T, root, sample string) (editor.Session, fixture) {
	t.Helper()
	raw, e := os.ReadFile(root + "/" + sample + "/D1BASE.WP5")
	if e != nil {
		t.Fatal(e)
	}
	s, f := loadNative(t, raw)
	s = text(t, end(t, s), "DIRTY1")
	s = key(t, s, editor.SwitchDocument)
	raw, e = os.ReadFile(root + "/" + sample + "/D2BASE.WP5")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(filepath.Join(f.path, "SECOND"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	s = text(t, key(t, s, editor.Retrieve), "B:\\SECOND")
	s, i := submit(t, s)
	s, _ = done(t, s, perform(i))
	s = text(t, end(t, s), "DIRTY2")
	return s, f
}
func TestOriginal38RepeatTargetsActualSecondBuffer(t *testing.T) {
	for _, sample := range []string{"repeat-doc2-1", "repeat-doc2-2"} {
		t.Run(sample, func(t *testing.T) {
			root := "../../docs/research/continuation/macro-session/runs/wp38-repeat-doc2-02"
			s, f := twoBuffers(t, root, sample)
			raw, e := os.ReadFile(root + "/input/M38.WPM")
			if e != nil {
				t.Fatal(e)
			}
			if e = os.WriteFile(filepath.Join(f.path, "M38.WPM"), raw, 0600); e != nil {
				t.Fatal(e)
			}
			beforeSource := s.Source().Identity()
			first, e := s.NativeOnScreen(1)
			if e != nil {
				t.Fatal(e)
			}
			before1, _ := first.Export()
			s, e = s.WithMacroRepeat(3)
			if e != nil {
				t.Fatal(e)
			}
			s, run := openMacro(t, s, "B:\\M38")
			s = runMacro(t, s, run)
			got, _ := s.Document().Export()
			want, e := os.ReadFile(root + "/" + sample + "/D2AFTER.WP5")
			if e != nil {
				t.Fatal(e)
			}
			compareMacroNative(t, got, want)
			first, e = s.NativeOnScreen(1)
			if e != nil {
				t.Fatal(e)
			}
			after1, _ := first.Export()
			if !bytes.Equal(after1, before1) || s.Snapshot().Screen != 2 || s.Source().Identity() != beforeSource || !s.Snapshot().Dirty || run.Snapshot().AppliedWords != 9 || run.Snapshot().Completed != 3 {
				t.Fatal("macro target/repeat/source identity")
			}
			s = key(t, s, editor.SwitchDocument)
			if s.Snapshot().Screen != 1 || !s.Snapshot().Dirty {
				t.Fatal("switch lost first native buffer")
			}
			raw1, _ := s.Document().Export()
			if !bytes.Equal(raw1, before1) {
				t.Fatal("second-target macro touched Doc1")
			}
		})
	}
}

func TestOriginal39NormalQuitRetainsRealPartialNativeAndManualReady(t *testing.T) {
	for _, kind := range []string{"root", "nested"} {
		for _, n := range []string{"1", "2"} {
			t.Run(kind+n, func(t *testing.T) {
				root := "../../docs/research/continuation/macro-quit/runs/wp39-" + kind + "-02"
				sample := kind + "-" + n
				s, f := twoBuffers(t, root, sample)
				s = key(t, s, editor.SwitchDocument)
				other, _ := s.NativeOnScreen(2)
				before2, _ := other.Export()
				name := "Q39R"
				files := []string{"Q39R"}
				if kind == "nested" {
					name = "Q39P"
					files = []string{"Q39P", "Q39C"}
				}
				for _, file := range files {
					raw, e := os.ReadFile(root + "/input/" + file + ".WPM")
					if e != nil {
						t.Fatal(e)
					}
					if e = os.WriteFile(filepath.Join(f.path, file+".WPM"), raw, 0600); e != nil {
						t.Fatal(e)
					}
				}
				s, run := openMacro(t, s, "B:\\"+name)
				s = runMacro(t, s, run)
				got, _ := s.Document().Export()
				want, e := os.ReadFile(root + "/" + sample + "/QBEFORE.WP5")
				if e != nil {
					t.Fatal(e)
				}
				compareMacroNative(t, got, want)
				s = text(t, s, "READY")
				got, _ = s.Document().Export()
				want, e = os.ReadFile(root + "/" + sample + "/QAFTER.WP5")
				if e != nil {
					t.Fatal(e)
				}
				compareMacroNative(t, got, want)
				other, _ = s.NativeOnScreen(2)
				after2, _ := other.Export()
				if !bytes.Equal(before2, after2) {
					t.Fatal("normal QUIT touched other screen")
				}
			})
		}
	}
}

func TestOriginal09MacroNativeOutputsThroughActualReducer(t *testing.T) {
	for _, runID := range []string{"2026-10-29-extended-03", "2026-10-29-extended-04"} {
		for _, caseID := range []string{"CMD51-131", "CMD51-132"} {
			t.Run(runID+caseID, func(t *testing.T) {
				root := "../../docs/research/reference-runs/" + runID + "/" + caseID
				file := "MACROOUT.WP5"
				if caseID == "CMD51-132" {
					file = "REPEAT.WP5"
				}
				original, e := os.ReadFile(root + "/" + file)
				if e != nil {
					t.Fatal(e)
				}
				s, f := loadNative(t, original)
				// Establish the captured supplied recording prefix (131) or the empty sourced
				// target (132) through real admitted ordinary edits. This is not a recorder
				// or native blank-document constructor; the original loaded guard remains.
				count := s.Document().TokenCount()
				if caseID == "CMD51-131" {
					count -= 3
				}
				for range count {
					s = key(t, s, editor.Delete)
				}
				if caseID == "CMD51-131" {
					s = end(t, s)
				} else {
					s, e = s.WithMacroRepeat(3)
					if e != nil {
						t.Fatal(e)
					}
				}
				macro, e := os.ReadFile(root + "/TESTMAC.WPM")
				if e != nil {
					t.Fatal(e)
				}
				if e = os.WriteFile(filepath.Join(f.path, "TESTMAC.WPM"), macro, 0600); e != nil {
					t.Fatal(e)
				}
				s, driver := openMacro(t, s, "B:\\TESTMAC")
				s = runMacro(t, s, driver)
				candidate, _ := s.Document().Export()
				compareMacroNative(t, candidate, original)
				if !bytes.Equal(s.Source().Export(), original) || !bytes.Equal(s.MacroSource().Export(), macro) {
					t.Fatal("source snapshots changed")
				}
			})
		}
	}
}
