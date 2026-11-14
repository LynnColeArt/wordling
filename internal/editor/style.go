package editor

import "github.com/lynncoleart/wordling/internal/document"

func (s Session) CreateNamedStyle(name string) (Session, error) {
	if s.mode != Editing || s.native == nil || s.workspace == nil || s.selection || s.mergeSource {
		return s, refuse("Styles require ordinary editing")
	}
	edit, err := s.native.CreateNamedStyle(s.cursor, name)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) ApplyNamedStyle(style document.NamedStyle) (Session, error) {
	if s.mode != Editing || s.native == nil || s.workspace == nil || s.selection || s.mergeSource {
		return s, refuse("Styles require ordinary editing")
	}
	edit, err := s.native.ApplyNamedStyle(s.cursor, style)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) CloseNamedStyle() (Session, error) {
	if s.native == nil || !s.native.AtStyleEnd(s.cursor) {
		return s, refuse("The cursor is not inside a named style")
	}
	cursor, err := s.native.CursorAt(s.cursor.Gap() + 3)
	if err != nil {
		return s, err
	}
	s.cursor = cursor.WithReveal(s.cursor.Reveal())
	return s, nil
}
