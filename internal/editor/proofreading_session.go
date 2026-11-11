package editor

import (
	"context"
	"errors"
	"maps"
	"strings"
	"sync/atomic"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/proofreading"
	"github.com/lynncoleart/wordling/internal/storage"
)

const (
	ProofLookupMode     Mode = "ProofLookup"
	ProofDictionaryMode Mode = "ProofDictionary"
)

const proofPageSize = 24

// ProofView is the read-only projection used by the contextual TUI.
// Start and End are the exact half-open native suspect range. Double Word
// also supplies the preceding word’s separate range in PreviousStart/End.
type ProofView struct {
	Phase                      ProofreadingPhase
	Scope                      ProofreadingScope
	Issue                      ProofIssue
	Word, Draft, Prompt        string
	Dictionary                 string
	Start, End, Count          int
	PreviousStart, PreviousEnd int
	Caret                      int
	Partial, More              bool
	Standalone                 bool
	Suggestions                []string
}

type Proofword struct {
	Word   string
	Index  int
	Number int
	Total  int
}

func (s Session) ProofStatus() ProofView {
	var view ProofView
	if s.proofResources != nil {
		view.Dictionary = s.proofResources.Supplementary.Name()
	}
	if s.proof == nil {
		return view
	}
	p := s.proof
	view.Phase, view.Scope, view.Issue = p.phase, p.scope, p.issue
	view.Count, view.Partial, view.Standalone = p.count, p.partial, p.standalone
	view.Draft, view.Caret = p.draft, len(p.draft)
	if word, ok := p.current(); ok && p.phase != ProofMenu && p.phase != ProofCompleteAck {
		view.Word, view.Start, view.End = word.text, word.start, word.end
		if p.issue == ProofDoubleWord && p.index > 0 {
			previous := p.words[p.index-1]
			view.PreviousStart, view.PreviousEnd = previous.start, previous.end
		}
	}
	from := p.suggestionPage * proofPageSize
	to := min(from+proofPageSize, len(p.suggestions))
	view.Suggestions = append([]string(nil), p.suggestions[from:to]...)
	view.More = to < len(p.suggestions)
	switch p.phase {
	case ProofMenu:
		view.Prompt = "Check: 1 Word; 2 Page; 3 Document; 4 New Sup. Dictionary; 5 Look Up; 6 Count"
	case ProofLookupInput:
		view.Prompt = "Word or word pattern:"
	case ProofLookupSelection:
		view.Prompt = "Select Word:"
	case ProofDictionaryName:
		view.Prompt = "New Sup. Dictionary:"
	case ProofEditing:
		view.Prompt = "Spell Edit   Press Exit when done"
	case ProofDictionaryPending:
		view.Prompt = "Supplementary dictionary"
	case ProofCompleteAck:
		view.Prompt = "Press any key to continue"
	case ProofQuestioning:
		switch p.issue {
		case ProofDoubleWord:
			view.Prompt = "Double Word: 1 2 Skip; 3 Delete 2nd; 4 Edit; 5 Disable Double Word Checking"
		case ProofIrregularCase:
			view.Prompt = "Irregular Case: 1 2 Skip; 3 Replace; 4 Edit; 5 Disable Case Checking"
		default:
			view.Prompt = "Not Found: 1 Skip Once; 2 Skip; 3 Add; 4 Edit; 5 Look Up; 6 Ignore Numbers"
		}
	}
	return view
}

func (s Session) ProofSnapshot() (Proofword, bool) {
	if s.proof == nil || s.proof.phase != ProofQuestioning {
		return Proofword{}, false
	}
	word, ok := s.proof.current()
	return Proofword{Word: word.text, Index: word.start, Number: s.proof.count + 1, Total: s.proof.count + len(s.proof.words) - s.proof.index}, ok
}

func (s Session) proofMenu(p proofreadingState) Session {
	p.phase, p.issue, p.draft, p.suggestions, p.suggestionPage = ProofMenu, "", "", nil, 0
	p.standalone = false
	s.proof, s.mode, s.notice = &p, ProofMenuMode, ""
	return s
}

