---
type: reference
updated: 2026-11-18
audience: Wordling release operator
---
# Mission 1 recovery checkpoint

**Mission 1 and ticket 7 remain open.** Windows native engineering checks pass for the combined candidate; full WordPerfect 5.1 DOS parity and production acceptance remain pending. The local command audit remains186 verified /38 partial /20 unimplemented, and the canonical acceptance matrix remains pending. All 49 continuation families,91 parent groups,36 lessons and complete FR/NFR/SC acceptance stay in scope.

PR 12 was independently reviewed and merged into fix/native-prerelease-builds at40ce35b86afc93710aa12fa12891c85e8360ffaa. Its source is incorporated in feat/wp51-parity. PowerShell is Wordling's default Windows Open Shell (7, then built-in5.1, normal profiles, absolute SHELL override), and Windows save-overwrite/backup/rollback support is included. This is not a main-branch production merge.

[Windows run 44402388644](https://github.com/LynnColeArt/wordling/actions/runs/44402388644) passes native PowerShell 7/5.1 console, save/overwrite, recovery, filesystem and CLI checks on Windows amd64. Exact tested Go candidate:f6cea1cc62dfc89b49cde1f076aaf52751e2a3b9. Verified normal packages are in bin/native-ci-f6cea1cc; [the refreshed report](windows-native-refresh-2026-11-18.md) records hashes and limits. The run has Linux build/regression plus Windows only, with no Mac build/package/job. ARM64 is cross-built only.

The combined candidate includes these independently approved deliveries:

- WP100: authenticated nested macros on genuinely New documents, preserving text/history/source/genesis/first-save behavior. Approval01M7Q8AXKV5THKECEEEQSEXJNV. Four macro audit rows still need original unsaved-New and original reopen/edit/print/save comparisons.
- WP106: balanced native Italics insertion through both insertion APIs. Approval01M7QYDD2V5CJ5F9H4BJ202RXG.
- WP109: the separate native Italics Copy producer. Approval01M7R6F9JH8KQZW8Q99235YWRS.
- WP110: exact queued ordinary Runtime completion ownership before accounting/publication. Approval01M7R8CBK55591MVCGVC0PRNK7. Genuine foreign callbacks cannot settle another request; all ten ordinary kinds retain real own/stale/late/duplicate/error controls.
- WP103: the bounded full coverage index, approval01M7R60MBV83DTHAPHWWFWY3YH. Frozen6d594d15 includes110 registered WPs,2556 numbered documentary steps across36 lessons,5671 typed nodes and1163 Git bindings. This is a dated planning snapshot, not product or lesson execution acceptance.

WP107 is in independent review at source/evidence b5353ff5965ab074629ed398284122986ab5f338. Its two exact public integration tests pass61 leaf cases using genuine rooted selection/Yes/read, loaded own-binding save/reopen/no-edit, edited-New first save, refusals, source/prefix/history conservation and real foreign/late callbacks. Full Go passes3325 leaf cases with4 known environment/platform skips; focused race passes427 leaves. Linux checks and the16-package Windows production cross-closure pass. Six exact later causal replays retain separate native insertion, Copy and host-accounting failures; no production changes were made under107. CI against f6cea1cc uses identical final Go/test inputs. Independent integration approval is required.

Fresh current-TEST qualification WP108 remains in progress. The old expected-inputs.json.gz payload remains unrecovered after recovery archive/Git and home-worktrees searches; [the recovery record](../research/continuation/test-runtime-recovery-2026-11-18/README.md) states the search limits. Current hashes cannot replace V19/188 custody. R1/R2 source design and narrow R3 unaccepted-DATA/API/test design are independently reviewed; actual source implementation, complete reference/tool/native/cache/writer/memory/clock closure, deliberate capture, independent reference/candidate acceptance and genuine public TEST qualification remain pending. Design approval is not operational qualification.

WP104 retains source-only and bounded CONTROL-plan approvals, with all 9 B DATA acceptances recorded at331bfb9d. Operational CONTROL and genuine TEST compatibility remain unrun; the whole-campaign ROOT clock has not started. WP108 must pass before WP104 completion. WP105 remains planned behind104, WP101 behind105 and prior dependencies, and WP102 behind100/101/86. Original occupied Retrieve/Copy and original native reopen/edit/print/save remain mandatory.

The workbook census preserves2556 numbered source steps across all36 lessons, not executed tests. Remaining original/candidate lesson and utility research/execution is not closed by the index. The reviewed local Spec Kitty source, clean-restore-tested repair bundle and actual event-sourced verdicts remain the mission authority; older/global readers intentionally refuse the v2 planning manifest.

The 29 old linked Wordling worktrees were integrated and retired; the primary owned checkout is the only registered Wordling checkout. Approved source through6fe41495 is pushed to feat/wp51-parity; later integration evidence/review still needs its final sync. Other projects' home worktrees remain untouched. Authorized changes are committed; finished replay archives/worktrees are removed.

Bosslady2 is the Linux physical-keyboard host. Its Cinnamon desktop binds Alt+F10 to maximize, so actual delivery needs a physical check; no global key setting was changed. Pink Menace Mac builds/testing are deferred to milestone end by the owner. Physical keyboard/mouse, original interoperability, complete parity and production release are not approved by this checkpoint.
