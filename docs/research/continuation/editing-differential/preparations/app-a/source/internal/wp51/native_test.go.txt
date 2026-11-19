package wp51_test

import (
	"bytes"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/wp51"
)

const root = "../.."
const catalogue = root + "/kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json"

type fixture struct {
	ID, Path, SHA256 string
	Size             int    `json:"size_bytes"`
	BodyOffset       int    `json:"body_offset"`
	BodySHA          string `json:"body_sha256"`
	Run              string `json:"run_manifest"`
	Scenario         string `json:"scenario_id"`
	Packets          []struct {
		Type           uint16
		Offset, Length int
		SHA256         string
	}
	Indexes []struct{ Offset, Count, Size, Next int }
}
type recipe struct {
	ID     string
	Seed   string `json:"seed_id"`
	Append string `json:"append_hex"`
	SHA256 string
	Size   int `json:"size_bytes"`
}

func corpus(t testing.TB) ([]fixture, []recipe) {
	t.Helper()
	b, err := os.ReadFile(catalogue)
	if err != nil {
		t.Fatal(err)
	}
	var c struct {
		Fixtures []fixture
		Recipes  []recipe `json:"supplemental_recipes"`
	}
	if err = json.Unmarshal(b, &c); err != nil {
		t.Fatal(err)
	}
	if len(c.Fixtures) != 6 || len(c.Recipes) != 2 {
		t.Fatal("catalogue unexpectedly changed")
	}
	return c.Fixtures, c.Recipes
}
func readFixture(t testing.TB, f fixture) []byte {
	t.Helper()
	b, e := os.ReadFile(filepath.Join(root, f.Path))
	if e != nil {
		t.Fatal(e)
	}
	return b
}
func hash(b []byte) string { s := sha256.Sum256(b); return hex.EncodeToString(s[:]) }
func checkError(t testing.TB, b []byte, want wp51.Category) {
	t.Helper()
	before := bytes.Clone(b)
	image, err := wp51.Parse(b)
	var failure *wp51.Failure
	if image != nil || !errors.As(err, &failure) || failure.Category != want || failure.Offset < 0 || failure.Field == "" {
		t.Fatalf("want %s refusal; image=%v err=%v", want, image, err)
	}
	if !bytes.Equal(before, b) {
		t.Fatal("refusal mutated caller")
	}
}
func TestOriginalFixtureIdentity(t *testing.T) {
	fixtures, recipes := corpus(t)
	seeds := map[string][]byte{}
	for _, f := range fixtures {
		t.Run(f.ID, func(t *testing.T) {
			b := readFixture(t, f)
			seeds[f.ID] = b
			if len(b) != f.Size || hash(b) != f.SHA256 {
				t.Fatal("original hash/size differs from WP01")
			}
			run, err := os.ReadFile(filepath.Join(root, f.Run))
			if err != nil {
				t.Fatal(err)
			}
			var r struct {
				Results []struct {
					ID       string `json:"case_id"`
					Evidence []struct {
						Path, SHA256 string
						Size         int
					}
				}
			}
			if err = json.Unmarshal(run, &r); err != nil {
				t.Fatal(err)
			}
			proven := false
			for _, c := range r.Results {
				for _, e := range c.Evidence {
					if c.ID == f.Scenario && e.Path == f.Path && e.SHA256 == f.SHA256 && e.Size == len(b) {
						proven = true
					}
				}
			}
			if !proven {
				t.Fatal("fixture not pinned by original run")
			}
			if f.ID == "macro" {
				checkError(t, b, wp51.UnsupportedFileType)
				return
			}
			image, err := wp51.Parse(b)
			if err != nil {
				t.Fatal(err)
			}
			out := image.Export()
			if len(out) != f.Size || !bytes.Equal(b, out) || hash(out) != f.SHA256 {
				t.Fatal("no-edit export changed original")
			}
			info := image.Inspect()
			if info.Validation != wp51.OuterFramedPayloadUnvalidated || info.Body.Offset != f.BodyOffset || hash(out[info.Body.Offset:]) != f.BodySHA {
				t.Fatal("body/support mismatch")
			}
			if len(info.Packets) != len(f.Packets) || len(info.Blocks) != len(f.Indexes) {
				t.Fatal("index enumeration mismatch")
			}
			for i, p := range info.Packets {
				expected := f.Packets[i]
				data, ok := image.Bytes(p.Data)
				if !ok || p.Type != expected.Type || p.Data.Offset != expected.Offset || p.Data.Length != expected.Length || hash(data) != expected.SHA256 {
					t.Fatalf("packet %d changed", i)
				}
			}
			for i, b := range info.Blocks {
				expected := f.Indexes[i]
				if b.Data.Offset != expected.Offset || b.Data.Length != expected.Size || b.Count != expected.Count || b.Next != uint32(expected.Next) {
					t.Fatal("block mismatch")
				}
			}
			b[0] = 0
			out[0] = 0
			info.Packets[0].Data.Offset = 0
			info.Blocks[0].Data.Offset = 0
			data, _ := image.Bytes(image.Inspect().Packets[0].Data)
			data[0] ^= 0xff
			if hash(image.Export()) != f.SHA256 || image.Inspect().Packets[0].Data.Offset != f.Packets[0].Offset || image.Inspect().Blocks[0].Data.Offset != 16 {
				t.Fatal("caller mutated owned state")
			}
			if _, ok := image.Bytes(wp51.Span{Offset: -1, Length: 2}); ok {
				t.Fatal("negative span accepted")
			}
			if _, ok := image.Bytes(wp51.Span{Offset: len(out), Length: 1}); ok {
				t.Fatal("outside span accepted")
			}
		})
	}
	// Re-read pristine inputs: the isolation test deliberately changed caller buffers.
	for _, f := range fixtures {
		seeds[f.ID] = readFixture(t, f)
	}
	for _, r := range recipes {
		t.Run(r.ID, func(t *testing.T) {
			suffix, err := hex.DecodeString(r.Append)
			if err != nil {
				t.Fatal(err)
			}
			b := append(bytes.Clone(seeds[r.Seed]), suffix...)
			if hash(b) != r.SHA256 || len(b) != r.Size {
				t.Fatal("recipe mismatch")
			}
			if r.ID == "unframed-tail" {
				checkError(t, b, wp51.MalformedBody)
				return
			}
			image, err := wp51.Parse(b)
			if err != nil {
				t.Fatal(err)
			}
			if !bytes.Equal(b, image.Export()) {
				t.Fatal("suffix dropped")
			}
		})
	}
}
func put16(b []byte, o int, n uint16) { binary.LittleEndian.PutUint16(b[o:], n) }
func put32(b []byte, o int, n uint32) { binary.LittleEndian.PutUint32(b[o:], n) }
func simple(body []byte) []byte {
	b := make([]byte, 66+len(body))
	copy(b, []byte{255, 'W', 'P', 'C'})
	put32(b, 4, 66)
	copy(b[8:], []byte{1, 10, 0, 1})
	put16(b, 16, 0xfffb)
	put16(b, 18, 5)
	put16(b, 20, 50)
	copy(b[66:], body)
	return b
}
func TestFailures(t *testing.T) {
	tests := []struct {
		name     string
		category wp51.Category
		mutate   func([]byte) []byte
	}{
		{"short", wp51.TruncatedInput, func(b []byte) []byte { return b[:15] }},
		{"signature", wp51.UnsupportedFormat, func(b []byte) []byte { b[0] = 0; return b }},
		{"product", wp51.UnsupportedProduct, func(b []byte) []byte { b[8] = 2; return b }},
		{"companion", wp51.UnsupportedFileType, func(b []byte) []byte { b[9] = 1; return b }},
		{"major", wp51.UnsupportedVersion, func(b []byte) []byte { b[10] = 1; return b }},
		{"minor", wp51.UnsupportedVersion, func(b []byte) []byte { b[11] = 0; return b }},
		{"encrypted", wp51.UnsupportedEncryption, func(b []byte) []byte { b[12] = 1; b[66] = 0; return b }},
		{"reserved", wp51.UnsupportedVariant, func(b []byte) []byte { b[14] = 1; return b }},
		{"body-before-prefix", wp51.MalformedPrefix, func(b []byte) []byte { put32(b, 4, 15); return b }},
		{"body-past-eof", wp51.MalformedPrefix, func(b []byte) []byte { put32(b, 4, 0xffffffff); return b }},
		{"partial-header", wp51.MalformedPrefix, func(b []byte) []byte { put32(b, 4, 20); return b }},
		{"partial-block", wp51.MalformedPrefix, func(b []byte) []byte { put32(b, 4, 60); return b }},
		{"block-type", wp51.MalformedPrefix, func(b []byte) []byte { put16(b, 16, 1); return b }},
		{"zero-count", wp51.MalformedPrefix, func(b []byte) []byte { put16(b, 18, 0); return b }},
		{"block-size", wp51.MalformedPrefix, func(b []byte) []byte { put16(b, 20, 49); return b }},
		{"consistent-variant", wp51.UnsupportedVariant, func(b []byte) []byte { put16(b, 18, 4); put16(b, 20, 40); return b }},
		{"special-entry", wp51.UnsupportedStructure, func(b []byte) []byte { put16(b, 26, 0xfffb); return b }},
		{"packet-header", wp51.MalformedPrefix, func(b []byte) []byte { put16(b, 26, 9); put32(b, 32, 15); return b }},
		{"packet-body", wp51.MalformedPrefix, func(b []byte) []byte { put16(b, 26, 9); put32(b, 32, 67); return b }},
		{"packet-overflow", wp51.MalformedPrefix, func(b []byte) []byte { put16(b, 26, 9); put32(b, 28, 0xffffffff); put32(b, 32, 66); return b }},
		{"packet-index-overlap", wp51.UnsupportedStructure, func(b []byte) []byte { put16(b, 26, 9); put32(b, 28, 1); put32(b, 32, 26); return b }},
		{"nul", wp51.MalformedBody, func(b []byte) []byte { b[66] = 0; return b }},
		{"delete", wp51.MalformedBody, func(b []byte) []byte { b[66] = 0x7f; return b }},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) { checkError(t, tt.mutate(simple([]byte("text"))), tt.category) })
	}
}
func TestEverySeedTruncation(t *testing.T) {
	fixtures, recipes := corpus(t)
	type seedCase struct {
		id         string
		data       []byte
		bodyOffset int
		macro      bool
	}
	seeds := make([]seedCase, 0, len(fixtures)+len(recipes))
	byID := map[string]seedCase{}
	for _, f := range fixtures {
		seed := seedCase{f.ID, readFixture(t, f), f.BodyOffset, f.ID == "macro"}
		seeds = append(seeds, seed)
		byID[f.ID] = seed
	}
	for _, r := range recipes {
		suffix, err := hex.DecodeString(r.Append)
		if err != nil {
			t.Fatal(err)
		}
		seed := byID[r.Seed]
		seed.id = r.ID
		seed.data = append(bytes.Clone(seed.data), suffix...)
		seeds = append(seeds, seed)
	}
	for _, seed := range seeds {
		t.Run(seed.id, func(t *testing.T) {
			for n := 0; n < len(seed.data); n++ {
				b := bytes.Clone(seed.data[:n])
				image, err := wp51.Parse(b)
				if err == nil {
					if seed.macro || n < seed.bodyOffset || !bytes.Equal(b, image.Export()) {
						t.Fatalf("bad truncation acceptance at %d", n)
					}
				} else {
					var e *wp51.Failure
					if image != nil || !errors.As(err, &e) {
						t.Fatalf("untyped truncation %d: %v", n, err)
					}
				}
				if !bytes.Equal(b, seed.data[:n]) {
					t.Fatal("mutation")
				}
			}
		})
	}
}