func (s Session) proofAcknowledgement(p proofreadingState) Session {
	p.phase, p.issue, p.suggestions, p.suggestionPage = ProofCompleteAck, "", nil, 0
	s.proof, s.mode, s.notice = &p, ProofAckMode, ""
	return s
}

func (s Session) finishProof() Session {
	s.proof, s.mode, s.notice = nil, Editing, ""
	return s
}

func (s Session) reduceProofEvent(event Event) (Session, *Intent, error) {
	p := *s.proof
	switch p.phase {
	case ProofMenu:
		switch event.Command {
		case F1, F7:
			return s.finishProof(), nil, nil
		case Text:
			switch event.Text {
			case "1":
				return s.startProofScope(ProofWord)
			case "2":
				return s.startProofScope(ProofPage)
			case "3":
				return s.startProofScope(ProofDocument)
			case "4":
				p.phase, p.draft = ProofDictionaryName, ""
				s.proof, s.mode = &p, ProofDictionaryMode
				return s, nil, nil
			case "5":
				return s.openProofLookup(true), nil, nil
			case "6":
				return s.startProofScope(ProofCount)
			}
		}
	case ProofQuestioning:
		return s.proofQuestion(event)
	case ProofCompleteAck:
		if !p.partial && (p.scope == ProofPage || p.scope == ProofCount) {
			return s.proofMenu(p), nil, nil
		}
		return s.finishProof(), nil, nil
	case ProofLookupInput, ProofLookupSelection:
		return s.proofLookup(event)
	case ProofDictionaryName:
		switch event.Command {
		case F1:
			return s.proofMenu(p), nil, nil
		case Enter:
			if p.draft == "" {
				return s, nil, refuse("supplementary dictionary name required")
			}
			return s.beginProofDictionary(false)
		case Text, Backspace:
			return s.editProofDraft(event, storage.MaxNameBytes)
		}
	}
	return s, nil, refuse("command unavailable in this proofreading prompt")
}

func (s Session) proofQuestion(event Event) (Session, *Intent, error) {
	p := *s.proof
	word, ok := p.current()
	if !ok {
		return s, nil, refuse("no active proofreading suspect")
	}
	switch event.Command {
	case F7:
		return s, nil, nil
	case F1:
		p.partial = true
		p.count++
		return s.proofAcknowledgement(p), nil, nil
	case Enter:
		return s.nextProofSuggestions(), nil, nil
	case ProofSkipOnce:
		return s.skipProof(false)
	case ProofSkip:
		return s.skipProof(true)
	case ProofAdd:
		if p.issue == ProofNotFound {
			return s.beginProofDictionary(true)
		}
	case Text:
		switch event.Text {
		case "1":
			return s.skipProof(false)
		case "2":
			return s.skipProof(true)
		case "3":
			switch p.issue {
			case ProofNotFound:
				return s.beginProofDictionary(true)
			case ProofDoubleWord:
				next, err := s.correctProof("", true)
				if err != nil {
					return s, nil, err
				}
				return next.scanProof()
			case ProofIrregularCase:
				return s.rememberProof(p.alternative)
			}
		case "4":
			p.phase, p.editTokenCount = ProofEditing, s.native.TokenCount()
			s.proof, s.mode = &p, Editing
			return s, nil, nil
		case "5":
			switch p.issue {
			case ProofNotFound:
				if p.scope == ProofBlock {
					return s, nil, refuse("Look Up is unavailable while checking a block")
				}
				return s.openProofLookup(false), nil, nil
			case ProofDoubleWord:
				p.ignoreDouble = true
			case ProofIrregularCase:
				p.ignoreCase = true
			}
			s.proof = &p
			return s.skipProof(false)
		case "6":
			if p.issue == ProofNotFound {
				p.ignoreNumbers = true
				s.proof = &p
				if strings.ContainsAny(word.text, "0123456789") {
					return s.skipProof(false)
				}
				return s, nil, nil
			}
		default:
			if replacement, ok := s.proofSelection(event.Text); ok {
				return s.rememberProof(replacement)
			}
		}
	}
	return s, nil, refuse("command unavailable for this proofreading issue")
}

