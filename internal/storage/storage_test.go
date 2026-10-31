package storage_test

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/storage"
	"github.com/lynncoleart/wordling/internal/wp51"
)

type fixture struct {
	ID, Path, SHA256 string
	Size             int `json:"size_bytes"`
}

func fixtures(t *testing.T) []fixture {
	t.Helper()
	raw, err := os.ReadFile("../../kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json")
	if err != nil {
		t.Fatal(err)
	}
	var c struct{ Fixtures []fixture }
	if err = json.Unmarshal(raw, &c); err != nil {
		t.Fatal(err)
	}
	return c.Fixtures
}
func directory(t *testing.T, path string) *storage.Directory {
	t.Helper()
	d, err := storage.OpenDirectory(path)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { d.Close() })
	return d
}
func expect(t *testing.T, err error, kind storage.Kind) *storage.Failure {
	t.Helper()
	var e *storage.Failure
	if !errors.As(err, &e) || e.Kind != kind {
		t.Fatalf("want %s, got %v", kind, err)
	}
	return e
}
func TestOriginalNoEditStorage(t *testing.T) {
	for _, f := range fixtures(t) {
		t.Run(f.ID, func(t *testing.T) {
			input, err := os.ReadFile(filepath.Join("../..", f.Path))
			if err != nil {
				t.Fatal(err)
			}
			if len(input) != f.Size || fmtHash(input) != f.SHA256 {
				t.Fatal("WP01 source bytes changed")
			}
			path := t.TempDir()
			if err = os.WriteFile(filepath.Join(path, "source.wp5"), input, 0600); err != nil {
				t.Fatal(err)
			}
			d := directory(t, path)
			doc, err := d.Read("source.wp5")
			if f.ID == "macro" {
				expect(t, err, storage.NativeRefused)
				var native *wp51.Failure
				if !errors.As(err, &native) || native.Category != wp51.UnsupportedFileType {
					t.Fatal("native failure was lost")
				}
				return
			}
			if err != nil {
				t.Fatal(err)
			}
			beforeInfo, _ := os.Stat(filepath.Join(path, "source.wp5"))
			if !bytes.Equal(doc.Export(), input) || doc.Identity().SHA256 != sha256.Sum256(input) {
				t.Fatal("read changed source")
			}
			exported := doc.Export()
			exported[0] ^= 1
			if !bytes.Equal(doc.Export(), input) {
				t.Fatal("document exports alias storage")
			}
			target, err := d.Observe("copy.wp5")
			if err != nil {
				t.Fatal(err)
			}
			if target.Exists() || target.Name() != "copy.wp5" || target.DirectoryID() != d.ID() {
				t.Fatal("destination identity mismatch")
			}
			outcome, err := d.Save(doc, target, storage.NoOverwrite)
			if err != nil {
				t.Fatal(err)
			}
			if outcome.State != storage.Published || outcome.Identity.SHA256 != sha256.Sum256(input) {
				t.Fatal("publication not reported exactly")
			}
			saved, err := os.ReadFile(filepath.Join(path, "copy.wp5"))
			if err != nil || !bytes.Equal(saved, input) || fmtHash(saved) != f.SHA256 {
				t.Fatal("published bytes changed")
			}
			afterInfo, _ := os.Stat(filepath.Join(path, "source.wp5"))
			if !os.SameFile(beforeInfo, afterInfo) {
				t.Fatal("source inode replaced")
			}
			source, _ := os.ReadFile(filepath.Join(path, "source.wp5"))
			if !bytes.Equal(source, input) {
				t.Fatal("source changed")
			}
			freshCopy, err := d.Read("copy.wp5")
			if err != nil || freshCopy.Identity() != outcome.Identity {
				t.Fatalf("receipt identity stale after own cleanup: %v", err)
			}
			copiedInfo, _ := os.Stat(filepath.Join(path, "copy.wp5"))
			if copiedInfo.Mode().Perm()&0077 != 0 {
				t.Fatal("candidate exposed to other users")
			}
			same, err := d.Observe("source.wp5")
			if err != nil {
				t.Fatal(err)
			}
			observed, exists := same.Identity()
			if !exists || observed.ID != doc.Identity().ID {
				t.Fatal("existing destination identity unavailable")
			}
			_, err = d.Save(doc, same, storage.NoOverwrite)
			expect(t, err, storage.OverwriteRequired)
			outcome, err = d.Save(doc, same, storage.AllowOverwrite)
			if err != nil || outcome.State != storage.Unchanged {
				t.Fatalf("no-op: %v", err)
			}
			afterInfo, _ = os.Stat(filepath.Join(path, "source.wp5"))
			if !os.SameFile(beforeInfo, afterInfo) {
				t.Fatal("no-op replaced source")
			}
			copyTarget, err := d.Observe("copy.wp5")
			if err != nil {
				t.Fatal(err)
			}
			_, err = d.Save(doc, copyTarget, storage.AllowOverwrite)
			expect(t, err, storage.UnsupportedReplacement)
			entries, err := os.ReadDir(path)
			if err != nil || len(entries) != 2 {
				t.Fatalf("candidate leaked: %v, %v", entries, err)
			}
		})
	}
}
func fmtHash(b []byte) string { s := sha256.Sum256(b); return hex.EncodeToString(s[:]) }

