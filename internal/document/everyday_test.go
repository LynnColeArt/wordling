package document_test

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
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

// The stopped 03/09/92 edge exports use the identical original EVERY.WP
// prefix. Reconstructing and checking their entire native image SHA binds the
// test to the captured file without distributing a separate duplicate fixture.
func capturedEverydayEdge(t *testing.T, body []byte, hash string) []byte {
	t.Helper()
	base, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/r3/EVERY.WP")
	if err != nil {
		t.Fatal(err)
	}
	raw := append(bytes.Clone(base[:324]), body...)
	got := sha256.Sum256(raw)
	if hex.EncodeToString(got[:]) != hash {
		t.Fatalf("capture identity mismatch: %x", got)
	}
	return raw
}

func TestEverydayReflowOriginalTabEdge(t *testing.T) {
	tab := []byte{0xc1, 2, 0x28, 0x23, 0x28, 0x23, 0x4b, 0, 0xc1}
	before := cat(bytes.Repeat([]byte("X"), 63), tab)
	captured := capturedEverydayEdge(t, cat(before, []byte{0x90, 'Y'}),
		"426c12a60c6a53ead446cd2a554fbb3f687dc6a829506f2a91348b9ecab7ac99")
	raw := cat(captured[:324], before, []byte("Y"))
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	c, _ := d.CursorAt(64)
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	plan, err := document.NewReflowPlan(d, []document.ReflowChange{{At: 64, Kind: document.InsertDeletedSoftReturn}})
	if err != nil {
		t.Fatal(err)
	}
	result, err := d.AdoptReflow(c, plan)
	if err != nil {
		t.Fatal(err)
	}
	if result.Cursor.Gap() != 65 {
		t.Fatalf("caret should stay before Y, got gap %d", result.Cursor.Gap())
	}
	h, err = h.AfterReflow(result)
	if err != nil || !h.Qualified() {
		t.Fatalf("Tab edge history: %v", err)
	}
	// Original format housekeeping remains the only expected prefix update.
	exported, _ := result.Document.Export()
	if !bytes.Equal(exported[324:], captured[324:]) {
		t.Fatalf("original tab/DSRt owner bytes changed: %x", exported[387:])
	}
	inverse, _ := document.NewReflowPlan(result.Document, []document.ReflowChange{{At: 64, Kind: document.RemoveDeletedSoftReturn}})
	undo, err := result.Document.AdoptReflow(result.Cursor, inverse)
	if err != nil || !bytes.Equal(everydayBody(t, undo.Document), raw[324:]) || undo.Cursor.Gap() != 64 {
		t.Fatalf("Tab edge did not reverse without text loss: %v", err)
	}
	if _, err = h.AfterReflow(undo); err != nil {
		t.Fatal(err)
	}
	for _, edge := range []int{0, d.TokenCount()} {
		bad, _ := document.NewReflowPlan(d, []document.ReflowChange{{At: edge, Kind: document.InsertDeletedSoftReturn}})
		if out, err := d.AdoptReflow(c, bad); err == nil || out.Document.Revision() != d.Revision() {
			t.Fatalf("unobserved document edge %d accepted: %v", edge, err)
		}
	}
}