func (s Session) skipProof(pass bool) (Session, *Intent, error) {
	p := *s.proof
	word, _ := p.current()
	if pass {
		p.skipped = maps.Clone(p.skipped)
		if p.skipped == nil {
			p.skipped = make(map[string]struct{})
		}
		p.skipped[strings.ToLower(word.text)] = struct{}{}
	}
	p.index++
	p.count++
	s.proof = &p
	return s.scanProof()
}

func (s Session) nextProofSuggestions() Session {
	p := *s.proof
	if (p.suggestionPage+1)*proofPageSize < len(p.suggestions) {
		p.suggestionPage++
		s.proof = &p
	}
	return s
}

func (s Session) proofSelection(key string) (string, bool) {
	if len(key) != 1 {
		return "", false
	}
	letter := key[0]
	if letter >= 'A' && letter <= 'X' {
		letter += 'a' - 'A'
	}
	if letter < 'a' || letter > 'x' {
		return "", false
	}
	p := s.proof
	index := p.suggestionPage*proofPageSize + int(letter-'a')
	if index >= len(p.suggestions) {
		return "", false
	}
	return p.suggestions[index], true
}

func (s Session) openProofLookup(standalone bool) Session {
	p := *s.proof
	p.phase, p.standalone, p.draft = ProofLookupInput, standalone, ""
	s.proof, s.mode = &p, ProofLookupMode
	return s
}

func (s Session) proofLookup(event Event) (Session, *Intent, error) {
	p := *s.proof
	switch event.Command {
	case F1:
		if p.standalone {
			return s.proofMenu(p), nil, nil
		}
		p.phase, p.draft, p.suggestionPage = ProofQuestioning, "", 0
		word, _ := p.current()
		var err error
		p.suggestions, err = s.proofResources.Lexicon.Suggest(word.text)
		if err != nil && !errors.Is(err, proofreading.ErrUnsupportedWord) {
			return s, nil, err
		}
		s.proof, s.mode = &p, ProofAskMode
		return s, nil, nil
	case Enter:
		if p.phase == ProofLookupSelection || p.draft == "" {
			return s.nextProofSuggestions(), nil, nil
		}
		candidates, err := s.proofResources.Lexicon.Lookup(p.draft)
		if err != nil {
			return s, nil, err
		}
		p.suggestions, p.suggestionPage, p.draft = candidates, 0, ""
		if !p.standalone {
			p.phase = ProofLookupSelection
		}
		s.proof = &p
		return s, nil, nil
	case Text, Backspace:
		if p.phase == ProofLookupInput {
			return s.editProofDraft(event, proofreading.MaxWordBytes)
		}
		if event.Command == Text {
			if replacement, ok := s.proofSelection(event.Text); ok {
				word, _ := p.current()
				// The witnessed capped replacement keeps the first glyph's
				// case and the all-uppercase residue as separate native text.
				if s.isCappedWrapSpelling(word) && len(replacement) > 1 {
					replacement = replacement[:1] + strings.ToUpper(replacement[1:])
				}
				return s.rememberProof(replacement)
			}
		}
	}
	return s, nil, refuse("command unavailable in Look Up")
}

func (s Session) isCappedWrapSpelling(word proofWord) bool {
	if !word.capped || len(word.text) != document.MaxProofWordBytes || word.text != strings.ToUpper(word.text) {
		return false
	}
	residue, err := s.native.Token(word.end)
	if err != nil || residue.Kind != document.ASCII || residue.Raw[0] < 'A' || residue.Raw[0] > 'Z' {
		return false
	}
	boundary, err := s.native.Token(word.end + 1)
	return err == nil && boundary.Kind == document.DeletedSoftReturn
}

