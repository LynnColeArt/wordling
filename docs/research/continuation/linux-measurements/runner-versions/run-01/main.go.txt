// Command performance measures the actual bounded composition; it is not an editor.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"syscall"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
	"github.com/lynncoleart/wordling/internal/tui"
	"github.com/lynncoleart/wordling/internal/wp51"
)

type sample struct {
	NS         int64  `json:"ns"`
	AllocBytes uint64 `json:"alloc_bytes"`
	Allocs     uint64 `json:"allocs"`
	Error      string `json:"error,omitempty"`
}
type phase struct {
	Name    string   `json:"name"`
	Warmup  []sample `json:"warmup"`
	Samples []sample `json:"samples"`
	Skipped string   `json:"skipped,omitempty"`
}
type report struct {
	Fixture           string            `json:"fixture"`
	Size              int               `json:"size"`
	SHA256            string            `json:"sha256"`
	TokenCount        int               `json:"token_count"`
	Phases            []phase           `json:"phases"`
	RSS               map[string]string `json:"rss"`
	PeakRSSKiB        int64             `json:"process_peak_rss_kib"`
	SourceUnchanged   bool              `json:"source_unchanged"`
	Publications      int               `json:"publications"`
	CompletedReceipts int               `json:"completed_receipts"`
	View              string            `json:"last_view"`
}

