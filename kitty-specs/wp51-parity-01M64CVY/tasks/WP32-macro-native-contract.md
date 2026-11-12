---
work_package_id: WP32
title: Original WPM field token and fixture contract
dependencies:
- WP01
- WP09
- WP10
requirement_refs:
- FR-002
- FR-003
- FR-012
- NFR-001
- NFR-003
- NFR-004
- C-002
- C-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity.
  During /spec-kitty.implement this WP may branch from a dependency-specific base,
  but completed changes must merge back into feat/wp51-parity unless the human explicitly
  redirects the landing branch.
subtasks:
- T094
- T095
- T096
phase: Source-backed macro continuation; full M1 remains open
history:
- at: '2026-10-31T01:07:01.952516+00:00'
  actor: planner-priti
  action: Authored as temporary next-tranche draft; unexecuted, not accepted
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/macro-framing.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/macro-framing.md
- kitty-specs/wp51-parity-01M64CVY/contracts/macro-fixtures.json
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/macro-framing.md
- kitty-specs/wp51-parity-01M64CVY/contracts/macro-fixtures.json
role: researcher
tags:
- m1-continuation
- native-macro
task_type: research
tracker_refs: []
---

# WP32: Original WPM field token and fixture contract

## Do this first: profile, governance and source boundaries

Resolve the frontmatter profile with `spec-kitty agent profile show researcher-robbie` and load action-scoped charter context for plan; apply its initialization and boundaries. Read spec.md, plan.md, research.md, data-model.md, continuation.md, contracts/automation.md, native-framing.md, language-data.md, docs/compatibility.md and docs/roadmap.md. Read actual approved dependencies and independent review feedback in their source lanes; primary is a planning checkout, not proof that code does not exist. Use the canonical runtime for this mission only. Do not alter another package's state or approved sources.

All38 requirements,91 inventory groups, discovered nested leaves and complete plain DOS03/09/92 M1 remain retained. PDF starts only after accepted M1 in M2. Original native/companion formats remain durable, unchanged input exports byte-exact, unknown content retained, unsafe writes refused. No proprietary application-code decompilation or redistribution of manuals, programs, dictionaries or resources. Maintain edition/resource/locale/physical-qualification gaps. No helper-only or original-only evidence closes a product scenario, group, FR or mission. Native WPM writing, recording/editing, conversion, full merge language, non-ASCII/resources and remaining commands stay explicit future obligations.

Only this package's declared paths may change. Preserve inherited source/raw evidence and historical catalogues; publish local results without changing current conformance registries, acceptance matrices or other lifecycle records. No automatic accept/merge or mission-completion claim. Production code stays Go1.26.4/Bubble Tea v2.1.1 on Linux; retain module pins and Apache-2.0 contributions.

Dependencies: WP01, WP09, WP10. Execution mode: `planning_artifact`. Full requirement acceptance: false.

## Subtask T094: WPM prefix and corpus evidence

Publish independently written field facts and fixture metadata in macro-framing.md/macro-fixtures.json. Pin SDK WP92–99/PDF105–112, REF373–393/PDF390–410 and relevant Appendix K locators, exact manual/OCR hashes and selected03/09/92 profile. Audit all46 WPM source exports/22 distinct hashes from20 macro observations and their sealed10 run manifests; separately retain the15 merge observations. Distinguish literal source tokens, original output, inference and unrun scope. Known fixtures have tuple1/1/1/1, FFFB four-entry40-byte index, description at56, body70 or75; document tuples1/10/0/1/five-entry indexes must not be generalized. Body alignment is relative to its stored offset: length169/body75 FLOW is valid. Do not impose even whole-file/body-offset alignment. Explain description byte encoding separately from word units and retain uninterpreted prefix/suffix bytes. Define typed malformed versus unsupported/opaque outcomes without inventing a universal prohibition from one producer.

## Subtask T095: Typed words operands and consumer API contract

Specify immutable image ownership/Export, spans, checked arithmetic and input/index/description/token/memory budgets. Word identities use little-endian words: ABC 4100/4200/4300, DISPLAY OFF0CFC and terminal0000 are fixture-proven. Distinguish original character set/number, original key units and macro commands; never DOC-decode WPM or normalize to Unicode source. Prove each supported opcode and operand boundary with raw-word offsets and archived recipe/screens. Nested VARIABLE operands have their own tilde terminator inside expressions; generic split-at-next-tilde parsing is invalid. Preserve hard tilde/unknown words; unknown statically reachable commands refuse execution before effects where possible. Define codec, rooted ReadMacro, injected CommandSink/resolver and evaluator step/result/error/cancellation contracts sufficiently for WP33–37 to share actual API syntax. The contract must include complete Go type/interface/function signatures and runnable acceptance call sequences for Parse/Image.Export/typed-word access, rooted ReadMacro snapshot identity, evaluator run/step/result, CommandSink delivery/error and nested resolver. Match existing storage/editor APIs by inspecting approved dependency source; document future WP36/37 additions and their exact required inputs/results. API labels or arrows alone are insufficient. Pure VM cannot import storage/editor/document/TUI; storage may consume codec. Sink exposes ordered native character/key/session effects and typed outcomes, not serialized document mutation. Identify actual consumer path WP34→WP36→WP37 and future editor APIs needed after WP27/28; interface names are implementer choices captured here before consumption. No executable project validator is a hidden planning deliverable.

## Subtask T096: Reviewable support matrix and retained gaps

Specify fixture coverage for recorded ABC, IF/ELSE/GO/LABEL, bounded numeric ASSIGN/VARIABLE/FOR/WHILE/FOR EACH/NEXT/BREAK and source-proven handlers/nesting. Quotes in observed string lists remain literal. File BREAK in tested root/child macros is ignored; merge primary/secondary BREAK/PAGE semantics remain separate. General coercion/precedence/undefined values/evaluation timing, invalid loops, IF-only BREAK, unobserved handler actions and resource/character cases stay unproved. Define a finite adversarial corpus, API acceptance examples and explicit execution/input/call/loop/output budgets plus cancellation safe points as Linux safeguards, not historical language limits. Review the complete ledger against existing source hashes. A temporary inline read-only audit is allowed as validation; no project Python/Go validator or claims of original CMD51-199 macro-editor roundtrip. Changes are only the two contract files and require independent review.

## Validation and independent review

Changed Go: gofmt, go build ./..., go test ./..., go vet ./... in the actual composed code lane; meaningful failure tests appropriate to the change. Binary readers additionally require malformed-input and reproducible measured fuzz tests. Changed Python: compile, public-entrypoint positive/negative checks and actual supported runner; export real JUnit/XML evidence, commands, exit codes, code/source/raw hashes and declared host/profile. A planning checkout's zero Go packages is not product verification. Use independent review with real artifact/case/API bindings. Report unsupported, not-run, failed and component-only distinctly; no fabricated original message or broad acceptance from bounded results.

Reviewer must inspect the real API/consumer/dependency boundary, scope of native proof and retained gaps; reject silent unknown-byte loss, invented original semantics or source/helper-only product claims. Commit only this package's authorized deliverables using canonical runtime instructions.

For this planning-only package, implementation/fuzz/Go/XML clauses describe downstream acceptance obligations, not executable deliverables here. Validate source hashes/locators/contracts with read-only temporary audits and report that evidence honestly.