func (s Session) editProofDraft(event Event, maxBytes int) (Session, *Intent, error) {
	p := *s.proof
	switch event.Command {
	case Backspace:
		if len(p.draft) > 0 {
			p.draft = p.draft[:len(p.draft)-1]
		}
	case Text:
		for i := range len(event.Text) {
			if event.Text[i] < 0x20 || event.Text[i] > 0x7e {
				return s, nil, refuse("proofreading input requires printable ASCII")
			}
		}
		if len(p.draft)+len(event.Text) > maxBytes {
			return s, nil, refuse("proofreading input exceeds its bound")
		}
		p.draft += event.Text
	}
	s.proof = &p
	return s, nil, nil
}

func (s Session) resumeProofEditing() (Session, *Intent, error) {
	p := *s.proof
	word, ok := p.current()
	if !ok {
		return s, nil, refuse("missing Spell Edit resume position")
	}
	words, err := s.proofWords(0)
	if err != nil {
		return s, nil, err
	}
	start := min(word.start, s.cursor.Gap())
	first := len(words)
	for i, candidate := range words {
		if candidate.fullEnd > start {
			first = i
			break
		}
	}
	p.limit += s.native.TokenCount() - p.editTokenCount
	p.words, p.index, p.phase = proofScopeWords(words[first:], p), 0, ProofQuestioning
	s.proof = &p
	return s.scanProof()
}

type proofDictionaryRequest struct {
	intent    Intent
	resources ProofResources
	buffer    *bufferIdentity
	resume    *proofreadingState
	word      proofWord
	add       bool
	claimed   atomic.Bool
	settled   atomic.Bool
}

type proofDictionaryObservation struct {
	request       *proofDictionaryRequest
	supplementary *proofreading.Supplementary
	result        Result
}

func (s Session) beginProofDictionary(add bool) (Session, *Intent, error) {
	if s.proofResources == nil || !s.proofResources.Workspace.OwnsDirectory(s.proofResources.Directory) ||
		(add && s.proofResources.Supplementary == nil) {
		return s, nil, refuse("supplementary dictionary is unavailable")
	}
	p := *s.proof
	word, _ := p.current()
	name := p.draft
	if add {
		name = s.proofResources.Supplementary.Name()
	}
	request := &proofDictionaryRequest{
		intent: Intent{Operation: s.sequence + 1, Revision: s.revision,
			Kind: ProofDictionaryIO, Name: name, Screen: s.screen,
			NativeRevision: s.native.Revision(), Directory: s.proofResources.Directory.Directory()},
		resources: *s.proofResources, buffer: s.bufferID, resume: s.proof, word: word, add: add,
	}
	intent := copyIntent(&request.intent)
	intent.proofDictionary = request
	s.sequence++
	s.pending, s.resume, s.mode = copyIntent(intent), s.mode, Waiting
	p.phase = ProofDictionaryPending
	s.proof, s.notice = &p, ""
	return s, intent, nil
}

func (p *proofDictionaryRequest) matches(i *Intent) bool {
	if p == nil || i == nil {
		return false
	}
	mirror := *i
	mirror.proofDictionary = nil
	directory := sameWrapper(mirror.Directory, p.intent.Directory)
	mirror.Directory = p.intent.Directory
	return directory && mirror.Operation == p.intent.Operation &&
		mirror.Revision == p.intent.Revision && mirror.Screen == p.intent.Screen &&
		mirror.NativeRevision == p.intent.NativeRevision && mirror.Kind == p.intent.Kind &&
		mirror.Name == p.intent.Name && mirror.firstProof == nil && mirror.everydayProof == nil &&
		mirror.macroProof == nil && mirror.Selection == nil && mirror.Document == nil &&
		mirror.Destination == nil && mirror.Decision == 0 && len(mirror.Candidate) == 0 &&
		mirror.MacroRun == 0 && mirror.MacroRequest == 0 && mirror.MacroParent == [32]byte{} && mirror.Repeat == 0
}

