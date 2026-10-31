---
work_package_id: WP52
title: Reveal Codes active native-token highlight
dependencies:
- WP48
- WP37
- WP47
- WP13
- WP11
- WP21
requirement_refs:
- FR-004
- FR-005
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T154
- T155
- T156
phase: M1 existing Reveal Codes parity detail; full M1 remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/tui/
create_intent:
- internal/tui/reveal_cursor_test.go
- internal/tui/evidence/wp52/
execution_mode: code_change
owned_files:
- internal/tui/**
role: implementer
tags:
- m1-continuation
- reveal-codes
- display-only
task_type: implementation
tracker_refs: []
---

# WP52: Reveal Codes active native-token highlight

## Governance, prerequisite authority and bounded objective

Resolve implementer-ivan and implement action-scoped charter context. Read actual spec/plan/data-model/continuation, charter, docs/compatibility.md, docs/roadmap.md and prerequisite independent review evidence. Use canonical runtime and real assigned workspace; coordinate lifecycle mutations with root. No self-review, other package advancement or mission acceptance.

Dependencies: **WP48, WP37, WP47, WP13, WP11, WP21**. WP48 must be ACTUALLY independently approved before implementation claim; current unreviewed48 source, its R1 correction/interoperability preflight, and presence on a moving H branch are not authority. Read approved48's actual source/API at claim, not a guessed/frozen future interface or copied overlay. If its API differs materially from the approved37/47 source context below, report the precise scoped contract issue before widening ownership or borrowing unreviewed code.

Approved source context: WP37 dfd2df9de6e6082cfdf32f9a82cbc5d68908b8f8 (relevant model/runtime bytes agree with d5c2ab97); WP47G3937a3d549ea2933745a82118147654824698f25 Present/Snapshot; document44aab36accdf14a370a67fd73945907871ab7193 cursor/token/Present. Read only existing domain APIs; no E/G source change. Original WP13 18d6afe9, WP11 contract3fb4a5b8 and WP21 leavesd7b94b1f are exact source-backed inputs. Full commits/blobs/SHA and raw capture/runner/environment/native assets are in the sealed Reveal reconnaissance handed off with this task: seal **be06e5e6dcfa76a2c6ba2515c31c0f2b71edcb097f4b90287b67d908345057a0**. Verify the inert byte-exact source map/seals, not its prose alone.

Implement one visible parity improvement in the existing lower Reveal stream: select the active native token/cell from the SAME authoritative native revision, cursor gap and token-owned spans as the normal pane. Keep the actual existing upper hardware caret mapping. This is not full split-screen geometry, a new code catalogue or a format/layout rewrite. There is no replacement document, IR, serialization, parser, native admission, source-capability or history permission added.

All38 obligations/91groups/36lessons/nested leaves/SC001–005 and full M1 remain open. This is original Reveal Codes M1 functionality, not a response-only enhancement or M2 feature. No queue-exhaustion acceptance, parent/FR closure, M2/PDF start or full clone claim. FC-001–009 remain binding and FC-010 stays M2-gated. No new original is needed or authorized; no research VM/private resource/extraction/guest grant.

## T154: Source-bound active token/cell rendering in the real view

Inspect approved48/37's actual panes/View and the shared Session.Present/Cursor values. Keep one source-consistent immutable snapshot for a rendering decision. Derive the active lower range from actual token index/gap, kind and original native span, never text matching, byte hashes, filename/fixture recognition, copied VGA screens or an independent format/model. View-local bounded cell/style ranges are display values only; they do not replace authoritative native token identities.

For the existing ASCII/Bold subset, select one display cell for ASCII; all six derived cells of a native BoldOn `[BOLD]` or BoldOff `[bold]` label; and one virtual blank cell at actual EOF only. Literal typed `[BOLD]` or `[bold]` remains six independent ASCII characters; the current one-character cell is selected, not a fabricated native Bold token. Adjacent/repeated equal labels and ordinary bracket text must remain distinguishable by source token identity. EOF is gap==TokenCount, not the end of a4096-token window while more native tokens exist. A virtual marker/blank never enters native bytes, history or IO.

Original source ORIGIN is334B SHA c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d: A324+1, BoldOn325+3=c30cc3, B328+1, C329+1, BoldOff330+3=c40cc4, D333+1. It is a witness, not a special production branch. The original gap mapping0..6 has upper caret columns0/1/1/2/3/3/4; lower active columns A0, BoldOn1–6, B7, C8, BoldOff9–14, D15, EOFblank16. Across a code boundary the upper caret stays stationary while lower selection moves. Preserve current upper terminal row/mapping: the original upper caret is row0, the existing Wordling upper row is1; do not move it into the code stream or use Reveal-label width as normal-text width.

Use a declared, source-backed Linux ANSI logical-role map for selected original VGA attributes: active0x47, base0x17 and inactive code labels0x1F. This is not a guessed inverse of the base style. Preserve foreground/background/intensity roles with explicit reset/containment through clipping; actual terminal RGB/palette/font/raster/physical key delivery remain unqualified. Do not replay literal attribute arrays from a fixture or pretend all user color setups are identical. The map is a presentation/profile rule derived from raw original attributes, never a new on-disk format.

The new style must visibly reach actual Model.View and the production executable, not an unused helper, test-only shim, exported side channel or screenshot overlay. Existing Alt-F3/Left/Right commands and semantic cursor behavior remain reducer-owned. No document serialization or byte interpretation moves into TUI; Present remains the domain source for supported token identity and native spans.

## T155: Preserve window/source/lifecycle boundaries and bounded work

Retain the current4096-token bounded presentation and horizontal clipping unless the actually approved48 code already narrows it for a justified reason. No new general scrolling, vertical flow, native pagination, CPI/LPI, Pos inches, printer/font/cache/default algorithms or arbitrary window-height interpretation. Requested windows containing Opaque tokens and gaps beyond the supported window retain truthful typed/refusal presentation and native/gap state. Do not silently skip unknown bytes, substitute a plausible label or report universal Reveal support. Whole native files remain retained for no-edit paths.

Clip styled ranges by visible cell intersections without splitting control sequences, leaking color/style, indexing outside token/window bounds or calling a window end EOF. Test widths1, label-width boundaries,80 and the existing capped4096, small heights and exact/over window boundaries with bounded allocations/work. Source token spans and virtual EOF remain distinct. Bound diagnostics and rendering from actual requested windows, not unbounded full-file scans or late “work” counters. Record meaningful measured maximum-window/memory evidence; do not claim historical DOS capacities or physical terminal latency.

Repeated View/State/Present observations and resize must not mutate document/source/IO state. Through actual navigation/toggles compare against the existing reducer's legitimate transitions: native bytes/revision/birth/source and dirty/saved values stay appropriately unchanged, while real cursor/view/selection/history grouping/knowledge changes remain exactly reducer-owned. Do not demand or create a fresh history merely for a display operation. Session/Document exported-wrapper replacement, independently parsed equal bytes and stale immutable Model values cannot retarget a captured render to a different current source.

Selection/HistoryPreview retains its existing `[Block]` virtual semantics and actual overlay origin identities. A fragment has no current native-file span; do not treat virtual overlay positions or absent spans as admitted native tokens. Keep unobserved active-style semantics in these modes explicitly scoped rather than inventing original behavior or changing domain refusal. Existing pending IO/detached receipts, question/prompt caret and source guards remain unchanged. A stale render may display its own captured source state but never combine its geometry with a newer native gap/revision.

For macro DISPLAY OFF, the frozen upper/lower display and caret must remain bound to the same captured render; do not apply a live changing gap to old frozen text/styles. Existing macro visibility, stop/buffer/repeat/cancel/receipts remain untouched. Display regression tests establish source consistency, not new original macro semantics or H1 operation permission. No new UI gate or label is added for hypothetical risks.

## T156: Public Model, actual executable PTY and original witnesses

Recompute all28 original13 selected captures (seven gaps × normal/Reveal × two fresh runs), with their six artifacts each: screen.txt, raw4000B text/attributes, CRTC cursor.json, PNG/PPM and guest-status. Check exact source fixture, runner archives/environment and native export SHA/length/Git provenance. This is reuse of already accepted originals, never a new guest. The source proof gives raw row/column/range facts; do not assume hardware cursor alone identifies a token or strip all attributes before comparison.

Use real public Model.Update/View with actual rooted Retrieve/runtime and a genuinely built production cmd/wordling PTY. Send Alt-F3 and Left/Right/toggles across native On/Off, ASCII and EOF; retain raw ANSI and a bounded decoded terminal-cell/style/cursor witness. Compare the lower active token/cell ranges and logical attribute roles against BOTH original runs. Compare stationary upper caret columns at code crossings. Original rows0/13 versus current Wordling rows1/3 and unrelated status/layout differences remain explicit; do not claim whole-screen/raster/pane geometry parity from a selected stream comparison. No helper-only renderer, copied-output terminal or fabricated screenshot replaces this execution.

Add non-fixture printable inputs, literal `[BOLD]`/`[bold]`, repeated native code labels, leading/trailing/adjacent supported codes, zero/empty/EOF, clipped active ranges and bounded-window-end-not-EOF cases so hash/path/string special-casing cannot pass. Use actual accepted native values and domain APIs for test inputs; reader-only synthetic framed cases are clearly test inputs, never original-verified semantics or a new native builder. Cross-image/source wrappers, stale Model render, selection/history virtual overlays, prompt/pending modes and DISPLAY OFF frozen render must retain source consistency and existing behavior. No new unreviewed native operation is required to manufacture tests.

Demonstrate meaningful production-path falsifiers: selecting only one cell of a native Bold label, using the first matching label text (confuses literal/duplicate tokens), using lower width for the normal caret, calling a window end EOF, and omitting/resetting clipped style incorrectly. Mutants must compile and fail the intended real tests, not merely alter a test expectation; restore exact source and bind red/green evidence. Verify view observations/resize cannot schedule IO, create a native revision or leak a virtual EOF/style marker into actual native output. A no-edit Save to an observed absent name through the actual app retains source bytes under existing storage rules; no original-app run is added.

Run gofmt, actual Go build, go test ./..., go vet ./..., genuine configured review_checks.py (all seven applicable checks, no blanket skip), applicable catalogue checks, race and focused bounded render/resource/PTY/mutant checks. Record actual tool/host/commands/exits and source, binary, GoFiles/GOMOD/module/input/output identities under internal/tui/evidence/wp52/. No unchanged native-parser600s fuzz repeat is required for this presentation-only slice; add further tests only for a real change/failure/unresolved concern. Preserve no physical-terminal/key/palette/raster qualification claim.

## Acceptance criteria

- Actual lower Reveal stream visibly selects native token/cell from current authoritative token/gap/spans; no string/hash/fixture replay, shadow document, new parser/writer/admission or format.
- Native Bold code labels select all six display cells; literal bracketed ASCII selects one actual character; actual EOF uses a virtual display blank and a bounded window end is not EOF.
- Both original13 runs' raw attribute/token/caret facts are checked through public Model and actual built-app ANSI PTY. Normal caret remains stationary across zero-width code boundaries; declared logical style map/reset/clipping is correct.
- Source/native/receipt/history/selection/macro-frozen/prompt/pending invariants and existing reducer transitions are preserved; unknown/window refusals remain truthful; actual no-edit output remains exact.
- Required genuine checks, race/falsifiers and measured bounded-render evidence pass. Full pane geometry/ruler/status/scroll/window-height/code catalogue/print metrics/resource/physical parity stay explicitly open M1.

## Ownership and explicit limits

Only **internal/tui/** may change, including existing production view code, tests/README as necessary and new owned internal/tui/evidence/wp52/**. Old broad TUI ownership is ordered through actual approved48; do not change any old ownership metadata. Existing source is not create_intent: actual37 code is immutable source proof and actual48 must be approved before claim. New test/evidence paths in frontmatter are truly absent/new; if an actual approved48 path already exists then preserve it and correct only a future approved task declaration rather than falsely label source creation.

No E/document/parser/writer/format/permission, G/editor/session/history, storage/input/macro engine, cmd/wordling, go.mod/go.sum, source fixture/manual/resource/private cache, canonical catalogue/contract/ADR/spec/plan/tasks/continuation/status or VM/helper/scheduler changes. Tests may build/run existing production cmd/wordling without editing it. Do not read/borrow unapproved48 fixes/preflight or solve a dependency by merging a moving source tip/overlay. If the actual domain/public host contract is insufficient, report a precise separate follow-up before widening this scope.

## Validation and independent review handoff

Commit only owned source/evidence. Before canonical T154–T156 done/for_review, obtain root's shared lifecycle quietpoint and use explicit assigned profile; no manual projections or self-approval. Independent reviewer receives exact source/closure/binary and original raw-attribute/token-span associations, actual public/PTY execution, old/new row differences, native no-change/IO tests, limits, falsifiers and remaining gaps. This prompt/draft/recon is not original grant, claim, runtime analysis or implementation approval. Root finishes current51 refresh/analysis, independent task review, quietpoint canonical52 promotion/finalization/current analysis and actual48 approval before any52 claim.
