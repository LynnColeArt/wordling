package document_test

import (
	"bytes"
	"os"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
)

// The captured flow document is the reference everyday original: it carries a
// soft return, an underline pair, the 9-byte Tab owner and an unbroken-word
// deleted soft return in one file. Exercising it end to end is stronger than the
// synthetic bodies above, which only prove the API accepts shapes.
const flowFirst = "../../docs/research/everyday-contract-2026-11-05/qualification/flow/exports/FIRST.WP"

func TestCapturedFlowDocumentOwners(t *testing.T) {
	raw, err := os.ReadFile(flowFirst)
	if err != nil {
		t.Fatal(err)
	}
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	exact(t, d, raw)

	insp, err := document.InspectRevealCatalogue(d, d.Revision(), 0, d.TokenCount())
	if err != nil {
		t.Fatal(err)
	}
	// Page structure is now admitted as named owners rather than refused, but no
	// captured screen shows how the original renders them, so they carry no label.
	counts := map[document.Kind]int{}
	var labels strings.Builder
	for _, e := range insp.Elements {
		counts[e.Kind]++
		labels.WriteString(e.Text)
		if e.Kind == document.Opaque {
			t.Fatalf("opaque owner at token %d: %x", e.TokenIndex, e.Span)
		}
		if e.Kind == document.EndOfPage && e.Text != "" {
			t.Fatalf("invented Reveal label for the page record: %q", e.Text)
		}
	}
	if counts[document.EndOfPage] != 2 || counts[document.HardReturnSoftPage] != 2 || counts[document.DormantHardReturn] != 2 {
		t.Fatalf("page owners %d/%d/%d, want 2/2/2",
			counts[document.EndOfPage], counts[document.HardReturnSoftPage], counts[document.DormantHardReturn])
	}
	for _, want := range []document.Kind{
		document.SoftReturn, document.UnderlineOn, document.UnderlineOff,
		document.Tab, document.HardReturn, document.DeletedSoftReturn,
	} {
		if counts[want] == 0 {
			t.Fatalf("captured document has no owner of kind %d", want)
		}
	}

	// The Reveal labels the original showed for this document.
	text := labels.String()
	for _, want := range []string{"[SRt]", "[UND]", "[und]", "[Tab]", "[HRt]", "[DSRt]"} {
		if !strings.Contains(text, want) {
			t.Fatalf("missing %s in revealed text", want)
		}
	}

	// The two page records are structurally identical except the page number, which
	// is the fact the readiness brief warns against turning into a constant. The
	// record's other fields stay literal and uninterpreted.
	var records [][]byte
	for i, e := range insp.Elements {
		if e.Kind != document.EndOfPage {
			continue
		}
		token, err := d.Token(i)
		if err != nil {
			t.Fatal(err)
		}
		records = append(records, token.Raw)
	}
	if len(records) != 2 {
		t.Fatalf("page records = %d", len(records))
	}
	differing := 0
	for i := range records[0] {
		if records[0][i] != records[1][i] {
			differing++
		}
	}
	if differing != 1 {
		t.Fatalf("page records differ in %d bytes, want only the page number", differing)
	}

	// The unbroken word keeps its exact 65 characters before the DSRt, which is
	// the bounded observation the proofreading contract records — not a rule.
	dsrt := -1
	for i, e := range insp.Elements {
		if e.Kind == document.DeletedSoftReturn {
			dsrt = i
		}
	}
	if dsrt < 0 {
		t.Fatal("no deleted soft return")
	}
	run := 0
	for i := dsrt - 1; i >= 0 && insp.Elements[i].Kind == document.ASCII; i-- {
		run++
	}
	if run != 65 {
		t.Fatalf("unbroken word run before DSRt = %d, want the captured 65", run)
	}

	// The page-bearing capture is now editable, and an edit must leave every page
	// record literal: no field is regenerated, no page number is recomputed.
	if err := d.CheckMutation(); err != nil {
		t.Fatalf("page-bearing capture refused: %v", err)
	}
	c, err := d.CursorAt(0)
	if err != nil {
		t.Fatal(err)
	}
	r, err := d.InsertASCII(c, []byte("Z"))
	if err != nil {
		t.Fatal(err)
	}
	out, err := r.Document.Export()
	if err != nil {
		t.Fatal(err)
	}
	for _, want := range records {
		if !bytes.Contains(out, want) {
			t.Fatalf("edit altered page record %x", want)
		}
	}
	if !bytes.Equal(out[324:], append([]byte("Z"), raw[324:]...)) {
		t.Fatal("body splice")
	}
	diffs := 0
	for i := 0; i < 324; i++ {
		if out[i] != raw[i] {
			diffs++
		}
	}
	if diffs > 1 {
		t.Fatalf("prefix differences %d, want at most the format flag", diffs)
	}
}

// The page-record shape validator is a guard, so a record that breaks any of its
// structural invariants must stop being a named owner and refuse mutation — the
// document must not be editable around a page structure it cannot account for.
func TestMalformedPageRecordRefused(t *testing.T) {
	raw, err := os.ReadFile(flowFirst)
	if err != nil {
		t.Fatal(err)
	}
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	insp, err := document.InspectRevealCatalogue(d, d.Revision(), 0, d.TokenCount())
	if err != nil {
		t.Fatal(err)
	}
	var span wp51.Span
	found := false
	for i, e := range insp.Elements {
		if e.Kind == document.EndOfPage {
			token, err := d.Token(i)
			if err != nil {
				t.Fatal(err)
			}
			span, found = token.Span, true
			break
		}
	}
	if !found {
		t.Fatal("no page record in the capture")
	}
	for name, at := range map[string]int{
		"declared length": span.Offset + 2,
		"group marker":    span.Offset + 4,
		"group length":    span.Offset + 5,
		"end delimiter":   span.Offset + span.Length - 1,
	} {
		for _, value := range []byte{0x01, 0x7f, 0xff} {
			tampered := bytes.Clone(raw)
			if tampered[at] == value {
				continue
			}
			tampered[at] = value
			d, err := document.Parse(tampered)
			if err != nil {
				continue // Framing may refuse first; that is also a refusal.
			}
			if err := d.CheckMutation(); err == nil {
				t.Fatalf("%s = %#x admitted", name, value)
			}
		}
	}
}
