---
work_package_id: WP22
title: Original Compose native character identity probes
dependencies:
- WP10
- WP12
requirement_refs:
- FR-014
- NFR-004
- C-004
- C-005
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-wp51-parity-01M64CVY
base_commit: 9585c4d0279627b91ef6e266def92181f68fef3a
created_at: '2026-10-30T23:13:37.079562+00:00'
subtasks:
- T064
- T065
- T066
phase: Bounded M1 continuation; full parity remains open
history:
- at: '2026-10-30'
  actor: planner-priti
  action: Authored from approved contracts; not executed or accepted
agent_profile: researcher-robbie
authoritative_surface: scripts/reference/character_identity.py
create_intent:
- scripts/reference/character_identity.py
- docs/research/continuation/character-identity/
execution_mode: code_change
owned_files:
- scripts/reference/character_identity.py
- docs/research/continuation/character-identity/
role: researcher
tags:
- m1-continuation
task_type: research
tracker_refs: []
---

# WP22: Original Compose native character identity probes

## Identity, governance and prerequisites

Load `researcher-robbie` through resolver-backed profile loading and load action-scoped charter context. Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and continuation.md. Read all dependency outputs and their independent review findings. Use canonical runtime; do not self-approve, accept/merge the mission or advance another package.

**Dependencies:** WP10, WP12.

**Requirement references:** FR-014, FC-006, NFR-004, C-004, C-005.

**Binding approved contract:** `kitty-specs/wp51-parity-01M64CVY/contracts/language-data.md CHR1 and native character identity; layout-resources.md resource boundary`. Section labels after the filename are locators. These are bounded evidence contracts; read exact tables/ledgers and verify fixture/source hashes before using them.

## Objective and observable outcome

Freeze original Compose prompts and native character-pair fixtures before extending document tokenization beyond its accepted ASCII/Bold subset.

This package is one milestone within complete WP 5.1 DOS parity. Completion does not close the entire referenced FR/FC/NFR or a parent inventory group. The continuation ledger retains remaining branches, resources, implementation and differential-verification work. PDF stays optional M2.

## Scope, outputs and subtasks

### T064

Implement scripts/reference/character_identity.py with fresh baseline copies and exact CHR1 inputs, including Ctrl+V Compose1,36 in ordinary document context. Record prompt/termination and native before/after source bytes; distinguish contextual Ctrl+2 documentary alternatives rather than assuming them observed.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T065

Repeat accepted Compose/retrieve/edit/save branches twice; annotate actual C0 character-number/set byte spans and preserved unknown identities. Publish selected WP pair identity, source/runner/profile/fixture hashes and original traces under docs/research/continuation/character-identity/. Any candidate C0 24 01 C0 sequence remains an expectation until exported bytes prove it.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T066

Publish bounded read-only tokenizer handoff and malformed/truncated/mismatched/unsupported-set cases with measured resource/fuzz proposals. Separate identity evidence from display Unicode/glyph and print/preview metrics; retain every other character set, foreign locale, language tool and resource format as explicit open scope.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

## Source and evidence contract

Use the selected plain U.S. English DOS WP5.1 Help03/09/92 baseline and declared QEMU/FreeDOS1.4/mixed-date Standard Printer limitations. Never claim historical DOS, graphics metrics or another locale from that baseline. Source identity includes executable, resources/settings, runner and fixtures; source publication dates do not prove executable behavior.

Canonical case leads: CMD51-138. These links are scope leads, not completed Wordling comparisons. Read exact titles/features and recorded oracle_status before selecting a fixture. Local subcases must have explicit starting state and output; no unrelated valid ID can substitute for semantic association.

Evidence levels stay distinct: documentary expectation, repeated original observation, implemented component, and differential Wordling/original verification. Do not edit raw evidence, normalize bytes, silently replace resources or promote canonical verified statuses based on self-comparison. Project-authored lawful scratch fixtures must retain provenance and raw SHA-256/length. Proprietary executables/manuals/resources stay external and ignored.

## Acceptance criteria

- Actual token bytes and native round trip, not screen resemblance, establish the selected observed identity.
- No proprietary resource redistribution, normalization, silent replacement or implied universal malformed rule.
- Future C0 tokenizer/writer packages require independent review and scoped queue authoring; no implementation is claimed here.

## Ownership and explicit limits

- No document source changes, general Unicode mapping, resource codec, semantic writer or canonical registry edits.
- Missing original resource/profile is recorded as a blocker without silently removing FC-006 scope.

Owned source paths are exactly the frontmatter `owned_files`; `create_intent` authorizes absent paths only. Do not modify dependency-owned sources, existing WP01–WP12 prompts, other lifecycle state, central plan or continuation ledger. If an API/contract is insufficient, record the narrow blocker and request a scoped follow-up rather than implementing a duplicate codec/model or expanding ownership silently.

This is honestly `code_change`: executable Go/Python harness or application code is part of the deliverable. Run in the canonical dependency-aware code lane. WP02 code exists at approved e7de080 and WP03 at approved 7deeaf6; the planning checkout has neither Go implementation. Resolve actual dependency commits in the assigned lane before making code claims. Do not reclassify as planning to bypass lane guards.

## Validation and independent review handoff

Run both catalogue checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp22-validation.xml
```

For changed Go, run gofmt, `go build ./...`, `go test ./...` and `go vet ./...`; include real failure/race tests where pending IO/filesystem state is involved. New or changed binary token interpretation needs negative/malformed cases, measured bounds and reproducible fuzz budget. Semantic writers require separately authorized native field contracts and original retrieve/edit/print/save evidence; this package cannot infer such authority from no-edit exports.

For Python harness changes, compile changed files and run existing harness/unit checks appropriate to the changed boundary. Original probes require two fresh-copy repetitions with exact profile/source/native/capture hashes and archived runner. Report an unavailable prerequisite honestly; do not fabricate a passing oracle or physical terminal result. Review must be able to rerun the evidence checks from committed manifests.

Commit only owned implementation/evidence surfaces using the applicable mission placement. Keep lifecycle events under runtime authority. Record actual commands, outputs, refusals and remaining limits in the owned evidence/report; mark this package’s subtasks and move it for independent review only after required checks pass. A blocked acceptance prerequisite must remain visible. No full-parity, success-criteria, acceptance or merge claim follows from this package.
