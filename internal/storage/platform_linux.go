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
	renameNoReplace = unix.RENAME_NOREPLACE
	renameExchange  = unix.RENAME_EXCHANGE
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
			callErr = unix.Renameat2(int(src), old, int(dst), new, flags)
		})
	})
	return errors.Join(err, controlErr, callErr)
}

func (r rooted) SyncDirectory() error { return r.dir.Sync() }

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

func identity(info os.FileInfo) (Identity, error) {
	stat, ok := info.Sys().(*syscall.Stat_t)
	if !ok {
		return Identity{}, errors.New("Linux file identity unavailable")
	}
	return Identity{ID: FileID{uint64(stat.Dev), uint64(stat.Ino)}, Size: info.Size(), Mode: info.Mode(), Modified: info.ModTime(), Changed: time.Unix(int64(stat.Ctim.Sec), int64(stat.Ctim.Nsec))}, nil
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