func plain(t *testing.T) []byte {
	t.Helper()
	for _, f := range fixtures(t) {
		if f.ID == "plain" {
			b, e := os.ReadFile(filepath.Join("../..", f.Path))
			if e != nil {
				t.Fatal(e)
			}
			return b
		}
	}
	t.Fatal("missing plain")
	return nil
}
func setup(t *testing.T) (*storage.Directory, *storage.Document, string, []byte) {
	t.Helper()
	path := t.TempDir()
	b := plain(t)
	if err := os.WriteFile(filepath.Join(path, "source"), b, 0600); err != nil {
		t.Fatal(err)
	}
	d := directory(t, path)
	doc, err := d.Read("source")
	if err != nil {
		t.Fatal(err)
	}
	return d, doc, path, b
}
func TestExplicitRefusalsAndStaleObservations(t *testing.T) {
	d, doc, path, input := setup(t)
	for _, name := range []string{"", ".", "..", "../outside", "child/file", "/tmp/a", "a\x00b", ".wordling-candidate-forbidden", strings.Repeat("x", storage.MaxNameBytes+1)} {
		_, err := d.Read(name)
		expect(t, err, storage.UnsafePath)
		_, err = d.Observe(name)
		expect(t, err, storage.UnsafePath)
	}
	target, _ := d.Observe("new")
	_, err := d.Save(nil, target, storage.NoOverwrite)
	expect(t, err, storage.InvalidRequest)
	_, err = d.Save(&storage.Document{}, target, storage.NoOverwrite)
	expect(t, err, storage.InvalidRequest)
	_, err = d.Save(doc, nil, storage.NoOverwrite)
	expect(t, err, storage.InvalidRequest)
	_, err = d.Save(doc, target, storage.Decision(99))
	expect(t, err, storage.InvalidRequest)
	other := directory(t, t.TempDir())
	_, err = other.Save(doc, target, storage.NoOverwrite)
	expect(t, err, storage.InvalidRequest)
	if err = os.WriteFile(filepath.Join(path, "new"), []byte("foreign"), 0600); err != nil {
		t.Fatal(err)
	}
	_, err = d.Save(doc, target, storage.AllowOverwrite)
	expect(t, err, storage.DestinationChanged)
	if err = os.WriteFile(filepath.Join(path, "different"), []byte("original destination"), 0600); err != nil {
		t.Fatal(err)
	}
	existing, _ := d.Observe("different")
	_, err = d.Save(doc, existing, storage.NoOverwrite)
	expect(t, err, storage.OverwriteRequired)
	_, err = d.Save(doc, existing, storage.AllowOverwrite)
	expect(t, err, storage.UnsupportedReplacement)
	if err = os.WriteFile(filepath.Join(path, "source"), append(bytes.Clone(input), 'x'), 0600); err != nil {
		t.Fatal(err)
	}
	fresh, _ := d.Observe("fresh")
	_, err = d.Save(doc, fresh, storage.NoOverwrite)
	expect(t, err, storage.StaleSource)
	if data, _ := os.ReadFile(filepath.Join(path, "different")); string(data) != "original destination" {
		t.Fatal("refusal overwrote existing data")
	}
	if data, _ := os.ReadFile(filepath.Join(path, "new")); string(data) != "foreign" {
		t.Fatal("stale observation overwrote foreign data")
	}
	if _, err = os.Stat(filepath.Join(path, "fresh")); !os.IsNotExist(err) {
		t.Fatal("stale source published")
	}
}
func TestBoundedReadAndUnsafeNodes(t *testing.T) {
	d, _, path, input := setup(t)
	if err := os.WriteFile(filepath.Join(path, "bad"), []byte("bad"), 0600); err != nil {
		t.Fatal(err)
	}
	_, err := d.Read("bad")
	expect(t, err, storage.NativeRefused)
	if err = os.Symlink("source", filepath.Join(path, "link")); err != nil {
		t.Fatal(err)
	}
	_, err = d.Read("link")
	expect(t, err, storage.UnsafePath)
	_, err = d.Observe("link")
	expect(t, err, storage.UnsafePath)
	if err = os.Mkdir(filepath.Join(path, "subdir"), 0700); err != nil {
		t.Fatal(err)
	}
	_, err = d.Read("subdir")
	expect(t, err, storage.UnsafePath)
	_, err = d.Observe("subdir")
	expect(t, err, storage.UnsafePath)
	huge, err := os.Create(filepath.Join(path, "huge"))
	if err != nil {
		t.Fatal(err)
	}
	if err = huge.Truncate(wp51.MaxInputBytes + 1); err != nil {
		t.Fatal(err)
	}
	huge.Close()
	_, err = d.Read("huge")
	expect(t, err, storage.InputLimit)
	// Exact-size native file acquisition succeeds and remains an exact no-edit image.
	max := append(bytes.Clone(input), bytes.Repeat([]byte{'x'}, wp51.MaxInputBytes-len(input))...)
	if err = os.WriteFile(filepath.Join(path, "max"), max, 0600); err != nil {
		t.Fatal(err)
	}
	doc, err := d.Read("max")
	if err != nil || !bytes.Equal(doc.Export(), max) {
		t.Fatalf("maximum read failed: %v", err)
	}
	target, err := d.Observe("max-copy")
	if err != nil {
		t.Fatal(err)
	}
	if _, err = d.Save(doc, target, storage.NoOverwrite); err != nil {
		t.Fatal(err)
	}
	copied, err := os.ReadFile(filepath.Join(path, "max-copy"))
	if err != nil || !bytes.Equal(copied, max) {
		t.Fatal("max-size publication changed bytes")
	}
	d.Close()
	_, err = d.Read("source")
	expect(t, err, storage.ReadFailed)
}
