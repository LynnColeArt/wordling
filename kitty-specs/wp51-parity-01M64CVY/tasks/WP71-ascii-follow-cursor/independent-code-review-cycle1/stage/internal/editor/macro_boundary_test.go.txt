package editor_test

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"path/filepath"
	"reflect"
	"testing"
)

func readyMacro(t *testing.T) (editor.Session, fixture) {
	t.Helper()
	f := setup(t)
	s := load(t, f)
	raw, e := os.ReadFile("../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(filepath.Join(f.path, "M38.WPM"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	s = key(t, s, editor.Macro)
	s = text(t, s, "B:\\M38")
	s, i := submit(t, s)
	s, _ = done(t, s, perform(i))
	return s, f
}
func asciiText(t *testing.T, s editor.Session) string {
	t.Helper()
	result := ""
	for i := range s.Document().TokenCount() {
		v, e := s.Document().Token(i)
		if e != nil {
			t.Fatal(e)
		}
		if v.Kind == document.ASCII {
			result += string(v.Raw)
		}
	}
	return result
}
func TestMacroNameCancelMissingAndPendingSave(t *testing.T) {
	f := setup(t)
	base := load(t, f)
	before, _ := base.Document().Export()
	s := text(t, key(t, base, editor.Macro), "UNEXECUTED")
	s = key(t, s, editor.F1)
	after, _ := s.Document().Export()
	if !bytes.Equal(before, after) || s.Snapshot().Mode != editor.Editing || s.Snapshot().Pending != nil {
		t.Fatal("unexecuted macro F1 changed document")
	}
	s = key(t, base, editor.Save)
	draft := s.Snapshot().Draft
	s = key(t, s, editor.Macro)
	if s.Snapshot().Mode != editor.SaveName || s.Snapshot().Draft != draft {
		t.Fatal("AltF10 nested in Save-name prompt")
	}
	s = text(t, key(t, base, editor.Macro), "C:\\OUT\\M38NONE")
	s, i := submit(t, s)
	s, _ = done(t, s, perform(i))
	if s.Snapshot().Mode != editor.MacroError || s.Snapshot().Notice != "ERROR: File not found -- C:\\OUT\\M38NONE.WPM" {
		t.Fatalf("actual missing macro: %+v", s.Snapshot())
	}
	s = key(t, s, editor.F1)
	after, _ = s.Document().Export()
	if !bytes.Equal(before, after) || s.Snapshot().Mode != editor.Editing {
		t.Fatal("missing macro F1 failed")
	}
}
func TestMacroLoadPrivateAuthorityAndObservation(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	raw, e := os.ReadFile("../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(filepath.Join(f.path, "M38.WPM"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	s = text(t, key(t, s, editor.Macro), "B:\\M38")
	s, i := submit(t, s)
	original := s.Snapshot().Pending
	// An independently opened equal-root wrapper has its own closed lifetime.
	// Public substitution cannot replace the actual captured opening capability.
	second, e := storage.OpenDirectory(f.path)
	if e != nil {
		t.Fatal(e)
	}
	if e = second.Close(); e != nil {
		t.Fatal(e)
	}
	*i.Directory = *second
	result := editor.ExecuteMacroRead(i)
	if result.Err != nil {
		t.Fatal("loader followed altered public equal-root wrapper", result.Err)
	}
	*result.Macro = storage.Macro{}
	next, _, err := s.Reduce(editor.Event{Command: editor.Complete, Result: &result})
	if err == nil || next.Snapshot().Pending.Operation != original.Operation {
		t.Fatal("changed public result consumed request")
	}
	result = editor.ExecuteMacroRead(original)
	s, _ = done(t, s, result)
	*result.Macro = storage.Macro{}
	*s.MacroSource().Image() = wpm.Image{}
	*s.MacroSource() = storage.Macro{}
	if !bytes.Equal(s.MacroSource().Export(), raw) {
		t.Fatal("accepted macro source followed public getter")
	}
	source := s.MacroSource().Identity()
	s, run, e := s.StartMacro(vm.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	copyDriver := *run
	*run = editor.MacroExecution{}
	if _, _, _, e = run.Step(context.Background(), s, 1); e == nil {
		t.Fatal("zero driver accepted")
	}
	s = runMacro(t, s, &copyDriver)
	if copyDriver.Snapshot().Source != source.SHA256 {
		t.Fatal("driver source rebound")
	}
}
func TestStaleLoaderAcrossScreenSwitchAndForeignResult(t *testing.T) {
	ready, f := readyMacro(t)
	base := load(t, f)
	s := text(t, key(t, base, editor.Macro), "B:\\M38")
	s, i := submit(t, s)
	result := perform(i)
	other := text(t, key(t, base, editor.Macro), "B:\\M38")
	other, foreign := submit(t, other)
	_ = other
	forged := perform(foreign)
	next, _, err := s.Reduce(editor.Event{Command: editor.Complete, Result: &forged})
	if err == nil || next.Snapshot().Pending.Operation != i.Operation {
		t.Fatal("foreign same-number read was accepted")
	}
	s = key(t, s, editor.CancelOperation)
	s = key(t, s, editor.F1)
	s = key(t, s, editor.SwitchDocument)
	s, _ = done(t, s, result)
	if s.Snapshot().Screen != 2 || s.MacroSource() != nil || s.Snapshot().Pending != nil {
		t.Fatal("late root load targeted new screen")
	}
	_, runA, e := ready.StartMacro(vm.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	activeB, runB, e := ready.StartMacro(vm.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	before := runA.Snapshot()
	if _, _, _, e = runA.Step(context.Background(), activeB, 1); e == nil || !reflect.DeepEqual(before, runA.Snapshot()) {
		t.Fatal("foreign private run/session identity accepted")
	}
	activeB = runMacro(t, activeB, runB)
	activeB = key(t, activeB, editor.SwitchDocument)
	if _, _, _, e = runB.Step(context.Background(), activeB, 1); e == nil {
		t.Fatal("terminal/screen-retargeted VM continued")
	}
}
func TestRepeatSharesTotalBudgetAndStaleStep(t *testing.T) {
	ready, _ := readyMacro(t)
	ready = key(t, ready, editor.CancelOperation)
	var e error
	ready, e = ready.WithMacroRepeat(3)
	if e != nil {
		t.Fatal(e)
	}
	expectRefusal(t, ready, editor.Event{Command: editor.Text, Text: "x"})
	ready = key(t, ready, editor.Macro)
	ready = text(t, ready, "B:\\M38")
	ready, i := submit(t, ready)
	ready, _ = done(t, ready, perform(i))
	limits := vm.DefaultLimits()
	limits.OutputWords = 5
	s, run, e := ready.StartMacro(limits)
	if e != nil {
		t.Fatal(e)
	}
	initial := s
	for !run.Snapshot().Terminal {
		old := s
		before := run.Snapshot().TotalSteps
		s, _, _, e = run.Step(context.Background(), s, 1)
		if e != nil {
			t.Fatal(e)
		}
		if run.Snapshot().TotalSteps-before > 1 {
			t.Fatal("slice budget reset")
		}
		if _, _, _, e = run.Step(context.Background(), old, 1); e == nil {
			t.Fatal("old Session continuation accepted")
		}
	}
	p := run.Snapshot()
	if p.State != "limited" || p.TotalWords > limits.OutputWords || p.AppliedWords != 3 || asciiText(t, s) != "ABCABCD" {
		t.Fatalf("shared output budget includes display control: %+v body%q", p, asciiText(t, s))
	}
	if initial.Snapshot().Mode != editor.MacroRunning {
		t.Fatal("prior persistent state mutated")
	}
}
func TestHostStopAndOriginalCancelStayDistinct(t *testing.T) {
	ready, _ := readyMacro(t)
	s, run, e := ready.StartMacro(vm.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	for run.Snapshot().AppliedWords < 1 {
		s, _, _, e = run.Step(context.Background(), s, 1)
		if e != nil {
			t.Fatal(e)
		}
	}
	before := s.Document().Revision()
	if _, _, e = run.OriginalCancel(s); e == nil {
		t.Fatal("unproved F1 promoted to host stop")
	}
	s, p, e := run.HostStop(s, "test host containment")
	if e != nil || p.State != "stopped" || s.Document().Revision() != before || p.Pending != nil {
		t.Fatal("stop rolled back or retained pending")
	}
	s = text(t, s, "USERREADY")
	if asciiText(t, s) != "AUSERREADYABCD" {
		t.Fatal("real partial effect/manual continuation")
	}
	receipts, e := run.Receipts(0, p.ReceiptCount)
	if e != nil {
		t.Fatal(e)
	}
	found := false
	for _, r := range receipts {
		if r.Applied {
			found = true
			r.Effect.Words[0].Value = 'Z'
		}
	}
	again, _ := run.Receipts(0, p.ReceiptCount)
	if !found || reflect.DeepEqual(receipts, again) {
		t.Fatal("receipt copy/observable effects")
	}
}
func TestMacroContextCancellationAndInvalidQuota(t *testing.T) {
	for _, test := range []string{"cancel", "quota"} {
		t.Run(test, func(t *testing.T) {
			ready, _ := readyMacro(t)
			s, run, e := ready.StartMacro(vm.DefaultLimits())
			if e != nil {
				t.Fatal(e)
			}
			before := s.Document().Revision()
			ctx := context.Background()
			quota := uint32(1)
			if test == "cancel" {
				c, cancel := context.WithCancel(ctx)
				cancel()
				ctx = c
			} else {
				quota = 0
			}
			s, _, p, e := run.Step(ctx, s, quota)
			if e != nil || !p.Terminal || p.Machine.Err == nil || s.Document().Revision() != before || s.Snapshot().Mode != editor.Editing {
				t.Fatal("failed boundary effects")
			}
		})
	}
}
func TestNestedRealHostFailureKeepsParentEffects(t *testing.T) {
	root := "../../docs/research/continuation/macro-quit/runs/wp39-nested-02"
	s, f := twoBuffers(t, root, "nested-1")
	s = key(t, s, editor.SwitchDocument)
	for _, file := range []string{"Q39P", "Q39C"} {
		raw, e := os.ReadFile(root + "/input/" + file + ".WPM")
		if e != nil {
			t.Fatal(e)
		}
		if e = os.WriteFile(filepath.Join(f.path, file+".WPM"), raw, 0600); e != nil {
			t.Fatal(e)
		}
	}
	s, run := openMacro(t, s, "B:\\Q39P")
	var pending *editor.Intent
	for pending == nil {
		var e error
		s, pending, _, e = run.Step(context.Background(), s, 16)
		if e != nil {
			t.Fatal(e)
		}
	}
	if run.Snapshot().AppliedWords != 3 {
		t.Fatal("parent effects missing before IO")
	}
	before := s.Document().Revision()
	request := run.Snapshot().Machine.NeedProgram
	request.Name[0].Value = 'Z'
	if e := f.dir.Close(); e != nil {
		t.Fatal(e)
	}
	failure := perform(pending)
	if failure.Err == nil {
		t.Fatal("actual closed root read succeeded")
	}
	var e error
	var p editor.MacroProgress
	s, p, e = run.Resume(s, failure)
	if e == nil || p.State != "failed" || s.Document().Revision() != before || asciiText(t, s) != "D1SENT DIRTY1P39" {
		t.Fatalf("host failure became handler/rollback %+v %v", p, e)
	}
	var vmFailure *vm.Failure
	if !errors.As(e, &vmFailure) || vmFailure.Code != "HostFailure" {
		t.Fatal("host failure became original CommandError", e)
	}
	if _, _, e = run.Resume(s, failure); e == nil {
		t.Fatal("late child read accepted")
	}
}

func TestCapturedLoaderCloseCannotBeRebasedByPublicDirectory(t *testing.T) {
	f := setup(t)
	base := load(t, f)
	raw, e := os.ReadFile("../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(filepath.Join(f.path, "M38.WPM"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	s := text(t, key(t, base, editor.Macro), "B:\\M38")
	s, i := submit(t, s)
	other, e := storage.OpenDirectory(f.path)
	if e != nil {
		t.Fatal(e)
	}
	defer other.Close()
	if e = f.dir.Close(); e != nil {
		t.Fatal(e)
	}
	*i.Directory = *other
	result := editor.ExecuteMacroRead(i)
	if result.Err == nil {
		t.Fatal("public open equal-root wrapper bypassed accepted Close")
	}
	s, _ = done(t, s, result)
	if s.MacroSource() != nil || s.Snapshot().Mode != editor.Editing {
		t.Fatal("closed read became acquisition")
	}
}
func TestNestedMissingConditionUsesActualAcquisition(t *testing.T) {
	root := "../../docs/research/continuation/macro-quit/runs/wp39-nested-02"
	s, f := twoBuffers(t, root, "nested-1")
	s = key(t, s, editor.SwitchDocument)
	raw, e := os.ReadFile(root + "/input/Q39P.WPM")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(filepath.Join(f.path, "Q39P.WPM"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	s, run := openMacro(t, s, "B:\\Q39P")
	var pending *editor.Intent
	for pending == nil {
		s, pending, _, e = run.Step(context.Background(), s, 16)
		if e != nil {
			t.Fatal(e)
		}
	}
	actual := perform(pending)
	if !errors.Is(actual.Err, os.ErrNotExist) {
		t.Fatal("real expected missing acquisition", actual.Err)
	}
	// Arbitrary host diagnostic causes are not universally cloned. Mutating that
	// diagnostic cannot change the privately captured actual missing classification.
	var pathError *os.PathError
	if errors.As(actual.Err, &pathError) {
		pathError.Err = os.ErrPermission
	}
	s, _, e = run.Resume(s, actual)
	if e != nil {
		t.Fatal(e)
	}
	s = runMacro(t, s, run)
	if asciiText(t, s) != "D1SENT DIRTY1P39PARENTERR" {
		t.Fatal("actual missing condition became host error or parent continuation")
	}
	// This is a derived component-negative branch, not an original39 execution.
}
func TestNestedResumePrivateRequestAndCopiedObservations(t *testing.T) {
	root := "../../docs/research/continuation/macro-quit/runs/wp39-nested-02"
	s, f := twoBuffers(t, root, "nested-1")
	s = key(t, s, editor.SwitchDocument)
	for _, file := range []string{"Q39P", "Q39C"} {
		raw, e := os.ReadFile(root + "/input/" + file + ".WPM")
		if e != nil {
			t.Fatal(e)
		}
		if e = os.WriteFile(filepath.Join(f.path, file+".WPM"), raw, 0600); e != nil {
			t.Fatal(e)
		}
	}
	s, run := openMacro(t, s, "B:\\Q39P")
	var pending *editor.Intent
	var e error
	for pending == nil {
		s, pending, _, e = run.Step(context.Background(), s, 16)
		if e != nil {
			t.Fatal(e)
		}
	}
	original := run.Snapshot().Pending
	request := run.Snapshot().Machine.NeedProgram
	request.Name[0].Value = 'Z'
	pending.Name = "ALTERED.WPM"
	*pending.Directory = storage.Directory{}
	broken := perform(pending)
	if _, _, e = run.Resume(s, broken); e == nil || run.Snapshot().Pending.Operation != original.Operation {
		t.Fatal("modified read intent consumed VM request")
	}
	result := perform(original)
	wrong := result
	wrong.Operation++
	if _, _, e = run.Resume(s, wrong); e == nil {
		t.Fatal("wrong read envelope accepted")
	}
	s, _, e = run.Resume(s, result)
	if e != nil {
		t.Fatal(e)
	}
	before := s.Document().Revision()
	if _, _, e = run.Resume(s, result); e == nil || s.Document().Revision() != before {
		t.Fatal("duplicate nested read accepted")
	}
	s = runMacro(t, s, run)
	if asciiText(t, s) != "D1SENT DIRTY1P39C39" {
		t.Fatal("copied request retargeted child")
	}
}
func TestUnsupportedMacroSourcePreservedBeforeEffects(t *testing.T) {
	for _, fixturePath := range []string{
		"../../docs/research/continuation/macro-session/runs/wp38-internal-cancel-02/input/M38.WPM",
		"../../docs/research/continuation/macro-session/runs/wp38-stop-default-02/input/M38.WPM",
		"../../docs/research/continuation/macro-session/runs/wp38-stop-on-02/input/M38.WPM",
		"../../docs/research/continuation/macro-session/runs/wp38-stop-off-01/input/M38.WPM",
	} {
		t.Run(filepath.Base(filepath.Dir(filepath.Dir(fixturePath))), func(t *testing.T) {
			ready, f := readyMacro(t)
			ready = key(t, ready, editor.CancelOperation)
			raw, e := os.ReadFile(fixturePath)
			if e != nil {
				t.Fatal(e)
			}
			if e = os.WriteFile(filepath.Join(f.path, "UNSUPPORTED.WPM"), raw, 0600); e != nil {
				t.Fatal(e)
			}
			before := ready.Document().Revision()
			ready = text(t, key(t, ready, editor.Macro), "B:\\UNSUPPORTED")
			ready, i := submit(t, ready)
			ready, _ = done(t, ready, perform(i))
			next, run, e := ready.StartMacro(vm.DefaultLimits())
			if e == nil || run != nil || next.Document().Revision() != before || !bytes.Equal(next.MacroSource().Export(), raw) {
				t.Fatal("unsupported source executed/disappeared")
			}
			next = key(t, next, editor.CancelOperation)
			if next.Snapshot().Mode != editor.Editing {
				t.Fatal("unstarted host discard")
			}
		})
	}
}

func TestUnsupportedSearchIsNotSyntheticOriginalNotFound(t *testing.T) {
	ledgerRaw, e := os.ReadFile("../../internal/macro/wpm/testdata/original-fixtures.json")
	if e != nil {
		t.Fatal(e)
	}
	var parsed map[string]json.RawMessage
	if e = json.Unmarshal(ledgerRaw, &parsed); e != nil {
		t.Fatal(e)
	}
	var exports []struct {
		Path string `json:"path"`
		Case string `json:"case_id"`
	}
	if e = json.Unmarshal(parsed["wpm_exports"], &exports); e != nil {
		t.Fatal(e)
	}
	selected := ""
	for _, v := range exports {
		if v.Case == "CMD51-178" {
			selected = v.Path
			break
		}
	}
	if selected == "" {
		t.Fatal("actual search WPM fixture absent")
	}
	raw, e := os.ReadFile("../../" + selected)
	if e != nil {
		t.Fatal(e)
	}
	ready, f := readyMacro(t)
	ready = key(t, ready, editor.CancelOperation)
	if e = os.WriteFile(filepath.Join(f.path, "SEARCH.WPM"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	before := ready.Document().Revision()
	ready = text(t, key(t, ready, editor.Macro), "B:\\SEARCH")
	ready, i := submit(t, ready)
	ready, _ = done(t, ready, perform(i))
	next, run, e := ready.StartMacro(vm.DefaultLimits())
	if e == nil || run != nil || next.Document().Revision() != before || !bytes.Equal(next.MacroSource().Export(), raw) {
		t.Fatal("unimplemented editor search was modeled as NotFound")
	}
}
func TestMacroContinuationCannotFollowChangedSourceGetters(t *testing.T) {
	ready, _ := readyMacro(t)
	s, run, e := ready.StartMacro(vm.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	*s.Document() = document.Document{}
	*s.Source() = storage.Document{}
	*s.MacroSource() = storage.Macro{}
	s = runMacro(t, s, run)
	if asciiText(t, s) != "ABCABCD" || !s.Snapshot().Dirty {
		t.Fatal("public wrappers retargeted actual execution")
	}
	s = key(t, s, editor.SwitchDocument)
	source1, _ := s.SourceOnScreen(1)
	native1, _ := s.NativeOnScreen(1)
	*source1 = storage.Document{}
	*native1 = document.Document{}
	first, _ := s.NativeOnScreen(1)
	raw, _ := first.Export()
	if len(raw) == 0 {
		t.Fatal("inactive-buffer getter retargeted state")
	}
}

func TestMacroNativeCandidateUsesActualLoadedSourcePublication(t *testing.T) {
	ready, f := readyMacro(t)
	s, run, e := ready.StartMacro(vm.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	s = runMacro(t, s, run)
	macroBefore := s.MacroSource().Export()
	sourceBefore := s.Source().Identity()
	native := s.Document().Revision()
	raw, _ := s.Document().Export()
	s, i := queued(t, s, "MACRESULT")
	if i.Kind != editor.PublishCandidate || i.Document.Identity() != sourceBefore {
		t.Fatal("macro used another publication/source path")
	}
	s, _ = done(t, s, perform(i))
	written, e := os.ReadFile(filepath.Join(f.path, "MACRESULT"))
	if e != nil || !bytes.Equal(raw, written) || s.Snapshot().Dirty || s.Snapshot().SavedRevision != native {
		t.Fatal("actual candidate save mismatch")
	}
	macroAfter, e := os.ReadFile(filepath.Join(f.path, "M38.WPM"))
	if e != nil || !bytes.Equal(macroBefore, macroAfter) {
		t.Fatal("macro source was written")
	}
	sourceAfter, e := os.ReadFile(filepath.Join(f.path, "ORIGIN"))
	if e != nil || !bytes.Equal(sourceAfter, f.raw) || s.Source().Identity() != sourceBefore {
		t.Fatal("document source guard rebased/modified")
	}
}
func TestMacroModePreservesEachBuffersActualState(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	s = key(t, s, editor.Delete)
	entry, e := s.History().Entry(0)
	if e != nil {
		t.Fatal(e)
	}
	source := s.Source().Identity()
	revision := s.Document().Revision()
	s = key(t, s, editor.SwitchDocument)
	if s.Snapshot().Screen != 2 || s.Source() != nil {
		t.Fatal("screen state constructor pretended native document")
	}
	s = key(t, s, editor.SwitchDocument)
	after, e := s.History().Entry(0)
	if e != nil || !bytes.Equal(entry.Native, after.Native) || s.Document().Revision() != revision || s.Source().Identity() != source || !s.Snapshot().Dirty || s.Snapshot().HistoryCountKnown {
		t.Fatal("screen switch cleared native/history/source or manufactured global count")
	}
	expectRefusal(t, s, editor.Event{Command: editor.F1})
}
