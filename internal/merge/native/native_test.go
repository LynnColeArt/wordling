package native_test

import (
	"bytes"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	n "github.com/lynncoleart/wordling/internal/merge/native"
	"github.com/lynncoleart/wordling/internal/wp51"
	"os"
	"path/filepath"
	"runtime"
	"sync"
	"testing"
	"time"
)

// Synthetic outer fixtures ONLY, not a product constructor or native writer.
func framed(body []byte) []byte {
	p := make([]byte, 66)
	copy(p, []byte{0xff, 'W', 'P', 'C', 66, 0, 0, 0, 1, 10, 0, 1})
	copy(p[16:], []byte{0xfb, 0xff, 5, 0, 50, 0})
	return append(p, body...)
}
func de(code byte, payload ...byte) []byte {
	l := 4 + len(payload)
	b := []byte{0xde, code, byte(l), byte(l >> 8)}
	b = append(b, payload...)
	return append(b, byte(l), byte(l>>8), code, 0xde)
}
func join(parts ...[]byte) []byte { return bytes.Join(parts, nil) }
func parse(t testing.TB, body []byte) *n.Image {
	t.Helper()
	im, e := n.Parse(framed(body), n.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	return im
}
func view(t testing.TB, im *n.Image, role n.Role) *n.View {
	t.Helper()
	v, e := im.View(role)
	if e != nil {
		t.Fatal(e)
	}
	return v
}
func codes(v *n.View) map[string]bool {
	i, _ := v.Inspect()
	out := map[string]bool{}
	for _, f := range i.Findings {
		out[f.Code] = true
	}
	return out
}
func failureCode(t testing.TB, err error, want string) {
	t.Helper()
	var f *n.Failure
	if !errors.As(err, &f) || f.Category != want {
		t.Fatalf("got %v want %s", err, want)
	}
}
func checkSpan(t testing.TB, v *n.View, raw []byte, s n.Span) {
	t.Helper()
	bounds, ok := s.Bounds()
	if !ok {
		t.Fatal("invalid captured span")
	}
	b, ok := v.Bytes(s)
	if !ok || !bytes.Equal(b, raw[bounds.Offset:bounds.Offset+bounds.Length]) {
		t.Fatalf("wrong source span %+v", bounds)
	}
}

type original struct {
	Path, Role, SHA256 string
	GitBlob            string `json:"git_blob"`
	Bytes              int
	BodyOffset         int `json:"body_offset"`
	Tokens             []struct {
		Offset int
		Raw    string
	}
}

func originals(t testing.TB) []original {
	t.Helper()
	data, e := os.ReadFile("evidence/originals.json")
	if e != nil {
		t.Fatal(e)
	}
	var d struct{ Files []original }
	if e = json.Unmarshal(data, &d); e != nil {
		t.Fatal(e)
	}
	return d.Files
}
func TestAll104OriginalPublicSpansAndRoles(t *testing.T) {
	rows := originals(t)
	if len(rows) != 104 {
		t.Fatal(len(rows))
	}
	hashes := map[string]bool{}
	seen := map[n.CommandKind]bool{}
	empty := false
	supported := 0
	for _, r := range rows {
		t.Run(r.Path, func(t *testing.T) {
			raw, e := os.ReadFile(filepath.Join("../../..", r.Path))
			if e != nil {
				t.Fatal(e)
			}
			digest := sha256.Sum256(raw)
			if hex.EncodeToString(digest[:]) != r.SHA256 || len(raw) != r.Bytes {
				t.Fatal("source identity")
			}
			blob := sha1.New()
			fmt.Fprintf(blob, "blob %d%c", len(raw), 0)
			blob.Write(raw)
			if hex.EncodeToString(blob.Sum(nil)) != r.GitBlob {
				t.Fatal("Git object identity")
			}
			hashes[r.SHA256] = true
			im, e := n.Parse(raw, n.DefaultLimits())
			if e != nil {
				t.Fatal(e)
			}
			if !bytes.Equal(im.Export(), raw) {
				t.Fatal("lossy export")
			}
			role := map[string]n.Role{"Primary": n.Primary, "Secondary": n.Secondary, "Result": n.Result}[r.Role]
			v := view(t, im, role)
			info, _ := v.Inspect()
			if len(info.Tokens) != len(r.Tokens) {
				t.Fatalf("tokens %d/%d", len(info.Tokens), len(r.Tokens))
			}
			for j, token := range info.Tokens {
				checkSpan(t, v, raw, token.Raw)
				span, _ := token.Raw.Bounds()
				want, _ := hex.DecodeString(r.Tokens[j].Raw)
				got, _ := v.Bytes(token.Raw)
				if span.Offset != r.Tokens[j].Offset || !bytes.Equal(got, want) {
					t.Fatal("outer span disagreement")
				}
			}
			for _, c := range info.Commands {
				seen[c.Kind] = true
				checkSpan(t, v, raw, c.Function)
				checkSpan(t, v, raw, c.Payload)
				if c.Operand.Kind != 0 {
					checkSpan(t, v, raw, c.Operand.Data)
					checkSpan(t, v, raw, c.Operand.Terminator)
					term, _ := v.Bytes(c.Operand.Terminator)
					if !bytes.Equal(term, []byte("~")) {
						t.Fatal("operand terminator")
					}
				}
			}
			for _, record := range info.Records {
				checkSpan(t, v, raw, record.Raw)
				checkSpan(t, v, raw, record.EndRecord)
				checkSpan(t, v, raw, record.Tail)
				for _, s := range record.Interstitial {
					checkSpan(t, v, raw, s)
				}
				for _, f := range record.Fields {
					checkSpan(t, v, raw, f.Content)
					checkSpan(t, v, raw, f.EndField)
					if _, ok := f.Separator.Bounds(); ok {
						checkSpan(t, v, raw, f.Separator)
					}
					empty = empty || f.Empty
				}
			}
			for _, f := range info.Findings {
				checkSpan(t, v, raw, f.At)
			}
			if role == n.Result {
				if v.Supported() {
					t.Fatal("Result admitted")
				}
				if p, e := v.Admit(); e == nil || p.Valid() {
					t.Fatal("Result program")
				}
			}
			if role == n.Secondary {
				if v.Supported() || !codes(v)["RecordCountUnresolved"] {
					t.Fatal("unresolved record relationship admitted")
				}
			}
			if v.Supported() {
				supported++
			}
		})
	}
	if len(hashes) != 35 || len(seen) != 11 || !empty || supported == 0 {
		t.Fatalf("hashes%d commands%d genuineempty%v supported%d", len(hashes), len(seen), empty, supported)
	}
}
func TestOwnershipCapturedProgramAndWrapperSubstitution(t *testing.T) {
	raw := framed(join([]byte("hello "), de(0x36), []byte("1~")))
	im, e := n.Parse(raw, n.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	v := view(t, im, n.Primary)
	p, e := v.Admit()
	if e != nil {
		t.Fatal(e)
	}
	source := p.Source()
	savedView := *v
	copyIm := *im
	original := bytes.Clone(raw)
	for j := range raw {
		raw[j] = 0
	}
	if !bytes.Equal(v.Export(), original) {
		t.Fatal("caller alias")
	}
	other := parse(t, []byte("different"))
	otherView := view(t, other, n.Primary)
	*im = *other
	*v = *otherView
	if !p.Source().Equal(source) || !bytes.Equal(savedView.Export(), original) || !bytes.Equal(copyIm.Export(), original) {
		t.Fatal("wrapper retarget")
	}
	info, _ := p.Inspect()
	token := info.Tokens[0].Raw
	out, _ := p.Bytes(token)
	out[0] = 0
	info.Commands[0].Operand.Data = n.Span{}
	info.Tokens[0].Raw = n.Span{}
	info.Findings = append(info.Findings, n.Finding{Code: "invented"})
	if !p.Valid() {
		t.Fatal("inspection became authority")
	}
	fresh, _ := p.Inspect()
	if len(fresh.Findings) != 0 || fresh.Commands[0].Operand.Kind != n.FieldNumber {
		t.Fatal("inspection alias")
	}
	if _, ok := other.Bytes(token); ok {
		t.Fatal("cross-source")
	}
	if _, ok := p.Bytes(n.Span{}); ok {
		t.Fatal("forged span")
	}
	if _, ok := p.Bytes(fresh.Commands[0].Operand.Terminator); !ok {
		t.Fatal("valid terminator")
	}
	if (n.Source{}).Equal(source) {
		t.Fatal("zero source")
	}
	*im = n.Image{}
	*v = n.View{}
	if !p.Valid() || !bytes.Equal(savedView.Export(), original) {
		t.Fatal("zero wrapper")
	}
	var nilImage *n.Image
	var nilView *n.View
	if nilImage.Valid() || nilImage.Export() != nil || nilView.Supported() || nilView.Export() != nil {
		t.Fatal("nil")
	}
	if _, e := nilImage.View(n.Primary); e == nil {
		t.Fatal("nil role")
	}
	if _, e := nilView.Admit(); e == nil {
		t.Fatal("nil admission")
	}
	if (n.Program{}).Valid() {
		t.Fatal("zero program")
	}
}
func TestRecordsKeepCountsFieldsAndInterstitialUnknowns(t *testing.T) {
	for _, test := range []struct {
		body   []byte
		count  uint16
		values []string
	}{{join([]byte("Alice"), de(0x31), []byte{10}, de(0x34, 2, 0)), 2, []string{"Alice"}}, {join([]byte("Bob"), de(0x31), []byte{10}, de(0x31), []byte{10}, de(0x34, 3, 0)), 3, []string{"Bob", ""}}, {join([]byte("Bob"), de(0x31), []byte{10}, []byte(" "), de(0x31), []byte{10}, de(0x34, 3, 0)), 3, []string{"Bob", " "}}} {
		im := parse(t, test.body)
		v := view(t, im, n.Secondary)
		i, _ := v.Inspect()
		if v.Supported() || !codes(v)["RecordCountUnresolved"] || len(i.Records) != 1 {
			t.Fatal("guessed record admission")
		}
		r := i.Records[0]
		if r.StoredCount != test.count || len(r.Fields) != len(test.values) {
			t.Fatal("count/field conflation")
		}
		for j, f := range r.Fields {
			actual, _ := v.Bytes(f.Content)
			if string(actual) != test.values[j] || f.Empty != (test.values[j] == "") || f.WhitespaceOnly != (test.values[j] == " ") {
				t.Fatal("empty/space/data loss")
			}
		}
		i.Records[0].Fields[0].Content = n.Span{}
		fresh, _ := v.Inspect()
		if _, ok := fresh.Records[0].Fields[0].Content.Bounds(); !ok {
			t.Fatal("field alias")
		}
	}
	// A payload-contained DE/tilde/return/page is wholly opaque, not recursively parsed.
	opaque := []byte{0x0a, 0x0c, '~', 0xde, 0x31, 4, 0, 4, 0, 0x31, 0xde}
	v := view(t, parse(t, de(0x00, opaque...)), n.Primary)
	i, _ := v.Inspect()
	if len(i.Tokens) != 1 || len(i.Commands) != 0 || !codes(v)["UnknownMergeCommand"] {
		t.Fatal("payload recursion")
	}
}
func TestSemanticFailuresAndNonFixtureSuccess(t *testing.T) {
	for _, b := range [][]byte{[]byte("arbitrary text"), join(de(0x36), []byte("1~")), join(de(0x3b), []byte("2~x"), de(0x30), []byte("y"), de(0x33)), join(de(0x4d), []byte("x"), de(0x4e), de(0x22))} {
		if !view(t, parse(t, b), n.Primary).Supported() {
			t.Fatalf("synthetic known context %x", b)
		}
	}
	tests := []struct {
		body []byte
		code string
	}{{de(0x99), "UnknownMergeCommand"}, {de(0x36, 1, 2), "CommandPayloadUnsupported"}, {de(0x34), "CommandPayloadUnsupported"}, {join(de(0x36), []byte("1")), "OperandDelimiterMissing"}, {join(de(0x36), []byte("1literal~")), "OperandSyntax"}, {join(de(0x36), de(0x4d)), "OperandDelimiterMissing"}, {join(de(0x36), []byte{0x80, '~'}), "OperandDelimiterMissing"}, {join(de(0x36), []byte("2~")), "UnobservedOperand"}, {join(de(0x3b), []byte("1~"), de(0x33)), "UnobservedOperand"}, {join(de(0x45), []byte("C:\\OUT\\CHILD~")), "NestedResolutionRequired"}, {join(de(0x45), []byte("\"C:\\OUT\\CHILD\"~")), "OperandSyntax"}, {de(0x30), "UnmatchedElse"}, {de(0x33), "UnmatchedEndIf"}, {join(de(0x3b), []byte("2~")), "UnmatchedIf"}, {de(0x31), "WrongCommandRole"}, {[]byte{0xd4, 0, 6, 0, 1, 2, 6, 0, 0, 0xd4}, "FormatterUnresolved"}, {[]byte{'~'}, "LiteralTildeUnsupported"}}
	for _, test := range tests {
		v := view(t, parse(t, test.body), n.Primary)
		if v.Supported() || !codes(v)[test.code] {
			t.Fatalf("%x: expected %s got %v", test.body, test.code, codes(v))
		}
	}
	// Malformed outer framing is wp51's actual typed failure, not retained semantics.
	bad := framed(de(0x36))
	bad[len(bad)-1] = 0
	im, e := n.Parse(bad, n.DefaultLimits())
	var outer *wp51.Failure
	if im != nil || !errors.As(e, &outer) || outer.Category != wp51.MalformedBody {
		t.Fatal(e)
	}
	missing := view(t, parse(t, join(de(0x36), []byte("1literal"), de(0x4d))), n.Primary)
	ii, _ := missing.Inspect()
	if len(ii.Commands) != 2 || ii.Commands[0].Operand.Kind != 0 || ii.Commands[1].Kind != n.PageOff {
		t.Fatal("swallowed next command/literal")
	}
}
func TestExactAndOneOverLimits(t *testing.T) {
	l := n.DefaultLimits()
	for _, bad := range []n.Limits{{}, {Bytes: n.MaxBytes + 1}} {
		if _, e := n.Parse(framed(nil), bad); e == nil {
			t.Fatal("bad limits")
		}
	}
	raw := framed([]byte("ab"))
	l.Bytes = len(raw)
	l.Tokens = 2
	if _, e := n.Parse(raw, l); e != nil {
		t.Fatal(e)
	}
	l.Bytes--
	_, e := n.Parse(raw, l)
	failureCode(t, e, "InputLimit")
	l.Bytes++
	l.Tokens--
	_, e = n.Parse(raw, l)
	failureCode(t, e, "TokenLimit")
	body := join(de(0x36), []byte("1~"))
	l = n.DefaultLimits()
	l.Operand = 2
	im, e := n.Parse(framed(body), l)
	if e != nil {
		t.Fatal(e)
	}
	if _, e = im.View(n.Primary); e != nil {
		t.Fatal(e)
	}
	l.Operand = 1
	im, e = n.Parse(framed(body), l)
	if e != nil {
		t.Fatal(e)
	}
	_, e = im.View(n.Primary)
	failureCode(t, e, "OperandLimit")
	record := join([]byte("a"), de(0x31), []byte{10}, de(0x34, 2, 0))
	l = n.DefaultLimits()
	l.Fields = 1
	l.Records = 1
	im, e = n.Parse(framed(record), l)
	if e != nil {
		t.Fatal(e)
	}
	if _, e = im.View(n.Secondary); e != nil {
		t.Fatal(e)
	}
	im, e = n.Parse(framed(join(record, record)), l)
	if e != nil {
		t.Fatal(e)
	}
	_, e = im.View(n.Secondary)
	failureCode(t, e, "FieldLimit")
	l.Fields = 2
	im, e = n.Parse(framed(join(record, record)), l)
	if e != nil {
		t.Fatal(e)
	}
	_, e = im.View(n.Secondary)
	failureCode(t, e, "RecordLimit")
	l = n.DefaultLimits()
	l.Findings = 1
	im, e = n.Parse(framed(join(de(0x99), de(0x98))), l)
	if e != nil {
		t.Fatal(e)
	}
	v := view(t, im, n.Primary)
	i, _ := v.Inspect()
	if v.Supported() || len(i.Findings) != 1 || !i.FindingsCapped || i.Findings[0].Code != "FindingsCapped" {
		t.Fatal("hidden unsupported")
	}
	l = n.DefaultLimits()
	l.Depth = 1
	im, e = n.Parse(framed(join(de(0x3b), []byte("2~"), de(0x3b), []byte("2~"))), l)
	if e != nil {
		t.Fatal(e)
	}
	_, e = im.View(n.Primary)
	failureCode(t, e, "DepthLimit")
	if _, e = im.View(n.Role(0)); e == nil {
		t.Fatal("invalid role")
	}
}
func TestResourceWorkAndConcurrency(t *testing.T) {
	// Exact1MiB with15 large opaque functions plus bounded remaining ASCII.
	function := de(0xd0, make([]byte, 65531)...)
	body := bytes.Repeat(function, 15)
	body = append(body, bytes.Repeat([]byte{' '}, n.MaxBytes-66-len(body))...)
	raw := framed(body)
	runtime.GC()
	var before, after runtime.MemStats
	runtime.ReadMemStats(&before)
	start := time.Now()
	im, e := n.Parse(raw, n.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	v := view(t, im, n.Result)
	info, _ := v.Inspect()
	export := v.Export()
	runtime.ReadMemStats(&after)
	allocated := after.TotalAlloc - before.TotalAlloc
	t.Logf("input=%d tokens=%d workBytes=%d allocation=%d elapsed=%s", len(raw), len(info.Tokens), info.WorkBytes, allocated, time.Since(start))
	if allocated > 32<<20 || info.WorkBytes > 3*len(raw) || !bytes.Equal(export, raw) {
		t.Fatal("bounded work/ownership")
	}
	_, e = n.Parse(append(bytes.Clone(raw), 'x'), n.DefaultLimits())
	failureCode(t, e, "InputLimit")
	small := parse(t, join([]byte("x"), de(0x36), []byte("1~")))
	v = view(t, small, n.Primary)
	var wg sync.WaitGroup
	for j := 0; j < 8; j++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for k := 0; k < 20; k++ {
				i, _ := v.Inspect()
				out := v.Export()
				if !v.Supported() || len(i.Commands) != 1 || len(out) == 0 {
					t.Error("concurrent read")
				}
			}
		}()
	}
	wg.Wait()
}
func FuzzMergeNative(f *testing.F) {
	for _, r := range originals(f) {
		raw, e := os.ReadFile(filepath.Join("../../..", r.Path))
		if e != nil {
			f.Fatal(e)
		}
		for _, role := range []byte{1, 2, 3} {
			f.Add(raw, role)
		}
	}
	for _, raw := range [][]byte{framed(nil), framed(join(de(0x36), []byte("1~"))), framed(de(0x99)), {0, 0x7f, 0xff}} {
		f.Add(raw, byte(1))
	}
	f.Fuzz(func(t *testing.T, raw []byte, role byte) {
		l := n.DefaultLimits()
		l.Bytes = 4096
		l.Tokens = 2048
		l.Fields = 64
		l.Records = 64
		l.Operand = 64
		l.Findings = 8
		l.Depth = 8
		before := bytes.Clone(raw)
		im, e := n.Parse(raw, l)
		if !bytes.Equal(before, raw) {
			t.Fatal("caller mutated")
		}
		if e != nil {
			if im != nil {
				t.Fatal("partial acceptance")
			}
			return
		}
		if !bytes.Equal(im.Export(), raw) {
			t.Fatal("lossy unknown export")
		}
		v, e := im.View(n.Role(role%3 + 1))
		if e != nil {
			return
		}
		i, _ := v.Inspect()
		if i.Role == n.Result && v.Supported() {
			t.Fatal("Result admission")
		}
		for _, token := range i.Tokens {
			checkSpan(t, v, raw, token.Raw)
		}
		for _, c := range i.Commands {
			checkSpan(t, v, raw, c.Function)
			checkSpan(t, v, raw, c.Payload)
			if c.Operand.Kind != 0 {
				checkSpan(t, v, raw, c.Operand.Data)
				checkSpan(t, v, raw, c.Operand.Terminator)
			}
		}
		if i.WorkBytes > 4*len(raw) {
			t.Fatalf("work %d input%d", i.WorkBytes, len(raw))
		}
		if v.Supported() {
			p, e := v.Admit()
			if e != nil || !p.Valid() {
				t.Fatal("admission identity")
			}
		}
	})
}
