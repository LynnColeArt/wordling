package editor

import (
	"errors"
	"maps"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
	"github.com/lynncoleart/wordling/internal/proofreading"
	"github.com/lynncoleart/wordling/internal/storage"
)

// ProofResources holds the admitted lexicon and the active supplementary
// dictionary observation. A missing supplementary file is a valid observation.
type ProofResources struct {
	Lexicon       *proofreading.Lexicon
	Workspace     *storage.Workspace
	Directory     *storage.WorkspaceDirectory
	Supplementary *proofreading.Supplementary
}

type ProofreadingScope uint8

const (
	ProofWord ProofreadingScope = iota + 1
	ProofPage
	ProofDocument
	ProofBlock
	ProofCount
)

type ProofreadingPhase uint8

const (
	ProofInactive ProofreadingPhase = iota
	ProofMenu
	ProofQuestioning
	ProofCompleteAck
	ProofLookupInput
	ProofLookupSelection
	ProofDictionaryName
	ProofEditing
	ProofDictionaryPending
)

type ProofIssue string

const (
	ProofNotFound      ProofIssue = "Not Found"
	ProofDoubleWord    ProofIssue = "Double Word"
	ProofIrregularCase ProofIssue = "Irregular Case"
)

type proofWord struct {
	text       string
	start, end int
	fullEnd    int
	page       int
	capped     bool
}

type proofReplacement struct {
	source, text string
}

func (r proofReplacement) forWord(word string) string {
	if r.text == "" || r.text == word {
		return ""
	}
	if strings.EqualFold(r.source, r.text) {
		if word == r.source {
			return r.text
		}
		return ""
	}
	return proofCase(word, r.text)
}

type proofreadingState struct {
	phase                                            ProofreadingPhase
	scope                                            ProofreadingScope
	issue                                            ProofIssue
	words                                            []proofWord
	index, count, page, lower, limit, editTokenCount int
	suggestions                                      []string
	suggestionPage                                   int
	corrections                                      map[string]proofReplacement
	skipped                                          map[string]struct{}
	draft, alternative                               string
	partial, standalone                              bool
	ignoreNumbers, ignoreCase, ignoreDouble          bool
}

func proofLetter(b byte) bool {
	return b >= 'a' && b <= 'z' || b >= 'A' && b <= 'Z'
}

func proofNumber(b byte) bool { return b >= '0' && b <= '9' }

func proofGlyph(b byte) bool { return proofLetter(b) || proofNumber(b) }

func proofTransparent(kind document.Kind) bool {
	switch kind {
	case document.BoldOn, document.BoldOff, document.UnderlineOn, document.UnderlineOff,
		document.DeletedSoftReturn, document.DeletedSoftPage, document.EndOfPage:
		return true
	default:
		return false
	}
}

// proofWords traverses complete native owners. DSRt and attribute codes
// carry no lexical separator. SRt and hyphens separate words. A numeric run
// contributes to checking and Count only when it contains a letter.
func (s Session) proofWords(from int) ([]proofWord, error) {
	physical, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return nil, err
	}
	pages := make([]int, s.native.TokenCount())
	for _, line := range physical.Lines {
		for _, position := range line.Tokens {
			pages[position.Index] = line.Page
		}
	}
	var words []proofWord
	var word proofWord
	var glyphs []byte
	var join byte
	var hasLetter bool
	flush := func() {
		if hasLetter {
			word.text = string(glyphs)
			words = append(words, word)
		}
		glyphs, join, word, hasLetter = glyphs[:0], 0, proofWord{}, false
	}
	for i := from; i < s.native.TokenCount(); i++ {
		token, err := s.native.Token(i)
		if err != nil {
			return nil, err
		}
		if proofTransparent(token.Kind) {
			continue
		}
		if token.Kind != document.ASCII {
			flush()
			continue
		}
		b := token.Raw[0]
		if proofGlyph(b) {
			hasLetter = hasLetter || proofLetter(b)
			word.fullEnd = i + 1
			if len(glyphs) == 0 {
				word.start, word.page = i, pages[i]
			}
			if !word.capped && (len(glyphs) == document.MaxProofWordBytes ||
				join != 0 && len(glyphs) == document.MaxProofWordBytes-1) {
				word.capped = true
			}
			if !word.capped {
				if join != 0 {
					glyphs = append(glyphs, join)
				}
				glyphs = append(glyphs, b)
				word.end = i + 1
			}
			join = 0
			continue
		}
		if b == '\'' && len(glyphs) != 0 && join == 0 {
			join = b
		} else {
			flush()
		}
	}
	flush()
	return words, nil
}

func (p *proofreadingState) current() (proofWord, bool) {
	if p != nil && p.index >= 0 && p.index < len(p.words) {
		return p.words[p.index], true
	}
	return proofWord{}, false
}