func TestEverydayReflowOriginalPageWrapEdges(t *testing.T) {
	record := []byte{
		0xd4, 0, 0x1c, 0, 0, 0x16, 0x68, 0x29, 1, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0x30, 0x2a, 0x30, 0x2a, 0x30, 0x2a, 0xb0, 4, 0xb0, 4, 0x1c, 0, 0, 0xd4,
	}
	for _, tc := range []struct {
		name, hash, text, following, separator, label string
		kind                                          document.ReflowKind
		continuation                                  byte
	}{
		{"unbroken", "d9329e2d9f84df55f042b622e93cc8d9dc6ffaf6d9b7017ba5a77080aad6a710",
			string(bytes.Repeat([]byte("Q"), 65)), "Q", "", "[DSRt]", document.InsertDeletedSoftPage, 0x91},
		{"space", "36fc35c978038bc442b9cdfcbd0e4a8d2237bbb3c65f0761827a77fb78205f61",
			string(bytes.Repeat([]byte("X"), 61)), "alpha", " ", "[SPg]", document.WrapSpaceToPage, 0x0b},
	} {
		t.Run(tc.name, func(t *testing.T) {
			prior := cat(bytes.Repeat([]byte{0x0a}, 53), []byte(tc.text))
			at := len(prior)
			captured := capturedEverydayEdge(t, cat(prior, record, []byte{tc.continuation}, []byte(tc.following)), tc.hash)
			original, err := document.Parse(captured)
			if err != nil {
				t.Fatal(err)
			}
			if err := original.CheckMutation(); err != nil {
				t.Fatal(err)
			}
			plain := cat(prior, []byte(tc.separator+tc.following))
			d, err := document.Parse(cat(captured[:324], plain))
			if err != nil {
				t.Fatal(err)
			}
			c, _ := d.CursorAt(at + len(tc.separator))
			h, _ := document.NewHistory(d)
			plan, err := document.NewReflowPlan(d, []document.ReflowChange{{At: at, Kind: tc.kind, Page: 1}})
			if err != nil {
				t.Fatal(err)
			}
			flow, err := d.AdoptReflow(c, plan)
			if err != nil {
				t.Fatal(err)
			}
			if !bytes.Equal(everydayBody(t, flow.Document), captured[324:]) || flow.Cursor.Gap() != at+2 {
				t.Fatalf("page wrap differs from capture or loses caret: %d", flow.Cursor.Gap())
			}
			h, err = h.AfterReflow(flow)
			if err != nil {
				t.Fatal(err)
			}
			inspection, err := document.InspectRevealCatalogue(flow.Document, flow.Document.Revision(), at, 2)
			if err != nil || inspection.Elements[0].Text != "" || inspection.Elements[1].Text != tc.label {
				t.Fatalf("page Reveal owner label: %+v %v", inspection, err)
			}
			soften, _ := document.NewReflowPlan(flow.Document, []document.ReflowChange{{At: at, Kind: document.SoftenPageBreak}})
			line, err := flow.Document.AdoptReflow(flow.Cursor, soften)
			wantReturn := byte(0x90)
			if tc.continuation == 0x0b {
				wantReturn = 0x0d
			}
			if err != nil || !bytes.Equal(everydayBody(t, line.Document), cat(prior, []byte{wantReturn}, []byte(tc.following))) ||
				line.Cursor.Gap() != at+1 {
				t.Fatalf("page-to-line break changed lexical meaning or caret: %v", err)
			}
			renumber, _ := document.NewReflowPlan(flow.Document, []document.ReflowChange{{At: at, Kind: document.RenumberSoftPage, Page: 2}})
			moved, err := flow.Document.AdoptReflow(flow.Cursor, renumber)
			if err != nil {
				t.Fatal(err)
			}
			want := bytes.Clone(captured[324:])
			want[at+8] = 2
			if !bytes.Equal(everydayBody(t, moved.Document), want) || moved.Cursor.Gap() != flow.Cursor.Gap() {
				t.Fatal("renumber changed a non-page owner")
			}
			h, err = h.AfterReflow(moved)
			if err != nil {
				t.Fatal(err)
			}
			inverse, _ := document.NewReflowPlan(moved.Document, []document.ReflowChange{{At: at, Kind: document.DemoteSoftPage}})
			unwrapped, err := moved.Document.AdoptReflow(moved.Cursor, inverse)
			if err != nil || !bytes.Equal(everydayBody(t, unwrapped.Document), plain) || unwrapped.Cursor.Gap() != c.Gap() {
				t.Fatalf("reverse wrap changed text, space semantics, or caret: %v", err)
			}
			if _, err = h.AfterReflow(unwrapped); err != nil {
				t.Fatal(err)
			}
			for _, bad := range [][]byte{
				cat(prior, []byte{tc.continuation}, []byte(tc.following)),
				cat(prior, record, []byte{0x90}, []byte(tc.following)),
				cat(prior, record, []byte{tc.continuation, 0x99}, []byte(tc.following)),
			} {
				doc, err := document.Parse(cat(captured[:324], bad))
				if err == nil {
					category(t, doc.CheckMutation(), document.UnsupportedBody)
				}
			}
		})
	}
}

func TestEverydayRetrievePreservesOriginalHardPage(t *testing.T) {
	raw, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/qualification/proof-pages/exports/BEFORE.WP")
	if err != nil {
		t.Fatal(err)
	}
	source, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	d, _ := document.Parse(synthetic(t, []byte("prefix ")))
	c, _ := d.CursorAt(d.TokenCount())
	result, err := d.InsertDocument(c, source)
	if err != nil {
		t.Fatal(err)
	}
	body := everydayBody(t, result.Document)
	if !bytes.Contains(body, []byte("here.\x0czorbly")) || bytes.Contains(body, []byte{0xd4}) {
		t.Fatalf("explicit hard page or formatter owner mishandled: %x", body)
	}
	exact(t, source, raw)
}
