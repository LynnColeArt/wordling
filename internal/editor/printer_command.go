package editor

func (s Session) InsertPrinterCommand(text string) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Printer Command requires ordinary document editing")
	}
	edit, err := s.native.InsertPrinterCommand(s.cursor, text)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
