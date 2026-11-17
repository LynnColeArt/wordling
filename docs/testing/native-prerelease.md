# Native Windows and macOS prerelease builds

The native build path is available for Windows and macOS on amd64 and arm64.
These are engineering test builds. Full WordPerfect parity and production
acceptance remain open.

The `Native prerelease` workflow builds normal executables with the pinned Go
toolchain, records compiled inputs, packages fixture-free smoke executables,
then runs the packages on Windows and macOS runners. Its artifact is named
`wordling-native-prerelease`. Building on Linux avoids the historical research
archive's case-sensitive path collisions in Windows source checkouts.

## Windows / PowerShell

Extract the ZIP matching the machine's architecture, then open PowerShell in
the extracted directory:

```powershell
.\storage-smoke.exe -test.run '^TestNativePlatform' -test.v
.\recovery-smoke.exe -test.run '^TestNative' -test.v
New-Item -ItemType Directory -Force .\scratch
.\wordling.exe -root (Resolve-Path .\scratch).Path -control-keys
```

Windows currently supports opening native documents and saving to **new
filenames**. Saving over an existing document returns an explicit refusal before
changing the document, backup, or staging files. Use another filename to retain
the edited copy. The inherited two-name atomic replacement/rollback protocol
has no implemented Windows equivalent; it is not simulated with a sequence of
ordinary renames.

Recovery uses native exclusive byte-range locks held beside session directories,
so startup publication and cleanup can rename directories while retaining lock
ownership. Candidate and recovery file
contents are flushed, but directory-entry durability across power loss is
unqualified. Windows builds advertise these limitations at startup and in the
package README. They are not a production overwrite/recovery acceptance claim.

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
backup/replacement support or explicit refusal, DOS listing, recovery locking,
recovery snapshot restoration, and repeated settings updates. They need no
private DOS installation or source-tree fixtures.

After those pass, check the interactive app with scratch copies: type/save/
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
[Windows rename flags](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/4217551b-d2c0-42cb-9dc1-69a716cf6d0c),
and the platform-specific calls in the pinned `golang.org/x/sys` source.
