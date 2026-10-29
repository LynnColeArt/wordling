# Extended original-application probes — 2026-10-29

These are bounded observations of the fingerprinted WP 5.1 03/09/92 executable,
not tests of Wordling. The same FreeDOS/text-only printer caveats apply as in
[the environment record](README.md). Each recipe starts from its own fresh disk
copy. The exact runner sources, keystroke traces, screen/VRAM captures, checks
and authored native outputs are retained with each run.

## Recipes

| Case | Fixture and checked outcome |
| --- | --- |
| CMD51-050 | Center `ABC`, expose codes, move before Center, Delete. Center disappears and `ABC` survives. |
| CMD51-051 | Same fixture, move immediately after Center, Backspace. Center disappears and `ABC` survives. |
| CMD51-200 | `A[BOLD]B[bold]C`, Delete at opening bold code. Both bold codes disappear; all three characters survive. |
| CMD51-201 | Same fixture, Backspace immediately after closing bold code. Both bold codes disappear; all three characters survive. |
| CMD51-067 | Save `ORIGINAL` as SAME; guest DOS COPY creates BEFORE; append `MODIFIED`; F10, Enter, decline Replace. WP requests another filename; F1 returns to the changed buffer. SAME and BEFORE are byte-identical after shutdown. |
| CMD51-131 | Record ABC using Ctrl+F10, stop, execute with Alt+F10. Buffer becomes `ABCABC`; retain original TESTMAC.WPM and native output. |
| CMD51-132 | Record the same macro, switch to blank Doc 2; Esc, 3, Alt+F10 executes it three times, producing `ABCABCABC`. |
| CMD51-134 | Create native secondary records Alice/Bob using F9 End Field and Shift+F9 End Record. Create primary `Hello {FIELD}1` and a hard page. Ctrl+F9 Merge produces `Hello Alice` and `Hello Bob` in order; both strings occur in the saved native result. |

The paired-bold cases are explicitly **oracle investigations**. They extend the
manual's Delete Codes discussion (REF51 pp. 112–113, PDF 129–130) without assuming
that all paired codes, deletion commands or Undelete behave identically.

The save case follows REF51 p. 566 (PDF 583); macro cases follow pp. 373–379
(PDF 390–396); merge follows pp. 420–433 (PDF 437–450). Sources are checksum-pinned
in [the source register](../sources.json). Guest DOS COPY is fixture preparation,
not a claim that the entire Shell feature has passed acceptance. No host reads
or changes a mounted live disk.

## Repetition and provenance

Published runs: [extended-03](../reference-runs/2026-10-29-extended-03/run.json)
and [extended-04](../reference-runs/2026-10-29-extended-04/run.json).
[Output comparison](extended-output-comparison.json) checks every exported native
file across these runs, including both WPM macros and the primary, secondary and
merged files. The `.WP5` host suffix labels byte-for-byte extracted native files; the guest
saves those document names without an extension. These are project-authored scratch contents written by the original
application; no bundled macro, executable, dictionary or printer resource is
redistributed. The primary deliberately ends with an explicit hard page; the
merged fixture ends on page 4, including blank pages. This records the actual
result of that input, not a claim of a two-page letter or pagination acceptance.

Calibration runs stay private. One corrected the guessed code label `[Cntr]` to
the observed `[Center]`. Another exposed screenshots taken before cursor movement
finished; the final deletion recipes wait for the expected insertion position
and allow the final code-boundary movement to redraw before capturing. Runs use
host-timed input, not instruction-level deterministic replay. A repeated run also
showed that disappearance of the save prompt can precede file-write completion.
Every published extended recipe now exits through WP to the DOS prompt before
QEMU stops and offline extraction begins.

To rerun against the pinned local master, use new run IDs:

```sh
python3 scripts/reference/smoke.py your-unique-run \
  CMD51-050 CMD51-051 CMD51-067 CMD51-131 CMD51-132 CMD51-134 CMD51-200 CMD51-201
```

These eight recipes supplement the seven earlier smoke recipes. Full scenario
branches, all other attribute pairs, blocked code-pair deletion, Undelete,
overwrite approval and save failures, macro editing/control flow/error behavior,
conditional and nested merges, and every Wordling comparison remain unverified.
