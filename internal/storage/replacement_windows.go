package storage

import (
	"crypto/rand"
	"errors"
	"io/fs"
	"os"
	"strings"
	"unsafe"

	"golang.org/x/sys/windows"
)

var replaceFile = windows.NewLazySystemDLL("kernel32.dll").NewProc("ReplaceFileW")

// ReplaceFile captures the actual displaced file in a private escrow. A single
// namespace replacement is atomic; the document and .BK! are separate steps.
// Unlike an exchange, ReplaceFile may partially move names on failure. Classify
// every error using both identities and contents before attempting restoration.
func platformReplaceStep(s *saveStep, undo bool) error {
	if s.staged.pin != nil {
		if err := s.staged.pin.Close(); err != nil {
			return err
		}
		s.staged.pin = nil
	}
	if undo && s.oldPin != nil {
		if err := s.oldPin.Close(); err != nil {
			return err
		}
		s.oldPin = nil
	}
	old, next := s.old, s.stagedSnapshot
	if undo {
		old, next = next, old
	}
	if err := s.verify(s.staged.name, next); err != nil {
		return err
	}
	escrow := candidatePrefix + rand.Text()
	if _, err := s.cap.ops.Lstat(escrow); !errors.Is(err, fs.ErrNotExist) {
		return errors.Join(err, errors.New("replacement escrow is not absent"))
	}
	previous := s.staged.name
	err := s.cap.ops.Replace(previous, s.target.name, escrow)
	if err == nil {
		s.staged.name = escrow
		s.applied = !undo
		return nil
	}
	absent := func(name string) bool {
		_, e := s.cap.ops.Lstat(name)
		return errors.Is(e, fs.ErrNotExist)
	}
	// Some filesystem/filter errors can arrive after the replacement completed.
	if s.verify(s.target.name, next) == nil && s.verify(escrow, old) == nil && absent(previous) {
		s.staged.name = escrow
		s.applied = !undo
		return err
	}
	if s.verify(previous, next) == nil {
		if s.verify(s.target.name, old) == nil && absent(escrow) {
			return err // All names retained (including errors 1175 and 1176).
		}
		if absent(s.target.name) && s.verify(escrow, old) == nil {
			// ERROR_UNABLE_TO_MOVE_REPLACEMENT_2 (1177). Restore only into
			// an absent destination; never clobber an independent writer.
			if restore := s.cap.ops.Rename(escrow, s.target.name, renameNoReplace); restore == nil {
				return err
			} else {
				err = errors.Join(err, restore)
			}
		}
	}
	s.uncertain = true
	s.residues = append(s.residues, escrow)
	return errors.Join(err, errors.New("replacement partially completed; private files retained"))
}

// ReplaceFileW takes paths, not directory handles. Lease each component of the
// resolved volume-GUID path without FILE_SHARE_DELETE, starting at the immutable
// volume root. This prevents ancestor renames/reparse substitution during the
// call. Verify the final directory is the originally acquired capability. UNC
// and filesystems without volume-GUID paths fail before modifying either file.
func replacementDirectory(dir *os.File) (path string, release func(), err error) {
	var held []windows.Handle
	release = func() {
		for i := len(held) - 1; i >= 0; i-- {
			windows.CloseHandle(held[i])
		}
	}
	defer func() {
		if err != nil {
			release()
		}
	}()
	buffer := make([]uint16, 32768)
	n, err := windows.GetFinalPathNameByHandle(windows.Handle(dir.Fd()), &buffer[0], uint32(len(buffer)), 1)
	if err != nil {
		return "", release, err
	}
	if n >= uint32(len(buffer)) {
		return "", release, errors.New("replacement directory path exceeds native limit")
	}
	path = windows.UTF16ToString(buffer[:n])
	if !strings.HasPrefix(path, `\\?\Volume{`) {
		return "", release, errors.New("replacement requires a local volume-GUID path")
	}
	boundary := strings.Index(path, `}\`)
	if boundary < 0 {
		return "", release, errors.New("invalid volume-GUID path")
	}
	root := path[:boundary+2]
	parts := []string{root}
	current := strings.TrimSuffix(root, `\`)
	for _, part := range strings.Split(path[len(root):], `\`) {
		if part == "" {
			continue
		}
		current += `\` + part
		parts = append(parts, current)
	}
	var final windows.ByHandleFileInformation
	for _, part := range parts {
		name, e := windows.UTF16PtrFromString(part)
		if e != nil {
			return "", release, e
		}
		h, e := windows.CreateFile(name, windows.FILE_READ_ATTRIBUTES|windows.SYNCHRONIZE,
			windows.FILE_SHARE_READ|windows.FILE_SHARE_WRITE, nil, windows.OPEN_EXISTING,
			windows.FILE_FLAG_BACKUP_SEMANTICS|windows.FILE_FLAG_OPEN_REPARSE_POINT, 0)
		if e != nil {
			return "", release, e
		}
		held = append(held, h)
		if e = windows.GetFileInformationByHandle(h, &final); e != nil {
			return "", release, e
		}
		if final.FileAttributes&windows.FILE_ATTRIBUTE_REPARSE_POINT != 0 || final.FileAttributes&windows.FILE_ATTRIBUTE_DIRECTORY == 0 {
			return "", release, errors.New("replacement ancestor is not a plain directory")
		}
	}
	var original windows.ByHandleFileInformation
	if err = windows.GetFileInformationByHandle(windows.Handle(dir.Fd()), &original); err != nil {
		return "", release, err
	}
	if original.VolumeSerialNumber != final.VolumeSerialNumber || original.FileIndexHigh != final.FileIndexHigh || original.FileIndexLow != final.FileIndexLow {
		return "", release, errors.New("replacement directory changed while acquiring path lease")
	}
	return strings.TrimSuffix(path, `\`), release, nil
}

func (r rooted) Replace(candidate, target, escrow string) error {
	for _, name := range []string{candidate, target, escrow} {
		if !platformName(name) {
			return errors.New("invalid replacement name")
		}
	}
	path, release, err := replacementDirectory(r.dir)
	if err != nil {
		return err
	}
	defer release()
	var names [3]*uint16
	for i, name := range []string{target, candidate, escrow} {
		names[i], err = windows.UTF16PtrFromString(path + `\` + name)
		if err != nil {
			return err
		}
	}
	ok, _, callErr := replaceFile.Call(uintptr(unsafe.Pointer(names[0])), uintptr(unsafe.Pointer(names[1])), uintptr(unsafe.Pointer(names[2])), 0, 0, 0)
	if ok == 0 {
		return callErr
	}
	return nil
}
