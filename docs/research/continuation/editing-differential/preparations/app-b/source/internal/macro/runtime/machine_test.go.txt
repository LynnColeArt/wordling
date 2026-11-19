package runtime_test

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/binary"
	"errors"
	"path/filepath"
	"sync"
	"testing"

	mac "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

// Derived native inputs exist in test memory only. This is not a production WPM
// writer, original-app fixture or a substitute source/effect format.
func native(t testing.TB, parts ...any) []byte {
	t.Helper()
	base := originalABC(t)
	out := append([]byte(nil), base[:70]...)
	for _, part := range parts {
		switch v := part.(type) {
		case uint16:
			out = binary.LittleEndian.AppendUint16(out, v)
		case string:
			for n := range v {
				out = binary.LittleEndian.AppendUint16(out, uint16(v[n]))
			}
		default:
			t.Fatalf("bad test input %T", part)
		}
	}
	return append(out, 0, 0)
}
func sink() *traceSink              { return &traceSink{policy: fullPolicy()} }
func textTrace(s *traceSink) string { return literalProjection(s.receipts, nil) }

func TestFrameHandlersDerivedControlOnly(t *testing.T) {
	// QUIT is replaced in memory by DISPLAY OFF solely to test already observed
	// handler/frame plumbing independently of the original-source tests. These
	// derived inputs do not count as native original conformance results.
	for _, id := range []string{"CMD51-206", "CMD51-210", "CMD51-212", "CMD51-213"} {
		t.Run(id, func(t *testing.T) {
			a := corpus(t)
			var c originalCase
			for _, row := range a.Cases {
				if row.ID == id {
					c = row
				}
			}
			files := map[string]*wpm.Image{}
			sources := map[[32]byte][]byte{}
			for _, f := range a.Exports {
				if f.Case != id || f.Run != c.Run {
					continue
				}
				raw := readArtifact(t, f)
				B := binary.LittleEndian.Uint32(raw[4:8])
				for n := B; n+2 <= uint32(len(raw)); n += 2 {
					if binary.LittleEndian.Uint16(raw[n:n+2]) == 0xfc20 {
						binary.LittleEndian.PutUint16(raw[n:n+2], 0xfc0c)
					}
				}
				i := image(t, raw)
				files[filepath.Base(f.Path)] = i
				sources[i.SHA256()] = raw
			}
			s := sink()
			keys := 0
			s.apply = func(_ context.Context, e mac.Effect) (mac.EffectResult, error) {
				r := mac.EffectResult{Condition: mac.NoCondition, MayHaveEffects: true}
				if e.Kind == "key" {
					keys++
					if keys == 2 {
						r.Condition = mac.NotFound
					}
				}
				return r, nil
			}
			r := resolverFunc(func(_ context.Context, req mac.ProgramRequest) mac.Resolution {
				if nativeName(req.Name) == "C:\\OUT\\CHILD" && files["CHILD.WPM"] != nil {
					return mac.Resolution{State: "ready", Image: files["CHILD.WPM"]}
				}
				return mac.Resolution{State: "condition", Condition: mac.CommandError}
			})
			p, err := mac.Compile(files[c.Root], fullPolicy(), mac.DefaultLimits())
			if err != nil {
				t.Fatal(err)
			}
			m := newMachine(t, p, s, r, mac.DefaultLimits())
			result := drive(t, m, 1)
			if result.State != "complete" || literalProjection(s.receipts, sources) != c.Expected.Text {
				t.Fatal("derived frame/handler control", result, literalProjection(s.receipts, sources), c.Expected.Text)
			}
		})
	}
}

