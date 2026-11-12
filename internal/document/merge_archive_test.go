package document_test

import (
	"bytes"
	"encoding/binary"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

func TestNestedMergeArchiveRequiresCompletePacketGraph(t *testing.T) {
	path := filepath.Join("../../docs/research/everyday-contract-2026-11-05/native-merge/wide", "wrapper", "MERGED.WP5")
	raw, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	d, err := document.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	compact, err := d.CompactFastSave()
	if err != nil {
		t.Fatal(err)
	}
	checked, err := compact.Export()
	if err != nil || !bytes.Equal(checked[324:], raw[1076:]) {
		t.Fatalf("compaction changed checked body: %v", err)
	}
	for name, mutate := range map[string]func([]byte){
		"missing live state":    func(b []byte) { binary.LittleEndian.PutUint16(b[36:], 99) },
		"foreign retired state": func(b []byte) { b[496] = 0x80 },
		"foreign retired pool":  func(b []byte) { b[256] ^= 1 },
	} {
		t.Run(name, func(t *testing.T) {
			candidate := bytes.Clone(raw)
			mutate(candidate)
			d, err := document.Parse(candidate)
			if err != nil {
				t.Fatal(err)
			}
			if result, err := d.CompactFastSave(); result != nil || err == nil {
				t.Fatal("unverified archive compacted")
			}
		})
	}
}
