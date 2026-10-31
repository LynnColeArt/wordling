package storage

import (
	"crypto/sha256"
	"errors"

	"github.com/lynncoleart/wordling/internal/wp51"
)

// PublicationID correlates an operation with a document revision. Both values
// must be nonzero. The session assigns them and decides which revision is current;
// storage does not enforce global uniqueness, monotonicity or cancellation.
type PublicationID struct{ Operation, Revision uint64 }

// Publication binds an immutable framing-validated payload to the original
// source guard, an absent destination observation, and a caller correlation ID.
// Construct it with PreparePublication. Framing does not establish edit safety.
type Publication struct {
	directory *Directory
	source    *Document
	target    *Destination
	image     *wp51.Image
	id        PublicationID
	sha256    [32]byte
	size      int
}

func (p *Publication) ID() PublicationID { return p.id }
func (p *Publication) Size() int         { return p.size }
func (p *Publication) SHA256() [32]byte  { return p.sha256 }

// PreparePublication validates and copies data through wp51.Parse. Callers must
// not mutate data during this call; after return they may reuse it independently.
// Source and destination must belong to this same Directory instance. The
// candidate carries no semantic-edit permission; its caller must establish that.
func (d *Directory) PreparePublication(source *Document, target *Destination, data []byte, id PublicationID) (*Publication, error) {
	if d == nil || source == nil || source.image == nil || source.origin != d || target == nil || target.directory != d || target.name == "" || id.Operation == 0 || id.Revision == 0 {
		return nil, failure(InvalidRequest, "prepare publication", "", errors.New("requires bound source, destination and nonzero operation/revision"))
	}
	if target.exists {
		return nil, failure(UnsupportedReplacement, "prepare publication", target.name, errors.New("edited candidates require an observed absent destination"))
	}
	if len(data) > wp51.MaxInputBytes {
		return nil, failure(InputLimit, "candidate size", target.name, errors.New("exceeds native input limit"))
	}
	image, err := wp51.Parse(data)
	if err != nil {
		return nil, failure(NativeRefused, "candidate framing", target.name, err)
	}
	if err = checkSource(source); err != nil {
		return nil, err
	}
	if err = d.checkDestination(target); err != nil {
		return nil, err
	}
	return &Publication{directory: d, source: source, target: target, image: image, id: id, sha256: sha256.Sum256(data), size: len(data)}, nil
}

// Publish uses the same no-replace transaction as Save, but verifies the edited
// payload separately from the loaded source. expectedID must match the prepared
// operation/revision. No outcome/error alone identifies the current UI revision:
// the caller must carry the ID with asynchronous results and handle uncertainty.
func (d *Directory) Publish(p *Publication, expectedID PublicationID) (Outcome, error) {
	if d == nil || p == nil || p.directory != d || p.source == nil || p.source.origin != d || p.target == nil || p.target.directory != d || p.image == nil || p.id.Operation == 0 || p.id.Revision == 0 || expectedID != p.id {
		return Outcome{}, failure(InvalidRequest, "publish request", "", errors.New("requires a publication bound to this directory and exact operation/revision"))
	}
	if err := checkSource(p.source); err != nil {
		return Outcome{}, err
	}
	if err := d.checkDestination(p.target); err != nil {
		return Outcome{}, err
	}
	return d.publish(p.source, p.target, p.image.Export(), p.sha256)
}
