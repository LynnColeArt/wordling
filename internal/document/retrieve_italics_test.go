package document_test

import (
	"bytes"
	"crypto/sha256"
	"fmt"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
	"github.com/lynncoleart/wordling/internal/wp51"
)

// Native owners observed in the pinned cached ITALICS.WP, not ANSI styles.
var retrieveItalicOn = []byte{0xc3, 0x08, 0xc3}
var retrieveItalicOff = []byte{0xc4, 0x08, 0xc4}

func retrieveItalicsParse(t *testing.T, body []byte) *document.Document {
	t.Helper()
	d, err := document.Parse(synthetic(t, body))
	if err != nil {
		t.Fatal(err)
	}
	return d
}

func retrieveItalicsCall(copy bool, d *document.Document, c document.Cursor, s *document.Document) (document.EditResult, error) {
	if copy {
		return d.InsertBlockCopy(c, s)
	}
	return d.InsertDocument(c, s)
}

func retrieveItalicsRefused(t *testing.T, copy bool, d *document.Document, c document.Cursor, s *document.Document, want document.Category) {
	t.Helper()
	before, _ := d.Export()
	birth, rev := d.Birth(), d.Revision()
	sourceBefore, _ := s.Export()
	sourceRev, sourceBirth := s.Revision(), s.Birth()
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	r, err := retrieveItalicsCall(copy, d, c, s)
	category(t, err, want)
	if r.Document != d || r.Cursor != c || r.Changed || d.Birth() != birth || d.Revision() != rev {
		t.Fatal("refusal changed receiver/dirty/cursor identity")
	}
	exact(t, d, before)
	if sourceBefore != nil {
		exact(t, s, sourceBefore)
	}
	if s.Revision() != sourceRev || s.Birth() != sourceBirth || !h.Qualified() {
		t.Fatal("refusal changed source/history")
	}
}

func retrieveItalicsInserted(t *testing.T, copy bool, d *document.Document, gap int, s *document.Document, inserted []byte, owners int) {
	t.Helper()
	raw, _ := d.Export()
	sourceRaw, _ := s.Export()
	sourceRev, sourceBirth := s.Revision(), s.Birth()
	c, err := d.CursorAt(gap)
	if err != nil {
		t.Fatal(err)
	}
	c = c.WithReveal(true)
	off, err := c.Offset()
	if err != nil {
		t.Fatal(err)
	}
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	r, err := retrieveItalicsCall(copy, d, c, s)
	if err != nil {
		t.Fatalf("balanced native source insertion failed: %v", err)
	}
	expected := cat(raw[:off], inserted, raw[off:])
	expected[256] |= 8
	exact(t, r.Document, expected)
	exact(t, d, raw)
	exact(t, s, sourceRaw)
	expectedGap := gap
	if !copy {
		expectedGap += owners
	}
	if !r.Changed || r.Cursor.Gap() != expectedGap || !r.Cursor.Reveal() || r.Cursor.Revision() != r.Document.Revision() || r.Document.Revision() == d.Revision() || r.Document.Birth() != d.Birth() || r.Document.TokenCount() != d.TokenCount()+owners {
		t.Fatal("insert revision/birth/caret/dirty/owners")
	}
	if s.Revision() != sourceRev || s.Birth() != sourceBirth {
		t.Fatal("source identity changed")
	}
	original, _ := r.Document.OriginalExport()
	if !bytes.Equal(original, raw) {
		t.Fatal("receiver original provenance replaced")
	}
	if err := r.Document.CheckMutation(); err != nil {
		t.Fatal(err)
	}
	if err := r.Document.CheckPrintBody(); err != nil {
		t.Fatal(err)
	}
	next, err := h.AfterRetrieval(r)
	if err != nil || !next.Qualified() {
		t.Fatalf("retrieval history: %v", err)
	}
	reopened, err := document.Parse(expected)
	if err != nil {
		t.Fatal(err)
	}
	exact(t, reopened, expected)
}

