# Mission Specification: WordPerfect 5.1 parity

**Mission Branch**: `feat/wp51-parity`  
**Created**: 2026-10-29  
**Status**: Initial specification; research and acceptance decomposition open  
**Mission**: `wp51-parity-01M64CVY` (`01M64CVYYRTDKBCYZ56H6XNTEQ`)  
**Input**: Lynn confirmed two missions: complete WP 5.1 DOS parity first, then
modern conveniences including PDF; original file formats remain unchanged.

## Confirmed intent and boundaries

For writers and original WP 5.1 users, opening or creating a document on Linux
must provide the original application's commands, formatting semantics,
automation, files, and printed results. Reveal Codes means the original editing
function, not merely a visual representation of formatting. Native documents and
companion artifacts must remain interoperable with the original application.

This is M1 of the [two-mission charter](../../.kittify/charter/charter.md).
PDF and newly selected modern conveniences belong to M2 after parity acceptance.
Existing backup, mouse, configuration, and other original functions remain M1.
Intermediate releases are milestones within M1, not a reduced definition of parity.
User confirmation is recorded in `decisions/DM-01M64CWKX056PQDXX2D3QW7QR0.md`.

The [compatibility contract](../../docs/compatibility.md) is binding. The exact
reference executable is now fingerprinted and its Help date confirmed; no
Wordling compatibility is claimed. The [selected primary target](../../docs/decisions/0001-reference-release.md)
is plain 5.1 DOS, U.S. English dated 1992-03-09, without excluding other original
language/character obligations.
The downloaded manuals span several publication dates and must be reconciled.

`main` is the GitHub integration/PR destination. Spec Kitty's `meta.json`
`target_branch` is `feat/wp51-parity`, the mission's planning placement; these are
distinct surfaces in this runtime. No mission merge or implementation acceptance
is requested by starting this specification.

## User Scenarios & Testing *(mandatory)*

Priorities establish sequencing, not optional scope. Source groups and initial
acceptance probes are in the [inventory](../../docs/research/feature-inventory.md).
These scenarios are authored requirements; none has been executed yet.

### User Story 1 — Keep original documents usable (Priority: P1)

A user retrieves, edits, and saves original documents without conversion or loss.

**Independent Test**: Execute the same bounded edits in Wordling and the declared
WP 5.1 reference, inspect native data, then retrieve and print both results in WP.

**Acceptance Scenarios**:

1. **Given** a valid original file, **when** it is opened and saved without edits,
   **then** the output bytes are identical (FC-002).
2. **Given** text containing attributes and an opaque valid structure, **when** a
   supported edit is made elsewhere, **then** unrelated content and relationships
   survive and WP retrieves the file without repair or feature loss (FC-003/004).
3. **Given** a new document, **when** the user saves through the original workflow,
   **then** WP 5.1 retrieves, edits, prints, and saves it, and Wordling reopens it.
4. **Given** a failed or unsafe save, **when** the error occurs, **then** the
   original file remains intact and the user receives an explicit failure.

### User Story 2 — Work through the original editor (Priority: P1)

An experienced user uses the original keys, prompts, menus, selection, search,
Reveal Codes, and editing semantics without relearning the word processor.

**Independent Test**: Replay a recorded reference session and compare command
state, cursor position, code effects, prompts, selections, and saved results.

**Acceptance Scenarios**:

1. **Given** a formatted paragraph, **when** Alt-F3 is used and a code is deleted,
   **then** both panes reflect the same change and the saved file matches its
   documented semantic effect (REF51 pp. 112-113, 560-562).
2. **Given** a code embedded in text, **when** typeover reaches it, **then** the
   code remains and inserted characters follow original behavior (p. 695).
3. **Given** three deletions made with declared commands, **when** the original
   Undelete choices are used, **then** text and code restoration match the
   reference command-specific behavior (p. 697).
