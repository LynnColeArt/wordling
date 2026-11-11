package document_test

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

const proofQualification = "../../docs/research/everyday-contract-2026-11-05/qualification"

func proofFixture(t *testing.T, family, name string) []byte {
	t.Helper()
	b, err := os.ReadFile(filepath.Join(proofQualification, family, "exports", name))
	if err != nil {
		t.Fatal(err)
	}
	return b
}

func proofParse(t *testing.T, raw []byte) *document.Document {
	t.Helper()
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	return d
}

func proofCursor(t *testing.T, d *document.Document, gap int) document.Cursor {
	t.Helper()
	c, err := d.CursorAt(gap)
	if err != nil {
		t.Fatal(err)
	}
	return c
}

func proofRange(t *testing.T, d *document.Document, native []byte) (document.Cursor, document.Cursor) {
	t.Helper()
	raw, err := d.Export()
	if err != nil {
		t.Fatal(err)
	}
	bodyStart, err := proofCursor(t, d, 0).Offset()
	if err != nil {
		t.Fatal(err)
	}
	offset := bytes.Index(raw[bodyStart:], native)
	if offset < 0 {
		t.Fatalf("native fixture has no %x", native)
	}
	at := bodyStart + offset
	start, end := -1, -1
	for gap := range d.TokenCount() + 1 {
		c := proofCursor(t, d, gap)
		position, err := c.Offset()
		if err != nil {
			t.Fatal(err)
		}
		if position == at {
			start = gap
		}
		if position == at+len(native) {
			end = gap
			break
		}
	}
	if start < 0 || end < 0 {
		t.Fatalf("fixture range %x cuts a native owner", native)
	}
	return proofCursor(t, d, start), proofCursor(t, d, end)
}

func proofReplace(t *testing.T, d *document.Document, h document.History, native []byte, expected, replacement string) (document.EditResult, document.History) {
	t.Helper()
	start, end := proofRange(t, d, native)
	edit, err := d.ReplaceProofWord(start, end, expected, replacement)
	if err != nil {
		t.Fatal(err)
	}
	next, err := h.AfterProofCorrection(edit)
	if err != nil || !next.Qualified() {
		t.Fatalf("proof history did not retain qualification: %v", err)
	}
	return edit, next
}

func proofExact(t *testing.T, d *document.Document, want []byte) {
	t.Helper()
	want = bytes.Clone(want)
	// These original 324-byte captures may leave the document formatting
	// flag clear after save. The existing publisher qualifies bit 3 only.
	want[256] |= 8
	exact(t, d, want)
}

func TestProofCorrectionPreservesOriginalWholeWordWrappersAndPage(t *testing.T) {
	raw := proofFixture(t, "proof-pages", "BEFORE.WP")
	d := proofParse(t, raw)
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	// First occurrence is enclosed by the original Bold pair.
	a, h := proofReplace(t, d, h, []byte("quik"), "quik", "quick")
	// Underline independently encloses the second suspect.
	b, h := proofReplace(t, a.Document, h, []byte("mispelled"), "mispelled", "misspelled")
	c, h := proofReplace(t, b.Document, h, []byte("quik"), "quik", "quick")
	proofExact(t, c.Document, proofFixture(t, "proof-pages", "PAGEONLY.WP"))
	last, h := proofReplace(t, c.Document, h, []byte("quik"), "quik", "quick")
	proofExact(t, last.Document, proofFixture(t, "proof-pages", "PAGES.WP"))
	exact(t, d, raw)
	if h.Count() != 0 {
		t.Fatal("original-style proof replacements invented an Undelete group")
	}
}

func TestProofCorrectionOriginalInteriorOwnersAndCappedResidue(t *testing.T) {
	raw := proofFixture(t, "proof-boundaries", "BEFORE.WP")
	d := proofParse(t, raw)
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	a, h := proofReplace(t, d, h, cat([]byte("qu"), []byte{0xc3, 0x0c, 0xc3}, []byte("ik")), "quik", "quick")
	b, h := proofReplace(t, a.Document, h,
		cat([]byte("mi"), underlineOn, []byte("spel"), underlineOf, []byte("led")), "mispelled", "misspelled")
	consumed := strings.Repeat("X", document.MaxProofWordBytes)
	c, h := proofReplace(t, b.Document, h, []byte(consumed), consumed, "qUICK")
	if !bytes.HasSuffix(everydayBody(t, c.Document), cat([]byte("qUICKX"), []byte{0x90}, []byte("YYYYYYYYYY"))) {
		t.Fatal("capped correction touched native residue outside the selected range")
	}
	wrap, _ := proofRange(t, c.Document, []byte{0x90})
	plan, err := document.NewReflowPlan(c.Document, []document.ReflowChange{{At: wrap.Gap(), Kind: document.RemoveDeletedSoftReturn}})
	if err != nil {
		t.Fatal(err)
	}
	final, err := c.Document.AdoptReflow(c.Cursor, plan)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := h.AfterReflow(final); err != nil {
		t.Fatal(err)
	}
	proofExact(t, final.Document, proofFixture(t, "proof-boundaries", "BOUNDARY.WP"))
	proofExact(t, final.Document, proofFixture(t, "proof-boundaries-repeat", "BOUNDARY.WP"))
	exact(t, d, raw)
}

