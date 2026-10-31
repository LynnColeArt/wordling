// Package storage provides bounded no-edit native snapshots and local Linux
// publication. Existing-file replacement, semantic writes and durability are
// unsupported; see README.md for observation points and concurrency limits.
package storage

import (
	"bytes"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"os"
	"strings"
	"syscall"
	"time"

	"github.com/lynncoleart/wordling/internal/wp51"
)

type Kind string

const (
	InvalidRequest         Kind = "InvalidRequest"
	UnsafePath             Kind = "UnsafePath"
	ReadFailed             Kind = "ReadFailed"
	InputLimit             Kind = "InputLimit"
	NativeRefused          Kind = "NativeRefused"
	StaleSource            Kind = "StaleSource"
	DestinationChanged     Kind = "DestinationChanged"
	OverwriteRequired      Kind = "OverwriteRequired"
	UnsupportedReplacement Kind = "UnsupportedReplacement"
	CandidateFailed        Kind = "CandidateFailed"
	PublicationFailed      Kind = "PublicationFailed"
	PublicationUncertain   Kind = "PublicationUncertain"
	CleanupFailed          Kind = "CleanupFailed"
)

// Failure never reports complete success. DestinationMayExist requires the caller
// to inspect the destination; Candidate identifies any known cleanup residue.
type Failure struct {
	Kind                   Kind
	Stage, Name, Candidate string
	DestinationMayExist    bool
	Cause                  error
}

func (e *Failure) Error() string {
	return fmt.Sprintf("storage: %s during %s (%q): %v", e.Kind, e.Stage, e.Name, e.Cause)
}
func (e *Failure) Unwrap() error { return e.Cause }
func failure(kind Kind, stage, name string, cause error) error {
	return &Failure{Kind: kind, Stage: stage, Name: name, Cause: cause}
}

// FileID identifies an inode on the declared local Linux filesystem.
type FileID struct{ Device, Inode uint64 }

// Identity records a read observation, not a lock or future freshness guarantee.
// SHA256 is populated for document and successful publication snapshots.
type Identity struct {
	ID                FileID
	Size              int64
	Mode              fs.FileMode
	Modified, Changed time.Time
	SHA256            [32]byte
}

// Decision is explicit authorization for an existing destination. Authorization
// does not make actual replacement supported; only a same-file no-op can pass.
type Decision uint8

const (
	NoOverwrite Decision = iota
	AllowOverwrite
)

type State string

const (
	Published State = "Published"
	Unchanged State = "Unchanged"
)

type Outcome struct {
	State       State
	Name        string
	DirectoryID FileID
	Identity    Identity
}

// Directory binds operations to an opened directory handle, across path renames.
// Names are flat basenames. Close releases the handle; os.Root methods provide
// concurrency safety, but independent external writes are not transactions.
type Directory struct {
	root *os.Root
	dir  *os.File
	ops  filesystem
	id   FileID
}

// Document owns an accepted wp51 snapshot and its private source observation.
type Document struct {
	image    *wp51.Image
	origin   *Directory
	name     string
	identity Identity
}

func (d *Document) Export() []byte      { return d.image.Export() }
func (d *Document) Identity() Identity  { return d.identity }
func (d *Document) Name() string        { return d.name }
func (d *Document) DirectoryID() FileID { return d.origin.id }

// Destination is an observation bound to its directory; callers cannot fabricate
// the existence or file-identity fields. Its metadata is not an overwrite lock.
type Destination struct {
	directory *Directory
	name      string
	exists    bool
	identity  Identity
}

func (d *Destination) Exists() bool        { return d.exists }
func (d *Destination) Name() string        { return d.name }
func (d *Destination) DirectoryID() FileID { return d.directory.id }

// Identity returns the observed metadata identity, with no destination content
// hash claim. The bool is false for an observed absent destination.
func (d *Destination) Identity() (Identity, bool) { return d.identity, d.exists }

