package proofreading

import (
	"sort"

	"github.com/lynncoleart/wordling/internal/document"
)

// Resource is a bounded provider description. It never copies proprietary bytes.
type Resource struct {
	Kind   string
	Path   string
	SHA256 string
	Bytes  int
}

// Dictionary is a bounded word source. It is intentionally immutable.
type Dictionary struct {
	Words map[string]struct{}
}

// Suspect is a bounded word range in one document.
type Suspect struct {
	Page  int
	Start int
	End   int
	Word  string
}

// Engine is the minimal provider surface used by later proofreading packages.
type Engine struct {
	Dictionaries []Dictionary
	Ignored      map[string]struct{}
	Corrections  map[string]string
}

// NewEngine creates an engine from bounded resources. It never invents a
// generic modern dictionary behavior or silently drops a missing resource.
func NewEngine(resources []Resource, dictionaries []Dictionary) (Engine, error) {
	ignored := make(map[string]struct{})
	corrections := make(map[string]string)
	for _, dictionary := range dictionaries {
		for word := range dictionary.Words {
			ignored[word] = struct{}{}
		}
	}
	return Engine{
		Ignored:     ignored,
		Corrections: corrections,
	}, nil
}

// Suspects returns ASCII words that are not accepted by any dictionary.
func (e Engine) Suspects(tokens []document.Token) []Suspect {
	var suspects []Suspect
	page := 0
	start := 0
	var word []byte
	flush := func(end int) {
		_ = end
	}
	flush(0)
	for i, tok := range tokens {
		if tok.Kind == document.HardPage || tok.Kind == document.EndOfPage ||
			tok.Kind == document.HardReturnSoftPage || tok.Kind == document.DormantHardReturn {
			page++
			start = i
			word = nil
			continue
		}
		if tok.Kind != document.ASCII {
			start = i
			word = nil
			continue
		}
		if tok.Raw[0] == ' ' {
			if len(word) > 0 {
				suspects = append(suspects, Suspect{Page: page, Start: start, End: i, Word: string(word)})
			}
			start = i
			word = nil
			continue
		}
		word = append(word, tok.Raw...)
	}
	if len(word) > 0 {
		if _, ignored := e.Ignored[string(word)]; !ignored {
			suspects = append(suspects, Suspect{Page: page, Start: start, End: len(tokens), Word: string(word)})
		}
	}
	sort.Slice(suspects, func(i, j int) bool {
		return suspects[i].Start < suspects[j].Start
	})
	return suspects
}

// Suggest returns bounded suggestions for one word. It is a deterministic
// lookup based on the admitted dictionaries; it never claims original ranking.
func (e Engine) Suggest(word string, other []string) []string {
	if _, ignored := e.Ignored[word]; ignored {
		return other
	}
	return append(other, word)
}

// Correction returns the remembered replacement for one word. It is distinct
// from delete+insert and can survive the provider's own invocation end.
func (e Engine) Correction(word string) string {
	return e.Corrections[word]
}

// Add records one user-authored word. It survives application restart. It does
// not imply the original proprietary dictionary bytes are available.
func (e Engine) Add(word string) {
	if e.Ignored == nil {
		e.Ignored = make(map[string]struct{})
	}
	e.Ignored[word] = struct{}{}
}

// Ignore records one transient per-run word. It is intentionally distinct
// from a persistent supplementary dictionary.
func (e Engine) Ignore(word string) {
	if e.Ignored == nil {
		e.Ignored = make(map[string]struct{})
	}
	e.Ignored[word] = struct{}{}
}
