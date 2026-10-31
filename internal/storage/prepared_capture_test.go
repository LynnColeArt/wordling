package storage_test

import (
	"bytes"
	"errors"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"path/filepath"
	"testing"
)

func ownedDirectory(t *testing.T, root string) *storage.Directory {
	t.Helper()
	d, err := storage.OpenDirectory(root)
	if err != nil {
		t.Fatal(err)
	}
	saved := *d
	t.Cleanup(func() { saved.Close() })
	return d
}
func captureSetup(t *testing.T) (*storage.Directory, *storage.Document, string, []byte) {
	t.Helper()
	root := t.TempDir()
	raw := plain(t)
	if err := os.WriteFile(filepath.Join(root, "source"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	d := ownedDirectory(t, root)
	src, err := d.Read("source")
	if err != nil {
		t.Fatal(err)
	}
	return d, src, root, raw
}
func noCandidates(t *testing.T, root string) {
	t.Helper()
	entries, err := os.ReadDir(root)
	if err != nil {
		t.Fatal(err)
	}
	for _, e := range entries {
		if len(e.Name()) >= 20 && e.Name()[:20] == ".wordling-candidate-" {
			t.Fatal("candidate residue", root, e.Name())
		}
	}
}
func TestPreparedSourceCapturesAcceptedOriginal(t *testing.T) {
	for _, replacement := range []string{"zero", "same-root", "cross-root"} {
		for _, changed := range []bool{false, true} {
			t.Run(replacement+map[bool]string{false: "/unchanged", true: "/changed"}[changed], func(t *testing.T) {
				d, src, root, raw := captureSetup(t)
				otherRoot := root
				if replacement == "cross-root" {
					otherRoot = t.TempDir()
				}
				if err := os.WriteFile(filepath.Join(otherRoot, "other"), append(bytes.Clone(raw), 'Z'), 0600); err != nil {
					t.Fatal(err)
				}
				od := ownedDirectory(t, otherRoot)
				other, err := od.Read("other")
				if err != nil {
					t.Fatal(err)
				}
				target, _ := d.Observe("first")
				id := storage.PublicationID{Operation: 1, Revision: 1}
				p, err := d.PreparePublication(src, target, raw, id)
				if err != nil {
					t.Fatal(err)
				}
				if replacement == "zero" {
					*src = storage.Document{}
				} else {
					*src = *other
				}
				if changed {
					if err = os.WriteFile(filepath.Join(root, "source"), []byte("changed original"), 0600); err != nil {
						t.Fatal(err)
					}
				}
				out, err := d.Publish(p, id)
				got, readErr := os.ReadFile(filepath.Join(root, "first"))
				if changed {
					expect(t, err, storage.StaleSource)
					if !errors.Is(readErr, os.ErrNotExist) || out.State != "" {
						t.Fatal("changed captured source published", out, readErr)
					}
				} else if err != nil || out.Name != "first" || !bytes.Equal(got, raw) {
					t.Fatal("accepted source capture lost", out, err)
				}
				noCandidates(t, root)
			})
		}
	}
}
func TestPreparedTargetObservationCannotBeSubstituted(t *testing.T) {
	for _, newRequest := range []bool{false, true} {
		for _, replacement := range []string{"zero", "absent", "existing", "foreign"} {
			for _, late := range []bool{false, true} {
				t.Run(map[bool]string{false: "loaded/", true: "new/"}[newRequest]+replacement+map[bool]string{false: "/absent", true: "/late"}[late], func(t *testing.T) {
					d, src, root, raw := captureSetup(t)
					foreignRoot := t.TempDir()
					otherRoot := root
					if replacement == "foreign" {
						otherRoot = foreignRoot
					}
					sentinel := []byte("unrelated second")
					if replacement == "existing" {
						if err := os.WriteFile(filepath.Join(root, "second"), sentinel, 0600); err != nil {
							t.Fatal(err)
						}
					}
					otherDir := ownedDirectory(t, otherRoot)
					other, _ := otherDir.Observe("second")
					first, _ := d.Observe("first")
					id := storage.PublicationID{Operation: 2, Revision: 1}
					var publish func() (storage.Outcome, error)
					if newRequest {
						p, err := d.PrepareNewPublication(first, raw, id)
						if err != nil {
							t.Fatal(err)
						}
						publish = func() (storage.Outcome, error) { return d.PublishNew(p, id) }
					} else {
						p, err := d.PreparePublication(src, first, raw, id)
						if err != nil {
							t.Fatal(err)
						}
						publish = func() (storage.Outcome, error) { return d.Publish(p, id) }
					}
					if replacement == "zero" {
						*first = storage.Destination{}
					} else {
						*first = *other
					}
					if late {
						if err := os.WriteFile(filepath.Join(root, "first"), []byte("late first"), 0600); err != nil {
							t.Fatal(err)
						}
					}
					out, err := publish()
					got, readErr := os.ReadFile(filepath.Join(root, "first"))
					if late {
						expect(t, err, storage.DestinationChanged)
						if string(got) != "late first" {
							t.Fatal("late target overwritten")
						}
					} else if err != nil || out.Name != "first" || readErr != nil || !bytes.Equal(got, raw) {
						t.Fatal(out, err, readErr)
					}
					second, secondErr := os.ReadFile(filepath.Join(otherRoot, "second"))
					if replacement == "existing" {
						if secondErr != nil || !bytes.Equal(second, sentinel) {
							t.Fatal("existing second changed")
						}
					} else if !errors.Is(secondErr, os.ErrNotExist) {
						t.Fatal("substituted second touched", secondErr)
					}
					noCandidates(t, root)
					noCandidates(t, foreignRoot)
				})
			}
		}
	}
}
func TestPreparedOpenedCapabilityCannotBeRebound(t *testing.T) {
	for _, newRequest := range []bool{false, true} {
		for _, replacement := range []string{"zero", "other-root", "independent-same-root"} {
			t.Run(map[bool]string{false: "loaded/", true: "new/"}[newRequest]+replacement, func(t *testing.T) {
				root, foreign := t.TempDir(), t.TempDir()
				raw := plain(t)
				if err := os.WriteFile(filepath.Join(root, "source"), raw, 0600); err != nil {
					t.Fatal(err)
				}
				// Before fresh Read: avoid accidental ctime rejection hiding capability drift.
				if err := os.Link(filepath.Join(root, "source"), filepath.Join(foreign, "source")); err != nil {
					t.Fatal(err)
				}
				d := ownedDirectory(t, root)
				source, err := d.Read("source")
				if err != nil {
					t.Fatal(err)
				}
				target, _ := d.Observe("first")
				id := storage.PublicationID{Operation: 3, Revision: 1}
				var publish func() (storage.Outcome, error)
				if newRequest {
					p, e := d.PrepareNewPublication(target, raw, id)
					if e != nil {
						t.Fatal(e)
					}
					publish = func() (storage.Outcome, error) { return d.PublishNew(p, id) }
				} else {
					p, e := d.PreparePublication(source, target, raw, id)
					if e != nil {
						t.Fatal(e)
					}
					publish = func() (storage.Outcome, error) { return d.Publish(p, id) }
				}
				switch replacement {
				case "zero":
					*d = storage.Directory{}
				case "other-root":
					*d = *ownedDirectory(t, foreign)
				case "independent-same-root":
					other := ownedDirectory(t, root)
					if other.ID() != d.ID() {
						t.Fatal("need same physical root")
					}
					*d = *other
				}
				out, err := publish()
				expect(t, err, storage.InvalidRequest)
				if out.State != "" {
					t.Fatal(out)
				}
				for _, r := range []string{root, foreign} {
					if _, e := os.Stat(filepath.Join(r, "first")); !errors.Is(e, os.ErrNotExist) {
						t.Fatal("rebound capability touched output", r, e)
					}
					noCandidates(t, r)
				}
			})
		}
	}
}
func TestCapabilityCopyCloseAndRenamedRootLifetime(t *testing.T) {
	for _, newRequest := range []bool{false, true} {
		for _, which := range []string{"copy", "closed-copy", "rebound-close-other", "renamed-root"} {
			t.Run(map[bool]string{false: "loaded/", true: "new/"}[newRequest]+which, func(t *testing.T) {
				d, source, root, raw := captureSetup(t)
				copyDir := *d
				target, _ := d.Observe("first")
				id := storage.PublicationID{Operation: 4, Revision: 1}
				var publish func(*storage.Directory) (storage.Outcome, error)
				if newRequest {
					p, e := d.PrepareNewPublication(target, raw, id)
					if e != nil {
						t.Fatal(e)
					}
					publish = func(v *storage.Directory) (storage.Outcome, error) { return v.PublishNew(p, id) }
				} else {
					p, e := d.PreparePublication(source, target, raw, id)
					if e != nil {
						t.Fatal(e)
					}
					publish = func(v *storage.Directory) (storage.Outcome, error) { return v.Publish(p, id) }
				}
				outputRoot := root
				switch which {
				case "closed-copy":
					if e := copyDir.Close(); e != nil {
						t.Fatal(e)
					}
					if e := d.Close(); e == nil {
						t.Fatal("second Close must retain actual closed error")
					}
				case "rebound-close-other":
					other := ownedDirectory(t, t.TempDir())
					*d = *other
					if e := d.Close(); e != nil {
						t.Fatal(e)
					}
				case "renamed-root":
					outputRoot = root + "-moved"
					if e := os.Rename(root, outputRoot); e != nil {
						t.Fatal(e)
					}
					t.Cleanup(func() { os.RemoveAll(outputRoot) })
					if e := os.Mkdir(root, 0700); e != nil {
						t.Fatal(e)
					}
					if e := os.WriteFile(filepath.Join(root, "first"), []byte("foreign path"), 0600); e != nil {
						t.Fatal(e)
					}
				}
				out, err := publish(&copyDir)
				if which == "closed-copy" {
					expect(t, err, storage.InvalidRequest)
					if _, e := os.Stat(filepath.Join(root, "first")); !errors.Is(e, os.ErrNotExist) {
						t.Fatal("closed capability resurrected")
					}
				} else {
					if err != nil || out.State != storage.Published || out.DirectoryID != copyDir.ID() {
						t.Fatal(out, err)
					}
					got, e := os.ReadFile(filepath.Join(outputRoot, "first"))
					if e != nil || !bytes.Equal(got, raw) {
						t.Fatal(e)
					}
					if which == "renamed-root" {
						b, _ := os.ReadFile(filepath.Join(root, "first"))
						if string(b) != "foreign path" {
							t.Fatal("path authority escaped")
						}
					}
				}
			})
		}
	}
}
