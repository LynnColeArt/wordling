# Compose pair matrix, WordPerfect 5.1 DOS 03/09/92

Six independent guest runs (`compose-final-0` through `compose-final-5`)
cover 825 input pairs. Each folder records its input order and DOS native save.
The body contains each result followed by three literal vertical bars. A pair
can yield a four-byte C0 owner or nothing. Parse the framing before splitting on
the separator; number or set bytes can have the same value as a separator.
Ignore formatter-only deleted soft returns outside owners. The resulting
fixture is `internal/tui/testdata/compose-dos-pairs.json`.

The stock installation produced 219 owners in this matrix. The separate
`compose-uppercase-o` run additionally establishes uppercase `*O` as set 4,
number 1. In this profile `--` produces set 4, number 34, and `**` produces
set 4, number 0; those differ from some printed examples. `Pl` produced
no owner. Numeric entry can still reach the corresponding identities.

The separate `compose-reveal-caret` run establishes that the selected owner
expands to `[glyph:set,number]` in the lower pane; all other extended owners
keep their single display cell. `compose-wrap-dos` establishes a one-column
owner at the right margin and preserves the native wrapping marker.