func TestRetrieveItalicsPinnedOriginalAndPositions(t *testing.T) {
	raw, err := os.ReadFile("../../docs/research/reference-runs/mission1-appearance/ITALICS.WP")
	if err != nil {
		t.Fatal(err)
	}
	if fmt.Sprintf("%x", sha256.Sum256(raw)) != "24470a1f57bf84cd38527041d8e2d99b0f4330f5a8d442ce43230b334299f7c7" {
		t.Fatal("fixture pin changed")
	}
	source, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	if err := source.CheckMutation(); err != nil {
		t.Fatal(err)
	}
	exact(t, source, raw)
	want := cat(retrieveItalicOn, []byte("alpha"), retrieveItalicOff, []byte("beta"))
	if !bytes.Equal(everydayBody(t, source), want) {
		t.Fatal("independent original body mismatch")
	}
	kinds := []document.Kind{document.ItalicsOn, document.ASCII, document.ASCII, document.ASCII, document.ASCII, document.ASCII, document.ItalicsOff, document.ASCII, document.ASCII, document.ASCII, document.ASCII}
	for i, k := range kinds {
		tok, e := source.Token(i)
		if e != nil || tok.Kind != k {
			t.Fatalf("owner %d identity %v", i, e)
		}
	}
	for _, copy := range []bool{false, true} {
		for _, gap := range []int{0, 2, 4} {
			t.Run(fmt.Sprintf("copy=%v/gap=%d", copy, gap), func(t *testing.T) {
				retrieveItalicsInserted(t, copy, retrieveItalicsParse(t, []byte("LEFT")), gap, source, want, 11)
			})
		}
	}
}

func TestRetrieveItalicsReceiverBoundaries(t *testing.T) {
	receiver := cat([]byte("L"), retrieveItalicOn, []byte("AB"), retrieveItalicOff, []byte("R"))
	sources := map[string][]byte{
		"pair":       cat(retrieveItalicOn, []byte("i"), retrieveItalicOff),
		"surrounded": cat([]byte("p"), retrieveItalicOn, []byte("i"), retrieveItalicOff, []byte("s")),
		"multiple":   cat(retrieveItalicOn, []byte("a"), retrieveItalicOff, []byte("-"), retrieveItalicOn, []byte("b"), retrieveItalicOff),
		"empty-pair": cat(retrieveItalicOn, retrieveItalicOff),
	}
	for _, copy := range []bool{false, true} {
		for name, body := range sources {
			for _, gap := range []int{0, 1, 2, 3, 4, 5, 6} {
				t.Run(fmt.Sprintf("copy=%v/%s/gap=%d", copy, name, gap), func(t *testing.T) {
					d := retrieveItalicsParse(t, receiver)
					s := retrieveItalicsParse(t, body)
					if gap >= 2 && gap <= 4 {
						c, _ := d.CursorAt(gap)
						retrieveItalicsRefused(t, copy, d, c, s, document.UnsupportedBody)
					} else {
						retrieveItalicsInserted(t, copy, d, gap, s, body, s.TokenCount())
					}
				})
			}
		}
	}
}

func TestRetrieveItalicsPlainInsideAndIndependentAttributes(t *testing.T) {
	for _, copy := range []bool{false, true} {
		t.Run(fmt.Sprintf("plain/copy=%v", copy), func(t *testing.T) {
			d := retrieveItalicsParse(t, cat(retrieveItalicOn, []byte("AB"), retrieveItalicOff))
			s := retrieveItalicsParse(t, []byte("plain"))
			retrieveItalicsInserted(t, copy, d, 2, s, []byte("plain"), 5)
		})
		for name, pair := range map[string][2][]byte{"bold": {boldOn, boldOff}, "underline": {underlineOn, underlineOf}, "both": {cat(boldOn, underlineOn), cat(underlineOf, boldOff)}} {
			t.Run(fmt.Sprintf("%s/copy=%v", name, copy), func(t *testing.T) {
				d := retrieveItalicsParse(t, cat(pair[0], []byte("AB"), pair[1]))
				sbody := cat(retrieveItalicOn, []byte("i"), retrieveItalicOff)
				s := retrieveItalicsParse(t, sbody)
				gap := 2
				if name == "both" {
					gap = 3
				}
				retrieveItalicsInserted(t, copy, d, gap, s, sbody, 3)
				conflicting := retrieveItalicsParse(t, cat(pair[0], sbody, pair[1]))
				c, _ := d.CursorAt(gap)
				retrieveItalicsRefused(t, copy, d, c, conflicting, document.UnsupportedBody)
			})
		}
		t.Run(fmt.Sprintf("source-composition/copy=%v", copy), func(t *testing.T) {
			body := cat(boldOn, retrieveItalicOn, underlineOn, []byte("i"), underlineOf, retrieveItalicOff, boldOff)
			s := retrieveItalicsParse(t, body)
			retrieveItalicsInserted(t, copy, retrieveItalicsParse(t, []byte("AB")), 1, s, body, 7)
		})
	}
}

