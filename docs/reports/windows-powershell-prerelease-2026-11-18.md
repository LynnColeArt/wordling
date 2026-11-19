# Windows PowerShell and save-overwrite prerelease readiness

Date: November 18, 2026 (America/Chicago).

**Verdict: ready for Windows amd64 engineering prerelease testing.** PowerShell
is Wordling's default Windows Open Shell, and confirmed save-overwrite and
original-document backups pass native tests. Production acceptance, complete
WordPerfect parity, physical-terminal qualification and sudden power-loss
qualification remain separate.

## Verified candidate

[Native workflow 44252454714](https://github.com/LynnColeArt/wordling/actions/runs/44252454714)
passed all three jobs: Linux build/regression, Windows native, and macOS native.
The tested branch head is `0fcffa7c3c93393ad2649195124e58bef8663bae`.
CI compiled PR merge commit `2cee5313ec0d0a0340194a67e893dd2dc34d68bc`;
the downloaded packages' production trees and every compiled local source hash
were checked against the branch checkout and matched. These are normal builds,
with the `wordling_qa` seam excluded. Every packaged file's checksum was verified.

| Target | Verification |
| --- | --- |
| Windows amd64 | Native Windows Server 2025 / build 26100: storage, recovery, settings, PowerShell 7 and Windows PowerShell 5.1 console workflows |
| Windows arm64 | Cross-built and package/source hashes verified; native ARM hardware execution remains open |
| macOS arm64 | Native macOS 26.7.2: storage, replacement, backups, recovery, settings and CLI |
| macOS amd64 | Cross-built and package/source hashes verified; native Intel hardware execution remains open |
| Linux amd64 | Full Go regression, vet, storage/TUI race and packaged smoke checks; additional local QA-tag and interactive shell-return tests passed |

Download the `wordling-native-prerelease` artifact from that workflow. Windows
console transcripts and terminal-library input traces are retained in its
`native-evidence-windows-latest` artifact. Architecture-specific ZIPs contain
`candidate.json`, `SHA256SUMS.json`, the normal application and smoke executables.
The Windows amd64 application SHA-256 is
`c559d583764c6ce14ced62dead462dd0d92ae1f3feceea99053f6dd1682c0e4d`.

## Windows behavior and tests

Open Shell prefers PowerShell 7 on PATH, then built-in Windows PowerShell 5.1.
Profiles load normally; an absolute `SHELL` path remains an explicit override.
The shell inherits the terminal and environment and starts in the selected
workspace. `exit` returns to the editor. This configures Wordling, not the
operating system's default terminal or shell.

The real packaged application was launched from each PowerShell version under
ConPTY. Both passed typing, Ctrl+F1, dirty-buffer cancel/skip, commands and
pipelines, a workspace with spaces and Unicode, shell return with preserved
text/caret, first save, cancelled and confirmed overwrite, resize, menu shell
entry, nonzero shell return and normal shutdown with terminal restoration.
Native testing exposed and corrected the terminal dependency's conversion of
characterless modifier records to NUL. The [documented local correction](../../third_party/ultraviolet/WORDLING-PATCH.md)
preserves genuine Ctrl+Space/Ctrl+@ and Unicode; native record tests also passed.

Storage tests passed repeated saves and backup rotation, backup removal and
preservation, Save As over another document, explicit overwrite consent,
cancellation, stale-file refusal, unsafe-name refusal and directory leases.
Fault tests passed failures before/after native replacement, backup publication,
partial replacement/restoration, rollback and cleanup. An unexpected writer's
displaced bytes remain retained, with uncertainty reported rather than success.

Windows uses native `ReplaceFileW` and a private displaced-file escrow. It does
not emulate Unix atomic exchange with multiple renames. Document and `.BK!`
publication remain separate steps. Local volumes without the required
volume-GUID path/lease support and UNC replacement paths fail before publication.
Windows directory-entry durability across power loss remains unqualified.

## Delivery state

[PR #12](https://github.com/LynnColeArt/wordling/pull/12) is stacked on the native
build work in [PR #11](https://github.com/LynnColeArt/wordling/pull/11), which is
stacked on the recovered source in [PR #10](https://github.com/LynnColeArt/wordling/pull/10).
This pass reused the primary checkout and created no worktrees. Source changes
are committed and pushed. The [November 17 recovery report](infra-recovery-2026-11-17.md)
is a historical snapshot; its native-build blocker verdict is superseded here.
Its broader reference-harness failures and remaining parity work are still open.
See the [native prerelease guide](../testing/native-prerelease.md) for commands
and physical-machine follow-up checks.
