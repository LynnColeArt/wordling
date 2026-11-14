package editor

func (s Session) ColumnMathActive() bool {
	return s.mode == Editing && s.workspace != nil && s.native != nil && !s.mergeSource && s.native.ColumnMathAt(s.cursor)
}

func (s Session) SetColumnMath(enabled bool) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.mergeSource || s.selection {
		return s, refuse("Column Math requires ordinary document editing")
	}
	edit, err := s.native.SetColumnMath(s.cursor, enabled)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) insertColumnSubtotal() (Session, error) {
	edit, err := s.native.InsertColumnSubtotal(s.cursor)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) CalculateColumnSubtotal() (Session, error) {
	if !s.ColumnMathActive() || s.selection {
		return s, refuse("Calculate needs an active Math column")
	}
	edit, err := s.native.CalculateColumnSubtotal(s.cursor)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