func TestProofCorrectionCarriesExistingUndeleteAndChecksReceipt(t *testing.T) {
	raw := synthetic(t, []byte("  ONENE quik"))
	d := proofParse(t, raw)
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	c := proofCursor(t, d, 5)
	for range 2 {
		deleted, err := d.Delete(c, document.ForwardDelete, h)
		if err != nil {
			t.Fatal(err)
		}
		d, c, h = deleted.Document(), deleted.Cursor(), deleted.History()
	}
	prior, err := h.Entry(0)
	if err != nil || string(prior.Native) != "NE" {
		t.Fatalf("deletion premise: %+v, %v", prior, err)
	}
	changed, next := proofReplace(t, d, h, []byte("quik"), "quik", "quick")
	got, err := next.Entry(0)
	if err != nil || !bytes.Equal(got.Native, prior.Native) || next.Count() != h.Count() {
		t.Fatalf("proof changed history: %+v, %v", got, err)
	}
	p, err := next.Open(changed.Cursor)
	if err != nil {
		t.Fatal(err)
	}
	restored, err := changed.Document.Restore(next, p)
	if err != nil || string(everydayBody(t, restored.Document())) != "  ONE quickNE" {
		t.Fatalf("previous original-style Undelete group could not restore: %v", err)
	}
	if _, err := next.AfterProofCorrection(changed); err == nil {
		t.Fatal("stale correction receipt admitted")
	}
	if _, err := h.AfterRetrieval(changed); err == nil {
		t.Fatal("correction receipt admitted as retrieval")
	}
	forged := changed
	forged.Cursor = changed.Cursor.WithReveal(true)
	if _, err := h.AfterProofCorrection(forged); err == nil {
		t.Fatal("altered exported cursor changed proof authority")
	}
	start, end := proofRange(t, d, []byte("quik"))
	same, err := d.ReplaceProofWord(start, end, "quik", "quik")
	if err != nil || same.Changed || same.Cursor != start || same.Document.Revision() != d.Revision() {
		t.Fatalf("exact no-op changed native identity or cursor: %v", err)
	}
	unchanged, err := h.AfterProofCorrection(same)
	if err != nil || unchanged.Revision() != h.Revision() {
		t.Fatalf("no-op changed history: %v", err)
	}
	if out, err := changed.Document.ReplaceProofWord(start, end, "quik", "quick"); err == nil || out.Document.Revision() != changed.Document.Revision() {
		t.Fatal("foreign or stale range admitted")
	}
}

func TestProofCorrectionChecksSourceAndDerivedBoundaries(t *testing.T) {
	raw := synthetic(t, []byte("miss\x90ing and qu\rik"))
	d := proofParse(t, raw)
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	start, end := proofRange(t, d, []byte("miss\x90ing"))
	for _, tc := range []struct{ expected, replacement string }{
		{"mIssing", "message"}, {"missing", "two words"}, {"missing", ""}, {"missing", strings.Repeat("A", 65)},
	} {
		result, err := d.ReplaceProofWord(start, end, tc.expected, tc.replacement)
		if err == nil || result.Changed || result.Document.Revision() != d.Revision() {
			t.Fatalf("invalid correction changed native bytes: %+v", tc)
		}
	}
	s, z := proofRange(t, d, []byte("qu\rik"))
	if result, err := d.ReplaceProofWord(s, z, "quik", "quick"); err == nil || result.Changed {
		t.Fatal("space-bearing SRt was mistaken for an inline word break")
	}
	foreign := proofParse(t, raw)
	other := proofCursor(t, foreign, end.Gap())
	if result, err := d.ReplaceProofWord(start, other, "missing", "message"); err == nil || result.Changed {
		t.Fatal("foreign end cursor admitted")
	}
	correct, _ := proofReplace(t, d, h, []byte("miss\x90ing"), "missing", "message")
	if got := string(everydayBody(t, correct.Document)); got != "message and qu\rik" {
		t.Fatalf("checked word with internal DSRt: %q", got)
	}
	exact(t, d, raw)
}

