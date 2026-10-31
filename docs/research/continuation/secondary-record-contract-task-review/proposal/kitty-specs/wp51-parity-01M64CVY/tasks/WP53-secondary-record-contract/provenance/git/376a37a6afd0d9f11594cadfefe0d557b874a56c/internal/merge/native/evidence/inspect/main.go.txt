// Public-API evidence witness only. This tool reads the immutable provenance
// manifest and original scratch exports; it does not decode a second native IR.
package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	n "github.com/lynncoleart/wordling/internal/merge/native"
	"os"
	"path/filepath"
)

func must(e error) {
	if e != nil {
		panic(e)
	}
}
func bounds(s n.Span) any {
	v, ok := s.Bounds()
	if !ok {
		return nil
	}
	return v
}
func main() {
	if len(os.Args) != 3 {
		panic("usage: inspect REPO_ROOT ORIGINALS_JSON")
	}
	root := os.Args[1]
	data, e := os.ReadFile(os.Args[2])
	must(e)
	var catalogue struct{ Files []struct{ Path, Role string } }
	must(json.Unmarshal(data, &catalogue))
	var results []any
	for _, row := range catalogue.Files {
		raw, e := os.ReadFile(filepath.Join(root, row.Path))
		must(e)
		im, e := n.Parse(raw, n.DefaultLimits())
		must(e)
		role := map[string]n.Role{"Primary": n.Primary, "Secondary": n.Secondary, "Result": n.Result}[row.Role]
		v, e := im.View(role)
		must(e)
		i, _ := v.Inspect()
		sum := sha256.Sum256(raw)
		tokens := []any{}
		commands := []any{}
		records := []any{}
		findings := []any{}
		for _, t := range i.Tokens {
			b, ok := v.Bytes(t.Raw)
			if !ok {
				panic("token source")
			}
			tokens = append(tokens, map[string]any{"span": bounds(t.Raw), "hex": hex.EncodeToString(b), "kind": t.Kind, "code": t.Code})
		}
		for _, c := range i.Commands {
			operand, _ := v.Bytes(c.Operand.Data)
			commands = append(commands, map[string]any{"kind": c.Kind, "function": bounds(c.Function), "payload": bounds(c.Payload), "operand": bounds(c.Operand.Data), "operand_hex": hex.EncodeToString(operand), "tilde": bounds(c.Operand.Terminator), "raw_count": c.RawCount, "has_raw_count": c.HasRawCount, "match": c.Match})
		}
		for _, r := range i.Records {
			fields := []any{}
			interstitial := []any{}
			for _, f := range r.Fields {
				b, _ := v.Bytes(f.Content)
				fields = append(fields, map[string]any{"ordinal": f.Ordinal, "content": bounds(f.Content), "hex": hex.EncodeToString(b), "end_field": bounds(f.EndField), "documented_HR_convention": bounds(f.Separator), "genuinely_empty": f.Empty, "ASCII_spaces_only": f.WhitespaceOnly, "plainASCII": f.PlainASCII})
			}
			for _, s := range r.Interstitial {
				interstitial = append(interstitial, bounds(s))
			}
			records = append(records, map[string]any{"ordinal": r.Ordinal, "raw": bounds(r.Raw), "raw_stored_count": r.StoredCount, "end_record": bounds(r.EndRecord), "tail": bounds(r.Tail), "fields": fields, "owned_unresolved_interstitial": interstitial})
		}
		for _, f := range i.Findings {
			findings = append(findings, map[string]any{"code": f.Code, "span": bounds(f.At), "detail": f.Detail})
		}
		results = append(results, map[string]any{"path": row.Path, "requested_role": row.Role, "sha256": hex.EncodeToString(sum[:]), "bytes": len(raw), "exact_export": string(im.Export()) == string(raw), "supported_role": v.Supported(), "tokens": tokens, "commands": commands, "records": records, "findings": findings, "findings_capped": i.FindingsCapped, "covered_span_bytes": i.WorkBytes})
	}
	encoded, e := json.MarshalIndent(results, "", "  ")
	must(e)
	fmt.Println(string(encoded))
}
