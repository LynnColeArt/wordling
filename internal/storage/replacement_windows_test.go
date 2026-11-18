package storage

import (
	"bytes"
	"errors"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"golang.org/x/sys/windows"
)

type replacementFaultFS struct {
	filesystem
	replace func(string, string, string) error
	rename  func(string, string, uint) error
	remove  func(string) error
}

func (f replacementFaultFS) Replace(a, b, c string) error { return f.replace(a, b, c) }
func (f replacementFaultFS) Rename(a, b string, flags uint) error {
	if f.rename != nil {
		return f.rename(a, b, flags)
	}
	return f.filesystem.Rename(a, b, flags)
}
func (f replacementFaultFS) Remove(name string) error {
	if f.remove != nil {
		return f.remove(name)
	}
	return f.filesystem.Remove(name)
}

func TestNativePlatformReplacementFailures(t *testing.T) {
	for _, fault := range []string{"before", "after", "backup", "partial", "partial-restore", "rollback", "cleanup", "displaced-writer"} {
		t.Run(fault, func(t *testing.T) {
			root := t.TempDir()
			d, err := OpenDirectory(root)
			if err != nil {
				t.Fatal(err)
			}
			defer d.Close()
			old := make([]byte, 66)
			copy(old, []byte{255, 'W', 'P', 'C', 66, 0, 0, 0, 1, 10, 0, 1})
			copy(old[16:], []byte{251, 255, 5, 0, 50, 0})
			old = append(old, []byte("original")...)
			next := append(bytes.Clone(old), '!')
			for name, data := range map[string][]byte{"TEST.WP": old, "TEST.BK!": []byte("prior backup")} {
				if err := os.WriteFile(filepath.Join(root, name), data, 0600); err != nil {
					t.Fatal(err)
				}
			}
			dst, err := d.Observe("TEST.WP")
			if err != nil {
				t.Fatal(err)
			}
			id := PublicationID{1, 1}
			req, err := d.PrepareNewSave(dst, next, AllowOverwrite, OriginalBackupOn, id)
			if err != nil {
				t.Fatal(err)
			}
			base := d.ops
			calls := 0
			hooks := replacementFaultFS{filesystem: base}
			hooks.replace = func(a, b, c string) error {
				calls++
				switch {
				case fault == "before":
					return windows.ERROR_ACCESS_DENIED
				case fault == "backup" && calls == 2:
					return windows.ERROR_ACCESS_DENIED
				case fault == "rollback" && calls >= 2:
					return windows.ERROR_ACCESS_DENIED
				case (fault == "partial" || fault == "partial-restore") && calls == 1:
					if err := base.Rename(b, c, renameNoReplace); err != nil {
						return err
					}
					return windows.Errno(1177)
				case fault == "displaced-writer" && calls == 1:
					if err := os.WriteFile(filepath.Join(root, b), []byte("external writer"), 0600); err != nil {
						return err
					}
				}
				if err := base.Replace(a, b, c); err != nil {
					return err
				}
				if fault == "after" && calls == 1 {
					return windows.ERROR_ACCESS_DENIED
				}
				return nil
			}
			if fault == "partial-restore" {
				hooks.rename = func(a, b string, flags uint) error { return windows.ERROR_ACCESS_DENIED }
			}
			if fault == "cleanup" {
				hooks.remove = func(name string) error {
					if strings.HasPrefix(name, candidatePrefix) && calls > 0 {
						return windows.ERROR_ACCESS_DENIED
					}
					return base.Remove(name)
				}
			}
			d.ops = hooks
			result, err := d.PublishNewSave(req, id)
			var failure *Failure
			if !errors.As(err, &failure) || result.Document != nil {
				t.Fatalf("failure was reported as success: %+v %v", result, err)
			}
			uncertain := fault == "partial-restore" || fault == "rollback" || fault == "displaced-writer" || fault == "cleanup"
			if failure.DestinationMayExist != uncertain {
				t.Fatalf("incorrect uncertainty: %v", err)
			}
			if !uncertain {
				for name, want := range map[string][]byte{"TEST.WP": old, "TEST.BK!": []byte("prior backup")} {
					got, e := os.ReadFile(filepath.Join(root, name))
					if e != nil || !bytes.Equal(got, want) {
						t.Fatalf("rollback changed %s: %q %v (%v)", name, got, e, err)
					}
				}
				entries, e := os.ReadDir(root)
				if e != nil || len(entries) != 2 {
					t.Fatal("rollback residues", entries, e)
				}
			} else {
				if failure.Candidate == "" {
					t.Fatal("missing retained-file names", err)
				}
				preserved := false
				for _, name := range strings.Split(failure.Candidate, ",") {
					data, e := os.ReadFile(filepath.Join(root, name))
					want := old
					if fault == "displaced-writer" {
						want = []byte("external writer")
					}
					if e == nil && bytes.Equal(data, want) {
						preserved = true
					}
				}
				if !preserved {
					t.Fatal("displaced bytes were not retained", err)
				}
			}
		})
	}
}

func TestNativePlatformReplacementDirectoryLease(t *testing.T) {
	parent := t.TempDir()
	root := filepath.Join(parent, "space ü 文")
	if err := os.Mkdir(root, 0700); err != nil {
		t.Fatal(err)
	}
	name, err := windows.UTF16PtrFromString(root)
	if err != nil {
		t.Fatal(err)
	}
	// os.OpenRoot also holds a deny-delete handle on Windows. Use a separate
	// share-delete directory handle to isolate the replacement lease itself.
	handle, err := windows.CreateFile(name, windows.GENERIC_READ,
		windows.FILE_SHARE_READ|windows.FILE_SHARE_WRITE|windows.FILE_SHARE_DELETE,
		nil, windows.OPEN_EXISTING, windows.FILE_FLAG_BACKUP_SEMANTICS, 0)
	if err != nil {
		t.Fatal(err)
	}
	dir := os.NewFile(uintptr(handle), root)
	defer dir.Close()
	_, release, err := replacementDirectory(dir)
	if err != nil {
		t.Fatal(err)
	}
	if err := os.Rename(root, root+"-moved"); err == nil {
		release()
		t.Fatal("leased directory could be renamed")
	}
	release()
	if err := os.Rename(root, root+"-moved"); err != nil {
		t.Fatal("directory lease not released", err)
	}
	// Resolve the new physical path from the original handle; never touch a new
	// directory installed at the old pathname.
	if err := os.Mkdir(root, 0700); err != nil {
		t.Fatal(err)
	}
	path, release, err := replacementDirectory(dir)
	if err != nil {
		t.Fatal(err)
	}
	defer release()
	if !strings.HasSuffix(path, "-moved") {
		t.Fatal("lease followed rebound original pathname", path)
	}
}
