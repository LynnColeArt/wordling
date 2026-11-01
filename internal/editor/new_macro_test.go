package editor_test

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/binary"
	"errors"
	"fmt"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/editor"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
)

func newMacroInput(t *testing.T, source string) (editor.Session, string) {
	t.Helper()
	s, _, root := freshNew(t)
	raw, err := os.ReadFile(source)
	if err != nil {
		t.Fatal(err)
	}
	if err = os.WriteFile(filepath.Join(root, "ROOT.WPM"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	return s, root
}
func newMacroReady(t *testing.T, s editor.Session) editor.Session {
	t.Helper()
	s = key(t, s, editor.Macro)
	s = text(t, s, "ROOT")
	s, i := submit(t, s)
	if i.Kind != editor.ReadMacro || i.Repeat != 1 || i.Document != nil || i.Destination != nil {
		t.Fatal("root authority", i)
	}
	s, _ = done(t, s, editor.ExecuteMacroRead(i))
	if s.Snapshot().Mode != editor.MacroReady {
		t.Fatal(s.Snapshot())
	}
	return s
}
func newMacroRun(t *testing.T, s editor.Session, run *editor.MacroExecution, quota uint32) editor.Session {
	t.Helper()
	for count := 0; !run.Snapshot().Terminal; count++ {
		if count >= 4096 {
			t.Fatal("bounded macro driver")
		}
		before := run.Snapshot().TotalSteps
		next, i, p, err := run.Step(context.Background(), s, quota)
		if err != nil || i != nil || p.TotalSteps-before > uint64(quota) {
			t.Fatalf("step %v %+v %+v", err, i, p)
		}
		s = next
	}
	return s
}
func TestNewMacroGenuineFLOWAndFirstPublication(t *testing.T) {
	for _, sample := range []string{"03", "04"} {
		for _, quota := range []uint32{1, 16} {
			t.Run(fmt.Sprintf("%s-q%d", sample, quota), func(t *testing.T) {
				root := "../../docs/research/reference-runs/2026-10-29-advanced-" + sample + "/CMD51-205/"
				s, d, path := freshNew(t)
				input, err := os.ReadFile(root + "FLOW.WPM")
				if err != nil {
					t.Fatal(err)
				}
				if err = os.WriteFile(filepath.Join(path, "ROOT.WPM"), input, 0600); err != nil {
					t.Fatal(err)
				}
				before := s.Snapshot()
				birth := s.Document().Birth()
				s = newMacroReady(t, s)
				if s.Source() != nil || s.Snapshot().NativeRevision != before.NativeRevision || s.Document().Birth() != birth || s.Snapshot().Dirty {
					t.Fatal("acquisition edited New")
				}
				ready := s
				s, run, err := s.StartMacro(vm.DefaultLimits())
				if err != nil {
					t.Fatal(err)
				}
				// Persistent Session branches are legitimate; neither revokes the other.
				fork, second, err := ready.StartMacro(vm.DefaultLimits())
				if err != nil {
					t.Fatal(err)
				}
				if _, _, _, err = run.Step(context.Background(), fork, quota); err == nil {
					t.Fatal("foreign driver target")
				}
				s = newMacroRun(t, s, run, quota)
				fork = newMacroRun(t, fork, second, quota)
				raw, _ := s.Document().Export()
				other, _ := fork.Document().Export()
				if !bytes.Equal(raw, other) || string(raw[324:]) != "TRUEFALSETAIL" {
					t.Fatalf("actual output %q", raw[324:])
				}
				snap := s.Snapshot()
				p := run.Snapshot()
				if snap.Revision != 14 || snap.Gap != 13 || !snap.Dirty || snap.Name != "" || s.Source() != nil || snap.NewPhase != editor.NewUnpublished || snap.GenesisRevision != before.GenesisRevision || s.Document().Birth() != birth || p.State != "complete" || p.Repeat != 1 || p.Completed != 1 || p.AppliedWords != 13 || p.ReceiptCount != 14 || p.DisplaySuppressed {
					t.Fatalf("terminal %+v %+v", snap, p)
				}
				receipts, err := run.Receipts(0, 14)
				if err != nil {
					t.Fatal(err)
				}
				ascii := 0
				display := 0
				for _, r := range receipts {
					if !r.Applied || !r.Result.MayHaveEffects || r.Err != nil || r.Screen != 1 || len(r.Effect.Words) != 1 || r.Effect.Source != sha256.Sum256(input) {
						t.Fatal(r)
					}
					w := r.Effect.Words[0]
					offset := int(w.Span.Offset)
					if w.Span.Length != 2 || offset < 75 || offset+2 > len(input) || (offset-75)%2 != 0 || binary.LittleEndian.Uint16(input[offset:]) != w.Value {
						t.Fatal("source span", r)
					}
					if r.Effect.Kind == "display-off" {
						display++
						if r.Before != r.After || r.BeforeGap != r.AfterGap {
							t.Fatal(r)
						}
					} else {
						ascii++
						if r.After != r.Before+1 || r.AfterGap != r.BeforeGap+1 {
							t.Fatal(r)
						}
					}
				}
				if ascii != 13 || display != 1 {
					t.Fatal(ascii, display)
				}
				want, err := os.ReadFile(root + "FLOWOUT.WP5")
				if err != nil {
					t.Fatal(err)
				}
				if len(raw) != 337 {
					t.Fatal(len(raw))
				}
				compareMacroNative(t, raw, want)
				current := s.Snapshot()
				history := s.History().Revision()
				s, pub := firstRequest(t, s, d, "FIRST")
				s = finishFirst(t, s, pub)
				actual, err := os.ReadFile(filepath.Join(path, "FIRST"))
				if err != nil || !bytes.Equal(actual, raw) || s.Document().Birth() != birth || s.Snapshot().NativeRevision != current.NativeRevision || s.Snapshot().GenesisRevision != before.GenesisRevision || s.Snapshot().Gap != 13 || s.History().Revision() == history {
					t.Fatal("real first publication/read/history", err)
				}
				compareMacroNative(t, actual, want)
				if _, err = s.WithMacroRepeat(1); err == nil {
					t.Fatal("anchored New repeat")
				}
				expectRefusal(t, s, editor.Event{Command: editor.SwitchDocument})

				afterInput, _ := os.ReadFile(filepath.Join(path, "ROOT.WPM"))
				if !bytes.Equal(input, afterInput) {
					t.Fatal("source changed")
				}
			})
		}
	}
}

const newThirdMacro = "../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM"

func TestNewMacroDistinctRootAndCurrentDriver(t *testing.T) {
	s, _ := newMacroInput(t, newThirdMacro)
	ready := newMacroReady(t, s)
	s, run, err := ready.StartMacro(vm.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	old := s
	alias := *run
	s, _, _, err = run.Step(context.Background(), s, 1)
	if err != nil {
		t.Fatal(err)
	}
	if _, _, _, err = alias.Step(context.Background(), old, 1); err == nil {
		t.Fatal("copied handle accepted stale Session")
	}
	s = newMacroRun(t, s, &alias, 16)
	if asciiText(t, s) != "ABC" || run.Snapshot().AppliedWords != 3 {
		t.Fatal("distinct source was replaced", run.Snapshot())
	}
	if _, _, err = run.HostStop(s, "late"); err == nil {
		t.Fatal("terminal reused")
	}
	expectRefusal(t, s, editor.Event{Command: editor.Macro})
	expectRefusal(t, s, editor.Event{Command: editor.SwitchDocument})
	if _, err = s.WithMacroRepeat(1); err == nil {
		t.Fatal("New repeat broadened")
	}
	// The genuine New startup empty-history guard remains in force.
	base, _, _ := freshNew(t)
	expectRefusal(t, base, editor.Event{Command: editor.F1})
}
func TestNewMacroPublicPristineExclusions(t *testing.T) {
	for _, variant := range []string{"typed", "edited-empty", "typeover", "reveal", "block", "home", "name-cancel", "save-cancel", "ready-cancel", "missing", "pending-cancel"} {
		t.Run(variant, func(t *testing.T) {
			s, _ := newMacroInput(t, newThirdMacro)
			switch variant {
			case "typed":
				s = text(t, s, "A")
			case "edited-empty":
				s = text(t, s, "A")
				s = key(t, s, editor.Left)
				s = key(t, s, editor.Delete)
				if s.Document().TokenCount() != 0 {
					t.Fatal("edited-empty precondition")
				}
			case "typeover":
				s = key(t, s, editor.Insert)
			case "reveal":
				s = key(t, s, editor.Reveal)
			case "block":
				s = key(t, key(t, s, editor.Reveal), editor.Block)
			case "home":
				s = key(t, s, editor.Home)
			case "name-cancel":
				s = key(t, key(t, s, editor.Macro), editor.F1)
			case "save-cancel":
				s = key(t, key(t, s, editor.Save), editor.F1)
			case "ready-cancel":
				s = key(t, newMacroReady(t, s), editor.CancelOperation)
			case "missing":
				s = text(t, key(t, s, editor.Macro), "MISSING")
				var i *editor.Intent
				s, i = submit(t, s)
				s, _ = done(t, s, editor.ExecuteMacroRead(i))
				if s.Snapshot().Mode != editor.MacroError {
					t.Fatal(s.Snapshot())
				}
				s = key(t, s, editor.F1)
			case "pending-cancel":
				s = text(t, key(t, s, editor.Macro), "ROOT")
				var i *editor.Intent
				s, i = submit(t, s)
				r := editor.ExecuteMacroRead(i)
				s = key(t, s, editor.CancelOperation)
				expectRefusal(t, s, editor.Event{Command: editor.Enter})
				s, _ = done(t, s, r)
				if s.Snapshot().Mode == editor.MacroReady || s.Snapshot().Detached.Applied {
					t.Fatal("late acquisition attached")
				}
				s = key(t, s, editor.F1)
			}
			before := s.Snapshot()
			native, _ := s.Document().Export()
			expectRefusal(t, s, editor.Event{Command: editor.Macro})
			after, _ := s.Document().Export()
			if !bytes.Equal(native, after) || s.Snapshot().Revision != before.Revision {
				t.Fatal("refusal edited")
			}
		})
	}
	var zero editor.Session
	expectRefusal(t, zero, editor.Event{Command: editor.Macro})
}
func TestNewMacroRootWrappersReceiptsAndLifetimes(t *testing.T) {
	s, path := newMacroInput(t, newThirdMacro)
	s = text(t, key(t, s, editor.Macro), "ROOT")
	s, i := submit(t, s)
	result := editor.ExecuteMacroRead(i)
	for _, field := range []string{"repeat", "native", "name", "screen", "operation", "directory", "candidate"} {
		t.Run(field, func(t *testing.T) {
			altered := *i
			switch field {
			case "repeat":
				altered.Repeat = 3
			case "native":
				altered.NativeRevision = (editor.Session{}).Snapshot().NativeRevision
			case "name":
				altered.Name = "OTHER.WPM"
			case "screen":
				altered.Screen = 2
			case "operation":
				altered.Operation++
			case "directory":
				altered.Directory = nil
			case "candidate":
				altered.Candidate = []byte("fake")
			}
			r := editor.ExecuteMacroRead(&altered)
			if r.Err == nil {
				t.Fatal("wrapper accepted")
			}
		})
	}
	for _, kind := range []string{"foreign-op", "borrowed-macro", "forged-error", "absent-observation"} {
		t.Run(kind, func(t *testing.T) {
			r := result
			switch kind {
			case "foreign-op":
				r.Operation++
			case "borrowed-macro":
				r.Macro = nil
			case "forged-error":
				r.Err = fmt.Errorf("forged")
			case "absent-observation":
				r = editor.Result{Kind: i.Kind, Operation: i.Operation, Revision: i.Revision, Macro: result.Macro}
			}
			next, _, err := s.Reduce(editor.Event{Command: editor.Complete, Result: &r})
			if err == nil || next.Snapshot().Mode != editor.Waiting || next.Snapshot().Pending.Operation != i.Operation {
				t.Fatal("forged completion consumed root", err)
			}
			// The authentic pending request remains usable after each rejected result.
			next, _ = done(t, next, result)
			if next.Snapshot().Mode != editor.MacroReady {
				t.Fatal(next.Snapshot())
			}
		})
	}
	// Equal-byte independent New is not the issued target.
	other, _ := newMacroInput(t, newThirdMacro)
	other = text(t, key(t, other, editor.Macro), "ROOT")
	other, _ = submit(t, other)
	if _, _, err := other.Reduce(editor.Event{Command: editor.Complete, Result: &result}); err == nil {
		t.Fatal("foreign root receipt borrowed")
	}
	ready, _ := done(t, s, result)
	*ready.MacroSource() = storage.Macro{}
	*ready.Document() = document.Document{}
	*result.Macro = storage.Macro{}
	active, run, err := ready.StartMacro(vm.DefaultLimits())
	if err != nil {
		t.Fatal("getter changed private source", err)
	}
	if err = os.Remove(filepath.Join(path, "ROOT.WPM")); err != nil {
		t.Fatal(err)
	}
	active = newMacroRun(t, active, run, 16)
	if asciiText(t, active) != "ABC" {
		t.Fatal("execution reread source")
	}
	// Closing the actual root before acquisition produces a truthful failure.
	closed, dir, root := freshNew(t)
	input, _ := os.ReadFile(newThirdMacro)
	if err = os.WriteFile(filepath.Join(root, "ROOT.WPM"), input, 0600); err != nil {
		t.Fatal(err)
	}
	closed = text(t, key(t, closed, editor.Macro), "ROOT")
	closed, i = submit(t, closed)
	if err = dir.Close(); err != nil {
		t.Fatal(err)
	}
	r := editor.ExecuteMacroRead(i)
	if r.Err == nil {
		t.Fatal("closed root read")
	}
	closed, _ = done(t, closed, r)
	if closed.Snapshot().Mode != editor.Editing || closed.Source() != nil || closed.Snapshot().Dirty {
		t.Fatal(closed.Snapshot())
	}
	expectRefusal(t, closed, editor.Event{Command: editor.Macro})
}

// Host-derived adversaries reuse an approved public WPM header and existing
// admitted words. These are not original artifacts or guessed CHAIN encodings.
func newHostMacro(t *testing.T, parts ...any) (editor.Session, string) {
	t.Helper()
	s, _, root := freshNew(t)
	base, err := os.ReadFile(newThirdMacro)
	if err != nil {
		t.Fatal(err)
	}
	raw := append([]byte(nil), base[:70]...)
	word := func(w uint16) { raw = append(raw, byte(w), byte(w>>8)) }
	for _, part := range parts {
		switch v := part.(type) {
		case string:
			for _, c := range []byte(v) {
				word(uint16(c))
			}
		case uint16:
			word(v)
		default:
			t.Fatal("test source type")
		}
	}
	word(0)
	if err = os.WriteFile(filepath.Join(root, "ROOT.WPM"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	return s, root
}
func TestNewMacroNestIsHostFailureBeforeChildIOAndPartialEffectsRemain(t *testing.T) {
	for _, handler := range []bool{false, true} {
		t.Run(fmt.Sprint(handler), func(t *testing.T) {
			parts := []any{uint16(0xfc0c), "BEFORE", uint16(0xfc18), "CHILD~AFTER"}
			if handler {
				parts = append([]any{uint16(0xfc1c), uint16(0xfc14), "ERR~~"}, parts...)
				parts = append(parts, uint16(0xfc16), "ERR~HANDLED")
			}
			s, root := newHostMacro(t, parts...)
			// Existing child makes accidental admission observable even if it could read.
			child, _ := os.ReadFile(newThirdMacro)
			if err := os.WriteFile(filepath.Join(root, "CHILD.WPM"), child, 0600); err != nil {
				t.Fatal(err)
			}
			s = newMacroReady(t, s)
			s, run, err := s.StartMacro(vm.DefaultLimits())
			if err != nil {
				t.Fatal(err)
			}
			s = newMacroRun(t, s, run, 1)
			p := run.Snapshot()
			var failure *vm.Failure
			if p.State != "failed" || !errors.As(p.Machine.Err, &failure) || failure.Code != "HostFailure" || p.Pending != nil || p.Machine.NeedProgram != nil || p.AppliedWords != 6 || asciiText(t, s) != "BEFORE" || !s.Snapshot().Dirty || s.Source() != nil {
				t.Fatalf("host failure/partial truth %+v %v", p, p.Machine.Err)
			}
			if _, _, err = run.Resume(s, editor.Result{}); err == nil {
				t.Fatal("New child reply admitted")
			}
		})
	}
}
func TestNewMacroStaticUnknownRefusalIsBeforeAllEffects(t *testing.T) {
	s, _ := newHostMacro(t, "BEFORE", uint16(0xfc3a), "AFTER")
	s = newMacroReady(t, s)
	before := s.Snapshot()
	next, run, err := s.StartMacro(vm.DefaultLimits())
	var failure *vm.Failure
	if err == nil || run != nil || !errors.As(err, &failure) || failure.Code != "UnsupportedImage" || next.Snapshot().NativeRevision != before.NativeRevision || next.Snapshot().Dirty {
		t.Fatal("UNKNOWN static refusal", err)
	}
	if _, run, err = next.StartMacro(vm.DefaultLimits()); err == nil || run != nil {
		t.Fatal("discarded New admission reused")
	}
	next = key(t, next, editor.CancelOperation)
	expectRefusal(t, next, editor.Event{Command: editor.Macro})
}
func TestNewMacroBudgetsStopAndCancellationKeepActualEffects(t *testing.T) {
	for _, mode := range []string{"words", "steps", "stop", "context"} {
		t.Run(mode, func(t *testing.T) {
			s, _ := newHostMacro(t, uint16(0xfc0c), "ABCDEFGHIJ")
			s = newMacroReady(t, s)
			limits := vm.DefaultLimits()
			if mode == "words" {
				limits.OutputWords = 3
			}
			if mode == "steps" {
				limits.Steps = 20
			}
			s, run, err := s.StartMacro(limits)
			if err != nil {
				t.Fatal(err)
			}
			if mode == "stop" || mode == "context" {
				for run.Snapshot().AppliedWords < 2 {
					s, _, _, err = run.Step(context.Background(), s, 1)
					if err != nil {
						t.Fatal(err)
					}
				}
				if mode == "stop" {
					s, _, err = run.HostStop(s, "bounded operator stop")
				} else {
					ctx, cancel := context.WithCancel(context.Background())
					cancel()
					s, _, _, err = run.Step(ctx, s, 1)
				}
				if err != nil {
					t.Fatal(err)
				}
			} else {
				s = newMacroRun(t, s, run, 1)
			}
			p := run.Snapshot()
			if !p.Terminal || p.State == "complete" || p.DisplaySuppressed || p.Pending != nil || uint64(len(asciiText(t, s))) != p.AppliedWords || !s.Snapshot().Dirty || s.Source() != nil || s.Snapshot().NewPhase != editor.NewUnpublished {
				t.Fatalf("partial/budget %+v %+v", s.Snapshot(), p)
			}
			if p.TotalWords > limits.OutputWords || p.TotalSteps > limits.Steps {
				t.Fatal("budget reset", p)
			}
			s = text(t, s, "Z")
			if !strings.HasSuffix(asciiText(t, s), "Z") {
				t.Fatal("terminal did not release ordinary editing")
			}
		})
	}
}

func TestNewMacroFirstPublicationFailureCancelRetryAndUnknownRemainReal(t *testing.T) {
	for _, variant := range []string{"missing", "same-bytes-new-inode", "metadata", "closed", "cancel-read", "cancel-publish", "stale-candidate"} {
		t.Run(variant, func(t *testing.T) {
			s, d, path := freshNew(t)
			input, err := os.ReadFile(newThirdMacro)
			if err != nil {
				t.Fatal(err)
			}
			if err = os.WriteFile(filepath.Join(path, "ROOT.WPM"), input, 0600); err != nil {
				t.Fatal(err)
			}
			s = newMacroReady(t, s)
			s, run, err := s.StartMacro(vm.DefaultLimits())
			if err != nil {
				t.Fatal(err)
			}
			s = newMacroRun(t, s, run, 16)
			before := s.Snapshot()
			birth := s.Document().Birth()
			raw, _ := s.Document().Export()
			s, pub := firstRequest(t, s, d, "FIRST")
			history := s.History().Revision()
			if variant == "stale-candidate" {
				fake := *pub
				fake.Candidate = append([]byte(nil), pub.Candidate...)
				fake.Candidate[324] ^= 1
				r := editor.ExecuteNewPublication(&fake)
				if r.Err == nil {
					t.Fatal("candidate redirected")
				}
				if _, err = os.Stat(filepath.Join(path, "FIRST")); !os.IsNotExist(err) {
					t.Fatal("refused candidate wrote")
				}
				s = finishFirst(t, s, pub)
				return
			}
			result := editor.ExecuteNewPublication(pub)
			if variant == "cancel-publish" {
				s = key(t, s, editor.CancelOperation)
				s, _ = done(t, s, result)
				if s.Snapshot().NewPhase != editor.PublicationUncertain || s.Source() != nil || !s.Snapshot().Dirty || s.Snapshot().Name != "" || s.Snapshot().Detached.Applied {
					t.Fatal("cancel claimed rollback/source", s.Snapshot())
				}
				expectRefusal(t, s, editor.Event{Command: editor.RetryFirstRead})
				expectRefusal(t, s, editor.Event{Command: editor.Macro})
				file, err := os.ReadFile(filepath.Join(path, "FIRST"))
				if err != nil || !bytes.Equal(file, raw) {
					t.Fatal("actual publication truth", err)
				}
				return
			}
			s, read := done(t, s, result)
			file := filepath.Join(path, "FIRST")
			switch variant {
			case "missing":
				if err = os.Rename(file, file+".held"); err != nil {
					t.Fatal(err)
				}
			case "same-bytes-new-inode":
				if err = os.Rename(file, file+".held"); err != nil {
					t.Fatal(err)
				}
				if err = os.WriteFile(file, raw, 0600); err != nil {
					t.Fatal(err)
				}
			case "metadata":
				if err = os.Chmod(file, 0644); err != nil {
					t.Fatal(err)
				}
			case "closed":
				if err = d.Close(); err != nil {
					t.Fatal(err)
				}
			case "cancel-read":
				s = key(t, s, editor.CancelOperation)
			}
			if variant != "cancel-read" {
				s, _ = done(t, s, editor.ExecuteFirstRead(read))
			}
			if s.Snapshot().NewPhase != editor.PublishedUnbound || s.Source() != nil || !s.Snapshot().Dirty || s.Snapshot().Name != "" || s.Document().Birth() != birth || s.Snapshot().NativeRevision != before.NativeRevision || s.History().Revision() != history {
				t.Fatal("failed read replaced native/history", s.Snapshot())
			}
			next, retry, err := s.Reduce(editor.Event{Command: editor.RetryFirstRead})
			if err != nil || retry.Kind != editor.BindNewSource || retry.RequestKey() == read.RequestKey() {
				t.Fatal("retry not fresh readonly", err)
			}
			next, _ = done(t, next, editor.ExecuteFirstRead(retry))
			want := editor.PublishedUnbound
			if variant == "cancel-read" {
				want = editor.NewAnchored
			}
			after, _ := next.Document().Export()
			if next.Snapshot().NewPhase != want || !bytes.Equal(after, raw) || next.Document().Birth() != birth {
				t.Fatal("retry invented publication or replaced live New")
			}
			_, err = next.Document().OriginalExport()
			var failure *document.Failure
			if !errors.As(err, &failure) || failure.Category != document.NoLoadedOriginal {
				t.Fatal("New became Loaded", err)
			}
		})
	}
}
