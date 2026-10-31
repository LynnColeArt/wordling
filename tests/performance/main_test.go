package main

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestMeasurementRetainsFailuresWarmupAndOutlier(t *testing.T) {
	calls := 0
	p := measure("test", 3, 1, func() error {
		calls++
		if calls == 3 {
			time.Sleep(2 * time.Millisecond)
			return os.ErrPermission
		}
		return nil
	})
	if calls != 4 || len(p.Warmup) != 1 || len(p.Samples) != 3 || p.Samples[1].Error == "" || p.Samples[1].NS < 1_000_000 {
		t.Fatal(p)
	}
}
func TestCountsRefuseUnboundedOrEmpty(t *testing.T) {
	for _, n := range []int{0, -1, 1001} {
		if validateCounts(n, 0) == nil {
			t.Fatal(n)
		}
	}
	for _, w := range []int{-1, 21} {
		if validateCounts(1, w) == nil {
			t.Fatal(w)
		}
	}
}
func TestActualCompositionPreservesSourceAndEveryPublication(t *testing.T) {
	path := filepath.Join(t.TempDir(), "INPUT")
	b, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(path, b, 0600); e != nil {
		t.Fatal(e)
	}
	r, e := run(path, 2, 1)
	if e != nil {
		t.Fatal(e)
	}
	if !r.SourceUnchanged || r.Publications != 3 || r.CompletedReceipts != 7 {
		t.Fatal(r)
	}
	for _, p := range r.Phases {
		if p.Skipped != "" {
			t.Fatal(p)
		}
		for _, s := range p.Samples {
			if s.Error != "" {
				t.Fatal(p)
			}
		}
	}
}
func TestMalformedIsRetainedRefusalNotZeroLatencySuccess(t *testing.T) {
	p := filepath.Join(t.TempDir(), "BAD")
	if e := os.WriteFile(p, []byte("bad"), 0600); e != nil {
		t.Fatal(e)
	}
	r, e := run(p, 2, 0)
	if e != nil {
		t.Fatal(e)
	}
	if !r.SourceUnchanged || r.Publications != 0 {
		t.Fatal(r)
	}
	for _, phase := range r.Phases {
		if phase.Name == "native_parse" && phase.Samples[0].Error == "" {
			t.Fatal(phase)
		}
	}
}
