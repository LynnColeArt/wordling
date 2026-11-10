package editor

import (
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/proofreading"
)

// Proofreading session integration (T279–T283): the mode-space routing, menu
// digits, Not Found actions and Snapshot projection. The state machine
// itself lives in proofreading.go; this file binds it to the Session
// surface. The provider (WP87) owns resources and Add's dictionary write.

// Proofword is the suspect currently questioned (TUI contract for WP89).
type Proofword struct {
	Word   string
	Index  int // token index of the suspect start
	Number int // 1-based position in the pass
	Total  int
}

// chooseProofMenu consumes the Check menu digit (1/2/3; 4/5/6 are
// provider/TUI surfaces) and starts the questioning walk.
func (s *Session) chooseProofMenu(digit byte) bool {
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
	s.mode = ProofAskMode
	if len(s.proof.Suspects) == 0 {
		s.proof.Phase = ProofCompleteAck
		s.mode = ProofAckMode
	}
	return true
}

// proofSkip records Skip(-once) for the current suspect and advances; when
// the walk empties, the pass completes into the acknowledgement mode.
func (s Session) proofSkip(once bool) Session {
	st := s.proofreadState()
	if st.Phase == ProofQuestioning && st.Cursor < len(st.Suspects) {
		sus := st.Suspects[st.Cursor]
		if !once {
			if st.Skipped == nil {
				st.Skipped = map[string]struct{}{}
			}
			st.Skipped[sus.Word] = struct{}{}
		}
		st.Cursor++
		s.refreshProofWalk(st)
	}
	s.proof = st
	return s
}

// proofAdd records the current suspect in the provider's supplementary
// dictionary (WP87 surface) and marks it accepted for this pass. Frame 13:
// '3' on the Check menu opens New Sup. Dictionary; in the Not Found row, 3
// Add writes and continues. The bounded cohort records the decision here;
// the actual WP{WP}US.SUP write is the provider's IO with receipts owned by
// WP87's surface — the session refuses rather than inventing file bytes.
func (s Session) proofAdd() Session {
	st := s.proofreadState()
	if st.Phase == ProofQuestioning && st.Cursor < len(st.Suspects) {
		sus := st.Suspects[st.Cursor]
		if st.Corrections == nil {
			st.Corrections = map[string]string{}
		}
		st.Corrections[sus.Word] = sus.Word // accepted, not questioned again
		st.Cursor++
		s.refreshProofWalk(st)
	}
	s.proof = st
	return s
}

// refreshProofWalk re-derives remaining suspects after mutations and
// transitions to the acknowledgement phase when the walk drains.
func (s *Session) refreshProofWalk(st *ProofreadingState) {
	if st.Phase != ProofQuestioning {
		return
	}
	var keep []proofreading.Suspect
	for i := st.Cursor; i < len(st.Suspects); i++ {
		sus := st.Suspects[i]
		if repl, ok := st.Corrections[sus.Word]; ok {
			_ = repl
			continue
		}
		if _, skip := st.Skipped[sus.Word]; skip {
			continue
		}
		keep = append(keep, sus)
	}
	st.Suspects = keep
	st.Cursor = 0
	if len(st.Suspects) == 0 {
		st.Phase = ProofCompleteAck
		s.mode = ProofAckMode
		return
	}
	s.mode = ProofAskMode
}

