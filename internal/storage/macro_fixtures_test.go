package storage_test

import (
	"crypto/sha1"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"testing"
)

type macroFixture struct {
	Path, SHA256, GitBlob string
	Size                  int
}

func macroFixtures(t testing.TB) []macroFixture {
	t.Helper()
	b, err := os.ReadFile("../macro/wpm/testdata/original-fixtures.json")
	if err != nil {
		t.Fatal(err)
	}
	var ledger struct {
		Source  string `json:"source_ledger_sha256"`
		Exports []struct {
			Path    string `json:"path"`
			SHA256  string `json:"sha256"`
			GitBlob string `json:"git_blob"`
			Size    int    `json:"size"`
		} `json:"wpm_exports"`
	}
	if err := json.Unmarshal(b, &ledger); err != nil {
		t.Fatal(err)
	}
	if len(ledger.Exports) != 46 || ledger.Source != "fca8446e98ad95ab118fc672e48e821afc65e9e3b2b5a43c27f7759824c2ce5d" {
		t.Fatal("wrong approved corpus source")
	}
	var out []macroFixture
	for _, f := range ledger.Exports {
		out = append(out, macroFixture{f.Path, f.SHA256, f.GitBlob, f.Size})
	}
	return out
}
func macroBytes(t testing.TB, f macroFixture) []byte {
	t.Helper()
	b, err := os.ReadFile(filepath.Join("../..", f.Path))
	if err != nil {
		t.Fatal(err)
	}
	if len(b) != f.Size || fmtHash(b) != f.SHA256 {
		t.Fatal("original WPM evidence changed", f.Path)
	}
	blob := sha1.Sum(append([]byte(fmt.Sprintf("blob %d\x00", len(b))), b...))
	if hex.EncodeToString(blob[:]) != f.GitBlob {
		t.Fatal("original Git blob changed")
	}
	return b
}
