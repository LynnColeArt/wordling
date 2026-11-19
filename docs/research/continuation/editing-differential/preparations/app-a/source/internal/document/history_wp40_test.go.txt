package document_test

import (
	"bytes"
	"encoding/json"
	"github.com/lynncoleart/wordling/internal/document"
	"os"
	"testing"
)

// Given the exact WP40 seeded/pre-browsed/Right-separated original setup,
// When one researched target and the bounded history sequence are applied,
// Then native marker bytes and original cursor identity agree in both fresh runs.
func TestWP40ExactObservedPaths(t *testing.T) {
	for _, view := range []string{"normal", "reveal"} {
		for _, direction := range []string{"delete", "backspace"} {
			for _, target := range []string{"on", "off"} {
				name := "direct-" + view + "-" + direction + "-" + target
				for _, repeat := range []string{"r1", "r2"} {
					t.Run(name+"-"+repeat, func(t *testing.T) {
						d, c, h := wp40Setup(t, name, repeat, view == "reveal")
						gap := 1
						if target == "off" {
							gap = 4
						}
						dir := document.ForwardDelete
						if direction == "backspace" {
							gap++
							dir = document.Backspace
						}
						c, _ = d.CursorAt(gap)
						c = c.WithReveal(view == "reveal")
						r, e := d.Delete(c, dir, h)
						if e != nil {
							t.Fatal(e)
						}
						if r.Pending() {
							r, e = d.AnswerDeletion(h, r, document.Yes)
							if e != nil {
								t.Fatal(e)
							}
						}
						d, c, h = r.Document(), r.Cursor(), r.History()
						if h.CountKnown() {
							t.Fatal("bounded rows became absolute count")
						}
						out := 1
						if target == "off" {
							out = 3
						}
						if c.Gap() != out {
							t.Fatal(c.Gap())
						}
						finishWP40(t, name, repeat, d, c, h, out+1)
					})
				}
			}
		}
	}
	for _, repeat := range []string{"r1", "r2"} {
		t.Run("closing-"+repeat, func(t *testing.T) {
			name := "closing-block-repair-yes"
			d, _, h := wp40Setup(t, name, repeat, true)
			a, _ := d.CursorAt(4)
			b, _ := d.CursorAt(5)
			q, e := d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), h)
			if e != nil {
				t.Fatal(e)
			}
			r, e := d.AnswerDeletion(h, q, document.Yes)
			if e != nil {
				t.Fatal(e)
			}
			if r.BodyChanged() || r.BlockActive() || r.Cursor().Gap() != 5 || r.History().CountKnown() {
				t.Fatal("closing context")
			}
			finishWP40(t, name, repeat, r.Document(), r.Cursor(), r.History(), 7)
		})
	}
}
func wp40Setup(t *testing.T, name, repeat string, reveal bool) (*document.Document, document.Cursor, document.History) {
	t.Helper()
	raw, e := os.ReadFile("../../docs/research/continuation/code-pair-history/runs/wp40-" + name + "-" + repeat + "/N0000.WP5")
	if e != nil {
		t.Fatal(e)
	}
	d, e := document.Parse(raw)
	if e != nil {
		t.Fatal(e)
	}
	h, e := document.NewHistory(d)
	if e != nil {
		t.Fatal(e)
	}
	c, _ := d.CursorAt(0)
	c = c.WithReveal(reveal)
	d, c, h = deleteForward(t, d, c, h)
	p, e := h.Open(c)
	if e != nil {
		t.Fatal(e)
	}
	for range 3 {
		p, e = p.Previous()
		if e != nil {
			t.Fatal(e)
		}
	}
	h, e = h.CancelPreview(p)
	if e != nil {
		t.Fatal(e)
	}
	c, _ = c.Move(1)
	h, e = h.Separate(document.RightBoundary)
	if e != nil {
		t.Fatal(e)
	}
	return d, c, h
}
func finishWP40(t *testing.T, name, repeat string, d *document.Document, c document.Cursor, h document.History, gap int) {
	t.Helper()
	before, _ := d.Export()
	p, e := h.Open(c)
	if e != nil {
		t.Fatal(e)
	}
	for i, want := range wp40Rows(t, name, repeat, "immediate-target-history") {
		if normalOverlay(t, p) != want {
			t.Fatal("source40 immediate whole overlay", normalOverlay(t, p), want)
		}
		if i < 3 {
			p, e = p.Previous()
			if e != nil {
				t.Fatal(e)
			}
		}
	}
	_, e = p.Previous()
	category(t, e, document.UnsupportedHistoryEffect)
	h, e = h.CancelPreview(p)
	if e != nil {
		t.Fatal(e)
	}
	exact(t, d, before)
	p, e = h.Open(c)
	if e != nil {
		t.Fatal(e)
	}
	r, e := d.Restore(h, p)
	if e != nil {
		t.Fatal(e)
	}
	d, c, h = r.Document(), r.Cursor(), r.History()
	if c.Gap() != gap {
		t.Fatal("Restore gap", c.Gap(), gap)
	}
	p, e = h.Open(c)
	if e != nil {
		t.Fatal(e)
	}
	_, e = d.Restore(h, p)
	category(t, e, document.UnsupportedHistoryEffect)
	for i, want := range wp40Rows(t, name, repeat, "post-restore-history") {
		if normalOverlay(t, p) != want {
			t.Fatal("source40 post-Restore whole overlay", normalOverlay(t, p), want)
		}
		if i < 3 {
			p, e = p.Previous()
			if e != nil {
				t.Fatal(e)
			}
		}
	}
	h, e = h.CancelPreview(p)
	if e != nil {
		t.Fatal(e)
	}
	marker, e := d.InsertASCII(c, []byte("X"))
	if e != nil {
		t.Fatal(e)
	}
	after, e := h.AfterEdit(marker)
	if e != nil || after.Qualified() {
		t.Fatal("marker history", e)
	}
	want, e := os.ReadFile("../../docs/research/continuation/code-pair-history/runs/wp40-" + name + "-" + repeat + "/N0001.WP5")
	if e != nil {
		t.Fatal(e)
	}
	got, _ := marker.Document.Export()
	if !bytes.Equal(got, want) {
		t.Fatal("exact original native marker differs")
	}
	if marker.Cursor.Gap() != gap+1 {
		t.Fatal("marker gap")
	}
}

