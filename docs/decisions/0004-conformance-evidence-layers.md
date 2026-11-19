# ADR 0004 — Historical reference snapshots and current conformance evidence

Status: implemented for bounded WP30 tooling; independent implementation review pending.
Audience: maintainers and reviewers assessing evidence, coverage and future acceptance.

The original catalogue describes documentary expectations and original-only probes.
Its existing validators deliberately require unimplemented/pending product labels.
Approved WP13 extends that catalogue to 244 scenarios; older primary snapshots have
236. Meanwhile independently reviewed components exist. Treating old labels as
current would contradict actual bounded progress; changing original-only rows into
product passes would erase evidence distinctions.

Keep original-source catalogue rows and generated views immutable at their approved
snapshot. Add versioned current tooling in docs/conformance/v1/, scripts/conformance/v1/
and tests/conformance/v1/. The root README and current index identify this authority
and explicitly date/classify links to historical views. Source revision/hash checks
prevent accidentally importing the older catalogue. No files are moved or relabeled
to evade ownership; WP30 and dependent WP31 honestly share this new namespace in
sequence, with all declared dependencies retained. Installed runtime migration,
private merge functions and codebase-wide exemptions are unnecessary.

This follows charter WL-004's separate discovery, original, implementation and
comparison evidence; WL-007's complete retained scope; spec FR-001 and SC-001–005;
and the conceptual data model's explicitly unfinished on-disk schema. It changes
no product scope, native/companion format, baseline, resource rights or M1/M2 gate.
The rejected alternative is promoting historical original observations into current
product verdicts; another alternative, writing the old shared catalogue downstream,
would also create a lane contraction cycle. The selected separation has a real
semantic purpose independent of that topology benefit.

All 38 obligations, 91 groups and inherited cases are retained. Full WP20 resource
and WP21 leaf/proposal/lesson/version ledgers remain immutable and open. Known
counts are not complete command breadth. Additive discovered obligations and authored
stable case extensions retain source/version/locator, parent links and explicit
lineage; no local probe alone becomes a canonical acceptance case. The current
extension mechanism fulfills older contracts' requirement to author canonical cases
before acceptance without rewriting approved historical prompts.

Separate documentary, original observation, component, executable integration,
differential and physical qualification. Positive rows require exact source/review,
case/invocation/executable/raw hash/profile/comparator/scope bindings, with raw
comparisons recomputed and no arbitrary comparator execution. The verifier proves
integrity, not honesty of forged history; independent semantic review remains
mandatory. Missing or unsuitable proof stays open/blocked. v1 cannot close whole
parents/M1 and supports only exact byte/JSON comparisons; future semantic comparators
or complete-coverage closure require a reviewed extension rather than a permissive
fallback. Helper-only, source-only and original-only proof cannot become product
integration/differential proof. Resource presence is not physical qualification.

WP18's actual approved implementation candidate is 72369dbef52b1528e61b840669199efb9466f471.
Its independent cycle-2 review records bounded runnable no-edit behavior, exact
preservation/refusal/reconciliation and physical/full-parity limits. This is context,
not evidence that any complete catalogue scenario or original feature family passes.
The default current registry therefore imports no positive product rows. WP31 later
ingests actual reviewed WP29 outputs with their precise bounded scope.

Read/check modes never rewrite files, check out Git, start guests or execute supplied
code. Explicit import refuses replacement of existing evidence; regeneration validates
before updating only the deterministic index. Future normal acceptance work links
exact current evidence revisions to matrix criteria, retaining every open branch and
resource gap. WP30 does not edit that matrix or approve M1. Queue exhaustion and
schema validity do not authorize acceptance or M2/PDF.

See [CLI and evidence protocol](../conformance/v1/README.md) and
[current conformance index](../conformance/v1/index.md).

Cycle-1 integrity correction: positive rows additionally bind a separate immutable
build-provenance record to actual executable Git blob bytes, exact implementation,
case/revision/scope/invocation/review and captured build context. A declared digest
alone cannot establish binary identity. Distinct build contexts are allowed with
separate consistent witnesses. Immutable source/default-state comparison retains
exact JSON types, with boolean false mission flags explicitly enforced; no input
normalization or general JSON Schema numeric-notation claim is introduced.