4. **Given** nested menus, both document screens, and search prompts, **when**
   original navigation/cancel commands are replayed, **then** document and prompt
   state match the reference, including unchanged state after cancellation.

### User Story 3 — Format and print the same document (Priority: P1)

A user produces the original formatted pages, including advanced structures.

**Independent Test**: Compare page boundaries, glyph positioning, codes, and
printer output with fixed page settings and identical declared resource metrics.

**Acceptance Scenarios**:

1. **Given** fixed printer/font resources and layout settings, **when** margins,
   tabs, columns, headers, notes, and hard/soft breaks are combined, **then**
   pagination, numbering, and printed positions agree with the reference.
2. **Given** a table, equation, and anchored graphics box, **when** they are edited
   and printed, **then** structure, calculations, placement, wrapping, and saved
   representation retain original semantics.
3. **Given** original index/contents/authorities marks and subdocuments, **when**
   generation runs, **then** entries, order, numbering, and references agree.
4. **Given** selected original printer resources, **when** print-to-disk is used,
   **then** the documented original printer-language output is retained.
5. **Given** a graphics-capable reference preview, **when** preview is opened on
   Linux, **then** the original page-inspection functions have a tested Linux
   presentation; terminal limitations cannot silently remove this obligation.

### User Story 4 — Automate and manage work (Priority: P2)

A user reuses original macros, merge files, styles, dictionaries, spreadsheet
links, and utilities without migrating those artifacts to new formats.

**Independent Test**: Run fixtures and keystrokes through both applications,
compare generated files and results, and reopen them in the original app.

**Acceptance Scenarios**:

1. **Given** an original macro or merge workflow, **when** it is executed or
   edited, **then** commands, variables, expressions, prompts, output, and errors
   agree with the declared reference (including native serialization).
2. **Given** text, language resources, sort keys, or a spreadsheet link, **when**
   original language/data tools operate, **then** original results and update
   behavior are reproduced using declared resources.
3. **Given** backup, configuration, utility, and file-management workflows,
   **when** exercised on Linux, **then** original artifact semantics remain and
   platform adaptations are documented and tested.

### Edge Cases

- Truncated prefixes, invalid pointers, cyclic packet chains, bad lengths,
  mismatched delimiters, deeply nested text, and malformed encrypted data.
- Unrecognized valid code/packet types; edits that invalidate opaque references.
- Paired attributes crossing selections, deletion boundaries and subdocuments.
- Typeover at code boundaries, cancellation during prompts, and deletion history.
- Unsupported characters, missing fonts/dictionaries/graphics, and printer changes.
- Hard/soft pages, tables spanning pages, note continuation, and field regeneration.
- Wrong passwords, interrupted writes, disk exhaustion, permissions, and shared
  file conflicts. No failing path may damage the original or report false success.
- Terminal resize, unavailable modified function keys, and graphics presentation.
- DOS paths, 8.3 names and case handling versus Linux paths; explicit mappings
  must be resolved before compatibility claims for those workflows.

## Requirements *(mandatory)*

All statuses below describe delivery, not user approval of project direction.
`Open` means required and not yet implemented/verified. Inventory groups are
research coverage units; decomposition adds obligations without narrowing scope.

### Functional Requirements

