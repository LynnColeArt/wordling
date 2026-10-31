// Producer executes the real public document APIs over pinned lawful original
// scratch files. No native header/prefix/body is constructed by this tool.
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
	"runtime"
	"strings"
)

var verifyInput = flag.String("verify", "", "actual native file to check read-only")
var reeditOutput = flag.String("reedit-out", "", "new owned second-public-edit output")
var out = flag.String("out", "internal/document/evidence/wp44/candidates", "new owned emission directory")

func sha(b []byte) string { s := sha256.Sum256(b); return hex.EncodeToString(s[:]) }
func must(e error) {
	if e != nil {
		panic(e)
	}
}
func read(p string) []byte { b, e := os.ReadFile(p); must(e); return b }
func write(p string, v any) {
	b, e := json.MarshalIndent(v, "", "  ")
	must(e)
	must(os.WriteFile(p, append(b, '\n'), 0644))
}

type state struct {
	d      *document.Document
	c      document.Cursor
	h      document.History
	trace  []any
	source string
}

func load(path string) *state {
	d, e := document.Parse(read(path))
	must(e)
	h, e := document.NewHistory(d)
	must(e)
	c, e := d.CursorAt(0)
	must(e)
	return &state{d: d, c: c, h: h, source: path}
}
func (s *state) body() string {
	raw, e := s.d.Export()
	must(e)
	i, e := wp51.Parse(raw)
	must(e)
	b, ok := i.Bytes(i.Inspect().Body)
	if !ok {
		panic("validated body missing")
	}
	return hex.EncodeToString(b)
}
func (s *state) at(g int, reveal bool) {
	c, e := s.d.CursorAt(g)
	must(e)
	s.c = c.WithReveal(reveal)
	s.trace = append(s.trace, map[string]any{"command": "explicit token gap/view", "gap": g, "reveal": reveal})
}
func (s *state) adopt(r document.Deletion, command string) {
	before, e := s.d.Export()
	must(e)
	after, e := r.Document().Export()
	must(e)
	s.d, s.c, s.h = r.Document(), r.Cursor(), r.History()
	s.trace = append(s.trace, map[string]any{"command": command, "input_sha256": sha(before), "output_sha256": sha(after), "gap": s.c.Gap(), "reveal": s.c.Reveal(), "kind": r.Kind(), "applied": r.Applied(), "body_changed": r.BodyChanged(), "native_changed": r.NativeChanged(), "stored_fragments": s.h.Count(), "count_known": s.h.CountKnown()})
}
func (s *state) del(direction document.DeleteDirection) {
	r, e := s.d.Delete(s.c, direction, s.h)
	must(e)
	if r.Pending() {
		s.trace = append(s.trace, map[string]any{"question": r.Prompt(), "answer": "Yes"})
		r, e = s.d.AnswerDeletion(s.h, r, document.Yes)
		must(e)
	}
	s.adopt(r, fmt.Sprint("Delete direction ", direction))
}
func (s *state) block(start, end int) {
	a, e := s.d.CursorAt(start)
	must(e)
	b, e := s.d.CursorAt(end)
	must(e)
	r, e := s.d.DeleteBlock(a.WithReveal(true), b.WithReveal(true), s.h)
	must(e)
	s.trace = append(s.trace, map[string]any{"command": "forward Reveal block", "start": start, "end": end, "question": r.Prompt(), "answer": "Yes"})
	r, e = s.d.AnswerDeletion(s.h, r, document.Yes)
	must(e)
	s.adopt(r, "confirmed block")
}
func (s *state) browse(previous int) {
	p, e := s.h.Open(s.c)
	must(e)
	var rows []string
	for i := 0; i <= previous; i++ {
		z, e := p.Present(0, 0, false)
		must(e)
		v, e := p.Present(0, z.TotalTokens, false)
		must(e)
		var b strings.Builder
		for _, x := range v.Elements {
			b.WriteString(x.Text)
		}
		rows = append(rows, b.String())
		if i < previous {
			p, e = p.Previous()
			must(e)
		}
	}
	s.h, e = s.h.CancelPreview(p)
	must(e)
	s.trace = append(s.trace, map[string]any{"command": "F1/Previous/F1 cancel", "previous": previous, "derived_whole_rows": rows, "native_write": false})
}
func (s *state) restore() {
	p, e := s.h.Open(s.c)
	must(e)
	r, e := s.d.Restore(s.h, p)
	must(e)
	s.adopt(r, "F1/newest Restore1")
}
func (s *state) marker() {
	r, e := s.d.InsertASCII(s.c, []byte("X"))
	must(e)
	h, e := s.h.AfterEdit(r)
	must(e)
	s.d, s.c, s.h = r.Document, r.Cursor, h
	s.trace = append(s.trace, map[string]any{"command": "InsertASCII X; real AfterEdit receipt", "gap": s.c.Gap(), "history_qualified": s.h.Qualified()})
}
func (s *state) seed(reveal bool, gap int) {
	s.at(0, reveal)
	s.del(document.ForwardDelete)
	s.browse(3)
	c, e := s.c.Move(1)
	must(e)
	s.c = c
	s.h, e = s.h.Separate(document.RightBoundary)
	must(e)
	s.trace = append(s.trace, map[string]any{"command": "actual Right grouping separator"})
	s.at(gap, reveal)
}

