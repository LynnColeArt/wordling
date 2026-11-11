package proofreading_test

import (
	"bytes"
	"context"
	"errors"
	"os"
	"path/filepath"
	"sync"
	"testing"

	"github.com/lynncoleart/wordling/internal/proofreading"
	"github.com/lynncoleart/wordling/internal/storage"
)

func require(t *testing.T, err error) {
	t.Helper()
	if err != nil {
		t.Fatal(err)
	}
}

func proofWorkspace(t *testing.T, path string) (*storage.Workspace, *storage.WorkspaceDirectory) {
	t.Helper()
	w, err := storage.OpenWorkspace(path)
	require(t, err)
	t.Cleanup(func() { _ = w.Close() })
	d, err := w.Root()
	require(t, err)
	return w, d
}

func originalSUP(t *testing.T) []byte {
	t.Helper()
	data, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/spelling/proof/supplementary/WP{WP}US.SUP")
	require(t, err)
	return data
}

func proofID(n uint64) storage.PublicationID { return storage.PublicationID{Operation: n, Revision: n} }

func assertFile(t *testing.T, name string, want []byte) {
	t.Helper()
	data, err := os.ReadFile(name)
	require(t, err)
	if !bytes.Equal(data, want) {
		t.Fatalf("unexpected bytes in %s: %x", name, data)
	}
}

func TestSupplementaryDefaultAddPreservesOriginalFramingAndReopens(t *testing.T) {
	ctx := context.Background()
	path := t.TempDir()
	w, d := proofWorkspace(t, path)
	file := filepath.Join(path, proofreading.DefaultSupplementaryName)
	backup := filepath.Join(path, "WP{WP}US.BK!")
	require(t, os.WriteFile(backup, []byte("unrelated backup"), 0600))

	absent, err := proofreading.OpenSupplementary(ctx, w, d, "")
	require(t, err)
	if absent.Exists() || absent.Name() != proofreading.DefaultSupplementaryName {
		t.Fatal("missing default selection was not represented")
	}
	first, err := absent.Add(ctx, "zorbly", proofID(1))
	require(t, err)
	assertFile(t, file, originalSUP(t))
	if accepted, _ := absent.Accepts("zorbly"); accepted {
		t.Fatal("first publication changed the prior immutable snapshot")
	}
	second, err := first.Add(ctx, "Vimward", proofID(2))
	require(t, err)
	want := append(originalSUP(t), []byte("Vimward\n")...)
	assertFile(t, file, want)
	_, err = second.Add(ctx, "VIMWARD", proofID(3))
	require(t, err)
	assertFile(t, file, want)
	assertFile(t, backup, []byte("unrelated backup"))

	freshWorkspace, freshDirectory := proofWorkspace(t, path)
	reopened, err := proofreading.OpenSupplementary(ctx, freshWorkspace, freshDirectory, "")
	require(t, err)
	for _, word := range []string{"Zorbly", "vimward"} {
		if accepted, err := reopened.Accepts(word); err != nil || !accepted {
			t.Fatalf("reopened dictionary missing %q: %v", word, err)
		}
	}
}

func TestSupplementaryCustomCreationAndForeignOrMalformedRefusal(t *testing.T) {
	ctx := context.Background()
	path := t.TempDir()
	w, d := proofWorkspace(t, path)
	other, _ := proofWorkspace(t, path)
	if _, err := proofreading.OpenSupplementary(ctx, other, d, "SPELLADD"); err == nil {
		t.Fatal("accepted foreign workspace directory")
	}
	s, err := proofreading.OpenSupplementary(ctx, w, d, "SPELLADD")
	require(t, err)
	s, err = s.Create(ctx, proofID(1))
	require(t, err)
	assertFile(t, filepath.Join(path, "SPELLADD"), originalSUP(t)[:66])
	s, err = s.Add(ctx, "Zorbly", proofID(2))
	require(t, err)
	assertFile(t, filepath.Join(path, "SPELLADD"), append(originalSUP(t)[:66], []byte("Zorbly\n")...))
	if _, err = s.Create(ctx, proofID(3)); err == nil {
		t.Fatal("custom create truncated an existing dictionary")
	}

	badName := filepath.Join(path, "BAD.SUP")
	for _, mutate := range []func([]byte) []byte{
		func(data []byte) []byte { data[32] = 1; return data },
		func(data []byte) []byte { data[12] = 1; return data },
		func(data []byte) []byte { return data[:len(data)-1] },
		func(data []byte) []byte { return append(data, []byte("bad word\n")...) },
	} {
		invalid := mutate(originalSUP(t))
		require(t, os.WriteFile(badName, invalid, 0600))
		if s, err := proofreading.OpenSupplementary(ctx, w, d, "BAD.SUP"); err == nil || s != nil {
			t.Fatal("admitted unsupported, encrypted, or malformed SUP")
		}
		assertFile(t, badName, invalid)
	}
}