| ID | Title | User Story | Priority | Status |
| --- | --- | --- | --- | --- |
| FR-001 | Full traceable coverage | As a maintainer, I can trace every original manual chapter, appendix, menu, command and bundled utility to stable inventory IDs, version applicability and acceptance evidence; completion leaves zero unclassified entries. | High | Open |
| FR-002 | Native documents | As a user, I create/retrieve/edit/save original WP 5.1 documents under FC-001 through FC-004 and FC-007; Story 1 is the acceptance basis. | High | Open |
| FR-003 | Companion artifacts | As a user, I retain original formats for all read/written companion artifacts under FC-005; Story 4 compares artifacts in both apps. | High | Open |
| FR-004 | Classic interaction | As an experienced user, I retain original command keys, menus, prompts, help, cancellation, repeat, display configuration, mouse actions and document windows; Story 2 compares sessions. | High | Open |
| FR-005 | Editing and Reveal Codes | As a writer, I retain original cursor, block, protected text, copy/move/append, deletion/undelete, typeover, search/replace and code-editing semantics; Story 2 and editing inventory probes apply. | High | Open |
| FR-006 | File operations | As a user, I retain original retrieval, save/overwrite, file lists, directories, backup/recovery, Fast Save, locking, comments, compare and exit behavior; Story 1 and file inventory probes apply. | High | Open |
| FR-007 | Original conversions | As a user, I can use all documented original text and 4.2 conversion modes with their original formats, behavior and declared losses (FC-008). | High | Open |
| FR-008 | Text formatting | As a writer, I retain attributes, fonts, kerning, initial codes, margins, alignment, tabs, positioning, hyphenation, spacing, numbering and measurement semantics; Story 3 and format inventory probes apply. | High | Open |
| FR-009 | Pagination | As a writer, I retain original page breaks, paper definitions, numbering, keep rules, columns, headers/footers and notes; Story 3 compares page membership and geometry. | High | Open |
| FR-010 | Structured documents | As a writer, I retain styles, outlines, tables and calculations, generated references, master documents, dates, labels and envelopes; Story 3 compares editing and generated results. | High | Open |
| FR-011 | Graphics and equations | As a writer, I retain original graphics formats, boxes, captions, wrapping, rules, equations, editing and original conversion utility behavior; Story 3 compares native structures and printed geometry. | High | Open |
| FR-012 | Macros and merges | As a user, I record/edit/run original macro and merge languages and original conversion utilities; Story 4 compares commands, expressions, variables, output and errors. | High | Open |
| FR-013 | Data operations | As a user, I retain sorting, record selection, column math, spreadsheet import and links; Story 4 compares results and refresh behavior. | High | Open |
| FR-014 | Language tools | As a writer, I retain original character identities, composition, language selection/resources, spelling/dictionaries, lookup/counts and thesaurus behavior; Story 4 and FC-006 apply. | High | Open |
| FR-015 | Printing | As a user, I retain original print choices, quality, printer commands/resources, font substitutions, print jobs, printer utilities and print-to-disk behavior; Story 3 and print probes apply. | High | Open |
| FR-016 | Document preview | As a user, I retain original page-inspection functions based on declared printer resources; Story 3 compares preview to original output. | High | Open |
| FR-017 | Platform-dependent functions | As a user, I retain documented settings, startup options, network/shared-file workflows, shell/process and utility functions through explicit, tested Linux mappings; Story 4 applies. | High | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | No-edit preservation | 100% of accepted valid native no-edit fixtures save with identical length, SHA-256 and bytes. | Integrity | High | Open |
| NFR-002 | Failure safety | 100% of declared failed-save and rejected-unsafe-edit scenarios leave original files intact; zero silent truncation, content loss or false-success results. | Reliability | High | Open |
| NFR-003 | Bounded parsing | Zero crashes, out-of-bounds accesses or infinite loops in the committed malformed-input corpus; resource bounds and a reproducible fuzz budget must be declared before parser acceptance. | Robustness | High | Open |
| NFR-004 | Evidence completeness | 100% of features claimed verified link durable reference/version/resource and test evidence; zero verified labels based only on manual text or self-comparison. | Auditability | High | Open |
| NFR-005 | Layout fidelity | Zero unexplained page-break, numbering, or glyph-position differences in accepted reference scenarios under matched resources; any comparison tolerance must be justified and recorded before its test runs. | Fidelity | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| C-001 | Platform and stack | Linux application in Go with Bubble Tea, as explicitly selected by the owner. | Technical | High | Open |
| C-002 | Permanent native formats | Original WP 5.1 document and companion formats remain durable; product name Wordling 5.2 does not change stored format versions. No required Wordling wrapper, sidecar or intermediary conversion. | Compatibility | High | Open |
| C-003 | Two missions | Complete plain WP 5.1 DOS parity precedes M2. PDF and newly chosen conveniences are M2; original features stay M1. | Scope | High | Open |
| C-004 | Licensing | Apache-2.0 for original contributions. External manuals, binaries, dictionaries and resources are not relicensed; committed fixtures require provenance and redistribution permission. | Distribution | High | Open |
| C-005 | Exact reference declaration | Record executable edition, date, locale and hashes, environment and resources before accepting original-app comparisons. 5.1+ and Windows 5.2 are not the target. | Evidence | High | Open |
| C-006 | No hidden scope cuts | Unresolved platform/resource/graphics behavior stays visible in M1; any exclusion or baseline change requires an explicit owner decision recorded in git. | Governance | High | Open |

