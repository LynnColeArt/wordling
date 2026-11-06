package proofreading_test

import (
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/proofreading"
)

func TestProviderSuspectsSimpleWord(t *testing.T) {
	dictionary := proofreading.Dictionary{Words: map[string]struct{}{"quick": {}}}
	resources := []proofreading.Resource{}
	engine, err := proofreading.NewEngine(resources, []proofreading.Dictionary{dictionary})
	if err != nil {
		t.Fatal(err)
	}
	suspects := engine.Suspects([]document.Token{{Kind: document.ASCII, Raw: []byte("quik")}})
	if len(suspects) != 1 {
		t.Fatalf("expected one suspect, got %d", len(suspects))
	}
}
