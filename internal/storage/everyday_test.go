package storage

import (
	"bytes"
	"errors"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"sync"
	"syscall"
	"testing"
	"time"

	"golang.org/x/sys/unix"
)

func everydayData(t *testing.T) []byte {
	t.Helper()
	b, e := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/r2/EVERY.WP")
	if e != nil {
		t.Fatal(e)
	}
	return b
}
func everydayDir(t *testing.T) (*Directory, string) {
	t.Helper()
	path := t.TempDir()
	d, e := OpenDirectory(path)
	must(t, e)
	t.Cleanup(func() { d.Close() })
	return d, path
}
func putEveryday(t *testing.T, path, name string, b []byte) {
	t.Helper()
	must(t, os.WriteFile(filepath.Join(path, name), b, 0600))
}
func observeEveryday(t *testing.T, d *Directory, name string) *Destination {
	t.Helper()
	dst, e := d.Observe(name)
	must(t, e)
	return dst
}
func readEveryday(t *testing.T, d *Directory, name string) *Document {
	t.Helper()
	doc, e := d.Read(name)
	must(t, e)
	return doc
}
func saveEveryday(t *testing.T, d *Directory, src *Document, name string, data []byte, backup OriginalBackup, op uint64) SaveResult {
	t.Helper()
	id := PublicationID{op, op}
	dst := observeEveryday(t, d, name)
	if src == nil {
		p, e := d.PrepareNewSave(dst, data, AllowOverwrite, backup, id)
		must(t, e)
		r, e := d.PublishNewSave(p, id)
		must(t, e)
		return r
	}
	p, e := d.PrepareSave(src, dst, data, AllowOverwrite, backup, id)
	must(t, e)
	r, e := d.PublishSave(p, id)
	must(t, e)
	return r
}
func nativeEdit(b []byte, s string) []byte { return append(append([]byte{}, b...), []byte(s)...) }

