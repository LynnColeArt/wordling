# WP01 independent review evidence — 2026-10-30

Assessment: approve the bounded research handoff. Lifecycle verdict is recorded only through Spec Kitty's review_result event, not this prose.

Reviewed owned artifacts `contracts/native-framing.md` and `contracts/native-fixtures.json` from commits e536854 and c06e6bf, against claim-time baseline 5e02d97. The generated review prompt had no deterministic diff command; scoped `git diff 5e02d97..c06e6bf -- kitty-specs/wp51-parity-01M64CVY/contracts` identifies the two owned files and no raw evidence edits. This reviewer is separate from the researcher who authored them and loaded reviewer-renata plus review-action governance.

## Acceptance evidence

- T001: Verified actual pinned SDK51 extracted text at the declared WP-3–8,12,16–18,23–26 locators for header fields, little endian widths, linked blocks, general packet entries, special/deleted entries, packet 8 and body/fixed framing. Exact PDF and extraction SHA-256 hashes match. The later toolkit publication and FreeDOS/mixed-date printer limitations are explicit. Unsupported variants are separated from malformed framing; payload/nested semantics remain unvalidated rather than falsely accepted.
- The body-length discrepancy is represented honestly: actual original merge primary/secondary contain eight-byte DE functions with L=4 and mirrored framing. The field-derived full span L+4 agrees, while the manual's nine-byte prose minimum does not. The contract labels this bounded observation rather than inventing a universal semantic rule.
- T002: All six original output paths, sizes and hashes match corresponding run-manifest evidence; source, scenario, archived runner and baseline links exist. The earlier plain fixture retains its historical catalogue commit pointer. Macro tuple/type/index count are separately recorded and refused by the initial document reader; merge primary/secondary remain ordinary document types. No native fixture was rewritten. New suffix recipes are explicitly synthetic; absent original encrypted/nonzero graphics/trailing-garbage/unknown-packet cases remain visible gaps, not fabricated oracle coverage.
- T003: Input/image/export, block/entry/token/depth and variable-frame budgets are explicit and classified as implementation safety policies rather than DOS format limits. Bounded arithmetic/progress, overlaps, malformed cases, unknown framing, immutable buffer ownership and rejection-before-replacement are stated. WP02 must measure the actual parser and run the declared deterministic/fuzz matrix; WP01 claims no parser or executed fuzz run.

## Reproduced checks

1. Ran the contract's embedded read-only validation: six original fixtures and two synthetic recipes pass source hashes, native hashes/lengths, run-evidence matching, prefix bounds and outer frames.
2. Independently enumerated raw linked-block entries and compared actual packet records and body-token offsets/lengths against the JSON manifest. All agree. Recomputed every maximum: input 683 bytes, prefix 564, body 119, 3 blocks, 9 live/deleted entries, 6 outer multibyte tokens. Packet 8 zero counts and selected-document nonoverlap checks pass.
3. Actual project regression adapter passes inventory, scenarios, adapter tests and real Go discovery. Current repository has no Go packages, so build/test/vet are explicitly skipped with that reason; no Wordling implementation checks are claimed. JUnit artifact: `/tmp/wordling-wp01-review-junit.xml`. `git diff --check` passes.
4. The historical claim-time pytest baseline collection failure and later declared-runner source mismatch remain disclosed. This is a passing current configured command, not proof of a clean comparable historical regression baseline. Supporting gate repair 8409047 was independently reviewed separately.

No blocking findings. Approval permits WP02's bounded reader work, not semantic writes, macro execution, general companion support, layout fidelity, or M1 acceptance. WP02/WP04 dependents were still planned during this review. No source/planning remediation or mission completion action performed by this reviewer.
