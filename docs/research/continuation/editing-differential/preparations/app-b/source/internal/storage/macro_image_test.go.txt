package storage_test

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/macro/wpm"
	"github.com/lynncoleart/wordling/internal/storage"
)

func TestMacroImageViewCannotReplaceSnapshot(t *testing.T) {
	fixtures := macroFixtures(t)
	raw := macroBytes(t, fixtures[0])
	var different []byte
	for _, fixture := range fixtures[1:] {
		candidate := macroBytes(t, fixture)
		if !bytes.Equal(raw, candidate) {
			different = candidate
			break
		}
	}
	if different == nil {
		t.Fatal("need two distinct approved original images")
	}
	replacement, err := wpm.Parse(different, wpm.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	for _, tc := range []struct {
		name  string
		value wpm.Image
	}{{"zero-assignment", wpm.Image{}}, {"cross-image-assignment", *replacement}} {
		t.Run(tc.name, func(t *testing.T) {
			root := t.TempDir()
			if err := os.WriteFile(filepath.Join(root, "macro"), raw, 0600); err != nil {
				t.Fatal(err)
			}
			d := directory(t, root)
			m, err := d.ReadMacro("macro")
			if err != nil {
				t.Fatal(err)
			}
			identity, directoryID, name := m.Identity(), m.DirectoryID(), m.Name()
			first, second := m.Image(), m.Image()
			*first = tc.value
			// Whole-value replacement changes the caller's view, not the acquired
			// snapshot or another previously returned wrapper over that snapshot.
			if !bytes.Equal(first.Export(), tc.value.Export()) {
				t.Fatal("assignment did not change the caller's wrapper")
			}
			if !bytes.Equal(m.Export(), raw) || m.Identity() != identity || m.DirectoryID() != directoryID || m.Name() != name {
				t.Fatal("caller image assignment changed the acquired source snapshot")
			}
			for _, view := range []*wpm.Image{second, m.Image(), m.Image()} {
				if !bytes.Equal(view.Export(), raw) || view.SHA256() != identity.SHA256 {
					t.Fatal("returned image wrappers share replaceable identity")
				}
			}
			*second = wpm.Image{}
			if !bytes.Equal(m.Image().Export(), raw) || m.Image().SHA256() != identity.SHA256 {
				t.Fatal("later accessor replacement changed the snapshot")
			}
			if first == second || second == m.Image() || first == m.Image() {
				t.Fatal("accessors did not return independent wrappers")
			}
		})
	}
}

func TestMacroImageZeroAndNilBehavior(t *testing.T) {
	var zero storage.Macro
	if zero.Image() != nil || zero.Export() != nil {
		t.Fatal("zero Macro acquired an image")
	}
	// A nil Macro receiver remains invalid, as for its other accessors.
	defer func() {
		if recover() == nil {
			t.Fatal("nil Macro receiver unexpectedly accepted")
		}
	}()
	var absent *storage.Macro
	absent.Image()
}
