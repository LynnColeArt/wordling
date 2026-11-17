package layout_test

import (
	"bytes"
	"crypto/sha256"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
)

func TestAdvanceCapturedLayout(t *testing.T) {
	dir := os.Getenv("WORDLING_ADVANCE_REFERENCE_DIR")
	if dir == "" {
		t.Skip("historical Advance oracle unavailable: set WORDLING_ADVANCE_REFERENCE_DIR explicitly; synthetic tests are not DOS parity")
	}
	if !filepath.IsAbs(dir) {
		t.Fatal("reference directory must be absolute")
	}
	hashes := map[string]string{
		"BOUNDARY.WP": "bd8e615cd5fd5baea21e953422330d834c021c960e067c164f83b2e3b17f8622",
		"HORIZ.WP":    "67caf25abae5a7dd73055367f93b59cfe37564b3f5bad3e0a792e54f72289957",
		"HORIZ.PRN":   "a134734af2dd10d2d202234e6e84002e2bba37c9029f3fd3251581afd1b20ba3",
	}
	verified := make(map[string][]byte)
	for name, want := range hashes {
		raw, err := os.ReadFile(filepath.Join(dir, name))
		if err != nil {
			t.Fatal(err)
		}
		if fmt.Sprintf("%x", sha256.Sum256(raw)) != want {
			t.Fatalf("historical reference digest mismatch: %s", name)
		}
		verified[name] = raw
	}
	read := func(name string) []byte {
		t.Helper()
		data, ok := verified[name]
		if !ok {
			t.Fatalf("unbound reference %s", name)
		}
		return data
	}

	for _, tc := range []struct {
		name                    string
		screenColumn            int
		baseline, printedColumn float64
	}{
		{"HORIZ", 2, 1, 4.2},
		{"BOUNDARY", 7, 10, 1.7},
	} {
		t.Run(tc.name, func(t *testing.T) {
			doc, err := document.Parse(read(tc.name + ".WP"))
			if err != nil {
				t.Fatal(err)
			}
			projected, err := layout.FromDocument(doc, matchedSettings())
			if err != nil {
				t.Fatal(err)
			}
			gap := doc.TokenCount()
			row, column, ok := projected.PositionAt(gap)
			if !ok || column != tc.screenColumn || projected.Lines[row].Page != 1 {
				t.Fatalf("screen row=%d column=%d known=%t", row, column, ok)
			}
			baseline, _ := projected.PrintedBaseline(gap)
			printed, _ := projected.PrintedColumn(gap)
			if math.Abs(baseline-tc.baseline) > 1e-9 || math.Abs(printed-tc.printedColumn) > 1e-9 {
				t.Fatalf("baseline=%.6f column=%.6f", baseline, printed)
			}
			pages, err := layout.StandardPages(doc, matchedSettings())
			if err != nil || len(pages) != 1 {
				t.Fatalf("pages=%d err=%v", len(pages), err)
			}
			if tc.name == "HORIZ" {
				if stream := layout.StandardPrint(pages); !bytes.Equal(stream, read("HORIZ.PRN")) {
					t.Fatalf("horizontal printer bytes differ: %q", stream)
				}
			} else {
				// The DOS capture gives baselines but has no Down printer stream.
				lines := pages[0].TextLines()
				if lines[57] != "          bottom" || lines[60] != "                Z" {
					t.Fatalf("bottom row=%q clamped row=%q", lines[57], lines[60])
				}
			}
		})
	}
}

// These documents are authored through public APIs, not copied oracle bytes.
func syntheticAdvance(t *testing.T, kind string) *document.Document {
	t.Helper()
	d, err := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if err != nil {
		t.Fatal(err)
	}
	cursor := func() document.Cursor {
		c, e := d.CursorAt(d.TokenCount())
		if e != nil {
			t.Fatal(e)
		}
		return c
	}
	apply := func(r document.EditResult, e error) {
		if e != nil {
			t.Fatal(e)
		}
		d = r.Document
	}
	text := func(s string) { apply(d.InsertASCII(cursor(), []byte(s))) }
	advance := func(m document.AdvanceMode, value int) {
		apply(d.InsertAdvance(cursor(), m, 0, value*document.UnitsPerInch))
	}
	switch kind {
	case "horizontal":
		advance(document.AdvancePosition, 3)
		text("A")
		advance(document.AdvanceRight, 1)
		text("B")
	case "boundary":
		text("top")
		for i := 0; i < 51; i++ {
			apply(d.InsertHardReturn(cursor()))
		}
		text("bottom")
		advance(document.AdvanceDown, 3)
		text("Z")
	case "wrapped":
		advance(document.AdvanceRight, 1)
		text(strings.Repeat("a", 60) + " betaZ")
	default:
		t.Fatal("unknown synthetic case")
	}
	return d
}

func TestAdvanceSyntheticLayout(t *testing.T) {
	for _, kind := range []string{"horizontal", "boundary", "wrapped"} {
		t.Run(kind, func(t *testing.T) {
			d := syntheticAdvance(t, kind)
			raw, err := d.Export()
			if err != nil {
				t.Fatal(err)
			}
			reopened, err := document.Parse(raw)
			if err != nil {
				t.Fatal(err)
			}
			for _, doc := range []*document.Document{d, reopened} {
				l, err := layout.FromDocument(doc, matchedSettings())
				if err != nil {
					t.Fatal(err)
				}
				pages, err := layout.StandardPages(doc, matchedSettings())
				if err != nil || len(pages) != 1 {
					t.Fatalf("pages=%d error=%v", len(pages), err)
				}
				rows := bytes.Split(layout.StandardPrint(pages), []byte("\r\n"))
				if kind == "wrapped" {
					if !bytes.Equal(rows[6], []byte(strings.Repeat(" ", 20)+strings.Repeat("a", 55))) || !bytes.Equal(rows[7], []byte("          aaaaa betaZ\r")) {
						t.Fatalf("wrap rows: %q / %q", rows[6], rows[7])
					}
					continue
				}
				gap := doc.TokenCount()
				_, column, ok := l.PositionAt(gap)
				baseline, bok := l.PrintedBaseline(gap)
				printed, pok := l.PrintedColumn(gap)
				wantCol, wantBase, wantPrinted := 2, 1.0, 4.2
				if kind == "boundary" {
					wantCol, wantBase, wantPrinted = 7, 10, 1.7
					if !bytes.Equal(rows[57], []byte("          bottom")) || !bytes.Equal(rows[60], []byte("                Z\r")) {
						t.Fatalf("boundary print rows: %q / %q", rows[57], rows[60])
					}
				}
				if !ok || !bok || !pok || column != wantCol || math.Abs(baseline-wantBase) > 1e-9 || math.Abs(printed-wantPrinted) > 1e-9 {
					t.Fatalf("column=%d baseline=%g printed=%g", column, baseline, printed)
				}
			}
		})
	}
}
