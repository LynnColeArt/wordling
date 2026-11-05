package document_test

import (
	"os"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
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
	counts := map[document.Kind]int{}
	var labels strings.Builder
	var unnamed []document.Element
	for _, e := range insp.Elements {
		counts[e.Kind]++
		labels.WriteString(e.Text)
		if e.Kind == document.Opaque {
			unnamed = append(unnamed, e)
		}
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

	// Everything still unnamed must be page structure, not text content: two page
	// transitions, each a variable-length D4 subcode-00 record plus its 8C/99
	// companions. Page records are WP81 and T247 territory; naming them here on a
	// guess would let an edit relocate a structure whose fields are not qualified.
	if len(unnamed) != 6 {
		t.Fatalf("unnamed owners = %d, want two D4 page transitions", len(unnamed))
	}
	var records [][]byte
	for i, e := range unnamed {
		token, err := d.Token(e.TokenIndex)
		if err != nil {
			t.Fatal(err)
		}
		switch i % 3 {
		case 0:
			if token.Raw[0] != 0xd4 || token.Raw[len(token.Raw)-1] != 0xd4 || token.Raw[1] != 0x00 {
				t.Fatalf("expected a D4 subcode-00 page record, got %x", token.Raw)
			}
			records = append(records, token.Raw)
		case 1:
			if len(token.Raw) != 1 || token.Raw[0] != 0x8c {
				t.Fatalf("expected 8C companion, got %x", token.Raw)
			}
		case 2:
			if len(token.Raw) != 1 || token.Raw[0] != 0x99 {
				t.Fatalf("expected 99 companion, got %x", token.Raw)
			}
		}
	}
	// The two captured page records differ in exactly one byte — the page number —
	// which the readiness brief warns must not be treated as a universal constant.
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

	// Declared gap: this capture is refused for mutation because of the unnamed
	// page record. Admitting ordinary page boundaries is the remaining T244
	// task, and it needs a qualified D4 structure rather than a guess.
	if err := d.CheckMutation(); err == nil {
		t.Fatal("page-bearing capture admitted before page records are qualified")
	} else if f, ok := err.(*document.Failure); !ok || f.Category != document.UnsupportedBody {
		t.Fatalf("want UnsupportedBody for the page record, got %v", err)
	}
}
