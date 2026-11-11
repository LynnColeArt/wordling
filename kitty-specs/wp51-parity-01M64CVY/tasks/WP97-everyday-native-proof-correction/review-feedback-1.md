# WP97 independent review, cycle 1

Request changes on frozen source `de2371360bee4bd78f630ba7a534665be4195020`, issued base `036e1ba6` with approved WP92 `bfea5e24` in ancestry. Scope is exact to the three owned source paths and their existing shared document lane.

## R97-001 — Short interior ranges are accepted as complete proof words

`ReplaceProofWord` at proof_correction.go checks that the caller-supplied glyphs equal the expected spelling. It does not check the outer lexical boundaries of that range. In an admitted document with body `abcdef fox`, call the public method with gap [0,3), expected `abc`, replacement `edit`. It returns success and native body `editdef fox`. Gap [1,4), expected `bcd`, replacement `edit` also succeeds, producing `aeditef fox`. See the independent executable source and output in `/tmp/wordling-WP97-independent/`.

The exact native proof-word operation must refuse unrelated short partial spans before publishing. Resolve outer neighbors through zero-width formatting and no-separator derived line/page owners; lexical spaces and explicit page boundaries terminate words. Retain the witnessed first-64-character exception at the beginning of the native word, with its untouched residue. Do not admit an interior 64-character substring. Add public regressions for plain and formatting-separated partial ranges, unchanged refusal, and the valid witnessed capped and enclosed cases. The existing source equality check, bounds, receipt authority and original Undelete behavior must remain.

## Verified remainder

Original output WLP97.WP SHA-256 `8659bfb59b321135eefb1fa1ad037527705f5f7c200b769660cba75e2000ea3f` and returned REP97.WP SHA-256 `e70e05c25d908acac05a110fd14f9f29f82f66e3dbfed8e052908c69791fcd41` match the pinned private run. Existing tests preserve enclosing attributes, relocate observed interior attribute owners, apply the bounded duplicate action, keep NE Undelete, reject forged/stale history and keep the old native file on refusal. Full Go build/test/vet, fresh targeted document race, gofmt and scoped diff checks pass. Existing passing cases do not exercise the short partial span above.

| Check | Result |
| --- | --- |
| Dead code | N/A at native layer. WP96 owns the production consumer. |
| Synthetic fixture | PASS. Original exact native comparisons and live roundtrip, plus public probes using a real admitted prefix. |
| Silent empty return | PASS. No-op and refusal are explicit. |
| FR coverage | FAIL. T318 does not enforce checked outer boundaries. |
| Frozen surface | PASS. Only assigned document paths changed. |
| Locked decision | PASS apart from R97-001. Existing native safety, ownership and on-disk compatibility are preserved. |
| Shared ownership | PASS. Existing WP92 shared source is coordinated in lane E. |
| Production fragility | PASS. No unconditional retry or newly introduced panic. |
