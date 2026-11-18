# Native Windows and macOS prerelease builds

The native build path is available for Windows and macOS on amd64 and arm64.
These are engineering test builds. Full WordPerfect parity and production
acceptance remain open.

The [November 18 readiness report](../reports/windows-powershell-prerelease-2026-11-18.md)
records the passing native Windows/PowerShell and Mac checks, exact candidate,
artifacts, and remaining hardware/durability qualification.

The `Native prerelease` workflow builds normal executables with the pinned Go
toolchain, records compiled inputs, packages fixture-free smoke executables,
then runs the packages on Windows and macOS runners. Its artifact is named
`wordling-native-prerelease`. Building on Linux avoids the historical research
archive's case-sensitive path collisions in Windows source checkouts.

For Windows-only validation, publish the reviewed commit to the dedicated
`validation/windows-native` branch without opening a PR. That exact push runs
Linux regression and Windows native checks, builds Linux and both Windows
architectures, and creates no Darwin build or macOS job. Manual dispatch also
offers `platform=windows` once the workflow is available for dispatch; `all`
remains the default. PRs retain the existing Windows and macOS checks, so opening
a PR is not a Windows-only validation route.

Fresh Mac testing is deferred until milestone end. A Windows-only run must be
recorded with its run URL, source commit and packaged candidate/input hashes;
it does not refresh the historical Mac results. The fixture-free native smoke
filters do not execute the fixture-dependent `TestNewNested` macro cases, and
the Windows ARM64 package is compiled rather than run on the amd64 runner.

## Windows / PowerShell

Extract the ZIP matching the machine's architecture, then open PowerShell in
the extracted directory:

```powershell
.\console-input-smoke.exe -test.run '^TestWordling' -test.v
.\storage-smoke.exe -test.run '^TestNativePlatform' -test.v
.\recovery-smoke.exe -test.run '^TestNative' -test.v
New-Item -ItemType Directory -Force .\scratch
.\wordling.exe -root (Resolve-Path .\scratch).Path -control-keys
```

Open Shell (Ctrl+F1 or File → Open Shell) prefers PowerShell 7 (`pwsh.exe`
on PATH), then built-in Windows PowerShell 5.1. Profiles load normally. An
absolute `SHELL` environment variable overrides the default; `cmd.exe` and
POSIX-style shells retain their appropriate arguments. Shell commands start in
the selected workspace, inherit the terminal and environment, and `exit` returns
to the editor with buffers and caret preserved. A nonzero shell exit is reported
in the editor. Wordling does not change the operating system's default shell.

Windows supports repeated Save, Save As over an existing file after confirmation,
and original-document `.BK!` backup creation, replacement, removal and preservation.
Cancelled overwrites leave the original intact. Changed source/destination
observations still refuse publication.

The Windows backend uses `ReplaceFileW` with a private escrow containing the actual
displaced file. The document and original backup remain separate publication
steps. The directory's resolved volume-GUID ancestry is held against renames and
checked against the acquired directory identity while calling the path-based API.
Local volumes without that facility and UNC paths refuse replacement. Partial
replacement errors are inspected before rollback; restoration never overwrites
an independent file. If rollback or cleanup cannot be verified, the app reports
uncertainty and retains private files for inspection rather than claiming success.
Do not delete a reported `.wordling-*` residue until the destination and backup
have been inspected. This is not an emulation of atomic two-name exchange.

Recovery uses native exclusive byte-range locks held beside session directories,
so startup publication and cleanup can rename directories while retaining lock
ownership. Candidate and recovery file
contents are flushed, but directory-entry durability across power loss is
unqualified. Windows builds advertise the durability limitation at startup and in the
package README. Successful native tests do not qualify sudden power loss.

## macOS

Extract the architecture-matching ZIP and run in Terminal:

```sh
chmod +x wordling storage-smoke recovery-smoke
./storage-smoke -test.run '^TestNativePlatform' -test.v
./recovery-smoke -test.run '^TestNative' -test.v
mkdir -p "$HOME/wordling-prerelease-scratch"
./wordling -root "$HOME/wordling-prerelease-scratch" -control-keys
```

macOS uses `renameatx_np` exclusive rename and atomic swap for the existing
replacement/backup protocol. If the selected filesystem does not support those
operations, the operation must fail. Local native filesystem behavior still
needs qualification; a successful build is not a power-loss or network-volume
guarantee.

## Native host checks

The smoke executables author their own temporary data. They check native file
publication, byte preservation, collision refusal, cross-directory moves,
repeated replacement and original backups, DOS listing, recovery locking,
recovery snapshot restoration, and repeated settings updates. They need no
private DOS installation or source-tree fixtures.

On Windows, the packaged recovery smoke executable also launches the real app
from PowerShell under ConPTY, for both PowerShell 7 and Windows PowerShell 5.1.
It exercises dirty-buffer cancel/skip, shell commands and pipelines, a workspace
path with spaces and Unicode, return to the same edited buffer, saving, resizing,
the menu shell entry, nonzero shell return, and normal application exit. Native
storage tests inject failures before/after replacement, during backup publication,
during partial replacement restoration, rollback and cleanup, and retain a
substituted writer's displaced bytes. CI uploads console transcripts as native
evidence even when a test fails.

After those pass, check the physical interactive app with scratch copies: type/save/
retrieve, repeat save or Save As, cancel overwrite, switch buffers, restart and
recover edits, function keys and modifiers, mouse, resize, and shell return.
Check native documents in the original DOS reference environment separately.
The wider reference-harness failures recorded in the infrastructure recovery
report are not closed by this native build work.

## Rebuild packages

Use a clean production tree:

```sh
python3 scripts/build-prerelease.py --output bin/prerelease \
  --target windows/amd64 --target windows/arm64 \
  --target darwin/amd64 --target darwin/arm64
```

Each package contains `candidate.json`, source/target and compiled-input hashes,
and `SHA256SUMS.json`. Product builds explicitly exclude the `wordling_qa` seam.
Output directories must be new so earlier candidates are not overwritten.

The platform primitives follow the native API contracts:
[Windows handle-relative creation](https://learn.microsoft.com/windows/win32/api/winternl/nf-winternl-ntcreatefile),
[Windows replacement and partial errors](https://learn.microsoft.com/windows/win32/api/winbase/nf-winbase-replacefilew),
[PowerShell startup options](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_pwsh),
[Windows pseudoconsole sessions](https://learn.microsoft.com/windows/console/creating-a-pseudoconsole-session),
[Windows rename flags](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/4217551b-d2c0-42cb-9dc1-69a716cf6d0c),
and the platform-specific calls in the pinned `golang.org/x/sys` source.
