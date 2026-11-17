package editor_test

import (
	"context"
	"github.com/lynncoleart/wordling/internal/editor"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
	"testing"
)

func TestRepeatSharesActualWorkBudget(t *testing.T) {
	s, _ := readyMacro(t)
	s = key(t, s, editor.CancelOperation)
	var e error
	s, e = s.WithMacroRepeat(3)
	if e != nil {
		t.Fatal(e)
	}
	s = key(t, s, editor.Macro)
	s = text(t, s, "B:\\M38")
	s, i := submit(t, s)
	s, _ = done(t, s, perform(i))
	limits := vm.DefaultLimits()
	limits.Steps = 20
	s, run, e := s.StartMacro(limits)
	if e != nil {
		t.Fatal(e)
	}
	for !run.Snapshot().Terminal {
		s, _, _, e = run.Step(context.Background(), s, 1)
		if e != nil {
			t.Fatal(e)
		}
	}
	p := run.Snapshot()
	if p.State != "limited" || p.TotalSteps != 20 || p.Completed != 1 || asciiText(t, s) != "ABCAABCD" {
		t.Fatalf("work reset across repeat: %+v native%q", p, asciiText(t, s))
	}
}
func TestAcceptedMacroSinkReceiptsDescribeRealEffects(t *testing.T) {
	s, _ := readyMacro(t)
	s, run, e := s.StartMacro(vm.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	s = runMacro(t, s, run)
	receipts, e := run.Receipts(0, run.Snapshot().ReceiptCount)
	if e != nil {
		t.Fatal(e)
	}
	literals, controls := 0, 0
	for _, r := range receipts {
		if !r.Applied || !r.Result.MayHaveEffects || r.Err != nil {
			t.Fatal("accepted effect missing receipt", r)
		}
		if r.Effect.Kind == "literal" {
			literals++
			if r.After <= r.Before || r.AfterGap != r.BeforeGap+1 {
				t.Fatal("literal receipt divorced from actual ordinary reduction")
			}
		} else if r.Effect.Kind == "display-off" {
			controls++
			if r.After != r.Before || r.AfterGap != r.BeforeGap {
				t.Fatal("display metadata fabricated native edit")
			}
		}
	}
	if literals != 3 || controls != 1 || run.Snapshot().AppliedWords != 3 || s.Snapshot().Mode != editor.Editing {
		t.Fatal("sink counters are not real delivery receipts")
	}
}
