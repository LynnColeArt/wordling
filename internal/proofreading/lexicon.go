package proofreading

import (
	"crypto/sha256"
	"embed"
	"errors"
	"fmt"
	"sort"
	"strings"
	"sync"
)

const (
	ProfileID      = "linux-esdb-en-us-2026.02.25-plain-v1"
	MaxWordBytes   = 64
	MaxSuggestions = 72

	wordlistDigest = "fe44d9ed8804beb4dfb78c10e1625e9a1f670f0b3074094c92e70bde6e6b0ac9"
	wordlistCount  = 109902
	wordlistBytes  = 1143387
	maxEntryBytes  = 23
)

//go:embed resources/en_US.txt resources/README.txt resources/README_en_US.txt
var resources embed.FS

var (
	loadLexicon = sync.OnceValues(func() (*Lexicon, error) {
		raw, err := resources.ReadFile("resources/en_US.txt")
		if err != nil {
			return nil, fmt.Errorf("read proofreading resource: %w", err)
		}
		for name, digest := range map[string]string{
			"README.txt":       "12830141b6e317ce68c4d6cbc9495b6b8a3f31b98e761be3c05206e02ca3c40d",
			"README_en_US.txt": "d63c711523fc9504fb71e1278489c6d7bb8cafcba75158c107cd17844955470f",
		} {
			notice, err := resources.ReadFile("resources/" + name)
			if err != nil {
				return nil, fmt.Errorf("read proofreading notice %s: %w", name, err)
			}
			if fmt.Sprintf("%x", sha256.Sum256(notice)) != digest {
				return nil, fmt.Errorf("proofreading notice %s has unexpected bytes", name)
			}
		}
		return admitLexicon(raw)
	})
	ErrUnsupportedWord = errors.New("proofreading accepts only bounded ASCII words with internal apostrophes")
)

type lexicalEntry struct{ spelling, folded string }

// Lexicon is the immutable admitted ESDB US English resource.
type Lexicon struct {
	exact   map[string]struct{}
	entries []lexicalEntry
}

// LoadLexicon admits the embedded versioned resource or returns its load error.
func LoadLexicon() (*Lexicon, error) { return loadLexicon() }

func admitLexicon(raw []byte) (*Lexicon, error) {
	if len(raw) != wordlistBytes || fmt.Sprintf("%x", sha256.Sum256(raw)) != wordlistDigest {
		return nil, errors.New("proofreading resource does not match the pinned ESDB US wordlist")
	}
	exact := make(map[string]struct{}, wordlistCount)
	entries := make([]lexicalEntry, 0, wordlistCount)
	for rest := string(raw); rest != ""; {
		var spelling string
		var ok bool
		spelling, rest, ok = strings.Cut(rest, "\r\n")
		if !ok || !validWord(spelling, maxEntryBytes) {
			return nil, errors.New("malformed CRLF proofreading wordlist")
		}
		if _, duplicate := exact[spelling]; duplicate {
			return nil, errors.New("duplicate exact spelling in proofreading wordlist")
		}
		exact[spelling] = struct{}{}
		entries = append(entries, lexicalEntry{spelling, strings.ToLower(spelling)})
	}
	if len(entries) != wordlistCount {
		return nil, errors.New("unexpected proofreading word count")
	}
	sort.Slice(entries, func(i, j int) bool {
		a, b := entries[i], entries[j]
		if a.folded != b.folded {
			return a.folded < b.folded
		}
		return a.spelling < b.spelling
	})
	return &Lexicon{exact: exact, entries: entries}, nil
}

// Count returns the number of exact admitted spellings.
func (l *Lexicon) Count() int {
	if l == nil {
		return 0
	}
	return len(l.entries)
}