func TestWP40UnqualifiedContextsRemainAtomic(t *testing.T) {
	for _, variant := range []string{"fresh", "unbrowsed", "two-previous", "extra-previous", "wrong-seed-gap", "save-separator", "pane-interleave", "wrong-view", "two-seeds"} {
		t.Run(variant, func(t *testing.T) {
			raw, e := os.ReadFile("../../docs/research/continuation/code-pair-history/runs/wp40-direct-normal-delete-on-r1/N0000.WP5")
			if e != nil {
				t.Fatal(e)
			}
			d, _ := document.Parse(raw)
			h, _ := document.NewHistory(d)
			c, _ := d.CursorAt(0)
			if variant != "fresh" {
				d, c, h = deleteForward(t, d, c, h)
			} else {
				edit, _ := d.Delete(c, document.ForwardDelete, h)
				d, c = edit.Document(), edit.Cursor()
				h, _ = document.NewHistory(d)
			}
			if variant != "unbrowsed" && variant != "fresh" {
				if variant == "wrong-seed-gap" {
					c, _ = d.CursorAt(1)
				}
				p, _ := h.Open(c)
				n := 3
				if variant == "two-previous" {
					n = 2
				}
				if variant == "extra-previous" {
					n = 4
				}
				for range n {
					p, _ = p.Previous()
				}
				h, _ = h.CancelPreview(p)
			}
			boundary := document.RightBoundary
			if variant == "save-separator" {
				boundary = document.SavedBoundary
			}
			h, _ = h.Separate(boundary)
			if variant == "pane-interleave" {
				h, _ = h.InterruptGrouping()
			}
			if variant == "two-seeds" {
				c, _ = d.CursorAt(0)
				d, c, h = deleteForward(t, d, c, h)
				h, _ = h.Separate(document.RightBoundary)
			}
			targetGap := 1
			if variant == "two-seeds" {
				targetGap = 0
			}
			c, _ = d.CursorAt(targetGap)
			if variant == "wrong-view" {
				c = c.WithReveal(true)
			}
			before, _ := d.Export()
			saved := h.Revision()
			r, e := d.Delete(c, document.ForwardDelete, h)
			if e == nil && r.Pending() {
				r, e = d.AnswerDeletion(h, r, document.Yes)
			}
			if e == nil {
				t.Fatal("unqualified context admitted")
			}
			if r.History().Revision() != saved {
				t.Fatal("history changed")
			}
			exact(t, r.Document(), before)
			exact(t, d, before)
		})
	}
}

