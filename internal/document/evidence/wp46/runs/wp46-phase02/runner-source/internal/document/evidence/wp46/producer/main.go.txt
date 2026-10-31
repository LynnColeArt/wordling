// Explicit isolated evidence binary; the nested module keeps this package out of
// root package discovery. Production document.New performs no filesystem IO.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
	"os"
	"path/filepath"
)

var out = flag.String("out", "", "fresh candidate output directory")
var verify = flag.String("verify", "", "actual native to consume")
var reedit = flag.String("reedit-out", "", "fresh stopped-output second Go edit")
var required = flag.Bool("require-preprint", false, "require exact selected pre-print cache and counter")

func hash(b []byte) string { s := sha256.Sum256(b); return hex.EncodeToString(s[:]) }
func must(e error) {
	if e != nil {
		panic(e)
	}
}
func absentWrite(p string, b []byte) {
	f, e := os.OpenFile(p, os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0644)
	must(e)
	_, e = f.Write(b)
	must(e)
	must(f.Close())
}
func jsonBytes(v any) []byte {
	b, e := json.MarshalIndent(v, "", "  ")
	must(e)
	return append(b, '\n')
}
func noOriginal(d *document.Document) {
	b, e := d.OriginalExport()
	if b != nil || e == nil || !d.Birth().IsNew() {
		panic("New lineage/original")
	}
}
func main() {
	flag.Parse()
	if *verify != "" {
		consume()
		return
	}
	if *out == "" {
		panic("explicit fresh out required")
	}
	must(os.Mkdir(*out, 0755))
	d, e := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	must(e)
	birth := d.Birth()
	rev := d.Revision()
	noOriginal(d)
	empty, e := d.Export()
	must(e)
	absentWrite(filepath.Join(*out, "empty.WP5"), empty)
	c, e := d.CursorAt(0)
	must(e)
	r, e := d.InsertASCII(c, []byte("G43ASCII"))
	must(e)
	noOriginal(r.Document)
	if r.Document.Birth() != birth || r.Document.Revision() == rev || r.Cursor.Gap() != 8 {
		panic("real first edit identity")
	}
	ascii, e := r.Document.Export()
	must(e)
	absentWrite(filepath.Join(*out, "ascii.WP5"), ascii)
	report := map[string]any{"producer": "real document.New then public InsertASCII", "runtime_native_input": "none", "config": document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter}, "new_birth_preserved": true, "lifetime_NoLoadedOriginal": true, "first_ascii_cursor_gap": 8, "fresh_revision": true, "classes": []any{map[string]any{"name": "empty", "bytes": len(empty), "sha256": hash(empty), "operations": []string{"New closed profile", "Export empty"}}, map[string]any{"name": "ascii", "bytes": len(ascii), "sha256": hash(ascii), "operations": []string{"New closed profile", "InsertASCII G43ASCII at gap0"}}}}
	absentWrite(filepath.Join(*out, "provenance.json"), jsonBytes(report))
	fmt.Print(string(jsonBytes(report)))
}
func consume() {
	raw, e := os.ReadFile(*verify)
	must(e)
	d, e := document.Parse(raw)
	must(e)
	same, e := d.Export()
	must(e)
	if !bytes.Equal(same, raw) || !d.Birth().IsLoaded() {
		panic("actual Loaded no-edit")
	}
	im, e := wp51.Parse(raw)
	must(e)
	info := im.Inspect()
	body, ok := im.Bytes(info.Body)
	if !ok {
		panic("body")
	}
	q := d.CheckMutation()
	v := map[string]any{"bytes": len(raw), "sha256": hash(raw), "inspection": info, "body_hex": hex.EncodeToString(body), "admitted": q == nil, "exact_no_edit": true, "origin_loaded": true}
	if q != nil {
		v["refusal"] = q.Error()
	}
	if *required {
		if q != nil {
			panic(q)
		}
		found15, found6 := false, false
		for _, p := range info.Packets {
			if p.Type == 15 {
				b, _ := im.Bytes(p.Data)
				if b[21] != 0xe7 || b[22] != 0x24 {
					panic("required e724 descriptor cache")
				}
				found15 = true
			}
			if p.Type == 6 {
				b, _ := im.Bytes(p.Data)
				if b[8] != 1 {
					panic("required counter01")
				}
				found6 = true
			}
		}
		if !found15 || !found6 {
			panic("required owners")
		}
	}
	if *reedit != "" {
		if q != nil {
			panic(q)
		}
		c, e := d.CursorAt(d.TokenCount())
		must(e)
		r, e := d.InsertASCII(c, []byte("Q"))
		must(e)
		original, e := r.Document.OriginalExport()
		must(e)
		if !bytes.Equal(original, raw) || r.Document.Birth() != d.Birth() || r.Document.Revision() == d.Revision() || r.Cursor.Gap() != d.TokenCount()+1 || r.Document.CheckMutation() != nil {
			panic("second edit lineage/gap/revision/admission")
		}
		b, e := r.Document.Export()
		must(e)
		absentWrite(*reedit, b)
		v["second_real_edit"] = map[string]any{"command": "public EOF InsertASCII Q", "sha256": hash(b), "OriginalExport_exact": true, "same_loaded_birth": true, "fresh_revision": true, "gap": r.Cursor.Gap()}
	}
	fmt.Print(string(jsonBytes(v)))
}