// file/filesystem keep fault injection at actual filesystem responsibility
// boundaries. Production always uses rooted os operations and real files.
type file interface {
	io.Reader
	io.Writer
	Stat() (os.FileInfo, error)
	Close() error
}
type filesystem interface {
	OpenFile(string, int, fs.FileMode) (file, error)
	Lstat(string) (os.FileInfo, error)
	Link(string, string) error
	Remove(string) error
}
type rooted struct {
	*os.Root
	dir *os.File
}

func (r rooted) OpenFile(name string, flags int, mode fs.FileMode) (file, error) {
	// Root.OpenFile follows in-root symlinks even with O_NOFOLLOW. Flat names let
	// Linux openat enforce final-component no-follow on the pinned directory FD.
	// RawConn.Control pins that FD against concurrent Close/reuse during openat.
	raw, err := r.dir.SyscallConn()
	if err != nil {
		return nil, err
	}
	opened := -1
	var openErr error
	if err = raw.Control(func(fd uintptr) {
		opened, openErr = syscall.Openat(int(fd), name, flags|syscall.O_CLOEXEC, uint32(mode))
	}); err != nil {
		return nil, err
	}
	if openErr != nil {
		return nil, openErr
	}
	return os.NewFile(uintptr(opened), name), nil
}

// OpenDirectory chooses the directory reached at open time. It does not certify
// an untrusted pathname's ownership or provenance; later operations are anchored.
func OpenDirectory(path string) (*Directory, error) {
	r, err := os.OpenRoot(path)
	if err != nil {
		return nil, failure(ReadFailed, "open directory", path, err)
	}
	info, err := r.Stat(".")
	if err != nil {
		r.Close()
		return nil, failure(ReadFailed, "directory identity", path, err)
	}
	id, err := identity(info)
	if err != nil {
		r.Close()
		return nil, failure(ReadFailed, "directory identity", path, err)
	}
	dir, err := r.Open(".")
	if err != nil {
		r.Close()
		return nil, failure(ReadFailed, "directory descriptor", path, err)
	}
	return &Directory{root: r, dir: dir, ops: rooted{Root: r, dir: dir}, id: id.ID}, nil
}
func (d *Directory) Close() error { return errors.Join(d.root.Close(), d.dir.Close()) }
func (d *Directory) ID() FileID   { return d.id }

// MaxNameBytes is a conservative local Linux basename policy, not a DOS rule.
const MaxNameBytes = 255
const candidatePrefix = ".wordling-candidate-"

func validName(name string) error {
	if len(name) > MaxNameBytes || name == "" || name == "." || name == ".." || strings.ContainsAny(name, "/\x00") || strings.HasPrefix(name, candidatePrefix) {
		return failure(UnsafePath, "name", name, errors.New("requires an unreserved flat basename"))
	}
	return nil
}
func identity(info os.FileInfo) (Identity, error) {
	stat, ok := info.Sys().(*syscall.Stat_t)
	if !ok {
		return Identity{}, errors.New("Linux file identity unavailable")
	}
	return Identity{ID: FileID{uint64(stat.Dev), uint64(stat.Ino)}, Size: info.Size(), Mode: info.Mode(), Modified: info.ModTime(), Changed: time.Unix(int64(stat.Ctim.Sec), int64(stat.Ctim.Nsec))}, nil
}
func sameStamp(a, b Identity) bool {
	return a.ID == b.ID && a.Size == b.Size && a.Mode == b.Mode && a.Modified.Equal(b.Modified) && a.Changed.Equal(b.Changed)
}
func sameSnapshot(a, b Identity) bool { return sameStamp(a, b) && a.SHA256 == b.SHA256 }

type snapshot struct {
	identity Identity
	data     []byte
}

