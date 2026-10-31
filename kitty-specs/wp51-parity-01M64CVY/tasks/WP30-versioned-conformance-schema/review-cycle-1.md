---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-10-31T01:10:30Z'
reviewer_agent: reviewer-renata
wp_id: WP30
---

# WP30 independent review — changes required

Reviewed afe4280bfacb9ca289fa1253c93c157b16fa31b6. These are integrity-tool defects; current registry still has zero positive product rows and no parity acceptance.

## I1 — P2: executable identity is declared, not bound to evidence

**Location:** scripts/conformance/v1/conformance.py:361–378, passing(). **Criteria:** T088 positive evidence contract; T089 exact positive bindings; T090 corruption rejection.

`executable_sha256` is only checked for64 lowercase hex characters; argv basename wordling is the sole executable check. No immutable executable/build witness joins that digest to implementation commit, invocation and independently reviewed run. Existing input/output/comparator blobs can stay identical while an arbitrary executable identity is accepted as a passing differential row.

Independent external public-CLI test extends the existing isolated protocol control with one negative: change executable_sha256 from111… to222…. It still returns exit0 valid/evidence_rows1. Retained baseline/negative run JSON prove this is the ONLY changed run field; raw refs, implementation commit, case/revision, profile and review are unchanged. The isolated Git bundle and raw witnesses are retained. This is not product execution evidence, nor a demand for cryptographic proof that a repository's author is honest; it is a missing machine-checkable join between declared evidence records.

**Fix:** Bind positive product evidence to an immutable executable/build provenance witness with the actual executable digest, source implementation identity, invocation/build context and exact reviewed case/run scope, and verify the joins. A mismatched/missing build/executable identity must fail or remain explicitly open, not pass. Preserve read-only validation and never execute supplied shell/comparator/product code. Do not require identical binary hashes across different build/VCS contexts. Update documented schema/protocol and public tests with valid bound control and wrong/missing executable/source/case/run binding negatives; retain actual raw comparison recomputation and independent review checks.

## I2 — P2: immutable equality silently accepts JSON type changes

**Location:** scripts/conformance/v1/conformance.py:439–441. **Criteria:** T088 exact source/default-state fidelity; T089 declared schema semantics and immutable coverage; T090 corruption tests.

Python deep == treats False==0 and integer27==float27.0. A proposed registry differing only in mission.parity_accepted from JSONfalse to integer0 is accepted exit0 valid. The same validator accepts pinned historical locator pdf_start27→27.0. The clear contract violation is this v1 registry's immutable mission boolean/source identity; this is not an assertion that all generic JSON Schema integer definitions reject mathematically integral floats. New extension locators already explicitly require type int.

**Fix:** Compare immutable JSON trees without boolean/number coercion, preserving the declared/pinned types (or equivalent canonical source identity), and enforce boolean mission defaults explicitly. Reject mismatched typed data before accepting/regenerating; leave proposal, raw sources and existing registry untouched. Add public CLI tests for false→0/true→1 and source-type drift under this exact-source contract, while valid import/regeneration remain idempotent. Do not normalize the input to hide the corruption.

The existing14 tests,2 behavioral mutants and real7-check project gate pass, but do not catch these independent negatives. Full M1/native/M2 scope, open parents/resources and immutable historical catalogue separation otherwise remain intact. WP31 sequentially reuses the same owned namespace and depends on WP30; do not dispatch it from this rejected source. No production editor/storage/codec or original-run changes are required.
