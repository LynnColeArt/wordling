---
work_package_id: WP33
title: Immutable bounded WPM reader and exact no-edit export
dependencies:
- WP32
- WP02
requirement_refs:
- FR-002
- FR-003
- FR-012
- NFR-001
- NFR-003
- NFR-004
- C-001
- C-002
- C-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-wp51-parity-01M64CVY
base_commit: 9585c4d0279627b91ef6e266def92181f68fef3a
created_at: '2026-10-31T01:44:00.648005+00:00'
subtasks:
- T097
- T098
- T099
phase: Source-backed macro continuation; full M1 remains open
history:
- at: '2026-10-31T01:07:01.953725+00:00'
  actor: planner-priti
  action: Authored as temporary next-tranche draft; unexecuted, not accepted
agent_profile: implementer-ivan
authoritative_surface: internal/macro/wpm/
create_intent:
- internal/macro/wpm/
execution_mode: code_change
owned_files:
- internal/macro/wpm/**
role: implementer
tags:
- m1-continuation
- native-macro
task_type: implementation
tracker_refs: []
---

# WP33: Immutable bounded WPM reader and exact no-edit export

## Do this first: profile, governance and source boundaries

Resolve the frontmatter profile with `spec-kitty agent profile show implementer-ivan` and load action-scoped charter context for implement; apply its initialization and boundaries. Read spec.md, plan.md, research.md, data-model.md, continuation.md, contracts/automation.md, native-framing.md, language-data.md, docs/compatibility.md and docs/roadmap.md. Read actual approved dependencies and independent review feedback in their source lanes; primary is a planning checkout, not proof that code does not exist. Use the canonical runtime for this mission only. Do not alter another package's state or approved sources.

All38 requirements,91 inventory groups, discovered nested leaves and complete plain DOS03/09/92 M1 remain retained. PDF starts only after accepted M1 in M2. Original native/companion formats remain durable, unchanged input exports byte-exact, unknown content retained, unsafe writes refused. No proprietary application-code decompilation or redistribution of manuals, programs, dictionaries or resources. Maintain edition/resource/locale/physical-qualification gaps. No helper-only or original-only evidence closes a product scenario, group, FR or mission. Native WPM writing, recording/editing, conversion, full merge language, non-ASCII/resources and remaining commands stay explicit future obligations.

Only this package's declared paths may change. Preserve inherited source/raw evidence and historical catalogues; publish local results without changing current conformance registries, acceptance matrices or other lifecycle records. No automatic accept/merge or mission-completion claim. Production code stays Go1.26.4/Bubble Tea v2.1.1 on Linux; retain module pins and Apache-2.0 contributions.

Dependencies: WP32, WP02. Execution mode: `code_change`. Full requirement acceptance: false.

## Subtask T097: Separate immutable WPM image

Implement the reviewed WP32 API in internal/macro/wpm only. Consume actual WP02 module/toolchain foundation but leave internal/wp51 unchanged: DOC Parse must continue refusing WPM. Own/copy input and exported buffers; byte-exact Export preserves all admitted original bytes, unused prefix indexes/description/gaps/unknown words/trailing data according to contract. Parse signature/tuple/version/encryption/reserved, macro index and description with checked widths and bounds; recognize unsupported producers/versions separately from corruption. Do not inherit DOC five-index or single-byte body grammar, assume offset70/75 universally, or require absolute even offsets. No WPM writer, serializer reconstruction, filesystem or UI.

## Subtask T098: Lossless typed word and operand reader

Expose original word identities and exact source spans with recognized/opaque/malformed support states. Decode only WP32-proven words and operand structures; nested VARIABLE termination and literal versus command tildes retain original identity. Opaque unknown instructions remain present in image/tokens and cannot acquire implicit execution permission. Preserve character set/number without lossy UTF-8/CP437 substitution. Provide the actual installed API required by WP34/35 and examples binding image/support/tokens; an unconsumed demonstration parser is insufficient. Do not manufacture WPM from DOC fixture bytes or claim broad macro-language support from header acceptance.

## Subtask T099: Original corpus adversarial and measured parser verification

Verify all46 sealed original WPM source exports/22 distinct hashes, exact length/hash/Export and buffer isolation; provenance allows project-authored inputs only. Explicitly test FLOW169/body75, ABC80/body70, malformed/truncated header/index/description/odd-body/terminal/offset lengths, oversized inputs, overlap/cycles where applicable and opaque commands. Preserve evidence files read-only; derived corruptions live in test memory. Run a declared reproducible fuzz budget plus limit/termination/allocation checks and record actual host/commands/results under owned evidence. Source-only/fixture-only acceptance is component reader evidence. Export equality does not claim CMD51-199 original macro-editor roundtrip or disk save/reopen/edit compatibility.

## Validation and independent review

Changed Go: gofmt, go build ./..., go test ./..., go vet ./... in the actual composed code lane; meaningful failure tests appropriate to the change. Binary readers additionally require malformed-input and reproducible measured fuzz tests. Changed Python: compile, public-entrypoint positive/negative checks and actual supported runner; export real JUnit/XML evidence, commands, exit codes, code/source/raw hashes and declared host/profile. A planning checkout's zero Go packages is not product verification. Use independent review with real artifact/case/API bindings. Report unsupported, not-run, failed and component-only distinctly; no fabricated original message or broad acceptance from bounded results.

Reviewer must inspect the real API/consumer/dependency boundary, scope of native proof and retained gaps; reject silent unknown-byte loss, invented original semantics or source/helper-only product claims. Commit only this package's authorized deliverables using canonical runtime instructions.
