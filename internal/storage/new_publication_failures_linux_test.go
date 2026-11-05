package storage

import (
	"bytes"
	"errors"
	"github.com/lynncoleart/wordling/internal/wp51"
	"io"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func newPublicationCase(t *testing.T) (*Directory, *NewPublication, string, []byte, []byte) {
	t.Helper()
	input, err := os.ReadFile("../../docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5")
	must(t, err)
	path := t.TempDir()
	d, err := OpenDirectory(path)
	must(t, err)
	saved := *d
	t.Cleanup(func() { saved.Close() })
	target, err := d.Observe("destination")
	must(t, err)
	payload := append(bytes.Clone(input), 'X')
	p, err := d.PrepareNewPublication(target, payload, PublicationID{Operation: 90, Revision: 2})
	must(t, err)
	return d, p, path, input, payload
}
func TestNewPublicationFailureBoundaries(t *testing.T) {
	for _, which := range []string{"create", "short write", "write", "close", "link", "link after side effect", "cleanup", "late destination", "candidate substitution", "foreign after link", "foreign after cleanup"} {
		t.Run(which, func(t *testing.T) {
			d, p, path, _, payload := newPublicationCase(t)
			base := d.ops
			injected := errors.New("injected " + which)
			foreign := []byte("foreign entry")
			changedSource := false
			d.ops = hookFS{filesystem: base,
				open: func(n string, flags int, mode fs.FileMode) (file, error) {
					if flags&os.O_CREATE != 0 && which == "create" {
						return nil, injected
					}
					f, err := base.OpenFile(n, flags, mode)
					if err != nil || flags&os.O_CREATE == 0 {
						return f, err
					}
					return hookFile{file: f, write: func(b []byte) (int, error) {
						switch which {
						case "short write":
							return f.Write(b[:len(b)/2])
						case "write":
							n, _ := f.Write(b[:len(b)/2])
							return n, injected
						case "source mutation":
							must(t, os.WriteFile(filepath.Join(path, "source"), payload, 0600))
							changedSource = true
						case "source replacement":
							must(t, os.WriteFile(filepath.Join(path, "replacement"), payload, 0600))
							must(t, os.Rename(filepath.Join(path, "replacement"), filepath.Join(path, "source")))
							changedSource = true
						case "late destination":
							must(t, os.WriteFile(filepath.Join(path, "destination"), foreign, 0600))
						}
						return f.Write(b)
					}, close: func() error {
						err := f.Close()
						if which == "close" {
							return errors.Join(err, injected)
						}
						return err
					}}, nil
				},
				link: func(a, b string) error {
					if which == "link" {
						return injected
					}
					if which == "candidate substitution" {
						must(t, os.Rename(filepath.Join(path, a), filepath.Join(path, "retained-candidate")))
						must(t, os.WriteFile(filepath.Join(path, a), foreign, 0600))
					}
					if err := base.Link(a, b); err != nil {
						return err
					}
					if which == "foreign after link" {
						must(t, os.Remove(filepath.Join(path, b)))
						must(t, os.WriteFile(filepath.Join(path, b), foreign, 0600))
					}
					if which == "link after side effect" {
						return injected
					}
					return nil
				},
				remove: func(n string) error {
					if which == "cleanup" {
						return injected
					}
					if err := base.Remove(n); err != nil {
						return err
					}
					if which == "foreign after cleanup" {
						must(t, os.Remove(filepath.Join(path, "destination")))
						must(t, os.WriteFile(filepath.Join(path, "destination"), foreign, 0600))
					}
					return nil
				}}
			out, err := d.PublishNew(p, p.ID())
			kind := CandidateFailed
			switch which {
			case "link", "link after side effect":
				kind = PublicationFailed
			case "cleanup":
				kind = CleanupFailed
			case "source mutation", "source replacement":
				kind = StaleSource
			case "late destination":
				kind = DestinationChanged
			case "candidate substitution", "foreign after link", "foreign after cleanup":
				kind = PublicationUncertain
			}
			failure := refusal(t, out, err, kind)
			if which == "short write" && !errors.Is(err, io.ErrShortWrite) {
				t.Fatal("short-write cause lost")
			}
			if which == "create" || which == "write" || which == "close" || which == "link" || which == "link after side effect" || which == "cleanup" {
				if !errors.Is(err, injected) {
					t.Fatal("IO cause lost")
				}
			}
			if changedSource {
				content(t, filepath.Join(path, "source"), payload)
			} else {
				absent(t, filepath.Join(path, "source"))
			}
			switch which {
			case "cleanup", "link after side effect":
				content(t, filepath.Join(path, "destination"), payload)
			case "late destination", "candidate substitution", "foreign after link", "foreign after cleanup":
				content(t, filepath.Join(path, "destination"), foreign)
			default:
				absent(t, filepath.Join(path, "destination"))
			}
			mayExist := kind == PublicationUncertain || kind == PublicationFailed || which == "cleanup"
			if failure.DestinationMayExist != mayExist {
				t.Fatalf("uncertain side effect hidden: %+v", failure)
			}
			leftovers := candidateNames(t, path)
			if which == "cleanup" || which == "candidate substitution" {
				if len(leftovers) != 1 || failure.Candidate == "" {
					t.Fatal("candidate residue hidden")
				}
			} else if len(leftovers) != 0 {
				t.Fatal("ordinary failed publication leaked candidate")
			}
		})
	}
}

func TestNewPublicationVerificationAndPinFailures(t *testing.T) {
	for _, which := range []string{"writer-stat", "pin-open", "pin-stat", "pin-close", "verify-open", "verify-read", "verify-close"} {
		t.Run(which, func(t *testing.T) {
			d, p, root, _, payload := newPublicationCase(t)
			base := d.ops
			injected := errors.New("injected " + which)
			candidateReads := 0
			d.ops = hookFS{filesystem: base, open: func(name string, flags int, mode fs.FileMode) (file, error) {
				candidate := strings.HasPrefix(name, candidatePrefix)
				if candidate && flags&os.O_CREATE == 0 {
					candidateReads++
					if (which == "pin-open" && candidateReads == 1) || (which == "verify-open" && candidateReads == 2) {
						return nil, injected
					}
				}
				f, e := base.OpenFile(name, flags, mode)
				if e != nil {
					return f, e
				}
				if candidate && flags&os.O_CREATE != 0 && which == "writer-stat" {
					return hookFile{file: f, stat: func() (os.FileInfo, error) { return nil, injected }}, nil
				}
				if candidate && candidateReads == 1 && flags&os.O_CREATE == 0 {
					if which == "pin-stat" {
						return hookFile{file: f, stat: func() (os.FileInfo, error) { return nil, injected }}, nil
					}
					if which == "pin-close" {
						return hookFile{file: f, close: func() error { return errors.Join(f.Close(), injected) }}, nil
					}
				}
				if candidate && candidateReads == 2 && flags&os.O_CREATE == 0 {
					if which == "verify-read" {
						return hookFile{file: f, read: func([]byte) (int, error) { return 0, injected }}, nil
					}
					if which == "verify-close" {
						return hookFile{file: f, close: func() error { return errors.Join(f.Close(), injected) }}, nil
					}
				}
				return f, nil
			}}
			out, err := d.PublishNew(p, p.ID())
			want := CandidateFailed
			if which == "pin-close" {
				want = CleanupFailed
			}
			f := refusal(t, out, err, want)
			if !errors.Is(err, injected) {
				t.Fatal("fault cause lost", err)
			}
			absent(t, filepath.Join(root, "source"))
			if which == "pin-close" {
				content(t, filepath.Join(root, "destination"), payload)
				if !f.DestinationMayExist {
					t.Fatal("pin-close uncertainty lost")
				}
			} else {
				absent(t, filepath.Join(root, "destination"))
			}
			if which == "writer-stat" {
				if f.Candidate == "" || len(candidateNames(t, root)) != 1 {
					t.Fatal("unknown candidate inode residue not reported")
				}
			} else if len(candidateNames(t, root)) != 0 {
				t.Fatal("unexpected candidate residue")
			}
		})
	}
}
func TestInvalidReceiverRefusesBeforeAnyIO(t *testing.T) {
	for _, which := range []string{"zero", "nil", "rebound", "independent-same-root", "closed-copy"} {
		t.Run(which, func(t *testing.T) {
			d, doc, target, root, raw := storageCase(t)
			id := PublicationID{Operation: 81, Revision: 1}
			loaded, err := d.PreparePublication(doc, target, raw, id)
			must(t, err)
			fresh, err := d.PrepareNewPublication(target, raw, id)
			must(t, err)
			original := *d
			other, err := OpenDirectory(t.TempDir())
			must(t, err)
			defer other.Close()
			savedOther := *other
			var calls int
			trap := func(cap *openedDirectory) {
				base := cap.ops
				cap.ops = hookFS{filesystem: base, open: func(string, int, fs.FileMode) (file, error) { calls++; return nil, errors.New("forbidden IO") }, lstat: func(string) (os.FileInfo, error) { calls++; return nil, errors.New("forbidden IO") }, link: func(string, string) error { calls++; return errors.New("forbidden IO") }, remove: func(string) error { calls++; return errors.New("forbidden IO") }}
			}
			trap(original.openedDirectory)
			trap(other.openedDirectory)
			receiver := d
			switch which {
			case "zero":
				*d = Directory{}
			case "nil":
				receiver = nil
			case "rebound":
				*d = *other
			case "independent-same-root":
				same, e := OpenDirectory(root)
				must(t, e)
				defer same.Close()
				if same.ID() != original.ID() {
					t.Fatal("need equal root identity")
				}
				trap(same.openedDirectory)
				*d = *same
			case "closed-copy":
				must(t, original.Close())
			}
			out, e := receiver.Publish(loaded, id)
			refusal(t, out, e, InvalidRequest)
			out, e = receiver.PublishNew(fresh, id)
			refusal(t, out, e, InvalidRequest)
			if calls != 0 {
				t.Fatal("invalid capability touched filesystem", calls)
			}
			// Close the original capability even if the public wrapper was rebound.
			original.Close()
			savedOther.Close()
		})
	}
}
func TestExplicitTransactionGuardCannotBeOmitted(t *testing.T) {
	d, doc, target, root, raw := storageCase(t)
	base := d.ops
	calls := 0
	d.ops = hookFS{filesystem: base, open: func(string, int, fs.FileMode) (file, error) { calls++; return nil, errors.New("must not create") }}
	for _, guard := range []sourceGuard{{}, {kind: 99}, {kind: guardLoaded}, {kind: guardNew, source: doc}} {
		out, e := d.openedDirectory.publish(guard, target, raw, doc.identity.SHA256)
		refusal(t, out, e, InvalidRequest)
	}
	if calls != 0 || len(candidateNames(t, root)) != 0 {
		t.Fatal("invalid guard reached transaction")
	}
}
func TestCloseReallyReleasesDesignatedCapabilities(t *testing.T) {
	d, _, _, _, _ := storageCase(t)
	original := *d
	other, err := OpenDirectory(t.TempDir())
	must(t, err)
	savedOther := *other
	*d = *other
	must(t, d.Close())
	if _, e := savedOther.dir.Stat(); !errors.Is(e, os.ErrClosed) {
		t.Fatal("rebound Close lost directory FD ownership", e)
	}
	if _, e := savedOther.root.Stat("."); !errors.Is(e, os.ErrClosed) {
		t.Fatal("rebound Close lost root ownership", e)
	}
	if _, e := original.dir.Stat(); e != nil {
		t.Fatal("rebound Close closed original FD", e)
	}
	must(t, original.Close())
	if _, e := original.dir.Stat(); !errors.Is(e, os.ErrClosed) {
		t.Fatal("original copy leaked descriptor", e)
	}
	if _, e := original.root.Stat("."); !errors.Is(e, os.ErrClosed) {
		t.Fatal("original copy leaked root", e)
	}
	if e := original.Close(); !errors.Is(e, os.ErrClosed) {
		t.Fatal("real repeat Close error lost", e)
	}
}
func TestNewPublicationSourceLessMaximumFrame(t *testing.T) {
	d, p, _, raw, _ := newPublicationCase(t)
	target, err := d.Observe("maximum")
	must(t, err)
	maximum := append(bytes.Clone(raw), bytes.Repeat([]byte{'X'}, wp51.MaxInputBytes-len(raw))...)
	request, err := d.PrepareNewPublication(target, maximum, p.ID())
	must(t, err)
	if request.Size() != wp51.MaxInputBytes {
		t.Fatal("native size cap changed")
	}
}

func TestLoadedGuardRetainsAllThreeObservationBoundaries(t *testing.T) {
	d, doc, target, _, raw := storageCase(t)
	base := d.ops
	sourceReads := 0
	d.ops = hookFS{filesystem: base, open: func(name string, flags int, mode fs.FileMode) (file, error) {
		if name == "source" && flags&os.O_CREATE == 0 {
			sourceReads++
		}
		return base.OpenFile(name, flags, mode)
	}}
	id := PublicationID{Operation: 95, Revision: 1}
	p, err := d.PreparePublication(doc, target, raw, id)
	must(t, err)
	if sourceReads != 1 {
		t.Fatal("prepare source observation missing", sourceReads)
	}
	out, err := d.Publish(p, id)
	must(t, err)
	if out.State != Published || sourceReads != 3 {
		t.Fatal("publish/pre-link source observations missing", out, sourceReads)
	}
}
func TestNewGuardNeverInventsLoadedSourceObservation(t *testing.T) {
	d, p, root, _, _ := newPublicationCase(t)
	base := d.ops
	d.ops = hookFS{filesystem: base, open: func(name string, flags int, mode fs.FileMode) (file, error) {
		if name == "source" {
			t.Fatal("source-less publication fabricated a loaded guard")
		}
		return base.OpenFile(name, flags, mode)
	}}
	out, err := d.PublishNew(p, p.ID())
	must(t, err)
	if out.State != Published {
		t.Fatal(out)
	}
	absent(t, filepath.Join(root, "source"))
}
