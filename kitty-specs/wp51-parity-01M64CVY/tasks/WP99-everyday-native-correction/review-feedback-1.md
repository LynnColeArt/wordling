# WP99 independent review, cycle 1

Request changes on frozen source `5df5ddd4bbe161ecc38ec1a3d06ce54113b79b97`. The six owner files and approved WP92/WP97 ancestry are correct. Full Go build, test, vet, fresh targeted document race and format/diff checks pass. The stated original Tab, loaded Backspace, block confirmation, history and interoperability positive checks remain useful. Independent hashes match WLP99.WP `edcef28dfb28bd2000bc59ec56592982d1f1726fd40b06894c4f460116bb63a2` and original returned REP99.WP `e4fcb0cacad440ce0cbaec7a117fe56ae8a1bb4483605876f57996eea42b1ae8`. No FastSave receiver admission change.

## R99-001 — Everyday Delete opens a paired-code question but cannot complete it

WP78 corrections frame 27 directly deletes a loaded Bold pair in Reveal while preserving its text and the independent overlapping Underline. A fresh private 03/09/92 reproduction retrieved the exact admitted 324-byte proof-pages BEFORE.WP (SHA-256 `23f2dbe7c2857709510c02787c518d7a8c9701112fb8f4b46cc2bb170ebc246e`), entered Reveal, moved to the BoldOn at gap 4 (Pos 1.4), and pressed Delete. Original save at Fast Save No produced SHA-256 `7ac2b45c1c6fafc2f5b03d5f055cf24a1d613e676e8047784668a5fc53e5532f`; the complete body is byte-identical except removal of the exact BoldOn/BoldOff owners. Raw captures and stopped-guest output are in `/tmp/wordling-WP99-review-pair`.

Against the same admitted native file and a fresh qualified History, the public DeleteEveryday method returns UnsupportedHistoryEffect at token 4 in Reveal. Normal view produces the authentic-looking Delete [BOLD]? No (Yes) prompt, then AnswerDeletion(Yes) returns the same refusal and native bytes do not change. The new everyday path delegates to the old WP40-specific structural-history gate. Independent public probe: `/tmp/wordling-WP99-review-native`.

T322's qualified ordinary native range handling and EE-A07 require this witnessed pair action. Add an everyday checked pair continuation with authentic before/history receipt and exact two-owner removal. Preserve unrelated bytes and the separate format anchor. Keep legacy callers on their existing guarded API. Bind original history behavior before changing the stack (including a prior deletion entry as T322 directs), retain default No/cancel and stale/foreign refusal, and use the actual native pair kind for Bold and Underline prompts. Do not generalize to unobserved repair shapes.

## R99-002 — The witnessed trailing DSRt has no checked everyday Backspace

A fresh private original typed 64 X followed by YZ. It displayed 65 glyphs on row 1 and Z on row 2. One Backspace removed Z and left the cursor at row 2 col 0 with Y still on row 1. The next Backspace moved to row 1 col 65 and still preserved Y, so it removed only the trailing DSRt. Undelete then previewed Z on the following row. Raw before/first/second/Undelete captures and exact commands are under `/tmp/wordling-WP99-review-wrap`.

In the corresponding admitted native first-result body, 64 X + Y + 0x90, DeleteEveryday(Backspace) at the end returns UnsupportedDeletion and leaves the old revision. If an editor eagerly removes the DSRt with ordinary formatter reflow after Z, the next Backspace deletes the wrong native character Y. The independent checked-plan probe also demonstrates two history entries after eager formatting, because the formatter closes the deletion group.

Add a bounded native everyday action for this witnessed trailing DSRt Backspace, validating the complete owner and conserving caret/history without assigning it a lexical space. Bind the observed original grouping and exact bytes in a test. WP94 owns command-specific timing: preserve this trailing derived return through the first Backspace, and route the subsequent one to the checked native action. No broad reflow redesign or FastSave admission change is needed.

| Check | Result |
| --- | --- |
| Dead code | N/A for a native API package with WP94 as consumer. |
| Synthetic fixture | PASS. Actual original files and live original probes support the defects. |
| Silent empty return | PASS for no-op/refusals. R99-001 exposes a prompt whose affirmative cannot execute. |
| FR coverage | FAIL for qualified ordinary pair deletion and trailing DSRt correction. |
| Frozen surface | PASS. Only six owned paths changed. |
| Locked decision | PASS apart from observed command gaps. Native format and unsafe-prefix policy remain intact. |
| Shared ownership | PASS. Existing document lane and legacy guarded callers retained. |
| Production fragility | PASS. No new panic or unconditional retry. |
