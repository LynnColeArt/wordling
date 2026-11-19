//go:build wordling_qa

package storage

import (
	"encoding/json"
	"golang.org/x/sys/unix"
	"os"
	"strings"
	"sync/atomic"
)

// Test-only, process-local, one-shot fault at the same storage boundary as the
// former syscall injector. Never compiled into a normal or release binary.
var qualificationUsed atomic.Bool

func qualificationFault(stage, old, new string, flags uint) error {
	mode := os.Getenv("WORDLING_QA_SAVE_FAULT")
	matches := (stage == "sync" && mode == "sync-error") ||
		(stage == "exchange" && flags == unix.RENAME_EXCHANGE && (mode == "exchange-error" || mode == "exchange-crash"))
	if !matches || !strings.HasPrefix(old, ".wordling-candidate-") || !qualificationUsed.CompareAndSwap(false, true) {
		return nil
	}
	// Evidence must be newly created; a missing/bad evidence destination fails the
	// QA process rather than pretending a requested fault was observed.
	f, err := os.OpenFile(os.Getenv("WORDLING_QA_FAULT_RECORD"), os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0600)
	if err != nil {
		os.Exit(125)
	}
	err = json.NewEncoder(f).Encode(struct {
		Mode, Stage, Old, New string
		Flags                 uint
		PID                   int
	}{mode, stage, old, new, flags, os.Getpid()})
	if err == nil {
		err = f.Sync()
	}
	closeErr := f.Close()
	if err != nil || closeErr != nil {
		os.Exit(125)
	}
	if mode == "exchange-crash" {
		_ = unix.Kill(os.Getpid(), unix.SIGKILL)
		os.Exit(125)
	}
	return unix.EIO
}
