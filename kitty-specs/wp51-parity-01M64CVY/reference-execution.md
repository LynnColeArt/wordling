# Original-reference execution pass — 2026-10-29

User request: acquire the selected March 9, 1992 release, establish a reproducible
DOS reference environment and begin executing acceptance scenarios.

## Outcome

The original Help screen displays WP 5.1 03/09/92. WP.EXE, WP.FIL and 158 installed
files are fingerprinted. Pinned media/provisioning and offline QEMU/FreeDOS
profiles are in [the environment record](../../docs/research/reference-environment/README.md).
Original media and resources remain private in the ignored research cache.

The seven recipes CMD51-001, 004, 005, 028, 046, 048 and 066 matched their bounded
smoke expectations in two fresh-copy runs. A new original document from both
runs is identical (337 bytes, original 5.1 header). No Wordling implementation or
differential conformance was exercised. Scenario state advances only to
`partially-observed`, with scope and checksum-validated evidence links.

Automated reinstallation from pinned sources succeeded. All 157 non-personal-
setup file contents match the first installation. The personal setup file has
one byte difference at offset 1366: the cached Standard Printer modification-time
word. SDK51 Appendix A p. 8 (PDF 507), independent FAT16 inspection and a
three-trial timestamp-only experiment establish its meaning. Idle launch/exit
retains a stale cache; explicit printer selection refreshes it, changing only
that byte. The master and printer content remain unchanged.
[Investigation](../../docs/research/reference-environment/setup-timestamp.md).
Its independently fingerprinted rebuilt profile also passed the menu probe.
Do not normalize the field or claim identical raw installation disks.

## Expanded probes

Eight more recipes (CMD51-050, 051, 067, 131, 132, 134, 200 and 201) pass twice
from fresh copies: unpaired Center deletion from both sides; paired Bold deletion
from both boundaries; refusal to overwrite; macro recording/execution/repetition;
and a two-record native merge. The overwrite target is byte-identical to its
pre-edit guest copy. All 13 authored native outputs in each run are compared
across repetitions, including original WPM, primary, secondary and merged files.
[Recipes and evidence](../../docs/research/reference-environment/extended-probes.md).

The catalogue now contains 201 representative drafts, 15 partially observed and
186 not run. All Wordling implementation statuses remain not implemented. The
paired-bold additions are bounded oracle investigations, not a completed model
for all paired codes. The merge fixture includes an explicit primary hard page
and ends on page 4; no general pagination conformance is claimed.

Extended calibration found premature cursor captures and a save-prompt/file-write
race. The published deletion captures wait for cursor position, and every extended
recipe exits WP normally before QEMU stops and offline extraction begins. Diagnostic
attempts remain private; source snapshots and evidence hashes identify final runs.

## Material limits

- The media combines March program files with a July 17, 1992 printer disk.
  This is explicitly recorded, not treated as an untouched March shipping set.
- Standard Printer supports 10-cpi text only. Graphics/font/pagination and printer-
  byte conformance are still pending a suitable resource profile.
- FreeDOS 1.4 is the boot environment, not historical MS-DOS. OS-sensitive
  behavior requires another corroborating profile.
- Input traces are host-timed. We have a repeatable configuration and copied
  starting state, not instruction-level deterministic replay.
- Early harness calibration failures were excluded. No failure was converted into
  a passing original-app assertion.

The full command catalogue, detailed plan and work packages remain open. Next
execution work should cover blocked code-pair deletion and Undelete, macro
control flow/errors, merge pagination and conditional behavior, End C/A and
unsorted lists, then a declared printer-byte profile.