// ExecuteProofreading performs one checked dictionary operation outside Reduce.
func ExecuteProofreading(ctx context.Context, i *Intent) Result {
	if i == nil {
		return Result{Err: refuse("missing proofreading dictionary request")}
	}
	out := Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind}
	p := i.proofDictionary
	if !p.matches(i) || !p.claimed.CompareAndSwap(false, true) {
		out.Err = refuse("invalid, cancelled or previously dispatched dictionary request")
		return out
	}
	id := storage.PublicationID{Operation: i.Operation, Revision: i.Revision}
	var supplementary *proofreading.Supplementary
	published := false
	if p.add {
		prior := p.resources.Supplementary
		var accepted bool
		accepted, out.Err = prior.Accepts(p.word.text)
		if out.Err == nil {
			supplementary, out.Err = prior.Add(ctx, p.word.text, id)
			published = !accepted && out.Err == nil
		}
	} else {
		supplementary, out.Err = proofreading.OpenSupplementary(ctx, p.resources.Workspace, p.resources.Directory, i.Name)
		if out.Err == nil && !supplementary.Exists() {
			supplementary, out.Err = supplementary.Create(ctx, id)
			published = out.Err == nil
		}
	}
	if out.Err == nil {
		out.Outcome = storage.Outcome{State: storage.Unchanged, Name: supplementary.Name(), DirectoryID: i.Directory.ID()}
		if published {
			out.Outcome.State = storage.Published
		}
	}
	out.proofDictionary = &proofDictionaryObservation{request: p, supplementary: supplementary, result: copyResult(out)}
	return out
}

func (s Session) cancelProofDictionary() (Session, *Intent, error) {
	p := s.pending.proofDictionary
	prevented := p.claimed.CompareAndSwap(false, true)
	s.pending, s.mode, s.proof = nil, s.resume, p.resume
	if prevented {
		s.notice = "Supplementary dictionary operation cancelled"
	} else {
		s.notice = "Supplementary dictionary operation detached; publication may have occurred"
	}
	return s, nil, nil
}

func (s Session) completeProofDictionary(result Result) (Session, *Intent, error) {
	observation := result.proofDictionary
	if observation == nil {
		return s, nil, refuse("unauthenticated proofreading dictionary completion")
	}
	p := observation.request
	if result.Operation != p.intent.Operation || result.Revision != p.intent.Revision || result.Kind != p.intent.Kind {
		return s, nil, refuse("proofreading dictionary completion envelope mismatch")
	}
	result = copyResult(observation.result)
	if s.bufferID != p.buffer && (s.other == nil || s.other.bufferID != p.buffer) {
		return s, nil, refuse("foreign proofreading dictionary completion")
	}
	if !p.settled.CompareAndSwap(false, true) {
		return s, nil, refuse("proofreading dictionary completion already settled")
	}
	if s.pending == nil || s.pending.proofDictionary != p {
		s.detached = receipt(result, false)
		if s.pending == nil && s.detached.DestinationMayExist {
			s.notice = "Detached supplementary dictionary operation completed; reopen it to refresh"
		}
		return s, nil, nil
	}
	if s.screen != p.intent.Screen || s.bufferID != p.buffer ||
		s.revision != p.intent.Revision || s.native.Revision() != p.intent.NativeRevision {
		s.pending, s.mode, s.proof = nil, s.resume, p.resume
		s.detached = receipt(result, false)
		s.notice = "Stale supplementary dictionary completion; reopen it to refresh"
		return s, nil, nil
	}
	s.pending, s.mode, s.proof = nil, s.resume, p.resume
	s.last = receipt(result, result.Err == nil)
	if result.Err != nil {
		s.notice = result.Err.Error()
		return s, nil, nil
	}
	resources := *s.proofResources
	resources.Supplementary = observation.supplementary
	s.proofResources = &resources
	if s.other != nil {
		other := *s.other
		other.proofResources = &resources
		s.other = &other
	}
	if !p.add {
		return s.proofMenu(*s.proof), nil, nil
	}
	next, intent, err := s.skipProof(false)
	if err != nil {
		s.notice = err.Error()
		return s, nil, nil
	}
	return next, intent, nil
}
