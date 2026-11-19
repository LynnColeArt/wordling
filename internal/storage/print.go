//go:build linux || darwin || windows

package storage

import (
	"crypto/sha256"
	"errors"

	"github.com/lynncoleart/wordling/internal/wp51"
)

// PrintToNewFile publishes printer bytes to an unused DOS name in the workspace.
func (d *WorkspaceDirectory) PrintToNewFile(name string, data []byte) error {
	if len(data) == 0 || len(data) > wp51.MaxInputBytes {
		return failure(InputLimit, "print to disk", name, nil)
	}
	target, err := d.Observe(name)
	if err != nil {
		return err
	}
	if target.Exists() {
		return failure(DestinationChanged, "print to disk", name, errors.New("destination already exists"))
	}
	_, err = target.directory.publish(sourceGuard{kind: guardNew}, target, data, sha256.Sum256(data))
	return err
}
