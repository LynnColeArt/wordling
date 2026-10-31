package editor_test

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
	"testing"
)

func TestOwnedRetrievedWrappers(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	original := s.Source().Identity()
	rev := s.Document().Revision()
	*s.Source() = storage.Document{}
	*s.Document() = document.Document{}
	if s.Source().Identity() != original || s.Document().Revision() != rev {
		t.Fatal("getter retargeted accepted source/revision")
	}
}
func TestEditingRoutesRealDocument(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	before := s.Document().Revision()
	next, _, err := s.Reduce(editor.Event{Command: editor.Text, Text: "X"})
	if err != nil {
		t.Fatal(err)
	}
	raw, _ := next.Document().Export()
	if !bytes.Equal(raw[len(raw)-11:], append([]byte("X"), f.raw[324:]...)) {
		t.Fatal("native insertion")
	}
	if next.Document().Revision() == before || s.Document().Revision() != before {
		t.Fatal("revision isolation")
	}
}
