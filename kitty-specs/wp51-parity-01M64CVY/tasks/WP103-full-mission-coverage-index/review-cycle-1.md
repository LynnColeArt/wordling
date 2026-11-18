---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-11-18T18:56:15Z'
reviewer_agent: reviewer-renata
wp_id: WP103
---

# WP103 independent coverage-index review

**REQUEST_CHANGES — two verified pre-snapshot mapping gaps.** Structural integrity passes, but the declared snapshot omits known census collections and loses existing menu-to-lesson associations. The fixes stay within the two owned planning artifacts; no product/VM/reference execution, new task or broader exhaustive source study is required.

Reviewed fixed source `ba24b98d62786c22eb79dfd5516c73624db697f0`, two outputs only:

- `contracts/mission1-closeout-coverage.json`: SHA256 `845ce3731e12e7771efcd272d3adc54be782a376dfbe29d05b50b6cf6087c6f1`
- `contracts/mission1-closeout-coverage.md`: SHA256 `5bad927ae0473d4b7d9999ad3666d0b352613e89fb72932e5e2fe1bf0fdd8ece`

Both are relative to `kitty-specs/wp51-parity-01M64CVY/`. Exact execution snapshot is `2e8327d424ac3c8fe4bf76be8ce24bcf5f87c51c`; the review is independent of author `coverage103_impl`. Reviewer Renata's previously resolved profile/action-review governance and the actual canonical WP103 T335–337 scope were used read-only. Parent confirms normal in_review event `01M7QZQA4DHS3E76HXCJH5E161` after for_review `01M7QZMCK5V2W4K6PSG8SBN0MF`. The owned claim route emits no generated review prompt; actual task/contracts/fixed bytes/events replace no fabricated prompt or issuance. ROOT owns canonical verdict capture.

## R1 — known pre-freeze source collections are absent from the typed index

Canonical T335/T336 and its adoption boundary require every newly discovered source leaf/known researched span to remain indexed and independently assignable, while permitting still-unexpanded material to remain pending. A hash binding the entire source file does not supply a missing leaf/lead's stable ID, association or research assignment.

All of the following source collections exist in the exact declared snapshot and are bound by the index, but zero documentary/pending nodes point to them:

| Pinned source under `docs/research/continuation/workbook-source-census-2026-11-18/` | Exact omitted JSON location | Verified missing content |
| --- | --- | --- |
| `workbook-b06-source-census.json` | `/unnumbered_diagram_exercise_entries/0` through `/8` | Nine WB18 completed-outline entries, PDF193/printed184, source labels III.A.1 through III.B.3, with D1/Q1/Q2/Q3 family dependencies. Neither these pointers nor their typed lesson associations exist. |
| `workbook-b02-source-census.json` | `/illustrated_format_menu/groups` | Known Line/Page/Document/Other pictured menu groups and their explicit choices, PDF29/printed20. No source-lead/span node retains this group for further bounded expansion. |
| `workbook-b03-source-census.json` | `/illustrated_menu_leads/0` through `/4` | Five pictured menu/choice leads: Undelete, Page Number Position, Suppress, Select Printer, Move context, with precise pages and explicit unselected branches. |
| `workbook-b03-source-census.json` | `/unresolved_or_freeform/0` through `/3` | Four explicit unresolved execution/source conditions, including WB07 finite Cancel inputs and WB09 textMEMO versus screenshotMEMO.WKB identity. No pending node assigns these known gaps. |

These are not future B11/B12 additions and not missing private-source research. They are already available facts inside the frozen inputs. Existing broad pending lesson/parent nodes do not name them. The current embedded audit checks that existing projections equal their sources, but has no source-collection completeness rule, so it passes despite these omissions.

