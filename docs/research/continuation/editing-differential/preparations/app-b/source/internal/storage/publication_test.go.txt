package storage_test

import (
	"bytes"
	"crypto/sha256"
	"errors"
	"os"
	"path/filepath"
	"sync"
	"testing"

	"github.com/lynncoleart/wordling/internal/storage"
	"github.com/lynncoleart/wordling/internal/wp51"
)

func TestEditedPublicationOwnsPayloadAndPreservesSource(t *testing.T) {
	d, source, path, original := setup(t)
	target, err := d.Observe("edited")
	if err != nil {
		t.Fatal(err)
	}
	// Synthetic framing-valid payload tests IO identity, not semantic edit safety.
	want := append(bytes.Clone(original), 'X')
	input := bytes.Clone(want)
	id := storage.PublicationID{Operation: 7, Revision: 3}
	request, err := d.PreparePublication(source, target, input, id)
	if err != nil {
		t.Fatal(err)
	}
	input[0] ^= 1
	if request.ID() != id || request.Size() != len(want) || request.SHA256() != sha256.Sum256(want) || request.SHA256() == source.Identity().SHA256 {
		t.Fatal("candidate/source identity or owned payload confused")
	}
	out, err := d.Publish(request, id)
	if err != nil || out.State != storage.Published || out.Identity.SHA256 != sha256.Sum256(want) || out.Identity.Size != int64(len(want)) {
		t.Fatalf("different candidate not published exactly: %+v / %v", out, err)
	}
	got, err := os.ReadFile(filepath.Join(path, "edited"))
	if err != nil || !bytes.Equal(got, want) {
		t.Fatal("wrong candidate bytes")
	}
	got, err = os.ReadFile(filepath.Join(path, "source"))
	if err != nil || !bytes.Equal(got, original) || !bytes.Equal(source.Export(), original) {
		t.Fatal("loaded source changed")
	}
	_, err = d.Publish(request, id)
	expect(t, err, storage.DestinationChanged)
}

func TestPublicationRejectsUnboundAndUnsupportedRequests(t *testing.T) {
	d, source, path, original := setup(t)
	target, _ := d.Observe("edited")
	id := storage.PublicationID{Operation: 1, Revision: 1}
	request, err := d.PreparePublication(source, target, original, id)
	if err != nil {
		t.Fatal(err)
	}
	other := directory(t, path)
	otherTarget, _ := other.Observe("elsewhere")
	for _, tc := range []struct {
		doc    *storage.Document
		target *storage.Destination
		id     storage.PublicationID
	}{
		{nil, target, id}, {&storage.Document{}, target, id}, {source, nil, id},
		{source, &storage.Destination{}, id}, {source, otherTarget, id},
		{source, target, storage.PublicationID{}},
		{source, target, storage.PublicationID{Operation: 1}},
		{source, target, storage.PublicationID{Revision: 1}},
	} {
		_, err = d.PreparePublication(tc.doc, tc.target, original, tc.id)
		expect(t, err, storage.InvalidRequest)
	}
	_, err = other.PreparePublication(source, otherTarget, original, id)
	expect(t, err, storage.InvalidRequest)
	for _, r := range []*storage.Publication{nil, {}} {
		_, err = d.Publish(r, id)
		expect(t, err, storage.InvalidRequest)
	}
	for _, wrong := range []storage.PublicationID{{}, {Operation: 2, Revision: 1}, {Operation: 1, Revision: 2}} {
		_, err = d.Publish(request, wrong)
		expect(t, err, storage.InvalidRequest)
	}
	_, err = other.Publish(request, id)
	expect(t, err, storage.InvalidRequest)
	var missing *storage.Directory
	_, err = missing.PreparePublication(source, target, original, id)
	expect(t, err, storage.InvalidRequest)
	_, err = missing.Publish(request, id)
	expect(t, err, storage.InvalidRequest)
	for _, name := range []string{"source", "existing"} {
		if name == "existing" {
			if err = os.WriteFile(filepath.Join(path, name), []byte("unrelated"), 0600); err != nil {
				t.Fatal(err)
			}
		}
		existing, _ := d.Observe(name)
		_, err = d.PreparePublication(source, existing, original, id)
		expect(t, err, storage.UnsupportedReplacement)
	}
	_, err = d.PreparePublication(source, target, nil, id)
	expect(t, err, storage.NativeRefused)
	var native *wp51.Failure
	if !errors.As(err, &native) || native.Category != wp51.TruncatedInput {
		t.Fatal("candidate framing refusal lost native cause")
	}
	_, err = d.PreparePublication(source, target, make([]byte, wp51.MaxInputBytes+1), id)
	expect(t, err, storage.InputLimit)
	entries, _ := os.ReadDir(path)
	if len(entries) != 2 {
		t.Fatal("invalid request created a file")
	}
}

