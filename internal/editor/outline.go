package editor

func (s Session) StartOutline() (Session, error) {
	if s.mode != Editing || s.native == nil || s.workspace == nil || s.selection || s.mergeSource {
		return s, refuse("Outline requires ordinary document editing")
	}
	edit, err := s.native.StartOutline(s.cursor)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) nextOutline(changeLevel bool) (Session, error) {
	edit, err := s.native.NextOutline(s.cursor, changeLevel)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
