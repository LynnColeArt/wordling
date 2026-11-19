//go:build wordling_qa

package storage

import (
	"encoding/json"
	"errors"
	"golang.org/x/sys/unix"
	"os"
	"path/filepath"
	"testing"
)

func TestQualificationBoundaryAndOneShot(t *testing.T) {
	for _, mode := range []string{"sync-error", "exchange-error"} {
		t.Run(mode, func(t *testing.T) {
			qualificationUsed.Store(false)
			defer qualificationUsed.Store(false)
			p := filepath.Join(t.TempDir(), "fault.json")
			t.Setenv("WORDLING_QA_SAVE_FAULT", mode)
			t.Setenv("WORDLING_QA_FAULT_RECORD", p)
			if err := qualificationFault("exchange", "ordinary", "TARGET.WP", 2); err != nil {
				t.Fatal(err)
			}
			if err := qualificationFault("exchange", ".wordling-candidate-test", "TARGET.WP", 1); err != nil {
				t.Fatal(err)
			}
			stage := "sync"
			if mode == "exchange-error" {
				stage = "exchange"
			}
			if err := qualificationFault(stage, ".wordling-candidate-test", "TARGET.WP", 2); !errors.Is(err, unix.EIO) {
				t.Fatal(err)
			}
			data, err := os.ReadFile(p)
			if err != nil {
				t.Fatal(err)
			}
			var record struct{ Mode, Stage string }
			if json.Unmarshal(data, &record) != nil || record.Mode != mode || record.Stage != stage {
				t.Fatal(string(data))
			}
			if err := qualificationFault(stage, ".wordling-candidate-test", "TARGET.WP", 2); err != nil {
				t.Fatal("fault repeated", err)
			}
		})
	}
}