func TestWP40SnapshotAndGapBoundaries(t *testing.T) {
	d, c, h := wp40Setup(t, "direct-reveal-delete-on", "r1", true)
	r, e := d.Delete(c, document.ForwardDelete, h)
	if e != nil {
		t.Fatal(e)
	}
	d, c, h = r.Document(), r.Cursor(), r.History()
	p, _ := h.Open(c)
	saved := h
	retained := p
	h = document.History{}
	_, e = d.Restore(h, p)
	category(t, e, document.InvalidHistory)
	h = saved
	other, _ := document.NewHistory(d)
	h = other
	_, e = d.Restore(h, p)
	category(t, e, document.HistoryMismatch)
	h = saved
	wrong, _ := c.Move(1)
	_, e = h.Open(wrong)
	category(t, e, document.UnsupportedHistoryEffect)
	_, e = h.Open(c.WithReveal(false))
	category(t, e, document.UnsupportedHistoryEffect)
	for range 3 {
		p, _ = p.Previous()
	}
	h, _ = h.CancelPreview(p)
	if retained.Index() != 0 {
		t.Fatal("preview wrapper retargeted")
	}
	_, e = d.Restore(h, retained)
	category(t, e, document.HistoryMismatch)
	_, e = h.Separate(document.RightBoundary)
	category(t, e, document.UnsupportedHistoryEffect)
	_, e = h.InterruptGrouping()
	category(t, e, document.UnsupportedHistoryEffect)
}

func wp40Rows(t testing.TB, name, repeat, label string) []string {
	t.Helper()
	raw, e := os.ReadFile("../../docs/research/continuation/code-pair-history/observations.json")
	if e != nil {
		t.Fatal(e)
	}
	var ledger struct {
		Observations struct {
			Cases []struct {
				Plan struct {
					ID string `json:"id"`
				} `json:"plan"`
				Samples []struct {
					RunID string `json:"run_id"`
					Menus []struct {
						Label string   `json:"label"`
						Rows  []string `json:"whole_overlaid_rows"`
					} `json:"menus"`
				} `json:"samples"`
			} `json:"cases"`
		} `json:"observations"`
	}
	if e = json.Unmarshal(raw, &ledger); e != nil {
		t.Fatal(e)
	}
	for _, c := range ledger.Observations.Cases {
		if c.Plan.ID == name {
			for _, s := range c.Samples {
				if s.RunID == "wp40-"+name+"-"+repeat {
					for _, m := range s.Menus {
						if m.Label == label {
							return m.Rows
						}
					}
				}
			}
		}
	}
	t.Fatal("missing exact40 case/run/menu association")
	return nil
}

func TestStructuralProjectionUsesActualNativeValues(t *testing.T) {
	// Algorithmic data-identity check, not another original observation. Printable
	// ASCII values cannot be code delimiters; qualification is command/token shape.
	raw, e := os.ReadFile("../../docs/research/continuation/code-pair-history/runs/wp40-direct-reveal-delete-on-r1/N0000.WP5")
	if e != nil {
		t.Fatal(e)
	}
	d, _ := document.Parse(raw)
	for _, change := range []struct {
		gap  int
		text string
	}{{0, "!"}, {1, "p"}, {3, "q"}, {4, "r"}, {6, "s"}} {
		c, _ := d.CursorAt(change.gap)
		r, e := d.TypeoverASCII(c, []byte(change.text))
		if e != nil {
			t.Fatal(e)
		}
		d = r.Document
	}
	h, _ := document.NewHistory(d)
	c, _ := d.CursorAt(0)
	c = c.WithReveal(true)
	d, c, h = deleteForward(t, d, c, h)
	p, _ := h.Open(c)
	for range 3 {
		p, _ = p.Previous()
	}
	h, _ = h.CancelPreview(p)
	h, _ = h.Separate(document.RightBoundary)
	c, _ = c.Move(1)
	r, e := d.Delete(c, document.ForwardDelete, h)
	if e != nil {
		t.Fatal(e)
	}
	d, c, h = r.Document(), r.Cursor(), r.History()
	p, _ = h.Open(c)
	if normalOverlay(t, p) != "p!qrs" {
		t.Fatal("native fragment replaced by fixture sentinel")
	}
	for range 3 {
		p, _ = p.Previous()
	}
	h, _ = h.CancelPreview(p)
	p, _ = h.Open(c)
	restored, e := d.Restore(h, p)
	if e != nil {
		t.Fatal(e)
	}
	got, _ := restored.Document().Export()
	if !bytes.HasSuffix(got, []byte("p!qrs")) {
		t.Fatal("actual data transform")
	}
}
