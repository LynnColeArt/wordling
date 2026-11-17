//go:build linux || darwin

package tui

import (
	"bytes"
	"golang.org/x/sys/unix"
	"os"
	"path/filepath"
	"testing"
)

func TestEverydaySettingsRefuseCorruptSpecialAndSymlinkFiles(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "settings")
	corrupt := []byte("wordling-settings=2\n")
	if err := os.WriteFile(path, corrupt, 0600); err != nil {
		t.Fatal(err)
	}
	if yes, err := readMenuPreference(dir); !yes || err == nil {
		t.Fatal("malformed config did not report error with Yes fallback")
	}
	if err := writeMenuPreference(dir, false); err == nil {
		t.Fatal("unknown version was overwritten")
	}
	if raw, err := os.ReadFile(path); err != nil || !bytes.Equal(raw, corrupt) {
		t.Fatalf("unknown version changed: %q %v", raw, err)
	}
	if err := os.Remove(path); err != nil {
		t.Fatal(err)
	}
	if err := unix.Mkfifo(path, 0600); err != nil {
		t.Fatal(err)
	}
	if _, err := readMenuPreference(dir); err == nil {
		t.Fatal("FIFO accepted as regular settings")
	}
	if err := os.Remove(path); err != nil {
		t.Fatal(err)
	}
	target := filepath.Join(t.TempDir(), "outside")
	if err := os.WriteFile(target, []byte(settingsHeader+"no\n"), 0600); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(target, path); err != nil {
		t.Fatal(err)
	}
	if _, err := readMenuPreference(dir); err == nil {
		t.Fatal("external symlink accepted as settings")
	}
	if err := writeMenuPreference(dir, true); err == nil {
		t.Fatal("external symlink accepted for publication")
	}
}
