// Command reopen exercises the actual document API on original post-save native
// outputs. Read-only success and fresh mutation admission are distinct results.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"github.com/lynncoleart/wordling/internal/document"
	"os"
)

func main() {
	if e := run(); e != nil {
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
}
func run() error {
	var rows []any
	for _, path := range os.Args[1:] {
		raw, e := os.ReadFile(path)
		if e != nil {
			return e
		}
		before := bytes.Clone(raw)
		d, e := document.Parse(raw)
		if e != nil {
			return fmt.Errorf("%s: %w", path, e)
		}
		out, e := d.Export()
		if e != nil || !bytes.Equal(out, before) {
			return fmt.Errorf("%s: non-lossless document reopen: %v", path, e)
		}
		sum := sha256.Sum256(raw)
		admission := "admitted"
		if e = d.CheckMutation(); e != nil {
			admission = e.Error()
		}
		// Confirm normal/Reveal projections share source-token spans for all original
		// outputs in this small ASCII/Bold corpus, independently of terminal cells.
		c, e := d.CursorAt(0)
		if e != nil {
			return e
		}
		n, e := c.Present(0, d.TokenCount())
		if e != nil {
			return e
		}
		r, e := c.WithReveal(true).Present(0, d.TokenCount())
		if e != nil {
			return e
		}
		for i := range n.Elements {
			if n.Elements[i].Span != r.Elements[i].Span || n.Elements[i].TokenIndex != r.Elements[i].TokenIndex {
				return fmt.Errorf("%s: view identity drift", path)
			}
		}
		rows = append(rows, map[string]any{"path": path, "size": len(raw), "sha256": hex.EncodeToString(sum[:]), "document_reopen_lossless": true, "shared_token_spans": true, "tokens": d.TokenCount(), "mutation_admission": admission})
	}
	return json.NewEncoder(os.Stdout).Encode(map[string]any{"scope": "actual document.Parse/Export and shared token projections on original outputs; separate strict mutation admission; not whole M1", "files": rows})
}