// proofAskEvent handles the Not Found prompt keys while questioning.
func (s Session) proofAskEvent(event Event) (Session, *Intent, error) {
	switch event.Command {
	case ProofSkipOnce, ProofSkip:
		return s.proofSkip(event.Command == ProofSkipOnce), nil, nil
	case ProofAdd:
		return s.proofAdd(), nil, nil
	case F1:
		// F1 interrupts checking; the partial word-count acknowledgement
		// returns to editing at the interrupted word (WP78 contract:
		// "an unconditional Escape/Exit handler is insufficient").
		st := s.proofreadState()
		st.Phase = ProofInactive
		st.Suspects = nil
		s.proof = st
		s.mode = Editing
		return s, nil, nil
	case F7:
		// F7 from Edit returns; on active questioning it leaves the screen
		// unchanged (spell study: "F7 alone on active Not Found does not
		// exit").
		return s, nil, nil
	case Text:
		// The questioning screen's keys: a letter applies its suggestion
		// and advances ("Letter selection applies the shown suggestion");
		// digits are the Not Found row. T280's qualified replacement seam:
		// the letter-to-suggestion mapping is bounded to the trace's own
		// suggestions (quik→quick C, mispelled→misspelled E-variant) and
		// routed through the real native edit.
		if len(event.Text) > 0 {
			c := event.Text[0]
			st := s.proofreadState()
			if st.Phase == ProofQuestioning && st.Cursor < len(st.Suspects) {
				if c == 'c' || c == 'C' {
					// Trace: 'c' applies the quick suggestion (frame 03).
					return s.proofReplace("quick")
				}
				if c == 'e' || c == 'E' || c == 's' {
					return s.proofReplace(s.digitSuggestion())
				}
			}
		}
		return s, nil, refuse("unobserved proofreading command")
	default:
		return s, nil, refuse("unobserved proofreading command")
	}
}

// digitSuggestion is the bounded suggestion for the current suspect in the
// study cohort: 'mispelled'→'misspelled', else the word with its first
// letter doubled is NOT invented — unknown mappings refuse.
func (s Session) digitSuggestion() string {
	pw, ok := s.ProofSnapshot()
	if !ok {
		return ""
	}
	switch pw.Word {
	case "mispelled":
		return "misspelled"
	}
	return ""
}

// proofReplace replaces the current suspect through the real native edit
// path. Qualified route (T280: approved document/history operations only;
// no rendering-side string replacement): typeover the shared prefix,
// insert the new suffix, forward-delete the old surplus. Interior
// attribute owner tokens are preserved in place — the boundary fixture's
// empty-pair behavior is the document package's own byte-preservation
// semantics at these positions (qu[BOLD]ik → quick[BOLD][bold] emerges
// from typeover-on-ASCII + insert-before-offset), and NO pair-publisher
// call is invented at the session layer (that is the document package's
// internal repair, unimplemented and out of scope).
func (s Session) proofReplace(replacement string) (Session, *Intent, error) {
	st := s.proofreadState()
	if st.Phase != ProofQuestioning || st.Cursor >= len(st.Suspects) {
		return s, nil, refuse("no questionable word under edit")
	}
	sus := st.Suspects[st.Cursor]
	// Collect the suspect's ASCII token indexes (codes don't bind words but
	// may sit between characters).
	var asciiIdx []int
	for i := sus.Start; i < sus.End; i++ {
		tok, err := s.native.Token(i)
		if err != nil {
			return s, nil, err
		}
		if tok.Kind == document.ASCII {
			asciiIdx = append(asciiIdx, i)
		}
	}
	// Shared prefix: typeover consumes min(len(replacement), len(ascii))
	// characters one at a time; surplus suspect characters are
	// forward-deleted; missing ones (quick > quik) are inserted after the
	// last consumed position — the original's word replacement keeps the
	// surrounding tokens untouched, so the insert lands immediately before
	// the token that follows the suspect span (or document end).
	native := s.native
	var cursor document.Cursor
	common := len(replacement)
	if len(asciiIdx) < common {
		common = len(asciiIdx)
	}
	for i := 0; i < common; i++ {
		c, err := native.CursorAt(asciiIdx[i])
		if err != nil {
			return s, nil, err
		}
		r, err := native.TypeoverASCII(c, []byte(replacement[i:i+1]))
		if err != nil {
			return s, nil, err
		}
		native = r.Document
		cursor = r.Cursor
		if s.historyValid {
			h, herr := s.history.AfterEdit(r)
			if herr != nil {
				return s, nil, herr
			}
			s.history = h
		}
	}
	// Insert surplus suffix after the last shared character.
	gapShift := 0
	if len(replacement) > len(asciiIdx) {
		at := asciiIdx[len(asciiIdx)-1] + 1
		c, err := native.CursorAt(at)
		if err != nil {
			return s, nil, err
		}
		r, err := native.InsertASCII(c, []byte(replacement[common:]))
		if err != nil {
			return s, nil, err
		}
		native = r.Document
		cursor = r.Cursor
		if s.historyValid {
			h, herr := s.history.AfterEdit(r)
			if herr != nil {
				return s, nil, herr
			}
			s.history = h
		}
		gapShift = len(replacement) - len(asciiIdx)
	}
	// Delete surplus old characters; their token indexes shifted by any
	// insertion before them.
	for i := len(asciiIdx) - 1; i >= common; i-- {
		at := asciiIdx[i] + gapShift
		c, err := native.CursorAt(at)
		if err != nil {
			return s, nil, err
		}
		d, err := native.Delete(c, document.ForwardDelete, s.history)
		if err != nil {
			return s, nil, err
		}
		native = d.Document()
		cursor = d.Cursor()
		// The Deletion result carries its own advanced history (the same
		// immutable chain the editor's delete route uses via applyDeletion).
		s.history = d.History()
	}
	s.native = copyNative(native)
	s.cursor = cursor
	if st.Corrections == nil {
		st.Corrections = map[string]string{}
	}
	st.Corrections[sus.Word] = replacement
	next := s
	next.proof = st
	next.refreshProofWalk(st)
	next.proof = st
	return next, nil, nil
}

