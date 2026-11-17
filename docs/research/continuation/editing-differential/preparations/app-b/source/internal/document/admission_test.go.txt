package document_test

import (
	"bytes"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
)

func TestEveryQualifiedPrefixByteAndLiteralVariants(t *testing.T) {
	original := fixture(t)
	for offset := 16; offset < 324; offset++ {
		input := bytes.Clone(original)
		input[offset] ^= 1
		d, e := document.Parse(input)
		if e != nil {
			continue
		} // Native framing retains its own stricter typed refusals.
		if d.CheckMutation() == nil {
			t.Fatalf("unqualified field byte %d admitted", offset)
		}
		exact(t, d, input)
		c, _ := d.CursorAt(0)
		r, e := d.InsertASCII(c, []byte("X"))
		if e == nil || r.Document != d || r.Cursor != c || r.Changed {
			t.Fatal("prefix refusal mutated", offset)
		}
	}
	for _, flags := range []byte{0, 8} {
		for _, hash := range [][]byte{{0xe7, 0x24}, {0x11, 0x72}} {
			input := bytes.Clone(original)
			input[256] = flags
			copy(input[101:103], hash)
			d, e := document.Parse(input)
			if e != nil || d.CheckMutation() != nil {
				t.Fatal("qualified literal variant", e)
			}
			c, _ := d.CursorAt(2)
			r, e := d.InsertASCII(c, []byte("X"))
			if e != nil {
				t.Fatal(e)
			}
			out, _ := r.Document.Export()
			want := append(append(bytes.Clone(input[:328]), 'X'), input[328:]...)
			want[256] |= 8
			if !bytes.Equal(out, want) {
				t.Fatal("cache/counter/prefix changed")
			}
		}
	}
}

// Labelled synthetic ownership test: same qualified fields physically relocated,
// not an original layout observation and not an input template for the writer.
func TestIndexedFlagLocationAndInputPrefixOwnership(t *testing.T) {
	input := fixture(t)
	before := bytes.Clone(input)
	copy(input[166:182], before[256:272])
	copy(input[182:272], before[166:256])
	binary.LittleEndian.PutUint32(input[52:56], 182) // packet12 index offset
	binary.LittleEndian.PutUint32(input[62:66], 166) // packet6 index offset
	d, e := document.Parse(input)
	if e != nil || d.CheckMutation() != nil {
		t.Fatal(e, d.CheckMutation())
	}
	c, _ := d.CursorAt(4)
	r, e := d.InsertASCII(c, []byte("X"))
	if e != nil {
		t.Fatal(e)
	}
	out, _ := r.Document.Export()
	want := append(append(bytes.Clone(input[:330]), 'X'), input[330:]...)
	want[166] |= 8
	if !bytes.Equal(out, want) || out[256] != input[256] {
		t.Fatal("hardcoded flags/template substituted")
	}
	exact(t, d, input)
}

func TestMutationBoundariesAndIdenticalTypeover(t *testing.T) {
	raw := synthetic(t, bytes.Repeat([]byte{'A'}, document.MaxMutationTokens))
	d, _ := document.Parse(raw)
	c, _ := d.CursorAt(0)
	if d.CheckMutation() != nil {
		t.Fatal("exact mutation token ceiling")
	}
	r, e := d.TypeoverASCII(c, []byte("A"))
	if e != nil || r.Document != d || r.Changed || r.Cursor.Gap() != 1 {
		t.Fatal("identical typeover invented dirty metadata", r, e)
	}
	r, e = d.InsertASCII(c, []byte("X"))
	category(t, e, document.MutationLimit)
	if r.Document != d || r.Cursor != c {
		t.Fatal("limit partial mutation")
	}
	r, e = d.TypeoverASCII(c, []byte("X"))
	if e != nil || r.Document.TokenCount() != document.MaxMutationTokens {
		t.Fatal("bounded replacement", e)
	}
	tooMany, _ := document.Parse(synthetic(t, bytes.Repeat([]byte{'x'}, document.MaxMutationTokens+1)))
	category(t, tooMany.CheckMutation(), document.MutationLimit)
	exact(t, d, raw)
	var zero document.Document
	var cursor document.Cursor
	_, e = zero.InsertASCII(cursor, []byte("X"))
	category(t, e, document.InvalidDocument)
	_, e = zero.OriginalExport()
	category(t, e, document.InvalidDocument)
	if zero.Revision() != cursor.Revision() {
		t.Fatal("zero revision")
	}
	other, _ := document.Parse(raw)
	otherCursor, _ := other.CursorAt(0)
	_, e = d.TypeoverASCII(otherCursor, []byte("X"))
	category(t, e, document.RevisionMismatch)
}

