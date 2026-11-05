package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
	"os"
)

// Independent actual public consumer invoked on stopped original exports. No
// prefix construction/normalization and no duplicate parser.
func verify(path, output string) error {
	raw, e := os.ReadFile(path)
	if e != nil {
		return e
	}
	d, e := document.Parse(raw)
	if e != nil {
		return e
	}
	exact, e := d.Export()
	if e != nil || !bytes.Equal(raw, exact) {
		return fmt.Errorf("reader no-edit mismatch")
	}
	i, e := wp51.Parse(raw)
	if e != nil {
		return e
	}
	info := i.Inspect()
	body, ok := i.Bytes(info.Body)
	if !ok {
		return fmt.Errorf("body missing")
	}
	q := d.CheckMutation()
	v := map[string]any{"path": path, "sha256": sha(raw), "bytes": len(raw), "exact_no_edit": true, "inspection": info, "body_hex": fmt.Sprintf("%x", body), "admitted": q == nil}
	if q != nil {
		v["refusal"] = q.Error()
	}
	if output != "" {
		if q != nil {
			return fmt.Errorf("required pre-print re-edit refused: %w", q)
		}
		c, e := d.CursorAt(d.TokenCount())
		if e != nil {
			return e
		}
		r, e := d.InsertASCII(c, []byte("Q"))
		if e != nil {
			return e
		}
		orig, e := r.Document.OriginalExport()
		if e != nil || !bytes.Equal(orig, raw) || r.Cursor.Gap() != d.TokenCount()+1 || r.Document.Revision() == d.Revision() || r.Document.CheckMutation() != nil {
			return fmt.Errorf("real second Go edit lineage/gap/admission")
		}
		candidate, e := r.Document.Export()
		if e != nil {
			return e
		}
		if e = os.WriteFile(output, candidate, 0644); e != nil {
			return e
		}
		v["second_real_edit"] = map[string]any{"command": "public InsertASCII Q at EOF", "output": output, "sha256": sha(candidate), "OriginalExport_exact": true, "gap": r.Cursor.Gap(), "fresh_revision": true}
	}
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	return enc.Encode(v)
}
