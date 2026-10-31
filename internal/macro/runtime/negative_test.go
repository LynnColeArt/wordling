package runtime_test

import (
	"context"
	"testing"

	mac "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

func compileFailure(t testing.TB, raw []byte, l mac.Limits, code string) {
	t.Helper()
	i := image(t, raw)
	p, err := mac.Compile(i, fullPolicy(), l)
	if p != nil || errorCode(err) != code {
		t.Fatalf("want compile %s; got %v/%v", code, p, err)
	}
}
func TestCompileRefusesStaticUnknownAndUnqualifiedContexts(t *testing.T) {
	for _, tc := range []struct {
		name, code string
		parts      []any
	}{
		{"unknown-dead", "UnsupportedImage", []any{"BEFORE", uint16(0xfc15), "0~", uint16(0xfc3a), uint16(0xfc10)}},
		{"quit-dead", "UnqualifiedQuit", []any{"BEFORE", uint16(0xfc15), "0~", uint16(0xfc20), uint16(0xfc10)}},
		{"missing-label", "MissingLabel", []any{uint16(0xfc14), "MISSING~"}},
		{"duplicate-label", "DuplicateLabel", []any{uint16(0xfc16), "A~", uint16(0xfc16), "A~"}},
		{"missing-end", "UnmatchedStructure", []any{uint16(0xfc15), "1~BODY"}},
		{"wrong-end", "UnmatchedStructure", []any{uint16(0xfc15), "1~", uint16(0xfc0f)}},
		{"orphan-else", "UnmatchedStructure", []any{uint16(0xfc0e)}},
		{"duplicate-else", "UnmatchedStructure", []any{uint16(0xfc15), "1~", uint16(0xfc0e), uint16(0xfc0e), uint16(0xfc10)}},
		{"unowned-tilde", "UnexpectedDelimiter", []any{"A~"}},
		{"missing-outer-tilde", "MalformedOperand", []any{uint16(0xfc2b), uint16(0xfc34), "N~<3", uint16(0xfc11)}},
		{"unsupported-operator", "UnsupportedExpression", []any{uint16(0xfc15), "1/2~", uint16(0xfc10)}},
		{"unsupported-precedence", "UnsupportedExpression", []any{uint16(0xfc15), "1+2+3~", uint16(0xfc10)}},
		{"undefined", "UndefinedVariable", []any{"BEFORE", uint16(0xfc34), "N~"}},
		{"if-break", "UnsupportedLoopControl", []any{uint16(0xfc15), "1~", uint16(0xfc03), uint16(0xfc10)}},
		{"while-next", "UnsupportedLoopControl", []any{uint16(0xfc2b), "1~", uint16(0xfc19), uint16(0xfc11)}},
		{"each-break", "UnsupportedLoopControl", []any{uint16(0xfc13), "V~1~~", uint16(0xfc03), uint16(0xfc0f)}},
		{"jump-scope", "UnsupportedContext", []any{uint16(0xfc15), "1~", uint16(0xfc14), "A~", uint16(0xfc10), uint16(0xfc16), "A~"}},
		{"loop-var-write", "UnsupportedLoopVariableMutation", []any{uint16(0xfc12), "N~1~3~1~", uint16(0xfc01), "N~1~", uint16(0xfc0f)}},
		{"zero-step", "UnsupportedLoopRange", []any{uint16(0xfc12), "N~1~3~0~", uint16(0xfc0f)}},
		{"unqualified-step", "UnsupportedLoopRange", []any{uint16(0xfc12), "N~1~3~2~", uint16(0xfc0f)}},
		{"variable-bound", "UnsupportedForBounds", []any{uint16(0xfc01), "B~1~", uint16(0xfc12), "N~", uint16(0xfc34), "B~", "~3~1~", uint16(0xfc0f)}},
		{"each-timing", "UnsupportedEvaluationTiming", []any{uint16(0xfc01), "B~1~", uint16(0xfc13), "V~", uint16(0xfc34), "B~~~", uint16(0xfc01), "B~2~", uint16(0xfc0f)}},
		{"each-unclosed-quote", "UnsupportedExpression", []any{uint16(0xfc13), "V~\"red~~", uint16(0xfc0f)}},
		{"empty-each", "MalformedOperand", []any{uint16(0xfc13), "V~~", uint16(0xfc0f)}},
		{"cross-file-vars", "UnsupportedVariableScope", []any{uint16(0xfc01), "N~1~", uint16(0xfc18), "CHILD~"}},
		{"handler-nest", "UnsupportedHandlerContext", []any{uint16(0xfc1c), uint16(0xfc14), "ERR~~", uint16(0xfc16), "ERR~", uint16(0xfc18), "CHILD~"}},
		{"handler-backward-search", "UnsupportedHandlerContext", []any{uint16(0xfc1c), uint16(0xfc14), "ERR~~", uint16(0xfc16), "SEARCH~", uint16(0x8021), uint16(0xfc16), "ERR~", uint16(0xfc14), "SEARCH~"}},
		{"handler-action", "UnsupportedHandler", []any{uint16(0xfc1c), uint16(0xfc22), "~"}},
		{"handler-outer-tilde", "MalformedOperand", []any{uint16(0xfc1c), uint16(0xfc14), "ERR~", uint16(0xfc16), "ERR~"}},
		{"constant-overflow", "NumericOverflow", []any{uint16(0xfc01), "N~9223372036854775807+1~"}},
	} {
		t.Run(tc.name, func(t *testing.T) { compileFailure(t, native(t, tc.parts...), mac.DefaultLimits(), tc.code) })
	}
}

func TestLimitsPoliciesAndBoundedRuns(t *testing.T) {
	base := native(t, "ABC")
	defaults := mac.DefaultLimits()
	for _, l := range []mac.Limits{{}, {Steps: defaults.Steps + 1}, {OutputWords: defaults.OutputWords + 1}} {
		if _, err := mac.Compile(image(t, base), fullPolicy(), l); errorCode(err) != "InvalidLimit" {
			t.Fatal(err)
		}
	}
	if _, err := mac.Compile(nil, fullPolicy(), defaults); errorCode(err) != "InvalidImage" {
		t.Fatal(err)
	}
	if _, err := mac.Compile(&wpm.Image{}, fullPolicy(), defaults); errorCode(err) != "InvalidImage" {
		t.Fatal(err)
	}
	l := defaults
	l.Steps = 2
	compileFailure(t, base, l, "CompilationLimit")
	l = defaults
	l.ExpressionDepth = 1
	compileFailure(t, native(t, uint16(0xfc01), "N~1+2~"), l, "ExpressionLimit")
	l = defaults
	l.Variables = 1
	compileFailure(t, native(t, uint16(0xfc01), "A~1~", uint16(0xfc01), "B~2~"), l, "VariableLimit")
	l = defaults
	l.LoopDepth = 1
	compileFailure(t, native(t, uint16(0xfc12), "I~1~2~1~", uint16(0xfc12), "J~1~2~1~", uint16(0xfc0f), uint16(0xfc0f)), l, "LoopLimit")
	if _, err := mac.Compile(image(t, base), mac.Policy{}, defaults); errorCode(err) != "UnsupportedPolicy" {
		t.Fatal(err)
	}
	p := program(t, base, defaults)
	tighter := defaults
	tighter.Steps = 100
	restricted := program(t, base, tighter)
	tighter.Steps = defaults.Steps
	if _, err := mac.New(restricted, sink(), nil, tighter); errorCode(err) != "BroadenedLimits" {
		t.Fatal("caller mutation broadened stored compile limits", err)
	}
	if _, err := mac.New(p, &traceSink{}, nil, defaults); errorCode(err) != "UnsupportedSink" {
		t.Fatal(err)
	}
	if _, err := mac.New(nil, sink(), nil, defaults); errorCode(err) != "InvalidProgram" {
		t.Fatal(err)
	}
	if _, err := mac.New(p, nil, nil, defaults); errorCode(err) != "InvalidSink" {
		t.Fatal(err)
	}
	child := program(t, native(t, "C", uint16(0xfc22)), defaults)
	if _, err := mac.New(child, sink(), nil, defaults); errorCode(err) != "UnsupportedReturnContext" {
		t.Fatal(err)
	}
	l = defaults
	l.Steps = 64
	loop := native(t, uint16(0xfc16), "AGAIN~X", uint16(0xfc14), "AGAIN~")
	s := sink()
	m := newMachine(t, program(t, loop, l), s, nil, l)
	r := drive(t, m, 3)
	if r.State != "limited" || errorCode(r.Err) != "StepLimit" || r.Steps != l.Steps {
		t.Fatal("GO cycle not bounded", r)
	}
	l = defaults
	l.Steps = 50
	while := native(t, uint16(0xfc2b), "1~", uint16(0xfc11))
	m = newMachine(t, program(t, while, l), sink(), nil, l)
	r = drive(t, m, 7)
	if r.State != "limited" || r.Steps != l.Steps {
		t.Fatal("empty WHILE not charged", r)
	}
	l = defaults
	l.OutputWords = 2
	s = sink()
	m = newMachine(t, program(t, base, l), s, nil, l)
	r = drive(t, m, 1)
	if r.State != "limited" || errorCode(r.Err) != "OutputLimit" || r.EmittedWords != 2 || textTrace(s) != "AB" {
		t.Fatal("output budget/partial effects", r, textTrace(s))
	}
	m = newMachine(t, p, sink(), nil, defaults)
	if errorCode(m.Step(context.Background(), 0).Err) != "InvalidQuota" {
		t.Fatal("invalid quota")
	}
}

func TestNestedBudgetsAndUnqualifiedChildPreflight(t *testing.T) {
	parent := native(t, "P", uint16(0xfc18), "CHILD~R")
	child := image(t, native(t, "C"))
	l := mac.DefaultLimits()
	l.CallDepth = 1
	s := sink()
	m := newMachine(t, program(t, parent, l), s, resolverFunc(func(context.Context, mac.ProgramRequest) mac.Resolution {
		return mac.Resolution{State: "ready", Image: child}
	}), l)
	r := drive(t, m, 1)
	if r.State != "limited" || errorCode(r.Err) != "CallLimit" || textTrace(s) != "P" {
		t.Fatal(r, textTrace(s))
	}
	l = mac.DefaultLimits()
	l.Steps = uint64(image(t, parent).Inspect().Body.Length/2) + 5
	s = sink()
	m = newMachine(t, program(t, parent, l), s, resolverFunc(func(context.Context, mac.ProgramRequest) mac.Resolution {
		return mac.Resolution{State: "ready", Image: child}
	}), l)
	r = drive(t, m, 1)
	if r.State != "limited" || r.Steps > l.Steps || textTrace(s) != "P" {
		t.Fatal("nested scan reset budget", r, textTrace(s))
	}
	l = mac.DefaultLimits()
	badChild := image(t, native(t, "CHILD-BAD", uint16(0xfc15), "0~", uint16(0xfc3a), uint16(0xfc10)))
	s = sink()
	m = newMachine(t, program(t, parent, l), s, resolverFunc(func(context.Context, mac.ProgramRequest) mac.Resolution {
		return mac.Resolution{State: "ready", Image: badChild}
	}), l)
	r = drive(t, m, 16)
	if r.State != "refused" || errorCode(r.Err) != "NestedCompile" || textTrace(s) != "P" {
		t.Fatal("unsupported child emitted effects", r, textTrace(s))
	}
	cycle := image(t, native(t, "X", uint16(0xfc18), "SELF~"))
	l.CallDepth = 3
	s = sink()
	p, err := mac.Compile(cycle, fullPolicy(), l)
	if err != nil {
		t.Fatal(err)
	}
	m = newMachine(t, p, s, resolverFunc(func(context.Context, mac.ProgramRequest) mac.Resolution {
		return mac.Resolution{State: "ready", Image: cycle}
	}), l)
	r = drive(t, m, 1)
	if r.State != "limited" || errorCode(r.Err) != "CallLimit" || textTrace(s) != "XXX" {
		t.Fatal("recursive nesting not bounded", r, textTrace(s))
	}
	l = mac.DefaultLimits()
	l.OutputWords = 2
	s = sink()
	m = newMachine(t, program(t, parent, l), s, resolverFunc(func(context.Context, mac.ProgramRequest) mac.Resolution {
		return mac.Resolution{State: "ready", Image: child}
	}), l)
	r = drive(t, m, 1)
	if r.State != "limited" || errorCode(r.Err) != "OutputLimit" || r.EmittedWords != 2 || textTrace(s) != "PC" {
		t.Fatal("nested output budget reset", r, textTrace(s))
	}
}

func TestDynamicUndefinedOverflowAndValueLimits(t *testing.T) {
	l := mac.DefaultLimits()
	for _, tc := range []struct {
		name, code string
		raw        []byte
	}{
		{"undefined-path", "UndefinedVariable", native(t, uint16(0xfc14), "SKIP~", uint16(0xfc01), "N~1~", uint16(0xfc16), "SKIP~P", uint16(0xfc34), "N~")},
		{"overflow", "NumericOverflow", native(t, uint16(0xfc01), "N~9223372036854775807~P", uint16(0xfc01), "N~", uint16(0xfc34), "N~+1~")},
		{"string-assignment", "UnsupportedAssignment", native(t, uint16(0xfc13), "V~red~~P", uint16(0xfc01), "N~", uint16(0xfc34), "V~~", uint16(0xfc0f))},
	} {
		t.Run(tc.name, func(t *testing.T) {
			s := sink()
			m := newMachine(t, program(t, tc.raw, l), s, nil, l)
			r := drive(t, m, 2)
			if r.State != "refused" || errorCode(r.Err) != tc.code || textTrace(s) != "P" {
				t.Fatal(r, textTrace(s))
			}
		})
	}
	l.VariableWords = 1
	raw := native(t, uint16(0xfc01), "N~9~P", uint16(0xfc01), "N~", uint16(0xfc34), "N~+1~")
	s := sink()
	m := newMachine(t, program(t, raw, l), s, nil, l)
	r := drive(t, m, 1)
	if r.State != "limited" || errorCode(r.Err) != "ValueLimit" || textTrace(s) != "P" {
		t.Fatal(r, textTrace(s))
	}
}
