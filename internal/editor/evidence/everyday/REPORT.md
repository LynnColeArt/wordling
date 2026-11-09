# WP82 — everyday session evidence report

Status: in_progress (lane-g, actor kat, started 2026-11-09).

Scope: complete everyday session lifecycle, navigation, native reflow
adoption, correction/history, repeated save/backup continuations, save-on-exit,
Doc 2 and New. Requirements EE-004…EE-008, EE-011…EE-013. Owned surface:
`internal/editor/` files per WP82 owned_files.

## Consumer design note (T254 integration seam)

WP82 is the first production consumer of `internal/layout`. The approved
engine (WP81, merged PR #2) is a bounded pure projector; it is NOT a complete
wrap planner. Observed in lane-g against HEAD d23171fe (probe script deleted
after reading; results reproduced in table below):

| input | expected by consumer | observed |
| --- | --- | --- |
| `"HELLO"` ASCII token (5 chars) | width 0.5" at 10 CPI | Width=0.1" per-token flat rate |
| 30-token unbroken 6-char run | wraps at printable width 6.5" | 30 Lines entries, one token each, Left 1.0→3.9 with no wrap and no width limit |
| SoftReturn between words | paragraph coalescing into one physical line | two separate Line entries, both Top=0.1" |
| any token stream | vertical line index / per-line ordinal (Ln) | not exposed; TopInches is a horizontal position, not a line index |
| HardPage | Page increments | works (Page=2 after token) |

Consequences for WP82:

1. `Layout.Lines` cannot supply Pg/Ln/Pos for real documents (the EE-A04/A05
   journeys) until layout plans *physical lines* the way D-EE-06 requires
   (1.17-inch next-line advance, wrap at 6.5", tab-to-relative-stop).
2. Per the cross-WP rule we do not patch `internal/layout` from WP82. This is
   a named gap with an owning WP (WP81 amendment).

## Named gaps (carry forward, file:line at time of finding)

- GAP-1 (layout): projector treats each token width as one CPI cell (0.1")
  regardless of text length; wrap boundary never reached in probe. Owning WP:
  WP81 (layout engine amendment) before EE-A04 printed-geometry journeys can
  pass. WP82 will build the document→projection seam so the amendment lands
  against a real consumer.
- GAP-2 (editor): `internal/editor/everyday.go` is in WP82 create_intent but
  does not exist in lane-g HEAD; T254 creates it. (Expected; not a defect.)
- GAP-3 (tui): `internal/tui/historic.go:370` prints `Pg -- Ln -- Pos --`
  pending "a qualified layout engine"; consumer handoff is WP84's file. WP82
  delivers the qualified geometry surface for WP84 to port; the TUI file
  itself remains WP84-owned.

## Subtask ledger

- T254 done (committed 5640032b): qualified printed-geometry seam.
- T255 done (committed bc60a480): Pg/Ln/Pos walker, frame-reconciled
  (06/07/08 exact; 16 page-exact with honest Ln/Pos unknowns past the Tab),
  composite page break mapped, 65-col fold corroborated.
- T256 done (committed 16fbeb64): ExitSaveQuestion Yes route, fromExit
  landing continue-to-exit (rooted + New-buffer), contextual
  ExitDocQuestion, three pinned refusals re-pinned with trace citations.
  Suite green at commit.
- T257 attempted and REVERTED 11-09 (tree back to 16fbeb64; suite green).
  Findings were real but the change was too broad — see the findings list.

## T257 findings (evidence recorded for the retry)

1. Fresh Doc 2 refuses typing in current code ("command requires a loaded
   document"); the original types "SCREEN TWO" straight into the acquired
   screen (trace: shift-f3, type 'SCREEN TWO', frame corrections/03). The
   fresh side must be a usable New document.
2. Screen acquisition after closing Doc 1 yields "Doc 1" (frame 33):
   next-free-number allocation is correct and witnessed.
3. switchDocument's current guard refuses switching away from ANY New-born
   document; the trace witnesses switching from a typed unpublished Doc 2
   (frames 03→04) and from a continued New Doc 1 (frames 33→34).
4. BUT new_macro_test.go:156 pins "anchored New refuses SwitchDocument" as
   an explicit refusal property (WP75-lineage decision), and four other
   suites failed after the naive guard rewrite. Candidate shape: split the
   guard on source binding (unbound New may switch when nothing is pending;
   anchored contexts keep refusing) rather than on birth. The retry must
   read new_macro_test.go:108-165 and the macro_boundary/save_history/
   original_history failing sites BEFORE editing.
5. Unqualified-clear law stands (new_binding_test): an unqualified clear
   must not mint a New phase. Renewal at exit-time was wrong; renewal at
   screen-acquisition time is the witnessed shape.
- T258 not started.

## Frame reconciliation (T255 evidence)

| frame | original status | WP82 walker | match |
| --- | --- | --- | --- |
| 06 end-wrapped-line | Pg 1 Ln 1" Pos 7.3" | Pg 1 Ln 1 Pos 64 → 7.30" | exact |
| 07 down-desired | Pg 1 Ln 1.17" Pos 6.8" | Pg 1 Ln 2 Pos 59 → 6.80" | exact |
| 08 down-empty | Pg 1 Ln 1.33" Pos 1" | Pg 1 Ln 3 Pos 1 → 1.33" | exact |
| 16 document-end | Pg 3 Ln 2.17" Pos 3" | Pg 3; Ln/Pos unknown (Tab, GAP-1b) | page exact, flow unknown-honest |

Original-observed Ln/Pos are not synthesized: they arrive from native
boundary tokens and the pinned profile's deterministic arithmetic. Full
Line/Pos qualification for tabbed/edited documents remains WP81's amendment
(GAP-1/GAP-1b, tracer design-decisions-4487b48316da + -3204c4f2e908).