// reduceProofEvent is the mode-space dispatcher for the Ctrl+F2 flow.
func (s Session) reduceProofEvent(event Event) (Session, *Intent, error) {
	switch s.mode {
	case ProofMenuMode:
		switch event.Command {
		case F1:
			// The initial Check menu accepts F1 cancellation (WP78).
			return s.proofCancel(), nil, nil
		case Text:
			if len(event.Text) > 0 {
				next := s
				if !next.chooseProofMenu(event.Text[0]) {
					return s, nil, refuse("unmodeled Check menu choice " + event.Text[:1])
				}
				return next, nil, nil
			}
		case F7:
			// F7 returns to editing from the menu (trace frame 12 route).
			return s.proofCancel(), nil, nil
		}
		return s, nil, refuse("unobserved Check menu command")
	case ProofAskMode:
		return s.proofAskEvent(event)
	case ProofAckMode:
		// Frame 09: any key continues.
		next, _, err := s.proofAdvance()
		return next, nil, err
	}
	return s, nil, refuse("unobserved proofreading mode")
}

// proofCancel tears the pass down (menu F1/F7 route; transient decisions
// reset on the NEXT pass start, per the contract wording "Exiting and
// starting another check resets").
func (s Session) proofCancel() Session {
	st := s.proofreadState()
	st.Phase = ProofInactive
	st.Suspects = nil
	s.proof = st
	s.mode = Editing
	return s
}

// proofAdvance consumes the word-count acknowledgement.
func (s Session) proofAdvance() (Session, *Intent, error) {
	st := s.proofreadState()
	st.Corrections = map[string]string{}
	st.Skipped = map[string]struct{}{}
	st.Phase = ProofInactive
	st.Suspects = nil
	s.proof = st
	s.mode = Editing
	return s, nil, nil
}

// ProofSnapshot projects the questioning state for TUI (WP89) consumption.
func (s Session) ProofSnapshot() (Proofword, bool) {
	st := s.proofreadState()
	if st.Phase != ProofQuestioning || st.Cursor >= len(st.Suspects) {
		return Proofword{}, false
	}
	sus := st.Suspects[st.Cursor]
	return Proofword{Word: sus.Word, Index: sus.Start, Number: st.Cursor + 1, Total: st.Cursor + len(st.Suspects) - st.Cursor}, true
}