func digest(b []byte) string { h := sha256.Sum256(b); return hex.EncodeToString(h[:]) }
func rss() map[string]string {
	b, e := os.ReadFile("/proc/self/status")
	if e != nil {
		panic(e)
	}
	v := map[string]string{}
	for _, l := range strings.Split(string(b), "\n") {
		for _, k := range []string{"VmRSS:", "VmHWM:", "Cpus_allowed_list:"} {
			if strings.HasPrefix(l, k) {
				v[strings.TrimSuffix(k, ":")] = strings.TrimSpace(strings.TrimPrefix(l, k))
			}
		}
	}
	return v
}
func measure(name string, n, w int, fn func() error) phase {
	p := phase{Name: name}
	for i := 0; i < n+w; i++ {
		var a, b runtime.MemStats
		runtime.ReadMemStats(&a)
		t := time.Now()
		e := fn()
		elapsed := time.Since(t).Nanoseconds()
		runtime.ReadMemStats(&b)
		s := sample{NS: elapsed, AllocBytes: b.TotalAlloc - a.TotalAlloc, Allocs: b.Mallocs - a.Mallocs}
		if e != nil {
			s.Error = e.Error()
		}
		if i < w {
			p.Warmup = append(p.Warmup, s)
		} else {
			p.Samples = append(p.Samples, s)
		}
	}
	return p
}
func press(m tui.Model, code rune, mod tea.KeyMod, text string) (tui.Model, tea.Cmd) {
	next, c := m.Update(tea.KeyPressMsg(tea.Key{Code: code, Mod: mod, Text: text}))
	return next.(tui.Model), c
}
func drain(m tui.Model, c tea.Cmd) (tui.Model, error) {
	for i := 0; c != nil; i++ {
		if i >= 8 {
			return m, errors.New("measurement drain bound")
		}
		next, n := m.Update(c())
		m, c = next.(tui.Model), n
	}
	return m, nil
}
func load(m tui.Model) (tui.Model, error) {
	m, _ = press(m, tea.KeyF10, tea.ModShift, "")
	m, _ = press(m, 'S', 0, "SOURCE")
	m, c := press(m, tea.KeyEnter, 0, "")
	return drain(m, c)
}
func validateCounts(n, w int) error {
	if n < 1 || n > 1000 || w < 0 || w > 20 {
		return errors.New("samples must be1..1000 and warmup0..20")
	}
	return nil
}
func run(path string, n, w int) (report, error) {
	if e := validateCounts(n, w); e != nil {
		return report{}, e
	}
	raw, e := os.ReadFile(path)
	if e != nil {
		return report{}, e
	}
	r := report{Fixture: path, Size: len(raw), SHA256: digest(raw), TokenCount: -1, RSS: map[string]string{}}
	work, e := os.MkdirTemp("", "wordling-performance-")
	if e != nil {
		return r, e
	}
	defer os.RemoveAll(work)
	if e = os.WriteFile(filepath.Join(work, "SOURCE"), raw, 0600); e != nil {
		return r, e
	}
	runtime.GC()
	for k, v := range rss() {
		r.RSS["before_"+k] = v
	}
	var image *wp51.Image
	r.Phases = append(r.Phases, measure("native_parse", n, w, func() error { var e error; image, e = wp51.Parse(raw); return e }))
	if image != nil {
		r.TokenCount = image.Inspect().OuterTokenCount
		if !bytes.Equal(image.Export(), raw) {
			return r, errors.New("parser changed source")
		}
	}
	dir, e := storage.OpenDirectory(work)
	if e != nil {
		return r, e
	}
	defer dir.Close()
	var stored *storage.Document
	r.Phases = append(r.Phases, measure("rooted_read_native_parse", n, w, func() error { var e error; stored, e = dir.Read("SOURCE"); return e }))
	if stored != nil && !bytes.Equal(stored.Export(), raw) {
		return r, errors.New("storage changed source")
	}
	var d *document.Document
	r.Phases = append(r.Phases, measure("document_construction", n, w, func() error { var e error; d, e = document.Parse(raw); return e }))
	if d != nil {
		r.Phases = append(r.Phases, measure("all_token_traversal", n, w, func() error {
			sum := 0
			for i := 0; i < d.TokenCount(); i++ {
				t, e := d.Token(i)
				if e != nil {
					return e
				}
				sum += len(t.Raw)
			}
			if sum != len(raw)-image.Inspect().Body.Offset {
				return errors.New("traversal byte mismatch")
			}
			return nil
		}))
		var exported []byte
		r.Phases = append(r.Phases, measure("no_edit_export", n, w, func() error { var e error; exported, e = d.Export(); return e }))
		if !bytes.Equal(exported, raw) {
			return r, errors.New("export changed source")
		}
	}
	r.Phases = append(r.Phases, measure("runtime_open_close", n, w, func() error {
		rt, _, e := tui.Open(tui.Config{Root: work, Profile: tui.LocalFlat})
		if e != nil {
			return e
		}
		return rt.Close()
	}))
	// A fresh real Runtime per retrieve avoids reusing or forking operation IDs.
	r.Phases = append(r.Phases, measure("composition_open_retrieve_close", n, w, func() error {
		rt, m, e := tui.Open(tui.Config{Root: work, Profile: tui.LocalFlat})
		if e != nil {
			return e
		}
		m, e = load(m)
		closed := rt.Close()
		if e != nil {
			return e
		}
		if closed != nil {
			return closed
		}
		if m.Session().Source() == nil {
			return fmt.Errorf("retrieval refused: %s", m.State().Session.Notice)
		}
		return nil
	}))
	rt, m, e := tui.Open(tui.Config{Root: work, Profile: tui.LocalFlat})
	if e != nil {
		return r, e
	}
	defer rt.Close()
	resized, _ := m.Update(tea.WindowSizeMsg{Width: 100, Height: 25})
	m = resized.(tui.Model)
	m, e = load(m)
	if e != nil {
		return r, e
	}
	if m.Session().Source() != nil {
		s := m.Session()
		r.Phases = append(r.Phases, measure("reducer_reveal_event", n, w, func() error {
			var intent *editor.Intent
			var e error
			s, intent, e = s.Reduce(editor.Event{Command: editor.Reveal})
			if intent != nil {
				return errors.New("unexpected IO from Reveal")
			}
			return e
		}))
		r.Phases = append(r.Phases, measure("model_update_reveal", n, w, func() error { m, _ = press(m, tea.KeyF3, tea.ModAlt, ""); return nil }))
		r.Phases = append(r.Phases, measure("model_view_100x25", n, w, func() error { r.View = m.View().Content; return nil }))
		index := 0
		r.Phases = append(r.Phases, measure("composition_newname_publication", n, w, func() error {
			index++
			name := "COPY" + strconv.Itoa(index)
			m, _ = press(m, tea.KeyF10, 0, "")
			m, _ = press(m, 'C', 0, name)
			var c tea.Cmd
			m, c = press(m, tea.KeyEnter, 0, "")
			var err error
			m, err = drain(m, c)
			if err != nil {
				return err
			}
			if m.State().Session.SaveState != editor.NewNamePublished {
				return fmt.Errorf("publication refused: %+v", m.State())
			}
			return nil
		}))
		for i := 1; i <= index; i++ {
			p, e := os.ReadFile(filepath.Join(work, "COPY"+strconv.Itoa(i)))
			if e != nil || !bytes.Equal(p, raw) {
				return r, fmt.Errorf("publication bytes %d: %v", i, e)
			}
			r.Publications++
		}
	} else {
		r.Phases = append(r.Phases, phase{Name: "loaded_model_phases", Skipped: "model retrieval refused: " + m.State().Session.Notice})
	}
	r.CompletedReceipts = len(rt.Completed())
	if e := rt.Close(); e != nil {
		return r, e
	}
	runtime.GC()
	for k, v := range rss() {
		r.RSS["after_"+k] = v
	}
	var usage syscall.Rusage
	if e = syscall.Getrusage(syscall.RUSAGE_SELF, &usage); e != nil {
		return r, e
	}
	r.PeakRSSKiB = usage.Maxrss
	after, e := os.ReadFile(filepath.Join(work, "SOURCE"))
	if e != nil {
		return r, e
	}
	fixture, e := os.ReadFile(path)
	if e != nil {
		return r, e
	}
	r.SourceUnchanged = bytes.Equal(after, raw) && bytes.Equal(fixture, raw)
	if !r.SourceUnchanged {
		return r, errors.New("measurement modified source")
	}
	return r, nil
}
func main() {
	path := flag.String("fixture", "", "exact native input")
	n := flag.Int("samples", 31, "retained samples per phase")
	w := flag.Int("warmup", 3, "separately retained warmups")
	out := flag.String("output", "", "new report path")
	flag.Parse()
	if *out == "" {
		panic("output required")
	}
	r, e := run(*path, *n, *w)
	if e != nil {
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
	raw, e := json.MarshalIndent(r, "", "  ")
	if e != nil {
		panic(e)
	}
	f, e := os.OpenFile(*out, os.O_CREATE|os.O_EXCL|os.O_WRONLY, 0600)
	if e != nil {
		panic(e)
	}
	if _, e = f.Write(append(raw, '\n')); e != nil {
		panic(e)
	}
	if e = f.Close(); e != nil {
		panic(e)
	}
}
