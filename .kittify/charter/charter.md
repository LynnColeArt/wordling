# Wordling 5.2 project charter

Adopted 2026-10-29 from Lynn's confirmed project direction. The structured
`charter.yaml` contains runtime rules; this companion explains their intent.

## Purpose

Reconstruct WordPerfect 5.1 for DOS as a native Linux word processor in Go with
Bubble Tea. Preserve the original application's functionality, interaction model,
and document semantics. A useful partial build is an intermediate milestone,
never a substitute for complete parity.

Primary users are writers and existing WP 5.1 users who want the original tool
and their original documents to work on Linux. The project owner is Lynn Cole
(`lynncoleart`); the public repository is `lynncoleart/wordling`.

## Mission 1: WordPerfect 5.1 parity

Reproduce the original editing environment and commands, Reveal Codes, file
management, formatting, pagination, tables, equations, graphics, spelling and
language functions, styles, references, macros, merges, document utilities,
configuration, preview, and printing. Original supported import/export modes and
companion artifact formats are part of parity, not optional modern additions.

Linux requires explicit adaptations for paths, terminal capabilities, process
launching, and printer delivery. Record these adaptations and test their effects;
do not silently remove DOS-era features or redefine editing behavior. Hardware
emulation and executing original DOS binaries are not the implementation strategy.
Original bundled utility behavior remains in the inventory even when its Linux
mapping is unresolved. Terminal limits must be surfaced as open design work,
not used to declare graphics or preview out of scope.

The baseline is plain WP 5.1 for DOS. US English is a provisional research
baseline, not a user-approved permanent language restriction. Record the exact
executable release date, language, configuration, printer resources, and hashes
before accepting differential results. Neither WP 5.1+ nor WP for Windows 5.2
defines parity; later documentation must be checked for version applicability.

Milestones and work packages may deliver usable subsets. Mission completion
requires all inventoried obligations to be implemented and verified; any proposed
exclusion or changed baseline requires an explicit owner decision recorded in git.

## Mission 2: Modern conveniences

Begins after Mission 1 is accepted. PDF export is the first confirmed addition.
Clipboard enhancements, improved recovery, and other conveniences are candidates
only; their requirements will be selected when this mission is specified.
Classic workflows remain available, and permanent format rules still apply.
Existing WP backup/recovery behavior belongs to Mission 1; enhanced recovery
belongs to Mission 2.

## Permanent file-format rules

The [compatibility contract](../../../docs/compatibility.md) is binding in both
missions. Original WP 5.1 formats are the durable formats. Wordling's version
number must never be written as a new native file-format version. Native files
need no Wordling sidecar, private extension, or conversion intermediary.

Unchanged valid files must save byte for byte. Edits must preserve unrelated data
and remain usable by the original application. If an edit cannot safely preserve
an unsupported structure, reject that edit or save before touching the original.
Unknown content is not permission to discard it. New text must be representable
by the selected original format; never substitute characters silently.

## Evidence and quality

Use original manuals and the Developer's Toolkit as primary documentary sources.
Track citations by source checksum and both printed and PDF page locations.
Separate table-of-contents discovery, section study, original-app observation,
implementation, and differential verification. No verified status without durable
evidence. Maintain unresolved questions and a complete coverage reconciliation.

For changed Go code: gofmt, build, `go test ./...`, and `go vet ./...` must pass.
Binary parsing requires meaningful malformed-input tests and fuzzing; format
writing requires binary preservation and original-app interoperability checks.
Layout tests declare printer/font resources, page geometry, and tolerances.
Tests must verify behavior and data integrity, not just reproduce implementation.
Latency and scale budgets will be set using measured Linux baselines during
planning; no unmeasured speed or pagination-fidelity claim is permitted.

Keep the document model and layout behavior independent of terminal rendering.
Use original formatting codes as meaningful editing objects so Reveal Codes,
normal editing, and saving cannot develop conflicting document interpretations.
Specific data structures and package boundaries are planning decisions.

## Ownership, licensing, and delivery

Apache-2.0 applies to original project contributions. External reference manuals,
proprietary executables, resources, and dictionaries are not relicensed or bundled.
Record provenance and redistribution permission for committed fixtures.

The initial project foundation lands on `main`. Mission work uses a dedicated
`feat/wp51-parity` branch targeting `main`; reviewable changes should remain small
even though parity is one large mission. Do not start a third product mission
merely to accommodate milestones. Scope changes require a recorded decision.