func TestOriginalNativeAdmissionCorpus(t *testing.T) {
	// All inclusive WP23 paths, including pilots/diagnostics. These are not
	// independent original documents; strict admission and read-only are separate.
	base := "../../docs/research/continuation/native-edits"
	count, admitted, refused := 0, 0, 0
	e := filepath.WalkDir(base, func(path string, entry os.DirEntry, e error) error {
		if e != nil {
			return e
		}
		if entry.IsDir() || filepath.Ext(path) != ".WP5" {
			return nil
		}
		raw, e := os.ReadFile(path)
		if e != nil {
			return e
		}
		d, e := document.Parse(raw)
		if e != nil {
			t.Fatal(path, e)
		}
		exact(t, d, raw)
		count++
		if d.CheckMutation() == nil {
			admitted++
		} else {
			refused++
		}
		return nil
	})
	if e != nil {
		t.Fatal(e)
	}
	if count != 666 || admitted != 303 || refused != 363 {
		t.Fatalf("classification %d admitted%d refused%d", count, admitted, refused)
	}
}

func TestExactOriginalCommandOutputs(t *testing.T) {
	// No guessed body outputs: source/final bytes are actual reviewed WP23 runs.
	type observedCase struct {
		ID     string `json:"id"`
		Source string `json:"source"`
		Final  string `json:"final"`
		Gap    int    `json:"gap"`
		View   string `json:"view"`
		Mode   string `json:"mode"`
	}
	for _, repeat := range []string{"r1", "r2"} {
		dir := "../../docs/research/continuation/native-edits/runs/wp23-a-boundaries-" + repeat
		raw, e := os.ReadFile(dir + "/run.json")
		if e != nil {
			t.Fatal(e)
		}
		var run struct {
			Cases []observedCase `json:"cases"`
		}
		if e = json.Unmarshal(raw, &run); e != nil {
			t.Fatal(e)
		}
		if len(run.Cases) != 16 {
			t.Fatal("boundary branch count")
		}
		for _, c := range run.Cases {
			input, e := os.ReadFile(dir + "/" + c.Source)
			if e != nil {
				t.Fatal(e)
			}
			want, e := os.ReadFile(dir + "/" + c.Final)
			if e != nil {
				t.Fatal(e)
			}
			d, e := document.Parse(input)
			if e != nil {
				t.Fatal(e)
			}
			cursor, _ := d.CursorAt(c.Gap)
			cursor = cursor.WithReveal(c.View == "reveal")
			var r document.EditResult
			if c.Mode == "typeover" {
				r, e = d.TypeoverASCII(cursor, []byte("X"))
			} else {
				r, e = d.InsertASCII(cursor, []byte("X"))
			}
			if e != nil {
				t.Fatal(c.ID, e)
			}
			// Original after-Off typeover saves flag0 in these two witnesses.
			// WP23 permits the writer's body-change flag8 policy; compare this
			// one explicitly allowed difference without changing raw evidence.
			candidate, _ := r.Document.Export()
			for i, b := range candidate {
				if i == 256 {
					if b != want[i]|8 {
						t.Fatal(c.ID, "must-format policy")
					}
					continue
				}
				if b != want[i] {
					t.Fatal(c.ID, "unexplained native difference", i)
				}
			}
			if len(candidate) != len(want) {
				t.Fatal(c.ID, "length")
			}
			if r.Cursor.Gap() != c.Gap+1 {
				t.Fatal(c.ID, "post-command gap")
			}
			token, _ := r.Document.Token(c.Gap)
			if token.Kind != document.ASCII || hex.EncodeToString(token.Raw) != "58" {
				t.Fatal(c.ID, "inserted token identity")
			}
			native, e := wp51.Parse(want)
			if e != nil || !bytes.Equal(native.Export(), want) {
				t.Fatal(e)
			}
		}
	}
}
