package tui

import (
	"bytes"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"slices"
	"sort"
	"strings"
	"syscall"
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
)

func TestRecoveryDecisionSurvivesCrashBeforeCleanup(t *testing.T) {
	t.Setenv("XDG_CACHE_HOME", t.TempDir())
	workspace := t.TempDir()
	open := func() (*recoveryStore, []recoveryRecord) {
		t.Helper()
		store, records, err := openRecovery(workspace)
		if err != nil {
			t.Fatal(err)
		}
		return store, records
	}
	first, _ := open()
	if err := first.write([]recoveryRecord{{ID: "selected"}, {ID: "unchecked"}}); err != nil {
		t.Fatal(err)
	}
	if err := first.close(false); err != nil {
		t.Fatal(err)
	}

	decision, originals := open()
	if len(originals) != 2 {
		t.Fatalf("want both original snapshots, got %v", originals)
	}
	decision.resolved = []string{"selected", "unchecked"}
	if err := decision.write([]recoveryRecord{{ID: "restored"}}); err != nil {
		t.Fatal(err)
	}
	// Stop after publishing the new session and before touching the old one.
	if err := decision.close(false); err != nil {
		t.Fatal(err)
	}

	restarted, records := open()
	defer restarted.close(true)
	if len(records) != 1 || records[0].ID != "restored" {
		t.Fatalf("expected only committed restored copy, got %v", records)
	}
	if err := restarted.resolve(); err != nil {
		t.Fatal(err)
	}
}

func TestConfirmedRecoveryCrashBoundaries(t *testing.T) {
	if boundary := os.Getenv("WORDLING_TEST_RECOVERY_CRASH"); boundary != "" {
		_, model, err := Open(Config{Root: os.Getenv("WORDLING_TEST_RECOVERY_ROOT"), Profile: LocalFlat, EditorChrome: true})
		if err != nil {
			t.Fatal(err)
		}
		model = model.EnableRecovery(os.Getenv("WORDLING_TEST_RECOVERY_ROOT"))
		if len(model.recovery.entries) != 5 {
			t.Fatalf("expected five documents, got %d", len(model.recovery.entries))
		}
		model = inputKeys(t, model, everydayKey(tea.KeyDown), textKey(" "),
			everydayKey(tea.KeyDown), everydayKey(tea.KeyDown), textKey(" "), everydayKey(tea.KeyEnter))
		if !model.recovery.confirm {
			t.Fatal("deletion confirmation did not open")
		}
		crash := func() {
			fmt.Println("reached recovery boundary:", boundary)
			if err := syscall.Kill(os.Getpid(), syscall.SIGKILL); err != nil {
				t.Fatal(err)
			}
		}
		switch boundary {
		case "before-commit":
			model.recovery.store.beforePublish = crash
		case "after-commit":
			model.recovery.store.beforeCleanup = crash
		default:
			t.Fatalf("unknown boundary %q", boundary)
		}
		inputKeys(t, model, textKey("y"))
		t.Fatal("confirmed recovery did not reach the crash boundary")
	}

	for _, tc := range []struct {
		boundary string
		want     []string
	}{
		{"before-commit", []string{"FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH"}},
		{"after-commit", []string{"FIRST", "THIRD", "FIFTH"}},
	} {
		t.Run(tc.boundary, func(t *testing.T) {
			t.Setenv("XDG_CACHE_HOME", t.TempDir())
			model, root := everydayUI(t)
			store, _, err := openRecovery(root)
			if err != nil {
				t.Fatal(err)
			}
			var originals []recoveryRecord
			for i, name := range []string{"FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH"} {
				_, fresh, err := Open(Config{Root: root, Profile: LocalFlat, EditorChrome: true})
				if err != nil {
					t.Fatal(err)
				}
				t.Cleanup(func() { _ = fresh.runtime.Close() })
				fresh = inputKeys(t, fresh, textKey(name))
				originals = append(originals, recoveryRecord{
					ID: name, Name: name, Time: time.Unix(int64(5-i), 0), Native: hBoldNative(t, fresh),
				})
			}
			if err := store.write(originals); err != nil {
				t.Fatal(err)
			}
			if err := store.close(false); err != nil {
				t.Fatal(err)
			}
			cmd := exec.Command(os.Args[0], "-test.run=^TestConfirmedRecoveryCrashBoundaries$")
			cmd.Env = append(os.Environ(), "WORDLING_TEST_RECOVERY_CRASH="+tc.boundary, "WORDLING_TEST_RECOVERY_ROOT="+root)
			output, err := cmd.CombinedOutput()
			var exit *exec.ExitError
			if !errors.As(err, &exit) || exit.Sys().(syscall.WaitStatus).Signal() != syscall.SIGKILL ||
				!strings.Contains(string(output), "reached recovery boundary: "+tc.boundary) {
				t.Fatalf("expected SIGKILL at %s, got %v\n%s", tc.boundary, err, output)
			}
			model = model.EnableRecovery(root)
			defer model.CloseRecovery(false)
			var got []string
			for _, record := range model.recovery.entries {
				got = append(got, record.Name)
				for _, original := range originals {
					if record.Name == original.Name && !bytes.Equal(record.Native, original.Native) {
						t.Fatalf("%s content changed", record.Name)
					}
				}
			}
			sort.Strings(got)
			sort.Strings(tc.want)
			if !slices.Equal(got, tc.want) {
				t.Fatalf("restart offered %v, want %v", got, tc.want)
			}
		})
	}
}
