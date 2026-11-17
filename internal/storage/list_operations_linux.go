package storage

import (
	"errors"
	"os"
	"strings"

	"golang.org/x/sys/unix"
)

func splitDOSFile(path string) (string, string) {
	if i := strings.LastIndexAny(path, `\:`); i >= 0 {
		return path[:i+1], path[i+1:]
	}
	return "", path
}

// Transfer copies bytes as-is or renames a selected regular file. It refuses
// collisions and revalidates the listing snapshot before mutating the root.
func (s *EntrySelection) Transfer(path string, move bool) error {
	if s == nil || s.directory == nil || !s.entry.view.Mode.IsRegular() {
		return errors.New("select a regular file")
	}
	dirName, name := splitDOSFile(path)
	dir, err := s.directory.Navigate(dirName)
	if err != nil {
		return err
	}
	w := dir.workspace
	w.mu.Lock()
	defer w.mu.Unlock()
	if err := s.check(); err != nil {
		return err
	}
	cap, source := dir.directory.acquired(), s.directory.directory.acquired()
	actual, err := resolveDOS(cap, name)
	if err != nil {
		return err
	}
	target, err := cap.observe(actual)
	if err != nil {
		return err
	}
	if target.exists {
		return errors.New("destination already exists")
	}
	if move {
		if cap == source {
			return source.ops.Rename(s.entry.view.Name, actual, unix.RENAME_NOREPLACE)
		}
		// Both directory descriptors are pinned by the workspace lock.
		from, err := source.dir.SyscallConn()
		if err != nil {
			return err
		}
		to, err := cap.dir.SyscallConn()
		if err != nil {
			return err
		}
		var renameErr, controlErr error
		err = from.Control(func(src uintptr) {
			controlErr = to.Control(func(dst uintptr) {
				renameErr = unix.Renameat2(int(src), s.entry.view.Name, int(dst), actual, unix.RENAME_NOREPLACE)
			})
		})
		return errors.Join(err, controlErr, renameErr)
	}
	snap, err := source.readStable(s.entry.view.Name)
	if err != nil {
		return err
	}
	if !sameStamp(snap.identity, s.entry.identity) {
		return failure(StaleSource, "copy", s.entry.view.Name, nil)
	}
	_, err = cap.publish(sourceGuard{kind: guardSelectedFile, selection: s}, target, snap.data, snap.identity.SHA256)
	return err
}

func (s *EntrySelection) Delete() error {
	if s == nil || s.directory == nil || !s.entry.view.Mode.IsRegular() {
		return errors.New("select a regular file")
	}
	w := s.directory.workspace
	w.mu.Lock()
	defer w.mu.Unlock()
	if err := s.check(); err != nil {
		return err
	}
	return s.directory.directory.acquired().ops.Remove(s.entry.view.Name)
}

// PrepareDOSTextSave binds a text snapshot to the observed destination.
func (d *WorkspaceDirectory) PrepareDOSTextSave(path string, data []byte) (*DOSTextSave, error) {
	dirName, name := splitDOSFile(path)
	dir, err := d.Navigate(dirName)
	if err != nil {
		return nil, err
	}
	w := dir.workspace
	w.mu.Lock()
	defer w.mu.Unlock()
	if w.closed {
		return nil, os.ErrClosed
	}
	cap := dir.directory.acquired()
	actual, err := resolveDOS(cap, name)
	if err != nil {
		return nil, err
	}
	target, err := cap.observe(actual)
	if err != nil {
		return nil, err
	}
	id := PublicationID{Operation: 1, Revision: 1}
	request, err := dir.directory.prepareSaveData(sourceGuard{kind: guardNew}, target, data, AllowOverwrite, OriginalBackupPreserve, id, true)
	if err != nil {
		return nil, err
	}
	return &DOSTextSave{dir, request}, nil
}

type DOSTextSave struct {
	dir     *WorkspaceDirectory
	request *saveRequest
}

func (s *DOSTextSave) Exists() bool { return s.request.target.exists }

func (s *DOSTextSave) Publish() error {
	w := s.dir.workspace
	w.mu.Lock()
	defer w.mu.Unlock()
	if w.closed {
		return os.ErrClosed
	}
	_, err := s.dir.directory.publishEveryday(s.request, s.request.id, guardNew)
	return err
}
