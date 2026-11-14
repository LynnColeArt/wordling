package tui

import (
	"encoding/hex"
	"encoding/json"
	"os"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

func TestComposePairMatrixAgainstDOSNativeOwners(t *testing.T) {
	raw, err := os.ReadFile("testdata/compose-dos-pairs.json")
	if err != nil {
		t.Fatal(err)
	}
	var matrix map[string]string
	if err := json.Unmarshal(raw, &matrix); err != nil {
		t.Fatal(err)
	}
	for pair, expected := range matrix {
		result, ok := lookupComposePair(pair)
		if ok != (expected != "") || ok && hex.EncodeToString(document.CharacterBytes(result.set, result.number)) != expected {
			t.Errorf("%q: got %+v (%v), DOS native owner %q", pair, result, ok, expected)
		}
		if ok {
			reversed, ok := lookupComposePair(pair[1:] + pair[:1])
			if !ok || reversed != result {
				t.Errorf("%q: reverse lookup got %+v (%v), want %+v", pair, reversed, ok, result)
			}
		}
	}
}