func (s Session) beginProofreading() (Session, *Intent, error) {
	if s.native == nil || s.proofResources == nil || s.proofResources.Lexicon.Count() == 0 {
		return s, nil, refuse("proofreading lexicon is unavailable")
	}
	s.proof = &proofreadingState{phase: ProofMenu}
	s.mode, s.notice = ProofMenuMode, ""
	if s.selection {
		return s.startProofScope(ProofBlock)
	}
	return s, nil, nil
}

func (s Session) startProofScope(scope ProofreadingScope) (Session, *Intent, error) {
	words, err := s.proofWords(0)
	if err != nil {
		return s, nil, err
	}
	p := *s.proof
	p.scope, p.index, p.count, p.partial = scope, 0, 0, false
	p.words = words
	p.limit = s.native.TokenCount()
	switch scope {
	case ProofCount:
		p.count = len(words)
		p.words = nil
		return s.proofAcknowledgement(p), nil, nil
	case ProofWord:
		gap := s.cursor.Gap()
		p.words = nil
		for _, word := range words {
			if s.proofWordAt(word, gap) {
				p.words = []proofWord{word}
				break
			}
		}
	case ProofPage:
		position, err := s.EverydayPosition()
		if err != nil {
			return s, nil, err
		}
		p.page = position.Page
		p.words = proofScopeWords(words, p)
	case ProofBlock:
		a, b := s.anchor.Gap(), s.cursor.Gap()
		p.lower, p.limit = min(a, b), max(a, b)
		p.words = proofScopeWords(words, p)
		s.selection = false
	}
	p.phase = ProofQuestioning
	s.proof = &p
	return s.scanProof()
}

func (s Session) proofWordAt(word proofWord, gap int) bool {
	if gap >= word.start && gap <= word.fullEnd {
		return true
	}
	first, last := gap, word.start
	if gap > word.fullEnd {
		first, last = word.fullEnd, gap
	}
	for index := first; index < last; index++ {
		token, err := s.native.Token(index)
		if err != nil {
			return false
		}
		switch token.Kind {
		case document.BoldOn, document.BoldOff, document.UnderlineOn, document.UnderlineOff:
		default:
			return false
		}
	}
	return true
}

func proofScopeWords(words []proofWord, p proofreadingState) []proofWord {
	switch p.scope {
	case ProofPage, ProofBlock:
		var selected []proofWord
		for _, word := range words {
			if p.scope == ProofPage && word.page == p.page || p.scope == ProofBlock && word.start >= p.lower && word.fullEnd <= p.limit {
				selected = append(selected, word)
			}
		}
		return selected
	case ProofWord:
		if len(words) != 0 {
			return words[:1]
		}
		return nil
	default:
		return words
	}
}

func proofCase(word, replacement string) string {
	if word == strings.ToUpper(word) {
		return strings.ToUpper(replacement)
	}
	if word[0] >= 'A' && word[0] <= 'Z' && word[1:] == strings.ToLower(word[1:]) {
		return strings.ToUpper(replacement[:1]) + replacement[1:]
	}
	return replacement
}

func (s Session) proofAccepts(word string) (bool, error) {
	ok, err := s.proofResources.Lexicon.Accepts(word)
	if errors.Is(err, proofreading.ErrUnsupportedWord) {
		return false, nil
	}
	if err != nil || ok || s.proofResources.Supplementary == nil {
		return ok, err
	}
	ok, err = s.proofResources.Supplementary.Accepts(word)
	if errors.Is(err, proofreading.ErrUnsupportedWord) {
		return false, nil
	}
	return ok, err
}

