package storage

import (
	"bytes"
	"errors"
	"io"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"syscall"
	"testing"

	"github.com/lynncoleart/wordling/internal/wp51"
)

type hookFS struct {
	filesystem
	open   func(string, int, fs.FileMode) (file, error)
	link   func(string, string) error
	remove func(string) error
	lstat  func(string) (os.FileInfo, error)
}

func (f hookFS) OpenFile(n string, flags int, p fs.FileMode) (file, error) {
	if f.open != nil {
		return f.open(n, flags, p)
	}
	return f.filesystem.OpenFile(n, flags, p)
}
func (f hookFS) Link(a, b string) error {
	if f.link != nil {
		return f.link(a, b)
	}
	return f.filesystem.Link(a, b)
}
func (f hookFS) Remove(n string) error {
	if f.remove != nil {
		return f.remove(n)
	}
	return f.filesystem.Remove(n)
}
func (f hookFS) Lstat(n string) (os.FileInfo, error) {
	if f.lstat != nil {
		return f.lstat(n)
	}
	return f.filesystem.Lstat(n)
}

type hookFile struct {
	file
	write func([]byte) (int, error)
	read  func([]byte) (int, error)
	close func() error
	stat  func() (os.FileInfo, error)
}

func (f hookFile) Write(p []byte) (int, error) {
	if f.write != nil {
		return f.write(p)
	}
	return f.file.Write(p)
}
func (f hookFile) Read(p []byte) (int, error) {
	if f.read != nil {
		return f.read(p)
	}
	return f.file.Read(p)
}
func (f hookFile) Close() error {
	if f.close != nil {
		return f.close()
	}
	return f.file.Close()
}
func (f hookFile) Stat() (os.FileInfo, error) {
	if f.stat != nil {
		return f.stat()
	}
	return f.file.Stat()
}
func storageCase(t *testing.T) (*Directory, *Document, *Destination, string, []byte) {
	t.Helper()
	input, err := os.ReadFile("../../docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5")
	if err != nil {
		t.Fatal(err)
	}
	path := t.TempDir()
	must(t, os.WriteFile(filepath.Join(path, "source"), input, 0600))
	d, err := OpenDirectory(path)
	must(t, err)
	t.Cleanup(func() { d.Close() })
	doc, err := d.Read("source")
	must(t, err)
	target, err := d.Observe("destination")
	must(t, err)
	return d, doc, target, path, input
}
func must(t *testing.T, err error) {
	t.Helper()
	if err != nil {
		t.Fatal(err)
	}
}
func refusal(t *testing.T, out Outcome, err error, kind Kind) *Failure {
	t.Helper()
	var f *Failure
	if out.State != "" || !errors.As(err, &f) || f.Kind != kind {
		t.Fatalf("want %s refusal and empty outcome, got %+v / %v", kind, out, err)
	}
	return f
}
func content(t *testing.T, path string, want []byte) {
	t.Helper()
	got, err := os.ReadFile(path)
	must(t, err)
	if !bytes.Equal(got, want) {
		t.Fatalf("bytes changed at %s", path)
	}
}
func absent(t *testing.T, path string) {
	t.Helper()
	_, err := os.Lstat(path)
	if !errors.Is(err, fs.ErrNotExist) {
		t.Fatalf("unexpected entry at %s: %v", path, err)
	}
}
func candidateNames(t *testing.T, path string) []string {
	t.Helper()
	entries, err := os.ReadDir(path)
	must(t, err)
	var out []string
	for _, entry := range entries {
		if strings.HasPrefix(entry.Name(), candidatePrefix) {
			out = append(out, entry.Name())
		}
	}
	return out
}

