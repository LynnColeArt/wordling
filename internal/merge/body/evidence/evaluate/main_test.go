package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"github.com/lynncoleart/wordling/internal/merge/native"
	"io"
	"os"
	"path/filepath"
	"testing"
)

func input(t *testing.T, id string) []byte {
	t.Helper()
	p := "../../../../../docs/research/reference-runs/2026-10-29-advanced-03/CMD51-" + id
	a, e := os.ReadFile(filepath.Join(p, "PRIMARY.WP5"))
	if e != nil {
		t.Fatal(e)
	}
	b, e := os.ReadFile(filepath.Join(p, "SECOND.WP5"))
	if e != nil {
		t.Fatal(e)
	}
	r, e := json.Marshal(map[string][]byte{"primary": a, "secondary": b})
	if e != nil {
		t.Fatal(e)
	}
	return r
}
func TestRunComputesAndRefusesAtomically(t *testing.T) {
	for _, id := range []string{"207", "209"} {
		var out bytes.Buffer
		if e := run(bytes.NewReader(input(t, id)), &out); e != nil {
			t.Fatal(e)
		}
		var r report
		if e := json.Unmarshal(out.Bytes(), &r); e != nil {
			t.Fatal(e)
		}
		want := []string{"Hello Alice\n", "Hello Bob\n"}
		if id == "209" {
			want = []string{"FILLED Alice", "EMPTY Bob"}
		}
		if len(r.Rows) != 2 {
			t.Fatal("rows")
		}
		for j, w := range want {
			if string(r.Rows[j].Body) != w {
				t.Fatal(string(r.Rows[j].Body))
			}
		}
	}
	for _, raw := range [][]byte{[]byte(`{}`), []byte(`{"primary":"YQ==","primary":"YQ==","secondary":"Yg=="}`), []byte(`{"primary":"YQ==","secondary":"Yg==","expected":"x"}`), append(input(t, "207"), []byte(`{}`)...), input(t, "208"), []byte(`{"primary":null,"secondary":"Yg=="}`), []byte(`[]`), bytes.Repeat([]byte{' '}, maxRequest+1)} {
		var out bytes.Buffer
		if e := run(bytes.NewReader(raw), &out); e == nil || out.Len() != 0 {
			t.Fatalf("not atomic %v %d", e, out.Len())
		}
	}
}

type shortWriter struct{}

func (shortWriter) Write(p []byte) (int, error) { return len(p) / 2, nil }

type failedWriter struct{}

func (failedWriter) Write(p []byte) (int, error) { return 1, errors.New("pipe failed") }
func TestOutputUncertaintyIsFailure(t *testing.T) {
	if e := run(bytes.NewReader(input(t, "207")), shortWriter{}); e != io.ErrShortWrite {
		t.Fatal(e)
	}
	if e := run(bytes.NewReader(input(t, "207")), failedWriter{}); e == nil {
		t.Fatal("failed writer")
	}
}

func TestConsumerCumulativeAndLateRefusal(t *testing.T) {
	raw := input(t, "209")
	var pair map[string][]byte
	if e := json.Unmarshal(raw, &pair); e != nil {
		t.Fatal(e)
	}
	// Compose authored host cases using authentic public spans, never an alternate parser.
	si, e := native.Parse(pair["secondary"], native.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	sv, e := si.View(native.Secondary)
	if e != nil {
		t.Fatal(e)
	}
	info, _ := sv.Inspect()
	first, _ := info.Tokens[0].Raw.Bounds()
	prefix := append([]byte(nil), pair["secondary"][:first.Offset]...)
	record := func(im *native.Image, r native.Record) []byte {
		b, ok := im.Bytes(r.Raw)
		if !ok {
			t.Fatal("record owner")
		}
		for _, s := range r.Interstitial {
			x, ok := im.Bytes(s)
			if !ok {
				t.Fatal("metadata owner")
			}
			b = append(b, x...)
		}
		return b
	}
	one := record(si, info.Records[0])
	for _, n := range []int{23, 33} {
		pair["secondary"] = append(append([]byte(nil), prefix...), bytes.Repeat(one, n)...)
		req, _ := json.Marshal(pair)
		var out bytes.Buffer
		if e := run(bytes.NewReader(req), &out); e == nil || out.Len() != 0 {
			t.Fatal("cumulative/record refusal", n, e)
		}
	}
	// A genuinely successful first209 record followed by207's missing field2
	// must not publish the earlier staged body.
	p207 := "../../../../../docs/research/reference-runs/2026-10-29-advanced-03/CMD51-207/SECOND.WP5"
	b, e := os.ReadFile(p207)
	if e != nil {
		t.Fatal(e)
	}
	im, e := native.Parse(b, native.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	v, e := im.View(native.Secondary)
	if e != nil {
		t.Fatal(e)
	}
	inf, _ := v.Inspect()
	pair["secondary"] = append(append(append([]byte(nil), prefix...), one...), record(im, inf.Records[0])...)
	req, _ := json.Marshal(pair)
	var out bytes.Buffer
	if e := run(bytes.NewReader(req), &out); e == nil || out.Len() != 0 {
		t.Fatal("late missing leaked", e)
	}
}
