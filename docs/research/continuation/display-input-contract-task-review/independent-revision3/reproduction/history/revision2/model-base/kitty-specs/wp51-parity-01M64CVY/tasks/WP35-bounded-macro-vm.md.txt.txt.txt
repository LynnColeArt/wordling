---
work_package_id: WP35
title: Bounded source-backed macro evaluator with injected command sink
dependencies:
- WP33
- WP39
requirement_refs:
- FR-012
- NFR-001
- NFR-002
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
created_at: '2026-10-31T02:26:47.236670+00:00'
subtasks:
- T103
- T104
- T105
phase: Source-backed macro continuation; full M1 remains open
history:
- at: '2026-10-31T01:07:01.955450+00:00'
  actor: planner-priti
  action: Authored as temporary next-tranche draft; unexecuted, not accepted
agent_profile: implementer-ivan
authoritative_surface: internal/macro/runtime/
create_intent:
- internal/macro/runtime/
execution_mode: code_change
owned_files:
- internal/macro/runtime/**
role: implementer
tags:
- m1-continuation
- native-macro
task_type: implementation
tracker_refs: []
---

# WP35: Bounded source-backed macro evaluator with injected command sink

## Do this first: profile, governance and source boundaries

Resolve the frontmatter profile with `spec-kitty agent profile show implementer-ivan` and load action-scoped charter context for implement; apply its initialization and boundaries. Read spec.md, plan.md, research.md, data-model.md, continuation.md, contracts/automation.md, native-framing.md, language-data.md, docs/compatibility.md and docs/roadmap.md. Read actual approved dependencies and independent review feedback in their source lanes; primary is a planning checkout, not proof that code does not exist. Use the canonical runtime for this mission only. Do not alter another package's state or approved sources.

All38 requirements,91 inventory groups, discovered nested leaves and complete plain DOS03/09/92 M1 remain retained. PDF starts only after accepted M1 in M2. Original native/companion formats remain durable, unchanged input exports byte-exact, unknown content retained, unsafe writes refused. No proprietary application-code decompilation or redistribution of manuals, programs, dictionaries or resources. Maintain edition/resource/locale/physical-qualification gaps. No helper-only or original-only evidence closes a product scenario, group, FR or mission. Native WPM writing, recording/editing, conversion, full merge language, non-ASCII/resources and remaining commands stay explicit future obligations.

Only this package's declared paths may change. Preserve inherited source/raw evidence and historical catalogues; publish local results without changing current conformance registries, acceptance matrices or other lifecycle records. No automatic accept/merge or mission-completion claim. Production code stays Go1.26.4/Bubble Tea v2.1.1 on Linux; retain module pins and Apache-2.0 contributions.

Dependencies: WP33, WP39. Execution mode: `code_change`. Full requirement acceptance: false.

## Subtask T103: Typed execution boundary and observable sink

Implement WP32's evaluator API over actual WP33 decoded sources. Inject CommandSink and nested-program resolver; the package must not import storage/editor/document/TUI or own their state. Preserve typed native character/key identity and exact source positions; do not reparse pretty-printed macro text, convert native source to a private format, build a shadow text/document editor or serialize DOC. Each emitted event is genuinely delivered to an observable sink with ordered effect/error results. Define run/step/continuation/stop/resource-limit results, no false successful completion. Bound input/tokens/steps/calls/loops/output and safe cancellation; report implementation-limit errors distinctly from original errors. Component sink traces are not Wordling native output.

## Subtask T104: Only proven macro control expressions and frames

Implement exact supported IF/ELSE/GO/LABEL; bounded ASSIGN/VARIABLE and positive/negative inclusive FOR, false/updated WHILE, explicit FOR EACH order/duplicates/literal quotes/arithmetic cases, NEXT and loop/file BREAK from original macro cases205,214,215,218–222,226–230 as admitted by contract. Preserve completion/continuation markers; no merge PAGE/record semantics. Source-proven local/default handler and nested-call behavior from178/206/210/212/213 may be implemented only where WP32 proves their tokens and contexts; injected search/missing-file errors test interpreter state only, not integrated original search compatibility. Unknown operators/commands/dynamic input fail explicitly, statically preflight before side effects where possible; preserve source and report partial effects accurately. Do not broaden evaluation timing/coercion/undefined-variable behavior or Plus-only commands from manual presence.

## Subtask T105: Native-source component acceptance and adversarial execution

Run admitted original WPM bytes through reader→VM→real trace sink, compare ordered literals/control decisions/termination with WP09's exact supported20 macro observations and independent original-result inspector where meaningful. Keep the15 merge cases out of macro success counts. Test unsupported reachable opcodes, malformed structures, missing labels/nested input, step/call/output limits, loops and cancellation with immutable source checks; no fake historical error messages. Export JUnit/XML, hashes and actual API invocation evidence. Approve only bounded interpreter/component behavior, never document/native output or executable interaction. WP36/37 must consume this API through ordinary commands before product integration claims.

## Validation and independent review

Changed Go: gofmt, go build ./..., go test ./..., go vet ./... in the actual composed code lane; meaningful failure tests appropriate to the change. Binary readers additionally require malformed-input and reproducible measured fuzz tests. Changed Python: compile, public-entrypoint positive/negative checks and actual supported runner; export real JUnit/XML evidence, commands, exit codes, code/source/raw hashes and declared host/profile. A planning checkout's zero Go packages is not product verification. Use independent review with real artifact/case/API bindings. Report unsupported, not-run, failed and component-only distinctly; no fabricated original message or broad acceptance from bounded results.

Reviewer must inspect the real API/consumer/dependency boundary, scope of native proof and retained gaps; reject silent unknown-byte loss, invented original semantics or source/helper-only product claims. Commit only this package's authorized deliverables using canonical runtime instructions.

## Scoped prerequisite clarification: unexecuted QUIT sites

WP32 identifies FC20 in handler fixtures206/210/212/213 but their captured branches skip it. Preserve static unsupported-instruction preflight: do not implement a reached-only refusal to bypass that rule. WP39 independently qualifies only normal root/nested-child QUIT with handlers registered and supplies an owned original-evidence handoff. Consume its approved result before admitting those sources; unobserved active-handler/interaction contexts remain refused. This adds a research prerequisite without granting broader execution semantics or changing the approved API. Continue independent proven compiler work while qualification is pending.
