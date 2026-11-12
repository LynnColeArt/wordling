# WP27 review feedback — cycle 1

## I1 [P2] Route the original blocked-selection Backspace command

**Source:** `internal/editor/session.go:410` and `internal/editor/editing.go:214`.
**Contract:** `contracts/editing.md:108,110,165` (EC202/203/204), approved23
`run_blocks`, and approved40 closing-block handoff/actual AltF4/Right/Backspace
trace. This is the researched supported block context, not an unobserved history
or cancellation variant.

Given the actual approved ORIGIN document with fresh qualified history, send
Reveal, Right, Block, Right. The public snapshot is Editing/gap2/Selection=true,
representing only Bold On selected. When the next public event is Backspace,
Session.Reduce refuses with `only forward block movement/Delete and qualified F1
cleanup`; mode remains Editing and no Delete Block question appears. The same
state accepts Delete and produces `Delete Block? No (Yes)`. Native bytes remain
intact on refusal; this is a required command-routing failure, not data corruption.
The independent external-API overlay reproducer fails on8b0a8ed. Existing
original_history_test.go maps the original block Backspace to Delete, so its two
closing original replays and the other block tests do not exercise the required
public Backspace route despite matching resulting native data.

**Required remediation:** enable the original Backspace event through the active
selection guard and actual document.DeleteBlock composition for researched ranges.
Do not require a future UI/transport adapter to silently alias Backspace to Delete.
Keep any unobserved selected-block forward Delete behavior explicitly refused
unless separately supported by approved original evidence. Update original-derived
replays and block Yes/No/F1/Escape/full-span Restore tests to send the actual
Backspace event, with exact question, selection, native/cursor/dirty/history and
refusal assertions. Preserve ordinary directional Backspace behavior, source/
revision ownership, existing unqualified history refusals and safe publication
paths. Rebind final-source checks/seals and scoped event-fuzz evidence as needed;
no VM/new original probe is required for this already approved command.

**Dependency impact:** WP28/WP36 must consume the corrected reducer command;
keep their dependent routing gated/rebase onto the corrected WP27. No source fix,
downstream edit, original probe or other-WP lifecycle change was made in review.
