package editor

func (s Session) ExtendHorizontalDrawing(start, steps int, double bool) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Line Draw requires ordinary editing")
	}
	pos, err := s.EverydayPosition()
	if err != nil || pos.Pos <= 0 || pos.Pos >= 66 {
		return s, refuse("draw within one fixed-pitch line")
	}
	edit, err := s.native.ExtendHorizontalDrawing(s.cursor, start, steps, double)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
