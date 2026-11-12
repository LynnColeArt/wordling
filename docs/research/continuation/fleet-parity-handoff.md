# Wordling assignments for agent-fleet

Start from `feat/wp51-parity` at `febed7bd` or a later reviewed integration point. Use a separate branch for each assignment. The reference is WordPerfect 5.1 US DOS dated March 9, 1992. Keep native files in the original format and use stopped guest exports for byte comparisons. Submit each change for independent review with exact reproduction steps and results.

1. **Merge records that span pages.** Author a secondary record that crosses the first automatic page boundary in DOS. Capture its native page owners, record count and output when Ctrl+F9 substitutes fields on both sides of the break. Add the verified form to the parser and editor. Preserve the existing 53-field single-page fixtures and reject unfamiliar layouts before mutation. See [the current merge replays](../everyday-contract-2026-11-05/native-merge/wide/README.md).
2. **Printing and document preview.** Establish a DOS Print to Disk fixture using the pinned Standard Printer profile. Record the exact command sequence, output bytes and printer resources, then trace the smallest equivalent Wordling path. Keep the printer profile fixed for the first comparison. See the [mission requirements](../../../kitty-specs/wp51-parity-01M64CVY/spec.md).
3. **Structured document intake.** Start with a small table authored in DOS. Map the bytes that delimit the table, rows and cells. Demonstrate lossless open and save and one bounded cell edit that the original can reopen. Include an unsupported table case that preserves the source.

The assignments are ready for dispatch when the Go fleet can start workers. Wordling's ordinary Undelete work is being handled separately.
