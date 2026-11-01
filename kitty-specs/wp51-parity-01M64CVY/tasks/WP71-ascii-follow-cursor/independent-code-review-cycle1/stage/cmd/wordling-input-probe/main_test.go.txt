package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"sync"
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
)

type failedWriter struct{}

func (failedWriter) Write([]byte) (int, error) { return 0, io.ErrClosedPipe }

func TestJournalFailureStopsProbe(t *testing.T) {
	j := &journal{start: time.Now(), encoder: json.NewEncoder(failedWriter{})}
	m := model{journal: j}
	_, cmd := m.Update(tea.KeyPressMsg{Code: 'q', Text: "q"})
	if !errors.Is(j.failure(), io.ErrClosedPipe) || cmd == nil {
		t.Fatal("lost evidence failure")
	}
	if _, ok := cmd().(tea.QuitMsg); !ok {
		t.Fatal("failed journal should stop")
	}
}

func TestNoInventedQuitBinding(t *testing.T) {
	var b bytes.Buffer
	j := &journal{start: time.Now(), encoder: json.NewEncoder(&b)}
	m := model{journal: j, enhanced: true}
	for _, k := range []tea.Key{{Code: 'q', Text: "q"}, {Code: 'q', Mod: tea.ModCtrl}, {Code: 's', Mod: tea.ModCtrl}, {Code: tea.KeyEscape}, {Code: tea.KeyF7}} {
		_, cmd := m.Update(tea.KeyPressMsg(k))
		if cmd != nil {
			t.Fatalf("invented probe key action %#v", k)
		}
	}
	_, cmd := m.Update(finish{})
	if cmd == nil {
		t.Fatal("deadline must stop")
	}
	v := m.View()
	if !v.KeyboardEnhancements.ReportEventTypes || !v.KeyboardEnhancements.ReportAllKeysAsEscapeCodes {
		t.Fatal("enhancements not requested")
	}
	if (model{}).View().KeyboardEnhancements.ReportAllKeysAsEscapeCodes {
		t.Fatal("legacy requests enhanced flags")
	}
}

func TestJournalOrdersConcurrentStreams(t *testing.T) {
	var b bytes.Buffer
	j := &journal{start: time.Now(), encoder: json.NewEncoder(&b)}
	var wg sync.WaitGroup
	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for n := 0; n < 100; n++ {
				if err := j.add("test", n); err != nil {
					t.Error(err)
				}
			}
		}()
	}
	wg.Wait()
	d := json.NewDecoder(&b)
	var prev int64
	for n := 1; n <= 300; n++ {
		var r record
		if err := d.Decode(&r); err != nil {
			t.Fatal(err)
		}
		if r.Sequence != uint64(n) || r.Nanoseconds < prev {
			t.Fatalf("disordered journal: %#v", r)
		}
		prev = r.Nanoseconds
	}
	if j.failure() != nil {
		t.Fatal(j.failure())
	}
}