func (s *state) insert(text string, over bool) {
	before, e := s.d.Export()
	must(e)
	var r document.EditResult
	if over {
		r, e = s.d.TypeoverASCII(s.c, []byte(text))
	} else {
		r, e = s.d.InsertASCII(s.c, []byte(text))
	}
	must(e)
	s.d, s.c = r.Document, r.Cursor
	s.trace = append(s.trace, map[string]any{"command": "ASCII", "typeover": over, "text": text, "input_sha256": sha(before), "gap_after": s.c.Gap(), "changed": r.Changed})
	if s.d.CheckMutation() != nil {
		panic("candidate not requalified")
	}
}
func (s *state) prependSeed() {
	s.at(0, false)
	s.insert("S", false)
	h, e := document.NewHistory(s.d)
	must(e)
	s.h = h
	s.trace = append(s.trace, map[string]any{"command": "new history after real prepend S; same seeded input shape"})
}

type recipe struct {
	name, source, referenceFinal, referencePrint string
	run                                          func(*state)
}

func main() {
	flag.Parse()
	if *verifyInput != "" {
		must(verify(*verifyInput, *reeditOutput))
		return
	}
	must(run())
}
func run() error {
	if !strings.HasPrefix(filepath.Clean(*out), "internal/document/evidence/wp44/") {
		return fmt.Errorf("owned output required")
	}
	must(os.Mkdir(*out, 0755))
	base := "docs/research/continuation/native-edits/runs/"
	forty := "docs/research/continuation/code-pair-history/runs/"
	source := func(grammar string) string {
		return "docs/research/continuation/resaved-prefix/runs/w42-" + grammar + "-disabled/r1/W42G3.WP5"
	}
	var recipes []recipe
	add := func(name, grammar, reference, print string, fn func(*state)) {
		recipes = append(recipes, recipe{name, source(grammar), reference, print, fn})
	}
	// Every source is an exact approved42 original; all transformations are public APIs.
	for _, gap := range []int{0, 2, 4} {
		g := gap
		add(fmt.Sprint("ascii-insert-", g), "ascii", "", "", func(s *state) { s.at(g, false); s.insert("X", false) })
	}
	for _, gap := range []int{1, 2, 4, 5} {
		g := gap
		add(fmt.Sprint("code-typeover-", g), "one-bold", "", "", func(s *state) { s.at(g, true); s.insert("XY", true) })
	}
	add("two-pair-insert", "two-bold", "", "", func(s *state) { s.at(s.d.TokenCount(), false); s.insert("X", false) })
	for _, view := range []bool{false, true} {
		for _, dir := range []document.DeleteDirection{document.ForwardDelete, document.Backspace} {
			for _, target := range []int{1, 4} {
				v, di, g := view, dir, target
				if di == document.Backspace {
					g++
				}
				add(fmt.Sprintf("direct-%t-%d-%d", v, di, g), "one-bold", base+"wp23-b-deletions-r1/N0001.WP5", base+"wp23-b-deletions-r1/P0004.PRN", func(s *state) { s.prependSeed(); s.seed(v, g); s.del(di) })
			}
		}
	}
	add("opening-repair", "one-bold", base+"wp23-a-blocks-r1/N0001.WP5", base+"wp23-a-blocks-r1/P0004.PRN", func(s *state) { s.block(1, 2) })
	add("closing-repair", "one-bold", base+"wp23-a-blocks-r1/N0025.WP5", base+"wp23-a-blocks-r1/P0028.PRN", func(s *state) { s.prependSeed(); s.seed(true, 4); s.block(4, 5) })
	add("attributed-delete", "one-bold", base+"wp23-a-blocks-r1/N0049.WP5", base+"wp23-a-blocks-r1/P0052.PRN", func(s *state) { s.block(1, 5) })
	add("attributed-restore", "one-bold", base+"wp23-a-blocks-r1/N0001.WP5", base+"wp23-a-blocks-r1/P0004.PRN", func(s *state) { s.block(1, 5); s.restore() })
	add("plain-restore-marker", "one-bold", forty+"wp40-direct-normal-delete-on-r1/N0001.WP5", forty+"wp40-direct-normal-delete-on-r1/P0004.PRN", func(s *state) {
		s.prependSeed()
		s.seed(false, 1)
		s.del(document.ForwardDelete)
		s.browse(3)
		s.restore()
		s.browse(3)
		s.marker()
	})
	add("opening-literal-empty-restore", "one-bold", "", "", func(s *state) { s.block(1, 2); s.browse(1); s.restore() })
	add("closing-literal-empty-restore", "one-bold", "", "", func(s *state) { s.prependSeed(); s.seed(true, 4); s.block(4, 5); s.browse(3); s.restore() })

	sources := map[string]string{}
	paths, e := filepath.Glob("internal/document/*.go")
	must(e)
	paths = append(paths, "internal/document/evidence/wp44/producer/main.go", "internal/document/evidence/wp44/producer/verify.go", "internal/wp51/native.go")
	for _, p := range paths {
		sources[p] = sha(read(p))
	}
	var cases []any
	unique := map[string]string{}
	var uniqueCases []any
	for _, r := range recipes {
		s := load(r.source)
		r.run(s)
		raw, e := s.d.Export()
		must(e)
		var referenceRaw []byte
		referenceExact := false
		if r.referenceFinal != "" {
			referenceRaw = read(r.referenceFinal)
			referenceImage, e := wp51.Parse(referenceRaw)
			must(e)
			referenceBody, ok := referenceImage.Bytes(referenceImage.Inspect().Body)
			if !ok || s.body() != hex.EncodeToString(referenceBody) {
				return fmt.Errorf("%s original endpoint body differs", r.name)
			}
			referenceExact = bytes.Equal(raw, referenceRaw)
		}
		hash := sha(raw)
		alias, exists := unique[hash]
		if exists {
			if !bytes.Equal(raw, read(*out+"/"+alias+"/candidate.WP5")) {
				return fmt.Errorf("digest alias without whole bytes")
			}
		} else {
			alias = r.name
			unique[hash] = alias
		}
		dir := *out + "/" + r.name
		must(os.Mkdir(dir, 0755))
		must(os.WriteFile(dir+"/candidate.WP5", raw, 0644))
		provenance := map[string]any{"rights": "project-authored scratch", "producer": "go run ./internal/document/evidence/wp44/producer; " + runtime.Version(), "source_sha256": hash, "description": r.name + ": actual immutable document/history APIs; no native construction", "loaded_source": r.source, "loaded_source_sha256": sha(read(r.source)), "executing_go_sources": sources, "commands": s.trace, "final_gap": s.c.Gap(), "final_reveal": s.c.Reveal(), "source_reference_endpoint": r.referenceFinal, "whole_native_reference_equality": referenceExact, "reference_prefix_role": "Independent original endpoint may retain a different admitted font-cache variant; Go preserves OWNED input prefix. No reference normalization or body-only native alias."}
		write(dir+"/provenance.json", provenance)
		expected := map[string]any{"schema_version": 1, "candidate_sha256": hash, "input_body_hex": s.body(), "subsequent_edit": map[string]any{"command": "append-ascii-at-end", "text": "Z", "expected_body_hex": s.body() + "5a"}, "environment_sha256": sha(read("docs/research/reference-environment/environment.json")), "reference_print": r.referencePrint}
		write(dir+"/expectations.json", expected)
		row := map[string]any{"name": r.name, "candidate_sha256": hash, "bytes": len(raw), "body_hex": s.body(), "gap": s.c.Gap(), "reveal": s.c.Reveal(), "whole_byte_alias_of": alias, "reference_final": r.referenceFinal, "reference_print": r.referencePrint, "provenance_sha256": sha(read(dir + "/provenance.json")), "expectations_sha256": sha(read(dir + "/expectations.json"))}
		cases = append(cases, row)
		if !exists {
			uniqueCases = append(uniqueCases, row)
		}
	}
	write(*out+"/sealed-plan.json", map[string]any{"status": "sealed actual Go outputs; original interoperability NOT RUN", "source_hashes": sources, "cases": cases, "unique_whole_byte_candidates": uniqueCases, "fresh_repetitions": 2, "candidate_guest_count": len(uniqueCases) * 2, "guest_count": "UNSEALED until exact missing logical controls identified", "alias_rule": "exact whole native byte and SHA equality with separate per-command provenance, never body-only", "no_full_M1_claim": true})
	return nil
}
