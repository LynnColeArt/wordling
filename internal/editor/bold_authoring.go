package editor

import "github.com/lynncoleart/wordling/internal/document"

const (
	boldPresentationOwners = 4096
	boldOpenOwners         = 2
	boldOpenBytes          = 6
	boldRecoveryASCII      = 1
)

// Only E's native-owner-bound history can report an active span. A retained
// handle after clear or Retrieve cannot authorize commands on another buffer.
func (s Session) hasActiveBold() bool {
	_, active := s.history.ActiveBold(s.native)
	return active
}

func (s Session) boldEditingContext() bool {
	return s.initialized && s.transition != nil && s.bufferID != nil &&
		s.mode == Editing && s.screen == 1 && !s.over && !s.selection &&
		s.homes == 0 && s.notice == "" && s.historyValid &&
		s.native != nil && s.native.Birth().IsNew() &&
		s.genesis != (document.Revision{}) && s.genesisHistory != (document.HistoryRevision{}) &&
		s.native.Revision() != (document.Revision{}) && s.cursor.Revision() == s.native.Revision() &&
		s.macroOwner == nil && !s.macroDelivery && s.macroReady == nil &&
		s.newMacro == nil && s.macroRepeat == 1
}

func (s Session) boldBeforeIO() bool {
	return s.source == nil && s.newPhase == NewUnpublished && s.first == nil &&
		s.sequence == 0 && s.pending == nil && s.target == nil &&
		s.targetDir == nil && s.targetName == "" && !s.fromExit &&
		s.name == "" && s.draft == "" && s.original == "" &&
		s.saved == (document.Revision{}) && s.publishedRevision == (document.Revision{}) &&
		s.publishedName == "" && s.lastSave == NotSaved &&
		s.published == (Receipt{}) && s.last == (Receipt{}) && s.detached == (Receipt{}) &&
		!s.historyUsed
}

func (s Session) boldExtent() (owners, nativeBytes int, err error) {
	owners = s.native.TokenCount()
	eof, err := s.native.CursorAt(owners)
	if err != nil {
		return 0, 0, err
	}
	nativeBytes, err = eof.Offset()
	return owners, nativeBytes, err
}

// boldActiveGuard runs after payload validation and after Complete dispatch.
// Active filename modes are defensive only. Neither a real completion nor a
// read-only retry is treated as a user save key.
func (s Session) boldActiveGuard(e Event) error {
	if !s.hasActiveBold() {
		return nil
	}
	switch s.mode {
	case Editing:
		switch e.Command {
		case Bold, Reveal, F7:
			return nil
		case Text:
			return s.boldTextGuard(e.Text)
		default:
			return refuse("command unavailable inside active Bold")
		}
	case ExitSaveQuestion:
		if e.Command != F1 && e.Command != No {
			return refuse("active Bold cannot be saved on exit")
		}
	case SaveName:
		if e.Command == Enter {
			return refuse("active Bold cannot submit a save name")
		}
	case ReplaceQuestion:
		if e.Command == Yes {
			return refuse("active Bold cannot replace a document")
		}
	}
	return nil
}

func (s Session) boldTextGuard(text string) error {
	if !s.boldEditingContext() || !s.boldBeforeIO() {
		return refuse("active Bold Text requires its current unpublished Insert session")
	}
	owners, size, err := s.boldExtent()
	if err != nil {
		return err
	}
	if s.cursor.Gap() != owners-1 || len(text) == 0 ||
		len(text) > boldPresentationOwners-owners || len(text) > document.MaxMutationBytes-size {
		return refuse("active Bold Text requires printable ASCII at Off within capacity")
	}
	for i := range len(text) {
		if text[i] < 0x20 || text[i] > 0x7e {
			return refuse("active Bold Text requires printable ASCII")
		}
	}
	return nil
}

func (s Session) boldWriteGuard(kind IntentKind) error {
	switch kind {
	case Observe, WriteSnapshot, PublishCandidate, PublishNewBuffer:
		if s.hasActiveBold() {
			return refuse("active Bold cannot create a save intent")
		}
	}
	return nil
}

func (s Session) authorBold() (Session, *Intent, error) {
	if !s.boldEditingContext() || !s.boldBeforeIO() {
		return s, nil, refuse("Bold requires its unpublished New editing session")
	}
	var result document.BoldResult
	var err error
	if active, ok := s.history.ActiveBold(s.native); ok {
		result, err = s.native.CloseBold(s.cursor, active)
	} else {
		owners, size, extentErr := s.boldExtent()
		if extentErr != nil {
			return s, nil, extentErr
		}
		if owners > boldPresentationOwners-boldOpenOwners-boldRecoveryASCII ||
			size > document.MaxMutationBytes-boldOpenBytes-boldRecoveryASCII {
			return s, nil, refuse("Bold needs room for both boundaries and one recovery character")
		}
		result, err = s.native.BeginBold(s.cursor)
	}
	if err != nil {
		return s, nil, err
	}
	history, err := s.history.AfterBold(result)
	if err != nil {
		return s, nil, err
	}
	s.native = result.Document()
	s.cursor = result.Cursor()
	s.history = history
	if result.Changed() {
		s.revision++
	}
	return s, nil, nil
}
