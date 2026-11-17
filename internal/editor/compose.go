package editor

// insertComposed writes a character by native set and number, using the same
// history, reflow and dirty-state path as other everyday typing.
func (s Session) insertComposed(set, number byte) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection {
		return s, refuse("Compose requires the everyday editor without an active block")
	}
	if s.mergeSource {
		edit, err := s.native.WriteMergeCharacter(s.cursor, set, number, s.over)
		if err != nil || !edit.Changed {
			return s, err
		}
		next, _, err := s.adoptMergeAuthoring(edit)
		return next, err
	}
	edit, err := s.native.WriteCharacter(s.cursor, set, number, s.over)
	if err != nil {
		return s, err
	}
	next, err := s.adoptEverydayEdit(edit)
	if err == nil {
		next.notice, next.homes = "", 0
	}
	return next, err
}
