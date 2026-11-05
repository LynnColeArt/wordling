# WP90 independent review — APPROVE

Reviewer: `/root/everyday_baseline_audit`, independent of the repair implementer. Runtime-assigned agent identity remains `codex`; this document records the actual reviewer separation.
Issued review invocation: `f7e339e23afd4b79a7142d6bafc8202a`.
Reviewed fixed source: `78a05497dcf1d175049fe2c8e57fd502818521fe`.
Exact diff parent: `426c1bf5f2e38b76ade38d232e1b5578e74702fd`.

## Verdict and scope

Approve the narrow R77-001 repair. The configured historical UI retains modal input ownership below the rendering threshold; invisible action keys cannot execute and the small-window view identifies the active mode without a document caret. Escape/F7 and existing F1 handling preserve explicit focus return. Normal rendering and session/native/async authority remain in their original routes. The actual failing cases no longer modify document bytes.

Approval covers only this 15-file correction: `internal/tui/model.go`, `internal/tui/historic_resize_test.go` and focused files under `internal/tui/evidence/resize-modal/`. All source/test/evidence changes were inspected. No other inherited candidate behavior is approved by this verdict. WP77 remains rejected pending reviewed source intake, canonical retry and complete candidate-plus-repair independent review. No user-preview replacement or full M1 acceptance is authorized by this approval.

## Independent verification

- Verified exact commit/parent, clean tracked source, scoped changed paths, and that the issued pre-fix source had no product-file differences from c7 under internal/, cmd/, go.mod or go.sum. Verified all manifest file lengths and SHA-256 values. The preserved first WP77 rejection remains the cited origin of R77-001.
- Inspected the committed red Model result: identical public regression detects unwanted `a`→`ax` in both modes on the pre-fix source. The committed CLI red evidence saved `BASEx` in both modes. This matches the independent pre-repair public reproduction from the first review.
- Independently reran the original external public reproducer against the fixed checkout: F5 and Alt+= each conserve bytes at normal height and height11, retain gap1, and restore their modal views at25rows. Runner: `/tmp/wordling-WP90-independent-public`.
- Fresh `go test ./internal/tui -run TestHistoricResize -count=1 -v` passed. Covers 1/2/11/12/25row rendering, repeated boundary crossings, complete session/history/native conservation, cancellation/focus return, small-window entry, stale-model rejection, invisible Enter/mouse input, and real pending-save completion.
- Independently built `/tmp/wordling-WP90-independent` from the fixed checkout and ran the actual CLI/PTTY resize harness. Both modes saved exact native body `42415345` (BASE), exited0, and restored termios/alternate screen. Result JSON: `/tmp/wordling-WP90-independent-cli.json`; binary SHA-256: `f77fa015d4835f6172590aabe728be55054457ceab7594457c02840d148dfe81`.
- Reran `go test ./...` and `go vet ./...`: PASS. These reused cache for unchanged/full-suite cases; the focused modal and realCLI probes above were freshly executed. Changed Go source is gofmt-clean and exact diff passes `git diff --check`. Reviewed implementation build/test/vet records also report all gates passing.

The reported stale active-WP commit-guard ambiguity was not treated as authorization. The canonical issued review binds WP90 to H and this exact source; the diff independently satisfies all three declared ownership paths. Existing H owners remain ordered by WP76→WP90→WP84. No rejected WP77 test code was imported into H.

## Required anti-pattern checklist

| Check | Verdict | Basis |
|---|---|---|
| Dead code | PASS | New production branches are reached through normal Update/View; no unused public API or alternate implementation. |
| Synthetic-fixture test | PASS | External tui_test probes use exported production Model/session APIs and actual returned I/O; CLI probe executes the compiled application. |
| Silent empty return | PASS | Deliberate nil-command returns implement documented input suppression during an acknowledged modal; they preserve state and are covered. |
| FR coverage | PASS | Scoped FR-004 modal control, native/Reveal-related preservation and robustness/evidence obligations have public behavior assertions. Broad M1 obligations are explicitly not claimed complete. |
| Frozen surface | PASS | Only declared production file, new regression and owned evidence paths changed. Native-format source is untouched. |
| Locked decision | PASS | Defect fixed before baseline approval; no historical rejection rewrite, scope cut or modern control addition. |
| Shared-file ownership | PASS | model.go is existing H ownership; reviewed WP90 prerequisite76 and WP84 prerequisite90 explicitly order overlap. |
| Production fragility | PASS | No new panic/exception, asynchronous worker or resource acquisition. Minimum dimensions are clamped by existing public resize input, and tiny views are tested. |

## Required downstream handoff

The orchestrator must review the exact approved repair-source intake and preserve all earlier lifecycle/approval identities. WP77 retry must verify unaffected candidate bytes, exact changed repair paths, repair review evidence and integration ancestry, rerun its complete public probes and re-audit all original 23 paths. WP84 and final WP86 must retain/rerun this modal regression. This approval alone does not satisfy those gates.
