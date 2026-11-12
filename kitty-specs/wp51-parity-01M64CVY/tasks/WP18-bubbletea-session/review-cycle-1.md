---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-10-31T00:25:04Z'
reviewer_agent: reviewer-renata
wp_id: WP18
---

# WP18 review cycle 1 — changes required

## I1 — P2: duplicate dispatch refusal settles authentic pending IO

**Affected source:** `internal/tui/runtime.go:94–110` and `internal/tui/model.go:61–82` at e274290bf797f9a6867e5d6c0c31956cb949b376. **Acceptance:** T053 async result ownership, duplicate/late completion and safe exit; T054 negative validation.

Runtime's duplicate-dispatch guard returns an ordinary `resultMsg` bearing the admitted operation/revision/kind. Model.Update treats it as that operation's completion, removes its unsettled entry and passes the refusal to the reducer. This notification did not complete the already admitted backend work.

**Reproduction:** retrieve ORIGIN; F10, COPY, Enter; execute destination observation; execute returned save command once and withhold its authentic Published receipt. Confirm real COPY exists with the exact source bytes. Invoke the same save command again and deliver its duplicate refusal first. PendingIO becomes zero, mode SaveName and SaveFailed, DestinationMayExist false and reconciliation empty. F1, F7, n, y then produces Exited/tea.Quit before authentic receipt delivery. Thus a real published destination can be omitted from reconciliation at a clean exit. This is a defensive duplicate-dispatch boundary defect; the ordinary PTY workflow passes and no claim is made that Bubble Tea normally invokes commands twice.

**Required correction:** distinguish non-settling duplicate dispatch notices from authentic backend completion. Refusing a second invocation must not clear an already admitted operation, consume its reducer pending receipt, or permit exit before its real outcome is handled. Preserve late authentic publication/uncertainty reconciliation, exactly one backend execution, and shutdown/receipt limits. Do not add filesystem calls to the reducer or broaden writer/format authority. Consider duplicate invocation after shutdown/limit as well, since these early guards also emit the same completion envelope.

**Validation:** retain regression coverage for the exact ordering above, including no premature clean exit and subsequent authentic Published receipt processing. Preserve cancelled/late publication reconciliation and existing real IO/race checks. The independent two-test overlay and observed failing output are retained beside this feedback. All seven configured checks, race suite, composed evidence verifier and four existing mutants pass; they do not detect this ordering.