func TestInjectedCandidateAndPublicationFailures(t *testing.T) {
	for _, which := range []string{"create", "short write", "zero write", "partial write error", "full write error", "close", "corrupt bytes", "candidate read close", "link", "cleanup", "pin close", "guard open", "guard stat", "create stat"} {
		t.Run(which, func(t *testing.T) {
			d, doc, target, path, input := storageCase(t)
			base := d.ops
			injected := errors.New("injected " + which)
			readOpens := 0
			d.ops = hookFS{filesystem: base, open: func(name string, flags int, mode fs.FileMode) (file, error) {
				candidate := strings.HasPrefix(name, candidatePrefix)
				if candidate && flags&os.O_CREATE != 0 && which == "create" {
					return nil, injected
				}
				if candidate && flags&os.O_CREATE == 0 {
					readOpens++
					if readOpens == 1 && which == "guard open" {
						return nil, injected
					}
				}
				f, err := base.OpenFile(name, flags, mode)
				if err != nil {
					return nil, err
				}
				if !candidate {
					return f, nil
				}
				if flags&os.O_CREATE != 0 {
					switch which {
					case "short write":
						return hookFile{file: f, write: func(p []byte) (int, error) { return f.Write(p[:len(p)/2]) }}, nil
					case "zero write":
						return hookFile{file: f, write: func([]byte) (int, error) { return 0, nil }}, nil
					case "partial write error":
						return hookFile{file: f, write: func(p []byte) (int, error) { n, _ := f.Write(p[:len(p)/2]); return n, injected }}, nil
					case "full write error":
						return hookFile{file: f, write: func(p []byte) (int, error) { n, _ := f.Write(p); return n, injected }}, nil
					case "close":
						return hookFile{file: f, close: func() error { f.Close(); return injected }}, nil
					case "corrupt bytes":
						return hookFile{file: f, write: func(p []byte) (int, error) { copy := bytes.Clone(p); copy[len(copy)-1] ^= 1; return f.Write(copy) }}, nil
					case "create stat":
						return hookFile{file: f, stat: func() (os.FileInfo, error) { return nil, injected }}, nil
					}
				} else if which == "pin close" && readOpens == 1 {
					return hookFile{file: f, close: func() error { f.Close(); return injected }}, nil
				} else if which == "guard stat" && readOpens == 1 {
					return hookFile{file: f, stat: func() (os.FileInfo, error) { return nil, injected }}, nil
				} else if which == "candidate read close" {
					return hookFile{file: f, close: func() error { f.Close(); return injected }}, nil
				}
				return f, nil
			}, link: func(a, b string) error {
				if which == "link" {
					return injected
				}
				return base.Link(a, b)
			}, remove: func(n string) error {
				if which == "cleanup" {
					return injected
				}
				return base.Remove(n)
			}}
			out, err := d.Save(doc, target, NoOverwrite)
			kind := CandidateFailed
			if which == "link" {
				kind = PublicationFailed
			}
			if which == "cleanup" || which == "pin close" {
				kind = CleanupFailed
			}
			f := refusal(t, out, err, kind)
			if which == "short write" || which == "zero write" {
				if !errors.Is(err, io.ErrShortWrite) {
					t.Fatal("short-write identity lost")
				}
			}
			if which == "create" || which == "partial write error" || which == "full write error" || which == "close" || which == "candidate read close" || which == "link" || which == "cleanup" || which == "create stat" || which == "pin close" || which == "guard open" || which == "guard stat" {
				if !errors.Is(err, injected) {
					t.Fatal("I/O cause lost")
				}
			}
			content(t, filepath.Join(path, "source"), input)
			if which == "cleanup" || which == "pin close" {
				content(t, filepath.Join(path, "destination"), input)
				if !f.DestinationMayExist || (which == "cleanup" && f.Candidate == "") {
					t.Fatal("published cleanup failure not explicit")
				}
			} else {
				absent(t, filepath.Join(path, "destination"))
			}
			leftovers := candidateNames(t, path)
			if which == "cleanup" || which == "create stat" {
				if len(leftovers) != 1 || f.Candidate == "" {
					t.Fatal("cleanup residue hidden")
				}
			} else if len(leftovers) != 0 {
				t.Fatal("ordinary failure leaked candidate")
			}
		})
	}
}
func TestSourceChangedDuringCandidateWrite(t *testing.T) {
	for _, replacement := range []bool{false, true} {
		t.Run(map[bool]string{false: "in-place", true: "inode-replacement"}[replacement], func(t *testing.T) {
			d, doc, target, path, input := storageCase(t)
			base := d.ops
			changed := append(bytes.Clone(input), 'x')
			d.ops = hookFS{filesystem: base, open: func(n string, flags int, p fs.FileMode) (file, error) {
				f, err := base.OpenFile(n, flags, p)
				if err != nil {
					return nil, err
				}
				if flags&os.O_CREATE == 0 {
					return f, nil
				}
				return hookFile{file: f, write: func(b []byte) (int, error) {
					if replacement {
						must(t, os.WriteFile(filepath.Join(path, "replacement"), changed, 0600))
						must(t, os.Rename(filepath.Join(path, "replacement"), filepath.Join(path, "source")))
					} else {
						must(t, os.WriteFile(filepath.Join(path, "source"), changed, 0600))
					}
					return f.Write(b)
				}}, nil
			}}
			out, err := d.Save(doc, target, NoOverwrite)
			refusal(t, out, err, StaleSource)
			content(t, filepath.Join(path, "source"), changed)
			absent(t, filepath.Join(path, "destination"))
			if len(candidateNames(t, path)) != 0 {
				t.Fatal("candidate leaked")
			}
		})
	}
}
func TestAtomicNoReplaceAgainstLateDestination(t *testing.T) {
	for _, symlink := range []bool{false, true} {
		t.Run(map[bool]string{false: "file", true: "symlink"}[symlink], func(t *testing.T) {
			d, doc, target, path, input := storageCase(t)
			base := d.ops
			foreign := []byte("unrelated bytes")
			outside := filepath.Join(t.TempDir(), "outside")
			must(t, os.WriteFile(outside, foreign, 0600))
			d.ops = hookFS{filesystem: base, link: func(a, b string) error {
				if symlink {
					must(t, os.Symlink(outside, filepath.Join(path, b)))
				} else {
					must(t, os.WriteFile(filepath.Join(path, b), foreign, 0600))
				}
				return base.Link(a, b)
			}}
			out, err := d.Save(doc, target, NoOverwrite)
			f := refusal(t, out, err, PublicationFailed)
			if !errors.Is(err, fs.ErrExist) || !f.DestinationMayExist {
				t.Fatal("late destination conflict hidden")
			}
			content(t, filepath.Join(path, "source"), input)
			content(t, filepath.Join(path, "destination"), foreign)
			content(t, outside, foreign)
			if len(candidateNames(t, path)) != 0 {
				t.Fatal("candidate leaked")
			}
		})
	}
}
func TestCandidateSubstitutionBeforeAndDuringLink(t *testing.T) {
	for _, when := range []string{"before verification", "between check and link", "different inode between check and link"} {
		t.Run(when, func(t *testing.T) {
			d, doc, target, path, input := storageCase(t)
			base := d.ops
			foreign := []byte("foreign candidate")
			outside := filepath.Join(t.TempDir(), "outside")
			must(t, os.WriteFile(outside, foreign, 0600))
			substitute := func(name string) {
				must(t, os.Remove(filepath.Join(path, name)))
				if when == "different inode between check and link" {
					must(t, os.WriteFile(filepath.Join(path, name), foreign, 0600))
				} else {
					must(t, os.Symlink(outside, filepath.Join(path, name)))
				}
			}
			d.ops = hookFS{filesystem: base, open: func(n string, flags int, p fs.FileMode) (file, error) {
				f, err := base.OpenFile(n, flags, p)
				if err != nil {
					return nil, err
				}
				if flags&os.O_CREATE != 0 && when == "before verification" {
					return hookFile{file: f, close: func() error { err := f.Close(); substitute(n); return err }}, nil
				}
				return f, nil
			}, link: func(a, b string) error {
				if when != "before verification" {
					substitute(a)
				}
				return base.Link(a, b)
			}}
			out, err := d.Save(doc, target, NoOverwrite)
			kind := PublicationUncertain
			if when == "before verification" {
				kind = CandidateFailed
			}
			f := refusal(t, out, err, kind)
			if f.Candidate == "" {
				t.Fatal("substituted candidate residue hidden")
			}
			if when == "before verification" {
				absent(t, filepath.Join(path, "destination"))
			} else if !f.DestinationMayExist {
				t.Fatal("uncertain publication hidden")
			}
			content(t, filepath.Join(path, "source"), input)
			content(t, outside, foreign)
			if len(candidateNames(t, path)) != 1 {
				t.Fatal("substituted candidate was removed")
			}
		})
	}
}
func TestForeignDestinationAfterLinkIsNeverRolledBack(t *testing.T) {
	d, doc, target, path, input := storageCase(t)
	base := d.ops
	foreign := []byte("concurrent owner's destination")
	d.ops = hookFS{filesystem: base, link: func(a, b string) error {
		must(t, base.Link(a, b))
		must(t, os.WriteFile(filepath.Join(path, "foreign"), foreign, 0600))
		return os.Rename(filepath.Join(path, "foreign"), filepath.Join(path, b))
	}}
	out, err := d.Save(doc, target, NoOverwrite)
	f := refusal(t, out, err, PublicationUncertain)
	if !f.DestinationMayExist {
		t.Fatal("post-link uncertainty hidden")
	}
	content(t, filepath.Join(path, "source"), input)
	content(t, filepath.Join(path, "destination"), foreign)
}
func TestLinkErrorAfterSideEffectIsNotSuccess(t *testing.T) {
	d, doc, target, path, input := storageCase(t)
	base := d.ops
	injected := errors.New("publication result uncertain")
	d.ops = hookFS{filesystem: base, link: func(a, b string) error { must(t, base.Link(a, b)); return injected }}
	out, err := d.Save(doc, target, NoOverwrite)
	f := refusal(t, out, err, PublicationFailed)
	if !f.DestinationMayExist || !errors.Is(err, injected) {
		t.Fatal("uncertain result hidden")
	}
	content(t, filepath.Join(path, "source"), input)
	content(t, filepath.Join(path, "destination"), input)
}
func TestDirectoryPathReplacementCannotRedirectPublication(t *testing.T) {
	parent := t.TempDir()
	path := filepath.Join(parent, "chosen")
	moved := filepath.Join(parent, "moved")
	outside := t.TempDir()
	must(t, os.Mkdir(path, 0700))
	input, err := os.ReadFile("../../docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5")
	must(t, err)
	must(t, os.WriteFile(filepath.Join(path, "source"), input, 0600))
	d, err := OpenDirectory(path)
	must(t, err)
	defer d.Close()
	doc, err := d.Read("source")
	must(t, err)
	target, err := d.Observe("destination")
	must(t, err)
	base := d.ops
	d.ops = hookFS{filesystem: base, link: func(a, b string) error {
		must(t, os.Rename(path, moved))
		must(t, os.Symlink(outside, path))
		return base.Link(a, b)
	}}
	out, err := d.Save(doc, target, NoOverwrite)
	must(t, err)
	if out.State != Published || out.DirectoryID != d.ID() {
		t.Fatal("pinned directory identity lost")
	}
	content(t, filepath.Join(moved, "source"), input)
	content(t, filepath.Join(moved, "destination"), input)
	absent(t, filepath.Join(outside, "destination"))
	absent(t, filepath.Join(outside, "source"))
}
func TestReadPathRacesRefuseSymlinkAndFIFOWithoutFollowing(t *testing.T) {
	for _, fifo := range []bool{false, true} {
		t.Run(map[bool]string{false: "symlink", true: "fifo"}[fifo], func(t *testing.T) {
			d, _, _, path, input := storageCase(t)
			base := d.ops
			outside := filepath.Join(t.TempDir(), "outside")
			must(t, os.WriteFile(outside, input, 0600))
			swapped := false
			d.ops = hookFS{filesystem: base, open: func(n string, flags int, p fs.FileMode) (file, error) {
				if n == "source" && !swapped {
					swapped = true
					must(t, os.Rename(filepath.Join(path, n), filepath.Join(path, "original")))
					if fifo {
						must(t, syscall.Mkfifo(filepath.Join(path, n), 0600))
					} else {
						must(t, os.Symlink(outside, filepath.Join(path, n)))
					}
				}
				return base.OpenFile(n, flags, p)
			}}
			doc, err := d.Read("source")
			if doc != nil {
				t.Fatal("unsafe source accepted")
			}
			var f *Failure
			if !errors.As(err, &f) || f.Kind != UnsafePath {
				t.Fatal(err)
			}
			content(t, outside, input)
			content(t, filepath.Join(path, "original"), input)
		})
	}
}
func TestReadDetectsReplacementAfterOpen(t *testing.T) {
	d, _, _, path, input := storageCase(t)
	base := d.ops
	foreign := append(bytes.Clone(input), 'x')
	changed := false
	d.ops = hookFS{filesystem: base, open: func(n string, flags int, p fs.FileMode) (file, error) {
		f, err := base.OpenFile(n, flags, p)
		if err != nil {
			return nil, err
		}
		if n != "source" {
			return f, nil
		}
		return hookFile{file: f, read: func(b []byte) (int, error) {
			if !changed {
				changed = true
				must(t, os.Rename(filepath.Join(path, n), filepath.Join(path, "original")))
				must(t, os.WriteFile(filepath.Join(path, n), foreign, 0600))
			}
			return f.Read(b)
		}}, nil
	}}
	doc, err := d.Read("source")
	if doc != nil {
		t.Fatal("raced source accepted")
	}
	var f *Failure
	if !errors.As(err, &f) || f.Kind != StaleSource {
		t.Fatal(err)
	}
	content(t, filepath.Join(path, "original"), input)
	content(t, filepath.Join(path, "source"), foreign)
}
func TestGrowingReadIsCappedAtLimitPlusOne(t *testing.T) {
	d, _, _, path, _ := storageCase(t)
	base := d.ops
	readBytes := 0
	grew := false
	d.ops = hookFS{filesystem: base, open: func(n string, flags int, p fs.FileMode) (file, error) {
		f, err := base.OpenFile(n, flags, p)
		if err != nil {
			return nil, err
		}
		if n != "source" {
			return f, nil
		}
		return hookFile{file: f, read: func(b []byte) (int, error) {
			if !grew {
				grew = true
				g, err := os.OpenFile(filepath.Join(path, n), os.O_WRONLY, 0)
				must(t, err)
				must(t, g.Truncate(wp51.MaxInputBytes+100))
				must(t, g.Close())
			}
			n, err := f.Read(b)
			readBytes += n
			return n, err
		}}, nil
	}}
	doc, err := d.Read("source")
	if doc != nil {
		t.Fatal("oversized source accepted")
	}
	var f *Failure
	if !errors.As(err, &f) || f.Kind != InputLimit {
		t.Fatal(err)
	}
	if readBytes != wp51.MaxInputBytes+1 {
		t.Fatalf("read %d bytes, wanted limit+1", readBytes)
	}
}
func TestConcurrentCloseCannotReuseDirectoryDescriptor(t *testing.T) {
	d, _, _, path, input := storageCase(t)
	var group sync.WaitGroup
	start := make(chan struct{})
	for j := 0; j < 8; j++ {
		group.Add(1)
		go func() {
			defer group.Done()
			<-start
			for n := 0; n < 20; n++ {
				doc, err := d.Read("source")
				if err == nil {
					if !bytes.Equal(doc.Export(), input) {
						t.Error("directory descriptor redirected")
					}
				} else {
					var f *Failure
					if !errors.As(err, &f) || (f.Kind != ReadFailed && f.Kind != StaleSource) {
						t.Errorf("unexpected close race: %v", err)
					}
				}
			}
		}()
	}
	close(start)
	d.Close()
	group.Wait()
	content(t, filepath.Join(path, "source"), input)
}

