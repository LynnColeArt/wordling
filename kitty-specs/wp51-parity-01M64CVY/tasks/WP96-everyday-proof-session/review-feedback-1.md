# WP96 independent review, cycle 1

Request changes on frozen `af625c2653c47e9e1ee45c2d8ab55d7df7c42153`. Merged review lane head `7b1f69a1` has no source drift. The five source paths are within WP96 ownership and approved WP88, WP94, WP95 and WP97 sources are ancestors. Full Go build, test and vet, fresh editor/provider tests, focused editor/provider race, formatting and diff checks pass. Inspection and tests confirm the actual licensed ESDB provider, authenticated supplementary operations, stale and foreign refusal, detached resource outcomes, native correction/history retention, remembered/skip separation and Spell Edit/F7. The reported original roundtrip hashes independently match candidate `8659bfb59b321135eefb1fa1ad037527705f5f7c200b769660cba75e2000ea3f` and original resave `e70e05c25d908acac05a110fd14f9f29f82f66e3dbfed8e052908c69791fcd41`.

## R96-001 — Ordinary hyphen boundaries and Count misidentify the native words

Fresh 03/09/92 DOS on `well-known well-zorbly.` accepts the first compound's parts, questions only `zorbly` in red cells 16–21, and reports four words in Document check and Count. Raw original capture and script are in `/tmp/wordling-WP96-review-compound.hrgoeo27`. Original isolated Count results in `/tmp/wordling-WP96-review-count.w9p29dy0` are `can-t` = 2, `123` = 0, `123abc` = 1 and `a` = 1.

Frozen public Session instead reports Not Found `well-known` at [0,10), then Not Found `well-zorbly` at [11,22), no suggestions for either, and count two. The licensed lexicon and the atomic native correction both reject the merged hyphen token. The current scanner consumes an internal hyphen as a lexical joiner and counts pure numeric tokens. Its existing mixed Count=6 test passes because those two effects compensate. Reproduction through the actual loaded ESDB provider is in `/tmp/wordling-WP96-review-public.ST4nP5/public.log`.

Correct T315 lexical boundaries so ordinary hyphens delimit the original suspect ranges and Count excludes purely numeric words. Preserve internal apostrophe, existing DSRt/SRt and observed alphanumeric behavior. Assert isolated original Count values and the exact 16–22 half-open questioning span. Exercise real correction of a misspelled constituent without consuming or replacing its hyphen. This is a session correction within the existing WP96 owner paths.

## R96-002 — Double Word across two spaces is silently missed

Fresh 03/09/92 DOS text `the  the fox` highlights both words and offers 3 Delete 2nd. Original choice 3 produces exact native body `the  fox`, stopped file SHA-256 `51e84ee07d5544ed7d8f8e2f7987c28cfa509d629e4549b1cc39cdbf1047084d`, in `/tmp/wordling-WP96-review-duplicate.o9wg54ie`. The complementary `the  the.` original yields `the .`, SHA-256 `32380abb637d73818e1cdcb14dbbe5ee95e594b1f75042b235b5e0555a01aa37`, in `/tmp/wordling-WP96-review-dup-period.h7u6xqun`. Together these show removal of the second word and exactly one preceding ordinary space, retaining the other space and any following separator. Independent `well-known the  the can-t the the.` captures in `/tmp/wordling-WP96-review-punctuation.5kW4N1` show both two-space and one-space cases in one pass, with the first pair highlighted in cells 11–13 and 16–18.

Frozen Session completes `the  the` without questioning. Its detection requires exactly one ASCII space. A direct public native probe of the same complete two-space word owners confirms existing WP97 DeleteProofDuplicate atomically refuses, so a session-only widening would produce a broken affirmative action. The live status also exposes only the second word's span while the original highlights both separate spans.

For T316, qualify this exact separator behavior and expose both actual native highlight spans for WP89. Keep the native mutation in the document owner through a separately reviewed narrow repair, preserving the existing atomic proof receipt, lexical boundaries, formatting, unrelated bytes and old Undelete entries. Then route WP96 detection and selection through that approved operation. Assert both stopped-original native output bodies, prior history and correct skip behavior in editor tests. No broader whitespace handling is inferred from this two-space evidence.

| Check | Result |
| --- | --- |
| Dead code | PASS. Public session drives the admitted provider and native receipts. WP89 owns actual terminal dispatch. |
| Synthetic fixture | PASS. General lexical resources and original formatted fixtures are used in production tests. |
| Silent empty return | FAIL. The witnessed hyphen parts lose usable suggestions, and the two-space duplicate receives no question. |
| FR coverage | FAIL. Exact original punctuation, Count and duplicate correction journeys have public red cases. |
| Frozen surface | PASS. Only five owned editor paths changed. |
| Locked decision | PASS on licensed lookup adaptation and native preservation. The findings concern original workflow/owner boundaries rather than lexical ranking. |
| Shared ownership | PASS. WP96 follows approved WP94 in G. The duplicate native operation requires independent review before source intake. |
| Production fragility | PASS. No new panic or unconditional retry observed. |
