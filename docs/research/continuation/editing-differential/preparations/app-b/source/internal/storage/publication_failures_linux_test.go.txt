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
	"testing"
)

func editedCase(t *testing.T) (*Directory, *Publication, string, []byte, []byte) {
	t.Helper()
	d, doc, target, path, original := storageCase(t)
	payload := append(bytes.Clone(original), 'X') // synthetic framing-valid IO fixture
	p, err := d.PreparePublication(doc, target, payload, PublicationID{Operation: 9, Revision: 2})
	must(t, err)
	return d, p, path, original, payload
}

func TestEditedPublicationFailureBoundaries(t *testing.T) {
	for _, which := range []string{"create", "short write", "write", "close", "link", "link after side effect", "cleanup", "source mutation", "source replacement", "late destination", "candidate substitution", "foreign after link", "foreign after cleanup"} {
		t.Run(which, func(t *testing.T) {
			d, p, path, original, payload := editedCase(t)
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
			out, err := d.Publish(p, p.ID())
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
				content(t, filepath.Join(path, "source"), original)
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

func TestEditedPublicationUsesPinnedParent(t *testing.T) {
	d, p, path, original, payload := editedCase(t)
	moved := path + "-moved"
	t.Cleanup(func() { os.RemoveAll(moved) })
	base := d.ops
	d.ops = hookFS{filesystem: base, open: func(n string, flags int, mode fs.FileMode) (file, error) {
		f, err := base.OpenFile(n, flags, mode)
		if err != nil || flags&os.O_CREATE == 0 {
			return f, err
		}
		return hookFile{file: f, write: func(b []byte) (int, error) {
			must(t, os.Rename(path, moved))
			must(t, os.Mkdir(path, 0700))
			must(t, os.WriteFile(filepath.Join(path, "destination"), []byte("foreign path"), 0600))
			return f.Write(b)
		}}, nil
	}}
	out, err := d.Publish(p, p.ID())
	must(t, err)
	if out.State != Published {
		t.Fatal("pinned publication failed")
	}
	content(t, filepath.Join(moved, "source"), original)
	content(t, filepath.Join(moved, "destination"), payload)
	content(t, filepath.Join(path, "destination"), []byte("foreign path"))
}

func TestEditedPublicationAndDirectoryClose(t *testing.T) {
	for range 16 {
		d, p, path, original, payload := editedCase(t)
		start := make(chan struct{})
		var out Outcome
		var publishErr error
		var wg sync.WaitGroup
		wg.Go(func() { <-start; out, publishErr = d.Publish(p, p.ID()) })
		wg.Go(func() { <-start; d.Close() })
		close(start)
		wg.Wait()
		content(t, filepath.Join(path, "source"), original)
		if publishErr == nil {
			if out.State != Published {
				t.Fatal("successful closed-race outcome missing")
			}
			content(t, filepath.Join(path, "destination"), payload)
		} else {
			var failure *Failure
			if out.State != "" || !errors.As(publishErr, &failure) {
				t.Fatalf("close race lost typed failure: %v", publishErr)
			}
		}
		// Close may prevent safe candidate cleanup; any known residue is reported.
		if names := candidateNames(t, path); len(names) != 0 {
			var failure *Failure
			if !errors.As(publishErr, &failure) || failure.Candidate == "" || !strings.HasPrefix(failure.Candidate, candidatePrefix) {
				t.Fatal("close race hid candidate residue")
			}
		}
	}
}