func letter(c byte) bool { return c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z' }

func validWord(word string, limit int) bool {
	if len(word) == 0 || len(word) > limit || !letter(word[0]) || !letter(word[len(word)-1]) {
		return false
	}
	for i := 1; i+1 < len(word); i++ {
		if !letter(word[i]) && (word[i] != '\'' || !letter(word[i-1]) || !letter(word[i+1])) {
			return false
		}
	}
	return true
}

func titleWord(lower string) string {
	return strings.ToUpper(lower[:1]) + lower[1:]
}

// Accepts admits exact case, and title/all-uppercase forms of a word present
// in lowercase. An unlisted mixed-case form remains questionable.
func (l *Lexicon) Accepts(word string) (bool, error) {
	if l.Count() == 0 {
		return false, errors.New("proofreading lexicon is unavailable")
	}
	if !validWord(word, MaxWordBytes) {
		return false, ErrUnsupportedWord
	}
	if _, ok := l.exact[word]; ok {
		return true, nil
	}
	lower := strings.ToLower(word)
	if word == titleWord(lower) || word == strings.ToUpper(word) {
		_, ok := l.exact[lower]
		return ok, nil
	}
	return false, nil
}

type lexicalMatch struct {
	spelling string
	folded   string
	distance int
	caseCost int
}

// Suggest ranks lexical candidates at up to two insertions, deletions,
// substitutions or adjacent transpositions. It excludes the original exact word
// and returns at most MaxSuggestions stable, distinct display spellings.
func (l *Lexicon) Suggest(word string) ([]string, error) {
	if l.Count() == 0 {
		return nil, errors.New("proofreading lexicon is unavailable")
	}
	if !validWord(word, MaxWordBytes) {
		return nil, ErrUnsupportedWord
	}
	return l.rank(word, false), nil
}

// Lookup supports ? (one byte) and * (any bytes) over the ASCII wordlist.
// A literal lookup returns a matching spelling first, followed by nearby
// spellings. This is the declared lexical adaptation, not phonetic matching.
func (l *Lexicon) Lookup(pattern string) ([]string, error) {
	if l.Count() == 0 {
		return nil, errors.New("proofreading lexicon is unavailable")
	}
	if !strings.ContainsAny(pattern, "*?") {
		if !validWord(pattern, MaxWordBytes) {
			return nil, ErrUnsupportedWord
		}
		return l.rank(pattern, true), nil
	}
	if len(pattern) > MaxWordBytes {
		return nil, ErrUnsupportedWord
	}
	for i := range len(pattern) {
		c := pattern[i]
		if !letter(c) && c != '\'' && c != '*' && c != '?' {
			return nil, ErrUnsupportedWord
		}
	}
	pattern = strings.ToLower(pattern)
	var result []string
	last := ""
	for _, entry := range l.entries {
		if entry.folded == last || !wildcardMatch(pattern, entry.folded) {
			continue
		}
		last = entry.folded
		display := entry.spelling
		if _, lowerExists := l.exact[entry.folded]; lowerExists {
			display = entry.folded
		}
		result = append(result, display)
		if len(result) == MaxSuggestions {
			break
		}
	}
	return result, nil
}

func wildcardMatch(pattern, word string) bool {
	p, w := 0, 0
	star, matched := -1, 0
	for w < len(word) {
		switch {
		case p < len(pattern) && (pattern[p] == '?' || pattern[p] == word[w]):
			p++
			w++
		case p < len(pattern) && pattern[p] == '*':
			star, matched = p, w
			p++
		case star >= 0:
			matched++
			w, p = matched, star+1
		default:
			return false
		}
	}
	for p < len(pattern) && pattern[p] == '*' {
		p++
	}
	return p == len(pattern)
}

func (l *Lexicon) rank(word string, includeExact bool) []string {
	const maxDistance = 2
	folded := strings.ToLower(word)
	if len(folded) > maxEntryBytes+maxDistance {
		return nil
	}
	upper := word == strings.ToUpper(word)
	title := word == titleWord(folded)
	var matches []lexicalMatch
	for _, entry := range l.entries {
		lengthDelta := len(entry.folded) - len(folded)
		if lengthDelta < -maxDistance || lengthDelta > maxDistance {
			continue
		}
		distance := adjacentEditDistance(folded, entry.folded, maxDistance)
		if distance > maxDistance {
			continue
		}
		display := entry.spelling
		if entry.spelling == entry.folded {
			switch {
			case upper:
				display = strings.ToUpper(display)
			case title:
				display = titleWord(display)
			}
		}
		if !includeExact && display == word {
			continue
		}
		caseCost := 1
		if display == word || display == entry.folded || display != entry.spelling {
			caseCost = 0
		}
		matches = append(matches, lexicalMatch{display, entry.folded, distance, caseCost})
	}
	sort.Slice(matches, func(i, j int) bool {
		a, b := matches[i], matches[j]
		if a.distance != b.distance {
			return a.distance < b.distance
		}
		if a.caseCost != b.caseCost {
			return a.caseCost < b.caseCost
		}
		if a.folded != b.folded {
			return a.folded < b.folded
		}
		return a.spelling < b.spelling
	})
	result := make([]string, 0, min(len(matches), MaxSuggestions))
	seen := make(map[string]struct{}, cap(result))
	for _, match := range matches {
		if _, duplicate := seen[match.spelling]; duplicate {
			continue
		}
		seen[match.spelling] = struct{}{}
		result = append(result, match.spelling)
		if len(result) == MaxSuggestions {
			break
		}
	}
	return result
}

// adjacentEditDistance computes optimal string alignment distance, allowing
// adjacent transposition in addition to the three Levenshtein operations.
func adjacentEditDistance(query, entry string, limit int) int {
	var rows [3][maxEntryBytes + 1]int
	before, previous, current := &rows[0], &rows[1], &rows[2]
	for j := range len(entry) + 1 {
		previous[j] = j
	}
	for i := 1; i <= len(query); i++ {
		current[0] = i
		rowMin := i
		for j := 1; j <= len(entry); j++ {
			cost := 0
			if query[i-1] != entry[j-1] {
				cost = 1
			}
			value := min(previous[j]+1, current[j-1]+1, previous[j-1]+cost)
			if i > 1 && j > 1 && query[i-1] == entry[j-2] && query[i-2] == entry[j-1] {
				value = min(value, before[j-2]+1)
			}
			current[j] = value
			rowMin = min(rowMin, value)
		}
		if rowMin > limit {
			return limit + 1
		}
		before, previous, current = previous, current, before
	}
	return previous[len(entry)]
}