**Minimal remediation:** add stable local documentary/pending-lead/gap nodes with exact frozen source JSON pointers and applicable lesson/family/research-assignment links for the known entries/groups above. Preserve their unexecuted/unverified and unresolved character. A bounded source-span node may explicitly retain an unexpanded pictured group and its declared choices instead of inventing official CMD IDs or completed behavior. Examine the other frozen census collections for the same selective-collection loss and explicitly disposition metadata-only collections. Extend the embedded read-only audit to compare the declared relevant source-collection record/pointer sets with the indexed nodes; removing an indexed known entry must fail. Update totals and Markdown truthfully. Do not rewrite source census, manufacture execution evidence or reopen exhaustive manual study.

## R2 — nine WP21 menu alternatives lose explicit target-step lesson associations

`coverage-leaves.md`'s embedded `menu_alternatives` records explicitly name existing workbook `target_step` IDs. The index creates all nine `leaf:WP21:ALT-*` nodes but assigns `lesson_refs: []` to every one. It therefore excludes them from both the corresponding `lesson:WBxx.known_leaf_refs` and `gap:lesson:WBxx.known_leaf_refs`, despite their target steps being present with unambiguous lesson references.

Concrete example: `leaf:WP21:ALT-WB01-PRINT` points to `embedded-ledger/menu_alternatives/0`, whose `target_step` is `WB01-PRINT-01` and `menu_route` is `File→Print`. `leaf:WP21:WB01-PRINT-01` has `lesson_refs: [lesson:WB01]`; the alternative has none and is absent from WB01's known-leaf/closure assignment. The other eight losses are WB01 EXIT/NO-SAVE/NO-EXIT, WB02 PRINT/EXIT/LIST and WB03 BOLD/DATE. Exact IDs and target/lesson triples are retained in `independent-mapping-audit.json`.

**Minimal remediation:** resolve each existing explicit target_step through the indexed source step, add its known lesson association to the alternative, and include the alternative in that lesson's known-leaf and pending closure lists. Do not infer behavior from title text or copy an execution label. Add an audit assertion that a known menu target step's lesson association is conserved (and its reverse lesson membership agrees). All existing stable IDs can remain unchanged.

## Checks that passed and scope preserved

The exact embedded Markdown audit was extracted without changing its code and executed from the repository root using `/usr/bin/python -B`; it exited0 in7.61s. The script SHA is `dc519d4b9abb180f22388d7fbbdf53a34144e2ebcb9ef0eb289f7a6e75929bd6`; exact script/stdout/stderr/receipt are preserved beside this report. It verified4,486 unique nodes,956 Git-bound sizes/SHA/blob IDs, existing projected documentary pointers, typed link resolution, acyclic dependencies, exact canonical ID sets,1,935 numbered steps,431 source entries and pending matrix/final acceptance. This is a data/index audit, not product tests, original behavior or a complete source-collection accuracy proof.

I additionally compared actual source records and derived relationships, rather than accepting mechanical_validation booleans:

