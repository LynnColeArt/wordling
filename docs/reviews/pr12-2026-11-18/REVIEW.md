# Independent review: Wordling PR #12

Reviewer: Reviewer Renata (resolved through `spec-kitty agent profile show reviewer-renata --json`).
Date: November 18, 2026 (America/Chicago).
Governance Op: `01M7Q23CBJQYK4DVWTKVPS2871` (owned by root orchestrator).
Base: `54afa6c889d610608206eafa6eecabbb827eedb5`.
Reviewed head: `4ef80ea456d7605b83b32ca34af7de198ac608b4`.

**Verdict: APPROVE for its stated engineering-prerelease scope. No blocking correctness findings.** This review does not accept Mission 1 or imply qualification of every Windows volume, physical terminal, or power-loss case. Merge this reviewed delta into its declared base branch; the recovery/native parent PRs are separate changes.

## Intent and scope

The change makes actual interactive PowerShell the default Windows shell, enables existing-file save replacement and original backups through the native Windows filesystem API, corrects erroneous NUL input synthesized from characterless Windows modifier records, and adds native executable/console qualification. The large diff is mostly a local copy of the already-pinned terminal dependency. I compared every copied upstream file with the exact pinned module cache: only `terminal_reader_windows.go` differs among existing upstream files, by the documented modifier-record guard. License and upstream `go.mod` match exactly.

## Correctness assessment

- The Windows replacement step releases the candidate's read pin before exclusive `ReplaceFileW` access. A fresh random private name receives the actual displaced file; success is followed by destination and escrow identity/content verification. Rollback uses another replacement, and its ownership checks refuse interference.
- Error classification accounts for operations that completed despite an error, unchanged namespaces, and the documented partially moved state. Partial restoration uses no-replace rename; ambiguous states retain evidence and report `PublicationUncertain`, rather than returning a successful receipt or deleting unknown data. The failure tests cover before/after replacement, backup failure, partial restoration, failed rollback, cleanup failure and an externally modified displaced file.
- Native replacement operates through normalized volume-GUID paths while every plain ancestor is opened with directory read access and without delete sharing. The final leased directory's volume/file identity must match the acquired handle. Unsupported paths fail before replacement. No stronger hostile-directory compare-and-swap guarantee is claimed.
- Linux/macOS continue through the pre-existing atomic exchange primitive. Prepared-request consumption, explicit overwrite consent, source/destination validation, byte preservation and original-backup policy remain in the common implementation.
- PowerShell launch uses an actual executable and inherited terminal/environment, loads normal profiles, prefers version 7 and retains the built-in fallback and explicit absolute shell overrides. Native ConPTY tests exercise both PowerShell 7 and Windows PowerShell 5, shell return, editor text/caret preservation, save and overwrite decisions, resize, menu entry, nonzero exit, and normal terminal-restored shutdown.
- The input correction is applied while virtual-key metadata is still available; it skips only zero-character modifier/lock records. Tests separately preserve genuine Ctrl+Space/Ctrl+@ NUL input, key releases, ordinary shifted text, Alt plus VT input and UTF-16 surrogate pairs. It does not globally discard NUL bytes or alter editor commands.
- Candidate provenance now includes local dependency source files and the tracked `third_party` production tree. ZIP checksums cover packaged executables and the retained MIT license. Normal builds exclude the fault-injection seam.

I checked native semantics against Microsoft's primary API documentation: [ReplaceFileW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew) documents exclusive replacement access, partial failures and unsupported write-through; [GetFinalPathNameByHandleW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfinalpathnamebyhandlew) documents normalized volume-GUID paths and network-volume limitations. The implementation and declared limitations are consistent with those contracts.

## Validation evidence

Fresh independent checks at the reviewed head:

- `go test -count=1 ./...`: passed (23 packages with test results). Full output: `/tmp/wordling-mission1-closeout-20261118/pr12-review-go-tests.log`.
- `go build ./...`: passed.
- `go vet ./...`: passed.
- `GOOS=windows GOARCH=amd64 go vet ./internal/storage ./internal/tui github.com/charmbracelet/ultraviolet`: passed.
- `go mod verify`: all modules verified.
- `git diff --check BASE HEAD`: passed.
- GitHub run [44253191919](https://github.com/LynnColeArt/wordling/actions/runs/44253191919) is completed successfully at the exact reviewed head: Linux build/regression, Windows native and macOS native jobs all pass. Native Windows execution is supplied by that runner; I did not relabel Linux cross-compilation as native testing.

## Supply-chain disposition

- Registry/authenticity: the official Go proxy returned the exact required upstream version at `https://proxy.golang.org/github.com/charmbracelet/ultraviolet/@v/v0.0.0-20261008173134-6b8d4baf91b4.info`, pointing to `https://github.com/charmbracelet/ultraviolet`, full source commit `6b8d4baf91b4c933e6613b0eefc8f180f6eda002`. Exact-file comparison and `go mod verify` passed.
- Freshness: upstream source version timestamp is October 8, 2026 at 17:31:34 UTC (about six weeks before this review), already pinned by Bubble Tea; this is a local correction, not adoption of a freshly published replacement package. No transitive version changes were introduced.
- Lifecycle scripts: Go source build; no added npm lifecycle scripts or automatic script approvals. The copied package is Go source/module metadata plus its original license/README and the documented patch/test.
- Node LTS: not applicable to this Go dependency/runtime change. No Node runtime or package-manager configuration is added or changed.
- Incident/IoC posture: queried the current OSV API for the exact Go module/version, `https://api.osv.dev/v1/query`; response `{}` (no matching reported vulnerability). The response and registry query are retained in `/tmp/wordling-mission1-closeout-20261118/pr12-supply-chain.json`. The source comparison found no unexplained changes, install-time network code or persistence additions. This is a bounded current-source/feed check, not a guarantee against undisclosed incidents.

## Scope limits retained

Windows directory-entry durability across sudden power loss remains unqualified; document and backup publication are separate steps. Windows ARM64 and macOS Intel are cross-built, with native hardware qualification still open. Full WordPerfect behavior and original-reference acceptance remain Mission 1 obligations. These limits are stated in the readiness report and package guidance, so they are not new blockers to the requested engineering prerelease merge.

Tooling note: the project-local `WL-*` directive selector returns a lookup error through `charter context`; I read their actual structured definitions in `.kittify/charter/charter.yaml` and their required compatibility/roadmap/charter documents instead. No governance, WP state or source file was changed during this review.
