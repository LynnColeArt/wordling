# Native merge-code authoring

The reference is US WordPerfect 5.1 DOS dated 03/09/92, using the Standard Printer profile. Fresh private reference runs started from the pinned guest, with separate disk copies for original authoring, original operand navigation, and original consumption of Wordling outputs. Captures and disk copies remain in `/tmp/wordling-merge-structure.A0HUCB`. The repository also carries the original exports and recorded cells for CMD51-134 and CMD51-223.

## Reproduce the Linux journey

From the Wordling checkout, choose fresh output paths.

```sh
go build -o /tmp/wordling-merge-authoring ./cmd/wordling
python3 tests/everyday_qualification/merge_authoring.py "$PWD" /tmp/wordling-merge-authoring /tmp/wordling-merge-authoring-run
go test -count=1 ./internal/document -run 'TestAuthored'
```

The driver launches the normal Bubble Tea CLI in an 80×25 PTY. It uses Shift+F9, F9, F11, Ctrl+F9 and Ctrl+Enter delivered as `CSI 13;5u`. Ctrl+Enter requires a terminal that reports the modifier. In a New document type `Hello `, press Shift+F9 and 1, type a field number and cancel with F1. Reopen and select Field 1 with Enter. Press Ctrl+Enter to append the hard page. Reveal shows `Hello [Mrg:FIELD]1~[HPg]`. Save with F10 to `PRIM.WP`. In Doc 2 type `Alice`, press F9, then Shift+F9 and 2. Repeat for `Bob` and save to `SECOND.WP`. Ctrl+F9, 1 runs the two authored files and produces `Hello Alice` and `Hello Bob`.

For a retrieved `PRIM.WP`, open Reveal and Home Home Up. From the start, three Rights then Backspace remove the adjacent literal `l`. Retype it and use four Rights to get to the operand. Typing `2` then Delete changes `1~` to `2~` while preserving the DE36 frame. The original cells are in `operand/{literal-backspace,literal-restored,at-operand,operand-insert,operand-delete}`. A Delete on the Field owner removes only DE36 and leaves the operand text. The original also removes End Field while keeping HRt, and End Record while keeping HPg, as captured in `deletion2`.

The nested journey selects PAGE ON through Shift+F9, 6, Name Search and Enter. The child writes `C`, Field 1 and Enter to `C:\OUT\CHILD`. The parent uses Shift+F9, 4 for PAGE OFF, writes `P`, Field 1 and Enter, selects NEST PRIMARY through More, and enters `C:\OUT\CHILD` as its native filename. It writes `R` and Enter after the operand. Reveal shows the PAGE and NEST labels and the original native filename. Ctrl+F9 using the authored parent, child and data emits `PAlice`, `CAlice`, `PBob` and `CBob` in order.

## Native comparisons

| Output | SHA-256 | Comparison |
| --- | --- | --- |
| Wordling and original New `PRIM.WP` | `635a545c0bd722194f5aa8fa300e384732428ee2c39c64fbeb99c6e32cc2ccb4` | Complete bytes equal from independent authoring |
| Wordling and original New `SECOND.WP` | `8938b5d63f74f88238aded933922eb6239696312b91151d05f62248b00fee302` | Complete bytes equal from independent authoring |
| Wordling `OPERAND.WP` | `0b22909ca100da4d1d2c41fed0efeb9f19a2b6940f3c9292a8b996160b2ae7dd` | Native body changes only the intended operand digit, consistent with original captured editor cells |
| Wordling `DEL.WP` | `5dcf38fd48bcb2596413db340a90a00c1b1c8cc2fa16aac987c471a018b4100c` | Native body equals original code deletion, whose first-save profile differs from the tested retrieved Wordling document |
| Wordling and original `NOFIELD.WP` | `10aa4f69fbabfbca06fb1e00cb17f82fb5d674f7f5ad16dcfc0b837ca2bdce07` | Complete bytes equal after deleting End Field and decrementing the enclosing End Record count |
| Wordling and original `NORETURN.WP` | `f3bff0f1b58e543c92ca1a3113cd121ab812c4467597dc7d2d203b8e43a7b178` | Complete bytes equal after deleting the exposed return and updating its page cache |
| Wordling and original `NORECORD.WP` | `56d02375129b72eda47d280b60c6af134f73d8bfa82989cbbc19ed6c00f8bf00` | Complete bytes equal after deleting End Record. Reveal highlights `[HPg]` immediately after `Alice`. |
| Wordling `NESTED.WP` | `1dd5dda8d21fbe93d32c6240f3d2cb3fd2bddae94e8aa1bf30d3ecbe45951dcd` | Native body equals original CMD51-223 PRIMARY |
| Wordling `OUT/CHILD` | `e2dbde92ddff4c2ac0864976a94e2ef6f3f016b83fc1094116c14fd32a7b9a17` | Native body equals original CMD51-223 CHILD |
| Original `MERGED.WP` consuming Wordling's authored primary/secondary | `8a2782895e3605538f56f656499df83c0e460fb25458b6cccbaee9aeb6b96bd3` | Complete 683-byte output equals original CMD51-134 MERGED |

The PTY captures and native outputs are under `pty-operand`. A separate private guest under `dos-consume` shows the original release, actual Ctrl+F9 result, settled save and extracted output. Go build, fresh full tests, vet and focused document/editor/TUI/merge race checks passed.

To reproduce the three secondary deletions in DOS, set Fast Save No and retrieve the `SECOND.WP` authored above. Open Reveal, go to document start and move right five times. Press Delete and F10 for each successive save. After the third deletion the first Reveal row begins `Alice[HPg]`, with exactly columns 5–9 (zero-based) active. The release candidate's terminal replay verifies all three complete files and those five active cells.

Authoring uses exact recognized frames and checked operands. It refuses an opaque owner or a cut through a formatter cache, and refuses edits that remove the only operand byte or the native tilde terminator. Nested operands are native text; execution still resolves them through the scoped workspace. The More chooser displays the original command vocabulary, with unsupported entries reporting their state. The tested chooser behavior covers Name Search and selection, rather than a cell-for-cell comparison of every scrolled pane. Structural-source Undelete, operand typeover, general merge commands and wrap beyond the checked authoring layout remain open.