func TestForeignDestinationAfterCleanupIsReportedUncertain(t *testing.T) {
	d, doc, target, path, input := storageCase(t)
	base := d.ops
	foreign := []byte("changed during candidate cleanup")
	d.ops = hookFS{filesystem: base, remove: func(n string) error {
		must(t, base.Remove(n))
		must(t, os.WriteFile(filepath.Join(path, "foreign"), foreign, 0600))
		return os.Rename(filepath.Join(path, "foreign"), filepath.Join(path, "destination"))
	}}
	out, err := d.Save(doc, target, NoOverwrite)
	f := refusal(t, out, err, PublicationUncertain)
	if !f.DestinationMayExist || f.Candidate != "" {
		t.Fatal("post-cleanup state incorrect")
	}
	content(t, filepath.Join(path, "source"), input)
	content(t, filepath.Join(path, "destination"), foreign)
}
func TestSnapshotPublicationDoesNotPromiseSourceFreshnessAfterItsCheck(t *testing.T) {
	d, doc, target, path, input := storageCase(t)
	base := d.ops
	foreign := append(bytes.Clone(input), 'x')
	d.ops = hookFS{filesystem: base, link: func(a, b string) error {
		must(t, os.WriteFile(filepath.Join(path, "source"), foreign, 0600))
		return base.Link(a, b)
	}}
	out, err := d.Save(doc, target, NoOverwrite)
	must(t, err)
	if out.State != Published {
		t.Fatal("snapshot was not published")
	}
	content(t, filepath.Join(path, "destination"), input)
	content(t, filepath.Join(path, "source"), foreign)
}
func TestReadFailuresRetainUnderlyingCause(t *testing.T) {
	for _, at := range []string{"read", "close"} {
		t.Run(at, func(t *testing.T) {
			d, _, _, path, input := storageCase(t)
			base := d.ops
			injected := errors.New("injected source " + at)
			d.ops = hookFS{filesystem: base, open: func(n string, flags int, p fs.FileMode) (file, error) {
				f, err := base.OpenFile(n, flags, p)
				if err != nil {
					return nil, err
				}
				if at == "read" {
					return hookFile{file: f, read: func(b []byte) (int, error) { n, _ := f.Read(b); return n, injected }}, nil
				}
				return hookFile{file: f, close: func() error { f.Close(); return injected }}, nil
			}}
			doc, err := d.Read("source")
			var failure *Failure
			if doc != nil || !errors.As(err, &failure) || failure.Kind != ReadFailed || !errors.Is(err, injected) {
				t.Fatalf("read failure obscured: %v", err)
			}
			content(t, filepath.Join(path, "source"), input)
		})
	}
}

func TestCandidateCollisionsHaveAFiniteRetryBudget(t *testing.T) {
	d, doc, target, path, input := storageCase(t)
	base := d.ops
	attempts := 0
	d.ops = hookFS{filesystem: base, open: func(n string, flags int, p fs.FileMode) (file, error) {
		if flags&os.O_CREATE != 0 {
			attempts++
			return nil, fs.ErrExist
		}
		return base.OpenFile(n, flags, p)
	}}
	out, err := d.Save(doc, target, NoOverwrite)
	refusal(t, out, err, CandidateFailed)
	if attempts != 16 {
		t.Fatalf("candidate attempts = %d", attempts)
	}
	content(t, filepath.Join(path, "source"), input)
	absent(t, filepath.Join(path, "destination"))
}
