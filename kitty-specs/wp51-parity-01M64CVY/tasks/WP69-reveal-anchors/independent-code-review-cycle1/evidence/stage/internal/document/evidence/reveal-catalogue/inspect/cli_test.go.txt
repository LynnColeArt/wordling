package inspect_test

import (
	"bytes"
	"encoding/json"
	"errors"
	host "github.com/lynncoleart/wordling/internal/document/evidence/reveal-catalogue/inspect"
	"io"
	"os"
	"path/filepath"
	"testing"
)

type failingWriter struct{ short bool }

func (w failingWriter) Write(b []byte) (int, error) {
	if w.short {
		return len(b) - 1, nil
	}
	return 0, errors.New("output failed")
}
func TestPublicRun(t *testing.T) {
	input := "../../../../../docs/research/continuation/text-layout/runs/wp14-r01-L1-HR/BASEA.WP5"
	var out, err bytes.Buffer
	if code := host.Run([]string{"-input", input}, &out, &err); code != 0 {
		t.Fatal(code, err.String())
	}
	var r map[string]json.RawMessage
	if e := json.Unmarshal(out.Bytes(), &r); e != nil {
		t.Fatal(e)
	}
	if !bytes.Contains(out.Bytes(), []byte(`[HRt]`)) || !bytes.Contains(out.Bytes(), []byte(`"unsupported":true`)) {
		t.Fatal(out.String())
	}
	before, e := os.ReadFile(input)
	if e != nil {
		t.Fatal(e)
	}
	out.Reset()
	err.Reset()
	if code := host.Run([]string{"-input", input}, &out, &err); code != 0 {
		t.Fatal(code, err.String())
	}
	after, _ := os.ReadFile(input)
	if !bytes.Equal(before, after) {
		t.Fatal("input changed")
	}
	for _, args := range [][]string{nil, {"-unknown"}, {"-input", input, "extra"}, {"-input", input, "-start", "-1"}, {"-input", input, "-count", "999999"}, {"-input", input, "-count", "-2"}} {
		out.Reset()
		err.Reset()
		if code := host.Run(args, &out, &err); code == 0 || out.Len() != 0 {
			t.Fatal("invalid CLI succeeded", args, code)
		}
	}
	for _, w := range []io.Writer{failingWriter{}, failingWriter{short: true}} {
		err.Reset()
		if code := host.Run([]string{"-input", input}, w, &err); code == 0 || err.Len() == 0 {
			t.Fatal("lost output failure")
		}
	}
	dir := t.TempDir()
	bad := filepath.Join(dir, "bad.wp5")
	if e := os.WriteFile(bad, []byte("malformed"), 0600); e != nil {
		t.Fatal(e)
	}
	link := filepath.Join(dir, "link.wp5")
	if e := os.Symlink(input, link); e != nil {
		t.Fatal(e)
	}
	large := filepath.Join(dir, "large.wp5")
	f, e := os.Create(large)
	if e != nil {
		t.Fatal(e)
	}
	if e = f.Truncate((16 << 20) + 1); e != nil {
		t.Fatal(e)
	}
	f.Close()
	for _, p := range []string{bad, link, large, dir, filepath.Join(dir, "absent")} {
		out.Reset()
		err.Reset()
		if code := host.Run([]string{"-input", p}, &out, &err); code == 0 || out.Len() != 0 {
			t.Fatal("invalid file succeeded", p, code)
		}
	}
}
