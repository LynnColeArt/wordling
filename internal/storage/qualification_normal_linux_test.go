//go:build !wordling_qa

package storage

import (
	"os"
	"path/filepath"
	"testing"
)

func TestNormalBuildCannotActivateQualificationFault(t *testing.T) {
	p := filepath.Join(t.TempDir(), "must-not-exist")
	t.Setenv("WORDLING_QA_FAULT_RECORD", p)
	for _, mode := range []string{"sync-error", "exchange-error", "exchange-crash"} {
		t.Setenv("WORDLING_QA_SAVE_FAULT", mode)
		if err := qualificationFault("sync", ".wordling-candidate-test", "", 0); err != nil {
			t.Fatal(err)
		}
		if err := qualificationFault("exchange", ".wordling-candidate-test", "TARGET.WP", 2); err != nil {
			t.Fatal(err)
		}
	}
	if _, err := os.Stat(p); !os.IsNotExist(err) {
		t.Fatal("normal build created QA evidence", err)
	}
}
