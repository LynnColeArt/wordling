package storage_test

import (
	"bytes"
	"crypto/sha256"
	"errors"
	"fmt"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"path/filepath"
	"testing"
)

func BenchmarkPrepareNewPublication(b *testing.B) {
	raw, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5")
	if e != nil {
		b.Fatal(e)
	}
	d, e := storage.OpenDirectory(b.TempDir())
	if e != nil {
		b.Fatal(e)
	}
	defer d.Close()
	target, e := d.Observe("new")
	if e != nil {
		b.Fatal(e)
	}
	id := storage.PublicationID{Operation: 1, Revision: 1}
	b.ReportAllocs()
	b.ResetTimer()
	for n := 0; n < b.N; n++ {
		p, e := d.PrepareNewPublication(target, raw, id)
		if e != nil || p.Size() != len(raw) {
			b.Fatal(e)
		}
	}
}
func BenchmarkPublishNewRealFilesystem(b *testing.B) {
	raw, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5")
	if e != nil {
		b.Fatal(e)
	}
	d, e := storage.OpenDirectory(b.TempDir())
	if e != nil {
		b.Fatal(e)
	}
	defer d.Close()
	b.ReportAllocs()
	b.ResetTimer()
	for n := 0; n < b.N; n++ {
		target, e := d.Observe(fmt.Sprintf("new-%d", n))
		if e != nil {
			b.Fatal(e)
		}
		p, e := d.PrepareNewPublication(target, raw, storage.PublicationID{Operation: uint64(n + 1), Revision: 1})
		if e != nil {
			b.Fatal(e)
		}
		out, e := d.PublishNew(p, p.ID())
		if e != nil || out.State != storage.Published {
			b.Fatal(out, e)
		}
	}
}
func FuzzNewPublicationBoundary(f *testing.F) {
	raw, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5")
	if e != nil {
		f.Fatal(e)
	}
	f.Add(raw, byte(0))
	f.Add(raw, byte(1))
	f.Add(raw, byte(2))
	f.Add([]byte("malformed"), byte(0))
	f.Fuzz(func(t *testing.T, data []byte, flags byte) {
		if len(data) > 4096 {
			return
		}
		root := t.TempDir()
		d, e := storage.OpenDirectory(root)
		if e != nil {
			t.Fatal(e)
		}
		original := *d
		defer original.Close()
		target, e := d.Observe("first")
		if e != nil {
			t.Fatal(e)
		}
		id := storage.PublicationID{Operation: 1, Revision: 1}
		want := bytes.Clone(data)
		input := bytes.Clone(data)
		p, e := d.PrepareNewPublication(target, input, id)
		if e != nil {
			var failure *storage.Failure
			if !errors.As(e, &failure) {
				t.Fatal("untyped preparation refusal", e)
			}
			return
		}
		sum := sha256.Sum256(want)
		if p.Size() != len(want) || p.SHA256() != sum {
			t.Fatal("payload inspection mismatch")
		}
		clear(input)
		if flags&1 != 0 {
			other, e := d.Observe("second")
			if e != nil {
				t.Fatal(e)
			}
			*target = *other
		} else {
			*target = storage.Destination{}
		}
		if flags&2 != 0 {
			*d = storage.Directory{}
		}
		out, e := d.PublishNew(p, id)
		if flags&2 != 0 {
			if e == nil || out.State != "" {
				t.Fatal("zero receiver authorized IO")
			}
		} else {
			if e != nil || out.State != storage.Published {
				t.Fatal(out, e)
			}
			got, e := os.ReadFile(filepath.Join(root, "first"))
			if e != nil || !bytes.Equal(got, want) || out.Identity.SHA256 != sum {
				t.Fatal("prepared payload/target retargeted", e)
			}
		}
		if _, e = os.Stat(filepath.Join(root, "second")); !os.IsNotExist(e) {
			t.Fatal("substituted leaf touched", e)
		}
	})
}