func TestPendingResumeCopiesAndExactOnce(t *testing.T) {
	raw := native(t, "P", uint16(0xfc18), "CHILD~R")
	childRaw := native(t, "C", uint16(0xfc22))
	child := image(t, childRaw)
	s := sink()
	calls := 0
	resolver := resolverFunc(func(_ context.Context, req mac.ProgramRequest) mac.Resolution {
		calls++
		if nativeName(req.Name) != "CHILD" {
			t.Fatal("request source")
		}
		req.Name[0].Value = 'Z'
		req.Parent = [32]byte{}
		return mac.Resolution{State: "pending"}
	})
	m := newMachine(t, program(t, raw, mac.DefaultLimits()), s, resolver, mac.DefaultLimits())
	r := drive(t, m, 5)
	if r.State != "waiting" || calls != 1 || textTrace(s) != "P" {
		t.Fatal(r, calls, textTrace(s))
	}
	id := r.NeedProgram.ID
	parent := sha256.Sum256(raw)
	if r.NeedProgram.Parent != parent || nativeName(r.NeedProgram.Name) != "CHILD" {
		t.Fatal("resolver argument alias")
	}
	r.NeedProgram.Name[0].Value = 'X'
	r.NeedProgram.ID = 999
	r.NeedProgram.Parent = [32]byte{}
	for n := 0; n < 3; n++ {
		next := m.Step(context.Background(), 1)
		if next.State != "waiting" || next.Steps != r.Steps || calls != 1 || nativeName(next.NeedProgram.Name) != "CHILD" || next.NeedProgram.Parent != parent {
			t.Fatal("waiting repeated effect/resolution or alias", next)
		}
	}
	if errorCode(m.Resume(id+1, mac.Resolution{State: "ready", Image: child})) != "StaleResume" {
		t.Fatal("wrong request accepted")
	}
	if errorCode(m.Resume(id, mac.Resolution{State: "pending"})) != "InvalidResolution" || m.State().State != "waiting" {
		t.Fatal("pending continuation changed")
	}
	if err := m.Resume(id, mac.Resolution{State: "ready", Image: child}); err != nil {
		t.Fatal(err)
	}
	// A caller may replace its Image wrapper after Resume; child compilation owns
	// its snapshot and must still execute C/RETURN rather than the replacement.
	*child = wpm.Image{}
	if errorCode(m.Resume(id, mac.Resolution{State: "ready", Image: image(t, childRaw)})) != "StaleResume" {
		t.Fatal("duplicate resume accepted")
	}
	result := drive(t, m, 1)
	if result.State != "complete" || textTrace(s) != "PCR" || calls != 1 {
		t.Fatal(result, textTrace(s), calls)
	}
	before := len(s.receipts)
	again := m.Step(context.Background(), 1)
	if again.State != "complete" || len(s.receipts) != before {
		t.Fatal("completed run replayed effects")
	}
}

func TestHostFailureReceiptsAndOwnFailureCopies(t *testing.T) {
	for _, may := range []bool{false, true} {
		t.Run(map[bool]string{false: "before-effects", true: "possible-effects"}[may], func(t *testing.T) {
			s := sink()
			host := errors.New("injected host failure")
			s.apply = func(context.Context, mac.Effect) (mac.EffectResult, error) {
				return mac.EffectResult{Condition: mac.CommandError, MayHaveEffects: may}, host
			}
			m := newMachine(t, program(t, native(t, "ABC"), mac.DefaultLimits()), s, nil, mac.DefaultLimits())
			r := drive(t, m, 4)
			if r.State != "failed" || errorCode(r.Err) != "HostFailure" || len(s.receipts) != 1 || s.receipts[0].Result.MayHaveEffects != may || !errors.Is(s.receipts[0].Err, host) || r.EmittedWords != 1 {
				t.Fatal("charged counters are not applied receipts", r, s.receipts)
			}
			r.Err.(*mac.Failure).Code = "forged"
			if errorCode(m.State().Err) != "HostFailure" {
				t.Fatal("returned failure aliases machine")
			}
			m.Step(context.Background(), 1)
			if len(s.receipts) != 1 {
				t.Fatal("host error replayed effect")
			}
		})
	}
	// Explicit original conditions are distinct from host errors and restricted to
	// qualified effect contexts, never interpreted from a host error's wording.
	s := sink()
	s.apply = func(context.Context, mac.Effect) (mac.EffectResult, error) {
		return mac.EffectResult{Condition: mac.NotFound, MayHaveEffects: true}, nil
	}
	m := newMachine(t, program(t, native(t, "A"), mac.DefaultLimits()), s, nil, mac.DefaultLimits())
	r := drive(t, m, 8)
	if r.State != "refused" || errorCode(r.Err) != "UnsupportedConditionContext" {
		t.Fatal(r)
	}
}

