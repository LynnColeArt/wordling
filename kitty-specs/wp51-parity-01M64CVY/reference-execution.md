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
one unexplained byte difference; its independently fingerprinted profile passed
the menu probe. Do not silently normalize that byte or claim identical raw disks.

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
execution work should cover deletion/code boundaries, overwrite rejection,
macros/merges, End C/A and unsorted lists, then a declared printer-byte profile.
