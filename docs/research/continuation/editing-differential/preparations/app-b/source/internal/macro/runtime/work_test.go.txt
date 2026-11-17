package runtime_test

import (
	"bytes"
	"context"
	goruntime "runtime"
	"strings"
	"testing"
	"time"

	mac "github.com/lynncoleart/wordling/internal/macro/runtime"
)

func expandedEach(t testing.TB, words, items int, body ...any) []byte {
	t.Helper()
	parts := []any{uint16(0xfc13), "I~" + strings.Repeat("r", words) + "~~", uint16(0xfc13), "V~"}
	for n := 0; n < items; n++ {
		parts = append(parts, uint16(0xfc34), "I~~")
	}
	parts = append(parts, "~")
	parts = append(parts, body...)
	parts = append(parts, uint16(0xfc0f), uint16(0xfc0f))
	return native(t, parts...)
}
func TestListPreparationRunSliceAndAllocationBounds(t *testing.T) {
	raw := expandedEach(t, 4096, 1024)
	i := image(t, raw)
	cost := uint64(i.Inspect().Body.Length / 2)
	for _, extra := range []uint64{2, 200, 1088, mac.DefaultLimits().Steps - cost} {
		t.Run(stringName(extra), func(t *testing.T) {
			l := mac.DefaultLimits()
			l.SliceSteps = 1
			l.OutputWords = 1
			l.Steps = cost + extra
			s := sink()
			m := newMachine(t, program(t, raw, l), s, nil, l)
			goruntime.GC()
			var a, b goruntime.MemStats
			goruntime.ReadMemStats(&a)
			start := time.Now()
			var result mac.Result
			for n := uint64(0); n <= l.Steps+1; n++ {
				before := m.State().Steps
				result = m.Step(context.Background(), 1)
				if result.Steps < before || result.Steps-before > 1 || result.Steps > l.Steps {
					t.Fatal("slice/run escape", before, result)
				}
				if result.State != "running" && result.State != "ready" {
					break
				}
			}
			goruntime.ReadMemStats(&b)
			allocated := b.TotalAlloc - a.TotalAlloc
			t.Logf("extra=%d state=%s steps=%d total allocation=%d elapsed=%v", extra, result.State, result.Steps, allocated, time.Since(start))
			if allocated > 2<<20 {
				t.Fatal("list expanded/copied aggregate value words", allocated)
			}
			if extra == mac.DefaultLimits().Steps-cost {
				if result.State != "complete" || result.Steps < cost+2048 {
					t.Fatal(result)
				}
			} else if result.State != "limited" || errorCode(result.Err) != "StepLimit" || result.Steps != l.Steps {
				t.Fatal(result)
			}
			if len(s.receipts) != 0 || result.EmittedWords != 0 || !bytes.Equal(i.Export(), raw) {
				t.Fatal("non-emitting list/source invariant", result)
			}
			again := m.Step(context.Background(), 1)
			if again.State != result.State || again.Steps != result.Steps || len(s.receipts) != 0 {
				t.Fatal("terminal work repeated")
			}
		})
	}
}
func stringName(n uint64) string { // stable descriptive names without fmt in production
	if n == 2 {
		return "one_remaining_after_start"
	}
	if n == 1088 {
		return "argument_plus_loop_minimum"
	}
	if n == 200 {
		return "partial_inner_preparation"
	}
	return "complete_non_emitting"
}
func TestListPreparationCancellation(t *testing.T) {
	raw := expandedEach(t, 4096, 1024)
	l := mac.DefaultLimits()
	l.SliceSteps = 1
	s := sink()
	m := newMachine(t, program(t, raw, l), s, nil, l)
	cost := uint64(image(t, raw).Inspect().Body.Length / 2)
	for m.State().Steps < cost+200 {
		r := m.Step(context.Background(), 1)
		if r.State != "running" {
			t.Fatal(r)
		}
	}
	before := m.State()
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	r := m.Step(ctx, 1)
	if r.State != "stopped" || errorCode(r.Err) != "HostCancelled" || r.Steps != before.Steps || len(s.receipts) != 0 {
		t.Fatal(r)
	}
	if next := m.Step(context.Background(), 1); next.State != "stopped" || next.Steps != r.Steps {
		t.Fatal(next)
	}
	// Explicit host Stop also stops an unfinished preparation without effects.
	m = newMachine(t, program(t, raw, l), s, nil, l)
	for m.State().Steps < cost+200 {
		m.Step(context.Background(), 1)
	}
	before = m.State()
	r = m.Stop("host test")
	if r.State != "stopped" || r.Steps != before.Steps || len(s.receipts) != 0 {
		t.Fatal(r)
	}
}
func TestVariableEmissionDoesNotMaterializeLongWordArray(t *testing.T) {
	raw := native(t, uint16(0xfc13), "I~"+strings.Repeat("r", 4096)+"~~", uint16(0xfc34), "I~", uint16(0xfc0f))
	l := mac.DefaultLimits()
	l.SliceSteps = 1
	l.OutputWords = 1
	s := sink()
	m := newMachine(t, program(t, raw, l), s, nil, l)
	cost := uint64(image(t, raw).Inspect().Body.Length / 2)
	for m.State().Steps < cost {
		m.Step(context.Background(), 1)
	}
	goruntime.GC()
	var maxAlloc uint64
	var result mac.Result
	for n := 0; n < 256; n++ {
		var a, b goruntime.MemStats
		goruntime.ReadMemStats(&a)
		before := m.State().Steps
		result = m.Step(context.Background(), 1)
		goruntime.ReadMemStats(&b)
		if b.TotalAlloc-a.TotalAlloc > maxAlloc {
			maxAlloc = b.TotalAlloc - a.TotalAlloc
		}
		if result.Steps-before > 1 {
			t.Fatal("slice escape")
		}
		if result.State != "running" {
			break
		}
	}
	t.Logf("max allocation per one-work-unit Step=%d", maxAlloc)
	if maxAlloc > 16<<10 || result.State != "limited" || errorCode(result.Err) != "OutputLimit" || result.EmittedWords != 1 || len(s.receipts) != 1 || s.receipts[0].Effect.Words[0].Value != 'r' {
		t.Fatal(result, maxAlloc, len(s.receipts))
	}
}
func TestLongNameControlEvaluationUsesBoundedSlots(t *testing.T) {
	name := strings.Repeat("N", 4096)
	raw := native(t, uint16(0xfc01), name+"~0~", uint16(0xfc2b), uint16(0xfc34), name+"~<1~", uint16(0xfc01), name+"~", uint16(0xfc34), name+"~+1~", uint16(0xfc11))
	l := mac.DefaultLimits()
	l.SliceSteps = 1
	s := sink()
	m := newMachine(t, program(t, raw, l), s, nil, l)
	cost := uint64(image(t, raw).Inspect().Body.Length / 2)
	var r mac.Result
	for n := 0; n < 200000; n++ {
		before := m.State().Steps
		r = m.Step(context.Background(), 1)
		if r.Steps-before > 1 {
			t.Fatal("long-name slice escape")
		}
		if r.State != "running" {
			break
		}
	}
	if r.State != "complete" || r.Steps <= cost || r.Steps > cost+100 || len(s.receipts) != 0 {
		t.Fatal("compiled name lookup/control did not stay bounded", cost, r)
	}
}
func TestPreparedListErrorsBeforeAnyBodyEffects(t *testing.T) {
	raw := native(t, uint16(0xfc14), "SKIP~", uint16(0xfc01), "U~1~", uint16(0xfc16), "SKIP~", uint16(0xfc13), "V~safe~", uint16(0xfc34), "U~~~BODY", uint16(0xfc0f))
	l := mac.DefaultLimits()
	s := sink()
	m := newMachine(t, program(t, raw, l), s, nil, l)
	r := drive(t, m, 1)
	if r.State != "refused" || errorCode(r.Err) != "UndefinedVariable" || len(s.receipts) != 0 {
		t.Fatal("eager-before-body failure timing changed", r, s.receipts)
	}
}

