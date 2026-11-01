package explicit_test

import (
	"bytes"
	"encoding/binary"
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"reflect"
	"runtime"
	"sync"
	"testing"

	"github.com/lynncoleart/wordling/internal/merge/explicit"
	"github.com/lynncoleart/wordling/internal/merge/native"
)

func fixture(t testing.TB, name string) []byte {
	t.Helper()
	b, e := os.ReadFile(filepath.Join("../../../docs/research/reference-runs", name))
	if e != nil {
		t.Fatal(e)
	}
	return b
}
func second(t testing.TB) []byte { return fixture(t, "2026-10-29-advanced-03/CMD51-209/SECOND.WP5") }
func parse(t testing.TB, b []byte, role native.Role) (*native.Image, *native.View) {
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
func accept(t testing.TB, b []byte) (*native.Image, *native.View, explicit.Data) {
	t.Helper()
	i, v := parse(t, b, native.Secondary)
	d, e := explicit.Admit(v, i.Source())
	if e != nil {
		t.Fatal(e)
	}
	return i, v, d
}
func field(t testing.TB, d explicit.Data, r, f int, want string, empty bool) {
	t.Helper()
	v, e := d.Field(r, f)
	if e != nil || !v.Valid() {
		t.Fatalf("Field %d/%d: %v", r, f, e)
	}
	b, e := v.Bytes()
	if e != nil || string(b) != want {
		t.Fatalf("bytes %q %v", b, e)
	}
	z, e := v.ExplicitlyEmpty()
	if e != nil || z != empty {
		t.Fatalf("empty %v %v", z, e)
	}
}
func missing(t testing.TB, d explicit.Data, r, f int) {
	t.Helper()
	v, e := d.Field(r, f)
	var m *explicit.ExplicitFieldMissing
	if !errors.As(e, &m) || v.Valid() {
		t.Fatalf("missing %d/%d: %v valid=%v", r, f, e, v.Valid())
	}
	if _, e = v.Bytes(); e == nil {
		t.Fatal("missing bytes accepted")
	}
	if _, e = v.ExplicitlyEmpty(); e == nil {
		t.Fatal("missing empty accepted")
	}
}

func TestOriginalCorpus(t *testing.T) {
	raw, e := os.ReadFile("../../../docs/research/continuation/explicit-secondary-data/corpus.json")
	if e != nil {
		t.Fatal(e)
	}
	var corpus struct {
		Paired []struct {
			SourcePaths map[string]string `json:"source_paths"`
			Values      [][]string        `json:"explicit_values_hex"`
		} `json:"paired"`
	}
	if e = json.Unmarshal(raw, &corpus); e != nil {
		t.Fatal(e)
	}
	records, fields, empty := 0, 0, 0
	profiles := map[string]bool{}
	for _, p := range corpus.Paired {
		b, e := os.ReadFile("../../../" + p.SourcePaths["Secondary"])
		if e != nil {
			t.Fatal(e)
		}
		i, v, d := accept(t, b)
		if !d.Valid() || !d.Source().Equal(i.Source()) {
			t.Fatal("source")
		}
		info, _ := v.Inspect()
		before, _ := json.Marshal(info)
		if d.RecordCount() != len(p.Values) {
			t.Fatal("record count")
		}
		for r, fs := range p.Values {
			records++
			for f, h := range fs {
				want := make([]byte, len(h)/2)
				for k := range want {
					var q uint8
					for _, c := range []byte(h[k*2 : k*2+2]) {
						q *= 16
						if c >= 'a' {
							q += c - 'a' + 10
						} else {
							q += c - '0'
						}
					}
					want[k] = q
				}
				field(t, d, r+1, f+1, string(want), len(want) == 0)
				fields++
				if len(want) == 0 {
					empty++
				}
			}
			missing(t, d, r+1, len(fs)+1)
			o, _ := d.Inspect()
			ob, ok := v.Bytes(o.Records[r].Interstitial[0])
			if !ok {
				t.Fatal("owner")
			}
			profiles[string(ob)] = true
		}
		if !bytes.Equal(i.Export(), b) || !bytes.Equal(v.Export(), b) {
			t.Fatal("export")
		}
		after, _ := v.Inspect()
		a, _ := json.Marshal(after)
		if !bytes.Equal(before, a) || v.Supported() {
			t.Fatal("generic changed")
		}
		if q, e := v.Admit(); e == nil || q.Valid() {
			t.Fatal("generic admitted")
		}
	}
	if records != 24 || fields != 36 || empty != 6 || len(profiles) != 6 {
		t.Fatalf("totals %d/%d/%d/%d", records, fields, empty, len(profiles))
	}
}
func TestPresenceSourceCaptureAndCopies(t *testing.T) {
	b := second(t)
	i, v, d := accept(t, b)
	field(t, d, 1, 1, "Alice", false)
	field(t, d, 1, 2, "YES", false)
	field(t, d, 2, 2, "", true)
	missing(t, d, 0, 1)
	missing(t, d, 1, 0)
	missing(t, d, 3, 1)
	missing(t, d, 1, 3)
	j, w := parse(t, b, native.Secondary)
	if _, e := explicit.Admit(w, i.Source()); e == nil {
		t.Fatal("foreign equal bytes")
	}
	*v = *w
	if _, e := explicit.Admit(v, i.Source()); e == nil {
		t.Fatal("wrapper before")
	}
	x, _ := d.Field(1, 1)
	*i = *j
	*v = native.View{}
	field(t, d, 1, 1, "Alice", false)
	xb, _ := x.Bytes()
	xb[0] = 'X'
	field(t, d, 1, 1, "Alice", false)
	inf, ok := d.Inspect()
	if !ok {
		t.Fatal("inspection")
	}
	inf.Records[0].Fields[0] = native.Field{}
	inf.Records[0].Interstitial[0] = native.Span{}
	inf.Findings[0].Code = "forged"
	inf.Tokens[0] = native.Token{}
	inf.Commands[0] = native.Command{}
	q, _ := d.Inspect()
	if q.Records[0].Fields[0].Ordinal != 1 || q.Findings[0].Code == "forged" {
		t.Fatal("alias")
	}
	r, f, ok := x.Provenance()
	if !ok || f.Ordinal != 1 {
		t.Fatal("provenance")
	}
	r.Fields[0] = native.Field{}
	field(t, d, 1, 1, "Alice", false)
	clone := d
	alias := x
	var wg sync.WaitGroup
	for k := 0; k < 12; k++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for n := 0; n < 40; n++ {
				field(t, clone, 1, 1, "Alice", false)
				z, e := alias.Bytes()
				if e != nil || string(z) != "Alice" {
					t.Error("concurrent")
				}
				o, _ := clone.Inspect()
				o.Records[0].Fields = nil
			}
		}()
	}
	wg.Wait()
	for _, role := range []native.Role{native.Primary, native.Result} {
		a, c := parse(t, b, role)
		if z, e := explicit.Admit(c, a.Source()); e == nil || z.Valid() {
			t.Fatal("role")
		}
	}
	for _, v := range []*native.View{nil, {}, w} {
		if z, e := explicit.Admit(v, native.Source{}); e == nil || z.Valid() {
			t.Fatal("zero source")
		}
	}
	var z explicit.Data
	var val explicit.Value
	if z.Valid() || val.Valid() || z.Source().Valid() || z.RecordCount() != 0 {
		t.Fatal("zero valid")
	}
	if _, ok := z.Inspect(); ok {
		t.Fatal("zero inspection")
	}
	if _, _, ok := val.Provenance(); ok {
		t.Fatal("zero provenance")
	}
	if _, e := val.Bytes(); e == nil {
		t.Fatal("zero bytes")
	}
	if _, e := val.ExplicitlyEmpty(); e == nil {
		t.Fatal("zero empty")
	}
	b = second(t)
	at := bytes.Index(b, []byte("Alice"))
	copy(b[at:], []byte("Clara"))
	_, _, c := accept(t, b)
	field(t, c, 1, 1, "Clara", false)
}
func endfield() []byte        { return []byte{0xde, 0x31, 4, 0, 4, 0, 0x31, 0xde} }
func endrecord(n byte) []byte { return []byte{0xde, 0x34, 6, 0, n, 0, 6, 0, 0x34, 0xde} }
func TestReaderValidRefusals(t *testing.T) {
	b := second(t)
	_, v := parse(t, b, native.Secondary)
	o, _ := v.Inspect()
	f := o.Records[0].Fields[0]
	cb, _ := f.Content.Bounds()
	ef, _ := f.EndField.Bounds()
	er, _ := o.Records[0].EndRecord.Bounds()
	d4, _ := o.Records[0].Interstitial[0].Bounds()
	one := fixture(t, "2026-10-29-advanced-03/CMD51-207/SECOND.WP5")
	_, ov := parse(t, one, native.Secondary)
	oi, _ := ov.Inspect()
	oe, _ := oi.Records[0].EndRecord.Bounds()
	replace := func(b []byte, a, n int, x []byte) []byte {
		return append(append(append([]byte{}, b[:a]...), x...), b[a+n:]...)
	}
	cases := map[string][]byte{"count1": append([]byte{}, b...), "count4": append([]byte{}, b...), "count2two": append([]byte{}, b...), "count3one": append([]byte{}, one...), "third": replace(b, er.Offset, 0, append([]byte{'X'}, append(endfield(), 0x0a)...)), "noEF": replace(b, ef.Offset, 8, nil), "noHR": replace(b, ef.Offset+8, 1, nil), "extraHR": replace(b, ef.Offset+8, 0, []byte{0x0a}), "extraSpace": replace(b, ef.Offset+8, 0, []byte{' '}), "newline": replace(b, cb.Offset, cb.Length, []byte("A\nB")), "allspace": replace(b, cb.Offset, cb.Length, []byte("     ")), "tilde": replace(b, cb.Offset, cb.Length, []byte("A~ice")), "control": replace(b, cb.Offset, cb.Length, []byte{1}), "format": replace(b, cb.Offset, cb.Length, []byte{0xc3, 0x0c, 0xc3}), "tail": replace(b, er.Offset, 0, []byte("TAIL")), "eorExtent": replace(b, er.Offset, 10, []byte{0xde, 0x34, 4, 0, 4, 0, 0x34, 0xde}), "nod4": replace(b, d4.Offset, 32, nil), "extrad4": replace(b, d4.Offset, 0, b[d4.Offset:d4.Offset+32]), "d4move": replace(b, cb.Offset, 0, b[d4.Offset:d4.Offset+32]), "nopage": replace(b, d4.Offset+32, 1, nil), "extrapage": replace(b, d4.Offset+32, 0, []byte{0x0c}), "trailing": append(append([]byte{}, b...), byte('Z')), "unknown": replace(b, cb.Offset, 0, []byte{0xde, 0x20, 4, 0, 4, 0, 0x20, 0xde}), "nested": replace(b, cb.Offset, 0, append([]byte{0xde, 0x46, 4, 0, 4, 0, 0x46, 0xde}, []byte("A~")...)), "context": replace(b, cb.Offset, 0, []byte{0xde, 0x4d, 4, 0, 4, 0, 0x4d, 0xde})}
	cases["count1"][er.Offset+4] = 1
	cases["count4"][er.Offset+4] = 4
	cases["count2two"][er.Offset+4] = 2
	cases["count3one"][oe.Offset+4] = 3
	for _, idx := range []int{1, 6, 8, 17} {
		x := append([]byte{}, b...)
		x[d4.Offset+idx] ^= 1
		if idx == 1 {
			x[d4.Offset+30] ^= 1
		}
		cases["d4alter"+string(rune('a'+idx))] = x
	}
	for _, n := range []byte{3, 4} {
		x := append([]byte{}, one...)
		pos, _ := oi.Records[0].Interstitial[0].Bounds()
		x[pos.Offset+8] = n
		cases["broaderC8"+string(rune('0'+n))] = x
	}
	for name, x := range cases {
		t.Run(name, func(t *testing.T) {
			i, e := native.Parse(x, native.DefaultLimits())
			if e != nil {
				t.Fatalf("must reach DATA boundary: %v", e)
			}
			v, e := i.View(native.Secondary)
			if e != nil {
				t.Fatal(e)
			}
			if d, e := explicit.Admit(v, i.Source()); e == nil || d.Valid() {
				t.Fatal("accepted invalid DATA")
			}
			if !bytes.Equal(i.Export(), x) {
				t.Fatal("changed native")
			}
		})
	}
	lim := native.DefaultLimits()
	lim.Findings = 1
	i, e := native.Parse(b, lim)
	if e != nil {
		t.Fatal(e)
	}
	cv, e := i.View(native.Secondary)
	if e != nil {
		t.Fatal(e)
	}
	if d, e := explicit.Admit(cv, i.Source()); e == nil || d.Valid() {
		t.Fatal("capped")
	}
}
func TestMalformedReaderFirst(t *testing.T) {
	b := second(t)
	for _, x := range [][]byte{nil, b[:20], b[:len(b)-2]} {
		if _, e := native.Parse(x, native.DefaultLimits()); e == nil {
			t.Fatal("reader accepted malformed")
		}
	}
	x := append([]byte{}, b...)
	binary.LittleEndian.PutUint32(x[4:8], 0xffffffff)
	if _, e := native.Parse(x, native.DefaultLimits()); e == nil {
		t.Fatal("reader accepted header")
	}
}
func TestFiniteAdmissionMemory(t *testing.T) {
	b := second(t)
	_, v := parse(t, b, native.Secondary)
	info, _ := v.Inspect()
	var a, c runtime.MemStats
	runtime.GC()
	runtime.ReadMemStats(&a)
	d, e := explicit.Admit(v, info.Source)
	runtime.ReadMemStats(&c)
	if e != nil {
		t.Fatal(e)
	}
	if c.TotalAlloc-a.TotalAlloc > 32<<20 {
		t.Fatal("admission memory cap")
	}
	t.Logf("admission_allocated_bytes=%d records=%d", c.TotalAlloc-a.TotalAlloc, d.RecordCount())
	copy, _ := d.Inspect()
	if !reflect.DeepEqual(info, copy) {
		t.Fatal("metadata not retained")
	}
}
func FuzzAdmission(f *testing.F) {
	f.Add(second(f))
	f.Fuzz(func(t *testing.T, b []byte) {
		if len(b) > native.MaxBytes {
			return
		}
		i, e := native.Parse(b, native.DefaultLimits())
		if e != nil {
			return
		}
		v, e := i.View(native.Secondary)
		if e != nil {
			return
		}
		d, e := explicit.Admit(v, i.Source())
		if e != nil {
			if d.Valid() {
				t.Fatal("partial")
			}
			return
		}
		if !d.Source().Equal(i.Source()) || v.Supported() {
			t.Fatal("authority")
		}
		if !bytes.Equal(i.Export(), b) {
			t.Fatal("export")
		}
		total := 0
		for r := 1; r <= d.RecordCount(); r++ {
			for q := 1; q <= 2; q++ {
				x, e := d.Field(r, q)
				if e != nil {
					break
				}
				z, e := x.Bytes()
				if e != nil {
					t.Fatal(e)
				}
				total += len(z)
			}
		}
		if total > len(b) {
			t.Fatal("cumulative bytes")
		}
	})
}

