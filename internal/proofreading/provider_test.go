package proofreading_test

import (
	"testing"

	"github.com/lynncoleart/wordling/internal/proofreading"
)

func TestProviderIdentity(t *testing.T) {
	lex, err := proofreading.LoadLexicon()
	if err != nil {
		t.Fatal(err)
	}
	if lex.Count() != 109902 || proofreading.ProfileID != "linux-esdb-en-us-2026.02.25-plain-v1" {
		t.Fatalf("wrong admitted provider: %q, %d entries", proofreading.ProfileID, lex.Count())
	}
}