func TestPreparedPublicationStillChecksLoadedSource(t *testing.T) {
	d, source, path, original := setup(t)
	target, _ := d.Observe("edited")
	id := storage.PublicationID{Operation: 1, Revision: 1}
	payload := append(bytes.Clone(original), 'X')
	request, err := d.PreparePublication(source, target, payload, id)
	if err != nil {
		t.Fatal(err)
	}
	if err = os.WriteFile(filepath.Join(path, "source"), payload, 0600); err != nil {
		t.Fatal(err)
	}
	_, err = d.Publish(request, id)
	expect(t, err, storage.StaleSource)
	_, err = d.PreparePublication(source, target, payload, id)
	expect(t, err, storage.StaleSource)
	if _, err = os.Stat(filepath.Join(path, "edited")); !os.IsNotExist(err) {
		t.Fatal("stale source published")
	}
}

func TestPublicationNativeBoundary(t *testing.T) {
	d, source, _, original := setup(t)
	target, _ := d.Observe("edited")
	id := storage.PublicationID{Operation: 1, Revision: 1}
	bad := bytes.Clone(original)
	bad[len(bad)-1] = 0 // standalone NUL is not valid outer-body framing
	_, err := d.PreparePublication(source, target, bad, id)
	expect(t, err, storage.NativeRefused)
	var native *wp51.Failure
	if !errors.As(err, &native) || native.Category != wp51.MalformedBody {
		t.Fatal("malformed candidate cause changed")
	}
	maximum := append(bytes.Clone(original), bytes.Repeat([]byte{'X'}, wp51.MaxInputBytes-len(original))...)
	p, err := d.PreparePublication(source, target, maximum, id)
	if err != nil || p.Size() != wp51.MaxInputBytes || p.SHA256() != sha256.Sum256(maximum) {
		t.Fatalf("exact parser policy limit rejected or changed: %v", err)
	}
}

func TestConcurrentEditedPublicationHasOneNoReplaceWinner(t *testing.T) {
	d, source, path, original := setup(t)
	const count = 8
	requests := make([]*storage.Publication, count)
	for i := range requests {
		target, _ := d.Observe("winner")
		var err error
		requests[i], err = d.PreparePublication(source, target, append(bytes.Clone(original), byte('A'+i)), storage.PublicationID{Operation: uint64(i + 1), Revision: 1})
		if err != nil {
			t.Fatal(err)
		}
	}
	var wg sync.WaitGroup
	results := make(chan storage.Outcome, count)
	errCh := make(chan error, count)
	for _, request := range requests {
		wg.Go(func() {
			out, err := d.Publish(request, request.ID())
			results <- out
			errCh <- err
		})
	}
	wg.Wait()
	close(results)
	close(errCh)
	winners := 0
	var winner storage.Outcome
	for out := range results {
		if out.State == storage.Published {
			winners++
			winner = out
		}
	}
	if winners != 1 {
		t.Fatalf("wanted one winner, got %d", winners)
	}
	for err := range errCh {
		if err == nil {
			continue
		}
		var f *storage.Failure
		if !errors.As(err, &f) || (f.Kind != storage.DestinationChanged && f.Kind != storage.PublicationFailed) {
			t.Fatalf("unexpected loser: %v", err)
		}
	}
	actual, err := os.ReadFile(filepath.Join(path, "winner"))
	if err != nil || sha256.Sum256(actual) != winner.Identity.SHA256 || len(actual) != len(original)+1 || !bytes.Equal(actual[:len(original)], original) {
		t.Fatal("winner is not an exact candidate")
	}
}
