package editor_test

import (
	"bytes"
	"encoding/json"
	"github.com/lynncoleart/wordling/internal/editor"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// These are actual35 programs and real native candidates from the actual ordinary
// reducer. Erasing a loaded sourced target is not a blank-document constructor.
// Search remains blocked, never a synthetic injected NotFound success.
func TestOriginal09AllAvailableMacroContextsUseOrdinaryDocument(t *testing.T) {
	raw, e := os.ReadFile("../../internal/macro/runtime/testdata/original-cases.json")
	if e != nil {
		t.Fatal(e)
	}
	var corpus struct {
		Cases []struct {
			ID      string `json:"case_id"`
			Root    string `json:"root_macro"`
			Results []struct {
				Path string `json:"path"`
			} `json:"native_results"`
		} `json:"macro_cases"`
		Exports []struct {
			Path, Run string
			ID        string `json:"case_id"`
		} `json:"wpm_exports"`
	}
	if e = json.Unmarshal(raw, &corpus); e != nil {
		t.Fatal(e)
	}
	if len(corpus.Cases) != 20 || len(corpus.Exports) != 46 {
		t.Fatal("approved macro corpus identity")
	}
	for _, c := range corpus.Cases {
		for _, result := range c.Results {
			t.Run(c.ID+filepath.Base(filepath.Dir(filepath.Dir(result.Path))), func(t *testing.T) {
				original, e := os.ReadFile("../../" + result.Path)
				if e != nil {
					t.Fatal(e)
				}
				s, f := loadNative(t, original)
				count := s.Document().TokenCount()
				if c.ID == "CMD51-131" {
					count -= 3
				}
				for range count {
					s = key(t, s, editor.Delete)
				}
				if c.ID == "CMD51-131" {
					s = end(t, s)
				}
				if c.ID == "CMD51-132" {
					s, e = s.WithMacroRepeat(3)
					if e != nil {
						t.Fatal(e)
					}
				}
				for _, source := range corpus.Exports {
					if source.ID == c.ID && strings.Contains(result.Path, "/"+source.Run+"/") {
						data, e := os.ReadFile("../../" + source.Path)
						if e != nil {
							t.Fatal(e)
						}
						if e = os.WriteFile(filepath.Join(f.path, filepath.Base(source.Path)), data, 0600); e != nil {
							t.Fatal(e)
						}
					}
				}
				name := strings.TrimSuffix(c.Root, ".WPM")
				s = key(t, s, editor.Macro)
				s = text(t, s, "B:\\"+name)
				s, i := submit(t, s)
				s, _ = done(t, s, perform(i))
				before := s.Document().Revision()
				active, driver, e := s.StartMacro(vm.DefaultLimits())
				if c.ID == "CMD51-178" || c.ID == "CMD51-206" {
					if e == nil || driver != nil || active.Document().Revision() != before {
						t.Fatal("search/handler source falsely admitted without real editor search")
					}
					t.Log("explicit unsupported production search integration; original source preserved")
					return
				}
				if e != nil {
					t.Fatal(e)
				}
				active = runMacro(t, active, driver)
				candidate, _ := active.Document().Export()
				compareMacroNative(t, candidate, original)
				if !bytes.Equal(active.Source().Export(), original) {
					t.Fatal("loaded source guard/data changed")
				}
			})
		}
	}
}
