package document_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/document"
	"os"
	"strings"
	"testing"
)

func plainOriginal(t testing.TB) *document.Document {
	t.Helper()
	raw, e := os.ReadFile("../../docs/research/continuation/native-edits/runs/wp23-a-modes-r1/N0000.WP5")
	if e != nil {
		t.Fatal(e)
	}
	d, e := document.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	return d
}
func normalOverlay(t testing.TB, p document.Preview) string {
	t.Helper()
	view, e := p.Present(0, 128, false)
	if e != nil { // Ask the exact bounded total, never silently truncate.
		view, e = p.Present(0, 0, false)
		if e != nil {
			t.Fatal(e)
		}
		view, e = p.Present(0, view.TotalTokens, false)
		if e != nil {
			t.Fatal(e)
		}
	}
	var text strings.Builder
	for _, element := range view.Elements {
		text.WriteString(element.Text)
	}
	return text.String()
}
func deleteForward(t testing.TB, d *document.Document, c document.Cursor, h document.History) (*document.Document, document.Cursor, document.History) {
	t.Helper()
	r, e := d.Delete(c, document.ForwardDelete, h)
	if e != nil || !r.Applied() {
		t.Fatal(e)
	}
	return r.Document(), r.Cursor(), r.History()
}

func TestOriginalASCIIGroupingSaveAndRight(t *testing.T) {
	for _, tc := range []struct {
		name     string
		boundary document.HistoryBoundary
		right    bool
		previews []string
		restored string
		gap      int
	}{
		{"consecutive", 0, false, []string{"abc", "abc", "abc", "abc"}, "abc", 2},
		{"save-only", document.SavedBoundary, false, []string{"bc", "ac", "bc", "ac"}, "bc", 1},
		{"right", document.RightBoundary, true, []string{"bc", "ba", "bc", "ba"}, "bc", 2},
	} {
		t.Run(tc.name, func(t *testing.T) {
			d := plainOriginal(t)
			h, _ := document.NewHistory(d)
			c, _ := d.CursorAt(0)
			d, c, h = deleteForward(t, d, c, h)
			if tc.boundary != 0 {
				var e error
				h, e = h.Separate(tc.boundary)
				if e != nil {
					t.Fatal(e)
				}
			}
			if tc.right {
				c, _ = c.Move(1)
			}
			d, c, h = deleteForward(t, d, c, h)
			before, _ := d.Export()
			p, e := h.Open(c)
			if e != nil {
				t.Fatal(e)
			}
			for _, want := range tc.previews {
				if got := normalOverlay(t, p); got != want {
					t.Fatal(got, want)
				}
				p, e = p.Previous()
				if e != nil {
					t.Fatal(e)
				}
			}
			exact(t, d, before)
			cancelled, e := h.CancelPreview(p)
			if e != nil {
				t.Fatal(e)
			}
			exact(t, d, before)
			p, e = cancelled.Open(c)
			if e != nil || p.Index() != 0 {
				t.Fatal("reopen did not select newest", e)
			}
			r, e := d.Restore(cancelled, p)
			if e != nil {
				t.Fatal(e)
			}
			raw, _ := r.Document().Export()
			if string(raw[324:]) != tc.restored || r.Cursor().Gap() != tc.gap {
				t.Fatal(raw[324:], r.Cursor().Gap())
			}
			// Exact whole overlaid post-Restore lines from approved history-expectations.
			reopened, e := r.History().Open(r.Cursor())
			if e != nil {
				t.Fatal(e)
			}
			want := map[string]string{"consecutive": "ababc", "save-only": "bbc", "right": "bcc"}[tc.name]
			if normalOverlay(t, reopened) != want {
				t.Fatal("Restore consumed/reordered an entry")
			}
		})
	}
}

func TestRepeatedRestoreRetainsEntryWithoutSave(t *testing.T) {
	d := plainOriginal(t)
	h, _ := document.NewHistory(d)
	c, _ := d.CursorAt(0)
	d, c, h = deleteForward(t, d, c, h)
	c, _ = c.Move(1)
	h, _ = h.Separate(document.RightBoundary)
	d, c, h = deleteForward(t, d, c, h)
	for _, want := range []string{"bc", "bcc"} {
		p, _ := h.Open(c)
		r, e := d.Restore(h, p)
		if e != nil {
			t.Fatal(e)
		}
		d, c, h = r.Document(), r.Cursor(), r.History()
		raw, _ := d.Export()
		if string(raw[324:]) != want || h.Count() != 2 {
			t.Fatal("Restore retained entries", string(raw[324:]))
		}
	}
	p, _ := h.Open(c)
	if normalOverlay(t, p) != "bccc" {
		t.Fatal("wrong retained newest")
	}
	p, _ = p.Previous()
	if normalOverlay(t, p) != "bcca" {
		t.Fatal("wrong retained older")
	}
}

func TestThreeEntryEvictionAndPreviewIsolation(t *testing.T) {
	for _, words := range [][]string{{"ONE", "TWO", "THREE"}, {"ONE", "TWO", "THREE", "FOUR"}} {
		// The original runner typed these exact ASCII words without a native source
		// save. This Go-created setup over a lawful loaded original is labelled as
		// setup, not an invented original pre-deletion native hash.
		base := plainOriginal(t)
		c, _ := base.CursorAt(0)
		setup, e := base.TypeoverASCII(c, []byte(strings.Join(words, " ")))
		if e != nil {
			t.Fatal(e)
		}
		d := setup.Document
		c, _ = d.CursorAt(0)
		h, _ := document.NewHistory(d)
		for index, word := range words {
			for range word {
				d, c, h = deleteForward(t, d, c, h)
			}
			if index < len(words)-1 {
				c, _ = c.Move(1)
				h, _ = h.Separate(document.RightBoundary)
			}
		}
		before, _ := d.Export()
		h, _ = h.Separate(document.SavedBoundary)
		p, _ := h.Open(c)
		count := len(words)
		if h.Count() != 3 {
			t.Fatal(h.Count())
		}
		for i := 0; i < 4; i++ {
			want := strings.Repeat(" ", count-1) + words[count-1-(i%3)]
			if normalOverlay(t, p) != want {
				t.Fatal("capacity/cycle", normalOverlay(t, p), want)
			}
			p, _ = p.Previous()
		}
		cancelled, _ := h.CancelPreview(p)
		exact(t, d, before)
		p, _ = cancelled.Open(c)
		if p.Index() != 0 {
			t.Fatal("reopen selection")
		}
		p, _ = p.Previous()
		p, _ = p.Previous()
		r, e := d.Restore(cancelled, p)
		if e != nil {
			t.Fatal(e)
		}
		expected := strings.Repeat(" ", count-1) + words[count-3]
		raw, _ := r.Document().Export()
		if string(raw[324:]) != expected {
			t.Fatal(string(raw[324:]), expected)
		}
		family := "043"
		if count == 4 {
			family = "211"
		}
		original, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-history-02/CMD51-" + family + "/HISTORY.WP5")
		if e != nil {
			t.Fatal(e)
		}
		if !bytes.Equal(raw[324:], original[324:]) {
			t.Fatal("original restored body differs")
		}
	}
}
