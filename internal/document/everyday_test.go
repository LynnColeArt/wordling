package document_test

import (
	"bytes"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

// Observed everyday native shapes (WP78 r2/r3 EVERY.WP, REPORT.md):
// soft return 0D, hard return 0A, hard page 0C, attribute ON C3 <type> C3 and
// OFF C4 <type> C4 with type 0C Bold and 0E Underline, and the 9-byte Tab owner.
// The bodies below are synthetic substitutions over the real qualified prefix,
// used to exercise the API — never as an oracle for original output.
var (
	boldOn      = []byte{0xc3, 0x0c, 0xc3}
	boldOff     = []byte{0xc4, 0x0c, 0xc4}
	underlineOn = []byte{0xc3, 0x0e, 0xc3}
	underlineOf = []byte{0xc4, 0x0e, 0xc4}
	observedTab = []byte{0xc1, 0x02, 0x08, 0x07, 0x08, 0x07, 0x0f, 0x00, 0xc1}
)

func cat(a ...[]byte) []byte { return bytes.Join(a, nil) }

func TestEverydayCodesAdmittedAndLabelled(t *testing.T) {
	body := cat([]byte("AB"), underlineOn, []byte("UN"), underlineOf, []byte{0x0d},
		observedTab, []byte("CD"), []byte{0x0a}, []byte{0x0c})
	raw := synthetic(t, body)
	d, e := document.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	if e := d.CheckMutation(); e != nil {
		t.Fatalf("everyday body refused: %v", e)
	}
	exact(t, d, raw)

	kinds := []document.Kind{
		document.ASCII, document.ASCII,
		document.UnderlineOn, document.ASCII, document.ASCII, document.UnderlineOff,
		document.SoftReturn, document.Tab,
		document.ASCII, document.ASCII,
		document.HardReturn, document.HardPage,
	}
	if d.TokenCount() != len(kinds) {
		t.Fatalf("token count %d, want %d", d.TokenCount(), len(kinds))
	}
	for i, want := range kinds {
		tok, e := d.Token(i)
		if e != nil {
			t.Fatal(e)
		}
		if tok.Kind != want {
			t.Fatalf("token %d kind %d, want %d", i, tok.Kind, want)
		}
	}
	// The Tab owner is retained whole: nine native bytes, never split.
	tab, _ := d.Token(7)
	if tab.Span.Length != 9 || !bytes.Equal(tab.Raw, observedTab) {
		t.Fatalf("tab owner %v", tab)
	}

	// One label source feeds both views, and Reveal never becomes serializer input.
	c, _ := d.CursorAt(0)
	normal, e := c.Present(0, d.TokenCount())
	if e != nil {
		t.Fatal(e)
	}
	reveal, e := c.WithReveal(true).Present(0, d.TokenCount())
	if e != nil {
		t.Fatal(e)
	}
	wantNormal := []string{"A", "B", "", "U", "N", "", "\n", "\t", "C", "D", "\n", ""}
	wantReveal := []string{"A", "B", "[UND]", "U", "N", "[und]", "[SRt]", "[Tab]", "C", "D", "[HRt]", "[HPg]"}
	for i := range wantNormal {
		if normal.Elements[i].Text != wantNormal[i] {
			t.Fatalf("normal %d = %q, want %q", i, normal.Elements[i].Text, wantNormal[i])
		}
		if reveal.Elements[i].Text != wantReveal[i] {
			t.Fatalf("reveal %d = %q, want %q", i, reveal.Elements[i].Text, wantReveal[i])
		}
	}
	insp, e := document.InspectRevealCatalogue(d, d.Revision(), 0, d.TokenCount())
	if e != nil {
		t.Fatal(e)
	}
	for i := range wantReveal {
		if insp.Elements[i].Text != wantReveal[i] || insp.Elements[i].TokenIndex != i {
			t.Fatalf("catalogue %d = %v", i, insp.Elements[i])
		}
	}
	// Movement now crosses the everyday owners instead of refusing them.
	for gap := 0; gap < d.TokenCount(); gap++ {
		next, e := c.Move(1)
		if e != nil || next.Gap() != gap+1 {
			t.Fatalf("forward move at %d: %v", gap, e)
		}
		if back, e := next.Move(-1); e != nil || back.Gap() != gap {
			t.Fatalf("backward move at %d: %v", gap, e)
		}
		c = next
	}
	// Export stays byte-exact: neither view normalized the source.
	exact(t, d, raw)
}

func TestEverydayAttributeRefusalsRetained(t *testing.T) {
	for name, body := range map[string][]byte{
		"duplicate underline on":  cat([]byte("A"), underlineOn, underlineOn, []byte("B"), underlineOf, underlineOf),
		"unmatched underline off": cat([]byte("A"), underlineOf),
		"unterminated underline":  cat([]byte("A"), underlineOn, []byte("BC")),
		"duplicate bold on":       cat([]byte("A"), boldOn, boldOn, []byte("B"), boldOff, boldOff),
		"unmatched bold off":      cat([]byte("A"), boldOff),
	} {
		raw := synthetic(t, body)
		d, e := document.Parse(raw)
		if e != nil {
			t.Fatalf("%s: parse %v", name, e)
		}
		if e := d.CheckMutation(); e == nil {
			t.Fatalf("%s admitted", name)
		}
		c, _ := d.CursorAt(0)
		r, e := d.InsertASCII(c, []byte("X"))
		if e == nil || r.Document != d || r.Cursor != c {
			t.Fatalf("%s mutated", name)
		}
		exact(t, d, raw)
	}
}

func TestNestedAndRepeatedPairsAdmitted(t *testing.T) {
	// Bold inside Underline, and three sequential Bold pairs: the former
	// two-pair ceiling and flat attribute state were WP23 policies, not format
	// limits, and the original stores both shapes.
	body := cat(boldOn, underlineOn, []byte("NEST"), underlineOf, boldOff,
		boldOn, []byte("1"), boldOff, boldOn, []byte("2"), boldOff,
		boldOn, []byte("3"), boldOff, []byte("end"))
	raw := synthetic(t, body)
	d, e := document.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	if e := d.CheckMutation(); e != nil {
		t.Fatalf("nested/repeated attributes refused: %v", e)
	}
	exact(t, d, raw)
}

func TestUnnamedTabShapeStaysOpaque(t *testing.T) {
	// Same outer C1 width, different interior. The observed field bytes are
	// evidence, not constants, so the owner is left unnamed rather than labelled
	// Tab on a guess — and unnamed means mutation refuses it.
	tab := bytes.Clone(observedTab)
	tab[1] = 0x03
	raw := synthetic(t, cat([]byte("A"), tab))
	d, e := document.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	tok, e := d.Token(1)
	if e != nil {
		t.Fatal(e)
	}
	if tok.Kind != document.Opaque || tok.Span.Length != 9 {
		t.Fatalf("unnamed tab %v", tok)
	}
	if e := d.CheckMutation(); e == nil {
		t.Fatal("unnamed C1 payload admitted")
	}
	exact(t, d, raw)
}

func TestEverydayReturnAndTabLifecycle(t *testing.T) {
	// Loaded, then saved by two successful edits. The result remains an exact
	// WP51 body revision, not a private container.
	body := cat([]byte("AB"), observedTab, []byte("CD"), []byte{0x0a})
	raw := synthetic(t, body)
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	if err := d.CheckMutation(); err != nil {
		t.Fatal(err)
	}
	c, _ := d.CursorAt(2)
	r, err := d.InsertSoftReturn(c)
	if err != nil || !r.Changed || r.Cursor.Gap() != 3 {
		t.Fatal("soft return insertion", err)
	}
	loaded := r.Document
	if got := mustExport(t, loaded); !bytes.Equal(got[324:], cat([]byte("AB"), []byte{0x0d}, observedTab, []byte("CD"), []byte{0x0a})) {
		t.Fatal("soft return was not inserted byte-exactly")
	}
	c, _ = loaded.CursorAt(r.Cursor.Gap())
	r, err = loaded.InsertTab(c, observedTab)
	if err != nil || !r.Changed || r.Cursor.Gap() != 4 {
		t.Fatal("tab insertion", err)
	}
	saved := r.Document
	tok, _ := saved.Token(3)
	if tok.Kind != document.Tab || tok.Span.Length != len(observedTab) || !bytes.Equal(tok.Raw, observedTab) {
		t.Fatalf("saved tab %v", tok)
	}
	tok, _ = saved.Token(4)
	if tok.Kind != document.Tab || tok.Span.Length != len(observedTab) || !bytes.Equal(tok.Raw, observedTab) {
		t.Fatalf("saved second tab %v", tok)
	}
	c, _ = saved.CursorAt(6)
	over, err := saved.InsertHardReturn(c)
	if err != nil || !over.Changed || over.Cursor.Gap() != 7 {
		t.Fatal("hard return through saved everyday body", err)
	}
	exact(t, d, raw)
}

func mustExport(t testing.TB, d *document.Document) []byte {
	t.Helper()
	got, err := d.Export()
	if err != nil {
		t.Fatal(err)
	}
	return got
}

func TestEverydayReflowConservesNativeOwnersAndIdentity(t *testing.T) {
	body := cat([]byte("A BCD"), observedTab, underlineOn, []byte("U"), underlineOf, []byte{0x0a}, []byte("tail"))
	d, err := document.Parse(synthetic(t, body))
	if err != nil {
		t.Fatal(err)
	}
	c, _ := d.CursorAt(10)
	h, _ := document.NewHistory(d)
	changes := []document.ReflowChange{
		{At: 1, Kind: document.WrapSpace},
		{At: 3, Kind: document.InsertDeletedSoftReturn},
		{At: 9, Kind: document.PromoteHardReturn, Page: 1},
	}
	plan, err := document.NewReflowPlan(d, changes)
	if err != nil {
		t.Fatal(err)
	}
	changes[0].At = 0 // The published plan cannot be changed by its input slice.
	edit, err := d.AdoptReflow(c, plan)
	if err != nil {
		t.Fatal(err)
	}
	if !edit.Changed || edit.Cursor.Gap() != 13 {
		t.Fatalf("changed=%v caret=%d", edit.Changed, edit.Cursor.Gap())
	}
	nextHistory, err := h.AfterReflow(edit)
	if err != nil || !nextHistory.Qualified() {
		t.Fatalf("history adoption: %v", err)
	}
	if _, err := h.AfterRetrieval(edit); err == nil {
		t.Fatal("reflow receipt accepted as retrieval")
	}
	for i, want := range []document.Kind{document.EndOfPage, document.HardReturnSoftPage, document.DormantHardReturn} {
		token, _ := edit.Document.Token(10 + i)
		if token.Kind != want {
			t.Fatalf("page owner %d: %v", i, token.Kind)
		}
	}
	if _, err := edit.Document.AdoptReflow(edit.Cursor, plan); err == nil {
		t.Fatal("stale plan accepted")
	}
	foreign, _ := document.Parse(synthetic(t, body))
	other, _ := foreign.CursorAt(c.Gap())
	if _, err := foreign.AdoptReflow(other, plan); err == nil {
		t.Fatal("equal bytes from a foreign revision accepted")
	}
	overlap, _ := document.NewReflowPlan(edit.Document, []document.ReflowChange{
		{At: 10, Kind: document.DemoteSoftPage}, {At: 11, Kind: document.RemoveDeletedSoftReturn},
	})
	if result, err := edit.Document.AdoptReflow(edit.Cursor, overlap); err == nil || result.Document.Revision() != edit.Document.Revision() {
		t.Fatalf("overlapping owner plan changed the input: %v", err)
	}
	bad, _ := document.NewReflowPlan(d, []document.ReflowChange{{At: 0, Kind: document.WrapSpace}})
	if result, err := d.AdoptReflow(c, bad); err == nil || result.Document.Revision() != d.Revision() {
		t.Fatalf("non-space plan changed the input: %v", err)
	}
	reverse, _ := document.NewReflowPlan(edit.Document, []document.ReflowChange{
		{At: 1, Kind: document.UnwrapSpace}, {At: 3, Kind: document.RemoveDeletedSoftReturn},
		{At: 10, Kind: document.DemoteSoftPage},
	})
	restored, err := edit.Document.AdoptReflow(edit.Cursor, reverse)
	if err != nil {
		t.Fatal(err)
	}
	if got := everydayBody(t, restored.Document); !bytes.Equal(got, body) || restored.Cursor.Gap() != c.Gap() {
		t.Fatalf("reversed semantic owners %x, gap %d", got, restored.Cursor.Gap())
	}
	noop, _ := document.NewReflowPlan(restored.Document, nil)
	same, err := restored.Document.AdoptReflow(restored.Cursor, noop)
	if err != nil || same.Changed || same.Document.Revision() != restored.Document.Revision() {
		t.Fatalf("empty plan changed identity: %v", err)
	}
}

func everydayBody(t *testing.T, d *document.Document) []byte {
	t.Helper()
	var body []byte
	for i := 0; i < d.TokenCount(); i++ {
		tok, err := d.Token(i)
		if err != nil {
			t.Fatal(err)
		}
		body = append(body, tok.Raw...)
	}
	return body
}

func TestEverydayOccupiedRetrieveKeepsPrefixAndHistory(t *testing.T) {
	raw := synthetic(t, []byte("Xleft-right"))
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	c, _ := d.CursorAt(0)
	h, _ := document.NewHistory(d)
	deleted, err := d.Delete(c, document.ForwardDelete, h)
	if err != nil {
		t.Fatal(err)
	}
	d = deleted.Document()
	h = deleted.History()
	c, _ = d.CursorAt(4)
	srcBody := cat(underlineOn, []byte("qu"), []byte{0x90}, []byte("ick"), underlineOf,
		[]byte{0x0d}, observedTab, []byte("fox\n"), []byte{0x0c})
	src, err := document.Parse(synthetic(t, srcBody))
	if err != nil {
		t.Fatal(err)
	}
	edit, err := d.InsertDocument(c, src)
	if err != nil {
		t.Fatal(err)
	}
	wanted := cat([]byte("left"), underlineOn, []byte("quick"), underlineOf,
		[]byte{' '}, observedTab, []byte("fox\n"), []byte{0x0c}, []byte("-right"))
	if got := everydayBody(t, edit.Document); !bytes.Equal(got, wanted) || edit.Cursor.Gap() != 18 {
		t.Fatalf("inserted body %x, gap %d", got, edit.Cursor.Gap())
	}
	if !bytes.Equal(everydayBody(t, src), srcBody) {
		t.Fatal("source changed")
	}
	birth, _ := edit.Document.OriginalExport()
	if !bytes.Equal(birth, raw) {
		t.Fatal("receiver provenance lost")
	}
	h, err = h.AfterRetrieval(edit)
	if err != nil || !h.Qualified() {
		t.Fatalf("insert history: %v", err)
	}
	item, err := h.Entry(0)
	if err != nil || string(item.Native) != "X" {
		t.Fatalf("existing history lost: %+v %v", item, err)
	}
	typed, err := edit.Document.TypeoverASCII(edit.Cursor, []byte("!"))
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterEverydayEdit(typed)
	if err != nil || !h.Qualified() {
		t.Fatalf("ordinary typeover disabled prior history: %v", err)
	}
	item, err = h.Entry(0)
	if err != nil || string(item.Native) != "X" {
		t.Fatalf("existing history lost after typeover: %+v %v", item, err)
	}
	bad, err := document.Parse(synthetic(t, []byte{0x8c, 'x'}))
	if err != nil {
		t.Fatal(err)
	}
	if result, err := d.InsertDocument(c, bad); err == nil || result.Document.Revision() != d.Revision() {
		t.Fatalf("unpaired page owner changed the receiver: %v", err)
	}
}

func TestEverydayActiveUnderlineSurvivesReflowAndInsertion(t *testing.T) {
	d, err := document.Parse(synthetic(t, []byte("a b")))
	if err != nil {
		t.Fatal(err)
	}
	h, _ := document.NewHistory(d)
	c, _ := d.CursorAt(3)
	on, err := d.BeginUnderline(c)
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterUnderline(on)
	if err != nil {
		t.Fatal(err)
	}
	source, _ := document.Parse(synthetic(t, []byte("text")))
	edit, err := on.Document().InsertDocument(on.Cursor(), source)
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterRetrieval(edit)
	if err != nil {
		t.Fatal(err)
	}
	plan, _ := document.NewReflowPlan(edit.Document, []document.ReflowChange{{At: 1, Kind: document.WrapSpace}})
	reflow, err := edit.Document.AdoptReflow(edit.Cursor, plan)
	if err != nil {
		t.Fatal(err)
	}
	h, err = h.AfterReflow(reflow)
	if err != nil {
		t.Fatal(err)
	}
	active, ok := h.ActiveUnderline(reflow.Document)
	if !ok {
		t.Fatal("underline lost after checked edits")
	}
	if _, err := reflow.Document.CloseUnderline(reflow.Cursor, active); err != nil {
		t.Fatalf("remapped underline cannot close: %v", err)
	}
}

func TestEverydayRetrieveFastSaveSourceIntoAdmittedReceiver(t *testing.T) {
	const reference = "../../docs/research/everyday-contract-2026-11-05/"
	read := func(path string) (*document.Document, []byte) {
		t.Helper()
		raw, err := os.ReadFile(reference + path)
		if err != nil {
			t.Fatal(err)
		}
		d, err := document.Parse(raw)
		if err != nil {
			t.Fatal(err)
		}
		return d, raw
	}
	target, targetRaw := read("r3/EVERY.WP")
	source, sourceRaw := read("qualification/flow/exports/FLOW.WP")
	category(t, source.CheckMutation(), document.UnsupportedPrefix)
	c, _ := target.CursorAt(target.TokenCount())
	edit, err := target.InsertDocument(c, source)
	if err != nil {
		t.Fatal(err)
	}
	got, err := edit.Document.Export()
	if err != nil {
		t.Fatal(err)
	}
	// The receiver keeps its original prefix. Only the qualified document
	// formatting flag may change, never the source's deleted/slack extents.
	expectedPrefix := bytes.Clone(targetRaw[:324])
	expectedPrefix[256] |= 8
	if !bytes.Equal(got[:324], expectedPrefix) || !bytes.Equal(got[324:len(targetRaw)], targetRaw[324:]) {
		t.Fatal("retrieval replaced receiver prefix or existing body")
	}
	if !bytes.Contains(got[len(targetRaw):], []byte("LAST PAGE alpha EDIT MORE")) {
		t.Fatal("missing original three-page fragment")
	}
	exact(t, source, sourceRaw)
}

func TestEverydayHistoryPreviewPreservesWideOwners(t *testing.T) {
	native := cat(underlineOn, observedTab, []byte("X"), underlineOf)
	d, err := document.Parse(synthetic(t, native))
	if err != nil {
		t.Fatal(err)
	}
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	a, _ := d.CursorAt(0)
	z, _ := d.CursorAt(d.TokenCount())
	question, err := d.DeleteBlock(a.WithReveal(true), z.WithReveal(true), h)
	if err != nil {
		t.Fatal(err)
	}
	deleted, err := d.AnswerDeletion(h, question, document.Yes)
	if err != nil {
		t.Fatal(err)
	}
	preview, err := deleted.History().Open(deleted.Cursor())
	if err != nil {
		t.Fatal(err)
	}
	overlay, err := preview.Present(0, 4, true)
	if err != nil {
		t.Fatal(err)
	}
	for i, want := range [][]byte{underlineOn, observedTab, []byte("X"), underlineOf} {
		if !bytes.Equal(overlay.Elements[i].Raw, want) {
			t.Fatalf("fragment owner %d = %x; want %x", i, overlay.Elements[i].Raw, want)
		}
	}
	restored, err := deleted.Document().Restore(deleted.History(), preview)
	if err != nil || !bytes.Equal(everydayBody(t, restored.Document()), native) {
		t.Fatalf("restore changed fragment: %v", err)
	}
}
