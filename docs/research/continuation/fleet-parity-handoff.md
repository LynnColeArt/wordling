# Wordling assignments for agent-fleet

Start from `feat/wp51-parity` at `febed7bd` or a later reviewed integration point. Use a separate branch for each assignment. The reference is WordPerfect 5.1 US DOS dated March 9, 1992. Keep native files in the original format and use stopped guest exports for byte comparisons. Submit each change for independent review with exact reproduction steps and results.

1. **Author and edit merge records that span pages.** Wordling can execute the first verified two-page form. Extend its editor so F9 writes the correct field and page owners at the boundary, edits retain or update those owners, and F10 produces files the original can reopen and merge. Preserve the 53-field single-page fixtures and use the 54- and 60-field originals as controls. See [the current merge replays](../everyday-contract-2026-11-05/native-merge/wide/README.md).
2. **Printing and document preview.** Establish a DOS Print to Disk fixture using the pinned Standard Printer profile. Record the exact command sequence, output bytes and printer resources, then trace the smallest equivalent Wordling path. Keep the printer profile fixed for the first comparison. See the [mission requirements](../../../kitty-specs/wp51-parity-01M64CVY/spec.md).
3. **Structured document intake.** Start with a small table authored in DOS. Map the bytes that delimit the table, rows and cells. Demonstrate lossless open and save and one bounded cell edit that the original can reopen. Include an unsupported table case that preserves the source.

The assignments are ready for dispatch when the Go fleet can start workers. Wordling's ordinary Undelete work is being handled separately.
