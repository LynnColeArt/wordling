package editor

func (s Session) Language() string {
	if s.native == nil {
		return "US"
	}
	return s.native.LanguageAt(s.cursor.Gap())
}

func (s Session) SetLanguage(code string) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Language requires ordinary document editing")
	}
	edit, err := s.native.InsertLanguage(s.cursor, code)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
