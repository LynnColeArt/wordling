package storage

import (
	"errors"
	"golang.org/x/sys/unix"
	"io/fs"
	"os"
	"syscall"
	"time"
)

const (
	noFollow        = syscall.O_NOFOLLOW
	nonBlock        = syscall.O_NONBLOCK
	renameNoReplace = 1
	renameExchange  = 2
)

var symlinkLoop = error(syscall.ELOOP)

func platformName(string) bool                                                 { return true }
func platformAtomicExchange() bool                                             { return true }
func platformFileInfo(f *os.File) (os.FileInfo, error)                         { return f.Stat() }
func platformEntryInfo(_ *openedDirectory, i os.FileInfo) (os.FileInfo, error) { return i, nil }
func (r rooted) Rename(old, new string, flags uint) error {
	return platformRename(r.dir, old, r.dir, new, flags)
}
func platformRename(from *os.File, old string, to *os.File, new string, flags uint) error {
	var nativeFlags uint32
	switch flags {
	case renameNoReplace:
		nativeFlags = unix.RENAME_EXCL
	case renameExchange:
		nativeFlags = unix.RENAME_SWAP
	default:
		return syscall.EINVAL
	}

	if err := qualificationFault("exchange", old, new, flags); err != nil {
		return err
	}
	raw, err := from.SyscallConn()
	if err != nil {
		return err
	}
	toRaw, err := to.SyscallConn()
	if err != nil {
		return err
	}
	var callErr, controlErr error
	err = raw.Control(func(src uintptr) {
		controlErr = toRaw.Control(func(dst uintptr) {
			callErr = unix.RenameatxNp(int(src), old, int(dst), new, nativeFlags)
		})
	})
	return errors.Join(err, controlErr, callErr)
}

func (r rooted) SyncDirectory() error { return r.dir.Sync() }

func (r rooted) OpenFile(name string, flags int, mode fs.FileMode) (file, error) {
	// Root.OpenFile follows in-root symlinks even with O_NOFOLLOW. Flat names let
	// Darwin openat enforce final-component no-follow on the pinned directory FD.
	// RawConn.Control pins that FD against concurrent Close/reuse during openat.
	raw, err := r.dir.SyscallConn()
	if err != nil {
		return nil, err
	}
	opened := -1
	var openErr error
	if err = raw.Control(func(fd uintptr) {
		opened, openErr = unix.Openat(int(fd), name, flags|syscall.O_CLOEXEC, uint32(mode))
	}); err != nil {
		return nil, err
	}
	if openErr != nil {
		return nil, openErr
	}
	return os.NewFile(uintptr(opened), name), nil
}

func identity(info os.FileInfo) (Identity, error) {
	stat, ok := info.Sys().(*syscall.Stat_t)
	if !ok {
		return Identity{}, errors.New("Darwin file identity unavailable")
	}
	return Identity{ID: FileID{uint64(stat.Dev), uint64(stat.Ino)}, Size: info.Size(), Mode: info.Mode(), Modified: info.ModTime(), Changed: time.Unix(int64(stat.Ctimespec.Sec), int64(stat.Ctimespec.Nsec))}, nil
}

func platformDiskSpace(dir *os.File) (total, free, available uint64, err error) {
	raw, err := dir.SyscallConn()
	if err != nil {
		return
	}
	var st syscall.Statfs_t
	var callErr error
	err = raw.Control(func(fd uintptr) { callErr = syscall.Fstatfs(int(fd), &st) })
	err = errors.Join(err, callErr)
	return st.Blocks * uint64(st.Bsize), st.Bfree * uint64(st.Bsize), st.Bavail * uint64(st.Bsize), err
}
