---
work_package_id: WP109
title: Complete native Italics block-copy fragment production
dependencies:
- WP106
requirement_refs:
- FR-002
- FR-004
- FR-005
- FR-006
- FR-008
- NFR-003
- NFR-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity.
  During /spec-kitty.implement this WP may branch from a dependency-specific base,
  but completed changes must merge back into feat/wp51-parity unless the human explicitly
  redirects the landing branch.
subtasks:
- T353
- T354
- T355
phase: Native block-copy producer correction before public integration closure
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/document/block_copy.go
create_intent:
- internal/document/block_copy_italics_test.go
- internal/document/evidence/block-copy-italics/
execution_mode: code_change
owned_files:
- internal/document/block_copy.go
- internal/document/block_copy_italics_test.go
- internal/document/evidence/block-copy-italics/**
role: implementer
tags:
- m1-continuation
- registered-continuation
- copy-italics-producer
task_type: implement
tracker_refs: []
---

# WP109 — native Italics Copy producer, preserving the insertion authority

## Context and bounded decision

WP107's genuine workspace-selected ITALICS source read followed by public Reveal/Block/Move→Copy fails UnsupportedBody at token0/span324+3 in CopyEverydayBlock. The source108-reference work is unrelated. Approved WP106 extends InsertDocument/InsertBlockCopy, but CopyEverydayBlock is a separate producer that still tracks/adopts only Bold/Underline. The public failure is preserved in the adoption packet at exact f6abda6b. Do not fix it inside test-only WP107 or claim prepared-fragment insertion proves public Copy.

Load actual implementer-ivan/action implement governance on the normal owned claim. This task is proposed until normal validation/finalization/claim; authored prose creates no status or authority. Use source-pinned ec868755 CLI in AGENTS.md. Dependencies are WP106 only; prior native framing/admission/history are transitive. WP107 adds WP109 to its existing predecessors, never the reverse. Root withholds107approval until109is independently approved even though an already-in-progress resume is not retroactively hard-gated by the new edge.

## T353 — actual producer RED and full attribute-consumer census

Capture the actual clean pre-code source/official baseline, raw executed check counts and exact pins. Create native producer acceptance tests before any production edit; commit genuine RED for the present UnsupportedBody behavior, with setup/compile failures excluded. Preserve the independently reproduced public107failure as supporting consumer evidence, not a substitute for native RED. Use existing approved source fixture identity and independent literal C3/08/C3 and C4/08/C4 vectors plus actual Kind assertions; do not derive expected bytes from the implementation's flags.

Inventory every active production Go use of ItalicsOn/Off and relevant attribute producer/admission/reader/editor routes (exclude historical evidence snapshots). Record exact file hashes, callers and per-use disposition. This closes the discovered producer/insertion coverage gap through an explicit consumer matrix and regression cases. It does not license a general formatting refactor or require unrelated Redline/Strikeout producers. This is an unimplemented producer extension discovered at first integration, not three recurrences or two shipped reactive PRs; ownership is unambiguous, so DIRECTIVE040's recurring/contested-boundary trigger has not been established. Any newly demonstrated separate source owner requires a precise reviewed amendment, not silent widening.

Cover full and partial selections: whole run; interior text with both edge wrappers; selection beginning/ending exactly before/after each ON/OFF; selection containing only boundary owners where the existing contract admits it; leading/trailing plain text; multiple runs; reversed anchor/end; independent active Bold, Underline and all three; legal crossing attributes without duplicate nesting assumptions. Each resulting fragment must be self-contained with exact bytes/Kind sequence and the existing historical detached prefix; source prefix/metadata/birth/identity bytes are unchanged and are not imported into the fragment. Keep old non-Italics Copy outputs and refusals as regression controls.

## T354 — smallest native producer change only

Edit only internal/document/block_copy.go. Reuse existing Italics token kinds, mutation admission, raw owners and fragment constructor. Track Italics independently, include existing ItalicsOn/Off owners, and synthesize only necessary edge ON/OFF owners so the selected fragment is self-contained. Preserve source order for selected owners and deterministic valid independent-attribute wrappers. No parser/kind/format/API, insertion/receiver rule, metadata transfer, editor/TUI/storage or external resource behavior changes. A private local literal/constant for the already proven subfunction08 is allowed only in this file and must have an independent original/literal+actual-Kind mirror test; do not edit document.go to add an owner.

Preserve exact typed invalid/foreign/stale cursor, empty selection, malformed/unbalanced/opaque/unsafe-body and mutation-limit behavior. Source and returned byte buffers remain independently owned. Enforce existing byte/token ceilings including every synthesized wrapper; never leave the old four-wrapper assumption able to undercount six wrappers with three active styles. Preserve the old non-Italics conservative acceptance/refusal bounds; do not silently relax them by switching to a smaller actual-wrapper count or tighten them without a precise reviewed reason. Test boundary arithmetic and all-three-style wrappers with independent expected token counts. Do not enlarge intrinsic limits or normalize unknown bytes to make a case pass. Keep WP106 insertion and active receiver same-attribute refusal unchanged; ordinary Retrieve versus Copy caret/history belongs to the real107consumer tests.

## T355 — verification, scope and independent handoff

Run owned gofmt and diff checks, native producer/retrieve/history/appearance tests, focused native/editor/TUI race, full Go test/vet/build, and exact production-application Windows cross-vet/build using the declared package closure. Preserve actual unchanged skips and existing broad Windows research-helper failures separately; no native-Windows claim from cross checks and no Mac builds/tests. Freeze source/tests, RED/GREEN raw outputs, complete attribute-consumer disposition matrix, all15canonical contract dispositions with concrete examples, exact original encoding provenance and baseline scope. The real public107repro must later turn GREEN only through the public caller; do not inject a Result, detached fragment or callback to bypass Copy. Exact final107tests later replay against pre109 for Copy-specific UnsupportedBody and against pre106 for native insertion UnsupportedBody; report the two failure sites separately and keep honest chronology.

Commit only owned files using safe explicit paths, hand a clean candidate to a different independent reviewer, and leave final verdict/lifecycle to ROOT. Never selfapprove, push, or promote CMD51-065/E3/audit/acceptance matrix/M1. Native/public source behavior and synthetic/original-derived fixture tests do not establish original occupied Retrieve/Copy or native reopen/edit/print/save interoperability; those later gates remain mandatory. All49families remain in M1; Mac stays deferred until milestone end. No VM, reference capture, TEST/P/CONTROL, original/private-resource or whole-campaign clock action occurs in this package.

## Branch and writer discipline

Use the issued normal owned single-branch primary checkout, with one source/index writer. No project worktree. Root coordinates metadata quiet points. Approved causal isolation may use a disposable /tmp source archive with exact source/test/fixture hashes, raw causal errors, complete cleanup and registered-worktree invariance; setup failure is never RED. Leave all authorized source/evidence committed.


## Current integration discovery clarification

Consumer107also exposed a separate host completion-accounting defect, assigned only to110; this package's native production scope is unchanged. Contract inventory covers every implementation-time canonical contract file (original15 plus103's two provisional orthogonal coverage artifacts). Exact-old-tree full107replays may contain the independently recorded pre110PendingIO control failure as well as UnsupportedBody. Preserve/classify all outcomes and use unchanged selected producer/insertion acceptance commands to isolate causality; no later-production overlay or all-failures-one-cause claim is permitted. Include beginBlockAppend as a shared CopyEverydayBlock caller in the native consumer census without expanding production ownership.
