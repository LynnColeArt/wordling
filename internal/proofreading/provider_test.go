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

func TestLoadLexiconIsolatesAssignableWrappers(t *testing.T) {
	first, err := proofreading.LoadLexicon()
	if err != nil {
		t.Fatal(err)
	}
	second, err := proofreading.LoadLexicon()
	if err != nil {
		t.Fatal(err)
	}
	*first = proofreading.Lexicon{}

	assertAdmitted := func(lex *proofreading.Lexicon) {
		t.Helper()
		ok, err := lex.Accepts("thermodynamics")
		if lex.Count() != 109902 || err != nil || !ok {
			t.Fatalf("caller reassignment affected another load: count %d, accepted %v, err %v", lex.Count(), ok, err)
		}
	}
	assertAdmitted(second)
	fresh, err := proofreading.LoadLexicon()
	if err != nil {
		t.Fatal(err)
	}
	assertAdmitted(fresh)
}
