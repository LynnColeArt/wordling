package editor

import (
	"fmt"

	"github.com/lynncoleart/wordling/internal/document"
)

// RecoveryCopy describes a buffer without granting access to its source file.
type RecoveryCopy struct {
	Name, Parent string
	Gap          int
	Native       *document.Document
}

func (s Session) RecoveryCopy(screen uint8) RecoveryCopy {
	if screen != s.screen {
		if screen >= 1 && screen <= MaxDocumentScreens && s.screens[screen-1] != nil {
			s = *s.screens[screen-1]
		} else if s.other == nil || s.other.screen != screen {
			return RecoveryCopy{}
		} else {
			s = *s.other
		}
	}
	if !s.dirty() || s.native == nil {
		return RecoveryCopy{}
	}
	copy := RecoveryCopy{Name: s.name, Gap: s.cursor.Gap(), Native: s.Document()}
	if s.workspaceBase != nil && s.name != "" {
		copy.Parent = s.workspaceBase.DOSPath()
	}
	return copy
}

// RestoreRecovery opens a detached, unsaved copy. Save uses the ordinary
// new-document flow, which asks before replacing an existing file.
func (s Session) RestoreRecovery(raw []byte, gap int) (Session, error) {
	if s.workspace == nil || s.mode != Editing || s.dirty() || s.source != nil {
		return s, fmt.Errorf("recovery requires an empty document screen")
	}
	d, err := document.Parse(raw)
	if err != nil {
		return s, err
	}
	cursor, err := d.CursorAt(min(max(gap, 0), d.TokenCount()))
	if err != nil {
		return s, err
	}
	history, historyErr := document.NewHistory(d)
	s.native, s.cursor = d, cursor
	s.history, s.historyValid = history, historyErr == nil
	s.mergeSource = d.CheckMergeSource() == nil
	s.revision++
	return s, nil
}
