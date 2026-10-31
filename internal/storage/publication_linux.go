package storage

import (
	"crypto/sha256"
	"errors"
	"github.com/lynncoleart/wordling/internal/wp51"
)

// PublicationID correlates a caller operation/revision; both must be nonzero.
// It is not authorization, global uniqueness, cancellation or document identity.
type PublicationID struct{ Operation, Revision uint64 }

// Publication owns its accepted original source and destination observations.
// Framing acceptance is not semantic edit permission.
type Publication struct {
	directory *openedDirectory
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

// NewPublication is distinct: it has no loaded source guard and grants only
// native-document framing and absent-target transaction admission. Future editor
// routing must limit it to a genuinely never-sourced New buffer.
type NewPublication struct {
	directory *openedDirectory
	target    *Destination
	image     *wp51.Image
	id        PublicationID
	sha256    [32]byte
	size      int
}

func (p *NewPublication) ID() PublicationID { return p.id }
func (p *NewPublication) Size() int         { return p.size }
func (p *NewPublication) SHA256() [32]byte  { return p.sha256 }

func candidateImage(target *Destination, data []byte) (*wp51.Image, error) {
	if target.exists {
		return nil, failure(UnsupportedReplacement, "prepare publication", target.name, errors.New("requires an observed absent destination"))
	}
	if len(data) > wp51.MaxInputBytes {
		return nil, failure(InputLimit, "candidate size", target.name, errors.New("exceeds native input limit"))
	}
	image, err := wp51.Parse(data)
	if err != nil {
		return nil, failure(NativeRefused, "candidate framing", target.name, err)
	}
	return image, nil
}

// PreparePublication captures a same-capability real source and absent target.
// Caller data must not change during this call; Parse owns the returned bytes.
func (d *Directory) PreparePublication(source *Document, target *Destination, data []byte, id PublicationID) (*Publication, error) {
	cap := d.acquired()
	if err := receiver(cap, "prepare publication"); err != nil {
		return nil, err
	}
	if source == nil || target == nil {
		return nil, failure(InvalidRequest, "prepare publication", "", errors.New("requires source and destination"))
	}
	src, dst := *source, *target
	if src.image == nil || src.origin != cap || dst.directory != cap || dst.name == "" || id.Operation == 0 || id.Revision == 0 {
		return nil, failure(InvalidRequest, "prepare publication", "", errors.New("requires bound source, destination and nonzero operation/revision"))
	}
	image, err := candidateImage(&dst, data)
	if err != nil {
		return nil, err
	}
	if err = checkSource(&src); err != nil {
		return nil, err
	}
	if err = cap.checkDestination(&dst); err != nil {
		return nil, err
	}
	return &Publication{directory: cap, source: &src, target: &dst, image: image, id: id, sha256: sha256.Sum256(data), size: len(data)}, nil
}

// Publish refuses a rebound/closed receiver before filesystem IO. The captured
// request is observed once; all work thereafter follows private capability state.
func (d *Directory) Publish(p *Publication, expectedID PublicationID) (Outcome, error) {
	cap := d.acquired()
	if err := receiver(cap, "publish request"); err != nil {
		return Outcome{}, err
	}
	if p == nil {
		return Outcome{}, failure(InvalidRequest, "publish request", "", errors.New("nil publication"))
	}
	request := *p
	if request.directory != cap || request.source == nil || request.source.origin != cap || request.target == nil || request.target.directory != cap || request.image == nil || request.id.Operation == 0 || request.id.Revision == 0 || request.id != expectedID {
		return Outcome{}, failure(InvalidRequest, "publish request", "", errors.New("requires exact prepared capability and operation/revision"))
	}
	if err := checkSource(request.source); err != nil {
		return Outcome{}, err
	}
	if err := cap.checkDestination(request.target); err != nil {
		return Outcome{}, err
	}
	return cap.publish(sourceGuard{kind: guardLoaded, source: request.source}, request.target, request.image.Export(), request.sha256)
}
func (d *Directory) PrepareNewPublication(target *Destination, data []byte, id PublicationID) (*NewPublication, error) {
	cap := d.acquired()
	if err := receiver(cap, "prepare new publication"); err != nil {
		return nil, err
	}
	if target == nil {
		return nil, failure(InvalidRequest, "prepare new publication", "", errors.New("requires destination"))
	}
	dst := *target
	if dst.directory != cap || dst.name == "" || id.Operation == 0 || id.Revision == 0 {
		return nil, failure(InvalidRequest, "prepare new publication", "", errors.New("requires bound destination and nonzero operation/revision"))
	}
	image, err := candidateImage(&dst, data)
	if err != nil {
		return nil, err
	}
	if err = cap.checkDestination(&dst); err != nil {
		return nil, err
	}
	return &NewPublication{directory: cap, target: &dst, image: image, id: id, sha256: sha256.Sum256(data), size: len(data)}, nil
}
func (d *Directory) PublishNew(p *NewPublication, expectedID PublicationID) (Outcome, error) {
	cap := d.acquired()
	if err := receiver(cap, "publish new request"); err != nil {
		return Outcome{}, err
	}
	if p == nil {
		return Outcome{}, failure(InvalidRequest, "publish new request", "", errors.New("nil publication"))
	}
	request := *p
	if request.directory != cap || request.target == nil || request.target.directory != cap || request.image == nil || request.id.Operation == 0 || request.id.Revision == 0 || request.id != expectedID {
		return Outcome{}, failure(InvalidRequest, "publish new request", "", errors.New("requires exact prepared capability and operation/revision"))
	}
	if err := cap.checkDestination(request.target); err != nil {
		return Outcome{}, err
	}
	return cap.publish(sourceGuard{kind: guardNew}, request.target, request.image.Export(), request.sha256)
}

type guardKind uint8

const (
	guardLoaded guardKind = iota + 1
	guardNew
)

type sourceGuard struct {
	kind   guardKind
	source *Document
}

func (g sourceGuard) validate(cap *openedDirectory, target *Destination) error {
	if !cap.open() || target == nil || target.directory != cap || target.name == "" {
		return failure(InvalidRequest, "transaction guard", "", errors.New("invalid opened capability/destination"))
	}
	switch g.kind {
	case guardLoaded:
		if g.source != nil && g.source.image != nil && g.source.origin.open() {
			return nil
		}
	case guardNew:
		if g.source == nil {
			return nil
		}
	}
	return failure(InvalidRequest, "transaction guard", "", errors.New("requires explicit loaded or new guard kind"))
}
func (g sourceGuard) check() error {
	switch g.kind {
	case guardLoaded:
		return checkSource(g.source)
	case guardNew:
		return nil
	}
	return failure(InvalidRequest, "transaction guard", "", errors.New("unknown guard kind"))
}
