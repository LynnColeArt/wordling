//go:build linux || darwin || windows

package storage

import (
	"bytes"
	"fmt"
	"os"
	"strings"

	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

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

// MacroDOSPath supplies the native extension and refuses other suffixes.
func MacroDOSPath(path string) (string, error) {
	base, name := splitDOSFile(path)
	if name == "" {
		return "", fmt.Errorf("enter a macro filename")
	}
	if !strings.Contains(name, ".") {
		name += ".WPM"
	}
	name, err := DOSName(name)
	if err != nil {
		return "", err
	}
	if !strings.HasSuffix(name, ".WPM") {
		return "", fmt.Errorf("macro filename requires .WPM")
	}
	return base + name, nil
}

func (d *WorkspaceDirectory) ResolveMacroFile(path string) (*Directory, string, error) {
	path, err := MacroDOSPath(path)
	if err != nil {
		return nil, "", err
	}
	dirPath, name := splitDOSFile(path)
	dir, err := d.Navigate(dirPath)
	if err != nil {
		return nil, "", err
	}
	w := dir.workspace
	w.mu.Lock()
	defer w.mu.Unlock()
	if w.closed {
		return nil, "", os.ErrClosed
	}
	actual, err := resolveDOS(dir.directory.acquired(), name)
	return dir.Directory(), actual, err
}

// MacroRecordingTarget retains the original destination observation across
// recording and replacement confirmation.
type MacroRecordingTarget struct {
	dir         *WorkspaceDirectory
	destination *Destination
	display     string
}

func (t *MacroRecordingTarget) Exists() bool {
	return t != nil && t.destination != nil && t.destination.Exists()
}
func (t *MacroRecordingTarget) Path() string { return t.display }

func (d *WorkspaceDirectory) ObserveMacroRecording(path string) (*MacroRecordingTarget, error) {
	path, err := MacroDOSPath(path)
	if err != nil {
		return nil, err
	}
	parent, name := splitDOSFile(path)
	dir, err := d.Navigate(parent)
	if err != nil {
		return nil, err
	}
	target, err := dir.Observe(name)
	if err != nil {
		return nil, err
	}
	display := strings.TrimSuffix(dir.DOSPath(), "\\") + "\\" + name
	return &MacroRecordingTarget{dir, target, display}, nil
}

func (t *MacroRecordingTarget) Publish(description string, keys []uint16, replace bool) error {
	if t == nil || t.dir == nil || t.destination == nil {
		return fmt.Errorf("macro recording has no destination")
	}
	raw, err := wpm.EncodeRecording(description, keys)
	if err != nil {
		return err
	}
	decision := NoOverwrite
	if replace && t.Exists() {
		decision = AllowOverwrite
	}
	return t.publish(raw, decision, nil)
}

// PublishEdit rewrites the observed WPM only if its content still matches the
// version handed to the editor. A byte-identical edit does not replace the file.
func (t *MacroRecordingTarget) PublishEdit(image *wpm.Image, description string, keys []uint16, replaceAction bool) error {
	raw, err := image.Edit(description, keys, replaceAction)
	if err != nil {
		return err
	}
	hash := image.SHA256()
	return t.publish(raw, AllowOverwrite, &hash)
}

func (t *MacroRecordingTarget) publish(raw []byte, decision Decision, expected *[32]byte) error {
	w := t.dir.workspace
	w.mu.Lock()
	defer w.mu.Unlock()
	if w.closed {
		return os.ErrClosed
	}
	d := t.dir.directory
	id := PublicationID{Operation: 1, Revision: 1}
	request, err := d.prepareSaveData(sourceGuard{kind: guardNew}, t.destination, raw, decision, OriginalBackupPreserve, id, true)
	if err != nil {
		return err
	}
	if expected != nil {
		if !t.Exists() || request.old.identity.SHA256 != *expected {
			return failure(DestinationChanged, "edited macro no longer matches the opened file", t.destination.name, nil)
		}
		if bytes.Equal(raw, request.old.data) {
			return nil
		}
	}
	_, err = d.publishEveryday(request, id, guardNew)
	return err
}

// ReadExisting returns the WPM only if it is still the file the editor selected.
func (t *MacroRecordingTarget) ReadExisting() (*wpm.Image, error) {
	if !t.Exists() {
		return nil, fmt.Errorf("macro does not exist")
	}
	w := t.dir.workspace
	w.mu.Lock()
	defer w.mu.Unlock()
	if w.closed {
		return nil, os.ErrClosed
	}
	cap := t.dir.directory.acquired()
	actual, err := resolveDOS(cap, t.destination.name)
	if err != nil {
		return nil, err
	}
	if actual != t.destination.name {
		return nil, failure(DestinationChanged, "macro name changed", t.destination.name, nil)
	}
	snapshot, err := cap.readStable(actual)
	if err != nil {
		return nil, err
	}
	if !sameStamp(t.destination.identity, snapshot.identity) {
		return nil, failure(DestinationChanged, "macro changed", actual, nil)
	}
	return wpm.Parse(snapshot.data, wpm.DefaultLimits())
}
