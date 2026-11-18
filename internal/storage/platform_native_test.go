package storage_test

import (
	"bytes"
	"errors"
	"os"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/lynncoleart/wordling/internal/storage"
)

// Authored framing-only fixture: no private original assets or source-tree paths.
func nativePlatformDocument() []byte {
	raw := make([]byte, 66)
	copy(raw, []byte{255, 'W', 'P', 'C', 66, 0, 0, 0, 1, 10, 0, 1})
	copy(raw[16:], []byte{251, 255, 5, 0, 50, 0})
	return append(raw, []byte("Native platform test")...)
}

func TestNativePlatformSaveAndReplacement(t *testing.T) {
	root := t.TempDir()
	d, err := storage.OpenDirectory(root)
	if err != nil {
		t.Fatal(err)
	}
	defer d.Close()
	raw := nativePlatformDocument()
	target, err := d.Observe("NATIVE.WP")
	if err != nil {
		t.Fatal(err)
	}
	id := storage.PublicationID{Operation: 1, Revision: 1}
	request, err := d.PrepareNewSave(target, raw, storage.NoOverwrite, storage.OriginalBackupOff, id)
	if err != nil {
		t.Fatal(err)
	}
	result, err := d.PublishNewSave(request, id)
	if err != nil {
		t.Fatal(err)
	}
	if result.Document == nil || !bytes.Equal(result.Document.Export(), raw) {
		t.Fatal("new native snapshot differs")
	}
	target, err = d.Observe("NATIVE.WP")
	if err != nil {
		t.Fatal(err)
	}
	changed := append(bytes.Clone(raw), '!')
	id = storage.PublicationID{Operation: 2, Revision: 2}
	next, err := d.PrepareSave(result.Document, target, changed, storage.AllowOverwrite, storage.OriginalBackupOn, id)
	if err != nil {
		t.Fatal(err)
	}
	result, err = d.PublishSave(next, id)
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(result.Document.Export(), changed) {
		t.Fatal("replacement differs")
	}
	if disk, e := os.ReadFile(filepath.Join(root, "NATIVE.BK!")); e != nil || !bytes.Equal(disk, raw) {
		t.Fatal("backup differs", e)
	}
	// Repeat with an existing backup, then remove it, then preserve it. Each
	// successful receipt must be usable immediately as the next source.
	for i, setting := range []storage.OriginalBackup{storage.OriginalBackupOn, storage.OriginalBackupOff, storage.OriginalBackupOn, storage.OriginalBackupPreserve} {
		previous := result.Document.Export()
		if setting == storage.OriginalBackupPreserve {
			raw, err = os.ReadFile(filepath.Join(root, "NATIVE.BK!"))
			if err != nil {
				t.Fatal(err)
			}
		} else {
			raw = previous
		}
		target, err = d.Observe("NATIVE.WP")
		if err != nil {
			t.Fatal(err)
		}
		changed = append(bytes.Clone(previous), byte('A'+i))
		id = storage.PublicationID{Operation: uint64(3 + i), Revision: uint64(3 + i)}
		next, err = d.PrepareSave(result.Document, target, changed, storage.AllowOverwrite, setting, id)
		if err != nil {
			t.Fatal(err)
		}
		result, err = d.PublishSave(next, id)
		if err != nil {
			t.Fatal(err)
		}
		disk, e := os.ReadFile(filepath.Join(root, "NATIVE.BK!"))
		if setting == storage.OriginalBackupOff {
			if !errors.Is(e, os.ErrNotExist) {
				t.Fatal("backup not removed", e)
			}
		} else if e != nil || !bytes.Equal(disk, raw) {
			t.Fatal("repeated backup differs", e)
		}
	}
	entries, err := os.ReadDir(root)
	if err != nil || len(entries) != 2 {
		t.Fatal("save left private files", entries, err)
	}
	copyTarget, err := d.Observe("COPY.WP")
	if err != nil {
		t.Fatal(err)
	}
	if _, err = d.Save(result.Document, copyTarget, storage.NoOverwrite); err != nil {
		t.Fatal("new-name copy", err)
	}
	w, err := storage.OpenWorkspace(root)
	if err != nil {
		t.Fatal(err)
	}
	defer w.Close()
	wd, err := w.Root()
	if err != nil {
		t.Fatal(err)
	}
	listing, err := wd.List("*.*")
	if err != nil {
		t.Fatal(err)
	}
	if len(listing.Entries()) < 2 {
		t.Fatal("native listing omitted documents")
	}
}

func TestNativePlatformWindowsPathRefusals(t *testing.T) {
	if runtime.GOOS != "windows" {
		t.Skip("Windows namespace")
	}
	d, err := storage.OpenDirectory(t.TempDir())
	if err != nil {
		t.Fatal(err)
	}
	defer d.Close()
	for _, name := range []string{`A.WP:stream`, `..\outside`, `CON`, `A.WP.`, `A.WP `} {
		if _, err := d.Observe(name); err == nil {
			t.Fatalf("unsafe Windows name admitted: %q", name)
		}
	}
}
