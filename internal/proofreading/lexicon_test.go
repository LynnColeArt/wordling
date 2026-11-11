package proofreading

import (
	"bytes"
	"errors"
	"slices"
	"strings"
	"testing"
)

func TestLexiconAdmissionRejectsChangedPhysicalBytes(t *testing.T) {
	raw, err := resources.ReadFile("resources/en_US.txt")
	if err != nil {
		t.Fatal(err)
	}
	modified := bytes.Clone(raw)
	modified[0] = 'Z'
	for _, rejected := range [][]byte{nil, modified, bytes.ReplaceAll(raw, []byte("\r\n"), []byte("\n"))} {
		if lex, err := admitLexicon(rejected); err == nil || lex != nil {
			t.Fatal("admitted an unpinned wordlist")
		}
	}
}

func TestLexiconChecksUnrelatedVocabularyAndCase(t *testing.T) {
	lex, err := LoadLexicon()
	if err != nil {
		t.Fatal(err)
	}
	for _, word := range []string{"thermodynamics", "Glacier", "PHOTOSYNTHESIS", "NASA", "don't"} {
		if ok, err := lex.Accepts(word); err != nil || !ok {
			t.Errorf("expected %q to be accepted: %v, %v", word, ok, err)
		}
	}
	for _, word := range []string{"mispelled", "zorbly", "quICK", "nasa"} {
		if ok, err := lex.Accepts(word); err != nil || ok {
			t.Errorf("expected %q to be questioned: %v, %v", word, ok, err)
		}
	}
	for _, word := range []string{"", "éclair", "ab2", "two words", "'odd", strings.Repeat("a", 65)} {
		if ok, err := lex.Accepts(word); !errors.Is(err, ErrUnsupportedWord) || ok {
			t.Errorf("expected %q to be unsupported: %v, %v", word, ok, err)
		}
	}
	var unavailable *Lexicon
	if _, err := unavailable.Accepts("quick"); err == nil {
		t.Fatal("resource absence reported successful admission")
	}
}

func TestLexiconSuggestionsAndLookupAreBoundedAndDeterministic(t *testing.T) {
	lex, err := LoadLexicon()
	if err != nil {
		t.Fatal(err)
	}
	for _, tc := range [][2]string{
		{"quik", "quick"}, {"mispelled", "misspelled"}, {"recieve", "receive"},
		{"acommodate", "accommodate"}, {"Glacir", "Glacier"}, {"quICK", "quick"},
	} {
		first, err := lex.Suggest(tc[0])
		if err != nil || len(first) > MaxSuggestions || !slices.Contains(first, tc[1]) || slices.Contains(first, tc[0]) {
			t.Fatalf("suggest %q: %v, %v", tc[0], first, err)
		}
		next, err := lex.Suggest(tc[0])
		if err != nil || !slices.Equal(first, next) {
			t.Fatalf("suggestion order changed for %q", tc[0])
		}
	}
	words, err := lex.Lookup("qu?ck")
	if err != nil || !slices.Contains(words, "quick") || !slices.Contains(words, "quack") {
		t.Fatalf("wildcard lookup: %v, %v", words, err)
	}
	words, err = lex.Lookup("quick")
	if err != nil || len(words) == 0 || words[0] != "quick" {
		t.Fatalf("literal lookup: %v, %v", words, err)
	}
	words, err = lex.Lookup("*")
	if err != nil || len(words) != MaxSuggestions {
		t.Fatalf("unconstrained lookup must be capped: %d, %v", len(words), err)
	}
	if _, err = lex.Lookup("a?ç"); !errors.Is(err, ErrUnsupportedWord) {
		t.Fatal("invalid lookup pattern was admitted")
	}
}
