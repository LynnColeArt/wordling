# WP83 — original search across text and native codes (evidence report)

Status: implemented on lane-g, actor kat; review-cycle-1 remediation path 1.

## Review-cycle-1 findings resolution index

- W83-1 (Find ignores `from`): resolved — Find honors the byte-offset
  anchor; nil/empty anchor means document start (forward) / end
  (backward); out-of-range anchors refuse rather than wrap.
- W83-2 (single match / dead Result): resolved — repetition is anchored
  re-issue (the caller advances the anchor past the previous match; the
  session keeps `lastSearchEnd` so repeated F2 with an untouched prefill
  advances); `FindResult` is the typed result (parent `Result` is the
  session IO receipt).
- W83-3 (subpackage vs planned paths): resolved — delivered at
  `internal/editor/search{,_test}.go` in the parent `internal/editor`
  package per create_intent; the narrow subpackage
  `internal/editor/search/` is retired on the planning branch
  (3b169e13 pattern, same as W82-2).
- W83-4 (evidence): this report; the subtask ledger follows.

## Subtask ledger

- T259 done (b4f127c2): direction-bound prompt state (`SearchForwardMode`
  / `SearchBackwardMode`), F2/Shift+F2 routing in Editing, `SearchF2`
  executes in the prompt's direction, `SearchBackF2` executes backward;
  Enter is unobserved in the original trace and is refused, not aliased.
- T260 done: results and repetition — forward/backward anchored Find over
  the concatenated native token stream; repetition advances across the
  three "alpha" occurrences (frames 19/21/23 reconciliation: Pos 2.4" →
  Pos 3" forward; backward returns to the prior occurrence).
- T261 done: cancellation and failure — F1 cancel and NOT FOUND leave the
  cursor exactly at the pre-search gap (frames 24/25/26) and the body
  unchanged; search is a pure function over the immutable document
  (byte-equality asserted).
- T262 done: semantic/native conservation — search never mutates native
  bytes (TestSearchIsPure); the walk uses `Token(i)` reads only; the SRt
  transparency (soft return matches a query space) is a read-side
  matching rule, no serialization.
- T263 done: full go build/vet/test green; journey tests over FLOW.WP
  (the original's own journey document): TestSearchFindHonorsFromAndRepeats,
  TestSearchEmptyAnchorStartsAtDocumentStart, TestSearchIsPure,
  TestEverydayJourneySearchForwardRepeats,
  TestEverydayJourneySearchBackward.

## Frame reconciliation (EE-A09)

| frame | original | WP83 | match |
| --- | --- | --- | --- |
| 18 forward-prompt | `→ Srch:` | prompt exactly | exact |
| 19 first-result | Ln 1.67" Pos 2.4" (cursor moves to match) | cursor at alpha#1 token | exact |
| 20 repeat-prompt | `→ Srch: alpha` (prefilled) | remembered prefill | exact |
| 21 second-result | Pos 3" (advance one cell) | cursor at alpha#2 | exact |
| 22 backward-prompt | `← Srch:` prefilled | remembered prefill | exact |
| 23 backward-result | returns to the prior occurrence | cursor at prior match | exact |
| 24/25 not-found | settles at same position | gap unchanged, "NOT FOUND" notice | exact |
| 26 cancel (F1) | body and cursor unchanged | gap unchanged, mode Editing | exact |
| 27 across-wrap | cross-SRt query matches | SRt matches a query space | exact |

## Search is text + native codes

The match space is the concatenated raw token stream (attribute owners
carry their raw bytes; a query over code bytes matches them — the F8/Reveal
code entry of frames 29/30 reads codes the same way). Rendered ANSI strings
are never searched (no projection involved).

## Downstream consumers

TUI routing of F2/Shift+F2 and prompt rendering is WP84's surface; the
session contract is: `Snapshot().Prompt` carries "→ Srch: <draft>" /
"← Srch: <draft>", `SearchF2`/`SearchBackF2` are the enum identities,
and `SearchForwardMode`/`SearchBackwardMode` are the prompt modes. The
TUI must not synthesize search results; it prints the snapshot prompt.
