package editor

import (
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
)

func (s Session) NextNoteNumber(end bool) int {
	number := 1
	for i := 0; s.native != nil && i < s.cursor.Gap(); i++ {
		token, _ := s.native.Token(i)
		if note, ok := token.Note(); ok && note.End == end {
			number++
		}
	}
	return number
}

func (s Session) CreateNote(text string, end bool) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Notes require ordinary document editing")
	}
	physical, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return s, err
	}
	line, _, ok := physical.PositionAt(s.cursor.Gap())
	if !ok {
		return s, refuse("Note insertion needs a known page")
	}
	page := physical.Lines[line].Page
	for line > 0 && physical.Lines[line-1].Page == page {
		line--
	}
	edit, err := s.native.InsertNote(s.cursor, text, end, physical.Lines[line].StartGap)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) FindNote(number int, end bool) (int, document.Note, bool) {
	for i := 0; s.native != nil && i < s.native.TokenCount(); i++ {
		token, _ := s.native.Token(i)
		if note, ok := token.Note(); ok && note.End == end && note.Number == number {
			return i, note, true
		}
	}
	return 0, document.Note{}, false
}

func (s Session) EditNote(index int, text string) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Notes require ordinary document editing")
	}
	edit, err := s.native.ReplaceNote(s.cursor, index, text)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) CreatePageText(record document.PageText) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Headers and footers require ordinary document editing")
	}
	projected, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return s, err
	}
	row, _, ok := projected.PositionAt(s.cursor.Gap())
	if !ok || projected.Lines[row].Row != 0 {
		return s, refuse("Move to the first line of a page to set its header or footer")
	}
	edit, err := s.native.InsertPageText(s.cursor, record)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) FootnoteKeep() int {
	for i := s.cursor.Gap() - 1; s.native != nil && i >= 0; i-- {
		item, _ := s.native.Token(i)
		if units, ok := item.FootnoteKeep(); ok {
			return units
		}
	}
	return document.DefaultNoteKeep
}

func (s Session) SetFootnoteKeep(units int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Footnote Options requires ordinary document editing")
	}
	edit, err := s.native.SetFootnoteKeep(s.cursor, s.FootnoteKeep(), units)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