func (d *Directory) readStable(name string) (result snapshot, err error) {
	f, openErr := d.ops.OpenFile(name, os.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_NONBLOCK, 0)
	if openErr != nil {
		kind := ReadFailed
		if errors.Is(openErr, syscall.ELOOP) {
			kind = UnsafePath
		}
		return result, failure(kind, "open", name, openErr)
	}
	defer func() {
		if closeErr := f.Close(); closeErr != nil {
			if err == nil {
				err = failure(ReadFailed, "read close", name, closeErr)
			} else {
				err = errors.Join(err, closeErr)
			}
		}
	}()
	info, statErr := f.Stat()
	if statErr != nil {
		return result, failure(ReadFailed, "read stat", name, statErr)
	}
	if !info.Mode().IsRegular() {
		return result, failure(UnsafePath, "read type", name, errors.New("only regular files supported"))
	}
	before, statErr := identity(info)
	if statErr != nil {
		return result, failure(ReadFailed, "read identity", name, statErr)
	}
	if before.Size > wp51.MaxInputBytes {
		return result, failure(InputLimit, "read size", name, errors.New("exceeds native input limit"))
	}
	data, readErr := io.ReadAll(io.LimitReader(f, wp51.MaxInputBytes+1))
	if readErr != nil {
		return result, failure(ReadFailed, "read", name, readErr)
	}
	if len(data) > wp51.MaxInputBytes {
		return result, failure(InputLimit, "bounded read", name, errors.New("exceeds native input limit"))
	}
	afterInfo, statErr := f.Stat()
	if statErr != nil {
		return result, failure(ReadFailed, "read final stat", name, statErr)
	}
	after, statErr := identity(afterInfo)
	if statErr != nil {
		return result, failure(ReadFailed, "read final identity", name, statErr)
	}
	currentInfo, statErr := d.ops.Lstat(name)
	if statErr != nil {
		return result, failure(StaleSource, "read path identity", name, statErr)
	}
	current, statErr := identity(currentInfo)
	if statErr != nil {
		return result, failure(ReadFailed, "read path identity", name, statErr)
	}
	if !sameStamp(before, after) || !sameStamp(after, current) || int64(len(data)) != after.Size {
		return result, failure(StaleSource, "read consistency", name, errors.New("file changed during acquisition"))
	}
	after.SHA256 = sha256.Sum256(data)
	return snapshot{after, data}, nil
}

// Read acquires at most limit+1 bytes and delegates all native validation to wp51.
func (d *Directory) Read(name string) (*Document, error) {
	if err := validName(name); err != nil {
		return nil, err
	}
	snap, err := d.readStable(name)
	if err != nil {
		return nil, err
	}
	image, err := wp51.Parse(snap.data)
	if err != nil {
		return nil, failure(NativeRefused, "native framing", name, err)
	}
	return &Document{image: image, origin: d, name: name, identity: snap.identity}, nil
}

// Observe records an absent name or a regular file's identity, without reading
// unrelated destination bytes. A future changed observation never grants access.
func (d *Directory) Observe(name string) (*Destination, error) {
	if err := validName(name); err != nil {
		return nil, err
	}
	info, err := d.ops.Lstat(name)
	if errors.Is(err, fs.ErrNotExist) {
		return &Destination{directory: d, name: name}, nil
	}
	if err != nil {
		return nil, failure(ReadFailed, "observe", name, err)
	}
	if !info.Mode().IsRegular() {
		return nil, failure(UnsafePath, "destination type", name, errors.New("only regular destination files supported"))
	}
	id, err := identity(info)
	if err != nil {
		return nil, failure(ReadFailed, "destination identity", name, err)
	}
	return &Destination{directory: d, name: name, exists: true, identity: id}, nil
}
func (d *Directory) checkDestination(target *Destination) error {
	current, err := d.Observe(target.name)
	if err != nil {
		return err
	}
	if current.exists != target.exists || (current.exists && !sameStamp(current.identity, target.identity)) {
		return failure(DestinationChanged, "destination observation", target.name, errors.New("destination changed since observation"))
	}
	return nil
}
func checkSource(doc *Document) error {
	current, err := doc.origin.readStable(doc.name)
	if err != nil {
		return failure(StaleSource, "source revalidation", doc.name, err)
	}
	if !sameSnapshot(current.identity, doc.identity) {
		return failure(StaleSource, "source revalidation", doc.name, errors.New("source differs from loaded snapshot"))
	}
	return nil
}

