//go:build linux || darwin

package tui

import (
	"errors"
	"io/fs"
	"os"
	"os/exec"
	"path/filepath"

	"golang.org/x/sys/unix"
)

func openRecoveryFile(path string, flags int, mode fs.FileMode) (*os.File, error) {
	return os.OpenFile(path, flags|unix.O_NOFOLLOW|unix.O_NONBLOCK, mode)
}

func lockRecovery(dir string) (*os.File, error) {
	f, err := openRecoveryFile(filepath.Join(dir, "lock"), os.O_CREATE|os.O_RDWR, 0600)
	if err != nil {
		return nil, err
	}
	if err = unix.Flock(int(f.Fd()), unix.LOCK_EX|unix.LOCK_NB); err != nil {
		f.Close()
		return nil, err
	}
	return f, nil
}

func syncRecoveryDirectory(path string) error {
	dir, err := os.Open(path)
	if err != nil {
		return err
	}
	return errors.Join(dir.Sync(), dir.Close())
}

func platformShell() *exec.Cmd {
	shell := os.Getenv("SHELL")
	if !filepath.IsAbs(shell) {
		shell = "/bin/sh"
	}
	return exec.Command(shell, "-i")
}

func openSettingsFile(root *os.Root) (*os.File, error) {
	return root.OpenFile("settings", os.O_RDONLY|unix.O_NOFOLLOW|unix.O_NONBLOCK, 0)
}

func retireRecoveryDirectory(path string, lock *os.File) error {
	return errors.Join(os.RemoveAll(path), lock.Close())
}
