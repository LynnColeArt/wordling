package document_test

import (
	"bytes"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
)

type reorderedManifest struct {
	Images    []struct{ Path, SHA256 string } `json:"original_image_pins"`
	Predicate struct {
		Fields []struct {
			Owner, Name, Representation string
			Offset                      int `json:"relative_offset"`
			Width                       int
			Hex                         string `json:"raw_hex"`
		} `json:"field_rules"`
	} `json:"reordered_source_predicate_R1"`
}

func reorderedSource(t *testing.T, grammar, stage string) []byte {
	t.Helper()
	b, e := os.ReadFile("../../docs/research/continuation/resaved-prefix/runs/w42-" + grammar + "-disabled/r1/" + stage + ".WP5")
	if e != nil {
		t.Fatal(e)
	}
	return b
}
func reorderedInfo(t *testing.T, raw []byte) wp51.Inspection {
	t.Helper()
	d, e := wp51.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	return d.Inspect()
}

func TestReorderedEveryOriginalFieldAndStage(t *testing.T) {
	b, e := os.ReadFile("../../docs/research/continuation/reordered-prefix-design/manifest.json")
	if e != nil {
		t.Fatal(e)
	}
	var m reorderedManifest
	if e = json.Unmarshal(b, &m); e != nil {
		t.Fatal(e)
	}
	if len(m.Predicate.Fields) != 72 || len(m.Images) != 72 {
		t.Fatal("field/image roster")
	}
	positive, negative := 0, 0
	for _, im := range m.Images {
		raw, e := os.ReadFile(filepath.Join("../..", im.Path))
		if e != nil {
			t.Fatal(e)
		}
		sum := sha256.Sum256(raw)
		if hex.EncodeToString(sum[:]) != im.SHA256 {
			t.Fatal("source seal", im.Path)
		}
		d, e := document.Parse(raw)
		if e != nil {
			t.Fatal(e)
		}
		exact(t, d, raw)
		expected := strings.Contains(im.Path, "-disabled/") && (strings.HasSuffix(im.Path, "W42G1.WP5") || strings.HasSuffix(im.Path, "W42G2.WP5") || strings.HasSuffix(im.Path, "W42G3.WP5") || strings.HasSuffix(im.Path, "W42EDIT.WP5"))
		if !expected {
			if strings.HasSuffix(im.Path, "W42FIN.WP5") || reorderedInfo(t, raw).Body.Offset == 564 {
				if d.CheckMutation() == nil {
					t.Fatal("FIN/564 admitted", im.Path)
				}
				negative++
			}
			continue
		}
		positive++
		if e = d.CheckMutation(); e != nil {
			t.Fatal(im.Path, e)
		}
		info := reorderedInfo(t, raw)

		// Owner keys in the reviewed72-field ledger are header and decimal packet IDs.
		for _, f := range m.Predicate.Fields {
			off := 0
			if f.Owner != "header" {
				found := false
				for _, p := range info.Packets {
					if f.Owner == packetOwner(p.Type) {
						off = p.Data.Offset
						found = true
						break
					}
				}
				if !found {
					t.Fatal("field owner", f.Owner)
				}
			}
			want, e := hex.DecodeString(f.Hex)
			if e != nil || len(want) != f.Width || !bytes.Equal(raw[off+f.Offset:off+f.Offset+f.Width], want) {
				t.Fatal(im.Path, f.Name, "field value/width")
			}
		}
		for _, gap := range []int{0, d.TokenCount() / 2, d.TokenCount()} {
			c, _ := d.CursorAt(gap)
			r, e := d.InsertASCII(c, []byte("q"))
			if e != nil {
				t.Fatal(e)
			}
			out, _ := r.Document.Export()
			if r.Document.CheckMutation() != nil || r.Cursor.Gap() != gap+1 || bytes.Equal(raw, out) {
				t.Fatal("real insertion")
			}
			orig, _ := r.Document.OriginalExport()
			if !bytes.Equal(orig, raw) {
				t.Fatal("lineage")
			}
		}
	}
	if positive != 24 || negative == 0 {
		t.Fatal(positive, negative)
	}
}
func packetOwner(n uint16) string {
	switch n {
	case 6:
		return "packet-6"
	case 7:
		return "packet-7"
	case 8:
		return "packet-8"
	case 12:
		return "packet-12"
	case 15:
		return "packet-15"
	}
	return "unknown"
}

