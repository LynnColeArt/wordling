package runtime_test

import (
	"bytes"
	"context"
	"crypto/sha256"
	"go/ast"
	"go/parser"
	"go/token"
	"path/filepath"
	"strconv"
	"strings"
	"testing"

	mac "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

func TestProductionDependencyBoundary(t *testing.T) {
	files, err := filepath.Glob("*.go")
	if err != nil {
		t.Fatal(err)
	}
	for _, name := range files {
		if strings.HasSuffix(name, "_test.go") {
			continue
		}
		file, err := parser.ParseFile(token.NewFileSet(), name, nil, parser.ImportsOnly)
		if err != nil {
			t.Fatal(err)
		}
		ast.Inspect(file, func(n ast.Node) bool {
			imp, ok := n.(*ast.ImportSpec)
			if !ok {
				return true
			}
			path, err := strconv.Unquote(imp.Path.Value)
			if err != nil {
				t.Fatal(err)
			}
			if strings.HasPrefix(path, "github.com/lynncoleart/wordling/") && path != "github.com/lynncoleart/wordling/internal/macro/wpm" {
				t.Fatal("forbidden production dependency", path)
			}
			for _, forbidden := range []string{"os", "io", "net", "syscall", "path/filepath"} {
				if path == forbidden || strings.HasPrefix(path, forbidden+"/") {
					t.Fatal("host IO in pure VM", path)
				}
			}
			return true
		})
	}
}

func FuzzCompilerMachine(f *testing.F) {
	seen := map[string]bool{}
	for _, a := range corpus(f).Exports {
		if !seen[a.SHA] {
			f.Add(readArtifact(f, a))
			seen[a.SHA] = true
		}
	}
	for _, raw := range [][]byte{
		native(f, uint16(0xfc2b), "1~", uint16(0xfc11)),
		native(f, uint16(0xfc16), "A~X", uint16(0xfc14), "A~"),
		native(f, "P", uint16(0xfc18), "SELF~R"),
		native(f, uint16(0xfc15), "0~", uint16(0xfc3a), uint16(0xfc10)),
		native(f, uint16(0xfc13), "V~", uint16(0xfc34), "B~~~", uint16(0xfc0f)),
	} {
		f.Add(raw)
	}
	f.Fuzz(func(t *testing.T, raw []byte) {
		before := bytes.Clone(raw)
		image, err := wpm.Parse(raw, wpm.DefaultLimits())
		if err != nil {
			return
		}
		limits := mac.Limits{Steps: 512, OutputWords: 128, CallDepth: 4, LoopDepth: 4, Variables: 16, VariableWords: 64, ExpressionDepth: 4, SliceSteps: 16}
		program, err := mac.Compile(image, fullPolicy(), limits)
		if err != nil {
			if program != nil || errorCode(err) == "" {
				t.Fatal("untyped compile refusal", program, err)
			}
			if !bytes.Equal(image.Export(), raw) {
				t.Fatal("compile source mutation")
			}
			return
		}
		s := sink()
		resolver := resolverFunc(func(context.Context, mac.ProgramRequest) mac.Resolution { return mac.Resolution{State: "pending"} })
		m, err := mac.New(program, s, resolver, limits)
		if err != nil {
			if errorCode(err) == "" {
				t.Fatal(err)
			}
			return
		}
		var previous uint64
		done := false
		for n := 0; n < 1024; n++ {
			r := m.Step(context.Background(), 16)
			if r.Steps < previous || r.Steps-previous > 16 || r.Steps > limits.Steps || r.EmittedWords > limits.OutputWords {
				t.Fatal("budget escape", previous, r)
			}
			previous = r.Steps
			if r.State == "waiting" {
				id := r.NeedProgram.ID
				r.NeedProgram.Name[0].Value = 0
				if errorCode(m.Resume(id+1, mac.Resolution{State: "ready", Image: image})) != "StaleResume" {
					t.Fatal("wrong request resumed")
				}
				_ = m.Resume(id, mac.Resolution{State: "ready", Image: image})
				continue
			}
			if r.State != "running" && r.State != "ready" {
				done = true
				break
			}
		}
		if !done {
			t.Fatal("finite run failed to stop")
		}
		beforeCount := len(s.receipts)
		again := m.Step(context.Background(), 1)
		if again.State == "running" || again.State == "waiting" || len(s.receipts) != beforeCount {
			t.Fatal("terminal run repeated work/effects")
		}
		if !bytes.Equal(image.Export(), raw) || !bytes.Equal(before, raw) || image.SHA256() != sha256.Sum256(raw) {
			t.Fatal("native source changed")
		}
	})
}

func BenchmarkCompileOriginal(b *testing.B) {
	i := image(b, originalABC(b))
	b.ReportAllocs()
	b.ResetTimer()
	for n := 0; n < b.N; n++ {
		if _, err := mac.Compile(i, fullPolicy(), mac.DefaultLimits()); err != nil {
			b.Fatal(err)
		}
	}
}
func BenchmarkMachineOriginal(b *testing.B) {
	p := program(b, originalABC(b), mac.DefaultLimits())
	b.ReportAllocs()
	b.ResetTimer()
	for n := 0; n < b.N; n++ {
		s := sink()
		m, err := mac.New(p, s, nil, mac.DefaultLimits())
		if err != nil {
			b.Fatal(err)
		}
		if drive(b, m, 64).State != "complete" {
			b.Fatal("run")
		}
	}
}
func TestResourceLargeLiteralAndFiniteLoop(t *testing.T) {
	l := mac.DefaultLimits()
	l.Steps = 20000
	l.OutputWords = 8192
	raw := native(t, strings.Repeat("X", 4096))
	s := sink()
	m := newMachine(t, program(t, raw, l), s, nil, l)
	r := drive(t, m, 256)
	if r.State != "complete" || r.EmittedWords != 4096 || len(s.receipts) != 4096 {
		t.Fatal(r)
	}
	loop := native(t, uint16(0xfc2b), "1~", uint16(0xfc13), "V~"+strings.Repeat("r", 4096)+"~~", uint16(0xfc0f), uint16(0xfc11))
	s = sink()
	m = newMachine(t, program(t, loop, l), s, nil, l)
	r = drive(t, m, 256)
	if r.State != "limited" || errorCode(r.Err) != "StepLimit" || r.Steps != l.Steps || len(s.receipts) != 0 {
		t.Fatal("empty loop resource accounting", r)
	}
	// The maximum admitted word count is preflighted without recursive descent
	// or per-character instructions. Its scan alone exhausts the run budget, so
	// no literal may be delivered afterward.
	raw = native(t, strings.Repeat("X", wpm.MaxWords-1))
	compileFailure(t, raw, mac.DefaultLimits(), "CompilationLimit")
	raw = native(t, strings.Repeat("X", int(mac.DefaultLimits().Steps)-1))
	s = sink()
	l = mac.DefaultLimits()
	m = newMachine(t, program(t, raw, l), s, nil, l)
	r = drive(t, m, 256)
	if r.State != "limited" || errorCode(r.Err) != "StepLimit" || r.Steps != l.Steps || r.EmittedWords != 0 || len(s.receipts) != 0 {
		t.Fatal("maximum word scan bypassed budget", r)
	}
}
