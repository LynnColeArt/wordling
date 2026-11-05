package wpm_test

import (
	"bytes"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"strconv"
	"strings"
	"sync"
	"testing"

	"github.com/lynncoleart/wordling/internal/macro/wpm"
	"github.com/lynncoleart/wordling/internal/wp51"
)

type fixture struct {
	Path        string   `json:"path"`
	Size        int      `json:"size"`
	SHA256      string   `json:"sha256"`
	GitBlob     string   `json:"git_blob"`
	Case        string   `json:"case_id"`
	BodyOffset  uint32   `json:"body_offset"`
	BodyWords   []string `json:"body_words"`
	Description struct {
		Offset, Length uint32
	} `json:"description_span"`
}

func root() string { return filepath.Join("..", "..", "..") }
func fixtures(t testing.TB) []fixture {
	t.Helper()
	b, err := os.ReadFile("testdata/original-fixtures.json")
	if err != nil {
		t.Fatal(err)
	}
	var ledger struct {
		SourceCommit string    `json:"source_commit"`
		SourceSHA256 string    `json:"source_ledger_sha256"`
		Exports      []fixture `json:"wpm_exports"`
	}
	if err := json.Unmarshal(b, &ledger); err != nil {
		t.Fatal(err)
	}
	if len(ledger.Exports) != 46 {
		t.Fatalf("need all46 original exports, got %d", len(ledger.Exports))
	}
	if ledger.SourceCommit != "4eb851eac3096d27d4743616ce3ae74f7a9edc05" || ledger.SourceSHA256 != "fca8446e98ad95ab118fc672e48e821afc65e9e3b2b5a43c27f7759824c2ce5d" {
		t.Fatal("wrong approved fixture ledger source")
	}
	return ledger.Exports
}
func readFixture(t testing.TB, fixture fixture) []byte {
	t.Helper()
	b, err := os.ReadFile(filepath.Join(root(), fixture.Path))
	if err != nil {
		t.Fatal(err)
	}
	hash := sha256.Sum256(b)
	if len(b) != fixture.Size || hex.EncodeToString(hash[:]) != fixture.SHA256 {
		t.Fatal("original evidence hash mismatch:", fixture.Path)
	}
	blob := sha1.Sum(append([]byte(fmt.Sprintf("blob %d\x00", len(b))), b...))
	if hex.EncodeToString(blob[:]) != fixture.GitBlob {
		t.Fatal("original Git blob mismatch:", fixture.Path)
	}
	return b
}
func abc(t testing.TB) []byte { t.Helper(); return readFixture(t, fixtures(t)[0]) }
func parse(t testing.TB, b []byte) *wpm.Image {
	t.Helper()
	image, err := wpm.Parse(b, wpm.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	return image
}
func failure(t testing.TB, b []byte, limits wpm.Limits, code string) *wpm.Failure {
	t.Helper()
	before := bytes.Clone(b)
	image, err := wpm.Parse(b, limits)
	var f *wpm.Failure
	if image != nil || !errors.As(err, &f) || f.Code != code {
		t.Fatalf("want %s/nil image, got %v/%v", code, image, err)
	}
	if !bytes.Equal(before, b) {
		t.Fatal("refusal changed caller buffer")
	}
	if f.Error() == "" {
		t.Fatal("empty typed diagnostic")
	}
	return f
}

func TestAllOriginalExportsAndIsolation(t *testing.T) {
	unique := map[string]bool{}
	offsets := map[uint32]int{}
	for _, fixture := range fixtures(t) {
		t.Run(fixture.Path, func(t *testing.T) {
			raw := readFixture(t, fixture)
			original := bytes.Clone(raw)
			image := parse(t, raw)
			unique[fixture.SHA256] = true
			offsets[fixture.BodyOffset]++
			info := image.Inspect()
			if info.Header != (wpm.Header{BodyOffset: fixture.BodyOffset, Product: 1, FileType: 1, Major: 1, Minor: 1}) {
				t.Fatal(info.Header)
			}
			if info.Description != (wpm.Span{Offset: fixture.Description.Offset, Length: fixture.Description.Length}) {
				t.Fatal(info.Description)
			}
			if info.Body.Offset != fixture.BodyOffset || info.Body.Length != uint32(len(raw))-fixture.BodyOffset || info.Terminal != (wpm.Span{Offset: uint32(len(raw)) - 2, Length: 2}) || info.Suffix.Length != 0 {
				t.Fatal(info)
			}
			if len(info.Findings) != 0 || info.ReleaseEvidence != "unknown-from-bytes" {
				t.Fatal("source provenance is external, not inferred from tuple:", info)
			}
			words := image.BodyWords()
			if len(words) != len(fixture.BodyWords) {
				t.Fatal("word count")
			}
			for n, word := range words {
				v, err := strconv.ParseUint(fixture.BodyWords[n], 16, 16)
				if err != nil {
					t.Fatal(err)
				}
				if word.Value != uint16(v) || word.Span != (wpm.Span{Offset: fixture.BodyOffset + uint32(n)*2, Length: 2}) {
					t.Fatalf("word%d: %+v", n, word)
				}
			}
			if words[len(words)-1].Kind != wpm.Terminal {
				t.Fatal("terminal identity")
			}
			if !bytes.Equal(image.Export(), original) || image.SHA256() != sha256.Sum256(original) {
				t.Fatal("no-edit source changed")
			}
			description := image.Description()
			if !bytes.Equal(description, raw[info.Description.Offset:info.Description.Offset+info.Description.Length]) {
				t.Fatal("description bytes")
			}
			raw[0] = 0
			words[0].Value = 0
			description[0] ^= 1
			exported := image.Export()
			exported[0] = 0
			info.Header.BodyOffset = 1
			if !bytes.Equal(image.Export(), original) || image.BodyWords()[0].Value != 0xfc0c || image.Inspect().Header.BodyOffset != fixture.BodyOffset || image.Description()[0] != original[fixture.Description.Offset] {
				t.Fatal("mutable caller alias")
			}
		})
	}
	if len(unique) != 22 || !reflect.DeepEqual(offsets, map[uint32]int{70: 4, 75: 42}) {
		t.Fatal(unique, offsets)
	}
}

func TestSeparateDocumentCodec(t *testing.T) {
	macro := abc(t)
	_, err := wp51.Parse(macro)
	var f *wp51.Failure
	if !errors.As(err, &f) || f.Category != wp51.UnsupportedFileType {
		t.Fatal("DOC parser no longer refuses WPM:", err)
	}
	fixture := fixtures(t)[0]
	doc, err := os.ReadFile(filepath.Join(root(), filepath.Dir(fixture.Path), "MACROOUT.WP5"))
	if err != nil {
		t.Fatal(err)
	}
	if _, err = wp51.Parse(doc); err != nil {
		t.Fatal("original result is not an admitted DOC:", err)
	}
	failure(t, doc, wpm.DefaultLimits(), "UnsupportedFileType")
}

func TestTypedWordsOpaqueFindingsAndCopies(t *testing.T) {
	for _, tc := range []struct {
		value uint16
		kind  wpm.Kind
		code  string
	}{
		{0x0041, wpm.Literal, ""}, {0x007e, wpm.Literal, ""}, {0x8021, wpm.Key, ""}, {0xfc34, wpm.Macro, ""},
		{0xfcfd, wpm.Opaque, "UnqualifiedMacro"}, {0xfc3a, wpm.Opaque, "UnqualifiedMacro"}, {0x8020, wpm.Key, "UnqualifiedKey"},
		{0xfe41, wpm.Key, "UnqualifiedKey"}, {0xff09, wpm.Key, "UnqualifiedKey"}, {0x0124, wpm.Character, "UnqualifiedCharacter"},
		{0x000a, wpm.Control, "UnqualifiedControl"}, {0x9999, wpm.Opaque, "UnknownWord"},
	} {
		t.Run(fmt.Sprintf("%04X", tc.value), func(t *testing.T) {
			raw := abc(t)
			binary.LittleEndian.PutUint16(raw[70:72], tc.value)
			image := parse(t, raw)
			word := image.BodyWords()[0]
			if word.Value != tc.value || word.Kind != tc.kind {
				t.Fatal(word)
			}
			if tc.code == "" {
				if len(image.Inspect().Findings) != 0 {
					t.Fatal(image.Inspect())
				}
				return
			}
			info := image.Inspect()
			if len(info.Findings) != 1 || info.Findings[0] != (wpm.Finding{Code: tc.code, Span: wpm.Span{Offset: 70, Length: 2}, ExecutionBlocked: true}) {
				t.Fatal(info)
			}
			info.Findings[0].Code = "changed"
			info.Findings[0].ExecutionBlocked = false
			if image.Inspect().Findings[0].Code != tc.code || !image.Inspect().Findings[0].ExecutionBlocked || !bytes.Equal(image.Export(), raw) {
				t.Fatal("finding/source alias")
			}
		})
	}
}

func TestSuffixGapAndOpaquePrefixPreservation(t *testing.T) {
	raw := append(abc(t), 0x99)
	image := parse(t, raw)
	if image.Inspect().Suffix != (wpm.Span{Offset: 80, Length: 1}) || len(image.BodyWords()) != 5 || !bytes.Equal(image.Export(), raw) {
		t.Fatal(image.Inspect())
	}
	if image.Inspect().Findings[0].Code != "OpaqueSuffix" {
		t.Fatal(image.Inspect())
	}
	// A gap shifts the body to another odd offset; description stays a byte span.
	raw = abc(t)
	raw = append(append(append([]byte{}, raw[:70]...), 0x99), raw[70:]...)
	binary.LittleEndian.PutUint32(raw[4:8], 71)
	image = parse(t, raw)
	if image.BodyWords()[0].Span.Offset != 71 || image.Inspect().Findings[0].Code != "UnsupportedVariant" || !bytes.Equal(image.Export(), raw) {
		t.Fatal(image.Inspect())
	}
	// Describe the inserted gap as a bounded unknown packet; retain its index/data.
	binary.LittleEndian.PutUint16(raw[36:38], 0x7777)
	binary.LittleEndian.PutUint32(raw[38:42], 1)
	binary.LittleEndian.PutUint32(raw[42:46], 70)
	image = parse(t, raw)
	if len(image.Inspect().Findings) != 2 || image.Inspect().Findings[1].Code != "OpaquePrefixIndex" || !bytes.Equal(image.Export(), raw) {
		t.Fatal(image.Inspect())
	}
	// A zero-length unused slot has no pointed extent, even with an opaque tag.
	raw = abc(t)
	binary.LittleEndian.PutUint16(raw[46:48], 0x7777)
	image = parse(t, raw)
	if image.Inspect().Findings[0].Code != "OpaquePrefixIndex" {
		t.Fatal(image.Inspect())
	}
}

func TestMalformedAndUnsupportedBoundaries(t *testing.T) {
	base := abc(t)
	for n := 0; n < 56; n++ {
		t.Run(fmt.Sprintf("truncate%d", n), func(t *testing.T) { failure(t, base[:n], wpm.DefaultLimits(), "TruncatedInput") })
	}
	tests := []struct {
		name, code string
		mutate     func([]byte) []byte
	}{
		{"signature", "UnsupportedFormat", func(b []byte) []byte { b[0] = 0; return b }},
		{"product", "UnsupportedProduct", func(b []byte) []byte { b[8] = 8; return b }},
		{"type", "UnsupportedFileType", func(b []byte) []byte { b[9] = 10; return b }},
		{"major", "UnsupportedVersion", func(b []byte) []byte { b[10] = 0; return b }},
		{"minor", "UnsupportedVersion", func(b []byte) []byte { b[11] = 0; return b }},
		{"key", "UnsupportedEncryption", func(b []byte) []byte { b[12] = 1; return b }},
		{"reserved", "UnsupportedVariant", func(b []byte) []byte { b[14] = 1; return b }},
		{"indexType", "MalformedPrefix", func(b []byte) []byte { b[16] = 0; return b }},
		{"zeroCount", "MalformedPrefix", func(b []byte) []byte { b[18] = 0; return b }},
		{"sizeDisagrees", "MalformedPrefix", func(b []byte) []byte { b[20] = 39; return b }},
		{"otherConsistentCount", "UnsupportedVariant", func(b []byte) []byte { b[18] = 5; b[20] = 50; return b }},
		{"bodyBeforePrefix", "MalformedPrefix", func(b []byte) []byte { binary.LittleEndian.PutUint32(b[4:8], 55); return b }},
		{"bodyPastEOF", "MalformedPrefix", func(b []byte) []byte { binary.LittleEndian.PutUint32(b[4:8], ^uint32(0)); return b }},
		{"cycleNotFollowed", "UnsupportedVariant", func(b []byte) []byte { binary.LittleEndian.PutUint32(b[22:26], 16); return b }},
		{"nextInBody", "MalformedPrefix", func(b []byte) []byte { binary.LittleEndian.PutUint32(b[22:26], 70); return b }},
		{"descType", "UnsupportedVariant", func(b []byte) []byte { b[26] = 2; return b }},
		{"descInHeader", "MalformedPrefix", func(b []byte) []byte { binary.LittleEndian.PutUint32(b[32:36], 16); return b }},
		{"descPastBody", "MalformedPrefix", func(b []byte) []byte { binary.LittleEndian.PutUint32(b[28:32], ^uint32(0)); return b }},
		{"emptyEditorDescription", "UnsupportedVariant", func(b []byte) []byte { binary.LittleEndian.PutUint32(b[28:32], 0); return b }},
		{"descMissingZero", "MalformedPrefix", func(b []byte) []byte { b[69] = 1; return b }},
		{"opaqueOverflow", "MalformedPrefix", func(b []byte) []byte { b[36] = 1; binary.LittleEndian.PutUint32(b[38:42], ^uint32(0)); return b }},
		{"opaqueAlias", "UnsupportedStructure", func(b []byte) []byte {
			b[36] = 1
			binary.LittleEndian.PutUint32(b[38:42], 1)
			binary.LittleEndian.PutUint32(b[42:46], 56)
			return b
		}},
		{"missingTerminal", "MalformedBody", func(b []byte) []byte { return b[:len(b)-2] }},
		{"oddBody", "MalformedBody", func(b []byte) []byte { return b[:len(b)-1] }},
	}
	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) { failure(t, tc.mutate(bytes.Clone(base)), wpm.DefaultLimits(), tc.code) })
	}
	if f := failure(t, base[:len(base)-1], wpm.DefaultLimits(), "MalformedBody"); f.Field != "OddWord" {
		t.Fatal(f)
	}
	if f := failure(t, base[:len(base)-2], wpm.DefaultLimits(), "MalformedBody"); f.Field != "MissingTerminator" {
		t.Fatal(f)
	}
}

