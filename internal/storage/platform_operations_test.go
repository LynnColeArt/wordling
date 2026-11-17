package storage

import (
	"errors"
	"os"
	"path/filepath"
	"testing"
)

func TestNativePlatformRenameNoReplace(t *testing.T) {
	fromPath, toPath := t.TempDir(), t.TempDir()
	from, err := OpenDirectory(fromPath)
	if err != nil {
		t.Fatal(err)
	}
	defer from.Close()
	to, err := OpenDirectory(toPath)
	if err != nil {
		t.Fatal(err)
	}
	defer to.Close()
	if err := os.WriteFile(filepath.Join(fromPath, "SOURCE.TXT"), []byte("source"), 0600); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(toPath, "TAKEN.TXT"), []byte("prior"), 0600); err != nil {
		t.Fatal(err)
	}
	if err := platformRename(from.dir, "SOURCE.TXT", to.dir, "TAKEN.TXT", renameNoReplace); !errors.Is(err, os.ErrExist) {
		t.Fatal("occupied target was not refused", err)
	}
	if raw, err := os.ReadFile(filepath.Join(toPath, "TAKEN.TXT")); err != nil || string(raw) != "prior" {
		t.Fatal("collision changed prior bytes", err)
	}
	if err := platformRename(from.dir, "SOURCE.TXT", to.dir, "MOVED.TXT", renameNoReplace); err != nil {
		t.Fatal(err)
	}
	if _, err := os.Stat(filepath.Join(fromPath, "SOURCE.TXT")); !errors.Is(err, os.ErrNotExist) {
		t.Fatal("source remains after move", err)
	}
	if raw, err := os.ReadFile(filepath.Join(toPath, "MOVED.TXT")); err != nil || string(raw) != "source" {
		t.Fatal("moved bytes differ", err)
	}
}
