package body_test

import (
	"bytes"
	"errors"
	"os"
	"sync"
	"testing"

	"github.com/lynncoleart/wordling/internal/merge/body"
	"github.com/lynncoleart/wordling/internal/merge/explicit"
	"github.com/lynncoleart/wordling/internal/merge/native"
)

func fixture(t testing.TB, name string) []byte {
	t.Helper()
	b, e := os.ReadFile("../../../docs/research/reference-runs/" + name)
	if e != nil {
		t.Fatal(e)
	}
	return b
}
func image(t testing.TB, b []byte, role native.Role) (*native.Image, *native.View) {
	t.Helper()
	i, e := native.Parse(b, native.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	v, e := i.View(role)
	if e != nil {
		t.Fatal(e)
	}
	return i, v
}
func program(t testing.TB, b []byte) (native.Program, native.Source) {
	t.Helper()
	i, v := image(t, b, native.Primary)
	p, e := v.Admit()
	if e != nil {
		t.Fatal(e)
	}
	return p, i.Source()
}
func data(t testing.TB, b []byte) (explicit.Data, native.Source) {
	t.Helper()
	i, v := image(t, b, native.Secondary)
	d, e := explicit.Admit(v, i.Source())
	if e != nil {
		t.Fatal(e)
	}
	return d, i.Source()
}
func primary(t testing.TB, n string) []byte {
	return fixture(t, "2026-10-29-advanced-03/CMD51-"+n+"/PRIMARY.WP5")
}
func secondary(t testing.TB, n string) []byte {
	return fixture(t, "2026-10-29-advanced-03/CMD51-"+n+"/SECOND.WP5")
}
func plan(t testing.TB, b []byte) body.Plan {
	t.Helper()
	p, s := program(t, b)
	q, e := body.Compile(p, s, body.DefaultLimits())
	if e != nil || !q.Valid() {
		t.Fatal(e)
	}
	return q
}
func result(t testing.TB, p body.Plan, d explicit.Data, s native.Source, r int, want string) body.Result {
	t.Helper()
	v, e := p.Evaluate(d, s, r)
	if e != nil || !v.Valid() {
		t.Fatalf("record%d: %v", r, e)
	}
	b, e := v.Bytes()
	if e != nil || string(b) != want {
		t.Fatalf("got %q want %q: %v", b, want, e)
	}
	pr, ok := v.Provenance()
	if !ok || !pr.Secondary.Equal(s) || pr.Record != r || len(pr.Trace) == 0 {
		t.Fatal("provenance")
	}
	return v
}
func frame(k byte) []byte             { return []byte{0xde, k, 4, 0, 4, 0, k, 0xde} }
func command(k byte, n string) []byte { b := frame(k); return append(b, []byte(n+"~")...) }
func authored(t testing.TB, b []byte) []byte {
	t.Helper()
	base := primary(t, "207")
	i, _ := image(t, base, native.Primary)
	f, _ := i.Framing()
	return append(append([]byte(nil), base[:f.Body.Offset]...), b...)
}
func formB(a, b, c string) []byte {
	x := command(0x3b, "2")
	x = append(x, []byte(a)...)
	x = append(x, frame(0x30)...)
	x = append(x, []byte(b)...)
	x = append(x, frame(0x33)...)
	x = append(x, []byte(c)...)
	return append(x, command(0x36, "1")...)
}
func TestAlternativeBodiesAndExactFootprints(t *testing.T) {
	d, s := data(t, secondary(t, "209"))
	p := plan(t, authored(t, formB("VACANT", "PRESENT", " / ")))
	a := result(t, p, d, s, 1, "PRESENT / Alice")
	result(t, p, d, s, 2, "VACANT / Bob")
	pr, _ := a.Provenance()
	if !pr.Conditional || pr.Blank || len(pr.Accesses) != 2 {
		t.Fatal("decision")
	}
	total := 0
	for _, tr := range pr.Trace {
		if tr.Start != total {
			t.Fatal("range")
		}
		sp, ok := tr.Span.Bounds()
		if !ok || tr.Length != sp.Length {
			t.Fatal("span")
		}
		total += tr.Length
	}
	if total != len("PRESENT / Alice") {
		t.Fatal(total)
	}
	changed := bytes.ReplaceAll(secondary(t, "209"), []byte("Alice"), []byte("Zelda"))
	changed = bytes.ReplaceAll(changed, []byte("Bob"), []byte("Eve"))
	d2, s2 := data(t, changed)
	result(t, p, d2, s2, 1, "PRESENT / Zelda")
	result(t, p, d2, s2, 2, "VACANT / Eve")
}
func TestMissingEmptyInvalidAndForeign(t *testing.T) {
	p, s := program(t, primary(t, "209"))
	q, e := body.Compile(p, s, body.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	d, ds := data(t, secondary(t, "207"))
	r, e := q.Evaluate(d, ds, 1)
	var m *explicit.ExplicitFieldMissing
	if r.Valid() || !errors.As(e, &m) || m.Field != 2 {
		t.Fatalf("missing %v", e)
	}
	for _, n := range []int{0, -1, 3} {
		r, e = q.Evaluate(d, ds, n)
		if e == nil || r.Valid() {
			t.Fatal("ordinal")
		}
	}
	other, foreign := program(t, primary(t, "209"))
	if x, e := body.Compile(p, foreign, body.DefaultLimits()); e == nil || x.Valid() {
		t.Fatal("primary owner")
	}
	if x, e := body.Compile(other, foreign, body.DefaultLimits()); e != nil || !x.Valid() {
		t.Fatal("equivalent pair")
	}
	_, df := data(t, secondary(t, "207"))
	if x, e := q.Evaluate(d, df, 1); e == nil || x.Valid() {
		t.Fatal("secondary owner")
	}
	if x, e := body.Compile(native.Program{}, s, body.DefaultLimits()); e == nil || x.Valid() {
		t.Fatal("zero program")
	}
	if x, e := body.Compile(p, native.Source{}, body.DefaultLimits()); e == nil || x.Valid() {
		t.Fatal("zero source")
	}
	if x, e := q.Evaluate(explicit.Data{}, ds, 1); e == nil || x.Valid() {
		t.Fatal("zero data")
	}
	if x, e := q.Evaluate(d, native.Source{}, 1); e == nil || x.Valid() {
		t.Fatal("zero secondary")
	}
	if x, e := (body.Plan{}).Evaluate(d, ds, 1); e == nil || x.Valid() {
		t.Fatal("zero plan")
	}
	if _, e := (body.Result{}).Bytes(); e == nil {
		t.Fatal("zero bytes")
	}
	if _, ok := (body.Result{}).Provenance(); ok {
		t.Fatal("zero provenance")
	}
}
func TestWholePrimaryRefusals(t *testing.T) {
	forms := [][]byte{formB("", "NO", " "), formB("YES", "", " "), formB("YES", "NO", ""), append(formB("YES", "NO", " "), 'x'), append(formB("YES", "NO", " "), '\n'), append([]byte("Hi "), command(0x36, "1")...), append(append([]byte("Hi "), command(0x36, "1")...), '\n', '\n')}
	for _, k := range []byte{0x4d, 0x4e, 0x22} {
		forms = append(forms, formB(string(frame(k)), "NO", " "))
	}
	forms = append(forms, formB("\n", "NO", " "), formB("\f", "NO", " "), formB(string(formB("a", "b", " ")), "NO", " "))
	for j, b := range forms {
		t.Run(string(rune('A'+j)), func(t *testing.T) {
			i, v := image(t, authored(t, b), native.Primary)
			p, e := v.Admit()
			if e != nil {
				return
			}
			q, e := body.Compile(p, i.Source(), body.DefaultLimits())
			if e == nil || q.Valid() {
				t.Fatalf("unsupported accepted %x", b)
			}
		})
	}
	bad := authored(t, append(command(0x3b, "2"), append([]byte("yes"), frame(0x33)...)...))
	p, s := program(t, bad)
	if q, e := body.Compile(p, s, body.DefaultLimits()); e == nil || q.Valid() {
		t.Fatal("optional ELSE")
	}
}
func TestDefensiveCaptureAndReadOnly(t *testing.T) {
	raw := primary(t, "209")
	i, v := image(t, raw, native.Primary)
	p, e := v.Admit()
	if e != nil {
		t.Fatal(e)
	}
	s := i.Source()
	q, e := body.Compile(p, s, body.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	info, _ := p.Inspect()
	info.Tokens[0] = native.Token{}
	info.Commands[0] = native.Command{}
	*i = native.Image{}
	*v = native.View{}
	p = native.Program{}
	d, ds := data(t, secondary(t, "209"))
	r := result(t, q, d, ds, 1, "FILLED Alice")
	b, _ := r.Bytes()
	b[0] = 'x'
	pr, _ := r.Provenance()
	pr.Trace[0].Start = 999
	pr.Accesses[0].Record.Fields[0] = native.Field{}
	pr.Accesses[0].Record.Interstitial[0] = native.Span{}
	pr2, _ := r.Provenance()
	if pr2.Trace[0].Start != 0 || pr2.Accesses[0].Record.Fields[0].Ordinal != 1 {
		t.Fatal("mutable provenance")
	}
	result(t, q, d, ds, 1, "FILLED Alice")
	var wg sync.WaitGroup
	for j := 0; j < 8; j++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for k := 0; k < 8; k++ {
				x, e := q.Evaluate(d, ds, 2)
				if e != nil {
					t.Error(e)
					return
				}
				b, _ := x.Bytes()
				if string(b) != "EMPTY Bob" {
					t.Error(string(b))
				}
			}
		}()
	}
	wg.Wait()
}
