package editor

import "github.com/lynncoleart/wordling/internal/document"

func (s Session) AuthoritySelection() (string, error) {
	if s.mode != Editing || s.native == nil || s.workspace == nil || !s.selection || s.mergeSource {
		return "", refuse("Select the citation text before marking an authority")
	}
	return s.native.AuthoritySelection(s.anchor, s.cursor)
}

func (s Session) MarkAuthority(section int, short, full string) (Session, error) {
	if _, err := s.AuthoritySelection(); err != nil {
		return s, err
	}
	edit, err := s.native.MarkAuthority(s.anchor, s.cursor, section, short, full)
	if err != nil {
		return s, err
	}
	next, err := s.adoptEverydayEdit(edit)
	if err != nil {
		return s, err
	}
	next.selection, next.blockMoved, next.anchor = false, false, document.Cursor{}
	return next, nil
}
