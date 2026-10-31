package storage

import "github.com/lynncoleart/wordling/internal/macro/wpm"

// Macro is an immutable WPM snapshot and its private rooted source observation.
// Construct it with ReadMacro. Its identity is not a lock or a future freshness
// guarantee. It carries no document-publication or macro-write permission.
type Macro struct {
	image    *wpm.Image
	origin   *Directory
	name     string
	identity Identity
}

func (m *Macro) Image() *wpm.Image   { return m.image }
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
	snap, err := d.readStable(name)
	if err != nil {
		return nil, err
	}
	image, err := wpm.Parse(snap.data, wpm.DefaultLimits())
	if err != nil {
		return nil, failure(NativeRefused, "macro framing", name, err)
	}
	return &Macro{image: image, origin: d, name: name, identity: snap.identity}, nil
}
