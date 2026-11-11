# WP89 contextual proofreading qualification

The normal Bubble Tea executable consumes the reviewed editor and provider paths. Cycle 2 base d31c2b8f includes WP85 d60550eb, WP96 7f20d18a, reviewed Search a06b7584 and proofreading interruption 18d2dcbf, WP95 f79beb9a and WP97 5c142928. The independent WP86 integrated acceptance remains separate.

## Original comparison

Reference is the pinned US WordPerfect 5.1 DOS 03/09/92 release, Enhanced keyboard, Standard Printer, Courier 10 cpi, 1-inch margins, 80×25, ordinary left tab stops every five screen cells. The product compares logical cells and roles under xterm-256color; it does not assert CRT raster or proprietary lexical identity.

- WP78 spelling/proof frames 01, 02, 06, 08, 11 and 18 establish Check, Not Found, Spell Edit, Count, interruption and supplemental filename. The suggestion traces establish the eight rows, three columns, A–X choice and Enter continuation. The terminal replay compares the full red ruler row, meaningful Not Found action cells and roles, exact red native suspect span, and hardware caret position with these sources. Standalone and contextual lookup keep different focus.
- Fresh reference trace /tmp/wordling-WP89-original.hzHa7l enables the original persistent bar first. The bar hides while proofreading and Spell Edit are active, then restores. Recorded hardware carets (column,row) are Check (13,0), Not Found and its F7 no-op (76,24), Edit (4,0), resumed question (76,24), partial Count (46,24), ordinary restored (4,1). The hardware cursor is an underline. The Linux viewport retains the same focus below the full-size canvas and holds hidden actions until resized back.
- Double Word preserves both separate native highlight ranges, excluding the intervening spaces. The driver checks the actual body after Delete 2nd. The Word/Page witness loads the original attributed BEFORE.WP, finds the word via actual F2, applies the displayed Word correction, corrects the rest of the physical Page, and F10 saves a byte-identical original PAGEONLY.WP. The second page and native attribute owners survive.
- Fresh original mnemonic traces /tmp/wordling-WP89-original-all-mnemonics.Q7cCAE and /tmp/wordling-WP89-original-page-interrupt.SVF1vm verify all six W/P/D/N/L/C routes and the distinct F1 returns. The real Linux PTY reproduces Word directly to Check, Page partial Count then Check, and Document partial Count then ordinary editing at the suspect. Literal C/N still edit the filename/pattern prompts, and the focused model test proves C still selects the displayed suggestion in the questioning phase.
- Production loads the approved ESDB en_US lexical adaptation and the exact native supplementary resource in the pinned workspace root. Displayed suggestions are real provider output; order and contents are not asserted equal to the proprietary OEM lexicon. Tools > Spell and physical Ctrl+F2 use the same reducer. Runtime seals supplementary outcomes and leaves the editor available after a malformed startup dictionary. The checked pinned destination mode refuses Add to read-only resources; read-only resources can still be selected.

## Actual executable replay

Build and execute from the lane with:

    go build -buildvcs=false -o /tmp/wordling-proof ./cmd/wordling
    python3 internal/tui/evidence/proofreading/run_pty.py "$PWD" /tmp/wordling-proof /tmp/wordling-proof-run

The optional --dos-resave <path> also reopens and continues editing an actual stopped original output. The build switch makes source content comparison independent of later metadata commits and does not change the runtime entry point. Every process is the normal executable with only the required -root and -profile local-flat options. The replay uses physical xterm and enhanced Ctrl+F2 escape bytes, F7, F1, F10, Shift+F10 and original menu mnemonics. The styled observer projects the UTF-8 ruler triangle and menu line drawing to one-cell ASCII marks while retaining raw terminal output. No test-only routes or private dictionary bytes are supplied.

Six actual processes passed at /tmp/wordling-WP89-cycle2.XaG6p4/final. The run contains the binary hash, exact sent byte stream, raw output, logical cell/role grids, cursors, exit status, and terminal restoration checks for each process. Original replay inputs, captures and outputs are in /tmp/wordling-WP89.ejMWec/dos-roundtrip.