func TestReorderedPrefixMutantsAreAtomic(t *testing.T) {
	raw := reorderedSource(t, "one-bold", "W42G3")
	info := reorderedInfo(t, raw)
	for offset := 0; offset < info.Body.Offset; offset++ {
		t.Run(string(rune(offset)), func(t *testing.T) {
			bad := bytes.Clone(raw)
			bad[offset] ^= 1
			d, e := document.Parse(bad)
			if e != nil {
				return
			}
			if d.CheckMutation() == nil {
				t.Fatalf("byte%d admitted", offset)
			}
			exact(t, d, bad)
			c, _ := d.CursorAt(1)
			r, e := d.InsertASCII(c, []byte("X"))
			if e == nil || r.Document != d || r.Cursor != c || r.Changed {
				t.Fatal("partial refusal")
			}
		})
	}
	var cache, flags, counter int
	for _, p := range info.Packets {
		if p.Type == 15 {
			cache = p.Data.Offset + 21
		}
		if p.Type == 6 {
			flags = p.Data.Offset
			counter = flags + 8
		}
	}
	for _, v := range []struct {
		cache          []byte
		counter, flags byte
	}{{[]byte{0x11, 0x72}, 1, 0}, {[]byte{0x11, 0x72}, 1, 8}, {[]byte{0xe7, 0x24}, 2, 0}, {[]byte{0xe7, 0x24}, 2, 8}, {[]byte{0x11, 0x72}, 2, 0}, {[]byte{0xe7, 0x24}, 1, 9}} {
		bad := bytes.Clone(raw)
		copy(bad[cache:cache+2], v.cache)
		bad[counter] = v.counter
		bad[flags] = v.flags
		d, e := document.Parse(bad)
		if e != nil {
			t.Fatal(e)
		}
		if d.CheckMutation() == nil {
			t.Fatal("new-order Cartesian expansion")
		}
		exact(t, d, bad)
	}
}

func FuzzReorderedPublicEdits(f *testing.F) {
	raw, e := os.ReadFile("../../docs/research/continuation/resaved-prefix/runs/w42-two-bold-disabled/r1/W42G3.WP5")
	if e != nil {
		f.Fatal(e)
	}
	f.Add(uint8(0), uint8(0), []byte("X")) // exact real new prefix reaches successful publication
	f.Add(uint8(1), uint8(2), []byte("Y")) // unmodified input, another gap
	for _, b := range []byte{0, 1, 2, 8, 255} {
		f.Add(uint8(4), b, []byte("X"))
	}
	f.Fuzz(func(t *testing.T, selector, value byte, text []byte) {
		if len(text) > 64 {
			return
		}
		input := bytes.Clone(raw)
		if selector%2 == 0 {
			input[16+int(value)%308] ^= selector / 2
		} // labelled malformed/success reachability, never source generation
		d, e := document.Parse(input)
		if e != nil {
			return
		}
		before, _ := d.Export()
		c, _ := d.CursorAt(int(value) % (d.TokenCount() + 1))
		r, e := d.InsertASCII(c, text)
		exact(t, d, before)
		if e != nil {
			if r.Document != d || r.Cursor != c || r.Changed {
				t.Fatal("refusal publication")
			}
			return
		}
		if r.Document.CheckMutation() != nil {
			t.Fatal("unqualified publication")
		}
		original, _ := r.Document.OriginalExport()
		if !bytes.Equal(original, before) {
			t.Fatal("source lost")
		}
	})
}

