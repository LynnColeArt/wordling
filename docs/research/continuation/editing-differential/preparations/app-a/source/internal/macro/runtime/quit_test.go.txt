package runtime_test

import (
	"context"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"

	mac "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

type quitLedger struct {
	SourceCommit string `json:"source_commit"`
	SourceLedger string `json:"source_ledger_sha256"`
	Complete     int
	Incomplete   int `json:"incomplete_excluded"`
	Rows         []struct {
		Context, ID string
		Expected    struct {
			Before string `json:"before_manual"`
			After  string `json:"after_manual"`
			Other  string `json:"other_buffer"`
		}
		Files []artifact
	}
}

func quitCorpus(t testing.TB) quitLedger {
	t.Helper()
	raw, err := os.ReadFile("testdata/quit-cases.json")
	if err != nil {
		t.Fatal(err)
	}
	var a quitLedger
	if err = json.Unmarshal(raw, &a); err != nil {
		t.Fatal(err)
	}
	if a.SourceCommit != "419edc23d0739d490f2fd2c0094f5cc5eb0b1f80" || a.Complete != 4 || a.Incomplete != 2 || len(a.Rows) != 4 {
		t.Fatal("wrong approved39 corpus")
	}
	if a.SourceLedger != "406563d4d3438bcc4b9de5fbd0ba254dc4872bfa3cc1eea419aac47e82a82f6b" {
		t.Fatal("approved39 ledger binding changed")
	}
	ledger, err := os.ReadFile("../../../docs/research/continuation/macro-quit/observations.json")
	if err != nil {
		t.Fatal(err)
	}
	sum := sha256.Sum256(ledger)
	if hex.EncodeToString(sum[:]) != a.SourceLedger {
		t.Fatal("approved39 ledger changed")
	}
	return a
}
func TestApprovedNormalQuitOriginalReplays(t *testing.T) {
	for _, c := range quitCorpus(t).Rows {
		t.Run(c.ID, func(t *testing.T) {
			files := map[string]*wpm.Image{}
			sources := map[[32]byte][]byte{}
			docs := map[string]string{}
			for _, a := range c.Files {
				raw := readArtifact(t, a)
				name := filepath.Base(a.Path)
				if strings.HasSuffix(name, ".WPM") {
					i := image(t, raw)
					files[name] = i
					sources[i.SHA256()] = raw
				} else {
					B := binary.LittleEndian.Uint32(raw[4:8])
					docs[name] = string(raw[B:])
				}
			}
			rootName, want := "Q39R.WPM", "R39"
			if c.Context == "nested" {
				rootName, want = "Q39P.WPM", "P39C39"
			}
			if docs["QBEFORE.WP5"] != c.Expected.Before || docs["QAFTER.WP5"] != c.Expected.After || docs["QOTHER.WP5"] != c.Expected.Other || c.Expected.Before != "D1SENT DIRTY1"+want || c.Expected.After != c.Expected.Before+"READY" || c.Expected.Other != "D2SENT DIRTY2" {
				t.Fatal("actual native39 results changed", docs)
			}
			s := sink()
			calls := 0
			resolver := resolverFunc(func(_ context.Context, r mac.ProgramRequest) mac.Resolution {
				calls++
				if nativeName(r.Name) != "C:\\OUT\\Q39C" {
					t.Fatal("nested native identity", r)
				}
				return mac.Resolution{State: "ready", Image: files["Q39C.WPM"]}
			})
			p, err := mac.Compile(files[rootName], fullPolicy(), mac.DefaultLimits())
			if err != nil {
				t.Fatal(err)
			}
			m := newMachine(t, p, s, resolver, mac.DefaultLimits())
			r := drive(t, m, 3)
			if r.State != "complete" || r.Err != nil || literalProjection(s.receipts, sources) != want {
				t.Fatal("normal QUIT must stop all frames retaining delivered literals", r, literalProjection(s.receipts, sources))
			}
			if (c.Context == "nested" && calls != 1) || (c.Context == "root" && calls != 0) {
				t.Fatal("resolver calls", calls)
			}
			count := len(s.receipts)
			again := m.Step(context.Background(), 3)
			if again.State != "complete" || len(s.receipts) != count || again.Steps != r.Steps {
				t.Fatal("terminal QUIT replayed effects")
			}
			trace, err := json.Marshal(s.receipts)
			if err != nil {
				t.Fatal(err)
			}
			t.Logf("approved39 component sink receipts: %s", trace)
			checkEffectSources(t, s, sources)
		})
	}
}