func TestSupplementaryCancelledStaleAmbiguousAndPermissionFailures(t *testing.T) {
	ctx := context.Background()
	path := t.TempDir()
	w, d := proofWorkspace(t, path)
	file := filepath.Join(path, "SPELLADD")
	initial := originalSUP(t)
	require(t, os.WriteFile(file, initial, 0600))
	s, err := proofreading.OpenSupplementary(ctx, w, d, "SPELLADD")
	require(t, err)

	canceled, cancel := context.WithCancel(ctx)
	cancel()
	if next, err := s.Add(canceled, "abloom", proofID(1)); next != nil || !errors.Is(err, context.Canceled) {
		t.Fatalf("cancellation not honored: %v", err)
	}
	assertFile(t, file, initial)

	changed := append(bytes.Clone(initial), []byte("another\n")...)
	require(t, os.WriteFile(file, changed, 0600))
	if next, err := s.Add(ctx, "abloom", proofID(2)); next != nil || err == nil {
		t.Fatal("stale Add overwrote a newer resource")
	}
	if next, err := s.Add(ctx, "zorbly", proofID(3)); next != nil || err == nil {
		t.Fatal("duplicate success concealed a stale resource")
	}
	assertFile(t, file, changed)

	fresh, err := proofreading.OpenSupplementary(ctx, w, d, "SPELLADD")
	require(t, err)
	alias := filepath.Join(path, "spelladd")
	require(t, os.WriteFile(alias, initial, 0600))
	if next, err := fresh.Add(ctx, "abloom", proofID(4)); next != nil || err == nil {
		t.Fatal("added to an ambiguous DOS name")
	}
	assertFile(t, file, changed)
	assertFile(t, alias, initial)
	require(t, os.Remove(alias))

	if os.Geteuid() != 0 {
		fresh, err = proofreading.OpenSupplementary(ctx, w, d, "SPELLADD")
		require(t, err)
		require(t, os.Chmod(path, 0500))
		defer func() { _ = os.Chmod(path, 0700) }()
		if next, err := fresh.Add(ctx, "abloom", proofID(5)); next != nil || err == nil {
			t.Fatal("read-only workspace publication falsely succeeded")
		}
		assertFile(t, file, changed)
	}
}

func TestSupplementaryConcurrentAddsUseOneSourceObservation(t *testing.T) {
	ctx := context.Background()
	path := t.TempDir()
	w, d := proofWorkspace(t, path)
	file := filepath.Join(path, "SPELLADD")
	initial := originalSUP(t)
	require(t, os.WriteFile(file, initial, 0600))
	s, err := proofreading.OpenSupplementary(ctx, w, d, "SPELLADD")
	require(t, err)
	var wg sync.WaitGroup
	type result struct {
		word string
		next *proofreading.Supplementary
		err  error
	}
	results := make(chan result, 2)
	for i, word := range []string{"acorn", "billow"} {
		wg.Go(func() {
			next, err := s.Add(ctx, word, proofID(uint64(i+1)))
			results <- result{word, next, err}
		})
	}
	wg.Wait()
	close(results)
	var winners []string
	for got := range results {
		if got.err == nil {
			if got.next == nil {
				t.Fatal("successful publication missing dictionary snapshot")
			}
			winners = append(winners, got.word)
		} else if got.next != nil {
			t.Fatal("failed publication adopted dictionary state")
		}
	}
	if len(winners) != 1 {
		t.Fatalf("expected one winner, got %v", winners)
	}
	assertFile(t, file, append(initial, []byte(winners[0]+"\n")...))
}