func TestReorderedIndexedRelocationNoopAndIsolation(t *testing.T) {
	raw := reorderedSource(t, "one-bold", "W42G3")
	info := reorderedInfo(t, raw)
	// Synthetic relocation exchanges whole packet6 and packet7 payloads and changes
	// their index locations. This is no original observation or production writer.
	var a, b wp51.Packet
	for _, p := range info.Packets {
		if p.Type == 6 {
			a = p
		}
		if p.Type == 7 {
			b = p
		}
	}
	moved := bytes.Clone(raw)
	copy(moved[a.Data.Offset:a.Data.Offset+b.Data.Length], raw[b.Data.Offset:b.Data.Offset+b.Data.Length])
	copy(moved[a.Data.Offset+b.Data.Length:a.Data.Offset+b.Data.Length+a.Data.Length], raw[a.Data.Offset:a.Data.Offset+a.Data.Length])
	binary.LittleEndian.PutUint32(moved[a.Index.Offset+6:a.Index.Offset+10], uint32(a.Data.Offset+b.Data.Length))
	binary.LittleEndian.PutUint32(moved[b.Index.Offset+6:b.Index.Offset+10], uint32(a.Data.Offset))
	d, e := document.Parse(moved)
	if e != nil || d.CheckMutation() != nil {
		t.Fatal(e)
	}
	c, _ := d.CursorAt(0)
	noop, e := d.TypeoverASCII(c, []byte("A"))
	if e != nil || noop.Changed || noop.Document != d {
		t.Fatal("same-byte metadata dirt")
	}
	exact(t, d, moved)
	edit, e := d.InsertASCII(c, []byte("X"))
	if e != nil {
		t.Fatal(e)
	}
	got, _ := edit.Document.Export()
	want := append(bytes.Clone(moved[:info.Body.Offset]), append([]byte("X"), moved[info.Body.Offset:]...)...)
	want[a.Data.Offset+b.Data.Length] |= 8
	if !bytes.Equal(got, want) {
		t.Fatal("indexed relocated flag")
	}
	other, _ := document.Parse(moved)
	foreign, _ := other.CursorAt(0)
	_, e = d.InsertASCII(foreign, []byte("X"))
	category(t, e, document.RevisionMismatch)
	captured := edit.Cursor
	*edit.Document = *other
	off, e := captured.Offset()
	if e != nil || off != info.Body.Offset+1 {
		t.Fatal("rebound handle corrupted cursor")
	}
	exact(t, d, moved)
}

func TestReorderedHistoryRefusalsAndLiteralGrowth(t *testing.T) {
	raw := reorderedSource(t, "one-bold", "W42G3")
	d, _ := document.Parse(raw)
	h, _ := document.NewHistory(d)
	c, _ := d.CursorAt(1)
	pending, e := d.Delete(c, document.ForwardDelete, h)
	if e != nil || !pending.Pending() {
		t.Fatal(e)
	}
	declined, e := d.AnswerDeletion(h, pending, document.No)
	if e != nil || declined.NativeChanged() {
		t.Fatal(e)
	}
	exact(t, declined.Document(), raw)
	_, e = d.AnswerDeletion(h, pending, document.Yes)
	category(t, e, document.UnsupportedHistoryEffect)
	a, _ := d.CursorAt(1)
	b, _ := d.CursorAt(2)
	p, e := d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), h)
	if e != nil {
		t.Fatal(e)
	}
	r, e := d.AnswerDeletion(h, p, document.Yes)
	if e != nil {
		t.Fatal(e)
	}
	preview, e := r.History().Open(r.Cursor())
	if e != nil {
		t.Fatal(e)
	}
	restored, e := r.Document().Restore(r.History(), preview)
	if e != nil {
		t.Fatal(e)
	}
	if restored.Document().CheckMutation() != nil {
		t.Fatal("empty pair not admitted")
	}
	// A second repair/restore would require a third Bold pair and must fail before
	// publication under the existing growth limit, retaining the previous state.
	d = restored.Document()
	h = restored.History()
	a, _ = d.CursorAt(4)
	b, _ = d.CursorAt(5)
	p, e = d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), h)
	if e == nil {
		r, e = d.AnswerDeletion(h, p, document.Yes)
		if e == nil {
			preview, e = r.History().Open(r.Cursor())
			if e == nil {
				_, e = r.Document().Restore(r.History(), preview)
			}
		}
	}
	if e == nil {
		t.Fatal("unqualified repeated context/growth admitted")
	}
	before, _ := d.Export()
	exact(t, d, before)
}

func TestReorderedFuzzSeedReachability(t *testing.T) {
	raw := reorderedSource(t, "two-bold", "W42G3")
	for _, v := range []struct {
		selector, value byte
		text            string
		success         bool
	}{{0, 0, "X", true}, {1, 2, "Y", true}, {4, 0, "X", false}} {
		input := bytes.Clone(raw)
		if v.selector%2 == 0 {
			input[16+int(v.value)%308] ^= v.selector / 2
		}
		d, e := document.Parse(input)
		if e != nil {
			if v.success {
				t.Fatal(e)
			}
			continue
		}
		c, _ := d.CursorAt(int(v.value) % (d.TokenCount() + 1))
		r, e := d.InsertASCII(c, []byte(v.text))
		if (e == nil) != v.success {
			t.Fatal("seed reachability", v, e)
		}
		exact(t, d, input)
		if v.success && (!r.Changed || r.Document.CheckMutation() != nil) {
			t.Fatal("seed did not publish a qualified new revision")
		}
	}
}
