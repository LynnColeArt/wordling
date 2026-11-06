// Command admission_probe reports which captured original resave stages the
// current document package admits for mutation. It is read-only: it parses each
// native witness through the public API, calls CheckMutation and prints the
// outcome, so WP80's admission work is driven by actual corpus results rather
// than by an assumed shape. No native bytes are written.
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"

	"github.com/lynncoleart/wordling/internal/document"
)

type row struct {
	Path         string `json:"path"`
	Size         int    `json:"size"`
	Prefix       int    `json:"prefix"`
	Body         int    `json:"body"`
	Blocks       int    `json:"blocks"`
	Packets      int    `json:"packets"`
	Tokens       int    `json:"tokens"`
	Catalogue    bool   `json:"catalogue"`
	CatalogueErr string `json:"catalogue_error,omitempty"`
	Opaque       int    `json:"opaque_tokens"`
	Admitted     bool   `json:"admitted"`
	Refusal      string `json:"refusal,omitempty"`
}

func main() {
	roots := os.Args[1:]
	if len(roots) == 0 {
		roots = []string{"docs/research/continuation/resaved-prefix/runs"}
	}
	var rows []row
	for _, root := range roots {
		var paths []string
		err := filepath.Walk(root, func(p string, info os.FileInfo, err error) error {
			if err != nil || info.IsDir() {
				return nil
			}
			if filepath.Ext(p) == ".WP5" {
				paths = append(paths, p)
			}
			return nil
		})
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
		sort.Strings(paths)
		for _, p := range paths {
			raw, err := os.ReadFile(p)
			if err != nil {
				fmt.Fprintln(os.Stderr, err)
				os.Exit(1)
			}
			r := row{Path: p, Size: len(raw)}
			d, err := document.Parse(raw)
			if err != nil {
				r.Refusal = "parse: " + err.Error()
				rows = append(rows, r)
				continue
			}
			r.Tokens = d.TokenCount()
			// Read/Reveal reachability is independent of mutation admission: the
			// catalogue inspects complete owners and never writes.
			if insp, err := document.InspectRevealCatalogue(d, d.Revision(), 0, d.TokenCount()); err == nil {
				r.Catalogue = true
				for _, e := range insp.Elements {
					if e.Kind == document.Opaque {
						r.Opaque++
					}
				}
			} else {
				r.CatalogueErr = err.Error()
			}
			if err := d.CheckMutation(); err != nil {
				r.Refusal = err.Error()
			} else {
				r.Admitted = true
			}
			rows = append(rows, r)
		}
	}
	out, _ := json.MarshalIndent(rows, "", " ")
	fmt.Println(string(out))
}
