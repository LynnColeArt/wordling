package body_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/merge/body"
	"github.com/lynncoleart/wordling/internal/merge/native"
	"testing"
)

func TestBothOriginalRuns(t *testing.T) {
	for _, run := range []string{"2026-10-29-advanced-03", "2026-10-29-advanced-04"} {
		for _, id := range []string{"207", "209"} {
			t.Run(run+id, func(t *testing.T) {
				path := run + "/CMD51-" + id + "/"
				raw := fixture(t, path+"PRIMARY.WP5")
				raw2 := fixture(t, path+"SECOND.WP5")
				p := plan(t, raw)
				d, s := data(t, raw2)
				want := []string{"Hello Alice\n", "Hello Bob\n"}
				if id == "209" {
					want = []string{"FILLED Alice", "EMPTY Bob"}
				}
				for j, w := range want {
					r := result(t, p, d, s, j+1, w)
					pr, _ := r.Provenance()
					if id == "207" && len(pr.Accesses) != 1 {
						t.Fatal("field2 requested")
					}
					if id == "209" && (!pr.Conditional || pr.Blank != (j == 1)) {
						t.Fatal("branch")
					}
				}
				i, _ := image(t, raw, native.Primary)
				i2, _ := image(t, raw2, native.Secondary)
				if !bytes.Equal(i.Export(), raw) || !bytes.Equal(i2.Export(), raw2) {
					t.Fatal("native changed")
				}
			})
		}
	}
}
func TestOriginalPagePrimariesRefused(t *testing.T) {
	for _, run := range []string{"2026-10-29-advanced-03", "2026-10-29-advanced-04"} {
		p, s := program(t, fixture(t, run+"/CMD51-208/PRIMARY.WP5"))
		if q, e := body.Compile(p, s, body.DefaultLimits()); e == nil || q.Valid() {
			t.Fatal("PAGE208")
		}
		data(t, fixture(t, run+"/CMD51-208/SECOND.WP5"))
	}
	for _, run := range []string{"2026-10-29-history-01", "2026-10-29-history-02"} {
		for _, id := range []string{"216", "217"} {
			p, s := program(t, fixture(t, run+"/CMD51-"+id+"/PRIMARY.WP5"))
			if q, e := body.Compile(p, s, body.DefaultLimits()); e == nil || q.Valid() {
				t.Fatal("PAGE" + id)
			}
			data(t, fixture(t, run+"/CMD51-"+id+"/SECOND.WP5"))
		}
	}
}
