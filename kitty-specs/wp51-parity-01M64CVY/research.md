# M1 discovery checkpoint — 2026-10-30

## Decisions and evidence

This checkpoint incorporates the existing research; it does not declare complete manual study or application parity.

- **Target:** plain U.S. English WordPerfect 5.1 DOS dated 03/09/92. See `docs/decisions/0001-reference-release.md`, `docs/research/reference-baseline.json`, and `reference-execution.md`. The executable is fingerprinted; FreeDOS and the mixed-date Standard Printer resource profile are explicit limitations, not historical MS-DOS equivalence.
- **Delivery:** complete original parity is M1; PDF and modern conveniences are M2 after acceptance. Intermediate implementation slices do not narrow M1. Binding rules: `docs/roadmap.md`, `docs/compatibility.md`, and `spec.md`.
- **Native storage:** preserve original bytes, prefix/index/packet relationships, opaque data, and original character identities. SDK51 WP pp. 3–8 and 17–18 describes framing; later toolkit publication requires reconciliation against the selected executable. Preserve framing separately from semantic interpretation; refuse unsafe mutation. See `docs/research/findings.md`.
- **Editor semantics:** one authoritative model serves normal editing and Reveal Codes. Typeover, blocked paired-code deletion and three-level Undelete are command-specific, established by bounded original-app probes. The existing command catalogue and native fixtures are the contracts, not a generic textarea or undo stack.
- **Automation:** macros and merges share some tokens but have distinct execution contexts. FOR EACH quoted values, nested NEXT, file-level BREAK and global merge pagination have observed edge cases. See `docs/research/reference-environment/values-secondary-probes.md` and preceding family reports. Preserve those distinctions in planning; do not generalize from token names.
- **Evidence:** 236 representative scenarios across 91 coverage groups; 53 partially observed, 183 not run at this checkpoint. All Wordling implementation statuses remain not implemented. Canonical machine-readable records are `docs/research/command-scenarios.json` and `feature-inventory.json`; rendered summaries are generated, not separately edited.
- **Stack:** Go and Bubble Tea on Linux. Rendering must not determine document, code, layout, character, macro or merge semantics. No new dependencies are selected by this checkpoint.

## Planning readiness

There is enough evidence to plan a lossless native reader and byte-identical no-edit round trip, then bounded editor commands tied to existing original fixtures. This does not authorize a general native writer, automation runtime or parity claim before their corresponding evidence exists. Plan remaining research as explicit, reviewable work alongside implementation rather than indefinitely extending an unstructured probe series.

## Open investigations to retain in the queue

1. Reconcile all manual/workbook/toolkit obligations against the 03/09/92 release; close unstudied subcommands and resource formats without silently excluding utilities.
2. Expand negative/malformed/encrypted/large-document coverage and identify safe limits for each editable native structure. Determine original recovery behavior before permitting edits.
3. Establish historical DOS and additional printer/font/graphics/language profiles; declare resource-specific comparisons and redistribution boundaries.
4. Establish layout/print metrics and measurable Linux latency/size targets on declared hardware; no invented performance threshold.
5. Extend automation expression, error, nesting and pagination matrices beyond the bounded observations. Quoted FOR EACH values and macro BREAK results are observations, not explanations of all interpreter behavior.
6. Validate every writer slice by original retrieval/edit/print/save plus unrelated-byte preservation. No-edit byte identity alone does not establish semantic edit compatibility.

## Audit trail

`research/source-register.csv` indexes pinned external sources; `research/evidence-log.csv` links decisions to durable in-repo evidence. Detailed research remains in `research-notes.md`, `reference-execution.md`, and `docs/research/`. No proprietary executable or manual is added to the public repository.
