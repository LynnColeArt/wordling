# WP92 independent review, cycle 1

**Request changes** for frozen source `5f56451d`, issued parent
`d70690b43fe276287bdb20fb71443ff7cb013d84`. Both findings are reproducible
under the matched original default profile. No source changes were made in
review.

## R92-001 — The typed reflow path rejects the original Tab edge

The offline pinned 03/09/92 run in
`/tmp/wordling-wp93-original-edges` exported TABEDGE.WP, SHA-256
`426c12a60c6a53ead446cd2a554fbb3f687dc6a829506f2a91348b9ecab7ac99`.
Its 324-byte prefix is followed by 63 `X` cells and
`c1 02 28 23 28 23 4b 00 c1 90 59`. Frame 05 shows
`[Tab][DSRt]` ending the first physical row and `Y` on the next row.
Remove only the derived 0x90 from the in-memory original fixture. The
result parses and passes CheckMutation. Apply an InsertDeletedSoftReturn
plan at gap 64 (between the complete Tab owner and Y). The public
AdoptReflow method refuses UnsupportedBody and leaves the revision unchanged
because reflowOwner requires immediate ASCII on both sides.

T302 must admit this bounded Tab-to-text DSRt transition without weakening
unrelated owner validation. Keep geometry computation in WP93. Preserve exact
Tab owner bytes, distinguish this transition from a lexical space, and test
insertion/removal plus caret/history remapping and invalid edge refusal.

## R92-002 — Soft wrap at a physical page edge needs its witnessed native form

The same run exported PAGEEDGE.WP, SHA-256
`d9329e2d9f84df55f042b622e93cc8d9dc6ffaf6d9b7017ba5a77080aad6a710`.
After 52 HRt and 65 `Q` cells, its body has the same witnessed 32-byte
D4 page record with page 1, followed by `91 51`. Frame 09 shows a
DSRt at the end of the first physical row and the final Q on page 2,
line 1, position 1.1. The existing ReflowPlan only promotes HRt into
D4/8C/99. The original D4/91 wrap is losslessly readable, but token 119
(0x91) is Opaque and CheckMutation refuses UnsupportedBody at 474+1.
The editor therefore cannot produce or continue the ordinary wrapped flow
across that page boundary. This is T302/EE-A04 and does not concern the
separately identified 564-byte Fast Save receiver admission family.

Coordinate a narrow ownership amendment for the native kind/admission
implementation before editing those paths. Recognize the observed matched
group, add typed production/removal/renumbering preserving the underlying
no-separator word, and bind the exact default-profile original export.
Preserve cursor, history and unrelated owners. Refuse lone 0x91 and malformed
or unqualified D4 combinations as mutation input. Avoid inferring other
soft-page forms from this sample; add only separately witnessed rules.
Confirm the following-page position and Reveal owner label with WP93/WP84.

## Independent evidence and checks

The public-API probe source and result are at
`/tmp/wordling-WP92-independent/main.go` and `reproduce.txt`. The official
tab/page fixtures and 80×25 screens are in the reference-run directory above.
I independently hashed the earlier successful original roundtrip, WL92.WP
`629afba5e8ec94cf6ab12283db2bdd823f447f31657305a096624798873e5ffe` and
RET92.WP `1c696ec4983dcddaa0897be39de0ec5d948950f8afa87a87829c77e5b599ff89`.
The selected fragment seam, variable-width history preview/restore and existing
typed-owner/receipt checks remain useful and pass. Exact four-path ownership,
approved WP80 ancestry, gofmt, scoped diff check, full Go build/test/vet and
fresh focused document race tests all pass. Those tests lack these two cases.

| Check | Result |
| --- | --- |
| Dead code | N/A for foundation APIs scheduled for actual WP93/WP94 consumers. |
| Synthetic fixture | PASS. Public tests exercise real native Parse/mutation/history; original captures independently ground the two failures. |
| Silent empty return | PASS. Nil results correspond to refused actions or explicit no-op / removed derived owner. |
| FR coverage | FAIL. T302's physical wrap/page contract cannot represent the two original matched-profile forms above. |
| Frozen surface | PASS. Exact four owned paths changed; no original evidence overwritten. |
| Locked decision | PASS. Raw body replacement removed; original native owner validation and private revision authority remain. |
| Shared ownership | PASS. Existing WP80 document paths are coordinated in the same lane; broaden ownership only through an explicit narrow amendment. |
| Production fragility | PASS. No new panic or unconditional retry in production. |
