package editor

import (
	"math"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
)

func (s Session) InsertAdvance(mode document.AdvanceMode, value int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Advance requires ordinary document editing")
	}
	settings := EverydaySettings()
	projected, err := layout.FromDocument(s.native, settings)
	if err != nil {
		return s, err
	}
	gap := s.cursor.Gap()
	prior, known := projected.PrintedColumn(gap)
	switch mode {
	case document.AdvanceDown:
		prior, known = projected.PrintedPageDepth(gap)
	case document.AdvanceRight:
		if prior+float64(value)/document.UnitsPerInch > settings.PageWidthInches {
			return s, refuse("Advance Right exceeds the paper width")
		}
	case document.AdvancePosition:
		if float64(value)/document.UnitsPerInch > settings.PageWidthInches {
			return s, refuse("Advance Position exceeds the paper width")
		}
	}
	if !known {
		return s, refuse("Advance requires a known formatter position")
	}
	edit, err := s.native.InsertAdvance(s.cursor, mode, int(math.Round(prior*document.UnitsPerInch)), value)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}
