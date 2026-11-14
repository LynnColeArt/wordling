package editor

import (
	"github.com/lynncoleart/wordling/internal/document"
	"time"
)

func (s Session) SetSummary(summary *document.Summary) (Session, error) {
	if s.mode != Editing || s.native == nil {
		return s, refuse("document summary requires the editor")
	}
	result, err := s.native.WithSummary(s.cursor, summary)
	if err != nil || !result.Changed {
		return s, err
	}
	if s.historyValid {
		s.history, err = s.history.AfterSummary(result)
		if err != nil {
			return s, err
		}
	}
	s.native, s.cursor = result.Document, result.Cursor
	s.revision++
	s.lastSave, s.notice = NotSaved, ""
	return s, nil
}

func (s Session) CaptureSummary(summary document.Summary) document.Summary {
	return s.native.CaptureSummary(summary)
}

// SummaryRevisionDate reports the timestamp of the last saved revision.
func (s Session) SummaryRevisionDate() time.Time {
	if s.source == nil {
		return time.Time{}
	}
	return s.source.Identity().Modified
}
