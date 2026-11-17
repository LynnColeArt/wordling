package document

// This is a finite history-knowledge state inside the existing History, not an
// inferred Add/Skip/Clear rule. Four actual positions can be indistinguishable;
// stored fragments do not assert the original hidden entry count or ordering.
type seedQualification uint8

const (
	seedUnqualified seedQualification = iota
	seedAwaitingBrowse
	seedBrowsed
	seedRightSeparated
)

type historyObservation struct {
	closing, restored, browsed bool
	gap                        int
	reveal                     bool
}

// The qualification class fixes command order, view and token shape, while all
// character identities/fragments come from the actual immutable native values.
// Character values are not control commands or prerecorded-screen selectors.
func wp40Shape(state *revisionState) bool {
	d := &Document{state: state}
	if !d.valid() || d.TokenCount() != 6 {
		return false
	}
	for i, k := range []Kind{ASCII, BoldOn, ASCII, ASCII, BoldOff, ASCII} {
		token, _ := d.Token(i)
		if token.Kind != k {
			return false
		}
	}
	return true
}
func (h History) wp40Target(s deletionState) bool {
	if h.state == nil || h.state.observed != nil || h.state.seedStage != seedRightSeparated || h.state.seedView != s.cursor.reveal || !wp40Shape(h.state.document) {
		return false
	}
	if h.state.count != 1 || len(h.state.entries[0].fragment.kinds) != 1 || h.state.entries[0].fragment.kinds[0] != ASCII || h.state.entries[0].commands != 1 {
		return false
	}
	return s.kind == PairDeletion || (s.kind == ClosingRepair && s.blockStart == 4 && s.blockEnd == 5 && s.cursor.reveal)
}
func (h History) observeTarget(s deletionState, closing fragment, after *revisionState) History {
	next := *h.state
	next.document = after
	next.groupOpen = false
	next.groupUnknown = false
	next.seedStage = 0
	gap := s.target
	if s.kind == ClosingRepair {
		gap = s.blockEnd
	} else if s.target == s.off {
		gap--
	}
	next.observed = &historyObservation{closing: s.kind == ClosingRepair, gap: gap, reveal: s.cursor.reveal}
	if s.kind == ClosingRepair {
		next.entries[1] = next.entries[0]
		next.entries[0] = historyEntry{fragment: closing, kind: ClosingRepair, commands: 1}
		next.count = 2 // number of distinct stored observed fragments, NOT stack size.
	}
	return History{&next}
}
func (p Preview) fragmentIndex() int {
	if p.state.history.observed != nil {
		if p.state.history.observed.closing {
			return p.state.index % 2
		}
		return 0
	}
	return p.state.index
}