func TestRetrieveItalicsRefusalControls(t *testing.T) {
	bad := map[string][]byte{
		"duplicate-on":  cat(retrieveItalicOn, retrieveItalicOn, []byte("i"), retrieveItalicOff, retrieveItalicOff),
		"unmatched-off": cat([]byte("p"), retrieveItalicOff),
		"unclosed":      cat(retrieveItalicOn, []byte("i")),
		"opaque":        {0x80}, "unsafe-page": {0x8c, 'x'},
		"italic-opaque": cat(retrieveItalicOn, []byte{0x80}, retrieveItalicOff),
	}
	for _, copy := range []bool{false, true} {
		for name, body := range bad {
			t.Run(fmt.Sprintf("copy=%v/%s", copy, name), func(t *testing.T) {
				d := retrieveItalicsParse(t, []byte("AB"))
				s := retrieveItalicsParse(t, body)
				c, _ := d.CursorAt(1)
				retrieveItalicsRefused(t, copy, d, c, s, document.UnsupportedBody)
			})
		}
	}
}

func TestRetrieveItalicsEmptyLimitsForeignStale(t *testing.T) {
	for _, copy := range []bool{false, true} {
		t.Run(fmt.Sprintf("copy=%v", copy), func(t *testing.T) {
			d := retrieveItalicsParse(t, []byte("AB"))
			c, _ := d.CursorAt(1)
			h, _ := document.NewHistory(d)
			empty := retrieveItalicsParse(t, nil)
			r, e := retrieveItalicsCall(copy, d, c, empty)
			if e != nil || r.Changed || r.Document != d || r.Cursor != c {
				t.Fatalf("empty no-op: %v", e)
			}
			next, e := h.AfterRetrieval(r)
			if e != nil || next.Revision() != h.Revision() {
				t.Fatalf("no-op history %v", e)
			}
			source := retrieveItalicsParse(t, cat(retrieveItalicOn, []byte("i"), retrieveItalicOff))
			foreign := retrieveItalicsParse(t, []byte("AB"))
			fc, _ := foreign.CursorAt(1)
			retrieveItalicsRefused(t, copy, d, fc, source, document.RevisionMismatch)
			edited, e := d.InsertASCII(c, []byte("x"))
			if e != nil {
				t.Fatal(e)
			}
			retrieveItalicsRefused(t, copy, edited.Document, c, source, document.RevisionMismatch)
			var invalid document.Document
			retrieveItalicsRefused(t, copy, d, c, &invalid, document.InvalidDocument)
			for name, body := range map[string][]byte{"token-source": bytes.Repeat([]byte("x"), document.MaxMutationTokens+1), "byte-source": bytes.Repeat(observedTab, document.MaxMutationBytes/len(observedTab)+1)} {
				t.Run(name, func(t *testing.T) {
					s := retrieveItalicsParse(t, body)
					retrieveItalicsRefused(t, copy, d, c, s, document.MutationLimit)
				})
			}
			large := retrieveItalicsParse(t, bytes.Repeat([]byte("x"), document.MaxMutationTokens-2))
			lc, _ := large.CursorAt(1)
			retrieveItalicsRefused(t, copy, large, lc, retrieveItalicsParse(t, []byte("iii")), document.MutationLimit)
		})
	}
}

