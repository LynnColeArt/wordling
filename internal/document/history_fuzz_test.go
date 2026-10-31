package document_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
	"testing"
)

// Declared budget: at most64 domain commands per input; existing16MiB reader,
// 16K mutation-token/64KiB native limits; three stored entries,4096-token preview.
// Source40-dependent branches remain explicit failures until actually qualified.
func FuzzDeletionHistory(f *testing.F) {
	plain, _ := plainOriginal(f).Export()
	f.Add(plain, []byte{0, 0, 8, 9, 10, 8, 11, 8, 11})
	f.Add(fixture(f), []byte{7, 2, 8, 11, 8, 11, 12})
	f.Add(fixture(f), []byte{0x27, 2, 8, 11, 8, 11})
	f.Add(fixture(f), []byte{0x13, 4, 0, 8, 9, 11})
	f.Add(fixture(f), []byte{0x17, 2, 8, 9, 11})
	f.Add(synthetic(f, bytes.Repeat([]byte{'x'}, document.MaxMutationTokens)), []byte{0, 8, 11, 8, 11})
	f.Add(synthetic(f, []byte{0xd0, 1, 7, 0, 0xc3, 12, 0xc3, 7, 0, 1, 0xd0}), []byte{0, 7, 8, 11})
	f.Add(fixture(f)[:15], []byte{0})
	f.Fuzz(func(t *testing.T, input, operations []byte) {
		if len(input) > wp51.MaxInputBytes+1 {
			return
		}
		original := bytes.Clone(input)
		d, e := document.Parse(input)
		if !bytes.Equal(input, original) {
			t.Fatal("Parse mutated caller")
		}
		if e != nil {
			return
		}
		exact(t, d, original)
		h, e := document.NewHistory(d)
		if e != nil {
			exact(t, d, original)
			return
		}
		c, _ := d.CursorAt(0)
		var pending, block document.Deletion
		var preview document.Preview
		initial, e := wp51.Parse(original)
		if e != nil {
			t.Fatal(e)
		}
		info := initial.Inspect()
		flag := -1
		for _, packet := range info.Packets {
			if packet.Type == 6 {
				flag = packet.Data.Offset
			}
		}
		for _, operation := range operations[:min(len(operations), 64)] {
			before, _ := d.Export()
			oldDocument := *d
			oldCursor := c
			oldOffset, _ := c.Offset()
			oldRevision := c.Revision()
			oldHistory := h
			oldPreview := preview
			stored := make([]document.EntryInfo, h.Count())
			for i := range stored {
				stored[i], e = h.Entry(i)
				if e != nil {
					t.Fatal(e)
				}
			}
			var oldOverlay document.Overlay
			if oldPreview.Active() {
				zero, e := oldPreview.Present(0, 0, true)
				if e != nil {
					t.Fatal(e)
				}
				oldOverlay, e = oldPreview.Present(0, min(zero.TotalTokens, 16), true)
				if e != nil {
					t.Fatal(e)
				}
			}
			failed := func(r document.Deletion, argumentCursor document.Cursor) {
				t.Helper()
				exact(t, r.Document(), before)
				if r.History().Revision() != oldHistory.Revision() || r.Cursor() != argumentCursor || r.Applied() {
					t.Fatal("failed command published partial state")
				}
			}
			adopt := func(r document.Deletion) { d, c, h = r.Document(), r.Cursor(), r.History() }
			switch operation & 15 {
			case 0, 1:
				direction := document.ForwardDelete
				if operation&15 == 1 {
					direction = document.Backspace
				}
				r, e := d.Delete(c, direction, h)
				if e != nil {
					failed(r, c)
				} else if r.Pending() {
					pending = r
				} else {
					adopt(r)
				}
			case 2:
				r, e := d.AnswerDeletion(h, pending, document.DeleteAnswer((operation>>4)%4+1))
				if e != nil {
					failed(r, pending.Cursor())
				} else {
					adopt(r)
					if r.BlockActive() {
						block = r
					}
					pending = document.Deletion{}
				}
			case 3:
				c, _ = d.CursorAt(int(operation>>4) % (d.TokenCount() + 1))
				if next, e := h.InterruptGrouping(); e == nil {
					h = next
				}
			case 4:
				c = c.WithReveal(!c.Reveal())
				if next, e := h.InterruptGrouping(); e == nil {
					h = next
				}
			case 5:
				if next, e := h.Separate(document.SavedBoundary); e == nil {
					h = next
				}
			case 6:
				if next, e := c.Move(1); e == nil {
					c = next
					if next, e := h.Separate(document.RightBoundary); e == nil {
						h = next
					}
				}
			case 7:
				on, off := -1, -1
				for i := 0; i < d.TokenCount(); i++ {
					token, _ := d.Token(i)
					if token.Kind == document.BoldOn {
						on = i
					}
					if token.Kind == document.BoldOff {
						off = i
						break
					}
				}
				if on < 0 {
					continue
				}
				start, end := on, on+1
				switch (operation >> 4) % 3 {
				case 1:
					start, end = off, off+1
				case 2:
					end = off + 1
				}
				a, _ := d.CursorAt(start)
				b, _ := d.CursorAt(end)
				if next, e := h.Separate(document.RightBoundary); e == nil {
					h = next
				}
				oldHistory = h
				r, e := d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), h)
				if e != nil {
					failed(r, b.WithReveal(true))
				} else {
					c = b.WithReveal(true)
					pending = r
				}
			case 8:
				if next, e := h.Open(c); e == nil {
					preview = next
				}
			case 9:
				if next, e := preview.Previous(); e == nil {
					preview = next
				}
			case 10:
				if next, e := h.CancelPreview(preview); e == nil {
					h = next
					preview = document.Preview{}
				}
			case 11:
				r, e := d.Restore(h, preview)
				if e != nil {
					failed(r, preview.Cursor())
				} else {
					adopt(r)
					preview = document.Preview{}
				}
			case 12, 13:
				var edit document.EditResult
				var e error
				text := []byte{32 + operation%95}
				if operation&15 == 12 {
					edit, e = d.InsertASCII(c, text)
				} else {
					edit, e = d.TypeoverASCII(c, text)
				}
				if e == nil {
					if next, e := h.AfterEdit(edit); e == nil {
						d, c, h = edit.Document, edit.Cursor, next
					}
				}
			case 14:
				edit, e := d.InsertASCII(c, []byte("X"))
				if e == nil {
					edit.Changed = !edit.Changed
					next, e := h.AfterEdit(edit)
					category(t, e, document.InvalidEditResult)
					if next.Revision() != h.Revision() {
						t.Fatal("forged public result changed history")
					}
				}
			case 15:
				copy := *d
				other, e := document.Parse(before)
				if e != nil {
					t.Fatal(e)
				}
				*d = *other
				r, e := d.Delete(c, document.ForwardDelete, h)
				category(t, e, document.RevisionMismatch)
				failed(r, c)
				*d = copy
				if preview.Active() {
					replacement, _ := document.NewHistory(d)
					r, e := d.Restore(replacement, preview)
					if e == nil {
						t.Fatal("replaced history retargeted preview")
					}
					if r.History().Revision() != replacement.Revision() {
						t.Fatal("failed replacement changed new history")
					}
				}
			}
			exact(t, &oldDocument, before)
			if offset, e := oldCursor.Offset(); e != nil || offset != oldOffset || oldCursor.Revision() != oldRevision {
				t.Fatal("cursor snapshot changed", e)
			}
			for i, want := range stored {
				got, e := oldHistory.Entry(i)
				if e != nil || !bytes.Equal(got.Native, want.Native) || got.Kind != want.Kind || got.Commands != want.Commands {
					t.Fatal("stored fragment snapshot mutated", e)
				}
			}
			if oldPreview.Active() {
				view, e := oldPreview.Present(0, len(oldOverlay.Elements), true)
				if e != nil {
					t.Fatal(e)
				}
				for i, element := range view.Elements {
					if element.Kind != oldOverlay.Elements[i].Kind || element.Text != oldOverlay.Elements[i].Text || !bytes.Equal(element.Raw, oldOverlay.Elements[i].Raw) {
						t.Fatal("preview snapshot changed")
					}
				}
			}
			if e := d.CheckMutation(); e != nil {
				t.Fatal("successful state not admitted", e)
			}
			raw, _ := d.Export()
			source, _ := d.OriginalExport()
			if !bytes.Equal(source, original) {
				t.Fatal("loaded source image lost")
			}
			if d.TokenCount() > document.MaxMutationTokens || len(raw) > document.MaxMutationBytes || h.Count() > document.HistoryCapacity {
				t.Fatal("resource policy exceeded")
			}
			for i, b := range raw[:info.Body.Offset] {
				if i == flag {
					if b != original[i] && b != original[i]|8 {
						t.Fatal("unapproved flag change")
					}
				} else if b != original[i] {
					t.Fatal("unrelated prefix byte changed", i)
				}
			}
			if block.BlockActive() && operation&15 == 10 {
				r, e := d.CancelBlock(h, block)
				if e == nil {
					adopt(r)
					block = document.Deletion{}
				}
			}
		}
	})
}
