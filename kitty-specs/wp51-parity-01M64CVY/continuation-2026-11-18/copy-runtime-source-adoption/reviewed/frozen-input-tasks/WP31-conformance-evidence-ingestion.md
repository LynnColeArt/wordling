---
work_package_id: WP31
title: Bounded executable evidence ingestion and conformance rollup
dependencies:
- WP30
- WP29
requirement_refs:
- FR-001
- FR-002
- FR-004
- FR-005
- FR-006
- FR-008
- FR-015
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- NFR-005
- C-001
- C-002
- C-003
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T091
- T092
- T093
phase: Versioned conformance evidence continuation; full M1 remains open
history:
- at: '2026-10-31T00:22:15.799023+00:00'
  actor: planner-priti
  action: Authored in temporary next-tranche draft; unexecuted, not accepted
agent_profile: implementer-ivan
authoritative_surface: scripts/conformance/v1/
create_intent:
- docs/conformance/v1/
- scripts/conformance/v1/
- tests/conformance/v1/
execution_mode: code_change
owned_files:
- docs/conformance/v1/**
- scripts/conformance/v1/**
- tests/conformance/v1/**
role: implementer
tags:
- m1-continuation
- versioned-conformance-evidence
task_type: implementation
tracker_refs: []
---

# WP31: Bounded executable evidence ingestion and conformance rollup

## ⚡ Do This First: Load Agent Profile

Use the resolver-backed profile-load skill (the /ad-hoc-profile-load alias resolves
there) before parsing the remaining prompt. Resolve the frontmatter profile with
`spec-kitty agent profile show implementer-ivan`, then load action-scoped charter
context for implementation and follow its initialization and boundaries.

- **Profile**: implementer-ivan
- **Role**: implementer
- **Agent/tool**: codex

Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and both
historical/appended continuation checkpoints. Read all actual dependency outputs and
independent review findings. Use canonical commands with
`--mission wp51-parity-01M64CVY`; never advance or approve another WP.

## Objective

Implement bounded evidence ingestion and truthful rollup of actual approved WP29
executable/original differential results into the current conformance layer. Preserve
case-level scope and publish readiness bindings for future normal mission acceptance.

## Context and prerequisites

Dependencies: WP30 and WP29. Use the actual reviewed WP30 schema/CLI and actual WP29
report/harness outputs, source hashes, executable provenance and independent reviews.
WP30 and WP31 share the same new namespace sequentially; do not duplicate the schema,
validator or create another competing current registry. No new VM/original run is
required for ingestion: preserve actual outcomes, including failure or missing proof.
If WP29 cannot prove a binding, ingest it as open/blocked, not a fabricated pass.
FC-001 through FC-010 and full SC-001 through SC-005 remain binding.

### Subtask T091: Source-bound actual evidence ingestion runner

**Purpose:** Translate actual approved evidence without promoting its scope.

**Steps:**
1. Implement an ingestion entrypoint under scripts/conformance/v1/ extending the real
   WP30 schema/validator. Read actual WP29 report shape before choosing field mappings.
2. Resolve reviewed WP29 commit/report/harness/output blobs; record independent review
   provenance and reconcile declared hashes with Git blob bytes. Retain failed attempts
   and superseded runs as such; only explicitly admissible results feed positive claims.
3. Bind each bounded case to its stable canonical/extension revision and exact inherited
   parent/requirement/source identities. Reject unrelated valid IDs used as substitutes.
4. Record implementation commit and executable build/hash/invocation, actual input/output
   hashes and raw paths, original baseline/environment/resource profiles, comparator,
   explained native changes and exact tested state/command/prompt/history scope.
5. Distinguish source-only component tests, helper-emitted files and real cmd/wordling
   integration. No serializer/helper result may be substituted for product execution.
6. Preserve raw evidence read-only. Store provenance references and normalized current
   records without rewriting originals or copying proprietary/private resources.
7. For incomplete/mismatching evidence emit an actionable record and open/blocked verdict;
   do not invent missing physical, display, historical-DOS, graphics or language witnesses.
8. Make ingestion deterministic/idempotent, with dry-check and explicit write modes;
   refuse conflicting repeated identities and leave prior accepted records unchanged.

**Files:** scripts/conformance/v1/ ingestion runner; current namespace registry/report
records and tests/conformance/v1/ ingestion tests.
**Validation:** Real approved WP29 input yields exactly its admissible bounded outcomes;
wrong hashes/IDs/revisions fail. Repeat ingestion is stable and raw evidence unchanged.

### Subtask T092: Bounded conformance rollup and future acceptance readiness bindings

**Purpose:** Make current progress reviewable without closing broader requirements.

**Steps:**
1. Add current evidence records for actual reviewed bounded components inherited through
   dependencies and real WP29 results, preserving each source's exact declared scope.
2. Keep original-observed, component-implemented, executable-integrated and differential
   pass/fail counts separate. Do not collapse them into one compatibility percentage.
3. Map passing local slices to their parent obligations as partial evidence only. Every
   whole scenario/group/FR/NFR/FC remains open until complete breadth is actually proved;
   this editing tranche supplies no blanket requirement acceptance.
4. Retain all 38 obligations/91 groups plus discovered leaves/extensions, whole remaining
   workflows, print/layout/resources/locales/platform duties and explicit refusals.
5. Generate current index/report of evidence bindings, missing prerequisites and unresolved
   resource/physical qualifications. Compare source/profile mismatches explicitly.
6. Produce a readiness/evidence-binding report for FUTURE normal acceptance workflow:
   each candidate matrix criterion reference resolves to current record revision and raw
   proof, with missing required coverage clearly shown. Do not write acceptance-matrix.json,
   runtime lifecycle, approval events, passing requirement rows or parity_accepted=true.
7. Keep parity_accepted=false, all_m1_obligations_closed=false and
   queue_exhaustion_authorizes_acceptance=false explicit in bounded rollup metadata.
8. State this package ingests evidence; it does not repair application defects, replace
   comparisons, qualify physical resources or authorize M2/PDF.

**Files:** docs/conformance/v1/ current registry/index/bounded ingestion report and
readiness bindings; supporting validator/ingestion tests in owned new paths only.
**Validation:** Independently trace every positive row to real source+review+execution+
raw comparator proof; all unproved siblings/parents/resources remain visibly open.

### Subtask T093: Adversarial ingestion tests and reproducible review handoff

**Purpose:** Reject evidence laundering, incomplete parent closure and stale bindings.

**Steps:**
1. Run real-input ingestion and external-CLI tests against the exact reviewed WP29 schema;
   avoid a synthetic happy-path fixture as the only integration evidence.
2. Mutate fixtures for forged executable hash, wrong code/case/source revision, missing
   independent review/raw output, original-only scope, helper-only generation and invalid
   comparator/resource identity. Require clear nonzero failure or explicit open disposition.
3. Test failed/superseded attempts cannot overwrite accepted outcomes; duplicate import
   cannot inflate counts; conflicting identities cannot silently pick a preferred result.
4. Test one editing pass cannot close an entire requirement/group/canonical scenario,
   omitted leaf, physical delivery, graphics profile, locale or full native format family.
5. Test malformed extension lineage, stale approved snapshot, undisclosed baseline changes,
   omitted known obligations and forged full-M1 flags. Keep negative inputs in owned tests.
6. Run validator/index regeneration and ingestion twice; compare deterministic outputs,
   prior frozen source hashes and raw evidence bytes. Check CLI failure leaves data intact.
7. Publish actual commands/results and independent review handoff with precise bounded
   acceptance/readiness limitations. If product defects emerge, report a scoped future
   repair; no out-of-map production-code changes belong here.
8. Submit normally for independent review. No VM launch or new original observation is
   required to fix missing ingestion proof; absent evidence remains absent.

**Files:** tests/conformance/v1/ negative fixtures and public-CLI tests, ingestion/validator
fixes, current bounded verification report.
**Validation:** Real source-bound integration succeeds only for admissible actual rows;
all negative promotion guards pass; complete M1 remains open after this package.

## Permanent scope and evidence boundaries

- This package is a bounded milestone inside full plain WP 5.1 DOS M1.
- Preserve all 38 FR/NFR/C/FC obligations, 91 inventory groups, inherited cases,
  discovered leaves, all original workflows/utilities, locales/resources and adaptations.
- The 91 groups and catalogue count are minimum traceability baselines, not a frozen
  exhaustive feature list. New findings expand the ledger; unexplained exclusions fail.
- Product native and companion formats never change; conformance JSON is test tooling,
  never a required document sidecar or replacement editable format.
- All unproved branches remain open/unverified. Distinguish documentary expectation,
  original-only observation, implemented component, executable integration, original
  differential pass/fail, and physical/resource qualification as separate evidence levels.
- Source presence, helper tests, original-only probes and WP approval cannot establish
  real executable integration or Wordling/original differential compatibility.
- A bounded local pass cannot close its whole canonical scenario, parent group, FR,
  NFR or FC. Missing resources and physical qualifications stay explicit and unqualified.
- Full SC-001 through SC-005 remain binding. Queue exhaustion does not authorize
  acceptance. No self-approval, mission acceptance/merge, or M2/PDF work is authorized.

## Ownership and runtime placement

Run only in the dependency-aware code lane assigned by the runtime. This is honestly
`code_change`: executable validator/ingestion behavior and external-interface tests
are deliverables. Do not reclassify as planning, add a codebase-wide exemption,
remove dependencies, invent ownership, patch installed tooling or call private merge
functions. WP30 and WP31 legitimately edit the new current namespace sequentially;
WP31 depends on WP30. Expected combined lane-m retains every old lane assignment.
Only frontmatter owned_files may change. create_intent identifies genuinely new paths.
Read frozen original catalogues, old contracts and prior reports without editing them.
Do not edit old prompts, spec/plan/continuation, sources.json, old renderers, production
application code, raw evidence, runtime lifecycle or acceptance-matrix.json. If a
prerequisite is insufficient, publish a scoped blocker, not an out-of-map repair.

## Immutable original-source identity

Pin approved WP13 commit `18d6afe95ffcd676fc3f9e964dcad884c9a8c289`:

| Source | SHA-256 |
| --- | --- |
| docs/research/command-scenarios.json | 8161fe7e5f032aa459c8f33a149a00f6e7263cd153f613533d297eeca9ec8d4a |
| docs/research/feature-inventory.json | 633cad8fbcc3e59a13bf0003566bfdb2f9925c26a5899a54a989a65da91138d5 |

The approved source has 244 scenarios and 91 groups. Older primary has 236 cases,
with scenario SHA a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0
and inventory SHA 49d37c3f13a537609346bc71751dabb8661676ecfa8fa40f25cee0752b5bccf8.
Do not silently initialize from that older primary snapshot. Verify Git blob bytes
against hashes before importing. Preserve IDs, exact titles, source/version/locators,
baselines and ordered case/feature back-links. Record source revision explicitly.
For reproducibility: `git show 18d6afe:docs/research/command-scenarios.json | sha256sum`
and the equivalent feature-inventory command are read-only source checks.
Old render-scenarios.py:65 rejects implementation_status other than not-implemented;
render-inventory.py:51 requires an evidence-schema extension before progress claims.
These historical original-reference labels are retained, not relabeled current passes.

## Definition of Done

- Every declared subtask has actual executable deliverables, public-interface validation
  and bounded evidence. Do not tick off planning text as implementation.
- Exact approved original source identity is preserved; only owned new current surfaces
  change. All historical original-only labels remain historically accurate.
- Evidence levels, open coverage and physical/resource gaps remain distinct and checkable.
- Current README authority (WP30) and versioned index remove contradictory current claims.
- Full M1 scope and SC-001–005 are retained; no runtime acceptance matrix or lifecycle
  is directly edited and no mission acceptance, merge or M2/PDF begins.
- Changed Python compiles and relevant tests/checks pass. Any changed Go code, if ever
  separately authorized, must meet charter formatting/build/test/vet; this WP owns none.
- Use normal runtime subtask status records only for actual completed work and submit
  independently reviewed exact commits; no self-approval or fabricated verdicts.

## Risks and review guidance

Review source/version identity, full inherited/discovered coverage, public executable
behavior, negative tests, atomic failure/idempotency, evidence admissibility and current
entrypoint wording. Verify no new path masks copied/renamed old code or fake ownership.
Schema validity establishes evidence-tool integrity, not historical behavior fidelity.
If a contract/source is unavailable, record the exact bounded blocker and preserve open
status. Do not weaken comparison criteria or repair dependency code out of scope.
