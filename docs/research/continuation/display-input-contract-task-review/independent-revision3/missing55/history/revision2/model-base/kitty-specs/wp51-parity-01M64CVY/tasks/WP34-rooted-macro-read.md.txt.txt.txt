---
work_package_id: WP34
title: Rooted read-only WPM acquisition through existing storage
dependencies:
- WP24
- WP33
requirement_refs:
- FR-006
- FR-012
- NFR-001
- NFR-002
- NFR-004
- C-001
- C-002
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity.
  During /spec-kitty.implement this WP may branch from a dependency-specific base,
  but completed changes must merge back into feat/wp51-parity unless the human explicitly
  redirects the landing branch.
subtasks:
- T100
- T101
- T102
phase: Source-backed macro continuation; full M1 remains open
history:
- at: '2026-10-31T01:07:01.954631+00:00'
  actor: planner-priti
  action: Authored as temporary next-tranche draft; unexecuted, not accepted
agent_profile: implementer-ivan
authoritative_surface: internal/storage/
create_intent: []
execution_mode: code_change
owned_files:
- internal/storage/**
role: implementer
tags:
- m1-continuation
- native-macro
task_type: implementation
tracker_refs: []
---

# WP34: Rooted read-only WPM acquisition through existing storage

## Do this first: profile, governance and source boundaries

Resolve the frontmatter profile with `spec-kitty agent profile show implementer-ivan` and load action-scoped charter context for implement; apply its initialization and boundaries. Read spec.md, plan.md, research.md, data-model.md, continuation.md, contracts/automation.md, native-framing.md, language-data.md, docs/compatibility.md and docs/roadmap.md. Read actual approved dependencies and independent review feedback in their source lanes; primary is a planning checkout, not proof that code does not exist. Use the canonical runtime for this mission only. Do not alter another package's state or approved sources.

All38 requirements,91 inventory groups, discovered nested leaves and complete plain DOS03/09/92 M1 remain retained. PDF starts only after accepted M1 in M2. Original native/companion formats remain durable, unchanged input exports byte-exact, unknown content retained, unsafe writes refused. No proprietary application-code decompilation or redistribution of manuals, programs, dictionaries or resources. Maintain edition/resource/locale/physical-qualification gaps. No helper-only or original-only evidence closes a product scenario, group, FR or mission. Native WPM writing, recording/editing, conversion, full merge language, non-ASCII/resources and remaining commands stay explicit future obligations.

Only this package's declared paths may change. Preserve inherited source/raw evidence and historical catalogues; publish local results without changing current conformance registries, acceptance matrices or other lifecycle records. No automatic accept/merge or mission-completion claim. Production code stays Go1.26.4/Bubble Tea v2.1.1 on Linux; retain module pins and Apache-2.0 contributions.

Dependencies: WP24, WP33. Execution mode: `code_change`. Full requirement acceptance: false.

## Subtask T100: ReadMacro using existing stable snapshot acquisition

Extend the real approved storage Directory with the reviewed typed ReadMacro API; reuse readStable, validName, pinned root, no-follow regular-file checks, bounded reads and source metadata/hash consistency. Delegate WPM framing to WP33; keep document Read/PreparePublication and their type/refusal contract intact. If a narrow shared read-limit parameter is needed, refactor this existing path and retain its tests rather than introducing another filesystem engine. Capture immutable macro image plus source identity; this is a read observation, not locking or future freshness guarantee. No WPM Save/Publish or generalized transaction, arbitrary host paths, replacement or DOC parser weakening.

## Subtask T101: Consumer-facing macro snapshot and failure behavior

Expose immutable source name/directory identity/hash and typed codec/failure outcomes needed by WP36's macro loading/nested resolver. Make codec unsupported versus malformed versus storage/stale/path errors distinguishable; no invented historical text or error class. Direct production consumer is the later editor adapter; no alternate CLI or new hidden on-disk companion. Native snapshots remain independent of UI revisions; later consumer owns operation/session identity. No source file changes on read/error/cancel; no implicit transfer of macro-write permission through existing document candidate APIs.

## Subtask T102: Rooted acquisition regression and fault evidence

Exercise actual approved storage public methods with original WPM fixtures and fault boundaries: DOC Read rejects WPM, ReadMacro rejects DOC, symlink/nonregular/unsafe name/size/read-close/change/stale cases, valid source identity and copy isolation. Preserve existing publication safety, source guard and all WP24 tests. Actual code-lane build/test/vet and appropriate race/failure verification; record local evidence in internal/storage/evidence/macro-read/. Test-only consumption proves API behavior, while real UI execution remains WP36/37; no claim that file read executes a macro or closes FR-012.

## Validation and independent review

Changed Go: gofmt, go build ./..., go test ./..., go vet ./... in the actual composed code lane; meaningful failure tests appropriate to the change. Binary readers additionally require malformed-input and reproducible measured fuzz tests. Changed Python: compile, public-entrypoint positive/negative checks and actual supported runner; export real JUnit/XML evidence, commands, exit codes, code/source/raw hashes and declared host/profile. A planning checkout's zero Go packages is not product verification. Use independent review with real artifact/case/API bindings. Report unsupported, not-run, failed and component-only distinctly; no fabricated original message or broad acceptance from bounded results.

Reviewer must inspect the real API/consumer/dependency boundary, scope of native proof and retained gaps; reject silent unknown-byte loss, invented original semantics or source/helper-only product claims. Commit only this package's authorized deliverables using canonical runtime instructions.
