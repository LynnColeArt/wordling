package editor

func (s Session) Kerning() bool {
	return s.native != nil && s.native.KerningAt(s.cursor.Gap())
}

func (s Session) SetKerning(enabled bool) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Kerning requires ordinary editing")
	}
	edit, err := s.native.InsertKerning(s.cursor, enabled)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
