# WP97 independent review, cycle 2 — approve

Reviewed the exact frozen lane E source `5c142928ff7c256e21faaeb1cb770844c2e12fee`. The two-file retry follows rejected source `de237136`, with the original three owned-path delta and approved WP92 `bfea5e24` preserved. No source was edited by this reviewer.

R97-001 is resolved. Rebuilding my prior standalone public probe now rejects both [0,3) and [1,4) short partial spans of `abcdef fox` as UnsupportedBody while keeping the byte-identical document. An independent second probe rejects partial ranges across either side of D4/91 and across inline formatting. It confirms that outer quote punctuation does not block a full word, an internal apostrophe does, and only a real start-of-word 64-character range can leave the bounded original residue. The complete word across a no-separator page group still corrects. Probe sources and outputs are in `/tmp/wordling-WP97-cycle2-independent`.

I ran the original-interoperability harness against this frozen retry source. It regenerated the exact same 369-byte WLP97.WP (SHA-256 `8659bfb59b321135eefb1fa1ad037527705f5f7c200b769660cba75e2000ea3f`) as the captured WordPerfect 5.1 03/09/92 input from cycle 1. The independently verified original REP97.WP result (SHA-256 `e70e05c25d908acac05a110fd14f9f29f82f66e3dbfed8e052908c69791fcd41`) reopens exactly and accepts the continued Go edit through current source. Original execution evidence remains in `/tmp/wordling-wp97-roundtrip.IEbVDo`. This retry reproduces the exact source file used in that original run, without implying another VM run.

Full Go build, tests, vet, fresh focused document race, gofmt and scoped diff checks passed. Existing tests preserve enclosing attributes, observed interior relocation, explicit native pages, previous NE Undelete, checked plain duplicate deletion, and stale/forged receipt refusal. The new check runs before no-op or publication and does not change the native writer or format semantics.

| Check | Result |
| --- | --- |
| Dead code | N/A at the native layer. WP96 is the normal editor consumer. |
| Synthetic fixture | PASS. Original exact native witness and independent public probes. |
| Silent empty return | PASS. Verified explicit no-op/refusal semantics. |
| FR coverage | PASS for WP97, including T318 lexical boundaries and T319 interoperability. |
| Frozen surface | PASS. Only the two owned retry paths changed. |
| Locked decision | PASS. Original file semantics and prior history preserved. |
| Shared ownership | PASS. Source remains in the existing document lane with approved WP92. |
| Production fragility | PASS. No added panic or unbounded retry. |
