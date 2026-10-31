---
work_package_id: WP30
title: Versioned conformance schema and current authority
dependencies:
- WP13
- WP18
- WP20
- WP21
requirement_refs:
- FR-001
- NFR-004
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
- T088
- T089
- T090
phase: Versioned conformance evidence continuation; full M1 remains open
history:
- at: '2026-10-31T00:22:15.797693+00:00'
  actor: planner-priti
  action: Authored in temporary next-tranche draft; unexecuted, not accepted
agent_profile: implementer-ivan
authoritative_surface: scripts/conformance/v1/
create_intent:
- docs/conformance/v1/
- scripts/conformance/v1/
- tests/conformance/v1/
- docs/decisions/0004-conformance-evidence-layers.md
execution_mode: code_change
owned_files:
- docs/conformance/v1/**
- scripts/conformance/v1/**
- tests/conformance/v1/**
- README.md
- docs/decisions/0004-conformance-evidence-layers.md
role: implementer
tags:
- m1-continuation
- versioned-conformance-evidence
task_type: implementation
tracker_refs: []
---

# WP30: Versioned conformance schema and current authority

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

Implement a versioned current conformance schema/importer/validator and reviewable
index that preserves historical source identity and defaults every unproved result
open. This tooling can complete independently of WP29 and makes no parity claim.

## Context and prerequisites

Dependencies: WP13, WP18, WP20, WP21. WP13 supplies approved original source/case
identity; WP18 exposes actual bounded executable behavior that must not be overstated;
WP20 retains resource/physical qualification gaps; WP21 retains documentary leaves.
No WP29 evidence is needed to build truthful schema/tooling with unverified defaults.
Apply the approved evidence-layer decision; record it in ADR0004 rather than changing
product architecture, mission scope or native formats. FC-001 through FC-010 stay binding.
The current registry/index has explicit current authority; old catalogues are historical
original-reference snapshots, not a competing current implementation ledger.

### Subtask T088: Versioned schema and exact approved-source import

**Purpose:** Make provenance, full retained coverage and independent evidence levels
machine-checkable before any compatibility claim.

**Steps:**
1. Create docs/conformance/v1/schema.json and registry.json plus an executable importer
   in scripts/conformance/v1/. Use project-standard-library Python unless an already
   approved dependency provides a justified smaller solution; do not upgrade dependencies.
2. Import the exact approved source blobs specified below, binding revision/hash/count,
   all 244 scenarios, 91 group identities/back-links and all 38 obligations from the
   actual spec/compatibility/continuation inputs. Do not assume 244 is complete breadth.
3. Import discovered leaf/disposition records from actual WP21 evidence and resource
   gaps from WP20, with their own source hashes and unresolved/open states preserved.
4. Define versioned case extensions with stable collision-checked IDs, parent links,
   source/version/page locators, declared starting state/steps/expected outputs and
   revision lineage. No local probe name alone becomes a canonical acceptance case.
5. Separate all evidence levels listed below. Default implementation/differential and
   physical qualification unverified; historical original observations retain exact scope.
6. Define a positive-evidence contract binding case revision, implementation commit,
   independent review, executable invocation, input/raw output hashes, reference baseline,
   environment/resources, comparator/tolerance and precise tested scope.
7. Specify deterministic read-only check and explicit regeneration/import modes. Checks
   must not rewrite registry/source files; unsupported schema versions fail clearly.
8. Keep source identity and current verdicts separate; additive extensions cannot erase
   inherited obligations or silently reinterpret an original recipe.

**Files:** docs/conformance/v1/schema.json, registry.json; scripts/conformance/v1/
importer/validator entrypoint; tests/conformance/v1/ public-CLI fixture tests.
**Validation:** Clean import reproduces exact IDs/counts/hashes and defaults; rerun is
idempotent. Check mode fails on corrupted input while leaving all source/output bytes
unchanged. Source hashes from Git and working data agree before accepted import.

### Subtask T089: Executable validation and current-authority documentation

**Purpose:** Publish one clear current conformance entrypoint and reject false closure.

**Steps:**
1. Implement the validator against declared schema semantics through a documented CLI;
   do not merely validate JSON syntax or trust caller-supplied passed booleans.
2. Validate complete inherited coverage, referential integrity and extension lineage.
   Validate positive claims against exact evidence bindings and distinguish unsupported,
   unexecuted, failed, blocked and qualified states without converting any into passes.
3. Keep parent closure unavailable while required children/known breadth are unresolved.
   Require explicit dispositions for version/platform discrepancies and scope decisions.
4. Generate docs/conformance/v1/index.md with bounded counts by evidence level, open
   obligations/resources/leaves and source revision. No full-parity percentage shortcut.
5. Author docs/decisions/0004-conformance-evidence-layers.md recording charter WL-004,
   source provenance, extension protocol and why original-only catalogue status is frozen.
   Address older contracts requiring canonical expansion before acceptance: the new
   versioned extension mechanism must supply authored semantics, not rename local probes.
6. Update root README.md to identify the current registry/index and bounded implementation
   accurately. Label links to old generated pages as historical snapshots with source
   revision/date; their old present-tense labels must not look like current product claims.
7. Explain conformance schema versions are tooling only. Preserve the two-mission
   boundary, original native/companion formats, and every full M1 success criterion.
8. Document future normal acceptance-matrix evidence linking, without editing that matrix
   or pre-authoring passing requirement rows. Schema correctness is not parity evidence.

**Files:** executable validator, generated current index, README.md, new ADR0004 and
public-CLI tests, all within owned scope.
**Validation:** Reviewer follows root README to current authority and can locate frozen
source provenance, every retained obligation and new extension identity without seeing
contradictory current claims. Check/regeneration round-trip is deterministic.

### Subtask T090: Negative integrity tests and independently reviewable tooling evidence

**Purpose:** Prove the validator rejects realistic evidence/coverage corruption.

**Steps:**
1. Test missing/duplicate inherited IDs, omitted obligation/group/leaf, unknown parent,
   broken source locator/back-link, source hash drift and wrong 236-case primary input.
2. Test a passed claim with missing raw evidence, wrong input/output hash, stale code or
   case revision, missing executable invocation/review and unknown resource profile.
3. Test original-only/helper-only evidence masquerading as executable differential proof;
   resource presence masquerading as qualification; local pass closing a broad parent.
4. Test duplicate extension ID, altered inherited behavior without lineage, unsupported
   schema revision and unexplained exclusion. Each failure reports the offending record.
5. Exercise the executable CLI externally, asserting exit status/output and unchanged
   input bytes; avoid tests that mirror private implementation details.
6. Publish reproducible commands, results and scope limits under docs/conformance/v1/.
   Bind executing script/test blobs and schema revision; do not claim WP29 execution.
7. Run relevant Python compile/tests plus old catalogue render checks when inherited
   files are present. Any unavailable legacy input is explicit, never a synthetic pass.
8. Submit for independent review using normal runtime; record only actual subtask work.

**Files:** tests/conformance/v1/, validator fixes and bounded tooling verification report.
**Validation:** Positive and all meaningful corruption tests pass; immutable source bytes
and old paths remain unchanged; index still marks unproved product behavior open.

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