func TestProofCorrectionCheckedPlainDuplicate(t *testing.T) {
	d := proofParse(t, synthetic(t, []byte("The the fox has tWo ears.")))
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	start, end := proofRange(t, d, []byte("the"))
	edit, err := d.DeleteProofDuplicate(start, end, "The", "the")
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterProofCorrection(edit)
	if err != nil {
		t.Fatal(err)
	}
	if got := string(everydayBody(t, edit.Document)); got != "The fox has tWo ears." || edit.Cursor.Gap() != 3 || h.Count() != 0 {
		t.Fatalf("duplicate correction changed wrong range or history: %q gap %d", got, edit.Cursor.Gap())
	}
	irregular, _ := proofReplace(t, edit.Document, h, []byte("tWo"), "tWo", "Two")
	if got := string(everydayBody(t, irregular.Document)); got != "The fox has Two ears." {
		t.Fatalf("case replacement lost requested spelling: %q", got)
	}
	for _, text := range []string{"XThe the fox", "The thermal", "The  the fox"} {
		bad := proofParse(t, synthetic(t, []byte(text)))
		start, end := proofRange(t, bad, []byte("the"))
		if result, err := bad.DeleteProofDuplicate(start, end, "The", "the"); err == nil || result.Changed {
			t.Fatalf("unqualified duplicate range accepted for %q", text)
		}
	}
}

func TestProofCorrectionAdoptsActiveFormattingAnchor(t *testing.T) {
	d := proofParse(t, synthetic(t, []byte("lead ")))
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	open, err := d.BeginUnderline(proofCursor(t, d, d.TokenCount()))
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterUnderline(open)
	if err != nil {
		t.Fatal(err)
	}
	typed, err := open.Document().InsertASCII(open.Cursor(), []byte("dont"))
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterEverydayEdit(typed)
	if err != nil {
		t.Fatal(err)
	}
	start, end := proofRange(t, typed.Document, []byte("dont"))
	edit, err := typed.Document.ReplaceProofWord(start, end, "dont", "don't")
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterProofCorrection(edit)
	if err != nil {
		t.Fatal(err)
	}
	if got := everydayBody(t, edit.Document); !bytes.Equal(got, cat([]byte("lead "), underlineOn, []byte("don't"), underlineOf)) {
		t.Fatalf("enclosing owners changed: %x", got)
	}
	active, ok := h.ActiveUnderline(edit.Document)
	if !ok {
		t.Fatal("original active format anchor no longer names the corrected revision")
	}
	if _, err := edit.Document.CloseUnderline(edit.Cursor, active); err != nil {
		t.Fatalf("remapped anchor cannot close: %v", err)
	}
}

func TestProofCorrectionChecksCompleteNoSeparatorPageGroup(t *testing.T) {
	for _, tc := range []struct {
		name, body, before, after string
		kind                      document.ReflowKind
		accepted                  bool
	}{
		{"no separator", "mispelled", "mis", "pelled", document.InsertDeletedSoftPage, true},
		{"lexical separator", "mis pelled", "mis", "pelled", document.WrapSpaceToPage, false},
	} {
		t.Run(tc.name, func(t *testing.T) {
			d := proofParse(t, synthetic(t, []byte(tc.body)))
			c := proofCursor(t, d, 0)
			p, err := document.NewReflowPlan(d, []document.ReflowChange{{At: len(tc.before), Kind: tc.kind, Page: 1}})
			if err != nil {
				t.Fatal(err)
			}
			reflowed, err := d.AdoptReflow(c, p)
			if err != nil {
				t.Fatal(err)
			}
			d = reflowed.Document
			start, end := proofCursor(t, d, 0), proofCursor(t, d, d.TokenCount())
			edit, err := d.ReplaceProofWord(start, end, tc.before+tc.after, "misspelled")
			if !tc.accepted {
				if err == nil || edit.Changed {
					t.Fatal("space-bearing page owner was mistaken for an inline word boundary")
				}
				return
			}
			if err != nil || string(everydayBody(t, edit.Document)) != "misspelled" {
				t.Fatalf("no-separator page group correction failed: %v", err)
			}
		})
	}
}

