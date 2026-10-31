package tui

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
)

func TestAllAcceptedOriginalsThroughActualModelAndStorage(t *testing.T) {
	var corpus struct {
		Fixtures []struct {
			ID, Path, SHA256 string
			Size             int `json:"size_bytes"`
		}
	}
	raw, e := os.ReadFile("../../kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json")
	if e != nil {
		t.Fatal(e)
	}
	if e = json.Unmarshal(raw, &corpus); e != nil {
		t.Fatal(e)
	}
	for _, f := range corpus.Fixtures {
		t.Run(f.ID, func(t *testing.T) {
			native, e := os.ReadFile("../../" + f.Path)
			if e != nil {
				t.Fatal(e)
			}
			sum := sha256.Sum256(native)
			if len(native) != f.Size || hex.EncodeToString(sum[:]) != f.SHA256 {
				t.Fatal("source fingerprint changed")
			}
			root := t.TempDir()
			if e = os.WriteFile(filepath.Join(root, "SOURCE"), native, 0600); e != nil {
				t.Fatal(e)
			}
			r, m, e := Open(Config{Root: root, Profile: LocalFlat})
			if e != nil {
				t.Fatal(e)
			}
			defer r.Close()
			m, _ = press(m, tea.KeyF10, tea.ModShift, "")
			m, _ = press(m, 'S', tea.ModShift, "SOURCE")
			m, c := press(m, tea.KeyEnter, 0, "")
			m = drain(m, c)
			if f.ID == "macro" {
				if m.Session().Source() != nil || m.Session().Snapshot().Notice == "" {
					t.Fatal("macro not refused")
				}
				return
			}
			if m.Session().Source() == nil {
				t.Fatal(m.State())
			}
			if strings.Contains(m.View().Content, "Unsupported document presentation") {
				t.Log("Opaque original explicitly refuses presentation while preserving its entire snapshot")
			}
			m, _ = press(m, tea.KeyF10, 0, "")
			m, _ = press(m, 'C', tea.ModShift, "COPY")
			m, c = press(m, tea.KeyEnter, 0, "")
			m = drain(m, c)
			if m.Session().Snapshot().SaveState != editor.NewNamePublished {
				t.Fatal(m.State())
			}
			for _, name := range []string{"SOURCE", "COPY"} {
				b, e := os.ReadFile(filepath.Join(root, name))
				if e != nil || string(b) != string(native) {
					t.Fatal("byte preservation", name, e)
				}
			}
			out, _ := m.Session().Document().Export()
			out[0] ^= 1
			again, _ := m.Session().Document().Export()
			if string(again) != string(native) {
				t.Fatal("view export aliased native")
			}
			t.Logf("%s source/published/export bytes=%d sha256=%s exact", f.ID, len(native), f.SHA256)
		})
	}
}
