package wpm_test

import (
	"bytes"
	"encoding/binary"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

func TestDescriptionEditKeepsOpaqueActionAndSuffix(t *testing.T) {
	raw, err := os.ReadFile("../../../docs/research/reference-runs/mission1-macro-recording/TYPED.WPM")
	if err != nil {
		t.Fatal(err)
	}
	body := binary.LittleEndian.Uint32(raw[4:])
	binary.LittleEndian.PutUint16(raw[body+2:], 0x9999)
	raw = append(raw, 0x34)
	src, err := wpm.Parse(raw, wpm.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	updated, err := src.Edit("New", nil, false)
	if err != nil {
		t.Fatal(err)
	}
	offset := binary.LittleEndian.Uint32(updated[4:])
	if !bytes.Equal(raw[body:], updated[offset:]) || !bytes.Equal(raw, src.Export()) {
		t.Fatal("description edit changed action, suffix, or source")
	}
	if _, err := src.Edit("New", []uint16{'A'}, true); err == nil {
		t.Fatal("opaque action was admitted for rewriting")
	}

	// A second live index could refer to bytes that must not be relocated.
	raw[36] = 2
	src, err = wpm.Parse(raw, wpm.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	if _, err := src.Edit("New", nil, false); err == nil {
		t.Fatal("unfamiliar prefix table admitted for rewriting")
	}
}
