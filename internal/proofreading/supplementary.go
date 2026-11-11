package proofreading

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"strings"

	"github.com/lynncoleart/wordling/internal/storage"
)

const (
	DefaultSupplementaryName = "WP{WP}US.SUP"
	MaxSupplementaryWords    = 8192
	supplementaryPrefixBytes = 66
	maxSupplementaryBytes    = supplementaryPrefixBytes + MaxSupplementaryWords*(MaxWordBytes+1)
)

// WP78 recorded this uncompressed prefix in both the default and custom
// dictionary. An unknown prefix might contain compressed words. Admit only
// this evidenced uncompressed family, with any qualified lexical body.
func supplementaryPrefix() [supplementaryPrefixBytes]byte {
	return [supplementaryPrefixBytes]byte{
		0xff, 'W', 'P', 'C', supplementaryPrefixBytes, 0, 0, 0,
		1, 0x0a, 0, 1, 0, 0, 0, 0,
		0xfb, 0xff, 5, 0, 0x32,
	}
}

var ErrUnsupportedSupplementary = errors.New("unsupported or malformed native supplementary dictionary")

// Supplementary is an immutable observation of a dictionary in one workspace
// directory. Reopen after external changes instead of reusing a stale snapshot.
type Supplementary struct {
	workspace   *storage.Workspace
	directory   *storage.WorkspaceDirectory
	destination *storage.Destination
	source      *storage.Document
	words       map[string]struct{}
}

// OpenSupplementary selects the named native dictionary. The empty name
// selects the default. Missing files are valid observations and remain absent
// until Add or Create succeeds.
func OpenSupplementary(ctx context.Context, workspace *storage.Workspace, directory *storage.WorkspaceDirectory, name string) (*Supplementary, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	if !workspace.OwnsDirectory(directory) {
		return nil, errors.New("supplementary dictionary needs a live workspace directory")
	}
	if name == "" {
		name = DefaultSupplementaryName
	}
	dirCopy, workspaceCopy := *directory, *workspace
	target, err := dirCopy.Observe(name)
	if err != nil {
		return nil, fmt.Errorf("observe supplementary dictionary: %w", err)
	}
	result := &Supplementary{
		workspace: &workspaceCopy, directory: &dirCopy, destination: target,
	}
	if target.Exists() {
		stamp, _ := target.Identity()
		if stamp.Size > maxSupplementaryBytes {
			return nil, fmt.Errorf("%w: file exceeds limit", ErrUnsupportedSupplementary)
		}
		source, err := dirCopy.Directory().Read(target.Name())
		if err != nil {
			return nil, fmt.Errorf("read supplementary dictionary: %w", err)
		}
		if !matchesDestination(source, target) {
			return nil, &storage.Failure{Kind: storage.DestinationChanged, Stage: "open supplementary dictionary", Name: target.Name()}
		}
		result.words, err = admitSupplementary(source.Export())
		if err != nil {
			return nil, err
		}
		result.source = source
	}
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	return result, nil
}

func matchesDestination(source *storage.Document, target *storage.Destination) bool {
	observed, exists := target.Identity()
	if !exists || source.Name() != target.Name() || source.DirectoryID() != target.DirectoryID() {
		return false
	}
	actual := source.Identity()
	return observed.ID == actual.ID && observed.Size == actual.Size && observed.Mode == actual.Mode &&
		observed.Modified.Equal(actual.Modified) && observed.Changed.Equal(actual.Changed)
}

func admitSupplementary(data []byte) (map[string]struct{}, error) {
	prefix := supplementaryPrefix()
	if len(data) < len(prefix) || len(data) > maxSupplementaryBytes ||
		!bytes.Equal(data[:len(prefix)], prefix[:]) {
		return nil, fmt.Errorf("%w: unrecognized uncompressed prefix or size", ErrUnsupportedSupplementary)
	}
	words := make(map[string]struct{})
	records := 0
	for body := string(data[len(prefix):]); body != ""; {
		var word string
		var ended bool
		word, body, ended = strings.Cut(body, "\n")
		records++
		if !ended || records > MaxSupplementaryWords || !validWord(word, MaxWordBytes) {
			return nil, fmt.Errorf("%w: expected bounded HRt-terminated words", ErrUnsupportedSupplementary)
		}
		words[strings.ToLower(word)] = struct{}{}
	}
	return words, nil
}

