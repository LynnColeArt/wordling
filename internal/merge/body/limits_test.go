package body_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/merge/body"
	"github.com/lynncoleart/wordling/internal/merge/explicit"
	"github.com/lynncoleart/wordling/internal/merge/native"
	"strings"
	"testing"
	"unsafe"
)

func TestCompileLimitBoundaries(t *testing.T) {
	p, s := program(t, primary(t, "207"))
	info, _ := p.Inspect()
	l := body.DefaultLimits()
	l.PrimaryTokens = len(info.Tokens)
	if q, e := body.Compile(p, s, l); e != nil || !q.Valid() {
		t.Fatal(e)
	}
	l.PrimaryTokens--
	if q, e := body.Compile(p, s, l); e == nil || q.Valid() {
		t.Fatal("one over token")
	}
	for _, l := range []body.Limits{{}, {-1, 1, 1}, {4097, 1, 1048576}, {1, 65537, 1048576}, {1, 1, 1048577}, {4096, 65536, 348159}} {
		if q, e := body.Compile(p, s, l); e == nil || q.Valid() {
			t.Fatalf("limits %+v", l)
		}
	}
	max := append([]byte(strings.Repeat("a", 4092)), command(0x36, "1")...)
	max = append(max, '\n')
	pm, sm := program(t, authored(t, max))
	if q, e := body.Compile(pm, sm, body.DefaultLimits()); e != nil || !q.Valid() {
		t.Fatal(e)
	}
	max = append([]byte{'a'}, max...)
	px, sx := program(t, authored(t, max))
	if q, e := body.Compile(px, sx, body.DefaultLimits()); e == nil || q.Valid() {
		t.Fatal("4097 tokens")
	}
}
func TestBodyAndWorkAtomicity(t *testing.T) {
	p, s := program(t, primary(t, "207"))
	d, ds := data(t, secondary(t, "207"))
	l := body.DefaultLimits()
	l.BodyBytes = 12
	q, e := body.Compile(p, s, l)
	if e != nil {
		t.Fatal(e)
	}
	result(t, q, d, ds, 1, "Hello Alice\n")
	l.BodyBytes = 11
	q, e = body.Compile(p, s, l)
	if e != nil {
		t.Fatal(e)
	}
	if r, e := q.Evaluate(d, ds, 1); e == nil || r.Valid() {
		t.Fatal("body overflow")
	}
	min := 348160
	max := 1048576
	for min < max {
		mid := (min + max) / 2
		l = body.DefaultLimits()
		l.WorkUnits = mid
		if _, e := body.Compile(p, s, l); e == nil {
			max = mid
		} else {
			min = mid + 1
		}
	}
	l = body.DefaultLimits()
	l.WorkUnits = min
	if q, e := body.Compile(p, s, l); e != nil || !q.Valid() {
		t.Fatal("exact work", e)
	}
	l.WorkUnits--
	if q, e := body.Compile(p, s, l); e == nil || q.Valid() {
		t.Fatal("work off by one")
	}
}
func TestPinnedInspectionReservationProof(t *testing.T) {
	sum := uint64(native.MaxTokens)*uint64(unsafe.Sizeof(native.Token{})) + uint64(native.MaxTokens)*uint64(unsafe.Sizeof(native.Command{})) + uint64(native.MaxFindings)*uint64(unsafe.Sizeof(native.Finding{})) + uint64(native.MaxRecords)*uint64(unsafe.Sizeof(native.Record{})) + uint64(native.MaxFields)*uint64(unsafe.Sizeof(native.Field{})) + uint64(native.MaxTokens)*uint64(unsafe.Sizeof(native.Span{}))
	if sum > 48<<20 {
		t.Fatalf("inspection sum %d", sum)
	}
	t.Logf("token=%d command=%d finding=%d record=%d field=%d span=%d full conservative=%d <48MiB", unsafe.Sizeof(native.Token{}), unsafe.Sizeof(native.Command{}), unsafe.Sizeof(native.Finding{}), unsafe.Sizeof(native.Record{}), unsafe.Sizeof(native.Field{}), unsafe.Sizeof(native.Span{}), sum)
}
func BenchmarkCompile(b *testing.B) {
	p, s := program(b, primary(b, "209"))
	b.ReportAllocs()
	for j := 0; j < b.N; j++ {
		if _, e := body.Compile(p, s, body.DefaultLimits()); e != nil {
			b.Fatal(e)
		}
	}
}
func BenchmarkEvaluate(b *testing.B) {
	p := plan(b, primary(b, "209"))
	d, s := data(b, secondary(b, "209"))
	b.ReportAllocs()
	for j := 0; j < b.N; j++ {
		if _, e := p.Evaluate(d, s, 1); e != nil {
			b.Fatal(e)
		}
	}
}

func maximum(t testing.TB) (native.Program, native.Source, explicit.Data, native.Source) {
	t.Helper()
	raw := append([]byte(strings.Repeat("P", 4092)), command(0x36, "1")...)
	raw = append(raw, '\n')
	p, s := program(t, authored(t, raw))
	d, ds := data(t, bytes.Replace(secondary(t, "207"), []byte("Alice"), []byte(strings.Repeat("V", 61443)), 1))
	return p, s, d, ds
}
func TestExactMaximumBody(t *testing.T) {
	p, s, d, ds := maximum(t)
	q, e := body.Compile(p, s, body.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	r, e := q.Evaluate(d, ds, 1)
	if e != nil {
		t.Fatal(e)
	}
	b, _ := r.Bytes()
	if len(b) != 65536 || string(b[:4092]) != strings.Repeat("P", 4092) || string(b[4092:65535]) != strings.Repeat("V", 61443) || b[65535] != '\n' {
		t.Fatal("maximum output")
	}
	l := body.DefaultLimits()
	l.BodyBytes = 65535
	q, e = body.Compile(p, s, l)
	if e != nil {
		t.Fatal(e)
	}
	if r, e := q.Evaluate(d, ds, 1); e == nil || r.Valid() {
		t.Fatal("one-byte overflow")
	}
}
func BenchmarkCompileMaximum(b *testing.B) {
	p, s, _, _ := maximum(b)
	b.ReportAllocs()
	b.ResetTimer()
	for j := 0; j < b.N; j++ {
		if _, e := body.Compile(p, s, body.DefaultLimits()); e != nil {
			b.Fatal(e)
		}
	}
}
func BenchmarkEvaluateMaximum(b *testing.B) {
	p, s, d, ds := maximum(b)
	q, e := body.Compile(p, s, body.DefaultLimits())
	if e != nil {
		b.Fatal(e)
	}
	b.ReportAllocs()
	b.ResetTimer()
	for j := 0; j < b.N; j++ {
		r, e := q.Evaluate(d, ds, 1)
		if e != nil {
			b.Fatal(e)
		}
		if _, e = r.Bytes(); e != nil {
			b.Fatal(e)
		}
		if _, ok := r.Provenance(); !ok {
			b.Fatal("provenance")
		}
	}
}
