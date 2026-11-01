package document_test

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"errors"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
	"os"
	"path/filepath"
	"reflect"
	"testing"
)

func newDocument(t testing.TB) *document.Document {
	t.Helper()
	d, e := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if e != nil || d == nil {
		t.Fatal(e)
	}
	return d
}
func newOriginalAbsent(t testing.TB, d *document.Document, birth document.Birth) {
	t.Helper()
	raw, e := d.OriginalExport()
	var f *document.Failure
	if raw != nil || !errors.As(e, &f) || f.Category != document.NoLoadedOriginal || d.Birth() != birth || !birth.IsNew() || birth.IsLoaded() {
		t.Fatal("New birth/original changed", e)
	}
}
func TestNewEveryTypedFieldAndOriginalObservation(t *testing.T) {
	d := newDocument(t)
	raw, e := d.Export()
	if e != nil {
		t.Fatal(e)
	}
	var schema struct {
		Fields []struct {
			Owner  string
			Offset int `json:"relative_owner_offset"`
			Width  int
			Hex    string
			Name   string
		}
		Images []struct{ Path string } `json:"eight_first_images"`
	}
	b, e := os.ReadFile("../../docs/research/continuation/native-constructor-design/schema.json")
	if e != nil {
		t.Fatal(e)
	}
	if e = json.Unmarshal(b, &schema); e != nil {
		t.Fatal(e)
	}
	if len(schema.Fields) != 72 {
		t.Fatal("field roster")
	}
	image, e := wp51.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	info := image.Inspect()
	owners := map[string]int{"header": 0}
	for _, p := range info.Packets {
		owners[map[uint16]string{7: "packet-7", 15: "packet-15", 12: "packet-12", 6: "packet-6", 8: "packet-8"}[p.Type]] = p.Data.Offset
	}
	for _, f := range schema.Fields {
		expected, e := hex.DecodeString(f.Hex)
		if e != nil || len(expected) != f.Width {
			t.Fatal(f.Name)
		}
		offset, ok := owners[f.Owner]
		if !ok || !bytes.Equal(raw[offset+f.Offset:offset+f.Offset+f.Width], expected) {
			t.Fatal("field", f.Name)
		}
	}
	if info.Body.Length != 0 || len(info.Blocks) != 2 || len(info.Packets) != 5 || d.TokenCount() != 0 || len(raw) > document.MaxNewPrefixBytes {
		t.Fatal("empty structural extents")
	}
	for _, im := range schema.Images {
		if len(im.Path) > 0 {
			other, e := os.ReadFile("../../" + im.Path)
			if e != nil {
				t.Fatal(e)
			}
			if len(other) == len(raw) && !bytes.Equal(other, raw) {
				t.Fatal("actual empty observation differs", im.Path)
			}
		}
	}
	if e = d.CheckMutation(); e != nil {
		t.Fatal(e)
	}
	c, e := d.CursorAt(0)
	if e != nil {
		t.Fatal(e)
	}
	for _, r := range []bool{false, true} {
		p, e := c.WithReveal(r).Present(0, 0)
		if e != nil || p.CursorGap != 0 || p.Reveal != r || len(p.Elements) != 0 {
			t.Fatal("empty shared gap/view")
		}
	}
	newOriginalAbsent(t, d, d.Birth())
}
func TestNewClosedSelectionIdentityAndOwnedExports(t *testing.T) {
	if reflect.TypeOf(document.NewConfig{}).NumField() != 1 {
		t.Fatal("config surface widened")
	}
	for i := 0; i < 256; i++ {
		if document.SerializationProfile(i) == document.HistoricalUS51DosTextStandardPrinter {
			continue
		}
		d, e := document.New(document.NewConfig{Profile: document.SerializationProfile(i)})
		var f *document.Failure
		if d != nil || !errors.As(e, &f) || f.Category != document.UnsupportedNewProfile {
			t.Fatal(i, e)
		}
	}
	config := document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter}
	d, e := document.New(config)
	if e != nil {
		t.Fatal(e)
	}
	config.Profile = 0
	other := newDocument(t)
	raw, _ := d.Export()
	birth := d.Birth()
	revision := d.Revision()
	c, _ := d.CursorAt(0)
	if birth == other.Birth() || revision == other.Revision() {
		t.Fatal("equal-byte identity conflation")
	}
	copyBytes, _ := d.Export()
	copyBytes[0] = 0
	exact(t, d, raw)
	loaded, e := document.Parse(raw)
	if e != nil || loaded.Birth() == birth || !loaded.Birth().IsLoaded() || loaded.Birth().IsNew() {
		t.Fatal("explicit separate acquisition", e)
	}
	original, e := loaded.OriginalExport()
	if e != nil || !bytes.Equal(original, raw) {
		t.Fatal(e)
	}
	original[0] = 0
	original, _ = loaded.OriginalExport()
	if !bytes.Equal(original, raw) {
		t.Fatal("loaded original alias")
	}
	// A filesystem/source capability is neither required nor faked here: merely
	// copying/publication of Export bytes cannot change this still-live lineage.
	published := bytes.Clone(raw)
	file := filepath.Join(t.TempDir(), "published.WP5")
	if e = os.WriteFile(file, published, 0600); e != nil {
		t.Fatal(e)
	}
	reread, e := os.ReadFile(file)
	if e != nil {
		t.Fatal(e)
	}
	acquired, e := document.Parse(reread)
	if e != nil || !acquired.Birth().IsLoaded() || acquired.Birth() == birth {
		t.Fatal("separate actual exported-byte publication/read", e)
	}
	newOriginalAbsent(t, d, birth)
	published[0] = 0
	newOriginalAbsent(t, d, birth)
	*d = *loaded
	if c.Revision() != revision || birth == d.Birth() || !birth.IsNew() {
		t.Fatal("wrapper retargeted captured state")
	}
	var zero document.Document
	if zero.Birth() != (document.Birth{}) || zero.Birth().IsNew() || zero.Birth().IsLoaded() {
		t.Fatal("zero birth")
	}
}
func TestNewBirthAcrossActualMutationPreviewAndRestore(t *testing.T) {
	d := newDocument(t)
	birth := d.Birth()
	c, _ := d.CursorAt(0)
	initial, _ := d.Export()
	r, e := d.InsertASCII(c, []byte("ABCD"))
	if e != nil {
		t.Fatal(e)
	}
	d, c = r.Document, r.Cursor
	newOriginalAbsent(t, d, birth)
	got, _ := d.Export()
	if len(got) != len(initial)+4 {
		t.Fatal("first real ASCII")
	}
	image, _ := wp51.Parse(got)
	flags := -1
	for _, p := range image.Inspect().Packets {
		if p.Type == 6 {
			flags = p.Data.Offset
		}
	}
	for i, b := range initial {
		want := b
		if i == flags {
			want |= 8
		}
		if got[i] != want {
			t.Fatal("unrelated prefix altered", i)
		}
	}
	h, e := document.NewHistory(d)
	if e != nil {
		t.Fatal(e)
	}
	for _, boundary := range []document.HistoryBoundary{0, document.RightBoundary, document.SavedBoundary} {
		start, _ := d.CursorAt(1)
		history := h
		if boundary != 0 {
			history, e = history.Separate(boundary)
			if e != nil {
				t.Fatal(e)
			}
		}
		deletion, e := d.Delete(start, document.ForwardDelete, history)
		if e != nil || !deletion.Applied() {
			t.Fatal("delete", e)
		}
		next := deletion.Document()
		newOriginalAbsent(t, next, birth)
		preview, e := deletion.History().Open(deletion.Cursor())
		if e != nil {
			t.Fatal(e)
		}
		newOriginalAbsent(t, next, birth)
		restored, e := next.Restore(deletion.History(), preview)
		if e != nil || !restored.Applied() {
			t.Fatal("restore", e)
		}
		newOriginalAbsent(t, restored.Document(), birth)
		out, _ := restored.Document().Export()
		if !bytes.Equal(out, got) {
			t.Fatal("restore bytes")
		}
	}
	same, _ := d.CursorAt(1)
	n, e := d.TypeoverASCII(same, []byte("B"))
	if e != nil || n.Changed || n.Document.Revision() != d.Revision() {
		t.Fatal("same byte no-op", e)
	}
	newOriginalAbsent(t, n.Document, birth)
	noop, e := d.InsertASCII(c, nil)
	if e != nil || noop.Document.Revision() != d.Revision() {
		t.Fatal(e)
	}
	newOriginalAbsent(t, noop.Document, birth)
	other := newDocument(t)
	bad, e := other.InsertASCII(c, []byte("X"))
	var f *document.Failure
	if !errors.As(e, &f) || f.Category != document.RevisionMismatch || bad.Document.Revision() != other.Revision() {
		t.Fatal("cross-state receipt")
	}
	newOriginalAbsent(t, other, other.Birth())
}
func FuzzNewClosedProfile(f *testing.F) {
	f.Add(uint8(1), []byte("AB"))
	f.Add(uint8(0), []byte{0})
	f.Add(uint8(1), []byte{0xff})
	f.Add(uint8(255), []byte("Z"))
	f.Fuzz(func(t *testing.T, p uint8, text []byte) {
		d, e := document.New(document.NewConfig{Profile: document.SerializationProfile(p)})
		if p != 1 {
			if d != nil || e == nil {
				t.Fatal("unsupported profile")
			}
			return
		}
		if e != nil {
			t.Fatal(e)
		}
		before, _ := d.Export()
		birth := d.Birth()
		c, _ := d.CursorAt(0)
		r, e := d.InsertASCII(c, text)
		newOriginalAbsent(t, d, birth)
		exact(t, d, before)
		if e != nil {
			if r.Document.Revision() != d.Revision() {
				t.Fatal("partial publication")
			}
			return
		}
		newOriginalAbsent(t, r.Document, birth)
		out, _ := r.Document.Export()
		loaded, e := document.Parse(out)
		if e != nil || !loaded.Birth().IsLoaded() {
			t.Fatal("real reopen", e)
		}
		original, e := loaded.OriginalExport()
		if e != nil || !bytes.Equal(original, out) {
			t.Fatal("loaded bytes")
		}
	})
}

