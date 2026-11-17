package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"
)

func TestNativeRecoveryLocksAndSnapshots(t *testing.T) {
	cache := t.TempDir()
	t.Setenv("XDG_CACHE_HOME", cache)
	t.Setenv("LOCALAPPDATA", cache)
	workspace := t.TempDir()
	first, records, err := openRecovery(workspace)
	if err != nil || len(records) != 0 {
		t.Fatal(records, err)
	}
	want := []recoveryRecord{{ID: "native-one", Name: "ONE.WP", Native: []byte("first authored snapshot")}, {ID: "native-two", Native: []byte("second authored snapshot")}}
	if err := first.write(want); err != nil {
		t.Fatal(err)
	}
	// A second process/session cannot claim a still-held recovery directory.
	second, records, err := openRecovery(workspace)
	if err != nil || len(records) != 0 {
		t.Fatal("live session was recovered", records, err)
	}
	if err := second.close(true); err != nil {
		t.Fatal(err)
	}
	if err := first.close(false); err != nil {
		t.Fatal(err)
	}
	restored, records, err := openRecovery(workspace)
	if err != nil || len(records) != len(want) {
		t.Fatal(records, err)
	}
	for i := range want {
		if records[i].ID != want[i].ID || !bytes.Equal(records[i].Native, want[i].Native) {
			t.Fatal("recovery bytes differ")
		}
	}
	if err := restored.resolve(); err != nil {
		t.Fatal(err)
	}
	if err := restored.close(true); err != nil {
		t.Fatal(err)
	}
	clean, records, err := openRecovery(workspace)
	if err != nil || len(records) != 0 {
		t.Fatal("resolved snapshots repeated", records, err)
	}
	if err := clean.close(true); err != nil {
		t.Fatal(err)
	}
}

func TestNativeSettingsAndLockRelease(t *testing.T) {
	dir := t.TempDir()
	for _, visible := range []bool{false, true, false} {
		if err := writeMenuPreference(dir, visible); err != nil {
			t.Fatal(err)
		}
		if actual, err := readMenuPreference(dir); err != nil || actual != visible {
			t.Fatal(actual, err)
		}
	}
	lock, err := lockRecovery(dir)
	if err != nil {
		t.Fatal(err)
	}
	if other, err := lockRecovery(dir); err == nil {
		other.Close()
		t.Fatal("recovery lock acquired twice")
	}
	if err := lock.Close(); err != nil {
		t.Fatal(err)
	}
	lock, err = lockRecovery(dir)
	if err != nil {
		t.Fatal(err)
	}
	if err := lock.Close(); err != nil {
		t.Fatal(err)
	}
	if _, err := os.Stat(filepath.Join(dir, "lock")); err != nil {
		t.Fatal(err)
	}
}