- All244 scenario full source records and direct parent/requirement links equal the pinned canonical scenarios.
- All91 parent full records and scenario links equal feature-inventory. All49 family historical records, scenario/parent associations and family/prerequisite/condition dependency translations equal the pinned backlog.
- All431 concordance rows preserve every row column and exact parent IDs; each is assigned to an at-most10-row single-source/single-kind batch containing that span. No contents-derived prose end is falsely asserted.
- All38 obligation full records and all8 negative-invariant full records equal acceptance-closure-contract. All5 SC requirement texts equal spec text after joining source line wraps. Required claim fields include exact source/version/resources/receiver/commands/reference/candidate/native/print/test-ID/raw-result and independent verifier/date/disposition; all final records remain pending with no fabricated claim evidence.
- All36 lessons retain canonical theme/source/start/parent associations. Existing leaf reverse membership is internally consistent for the associations the index records; R2 is the missing semantic target join, not an internally dangling link.
- All108 WP status_at_snapshot values equal frozen canonical status. WP106 native approval, WP107 planned public integration, WP100 versus101/102, WP104 in_progress→108 dependency and WP108 planned current TEST purpose are accurately separated. E3/A1 current component links do not close their original/native qualification.
- `prerequisite:backup-contract` is genuinely pending typed prerequisite, not a fake WP or satisfied capability. The ALL condition contains48 delivery families other than Q4, all91 parents,36 lessons,G01–09,eight version gaps and six platform/original/current-TEST qualifications. Q4 depends on the condition and is excluded from its own prerequisites. All remain pending; this index is neither a scheduler authorization nor a queue-exhaustion acceptance escape.
- G01/G02/G03 retain source leaves distinct from G04 mouse/G05 Overstrike/G06 paragraph numbering/G07 menus/G08 Screen/G09 diagnostics/PIF. Version applicability stays pending; V02's historical source/resource reconciliation is not an invented ninth pending discrepancy.
- Negative invariants are meaningful pinned requirements, not pass booleans: NI01 whole-image no-edit identity; NI02 opaque-owner/unsafe-edit refusal; NI03 save/overwrite failures/uncertainty; NI04 source/root/name/buffer/screen/revision/parent/run/request/foreign-result provenance; NI05 password/resource/character refusal; NI06 concurrent/backup/recovery safety; NI07 parser bounds/fuzz; NI08 presentation independence. The index does not fabricate exact existing test-ID coverage for these pending cross-cutting claims.

The official pre-review result was `unverified_baseline` with0 matched test targets and0 recorded failures; it is not a Go run or the data audit above. No new Go/build/product test was necessary for this planning-artifact review.

## Snapshot currentness and post-freeze research

The1,935 numbered steps throughWB30 exactly match the declared committed snapshot:55 original WP21 entries plus1,880 B02–B10 entries, with B01 refinement reused without duplicating numbered steps. `pending-preservation:WB-B11` explicitly records the later341 documentary steps, exact scratch hashes, owner and preservation/refresh obligation; WB31–33 are not falsely called unresearched. B12 is described as in progress outside that dated snapshot. ROOT subsequently preserved B11/B12 through242f9a1c/all36lessons2,556steps, but that later work does not retroactively change the historical snapshot.

WP103 explicitly allows bounded index delivery with pending expansion; an infinite requirement to re-index every future change would contradict that scope. I do **not** request a blanket B11/B12 refresh as an approval condition. Their later preservation/status can be added as a deliberate follow-on revision or a narrowly marked addendum at ROOT's discretion, without silently representing the historical1,935 total as current2,556. R1/R2 concern facts already inside2e8327d4 and therefore still block this snapshot's completeness. The current source/index/matrix field qualifications correctly keep historical not-started/not-implemented labels separate from current approved components and186/38/20 audit scope.

Windows a75aed55/run44311277838 is accurately described as historical after later Go source changes, with final candidate PowerShell7/5.1/default-shell/save-overwrite and physical-input checks pending. Pink Menace Mac builds/testing remain deferred to milestone end. Lost V19/188 custody stays unrecovered; fresh current TEST108 and genuine original104/105/101/102 remain separate. No record claims that source/CONTROL-plan DATA approval is an actual CONTROL/TEST/original run.

## Step3.5 — all15 preexisting contracts and concrete-example disposition

Every preexisting canonical contract file at the frozen snapshot is present among the956 source_bindings. The exact full bytes, SHA and Git blob identity of each passed the executed audit; the inventory is `contract-inventory.json`. All15 are in scope as immutable provenance. Payload execution is orthogonal to this documentary index: source-binding hashes preserve the exact examples without asserting that their behavior passed. The two coverage contracts additionally supply data projections requiring accurate mapping; R1/R2 identify the actual drift in that layer.