func TestLimitsAndLargeInputs(t *testing.T) {
	base := abc(t)
	limits := wpm.DefaultLimits()
	for _, l := range []wpm.Limits{{}, {InputBytes: limits.InputBytes, DescriptionBytes: limits.DescriptionBytes}, {InputBytes: limits.InputBytes + 1, DescriptionBytes: 1, Words: 1}, {InputBytes: 1, DescriptionBytes: limits.DescriptionBytes + 1, Words: 1}, {InputBytes: 1, DescriptionBytes: 1, Words: limits.Words + 1}} {
		failure(t, base, l, "InvalidLimit")
	}
	l := limits
	l.InputBytes = uint32(len(base) - 1)
	failure(t, base, l, "InputLimit")
	l = limits
	l.DescriptionBytes = 13
	failure(t, base, l, "TraversalLimit")
	l = limits
	l.Words = 4
	failure(t, base, l, "TraversalLimit")
	failure(t, make([]byte, wpm.MaxInputBytes+1), limits, "InputLimit")
	large := append(bytes.Clone(base[:70]), make([]byte, 2*wpm.MaxWords)...)
	for n := 70; n < len(large)-2; n += 2 {
		large[n] = 0x41
	}
	image := parse(t, large)
	if image.Inspect().Body.Length != 2*wpm.MaxWords {
		t.Fatal(image.Inspect())
	}
	tooMany := append(bytes.Clone(large[:len(large)-2]), 0x41, 0, 0, 0)
	failure(t, tooMany, limits, "TraversalLimit")
	maxInput := make([]byte, wpm.MaxInputBytes)
	copy(maxInput, base[:70])
	binary.LittleEndian.PutUint32(maxInput[4:8], wpm.MaxInputBytes-2)
	image = parse(t, maxInput)
	if image.Inspect().Header.BodyOffset != wpm.MaxInputBytes-2 || image.Inspect().Suffix.Length != 0 || len(image.BodyWords()) != 1 {
		t.Fatal(image.Inspect())
	}
}

