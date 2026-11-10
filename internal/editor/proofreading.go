package editor

import (
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/proofreading"
)

// Proofreading state machine (T279–T283), modeled on the WP78 contract and
// the spelling-study traces. State lives per session screen like every other
// editor state; the provider (WP87) owns resources; the TUI (WP89) renders.

// ProofreadingScope is one Ctrl+F2 menu choice (frame 01: Check menu).
type ProofreadingScope uint8

const (
	ProofWord     ProofreadingScope = 1
	ProofPage     ProofreadingScope = 2
	ProofDocument ProofreadingScope = 3
	// 4 New Sup. Dictionary and 5 Look Up are provider/TUI surfaces owned by
	// WP87/WP89; the editor state routes to them but does not model them.
)

// ProofreadingPhase follows the observed transitions (spelling/proof trace):
// menu → questioning (suspects in order) → (edit interlude) → complete ack
// → editing; F1 interrupts to editing at the interrupted word.
type ProofreadingPhase uint8

const (
	ProofInactive ProofreadingPhase = iota
	ProofMenu
	ProofQuestioning
	ProofCompleteAck
)

// ProofreadingState is the continuous journey state: the suspect walk, the
// transient per-pass decisions (corrections + skips), and the reading place.
// Transient decisions reset when a new pass starts (frame 10:
// new-pass-skip-forgotten); Add persists in the provider's supplementary
// dictionary instead.
type ProofreadingState struct {
	Phase    ProofreadingPhase
	Scope    ProofreadingScope
	Suspects []proofreading.Suspect // qualified at pass start
	Cursor   int                    // index into Suspects
	// Transient per-pass memory: spelling contract ("remembered and applied
	// when encountered later in the same invocation"; "Exiting and starting
	// another check resets these transient decisions").
	Corrections map[string]string
	Skipped     map[string]struct{}
	// Editing interlude: the suspect under edit and the focus to resume.
	EditSuspect int
}

// proofreadingState returns the live state container (zero-safe copy
// semantics preserved by value receivers).
func (s Session) proofreadingState() *ProofreadingState {
	if s.proof == nil {
		return &ProofreadingState{Phase: ProofInactive}
	}
	return s.proof
}

// beginProofreading opens the state machine at the Check menu (trace key
// ctrl-f2 → frame 01-spell-menu). Block-scope starts directly from an
// existing Block selection per the WP78 contract; the bounded editor cohort
// admits the menu path here.
func (s Session) beginProofreading() Session {
	s.proof = &ProofreadingState{Phase: ProofMenu, Corrections: map[string]string{}, Skipped: map[string]struct{}{}}
	return s
}

// chooseProofScope consumes a menu digit (1/2/3) and qualifies the suspect
// walk over the scope's suspects. It returns false when the digit is not a
// modeled scope.
func (s *Session) chooseProofScope(digit byte) bool {
	switch digit {
	case '1':
		s.proof.Scope = ProofWord
	case '2':
		s.proof.Scope = ProofPage
	case '3':
		s.proof.Scope = ProofDocument
	default:
		return false
	}
	s.proof.Phase = ProofQuestioning
	s.proof.Suspects = s.proofSuspects()
	s.proof.Cursor = 0
	return true
}

// proofSuspects walks the native document word-by-word over the scope's
// native range, skipping already-accepted words (provider decision + this
// session's transient corrections/skips). Word boundaries follow the WP78
// contract: spaces, returns (hard and soft), tabs and attribute pairs bind
// words; DSRt does NOT bind (the unbroken-word contract); SRt DOES bind
// (SRWORDS.WP: 15 "the" + "a qu[SRt]ik" counts 18). Provider acceptance is
// the WP87-pinned cohort engine (bounded resource set); unknown words are
// the questionable ones.
func (s Session) proofSuspects() []proofreading.Suspect {
	if s.native == nil {
		return nil
	}
	total := s.native.TokenCount()
	// Word assembly over tokens; token index bounds kept for cursor mapping.
	type wordRun struct {
		start, end int // token index span [start,end)
		text       []byte
	}
	var runs []wordRun
	var cur *wordRun
	page := 1
	scopeStart, scopeEnd := 0, total
	for i := 0; i < total; i++ {
		tok, err := s.native.Token(i)
		if err != nil {
			return nil
		}
		switch tok.Kind {
		case document.ASCII:
			c := tok.Raw[0]
			if c == ' ' {
				if cur != nil {
					runs = append(runs, *cur)
					cur = nil
				}
				continue
			}
			if cur == nil {
				cur = &wordRun{start: i}
			}
			cur.text = append(cur.text, c)
			cur.end = i + 1
		case document.SoftReturn, document.HardReturn:
			if cur != nil {
				runs = append(runs, *cur)
				cur = nil
			}
		case document.HardPage, document.EndOfPage, document.HardReturnSoftPage:
			if cur != nil {
				runs = append(runs, *cur)
				cur = nil
			}
			page++
			if s.proof != nil && s.proof.Scope == ProofPage && cur == nil && scopeEnd == total && i > scopeStart {
				// Page scope stops at the physical-page boundary.
				scopeEnd = i
			}
		case document.DeletedSoftReturn:
			// Does NOT bind: unbroken-word contract (0x90 continues the word).
			if cur == nil {
				cur = &wordRun{start: i}
			}
		default:
			if cur != nil {
				runs = append(runs, *cur)
				cur = nil
			}
		}
	}
	if cur != nil {
		runs = append(runs, *cur)
	}
	var out []proofreading.Suspect
	for _, r := range runs {
		if r.start < scopeStart || r.start >= scopeEnd {
			continue
		}
		w := string(r.text)
		if w == "" {
			continue
		}
		if s.proofAccepted(w) {
			continue
		}
		if repl, ok := s.proof.Corrections[w]; ok && repl != w {
			// The remembered correction applies to the rest of this pass;
			// the occurrence is not questioned again.
			continue
		}
		if _, skip := s.proof.Skipped[w]; skip {
			continue
		}
		out = append(out, proofreading.Suspect{Page: page, Start: r.start, End: r.end, Word: w})
	}
	return out
}