func TestResolverHostErrorDoesNotEnterOriginalHandler(t *testing.T) {
	raw := native(t, uint16(0xfc1c), uint16(0xfc14), "ERR~~P", uint16(0xfc18), "MISSING~BAD", uint16(0xfc16), "ERR~HANDLED")
	for _, host := range []bool{false, true} {
		t.Run(map[bool]string{false: "original-condition", true: "host-error"}[host], func(t *testing.T) {
			s := sink()
			resolver := resolverFunc(func(context.Context, mac.ProgramRequest) mac.Resolution {
				if host {
					return mac.Resolution{State: "host-error", Err: errors.New("not an original error")}
				}
				return mac.Resolution{State: "condition", Condition: mac.CommandError}
			})
			m := newMachine(t, program(t, raw, mac.DefaultLimits()), s, resolver, mac.DefaultLimits())
			r := drive(t, m, 3)
			if host {
				if r.State != "failed" || errorCode(r.Err) != "HostFailure" || textTrace(s) != "P" {
					t.Fatal(r, textTrace(s))
				}
			} else if r.State != "complete" || textTrace(s) != "PHANDLED" {
				t.Fatal(r, textTrace(s))
			}
		})
	}
}

func TestImageProgramEffectAndPolicyOwnership(t *testing.T) {
	raw := originalABC(t)
	i := image(t, raw)
	policy := fullPolicy()
	p, err := mac.Compile(i, policy, mac.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	policy.Keys[0] = 0x8020
	*i = wpm.Image{}
	s := sink()
	s.apply = func(_ context.Context, e mac.Effect) (mac.EffectResult, error) {
		e.Words[0].Value = 0
		e.Source = [32]byte{}
		e.At = wpm.Span{}
		return mac.EffectResult{Condition: mac.NoCondition}, nil
	}
	m := newMachine(t, p, s, nil, mac.DefaultLimits())
	other := program(t, native(t, "WRONG"), mac.DefaultLimits())
	*p = *other
	r := drive(t, m, 2)
	if r.State != "complete" || textTrace(s) != "ABC" {
		t.Fatal("whole wrapper/effect alias", r, textTrace(s))
	}
	for _, receipt := range s.receipts {
		if receipt.Effect.Source != sha256.Sum256(raw) {
			t.Fatal("program source retargeted")
		}
	}
}

func TestStopCancellationAndCallbackReentry(t *testing.T) {
	raw := native(t, "P", uint16(0xfc18), "CHILD~R")
	s := sink()
	calls := 0
	resolver := resolverFunc(func(context.Context, mac.ProgramRequest) mac.Resolution {
		calls++
		return mac.Resolution{State: "pending"}
	})
	m := newMachine(t, program(t, raw, mac.DefaultLimits()), s, resolver, mac.DefaultLimits())
	r := drive(t, m, 16)
	if r.State != "waiting" {
		t.Fatal(r)
	}
	id := r.NeedProgram.ID
	stopped := m.Stop("host safety only")
	if stopped.State != "stopped" || errorCode(stopped.Err) != "HostStop" || stopped.NeedProgram != nil {
		t.Fatal(stopped)
	}
	if errorCode(m.Resume(id, mac.Resolution{State: "ready", Image: image(t, native(t, "C"))})) != "StaleResume" {
		t.Fatal("stopped resumed")
	}
	m.Step(context.Background(), 1)
	if textTrace(s) != "P" || calls != 1 {
		t.Fatal("post-stop effects")
	}
	ctx, cancel := context.WithCancel(context.Background())
	s = sink()
	s.apply = func(context.Context, mac.Effect) (mac.EffectResult, error) {
		cancel()
		return mac.EffectResult{MayHaveEffects: true}, nil
	}
	m = newMachine(t, program(t, native(t, "ABC"), mac.DefaultLimits()), s, nil, mac.DefaultLimits())
	r = m.Step(ctx, 64)
	if r.State != "stopped" || errorCode(r.Err) != "HostCancelled" || textTrace(s) != "A" {
		t.Fatal("host cancellation mistaken for original Cancel", r, textTrace(s))
	}
	s = sink()
	var active *mac.Machine
	s.apply = func(context.Context, mac.Effect) (mac.EffectResult, error) {
		if errorCode(active.Step(context.Background(), 1).Err) != "Busy" || errorCode(active.Stop("reentrant").Err) != "Busy" {
			t.Fatal("callback reentry was accepted")
		}
		return mac.EffectResult{}, nil
	}
	active = newMachine(t, program(t, native(t, "AB"), mac.DefaultLimits()), s, nil, mac.DefaultLimits())
	r = drive(t, active, 8)
	if r.State != "complete" || textTrace(s) != "AB" {
		t.Fatal(r, textTrace(s))
	}
}

func TestIndependentMachinesConcurrent(t *testing.T) {
	raw := native(t, uint16(0xfc01), "N~0~", uint16(0xfc2b), uint16(0xfc34), "N~<3~", uint16(0xfc34), "N~", uint16(0xfc01), "N~", uint16(0xfc34), "N~+1~", uint16(0xfc11))
	p := program(t, raw, mac.DefaultLimits())
	var wg sync.WaitGroup
	for n := 0; n < 8; n++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			s := sink()
			m, err := mac.New(p, s, nil, mac.DefaultLimits())
			if err != nil {
				t.Error(err)
				return
			}
			r := drive(t, m, 3)
			if r.State != "complete" || textTrace(s) != "012" {
				t.Error("shared run variables", r, textTrace(s))
			}
		}()
	}
	wg.Wait()
}

