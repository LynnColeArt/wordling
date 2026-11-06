package document_test

import (
	"bytes"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

func TestUnderlineAuthoringOnLoadedEverydayRevision(t *testing.T) {
	d, err := document.Parse(synthetic(t, []byte("A")))
	if err != nil {
		t.Fatal(err)
	}
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	c, _ := d.CursorAt(d.TokenCount())
	open, err := d.BeginUnderline(c)
	if err != nil {
		t.Fatal(err)
	}
	if h, err = h.AfterUnderline(open); err != nil || h.Qualified() || h.CountKnown() || h.Count() != 0 {
		t.Fatalf("opened underline: %v %v", err, h)
	}
	underlined := open.Document()
	tok, err := underlined.Token(open.Cursor().Gap())
	if err != nil || tok.Kind != document.UnderlineOff || open.Cursor().Gap() != underlined.TokenCount()-1 {
		t.Fatalf("cursor is not immediately before underline Off: tok=%v cursor=%d", tok, open.Cursor().Gap())
	}
	r, err := underlined.InsertASCII(open.Cursor(), []byte("U"))
	if err != nil || !r.Changed {
		t.Fatal("insert inside underline", err)
	}
	if h, err = h.AfterEdit(r); err != nil {
		t.Fatal(err)
	}
	s, ok := h.ActiveUnderline(r.Document)
	if !ok {
		t.Fatal("missing active underline after insertion")
	}
	closed, err := r.Document.CloseUnderline(r.Cursor, s)
	if err != nil || closed.Changed() || closed.Cursor().Gap() != r.Document.TokenCount() {
		t.Fatalf("underline close: %v", err)
	}
	if h, err = h.AfterUnderline(closed); err != nil || h.Qualified() || h.CountKnown() || h.Count() != 0 {
		t.Fatalf("closed underline: %v %v", err, h)
	}
	if got := mustExport(t, closed.Document()); !bytes.Equal(got[324:], cat([]byte("A"), underlineOn, []byte("U"), underlineOf)) {
		t.Fatalf("underlined body % x", got[324:])
	}
}

func TestOverlappingBoldUnderlineAuthoring(t *testing.T) {
	d, err := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if err != nil {
		t.Fatal(err)
	}
	h, err := document.NewHistory(d)
	if err != nil {
		t.Fatal(err)
	}
	c, _ := d.CursorAt(d.TokenCount())
	under, err := d.BeginUnderline(c)
	if err != nil {
		t.Fatal(err)
	}
	if h, err = h.AfterUnderline(under); err != nil {
		t.Fatal(err)
	}
	d, c = under.Document(), under.Cursor()
	bold, err := d.BeginBold(c)
	if err != nil {
		t.Fatal(err)
	}
	if h, err = h.AfterBold(bold); err != nil {
		t.Fatal(err)
	}
	r, err := bold.Document().InsertASCII(bold.Cursor(), []byte("B"))
	if err != nil || !r.Changed {
		t.Fatal("insert inside nested Bold", err)
	}
	if h, err = h.AfterEdit(r); err != nil {
		t.Fatal(err)
	}
	bs, ok := h.ActiveBold(r.Document)
	if !ok {
		t.Fatal("missing active Bold after insertion")
	}
	bclosed, err := r.Document.CloseBold(r.Cursor, bs)
	if err != nil {
		t.Fatal(err)
	}
	if h, err = h.AfterBold(bclosed); err != nil {
		t.Fatal(err)
	}
	if _, ok := h.ActiveUnderline(r.Document); !ok {
		t.Fatal("missing active Underline before Bold close")
	}
	us, ok := h.ActiveUnderline(bclosed.Document())
	if !ok {
		t.Fatal("active Underline did not survive Bold close")
	}
	closed, err := bclosed.Document().CloseUnderline(bclosed.Cursor(), us)
	if err != nil {
		t.Fatal(err)
	}
	if h, err = h.AfterUnderline(closed); err != nil {
		t.Fatal(err)
	}
	got := mustExport(t, closed.Document())
	want := cat(underlineOn, boldOn, []byte("B"), boldOff, underlineOf)
	if !bytes.Equal(got[324:], want) {
		t.Fatalf("nested body % x; want % x", got[324:], want)
	}
}
