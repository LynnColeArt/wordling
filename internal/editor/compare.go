package editor

import "github.com/lynncoleart/wordling/internal/document"

func (s Session) CompareDisk(path string) (Session, error) {
	if s.mode != Editing || s.workspaceBase == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Document Compare requires ordinary workspace editing")
	}
	raw, err := s.workspaceBase.ReadDOSBytes(path)
	if err != nil {
		return s, err
	}
	other, err := document.Parse(raw)
	if err != nil {
		return s, err
	}
	edit, err := s.native.ComparePlainText(s.cursor, other)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
