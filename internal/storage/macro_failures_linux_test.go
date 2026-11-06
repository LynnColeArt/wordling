package storage

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"io/fs"
	"os"
	"path/filepath"
	"syscall"
	"testing"

	"github.com/lynncoleart/wordling/internal/macro/wpm"
	"github.com/lynncoleart/wordling/internal/wp51"
)

func macroReadCase(t *testing.T) (*Directory, string, []byte) {
	t.Helper()
	raw, err := os.ReadFile("../../docs/research/reference-runs/2026-10-29-extended-04/CMD51-131/TESTMAC.WPM")
	must(t, err)
	sum := sha256.Sum256(raw)
	if hex.EncodeToString(sum[:]) != "e0e71258e6dc4c678b27773831105f0e7fca0b0803d451fb58b80ac02bc20b4e" {
		t.Fatal("original macro changed")
	}
	path := t.TempDir()
	must(t, os.WriteFile(filepath.Join(path, "macro"), raw, 0600))
	d, err := OpenDirectory(path)
	must(t, err)
	t.Cleanup(func() { d.Close() })
	return d, path, raw
}
func macroFailure(t *testing.T, m *Macro, err error, kind Kind) *Failure {
	t.Helper()
	var f *Failure
	if m != nil || !errors.As(err, &f) || f.Kind != kind {
		t.Fatalf("want nil/%s got %v/%v", kind, m, err)
	}
	return f
}

func TestReadMacroReusesAcquisitionFaultBoundaries(t *testing.T) {
	for _, which := range []string{"open", "read", "close", "read+close", "stat-before", "stat-after", "lookup"} {
		t.Run(which, func(t *testing.T) {
			d, path, raw := macroReadCase(t)
			base := d.ops
			injected := errors.New("macro injected " + which)
			closeErr := errors.New("macro injected close")
			statCalls := 0
			d.ops = hookFS{filesystem: base,
				open: func(name string, flags int, mode fs.FileMode) (file, error) {
					if name != "macro" || flags&(os.O_WRONLY|os.O_RDWR|os.O_CREATE|os.O_TRUNC|os.O_APPEND) != 0 || flags&syscall.O_NOFOLLOW == 0 || flags&syscall.O_NONBLOCK == 0 {
						t.Fatal("read did not reuse no-follow/read-only/nonblocking engine", name, flags)
					}
					if which == "open" {
						return nil, injected
					}
					f, err := base.OpenFile(name, flags, mode)
					if err != nil {
						return nil, err
					}
					return hookFile{file: f,
						read: func(p []byte) (int, error) {
							if which == "read" || which == "read+close" {
								return 0, injected
							}
							return f.Read(p)
						},
						close: func() error {
							err := f.Close()
							if which == "close" {
								return injected
							}
							if which == "read+close" {
								return closeErr
							}
							return err
						},
						stat: func() (os.FileInfo, error) {
							statCalls++
							if which == "stat-before" && statCalls == 1 || which == "stat-after" && statCalls == 2 {
								return nil, injected
							}
							return f.Stat()
						},
					}, nil
				},
				lstat: func(name string) (os.FileInfo, error) {
					if which == "lookup" {
						return nil, injected
					}
					return base.Lstat(name)
				},
			}
			m, err := d.ReadMacro("macro")
			kind := ReadFailed
			if which == "lookup" {
				kind = StaleSource
			}
			f := macroFailure(t, m, err, kind)
			if !errors.Is(err, injected) {
				t.Fatal("storage cause discarded", err)
			}
			if which == "read+close" && !errors.Is(err, closeErr) {
				t.Fatal("close cause discarded", err)
			}
			if which == "close" && f.Stage != "read close" {
				t.Fatal("close exposed accepted snapshot", err)
			}
			var codec *wpm.Failure
			if errors.As(err, &codec) {
				t.Fatal("storage error rewritten as codec error")
			}
			content(t, filepath.Join(path, "macro"), raw)
			if len(candidateNames(t, path)) != 0 {
				t.Fatal("read created candidate")
			}
		})
	}
}

func TestReadMacroDetectsRealChangesAfterOpen(t *testing.T) {
	for _, which := range []string{"modify", "replace", "symlink"} {
		t.Run(which, func(t *testing.T) {
			d, path, raw := macroReadCase(t)
			base := d.ops
			foreign := bytes.Clone(raw)
			foreign[72] = 'Z'
			must(t, os.WriteFile(filepath.Join(path, "foreign"), foreign, 0600))
			changed := false
			d.ops = hookFS{filesystem: base, open: func(name string, flags int, mode fs.FileMode) (file, error) {
				f, err := base.OpenFile(name, flags, mode)
				if err != nil {
					return nil, err
				}
				return hookFile{file: f, read: func(p []byte) (int, error) {
					n, err := f.Read(p)
					if n > 0 && !changed {
						changed = true
						switch which {
						case "modify":
							must(t, os.WriteFile(filepath.Join(path, "macro"), append(bytes.Clone(raw), 'x'), 0600))
						case "replace":
							must(t, os.WriteFile(filepath.Join(path, "replacement"), foreign, 0600))
							must(t, os.Rename(filepath.Join(path, "replacement"), filepath.Join(path, "macro")))
						case "symlink":
							must(t, os.Rename(filepath.Join(path, "macro"), filepath.Join(path, "pinned-old")))
							must(t, os.Symlink("foreign", filepath.Join(path, "macro")))
						}
					}
					return n, err
				}}, nil
			}}
			m, err := d.ReadMacro("macro")
			macroFailure(t, m, err, StaleSource)
			if !changed {
				t.Fatal("fault not exercised")
			}
			content(t, filepath.Join(path, "foreign"), foreign)
			if which == "symlink" {
				content(t, filepath.Join(path, "pinned-old"), raw)
			}
			if len(candidateNames(t, path)) != 0 {
				t.Fatal("read created candidate")
			}
		})
	}
}

func TestReadMacroCapsGrowingInputAndNeverOpensUnsafeName(t *testing.T) {
	d, path, raw := macroReadCase(t)
	base := d.ops
	seen := 0
	if wp51.MaxInputBytes != wpm.MaxInputBytes {
		t.Fatal("shared acquisition and codec limits require reviewed update")
	}
	d.ops = hookFS{filesystem: base, open: func(name string, flags int, mode fs.FileMode) (file, error) {
		f, err := base.OpenFile(name, flags, mode)
		if err != nil {
			return nil, err
		}
		return hookFile{file: f, read: func(p []byte) (int, error) { clear(p); seen += len(p); return len(p), nil }}, nil
	}}
	m, err := d.ReadMacro("macro")
	f := macroFailure(t, m, err, InputLimit)
	if f.Stage != "bounded read" || seen != wp51.MaxInputBytes+1 {
		t.Fatal("unbounded/growing read", seen, err)
	}
	content(t, filepath.Join(path, "macro"), raw)
	opened := false
	d.ops = hookFS{filesystem: base, open: func(string, int, fs.FileMode) (file, error) { opened = true; return nil, errors.New("must not open") }}
	m, err = d.ReadMacro("../macro")
	macroFailure(t, m, err, UnsafePath)
	if opened {
		t.Fatal("unsafe name reached openat")
	}
}

func TestReadMacroClosedDirectoryRefuses(t *testing.T) {
	d, _, _ := macroReadCase(t)
	must(t, d.Close())
	m, err := d.ReadMacro("macro")
	macroFailure(t, m, err, ReadFailed)
}