func TestOriginalNestedOperandWordsAreNotRewritten(t *testing.T) {
	for _, fixture := range fixtures(t) {
		if fixture.Case != "CMD51-215" && fixture.Case != "CMD51-227" {
			continue
		}
		image := parse(t, readFixture(t, fixture))
		words := image.BodyWords()
		var serial strings.Builder
		for _, word := range words {
			fmt.Fprintf(&serial, "%04X ", word.Value)
		}
		want := "FC34 004E 007E 003C 0033 007E"
		if fixture.Case == "CMD51-227" {
			want = "FC34 0042 007E 002B 0034 007E"
		}
		if !strings.Contains(serial.String(), want) {
			t.Fatal("inner/outer delimiter identities changed:", serial.String())
		}
	}
}

func TestConcurrentReadOnlyImage(t *testing.T) {
	raw := abc(t)
	image := parse(t, raw)
	var wg sync.WaitGroup
	for n := 0; n < 8; n++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for k := 0; k < 50; k++ {
				out := image.Export()
				out[0] = 0
				words := image.BodyWords()
				words[0].Value = 0
				description := image.Description()
				description[0] = 0
				if image.SHA256() != sha256.Sum256(raw) {
					t.Error("image changed")
				}
			}
		}()
	}
	wg.Wait()
}