func TestEverydayWorkspaceMappingAndSelections(t *testing.T) {
	path := t.TempDir()
	data := everydayData(t)
	must(t, os.Mkdir(filepath.Join(path, "letters"), 0700))
	putEveryday(t, path, "Draft.wp", data)
	putEveryday(t, path, "TOOLONGNAME.WP", data)
	putEveryday(t, path, "DUP.WP", data)
	putEveryday(t, path, "dup.wp", data)
	putEveryday(t, path, "NOEXT", data)
	must(t, os.Symlink("Draft.wp", filepath.Join(path, "LINK.WP")))
	w, e := OpenWorkspace(path)
	must(t, e)
	defer w.Close()
	root, e := w.Root()
	must(t, e)
	l, e := root.List("*.*")
	must(t, e)
	if l.Metrics().Entries != 7 || l.Metrics().Unsupported != 4 || l.Metrics().TotalBytes == 0 {
		t.Fatalf("metrics %+v", l.Metrics())
	}
	entries := l.Entries()
	entries[0].Name = "forged"
	if l.Entries()[0].Name == "forged" {
		t.Fatal("mutable listing")
	}
	for _, name := range []string{"DUP", "LINK", "TOOLONG"} {
		i := l.Find(name)
		if name == "TOOLONG" {
			for j, v := range l.Entries() {
				if v.Name == "TOOLONGNAME.WP" {
					i = j
				}
			}
		}
		s, e := l.Select(i)
		must(t, e)
		if _, e = s.Read(); e == nil {
			t.Fatalf("unsupported %s read", name)
		}
	}
	s, e := l.Select(l.Find("DRAFT"))
	must(t, e)
	doc, e := s.Read()
	must(t, e)
	if !bytes.Equal(doc.Export(), data) {
		t.Fatal("Look altered native bytes")
	}
	putEveryday(t, path, "Draft.wp", nativeEdit(data, "changed"))
	if _, e = s.Read(); e == nil {
		t.Fatal("stale selection reacquired changed file")
	}
	for _, bad := range []string{`..`, `C:\..`, `D:\`, `letters/..`, `LINK.WP`} {
		if _, e = root.Navigate(bad); e == nil {
			t.Errorf("navigate %q", bad)
		}
	}
	child, e := root.Navigate(`c:\LETTERS`)
	must(t, e)
	if child.DOSPath() != `C:\LETTERS` {
		t.Fatal(child.DOSPath())
	}
	again, e := root.Navigate(`letters`)
	must(t, e)
	if again != child {
		t.Fatal("navigation retained redundant handles")
	}
	parent, e := child.Navigate(`..`)
	must(t, e)
	if parent != root {
		t.Fatal("parent differs")
	}
	dst, e := child.Observe("new.wp")
	must(t, e)
	if dst.Name() != "NEW.WP" {
		t.Fatal(dst.Name())
	}
	for _, n := range []string{"WP{WP}US.SUP", "SPELLADD", "A.BK!"} {
		if _, e = DOSName(n); e != nil {
			t.Fatal(n, e)
		}
	}
	for _, n := range []string{"CON.TXT", "É.WP", "two words.wp", "TOOLONGNAME.WP", "A/../B", "A.", "a..b"} {
		if _, e = DOSName(n); e == nil {
			t.Fatal("unsafe name", n)
		}
	}
	filtered, e := root.List("*.WP")
	must(t, e)
	if filtered.Find("NOEXT") != -1 {
		t.Fatal("wildcard ignored")
	}
	if _, e = root.Observe("Dup.wp"); e == nil {
		t.Fatal("case collision accepted")
	}
	must(t, w.Close())
	if _, e = s.Read(); e == nil {
		t.Fatal("selection survives closed workspace")
	}
	if _, e = child.Navigate("."); e == nil {
		t.Fatal("closed navigation")
	}
}
func TestEverydayPinnedWorkspaceAndFreshSelection(t *testing.T) {
	parent := t.TempDir()
	path := filepath.Join(parent, "root")
	must(t, os.Mkdir(path, 0700))
	must(t, os.Mkdir(filepath.Join(path, "CHILD"), 0700))
	data := everydayData(t)
	putEveryday(t, filepath.Join(path, "CHILD"), "OLD.WP", data)
	w, e := OpenWorkspace(path)
	must(t, e)
	defer w.Close()
	root, e := w.Root()
	must(t, e)
	l, e := root.List("")
	must(t, e)
	sel, e := l.Select(l.Find(`\CHILD`))
	must(t, e)
	child, e := sel.Enter()
	must(t, e)
	must(t, os.Rename(path, path+"-moved"))
	must(t, os.Mkdir(path, 0700))
	must(t, os.Mkdir(filepath.Join(path, "CHILD"), 0700))
	putEveryday(t, filepath.Join(path, "CHILD"), "EVIL.WP", data)
	files, e := child.List("")
	must(t, e)
	if files.Find("EVIL") != -1 || files.Find("OLD") < 0 {
		t.Fatal("rebound parent authority")
	}
	dst, e := child.Observe("NEW.WP")
	must(t, e)
	id := PublicationID{1, 1}
	p, e := child.Directory().PrepareNewSave(dst, data, NoOverwrite, OriginalBackupOff, id)
	must(t, e)
	_, e = child.Directory().PublishNewSave(p, id)
	must(t, e)
	content(t, filepath.Join(path+"-moved", "CHILD", "NEW.WP"), data)
	absent(t, filepath.Join(path, "CHILD", "NEW.WP"))
}
func TestEverydayRepeatedSaveAndOriginalBackupContract(t *testing.T) {
	for _, setting := range []OriginalBackup{OriginalBackupOff, OriginalBackupOn} {
		t.Run(map[OriginalBackup]string{OriginalBackupOff: "disabled", OriginalBackupOn: "enabled"}[setting], func(t *testing.T) {
			d, path := everydayDir(t)
			a := everydayData(t)
			b := nativeEdit(a, "second")
			c := nativeEdit(a, "third")
			first := saveEveryday(t, d, nil, "A.WP", a, setting, 1)
			content(t, filepath.Join(path, "A.WP"), a)
			absent(t, filepath.Join(path, "A.BK!"))
			second := saveEveryday(t, d, first.Document, "A.WP", b, setting, 2)
			if setting == OriginalBackupOn {
				content(t, filepath.Join(path, "A.BK!"), a)
			} else {
				absent(t, filepath.Join(path, "A.BK!"))
			}
			third := saveEveryday(t, d, second.Document, "A.WP", c, OriginalBackupOn, 3)
			content(t, filepath.Join(path, "A.BK!"), b)
			saveEveryday(t, d, third.Document, "A.WP", a, OriginalBackupOff, 4)
			content(t, filepath.Join(path, "A.WP"), a)
			absent(t, filepath.Join(path, "A.BK!"))
			if len(candidateNames(t, path)) != 0 {
				t.Fatal("staging residue")
			}
		})
	}
}
func TestEverydaySaveAsBacksUpDestinationAndCollision(t *testing.T) {
	source, sp := everydayDir(t)
	dest, dp := everydayDir(t)
	a := everydayData(t)
	b := nativeEdit(a, "other destination")
	edit := nativeEdit(a, "edited source")
	putEveryday(t, sp, "SOURCE.WP", a)
	src := readEveryday(t, source, "SOURCE.WP")
	putEveryday(t, dp, "A.TXT", b)
	putEveryday(t, dp, "A.WP", a)
	putEveryday(t, dp, "A.BK!", []byte("old arbitrary backup"))
	r := saveEveryday(t, dest, src, "A.TXT", edit, OriginalBackupOn, 1)
	content(t, filepath.Join(dp, "A.BK!"), b)
	content(t, filepath.Join(sp, "SOURCE.WP"), a)
	saveEveryday(t, dest, r.Document, "A.WP", edit, OriginalBackupOn, 2)
	content(t, filepath.Join(dp, "A.BK!"), a)
	// Existing same-basename backup is preserved on first save: no historical
	// evidence authorizes deleting it for an absent document destination.
	saveEveryday(t, dest, src, "A.NEW", edit, OriginalBackupOff, 3)
	content(t, filepath.Join(dp, "A.BK!"), a)
	target := observeEveryday(t, dest, "A.BK!")
	if _, e := dest.PrepareSave(src, target, edit, AllowOverwrite, OriginalBackupOn, PublicationID{4, 4}); e == nil {
		t.Fatal("backup selfcollision allowed")
	}
	must(t, os.Remove(filepath.Join(dp, "A.BK!")))
	must(t, os.Link(filepath.Join(dp, "A.WP"), filepath.Join(dp, "A.BK!")))
	if _, e := dest.PrepareSave(src, observeEveryday(t, dest, "A.WP"), edit, AllowOverwrite, OriginalBackupOn, PublicationID{5, 5}); e == nil {
		t.Fatal("backup hardlink alias allowed")
	}
}
func TestEverydayCancelRefusalReplayAndImmutableCapture(t *testing.T) {
	d, path := everydayDir(t)
	a := everydayData(t)
	edit := nativeEdit(a, "edited")
	putEveryday(t, path, "A.WP", a)
	putEveryday(t, path, "A.BK!", []byte("prior"))
	src := readEveryday(t, d, "A.WP")
	dst := observeEveryday(t, d, "A.WP")
	id := PublicationID{1, 1}
	if _, e := d.PrepareSave(src, dst, edit, NoOverwrite, OriginalBackupOn, id); e == nil {
		t.Fatal("overwrite default accepted")
	}
	p, e := d.PrepareSave(src, dst, edit, AllowOverwrite, OriginalBackupOn, id)
	must(t, e)
	copy := *p
	if !p.Cancel() || copy.Cancel() {
		t.Fatal("cancel capability not shared")
	}
	if _, e = d.PublishSave(&copy, id); e == nil {
		t.Fatal("canceled published")
	}
	content(t, filepath.Join(path, "A.WP"), a)
	content(t, filepath.Join(path, "A.BK!"), []byte("prior"))
	if len(candidateNames(t, path)) != 0 {
		t.Fatal("cancel staged files")
	}
	p, e = d.PrepareSave(src, dst, edit, AllowOverwrite, OriginalBackupOn, id)
	must(t, e)
	want := append([]byte{}, edit...)
	edit[0] ^= 0xff
	*src = Document{}
	*dst = Destination{}
	if _, e = d.PublishSave(p, PublicationID{2, 2}); e == nil {
		t.Fatal("wrong operation")
	}
	r, e := d.PublishSave(p, id)
	must(t, e)
	content(t, filepath.Join(path, "A.WP"), want)
	if r.ID != id || !bytes.Equal(r.Document.Export(), want) {
		t.Fatal("saved source receipt")
	}
	if _, e = d.PublishSave(p, id); e == nil {
		t.Fatal("replay allowed")
	}
}
func TestEverydayStalePreparedRequests(t *testing.T) {
	for _, name := range []string{"SOURCE.WP", "A.WP", "A.BK!"} {
		t.Run(name, func(t *testing.T) {
			d, path := everydayDir(t)
			a := everydayData(t)
			for _, n := range []string{"SOURCE.WP", "A.WP", "A.BK!"} {
				putEveryday(t, path, n, a)
			}
			p, e := d.PrepareSave(readEveryday(t, d, "SOURCE.WP"), observeEveryday(t, d, "A.WP"), nativeEdit(a, "edit"), AllowOverwrite, OriginalBackupOn, PublicationID{1, 1})
			must(t, e)
			changed := nativeEdit(a, "external")
			putEveryday(t, path, name, changed)
			if _, e = d.PublishSave(p, PublicationID{1, 1}); e == nil {
				t.Fatal("stale request")
			}
			for _, n := range []string{"A.WP", "A.BK!"} {
				want := a
				if name == n {
					want = changed
				}
				content(t, filepath.Join(path, n), want)
			}
		})
	}
	t.Run("case alias appeared", func(t *testing.T) {
		d, path := everydayDir(t)
		a := everydayData(t)
		id := PublicationID{1, 1}
		p, e := d.PrepareNewSave(observeEveryday(t, d, "A.WP"), a, NoOverwrite, OriginalBackupOff, id)
		must(t, e)
		putEveryday(t, path, "a.wp", a)
		if _, e = d.PublishNewSave(p, id); e == nil {
			t.Fatal("late case alias accepted")
		}
		absent(t, filepath.Join(path, "A.WP"))
	})
}

type everydayFS struct {
	filesystem
	rename  func(string, string, uint) error
	syncDir func() error
}

func (f everydayFS) Rename(a, b string, flags uint) error {
	if f.rename != nil {
		return f.rename(a, b, flags)
	}
	return f.filesystem.Rename(a, b, flags)
}
func (f everydayFS) SyncDirectory() error {
	if f.syncDir != nil {
		return f.syncDir()
	}
	return f.filesystem.SyncDirectory()
}

type everydaySyncFile struct {
	file
	sync func() error
}

func (f everydaySyncFile) Sync() error {
	if f.sync != nil {
		return f.sync()
	}
	return f.file.Sync()
}

func TestEverydaySaveFailureConservation(t *testing.T) {
	cases := []string{"short write", "file sync", "writer close", "backup stage", "main rename", "backup rename", "first directory sync"}
	for _, setting := range []OriginalBackup{OriginalBackupOn, OriginalBackupOff} {
		for _, fault := range cases {
			t.Run(string(rune('0'+setting))+"/"+fault, func(t *testing.T) {
				d, path := everydayDir(t)
				a := everydayData(t)
				backup := []byte("prior complete backup")
				edit := nativeEdit(a, "edited")
				putEveryday(t, path, "A.WP", a)
				putEveryday(t, path, "A.BK!", backup)
				id := PublicationID{1, 1}
				p, e := d.PrepareSave(readEveryday(t, d, "A.WP"), observeEveryday(t, d, "A.WP"), edit, AllowOverwrite, setting, id)
				must(t, e)
				base := d.ops
				fired := false
				created := 0
				syncs := 0
				hooks := hookFS{filesystem: base, open: func(n string, flags int, mode fs.FileMode) (file, error) {
					f, e := base.OpenFile(n, flags, mode)
					if e != nil {
						return f, e
					}
					if flags&os.O_CREATE != 0 {
						created++
						if (fault == "backup stage" && created == 2) || (created == 1 && fault == "short write") {
							return hookFile{file: f, write: func(b []byte) (int, error) { fired = true; return len(b) - 1, nil }}, nil
						}
						if fault == "file sync" && created == 1 {
							return everydaySyncFile{file: f, sync: func() error { fired = true; return syscall.EIO }}, nil
						}
						if fault == "writer close" && created == 1 {
							return hookFile{file: f, close: func() error { fired = true; return errors.Join(f.Close(), syscall.EIO) }}, nil
						}
					}
					return f, nil
				}}
				d.ops = everydayFS{filesystem: hooks, rename: func(a, b string, flags uint) error {
					if !fired && ((fault == "main rename" && b == "A.WP") || (fault == "backup rename" && (b == "A.BK!" || a == "A.BK!"))) {
						fired = true
						return syscall.EACCES
					}
					return base.Rename(a, b, flags)
				}, syncDir: func() error {
					syncs++
					if fault == "first directory sync" && syncs == 1 {
						fired = true
						return syscall.EIO
					}
					return base.SyncDirectory()
				}}
				_, e = d.PublishSave(p, id)
				if e == nil || !fired {
					t.Fatalf("unreached fault=%v err=%v", fired, e)
				}
				content(t, filepath.Join(path, "A.WP"), a)
				content(t, filepath.Join(path, "A.BK!"), backup)
				if len(candidateNames(t, path)) != 0 {
					t.Fatal("rollback residue", candidateNames(t, path))
				}
				// Retry is a fresh prepared request, retaining the prior backup semantics.
				d.ops = base
				saveEveryday(t, d, readEveryday(t, d, "A.WP"), "A.WP", edit, setting, 2)
			})
		}
	}
}
func TestEverydayRollbackCannotOverwriteConcurrentWriter(t *testing.T) {
	d, path := everydayDir(t)
	a := everydayData(t)
	external := nativeEdit(a, "external")
	backup := []byte("old backup")
	putEveryday(t, path, "A.WP", a)
	putEveryday(t, path, "A.BK!", backup)
	id := PublicationID{1, 1}
	p, e := d.PrepareSave(readEveryday(t, d, "A.WP"), observeEveryday(t, d, "A.WP"), nativeEdit(a, "our edit"), AllowOverwrite, OriginalBackupOn, id)
	must(t, e)
	base := d.ops
	fired := false
	d.ops = everydayFS{filesystem: base, rename: func(from, to string, flags uint) error {
		if to == "A.BK!" && !fired {
			fired = true
			must(t, os.Remove(filepath.Join(path, "A.WP")))
			putEveryday(t, path, "A.WP", external)
			return syscall.EIO
		}
		return base.Rename(from, to, flags)
	}}
	_, e = d.PublishSave(p, id)
	var failure *Failure
	if !errors.As(e, &failure) || failure.Kind != PublicationUncertain || !fired {
		t.Fatal(e)
	}
	content(t, filepath.Join(path, "A.WP"), external)
	content(t, filepath.Join(path, "A.BK!"), backup)
	if failure.Candidate == "" {
		t.Fatal("lost recovery evidence")
	}
	foundOld := false
	for _, n := range candidateNames(t, path) {
		b, e := os.ReadFile(filepath.Join(path, n))
		must(t, e)
		foundOld = foundOld || bytes.Equal(b, a)
	}
	if !foundOld {
		t.Fatal("old document not retained")
	}
}
func TestEverydayCommittedFailuresAreNotRefusals(t *testing.T) {
	for _, fault := range []string{"cleanup", "second sync", "pin close"} {
		t.Run(fault, func(t *testing.T) {
			d, path := everydayDir(t)
			a := everydayData(t)
			edit := nativeEdit(a, "edited")
			putEveryday(t, path, "A.WP", a)
			id := PublicationID{1, 1}
			p, e := d.PrepareSave(readEveryday(t, d, "A.WP"), observeEveryday(t, d, "A.WP"), edit, AllowOverwrite, OriginalBackupOn, id)
			must(t, e)
			base := d.ops
			fired := false
			syncs := 0
			hook := hookFS{filesystem: base, remove: func(n string) error {
				if fault == "cleanup" && !fired && strings.HasPrefix(n, candidatePrefix) {
					fired = true
					return syscall.EIO
				}
				return base.Remove(n)
			}, open: func(n string, flags int, mode fs.FileMode) (file, error) {
				f, e := base.OpenFile(n, flags, mode)
				if e == nil && fault == "pin close" && strings.HasPrefix(n, candidatePrefix) && flags == os.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_NONBLOCK && !fired {
					fired = true
					return hookFile{file: f, close: func() error { return errors.Join(f.Close(), syscall.EIO) }}, nil
				}
				return f, e
			}}
			d.ops = everydayFS{filesystem: hook, syncDir: func() error {
				syncs++
				if fault == "second sync" && syncs == 2 {
					fired = true
					return syscall.EIO
				}
				return base.SyncDirectory()
			}}
			r, e := d.PublishSave(p, id)
			var f *Failure
			if e == nil || !fired || !errors.As(e, &f) || !f.DestinationMayExist || r.Document != nil {
				t.Fatalf("false success: %#v %v", r, e)
			}
			content(t, filepath.Join(path, "A.WP"), edit)
			content(t, filepath.Join(path, "A.BK!"), a)
		})
	}
}
func TestEverydayCloseWaitsForStartedTransaction(t *testing.T) {
	d, path := everydayDir(t)
	a := everydayData(t)
	id := PublicationID{1, 1}
	p, e := d.PrepareNewSave(observeEveryday(t, d, "A.WP"), a, NoOverwrite, OriginalBackupOff, id)
	must(t, e)
	base := d.ops
	entered := make(chan struct{})
	resume := make(chan struct{})
	var once sync.Once
	d.ops = hookFS{filesystem: base, open: func(n string, flags int, m fs.FileMode) (file, error) {
		if flags&os.O_CREATE != 0 {
			once.Do(func() { close(entered); <-resume })
		}
		return base.OpenFile(n, flags, m)
	}}
	saved := make(chan error, 1)
	closed := make(chan error, 1)
	go func() { _, e := d.PublishNewSave(p, id); saved <- e }()
	<-entered
	if p.Cancel() {
		t.Fatal("cancel reported success after operation began")
	}
	go func() { closed <- d.Close() }()
	select {
	case e := <-closed:
		t.Fatalf("close interrupted transaction %v", e)
	case <-time.After(15 * time.Millisecond):
	}
	close(resume)
	must(t, <-saved)
	must(t, <-closed)
	content(t, filepath.Join(path, "A.WP"), a)
	if _, e = d.PublishNewSave(p, id); e == nil {
		t.Fatal("closed capability published")
	}
}
func TestEverydayWildcardProjection(t *testing.T) {
	for _, tc := range []struct {
		p           string
		names, want []string
	}{{"*.*", []string{"A", "A.WP", "B.TXT"}, []string{"A", "A.WP", "B.TXT"}}, {"A?.WP", []string{"A.WP", "AB.WP", "ABC.WP"}, []string{"A.WP", "AB.WP"}}, {"A", []string{"A", "A.WP"}, []string{"A"}}} {
		m, e := dosPattern(tc.p)
		must(t, e)
		got := []string{}
		for _, n := range tc.names {
			if m(n) {
				got = append(got, n)
			}
		}
		if !reflect.DeepEqual(got, tc.want) {
			t.Fatalf("%s %v", tc.p, got)
		}
	}
}

// Ensure production uses the filesystem's atomic exchange/no-replace primitives,
// rather than replacing backup contents in place through a writable descriptor.
func TestEverydayExchangeFlags(t *testing.T) {
	d, path := everydayDir(t)
	a := everydayData(t)
	putEveryday(t, path, "A.WP", a)
	putEveryday(t, path, "A.BK!", a)
	base := d.ops
	var flags []uint
	d.ops = everydayFS{filesystem: base, rename: func(a, b string, f uint) error { flags = append(flags, f); return base.Rename(a, b, f) }}
	saveEveryday(t, d, readEveryday(t, d, "A.WP"), "A.WP", nativeEdit(a, "edit"), OriginalBackupOn, 1)
	if !reflect.DeepEqual(flags, []uint{unix.RENAME_EXCHANGE, unix.RENAME_EXCHANGE}) {
		t.Fatal(flags)
	}
}

func TestEverydayNativeSupplementaryFiles(t *testing.T) {
	for _, name := range []string{"WP{WP}US.SUP", "SPELLADD"} {
		t.Run(name, func(t *testing.T) {
			data, e := os.ReadFile(filepath.Join("../../docs/research/everyday-contract-2026-11-05/spelling/proof/supplementary", name))
			must(t, e)
			d, path := everydayDir(t)
			first := saveEveryday(t, d, nil, name, data, OriginalBackupOff, 1)
			edit := nativeEdit(data, "additional\n")
			saveEveryday(t, d, first.Document, name, edit, OriginalBackupOff, 2)
			content(t, filepath.Join(path, name), edit)
		})
	}
}
func TestEverydayFailureWithoutPriorBackupAndNewTarget(t *testing.T) {
	for _, exists := range []bool{false, true} {
		for _, setting := range []OriginalBackup{OriginalBackupOff, OriginalBackupOn} {
			t.Run(fmt.Sprintf("exists=%v/backup=%d", exists, setting), func(t *testing.T) {
				d, path := everydayDir(t)
				data := everydayData(t)
				if exists {
					putEveryday(t, path, "A.WP", data)
				}
				id := PublicationID{1, 1}
				p, e := d.PrepareNewSave(observeEveryday(t, d, "A.WP"), nativeEdit(data, "edited"), AllowOverwrite, setting, id)
				must(t, e)
				base := d.ops
				calls := 0
				d.ops = everydayFS{filesystem: base, syncDir: func() error {
					calls++
					if calls == 1 {
						return syscall.EIO
					}
					return base.SyncDirectory()
				}}
				if _, e = d.PublishNewSave(p, id); e == nil {
					t.Fatal("durability failure reported success")
				}
				if exists {
					content(t, filepath.Join(path, "A.WP"), data)
				} else {
					absent(t, filepath.Join(path, "A.WP"))
				}
				absent(t, filepath.Join(path, "A.BK!"))
				if len(candidateNames(t, path)) != 0 {
					t.Fatal("rollback residue")
				}
			})
		}
	}
}
func TestEverydayDirectoryResourceBounds(t *testing.T) {
	path := t.TempDir()
	w, e := OpenWorkspace(path)
	must(t, e)
	defer w.Close()
	root, e := w.Root()
	must(t, e)
	for i := 0; i < MaxWorkspaceDirectories; i++ {
		name := fmt.Sprintf("D%06d", i)
		must(t, os.Mkdir(filepath.Join(path, name), 0700))
		_, e = root.Navigate(name)
		if i < MaxWorkspaceDirectories-1 {
			must(t, e)
		} else if e == nil {
			t.Fatal("unbounded retained handles")
		}
	}
	rootEntries := len(w.state.nodes)
	if rootEntries != MaxWorkspaceDirectories {
		t.Fatal(rootEntries)
	}
	again, e := root.Navigate("D000000")
	must(t, e)
	if again == nil || len(w.state.nodes) != rootEntries {
		t.Fatal("cached acquisition consumes budget")
	}
	// A fresh workspace verifies the independent parent-depth boundary through
	// both direct navigation and selection-based Look/Enter.
	path2 := t.TempDir()
	w2, e := OpenWorkspace(path2)
	must(t, e)
	defer w2.Close()
	at, e := w2.Root()
	must(t, e)
	physical := path2
	for i := 0; i <= MaxWorkspaceDepth; i++ {
		physical = filepath.Join(physical, "D")
		must(t, os.Mkdir(physical, 0700))
		l, e := at.List("")
		must(t, e)
		s, e := l.Select(l.Find(`\D`))
		must(t, e)
		next, e := s.Enter()
		if i < MaxWorkspaceDepth {
			must(t, e)
			at = next
		} else if e == nil {
			t.Fatal("selection escaped depth bound")
		}
	}
}
func TestEverydayEnumerationLimit(t *testing.T) {
	path := t.TempDir()
	for i := 0; i <= MaxDirectoryEntries; i++ {
		f, e := os.Create(filepath.Join(path, fmt.Sprintf("F%07d", i)))
		must(t, e)
		must(t, f.Close())
	}
	w, e := OpenWorkspace(path)
	must(t, e)
	defer w.Close()
	d, e := w.Root()
	must(t, e)
	if _, e = d.List(""); e == nil {
		t.Fatal("partial list/count reported as complete")
	}
}
func TestEverydayLateSymlinkAndPermissionRefusal(t *testing.T) {
	for _, fault := range []string{"destination symlink", "backup symlink", "denied candidate"} {
		t.Run(fault, func(t *testing.T) {
			d, path := everydayDir(t)
			data := everydayData(t)
			putEveryday(t, path, "A.WP", data)
			putEveryday(t, path, "OTHER.WP", nativeEdit(data, "other"))
			id := PublicationID{1, 1}
			p, e := d.PrepareSave(readEveryday(t, d, "A.WP"), observeEveryday(t, d, "A.WP"), nativeEdit(data, "edited"), AllowOverwrite, OriginalBackupOn, id)
			must(t, e)
			if fault == "destination symlink" {
				must(t, os.Remove(filepath.Join(path, "A.WP")))
				must(t, os.Symlink("OTHER.WP", filepath.Join(path, "A.WP")))
			}
			if fault == "backup symlink" {
				must(t, os.Symlink("OTHER.WP", filepath.Join(path, "A.BK!")))
			}
			if fault == "denied candidate" {
				base := d.ops
				d.ops = hookFS{filesystem: base, open: func(n string, f int, m fs.FileMode) (file, error) {
					if f&os.O_CREATE != 0 {
						return nil, syscall.EACCES
					}
					return base.OpenFile(n, f, m)
				}}
			}
			if _, e = d.PublishSave(p, id); e == nil {
				t.Fatal("unsafe save accepted")
			}
			content(t, filepath.Join(path, "OTHER.WP"), nativeEdit(data, "other"))
			if fault != "destination symlink" {
				content(t, filepath.Join(path, "A.WP"), data)
			}
		})
	}
}

func TestEverydayConcurrentPreparedSavesSerializeSharedCapability(t *testing.T) {
	d, path := everydayDir(t)
	data := everydayData(t)
	putEveryday(t, path, "A.WP", data)
	src := readEveryday(t, d, "A.WP")
	dst := observeEveryday(t, d, "A.WP")
	p1, e := d.PrepareSave(src, dst, nativeEdit(data, "one"), AllowOverwrite, OriginalBackupOn, PublicationID{1, 1})
	must(t, e)
	p2, e := d.PrepareSave(src, dst, nativeEdit(data, "two"), AllowOverwrite, OriginalBackupOn, PublicationID{2, 2})
	must(t, e)
	alias := *d
	start := make(chan struct{})
	type answer struct {
		r SaveResult
		e error
	}
	done := make(chan answer, 2)
	go func() { <-start; r, e := d.PublishSave(p1, PublicationID{1, 1}); done <- answer{r, e} }()
	go func() { <-start; r, e := alias.PublishSave(p2, PublicationID{2, 2}); done <- answer{r, e} }()
	close(start)
	a, b := <-done, <-done
	if (a.e == nil) == (b.e == nil) {
		t.Fatalf("exactly one request must win: %v %v", a.e, b.e)
	}
	winner := a
	if winner.e != nil {
		winner = b
	}
	content(t, filepath.Join(path, "A.WP"), winner.r.Document.Export())
	content(t, filepath.Join(path, "A.BK!"), data)
	if len(candidateNames(t, path)) != 0 {
		t.Fatal("concurrent residue")
	}
}

func TestEverydayMatchesOriginalCompleteBackupSnapshots(t *testing.T) {
	d, path := everydayDir(t)
	reference := "../../docs/research/everyday-contract-2026-11-05/backup/enabled/exports"
	load := func(name string) []byte { b, e := os.ReadFile(filepath.Join(reference, name)); must(t, e); return b }
	r := saveEveryday(t, d, nil, "BASE.WP", load("STAGE1.WP"), OriginalBackupOn, 1)
	absent(t, filepath.Join(path, "BASE.BK!"))
	r = saveEveryday(t, d, r.Document, "BASE.WP", load("STAGE2.WP"), OriginalBackupOn, 2)
	content(t, filepath.Join(path, "BASE.BK!"), load("BACK2.WP"))
	r = saveEveryday(t, d, r.Document, "BASE.WP", load("STAGE3.WP"), OriginalBackupOn, 3)
	content(t, filepath.Join(path, "BASE.BK!"), load("BACK3.WP"))
	saveEveryday(t, d, r.Document, "BASE.WP", load("BASE.WP"), OriginalBackupOff, 4)
	content(t, filepath.Join(path, "BASE.WP"), load("BASE.WP"))
	absent(t, filepath.Join(path, "BASE.BK!"))
}

func TestEverydayLocalFlatLowercaseAndLateAlias(t *testing.T) {
	d, path := everydayDir(t)
	data := everydayData(t)
	r := saveEveryday(t, d, nil, "a.wp", data, OriginalBackupOn, 1)
	content(t, filepath.Join(path, "a.wp"), data)
	putEveryday(t, path, "a.bk!", data)
	saveEveryday(t, d, r.Document, "a.wp", nativeEdit(data, "edit"), OriginalBackupOff, 2)
	absent(t, filepath.Join(path, "a.bk!"))
	id := PublicationID{3, 3}
	p, e := d.PrepareNewSave(observeEveryday(t, d, "B.WP"), data, NoOverwrite, OriginalBackupOff, id)
	must(t, e)
	base := d.ops
	d.ops = hookFS{filesystem: base, link: func(a, b string) error {
		e := base.Link(a, b)
		if e == nil {
			putEveryday(t, path, "b.wp", data)
		}
		return e
	}}
	_, e = d.PublishNewSave(p, id)
	var f *Failure
	if !errors.As(e, &f) || f.Kind != PublicationUncertain {
		t.Fatalf("late alias reported success: %v", e)
	}
	content(t, filepath.Join(path, "B.WP"), data)
	content(t, filepath.Join(path, "b.wp"), data)
}
