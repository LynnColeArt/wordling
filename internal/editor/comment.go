package editor

func (s Session) InsertComment(text string) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Comment requires ordinary document editing")
	}
	edit, err := s.native.InsertComment(s.cursor, text)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
