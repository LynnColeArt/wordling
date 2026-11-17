package editor

import "github.com/lynncoleart/wordling/internal/document"

func (s Session) PageNumberPosition() int {
	for i := s.cursor.Gap() - 1; s.native != nil && i >= 0; i-- {
		t, _ := s.native.Token(i)
		if p := t.PageNumberPosition(); p != 0 {
			return p
		}
	}
	return 0
}

func (s Session) SetPageNumberPosition(position int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Page numbering requires ordinary document editing")
	}
	edit, err := s.native.SetPageNumberPosition(s.cursor, position)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) PageNumberSuppressed() bool {
	for i := s.cursor.Gap() - 1; s.native != nil && i >= 0; i-- {
		t, _ := s.native.Token(i)
		switch t.Kind {
		case document.HardPage, document.SoftPage, document.DeletedSoftPage, document.HardReturnSoftPage:
			return false
		case document.SuppressPageNumber:
			return true
		}
	}
	return false
}

func (s Session) SuppressPageNumber() (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Suppress Page Numbering requires ordinary document editing")
	}
	if s.PageNumberSuppressed() {
		return s, nil
	}
	edit, err := s.native.SuppressPageNumber(s.cursor)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
