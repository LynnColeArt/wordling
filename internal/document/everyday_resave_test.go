package document_test

import (
	"bytes"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
)

// Captured original resave corpus (WP42): six contexts x six stages x two fresh
// witnesses, retained under docs/research/continuation/resaved-prefix/runs.
// These tests pin which family is mutable, which is only readable, and the
// single metadata value that separates them — so a future widening cannot
// quietly turn the blocked family on.
const resaveRoot = "../../docs/research/continuation/resaved-prefix/runs/"

func readFile(path string) ([]byte, error) { return os.ReadFile(path) }

func prefixBytes(t *testing.T, raw []byte) int {
	t.Helper()
	image, err := wp51.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	return image.Inspect().Prefix.Length
}

// statePacket locates the document-state packet's indexed format flag and its
// printer-select counter, so tests can assert on the only prefix bytes a body
// edit is allowed to touch.
func statePacket(t *testing.T, raw []byte) (flags, counter int) {
	t.Helper()
	image, err := wp51.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	for _, p := range image.Inspect().Packets {
		if p.Type == 6 {
			return p.Data.Offset, p.Data.Offset + 8
		}
	}
	t.Fatal("no document-state packet")
	return 0, 0
}

func resave(t *testing.T, rel string) (*document.Document, []byte) {
	t.Helper()
	raw, err := readFile(resaveRoot + rel)
	if err != nil {
		t.Fatal(err)
	}
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatalf("%s: %v", rel, err)
	}
	return d, raw
}

// Disabled-resave stages are the family WP42 nominated for a separately
// authored qualification: complete reordered index, no deleted extents.
func TestDisabledResaveFamilyIsMutable(t *testing.T) {
	for _, caseDir := range []string{
		"w42-ascii-disabled", "w42-one-bold-disabled", "w42-two-bold-disabled",
	} {
		for _, stage := range []string{"W42S0.WP5", "W42G1.WP5", "W42G2.WP5", "W42G3.WP5", "W42EDIT.WP5", "W42FIN.WP5"} {
			rel := caseDir + "/r1/" + stage
			d, raw := resave(t, rel)
			if err := d.CheckMutation(); err != nil {
				t.Fatalf("%s refused: %v", rel, err)
			}
			exact(t, d, raw)
			// A body edit must leave the prefix literal, including the
			// printer-select counter that reaches 02 in the post-print stage.
			c, e := d.CursorAt(0)
			if e != nil {
				t.Fatal(e)
			}
			r, e := d.InsertASCII(c, []byte("Q"))
			if e != nil {
				t.Fatalf("%s: %v", rel, e)
			}
			out, e := r.Document.Export()
			if e != nil {
				t.Fatal(e)
			}
			prefix := prefixBytes(t, raw)
			flags, counter := statePacket(t, raw)
			// The only permitted prefix change is the indexed format flag gaining
			// bit 8 (the original's own edited-state bit); the post-print counter
			// and every other prefix byte stay literal.
			if got := out[flags]; got != raw[flags]|8 {
				t.Fatalf("%s format flag %#x -> %#x", rel, raw[flags], got)
			}
			if out[counter] != raw[counter] {
				t.Fatalf("%s counter changed %#x -> %#x", rel, raw[counter], out[counter])
			}
			diffs := 0
			for i := 0; i < prefix; i++ {
				if i != flags && out[i] != raw[i] {
					t.Fatalf("%s prefix byte %d changed outside the format flag", rel, i)
				}
				if out[i] != raw[i] {
					diffs++
				}
			}
			if diffs > 1 {
				t.Fatalf("%s prefix diffs %d", rel, diffs)
			}
			if !bytes.Equal(out[prefix:], append([]byte("Q"), raw[prefix:]...)) {
				t.Fatalf("%s body splice", rel)
			}
		}
	}
}

// The FastSave baseline family keeps its index-deleted 564 prefix, whose four
// FFFF extents WP42 showed to change across Retrieve/Save/print. Mutation stays
// refused for the whole family; reading and Reveal are unaffected.
func TestFastSaveFamilyStaysRefusedButReadable(t *testing.T) {
	for _, caseDir := range []string{
		"w42-ascii-baseline", "w42-one-bold-baseline", "w42-two-bold-baseline",
	} {
		for _, stage := range []string{"W42G1.WP5", "W42G2.WP5", "W42G3.WP5", "W42EDIT.WP5", "W42FIN.WP5"} {
			rel := caseDir + "/r1/" + stage
			d, raw := resave(t, rel)
			if err := d.CheckMutation(); err == nil {
				t.Fatalf("%s admitted; WP42 blocked this family for writer admission", rel)
			} else if f, ok := err.(*document.Failure); !ok || f.Category != document.UnsupportedPrefix {
				t.Fatalf("%s: want UnsupportedPrefix, got %v", rel, err)
			}
			// Read and Reveal remain available: every owner is named, none opaque.
			insp, err := document.InspectRevealCatalogue(d, d.Revision(), 0, d.TokenCount())
			if err != nil {
				t.Fatalf("%s catalogue: %v", rel, err)
			}
			for _, e := range insp.Elements {
				if e.Kind == document.Opaque {
					t.Fatalf("%s: opaque owner %v", rel, e)
				}
			}
			c, _ := d.CursorAt(0)
			if _, err := c.Present(0, d.TokenCount()); err != nil {
				t.Fatalf("%s present: %v", rel, err)
			}
			exact(t, d, raw)
		}
	}
}

func TestPrinterSelectCounterAcceptedValues(t *testing.T) {
	// 01 before print, 02 after (WP42 FIN stages). Anything else is unqualified.
	raw, err := readFile(resaveRoot + "w42-ascii-disabled/r1/W42FIN.WP5")
	if err != nil {
		t.Fatal(err)
	}
	image, err := wp51.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	counter := -1
	for _, p := range image.Inspect().Packets {
		if p.Type == 6 {
			counter = p.Data.Offset + 8
		}
	}
	if counter < 0 {
		t.Fatal("no document-state packet in the captured stage")
	}
	if raw[counter] != 0x02 {
		t.Fatalf("post-print counter is %#x, not the documented 02", raw[counter])
	}
	for _, value := range []byte{0x00, 0x03, 0xff} {
		tampered := bytes.Clone(raw)
		tampered[counter] = value
		d, err := document.Parse(tampered)
		if err != nil {
			continue // Native framing may refuse first; that is also a refusal.
		}
		if err := d.CheckMutation(); err == nil {
			t.Fatalf("counter value %#x admitted", value)
		}
	}
}
