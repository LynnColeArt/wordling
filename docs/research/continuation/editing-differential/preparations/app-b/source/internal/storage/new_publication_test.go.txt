package storage_test

import (
	"bytes"
	"crypto/sha256"
	"errors"
	"github.com/lynncoleart/wordling/internal/storage"
	"github.com/lynncoleart/wordling/internal/wp51"
	"os"
	"path/filepath"
	"sync"
	"testing"
)

func TestNewPublicationOwnsPayloadWithoutLoadedSource(t *testing.T) {
	root := t.TempDir()
	d := ownedDirectory(t, root)
	raw := plain(t)
	want := append(bytes.Clone(raw), 'X')
	input := bytes.Clone(want)
	target, _ := d.Observe("first")
	id := storage.PublicationID{Operation: 91, Revision: 3}
	p, err := d.PrepareNewPublication(target, input, id)
	if err != nil {
		t.Fatal(err)
	}
	input[0] ^= 1
	if p.ID() != id || p.Size() != len(want) || p.SHA256() != sha256.Sum256(want) {
		t.Fatal("owned inspection changed")
	}
	out, err := d.PublishNew(p, id)
	if err != nil || out.State != storage.Published || out.Name != "first" || out.DirectoryID != d.ID() || out.Identity.Size != int64(len(want)) || out.Identity.SHA256 != sha256.Sum256(want) {
		t.Fatal(out, err)
	}
	got, e := os.ReadFile(filepath.Join(root, "first"))
	if e != nil || !bytes.Equal(got, want) {
		t.Fatal(e)
	}
	loaded, e := d.Read("first")
	if e != nil || loaded.Identity() != out.Identity || !bytes.Equal(loaded.Export(), want) {
		t.Fatal("real follow-up acquisition does not match receipt", e)
	}
	entries, e := os.ReadDir(root)
	if e != nil || len(entries) != 1 {
		t.Fatal("source-less path fabricated a loaded source/candidate", entries, e)
	}
	_, err = d.PublishNew(p, id)
	expect(t, err, storage.DestinationChanged)
}
func TestNewPublicationAdmissionAndNoNilSourceOverload(t *testing.T) {
	root := t.TempDir()
	d := ownedDirectory(t, root)
	target, _ := d.Observe("first")
	raw := plain(t)
	id := storage.PublicationID{Operation: 92, Revision: 1}
	other := ownedDirectory(t, root)
	foreign, _ := other.Observe("first")
	for _, tc := range []struct {
		target *storage.Destination
		id     storage.PublicationID
	}{{nil, id}, {&storage.Destination{}, id}, {foreign, id}, {target, storage.PublicationID{}}, {target, storage.PublicationID{Operation: 1}}, {target, storage.PublicationID{Revision: 1}}} {
		_, err := d.PrepareNewPublication(tc.target, raw, tc.id)
		expect(t, err, storage.InvalidRequest)
	}
	p, e := d.PrepareNewPublication(target, raw, id)
	if e != nil {
		t.Fatal(e)
	}
	for _, request := range []*storage.NewPublication{nil, {}} {
		_, err := d.PublishNew(request, id)
		expect(t, err, storage.InvalidRequest)
	}
	for _, wrong := range []storage.PublicationID{{}, {Operation: 2, Revision: 1}, {Operation: 92, Revision: 2}} {
		_, err := d.PublishNew(p, wrong)
		expect(t, err, storage.InvalidRequest)
	}
	_, err := other.PublishNew(p, id)
	expect(t, err, storage.InvalidRequest)
	var missing *storage.Directory
	_, err = missing.PrepareNewPublication(target, raw, id)
	expect(t, err, storage.InvalidRequest)
	_, err = missing.PublishNew(p, id)
	expect(t, err, storage.InvalidRequest)
	zero := new(storage.Directory)
	_, err = zero.PublishNew(p, id)
	expect(t, err, storage.InvalidRequest)
	_, err = d.PreparePublication(nil, target, raw, id)
	expect(t, err, storage.InvalidRequest)
	_, err = d.PrepareNewPublication(target, make([]byte, wp51.MaxInputBytes+1), id)
	expect(t, err, storage.InputLimit)
	_, err = d.PrepareNewPublication(target, nil, id)
	expect(t, err, storage.NativeRefused)
	var native *wp51.Failure
	if !errors.As(err, &native) || native.Category != wp51.TruncatedInput {
		t.Fatal(err)
	}
	bad := bytes.Clone(raw)
	bad[len(bad)-1] = 0
	_, err = d.PrepareNewPublication(target, bad, id)
	expect(t, err, storage.NativeRefused)
	macro := macroBytes(t, macroFixtures(t)[0])
	_, err = d.PrepareNewPublication(target, macro, id)
	expect(t, err, storage.NativeRefused)
	if e = os.WriteFile(filepath.Join(root, "existing"), []byte("unrelated"), 0600); e != nil {
		t.Fatal(e)
	}
	existing, _ := d.Observe("existing")
	_, err = d.PrepareNewPublication(existing, raw, id)
	expect(t, err, storage.UnsupportedReplacement)
	entries, _ := os.ReadDir(root)
	if len(entries) != 1 {
		t.Fatal("refused preparation had IO side effects", entries)
	}
}
func TestNewPublicationLateObservationBeforePrepare(t *testing.T) {
	root := t.TempDir()
	d := ownedDirectory(t, root)
	target, _ := d.Observe("first")
	if e := os.WriteFile(filepath.Join(root, "first"), []byte("late"), 0600); e != nil {
		t.Fatal(e)
	}
	_, err := d.PrepareNewPublication(target, plain(t), storage.PublicationID{Operation: 93, Revision: 1})
	expect(t, err, storage.DestinationChanged)
	b, _ := os.ReadFile(filepath.Join(root, "first"))
	if string(b) != "late" {
		t.Fatal("late target overwritten")
	}
	noCandidates(t, root)
}
func TestConcurrentNewPublicationOneNoReplaceWinner(t *testing.T) {
	root := t.TempDir()
	d := ownedDirectory(t, root)
	raw := plain(t)
	const count = 6
	requests := make([]*storage.NewPublication, count)
	for n := range requests {
		target, _ := d.Observe("winner")
		p, e := d.PrepareNewPublication(target, append(bytes.Clone(raw), byte('A'+n)), storage.PublicationID{Operation: uint64(n + 1), Revision: 1})
		if e != nil {
			t.Fatal(e)
		}
		requests[n] = p
	}
	var wg sync.WaitGroup
	outs := make(chan storage.Outcome, count)
	errs := make(chan error, count)
	for _, p := range requests {
		wg.Go(func() { o, e := d.PublishNew(p, p.ID()); outs <- o; errs <- e })
	}
	wg.Wait()
	close(outs)
	close(errs)
	winners := 0
	var winner storage.Outcome
	for out := range outs {
		if out.State == storage.Published {
			winners++
			winner = out
		}
	}
	if winners != 1 {
		t.Fatal("no-replace winners", winners)
	}
	for err := range errs {
		if err == nil {
			continue
		}
		var f *storage.Failure
		if !errors.As(err, &f) || (f.Kind != storage.DestinationChanged && f.Kind != storage.PublicationFailed) {
			t.Fatal(err)
		}
	}
	got, e := os.ReadFile(filepath.Join(root, "winner"))
	if e != nil || sha256.Sum256(got) != winner.Identity.SHA256 || len(got) != len(raw)+1 || !bytes.Equal(got[:len(raw)], raw) {
		t.Fatal("winner identity/bytes", e)
	}
	noCandidates(t, root)
}
