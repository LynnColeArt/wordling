package storage

import (
	"errors"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
	"syscall"
	"time"
	"unicode/utf16"
	"unsafe"

	"golang.org/x/sys/windows"
)

const (
	noFollow        = 1 << 28
	nonBlock        = 1 << 29
	renameNoReplace = 1
	renameExchange  = 2
)

var symlinkLoop = errors.New("reparse points are not supported")

func platformName(name string) bool {
	return filepath.IsLocal(name) && !strings.ContainsAny(name, `\/:`) && strings.TrimRight(name, ". ") == name
}

// Windows has no equivalent of the two-name atomic exchange used by the
// existing replacement/rollback protocol. Do not emulate it with three renames.
func platformAtomicExchange() bool { return false }

type windowsInfo struct {
	os.FileInfo
	stamp Identity
}

func identity(info os.FileInfo) (Identity, error) {
	if info, ok := info.(windowsInfo); ok {
		return info.stamp, nil
	}
	return Identity{}, errors.New("handle-bound Windows identity unavailable")
}

func platformFileInfo(file *os.File) (os.FileInfo, error) {
	info, err := file.Stat()
	if err != nil {
		return nil, err
	}
	raw, err := file.SyscallConn()
	if err != nil {
		return nil, err
	}
	var id windows.ByHandleFileInformation
	var basic struct {
		CreationTime, LastAccessTime, LastWriteTime, ChangeTime int64
		Attributes                                              uint32
	}
	var callErr error
	err = raw.Control(func(fd uintptr) {
		callErr = windows.GetFileInformationByHandle(windows.Handle(fd), &id)
		if callErr == nil {
			callErr = windows.GetFileInformationByHandleEx(windows.Handle(fd), windows.FileBasicInfo,
				(*byte)(unsafe.Pointer(&basic)), uint32(unsafe.Sizeof(basic)))
		}
	})
	if err = errors.Join(err, callErr); err != nil {
		return nil, err
	}
	const epoch = int64(116444736000000000)
	changed := basic.ChangeTime - epoch
	stamp := Identity{ID: FileID{uint64(id.VolumeSerialNumber), uint64(id.FileIndexHigh)<<32 | uint64(id.FileIndexLow)},
		Size: info.Size(), Mode: info.Mode(), Modified: info.ModTime(), Changed: time.Unix(changed/10000000, changed%10000000*100)}
	return windowsInfo{info, stamp}, nil
}

type windowsFile struct{ *os.File }

func (file windowsFile) Stat() (os.FileInfo, error) { return platformFileInfo(file.File) }

func ntError(err error) error {
	if status, ok := err.(windows.NTStatus); ok {
		return status.Errno()
	}
	return err
}

// Open a single component relative to the held directory handle. Opening the
// reparse point itself lets us reject it before any read or write of its target.
func openWindowsAt(dir *os.File, name string, flags int, metadata bool, access uint32) (*os.File, error) {
	if !platformName(name) {
		return nil, &os.PathError{Op: "openat", Path: name, Err: syscall.EINVAL}
	}
	objectName, err := windows.NewNTUnicodeString(name)
	if err != nil {
		return nil, err
	}
	attributes := windows.OBJECT_ATTRIBUTES{Length: uint32(unsafe.Sizeof(windows.OBJECT_ATTRIBUTES{})), ObjectName: objectName}
	disposition := uint32(windows.FILE_OPEN)
	if flags&os.O_CREATE != 0 {
		disposition = windows.FILE_OPEN_IF
		if flags&os.O_EXCL != 0 {
			disposition = windows.FILE_CREATE
		}
	}
	if flags&os.O_TRUNC != 0 {
		return nil, errors.New("in-place truncation is unsupported")
	}
	if access == 0 {
		access = windows.FILE_GENERIC_READ
		if flags&os.O_WRONLY != 0 {
			access = windows.FILE_GENERIC_WRITE
		}
		if flags&os.O_RDWR != 0 {
			access = windows.FILE_GENERIC_READ | windows.FILE_GENERIC_WRITE
		}
	}
	options := uint32(windows.FILE_SYNCHRONOUS_IO_NONALERT | windows.FILE_OPEN_REPARSE_POINT | windows.FILE_OPEN_FOR_BACKUP_INTENT)
	if !metadata {
		options |= windows.FILE_NON_DIRECTORY_FILE
	}
	raw, err := dir.SyscallConn()
	if err != nil {
		return nil, err
	}
	var handle windows.Handle
	var result windows.IO_STATUS_BLOCK
	var callErr error
	err = raw.Control(func(fd uintptr) {
		attributes.RootDirectory = windows.Handle(fd)
		callErr = ntError(windows.NtCreateFile(&handle, access, &attributes, &result, nil, windows.FILE_ATTRIBUTE_NORMAL,
			windows.FILE_SHARE_READ|windows.FILE_SHARE_WRITE|windows.FILE_SHARE_DELETE, disposition, options, 0, 0))
	})
	if err = errors.Join(err, callErr); err != nil {
		return nil, &os.PathError{Op: "openat", Path: name, Err: err}
	}
	file := os.NewFile(uintptr(handle), name)
	info, err := file.Stat()
	if err != nil {
		file.Close()
		return nil, err
	}
	if !metadata && info.Mode()&os.ModeSymlink != 0 {
		file.Close()
		return nil, symlinkLoop
	}
	var details windows.ByHandleFileInformation
	if err = windows.GetFileInformationByHandle(handle, &details); err != nil {
		file.Close()
		return nil, err
	}
	if !metadata && details.FileAttributes&windows.FILE_ATTRIBUTE_REPARSE_POINT != 0 {
		file.Close()
		return nil, symlinkLoop
	}
	return file, nil
}