func TestPendingHostErrorCopyAndInvalidResolution(t *testing.T) {
	s := sink()
	m := newMachine(t, program(t, native(t, uint16(0xfc18), "MISSING~BAD"), mac.DefaultLimits()), s, resolverFunc(func(context.Context, mac.ProgramRequest) mac.Resolution { return mac.Resolution{State: "pending"} }), mac.DefaultLimits())
	r := drive(t, m, 32)
	id := r.NeedProgram.ID
	if errorCode(m.Resume(id, mac.Resolution{State: "ready"})) != "InvalidResolution" || m.State().State != "waiting" {
		t.Fatal("invalid resolution changed pending state")
	}
	if err := m.Resume(id, mac.Resolution{State: "host-error", Err: errors.New("host failure")}); errorCode(err) != "HostFailure" {
		t.Fatal(err)
	}
	r = m.State()
	r.Err.(*mac.Failure).Detail = "changed"
	if m.State().Err.(*mac.Failure).Detail != "host failure" {
		t.Fatal("failure detail alias")
	}
	if len(s.receipts) != 0 {
		t.Fatal("host error emitted BAD")
	}
}

func TestSourceExportUnchangedAfterRun(t *testing.T) {
	raw := originalABC(t)
	before := bytes.Clone(raw)
	i := image(t, raw)
	p, err := mac.Compile(i, fullPolicy(), mac.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	m := newMachine(t, p, sink(), nil, mac.DefaultLimits())
	drive(t, m, 1)
	if !bytes.Equal(i.Export(), before) || !bytes.Equal(raw, before) {
		t.Fatal("interpreter modified native source")
	}
}

func TestCallbackWordViewsDoNotCorruptAnotherMachine(t *testing.T) {
	raw := originalABC(t)
	p := program(t, raw, mac.DefaultLimits())
	mutator := sink()
	mutator.apply = func(_ context.Context, e mac.Effect) (mac.EffectResult, error) {
		e.Words[0].Value = 0
		e.Words[0].Span = wpm.Span{}
		return mac.EffectResult{}, nil
	}
	first := newMachine(t, p, mutator, nil, mac.DefaultLimits())
	normal := sink()
	second := newMachine(t, p, normal, nil, mac.DefaultLimits())
	if drive(t, first, 8).State != "complete" || drive(t, second, 8).State != "complete" || textTrace(normal) != "ABC" {
		t.Fatal("callback received compiled-word backing")
	}
}

func TestCompileAndSinkCapabilitySlicesAreOwned(t *testing.T) {
	root := native(t, "P", uint16(0xfc18), "CHILD~R")
	child := image(t, native(t, uint16(0x8021)))
	policy := fullPolicy()
	p, err := mac.Compile(image(t, root), policy, mac.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	policy.Keys[0] = 0x8020
	s := sink()
	m := newMachine(t, p, s, resolverFunc(func(context.Context, mac.ProgramRequest) mac.Resolution {
		return mac.Resolution{State: "ready", Image: child}
	}), mac.DefaultLimits())
	s.policy.Keys[0] = 0x8020
	r := drive(t, m, 1)
	if r.State != "complete" || textTrace(s) != "PR" {
		t.Fatal("mutable policy/capability slice", r, textTrace(s))
	}
	keys := 0
	for _, receipt := range s.receipts {
		if receipt.Effect.Kind == "key" {
			keys++
			if receipt.Effect.Words[0].Value != 0x8021 {
				t.Fatal("key identity")
			}
		}
	}
	if keys != 1 {
		t.Fatal("missing child key")
	}
}
