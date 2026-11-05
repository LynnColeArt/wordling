// Command producer emits lawful WP25 integration fixtures through the actual
// public document API. It is evidence tooling, not a new-document/product writer.
package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
)

type command struct {
	Gap        int
	Mode, Text string
}
type fixture struct {
	Name, Directory, Source, ReferenceFinal, ReferencePrint, ExpectedBody string
	Commands                                                              []command
}

func main() {
	flag.Parse()
	if e := run(); e != nil {
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
}

var output = flag.String("out", "internal/document/evidence/wp25/candidates", "fresh owned emission directory")

func digest(b []byte) string { s := sha256.Sum256(b); return hex.EncodeToString(s[:]) }
func write(path string, v any) error {
	b, e := json.MarshalIndent(v, "", "  ")
	if e != nil {
		return e
	}
	return os.WriteFile(path, append(b, '\n'), 0644)
}
func run() error {
	base := "docs/research/continuation/native-edits/runs/"
	fixtures := []fixture{
		{"ascii-modes", base + "wp23-a-modes-r1", "N0000.WP5", "N0002.WP5", "P0005.PRN", "61585963", []command{{1, "typeover", "X"}, {2, "insert", "Y"}}},
		{"bold-insert-g1", base + "wp23-a-boundaries-r1", "N0000.WP5", "N0001.WP5", "P0004.PRN", "4158c30cc34243c40cc444", []command{{1, "insert", "X"}}},
		{"bold-typeover-g2", base + "wp23-a-boundaries-r1", "N0030.WP5", "N0031.WP5", "P0034.PRN", "41c30cc35843c40cc444", []command{{2, "typeover", "X"}}},
		{"bold-typeover-g5", base + "wp23-a-boundaries-r1", "N0042.WP5", "N0043.WP5", "P0046.PRN", "41c30cc34243c40cc458", []command{{5, "typeover", "X"}}},
		{"two-pair-typeover-Q", base + "wp23-b-history-follow-repair-restore-r1", "N0001.WP5", "", "", "41c30cc3c40cc4c30cc3514243c40cc444", []command{{4, "typeover", "Q"}}},
	}
	out := filepath.Clean(*output)
	if !strings.HasPrefix(out, "internal/document/evidence/wp25/") {
		return fmt.Errorf("owned evidence output directory required")
	}
	if e := os.Mkdir(out, 0755); e != nil {
		return e
	}
	environment, e := os.ReadFile("docs/research/reference-environment/environment.json")
	if e != nil {
		return e
	}
	sources := map[string]string{}
	paths, e := filepath.Glob("internal/document/*.go")
	if e != nil {
		return e
	}
	paths = append(paths, "internal/document/evidence/wp25/producer/main.go", "internal/wp51/native.go")
	for _, p := range paths {
		b, e := os.ReadFile(p)
		if e != nil {
			return e
		}
		sources[p] = digest(b)
	}
	var plan []any
	for _, f := range fixtures {
		sourcePath := f.Directory + "/" + f.Source
		input, e := os.ReadFile(sourcePath)
		if e != nil {
			return e
		}
		d, e := document.Parse(input)
		if e != nil {
			return e
		}
		for _, c := range f.Commands {
			cursor, e := d.CursorAt(c.Gap)
			if e != nil {
				return e
			}
			var r document.EditResult
			if c.Mode == "insert" {
				r, e = d.InsertASCII(cursor, []byte(c.Text))
			} else {
				r, e = d.TypeoverASCII(cursor, []byte(c.Text))
			}
			if e != nil {
				return e
			}
			if !r.Changed {
				return fmt.Errorf("%s is not an edited candidate", f.Name)
			}
			d = r.Document
		}
		candidate, e := d.Export()
		if e != nil {
			return e
		}
		bodyOffset := int(candidate[4]) | int(candidate[5])<<8 | int(candidate[6])<<16 | int(candidate[7])<<24
		if hex.EncodeToString(candidate[bodyOffset:]) != f.ExpectedBody {
			return fmt.Errorf("%s wrong emitted body", f.Name)
		}
		dir := out + "/" + f.Name
		if e = os.Mkdir(dir, 0755); e != nil {
			return e
		}
		if e = os.WriteFile(dir+"/candidate.WP5", candidate, 0644); e != nil {
			return e
		}
		provenance := map[string]any{"rights": "project-authored scratch", "producer": "go run ./internal/document/evidence/wp25/producer; " + runtime.Version(), "source_sha256": digest(candidate), "description": f.Name + ": existing project-authored original fixture edited by real document public API; no new prefix construction", "loaded_source": sourcePath, "loaded_source_sha256": digest(input), "commands": f.Commands, "executing_go_sources": sources}
		if e = write(dir+"/provenance.json", provenance); e != nil {
			return e
		}
		expected := map[string]any{"schema_version": 1, "candidate_sha256": digest(candidate), "input_body_hex": f.ExpectedBody, "subsequent_edit": map[string]any{"command": "append-ascii-at-end", "text": "Z", "expected_body_hex": f.ExpectedBody + "5a"}, "environment_sha256": digest(environment)}
		reference := "pending two independent original controls; no candidate VM launch until sealed"
		if f.ReferencePrint != "" {
			p := f.Directory + "/" + f.ReferencePrint
			b, e := os.ReadFile(p)
			if e != nil {
				return e
			}
			abs, e := filepath.Abs(p)
			if e != nil {
				return e
			}
			expected["reference_print"] = map[string]any{"path": abs, "size": len(b), "sha256": digest(b)}
			reference = p
		}
		if e = write(dir+"/expectations.json", expected); e != nil {
			return e
		}
		plan = append(plan, map[string]any{"name": f.Name, "candidate_sha256": digest(candidate), "loaded_source": sourcePath, "loaded_source_sha256": digest(input), "commands": f.Commands, "body_hex": f.ExpectedBody, "original_subsequent_body_hex": f.ExpectedBody + "5a", "reference_print": reference, "fresh_candidate_repetitions": 2, "source_final_comparison": f.ReferenceFinal, "native_policy": "only checked packet6 bit3 may differ from original prefix; all other owned bytes copied from loaded input"})
	}
	return write(out+"/sealed-plan.json", map[string]any{"status": "offline emitted; original interoperability unrun", "scope": "five real Go edited candidates;8 original candidate runs plus2 original two-pair controls then2 changed two-pair candidate runs", "go_version": runtime.Version(), "source_hashes": sources, "cases": plan})
}