func TestProofCorrectionRefusesUnrelatedPartialWordRanges(t *testing.T) {
	boldOn := []byte{0xc3, 0x0c, 0xc3}
	boldOff := []byte{0xc4, 0x0c, 0xc4}
	formatted := cat([]byte("ab"), boldOn, []byte("cde"), boldOff, []byte("f fox"))
	for _, tc := range []struct {
		name, expected string
		body, native   []byte
	}{
		{"short prefix", "abc", []byte("abcdef fox"), []byte("abc")},
		{"short interior", "bcd", []byte("abcdef fox"), []byte("bcd")},
		{"format-separated interior", "cde", formatted, []byte("cde")},
		{"format-separated prefix", "ab", formatted, []byte("ab")},
		{"derived line before", "def", []byte("abc\x90def"), []byte("def")},
		{"derived line after", "abc", []byte("abc\x90def"), []byte("abc")},
		{"number before", "abc", []byte("123abc"), []byte("abc")},
		{"number after", "abc", []byte("abc123"), []byte("abc")},
		{"internal apostrophe", "don", []byte("don't"), []byte("don")},
	} {
		t.Run(tc.name, func(t *testing.T) {
			raw := synthetic(t, tc.body)
			d := proofParse(t, raw)
			start, end := proofRange(t, d, tc.native)
			edit, err := d.ReplaceProofWord(start, end, tc.expected, "edit")
			if err == nil || edit.Changed || edit.Document.Revision() != d.Revision() || edit.Cursor != start {
				t.Fatalf("partial range escaped checked word authority: %v", err)
			}
			exact(t, d, raw)
		})
	}
}

func TestProofCorrectionChecksNeighborsAcrossMatchedSoftPage(t *testing.T) {
	for _, tc := range []struct {
		name string
		text string
		kind document.ReflowKind
	}{
		{"no separator", "abcdef", document.InsertDeletedSoftPage},
		{"lexical separator", "abc def", document.WrapSpaceToPage},
	} {
		t.Run(tc.name, func(t *testing.T) {
			d := proofParse(t, synthetic(t, []byte(tc.text)))
			p, err := document.NewReflowPlan(d, []document.ReflowChange{{At: 3, Kind: tc.kind, Page: 1}})
			if err != nil {
				t.Fatal(err)
			}
			reflowed, err := d.AdoptReflow(proofCursor(t, d, 0), p)
			if err != nil {
				t.Fatal(err)
			}
			d = reflowed.Document
			for _, word := range []string{"abc", "def"} {
				start, end := proofRange(t, d, []byte(word))
				edit, err := d.ReplaceProofWord(start, end, word, "edit")
				if tc.kind == document.InsertDeletedSoftPage {
					if err == nil || edit.Changed || edit.Document.Revision() != d.Revision() {
						t.Fatal("range consumed a partial word across a no-separator page")
					}
				} else if err != nil || !edit.Changed {
					t.Fatalf("space-bearing page did not end a word: %v", err)
				}
			}
		})
	}
}

func TestProofCorrectionCapMustStartAtOriginalWordBoundary(t *testing.T) {
	raw := synthetic(t, []byte(strings.Repeat("X", document.MaxProofWordBytes+2)+"!"))
	d := proofParse(t, raw)
	word := strings.Repeat("X", document.MaxProofWordBytes)
	start, end := proofCursor(t, d, 1), proofCursor(t, d, 1+document.MaxProofWordBytes)
	if result, err := d.ReplaceProofWord(start, end, word, "edit"); err == nil || result.Changed {
		t.Fatal("interior 64-character substring acquired cap authority")
	}
	start, end = proofCursor(t, d, 0), proofCursor(t, d, document.MaxProofWordBytes)
	result, err := d.ReplaceProofWord(start, end, word, "edit")
	if err != nil || string(everydayBody(t, result.Document)) != "editXX!" {
		t.Fatalf("true first-64 correction lost exact residue: %v", err)
	}
	exact(t, d, raw)
}

func TestProofCorrectionTreatsSurroundingQuoteAsPunctuation(t *testing.T) {
	raw := synthetic(t, []byte("'quik'"))
	d := proofParse(t, raw)
	start, end := proofRange(t, d, []byte("quik"))
	result, err := d.ReplaceProofWord(start, end, "quik", "quick")
	if err != nil || string(everydayBody(t, result.Document)) != "'quick'" {
		t.Fatalf("a quote was mistaken for an internal apostrophe: %v", err)
	}
}
