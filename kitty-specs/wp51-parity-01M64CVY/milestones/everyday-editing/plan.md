# Everyday editing implementation plan

This plan implements [spec.md](spec.md) inside `wp51-parity-01M64CVY`. The existing `feat/wp51-parity` planning target remains authoritative. Package numbers below are proposed continuations and require canonical task authoring/finalization before implementation claims.

## Source baseline and sequencing

At discovery the primary checkout contained planning and research, while the runnable integrated source was in the H worktree at `f89a48627916b5cb9e360c35047350031b6f06a9`. At discovery it also contained 18 modified tracked files and five untracked Go files. Root preserved those exact 23 files in candidate checkpoint `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, whose parent is the recorded H baseline. This candidate is explicitly UNREVIEWED. Its inherited delta and new WP77 probes both require independent review before downstream consumption. Those local changes include native newline/history changes, key adapters, navigation, menus, file listing and screen rendering. WP76 approval predates them. The reviewed source-intake procedure may merge the committed candidate into the feature target before WP77, with its UNREVIEWED status explicit. WP77 must capture its exact inventory, diff and hashes and independently review the entire candidate delta plus its own probes. Source presence cannot authorize downstream feature consumption before WP77 approval. Narrow corrective WP90 alone may repair the independently confirmed R77-001 before WP77/WP78 approval; it has no new feature scope and no authority to approve inherited source. Canonical finalization and claims determine the actual workspace. Inspect the computed lane and source ancestry rather than forcing a root workspace or guessing a lane. The runtime-mismatch decision and preservation sequence are recorded in decisions.md. Never label these changes approved by inheritance from WP76.

This component-focused ordering avoids declaring multiple existing source owners in one package. Canonical validation must still check the complete computed lane dependency graph for backedges, source propagation and identity changes before claims. Ownership metadata does not authorize an unreviewed cross-component edit. If an API need crosses a package boundary, amend the owning package and its affected downstream tests.

Keep the original immutable reader, document ownership, save transactions and command reducer where they preserve the required behavior. Replace narrow policy assumptions that were useful for earlier bounded demonstrations with explicit supported-document predicates and tested transitions. Old package-specific freeze rules govern their historical evidence. This amendment authorizes reviewed changes to production paths and to tests whose expected behavior this milestone deliberately extends. Preserve historical evidence files and identify superseded assertions precisely.

## Architecture and integration

The normal entry path remains `cmd/wordling` → Bubble Tea `Model.Update` → `editor.Session.Reduce` → document/layout/storage services → `Model.View`. Commands from menus, function keys and mouse selection all use the same session transitions. Reference scenarios and test drivers exercise this entry path.

| Component | Change responsibility |
| --- | --- |
| `internal/wp51` | Preserve the existing framing authority. Extend semantic knowledge only where required native codes or structural updates are proved by the original/toolkit contract. No view-text serialization. |
| `internal/document` | Admit and mutate the supported fixture family independently of New versus Loaded lineage. Add original Underline and return/page semantics, maintain pair relationships and immutable revision/history ownership. Preserve opaque spans and fail atomically on unsafe operations. |
| `internal/editor` | Own document-screen lifecycle, modal prompts, command defaults, save continuations, search state and editability policy. Remove implicit assumptions that saving ends editable life. Keep original receipts and stale-completion protection. |
| `internal/layout` | Produce document lines/pages, physical positions, tab and margin locations, soft-wrap boundaries and cursor mappings from native content and declared resource metrics. Remain independent of terminal dimensions. Use existing resource contracts and observations before introducing a new metric representation. |
| `internal/storage` | Extend pinned-directory capability handling for navigable workspace directories and stable file-list observations. Continue to validate the selected source and destination at use time and preserve failed-save guarantees. |
| `internal/tui` | Render the shared document/layout state into normal, Reveal, menu, Help, List Files and Look screens. Separate menu visibility from keyboard focus. Replace prototype duplicate production render paths with one tested composition. |
| Reference/test tooling | Replay explicit original inputs with state-based waits, capture character/attribute grids and cursor state, retain failures, compare native outputs and test actual Linux terminal delivery. |

Proofreading operates on native word/range positions, uses real admitted lexical resources, and applies every correction through the same document/history/session operations. The TUI preserves reading context, focus and continuation; it never substitutes a second editable string buffer. Supplementary dictionary writes receive the same provenance and failure scrutiny as other original companion formats.

Core data flow is native revision → layout result → viewport projection. Native code positions remain authoritative when visible text widths differ. Search and navigation use shared semantic positions rather than rescanning rendered ANSI strings. Saving consumes the native revision and its structural changes. A layout result cannot silently normalize an untouched source file.

## Proposed dependency chain

The source implementation chain follows storage → document → layout → editor → TUI. Reference work and baseline review are independent roots. Proofreading has a provider → editor → TUI chain and must complete before final qualification. Shared source owners execute sequentially. Canonical finalization determines actual ownership and workspace placement. Parallelize independent reference/review work only when source custody and VM isolation are explicit.

| WP | Deliverable | Dependencies | Requirement coverage |
| --- | --- | --- | --- |
| WP77 | Independently audit the complete UNREVIEWED integrated source candidate and add public-entry baseline probes. Own new `tests/baseline_adoption/`. | None; explicit committed source-epoch input | EE-001, EE-013 |
| WP78 | Qualify original everyday and proofreading journeys, resources, native effects, backups and settings. Own new reference research/tooling outputs. | None; independent reference work | Reference obligations for EE-002 through EE-015 |
| WP79 | Extend navigable pinned-directory storage, browser acquisitions, safe replacement and original backups. Own exact `internal/storage/` production/test files. | WP77, WP78, historical WP41 | EE-010, EE-011, EE-013 |
| WP80 | Extend lossless native everyday editing, return/tab semantics, repeated Bold/Underline and correction/history across New/saved/retrieved documents. Own exact `internal/document/` files. | WP79, historical WP74 | EE-004, EE-007, EE-008, EE-013 |
| WP81 | Implement resource-matched native layout, wrapping/reflow plans, pages, physical positions and cursor mappings. Own new `internal/layout/`. | WP80 | EE-005, EE-006, EE-008, EE-013 |
| WP82 | Complete session lifecycle, navigation, native reflow adoption, correction/history, repeated save/backup continuations, save-on-exit, Doc 2 and New. Own exact `internal/editor/` files. | WP81, historical WP75 | EE-004 through EE-008, EE-011 through EE-013 |
| WP83 | Complete original forward/backward/repeat/code Search. Own editor search and its session integration. | WP82 | EE-009 |
| WP90 | Repair confirmed R77-001 modal input leakage across terminal resize; independently review the narrow fix before a reviewed source-epoch intake and WP77 retry. Own model.go, new historic_resize_test.go and focused resize-modal evidence only. | Historical WP76 only | EE-001, EE-010, EE-013, EE-014 |
| WP84 | Integrate browser/Look/retrieve and shared-layout normal/Reveal views with real keys, physical status and resize. Own exact `internal/tui/` files. | WP83, historical WP76, WP90 | EE-004 through EE-011, EE-014 |
| WP85 | Complete original menus, Help, settings, prompts and command routing; remove superseded prototype TUI paths. | WP84 | EE-002, EE-003, EE-014 |
| WP87 | Implement actual resource-backed proofreading provider and supplementary-dictionary contract. Own new `internal/proofreading/`. | WP78, WP80 | EE-015, EE-013 |
| WP88 | Implement contextual proofreading state, corrections, skip/add and continuation in the editor. | WP83, WP87 | EE-015, EE-013 |
| WP89 | Recreate the original contextual proofreading screen and continuous terminal workflow. Own focused TUI integration. | WP85, WP88 | EE-015, EE-014 |
| WP86 | Independently qualify full editing and proofreading journeys, original interoperability and the exact delivered preview. Own new `tests/everyday_qualification/`; product fixes return to source owners. | WP85, WP89 | EE-001 through EE-015 |

Task authoring may split a package when implementation/review size warrants it. Preserve the named deliverable and dependencies. Every package has independent review before downstream consumption, with code review for implementation packages and reference-method/results review for research packages. WP86 is an additional cross-package review and cannot retroactively substitute for missing package reviews.

## Implementation decisions requiring original evidence

WP78 must settle focus using character/attribute grids. Follow-up research reports F1 deselecting a submenu child while its text remains visible, so text disappearance is an invalid oracle until corroborated. The next-key probe distinguishes the returned parent focus by moving Up to Endnote. The provisional native sample contains underline on/off as c3 0e c3 / c4 0e c4 and a soft return 0D replacing the wrapping space. The repeated original evidence is now in docs/research/everyday-contract-2026-11-05/REPORT.md and evidence-manifest.json. Both native exports have SHA-256 47a1dd33fe87a69a0303f82a2cdf4f10964a77f4ab1144998a2325a12f0bf6a3. Broader reflow and preservation tests remain required before native implementation. WP78 must also settle the native representation of soft-wrap changes, tab placement, page transitions, Underline pairing and display attributes, search termination/default behavior, menu function-key dispatch and F1/Space/Escape behavior. It must compare the current executable's actual menu tree with later manual descriptions. Do not infer exact behavior from the exploratory board where a capture was flagged unresolved or premature.

The repeated reference contract records Full justification, Auto line height, line spacing 1, one-inch margins, Hyphenation No, relative half-inch tabs and Widow/Orphan No. Bind layout to those observed defaults after repeat qualification. A Left-justified implementation cannot pass the original default-profile journey.

The Linux workspace mapping should use one explicitly selected root representing a DOS drive, with child/parent traversal confined to that root. Original path strings, wildcards, case behavior, filename rules and symlink policy need a reviewed adaptation contract. Preserve local-flat callers while introducing the required navigation capability through the normal application configuration. Newly created native files remain ordinary WP documents without host-specific sidecars.

Menu visibility should use the original Setup command path. If the original `.SET` format can be safely read and updated for this setting, use that representation with preservation tests. Otherwise the persistence design is an explicit adaptation decision requiring review before claiming setting parity. A session-only toggle may assist implementation but cannot satisfy EE-003's final persistence criterion.

## Verification and handoff

Run `gofmt`, `go build ./...`, `go test ./...` and `go vet ./...` on changed integrated source. New binary semantics require malformed-input and bounded fuzz checks. New native writers require original retrieval/edit/save checks and conservation tests. Carry existing fixture and macro tests forward, adapting only expectations whose behavior changes by this specification and recording why.

Each WP supplies an acceptance mapping, source/dependency commit identities, changed-file hashes, test commands/results and remaining limitations. Reference historical evidence in place by path/hash. Avoid redundant whole-repository snapshots or copied historical artifact trees. Retain relevant failed runs and original transcripts. Independent review checks public caller compatibility, normal CLI reachability, lossless behavior, error/race handling and original evidence. UI tests include real terminal escape sequences, modifier delivery and mouse selection, with a separate record for any host-intercepted combinations.

WP86 builds a candidate executable, exercises it against the final scenarios, then replaces the preview binary atomically. Existing user sessions continue running their loaded binary. The final handoff identifies the new build and the exact launch configuration. Completed milestone packages can be integrated through the supported workflow, but full mission acceptance remains unavailable while the broader M1 inventory is open.

## Risks

- Existing narrow admissibility and save guards cross document, history, session and UI layers. Relaxing one guard alone can produce unsafe edits or unreachable behavior. WP80 and WP82 must test the whole transition.
- Soft returns and physical positions connect storage to layout. A screen-only solution creates false parity and loses native interoperability.
- The exploratory VM run contained queued-key captures and failed paths. WP78 uses fresh copies, explicit state waits and repeatable checkpoints before expectations become binding.
- Linux terminal geometry and rendering differ from VGA. Character/attribute grids and semantic cursor positions are primary comparisons. Raster/font differences are disclosed, with no unexplained logical-layout tolerances.
- Browser enumeration is an observation. Files may change before retrieval or save. Reuse pinned capabilities and revalidate selected objects rather than trusting display rows as authority.
- Full menus expose unfinished M1 commands. The coverage report distinguishes historical context-disabled commands from implementation gaps, and the accepted everyday paths contain no placeholders.

Foundational package approval may use public API integration tests before its scheduled production consumer lands. The report names that consumer and makes no claim that the end-user feature is delivered. Consumer packages prove normal application reachability; WP86 proves all delivered journeys through the actual executable and rejects unused parallel implementations.

Canonical task staging: WP77 and WP78 are authored in the active task directory first. Complete WP79–WP89 drafts and their task outline remain in `planned-packages/` while the independently reproduced runtime lane-identifier capacity defect is repaired and reviewed. Product scope is unchanged. Historical same-source ordering dependencies are WP79→WP41, WP80→WP74, WP82→WP75 and WP84→WP76; these preserve overlap ordering without the earlier backward-lane cycle. Restore later prompts to the active task directory only after canonical validation preserves all prior identities and yields supported lane identifiers.


2026-11-05 activation update: The exact local multi-letter lane repair has independent approval and fresh-process installed checks. WP79–WP89 prompts are restored for canonical all-package validation. The staged drafts remain in git history; tasks.md is now the complete outline. No product acceptance is inferred. Finalization must preserve every original membership and existing approval; issued claims remain required. Optional synchronization is disabled only per command for this run using supported SPEC_KITTY_SYNC_DISABLE=1, preserving the existing queue and local authoritative lifecycle.

WP77 retry retains its original safety gate: it reviews all inherited candidate changes plus the approved WP90 repair and explicit source-intake receipt. No inferred approval, historical rejection rewrite or reverse H dependency is permitted. Pure full-graph validation found 90 WPs acyclic with all 89 current and 76 historical lane memberships preserved; canonical finalization and issued workspaces remain authoritative.
