---
work_package_id: WP101
title: Prepare a reviewed original route for four unsaved-New macro probes
dependencies:
- WP38
- WP63
- WP64
- WP70
requirement_refs:
- FR-001
- FR-012
- NFR-002
- NFR-003
- NFR-004
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T329
- T330
- T331
phase: Source and safety preparation only; no original/private VM execution
history: []
agent_profile: researcher-robbie
authoritative_surface: scripts/reference/new_macro_nesting.py
create_intent:
- scripts/reference/new_macro_nesting.py
- tests/reference/test_new_macro_nesting.py
- docs/research/continuation/new-macro-nesting/preparation/
execution_mode: code_change
owned_files:
- scripts/reference/new_macro_nesting.py
- tests/reference/test_new_macro_nesting.py
- docs/research/continuation/new-macro-nesting/preparation/**
role: researcher
tags:
- m1-continuation
- draft-unreserved
- original-reference-preflight
task_type: implementation
tracker_refs: []
---

# WP101 — source-reviewed preparation before fresh original execution

PROPOSAL ONLY; IDs tentative until task review/finalization. This is executable reference-harness work and therefore code_change, even though researcher-robbie owns reference investigation. No VM launch or image inspection is authorized here. WP100 can progress independently.

## T329 — choose and document a genuinely authorized original route

Read current original safety contracts, WP38/63/64/68/70 source/approval evidence, the infra-recovery diagnosis, and the exact candidate closure. Record which original route actually satisfies source binding, actual process ownership, exclusive private run root, one leaf/one use, immutable source/plan/case/repetition, bounded deadlines/accounting, authenticated readiness, retained-process stop and stopped read-only export/publish. Supply source hashes and attributable review references. Existing controller `ReferenceController.open_leaf` admits only TestGrant; WP70 is harmless TEST only. TestIssuer/TestGrant is NOT an original route. Legacy smoke.main/guest globals and a `--allow-vm` flag alone are also not proof of the current protocol.

If no approved original route exists, produce a concrete source/design amendment proposal identifying the minimal missing files/interfaces and safety tests, request the root's architecture/reviewer resolution and remain blocked on actual route delivery. Do not widen TestGrant, forge a grant, reuse a spent/expired grant, patch global source guards, copy archived runners into a bypass, or convert a readiness timeout into success. This is a source dependency, not an assumption that Lynn's full-M1 request lacks routine-work authorization. Only the root issues the fresh exact-case grants after source review.

## T330 — add an offline-by-default four-case recipe

New file only, with explicit offline preparation as the default. Preserve historical sources. Reuse authentic WPM exports and expected bodies through immutable paths/hashes in original-cases.json; record both source repetitions. Candidate recipe only selects CMD51-210/212/213/230; no arbitrary script, input path or regex case expansion. Keep root directory C:\OUT and exact parent/child names/identities. Ensure MISSING is genuinely absent in the private stopped/prepared fixture, not replaced by injected fake I/O. Each run starts a fresh real unsaved Doc1 with no Retrieve/EMPTY.WP surrogate. Before invocation record the blank/current filename/new-document state, original status, actual cursor and native/source start facts available from the original UI; establish the same conditions for the separately declared already-admitted edited-New variant. Capture errors/results/cursor and native save/export. Compare root/child WPMs before/after and retain source hashes.

Original construction helpers already exist: advanced.macro_error with macro_start/macro_finish; history_loops.nested(local=True/False), finish and output; value_secondary.macro_break(nested=True). smoke.Probe captures keys/type/stable screen and exports; each old smoke case gets a fresh guest. These are semantic recipes, not approved current launch authority. New probe can stage the authentic WPMs into the stopped private copy then invoke them; it must not modify archived source or manufacture a WPM format. Macro source editing can alter receiver context, so if reconstructing programs in the original, verify unsaved receiver identity again immediately before Alt-F10.

Stage a finite exact-case manifest for two independent fresh-copy repetitions per declared start context (four pristine cases minimum; edited-New positive expansion must get its own four cases/repetitions). Declare extra native-output reopen/edit/print checks as distinct leaves if required by the selected protocol. Record expected text as a hypothesis from the loaded/context recipe; never label it observed New until real runs establish it. Authorization notes bind current request, source, plan and each finite leaf; no historical blanket grant.

## T331 — offline negative checks and prelaunch review

Test denial without a genuine original release, foreign/spent/wrong-case/wrong-source/wrong-plan grants, dirty/existing run root, wrong master/resource/tool identities, live export, unexpected MISSING presence, new-vs-loaded receiver mismatch and deadline failure. Tests use harmless fake resources/TEST interfaces explicitly; a green TEST result is never original evidence. Reproduce infrastructure faults without weakening safety conditions. If fixes require source outside owned_files, submit a separately reviewed explicit amendment before launch.

Freeze source and manifest hashes; run parser/compile and bounded offline tests plus existing relevant protocol tests; obtain independent source/safety review with a concrete exact-case launch plan. Acceptance is a real reviewed, executable original route for these cases, not only a document saying blocked or a new controller that still admits TEST alone. If the route is unavailable, this WP stays incomplete while WP100, WP103 and unrelated HOST work continue.
