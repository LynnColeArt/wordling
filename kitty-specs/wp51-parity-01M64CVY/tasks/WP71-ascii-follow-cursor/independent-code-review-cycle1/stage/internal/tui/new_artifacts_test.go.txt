package tui

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
)

// Optional actual executable-output comparator, never a serializer/fixture producer.
func TestNewPTYWholeNativeArtifacts(t *testing.T) {
	path := os.Getenv("WORDLING_WP48_PTY_RESULTS")
	if path == "" {
		return
	}
	var reports []struct {
		Outputs []struct {
			Actual, Kind, SHA256 string
			Size                 int
		}
	}
	raw, e := os.ReadFile(path)
	if e != nil {
		t.Fatal(e)
	}
	if e = json.Unmarshal(raw, &reports); e != nil {
		t.Fatal(e)
	}
	count := 0
	for _, report := range reports {
		for _, row := range report.Outputs {
			t.Run(filepath.Base(filepath.Dir(filepath.Dir(row.Actual)))+"-"+filepath.Base(row.Actual), func(t *testing.T) {
				actual, e := os.ReadFile(row.Actual)
				if e != nil {
					t.Fatal(e)
				}
				if row.Kind == "external-interference" {
					if len(actual) != row.Size+1 {
						t.Fatal("external mutation premise")
					}
					return
				}
				h := sha256.Sum256(actual)
				if len(actual) != row.Size || hex.EncodeToString(h[:]) != row.SHA256 {
					t.Fatal("actual executable artifact changed")
				}
				image, e := wp51.Parse(actual)
				if e != nil || !bytes.Equal(image.Export(), actual) {
					t.Fatal("public framing reopen", e)
				}
				d, e := document.Parse(actual)
				if e != nil || !d.Birth().IsLoaded() {
					t.Fatal("actual file reload not Loaded", e)
				}
				loaded, e := d.OriginalExport()
				if e != nil || !bytes.Equal(loaded, actual) {
					t.Fatal("loaded original loss", e)
				}
				switch row.Kind {
				case "empty", "ascii":
					expected, e := os.ReadFile("../document/evidence/wp46/candidates/" + row.Kind + ".WP5")
					if e != nil || !bytes.Equal(actual, expected) {
						t.Fatal("not the qualified whole-byte class", e)
					}
				case "ascii-Z":
					expectedASCII, e := os.ReadFile("../document/evidence/wp46/candidates/ascii.WP5")
					if e != nil {
						t.Fatal(e)
					}
					if !bytes.Equal(actual, append(bytes.Clone(expectedASCII), 'Z')) {
						t.Fatal("subsequent edit changed unrelated whole native bytes")
					}
					for _, rep := range []string{"r1", "r2"} {
						expected, e := os.ReadFile("../document/evidence/wp46/runs/wp46-phase02/wp46-ascii-edit-candidate-" + rep + "/C46PRE.WP5")
						if e != nil {
							t.Fatal(e)
						}
						original, e := wp51.Parse(expected)
						if e != nil {
							t.Fatal(e)
						}
						// Original Save relocates indexed packets. Compare ALL checked owners,
						// including complete prefix coverage, rather than masking whole-file diffs.
						a, b := image.Inspect(), original.Inspect()
						if !bytes.Equal(actual[:16], expected[:16]) || a.Body != b.Body || len(a.Packets) != len(b.Packets) {
							t.Fatal("unexplained header/extent")
						}
						body, _ := image.Bytes(a.Body)
						ob, _ := original.Bytes(b.Body)
						if !bytes.Equal(body, ob) {
							t.Fatal("original subsequent edit differs")
						}
						for _, im := range []*wp51.Image{image, original} {
							coverage := make([]bool, im.Inspect().Body.Offset)
							mark := func(s wp51.Span) {
								for i := s.Offset; i < s.Offset+s.Length; i++ {
									if i >= len(coverage) || coverage[i] {
										t.Fatal("overlap/outside owner")
									}
									coverage[i] = true
								}
							}
							mark(wp51.Span{Offset: 0, Length: 16})
							for _, v := range im.Inspect().Blocks {
								mark(v.Data)
							}
							for _, v := range im.Inspect().Packets {
								mark(v.Data)
							}
							for _, v := range coverage {
								if !v {
									t.Fatal("unexplained prefix byte")
								}
							}
						}
						for _, p := range a.Packets {
							var matches []wp51.Packet
							for _, q := range b.Packets {
								if p.Type == q.Type {
									matches = append(matches, q)
								}
							}
							if len(matches) != 1 {
								t.Fatal("ambiguous owner")
							}
							av, _ := image.Bytes(p.Data)
							bv, _ := original.Bytes(matches[0].Data)
							if p.Type == 6 {
								if av[0] != 8 || bv[0] != 0 {
									t.Fatal("must-format premise")
								}
								av[0] = bv[0]
							}
							if !bytes.Equal(av, bv) {
								t.Fatal("unexplained owned payload difference", p.Type)
							}
						}
					}
				case "loaded-macro":
					body, ok := image.Bytes(image.Inspect().Body)
					if !ok || !bytes.HasPrefix(body, []byte("ABC")) {
						t.Fatal("actual macro effects absent")
					}
				default:
					t.Fatal("unqualified artifact kind", row.Kind)
				}
				count++
			})
		}
	}
	if count < 10 {
		t.Fatal("missing actual executable artifacts", count)
	}
}
