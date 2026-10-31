package tui

import (
	tea "charm.land/bubbletea/v2"
	"runtime"
	"testing"
	"time"
)

// This measures the real original finite loop through host workers and actual
// reducer effects. Wall times are observations, not callback-latency guarantees.
func TestMacroHostResourceObservation(t *testing.T) {
	r, m, root := macroLoaded(t)
	macroFile(t, root, "WHILELP.WPM", "docs/research/reference-runs/2026-10-29-history-02/CMD51-215/WHILELP.WPM")
	m, c := queuedMacro(t, m, "WHILELP")
	var before, after runtime.MemStats
	runtime.ReadMemStats(&before)
	started := time.Now()
	var workerMax, updateMax, resizeMax, viewMax time.Duration
	var maxAllocation uint64
	turns := 0
	for ; c != nil && turns < 1000; turns++ {
		prior := m.State().Macro.Steps
		var a, b runtime.MemStats
		runtime.ReadMemStats(&a)
		at := time.Now()
		msg := c()
		elapsed := time.Since(at)
		if elapsed > workerMax {
			workerMax = elapsed
		}
		runtime.ReadMemStats(&b)
		if b.TotalAlloc-a.TotalAlloc > maxAllocation {
			maxAllocation = b.TotalAlloc - a.TotalAlloc
		}
		at = time.Now()
		n, next := m.Update(msg)
		elapsed = time.Since(at)
		if elapsed > updateMax {
			updateMax = elapsed
		}
		m = n.(Model)
		c = next
		current := m.State().Macro.Steps
		if current > prior && current-prior > uint64(macroSliceQuota) {
			t.Fatal("slice expanded work quota", prior, current)
		}
		at = time.Now()
		n, extra := m.Update(tea.WindowSizeMsg{Width: 80, Height: 24})
		elapsed = time.Since(at)
		if elapsed > resizeMax {
			resizeMax = elapsed
		}
		m = n.(Model)
		if extra != nil {
			t.Fatal("resize starts work")
		}
		at = time.Now()
		_ = m.View()
		elapsed = time.Since(at)
		if elapsed > viewMax {
			viewMax = elapsed
		}
	}
	runtime.ReadMemStats(&after)
	if c != nil || m.State().Macro.Active || m.State().Macro.AppliedWords == 0 {
		t.Fatal("finite source did not complete", m.State())
	}
	elapsed := time.Since(started)
	at := time.Now()
	if e := r.Close(); e != nil {
		t.Fatal(e)
	}
	closeTime := time.Since(at)
	t.Logf("actual original WHILELP: workers=%d work=%d effects=%d total=%s worker_max=%s worker_alloc_max=%d update_max=%s resize_max=%s view_max=%s Close=%s total_alloc=%d mallocs=%d", turns, m.State().Macro.Steps, m.State().Macro.AppliedWords, elapsed, workerMax, maxAllocation, updateMax, resizeMax, viewMax, closeTime, after.TotalAlloc-before.TotalAlloc, after.Mallocs-before.Mallocs)
}
