# WP85 original menus, Help and Setup

The normal Bubble Tea editor uses the standard US WordPerfect 5.1 DOS 03/09/92 menu family and retains WP84's real viewport and pinned F5 browser. Approved WP84 source `16b3e4467036974653cf055b6199ee97f9ee6be7` is an actual ancestor. The independently checked shared test-only source `e38997d7` entered H through `27ea177d830079b3bf3a6448bcf58a805fc5beef`. The Windows/DOS .SET representation stays outside this implementation. The reviewed Linux app-preference design and decision are preserved beside this report.

## Original behavior and verification

| Contract | Verified behavior |
| --- | --- |
| T269 and EE-002 | Menu titles, mnemonics, native key columns, command groups, panel borders and logical VGA roles are driven by one table. Golden comparisons cover the full inactive/focused bar, complete File and Edit panels, the active Justify child and its retained inactive cells after F1, Escape and Space. Up activates the neighboring Endnote child. The menu table also uses the observed Font, Tools, Search, Mark, Graphics, Help and File Setup vocabulary and its real clipped positions. |
| T270 and EE-002 | Normal keys, menu choices and pointer hits use the same command paths. The physical terminal probe uses Alt+=, the actual Font mnemonic o, F6 from an active menu, SGR File selection, and F7 focus return. The native F6 output contains an exact Bold pair. File Exit uses the observed x mnemonic. Genuine block-dependent items use brackets. Out-of-scope historical commands give a development message when selected. |
| T271 and EE-003 | Physical F3 opens Help, F3 again opens the Enhanced Layout keyboard template, an editing function key selects the corresponding topic inside Help, and Enter returns the original editing cursor. Topic headings, template labels and control names derive from observed behavior. Explanations are authored for Wordling. |
| T271 and EE-003 | Shift+F1, 2 Display, 4 Menu Options and 8 Menu Bar Remains Visible reproduce the original Setup navigation. File → Setup → Display reaches the same state. Choice publication uses a checked regular descriptor and a synced exclusive sibling inside the pinned user configuration directory. Cancellation creates no file. The test suite verifies malformed versions, symlink/FIFO refusal, failed publication retention, and a distinct document workspace. |
| T272 and EE-014 | One historical view composes underlying document, status, menus and modal Help/Setup. A pending settings publication owns input, and clipped invisible menu choices cannot reach native commands. The previous R77-001 12/11-row modal tests and original F5/Reveal PTY retain their conservation assertions. |
| T273 | Three separate ordinary CLI processes verify default Yes, a persisted No restart and a persisted Yes restart. Both profiles deliver actual keys, original cells and menu focus. Each process saves native Bold, exits normally and restores its terminal. |

WP78 raw originals for File, Edit, Layout Justify and top bar are in `qualification/menus`. The matched retained-child repeats are in `qualification/focus-r1` and `qualification/focus-r2`. Fresh selected-release capture folders `/tmp/wordling-wp85-readiness/probe` and `/tmp/wordling-WP85-more-menus.8YF7gn` record other title and Setup panels. Mouse event delivery in the verification uses SGR Linux PTYs. Logical role comparisons use the documented ANSI mapping for the original VGA values 0x71, 0x74 and 0x47.

The original Environment → Backup Options → Original Document Backup path sets the active session's native backup preference. The model test writes a real prior `.BK!` snapshot, then switches the setting off and verifies its removal on the next native replacement. This Linux configuration format persists menu visibility. Proofreading starts in the succeeding resource and UI packages.

## Search trace and follow-up

Fresh original `/tmp/wordling-WP85-search-menu.drGjEX` starts with `alpha beta alpha gamma alpha` and shows Search Next and Previous execute the remembered search immediately. The menu uses the same editor events as the F2 family. Original first/next/previous status shows Pos 1.5/2.6/1.5. The editor source inherited at WP85 submission places the caret at the first owner of each match. This editor-owner correction is tracked separately so both menu and direct F2 receive the same native behavior.

## Commands

```sh
go build ./...
go test ./...
go vet ./...
go test -race ./internal/tui ./tests/baseline_adoption
go build -o /tmp/wordling-wp85 ./cmd/wordling
python3 internal/tui/evidence/everyday-menus/pty-menus.py "$PWD" /tmp/wordling-wp85 /tmp/wordling-wp85-menus-fresh
```

The baseline wrapper imports the frozen WP84 driver and translates added menu border characters to one-cell observer equivalents. WP84 assertions remain in their original driver. The WP85 driver separately compares exact menu geometry and attributes against original VGA. Linux terminal glyph rasterization and theme palette can vary.

## Verified output

- Ordinary binary SHA-256 `c4d09fdc0e9485f0578bc8bddb6935db8d12b982ca0fa74f2ffabaca066babb8`.
- Three original-profile PTY processes recorded in `/tmp/wordling-WP85-frozen.nZCKLM/menus`; steps per process 34, 32, 28. Their native files end in the exact expected Bold owners and each normal exit restored terminal attributes.
- Retained WP84 terminal run in `/tmp/wordling-WP85-frozen.nZCKLM/wp84` passed 50 checkpoints and produced native file SHA-256 `549b55dea301b159bc00ea7910de3695f6169630cfa72f1a2136f74ba39ed7f5`.
- Go build, test and vet passed. Focused TUI and baseline race, Go formatting, Python syntax and Git diff checks passed.

Changed source SHA-256

```text
078a357978cdd9eb66653d722bd510b6182e2ad676fd2265ec975f4e75d4620a  internal/tui/chrome_test.go
6f0b67002d8de498a1a1cf30aca4296843a726ec53f40db16e37127060baa505  internal/tui/historic.go
72c35cc6b1f0328cae8f8a5e2d54cbc50c628a4eb95764f271ea980c08dfae81  internal/tui/model.go
1c10d363ec06f74f2a1b8061d532868b15a32bd077bd6fed74c34778eef923f2  internal/tui/runtime.go
efd79d233bf218d599450c21078d50c33c91ca981de3c32f791d8b86acda0995  internal/tui/everyday_help.go
b353930252289c863d034054ab489477793851e525152c93ca26ace71dda096c  internal/tui/everyday_menus.go
893c196caa0a7a11aee94428428937e28ac0050d7f3e266caec4ee9c064e50c4  internal/tui/everyday_menus_test.go
86b91a36e40663f8e0664718d8e7c22fd26513816e7cbb6a4abf3b5e11e54d12  internal/tui/everyday_settings.go
d7f37136d3ef8c91170b0273942d8371ac3ebda0e0926d693c81622c6cf614db  internal/tui/evidence/everyday-menus/pty-menus.py
55b2f119d8074717557bea155d49e3c918ed2659cde3864511605799462ebb28  internal/tui/evidence/everyday-menus/pty-wp84.py
```
