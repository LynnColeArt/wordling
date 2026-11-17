package editor

import (
	"github.com/lynncoleart/wordling/internal/document"
	"time"
)

func (s Session) InsertDateText(now time.Time) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Date Text requires ordinary document editing")
	}
	edit, err := s.native.InsertASCII(s.cursor, []byte(document.FormatDate(now)))
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) InsertDateCode() (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Date Code requires ordinary document editing")
	}
	edit, err := s.native.InsertDateCode(s.cursor)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
