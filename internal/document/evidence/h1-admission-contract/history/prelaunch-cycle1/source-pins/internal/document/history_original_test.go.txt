package document_test

import (
	"encoding/json"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
	"os"
	"testing"
)

func TestOriginalFollowHistoryNativeMarkers(t *testing.T) {
	for _, family := range []string{"consecutive", "save-only", "consume-direct", "repair-restore"} {
		for _, repeat := range []string{"r1", "r2"} {
			t.Run(family+"-"+repeat, func(t *testing.T) {
				dir := "../../docs/research/continuation/native-edits/runs/wp23-b-history-follow-" + family + "-" + repeat
				raw, e := os.ReadFile(dir + "/run.json")
				if e != nil {
					t.Fatal(e)
				}
				var run struct {
					Cases []struct{ Source, Final string } `json:"cases"`
				}
				if e = json.Unmarshal(raw, &run); e != nil || len(run.Cases) != 1 {
					t.Fatal(e)
				}
				source, e := os.ReadFile(dir + "/" + run.Cases[0].Source)
				if e != nil {
					t.Fatal(e)
				}
				d, e := document.Parse(source)
				if e != nil {
					t.Fatal(e)
				}
				h, _ := document.NewHistory(d)
				c, _ := d.CursorAt(0)
				if family == "repair-restore" {
					a, _ := d.CursorAt(1)
					b, _ := d.CursorAt(2)
					q, e := d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), h)
					if e != nil {
						t.Fatal(e)
					}
					r, e := d.AnswerDeletion(h, q, document.Yes)
					if e != nil {
						t.Fatal(e)
					}
					d, c, h = r.Document(), r.Cursor(), r.History()
				} else {
					d, c, h = deleteForward(t, d, c, h)
					if family == "save-only" {
						h, _ = h.Separate(document.SavedBoundary)
					}
					if family == "consume-direct" {
						c, _ = c.Move(1)
						h, _ = h.Separate(document.RightBoundary)
					}
					d, c, h = deleteForward(t, d, c, h)
				}
				if family != "consume-direct" {
					p, _ := h.Open(c)
					iterations := 3
					if family == "repair-restore" {
						iterations = 1
					}
					for range iterations {
						p, _ = p.Previous()
					}
					h, e = h.CancelPreview(p)
					if e != nil {
						t.Fatal(e)
					}
				}
				restores := 1
				if family == "consume-direct" {
					restores = 2
				}
				for range restores {
					p, _ := h.Open(c)
					r, e := d.Restore(h, p)
					if e != nil {
						t.Fatal(e)
					}
					d, c, h = r.Document(), r.Cursor(), r.History()
				}
				// Source trace reopens/cancels before the unique marker; this tests that
				// known sequence, never a fictional post-X original history observation.
				p, _ := h.Open(c)
				iterations := 2
				if family == "repair-restore" {
					iterations = 1
				}
				for range iterations {
					p, _ = p.Previous()
				}
				h, e = h.CancelPreview(p)
				if e != nil {
					t.Fatal(e)
				}
				beforeMarker, _ := d.Export()
				marker, e := d.InsertASCII(c, []byte("X"))
				if e != nil {
					t.Fatal(e)
				}
				advanced, e := h.AfterEdit(marker)
				if e != nil {
					t.Fatal(e)
				}
				want, e := os.ReadFile(dir + "/" + run.Cases[0].Final)
				if e != nil {
					t.Fatal(e)
				}
				got, _ := marker.Document.Export()
				if len(got) != len(want) {
					t.Fatal("original length")
				}
				image, e := wp51.Parse(got)
				if e != nil {
					t.Fatal(e)
				}
				flags := -1
				for _, packet := range image.Inspect().Packets {
					if packet.Type == 6 {
						flags = packet.Data.Offset
					}
				}
				for i, b := range got {
					if family == "consume-direct" && i == flags {
						if b != want[i]|8 {
							t.Fatal("explicit approved must-format policy")
						}
						continue
					}
					if b != want[i] {
						t.Fatal("unexplained original native difference", family, repeat, i)
					}
				}
				gaps := map[string]int{"consecutive": 3, "save-only": 2, "consume-direct": 4, "repair-restore": 5}
				if marker.Cursor.Gap() != gaps[family] {
					t.Fatal("original marker-bound gap")
				}
				if advanced.Qualified() {
					t.Fatal("post-X history declared observed")
				}
				exact(t, d, beforeMarker)
			})
		}
	}
}