// Name returns the selected filename in the filesystem's actual spelling.
func (s *Supplementary) Name() string {
	if s == nil || s.destination == nil {
		return ""
	}
	return s.destination.Name()
}

// Exists reports whether the observed selection had a native file.
func (s *Supplementary) Exists() bool { return s != nil && s.source != nil }

// Accepts matches supplementary words without ASCII case distinctions.
func (s *Supplementary) Accepts(word string) (bool, error) {
	if s == nil || s.destination == nil {
		return false, errors.New("supplementary dictionary is unavailable")
	}
	if !validWord(word, MaxWordBytes) {
		return false, ErrUnsupportedWord
	}
	_, ok := s.words[strings.ToLower(word)]
	return ok, nil
}

// Create publishes an empty native dictionary. Existing selections are
// refused so this operation cannot truncate a dictionary.
func (s *Supplementary) Create(ctx context.Context, id storage.PublicationID) (*Supplementary, error) {
	if err := s.checkOperation(ctx, id); err != nil {
		return nil, err
	}
	if s.Exists() {
		return nil, &storage.Failure{Kind: storage.OverwriteRequired, Stage: "create supplementary dictionary", Name: s.Name()}
	}
	prefix := supplementaryPrefix()
	return s.publish(ctx, prefix[:], id)
}

// Add appends the exact word spelling using checked native publication. A
// case-folded duplicate is a no-op after checking the snapshot remains current.
func (s *Supplementary) Add(ctx context.Context, word string, id storage.PublicationID) (*Supplementary, error) {
	if err := s.checkOperation(ctx, id); err != nil {
		return nil, err
	}
	duplicate, err := s.Accepts(word)
	if err != nil {
		return nil, err
	}
	if duplicate {
		fresh, err := OpenSupplementary(ctx, s.workspace, s.directory, s.Name())
		if err != nil {
			return nil, err
		}
		if !fresh.Exists() || fresh.source.Identity() != s.source.Identity() {
			return nil, &storage.Failure{Kind: storage.DestinationChanged, Stage: "duplicate supplementary word", Name: s.Name()}
		}
		return fresh, nil
	}
	prefix := supplementaryPrefix()
	data := prefix[:]
	if s.Exists() {
		data = s.source.Export()
	}
	data = append(data, word...)
	data = append(data, '\n')
	return s.publish(ctx, data, id)
}

func (s *Supplementary) checkOperation(ctx context.Context, id storage.PublicationID) error {
	if err := ctx.Err(); err != nil {
		return err
	}
	if s == nil || s.destination == nil || !s.workspace.OwnsDirectory(s.directory) {
		return errors.New("supplementary dictionary needs a live workspace snapshot")
	}
	if id.Operation == 0 || id.Revision == 0 {
		return errors.New("supplementary dictionary needs a publication identity")
	}
	return nil
}

func (s *Supplementary) publish(ctx context.Context, data []byte, id storage.PublicationID) (*Supplementary, error) {
	words, err := admitSupplementary(data)
	if err != nil {
		return nil, err
	}
	d := s.directory.Directory()
	var result storage.SaveResult
	if s.Exists() {
		prepared, err := d.PrepareSave(s.source, s.destination, data, storage.AllowOverwrite, storage.OriginalBackupPreserve, id)
		if err != nil {
			return nil, err
		}
		if err = ctx.Err(); err != nil {
			prepared.Cancel()
			return nil, err
		}
		result, err = d.PublishSave(prepared, id)
		if err != nil {
			return nil, err
		}
	} else {
		prepared, err := d.PrepareNewSave(s.destination, data, storage.NoOverwrite, storage.OriginalBackupPreserve, id)
		if err != nil {
			return nil, err
		}
		if err = ctx.Err(); err != nil {
			prepared.Cancel()
			return nil, err
		}
		result, err = d.PublishNewSave(prepared, id)
		if err != nil {
			return nil, err
		}
	}
	target, err := s.directory.Observe(s.Name())
	if err != nil || result.Document == nil || result.ID != id || !matchesDestination(result.Document, target) {
		return nil, &storage.Failure{
			Kind: storage.PublicationUncertain, Stage: "refresh supplementary observation", Name: s.Name(),
			DestinationMayExist: true, Cause: err,
		}
	}
	return &Supplementary{
		workspace: s.workspace, directory: s.directory, destination: target,
		source: result.Document, words: words,
	}, nil
}
