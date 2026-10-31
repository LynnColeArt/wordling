package storage

import "github.com/lynncoleart/wordling/internal/macro/wpm"

// Macro is an immutable WPM snapshot and its private rooted source observation.
// Construct it with ReadMacro. Its identity is not a lock or a future freshness
// guarantee. It carries no document-publication or macro-write permission.
type Macro struct {
	image    *wpm.Image
	origin   *openedDirectory
	name     string
	identity Identity
}

// Image returns an independent wrapper over the codec's immutable private data.
// Replacing that wrapper cannot rebind the acquired snapshot or source identity.
func (m *Macro) Image() *wpm.Image {
	if m.image == nil {
		return nil
	}
	image := *m.image
	return &image
}
func (m *Macro) Export() []byte      { return m.image.Export() }
func (m *Macro) Identity() Identity  { return m.identity }
func (m *Macro) Name() string        { return m.name }
func (m *Macro) DirectoryID() FileID { return m.origin.id }

// ReadMacro reuses the existing rooted stable acquisition path and delegates
// WPM validation to the approved codec. NativeRefused preserves the typed codec
// cause; filesystem/stale/limit failures retain the existing storage kinds.
// Success establishes framing/preservation, not macro execution or safe editing.
func (d *Directory) ReadMacro(name string) (*Macro, error) {
	if err := validName(name); err != nil {
		return nil, err
	}
	cap := d.acquired()
	if cap == nil {
		return nil, failure(InvalidRequest, "read macro directory", name, nil)
	}
	snap, err := cap.readStable(name)
	if err != nil {
		return nil, err
	}
	image, err := wpm.Parse(snap.data, wpm.DefaultLimits())
	if err != nil {
		return nil, failure(NativeRefused, "macro framing", name, err)
	}
	return &Macro{image: image, origin: cap, name: name, identity: snap.identity}, nil
}
