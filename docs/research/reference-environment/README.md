# Executable WordPerfect reference environment

Established 2026-10-29 within M1. This is an **original-application oracle**;
Wordling has no implemented editor or differential conformance results yet.

## Confirmed identity

The original application displays **WP 5.1 03/09/92** in Help.
[Capture](release-identification.png) and [text capture](release-identification.txt).

- `WP.EXE`: 228352 bytes; SHA-256
  `0734d0734c78c113ddaf40293c2c21b02e2cacc063bca5aa3d02f696de0bdc6a`.
- `WP.FIL`: 617745 bytes; SHA-256
  `298c3d6a6acda762f3252bb5b0851aa9abd3b6c4f3d50881b7cde9d861f8d53a`.
- [All 158 installed-file fingerprints](installed-files.json).
- [Media provenance and image hashes](media-manifest.json).
- [Hardware, OS, firmware and master-image profile](environment.json).
- [Printer, language and setup resources](resource-profile.json).

The media came from the public [Internet Archive six-disk item](https://archive.org/details/word-perfect-5.1-for-dos-5.1-1992-03-3.5-720-kb-english).
Its ZIP SHA-1 matches the item's upstream metadata. SHA-256 is pinned by the
provisioner. Executing Help confirms the build beyond catalogue descriptions or
DOS file timestamps. Proprietary executables, disk images, dictionaries and
graphics resources stay in ignored `research/cache/reference/`, not in git.

## Precisely what this profile represents

QEMU 8.2.2, machine `pc-i440fx-8.2`, single-thread TCG, 486 CPU, 16 MiB RAM,
standard VGA, no NIC, no serial/parallel device, no shared host directory.
Only explicit raw disk files are attached. RTC starts at 1992-03-09 12:00:00
and advances with the VM. Captures pause the guest while recording raster and
80x25 VGA text/attribute memory, then resume it.

The boot disk derives from the official FreeDOS 1.4 Floppy Edition, using kernel
2043 and FreeCOM 0.86. The minimal boot configuration sets FILES=40, BUFFERS=20
and the shell/path; no XMS/EMS manager, network stack or custom keyboard is loaded.
FreeDOS is not historical MS-DOS. OS-sensitive results need corroboration on a
historical DOS profile before broader claims.

**The printer disk is dated 1992-07-17**, despite the application/program disk
being 1992-03-09. The selected `Standard Printer` resource comes from that later
disk. It supports basic 10-cpi text and no graphics. This is an explicitly pinned
mixed-date resource profile, not an untouched March shipping set and not a
graphics/font/pagination acceptance baseline. Learning and other bundled files
are installed, but installing them does not mean their behavior was tested.

The optional original license-number display field was left blank. No serial
number, executable patch or license-check workaround was introduced.

## Observations so far

| Case | Bounded original-app observation |
| --- | --- |
| CMD51-001 | Alt+= shows/hides the menu bar; visible cursor position retained. |
| CMD51-004 | Help shows the release identity; Space returns without advancing insertion position. |
| CMD51-005 | Repeat Value 5 followed by x inserts five x characters. |
| CMD51-028 | Typing b with Block on seeks b without inserting/replacing the text. |
| CMD51-046 | Typeover and then insertion produce `aXYc`; status switches back. |
| CMD51-048 | Reveal Codes shows `[BOLD]alpha[bold]beta`; toggling retains visible text. |
| CMD51-066 | F10 uses `Document to be saved:` and creates an original native file. |

Each ran from its own fresh copied boot and hard-disk images in
[smoke-02](../reference-runs/2026-10-29-smoke-02/run.json) and
[smoke-03](../reference-runs/2026-10-29-smoke-03/run.json): **14 successful recipe
executions**. Scope is deliberately `original-reference-only`; these checks do
not exhaust every branch or invariant in the larger catalogue scenarios.

Eight more recipes cover code-boundary deletion, overwrite refusal, original
macro recording/playback/repetition, and a native two-record merge. Each passes
in [extended-03](../reference-runs/2026-10-29-extended-03/run.json) and
[extended-04](../reference-runs/2026-10-29-extended-04/run.json), adding **16 recipe
executions**. See [fixtures, exact checks and limits](extended-probes.md).
The 13 native outputs from each extended run are compared
[byte for byte](extended-output-comparison.json).
All published extended recipes exit WP normally before QEMU is stopped.

Eleven additional recipes cover blocked half-pair deletion, block/character
Undelete, macro branching/jumps, failed-search defaults and handlers, missing
nested-macro errors, default/PAGE OFF merge pagination, and IF BLANK/ELSE.
[Advanced recipes and findings](advanced-probes.md) link two fresh-copy runs and
all 27 repeated native output pairs. All Wordling implementation states remain
unchanged.
Native inspections validate hard-page counts outside formatter structures and
record the original document's must-be-formatted prefix flag separately from
preserved text/code bytes.

Eight further recipes cover three-level history and eviction, child-local and
propagated macro errors, positive/negative FOR steps, zero-entry and terminating
WHILE loops, and PAGE ON resumption. [History/loop evidence](history-loops-probes.md)
records both fresh-copy repetitions, 22 native output pairs and exact body/text
audits. PAGE ON in Carol's record restores the next automatic separator before
Dave. Full scenario and Wordling differential acceptance remain open.

Eight iteration/nesting recipes add FOR EACH order/duplicates, NEXT, BREAK from
IF and inner loops, mixed FOR/WHILE nesting, and global PAGE OFF/PAGE ON effects
across parent/child primaries. [Iteration/nested-primary evidence](iteration-nesting-probes.md)
records two complete repetitions and 22 native output pairs. A child's page
setting remains active after return until explicitly changed by the parent.
All Wordling implementation states remain not implemented.

Eleven value/secondary recipes add raw/quoted FOR EACH strings and expressions,
nested NEXT, file-level BREAK in macro and merge contexts, and page controls
across nested secondary streams. [Values/secondary evidence](values-secondary-probes.md)
records literal quote retention, a nested macro BREAK that continues its child,
a partial copy retained after secondary BREAK, and exact cross-file page
boundaries. The catalogue now has **236 scenarios, 53 partially observed**.
These remain original-app observations, not Wordling implementation evidence.

The two earlier saved scratch documents are byte-identical, 337 bytes, with native
signature `FF 57 50 43`, product 1, document type 0A, stored version 00/01 and
document offset 324. [Independent inspection](native-save-inspection.json).
This is newly created original-app output, not evidence for Wordling no-edit
preservation or arbitrary document round-trips.

## Rebuild and run

Tested host package versions:

```text
qemu-system-x86 1:8.2.2+ds-0ubuntu1.18
seabios         1.16.3-2
mtools          4.0.43-1build1
dosfstools      4.2-1.1build1
python3-pil     10.2.0-1ubuntu1.3
```

Python 3.11+ is required for the research tools. Exact host binary and firmware
hashes are recorded; this first provisioner uses the Debian/Ubuntu SeaBIOS paths.

From the repository root:

```sh
# Downloads checksum-pinned sources only when absent. Does not publish them.
# Creates a new private installation; existing build directories are refused.
python3 scripts/reference/prepare.py local-01

# Verify all non-personal-setup installed files and fingerprint a fresh profile.
python3 scripts/reference/fingerprint.py \
  research/cache/reference/build/local-01 \
  research/cache/reference/build/local-01-profile

# Every recipe starts another copy of that master, rather than editing it.
WORDLING_REFERENCE_MASTER="$PWD/research/cache/reference/build/local-01" \
WORDLING_REFERENCE_PROFILE="$PWD/research/cache/reference/build/local-01-profile/environment.json" \
  python3 scripts/reference/smoke.py local-smoke-01 \
    CMD51-001 CMD51-004 CMD51-005 CMD51-028 CMD51-046 CMD51-048 CMD51-066
```

The provisioner replays original Basic installation, accepts the listed bundled
components, declines C: boot-file changes because A: has our explicit config,
selects Standard Printer, leaves the optional number blank, captures Help and
exits cleanly. Unknown screens time out rather than receiving arbitrary answers.

An independent automated installation completed successfully. **157 of 158 file
contents match** the first installation, including executable, overlay, printer,
language and graphics resources. The personal `WP{WP}.SET` differs at byte offset
1366 (`0x556`): 8A versus 09. It is the low byte of the cached printer
modification-time word. The decoded times match the two printer FAT timestamps;
a controlled timestamp-only experiment
confirms that explicit printer selection refreshes it. No normalization was
applied. [Investigation and control](setup-timestamp.md);
[comparison](rebuild-comparison.json). The independently fingerprinted
rebuilt profile passed [its menu probe](../reference-runs/2026-10-29-rebuilt-profile-01/run.json).
Raw disk hashes can differ across installation replay; we claim reproducible
software/configuration procedures, not bit-identical installer or RTC timing.

For this machine, the pinned first master is already available:

```sh
python3 scripts/reference/smoke.py another-unique-run CMD51-046
```

Use unique run IDs. Outputs are immutable directories; existing run directories
are refused. On a failure the tool captures the guest screen, retains the disk,
records the error, and exits nonzero. Master disk/boot, emulator and firmware
hashes must match the selected profile before a guest is started.

## Evidence and further work

Run manifests record input traces, checks, evidence sizes/hashes, QEMU arguments,
and original-only scope. `smoke-03` also pins runner-source hashes and archives
the exact scripts for audit. PNG and PPM captures are lossless; `vram.bin` contains
only 4000 VGA text/attribute bytes, not an executable or full guest-memory dump.
`NEWTEST.WP5` is the original app's output from our own `WORDLING TEST` input.
Original UI text in reference captures is not relicensed as project-authored prose.

Initial harness calibration had an incorrect save-prompt wait and one invalid
case association, plus one transient boot timeout. Those diagnostic attempts
are retained privately and do not count as successful observations. Two clean
seven-recipe runs, six clean eight-recipe runs, four clean eleven-recipe runs and
the independent rebuilt-profile probe are published. Extended calibration also corrected a code
label, premature cursor screenshots and a save-completion race; those diagnostic
runs stay private and do not count as passing evidence. Advanced calibration
also corrected the Macro Editor command-insert prompt and removed an unfounded
requirement for a persistent failed-search error message.

Remaining priorities: corroborate OS-sensitive behavior; acquire a period-matched
graphics-capable printer/font profile; extend other code pairs, history grouping
and low-memory behavior, deeper handler chains and ON NOT FOUND scope, empty/
escaped values and evaluation timing, NEXT in other loop types, IF-only BREAK,
loop errors, deeper/mixed merge nesting and page control, End C/A,
unsorted lists and printer-byte capture. No full scenario or Wordling parity
status is advanced by this reference set.
