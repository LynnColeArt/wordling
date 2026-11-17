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

func TestIndependentOriginalBlockBackspace(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	for _, c := range []editor.Command{editor.Reveal, editor.Right, editor.Block, editor.Right} {
		s = key(t, s, c)
	}
	before := s.Snapshot()
	original, _ := s.Document().Export()
	next, intent, err := s.Reduce(editor.Event{Command: editor.Backspace})
	after := next.Snapshot()
	native, _ := next.Document().Export()
	t.Logf("actual original Backspace: before mode=%s gap=%d selection=%v; after mode=%s gap=%d selection=%v prompt=%q; intent=%v err=%v nativeUnchanged=%v", before.Mode, before.Gap, before.Selection, after.Mode, after.Gap, after.Selection, after.Prompt, intent, err, bytes.Equal(native, original))
	control, _, controlErr := s.Reduce(editor.Event{Command: editor.Delete})
	t.Logf("untranslated Delete control: mode=%s prompt=%q err=%v", control.Snapshot().Mode, control.Snapshot().Prompt, controlErr)
	if err != nil || intent != nil || after.Mode != editor.DeleteQuestion || after.Prompt != "Delete Block? No (Yes)" {
		t.Fatal("approved original selected-block Backspace does not reach required question")
	}
}
