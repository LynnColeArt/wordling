// Read-only WP51 research probe. No mutation/history/constructor/publication API.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
	"os"
)

type Row struct {
	Path                                         string
	Bytes                                        int
	SHA256                                       string
	Parsed, ExportExact, OriginalExact, Admitted bool
	NativeError, Refusal                         string
	Failure                                      *document.Failure
	Inspection                                   wp51.Inspection
	BodyHex                                      string
}

func main() {
	if len(os.Args) < 2 || len(os.Args) > 129 {
		panic("1..128 immutable native paths required")
	}
	rows := []Row{}
	for _, path := range os.Args[1:] {
		st, e := os.Stat(path)
		if e != nil || !st.Mode().IsRegular() || st.Size() > 65536 {
			panic("bounded regular native input required: " + path)
		}
		raw, e := os.ReadFile(path)
		if e != nil {
			panic(e)
		}
		if len(raw) > 65536 {
			panic("input grew beyond budget")
		}
		sum := sha256.Sum256(raw)
		r := Row{Path: path, Bytes: len(raw), SHA256: hex.EncodeToString(sum[:])}
		d, e := document.Parse(raw)
		if e != nil {
			r.NativeError = e.Error()
			rows = append(rows, r)
			continue
		}
		r.Parsed = true
		out, e := d.Export()
		if e != nil {
			panic(e)
		}
		r.ExportExact = bytes.Equal(out, raw)
		out, e = d.OriginalExport()
		if e != nil {
			panic(e)
		}
		r.OriginalExact = bytes.Equal(out, raw)
		image, e := wp51.Parse(raw)
		if e != nil {
			panic(e)
		}
		r.Inspection = image.Inspect()
		body, ok := image.Bytes(r.Inspection.Body)
		if !ok {
			panic("actual native body span")
		}
		r.BodyHex = hex.EncodeToString(body)
		e = d.CheckMutation()
		r.Admitted = e == nil
		if e != nil {
			r.Refusal = e.Error()
			r.Failure, _ = e.(*document.Failure)
		}
		rows = append(rows, r)
	}
	data, e := json.MarshalIndent(rows, "", "  ")
	if e != nil {
		panic(e)
	}
	fmt.Println(string(data))
}
