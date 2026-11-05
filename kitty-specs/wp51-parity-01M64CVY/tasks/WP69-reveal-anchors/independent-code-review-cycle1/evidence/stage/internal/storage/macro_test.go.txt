package storage_test

import (
	"bytes"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"syscall"
	"testing"

	"github.com/lynncoleart/wordling/internal/macro/wpm"
	"github.com/lynncoleart/wordling/internal/storage"
	"github.com/lynncoleart/wordling/internal/wp51"
)

type macroFixture struct {
	Path, SHA256, GitBlob string
	Size                  int
}

func macroFixtures(t testing.TB) []macroFixture {
	t.Helper()
	b, err := os.ReadFile("../macro/wpm/testdata/original-fixtures.json")
	if err != nil {
		t.Fatal(err)
	}
	var ledger struct {
		Source  string `json:"source_ledger_sha256"`
		Exports []struct {
			Path    string `json:"path"`
			SHA256  string `json:"sha256"`
			GitBlob string `json:"git_blob"`
			Size    int    `json:"size"`
		} `json:"wpm_exports"`
	}
	if err := json.Unmarshal(b, &ledger); err != nil {
		t.Fatal(err)
	}
	if len(ledger.Exports) != 46 || ledger.Source != "fca8446e98ad95ab118fc672e48e821afc65e9e3b2b5a43c27f7759824c2ce5d" {
		t.Fatal("wrong approved corpus source")
	}
	var out []macroFixture
	for _, f := range ledger.Exports {
		out = append(out, macroFixture{f.Path, f.SHA256, f.GitBlob, f.Size})
	}
	return out
}
func macroBytes(t testing.TB, f macroFixture) []byte {
	t.Helper()
	b, err := os.ReadFile(filepath.Join("../..", f.Path))
	if err != nil {
		t.Fatal(err)
	}
	if len(b) != f.Size || fmtHash(b) != f.SHA256 {
		t.Fatal("original WPM evidence changed", f.Path)
	}
	blob := sha1.Sum(append([]byte(fmt.Sprintf("blob %d\x00", len(b))), b...))
	if hex.EncodeToString(blob[:]) != f.GitBlob {
		t.Fatal("original Git blob changed")
	}
	return b
}

func TestOriginalMacroStorageReadOnlySnapshots(t *testing.T) {
	unique := map[string]bool{}
	for _, f := range macroFixtures(t) {
		t.Run(f.Path, func(t *testing.T) {
			input := macroBytes(t, f)
			path := t.TempDir()
			name := "source.WPM"
			if err := os.WriteFile(filepath.Join(path, name), input, 0600); err != nil {
				t.Fatal(err)
			}
			before, err := os.Stat(filepath.Join(path, name))
			if err != nil {
				t.Fatal(err)
			}
			d := directory(t, path)
			m, err := d.ReadMacro(name)
			if err != nil {
				t.Fatal(err)
			}
			unique[f.SHA256] = true
			id := m.Identity()
			stat := before.Sys().(*syscall.Stat_t)
			if m.Name() != name || m.DirectoryID() != d.ID() || id.ID != (storage.FileID{Device: uint64(stat.Dev), Inode: uint64(stat.Ino)}) || id.Size != int64(len(input)) || id.Mode != before.Mode() || !id.Modified.Equal(before.ModTime()) || id.SHA256 != sha256.Sum256(input) || m.Image().SHA256() != id.SHA256 {
				t.Fatalf("source observation mismatch: %+v", id)
			}
			if !bytes.Equal(m.Export(), input) || !bytes.Equal(m.Image().Export(), input) {
				t.Fatal("snapshot changed bytes")
			}
			export := m.Export()
			export[0] ^= 1
			imageExport := m.Image().Export()
			imageExport[0] ^= 1
			words := m.Image().BodyWords()
			words[0].Value = 0
			copyID := m.Identity()
			copyID.SHA256[0] ^= 1
			if !bytes.Equal(m.Export(), input) || m.Image().BodyWords()[0].Value != 0xfc0c || m.Identity() != id {
				t.Fatal("mutable API alias")
			}
			_, err = d.Read(name)
			expect(t, err, storage.NativeRefused)
			var docFailure *wp51.Failure
			if !errors.As(err, &docFailure) || docFailure.Category != wp51.UnsupportedFileType {
				t.Fatal("DOC parser weakened", err)
			}
			after, err := os.Stat(filepath.Join(path, name))
			if err != nil || !os.SameFile(before, after) || !after.ModTime().Equal(before.ModTime()) {
				t.Fatal("read changed source identity", err)
			}
			actual, err := os.ReadFile(filepath.Join(path, name))
			if err != nil || !bytes.Equal(input, actual) {
				t.Fatal("read wrote source", err)
			}
			entries, err := os.ReadDir(path)
			if err != nil || len(entries) != 1 {
				t.Fatal("read created a companion/candidate", entries, err)
			}
		})
	}
	if len(unique) != 22 {
		t.Fatal("unique corpus count", len(unique))
	}
}