| File | Concrete-example disposition / index boundary |
| --- | --- |
| automation.md | Macro/merge original traces, native results and effect boundaries remain exact pinned historical evidence; A1–A5 and WP100–102 stay qualified by their actual roles, not promoted to full language acceptance. |
| coverage-concordance.md | All431 embedded rows, source IDs, printed/PDF starts, inventory links and follow-ups match exactly; bounded batches/source-end unknowns preserved. |
| coverage-leaves.md |29 G01–03 reference leaves,55 numbered steps,12 context records and9 menu alternative records are present as pointer-bound data; G04–09/version gaps remain pending. R2 blocks the missing known menu-target lesson joins. |
| editing.md | Literal `A[BOLD]BC[bold]D`/whole-code token gaps, deletion/Undelete provenance and native writer/original qualification examples remain pinned; E1/E3/current component approval does not claim all deletion/cancel/history branches passed. |
| files-platform.md | FP01 occupied/blank Retrieve, F1/F10/y/n, failure-safe replacement, shell and resource/version distinctions remain pinned. E3/S/O families and qualification nodes retain their pending scope; historical first-slice restrictions are not rewritten as final semantics. |
| language-data.md | Exact character/resource/locale/data examples remain source-bound; T1/T2/E2/L4 pending ownership avoids silently substituting host Unicode, locale or cache behavior. |
| layout-resources.md | L1–L7 recipe/settings, WPU/metric identity, exact raw-stream comparison and no post-result tolerance relaxation remain source-bound. L/P/G families do not convert text/source projection into full geometry/printer/original qualification. |
| macro-fixtures.json | Whole WPM fixture/opcode/operand/provenance/negative input examples remain byte-identical; no inferred macro runtime verdict or alternate format is authored by this index. |
| macro-framing.md | Concrete WPM framing/allowed opcode/API/effect/budget examples are retained verbatim as input evidence; no invocation was executed and no source/table allowed set was changed. |
| native-fixtures.json | Six original fixture identities, macro document-negative, two explicitly synthetic suffix recipes and literal reader limits remain unchanged. Native source presence and component approval do not certify all formats/variants. |
| native-framing.md | Signature/version tuple, full C0–CF width vector, L+4 trailers, eight-byte merge exceptions, typed failures and explicit fuzz CLI/budgets remain exact. No parser or timed fuzz claim arises from this data audit. |
| resource-readiness.md | Readiness/identity/access/licence blockers and reproducible acquisition/check examples remain source-bound, never interpreted as an acquisition grant or qualified current private input. |
| session.md | SESSION1, command/key/filename/cancel/Reveal/semantic revision examples remain qualified by actual evidence state; snapshot component statuses do not close the unrun original session branches. |
| startup-family-successors.md | WorkingLease retained-control successor examples remain exact metadata; no P/owner capability or operational approval is created. |
| structured-graphics.md | Structured content/equation/graphics/raw native/resource examples remain pinned; D/G/L/P pending families retain their real prerequisites rather than declaring unsupported structures complete. |

No new runtime enum/constant/command/validator is introduced. The closed-set SSOT round-trip here is actual set equality against the frozen canonical244/91/36/49/38/5 inputs, all8 exact NI source records and108 frozen status records, plus exact bytes for every contract copy. The JSON's local claim verdict vocabulary (`pending`, `verified`, `rejected`, `explicitly-adjudicated`) defines planning evidence disposition only, not new Spec Kitty lifecycle verdicts or runtime role admission. All final source claims remain pending. No runtime constant lacking a mirror assertion is introduced. The two missing-coverage findings are not excused by these preserved literals or passing counts.

## Effects and handoff

Only Git/file reads, standard-library documentary audits and scratch writes occurred. No CLI status/Op/index/lifecycle write, source edit, new worktree, Go/build, Mac, original/VM/private resource, grant, P, TEST or CONTROL action occurred. No official matrix, historical prompt/event, source registry or canonical audit was changed by this reviewer. Structured verdict and audit receipts are scratch evidence for ROOT's normal rejection/feedback capture; ROOT must preserve the fixed candidate and append history normally.
