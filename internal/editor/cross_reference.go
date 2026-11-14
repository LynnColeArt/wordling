package editor

import (
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
)

func (s Session) MarkPageReference(name string, target bool, originRevision document.Revision, origin int) (Session, error) {
	if s.mode != Editing || s.native == nil || s.workspace == nil || s.selection || s.mergeSource {
		return s, refuse("Cross-references require ordinary editing")
	}
	var edit document.EditResult
	var err error
	if origin >= 0 {
		if s.native.Revision() != originRevision {
			return s, refuse("The document changed while choosing a target")
		}
		physical, posErr := layout.FromDocument(s.native, EverydaySettings())
		if posErr != nil {
			return s, posErr
		}
		line, _, ok := physical.PositionAt(s.cursor.Gap())
		if !ok {
			return s, refuse("The target needs a known page")
		}
		edit, err = s.native.MarkPageReferenceAndTarget(s.cursor, origin, name, physical.PageLabels()[physical.Lines[line].Page-1])
	} else {
		edit, err = s.native.MarkPageReference(s.cursor, name, target)
	}
	if err != nil {
		return s, err
	}
	return s.adoptEverydayEdit(edit)
}

func (s Session) generatedPageTargets(physical layout.Layout, labels []string) (map[string]string, bool, error) {
	pages := map[string]string{}
	hasReferences := false
	duplicate := ""
	for i := 0; i < s.native.TokenCount(); i++ {
		t, _ := s.native.Token(i)
		if t.Kind == document.PageReference {
			hasReferences = true
		} else if t.Kind == document.ReferenceTarget {
			ref, _ := t.CrossReference()
			line, _, ok := physical.PositionAt(i)
			if !ok {
				return nil, false, refuse("A cross-reference target needs a known page")
			}
			name := strings.ToUpper(ref.Name)
			if _, exists := pages[name]; exists {
				duplicate = name
			}
			pages[name] = labels[physical.Lines[line].Page-1]
		}
	}
	if hasReferences && duplicate != "" {
		return nil, false, refuse("Duplicate cross-reference target " + duplicate)
	}
	return pages, hasReferences, nil
}
