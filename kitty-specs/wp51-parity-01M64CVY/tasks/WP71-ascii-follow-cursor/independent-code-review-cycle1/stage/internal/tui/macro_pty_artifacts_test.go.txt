package tui

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/wp51"
)

// The executable produces every actual file through normal UI/storage. This
// optional artifact-only comparator consumes the unchanged approved native
// reader; it is neither a serializer nor an alternate command implementation.
func TestMacroPTYNativeArtifacts(t *testing.T) {
	path := os.Getenv("WORDLING_WP37_PTY_MANIFEST")
	if path == "" {
		return
	}
	var manifest struct {
		Comparisons []struct {
			Actual, Expected, SHA256, Case string
			Exact                          bool
		}
	}
	raw, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	if err = json.Unmarshal(raw, &manifest); err != nil {
		t.Fatal(err)
	}
	if len(manifest.Comparisons) == 0 {
		t.Fatal("no actual native outputs")
	}
	for _, row := range manifest.Comparisons {
		t.Run(row.Case, func(t *testing.T) {
			actual, err := os.ReadFile(row.Actual)
			if err != nil {
				t.Fatal(err)
			}
			expectedPath := row.Expected
			if !filepath.IsAbs(expectedPath) {
				expectedPath = filepath.Join("../..", expectedPath)
			}
			expected, err := os.ReadFile(expectedPath)
			if err != nil {
				t.Fatal(err)
			}
			hash := sha256.Sum256(expected)
			if hex.EncodeToString(hash[:]) != row.SHA256 {
				t.Fatal("original source binding changed")
			}
			image, err := wp51.Parse(actual)
			if err != nil || !bytes.Equal(image.Export(), actual) {
				t.Fatal("actual native does not reopen losslessly", err)
			}
			if row.Exact {
				if !bytes.Equal(actual, expected) {
					t.Fatal("no-edit native differs")
				}
			} else {
				macroNative(t, actual, expected)
			}
		})
	}
}
