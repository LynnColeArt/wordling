package editor

import "math"

func (s Session) InsertSubdocument(name string) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Subdocument links require ordinary document editing")
	}
	pos, err := s.EverydayPosition()
	if err != nil {
		return s, err
	}
	if !pos.hasPrintedPos {
		return s, refuse("Subdocument link needs a known insertion position")
	}
	edit, err := s.native.InsertSubdocument(s.cursor, name, int(math.Round(pos.printedPos*EverydaySettings().CPI)))
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