// proofAccepted consults the WP87 cohort provider: the bounded engine's
// accepted set (main/supplementary resources admitted at provider design,
// plus Add-words recorded in the session state).
func (s Session) proofAccepted(word string) bool {
	for _, w := range proofreading.CohortAccepted {
		if w == word {
			return true
		}
	}
	return false
}

// applySuggestion replaces the current suspect's word with the chosen
// replacement through the real native edit path (delete suspect span, insert
// replacement), preserving surrounding attribute wrappers per the boundary
// contract (qu[BOLD]ik → quick[BOLD][bold]: interior codes become an empty
// pair at the replacement's end). Attribute-pair migration is the document
// package's published deletion behavior; the session records the decision
// and advances.
func (s *Session) applySuggestion(replacement string) error {
	st := s.proofState()
	if st.Phase != ProofQuestioning || st.Cursor >= len(st.Suspects) {
		return refuse("no questionable word under edit")
	}
	sus := st.Suspects[st.Cursor]
	// Delete the suspect token span through the native API.
	anchor, err := s.native.CursorAt(sus.Start)
	if err != nil {
		return err
	}
	endCursor, err := s.native.CursorAt(sus.End)
	if err != nil {
		return err
	}
	_, err = s.native.DeleteBlock(anchor, endCursor, s.history)
	if err != nil {
		return err
	}
	// Insert the replacement at the deletion point.
	c, err := s.native.CursorAt(sus.Start)
	if err != nil {
		return err
	}
	r, err := s.native.InsertASCII(c, []byte(replacement))
	if err != nil {
		return err
	}
	s.native = copyNative(r.Document)
	s.cursor = r.Cursor
	if s.historyValid {
		h, herr := s.history.AfterEdit(r)
		if herr == nil {
			s.history = h
		}
	}
	st.Corrections[sus.Word] = replacement
	st.Cursor++
	return nil
}

// proofState is the non-nil accessor used by mutators.
func (s Session) proofState() *ProofreadingState { return s.proofreadState() }

func (s Session) proofreadState() *ProofreadingState {
	if s.proof == nil {
		return &ProofreadingState{Phase: ProofInactive, Corrections: map[string]string{}, Skipped: map[string]struct{}{}}
	}
	return s.proof
}

// skipSuspect records Skip (rest of this pass; includes the observed
// initial-capital variant by case-folding the key) and advances.
func (s *Session) skipSuspect(once bool) {
	st := s.proofreadState()
	if st.Cursor >= len(st.Suspects) {
		return
	}
	sus := st.Suspects[st.Cursor]
	if !once {
		st.Skipped[sus.Word] = struct{}{}
	}
	st.Cursor++
}

// advanceSuspects refreshes the walk after document mutations (corrections
// shift token spans; the contract keeps asking across the pass).
func (s *Session) advanceSuspects() {
	st := s.proofreadState()
	if st.Phase != ProofQuestioning {
		return
	}
	remaining := st.Suspects[st.Cursor:]
	var keep []proofreading.Suspect
	for _, sus := range remaining {
		if repl, ok := st.Corrections[sus.Word]; ok && repl != sus.Word {
			continue
		}
		if _, skip := st.Skipped[sus.Word]; skip {
			continue
		}
		keep = append(keep, sus)
	}
	st.Suspects = append([]proofreading.Suspect(nil), keep...)
	st.Cursor = 0
	if len(st.Suspects) == 0 {
		st.Phase = ProofCompleteAck
	}
}