// Save supports atomic no-replace new publication and verified same-file no-op.
// It never opens source/existing destinations for writing or removes a destination.
// A nonnil error is not complete success; inspect Failure.DestinationMayExist.
func (d *Directory) Save(doc *Document, target *Destination, decision Decision) (Outcome, error) {
	if doc == nil || doc.image == nil || doc.origin == nil || target == nil || target.directory != d || target.name == "" || (decision != NoOverwrite && decision != AllowOverwrite) {
		return Outcome{}, failure(InvalidRequest, "save request", "", errors.New("requires document, bound destination and valid decision"))
	}
	if target.exists && decision != AllowOverwrite {
		return Outcome{}, failure(OverwriteRequired, "overwrite decision", target.name, errors.New("explicit permission required for existing destination"))
	}
	if err := checkSource(doc); err != nil {
		return Outcome{}, err
	}
	if err := d.checkDestination(target); err != nil {
		return Outcome{}, err
	}
	if target.exists {
		if target.identity.ID != doc.identity.ID {
			return Outcome{}, failure(UnsupportedReplacement, "existing destination", target.name, errors.New("actual existing-file replacement is unsupported"))
		}
		current, err := d.readStable(target.name)
		if err != nil {
			return Outcome{}, failure(DestinationChanged, "same-file verification", target.name, err)
		}
		if !sameSnapshot(current.identity, doc.identity) {
			return Outcome{}, failure(DestinationChanged, "same-file verification", target.name, errors.New("same-file snapshot changed"))
		}
		return Outcome{State: Unchanged, Name: target.name, DirectoryID: d.id, Identity: current.identity}, nil
	}
	return d.publish(doc, target)
}

type candidate struct {
	name string
	id   FileID
	file file
	pin  file
}

