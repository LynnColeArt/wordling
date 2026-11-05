# Independent task review

Verdict: **APPROVE canonical WP77–WP78 for finalization and issued implementation claims.** Date: 2026-11-05. Reviewer: `everyday_baseline_audit`.

The staged future WP79–WP89 remain planned work under `planned-packages/`; their task design and product coverage are reviewed below, but they must not be allocated until the recorded runtime naming defect is repaired and canonical finalization is repeated. This staging preserves the complete editing and proofreading milestone.

## Canonical validation and identity preservation

Ran the read-only command from the feature checkout:

```text
spec-kitty agent mission finalize-tasks --mission wp51-parity-01M64CVY --owned-checkout /home/lynn/projects/wordling --validate-only --json
```

Result: `validation_passed`, 78 work packages. Only WP77 and WP78 require the ordinary finalizer's branch-strategy normalization; all earlier 76 prompts are reported unchanged. Historical absent-path ownership advisories remain warnings, not evidence that their unrelated source is newly implemented.

A separate read-only invocation of the installed canonical `compute_lanes` over the task frontmatter/bodies produced 27 total lanes: the existing planning lane plus 26 code lanes. Compared every old WP-to-lane membership with `runtime-before.json`: **zero changes**. WP77 maps to `lane-z`; WP78 maps to `lane-planning`. There is no dependency cycle. No lanes, lifecycle state, index or refs were changed by this review.

WP77 has a legitimate source input in the committed feature-target intake, so it need not declare a reverse dependency on old WP76. Its required review explicitly covers the complete 23-path candidate delta after `f89a48627916b5cb9e360c35047350031b6f06a9`, as well as its new probes. That source remains UNREVIEWED until its separate implementation review approves it. WP78 independently qualifies original evidence and does not depend on unfinished product source.

## Resolved task findings

The initial all-89 canonical dry run failed because new overlapping storage/document/editor/TUI scopes lacked ordering relative to old owners. The planned prompts now add WP79→WP41, WP80→WP74, WP82→WP75 and WP84→WP76. A pure combined-graph check including all planned prompts is acyclic, and canonical `validate_no_overlap` reports **zero errors**. These edges record real predecessor ownership; source intake alone is not a substitute for ordering.

The generic live-caller requirement previously contradicted foundational packages that precede their production consumers. The amended rule now requires public API integration evidence for a layer, names the future consumer, and requires normal executable reachability in the consumer and final qualification. This resolves the contradiction without accepting unused implementations as product completion.

## Future allocation hold: runtime naming defect

With all 89 prompts, the installed 3.2.7 canonical computation preserves every old membership and remains acyclic, but generates WP81=`lane-{`, WP86=`lane-|`, WP87=`lane-}` after `lane-z`. `branch_naming.py` accepts only `lane-[a-z]`; generated names fail `lane_branch_name` → `parse_lane_id_from_branch` round-trip. `lanes/recovery.py` uses that parser to recognize and discover recoverable lane branches. This is an actual runtime identity defect, not a product architecture defect.

D-EE-14 correctly stages WP77/WP78 while retaining the natural layout/proofreading/final-qualification scopes. Repair generation and its consumers independently with boundary, old-name preservation, branch identity, recovery and ownership-guard tests before authoring/allocating the remaining packages. Do not introduce artificial ownership overlaps to evade this limit. Repeat canonical validation and the complete original-membership comparison afterward.

## Product and proofreading coverage

The component packages cover the approved browse/Look/retrieve, native editing/history/attributes, physical layout, navigation/Reveal, Search, original saves/backups, two-screen lifecycle, menus/Help/preferences and uninterrupted final executable journeys. Future product-code findings return to their owners rather than granting the final qualification package broad source authority.

The EE-015/EE-A15 amendment and WP87–WP89 add a real resource-backed provider, editor-native contextual correction state, and original Ctrl+F2 presentation. They include scope boundaries, repeated occurrences, suggestion/correction, per-pass versus persistent choices, Edit-and-resume, cancellation/restart, resource provenance, dictionary format/persistence and final native interoperability. WP86 depends on WP89, so a provider-only or UI-only proofreading implementation cannot satisfy final acceptance. Resource substitutions require explicit reviewed limits; absence cannot be disguised as success.

The amended product plan remains inside M1, retains complete parity obligations and leaves PDF in M2. Staging tasks is not a scope reduction or a claim that the future packages are approved implementations.

## Reviewed canonical prompt identities

| Prompt | SHA-256 before ordinary finalizer normalization |
| --- | --- |
| WP77-everyday-baseline.md | b8f159a43cd9a4acc773a1464299a15e50bf68eff0d71c3201676edaf53e45e0 |
| WP78-everyday-reference.md | 39eb8d59b9a2a2166491d7b4e0ab42c4daf7d0ea3d5411bcbd064ef646825924 |

After committing the planning amendment, canonical finalization should refresh its planning snapshot and preserve the existing lifecycle history. The actual issued workspace and candidate ancestry must still be checked at claim time. This approval is not approval of candidate implementation, any full-mission gate, or publication to `main`.

## Independent runtime repair review

Subsequently reviewed the four-file repair prepared at `/tmp/wordling-kitty-lane-repair/repair.patch` and its before/after manifest. Verdict: **APPROVE scoped application of that exact repair**, with post-install verification before future package finalization.

The change preserves a–z and generates bijective aa, ab, … suffixes. It updates the canonical branch parsers, legacy merge resolver and implementation-branch commit guard to accept multi-letter suffixes, excluding reserved `planning`. A search of installed Python consumers found the remaining sync parser already accepts multi-letter suffixes.

Independently verified all installed bytes still equal the manifest's before hashes and both prepared trees match their hashes. Executed the prepared tests in an isolated interpreter without modifying the installation: 10,000 unique suffixes, a/z/aa/zz/aaa boundaries, negative rejection, allocation sizes 1/26/27/29/52, modern/legacy branch identity, merge resolution, guard recognition and malformed/reserved exclusion passed.

Additionally computed this mission's complete 89-package graph with the prepared modules. All 76 old mappings remain unchanged; new mappings include WP77=z, WP81=aa, WP86=ab and WP87=ac. Every generated code branch round-trips through the canonical parser and is recognized by the implementation commit guard. The graph remains acyclic. This specifically addresses the recovery parser failure found above.

After installation, verify exact installed after hashes and run fresh-process diagnostics, canonical all-89 validate-only, full mapping preservation and normal claim/workspace verification. No real aa-branch allocation/review lifecycle was performed during this read-only review, so that operational behavior remains an execution check rather than a fabricated test claim. No source, installed tooling, lifecycle state, git index or refs were mutated by the reviewer.
