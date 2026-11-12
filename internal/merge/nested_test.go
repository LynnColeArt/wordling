package merge_test

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/merge"
)

func nestedFixture(t *testing.T, run, scenario, name string) []byte {
	t.Helper()
	raw, err := os.ReadFile(filepath.Join("../../docs/research/reference-runs", run, "CMD51-"+scenario, name+".WP5"))
	if err != nil {
		t.Fatal(err)
	}
	return raw
}

func TestRepeatedNestedPrimaryUsesOnePinnedRead(t *testing.T) {
	const run = "2026-10-29-iteration-01"
	primary, err := merge.CompilePrimary(nestedFixture(t, run, "223", "PRIMARY"))
	if err != nil {
		t.Fatal(err)
	}
	calls := 0
	resolve := func(parent, name string) (merge.Source, error) {
		calls++
		if parent != "P" || name != `C:\OUT\CHILD` {
			t.Fatalf("wrong child authority: %q in %q", name, parent)
		}
		return merge.Source{ID: "CHILD", Bytes: nestedFixture(t, run, "223", "CHILD")}, nil
	}
	d, err := merge.EvaluateWithSources(primary, "P", merge.Source{ID: "S", Bytes: nestedFixture(t, run, "223", "SECOND")}, resolve)
	if err != nil || calls != 1 {
		t.Fatalf("pinned child evaluation: reads=%d error=%v", calls, err)
	}
	b, _ := d.Export()
	at, _ := d.CursorAt(0)
	offset, _ := at.Offset()
	if got, want := string(b[offset:]), "PAlice\nCAlice\nR\n\fPBob\nCBob\nR\n"; got != want {
		t.Fatalf("nested record/page order: %q", got)
	}
}

func TestNestedMergeCyclesReturnNoFragment(t *testing.T) {
	for _, tc := range []struct {
		role, run, scenario string
	}{{"primary", "2026-10-29-iteration-01", "223"}, {"secondary", "2026-10-30-values-01", "233"}} {
		t.Run(tc.role, func(t *testing.T) {
			p := nestedFixture(t, tc.run, tc.scenario, "PRIMARY")
			s := nestedFixture(t, tc.run, tc.scenario, "SECOND")
			program, err := merge.CompilePrimary(p)
			if err != nil {
				t.Fatal(err)
			}
			resolve := func(parent, name string) (merge.Source, error) {
				if tc.role == "primary" {
					return merge.Source{ID: "P", Bytes: p}, nil
				}
				return merge.Source{ID: "S", Bytes: s}, nil
			}
			result, err := merge.EvaluateWithSources(program, "P", merge.Source{ID: "S", Bytes: s}, resolve)
			if result != nil || err == nil || !strings.Contains(err.Error(), "recursive "+tc.role) {
				t.Fatalf("cyclic merge published a fragment: %v", err)
			}
		})
	}
}

func TestPlainDocumentDoesNotAcquirePrimaryRole(t *testing.T) {
	program, err := merge.CompilePrimary(nestedFixture(t, "2026-10-29-iteration-01", "223", "MERGED"))
	if program.Valid() || err == nil {
		t.Fatal("ordinary result acquired primary execution")
	}
}
