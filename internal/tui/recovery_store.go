package tui

import (
	"crypto/sha256"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"

	"golang.org/x/sys/unix"
)

type recoveryRecord struct {
	ID, Name, Parent string
	Time             time.Time
	Gap              int
	Native           []byte
}

type recoveryBatch struct {
	Records  []recoveryRecord
	Resolved []string
}

type recoveryStore struct {
	beforePublish func()
	beforeCleanup func()
	resolved      []string
	dir           string
	lock          *os.File
	old           []recoveryStore
}

func openRecovery(workspace string) (*recoveryStore, []recoveryRecord, error) {
	cache, err := os.UserCacheDir()
	if err != nil {
		return nil, nil, err
	}
	parent := filepath.Join(cache, "wordling", "recovery", recoveryWorkspaceKey(workspace))
	if err = os.MkdirAll(parent, 0700); err != nil {
		return nil, nil, err
	}
	dir, err := os.MkdirTemp(parent, ".starting-")
	if err != nil {
		return nil, nil, err
	}
	lock, err := lockRecovery(dir)
	if err != nil {
		return nil, nil, errors.Join(err, os.RemoveAll(dir))
	}
	ready := filepath.Join(parent, "session-"+filepath.Base(dir))
	if err = os.Rename(dir, ready); err != nil {
		_ = lock.Close()
		return nil, nil, errors.Join(err, os.RemoveAll(dir))
	}
	dir = ready
	store := &recoveryStore{dir: dir, lock: lock}
	dirs, err := os.ReadDir(parent)
	if err != nil {
		_ = store.close(true)
		return nil, nil, err
	}
	var records []recoveryRecord
	var issues []error
	resolved := map[string]bool{}
	for _, entry := range dirs {
		if !entry.IsDir() || !strings.HasPrefix(entry.Name(), "session-") || filepath.Join(parent, entry.Name()) == dir {
			continue
		}
		path := filepath.Join(parent, entry.Name())
		lock, err := lockRecovery(path)
		if err != nil {
			continue
		}
		file, err := os.OpenFile(filepath.Join(path, "documents.json"), os.O_RDONLY|unix.O_NOFOLLOW|unix.O_NONBLOCK, 0)
		if errors.Is(err, os.ErrNotExist) {
			_ = os.RemoveAll(path)
			_ = lock.Close()
			continue
		}
		var batch recoveryBatch
		if err == nil {
			info, statErr := file.Stat()
			if statErr != nil {
				err = statErr
			} else if !info.Mode().IsRegular() {
				err = errors.New("recovery snapshot is not a regular file")
			} else {
				err = json.NewDecoder(io.LimitReader(file, 64<<20)).Decode(&batch)
			}
			_ = file.Close()
		}
		if err != nil {
			issues = append(issues, err)
			_ = lock.Close()
			continue
		}
		store.old = append(store.old, recoveryStore{dir: path, lock: lock})
		records = append(records, batch.Records...)
		for _, id := range batch.Resolved {
			resolved[id] = true
		}
	}
	kept := records[:0]
	for _, record := range records {
		if !resolved[record.ID] {
			kept = append(kept, record)
		}
	}
	records = kept
	for id := range resolved {
		store.resolved = append(store.resolved, id)
	}
	sort.SliceStable(records, func(i, j int) bool { return records[i].Time.After(records[j].Time) })
	return store, records, errors.Join(issues...)
}

func lockRecovery(dir string) (*os.File, error) {
	f, err := os.OpenFile(filepath.Join(dir, "lock"), os.O_CREATE|os.O_RDWR|unix.O_NOFOLLOW, 0600)
	if err != nil {
		return nil, err
	}
	if err = unix.Flock(int(f.Fd()), unix.LOCK_EX|unix.LOCK_NB); err != nil {
		_ = f.Close()
		return nil, err
	}
	return f, nil
}

func (s *recoveryStore) write(records []recoveryRecord) error {
	f, err := os.CreateTemp(s.dir, "snapshot-")
	if err != nil {
		return err
	}
	defer os.Remove(f.Name())
	err = json.NewEncoder(f).Encode(recoveryBatch{records, s.resolved})
	err = errors.Join(err, f.Sync(), f.Close())
	if err != nil {
		return err
	}
	if s.beforePublish != nil {
		s.beforePublish()
	}
	if err = os.Rename(f.Name(), filepath.Join(s.dir, "documents.json")); err != nil {
		return err
	}
	dir, err := os.Open(s.dir)
	if err != nil {
		return err
	}
	return errors.Join(dir.Sync(), dir.Close())
}

func (s *recoveryStore) resolve() error {
	if s.beforeCleanup != nil {
		s.beforeCleanup()
	}
	for len(s.old) > 0 {
		old := s.old[0]
		if err := os.RemoveAll(old.dir); err != nil {
			return err
		}
		_ = old.lock.Close()
		s.old = s.old[1:]
	}
	parent, err := os.Open(filepath.Dir(s.dir))
	if err != nil {
		return err
	}
	return errors.Join(parent.Sync(), parent.Close())
}

func (s *recoveryStore) close(clean bool) error {
	var err error
	if clean {
		err = os.RemoveAll(s.dir)
	}
	for _, old := range s.old {
		_ = old.lock.Close()
	}
	return errors.Join(err, s.lock.Close())
}

func recoveryWorkspaceKey(path string) string {
	if canonical, err := filepath.EvalSymlinks(path); err == nil {
		path = canonical
	}
	return fmt.Sprintf("%x", sha256.Sum256([]byte(filepath.Clean(path))))
}

func (s *recoveryStore) clearSnapshot() error {
	err := os.Remove(filepath.Join(s.dir, "documents.json"))
	if errors.Is(err, os.ErrNotExist) {
		return nil
	}
	return err
}
