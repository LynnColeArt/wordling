package tui

import (
	"crypto/rand"
	"errors"
	"io/fs"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"golang.org/x/sys/windows"
)

func openRecoveryFile(path string, flags int, _ fs.FileMode) (*os.File, error) {
	name, err := windows.UTF16PtrFromString(path)
	if err != nil {
		return nil, err
	}
	access := uint32(windows.GENERIC_READ)
	if flags&os.O_RDWR != 0 {
		access |= windows.GENERIC_WRITE
	}
	disposition := uint32(windows.OPEN_EXISTING)
	if flags&os.O_CREATE != 0 {
		disposition = windows.OPEN_ALWAYS
	}
	handle, err := windows.CreateFile(name, access, windows.FILE_SHARE_READ|windows.FILE_SHARE_WRITE|windows.FILE_SHARE_DELETE,
		nil, disposition, windows.FILE_FLAG_OPEN_REPARSE_POINT, 0)
	if err != nil {
		return nil, err
	}
	var info windows.ByHandleFileInformation
	if err = windows.GetFileInformationByHandle(handle, &info); err == nil && info.FileAttributes&windows.FILE_ATTRIBUTE_REPARSE_POINT != 0 {
		err = errors.New("recovery reparse point refused")
	}
	if err != nil {
		windows.CloseHandle(handle)
		return nil, err
	}
	return os.NewFile(uintptr(handle), path), nil
}

func lockRecovery(dir string) (*os.File, error) {
	// Windows forbids renaming a directory containing an open locked file,
	// even when that file shares delete access. Keep the lease beside the
	// session, using the same name before and after startup publication.
	name := strings.TrimPrefix(filepath.Base(dir), "session-")
	path := filepath.Join(filepath.Dir(dir), ".lock-"+name)
	f, err := openRecoveryFile(path, os.O_CREATE|os.O_RDWR, 0600)
	if err != nil {
		return nil, err
	}
	var overlapped windows.Overlapped
	if err = windows.LockFileEx(windows.Handle(f.Fd()), windows.LOCKFILE_EXCLUSIVE_LOCK|windows.LOCKFILE_FAIL_IMMEDIATELY,
		0, 1, 0, &overlapped); err != nil {
		f.Close()
		return nil, err
	}
	return f, nil
}

// Windows recovery flushes the snapshot file before its rename. Directory-entry
// power-loss durability remains unqualified, as for the native storage backend.
func syncRecoveryDirectory(string) error { return nil }

// PowerShell 7 is preferred; stock Windows PowerShell is available on supported
// Windows hosts. Do not silently fall back to cmd.exe. Profiles load normally.
func platformShell() *exec.Cmd {
	if shell := os.Getenv("SHELL"); filepath.IsAbs(shell) {
		switch strings.ToLower(filepath.Base(shell)) {
		case "pwsh.exe", "powershell.exe", "pwsh", "powershell":
			return exec.Command(shell, "-NoLogo")
		case "cmd.exe", "cmd":
			return exec.Command(shell, "/D")
		default:
			return exec.Command(shell, "-i")
		}
	}
	if shell, err := exec.LookPath("pwsh.exe"); err == nil {
		return exec.Command(shell, "-NoLogo")
	}
	root := os.Getenv("SystemRoot")
	if root == "" {
		root = `C:\Windows`
	}
	return exec.Command(filepath.Join(root, "System32", "WindowsPowerShell", "v1.0", "powershell.exe"), "-NoLogo")
}

func openSettingsFile(root *os.Root) (*os.File, error) {
	f, err := root.OpenFile("settings", os.O_RDONLY|0x00200000, 0)
	if err != nil {
		return nil, err
	}
	var info windows.ByHandleFileInformation
	if err = windows.GetFileInformationByHandle(windows.Handle(f.Fd()), &info); err == nil && info.FileAttributes&windows.FILE_ATTRIBUTE_REPARSE_POINT != 0 {
		err = errors.New("settings reparse point refused")
	}
	if err != nil {
		f.Close()
		return nil, err
	}
	return f, nil
}

func retireRecoveryDirectory(path string, lock *os.File) (bool, error) {
	// A held byte-range lock may leave a deleted file pending until Close, which
	// prevents removing its parent on Windows. First take the directory out of
	// the recovery discovery namespace while we still own its lock.
	retired := filepath.Join(filepath.Dir(path), ".retired-"+rand.Text())
	if err := os.Rename(path, retired); err != nil {
		return false, err
	}
	closeErr := lock.Close()
	removeErr := os.Remove(lock.Name())
	if errors.Is(removeErr, os.ErrNotExist) {
		removeErr = nil
	}
	return true, errors.Join(closeErr, removeErr, os.RemoveAll(retired))
}
