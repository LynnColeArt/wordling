package editor

import "github.com/lynncoleart/wordling/internal/document"

// newMacroTarget is an immutable fact captured before the name prompt. It is
// neither an exported permission nor global consumption of persistent Sessions.
// The UI owner schedules once; the execution driver owns its current transition.
type newMacroTarget struct {
	birth           document.Birth
	genesis, native document.Revision
	history         document.HistoryRevision
	buffer          *bufferIdentity
	screen          uint8
	revision        uint64
	entry           *transitionIdentity
}

func (s Session) pristineNewMacro() bool {
	return s.initialized && s.bufferID != nil && s.transition != nil && s.native != nil && s.native.Birth().IsNew() &&
		s.newPhase == NewUnpublished && s.genesis != (document.Revision{}) && s.native.Revision() == s.genesis &&
		s.source == nil && s.first == nil && s.other == nil && s.screen == 1 && s.mode == Editing && s.revision == 1 && s.sequence == 0 &&
		s.native.TokenCount() == 0 && s.cursor.Gap() == 0 && !s.cursor.Reveal() && !s.over && !s.selection && s.homes == 0 &&
		s.deletion == (document.Deletion{}) && s.preview == (document.Preview{}) && s.anchor == (document.Cursor{}) &&
		s.historyValid && !s.historyUsed && s.history.Qualified() && s.history.CountKnown() && s.history.Count() == 0 && s.history.Revision() == s.genesisHistory &&
		s.macroRepeat == 1 && s.macroOwner == nil && s.macroReady == nil && !s.macroDelivery && s.pending == nil && s.newMacro == nil &&
		s.name == "" && s.draft == "" && s.original == "" && s.caret == 0 && s.target == nil && s.targetDir == nil && s.targetName == "" &&
		!s.fromExit && !s.touched && !s.editedPrefill && s.provenance == Text && s.saved == (document.Revision{}) &&
		s.publishedRevision == (document.Revision{}) && s.publishedName == "" && s.lastSave == NotSaved &&
		s.last == (Receipt{}) && s.published == (Receipt{}) && s.detached == (Receipt{}) && s.notice == ""
}
func (s Session) captureNewMacro() *newMacroTarget {
	return &newMacroTarget{birth: s.native.Birth(), genesis: s.genesis, native: s.native.Revision(), history: s.history.Revision(), buffer: s.bufferID, screen: s.screen, revision: s.revision, entry: s.transition}
}
func (p *newMacroTarget) current(s Session) bool {
	return p != nil && p.entry != nil && s.newMacro == p && s.initialized && s.native != nil && s.native.Birth() == p.birth && p.birth.IsNew() &&
		s.genesis == p.genesis && s.bufferID == p.buffer && s.screen == p.screen && s.newPhase == NewUnpublished && s.source == nil && s.first == nil && s.other == nil &&
		s.saved == (document.Revision{}) && s.publishedRevision == (document.Revision{}) && s.publishedName == "" && s.name == "" && s.lastSave == NotSaved && s.target == nil && s.targetDir == nil && s.targetName == ""
}
func (p *newMacroTarget) unedited(s Session) bool {
	return p.current(s) && s.native.Revision() == p.native && s.revision == p.revision && s.history.Revision() == p.history &&
		s.native.TokenCount() == 0 && s.cursor.Gap() == 0 && !s.cursor.Reveal() && !s.over && !s.selection && s.homes == 0 && !s.historyUsed && s.historyValid && s.macroRepeat == 1
}
func (s Session) validNewMacroRead(i *Intent) bool {
	p := i.macroProof
	return p != nil && p.target == s.newMacro && p.target.unedited(s) && p.issued != nil && s.transition == p.issued && p.matches(i) && s.mode == Waiting && s.macroOwner == nil
}
