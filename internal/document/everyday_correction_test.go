package document_test

import (
	"bytes"
	"crypto/sha256"
	"fmt"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

var (
	everydayTab5  = []byte{0xc1, 2, 0x08, 0x07, 0x08, 0x07, 15, 0, 0xc1}
	everydayTab10 = []byte{0xc1, 2, 0x60, 0x09, 0x60, 0x09, 20, 0, 0xc1}
	everydayTab65 = []byte{0xc1, 2, 0x28, 0x23, 0x28, 0x23, 75, 0, 0xc1}
)

func everydayNative(t *testing.T, body []byte) []byte {
	t.Helper()
	base, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/r3/EVERY.WP")
	if err != nil {
		t.Fatal(err)
	}
	prefix := base[:324:324]
	return append(prefix, body...)
}

func everydayHistory(t *testing.T, d *document.Document) document.History {
	t.Helper()
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	return h
}

func everydayDelete(t *testing.T, d *document.Document, h document.History, gap int, direction document.DeleteDirection) document.Deletion {
	t.Helper()
	r, err := d.DeleteEveryday(proofCursor(t, d, gap), direction, h)
	if err != nil || !r.Applied() || !r.History().Qualified() {
		t.Fatalf("delete at %d failed: %v", gap, err)
	}
	return r
}

func everydayEntry(t *testing.T, h document.History, index int, want []byte, commands int) {
	t.Helper()
	e, err := h.Entry(index)
	if err != nil || !bytes.Equal(e.Native, want) || e.Commands != commands {
		t.Fatalf("history %d: got %x (%d commands), want %x (%d commands): %v", index, e.Native, e.Commands, want, commands, err)
	}
}

func TestEverydayLoadedBackspaceOriginalHistory(t *testing.T) {
	// BSP99.WP from the stopped 03/09/92 repeat with Fast Save disabled.
	// OUT99.WP has the same resulting body, with a DOS-rewritten prefix.
	source := everydayNative(t, cat([]byte("QABC\nDEF"), everydayTab5, []byte("GHI")))
	output := everydayNative(t, []byte("ABDEFGHI"))
	const digest = "de8e1c557352f849b42977dda91f803c12bf07e1b60e96b9d83fbac5a67219a6"
	if got := fmt.Sprintf("%x", sha256.Sum256(source)); got != digest {
		t.Fatalf("original fixture SHA-256 %s, want %s", got, digest)
	}
	d := proofParse(t, source)
	h := everydayHistory(t, d)
	q := everydayDelete(t, d, h, 0, document.ForwardDelete)
	hrt := everydayDelete(t, q.Document(), q.History(), 4, document.Backspace)
	everydayEntry(t, hrt.History(), 0, []byte("\n"), 1)
	everydayEntry(t, hrt.History(), 1, []byte("Q"), 1)
	joined, h := refreshEverydayTab(t, hrt.Document(), hrt.History(), 6, 10, hrt.Cursor().Gap())
	proofExact(t, joined.Document, everydayNative(t, cat([]byte("ABCDEF"), everydayTab10, []byte("GHI"))))
	tab := everydayDelete(t, joined.Document, h, 7, document.Backspace)
	everydayEntry(t, tab.History(), 0, everydayTab10, 1)
	everydayEntry(t, tab.History(), 1, []byte("\n"), 1)
	everydayEntry(t, tab.History(), 2, []byte("Q"), 1)
	ascii := everydayDelete(t, tab.Document(), tab.History(), 3, document.Backspace)
	if ascii.History().Count() != 3 || ascii.Cursor().Gap() != 2 {
		t.Fatalf("bad final stack/caret: count %d gap %d", ascii.History().Count(), ascii.Cursor().Gap())
	}
	everydayEntry(t, ascii.History(), 0, []byte("C"), 1)
	everydayEntry(t, ascii.History(), 1, everydayTab10, 1)
	everydayEntry(t, ascii.History(), 2, []byte("\n"), 1)
	proofExact(t, ascii.Document(), output)
	exact(t, d, source)

	preview, err := tab.History().Open(tab.Cursor())
	if err != nil {
		t.Fatal(err)
	}
	restored, err := tab.Document().Restore(tab.History(), preview)
	if err != nil || !restored.Applied() || restored.Cursor().Gap() != 7 || restored.History().Count() != 3 {
		t.Fatalf("restore complete Tab: %v", err)
	}
	exact(t, restored.Document(), mustEverydayExport(t, joined.Document))
}

func TestEverydayBackspacePrependsToItsOwnGroup(t *testing.T) {
	d := proofParse(t, everydayNative(t, []byte("ABC\nDEF")))
	h := everydayHistory(t, d)
	prior := everydayDelete(t, d, h, 0, document.ForwardDelete)
	e := everydayDelete(t, prior.Document(), prior.History(), 6, document.Backspace)
	f := everydayDelete(t, e.Document(), e.History(), 5, document.Backspace)
	everydayEntry(t, f.History(), 0, []byte("EF"), 2)
	everydayEntry(t, f.History(), 1, []byte("A"), 1)
	p, err := f.History().Open(f.Cursor())
	if err != nil {
		t.Fatal(err)
	}
	r, err := f.Document().Restore(f.History(), p)
	if err != nil {
		t.Fatal(err)
	}
	proofExact(t, r.Document(), everydayNative(t, []byte("BC\nDEF")))
}

func TestEverydayBlockNativeDirectionAndQuestionAuthority(t *testing.T) {
	for _, endpoints := range [][2]int{{3, 5}, {5, 3}} {
		t.Run(fmt.Sprint(endpoints), func(t *testing.T) {
			d := proofParse(t, everydayNative(t, []byte("Q  ONE")))
			prior := everydayDelete(t, d, everydayHistory(t, d), 0, document.ForwardDelete)
			d, h := prior.Document(), prior.History()
			current := proofCursor(t, d, 3)
			anchor, end := proofCursor(t, d, endpoints[0]), proofCursor(t, d, endpoints[1])
			ask := func(h document.History) document.Deletion {
				r, err := d.DeleteEverydayBlock(current, anchor, end, h)
				if err != nil || !r.Pending() || r.Prompt() != "Delete Block? No (Yes)" || r.Cursor() != current {
					t.Fatalf("block question: %v", err)
				}
				lo, hi, ok := r.BlockRange()
				if !ok || lo != 3 || hi != 5 {
					t.Fatalf("bad range: %d %d %t", lo, hi, ok)
				}
				return r
			}
			question := ask(h)
			no, err := d.AnswerDeletion(h, question, document.No)
			if err != nil || no.Pending() || !no.BlockActive() || no.Cursor() != current || no.History().Count() != 1 {
				t.Fatalf("decline lost block/caret/history: %v", err)
			}
			exact(t, no.Document(), mustEverydayExport(t, d))
			if stale, err := d.AnswerDeletion(no.History(), question, document.Yes); err == nil || stale.Applied() {
				t.Fatal("declined question remained authoritative")
			}
			cancel, err := d.CancelBlock(no.History(), no)
			if err != nil || cancel.BlockActive() || cancel.Cursor() != current || cancel.History().Count() != 1 {
				t.Fatalf("cancel block: %v", err)
			}
			h = cancel.History()
			yes, err := d.AnswerDeletion(h, ask(h), document.Yes)
			if err != nil || !yes.Applied() || yes.BlockActive() || yes.Cursor().Gap() != 3 {
				t.Fatalf("confirmed block: %v", err)
			}
			proofExact(t, yes.Document(), everydayNative(t, []byte("  O")))
			everydayEntry(t, yes.History(), 0, []byte("NE"), 1)
			everydayEntry(t, yes.History(), 1, []byte("Q"), 1)
			p, err := yes.History().Open(yes.Cursor())
			if err != nil {
				t.Fatal(err)
			}
			r, err := yes.Document().Restore(yes.History(), p)
			if err != nil || r.Cursor().Gap() != 5 {
				t.Fatalf("restore block: %v", err)
			}
			exact(t, r.Document(), mustEverydayExport(t, d))
			foreign := proofParse(t, mustEverydayExport(t, d))
			if wrong, err := d.DeleteEverydayBlock(current, proofCursor(t, foreign, 3), end, h); err == nil || wrong.Pending() {
				t.Fatal("foreign selection authorized")
			}
		})
	}
}

func mustEverydayExport(t *testing.T, d *document.Document) []byte {
	t.Helper()
	raw, err := d.Export()
	if err != nil {
		t.Fatal(err)
	}
	return raw
}

func refreshEverydayTab(t *testing.T, d *document.Document, h document.History, index int, column uint16, gap int) (document.EditResult, document.History) {
	t.Helper()
	p, err := document.NewReflowPlan(d, []document.ReflowChange{{At: index, Kind: document.RefreshTabCache, Column: column}})
	if err != nil {
		t.Fatal(err)
	}
	r, err := d.AdoptReflow(proofCursor(t, d, gap), p)
	if err != nil {
		t.Fatal(err)
	}
	next, err := h.AfterReflow(r)
	if err != nil || r.Cursor.Gap() != gap {
		t.Fatalf("refresh moved caret or lost history: %v", err)
	}
	return r, next
}

func TestEverydayTabCheckedStopsAndNoOp(t *testing.T) {
	d := proofParse(t, everydayNative(t, []byte("ABC")))
	h := everydayHistory(t, d)
	for _, tc := range []struct {
		stop int
		raw  []byte
	}{{5, everydayTab5}, {10, everydayTab10}, {65, everydayTab65}} {
		r, err := d.InsertEverydayTab(proofCursor(t, d, 0), tc.stop)
		if err != nil {
			t.Fatal(err)
		}
		have, err := r.Document.Token(0)
		if err != nil || !bytes.Equal(have.Raw, tc.raw) {
			t.Fatalf("Tab at stop %d: %x", tc.stop, have.Raw)
		}
		next, err := h.AfterEverydayEdit(r)
		if err != nil {
			t.Fatal(err)
		}
		no, unchanged := refreshEverydayTab(t, r.Document, next, 0, uint16(tc.stop), 1)
		if no.Changed || no.Document.Revision() != r.Document.Revision() || unchanged.Revision() != next.Revision() {
			t.Fatal("matching cache refresh changed revision")
		}
	}
	if _, err := d.InsertEverydayTab(proofCursor(t, d, 0), 6); err == nil {
		t.Fatal("non-profile stop accepted")
	}
	if _, err := document.NewReflowPlan(d, []document.ReflowChange{{At: 0, Kind: document.RefreshTabCache, Column: 70}}); err == nil {
		t.Fatal("outside-profile plan accepted")
	}
	raw := bytes.Clone(everydayTab5)
	raw[4]++
	unknown := proofParse(t, everydayNative(t, cat(raw, []byte("ABC"))))
	p, err := document.NewReflowPlan(unknown, []document.ReflowChange{{At: 0, Kind: document.RefreshTabCache, Column: 5}})
	if err != nil {
		t.Fatal(err)
	}
	no, err := unknown.AdoptReflow(proofCursor(t, unknown, 0), p)
	if err == nil || no.Changed {
		t.Fatal("unmatched cache refreshed")
	}
	refused, err := unknown.DeleteEveryday(proofCursor(t, unknown, 1), document.Backspace, everydayHistory(t, unknown))
	if err == nil || refused.Applied() {
		t.Fatal("unmatched cache deleted")
	}
	if r, err := d.AdoptReflow(proofCursor(t, d, 0), p); err == nil || r.Changed {
		t.Fatal("foreign cache plan accepted")
	}
}

func TestEverydayFormatOverlapsAndPreservesHistory(t *testing.T) {
	d := proofParse(t, everydayNative(t, []byte("X")))
	del := everydayDelete(t, d, everydayHistory(t, d), 0, document.ForwardDelete)
	d, c, h := del.Document(), del.Cursor(), del.History()
	format := func(attribute document.Attribute, close bool) {
		t.Helper()
		var r document.BoldResult
		var err error
		if close {
			var active document.BoldSpan
			var ok bool
			if attribute == document.BoldAttribute {
				active, ok = h.ActiveBold(d)
			} else {
				active, ok = h.ActiveUnderline(d)
			}
			if !ok {
				t.Fatal("active exact owner lost")
			}
			r, err = d.CloseEverydayFormat(c, active, attribute)
		} else {
			r, err = d.BeginEverydayFormat(c, attribute)
		}
		if err != nil {
			t.Fatal(err)
		}
		if _, err := h.AfterBold(r); err == nil {
			t.Fatal("everyday receipt accepted by legacy adopter")
		}
		h, err = h.AfterEverydayFormat(r)
		if err != nil || !h.Qualified() || h.Count() != 1 {
			t.Fatalf("toggle lost prior history: %v", err)
		}
		d, c = r.Document(), r.Cursor()
	}
	typeASCII := func(s string) {
		t.Helper()
		r, err := d.InsertASCII(c, []byte(s))
		if err != nil {
			t.Fatal(err)
		}
		h, err = h.AfterEverydayEdit(r)
		if err != nil {
			t.Fatal(err)
		}
		d, c = r.Document, r.Cursor
	}
	format(document.BoldAttribute, false)
	typeASCII("BOLD")
	format(document.UnderlineAttribute, false)
	typeASCII("BOTH")
	format(document.BoldAttribute, true)
	typeASCII("UNDER")
	format(document.UnderlineAttribute, true)
	typeASCII(" plain")
	want := cat([]byte{0xc3, 0x0c, 0xc3}, []byte("BOLD"), underlineOn, []byte("BOTH"),
		[]byte{0xc4, 0x0c, 0xc4}, []byte("UNDER"), underlineOf, []byte(" plain"))
	proofExact(t, d, everydayNative(t, want))
	everydayEntry(t, h, 0, []byte("X"), 1)
}

func TestEverydayMotionSeparatesBackspaceGroups(t *testing.T) {
	d := proofParse(t, everydayNative(t, []byte("ABCDEF")))
	f := everydayDelete(t, d, everydayHistory(t, d), 6, document.Backspace)
	h, err := f.History().Separate(document.EverydayMotionBoundary)
	if err != nil {
		t.Fatal(err)
	}
	e := everydayDelete(t, f.Document(), h, 5, document.Backspace)
	everydayEntry(t, e.History(), 0, []byte("E"), 1)
	everydayEntry(t, e.History(), 1, []byte("F"), 1)
}

func TestEverydayRefusesForeignFormatAndLegacyUnknownHistory(t *testing.T) {
	raw := everydayNative(t, []byte("XY"))
	d, foreign := proofParse(t, raw), proofParse(t, raw)
	h := everydayHistory(t, d)
	open, err := d.BeginEverydayFormat(proofCursor(t, d, 0), document.BoldAttribute)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := everydayHistory(t, foreign).AfterEverydayFormat(open); err == nil {
		t.Fatal("foreign history accepted format receipt")
	}
	legacy, err := d.BeginBold(proofCursor(t, d, 2))
	if err != nil {
		t.Fatal(err)
	}
	if _, err := h.AfterEverydayFormat(legacy); err == nil {
		t.Fatal("legacy receipt accepted as everyday format")
	}
	unqualified, err := h.AfterBold(legacy)
	if err != nil {
		t.Fatal(err)
	}
	r, err := legacy.Document().BeginEverydayFormat(legacy.Cursor(), document.UnderlineAttribute)
	if err != nil {
		t.Fatal(err)
	}
	next, err := unqualified.AfterEverydayFormat(r)
	if err == nil || next.Qualified() || next.Revision() != unqualified.Revision() {
		t.Fatal("unknown legacy history was qualified")
	}
	if del, err := legacy.Document().DeleteEveryday(legacy.Cursor(), document.ForwardDelete, unqualified); err == nil || del.Applied() {
		t.Fatal("unqualified history authorized everyday deletion")
	}
}

func TestEverydayFormatRetainsExactAnchorAcrossDeletionRestoreAndSave(t *testing.T) {
	d := proofParse(t, everydayNative(t, []byte("X")))
	del := everydayDelete(t, d, everydayHistory(t, d), 0, document.ForwardDelete)
	d, h := del.Document(), del.History()
	open, err := d.BeginEverydayFormat(del.Cursor(), document.BoldAttribute)
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterEverydayFormat(open)
	if err != nil {
		t.Fatal(err)
	}
	active, ok := h.ActiveBold(open.Document())
	if !ok {
		t.Fatal("missing active receipt")
	}
	typed, err := open.Document().InsertASCII(open.Cursor(), []byte("BOLD"))
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterEverydayEdit(typed)
	if err != nil {
		t.Fatal(err)
	}
	back := everydayDelete(t, typed.Document, h, typed.Cursor.Gap(), document.Backspace)
	p, err := back.History().Open(back.Cursor())
	if err != nil {
		t.Fatal(err)
	}
	restored, err := back.Document().Restore(back.History(), p)
	if err != nil {
		t.Fatal(err)
	}
	d = restored.Document()
	h, err = restored.History().Separate(document.SavedBoundary)
	if err != nil {
		t.Fatal(err)
	}
	if wrong, err := d.CloseEverydayFormat(restored.Cursor(), active, document.BoldAttribute); err == nil || wrong.Changed() {
		t.Fatal("stale format span accepted")
	}
	active, ok = h.ActiveBold(d)
	if !ok {
		t.Fatal("active format lost during deletion/restore/save")
	}
	close, err := d.CloseEverydayFormat(restored.Cursor(), active, document.BoldAttribute)
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterEverydayFormat(close)
	if err != nil || h.Count() != 2 {
		t.Fatalf("close after save: %v", err)
	}
	if stale, err := h.AfterEverydayFormat(close); err == nil || stale.Revision() != h.Revision() {
		t.Fatal("consumed close receipt accepted")
	}
	everydayEntry(t, h, 0, []byte("D"), 1)
	everydayEntry(t, h, 1, []byte("X"), 1)
	proofExact(t, close.Document(), everydayNative(t, cat(
		[]byte{0xc3, 0x0c, 0xc3}, []byte("BOLD"), []byte{0xc4, 0x0c, 0xc4})))
}

func TestEverydayBlockRefusesPartialAttributeAndAcceptsWholeOwners(t *testing.T) {
	body := cat([]byte("Q"), underlineOn, []byte("ONE"), underlineOf, everydayTab5, []byte("END"))
	d := proofParse(t, everydayNative(t, body))
	h := everydayHistory(t, d)
	c := func(gap int) document.Cursor { return proofCursor(t, d, gap) }
	if r, err := d.DeleteEverydayBlock(c(5), c(1), c(5), h); err == nil || r.Pending() {
		t.Fatal("block split an original attribute pair")
	}
	r, err := d.DeleteEverydayBlock(c(6), c(7), c(1), h)
	if err != nil {
		t.Fatal(err)
	}
	yes, err := d.AnswerDeletion(h, r, document.Yes)
	if err != nil {
		t.Fatal(err)
	}
	proofExact(t, yes.Document(), everydayNative(t, []byte("QEND")))
	everydayEntry(t, yes.History(), 0, body[1:len(body)-3], 1)
}

func TestEverydayLoadedPairDeletionOriginalHistoryAndExactBytes(t *testing.T) {
	// Fresh 03/09/92 pair-history repeat deletes T, then removes only the
	// Bold pair in Reveal. F1 still previews the lone earlier T.
	source := proofFixture(t, "proof-pages", "BEFORE.WP")
	const digest = "23f2dbe7c2857709510c02787c518d7a8c9701112fb8f4b46cc2bb170ebc246e"
	if got := fmt.Sprintf("%x", sha256.Sum256(source)); got != digest {
		t.Fatalf("original fixture SHA-256 %s, want %s", got, digest)
	}
	d := proofParse(t, source)
	prior := everydayDelete(t, d, everydayHistory(t, d), 0, document.ForwardDelete)
	d, h := prior.Document(), prior.History()
	c := proofCursor(t, d, 3)
	for _, reveal := range []bool{false, true} {
		r, err := d.DeleteEveryday(c.WithReveal(reveal), document.ForwardDelete, h)
		if err != nil {
			t.Fatal(err)
		}
		if !reveal {
			if !r.Pending() || r.Prompt() != "Delete [BOLD]? No (Yes)" {
				t.Fatalf("opening question: %q", r.Prompt())
			}
			no, err := d.AnswerDeletion(h, r, document.No)
			if err != nil || no.Pending() || no.Applied() || no.History().Count() != 1 {
				t.Fatalf("default No lost original history: %v", err)
			}
			exact(t, no.Document(), mustEverydayExport(t, d))
			if stale, err := d.AnswerDeletion(no.History(), r, document.Yes); err == nil || stale.Applied() {
				t.Fatal("declined pair question remained authoritative")
			}
			foreign := proofParse(t, mustEverydayExport(t, d))
			if wrong, err := foreign.AnswerDeletion(everydayHistory(t, foreign), r, document.Yes); err == nil || wrong.Applied() {
				t.Fatal("foreign pair question accepted")
			}
			r, err = d.AnswerDeletion(h, r, document.Yes)
			if err != nil {
				t.Fatal(err)
			}
		}
		if !r.Applied() || r.Kind() != document.PairDeletion || r.Cursor().Gap() != 3 || r.History().Count() != 1 {
			t.Fatal("pair result lost original caret or history")
		}
		// Same body as stopped DOS RET92.WP (SHA-256 8f30a298...).
		proofExact(t, r.Document(), cat(source[:324], source[325:328], source[331:335], source[338:]))
		everydayEntry(t, r.History(), 0, []byte("T"), 1)
	}
}

func TestEverydayUnderlinePairQuestionAndIndependentActiveBold(t *testing.T) {
	d := proofParse(t, everydayNative(t, cat(underlineOn, []byte("UNDER"), underlineOf)))
	h := everydayHistory(t, d)
	bold, err := d.BeginEverydayFormat(proofCursor(t, d, d.TokenCount()), document.BoldAttribute)
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterEverydayFormat(bold)
	if err != nil {
		t.Fatal(err)
	}
	r, err := bold.Document().InsertASCII(bold.Cursor(), []byte("BOLD"))
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterEverydayEdit(r)
	if err != nil {
		t.Fatal(err)
	}
	d = r.Document
	for _, tc := range []struct {
		gap    int
		prompt string
	}{{0, "Delete [UND]? No (Yes)"}, {6, "Delete [und]? No (Yes)"}} {
		q, err := d.DeleteEveryday(proofCursor(t, d, tc.gap), document.ForwardDelete, h)
		if err != nil || q.Prompt() != tc.prompt {
			t.Fatalf("Underline pair prompt: %q, %v", q.Prompt(), err)
		}
		yes, err := d.AnswerDeletion(h, q, document.Yes)
		if err != nil {
			t.Fatal(err)
		}
		active, ok := yes.History().ActiveBold(yes.Document())
		if !ok {
			t.Fatal("pair removal dropped the independent Bold anchor")
		}
		at := proofCursor(t, yes.Document(), yes.Document().TokenCount()-1)
		close, err := yes.Document().CloseEverydayFormat(at, active, document.BoldAttribute)
		if err != nil {
			t.Fatal(err)
		}
		if _, err := yes.History().AfterEverydayFormat(close); err != nil {
			t.Fatal(err)
		}
		proofExact(t, close.Document(), everydayNative(t, cat([]byte("UNDER"),
			[]byte{0xc3, 0x0c, 0xc3}, []byte("BOLD"), []byte{0xc4, 0x0c, 0xc4})))
	}
}

func TestEverydayTrailingDSRtBackspaceConservesNativeGroup(t *testing.T) {
	// 03/09/92: Z is erased, then the derived trailing DSRt is removed.
	// The third Backspace erases Y into Z's group, with no DSRt in Undelete.
	line := cat(bytes.Repeat([]byte("X"), 64), []byte("Y"))
	d := proofParse(t, everydayNative(t, cat([]byte("Q"), line, []byte{0x90, 'Z'})))
	prior := everydayDelete(t, d, everydayHistory(t, d), 0, document.ForwardDelete)
	z := everydayDelete(t, prior.Document(), prior.History(), 67, document.Backspace)
	proofExact(t, z.Document(), everydayNative(t, cat(line, []byte{0x90})))
	if z.Cursor().Gap() != 66 {
		t.Fatalf("Z removal lost original second-row caret: %d", z.Cursor().Gap())
	}
	wrap := everydayDelete(t, z.Document(), z.History(), z.Cursor().Gap(), document.Backspace)
	proofExact(t, wrap.Document(), everydayNative(t, line))
	if wrap.Cursor().Gap() != 65 || wrap.History().Count() != 2 {
		t.Fatal("DSRt removal changed the stack or lost the end-of-row caret")
	}
	everydayEntry(t, wrap.History(), 0, []byte("Z"), 1)
	everydayEntry(t, wrap.History(), 1, []byte("Q"), 1)
	y := everydayDelete(t, wrap.Document(), wrap.History(), wrap.Cursor().Gap(), document.Backspace)
	proofExact(t, y.Document(), everydayNative(t, line[:64]))
	everydayEntry(t, y.History(), 0, []byte("YZ"), 2)
	everydayEntry(t, y.History(), 1, []byte("Q"), 1)

	if r, err := z.Document().DeleteEveryday(proofCursor(t, z.Document(), 65), document.ForwardDelete, z.History()); err == nil || r.Applied() {
		t.Fatal("unobserved trailing forward-delete accepted")
	}
	if r, err := prior.Document().DeleteEveryday(proofCursor(t, prior.Document(), 66), document.Backspace, prior.History()); err == nil || r.Applied() {
		t.Fatal("nontrailing DSRt erased")
	}
	short := proofParse(t, everydayNative(t, []byte{'X', 0x90}))
	if r, err := short.DeleteEveryday(proofCursor(t, short, 2), document.Backspace, everydayHistory(t, short)); err == nil || r.Applied() {
		t.Fatal("unqualified short-row DSRt erased")
	}
}

func TestEverydayPairRemovalKeepsOverlappingActiveAttribute(t *testing.T) {
	on, off := []byte{0xc3, 0x0c, 0xc3}, []byte{0xc4, 0x0c, 0xc4}
	d := proofParse(t, everydayNative(t, cat(on, []byte("BOLD"), off)))
	h := everydayHistory(t, d)
	under, err := d.BeginEverydayFormat(proofCursor(t, d, 5), document.UnderlineAttribute)
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterEverydayFormat(under)
	if err != nil {
		t.Fatal(err)
	}
	r, err := under.Document().InsertASCII(under.Cursor(), []byte("BOTH"))
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterEverydayEdit(r)
	if err != nil {
		t.Fatal(err)
	}
	removed, err := r.Document.DeleteEveryday(proofCursor(t, r.Document, 0).WithReveal(true), document.ForwardDelete, h)
	if err != nil {
		t.Fatal(err)
	}
	d, h = removed.Document(), removed.History()
	active, ok := h.ActiveUnderline(d)
	if !ok {
		t.Fatal("overlapping active Underline was lost")
	}
	close, err := d.CloseEverydayFormat(proofCursor(t, d, d.TokenCount()-1), active, document.UnderlineAttribute)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := h.AfterEverydayFormat(close); err != nil {
		t.Fatal(err)
	}
	proofExact(t, close.Document(), everydayNative(t, cat([]byte("BOLD"), underlineOn, []byte("BOTH"), underlineOf)))
}