func FuzzNewBirthHistory(f *testing.F) {
	f.Add([]byte("ABCD"), []byte{0, 0, 4, 5, 1})
	f.Add([]byte("X"), []byte{1, 2, 3, 4})
	f.Add([]byte{}, []byte{0, 5})
	f.Fuzz(func(t *testing.T, text, commands []byte) {
		if len(text) > 128 || len(commands) > 64 {
			return
		}
		for _, b := range text {
			if b < 0x20 || b > 0x7e {
				return
			}
		}
		d := newDocument(t)
		birth := d.Birth()
		c, _ := d.CursorAt(0)
		r, e := d.InsertASCII(c, text)
		if e != nil {
			t.Fatal(e)
		}
		d, c = r.Document, r.Cursor
		h, e := document.NewHistory(d)
		if e != nil {
			t.Fatal(e)
		}
		for _, command := range commands {
			before, _ := d.Export()
			old := d
			switch command % 6 {
			case 0, 1:
				direction := document.ForwardDelete
				if command%6 == 1 {
					direction = document.Backspace
				}
				deletion, e := d.Delete(c, direction, h)
				if e == nil && deletion.Applied() {
					d, c, h = deletion.Document(), deletion.Cursor(), deletion.History()
				}
			case 2, 3:
				var edit document.EditResult
				if command%6 == 2 {
					edit, e = d.TypeoverASCII(c, []byte("X"))
				} else {
					edit, e = d.InsertASCII(c, []byte("Y"))
				}
				if e == nil {
					next, e2 := h.AfterEdit(edit)
					if e2 == nil {
						d, c, h = edit.Document, edit.Cursor, next
					}
				}
			case 4:
				preview, e := h.Open(c)
				if e == nil {
					next, e := h.CancelPreview(preview)
					if e == nil {
						h = next
					}
				}
			case 5:
				preview, e := h.Open(c)
				if e == nil {
					restored, e := d.Restore(h, preview)
					if e == nil && restored.Applied() {
						d, c, h = restored.Document(), restored.Cursor(), restored.History()
					}
				}
			}
			exact(t, old, before)
			newOriginalAbsent(t, d, birth)
			if c.Revision() != d.Revision() || d.CheckMutation() != nil {
				t.Fatal("published mismatch")
			}
		}
	})
}