func (d *Directory) createCandidate() (candidate, error) {
	for attempt := 0; attempt < 16; attempt++ {
		var random [16]byte
		if _, err := rand.Read(random[:]); err != nil {
			return candidate{}, err
		}
		name := candidatePrefix + hex.EncodeToString(random[:])
		f, err := d.ops.OpenFile(name, os.O_WRONLY|os.O_CREATE|os.O_EXCL|syscall.O_NOFOLLOW, 0600)
		if errors.Is(err, fs.ErrExist) {
			continue
		}
		if err != nil {
			return candidate{}, err
		}
		c := candidate{name: name, file: f}
		info, err := f.Stat()
		if err != nil {
			return c, err
		}
		id, err := identity(info)
		if err != nil {
			return c, err
		}
		c.id = id.ID
		// Keep the candidate inode allocated after closing its writer. Otherwise a
		// substituted leaf can immediately recycle the same device/inode identity.
		c.pin, err = d.ops.OpenFile(name, os.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_NONBLOCK, 0)
		if err != nil {
			return c, err
		}
		pinnedInfo, err := c.pin.Stat()
		if err != nil {
			return c, err
		}
		pinned, err := identity(pinnedInfo)
		if err != nil {
			return c, err
		}
		if pinned.ID != c.id || !pinnedInfo.Mode().IsRegular() {
			return c, errors.New("candidate changed while pinning")
		}
		return c, nil
	}
	return candidate{}, errors.New("candidate collision limit")
}
func (d *Directory) cleanup(c candidate) error {
	if c.name == "" {
		return nil
	}
	info, err := d.ops.Lstat(c.name)
	if errors.Is(err, fs.ErrNotExist) {
		return nil
	}
	if err != nil {
		return err
	}
	current, err := identity(info)
	if err != nil {
		return err
	}
	if current.ID != c.id || !info.Mode().IsRegular() {
		return errors.New("candidate substituted; residue left untouched")
	}
	return d.ops.Remove(c.name)
}
func (d *Directory) saveFailure(kind Kind, stage, name string, c candidate, cause error, mayExist bool) (Outcome, error) {
	cleanupErr := d.cleanup(c)
	residue := ""
	if cleanupErr != nil {
		residue = c.name
	}
	return Outcome{}, &Failure{Kind: kind, Stage: stage, Name: name, Candidate: residue, DestinationMayExist: mayExist, Cause: errors.Join(cause, cleanupErr)}
}
func (d *Directory) publish(doc *Document, target *Destination) (out Outcome, resultErr error) {
	data := doc.image.Export()
	c, err := d.createCandidate()
	defer func() {
		if c.pin != nil {
			if closeErr := c.pin.Close(); closeErr != nil {
				if resultErr == nil {
					out = Outcome{}
					resultErr = &Failure{Kind: CleanupFailed, Stage: "candidate pin close", Name: target.name, DestinationMayExist: true, Cause: closeErr}
				} else {
					resultErr = errors.Join(resultErr, closeErr)
				}
			}
		}
	}()
	if err != nil {
		// Cleanup precedes descriptor close so a known candidate inode stays pinned.
		out, resultErr = d.saveFailure(CandidateFailed, "candidate create", target.name, c, err, false)
		if c.file != nil {
			resultErr = errors.Join(resultErr, c.file.Close())
		}
		return out, resultErr
	}
	n, writeErr := c.file.Write(data)
	if writeErr == nil && n != len(data) {
		writeErr = io.ErrShortWrite
	}
	closeErr := c.file.Close()
	if err = errors.Join(writeErr, closeErr); err != nil {
		return d.saveFailure(CandidateFailed, "candidate write/close", target.name, c, err, false)
	}
	checked, err := d.readStable(c.name)
	if err != nil || checked.identity.ID != c.id || checked.identity.SHA256 != doc.identity.SHA256 || !bytes.Equal(checked.data, data) {
		return d.saveFailure(CandidateFailed, "candidate verification", target.name, c, errors.Join(err, errors.New("candidate identity/bytes do not match snapshot")), false)
	}
	if err = checkSource(doc); err != nil {
		return d.saveFailure(StaleSource, "pre-publication source", target.name, c, err, false)
	}
	if err = d.checkDestination(target); err != nil {
		return d.saveFailure(DestinationChanged, "pre-publication destination", target.name, c, err, false)
	}
	if err = d.ops.Link(c.name, target.name); err != nil {
		return d.saveFailure(PublicationFailed, "no-replace link", target.name, c, err, true)
	}
	published, err := d.readStable(target.name)
	if err != nil || published.identity.ID != c.id || published.identity.SHA256 != doc.identity.SHA256 || !bytes.Equal(published.data, data) {
		return d.saveFailure(PublicationUncertain, "post-link verification", target.name, c, errors.Join(err, errors.New("published identity/bytes do not match snapshot")), true)
	}
	if err = d.cleanup(c); err != nil {
		return Outcome{}, &Failure{Kind: CleanupFailed, Stage: "published candidate cleanup", Name: target.name, Candidate: c.name, DestinationMayExist: true, Cause: err}
	}
	// Removing the extra hard link changes ctime. Revalidate after our own
	// cleanup so the returned observation describes the final published file.
	published, err = d.readStable(target.name)
	if err != nil || published.identity.ID != c.id || published.identity.SHA256 != doc.identity.SHA256 || !bytes.Equal(published.data, data) {
		return Outcome{}, &Failure{Kind: PublicationUncertain, Stage: "final published verification", Name: target.name, DestinationMayExist: true, Cause: errors.Join(err, errors.New("published snapshot changed during cleanup"))}
	}
	return Outcome{State: Published, Name: target.name, DirectoryID: d.id, Identity: published.identity}, nil
}
