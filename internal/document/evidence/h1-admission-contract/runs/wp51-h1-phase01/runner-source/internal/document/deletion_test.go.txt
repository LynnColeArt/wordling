package document_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/document"
	"testing"
)

func TestNormalCodeQuestionDirectionalDeclines(t *testing.T) {
	for _, tc := range []struct {
		gap       int
		direction document.DeleteDirection
		out       int
		label     string
	}{{1, document.ForwardDelete, 2, "[BOLD]"}, {4, document.ForwardDelete, 5, "[bold]"}, {2, document.Backspace, 1, "[BOLD]"}, {5, document.Backspace, 4, "[bold]"}} {
		for _, answer := range []document.DeleteAnswer{document.No, document.F1, document.Escape} {
			d, _ := document.Parse(fixture(t))
			h, e := document.NewHistory(d)
			if e != nil {
				t.Fatal(e)
			}
			c, _ := d.CursorAt(tc.gap)
			pending, e := d.Delete(c, tc.direction, h)
			if e != nil || !pending.Pending() || pending.Prompt() != "Delete "+tc.label+"? No (Yes)" {
				t.Fatal(pending.Prompt(), e)
			}
			exact(t, pending.Document(), fixture(t))
			r, e := d.AnswerDeletion(h, pending, answer)
			if e != nil {
				t.Fatal(e)
			}
			if r.Pending() || r.Applied() || r.NativeChanged() || r.Cursor().Gap() != tc.out || r.BlockActive() {
				t.Fatal("wrong contextual decline")
			}
			exact(t, r.Document(), fixture(t))
			exact(t, d, fixture(t))
			if r.History().Count() != 0 {
				t.Fatal("decline created entry")
			}
		}
	}
}

func TestBlockDeclinesRetainSelectionAndSeparateCleanup(t *testing.T) {
	for _, pair := range [][2]int{{1, 2}, {4, 5}, {1, 5}} {
		for _, answer := range []document.DeleteAnswer{document.No, document.F1, document.Escape} {
			d, _ := document.Parse(fixture(t))
			h, _ := document.NewHistory(d)
			a, _ := d.CursorAt(pair[0])
			b, _ := d.CursorAt(pair[1])
			a = a.WithReveal(true)
			b = b.WithReveal(true)
			pending, e := d.DeleteBlock(a, b, h)
			if e != nil || pending.Prompt() != "Delete Block? No (Yes)" {
				t.Fatal(e)
			}
			r, e := d.AnswerDeletion(h, pending, answer)
			if e != nil || !r.BlockActive() || r.Cursor().Gap() != pair[1] {
				t.Fatal("block declined as global cancel", e)
			}
			exact(t, r.Document(), fixture(t))
			cleared, e := d.CancelBlock(r.History(), r)
			if e != nil || cleared.BlockActive() {
				t.Fatal(e)
			}
			exact(t, cleared.Document(), fixture(t))
			p, e := cleared.History().Open(cleared.Cursor())
			if e != nil || p.Active() {
				t.Fatal("fresh refused block created history", e)
			}
		}
	}
}

func TestAttributedBlockAndRepairHistory(t *testing.T) {
	for _, tc := range []struct {
		start, end int
		fragment   []byte
		deleted    string
		out        int
		restored   []byte
		restoreGap int
	}{
		{1, 5, []byte{0xc3, 12, 0xc3, 'B', 'C', 0xc4, 12, 0xc4}, "AD", 1, []byte{'A', 0xc3, 12, 0xc3, 'B', 'C', 0xc4, 12, 0xc4, 'D'}, 5},
		{1, 2, []byte{0xc4, 12, 0xc4, 0xc3, 12, 0xc3}, "ABCD", 2, []byte{'A', 0xc3, 12, 0xc3, 0xc4, 12, 0xc4, 0xc3, 12, 0xc3, 'B', 'C', 0xc4, 12, 0xc4, 'D'}, 4},
	} {
		d, _ := document.Parse(fixture(t))
		h, _ := document.NewHistory(d)
		a, _ := d.CursorAt(tc.start)
		b, _ := d.CursorAt(tc.end)
		pending, e := d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), h)
		if e != nil {
			t.Fatal(e)
		}
		r, e := d.AnswerDeletion(h, pending, document.Yes)
		if e != nil {
			t.Fatal(e)
		}
		if !r.Applied() || r.BlockActive() || r.Cursor().Gap() != tc.out || r.History().Count() != 1 {
			t.Fatal("confirmed block outcome")
		}
		info, e := r.History().Entry(0)
		if e != nil || !bytes.Equal(info.Native, tc.fragment) {
			t.Fatal("wrong remembered native fragment", info, e)
		}
		info.Native[0] = 0
		again, _ := r.History().Entry(0)
		if !bytes.Equal(again.Native, tc.fragment) {
			t.Fatal("fragment alias")
		}
		p, e := r.History().Open(r.Cursor())
		if e != nil || !p.Active() {
			t.Fatal(e)
		}
		restored, e := r.Document().Restore(r.History(), p)
		if e != nil {
			t.Fatal(e)
		}
		raw, _ := restored.Document().Export()
		if !bytes.Equal(raw[324:], tc.restored) || restored.Cursor().Gap() != tc.restoreGap {
			t.Fatal("restored code identity/gap", raw[324:])
		}
		if restored.History().Count() != 1 {
			t.Fatal("Restore discarded preserved entry bytes")
		}
		if tc.end == 5 {
			if restored.History().Qualified() {
				t.Fatal("invented later attributed-entry retention")
			}
			_, e = restored.History().Open(restored.Cursor())
			category(t, e, document.UnsupportedHistoryEffect)
		}
		if tc.start == 1 && tc.end == 2 {
			next, _ := restored.History().Open(restored.Cursor())
			bad, e := restored.Document().Restore(restored.History(), next)
			category(t, e, document.UnsupportedBody)
			if bad.History().Revision() != restored.History().Revision() || bad.Cursor() != restored.Cursor() {
				t.Fatal("above-two-pair refusal changed history/cursor")
			}
			exact(t, bad.Document(), raw)
		}
	}
}