func TestMacroStorageRefusalAndOpaqueSupport(t *testing.T) {
	path := t.TempDir()
	d := directory(t, path)
	raw := macroBytes(t, macroFixtures(t)[0])
	doc := plain(t)
	for _, tc := range []struct {
		name, code string
		data       []byte
	}{
		{"document", "UnsupportedFileType", doc},
		{"truncated", "TruncatedInput", raw[:8]},
		{"missing-terminal", "MalformedBody", raw[:len(raw)-2]},
	} {
		t.Run(tc.name, func(t *testing.T) {
			if err := os.WriteFile(filepath.Join(path, "input"), tc.data, 0600); err != nil {
				t.Fatal(err)
			}
			m, err := d.ReadMacro("input")
			if m != nil {
				t.Fatal("refusal exposed macro")
			}
			storageError := expect(t, err, storage.NativeRefused)
			var codec *wpm.Failure
			if storageError.Stage != "macro framing" || !errors.As(err, &codec) || codec.Code != tc.code {
				t.Fatal("codec cause lost", err)
			}
			got, err := os.ReadFile(filepath.Join(path, "input"))
			if err != nil || !bytes.Equal(got, tc.data) {
				t.Fatal("refusal changed file")
			}
		})
	}
	// An opaque, structurally admitted source stays lossless and execution-blocked.
	opaque := bytes.Clone(raw)
	binary.LittleEndian.PutUint16(opaque[70:72], 0xfcfd)
	if err := os.WriteFile(filepath.Join(path, "opaque"), opaque, 0600); err != nil {
		t.Fatal(err)
	}
	m, err := d.ReadMacro("opaque")
	if err != nil || !bytes.Equal(m.Export(), opaque) || len(m.Image().Inspect().Findings) != 1 || !m.Image().Inspect().Findings[0].ExecutionBlocked {
		t.Fatal("opaque content lost/refused", err)
	}
	if m.Image().Inspect().ReleaseEvidence != "unknown-from-bytes" {
		t.Fatal("storage fabricated release provenance")
	}
	// Existing publication remains document-only even with a valid DOC source guard.
	if err := os.WriteFile(filepath.Join(path, "doc"), doc, 0600); err != nil {
		t.Fatal(err)
	}
	source, err := d.Read("doc")
	if err != nil {
		t.Fatal(err)
	}
	target, err := d.Observe("new")
	if err != nil {
		t.Fatal(err)
	}
	publication, err := d.PreparePublication(source, target, raw, storage.PublicationID{Operation: 1, Revision: 1})
	expect(t, err, storage.NativeRefused)
	var documentFailure *wp51.Failure
	if publication != nil || !errors.As(err, &documentFailure) || documentFailure.Category != wp51.UnsupportedFileType {
		t.Fatal("WPM gained publication permission")
	}
	if _, err := os.Stat(filepath.Join(path, "new")); !errors.Is(err, os.ErrNotExist) {
		t.Fatal("publication created output", err)
	}
}