// A public request/result necessarily transfers a whole independent snapshot.
// This is the declared4096-word API boundary, not quota-proportional interpreter
// evaluation or a claim about callback latency. It cannot multiply list values.
func TestMaximumPendingRequestSnapshotBoundary(t *testing.T) {
	raw := native(t, uint16(0xfc18), strings.Repeat("X", 4096)+"~")
	l := mac.DefaultLimits()
	l.SliceSteps = 1
	s := sink()
	calls := 0
	resolver := resolverFunc(func(_ context.Context, r mac.ProgramRequest) mac.Resolution {
		calls++
		if len(r.Name) != 4096 {
			t.Fatal("name width")
		}
		r.Name[0].Value = 'Y'
		return mac.Resolution{State: "pending"}
	})
	m := newMachine(t, program(t, raw, l), s, resolver, l)
	cost := uint64(image(t, raw).Inspect().Body.Length / 2)
	for m.State().Steps < cost {
		m.Step(context.Background(), 1)
	}
	var a, b goruntime.MemStats
	goruntime.ReadMemStats(&a)
	r := m.Step(context.Background(), 1)
	goruntime.ReadMemStats(&b)
	t.Logf("whole native request/result boundary4096 words: allocation=%d; callback latency excluded", b.TotalAlloc-a.TotalAlloc)
	if r.State != "waiting" || calls != 1 || len(r.NeedProgram.Name) != 4096 || r.NeedProgram.Name[0].Value != 'X' || b.TotalAlloc-a.TotalAlloc > 2<<20 || len(s.receipts) != 0 {
		t.Fatal(r, calls)
	}
	r.NeedProgram.Name[0].Value = 'Z'
	if m.State().NeedProgram.Name[0].Value != 'X' {
		t.Fatal("pending snapshot alias")
	}
}

func TestExpressionNodesCannotBeDeferredToAnUnchargedBurst(t *testing.T) {
	raw := native(t, uint16(0xfc01), "N~1+2~", uint16(0xfc34), "N~")
	l := mac.DefaultLimits()
	l.SliceSteps = 1
	s := sink()
	m := newMachine(t, program(t, raw, l), s, nil, l)
	cost := uint64(image(t, raw).Inspect().Body.Length / 2)
	for m.State().Steps < cost+4 {
		r := m.Step(context.Background(), 1)
		if r.State != "running" {
			t.Fatal(r)
		}
	}
	if len(s.receipts) != 0 {
		t.Fatal("expression evaluation nodes were not charged before effects")
	}
	r := drive(t, m, 1)
	if r.State != "complete" || len(s.receipts) != 1 || s.receipts[0].Effect.Words[0].Value != '3' {
		t.Fatal(r, s.receipts)
	}
}
