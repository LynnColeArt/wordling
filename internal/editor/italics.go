package editor

func (s Session) ToggleItalics() (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource || s.over || s.homes != 0 {
		return s, refuse("Italics requires ordinary editing")
	}
	edit, err := s.native.ToggleItalics(s.cursor)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