func TestRetrieveItalicsPriorHistorySurvivesAndRemaps(t *testing.T) {
	for _, copy := range []bool{false, true} {
		t.Run(fmt.Sprintf("copy=%v", copy), func(t *testing.T) {
			d := retrieveItalicsParse(t, []byte("Xleft-right"))
			h, _ := document.NewHistory(d)
			c, _ := d.CursorAt(0)
			deleted, e := d.Delete(c, document.ForwardDelete, h)
			if e != nil {
				t.Fatal(e)
			}
			d = deleted.Document()
			h = deleted.History()
			c, _ = d.CursorAt(4)
			s := retrieveItalicsParse(t, cat(retrieveItalicOn, []byte("i"), retrieveItalicOff))
			r, e := retrieveItalicsCall(copy, d, c, s)
			if e != nil {
				t.Fatalf("balanced native source insertion failed: %v", e)
			}
			h, e = h.AfterRetrieval(r)
			if e != nil || !h.Qualified() {
				t.Fatal(e)
			}
			item, e := h.Entry(0)
			if e != nil || string(item.Native) != "X" {
				t.Fatalf("prior history lost: %v", e)
			}
			preview, e := h.Open(r.Cursor)
			if e != nil {
				t.Fatal(e)
			}
			restored, e := r.Document.Restore(h, preview)
			if e != nil {
				t.Fatal(e)
			}
			gap := 7
			if copy {
				gap = 4
			}
			want := cat([]byte("left"), retrieveItalicOn, []byte("i"), retrieveItalicOff, []byte("-right"))
			at := 4 + 7
			if copy {
				at = 4
			}
			want = cat(want[:at], []byte("X"), want[at:])
			if !bytes.Equal(everydayBody(t, restored.Document()), want) || restored.Cursor().Gap() != gap+1 {
				t.Fatal("history restoration/token mapping")
			}
		})
	}
}

// This exercises the source candidate's existing native/print projection. The
// cached PRN is a source-shape witness, never a new original process execution.
func TestRetrieveItalicsNewBirthAndCandidateProjection(t *testing.T) {
	raw, err := os.ReadFile("../../docs/research/reference-runs/mission1-appearance/ITALICS.WP")
	if err != nil {
		t.Fatal(err)
	}
	source, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	printWant, err := os.ReadFile("../../docs/research/reference-runs/mission1-appearance/ITALICS.PRN")
	if err != nil {
		t.Fatal(err)
	}
	if fmt.Sprintf("%x", sha256.Sum256(printWant)) != "74cd863025a77422e94876aca0171ef62116669aa5c0696eab2f01c099b4267a" {
		t.Fatal("print pin changed")
	}
	for _, copy := range []bool{false, true} {
		t.Run(fmt.Sprintf("copy=%v", copy), func(t *testing.T) {
			d := newDocument(t)
			before, _ := d.Export()
			birth := d.Birth()
			c, _ := d.CursorAt(0)
			h, _ := document.NewHistory(d)
			r, err := retrieveItalicsCall(copy, d, c, source)
			if err != nil {
				t.Fatalf("balanced native source insertion failed: %v", err)
			}
			want := cat(before, retrieveItalicOn, []byte("alpha"), retrieveItalicOff, []byte("beta"))
			image, err := wp51.Parse(before)
			if err != nil {
				t.Fatal(err)
			}
			flags := -1
			for _, p := range image.Inspect().Packets {
				if p.Type == 6 {
					flags = p.Data.Offset
				}
			}
			if flags < 0 {
				t.Fatal("missing receiver document-flags owner")
			}
			want[flags] |= 8
			exact(t, r.Document, want)
			exact(t, d, before)
			exact(t, source, raw)
			newOriginalAbsent(t, r.Document, birth)
			expectedGap := 11
			if copy {
				expectedGap = 0
			}
			if !r.Changed || r.Cursor.Gap() != expectedGap {
				t.Fatal("New insertion dirty/caret")
			}
			next, err := h.AfterRetrieval(r)
			if err != nil || !next.Qualified() {
				t.Fatalf("New history: %v", err)
			}
			reopened, err := document.Parse(want)
			if err != nil {
				t.Fatal(err)
			}
			exact(t, reopened, want)
			settings := layout.Settings{PageWidthInches: 8.5, PageHeightInches: 11, MarginLeftInches: 1, MarginRightInches: 1, MarginTopInches: 1, MarginBottomInches: 1, CPI: 10, LineSpacing: 1, HyphenationNo: true, FullJustification: true, RelativeTabSet: true}
			pages, err := layout.StandardPages(reopened, settings)
			if err != nil {
				t.Fatal(err)
			}
			if got := layout.StandardPrint(pages); !bytes.Equal(got, printWant) {
				t.Fatal("native inserted candidate projection differs from pinned source print")
			}
		})
	}
}
