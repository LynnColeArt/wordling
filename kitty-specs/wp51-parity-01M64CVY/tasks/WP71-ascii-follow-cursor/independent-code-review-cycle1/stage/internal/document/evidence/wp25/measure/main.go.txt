// Command measure reports host allocation/work observations for the actual public
// API. Synthetic boundary inputs are negative/safety fixtures, never product new
// document construction or original-app format-capacity evidence.
package main

import (
	"bytes"
	"encoding/binary"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"runtime"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
)

func main() {
	if e := run(); e != nil {
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
}
func run() error {
	source, e := os.ReadFile("docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if e != nil {
		return e
	}
	bodyStart := int(binary.LittleEndian.Uint32(source[4:8]))
	prefix := source[:bodyStart]
	body := append([]byte{0xc3, 12, 0xc3, 0xc4, 12, 0xc4, 0xc3, 12, 0xc3}, bytes.Repeat([]byte{'x'}, document.MaxMutationTokens-4)...)
	body = append(body, 0xc4, 12, 0xc4)
	admitted, e := document.Parse(append(bytes.Clone(prefix), body...))
	if e != nil {
		return e
	}
	if e = admitted.CheckMutation(); e != nil {
		return e
	}
	// Max inherited reader metadata:4096 linked50-byte blocks and16384 zero-length
	// FFFF opaque/deleted entries. It is valid read-only framing, never admitted
	// mutation/schema, and explicitly synthetic. Reader's exact export must survive.
	boundary := 16 + wp51.MaxIndexBlocks*50
	wide := make([]byte, boundary+1)
	copy(wide, source[:16])
	binary.LittleEndian.PutUint32(wide[4:8], uint32(boundary))
	wide[boundary] = 'A'
	for block := 0; block < wp51.MaxIndexBlocks; block++ {
		off := 16 + block*50
		binary.LittleEndian.PutUint16(wide[off:], 0xfffb)
		binary.LittleEndian.PutUint16(wide[off+2:], 5)
		binary.LittleEndian.PutUint16(wide[off+4:], 50)
		if block+1 < wp51.MaxIndexBlocks {
			binary.LittleEndian.PutUint32(wide[off+6:], uint32(off+50))
		}
		for slot := 1; slot < 5; slot++ {
			pos := off + slot*10
			binary.LittleEndian.PutUint16(wide[pos:], 0xffff)
			binary.LittleEndian.PutUint32(wide[pos+6:], 16)
		}
	}
	broad, e := document.Parse(wide)
	if e != nil {
		return e
	}
	out, e := broad.Export()
	if e != nil || !bytes.Equal(out, wide) {
		return fmt.Errorf("broad read-only preservation: %v", e)
	}
	e = broad.CheckMutation()
	var refusal *document.Failure
	if !errors.As(e, &refusal) || refusal.Category != document.MutationLimit {
		return fmt.Errorf("broad refusal: %v", e)
	}
	reader, e := wp51.Parse(wide)
	if e != nil {
		return e
	}
	inspection := reader.Inspect()
	if len(inspection.Blocks) != wp51.MaxIndexBlocks || len(inspection.Packets) != wp51.MaxPacketEntries {
		return fmt.Errorf("incorrect inherited metadata fixture")
	}
	c, _ := admitted.CursorAt(4)
	var results []any
	for _, test := range []struct {
		name  string
		bytes int
		fn    func()
	}{
		{"admitted-two-pair-max-token-inspection", len(prefix) + len(body), func() {
			if e := admitted.CheckMutation(); e != nil {
				panic(e)
			}
		}},
		{"admitted-two-pair-max-token-typeover", len(prefix) + len(body), func() {
			if _, e := admitted.TypeoverASCII(c, []byte("Y")); e != nil {
				panic(e)
			}
		}},
		{"inherited-max-metadata-read-only-refusal", len(wide), func() {
			if e := broad.CheckMutation(); e == nil {
				panic("unsafe admission")
			}
		}},
	} {
		r := testing.Benchmark(func(b *testing.B) {
			b.ReportAllocs()
			b.SetBytes(int64(test.bytes))
			for b.Loop() {
				test.fn()
			}
		})
		results = append(results, map[string]any{"name": test.name, "input_bytes": test.bytes, "ns_per_op": r.NsPerOp(), "allocated_bytes_per_op": r.AllocedBytesPerOp(), "allocs_per_op": r.AllocsPerOp(), "iterations": r.N, "raw": r.String() + " " + r.MemString()})
	}
	return json.NewEncoder(os.Stdout).Encode(map[string]any{"go_version": runtime.Version(), "GOOS": runtime.GOOS, "GOARCH": runtime.GOARCH, "policy": "existing broad Parse limits unchanged; narrower mutation policies; all are implementation/support limits, not original DOS limits", "admitted_max_tokens": admitted.TokenCount(), "admitted_derived_max_bytes": len(prefix) + len(body), "admitted_gap_index_bytes": (admitted.TokenCount() + 1) * 4, "broad_refusal_input_bytes": len(wide), "broad_refusal_reader_blocks": len(inspection.Blocks), "broad_refusal_reader_packets": len(inspection.Packets), "measurements": results, "interpretation": "B/op is cumulative allocation per call, not peak live memory or a hard refusal cap; metadata cloned by inherited Inspect is included. External time/RSS includes process/runtime/harness. No product SLO or new reader budget."})
}