func FuzzImage(f *testing.F) {
	seen := map[string]bool{}
	for _, fixture := range fixtures(f) {
		if !seen[fixture.SHA256] {
			f.Add(readFixture(f, fixture))
			seen[fixture.SHA256] = true
		}
	}
	base := abc(f)
	for n := 0; n < 56; n++ {
		f.Add(bytes.Clone(base[:n]))
	}
	f.Add(append(bytes.Clone(base), 0xff))
	f.Fuzz(func(t *testing.T, raw []byte) {
		before := bytes.Clone(raw)
		image, err := wpm.Parse(raw, wpm.DefaultLimits())
		if !bytes.Equal(before, raw) {
			t.Fatal("Parse mutates input")
		}
		if err != nil {
			var failure *wpm.Failure
			if image != nil || !errors.As(err, &failure) {
				t.Fatal("untyped refusal", image, err)
			}
			return
		}
		if !bytes.Equal(image.Export(), raw) || image.SHA256() != sha256.Sum256(raw) {
			t.Fatal("accepted bytes changed")
		}
		info := image.Inspect()
		words := image.BodyWords()
		if len(words) == 0 || words[len(words)-1].Value != 0 || words[len(words)-1].Kind != wpm.Terminal {
			t.Fatal("terminal")
		}
		if info.Body.Length != uint32(len(words))*2 || info.Body.Offset+info.Body.Length != info.Suffix.Offset || info.Suffix.Length != uint32(len(raw))-info.Suffix.Offset {
			t.Fatal("body/suffix boundary")
		}
		for n, w := range words {
			if w.Span != (wpm.Span{Offset: info.Body.Offset + uint32(n)*2, Length: 2}) || w.Value != binary.LittleEndian.Uint16(raw[w.Span.Offset:w.Span.Offset+2]) {
				t.Fatal("word/span")
			}
		}
		exported := image.Export()
		exported[0] ^= 1
		if !bytes.Equal(image.Export(), raw) {
			t.Fatal("export alias")
		}
	})
}

func BenchmarkParseOriginal(b *testing.B) {
	raw := abc(b)
	b.ReportAllocs()
	b.SetBytes(int64(len(raw)))
	b.ResetTimer()
	for n := 0; n < b.N; n++ {
		if _, err := wpm.Parse(raw, wpm.DefaultLimits()); err != nil {
			b.Fatal(err)
		}
	}
}
func BenchmarkWordsAtBudget(b *testing.B) {
	raw := abc(b)
	raw = append(bytes.Clone(raw[:70]), make([]byte, 2*wpm.MaxWords)...)
	for n := 70; n < len(raw)-2; n += 2 {
		raw[n] = 0x41
	}
	image := parse(b, raw)
	b.ReportAllocs()
	b.SetBytes(int64(len(raw)))
	b.ResetTimer()
	for n := 0; n < b.N; n++ {
		if len(image.BodyWords()) != wpm.MaxWords {
			b.Fatal("count")
		}
	}
}