func (r rooted) OpenFile(name string, flags int, _ fs.FileMode) (file, error) {
	f, err := openWindowsAt(r.dir, name, flags, false, 0)
	if err != nil {
		return nil, err
	}
	return windowsFile{f}, nil
}

func (r rooted) Lstat(name string) (os.FileInfo, error) {
	f, err := openWindowsAt(r.dir, name, os.O_RDONLY, true, windows.FILE_READ_ATTRIBUTES|windows.SYNCHRONIZE)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	return platformFileInfo(f)
}

func platformEntryInfo(cap *openedDirectory, info os.FileInfo) (os.FileInfo, error) {
	return cap.ops.Lstat(info.Name())
}

func (r rooted) Rename(old, new string, flags uint) error {
	return platformRename(r.dir, old, r.dir, new, flags)
}

func platformRename(from *os.File, old string, to *os.File, new string, flags uint) error {
	if flags != renameNoReplace {
		return errors.New("atomic file exchange is unavailable on Windows")
	}
	if !platformName(new) {
		return syscall.EINVAL
	}
	f, err := openWindowsAt(from, old, os.O_RDONLY, true, windows.DELETE|windows.FILE_READ_ATTRIBUTES|windows.SYNCHRONIZE)
	if err != nil {
		return err
	}
	defer f.Close()
	name := utf16.Encode([]rune(new))
	type renameInfo struct {
		Flags         uint32
		RootDirectory windows.Handle
		NameLength    uint32
		Name          [1]uint16
	}
	offset := int(unsafe.Offsetof(renameInfo{}.Name))
	buffer := make([]byte, offset+len(name)*2)
	info := (*renameInfo)(unsafe.Pointer(&buffer[0]))
	info.NameLength = uint32(len(name) * 2)
	copy(unsafe.Slice((*uint16)(unsafe.Pointer(&buffer[offset])), len(name)), name)
	source, err := f.SyscallConn()
	if err != nil {
		return err
	}
	target, err := to.SyscallConn()
	if err != nil {
		return err
	}
	var callErr, controlErr error
	err = source.Control(func(src uintptr) {
		controlErr = target.Control(func(dst uintptr) {
			info.RootDirectory = windows.Handle(dst)
			var status windows.IO_STATUS_BLOCK
			callErr = ntError(windows.NtSetInformationFile(windows.Handle(src), &status, &buffer[0], uint32(len(buffer)), windows.FileRenameInformation))
		})
	})
	return errors.Join(err, controlErr, callErr)
}

// File.Sync flushes candidate contents before publication. Windows does not
// expose an unprivileged directory fsync equivalent: namespace power-loss
// durability is explicitly unqualified for this prerelease backend.
func (r rooted) SyncDirectory() error { return nil }

var queryVolume = windows.NewLazySystemDLL("ntdll.dll").NewProc("NtQueryVolumeInformationFile")

func platformDiskSpace(dir *os.File) (total, free, available uint64, err error) {
	raw, err := dir.SyscallConn()
	if err != nil {
		return
	}
	var info struct {
		Total, Available, ActualAvailable int64
		Sectors, Bytes                    uint32
	}
	var status windows.IO_STATUS_BLOCK
	var callErr error
	err = raw.Control(func(fd uintptr) {
		code, _, _ := queryVolume.Call(fd, uintptr(unsafe.Pointer(&status)), uintptr(unsafe.Pointer(&info)), unsafe.Sizeof(info), 7)
		if code != 0 {
			callErr = windows.NTStatus(code).Errno()
		}
	})
	err = errors.Join(err, callErr)
	unit := uint64(info.Sectors) * uint64(info.Bytes)
	return uint64(info.Total) * unit, uint64(info.ActualAvailable) * unit, uint64(info.Available) * unit, err
}
