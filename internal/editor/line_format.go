package editor

import (
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
)

func (s Session) LineMargins() (left, right int) {
	return s.margins(false)
}

func (s Session) InsertConditionalPage(lines int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Conditional End of Page requires ordinary document editing")
	}
	edit, err := s.native.InsertConditionalPage(s.cursor, lines)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) WidowProtection() bool {
	for i := s.cursor.Gap() - 1; s.native != nil && i >= 0; i-- {
		t, _ := s.native.Token(i)
		switch t.Kind {
		case document.WidowProtectionOn:
			return true
		case document.WidowProtectionOff:
			return false
		}
	}
	return false
}

func (s Session) SetWidowProtection(enabled bool) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Widow/Orphan Protection requires ordinary document editing")
	}
	if enabled == s.WidowProtection() {
		return s, nil
	}
	edit, err := s.native.SetWidowProtection(s.cursor, enabled)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) SetBindingOffset(units int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Binding offset requires ordinary document editing")
	}
	edit, err := s.native.SetBindingOffset(s.cursor, units)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) LineSpacing() int {
	if s.native != nil {
		for i := s.cursor.Gap() - 1; i >= 0; i-- {
			owner, _ := s.native.Token(i)
			if spacing := owner.LineSpacing(); spacing != 0 {
				return spacing
			}
		}
		spacing, _ := s.native.InitialLineSpacing()
		return max(1, spacing)
	}
	return 1
}

func (s Session) SetInitialLineSpacing(spacing int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Initial Codes requires ordinary document editing")
	}
	edit, err := s.native.SetInitialLineSpacing(s.cursor, spacing)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) LineNumbering() bool {
	for i := s.cursor.Gap() - 1; s.native != nil && i >= 0; i-- {
		t, _ := s.native.Token(i)
		if t.Kind == document.LineNumbering {
			return t.EnablesLineNumbering()
		}
	}
	return false
}

func (s Session) SetLineNumbering(enabled bool) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Line numbering requires ordinary document editing")
	}
	if enabled == s.LineNumbering() {
		return s, nil
	}
	edit, err := s.native.SetLineNumbering(s.cursor, enabled)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) Justification() document.Justification {
	if s.native != nil {
		for i := s.cursor.Gap() - 1; i >= 0; i-- {
			token, _ := s.native.Token(i)
			if value, ok := token.Justification(); ok {
				return value
			}
		}
	}
	return document.JustifyFull
}

func (s Session) SetJustification(value document.Justification) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Justification requires ordinary document editing")
	}
	prior := s.Justification()
	if prior == value {
		return s, nil
	}
	edit, err := s.native.InsertJustification(s.cursor, prior, value)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) SetLineSpacing(spacing int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Line spacing requires ordinary document editing")
	}
	prior := s.LineSpacing()
	if prior == spacing {
		return s, nil
	}
	edit, err := s.native.InsertLineSpacing(s.cursor, prior, spacing)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) LineHeight() int {
	if s.native != nil {
		for i := s.cursor.Gap() - 1; i >= 0; i-- {
			owner, _ := s.native.Token(i)
			if owner.Kind == document.LineHeight {
				return owner.LineHeight()
			}
		}
	}
	return 0
}

func (s Session) SetLineHeight(height int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Line height requires ordinary document editing")
	}
	prior := s.LineHeight()
	if prior == height {
		return s, nil
	}
	edit, err := s.native.InsertLineHeight(s.cursor, prior, height)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) PageMargins() (top, bottom int) {
	return s.margins(true)
}

func (s Session) margins(page bool) (left, right int) {
	left, right = document.UnitsPerInch, document.UnitsPerInch
	if s.native == nil {
		return left, right
	}
	for i := s.cursor.Gap() - 1; i >= 0; i-- {
		token, _ := s.native.Token(i)
		if page {
			if t, b, ok := token.PageMargins(); ok {
				return t, b
			}
			continue
		}
		if l, r, ok := token.LineMargins(); ok {
			return l, r
		}
	}
	return left, right
}

func (s Session) SetPageMargins(top, bottom int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Margins require ordinary document editing")
	}
	oldTop, oldBottom := s.PageMargins()
	if oldTop == top && oldBottom == bottom {
		return s, nil
	}
	projected, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return s, err
	}
	gap := s.cursor.Gap()
	row, _, ok := projected.PositionAt(gap)
	if !ok || projected.Lines[row].Row != 0 || !projected.AtLineStart(gap) {
		return s, refuse("Move to the beginning of a page to set its margins")
	}
	edit, err := s.native.InsertPageMargins(s.cursor, oldTop, oldBottom, top, bottom)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) SetLineMargins(left, right int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Margins require ordinary document editing")
	}
	oldLeft, oldRight := s.LineMargins()
	if oldLeft == left && oldRight == right {
		return s, nil
	}
	projected, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return s, err
	}
	gap := s.cursor.Gap()
	row, _, ok := projected.PositionAt(gap)
	if !ok {
		return s, refuse("Margin change requires a known line position")
	}
	startLine := gap != projected.Lines[row].StartGap
	edit, err := s.native.InsertLineMargins(s.cursor, oldLeft, oldRight, left, right, startLine)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) lineAlignment(command Command) (Session, *Intent, error) {
	if s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, nil, refuse("Alignment requires ordinary document editing")
	}
	var edit document.EditResult
	var err error
	if command == EndCentering {
		edit, err = s.native.EndLineAlignment(s.cursor, true)
	} else {
		kind := document.CenterLine
		if command == AlignRight {
			kind = document.FlushRight
		} else if command == AlignDecimal {
			kind = document.DecimalTab
		}
		edit, err = s.native.InsertAlignment(s.cursor, kind)
	}
	if err != nil {
		return s, nil, err
	}
	next, err := s.adoptEverydayEdit(edit)
	return next, nil, err
}
