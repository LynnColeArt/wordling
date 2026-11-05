package storage

import (
	"os"
	"sort"
)

// List observes the pinned directory without sharing its enumeration offset.
// Entries are display data. Read still validates a selected file independently.
func (d *Directory) List() ([]os.FileInfo, error) {
	cap := d.acquired()
	if err := receiver(cap, "list directory"); err != nil {
		return nil, err
	}
	f, err := cap.root.Open(".")
	if err != nil {
		return nil, err
	}
	defer f.Close()
	entries, err := f.Readdir(-1)
	if err != nil {
		return nil, err
	}
	sort.Slice(entries, func(i, j int) bool { return entries[i].Name() < entries[j].Name() })
	return entries, nil
}
