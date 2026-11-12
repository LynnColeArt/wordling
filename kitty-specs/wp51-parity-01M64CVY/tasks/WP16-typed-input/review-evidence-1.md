# WP16 independent implementation review

Reviewer: reviewer-renata (independent Codex reviewer, not implementer).
Reviewed lane: /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-f.
Reviewed commits: fe0ced010bafe1e34ca5e65bfdbe972cb7487d7e and fb23263e1ed7e31ca9005c6b9adf450a7986b674; base9585c4d.
Recommendation: approve bounded input component/harness. No blocking findings.

## Criteria and source assessment

Read FULL generated prompt d5f6db0c57fb415bbd3fb79b84f1350c, actual current primary WP16 prompt/prerequisites, AGENTS.md and approved session/input contract. Refreshed resolver-backed reviewer-renata and software-dev review governance. Loaded review/verdict skills remain applicable. Scope is T046–T048, not later contextual commands/session, native documents, physical key qualification or M1 parity.

T046 passes: input.Translate consumes actual pinned-v2 KeyPressMsg/KeyReleaseMsg/Mouse/Paste/WindowSize/capability/focus types and actual Supports methods. Code/Mod/Text/ShiftedCode/BaseCode/IsRepeat remain exact. Press/release/repeat are separate; stateless translation never aggregates Escape, strips modifiers, normalizes text or replays paste as commands. Fresh Key/Mouse/Support values avoid cross-event aliases. Original unknown messages remain in process with their actual type; arbitrary pointer payload ownership is explicitly documented and JSON omission is paired with separate exact raw capture. No generic quit/save/cancel alias or session/native/Unicode-mapping implementation appears.

T047 passes: real executable Bubble Tea probe invokes input.Translate in Update. captureFile retains term.File/Fd, allowing actual raw-mode setup/restoration. Ordered locked JSONL journal stores raw input/output hex chunks and decoded events with sequence/monotonic timing, actual build/module identity, selected environment, terminfo, operator assertions, optional binary/config fingerprints and separate enhancement requests/responses. Deadline is probe control; no key is repurposed to quit. Invalid/non-TTY/existing-output paths refuse; journal errors propagate; host SIGTERM and incomplete deadline are abnormal. Unknown wire bytes remain in journal independently of their opaque in-process event.

T048 passes: typed tests and real Linux synthetic-PTY driver exercise exact function/navigation chords, enhanced control collision distinctions, repeat/release, escape-looking paste, unknown CSI, focus/mouse/resize, fragmentation, fast/delayed Escape, raw equality, new capture refusal and terminal restoration. README publishes a precise all-unqualified physical matrix with missing emulator/config/hardware/operator/desktop prerequisites. Synthetic31 capability reply and bytes are explicitly injected, not real negotiation or physical support. Operator physical-direct label never sets qualification. No inventory/original-app verification is promoted, and terminal/desktop/resource gaps remain M1.

Only internal/input/, cmd/wordling-input-probe/ and docs/research/continuation/terminal-input/ changed in source commits; go.mod/go.sum, native/document/storage and frozen planning/registry surfaces are unchanged. fb23263 adds only binary evidence attributes. Root coordinates WP18 dependency sequencing. No other WP status or implementation was changed by this reviewer.

## Checks executed independently

1. Actual declared runner `python3 scripts/review_checks.py --junitxml /tmp/wp16-independent-review.xml`:7 tests,0 failures/errors/skips. Includes catalogue inventory/scenarios, adapter regression, package discovery, real Go build/test/vet in this code lane. Retained as review-checks-1.xml.
2. `go test -race ./...`: both real packages pass. Existing tests actually invoke production Translate, model Update/View and journal paths. Failing evidence writer is tested fail-loud; concurrent journal sequencing is tested. No synthetic assertion bypasses the production path.
3. Source/capture verifier `python3 docs/research/continuation/terminal-input/verify.py` passes all source/dependency/governance fingerprints and both retained synthetic runs, raw bytes and scope flags. Pinned tty_unix source confirms term.File controls raw mode; adapter uses the actual v2 key/capability API, not v1 comments.
4. Diff-scoped gofmt -l emits no files; git diff --check passes. Both changed Python files compile using compile(source,path,'exec') without creating repository pycache.
5. Built `/tmp/wp16-review-input-probe`, reran `pty_test.py` to unique `/tmp/wp16-independent-pty-20261030`: all four scenarios pass. Copied exact authored synthetic rerun to review-synthetic-pty-1/ (its manifest seals all files). Enhanced/legacy-fast/legacy-slow/SIGTERM journals contain53/32/21/13 records and254/48/6/1 raw bytes. Independently concatenated raw journal bytes equal injected.json bytes; terminal-output concatenation equals observed wire-output bytes (239/238/238/238). End states retain unqualified-capture and synthetic-pty-only; deadline/abnormal exit and actual termios restoration checks pass.
6. Independent returned-value ownership test ran through Go overlay under race detector, with no repository implementation/test edit. Mutating one event's Key/Mouse/Support leaves another event and original typed value unchanged. Retained source as review-owned-events-1.go.txt. Command `go test -race -overlay=/tmp/wp16-review-overlay.json ./internal/input -run IndependentEventOwnership -count=1` passes; overlay maps virtual internal/input/review_owned_events_test.go to that temp test source.
7. Call-site search finds actual production `input.Translate(msg)` in cmd/wordling-input-probe/main.go. Unknown/non-key events keep discriminants and cannot accidentally become press commands in this adapter. Error returns in probe/driver fail-loud on evidence/transport failure; no silent empty fallback or panic-driven production path added.

Reproduce from the exact reviewed lane/head: run declared runner and race tests, source verifier, build probe to a fresh /tmp filename, and invoke the published PTY driver with a new output directory. Manifest hashes and scope flags in the copied review rerun can be independently checked without physical hardware. The ownership test can be overlaid from its retained text source; no permanent source mutation is needed. New physical qualification must follow the published actual operator/profile matrix before any physical support label.

## Required anti-pattern checklist

1. Dead code: PASS; new input module has live probe consumer; executable main is callable and all production helpers are used.
2. Synthetic-fixture test: PASS; typed tests call production adapter/model/journal and independent PTY rerun executes actual binary/library. Synthetic transport evidence remains labelled and is not original/physical evidence.
3. Silent empty return: PASS; unknown typed event is explicit and preserves Original/SourceType; errorText returns empty only for nil error; failures propagate. Python EIO handling documents PTY closure, other errors raise.
4. FR coverage: PASS for bounded WP16 scope: FR-004 key distinctions/paste/no aliases and FR-017 transport/profile/refusal/restore have actual assertions; C-001 real pinned Go/Bubble Tea build; C-006 blocked physical matrix/no silent scope cuts; NFR-004 hashed raw/source manifests and false qualification checks. Full interaction/platform parity remains open.
5. Frozen surface: PASS; source diff stays within exclusive WP16 scope, module pins/planning/native/registry unchanged.
6. Locked decision: PASS; no document mutation, aliases, physical qualification or general parity inference.
7. Shared-file ownership: PASS; sole WP16 lane and exclusive source scope. Root handles remaining sequencing; runtime-authorized review artifacts are separate from implementation.
8. Production fragility: PASS; evidence/TTY failures return errors with abnormal capture state; deadline exits only probe control. No transient-race panic or original F7 replacement.

Approval covers compiled bounded adapter, executable evidence harness and truthful blocked physical qualification. It does not certify terminal/keyboard delivery, original WP command behavior, native edit support or mission acceptance.
