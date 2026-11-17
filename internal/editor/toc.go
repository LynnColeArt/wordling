package editor

import (
	"maps"
	"slices"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
)

func (s Session) MarkContents(level int) (Session, error) {
	if s.mode != Editing || s.workspace == nil || s.native == nil || !s.selection || s.mergeSource {
		return s, refuse("Select the heading before marking it for the table of contents")
	}
	edit, err := s.native.MarkContents(s.anchor, s.cursor, level)
	if err != nil {
		return s, err
	}
	next, err := s.adoptEverydayEdit(edit)
	if err != nil {
		return s, err
	}
	next.selection, next.blockMoved, next.anchor = false, false, document.Cursor{}
	return next, nil
}

func (s Session) DefineContents(levels int) (Session, error) {
	if s.mode != Editing || s.native == nil || s.workspace == nil || s.selection || s.mergeSource {
		return s, refuse("Contents definition requires ordinary editing")
	}
	edit, err := s.native.DefineContents(s.cursor, levels)
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) GenerateContents() (Session, error) {
	if s.mode != Editing || s.native == nil || s.workspace == nil || s.selection || s.mergeSource {
		return s, refuse("Contents generation requires ordinary editing")
	}
	var contents []document.ContentsEntry
	var previousTargets map[string]string
	current := s
	// Each pass starts from the original session. Neither the contents nor
	// the reference values are published unless pagination stabilizes.
	for pass := range 5 {
		physical, err := layout.FromDocument(current.native, EverydaySettings())
		if err != nil {
			return s, err
		}
		labels := physical.PageLabels()
		targets, hasReferences, err := current.generatedPageTargets(physical, labels)
		if err != nil {
			return s, err
		}
		var entries []document.ContentsEntry
		if levels := current.native.ContentsLevels(); levels > 0 {
			headings, err := current.native.ContentsHeadings(levels)
			if err != nil {
				return s, err
			}
			for _, h := range headings {
				line, _, ok := physical.PositionAt(h.Gap)
				if !ok {
					return s, refuse("Contents requires a known page for every heading")
				}
				entries = append(entries, document.ContentsEntry{Text: h.Text, Page: labels[physical.Lines[line].Page-1], Level: h.Level})
			}
		} else if !hasReferences {
			return s, refuse("Define a table of contents or mark a cross-reference before generating")
		}
		if pass > 0 && slices.Equal(entries, contents) && maps.Equal(previousTargets, targets) {
			return current, nil
		}
		next := s
		if s.native.ContentsLevels() > 0 {
			edit, err := next.native.GenerateContents(next.cursor, entries)
			if err != nil {
				return s, err
			}
			next, err = next.adoptEverydayEdit(edit)
			if err != nil {
				return s, err
			}
		}
		if hasReferences {
			edit, err := next.native.ResolvePageReferences(next.cursor, targets)
			if err != nil {
				return s, err
			}
			next, err = next.adoptEverydayEdit(edit)
			if err != nil {
				return s, err
			}
		}
		current, contents, previousTargets = next, entries, targets
	}
	return s, refuse("Generated page numbering did not stabilize")
}