func TestLargeAdmissionAndSpanOwnership(t *testing.T) {
	b := second(t)
	at := bytes.Index(b, []byte("Alice"))
	b = append(append(append([]byte{}, b[:at]...), bytes.Repeat([]byte{'A'}, 60000)...), b[at+5:]...)
	i, v := parse(t, b, native.Secondary)
	var before, after runtime.MemStats
	runtime.GC()
	runtime.ReadMemStats(&before)
	d, e := explicit.Admit(v, i.Source())
	runtime.ReadMemStats(&after)
	if e != nil {
		t.Fatal(e)
	}
	if after.TotalAlloc-before.TotalAlloc > 32<<20 {
		t.Fatal("admission memory bound")
	}
	x, e := d.Field(1, 1)
	if e != nil {
		t.Fatal(e)
	}
	_, f, ok := x.Provenance()
	if !ok {
		t.Fatal("provenance")
	}
	owned, ok := v.Bytes(f.Content)
	if !ok || len(owned) != 60000 {
		t.Fatal("provenance is foreign")
	}
	_, foreign := parse(t, b, native.Secondary)
	if _, ok = foreign.Bytes(f.Content); ok {
		t.Fatal("foreign source accepted provenance")
	}
	t.Logf("large_input=%d admission_allocated_bytes=%d value_bytes=%d", len(b), after.TotalAlloc-before.TotalAlloc, len(owned))
}