func TestMacroStorageUnsafeNodesAndPinnedDirectory(t *testing.T) {
	parent := t.TempDir()
	path := filepath.Join(parent, "selected")
	foreign := filepath.Join(parent, "foreign")
	moved := filepath.Join(parent, "moved")
	for _, p := range []string{path, foreign} {
		if err := os.Mkdir(p, 0700); err != nil {
			t.Fatal(err)
		}
	}
	raw := macroBytes(t, macroFixtures(t)[0])
	other := bytes.Clone(raw)
	other[72] = 'Z'
	if err := os.WriteFile(filepath.Join(path, "macro"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(foreign, "macro"), other, 0600); err != nil {
		t.Fatal(err)
	}
	d := directory(t, path)
	if err := os.Rename(path, moved); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(foreign, path); err != nil {
		t.Fatal(err)
	}
	m, err := d.ReadMacro("macro")
	if err != nil || !bytes.Equal(m.Export(), raw) {
		t.Fatal("root rename redirected read", err)
	}
	if err := os.Symlink(filepath.Join(foreign, "macro"), filepath.Join(moved, "link")); err != nil {
		t.Fatal(err)
	}
	if err := os.Mkdir(filepath.Join(moved, "directory"), 0700); err != nil {
		t.Fatal(err)
	}
	if err := syscall.Mkfifo(filepath.Join(moved, "fifo"), 0600); err != nil {
		t.Fatal(err)
	}
	for _, name := range []string{"link", "directory", "fifo", "", ".", "..", "../foreign/macro", "/etc/passwd", "bad\x00name", strings.Repeat("x", 256), ".wordling-candidate-any"} {
		macro, err := d.ReadMacro(name)
		if macro != nil {
			t.Fatal("unsafe input exposed macro", name)
		}
		expect(t, err, storage.UnsafePath)
	}
	file, err := os.Create(filepath.Join(moved, "large"))
	if err != nil {
		t.Fatal(err)
	}
	if err = file.Truncate(wpm.MaxInputBytes + 1); err != nil {
		t.Fatal(err)
	}
	file.Close()
	macro, err := d.ReadMacro("large")
	if macro != nil {
		t.Fatal("oversize exposed macro")
	}
	expect(t, err, storage.InputLimit)
	// Later external changes do not rewrite a previously acquired snapshot/identity.
	oldID := m.Identity()
	if err := os.WriteFile(filepath.Join(moved, "macro"), other, 0600); err != nil {
		t.Fatal(err)
	}
	if m.Identity() != oldID || !bytes.Equal(m.Export(), raw) {
		t.Fatal("snapshot claimed future freshness or changed")
	}
}

func TestMacroStorageConcurrentReads(t *testing.T) {
	path := t.TempDir()
	raw := macroBytes(t, macroFixtures(t)[0])
	if err := os.WriteFile(filepath.Join(path, "macro"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	d := directory(t, path)
	var wg sync.WaitGroup
	for n := 0; n < 8; n++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for k := 0; k < 20; k++ {
				m, err := d.ReadMacro("macro")
				if err != nil {
					t.Error(err)
					return
				}
				if m.Identity().SHA256 != sha256.Sum256(raw) || !bytes.Equal(m.Export(), raw) {
					t.Error("concurrent observation changed")
				}
			}
		}()
	}
	wg.Wait()
}

func FuzzReadMacroNames(f *testing.F) {
	path := f.TempDir()
	raw := macroBytes(f, macroFixtures(f)[0])
	if err := os.WriteFile(filepath.Join(path, "macro"), raw, 0600); err != nil {
		f.Fatal(err)
	}
	if err := os.Mkdir(filepath.Join(path, "directory"), 0700); err != nil {
		f.Fatal(err)
	}
	if err := syscall.Mkfifo(filepath.Join(path, "fifo"), 0600); err != nil {
		f.Fatal(err)
	}
	if err := os.Symlink("macro", filepath.Join(path, "link")); err != nil {
		f.Fatal(err)
	}
	d, err := storage.OpenDirectory(path)
	if err != nil {
		f.Fatal(err)
	}
	f.Cleanup(func() { d.Close() })
	for _, name := range []string{"macro", "link", "fifo", "directory", "", ".", "..", "../macro", "/etc/passwd", "bad\x00name", strings.Repeat("x", 256), ".wordling-candidate-any", "C:\\OUT\\macro"} {
		f.Add(name)
	}
	f.Fuzz(func(t *testing.T, name string) {
		m, err := d.ReadMacro(name)
		unsafe := len(name) > 255 || name == "" || name == "." || name == ".." || strings.ContainsAny(name, "/\x00") || strings.HasPrefix(name, ".wordling-candidate-")
		if err == nil {
			if unsafe || name != "macro" || m == nil || !bytes.Equal(m.Export(), raw) || m.Identity().SHA256 != sha256.Sum256(raw) {
				t.Fatal("unexpected acquisition", name)
			}
			return
		}
		var failure *storage.Failure
		if m != nil || !errors.As(err, &failure) {
			t.Fatal("untyped/partial refusal", err)
		}
		if unsafe && failure.Kind != storage.UnsafePath {
			t.Fatal("lexical policy bypass", name, err)
		}
		entries, err := os.ReadDir(path)
		if err != nil || len(entries) != 4 {
			t.Fatal("read created/removed entry", entries, err)
		}
	})
}
