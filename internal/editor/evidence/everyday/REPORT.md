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

- T254 in progress (integration seam design complete, implementation next).
- T255–T258 not started.
