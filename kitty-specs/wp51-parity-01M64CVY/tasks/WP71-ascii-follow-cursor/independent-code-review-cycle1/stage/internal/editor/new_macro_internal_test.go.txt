package editor

import (
	"context"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/storage"
)

// Structural adversaries supplement, rather than substitute for, external
// public-call positives. No synthetic Session is used as a positive target.
func newMacroInternal(t *testing.T) Session { t.Helper(); s, _ := newMacroInternalRoot(t); return s }
func newMacroInternalRoot(t *testing.T) (Session, string) {
	t.Helper()
	root := t.TempDir()
	dir, err := storage.OpenDirectory(root)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = dir.Close() })
	raw, err := os.ReadFile("../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
	if err != nil {
		t.Fatal(err)
	}
	if err = os.WriteFile(filepath.Join(root, "ROOT.WPM"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	s, err := New(Config{Locations: []Location{{Directory: dir}}})
	if err != nil {
		t.Fatal(err)
	}
	return s, root
}
func internalMacroPending(t *testing.T, s Session) (Session, *Intent) {
	t.Helper()
	var i *Intent
	var err error
	for _, event := range []Event{{Command: Macro}, {Command: Text, Text: "ROOT"}, {Command: Enter}} {
		s, i, err = s.Reduce(event)
		if err != nil {
			t.Fatal(err)
		}
	}
	return s, i
}
func TestNewMacroPrivateConstructorFacts(t *testing.T) {
	base := newMacroInternal(t)
	other := newMacroInternal(t)
	changes := map[string]func(*Session){
		"buffer": func(s *Session) { s.bufferID = nil }, "transition": func(s *Session) { s.transition = nil }, "phase": func(s *Session) { s.newPhase = NewAnchored },
		"genesis": func(s *Session) { s.genesis = other.genesis }, "source": func(s *Session) { s.source = &storage.Document{} }, "first": func(s *Session) { s.first = &firstPublication{} }, "other-screen": func(s *Session) { s.other = &other }, "screen": func(s *Session) { s.screen = 2 }, "revision": func(s *Session) { s.revision = 2 }, "sequence": func(s *Session) { s.sequence = 1 },
		"history-unknown": func(s *Session) { s.history = document.History{} }, "foreign-history": func(s *Session) { s.history = other.history }, "history-used": func(s *Session) { s.historyUsed = true }, "history-invalid": func(s *Session) { s.historyValid = false },
		"repeat": func(s *Session) { s.macroRepeat = 3 }, "ready": func(s *Session) { s.macroReady = &macroAcquisition{} }, "delivery": func(s *Session) { s.macroDelivery = true }, "pending": func(s *Session) { s.pending = &Intent{} },
		"name": func(s *Session) { s.name = "X" }, "draft": func(s *Session) { s.draft = "X" }, "original": func(s *Session) { s.original = "X" }, "caret": func(s *Session) { s.caret = 1 }, "target": func(s *Session) { s.target = &storage.Destination{} }, "target-dir": func(s *Session) { s.targetDir = s.locations[0].Directory }, "target-name": func(s *Session) { s.targetName = "X" }, "exit": func(s *Session) { s.fromExit = true }, "touched": func(s *Session) { s.touched = true }, "prefill": func(s *Session) { s.editedPrefill = true }, "provenance": func(s *Session) { s.provenance = F1 }, "saved": func(s *Session) { s.saved = s.genesis }, "publication": func(s *Session) { s.publishedRevision = s.genesis }, "published-name": func(s *Session) { s.publishedName = "X" }, "save-state": func(s *Session) { s.lastSave = SaveFailed }, "last": func(s *Session) { s.last.Applied = true }, "published": func(s *Session) { s.published.Applied = true }, "detached": func(s *Session) { s.detached.Candidate = "X" }, "notice": func(s *Session) { s.notice = "authentic refusal" },
	}
	for name, change := range changes {
		t.Run(name, func(t *testing.T) {
			s := base
			change(&s)
			if _, _, err := s.Reduce(Event{Command: Macro}); err == nil {
				t.Fatal("non-pristine private state accepted")
			}
		})
	}
}
func TestNewMacroPrivateIssuedReadyAndCurrentBindings(t *testing.T) {
	base, root := newMacroInternalRoot(t)
	waiting, i := internalMacroPending(t, base)
	result := ExecuteMacroRead(i)
	for _, stage := range []string{"issued-transition", "issued-target", "issued-native", "issued-repeat"} {
		t.Run(stage, func(t *testing.T) {
			s := waiting
			switch stage {
			case "issued-transition":
				s = s.advanced()
			case "issued-target":
				s.genesis = document.Revision{}
			case "issued-native":
				p := *s.pending
				p.NativeRevision = document.Revision{}
				s.pending = &p
			case "issued-repeat":
				p := *s.pending
				p.Repeat = 3
				s.pending = &p
			}
			if _, _, err := s.Reduce(Event{Command: Complete, Result: &result}); err == nil {
				t.Fatal("invalid issued root consumed")
			}
		})
	}
	ready, _, err := waiting.Reduce(Event{Command: Complete, Result: &result})
	if err != nil {
		t.Fatal(err)
	}
	for _, stage := range []string{"ready-transition", "ready-target", "ready-proof", "ready-observation", "ready-source", "ready-receipt"} {
		t.Run(stage, func(t *testing.T) {
			s := ready
			a := *s.macroReady
			s.macroReady = &a
			switch stage {
			case "ready-transition":
				s = s.advanced()
			case "ready-target":
				s.genesis = document.Revision{}
			case "ready-proof":
				p := *a.request.macroProof
				p.issued = nil
				a.request.macroProof = &p
			case "ready-observation":
				a.observation = nil
			case "ready-source":
				raw, err := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-03/CMD51-205/FLOW.WPM")
				if err != nil {
					t.Fatal(err)
				}
				if err = os.WriteFile(filepath.Join(root, "ROOT.WPM"), raw, 0600); err != nil {
					t.Fatal(err)
				}
				a.source, err = s.locations[0].Directory.ReadMacro("ROOT.WPM")
				if err != nil {
					t.Fatal(err)
				}
			case "ready-receipt":
				s.last = Receipt{}
			}
			if _, _, err := s.StartMacro(vm.DefaultLimits()); err == nil {
				t.Fatal("invalid ready target/source accepted")
			}
		})
	}
	active, run, err := ready.StartMacro(vm.DefaultLimits())
	if err != nil {
		t.Fatal(err)
	}
	for _, stage := range []string{"current-birth", "current-genesis", "current-source", "current-first", "current-phase", "current-native-other", "current-transition"} {
		t.Run(stage, func(t *testing.T) {
			s := active
			other := newMacroInternal(t)
			switch stage {
			case "current-birth":
				target := *s.newMacro
				target.birth = other.native.Birth()
				s.newMacro = &target
			case "current-genesis":
				s.genesis = document.Revision{}
			case "current-source":
				s.source = &storage.Document{}
			case "current-first":
				s.first = &firstPublication{}
			case "current-phase":
				s.newPhase = NewAnchored
			case "current-native-other":
				s.native = other.native
			case "current-transition":
				s = s.advanced()
			}
			if _, _, _, err := run.Step(context.Background(), s, 1); err == nil {
				t.Fatal("invalid current target accepted")
			}
			if _, _, err := run.HostStop(s, "invalid"); err == nil {
				t.Fatal("invalid stop target accepted")
			}
		})
	}
}

func TestNewMacroAdmissionStageLifetime(t *testing.T) {
	for _, stage := range []string{"name-f1", "pending-cancel", "detached", "ready-cancel", "terminal"} {
		t.Run(stage, func(t *testing.T) {
			s := newMacroInternal(t)
			switch stage {
			case "name-f1":
				s, _, _ = s.Reduce(Event{Command: Macro})
				s, _, _ = s.Reduce(Event{Command: F1})
			case "detached":
				s, _, _ = s.Reduce(Event{Command: Macro})
				r := Result{Kind: ReadMacro, Operation: 123}
				s, _, _ = s.Reduce(Event{Command: Complete, Result: &r})
				if _, _, err := s.Reduce(Event{Command: Enter}); err == nil {
					t.Fatal("detached name stage issued IO")
				}
			default:
				var i *Intent
				s, i = internalMacroPending(t, s)
				if stage == "pending-cancel" {
					s, _, _ = s.Reduce(Event{Command: CancelOperation})
				} else {
					r := ExecuteMacroRead(i)
					var err error
					s, _, err = s.Reduce(Event{Command: Complete, Result: &r})
					if err != nil {
						t.Fatal(err)
					}
					if stage == "ready-cancel" {
						s, _, _ = s.Reduce(Event{Command: CancelOperation})
					} else {
						var run *MacroExecution
						s, run, err = s.StartMacro(vm.DefaultLimits())
						if err != nil {
							t.Fatal(err)
						}
						s, _, err = run.HostStop(s, "lifetime")
						if err != nil {
							t.Fatal(err)
						}
					}
				}
			}
			if s.newMacro != nil {
				t.Fatal("released stage retained target admission")
			}
		})
	}
}
