package editor

import (
	"math"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
)

func (s Session) TabSetAt(gap int) *document.TabSet {
	for i := gap - 1; s.native != nil && i >= 0; i-- {
		t, _ := s.native.Token(i)
		if ruler, ok := t.Tabs(); ok {
			return &ruler
		}
	}
	return nil
}

func (s Session) TabSetPosition() (document.TabSet, int, error) {
	if s.native == nil || s.workspace == nil || s.mergeSource || s.selection {
		return document.TabSet{}, 0, refuse("Tab Set requires ordinary document editing")
	}
	ruler := s.TabSetAt(s.cursor.Gap())
	if ruler == nil {
		value := document.DefaultTabSet()
		ruler = &value
	}
	physical, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return document.TabSet{}, 0, err
	}
	position, ok := physical.PrintedColumn(s.cursor.Gap())
	if !ok {
		return document.TabSet{}, 0, refuse("Tab Set requires a known cursor position")
	}
	return *ruler, int(math.Round(position * document.UnitsPerInch)), nil
}

func (s Session) SetTabSet(next document.TabSet) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Tab Set requires ordinary document editing")
	}
	prior := s.TabSetAt(s.cursor.Gap())
	if prior == nil {
		value := document.DefaultTabSet()
		prior = &value
	}
	edit, err := s.native.InsertTabSet(s.cursor, *prior, next)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