func (s Session) scanProof() (Session, *Intent, error) {
	original := s
	s.notice = ""
	p := *s.proof
	for {
		w, ok := p.current()
		if !ok {
			if p.scope == ProofWord {
				return s.proofMenu(p), nil, nil
			}
			if len(p.words) > 0 {
				last := p.words[len(p.words)-1]
				cursor, err := s.proofCursor(last.fullEnd)
				if err != nil {
					return original, nil, err
				}
				s.cursor = cursor
			}
			return s.proofAcknowledgement(p), nil, nil
		}
		key := strings.ToLower(w.text)
		_, skip := p.skipped[key]
		number := strings.ContainsAny(w.text, "0123456789")
		if replacement := p.corrections[key].forWord(w.text); !skip && replacement != "" {
			s.proof = &p
			next, err := s.correctProof(replacement, false)
			if err != nil {
				return original, nil, err
			}
			s = next
			p = *s.proof
			continue
		}
		accepted, err := s.proofAccepts(w.text)
		if err != nil {
			return original, nil, err
		}
		p.issue, p.alternative, p.suggestions, p.suggestionPage = "", "", nil, 0
		if !skip && !(number && p.ignoreNumbers) {
			switch {
			case !p.ignoreDouble && s.proofDuplicate(p, w):
				p.issue = ProofDoubleWord
			case !accepted:
				if p.alternative, err = s.proofCaseAlternative(w.text); err != nil {
					return original, nil, err
				}
				if p.alternative != "" && p.ignoreCase {
					break
				}
				if p.alternative != "" {
					p.issue = ProofIrregularCase
					break
				}
				p.issue = ProofNotFound
				p.suggestions, err = s.proofResources.Lexicon.Suggest(w.text)
				if err != nil && !errors.Is(err, proofreading.ErrUnsupportedWord) {
					return original, nil, err
				}
			}
		}
		if p.issue != "" {
			p.phase, p.standalone = ProofQuestioning, false
			s.proof, s.mode = &p, ProofAskMode
			s.cursor, err = s.proofCursor(w.start)
			if err != nil {
				return original, nil, err
			}
			return s, nil, nil
		}
		p.index++
		p.count++
	}
}

func (s Session) proofCaseAlternative(word string) (string, error) {
	lower := strings.ToLower(word)
	if word == lower {
		return "", nil
	}
	ok, err := s.proofAccepts(lower)
	if !ok || err != nil {
		return "", err
	}
	// The original direct case correction turns tWo into Two.
	return strings.ToUpper(lower[:1]) + lower[1:], nil
}

func (s Session) proofDuplicate(p proofreadingState, word proofWord) bool {
	if p.index == 0 {
		return false
	}
	prior := p.words[p.index-1]
	if prior.capped || word.capped || prior.end >= word.start ||
		prior.end-prior.start != len(prior.text) || word.end-word.start != len(word.text) ||
		strings.ContainsAny(word.text, "0123456789") || !strings.EqualFold(prior.text, word.text) {
		return false
	}
	for i := prior.end; i < word.start; i++ {
		separator, err := s.native.Token(i)
		if err != nil || separator.Kind != document.ASCII || separator.Raw[0] != ' ' {
			return false
		}
	}
	return true
}

func (s Session) proofCursor(gap int) (document.Cursor, error) {
	cursor, err := s.native.CursorAt(gap)
	return cursor.WithReveal(s.cursor.Reveal()), err
}

func (s Session) correctProof(replacement string, duplicate bool) (Session, error) {
	p := *s.proof
	word, ok := p.current()
	if !ok {
		return s, refuse("no proofreading suspect to correct")
	}
	start, err := s.proofCursor(word.start)
	if err != nil {
		return s, err
	}
	end, err := s.proofCursor(word.end)
	if err != nil {
		return s, err
	}
	var edit document.EditResult
	if duplicate {
		edit, err = s.native.DeleteProofDuplicate(start, end, p.words[p.index-1].text, word.text)
	} else {
		edit, err = s.native.ReplaceProofWord(start, end, word.text, replacement)
	}
	if err != nil {
		return s, err
	}
	if !edit.Changed {
		p.count++
		p.index++
		s.proof = &p
		return s, nil
	}
	history := s.history
	if s.historyValid {
		history, err = history.AfterProofCorrection(edit)
		if err != nil {
			return s, err
		}
	}
	next, err := s.finishEverydayEdit(edit, history)
	if err != nil {
		return s, err
	}
	p.limit += next.native.TokenCount() - s.native.TokenCount()
	if !duplicate {
		p.count++
	}
	p.index = 0
	p.words = nil
	if p.scope != ProofWord {
		from := 0
		if word.capped {
			// The original checks the unconsumed suffix separately even
			// though the replacement and residue are adjacent in native text.
			from = next.cursor.Gap()
		}
		words, err := next.proofWords(from)
		if err != nil {
			return s, err
		}
		words = proofScopeWords(words, p)
		first := 0
		for first < len(words) && words[first].start < next.cursor.Gap() {
			first++
		}
		if first > 0 {
			// Keep the previous word as context for Double Word without
			// checking or counting it again.
			first--
			p.index = 1
		}
		p.words = words[first:]
	}

	next.proof = &p
	return next, nil
}

func (s Session) rememberProof(replacement string) (Session, *Intent, error) {
	word, _ := s.proof.current()
	next, err := s.correctProof(replacement, false)
	if err != nil {
		return s, nil, err
	}
	p := *next.proof
	p.corrections = maps.Clone(p.corrections)
	if p.corrections == nil {
		p.corrections = make(map[string]proofReplacement)
	}
	p.corrections[strings.ToLower(word.text)] = proofReplacement{source: word.text, text: replacement}
	next.proof = &p
	return next.scanProof()
}
