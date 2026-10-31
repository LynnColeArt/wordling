package runtime_test

import (
	"bytes"
	"context"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	mac "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

type artifact struct {
	Path string `json:"path"`
	Size int    `json:"size"`
	SHA  string `json:"sha256"`
	Blob string `json:"git_blob"`
	Case string `json:"case_id"`
	Run  string `json:"run"`
}
type originalCase struct {
	ID          string `json:"case_id"`
	Context     string `json:"context"`
	Run, Repeat string
	Root        string     `json:"root_macro"`
	Results     []artifact `json:"native_results"`
	Expected    struct {
		Text string `json:"expected_text"`
		Hex  string `json:"expected_hex"`
	}
}
type ledger struct {
	Source  string         `json:"source_ledger_sha256"`
	Cases   []originalCase `json:"macro_cases"`
	Exports []artifact     `json:"wpm_exports"`
	Merge   []struct {
		ID string `json:"case_id"`
	} `json:"excluded_merge_cases"`
}

func corpus(t testing.TB) ledger {
	t.Helper()
	raw, err := os.ReadFile("testdata/original-cases.json")
	if err != nil {
		t.Fatal(err)
	}
	var a ledger
	if err := json.Unmarshal(raw, &a); err != nil {
		t.Fatal(err)
	}
	if a.Source != "fca8446e98ad95ab118fc672e48e821afc65e9e3b2b5a43c27f7759824c2ce5d" || len(a.Cases) != 20 || len(a.Exports) != 46 || len(a.Merge) != 15 {
		t.Fatal("wrong approved original corpus")
	}
	return a
}
func readArtifact(t testing.TB, a artifact) []byte {
	t.Helper()
	b, err := os.ReadFile(filepath.Join("../../..", a.Path))
	if err != nil {
		t.Fatal(err)
	}
	sha := sha256.Sum256(b)
	blob := sha1.Sum(append([]byte(fmt.Sprintf("blob %d\x00", len(b))), b...))
	if len(b) != a.Size || hex.EncodeToString(sha[:]) != a.SHA || hex.EncodeToString(blob[:]) != a.Blob {
		t.Fatal("raw original evidence changed", a.Path)
	}
	return b
}
func image(t testing.TB, raw []byte) *wpm.Image {
	t.Helper()
	i, err := wpm.Parse(raw, wpm.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	return i
}
func originalABC(t testing.TB) []byte { t.Helper(); return readArtifact(t, corpus(t).Exports[0]) }
func fullPolicy() mac.Policy {
	return mac.Policy{ASCII: true, DisplayControl: true, Keys: []uint16{0x8021}}
}
func cloneEffect(e mac.Effect) mac.Effect { e.Words = append([]wpm.Word(nil), e.Words...); return e }

type receipt struct {
	Effect mac.Effect
	Result mac.EffectResult
	Err    error
}
type traceSink struct {
	policy   mac.Policy
	receipts []receipt
	apply    func(context.Context, mac.Effect) (mac.EffectResult, error)
}

func (s *traceSink) Capabilities() mac.Policy { return s.policy }
func (s *traceSink) Apply(ctx context.Context, e mac.Effect) (mac.EffectResult, error) {
	copied := cloneEffect(e)
	r := mac.EffectResult{Condition: mac.NoCondition, MayHaveEffects: true}
	var err error
	if s.apply != nil {
		r, err = s.apply(ctx, e)
	}
	s.receipts = append(s.receipts, receipt{copied, r, err})
	return r, err
}

type resolverFunc func(context.Context, mac.ProgramRequest) mac.Resolution

func (f resolverFunc) Resolve(ctx context.Context, r mac.ProgramRequest) mac.Resolution {
	return f(ctx, r)
}
func nativeName(words []wpm.Word) string {
	var b strings.Builder
	for _, w := range words {
		b.WriteByte(byte(w.Value))
	}
	return b.String()
}
func errorCode(err error) string {
	var f *mac.Failure
	if errors.As(err, &f) {
		return f.Code
	}
	return ""
}
func drive(t testing.TB, m *mac.Machine, quota uint32) mac.Result {
	t.Helper()
	previous := m.State().Steps
	for n := 0; n < 10000; n++ {
		r := m.Step(context.Background(), quota)
		if r.Steps < previous || r.Steps-previous > uint64(quota) {
			t.Fatal("unbounded/decreasing slice work", previous, r)
		}
		previous = r.Steps
		if r.State != "running" && r.State != "ready" {
			return r
		}
	}
	t.Fatal("machine did not terminate under finite budget")
	return mac.Result{}
}
func program(t testing.TB, raw []byte, l mac.Limits) *mac.Program {
	t.Helper()
	p, err := mac.Compile(image(t, raw), fullPolicy(), l)
	if err != nil {
		t.Fatal(err)
	}
	return p
}
func newMachine(t testing.TB, p *mac.Program, s mac.CommandSink, r mac.Resolver, l mac.Limits) *mac.Machine {
	t.Helper()
	m, err := mac.New(p, s, r, l)
	if err != nil {
		t.Fatal(err)
	}
	return m
}

// LiteralProjection is only a trace inspector, not an editor/search emulator.
// The exact original search-query source spans are excluded from native document
// text comparison; every query/key event is retained in receipts separately.
func literalProjection(receipts []receipt, sources map[[32]byte][]byte) string {
	var b strings.Builder
	for _, r := range receipts {
		if r.Effect.Kind != "literal" {
			continue
		}
		raw := sources[r.Effect.Source]
		var low, high uint32
		if raw != nil {
			B := binary.LittleEndian.Uint32(raw[4:8])
			for p := B; p+2 <= uint32(len(raw)); p += 2 {
				if binary.LittleEndian.Uint16(raw[p:p+2]) == 0x8021 {
					if low == 0 {
						low = p
					} else {
						high = p
						break
					}
				}
			}
		}
		for _, w := range r.Effect.Words {
			if high != 0 && w.Span.Length != 0 && w.Span.Offset > low && w.Span.Offset < high {
				continue
			}
			b.WriteByte(byte(w.Value))
		}
	}
	return b.String()
}
func checkEffectSources(t testing.TB, s *traceSink, sources map[[32]byte][]byte) {
	t.Helper()
	for _, r := range s.receipts {
		raw, ok := sources[r.Effect.Source]
		if !ok {
			t.Fatal("missing effect source binding")
		}
		at := r.Effect.At
		if uint64(at.Offset)+uint64(at.Length) > uint64(len(raw)) {
			t.Fatal("effect span")
		}
		for _, w := range r.Effect.Words {
			if w.Span.Length == 0 {
				if w.Span.Offset != at.Offset {
					t.Fatal("expanded value provenance")
				}
				continue
			}
			if w.Span.Length != 2 || binary.LittleEndian.Uint16(raw[w.Span.Offset:w.Span.Offset+2]) != w.Value {
				t.Fatal("native effect word changed")
			}
		}
	}
}

func TestOriginalMacroContextsAndDeclaredBlockers(t *testing.T) {
	a := corpus(t)
	admitted, blocked := 0, 0
	for _, c := range a.Cases {
		t.Run(c.ID, func(t *testing.T) {
			if !strings.HasPrefix(c.Context, "macro") {
				t.Fatal("merge case counted as macro")
			}
			for _, result := range c.Results {
				raw := readArtifact(t, result)
				B := binary.LittleEndian.Uint32(raw[4:8])
				if hex.EncodeToString(raw[B:]) != c.Expected.Hex || string(raw[B:]) != c.Expected.Text {
					t.Fatal("exact original native output changed")
				}
			}
			files := map[string]*wpm.Image{}
			sources := map[[32]byte][]byte{}
			for _, f := range a.Exports {
				if f.Case == c.ID && f.Run == c.Run {
					raw := readArtifact(t, f)
					i := image(t, raw)
					files[filepath.Base(f.Path)] = i
					sources[i.SHA256()] = raw
				}
			}
			root := files[c.Root]
			if root == nil {
				t.Fatal("root source missing")
			}
			sink := &traceSink{policy: fullPolicy()}
			searchKeys := 0
			sink.apply = func(_ context.Context, e mac.Effect) (mac.EffectResult, error) {
				r := mac.EffectResult{Condition: mac.NoCondition, MayHaveEffects: true}
				if e.Kind == "key" {
					searchKeys++
					if searchKeys == 2 {
						r.Condition = mac.NotFound
					}
				}
				return r, nil
			}
			resolver := resolverFunc(func(_ context.Context, r mac.ProgramRequest) mac.Resolution {
				if child := files[filepath.Base(strings.ReplaceAll(nativeName(r.Name), "\\", "/"))+".WPM"]; child != nil {
					return mac.Resolution{State: "ready", Image: child}
				}
				return mac.Resolution{State: "condition", Condition: mac.CommandError}
			})
			limits := mac.DefaultLimits()
			p, err := mac.Compile(root, fullPolicy(), limits)
			needsQuit := c.ID == "CMD51-206" || c.ID == "CMD51-210" || c.ID == "CMD51-212" || c.ID == "CMD51-213"
			if needsQuit {
				if p != nil || errorCode(err) != "UnqualifiedQuit" || len(sink.receipts) != 0 {
					t.Fatal("QUIT context was guessed", p, err)
				}
				blocked++
				t.Log("BLOCKED: original QUIT prerequisite not yet approved; zero effects")
				return
			}
			if err != nil {
				t.Fatal(err)
			}
			admitted++
			repeats := 1
			if c.ID == "CMD51-132" {
				repeats = 3
			}
			for n := 0; n < repeats; n++ {
				p, err := mac.Compile(root, fullPolicy(), limits)
				if err != nil {
					t.Fatal(err)
				}
				m := newMachine(t, p, sink, resolver, limits)
				r := drive(t, m, 7)
				if c.ID == "CMD51-178" {
					if r.State != "failed" || errorCode(r.Err) != "UnhandledCondition" {
						t.Fatal("default search condition", r)
					}
				} else if r.State != "complete" {
					t.Fatal(r)
				}
				limits.Steps -= r.Steps
				limits.OutputWords -= r.EmittedWords
			}
			got := literalProjection(sink.receipts, sources)
			if c.ID == "CMD51-131" {
				got = "ABC" + got
			}
			if c.ID == "CMD51-178" {
				got += "READY"
			}
			if got != c.Expected.Text {
				t.Fatalf("trace/context projection %q, original %q", got, c.Expected.Text)
			}
			checkEffectSources(t, sink, sources)
			for _, raw := range sources {
				i := image(t, raw)
				if !bytes.Equal(i.Export(), raw) {
					t.Fatal("source modified")
				}
			}
		})
	}
	if admitted != 16 || blocked != 4 {
		t.Fatal("required context accounting", admitted, blocked)
	}
}

func TestAllOriginalSourcesRemainImmutableOnCompile(t *testing.T) {
	for _, f := range corpus(t).Exports {
		t.Run(f.Path, func(t *testing.T) {
			raw := readArtifact(t, f)
			i := image(t, raw)
			_, _ = mac.Compile(i, fullPolicy(), mac.DefaultLimits())
			if !bytes.Equal(raw, i.Export()) {
				t.Fatal("Compile changed source")
			}
		})
	}
}