### Key Entities *(include if feature involves data)*

- **Native document**: original bytes, text/codes, prefix packets, nested content,
  resources and their relationships; its saved representation obeys FC rules.
- **Formatting code**: a meaningful editable function affecting surrounding or
  nested content, not just a terminal style.
- **Companion artifact**: a macro, merge data source, style/keyboard definition or
  original resource with independently researched format and behavior.
- **Reference installation**: fingerprinted WP 5.1 DOS release and declared resources.
- **Feature obligation**: stable ID, source/version/locator, behavior, and evidence
  tracked separately for documentary study, implementation and verification.
- **Acceptance scenario**: declared starting data, keystrokes/settings, original
  output, expected invariants and durable test result.
- **Adaptation decision**: explicit Linux mapping of an original platform behavior
  with its compatibility implications and owner decisions where scope changes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every original documented feature and utility is accounted for with
  zero unexplained omissions after full coverage reconciliation.
- **SC-002**: Every M1 obligation has passing original-app comparison evidence;
  100% of accepted native fixtures satisfy FC-001 through FC-009 as applicable.
- **SC-003**: Every declared original workflow produces matching editing, generated
  document and printed semantics under the recorded baseline/resources.
- **SC-004**: Zero unresolved destructive data mismatches, false-success saves or
  undisclosed format substitutions remain at parity acceptance.
- **SC-005**: Every platform adaptation and version discrepancy has a recorded,
  tested disposition; exclusions require an explicit owner-approved scope change.

## Research dependencies and readiness

The expanded inventory contains 91 coverage groups and 236 representative draft
scenarios, not a final command catalogue. A thematic map covers all 36 lessons in
the pinned 1989 workbook; step-level lesson coverage remains incomplete.
Fifty-three bounded original-app recipes have matched expectations in two fresh
runs each, including code-pair repair and Undelete, overwrite refusal, macro
control flow, nested handlers and loops, value/iteration control, file-level
BREAK contexts and merge page settings across nested primary/secondary files. An
independently rebuilt profile passed a menu probe. The setup timestamp variation
is investigated separately without normalizing original files. This is partial
observation, not full scenario verification. [Execution evidence and limits](reference-execution.md).
No Wordling application implementation exists yet. Before detailed
work-package finalization, close these research decisions or provide bounded
investigation packages with explicit outputs:

1. Extend the fingerprinted selected target to historical DOS, graphics-capable
   printer/font and other language/resource profiles; the current FreeDOS and
   mixed-date text-only printer profile has explicit limits.
2. Reconcile the 6/92 reference, 11/89 workbook and 12/93 toolkit with that baseline.
3. Decompose compound groups and cover every command, appendix and workbook lesson.
4. Specify resource formats, encryption, graphics/preview and Linux platform mappings.
5. Define corpus provenance, reproducible comparison procedures and layout tolerances.
6. Establish measured latency/size targets and parser resource/fuzz budgets.

This commit starts the parity mission and preserves confirmed scope. It does not
mark the research, planning, tasks, implementation or acceptance phases complete.