| Artifact | SHA-256 | Comparison |
|---|---|---|
| Tested production executable | 77e14ed7802b05c1cef5648b8944174ef6b07308588a95235664ff69709bb457 | Six successful processes |
| Wordling PROOF.WP | 8d308448219e5505d3c83365d5425180cd668d2e26045a03b748f103ca38f274 | Exact original native body including SRt; prefix differs only at offset 256 (Wordling 08, DOS 00) |
| Original PROOF.WP | 0eb1b7448881dd041031ec06255dda595e10202633e8b0cdfcf7fe5a332607df | 427 bytes, body starts at 324 |
| Added WP{WP}US.SUP | c82c4ec8e16ff67d5295b1afe6944c2f6d07621dfe369d9597b7031234f337ea | Exact original 73-byte native SUP; fresh process accepts zorbly and its case variants |
| PAGEONLY.WP | da99eb0771e06349d6bb4e1c1edbae783430dc71110f5172987ca265d4a85d7a | Entire file identical to original attributed Page correction |
| MENU.WP | 2e27e2ca4c6e0281a2d31f62f2da1f3df117b8c15c82ac80af6e49a7f50627fa | Exact unchanged native document body after all mnemonic and cancellation routes |
| Original DOS REP89.WP | 1898183430484317f0347e06857455acdaf2761abba673823efe6b048ac39a5c | DOS retrieved the PTY output with Fast Save Off, appended DOSEND and saved |
| Wordling CONT89.WP | 6eaa773147f53770ff863c0262a3e5bd6567d24d9a6968046dd2ca73c5d2a3d5 | Real PTY retrieved REP89, appended GOEND and saved a new native file |

## Verification and scope

T284 is covered by context/focus, native highlight, ruler, suggestion positions, emphasis and footer checks. T285 is covered by the normal startup, physical key/menu delivery and checked filesystem tests. T286 and T287 are covered by the continuous six-process replay, including Skip Once, per-pass Skip, remembered correction, typed Edit, F7, interruption, lookup and pagination, Add, fresh process persistence and native continuation. T288 is this evidence plus independent review. Full Go build, fresh tests and vet, focused editor/TUI/provider/storage race, gofmt, Python compile and git diff checks passed.

Known format limits remain: some default Fast Save 564-byte documents can be inspected by the native parser but refuse ordinary workspace retrieval/adoption; the original typed hard-hyphen 0xA9 family is unqualified for native mutation; and the specialized save-time trailing DSRt regeneration remains open. The tests do not imply support for those producer families or OEM lexical equivalence.

### Source file SHA-256

```text
fb9e374a659e9f883ae0f2e62799f8e9689fc483f12f3ecc57073a25b6212b05  internal/tui/runtime.go
d9f8e63f7a6c8685d45b57fb3f061ac94065d9706d686dab1b13d89cae24ceeb  internal/tui/model.go
487c75ee18bc243c81a3d1b129211ad7346ee38f8d744d4a2283ce22bb26d972  internal/tui/historic.go
81260d5a8e5c2ee771f2b2959ec30b64326d2c6f75c682043528a8c84a3bb709  internal/tui/everyday_view.go
e7697f577ffc9f85ddbf235b20dd8b50ab3fd4060eda7c3972356f48f0d38891  internal/tui/everyday_menus.go
d6ea24dce17f3f463eb732c942639380ea1d24a4c1cfab4d8e69ad6f94e6fdba  internal/tui/proofreading.go
ca8e1083d72d09d768df6fb5a2d96c297ea1c047bc381204c79a81e074ef0e66  internal/tui/proofreading_test.go
b03b7e024f0a3640bdcf141a3e868450369ecfa8966bcee17954265ea6ee4654  internal/tui/proofreading_runtime_test.go
9bb05e670347362720018d8ed478cf325c9be38f53c4677e55f213e1d81d2928  internal/tui/evidence/proofreading/run_pty.py
```
