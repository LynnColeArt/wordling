# WP12 continuation and explicit M1 gap ledger

This checkpoint adds WP13–WP22/T037–T066 as the first bounded continuation tranche. **Full M1 parity remains open.** Every one of the 38 FR/NFR/C/FC requirements and 91 inventory groups has an explicit disposition below. Queued starters do not finish their parent feature. Entire feature families and subcommands still need later reviewed packages; the machine ledger marks all groups open and full implementation unqueued. Completing this tranche cannot authorize accept/merge or M2.

The approved code is on dependency lanes: WP02 at e7de080 implements outer framing and immutable exact export; WP03 at 7deeaf6 adds bounded local snapshot storage with same-file no-op and no-replace publication. Primary contains planning/scripts. These components establish neither semantic editing nor actual overwrite, new native document creation, layout or a complete original session. Their exact committed source/evidence hashes and independent review paths are recorded below. Canonical inventory/scenario status has deliberately not been promoted by this planning work: 53 original recipes remain partially observed, 183 unrun, and every canonical Wordling scenario not-implemented.

The critical implementation path is WP02 → WP15 (read-only token gaps), WP03/WP13/WP15 → WP17 (pure session), WP16/WP17 → WP18 (runnable Bubble Tea/storage composition), then WP14/WP18 → WP19 (measured Linux latency/resources/size). WP13 first closes original SESSION1 gaps; WP14 obtains elementary text/native/print observations using the current resource profile. WP22 separately establishes Compose identity. Neither probe completion is application implementation. WP20 resource readiness and WP21 source/lesson leaf coverage are honest documentary planning artifacts, depend only on planning outputs and share the single planning lane. No code→planning→code dependency cycle is introduced.

No semantic writer is queued without its required native relationship/relocation and original retrieve/edit/print/save evidence. The read-only session is a bounded implementation milestone, including truthful unsupported edit/replacement outcomes. Future task authoring must create separate insertion/typeover, code deletion/pair repair, command-specific three-entry Undelete, writer, layout and all other retained feature slices from reviewed evidence. That unqueued work is explicit, rather than being hidden behind the runnable milestone.

Resource gaps include historical DOS; graphics-capable printer/font/preview metrics; all original language/character locales and per-format resources; legacy conversion and worksheet producers. Field conflicts include WPG byte order, Link End overlapping row/filename offsets, packet8 nonzero size arrays and signed table-formula/border versions. Terminal interception, Linux platform mappings and missing network context remain distinct gaps; an actual baseline/scope change requires an explicit owner decision in git. FC-010 is an enforced M2-gated optional PDF constraint, with no M1 PDF implementation task.

The JSON is the checkable obligation ledger. `component_evidence` means only the exact scope of that component. `queued_starters` names bounded next work, `remaining_obligation` retains the original group breadth, and `full_group_implementation_queued: false` visibly marks uncovered implementation. Local source/lesson leaf expansion remains necessary beyond this baseline. None of the ledger’s open statuses may be inferred closed from runtime queue exhaustion.

<!-- WP12_LEDGER_BEGIN -->
```json
{
  "schema_version": 1,
  "mission": "wp51-parity-01M64CVY",
  "snapshot": "2026-10-30 WP12 continuation authoring",
  "parity_accepted": false,
  "all_m1_obligations_closed": false,
  "queue_exhaustion_authorizes_acceptance": false,
  "counts": {
    "requirements": 38,
    "inventory_groups": 91,
    "canonical_scenarios": 236,
    "partially_observed": 53,
    "not_run": 183,
    "new_wps": 10,
    "new_subtasks": 30,
    "concordance_dispositions": 431,
    "workbook_lessons": 36
  },
  "source_inputs": [
    {
      "path": "docs/compatibility.md",
      "sha256": "98014cd41863f1d38186b45391408455f9410fd35ab88ff1f75bfc03c8a5f27a"
    },
    {
      "path": "docs/roadmap.md",
      "sha256": "23b273639792f223097111526f2655fa3261c20539bf8714e524c3d61a3eca29"
    },
    {
      "path": "docs/research/feature-inventory.json",
      "sha256": "49d37c3f13a537609346bc71751dabb8661676ecfa8fa40f25cee0752b5bccf8"
    },
    {
      "path": "docs/research/command-scenarios.json",
      "sha256": "a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0"
    },
    {
      "path": "docs/research/sources.json",
      "sha256": "850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/spec.md",
      "sha256": "4255ca47a7e85912094e493dfe68473c2520db722402de081c927367951c6ed7"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/plan.md",
      "sha256": "7f8ab64334f8062c9a89e82a26a9f93741afa76e69800b0e0310f5ebdbeda1ed"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/research.md",
      "sha256": "ebe63969815afc29a0bcb934e380e91782939d21b7ffd8c107cd59cd2326cedb"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/data-model.md",
      "sha256": "c1ac3f4e78763355b1d3afd3a9a522ce2a229f0b4d03ec7b111d5a97e8efd3fc"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/automation.md",
      "sha256": "2529b6218b36fccba2c143c8158017ae853d10e8fe3d7afc1958d6407d50e6f6"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md",
      "sha256": "e2abc5792811326bab19b2d3edced4ccd7a72e26fc84c59d320fac1949c45919"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/editing.md",
      "sha256": "7f542edd647b8735575036b0be570a88b048c5ea97755f25dbddadf92ce3a4bd"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md",
      "sha256": "dee9951828b2176e0714e0434d8774e7d0e0d7f4cc591b797c29954be7ed63bb"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/language-data.md",
      "sha256": "ac75a7cc2840f863a7b2fe2af62b95f0a06caedfed271bd3e644aa21182f8a63"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md",
      "sha256": "aa6384662a74c1c0451a506bd9fdd169420614c558677a40715fbe0bab906631"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json",
      "sha256": "f0f4c945ec6551b5eeff68dd2c4ee108f98633a9979bdbfff6eda2854436e2bd"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md",
      "sha256": "6ff65887643570f264d4e71b362ae302eee1216ddd870b8febbd667b93a7e496"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/session.md",
      "sha256": "826badb986e3e74f3ef236c7222b0b663ca4891c75acd8e5fd34777e7d7b319d"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/structured-graphics.md",
      "sha256": "32a9fa1352c2a07fb754a7d6211cc43f8b356542ce816d7b42c3a9d5a0f425a6"
    }
  ],
  "components": [
    {
      "id": "COMP-WP02",
      "approved_commit": "e7de080452c2906e99c8ace0048c415d842f2f89",
      "scope": "Immutable outer-framed payload-unvalidated document image; exact no-edit export, bounded framing, typed refusals; five original documents accepted and WPM refused.",
      "source_location": "approved code lane; absent from primary planning checkout",
      "review_path": "kitty-specs/wp51-parity-01M64CVY/tasks/WP02-native-reader/review-cycle-1.md",
      "files": [
        {
          "path": "internal/wp51/README.md",
          "sha256": "ec42af13a0ab9ebb92b153c590e4de0ed4a07c341269afe0cc95558ad8926ab2"
        },
        {
          "path": "internal/wp51/evidence/README.md",
          "sha256": "f2a8d9edf6d4a162d686b53afe1d829b0f3c36c5b975fa750300f4f2dca01986"
        },
        {
          "path": "internal/wp51/native.go",
          "sha256": "e13c93687e6119bff44f8405616455849cb728f3b4a1b3949d987dbe2c30b1d6"
        },
        {
          "path": "internal/wp51/evidence/validation.xml",
          "sha256": "34f44ddc476b72cfb8deda592ee10b1db3b87b2d0e82a6a75740a87ae77f9b50"
        }
      ],
      "full_feature_acceptance": false
    },
    {
      "id": "COMP-WP03",
      "approved_commit": "7deeaf6d7b62ce291358eceb81cb08c6f82ce512",
      "scope": "Bounded Linux rooted flat-name snapshot read, same-file no-op with decision and absent-destination no-replace publication; failures and uncertainty exposed; actual replacement refused.",
      "source_location": "approved code lane; absent from primary planning checkout",
      "review_path": "kitty-specs/wp51-parity-01M64CVY/tasks/WP03-native-safe-save/review-cycle-1.md",
      "files": [
        {
          "path": "internal/storage/README.md",
          "sha256": "0791dc7799e59dc4d3bc2e4c46531a3e16b0941e63fa3a0c8735c94689f29b01"
        },
        {
          "path": "internal/storage/evidence/README.md",
          "sha256": "e11dc6188098e06ff3627228c95fa2467bd89b3a2ecaa3a32df3bbca2210f1a2"
        },
        {
          "path": "internal/storage/storage_linux.go",
          "sha256": "75e773e7ec01faa3943c76c874dd0bb4e99937113965139e9239e5ce498beb56"
        },
        {
          "path": "internal/storage/evidence/validation.xml",
          "sha256": "320812b91bfd7809de0a161b4894e8f85d6e45c59f1f18819bfd03c1b9570c81"
        }
      ],
      "full_feature_acceptance": false
    }
  ],
  "requirements": [
    {
      "id": "C-001",
      "requirement_cells": [
        "Platform and stack",
        "Linux application in Go with Bubble Tea, as explicitly selected by the owner.",
        "Technical",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [
        "COMP-WP02"
      ],
      "queued_starter_wps": [
        "WP15",
        "WP16",
        "WP17",
        "WP18",
        "WP19"
      ],
      "remaining": "Continue actual pinned Go/Bubble Tea Linux composition and physically qualified input; no complete editor exists in primary or code lanes.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "C-002",
      "requirement_cells": [
        "Permanent native formats",
        "Original WP 5.1 document and companion formats remain durable; product name Wordling 5.2 does not change stored format versions. No required Wordling wrapper, sidecar or intermediary conversion.",
        "Compatibility",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [
        "COMP-WP02",
        "COMP-WP03"
      ],
      "queued_starter_wps": [
        "WP18"
      ],
      "remaining": "Keep direct original native/companion persistence; future writers must avoid private wrappers/required sidecars and preserve unknown relationships.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "C-003",
      "requirement_cells": [
        "Two missions",
        "Complete plain WP 5.1 DOS parity precedes M2. PDF and newly chosen conveniences are M2; original features stay M1.",
        "Scope",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP21"
      ],
      "remaining": "All original scope stays M1; require real SC-001\u2013005 before M2. FC-010 PDF is optional M2, not a queued M1 export.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "C-004",
      "requirement_cells": [
        "Licensing",
        "Apache-2.0 for original contributions. External manuals, binaries, dictionaries and resources are not relicensed; committed fixtures require provenance and redistribution permission.",
        "Distribution",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP20",
        "WP22"
      ],
      "remaining": "Provenance and redistribution rights for every new fixture/resource; Apache-2.0 original work does not relicense external dictionaries, binaries or manuals.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "C-005",
      "requirement_cells": [
        "Exact reference declaration",
        "Record executable edition, date, locale and hashes, environment and resources before accepting original-app comparisons. 5.1+ and Windows 5.2 are not the target.",
        "Evidence",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP13",
        "WP14",
        "WP20",
        "WP21",
        "WP22"
      ],
      "remaining": "Current March US executable is pinned but mixed printer dates/FreeDOS limitations remain; historical DOS, graphics/font/locale profiles and edition applicability still require qualification.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "C-006",
      "requirement_cells": [
        "No hidden scope cuts",
        "Unresolved platform/resource/graphics behavior stays visible in M1; any exclusion or baseline change requires an explicit owner decision recorded in git.",
        "Governance",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP13",
        "WP16",
        "WP20",
        "WP21"
      ],
      "remaining": "All unresolved groups/leaves/resources/formats/platforms stay in M1; only explicit owner decision in git may exclude/change baseline; none supplied by this continuation.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FC-001",
      "requirement_cells": [
        "Save native documents as original WP 5.1 files. No replacement container, private version, or required sidecar.",
        "Original WP 5.1 opens, edits, prints, and saves Wordling-created files; Wordling reopens the results."
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [],
      "remaining": "A native semantic writer and original open/edit/print/save/Wordling-reopen comparison are absent; exact snapshot publication is not Wordling-created document interoperability.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FC-002",
      "requirement_cells": [
        "An untouched valid supported input saves byte-identically.",
        "SHA-256 and direct byte comparison, including prefix packets and embedded data. Opening must not silently normalize the source."
      ],
      "status": "open-full-obligation",
      "component_evidence": [
        "COMP-WP02",
        "COMP-WP03"
      ],
      "queued_starter_wps": [
        "WP15",
        "WP17",
        "WP18"
      ],
      "remaining": "Current accepted document snapshot bytes proven at component level; composed session and every later accepted input/companion domain need exact length/SHA/direct-byte no-edit acceptance.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FC-003",
      "requirement_cells": [
        "Editing preserves unrelated codes, packet content, embedded resources, and semantic relationships.",
        "Targeted edit fixtures; binary differences explained; original-app retrieval and behavior checked. Offset/length changes are permitted when required, arbitrary normalization is not."
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [],
      "remaining": "No semantic writer exists; prove targeted edits, checked relocation/reference/length updates and unrelated-byte/resource preservation before any mutation claim.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FC-004",
      "requirement_cells": [
        "Unknown or not-yet-supported structures are preserved. Unsafe edits/saves fail explicitly before replacing the original.",
        "Opaque-code and packet fixtures, reference checks, rejected-edit and failed-save scenarios with original bytes unchanged."
      ],
      "status": "open-full-obligation",
      "component_evidence": [
        "COMP-WP02",
        "COMP-WP03"
      ],
      "queued_starter_wps": [
        "WP15",
        "WP17",
        "WP18"
      ],
      "remaining": "Opaque outer-framed bytes preserved/current unsupported variants refused; extend explicit semantic refusal and failure safety as tokens/relationships/codecs are added.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FC-005",
      "requirement_cells": [
        "Original companion artifacts retain their original formats wherever the app reads/writes them.",
        "Per-format fixtures and original-app checks for macros, styles, merge data, keyboard definitions, and user resources; scope expanded from manual research."
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [],
      "remaining": "Per-companion native readers/writers and original-app fixtures/checks remain absent; WPM is explicitly refused by current document parser.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FC-006",
      "requirement_cells": [
        "Characters preserve their WP character-set identities and round-trip.",
        "Character-set corpus; unsupported input receives an explicit error or choice before modification, never silent replacement."
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP22"
      ],
      "remaining": "Native WP set/number corpus, C0 observation/token semantics, context-specific composition and independent mapping/roundtrip remain; ASCII/Bold-only document is insufficient.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FC-007",
      "requirement_cells": [
        "Native saves are independent of conversion through another word processor.",
        "The Go format writer emits original-format data directly; external tools may be independent test witnesses only."
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [],
      "remaining": "Future Go semantic writers must emit native formats directly and pass independent original witnesses; no writer is currently implemented.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FC-008",
      "requirement_cells": [
        "Original export/conversion and print-to-disk modes retain their documented formats and semantics.",
        "Per-mode comparison against original output with encoding, resources, and conversion losses declared. These modes do not replace the native save format."
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP14"
      ],
      "remaining": "Original text/legacy conversion and printer-language export contracts/oracles/implementation remain; PDF cannot substitute original print-to-disk.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FC-009",
      "requirement_cells": [
        "A failed save must not corrupt the existing file.",
        "Tests for permissions, interrupted/short writes, full storage, and failed replacement; original backup conventions researched and preserved."
      ],
      "status": "open-full-obligation",
      "component_evidence": [
        "COMP-WP03"
      ],
      "queued_starter_wps": [
        "WP17",
        "WP18"
      ],
      "remaining": "Local snapshot no-replace/no-op failure safety exists; actual replacement, backup/recovery, permissions/storage exhaustion/interruption and all future writer failures remain.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FC-010",
      "requirement_cells": [
        "PDF is a new, optional M2 export. It never becomes the editable native document format.",
        "M2 PDF acceptance tests against the shared layout output and native-file preservation checks."
      ],
      "status": "m2-gated-constraint",
      "component_evidence": [],
      "queued_starter_wps": [],
      "remaining": "Enforce optional PDF after M1 acceptance in M2; native document identity remains independent. No M1 PDF implementation task is authorized.",
      "unfulfilled_m1": false,
      "full_closure_queued": false
    },
    {
      "id": "FR-001",
      "requirement_cells": [
        "Full traceable coverage",
        "As a maintainer, I can trace every original manual chapter, appendix, menu, command and bundled utility to stable inventory IDs, version applicability and acceptance evidence; completion leaves zero unclassified entries.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP21"
      ],
      "remaining": "Close all command/menu/appendix/utility leaves and 36 workbook step sequences; reconcile editions; implement and differentially verify every resulting obligation. 431 contents dispositions and 91 groups are a baseline, not exhaustive leaves.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-002",
      "requirement_cells": [
        "Native documents",
        "As a user, I create/retrieve/edit/save original WP 5.1 documents under FC-001 through FC-004 and FC-007; Story 1 is the acceptance basis.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [
        "COMP-WP02"
      ],
      "queued_starter_wps": [
        "WP15",
        "WP18"
      ],
      "remaining": "Create/edit native files, semantic writers with relocation/relationship invariants and original retrieve/edit/print/save; encrypted/alternate/nonzero graphics/overlap variants; full workflow interoperability beyond read-only snapshot.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-003",
      "requirement_cells": [
        "Companion artifacts",
        "As a user, I retain original formats for all read/written companion artifacts under FC-005; Story 4 compares artifacts in both apps.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [],
      "remaining": "Independent native codecs and original checks for WPM, styles, merge sources, keyboards and user resources; no companion support follows from document framing.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-004",
      "requirement_cells": [
        "Classic interaction",
        "As an experienced user, I retain original command keys, menus, prompts, help, cancellation, repeat, display configuration, mouse actions and document windows; Story 2 compares sessions.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP13",
        "WP15",
        "WP16",
        "WP17",
        "WP18"
      ],
      "remaining": "Beyond bounded no-edit session: complete menus/help/keyboard maps/mouse/display/both documents, contextual Cancel/Repeat and physical original-key delivery for all commands.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-005",
      "requirement_cells": [
        "Editing and Reveal Codes",
        "As a writer, I retain original cursor, block, protected text, copy/move/append, deletion/undelete, typeover, search/replace and code-editing semantics; Story 2 and editing inventory probes apply.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP13",
        "WP15",
        "WP17",
        "WP18"
      ],
      "remaining": "Insertion/typeover, selection/protection/copy/move/append, deletion/repair/three-level Undelete/search/case and all cursor/Reveal branches; writer and history contracts/fixtures before mutation.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-006",
      "requirement_cells": [
        "File operations",
        "As a user, I retain original retrieval, save/overwrite, file lists, directories, backup/recovery, Fast Save, locking, comments, compare and exit behavior; Story 1 and file inventory probes apply.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [
        "COMP-WP03"
      ],
      "queued_starter_wps": [
        "WP13",
        "WP17",
        "WP18"
      ],
      "remaining": "Actual overwrite with original backups, recovery/timed two-screen behavior, Fast Save, locking/passwords, lists/directories/comments/compare/look/find/summary and full exit decisions; safe no-replace storage is only a foundation.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-007",
      "requirement_cells": [
        "Original conversions",
        "As a user, I can use all documented original text and 4.2 conversion modes with their original formats, behavior and declared losses (FC-008).",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [],
      "remaining": "Per-mode DOS/Generic/5.0/4.2 conversion and CONVERT with lawful legacy inputs/.CRS, exact losses/encoding/output and source-integrity comparison.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-008",
      "requirement_cells": [
        "Text formatting",
        "As a writer, I retain attributes, fonts, kerning, initial codes, margins, alignment, tabs, positioning, hyphenation, spacing, numbering and measurement semantics; Story 3 and format inventory probes apply.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP14"
      ],
      "remaining": "Attributes/fonts/kerning/initial codes, alignment/indent, margins/tabs, line/word/letter spacing, units/position/hyphenation/numbering; elementary text probes precede bounded layout implementation.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-009",
      "requirement_cells": [
        "Pagination",
        "As a writer, I retain original page breaks, paper definitions, numbering, keep rules, columns, headers/footers and notes; Story 3 compares page membership and geometry.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP14"
      ],
      "remaining": "Hard/soft/conditional pages, paper/numbering/parity/binding, keeps/widows/columns, headers/footers/notes with continuation; matched resource geometry and combination tests.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-010",
      "requirement_cells": [
        "Structured documents",
        "As a writer, I retain styles, outlines, tables and calculations, generated references, master documents, dates, labels and envelopes; Story 3 compares editing and generated results.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [],
      "remaining": "Styles/outlines, table structure/calculation/cache, generated references/authorities/index, masters, dates, labels/envelopes; original fixtures then separate decoding/state/writer/generation/layout slices.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-011",
      "requirement_cells": [
        "Graphics and equations",
        "As a writer, I retain original graphics formats, boxes, captions, wrapping, rules, equations, editing and original conversion utility behavior; Story 3 compares native structures and printed geometry.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP20"
      ],
      "remaining": "Nonzero packet8/WPG, native boxes/wrap/captions/rules/equation source+compact stream and GRAPHCNV; resolve field conflicts and resource/version limits before implementation.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-012",
      "requirement_cells": [
        "Macros and merges",
        "As a user, I record/edit/run original macro and merge languages and original conversion utilities; Story 4 compares commands, expressions, variables, output and errors.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [],
      "remaining": "WPM field/opcode grammar and bounded reader/replay/evaluator by macro/merge context, recording/editor/converters and all unobserved expressions/errors/control paths; no runtime exists.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-013",
      "requirement_cells": [
        "Data operations",
        "As a user, I retain sorting, record selection, column math, spreadsheet import and links; Story 4 compares results and refresh behavior.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [],
      "remaining": "SORT1 whole-record boundaries/key/collation/failure probes; SELECT predicate missing case; column Math; original spreadsheet formats/producers/import and persistent link refresh field conflict; then implementation.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-014",
      "requirement_cells": [
        "Language tools",
        "As a writer, I retain original character identities, composition, language selection/resources, spelling/dictionaries, lookup/counts and thesaurus behavior; Story 4 and FC-006 apply.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP20",
        "WP22"
      ],
      "remaining": "Compose native corpus and all WP identities/contexts, language/date/sort effects, original LRS/LEX/SUP/HYC/THS resources and spelling/count/lookup/thesaurus; foreign locales remain required.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-015",
      "requirement_cells": [
        "Printing",
        "As a user, I retain original print choices, quality, printer commands/resources, font substitutions, print jobs, printer utilities and print-to-disk behavior; Story 3 and print probes apply.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP14",
        "WP20"
      ],
      "remaining": "All print selection/quality/commands/substitutions/jobs/delivery, printer/font definitions/utilities and original print-to-disk languages; text streams cannot close graphics output.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-016",
      "requirement_cells": [
        "Document preview",
        "As a user, I retain original page-inspection functions based on declared printer resources; Story 3 compares preview to original output.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP20"
      ],
      "remaining": "All original preview modes/navigation/colors and resource-matched page geometry, including graphics and document structure combinations; no preview implementation exists.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "FR-017",
      "requirement_cells": [
        "Platform-dependent functions",
        "As a user, I retain documented settings, startup options, network/shared-file workflows, shell/process and utility functions through explicit, tested Linux mappings; Story 4 applies.",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP16",
        "WP20"
      ],
      "remaining": "Explicit tested Linux mappings for paths/case/8.3 names, settings/startup/memory/shell/PIF/cursor/capture/converters/shared resources and network locks; owner adjudication only for actual scope/baseline changes.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "NFR-001",
      "requirement_cells": [
        "No-edit preservation",
        "100% of accepted valid native no-edit fixtures save with identical length, SHA-256 and bytes.",
        "Integrity",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [
        "COMP-WP02",
        "COMP-WP03"
      ],
      "queued_starter_wps": [
        "WP15",
        "WP17",
        "WP18"
      ],
      "remaining": "Expand provenance-approved valid input domains beyond five document fixtures/current policy; retain exact bytes in real composed no-edit workflows and every later native/companion reader.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "NFR-002",
      "requirement_cells": [
        "Failure safety",
        "100% of declared failed-save and rejected-unsafe-edit scenarios leave original files intact; zero silent truncation, content loss or false-success results.",
        "Reliability",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [
        "COMP-WP03"
      ],
      "queued_starter_wps": [
        "WP17",
        "WP18"
      ],
      "remaining": "Preserve failure safety in real session and all future semantic writers/replacement/backup/recovery/conversion/shared-file scenarios; local no-replace fault injection is not full original save parity.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "NFR-003",
      "requirement_cells": [
        "Bounded parsing",
        "Zero crashes, out-of-bounds accesses or infinite loops in the committed malformed-input corpus; resource bounds and a reproducible fuzz budget must be declared before parser acceptance.",
        "Robustness",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [
        "COMP-WP02"
      ],
      "queued_starter_wps": [
        "WP15",
        "WP19"
      ],
      "remaining": "Measure/document per-decoder input/allocation/traversal/output budgets and malformed/fuzz suites as new formats/semantic tokens are introduced; current 16 MiB framing policy is not historical capacity.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "NFR-004",
      "requirement_cells": [
        "Evidence completeness",
        "100% of features claimed verified link durable reference/version/resource and test evidence; zero verified labels based only on manual text or self-comparison.",
        "Auditability",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP13",
        "WP14",
        "WP16",
        "WP19",
        "WP21",
        "WP22"
      ],
      "remaining": "Every verified claim needs durable exact version/resource/reference and Wordling differential evidence. Canonical 53 partial/183 unrun and all 236 not-implemented statuses remain; queue completion is not parity.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    },
    {
      "id": "NFR-005",
      "requirement_cells": [
        "Layout fidelity",
        "Zero unexplained page-break, numbering, or glyph-position differences in accepted reference scenarios under matched resources; any comparison tolerance must be justified and recorded before its test runs.",
        "Fidelity",
        "High",
        "Open"
      ],
      "status": "open-full-obligation",
      "component_evidence": [],
      "queued_starter_wps": [
        "WP14",
        "WP20"
      ],
      "remaining": "Matched resource metrics and pre-test tolerance derivation, elementary geometry then all pagination/glyph/generation/print/preview combinations; zero unexplained accepted differences.",
      "unfulfilled_m1": true,
      "full_closure_queued": false
    }
  ],
  "inventory": [
    {
      "id": "WP51-001",
      "area": "Interaction",
      "title": "Clean screen, status, menus and function keys",
      "requirement_refs": [
        "FR-004"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 3,
          "printed_end": 12,
          "pdf_start": 20,
          "pdf_end": 29
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-001",
        "CMD51-002"
      ],
      "oracle_counts": {
        "partially-observed": 1,
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP16",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-001"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Replay start, edit, nested menus, cancel and exit; record screen and prompts.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-001 (Clean screen, status, menus and function keys); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-002",
      "area": "Interaction",
      "title": "Context-sensitive help",
      "requirement_refs": [
        "FR-004"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 275,
          "printed_end": 276,
          "pdf_start": 292,
          "pdf_end": 293
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-003",
        "CMD51-004"
      ],
      "oracle_counts": {
        "not-run": 1,
        "partially-observed": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Open help from document and nested dialogs; return to the previous state.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-002 (Context-sensitive help); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-003",
      "area": "Interaction",
      "title": "Original keyboard layouts and remapping",
      "requirement_refs": [
        "FR-004"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 304,
          "printed_end": 318,
          "pdf_start": 321,
          "pdf_end": 335
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-009",
        "CMD51-010"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Load, edit, persist and exercise keyboard definitions.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-003 (Original keyboard layouts and remapping); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-004",
      "area": "Interaction",
      "title": "Mouse interactions",
      "requirement_refs": [
        "FR-004"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 434,
          "printed_end": 437,
          "pdf_start": 451,
          "pdf_end": 454
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-153"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Exercise original menu and selection actions with terminal event mapping recorded.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-004 (Mouse interactions); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-005",
      "area": "Interaction",
      "title": "Display configuration and screen type",
      "requirement_refs": [
        "FR-004"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 68,
          "printed_end": 74,
          "pdf_start": 85,
          "pdf_end": 91
        },
        {
          "printed_start": 120,
          "printed_end": 123,
          "pdf_start": 137,
          "pdf_end": 140
        },
        {
          "printed_start": 266,
          "printed_end": 268,
          "pdf_start": 283,
          "pdf_end": 285
        },
        {
          "printed_start": 689,
          "printed_end": 691,
          "pdf_start": 706,
          "pdf_end": 708
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-154"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Compare text attributes, display pitch, dimensions and graphics capabilities.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-005 (Display configuration and screen type); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-006",
      "area": "Interaction",
      "title": "Two-document switching and windows",
      "requirement_refs": [
        "FR-004"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 628,
          "printed_end": 630,
          "pdf_start": 645,
          "pdf_end": 647
        },
        {
          "printed_start": 706,
          "printed_end": 707,
          "pdf_start": 723,
          "pdf_end": 724
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-007",
        "CMD51-008"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Switch and split documents; verify independent cursor and formatting state.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-006 (Two-document switching and windows); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-007",
      "area": "Interaction",
      "title": "Cancel and command repetition",
      "requirement_refs": [
        "FR-004"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 55,
          "printed_end": 55,
          "pdf_start": 72,
          "pdf_end": 72
        },
        {
          "printed_start": 550,
          "printed_end": 550,
          "pdf_start": 567,
          "pdf_end": 567
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-002",
        "CMD51-005",
        "CMD51-006"
      ],
      "oracle_counts": {
        "not-run": 2,
        "partially-observed": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP16",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-005"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Cancel at multiple prompt depths; repeat input and commands.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-007 (Cancel and command repetition); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-008",
      "area": "Editing",
      "title": "Cursor movement and go-to",
      "requirement_refs": [
        "FR-005"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 103,
          "printed_end": 104,
          "pdf_start": 120,
          "pdf_end": 121
        },
        {
          "printed_start": 224,
          "printed_end": 224,
          "pdf_start": 241,
          "pdf_end": 241
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-011",
        "CMD51-012",
        "CMD51-013",
        "CMD51-014",
        "CMD51-015",
        "CMD51-016",
        "CMD51-017",
        "CMD51-018",
        "CMD51-019",
        "CMD51-020",
        "CMD51-021",
        "CMD51-022",
        "CMD51-023",
        "CMD51-024",
        "CMD51-025",
        "CMD51-026",
        "CMD51-049"
      ],
      "oracle_counts": {
        "not-run": 17
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP13",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-019",
            "CMD51-020",
            "CMD51-049"
          ]
        },
        {
          "wp": "WP15",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-049"
          ]
        },
        {
          "wp": "WP17",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-049"
          ]
        },
        {
          "wp": "WP18",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-049"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Move across text, codes, pages and subdocuments; compare cursor positions.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-008 (Cursor movement and go-to); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-009",
      "area": "Editing",
      "title": "Block selection and protection",
      "requirement_refs": [
        "FR-005",
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 48,
          "printed_end": 54,
          "pdf_start": 65,
          "pdf_end": 71
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-027",
        "CMD51-028",
        "CMD51-029",
        "CMD51-030",
        "CMD51-031",
        "CMD51-032",
        "CMD51-033",
        "CMD51-058",
        "CMD51-202",
        "CMD51-203",
        "CMD51-204"
      ],
      "oracle_counts": {
        "not-run": 7,
        "partially-observed": 4
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP15",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-204"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Select original block types and test protection during editing and reflow.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-009 (Block selection and protection); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-010",
      "area": "Editing",
      "title": "Copy, move and append",
      "requirement_refs": [
        "FR-005"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 34,
          "printed_end": 36,
          "pdf_start": 51,
          "pdf_end": 53
        },
        {
          "printed_start": 438,
          "printed_end": 443,
          "pdf_start": 455,
          "pdf_end": 460
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-155",
        "CMD51-156"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Copy or move selections and append to new/existing files with codes intact.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-010 (Copy, move and append); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-011",
      "area": "Editing",
      "title": "Text deletion and restoration",
      "requirement_refs": [
        "FR-005"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 112,
          "printed_end": 116,
          "pdf_start": 129,
          "pdf_end": 133
        },
        {
          "printed_start": 697,
          "printed_end": 697,
          "pdf_start": 714,
          "pdf_end": 714
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-030",
        "CMD51-031",
        "CMD51-034",
        "CMD51-035",
        "CMD51-036",
        "CMD51-037",
        "CMD51-038",
        "CMD51-039",
        "CMD51-040",
        "CMD51-041",
        "CMD51-042",
        "CMD51-043",
        "CMD51-044",
        "CMD51-045",
        "CMD51-050",
        "CMD51-051",
        "CMD51-200",
        "CMD51-201",
        "CMD51-202",
        "CMD51-203",
        "CMD51-204",
        "CMD51-211"
      ],
      "oracle_counts": {
        "not-run": 12,
        "partially-observed": 10
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP15",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-204"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Compare deletion units and three-entry undelete behavior including paired codes.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-011 (Text deletion and restoration); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-012",
      "area": "Editing",
      "title": "Insert versus typeover",
      "requirement_refs": [
        "FR-005"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 695,
          "printed_end": 696,
          "pdf_start": 712,
          "pdf_end": 713
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-046",
        "CMD51-047"
      ],
      "oracle_counts": {
        "partially-observed": 1,
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Type across text and formatting codes; verify codes are not overwritten.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-012 (Insert versus typeover); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-013",
      "area": "Editing",
      "title": "Reveal Codes",
      "requirement_refs": [
        "FR-005"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 560,
          "printed_end": 562,
          "pdf_start": 577,
          "pdf_end": 579
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-048",
        "CMD51-049",
        "CMD51-050",
        "CMD51-051",
        "CMD51-200",
        "CMD51-201",
        "CMD51-202",
        "CMD51-203",
        "CMD51-204"
      ],
      "oracle_counts": {
        "partially-observed": 8,
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP13",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-049"
          ]
        },
        {
          "wp": "WP15",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-048",
            "CMD51-049",
            "CMD51-204"
          ]
        },
        {
          "wp": "WP16",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-048"
          ]
        },
        {
          "wp": "WP17",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-048",
            "CMD51-049"
          ]
        },
        {
          "wp": "WP18",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-048",
            "CMD51-049"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Toggle Alt-F3; move/delete in the code pane and compare effects in the normal pane.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-013 (Reveal Codes); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-014",
      "area": "Editing",
      "title": "Search and replacement",
      "requirement_refs": [
        "FR-005"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 551,
          "printed_end": 554,
          "pdf_start": 568,
          "pdf_end": 571
        },
        {
          "printed_start": 571,
          "printed_end": 573,
          "pdf_start": 588,
          "pdf_end": 590
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-052",
        "CMD51-053",
        "CMD51-054",
        "CMD51-055",
        "CMD51-056",
        "CMD51-057",
        "CMD51-058",
        "CMD51-059",
        "CMD51-060",
        "CMD51-061",
        "CMD51-062"
      ],
      "oracle_counts": {
        "not-run": 11
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Exercise text/code searches, direction, case and extended subdocument replacement.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-014 (Search and replacement); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-015",
      "area": "Editing",
      "title": "Case changes and repeat input",
      "requirement_refs": [
        "FR-005"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 56,
          "printed_end": 57,
          "pdf_start": 73,
          "pdf_end": 74
        },
        {
          "printed_start": 550,
          "printed_end": 551,
          "pdf_start": 567,
          "pdf_end": 568
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-063",
        "CMD51-064"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Apply commands to text and blocks; compare boundaries and formatting.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-015 (Case changes and repeat input); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-016",
      "area": "Editing",
      "title": "Hard and soft returns and spaces",
      "requirement_refs": [
        "FR-005"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 269,
          "printed_end": 269,
          "pdf_start": 286,
          "pdf_end": 286
        },
        {
          "printed_start": 557,
          "printed_end": 560,
          "pdf_start": 574,
          "pdf_end": 577
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-110",
        "CMD51-111"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP14",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-111"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Distinguish explicit paragraph boundaries from reflow; preserve code identity.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-016 (Hard and soft returns and spaces); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-017",
      "area": "Editing",
      "title": "Line-drawing text",
      "requirement_refs": [
        "FR-005"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 337,
          "printed_end": 338,
          "pdf_start": 354,
          "pdf_end": 355
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-142",
        "CMD51-143"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Create and modify line-drawing structures without corrupting text or characters.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-017 (Line-drawing text); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-018",
      "area": "Editing",
      "title": "Refresh and reformat",
      "requirement_refs": [
        "FR-005"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 563,
          "printed_end": 564,
          "pdf_start": 580,
          "pdf_end": 581
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-144"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Trigger rewrite and inspect layout and cursor effects.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-018 (Refresh and reformat); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-019",
      "area": "Files",
      "title": "Retrieve and insert documents",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 554,
          "printed_end": 557,
          "pdf_start": 571,
          "pdf_end": 574
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-065"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [
        "COMP-WP03"
      ],
      "queued_starters": [
        {
          "wp": "WP13",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-065"
          ]
        },
        {
          "wp": "WP16",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-065"
          ]
        },
        {
          "wp": "WP17",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-065"
          ]
        },
        {
          "wp": "WP18",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-065"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Retrieve whole documents and blocks, preserving their codes and resource references.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-019 (Retrieve and insert documents); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-020",
      "area": "Files",
      "title": "Native save and overwrite workflow",
      "requirement_refs": [
        "FR-002",
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 565,
          "printed_end": 566,
          "pdf_start": 582,
          "pdf_end": 583
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-066",
        "CMD51-067",
        "CMD51-068",
        "CMD51-069",
        "CMD51-070",
        "CMD51-149",
        "CMD51-150",
        "CMD51-151",
        "CMD51-152"
      ],
      "oracle_counts": {
        "partially-observed": 2,
        "not-run": 7
      },
      "component_evidence": [
        "COMP-WP03"
      ],
      "queued_starters": [
        {
          "wp": "WP13",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-066",
            "CMD51-067",
            "CMD51-069",
            "CMD51-070"
          ]
        },
        {
          "wp": "WP16",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-066"
          ]
        },
        {
          "wp": "WP17",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-066",
            "CMD51-067",
            "CMD51-069",
            "CMD51-070",
            "CMD51-149"
          ]
        },
        {
          "wp": "WP18",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-066",
            "CMD51-067",
            "CMD51-149"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Save F10; verify filename editing, overwrite confirmation and initial codes.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-020 (Native save and overwrite workflow); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-021",
      "area": "Files",
      "title": "Original and timed backups",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 41,
          "printed_end": 44,
          "pdf_start": 58,
          "pdf_end": 61
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-071",
        "CMD51-072",
        "CMD51-073",
        "CMD51-074"
      ],
      "oracle_counts": {
        "not-run": 4
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Exercise both existing backup modes and recovery behavior; compare artifacts.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-021 (Original and timed backups); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-022",
      "area": "Files",
      "title": "Fast Save",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 197,
          "printed_end": 197,
          "pdf_start": 214,
          "pdf_end": 214
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-075"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Compare saved bytes and formatting with the option enabled and disabled.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-022 (Fast Save); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-023",
      "area": "Files",
      "title": "File lists, directories and resource locations",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 117,
          "printed_end": 119,
          "pdf_start": 134,
          "pdf_end": 136
        },
        {
          "printed_start": 347,
          "printed_end": 354,
          "pdf_start": 364,
          "pdf_end": 371
        },
        {
          "printed_start": 358,
          "printed_end": 361,
          "pdf_start": 375,
          "pdf_end": 378
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-076",
        "CMD51-077",
        "CMD51-078",
        "CMD51-079",
        "CMD51-080",
        "CMD51-081"
      ],
      "oracle_counts": {
        "not-run": 6
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Replay file operations and path resolution with explicit Linux mapping.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-023 (File lists, directories and resource locations); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-024",
      "area": "Files",
      "title": "Password-locked documents",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 362,
          "printed_end": 363,
          "pdf_start": 379,
          "pdf_end": 380
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-082"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Open and save correct/wrong-password fixtures without touching the original on failure.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-024 (Password-locked documents); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-025",
      "area": "Files",
      "title": "Original text import/export modes",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 685,
          "printed_end": 688,
          "pdf_start": 702,
          "pdf_end": 705
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-083",
        "CMD51-084"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Compare each original mode, encoding and documented losses.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-025 (Original text import/export modes); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-026",
      "area": "Files",
      "title": "Original 4.2 conversion modes",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 130,
          "printed_end": 142,
          "pdf_start": 147,
          "pdf_end": 159
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-157"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Compare both conversion directions using original-version fixtures.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-026 (Original 4.2 conversion modes); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-027",
      "area": "Files",
      "title": "Document comments and comparison",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 124,
          "printed_end": 129,
          "pdf_start": 141,
          "pdf_end": 146
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-158",
        "CMD51-159"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Persist comments and compare documents, inspecting marked changes.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-027 (Document comments and comparison); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-028",
      "area": "Files",
      "title": "Document look/find operations",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 197,
          "printed_end": 202,
          "pdf_start": 214,
          "pdf_end": 219
        },
        {
          "printed_start": 364,
          "printed_end": 368,
          "pdf_start": 381,
          "pdf_end": 385
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-085",
        "CMD51-086"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Exercise file-content inspection and conditional file finding.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-028 (Document look/find operations); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-029",
      "area": "Files",
      "title": "Exit and save decisions",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 194,
          "printed_end": 196,
          "pdf_start": 211,
          "pdf_end": 213
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-087"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP13",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-087"
          ]
        },
        {
          "wp": "WP16",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-087"
          ]
        },
        {
          "wp": "WP17",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-087"
          ]
        },
        {
          "wp": "WP18",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-087"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Replay saved/modified/unnamed documents through all exit decisions.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-029 (Exit and save decisions); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-090",
      "area": "Files",
      "title": "Document summaries and descriptive names",
      "requirement_refs": [
        "FR-006"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 145,
          "printed_end": 149,
          "pdf_start": 162,
          "pdf_end": 166
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-088",
        "CMD51-089"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Create, cancel, save and retrieve document summaries; inspect long-name file lists.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-090 (Document summaries and descriptive names); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-030",
      "area": "Format",
      "title": "Attributes and change markings",
      "requirement_refs": [
        "FR-005",
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 36,
          "printed_end": 40,
          "pdf_start": 53,
          "pdf_end": 57
        },
        {
          "printed_start": 549,
          "printed_end": 549,
          "pdf_start": 566,
          "pdf_end": 566
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-032",
        "CMD51-090",
        "CMD51-091",
        "CMD51-092"
      ],
      "oracle_counts": {
        "not-run": 4
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Apply/remove attributes and redline/strikeout; inspect paired codes and print results.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-030 (Attributes and change markings); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-031",
      "area": "Format",
      "title": "Fonts and kerning",
      "requirement_refs": [
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 205,
          "printed_end": 208,
          "pdf_start": 222,
          "pdf_end": 225
        },
        {
          "printed_start": 303,
          "printed_end": 303,
          "pdf_start": 320,
          "pdf_end": 320
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-160",
        "CMD51-161"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare font changes, sizes, printer substitutions and kerning with fixed resources.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-031 (Fonts and kerning); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-032",
      "area": "Format",
      "title": "Initial document and application codes",
      "requirement_refs": [
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 143,
          "printed_end": 144,
          "pdf_start": 160,
          "pdf_end": 161
        },
        {
          "printed_start": 292,
          "printed_end": 298,
          "pdf_start": 309,
          "pdf_end": 315
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-093"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Distinguish default settings from document initial codes and saved state.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-032 (Initial document and application codes); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-033",
      "area": "Format",
      "title": "Margins and format menus",
      "requirement_refs": [
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 218,
          "printed_end": 220,
          "pdf_start": 235,
          "pdf_end": 237
        },
        {
          "printed_start": 339,
          "printed_end": 340,
          "pdf_start": 356,
          "pdf_end": 357
        },
        {
          "printed_start": 394,
          "printed_end": 396,
          "pdf_start": 411,
          "pdf_end": 413
        },
        {
          "printed_start": 473,
          "printed_end": 473,
          "pdf_start": 490,
          "pdf_end": 490
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-162",
        "CMD51-163"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP14",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-162",
            "CMD51-163"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Change line/page/document defaults and verify their code scope.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-033 (Margins and format menus); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-034",
      "area": "Format",
      "title": "Alignment, centering and indents",
      "requirement_refs": [
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 63,
          "printed_end": 67,
          "pdf_start": 80,
          "pdf_end": 84
        },
        {
          "printed_start": 203,
          "printed_end": 204,
          "pdf_start": 220,
          "pdf_end": 221
        },
        {
          "printed_start": 285,
          "printed_end": 286,
          "pdf_start": 302,
          "pdf_end": 303
        },
        {
          "printed_start": 299,
          "printed_end": 302,
          "pdf_start": 316,
          "pdf_end": 319
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-094",
        "CMD51-095",
        "CMD51-096",
        "CMD51-097",
        "CMD51-098",
        "CMD51-099",
        "CMD51-100"
      ],
      "oracle_counts": {
        "not-run": 7
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare centered/right-aligned/justified text and indents across reflow.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-034 (Alignment, centering and indents); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-035",
      "area": "Format",
      "title": "Tabs and tab alignment",
      "requirement_refs": [
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 631,
          "printed_end": 639,
          "pdf_start": 648,
          "pdf_end": 656
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-101",
        "CMD51-102",
        "CMD51-103"
      ],
      "oracle_counts": {
        "not-run": 3
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP14",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-101",
            "CMD51-103"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Set tab types, alignment and leaders; verify native codes and layout.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-035 (Tabs and tab alignment); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-036",
      "area": "Format",
      "title": "Line height, spacing and numbering",
      "requirement_refs": [
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 341,
          "printed_end": 346,
          "pdf_start": 358,
          "pdf_end": 363
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-104",
        "CMD51-105",
        "CMD51-106"
      ],
      "oracle_counts": {
        "not-run": 3
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Combine proportional fonts, line height, spacing and line numbers.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-036 (Line height, spacing and numbering); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-037",
      "area": "Format",
      "title": "Word/letter spacing and measurement units",
      "requirement_refs": [
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 698,
          "printed_end": 700,
          "pdf_start": 715,
          "pdf_end": 717
        },
        {
          "printed_start": 708,
          "printed_end": 711,
          "pdf_start": 725,
          "pdf_end": 728
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-164"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Check unit conversion and spacing without cumulative layout drift.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-037 (Word/letter spacing and measurement units); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-038",
      "area": "Format",
      "title": "Precise positioning and advance",
      "requirement_refs": [
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 31,
          "printed_end": 34,
          "pdf_start": 48,
          "pdf_end": 51
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-107",
        "CMD51-108"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare absolute/relative advances, page limits and text-box origins.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-038 (Precise positioning and advance); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-039",
      "area": "Format",
      "title": "Hyphenation and zones",
      "requirement_refs": [
        "FR-008"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 277,
          "printed_end": 284,
          "pdf_start": 294,
          "pdf_end": 301
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-109"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare word breaking, zones, manual decisions and saved codes.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-039 (Hyphenation and zones); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-040",
      "area": "Pagination",
      "title": "Hard/soft pages and conditional breaks",
      "requirement_refs": [
        "FR-009"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 88,
          "printed_end": 88,
          "pdf_start": 105,
          "pdf_end": 105
        },
        {
          "printed_start": 217,
          "printed_end": 217,
          "pdf_start": 234,
          "pdf_end": 234
        },
        {
          "printed_start": 471,
          "printed_end": 473,
          "pdf_start": 488,
          "pdf_end": 490
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-112",
        "CMD51-113"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP14",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-112"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Reflow through hard, soft, conditional and odd/even page transitions.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-040 (Hard/soft pages and conditional breaks); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-041",
      "area": "Pagination",
      "title": "Page numbering and paper definitions",
      "requirement_refs": [
        "FR-009"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 474,
          "printed_end": 486,
          "pdf_start": 491,
          "pdf_end": 503
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-165",
        "CMD51-166"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP14",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-165"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Use paper definitions and page numbering across format changes.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-041 (Page numbering and paper definitions); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-042",
      "area": "Pagination",
      "title": "Keep-together and widow/orphan rules",
      "requirement_refs": [
        "FR-009"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 51,
          "printed_end": 54,
          "pdf_start": 68,
          "pdf_end": 71
        },
        {
          "printed_start": 705,
          "printed_end": 705,
          "pdf_start": 722,
          "pdf_end": 722
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-167"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Force borderline pagination and compare page membership.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-042 (Keep-together and widow/orphan rules); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-043",
      "area": "Pagination",
      "title": "Columns and screen column presentation",
      "requirement_refs": [
        "FR-009"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 74,
          "printed_end": 83,
          "pdf_start": 91,
          "pdf_end": 100
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-168",
        "CMD51-169"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare newspaper and parallel columns, breaks, balancing and display.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-043 (Columns and screen column presentation); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-044",
      "area": "Pagination",
      "title": "Headers, footers and suppression",
      "requirement_refs": [
        "FR-009"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 269,
          "printed_end": 274,
          "pdf_start": 286,
          "pdf_end": 291
        },
        {
          "printed_start": 626,
          "printed_end": 627,
          "pdf_start": 643,
          "pdf_end": 644
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-170"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Create header/footer variants; compare suppression and page-dependent placement.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-044 (Headers, footers and suppression); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-045",
      "area": "Pagination",
      "title": "Footnotes and endnotes",
      "requirement_refs": [
        "FR-009"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 209,
          "printed_end": 216,
          "pdf_start": 226,
          "pdf_end": 233
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-115",
        "CMD51-116",
        "CMD51-117"
      ],
      "oracle_counts": {
        "not-run": 3
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Test nested text, numbering, continuation and pagination.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-045 (Footnotes and endnotes); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-091",
      "area": "Pagination",
      "title": "Binding offsets and logical page parity",
      "requirement_refs": [
        "FR-009"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 46,
          "printed_end": 48,
          "pdf_start": 63,
          "pdf_end": 65
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-114"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare odd/even logical page offsets, labels and top-binding behavior.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-091 (Binding offsets and logical page parity); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-046",
      "area": "Structure",
      "title": "Styles and definitions",
      "requirement_refs": [
        "FR-010"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 616,
          "printed_end": 625,
          "pdf_start": 633,
          "pdf_end": 642
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-118",
        "CMD51-119"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Create and apply styles, edit definitions and compare resulting code scope.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-046 (Styles and definitions); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-047",
      "area": "Structure",
      "title": "Outlines and numbering",
      "requirement_refs": [
        "FR-010"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 449,
          "printed_end": 468,
          "pdf_start": 466,
          "pdf_end": 485
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-171"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Create, redefine, promote/demote and restyle outline levels.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-047 (Outlines and numbering); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-048",
      "area": "Structure",
      "title": "Tables and structural editing",
      "requirement_refs": [
        "FR-010"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 640,
          "printed_end": 664,
          "pdf_start": 657,
          "pdf_end": 681
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-120",
        "CMD51-121"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Create tables; edit rows, columns, joins and splits; preserve native structure.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-048 (Tables and structural editing); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-049",
      "area": "Structure",
      "title": "Table formatting and calculations",
      "requirement_refs": [
        "FR-010"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 665,
          "printed_end": 675,
          "pdf_start": 682,
          "pdf_end": 692
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-122",
        "CMD51-123"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare cell/column formatting, formulas and recalculation.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-049 (Table formatting and calculations); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-050",
      "area": "Structure",
      "title": "Generated contents, lists and index",
      "requirement_refs": [
        "FR-010"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 221,
          "printed_end": 223,
          "pdf_start": 238,
          "pdf_end": 240
        },
        {
          "printed_start": 287,
          "printed_end": 291,
          "pdf_start": 304,
          "pdf_end": 308
        },
        {
          "printed_start": 355,
          "printed_end": 357,
          "pdf_start": 372,
          "pdf_end": 374
        },
        {
          "printed_start": 682,
          "printed_end": 685,
          "pdf_start": 699,
          "pdf_end": 702
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-124",
        "CMD51-125"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Mark text, define and regenerate indexes/lists/contents; verify page references.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-050 (Generated contents, lists and index); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-051",
      "area": "Structure",
      "title": "Table of authorities",
      "requirement_refs": [
        "FR-010"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 676,
          "printed_end": 681,
          "pdf_start": 693,
          "pdf_end": 698
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-172"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Mark citations, define categories and regenerate with original ordering.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-051 (Table of authorities); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-052",
      "area": "Structure",
      "title": "Master documents and subdocuments",
      "requirement_refs": [
        "FR-010"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 397,
          "printed_end": 400,
          "pdf_start": 414,
          "pdf_end": 417
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-126"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Expand/condense subdocuments and regenerate references across them.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-052 (Master documents and subdocuments); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-053",
      "area": "Structure",
      "title": "Labels and envelopes",
      "requirement_refs": [
        "FR-010"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 319,
          "printed_end": 327,
          "pdf_start": 336,
          "pdf_end": 344
        },
        {
          "printed_start": 771,
          "printed_end": 772,
          "pdf_start": 788,
          "pdf_end": 789
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-173"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare definitions, repeated labels and envelope placement with fixed printer settings.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-053 (Labels and envelopes); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-054",
      "area": "Structure",
      "title": "Date values and codes",
      "requirement_refs": [
        "FR-010"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 109,
          "printed_end": 112,
          "pdf_start": 126,
          "pdf_end": 129
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-127",
        "CMD51-128"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare inserted values and generated dates under fixed clock and language settings.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-054 (Date values and codes); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-089",
      "area": "Structure",
      "title": "Cross-reference targets and generated references",
      "requirement_refs": [
        "FR-010"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 96,
          "printed_end": 103,
          "pdf_start": 113,
          "pdf_end": 120
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-129",
        "CMD51-130"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Mark references and named targets separately and together; regenerate after pagination changes.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-089 (Cross-reference targets and generated references); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-055",
      "area": "Graphics",
      "title": "Graphics boxes, wrapping and captions",
      "requirement_refs": [
        "FR-011"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 232,
          "printed_end": 250,
          "pdf_start": 249,
          "pdf_end": 267
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-174"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Create/edit boxes and anchored objects; verify wrapping, sizing and captions.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-055 (Graphics boxes, wrapping and captions); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-056",
      "area": "Graphics",
      "title": "Graphics formats and conversion utility",
      "requirement_refs": [
        "FR-011"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 228,
          "printed_end": 231,
          "pdf_start": 245,
          "pdf_end": 248
        },
        {
          "printed_start": 251,
          "printed_end": 256,
          "pdf_start": 268,
          "pdf_end": 273
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-175"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-175"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Reproduce original import/conversion behavior and preserve embedded/linked resources.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-056 (Graphics formats and conversion utility); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-057",
      "area": "Graphics",
      "title": "Graphic rules and display options",
      "requirement_refs": [
        "FR-011"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 257,
          "printed_end": 268,
          "pdf_start": 274,
          "pdf_end": 285
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-176"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare rules, boxes, display settings and printed placement.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-057 (Graphic rules and display options); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-058",
      "area": "Graphics",
      "title": "Equations and equation editor",
      "requirement_refs": [
        "FR-011"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 163,
          "printed_end": 193,
          "pdf_start": 180,
          "pdf_end": 210
        },
        {
          "printed_start": 729,
          "printed_end": 740,
          "pdf_start": 746,
          "pdf_end": 757
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-177"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Edit equation expressions and compare native representation and rendering.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-058 (Equations and equation editor); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-059",
      "area": "Automation",
      "title": "Macro definition, execution and editor",
      "requirement_refs": [
        "FR-012"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 369,
          "printed_end": 393,
          "pdf_start": 386,
          "pdf_end": 410
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-131",
        "CMD51-132",
        "CMD51-133",
        "CMD51-205",
        "CMD51-206",
        "CMD51-210",
        "CMD51-212",
        "CMD51-213",
        "CMD51-214",
        "CMD51-215",
        "CMD51-218",
        "CMD51-219",
        "CMD51-220",
        "CMD51-221",
        "CMD51-222",
        "CMD51-226",
        "CMD51-227",
        "CMD51-228",
        "CMD51-229",
        "CMD51-230"
      ],
      "oracle_counts": {
        "partially-observed": 19,
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Record, edit and execute original macros; compare prompts, keys and errors.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-059 (Macro definition, execution and editor); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-060",
      "area": "Automation",
      "title": "Macro language, expressions and variables",
      "requirement_refs": [
        "FR-012"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 777,
          "printed_end": 892,
          "pdf_start": 794,
          "pdf_end": 909
        },
        {
          "printed_start": 963,
          "printed_end": 986,
          "pdf_start": 980,
          "pdf_end": 1003
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-178",
        "CMD51-205",
        "CMD51-206",
        "CMD51-210",
        "CMD51-212",
        "CMD51-213",
        "CMD51-214",
        "CMD51-215",
        "CMD51-218",
        "CMD51-219",
        "CMD51-220",
        "CMD51-221",
        "CMD51-222",
        "CMD51-226",
        "CMD51-227",
        "CMD51-228",
        "CMD51-229",
        "CMD51-230"
      ],
      "oracle_counts": {
        "partially-observed": 18
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Catalogue and test each command, expression, variable and value-table behavior.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-060 (Macro language, expressions and variables); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-061",
      "area": "Automation",
      "title": "Original macro conversion utility",
      "requirement_refs": [
        "FR-012"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 370,
          "printed_end": 372,
          "pdf_start": 387,
          "pdf_end": 389
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-179"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Compare supported original conversions and unsupported-input handling.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-061 (Original macro conversion utility); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-062",
      "area": "Automation",
      "title": "Merge documents, data and commands",
      "requirement_refs": [
        "FR-012"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 418,
          "printed_end": 433,
          "pdf_start": 435,
          "pdf_end": 450
        },
        {
          "printed_start": 777,
          "printed_end": 892,
          "pdf_start": 794,
          "pdf_end": 909
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-134",
        "CMD51-207",
        "CMD51-208",
        "CMD51-209",
        "CMD51-216",
        "CMD51-217",
        "CMD51-223",
        "CMD51-224",
        "CMD51-225",
        "CMD51-231",
        "CMD51-232",
        "CMD51-233",
        "CMD51-234",
        "CMD51-235",
        "CMD51-236"
      ],
      "oracle_counts": {
        "partially-observed": 15
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Run simple and conditional merges using original file formats and command semantics.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-062 (Merge documents, data and commands); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-063",
      "area": "Automation",
      "title": "Sorting and record selection",
      "requirement_refs": [
        "FR-013"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 577,
          "printed_end": 586,
          "pdf_start": 594,
          "pdf_end": 603
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-135"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Compare keys, ordering, selected records and preservation of fields/codes.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-063 (Sorting and record selection); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-064",
      "area": "Automation",
      "title": "Column math and calculations",
      "requirement_refs": [
        "FR-013"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 401,
          "printed_end": 414,
          "pdf_start": 418,
          "pdf_end": 431
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-180"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Define columns and functions; compare arithmetic results and formatting.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-064 (Column math and calculations); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-065",
      "area": "Automation",
      "title": "Spreadsheet import and links",
      "requirement_refs": [
        "FR-013"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 606,
          "printed_end": 615,
          "pdf_start": 623,
          "pdf_end": 632
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-136",
        "CMD51-137"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-136",
            "CMD51-137"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Import supported worksheets; update links and compare data/format refresh behavior.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-065 (Spreadsheet import and links); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-066",
      "area": "Language",
      "title": "WP characters and compose",
      "requirement_refs": [
        "FR-014"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 84,
          "printed_end": 87,
          "pdf_start": 101,
          "pdf_end": 104
        },
        {
          "printed_start": 913,
          "printed_end": 920,
          "pdf_start": 930,
          "pdf_end": 937
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-138"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        },
        {
          "wp": "WP22",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-138"
          ]
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Input original character-set identities and round-trip every supported mapping.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-066 (WP characters and compose); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-067",
      "area": "Language",
      "title": "Language selection and resources",
      "requirement_refs": [
        "FR-014"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 328,
          "printed_end": 336,
          "pdf_start": 345,
          "pdf_end": 353
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-181"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-181"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Switch language-dependent formatting and resources; record edition applicability.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-067 (Language selection and resources); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-068",
      "area": "Language",
      "title": "Spelling, dictionaries, lookup and counts",
      "requirement_refs": [
        "FR-014"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 587,
          "printed_end": 605,
          "pdf_start": 604,
          "pdf_end": 622
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-139",
        "CMD51-140",
        "CMD51-141"
      ],
      "oracle_counts": {
        "not-run": 3
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Check corrections, dictionaries, lookup, counts and original utility behavior.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-068 (Spelling, dictionaries, lookup and counts); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-069",
      "area": "Language",
      "title": "Thesaurus",
      "requirement_refs": [
        "FR-014"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 692,
          "printed_end": 694,
          "pdf_start": 709,
          "pdf_end": 711
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-182"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare lookup, replacement and return-to-editor workflow using declared resources.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-069 (Thesaurus); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-070",
      "area": "Print",
      "title": "Print selection, options and quality",
      "requirement_refs": [
        "FR-015"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 487,
          "printed_end": 503,
          "pdf_start": 504,
          "pdf_end": 520
        },
        {
          "printed_start": 533,
          "printed_end": 542,
          "pdf_start": 550,
          "pdf_end": 559
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-183",
        "CMD51-184"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Print documents, pages and blocks; compare copies, quality, ordering and stopping.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-070 (Print selection, options and quality); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-071",
      "area": "Print",
      "title": "Printer selection and editing",
      "requirement_refs": [
        "FR-015"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 504,
          "printed_end": 509,
          "pdf_start": 521,
          "pdf_end": 526
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-185"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-185"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Select/edit original printer settings; preserve resource references and metrics.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-071 (Printer selection and editing); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-072",
      "area": "Print",
      "title": "Printer commands and functions",
      "requirement_refs": [
        "FR-015"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 510,
          "printed_end": 517,
          "pdf_start": 527,
          "pdf_end": 534
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-186"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Exercise direct commands and layout-affecting printer controls.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-072 (Printer commands and functions); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-073",
      "area": "Print",
      "title": "Printer-definition utility and fonts",
      "requirement_refs": [
        "FR-015"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 518,
          "printed_end": 532,
          "pdf_start": 535,
          "pdf_end": 549
        },
        {
          "printed_start": 763,
          "printed_end": 764,
          "pdf_start": 780,
          "pdf_end": 781
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-187"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Inventory resource-editing and substitution behavior; define Linux equivalent explicitly.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-073 (Printer-definition utility and fonts); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-074",
      "area": "Print",
      "title": "Printing to disk",
      "requirement_refs": [
        "FR-015"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 543,
          "printed_end": 543,
          "pdf_start": 560,
          "pdf_end": 560
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-145"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP14",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-145"
          ]
        },
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare original printer-language output bytes with matching resources.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-074 (Printing to disk); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-075",
      "area": "Print",
      "title": "Print jobs and delivery",
      "requirement_refs": [
        "FR-015"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 495,
          "printed_end": 500,
          "pdf_start": 512,
          "pdf_end": 517
        },
        {
          "printed_start": 576,
          "printed_end": 576,
          "pdf_start": 593,
          "pdf_end": 593
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-148"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Inspect, cancel and prioritize jobs; map delivery to Linux without changing print data.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-075 (Print jobs and delivery); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-076",
      "area": "Print",
      "title": "Document preview and options",
      "requirement_refs": [
        "FR-016"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 701,
          "printed_end": 704,
          "pdf_start": 718,
          "pdf_end": 721
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-146",
        "CMD51-147"
      ],
      "oracle_counts": {
        "not-run": 2
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-146",
            "CMD51-147"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "resource-or-field-contract"
      ],
      "remaining_obligation": "Compare page view and facing pages using declared printer metrics.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-076 (Document preview and options); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-077",
      "area": "Platform",
      "title": "Setup, environment and sound",
      "requirement_refs": [
        "FR-017"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 45,
          "printed_end": 47,
          "pdf_start": 62,
          "pdf_end": 64
        },
        {
          "printed_start": 122,
          "printed_end": 123,
          "pdf_start": 139,
          "pdf_end": 140
        },
        {
          "printed_start": 159,
          "printed_end": 162,
          "pdf_start": 176,
          "pdf_end": 179
        },
        {
          "printed_start": 574,
          "printed_end": 575,
          "pdf_start": 591,
          "pdf_end": 592
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-188"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "platform-mapping",
        "owner-decision-if-scope-change"
      ],
      "remaining_obligation": "Persist original settings and document Linux adaptations.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-077 (Setup, environment and sound); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-078",
      "area": "Platform",
      "title": "DOS and shell integration",
      "requirement_refs": [
        "FR-017"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 150,
          "printed_end": 156,
          "pdf_start": 167,
          "pdf_end": 173
        },
        {
          "printed_start": 225,
          "printed_end": 227,
          "pdf_start": 242,
          "pdf_end": 244
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-189"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "platform-mapping",
        "owner-decision-if-scope-change"
      ],
      "remaining_obligation": "Inventory external-process workflows and define explicit Linux mappings.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-078 (DOS and shell integration); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-079",
      "area": "Platform",
      "title": "Bundled conversion, cursor and capture utilities",
      "requirement_refs": [
        "FR-017"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 89,
          "printed_end": 95,
          "pdf_start": 106,
          "pdf_end": 112
        },
        {
          "printed_start": 105,
          "printed_end": 108,
          "pdf_start": 122,
          "pdf_end": 125
        },
        {
          "printed_start": 567,
          "printed_end": 570,
          "pdf_start": 584,
          "pdf_end": 587
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-190"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "platform-mapping",
        "owner-decision-if-scope-change"
      ],
      "remaining_obligation": "Study utility boundaries and original artifact behavior before choosing Linux implementation.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-079 (Bundled conversion, cursor and capture utilities); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-080",
      "area": "Platform",
      "title": "Memory and startup controls",
      "requirement_refs": [
        "FR-017"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 415,
          "printed_end": 417,
          "pdf_start": 432,
          "pdf_end": 434
        },
        {
          "printed_start": 897,
          "printed_end": 904,
          "pdf_start": 914,
          "pdf_end": 921
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-191"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "platform-mapping",
        "owner-decision-if-scope-change"
      ],
      "remaining_obligation": "Classify original startup and memory controls; record hardware-only adaptations.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-080 (Memory and startup controls); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-081",
      "area": "Platform",
      "title": "Network and original resource files",
      "requirement_refs": [
        "FR-017"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 921,
          "printed_end": 960,
          "pdf_start": 938,
          "pdf_end": 977
        }
      ],
      "documentary_status": "indexed",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-192"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "platform-mapping",
        "owner-decision-if-scope-change"
      ],
      "remaining_obligation": "Inventory shared-file behavior, locking, resource discovery and companion formats.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-081 (Network and original resource files); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "WP51-082",
      "area": "Platform",
      "title": "Code tables, defaults, keyboards and errors",
      "requirement_refs": [
        "FR-017"
      ],
      "source_id": "REF51",
      "locators": [
        {
          "printed_start": 715,
          "printed_end": 728,
          "pdf_start": 732,
          "pdf_end": 745
        },
        {
          "printed_start": 741,
          "printed_end": 762,
          "pdf_start": 758,
          "pdf_end": 779
        },
        {
          "printed_start": 765,
          "printed_end": 776,
          "pdf_start": 782,
          "pdf_end": 793
        },
        {
          "printed_start": 893,
          "printed_end": 896,
          "pdf_start": 910,
          "pdf_end": 913
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-193"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP20",
          "scope": "resource/format readiness only",
          "case_ids": []
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification",
        "platform-mapping",
        "owner-decision-if-scope-change"
      ],
      "remaining_obligation": "Reconcile appendices against feature coverage and negative scenarios.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for WP51-082 (Code tables, defaults, keyboards and errors); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "FMT51-001",
      "area": "Native formats",
      "title": "File prefix and document pointer",
      "requirement_refs": [
        "FR-002"
      ],
      "source_id": "SDK51",
      "locators": [
        {
          "printed_start": 3,
          "printed_end": 6,
          "pdf_start": 16,
          "pdf_end": 19
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-194"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [
        "COMP-WP02"
      ],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Check identifiers, versions, byte order, encryption marker and document pointer against original files.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for FMT51-001 (File prefix and document pointer); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "FMT51-002",
      "area": "Native formats",
      "title": "Prefix index chains and packets",
      "requirement_refs": [
        "FR-002"
      ],
      "source_id": "SDK51",
      "locators": [
        {
          "printed_start": 7,
          "printed_end": 16,
          "pdf_start": 20,
          "pdf_end": 29
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-195"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [
        "COMP-WP02"
      ],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Preserve packet bytes and references while testing bounds, cycles and relocations.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for FMT51-002 (Prefix index chains and packets); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "FMT51-003",
      "area": "Native formats",
      "title": "Document code framing and nested text",
      "requirement_refs": [
        "FR-002"
      ],
      "source_id": "SDK51",
      "locators": [
        {
          "printed_start": 17,
          "printed_end": 18,
          "pdf_start": 30,
          "pdf_end": 31
        }
      ],
      "documentary_status": "studied",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-196"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [
        "COMP-WP02"
      ],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Validate fixed/variable frames, nested codes and unknown-code preservation.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for FMT51-003 (Document code framing and nested text); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "FMT51-004",
      "area": "Native formats",
      "title": "Original character and function encoding",
      "requirement_refs": [
        "FR-002"
      ],
      "source_id": "SDK51",
      "locators": [
        {
          "printed_start": 19,
          "printed_end": 35,
          "pdf_start": 32,
          "pdf_end": 48
        }
      ],
      "documentary_status": "indexed",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-197"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [
        "COMP-WP02"
      ],
      "queued_starters": [
        {
          "wp": "WP14",
          "scope": "bounded case/subcase starter only",
          "case_ids": [
            "CMD51-197"
          ]
        },
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Check every defined code class against fixtures, including hard/soft boundary codes.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for FMT51-004 (Original character and function encoding); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "FMT51-005",
      "area": "Native formats",
      "title": "Formatting, structure and automation code groups",
      "requirement_refs": [
        "FR-002"
      ],
      "source_id": "SDK51",
      "locators": [
        {
          "printed_start": 36,
          "printed_end": 91,
          "pdf_start": 49,
          "pdf_end": 104
        }
      ],
      "documentary_status": "indexed",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-198"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [
        "COMP-WP02"
      ],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Map every WP code group to semantic behavior and round-trip fixtures.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for FMT51-005 (Formatting, structure and automation code groups); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    },
    {
      "id": "FMT51-006",
      "area": "Native formats",
      "title": "Native WPM macro serialization",
      "requirement_refs": [
        "FR-003",
        "FR-012"
      ],
      "source_id": "SDK51",
      "locators": [
        {
          "printed_start": 92,
          "printed_end": 99,
          "pdf_start": 105,
          "pdf_end": 112
        }
      ],
      "documentary_status": "indexed",
      "canonical_implementation": "not-started",
      "canonical_oracle": "pending",
      "case_ids": [
        "CMD51-199"
      ],
      "oracle_counts": {
        "not-run": 1
      },
      "component_evidence": [],
      "queued_starters": [
        {
          "wp": "WP21",
          "scope": "documentary leaf reconciliation only",
          "case_ids": []
        }
      ],
      "remaining_gap_kinds": [
        "implementation",
        "original-verification"
      ],
      "remaining_obligation": "Read/write macro headers and command encodings with original interpreter evidence.",
      "full_group_implementation_queued": false,
      "uncovered_subtasks_visible": true,
      "next_unqueued_action": "Author independently reviewable remaining native/command/resource/failure and original comparison slices for FMT51-006 (Native WPM macro serialization); expand compound group/command leaves before full closure.",
      "responsible_role": "future planner after reviewed evidence; implementer and independent reviewer",
      "closed": false
    }
  ],
  "reference_resource_locale_format_owner_gaps": [
    {
      "id": "R01",
      "kind": "resource",
      "gap": "Licensed historical DOS media and fresh fingerprinted profile missing; FreeDOS1.4 is not historical corroboration.",
      "next_wp": "WP20",
      "owner": "researcher/resource custodian",
      "scope_cut": false
    },
    {
      "id": "R02",
      "kind": "resource",
      "gap": "Graphics-capable original printer definition, fonts/metrics and preview profile absent; current Standard Printer is text-only/mixed date. Need L5\u2013L7 and original language stream.",
      "next_wp": "WP20",
      "owner": "researcher/resource custodian",
      "scope_cut": false
    },
    {
      "id": "R03",
      "kind": "locale",
      "gap": "US baseline does not discharge Greek/Russian/Hebrew/other original character/language/font/resource obligations. LRS/LEX/SUP/HYC/THS/SET each needs licensed inputs and independent codec/probe.",
      "next_wp": "WP20",
      "owner": "researcher/resource custodian",
      "scope_cut": false
    },
    {
      "id": "R04",
      "kind": "format",
      "gap": "WPG DR byte-order prose conflicts with low/high diagram; nonzero packet8 count needs full checked size array/image extents, not index length2. Unknown variants remain refused.",
      "next_wp": "WP20",
      "owner": "format researcher",
      "scope_cut": false
    },
    {
      "id": "R05",
      "kind": "conflicting-field",
      "gap": "DOS Link End ending-row short at13 overlaps filename start14; original native fixture must resolve boundary. WPWin DDE is separate and not a DOS shortcut.",
      "next_wp": "WP20",
      "owner": "format researcher",
      "scope_cut": false
    },
    {
      "id": "R06",
      "kind": "format",
      "gap": "Table formula relative row positive=up/negative=down, columns positive=right/negative=left; test nonzero directions and older/newer border encodings. Style/outline name/ID relationships remain undecoded.",
      "next_wp": "WP20",
      "owner": "format researcher",
      "scope_cut": false
    },
    {
      "id": "R07",
      "kind": "format-resource",
      "gap": "Original PlanPerfect/Lotus/Excel2x\u20133.0/Quattro/Symphony worksheet producers/specifications, legacy4.2/5.0/.CRS, 4.x macro and graphics converter inputs needed; modern CSV/xlsx is no substitute.",
      "next_wp": "WP20",
      "owner": "researcher/resource custodian",
      "scope_cut": false
    },
    {
      "id": "R08",
      "kind": "owner-decision-if-scope-change",
      "gap": "Terminal desktop-intercepted original chords and ambiguous legacy bytes require actual profile qualification. Remapping or excluding original commands requires explicit owner decision; no such change is selected.",
      "next_wp": "WP16",
      "owner": "terminal researcher then owner if scope change proposed",
      "scope_cut": false
    },
    {
      "id": "R09",
      "kind": "owner-decision-if-scope-change",
      "gap": "DOS/PIF/shell/startup/cursor/capture/network/platform applicability requires explicit tested Linux mapping. POSIX local safety is not original locking. Exclusion or baseline change requires owner decision; none exists.",
      "next_wp": "WP21",
      "owner": "platform researcher then owner if scope change proposed",
      "scope_cut": false
    },
    {
      "id": "R10",
      "kind": "measurement",
      "gap": "No accepted Linux product latency/size target exists; parser three-iteration benchmark/fuzz RSS is component evidence only. Measure actual session distributions, peak RSS/binary size before proposing budgets.",
      "next_wp": "WP19",
      "owner": "implementer then independent reviewer",
      "scope_cut": false
    }
  ],
  "queued_packages": [
    {
      "id": "WP13",
      "prompt": "kitty-specs/wp51-parity-01M64CVY/tasks/WP13-original-session-probes.md",
      "dependencies": [
        "WP03",
        "WP04",
        "WP06",
        "WP11",
        "WP12"
      ],
      "execution_mode": "code_change",
      "requirement_refs": [
        "FR-004",
        "FR-005",
        "FR-006",
        "NFR-004",
        "C-005",
        "C-006"
      ],
      "compatibility_refs": [],
      "subtasks": [
        "T037",
        "T038",
        "T039"
      ],
      "owned_files": [
        "scripts/reference/session1.py",
        "docs/research/continuation/session1/",
        "docs/research/command-scenarios.json",
        "docs/research/command-scenarios.md",
        "docs/research/scenario-coverage.md",
        "docs/research/workbook-map.md",
        "docs/research/feature-inventory.json",
        "docs/research/feature-inventory.md"
      ]
    },
    {
      "id": "WP14",
      "prompt": "kitty-specs/wp51-parity-01M64CVY/tasks/WP14-text-layout-probes.md",
      "dependencies": [
        "WP07",
        "WP12"
      ],
      "execution_mode": "code_change",
      "requirement_refs": [
        "FR-008",
        "FR-009",
        "FR-015",
        "NFR-004",
        "NFR-005",
        "C-005"
      ],
      "compatibility_refs": [
        "FC-008"
      ],
      "subtasks": [
        "T040",
        "T041",
        "T042"
      ],
      "owned_files": [
        "scripts/reference/text_layout.py",
        "docs/research/continuation/text-layout/"
      ]
    },
    {
      "id": "WP15",
      "prompt": "kitty-specs/wp51-parity-01M64CVY/tasks/WP15-readonly-document.md",
      "dependencies": [
        "WP02",
        "WP04",
        "WP10",
        "WP12"
      ],
      "execution_mode": "code_change",
      "requirement_refs": [
        "FR-002",
        "FR-004",
        "FR-005",
        "NFR-001",
        "NFR-003",
        "C-001"
      ],
      "compatibility_refs": [
        "FC-002",
        "FC-004"
      ],
      "subtasks": [
        "T043",
        "T044",
        "T045"
      ],
      "owned_files": [
        "internal/document/"
      ]
    },
    {
      "id": "WP16",
      "prompt": "kitty-specs/wp51-parity-01M64CVY/tasks/WP16-typed-input.md",
      "dependencies": [
        "WP11",
        "WP12"
      ],
      "execution_mode": "code_change",
      "requirement_refs": [
        "FR-004",
        "FR-017",
        "C-001",
        "C-006",
        "NFR-004"
      ],
      "compatibility_refs": [],
      "subtasks": [
        "T046",
        "T047",
        "T048"
      ],
      "owned_files": [
        "internal/input/",
        "cmd/wordling-input-probe/",
        "docs/research/continuation/terminal-input/"
      ]
    },
    {
      "id": "WP17",
      "prompt": "kitty-specs/wp51-parity-01M64CVY/tasks/WP17-bounded-session.md",
      "dependencies": [
        "WP03",
        "WP11",
        "WP12",
        "WP13",
        "WP15"
      ],
      "execution_mode": "code_change",
      "requirement_refs": [
        "FR-004",
        "FR-005",
        "FR-006",
        "NFR-001",
        "NFR-002",
        "C-001"
      ],
      "compatibility_refs": [
        "FC-002",
        "FC-004",
        "FC-009"
      ],
      "subtasks": [
        "T049",
        "T050",
        "T051"
      ],
      "owned_files": [
        "internal/editor/"
      ]
    },
    {
      "id": "WP18",
      "prompt": "kitty-specs/wp51-parity-01M64CVY/tasks/WP18-bubbletea-session.md",
      "dependencies": [
        "WP03",
        "WP15",
        "WP16",
        "WP17"
      ],
      "execution_mode": "code_change",
      "requirement_refs": [
        "FR-002",
        "FR-004",
        "FR-005",
        "FR-006",
        "C-001",
        "C-002",
        "NFR-001",
        "NFR-002"
      ],
      "compatibility_refs": [
        "FC-002",
        "FC-004",
        "FC-009"
      ],
      "subtasks": [
        "T052",
        "T053",
        "T054"
      ],
      "owned_files": [
        "internal/tui/",
        "cmd/wordling/",
        "docs/research/continuation/composed-session/"
      ]
    },
    {
      "id": "WP19",
      "prompt": "kitty-specs/wp51-parity-01M64CVY/tasks/WP19-linux-measurements.md",
      "dependencies": [
        "WP14",
        "WP18"
      ],
      "execution_mode": "code_change",
      "requirement_refs": [
        "C-001",
        "NFR-003",
        "NFR-004"
      ],
      "compatibility_refs": [],
      "subtasks": [
        "T055",
        "T056",
        "T057"
      ],
      "owned_files": [
        "tests/performance/",
        "docs/research/continuation/linux-measurements/"
      ]
    },
    {
      "id": "WP20",
      "prompt": "kitty-specs/wp51-parity-01M64CVY/tasks/WP20-resource-readiness.md",
      "dependencies": [
        "WP07",
        "WP08",
        "WP10",
        "WP12"
      ],
      "execution_mode": "planning_artifact",
      "requirement_refs": [
        "FR-011",
        "FR-014",
        "FR-015",
        "FR-016",
        "FR-017",
        "NFR-005",
        "C-004",
        "C-005",
        "C-006"
      ],
      "compatibility_refs": [],
      "subtasks": [
        "T058",
        "T059",
        "T060"
      ],
      "owned_files": [
        "kitty-specs/wp51-parity-01M64CVY/contracts/resource-readiness.md"
      ]
    },
    {
      "id": "WP21",
      "prompt": "kitty-specs/wp51-parity-01M64CVY/tasks/WP21-coverage-leaves.md",
      "dependencies": [
        "WP05",
        "WP12"
      ],
      "execution_mode": "planning_artifact",
      "requirement_refs": [
        "FR-001",
        "NFR-004",
        "C-003",
        "C-005",
        "C-006"
      ],
      "compatibility_refs": [],
      "subtasks": [
        "T061",
        "T062",
        "T063"
      ],
      "owned_files": [
        "kitty-specs/wp51-parity-01M64CVY/contracts/coverage-leaves.md"
      ]
    },
    {
      "id": "WP22",
      "prompt": "kitty-specs/wp51-parity-01M64CVY/tasks/WP22-character-probes.md",
      "dependencies": [
        "WP10",
        "WP12"
      ],
      "execution_mode": "code_change",
      "requirement_refs": [
        "FR-014",
        "NFR-004",
        "C-004",
        "C-005"
      ],
      "compatibility_refs": [
        "FC-006"
      ],
      "subtasks": [
        "T064",
        "T065",
        "T066"
      ],
      "owned_files": [
        "scripts/reference/character_identity.py",
        "docs/research/continuation/character-identity/"
      ]
    }
  ],
  "acceptance_barriers": [
    "Complete every remaining implementation and original-verification obligation, including currently unqueued work and newly expanded leaves.",
    "Full manual/menu/appendix/utility/36-lesson-step reconciliation, not just 91 groups or 431 contents rows.",
    "All accepted native/companion domains meet FC-001\u2013009; no destructive mismatch or false-success save.",
    "All declared resources/locales/platform mappings are qualified; any scope/baseline change has explicit owner decision in git.",
    "NFR-005 matched metrics and predeclared tolerances; all SC-001\u2013005 satisfied before accept/merge.",
    "Fresh independent cross-artifact analysis after final queue derivation; changed task hashes invalidate prior analysis.",
    "FC-010 PDF remains optional M2 after M1 acceptance; no M1 PDF task."
  ],
  "runtime_derivation": {
    "commit_hash": "0234b85ec36e12c246af7d4c47a58c0b195c5d81",
    "bootstrap": {
      "total_wps": 22,
      "newly_seeded": 10,
      "already_initialized": 12
    },
    "lanes": {
      "computed": true,
      "count": 11,
      "lane_ids": [
        "lane-planning",
        "lane-a",
        "lane-d",
        "lane-f",
        "lane-j",
        "lane-b",
        "lane-e",
        "lane-c",
        "lane-g",
        "lane-h",
        "lane-i"
      ],
      "planning_artifact_wps": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21"
      ],
      "collapse_report": {
        "events": [],
        "total_merges": 0,
        "independent_wps_collapsed": 0,
        "by_rule": {}
      }
    },
    "ownership_warnings": [],
    "requirement_extraction_warnings": [],
    "post_integration_acceptance_warnings": [],
    "fc_mapping_rule": "Runtime extraction recognizes spec FR/NFR/C IDs, normalizing away FC IDs. compatibility_refs below retain permanent FC traceability explicitly from prompt bodies/docs/compatibility.md, not fabricated runtime acceptance mappings."
  }
}
```
<!-- WP12_LEDGER_END -->

## Reproducible planning checks

Run the following from the primary planning checkout. This checks every source hash (using committed code-lane revisions for code), all 38 requirements, all 91 exact inventory/case associations, all 236 case statuses, exact new task IDs, dependency closure/acyclicity, declared create intent/ownership and prompt/outline agreement. The negative checks prove omissions and an unrelated case substitution cannot silently pass. Runtime task finalization separately derives status, acceptance mappings and lanes; no lifecycle/frontmatter status is hand-authored. Its requirement extractor recognizes spec FR/NFR/C only and normalizes away FC frontmatter IDs. The ledger therefore records derived requirement_refs plus explicit compatibility_refs from prompt bodies and docs/compatibility.md; FC coverage is preserved without pretending the runtime acceptance matrix contains FC rows.

```sh
python3 - <<'PYVALIDATE'
from pathlib import Path
import collections, hashlib, json, re, subprocess, yaml, fnmatch
root = Path.cwd()
mission = root / 'kitty-specs/wp51-parity-01M64CVY'
text = (mission / 'continuation.md').read_text()
a = json.loads(text.split('<!-- WP12_LEDGER_BEGIN -->',1)[1].split('```json\n',1)[1].split('\n```',1)[0])
inv = {x['id']:x for x in json.loads((root/'docs/research/feature-inventory.json').read_text())}
cases = {x['id']:x for x in json.loads((root/'docs/research/command-scenarios.json').read_text())}
def check_coverage(a):
    expected = {f'{prefix}-{n:03}' for prefix,limit in [('FR',17),('NFR',5),('C',6),('FC',10)] for n in range(1,limit+1)}
    assert len(a['requirements']) == 38 and {x['id'] for x in a['requirements']} == expected
    assert len(a['inventory']) == 91 and {x['id'] for x in a['inventory']} == inv.keys()
    for row in a['inventory']:
        f = inv[row['id']]
        assert row['title'] == f['title'] and row['case_ids'] == f['command_scenario_ids']
        assert not row['closed'] and not row['full_group_implementation_queued']
        assert row['remaining_obligation'] == f['acceptance_probe'] and row['uncovered_subtasks_visible']
        assert all(row['id'] in cases[c]['feature_ids'] for c in row['case_ids'])
        assert row['oracle_counts'] == dict(collections.Counter(cases[c]['oracle_status'] for c in row['case_ids']))
    assert len(cases)==236 and collections.Counter(c['oracle_status'] for c in cases.values()) == {'partially-observed':53,'not-run':183}
    assert all(c['implementation_status']=='not-implemented' for c in cases.values())
    pdf = next(x for x in a['requirements'] if x['id']=='FC-010')
    assert pdf['status']=='m2-gated-constraint' and not pdf['queued_starter_wps'] and not pdf['unfulfilled_m1']
    assert not a['parity_accepted'] and not a['all_m1_obligations_closed'] and not a['queue_exhaustion_authorizes_acceptance']
check_coverage(a)
for source in a['source_inputs']:
    assert hashlib.sha256((root/source['path']).read_bytes()).hexdigest()==source['sha256'], source['path']
for c in a['components']:
    assert (root/c['review_path']).exists()
    for f in c['files']:
        raw = subprocess.check_output(['git','show',c['approved_commit']+':'+f['path']])
        assert hashlib.sha256(raw).hexdigest()==f['sha256']
packages={}
for path in sorted((mission/'tasks').glob('WP[0-9][0-9]-*.md')):
    parts=path.read_text().split('---',2)
    fm=yaml.safe_load(parts[1]); packages[fm['work_package_id']]=(fm,parts[2])
assert set(packages)=={f'WP{i:02}' for i in range(1,23)}
outline=(mission/'tasks.md').read_text()
assert [p['id'] for p in a['queued_packages']]==[f'WP{i:02}' for i in range(13,23)]
assert [s for p in a['queued_packages'] for s in p['subtasks']]==[f'T{i:03}' for i in range(37,67)]
all_tasks=[s for fm,_ in packages.values() for s in fm['subtasks']]
assert len(all_tasks)==len(set(all_tasks))==66
for p in a['queued_packages']:
    fm,body=packages[p['id']]
    for k in ['dependencies','execution_mode','requirement_refs','subtasks','owned_files']:
        assert fm[k]==p[k], (p['id'],k)
    assert all(d in packages for d in fm['dependencies'])
    assert all(c in body and c in outline for c in p['compatibility_refs'])
    assert p['id'] in outline and Path(p['prompt']).name in outline
    assert all(s in outline and s in body for s in p['subtasks'])
    assert all(k in body for k in ['Acceptance criteria','Ownership and explicit limits','Validation and independent review handoff'])
    assert set(fm['create_intent'])=={x for x in fm['owned_files'] if not (root/x).exists()}
    for other in a['queued_packages']:
        if other['id']<=p['id']: continue
        for left in p['owned_files']:
            for right in other['owned_files']:
                assert left!=right and not left.startswith(right.rstrip('/')+'/') and not right.startswith(left.rstrip('/')+'/'), (p['id'],other['id'],left,right)
seen=set(); active=set()
def visit(n):
    assert n not in active, n
    if n in seen:return
    active.add(n)
    for d in packages[n][0]['dependencies']:visit(d)
    active.remove(n);seen.add(n)
for n in packages:visit(n)
planning={n for n,(fm,_) in packages.items() if fm['execution_mode']=='planning_artifact'}
assert {'WP20','WP21'} <= planning
assert all(set(packages[n][0]['dependencies']) <= planning for n in planning)
lanes=json.loads((mission/'lanes.json').read_text())['lanes']
assert len(lanes)==a['runtime_derivation']['lanes']['count']==11
pl=[l for l in lanes if l['lane_id']=='lane-planning']
assert len(pl)==1 and set(pl[0]['wp_ids'])==planning
assert not pl[0]['depends_on_lanes']
assert not a['runtime_derivation']['ownership_warnings'] and not a['runtime_derivation']['requirement_extraction_warnings']
for mutate in ['requirement','group','case']:
    bad=json.loads(json.dumps(a))
    if mutate=='requirement':bad['requirements'].pop()
    elif mutate=='group':bad['inventory'].pop()
    else:bad['inventory'][0]['case_ids']=['CMD51-143']
    try:check_coverage(bad)
    except AssertionError:pass
    else:raise AssertionError('negative omission/substitution accepted: '+mutate)
print('WP12: 38 requirements, 91 groups, 236 cases, 10 WPs/30 subtasks, hashes/DAG/ownership/prompts and negative omission/substitution checks pass')
PYVALIDATE
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp12-validation.xml
git diff --check
```

After authoring, run `spec-kitty tasks --mission wp51-parity-01M64CVY --json` and inspect derived dependencies, acceptance mappings, initialized new status, single planning lane and all code ownership. Preserve its actual finalizer commits. Commit this ledger and queue planning artifacts through `spec-kitty spec-commit`. Fresh independent analysis must be regenerated against the final spec/plan/tasks hashes before WP12 moves for_review; the previous report is stale after queue expansion. Mark only T034–T036 through runtime authority after validation, and never self-approve or run the new WPs from this planning package.

Validation results and exact finalizer/commit identities are recorded in runtime history/review handoff after these checks execute. This text does not preclaim a passing future probe, application test or terminal/resource qualification.


## Next supported native editing tranche: WP23–WP29

This appended checkpoint preserves the entire prior WP12 ledger, queue snapshot
and historical validation text byte-for-byte. The old236-case/22-WP/66-subtask
checks describe their original checkpoint, not a current acceptance command.
Use the appended ledger and the actual latest canonical/approved code evidence
for this amendment. Do not rewrite old counts or raw observations to hide drift.

The new tranche has21 new subtasks T067–T087. It advances the existing read-only
milestone into explicitly admitted native edits and changed-document Save As.
It does not construct new documents, implement actual replacement, or close the
rest of M1. All38 requirements and91 groups below remain open at full breadth;
FC-010 remains an M2-gated constraint with no M1 PDF task.

Critical path: WP23 original mutation/field evidence → WP25 safe immutable native
edits/writer → WP26 exact code deletion/history → WP27 dirty/session/save intents
→ WP28 actual Bubble Tea executable → WP29 original-app differential acceptance.
WP24 source-bound candidate publication is independent of the writer and feeds
WP27. It must refactor the existing transaction to separate loaded-source identity
from edited-candidate bytes/hash, rather than duplicate it or synthesize a source.

WP23 has no WP15 hard dependency: its original probes require WP01/04/13/14,
while the WP15 API is context for the handoff. This avoids an e↔new-probe lane
cycle. WP24 remains below document/editor: making it depend on WP23/25 would
create a b→writer/probe→c→b cycle. New differential results stay local; a late
canonical-registry lane-c dependency on TUI lane-h would also create a cycle.

The installed runtime's ownership validator accepts true dependency-ordered
narrow overlaps, despite older skill wording saying codebase-wide is the only
exemption. Pure in-memory checks through the actual finalizer bridge reject an
unordered shared scope and accept its ordered form; the full22+7 graph is acyclic.
No installed runtime is patched, policy bypassed or old WP metadata reclassified.
Canonical validate-only/finalize and fresh independent analysis remain required
after primary promotion, at a quiet lifecycle point chosen by the root agent.

Zero-primary-match source globs are expected because approved Go code resides
on dependency branches/worktrees, with exact commit/file proofs below. Existing
source is not labelled newly created. Runtime chooses actual workspace/base;
no caller-selected worktree or fabricated source tree is authorized.

Writer admission remains blocked until independently reviewed WP23 demonstrates
all allowed prefix/body fields and relationships. The observed fixed324-byte
prefix and packet6 bit3 behavior do not alone authorize serialization. Unknown
offsets, formatter/nested/graphics/style/Fast Save variants and unsupported
identities remain preserved/refused. Every supported writer requires original
Retrieve, subsequent edit, selected-resource print and Save, plus Wordling reopen.
No screenshot or self-parsing candidate alone establishes interoperability.

<!-- NATIVE_EDIT_TRANCHE_LEDGER_BEGIN -->
```json
{
  "schema_version": 1,
  "mission": "wp51-parity-01M64CVY",
  "snapshot": "2026-10-30T23:29:50Z",
  "scope": "next supported-native-editing tranche; not M1 completion",
  "parity_accepted": false,
  "all_m1_obligations_closed": false,
  "queue_exhaustion_authorizes_acceptance": false,
  "previous_ledger_preserved_sha256": "327f67e0bde81763c8cc456293b747c48a4e3e1ca71386e1e48893a1747e651b",
  "counts": {
    "requirements": 38,
    "inventory_groups": 91,
    "total_queued_wps_after_promotion": 29,
    "total_subtasks_after_promotion": 87,
    "new_wps": 7,
    "new_subtasks": 21
  },
  "primary_catalogue_snapshot": {
    "case_count": 236,
    "oracle_counts": {
      "partially-observed": 53,
      "not-run": 183
    },
    "source_path": "docs/research/command-scenarios.json",
    "sha256": "a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0",
    "qualifier": "primary planning snapshot only; WP13 updated canonical registries remain on code lane until supported integration"
  },
  "source_inputs": [
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/spec.md",
      "sha256": "4255ca47a7e85912094e493dfe68473c2520db722402de081c927367951c6ed7"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/plan.md",
      "sha256": "7f8ab64334f8062c9a89e82a26a9f93741afa76e69800b0e0310f5ebdbeda1ed"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/data-model.md",
      "sha256": "c1ac3f4e78763355b1d3afd3a9a522ce2a229f0b4d03ec7b111d5a97e8efd3fc"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md",
      "sha256": "6ff65887643570f264d4e71b362ae302eee1216ddd870b8febbd667b93a7e496"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json",
      "sha256": "f0f4c945ec6551b5eeff68dd2c4ee108f98633a9979bdbfff6eda2854436e2bd"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/editing.md",
      "sha256": "7f542edd647b8735575036b0be570a88b048c5ea97755f25dbddadf92ce3a4bd"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md",
      "sha256": "dee9951828b2176e0714e0434d8774e7d0e0d7f4cc591b797c29954be7ed63bb"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md",
      "sha256": "aa6384662a74c1c0451a506bd9fdd169420614c558677a40715fbe0bab906631"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/session.md",
      "sha256": "826badb986e3e74f3ef236c7222b0b663ca4891c75acd8e5fd34777e7d7b319d"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/resource-readiness.md",
      "sha256": "39f982db595d35b754075b4d94c76bfd70659c61e3f24f454374c66c8c0fc0bd"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/coverage-leaves.md",
      "sha256": "0a095521e8f378351b12c64c0b326c141946f653c9dfce1fec801110e60e8118"
    },
    {
      "path": "docs/compatibility.md",
      "sha256": "98014cd41863f1d38186b45391408455f9410fd35ab88ff1f75bfc03c8a5f27a"
    },
    {
      "path": "docs/roadmap.md",
      "sha256": "23b273639792f223097111526f2655fa3261c20539bf8714e524c3d61a3eca29"
    },
    {
      "path": "docs/decisions/0002-lossless-native-boundary.md",
      "sha256": "29a97ba0379e35e9d20ada3d35609324a2f24fb9a49b9dde194f8d2a7099b325"
    },
    {
      "path": "docs/research/feature-inventory.json",
      "sha256": "49d37c3f13a537609346bc71751dabb8661676ecfa8fa40f25cee0752b5bccf8"
    },
    {
      "path": "docs/research/command-scenarios.json",
      "sha256": "a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0"
    },
    {
      "path": "docs/research/sources.json",
      "sha256": "850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"
    }
  ],
  "approved_code_source_proof": [
    {
      "wp": "WP02",
      "approved_source_commit": "e7de080452c2906e99c8ace0048c415d842f2f89",
      "source_location": "approved dependency code lane; absent from primary planning checkout",
      "files": [
        {
          "path": "internal/wp51/native.go",
          "sha256": "e13c93687e6119bff44f8405616455849cb728f3b4a1b3949d987dbe2c30b1d6"
        },
        {
          "path": "internal/wp51/README.md",
          "sha256": "ec42af13a0ab9ebb92b153c590e4de0ed4a07c341269afe0cc95558ad8926ab2"
        }
      ]
    },
    {
      "wp": "WP03",
      "approved_source_commit": "7deeaf6d7b62ce291358eceb81cb08c6f82ce512",
      "source_location": "approved dependency code lane; absent from primary planning checkout",
      "files": [
        {
          "path": "internal/storage/storage_linux.go",
          "sha256": "75e773e7ec01faa3943c76c874dd0bb4e99937113965139e9239e5ce498beb56"
        },
        {
          "path": "internal/storage/README.md",
          "sha256": "0791dc7799e59dc4d3bc2e4c46531a3e16b0941e63fa3a0c8735c94689f29b01"
        }
      ]
    },
    {
      "wp": "WP15",
      "approved_source_commit": "44f1a6dada2d90224f0ba856e240a018154646e7",
      "source_location": "approved dependency code lane; absent from primary planning checkout",
      "files": [
        {
          "path": "internal/document/document.go",
          "sha256": "a9b13f4ff5d759059ccebd6b8a5d6066c723ea17136c0d1261dc3290dd7d3aff"
        },
        {
          "path": "internal/document/README.md",
          "sha256": "999615e02c2933fb05e64786d88f4d5694ba16e6cf0ea0e70058123491c11295"
        }
      ]
    },
    {
      "wp": "WP16",
      "approved_source_commit": "fb23263e1ed7e31ca9005c6b9adf450a7986b674",
      "source_location": "approved dependency code lane; absent from primary planning checkout",
      "files": [
        {
          "path": "internal/input/event.go",
          "sha256": "beb1d62085b7c90d27803442a6013b59d52e82aa03d7414d8e5a653941a7a980"
        }
      ]
    }
  ],
  "requirements": [
    {
      "id": "C-001",
      "status": "open-full-obligation",
      "new_starters": [
        "WP24",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/C-001",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "C-002",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP24",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/C-002",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "C-003",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/C-003",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "C-004",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/C-004",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "C-005",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP25",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/C-005",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "C-006",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/C-006",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FC-001",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP25",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FC-001",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FC-002",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP24",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FC-002",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FC-003",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FC-003",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FC-004",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP24",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FC-004",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FC-005",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FC-005",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FC-006",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP25",
        "WP26",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FC-006",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FC-007",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP24",
        "WP25",
        "WP26",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FC-007",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FC-008",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FC-008",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FC-009",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP24",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FC-009",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FC-010",
      "status": "m2-gated-constraint",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FC-010",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-001",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-001",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-002",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP25",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-002",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-003",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-003",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-004",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-004",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-005",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-005",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-006",
      "status": "open-full-obligation",
      "new_starters": [
        "WP24",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-006",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-007",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-007",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-008",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP25",
        "WP26",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-008",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-009",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-009",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-010",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-010",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-011",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-011",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-012",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-012",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-013",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-013",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-014",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-014",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-015",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-015",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-016",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-016",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "FR-017",
      "status": "open-full-obligation",
      "new_starters": [],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/FR-017",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "NFR-001",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP24",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/NFR-001",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "NFR-002",
      "status": "open-full-obligation",
      "new_starters": [
        "WP24",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/NFR-002",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "NFR-003",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP25",
        "WP26",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/NFR-003",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "NFR-004",
      "status": "open-full-obligation",
      "new_starters": [
        "WP23",
        "WP24",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/NFR-004",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    },
    {
      "id": "NFR-005",
      "status": "open-full-obligation",
      "new_starters": [
        "WP29"
      ],
      "remaining_obligation_source": "unchanged WP12_LEDGER requirements/NFR-005",
      "full_obligation_closed": false,
      "unqueued_scope_retained": true
    }
  ],
  "inventory_groups": [
    {
      "id": "WP51-001",
      "title": "Clean screen, status, menus and function keys",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Replay start, edit, nested menus, cancel and exit; record screen and prompts.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-001"
    },
    {
      "id": "WP51-002",
      "title": "Context-sensitive help",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Open help from document and nested dialogs; return to the previous state.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-002"
    },
    {
      "id": "WP51-003",
      "title": "Original keyboard layouts and remapping",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Load, edit, persist and exercise keyboard definitions.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-003"
    },
    {
      "id": "WP51-004",
      "title": "Mouse interactions",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Exercise original menu and selection actions with terminal event mapping recorded.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-004"
    },
    {
      "id": "WP51-005",
      "title": "Display configuration and screen type",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare text attributes, display pitch, dimensions and graphics capabilities.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-005"
    },
    {
      "id": "WP51-006",
      "title": "Two-document switching and windows",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Switch and split documents; verify independent cursor and formatting state.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-006"
    },
    {
      "id": "WP51-007",
      "title": "Cancel and command repetition",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Cancel at multiple prompt depths; repeat input and commands.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-007"
    },
    {
      "id": "WP51-008",
      "title": "Cursor movement and go-to",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Move across text, codes, pages and subdocuments; compare cursor positions.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-008"
    },
    {
      "id": "WP51-009",
      "title": "Block selection and protection",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [
        "WP23",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Select original block types and test protection during editing and reflow.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-009"
    },
    {
      "id": "WP51-010",
      "title": "Copy, move and append",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Copy or move selections and append to new/existing files with codes intact.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-010"
    },
    {
      "id": "WP51-011",
      "title": "Text deletion and restoration",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [
        "WP23",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare deletion units and three-entry undelete behavior including paired codes.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-011"
    },
    {
      "id": "WP51-012",
      "title": "Insert versus typeover",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [
        "WP23",
        "WP25",
        "WP27",
        "WP28",
        "WP29"
      ],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Type across text and formatting codes; verify codes are not overwritten.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-012"
    },
    {
      "id": "WP51-013",
      "title": "Reveal Codes",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [
        "WP23",
        "WP25",
        "WP26",
        "WP27",
        "WP28",
        "WP29"
      ],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Toggle Alt-F3; move/delete in the code pane and compare effects in the normal pane.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-013"
    },
    {
      "id": "WP51-014",
      "title": "Search and replacement",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Exercise text/code searches, direction, case and extended subdocument replacement.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-014"
    },
    {
      "id": "WP51-015",
      "title": "Case changes and repeat input",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Apply commands to text and blocks; compare boundaries and formatting.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-015"
    },
    {
      "id": "WP51-016",
      "title": "Hard and soft returns and spaces",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Distinguish explicit paragraph boundaries from reflow; preserve code identity.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-016"
    },
    {
      "id": "WP51-017",
      "title": "Line-drawing text",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Create and modify line-drawing structures without corrupting text or characters.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-017"
    },
    {
      "id": "WP51-018",
      "title": "Refresh and reformat",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Trigger rewrite and inspect layout and cursor effects.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-018"
    },
    {
      "id": "WP51-019",
      "title": "Retrieve and insert documents",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Retrieve whole documents and blocks, preserving their codes and resource references.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-019"
    },
    {
      "id": "WP51-020",
      "title": "Native save and overwrite workflow",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [
        "WP24",
        "WP25",
        "WP27",
        "WP28",
        "WP29"
      ],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Save F10; verify filename editing, overwrite confirmation and initial codes.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-020"
    },
    {
      "id": "WP51-021",
      "title": "Original and timed backups",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Exercise both existing backup modes and recovery behavior; compare artifacts.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-021"
    },
    {
      "id": "WP51-022",
      "title": "Fast Save",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare saved bytes and formatting with the option enabled and disabled.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-022"
    },
    {
      "id": "WP51-023",
      "title": "File lists, directories and resource locations",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Replay file operations and path resolution with explicit Linux mapping.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-023"
    },
    {
      "id": "WP51-024",
      "title": "Password-locked documents",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Open and save correct/wrong-password fixtures without touching the original on failure.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-024"
    },
    {
      "id": "WP51-025",
      "title": "Original text import/export modes",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare each original mode, encoding and documented losses.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-025"
    },
    {
      "id": "WP51-026",
      "title": "Original 4.2 conversion modes",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare both conversion directions using original-version fixtures.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-026"
    },
    {
      "id": "WP51-027",
      "title": "Document comments and comparison",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Persist comments and compare documents, inspecting marked changes.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-027"
    },
    {
      "id": "WP51-028",
      "title": "Document look/find operations",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Exercise file-content inspection and conditional file finding.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-028"
    },
    {
      "id": "WP51-029",
      "title": "Exit and save decisions",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [
        "WP27",
        "WP28"
      ],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Replay saved/modified/unnamed documents through all exit decisions.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-029"
    },
    {
      "id": "WP51-090",
      "title": "Document summaries and descriptive names",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Create, cancel, save and retrieve document summaries; inspect long-name file lists.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-090"
    },
    {
      "id": "WP51-030",
      "title": "Attributes and change markings",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Apply/remove attributes and redline/strikeout; inspect paired codes and print results.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-030"
    },
    {
      "id": "WP51-031",
      "title": "Fonts and kerning",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare font changes, sizes, printer substitutions and kerning with fixed resources.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-031"
    },
    {
      "id": "WP51-032",
      "title": "Initial document and application codes",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Distinguish default settings from document initial codes and saved state.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-032"
    },
    {
      "id": "WP51-033",
      "title": "Margins and format menus",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Change line/page/document defaults and verify their code scope.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-033"
    },
    {
      "id": "WP51-034",
      "title": "Alignment, centering and indents",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare centered/right-aligned/justified text and indents across reflow.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-034"
    },
    {
      "id": "WP51-035",
      "title": "Tabs and tab alignment",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Set tab types, alignment and leaders; verify native codes and layout.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-035"
    },
    {
      "id": "WP51-036",
      "title": "Line height, spacing and numbering",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Combine proportional fonts, line height, spacing and line numbers.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-036"
    },
    {
      "id": "WP51-037",
      "title": "Word/letter spacing and measurement units",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Check unit conversion and spacing without cumulative layout drift.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-037"
    },
    {
      "id": "WP51-038",
      "title": "Precise positioning and advance",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare absolute/relative advances, page limits and text-box origins.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-038"
    },
    {
      "id": "WP51-039",
      "title": "Hyphenation and zones",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare word breaking, zones, manual decisions and saved codes.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-039"
    },
    {
      "id": "WP51-040",
      "title": "Hard/soft pages and conditional breaks",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Reflow through hard, soft, conditional and odd/even page transitions.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-040"
    },
    {
      "id": "WP51-041",
      "title": "Page numbering and paper definitions",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Use paper definitions and page numbering across format changes.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-041"
    },
    {
      "id": "WP51-042",
      "title": "Keep-together and widow/orphan rules",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Force borderline pagination and compare page membership.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-042"
    },
    {
      "id": "WP51-043",
      "title": "Columns and screen column presentation",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare newspaper and parallel columns, breaks, balancing and display.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-043"
    },
    {
      "id": "WP51-044",
      "title": "Headers, footers and suppression",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Create header/footer variants; compare suppression and page-dependent placement.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-044"
    },
    {
      "id": "WP51-045",
      "title": "Footnotes and endnotes",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Test nested text, numbering, continuation and pagination.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-045"
    },
    {
      "id": "WP51-091",
      "title": "Binding offsets and logical page parity",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare odd/even logical page offsets, labels and top-binding behavior.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-091"
    },
    {
      "id": "WP51-046",
      "title": "Styles and definitions",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Create and apply styles, edit definitions and compare resulting code scope.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-046"
    },
    {
      "id": "WP51-047",
      "title": "Outlines and numbering",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Create, redefine, promote/demote and restyle outline levels.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-047"
    },
    {
      "id": "WP51-048",
      "title": "Tables and structural editing",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Create tables; edit rows, columns, joins and splits; preserve native structure.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-048"
    },
    {
      "id": "WP51-049",
      "title": "Table formatting and calculations",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare cell/column formatting, formulas and recalculation.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-049"
    },
    {
      "id": "WP51-050",
      "title": "Generated contents, lists and index",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Mark text, define and regenerate indexes/lists/contents; verify page references.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-050"
    },
    {
      "id": "WP51-051",
      "title": "Table of authorities",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Mark citations, define categories and regenerate with original ordering.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-051"
    },
    {
      "id": "WP51-052",
      "title": "Master documents and subdocuments",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Expand/condense subdocuments and regenerate references across them.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-052"
    },
    {
      "id": "WP51-053",
      "title": "Labels and envelopes",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare definitions, repeated labels and envelope placement with fixed printer settings.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-053"
    },
    {
      "id": "WP51-054",
      "title": "Date values and codes",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare inserted values and generated dates under fixed clock and language settings.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-054"
    },
    {
      "id": "WP51-089",
      "title": "Cross-reference targets and generated references",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Mark references and named targets separately and together; regenerate after pagination changes.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-089"
    },
    {
      "id": "WP51-055",
      "title": "Graphics boxes, wrapping and captions",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Create/edit boxes and anchored objects; verify wrapping, sizing and captions.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-055"
    },
    {
      "id": "WP51-056",
      "title": "Graphics formats and conversion utility",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Reproduce original import/conversion behavior and preserve embedded/linked resources.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-056"
    },
    {
      "id": "WP51-057",
      "title": "Graphic rules and display options",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare rules, boxes, display settings and printed placement.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-057"
    },
    {
      "id": "WP51-058",
      "title": "Equations and equation editor",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Edit equation expressions and compare native representation and rendering.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-058"
    },
    {
      "id": "WP51-059",
      "title": "Macro definition, execution and editor",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Record, edit and execute original macros; compare prompts, keys and errors.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-059"
    },
    {
      "id": "WP51-060",
      "title": "Macro language, expressions and variables",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Catalogue and test each command, expression, variable and value-table behavior.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-060"
    },
    {
      "id": "WP51-061",
      "title": "Original macro conversion utility",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare supported original conversions and unsupported-input handling.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-061"
    },
    {
      "id": "WP51-062",
      "title": "Merge documents, data and commands",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Run simple and conditional merges using original file formats and command semantics.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-062"
    },
    {
      "id": "WP51-063",
      "title": "Sorting and record selection",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare keys, ordering, selected records and preservation of fields/codes.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-063"
    },
    {
      "id": "WP51-064",
      "title": "Column math and calculations",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Define columns and functions; compare arithmetic results and formatting.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-064"
    },
    {
      "id": "WP51-065",
      "title": "Spreadsheet import and links",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Import supported worksheets; update links and compare data/format refresh behavior.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-065"
    },
    {
      "id": "WP51-066",
      "title": "WP characters and compose",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Input original character-set identities and round-trip every supported mapping.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-066"
    },
    {
      "id": "WP51-067",
      "title": "Language selection and resources",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Switch language-dependent formatting and resources; record edition applicability.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-067"
    },
    {
      "id": "WP51-068",
      "title": "Spelling, dictionaries, lookup and counts",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Check corrections, dictionaries, lookup, counts and original utility behavior.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-068"
    },
    {
      "id": "WP51-069",
      "title": "Thesaurus",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare lookup, replacement and return-to-editor workflow using declared resources.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-069"
    },
    {
      "id": "WP51-070",
      "title": "Print selection, options and quality",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Print documents, pages and blocks; compare copies, quality, ordering and stopping.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-070"
    },
    {
      "id": "WP51-071",
      "title": "Printer selection and editing",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Select/edit original printer settings; preserve resource references and metrics.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-071"
    },
    {
      "id": "WP51-072",
      "title": "Printer commands and functions",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Exercise direct commands and layout-affecting printer controls.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-072"
    },
    {
      "id": "WP51-073",
      "title": "Printer-definition utility and fonts",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Inventory resource-editing and substitution behavior; define Linux equivalent explicitly.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-073"
    },
    {
      "id": "WP51-074",
      "title": "Printing to disk",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare original printer-language output bytes with matching resources.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-074"
    },
    {
      "id": "WP51-075",
      "title": "Print jobs and delivery",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Inspect, cancel and prioritize jobs; map delivery to Linux without changing print data.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-075"
    },
    {
      "id": "WP51-076",
      "title": "Document preview and options",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Compare page view and facing pages using declared printer metrics.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-076"
    },
    {
      "id": "WP51-077",
      "title": "Setup, environment and sound",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Persist original settings and document Linux adaptations.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-077"
    },
    {
      "id": "WP51-078",
      "title": "DOS and shell integration",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Inventory external-process workflows and define explicit Linux mappings.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-078"
    },
    {
      "id": "WP51-079",
      "title": "Bundled conversion, cursor and capture utilities",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Study utility boundaries and original artifact behavior before choosing Linux implementation.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-079"
    },
    {
      "id": "WP51-080",
      "title": "Memory and startup controls",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Classify original startup and memory controls; record hardware-only adaptations.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-080"
    },
    {
      "id": "WP51-081",
      "title": "Network and original resource files",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Inventory shared-file behavior, locking, resource discovery and companion formats.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-081"
    },
    {
      "id": "WP51-082",
      "title": "Code tables, defaults, keyboards and errors",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Reconcile appendices against feature coverage and negative scenarios.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/WP51-082"
    },
    {
      "id": "FMT51-001",
      "title": "File prefix and document pointer",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Check identifiers, versions, byte order, encryption marker and document pointer against original files.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/FMT51-001"
    },
    {
      "id": "FMT51-002",
      "title": "Prefix index chains and packets",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Preserve packet bytes and references while testing bounds, cycles and relocations.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/FMT51-002"
    },
    {
      "id": "FMT51-003",
      "title": "Document code framing and nested text",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Validate fixed/variable frames, nested codes and unknown-code preservation.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/FMT51-003"
    },
    {
      "id": "FMT51-004",
      "title": "Original character and function encoding",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Check every defined code class against fixtures, including hard/soft boundary codes.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/FMT51-004"
    },
    {
      "id": "FMT51-005",
      "title": "Formatting, structure and automation code groups",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Map every WP code group to semantic behavior and round-trip fixtures.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/FMT51-005"
    },
    {
      "id": "FMT51-006",
      "title": "Native WPM macro serialization",
      "status": "open-full-obligation",
      "closed": false,
      "new_starters": [],
      "full_group_implementation_queued": false,
      "remaining_obligation": "Read/write macro headers and command encodings with original interpreter evidence.",
      "historical_scope_source": "unchanged WP12_LEDGER inventory/FMT51-006"
    }
  ],
  "queued_packages": [
    {
      "id": "WP23",
      "title": "Original native mutation evidence and supported writer contract",
      "dependencies": [
        "WP01",
        "WP04",
        "WP13",
        "WP14"
      ],
      "subtasks": [
        "T067",
        "T068",
        "T069"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "scripts/reference/native_edits.py",
        "docs/research/continuation/native-edits/**",
        "docs/decisions/0003-supported-native-mutations.md"
      ],
      "create_intent": [
        "scripts/reference/native_edits.py",
        "docs/research/continuation/native-edits/",
        "docs/decisions/0003-supported-native-mutations.md"
      ],
      "requirement_refs": [
        "FR-002",
        "FR-004",
        "FR-005",
        "FR-008",
        "FR-015",
        "NFR-001",
        "NFR-003",
        "NFR-004",
        "C-002",
        "C-004",
        "C-005",
        "C-006"
      ],
      "compatibility_refs": [
        "FC-001",
        "FC-002",
        "FC-003",
        "FC-004",
        "FC-006",
        "FC-007",
        "FC-008",
        "FC-009"
      ],
      "prompt": "tasks/WP23-native-mutation-probes.md",
      "canonical_case_leads": [
        "CMD51-046",
        "CMD51-047",
        "CMD51-200",
        "CMD51-201",
        "CMD51-202",
        "CMD51-203",
        "CMD51-204",
        "CMD51-045",
        "CMD51-043",
        "CMD51-211"
      ],
      "execution_status": "not-executed-by-this-authoring"
    },
    {
      "id": "WP24",
      "title": "Source-bound edited candidate publication without replacement",
      "dependencies": [
        "WP03",
        "WP06"
      ],
      "subtasks": [
        "T070",
        "T071",
        "T072"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "internal/storage/**"
      ],
      "create_intent": [],
      "requirement_refs": [
        "FR-006",
        "NFR-001",
        "NFR-002",
        "NFR-004",
        "C-001",
        "C-002"
      ],
      "compatibility_refs": [
        "FC-002",
        "FC-004",
        "FC-007",
        "FC-009"
      ],
      "prompt": "tasks/WP24-edited-candidate-publication.md",
      "canonical_case_leads": [
        "CMD51-067",
        "CMD51-069",
        "CMD51-070",
        "CMD51-149"
      ],
      "execution_status": "not-executed-by-this-authoring"
    },
    {
      "id": "WP25",
      "title": "Immutable ASCII Bold edits and supported native serialization",
      "dependencies": [
        "WP15",
        "WP23"
      ],
      "subtasks": [
        "T073",
        "T074",
        "T075"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "internal/document/**"
      ],
      "create_intent": [],
      "requirement_refs": [
        "FR-002",
        "FR-005",
        "FR-008",
        "NFR-001",
        "NFR-002",
        "NFR-003",
        "NFR-004",
        "C-001",
        "C-002",
        "C-005"
      ],
      "compatibility_refs": [
        "FC-001",
        "FC-002",
        "FC-003",
        "FC-004",
        "FC-006",
        "FC-007",
        "FC-009"
      ],
      "prompt": "tasks/WP25-supported-native-edit-writer.md",
      "canonical_case_leads": [
        "CMD51-046",
        "CMD51-047",
        "CMD51-048",
        "CMD51-149"
      ],
      "execution_status": "not-executed-by-this-authoring"
    },
    {
      "id": "WP26",
      "title": "Bold code deletion block repair and three-entry Undelete",
      "dependencies": [
        "WP25",
        "WP23",
        "WP04"
      ],
      "subtasks": [
        "T076",
        "T077",
        "T078"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "internal/document/**"
      ],
      "create_intent": [],
      "requirement_refs": [
        "FR-005",
        "FR-008",
        "NFR-001",
        "NFR-002",
        "NFR-003",
        "NFR-004",
        "C-001",
        "C-002"
      ],
      "compatibility_refs": [
        "FC-002",
        "FC-003",
        "FC-004",
        "FC-006",
        "FC-007",
        "FC-009"
      ],
      "prompt": "tasks/WP26-deletion-and-undelete.md",
      "canonical_case_leads": [
        "CMD51-200",
        "CMD51-201",
        "CMD51-202",
        "CMD51-203",
        "CMD51-204",
        "CMD51-045",
        "CMD51-043",
        "CMD51-211"
      ],
      "execution_status": "not-executed-by-this-authoring"
    },
    {
      "id": "WP27",
      "title": "Revision-bound editing session and candidate Save As",
      "dependencies": [
        "WP17",
        "WP24",
        "WP25",
        "WP26"
      ],
      "subtasks": [
        "T079",
        "T080",
        "T081"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "internal/editor/**"
      ],
      "create_intent": [],
      "requirement_refs": [
        "FR-004",
        "FR-005",
        "FR-006",
        "NFR-001",
        "NFR-002",
        "NFR-004",
        "C-001",
        "C-002"
      ],
      "compatibility_refs": [
        "FC-002",
        "FC-003",
        "FC-004",
        "FC-009"
      ],
      "prompt": "tasks/WP27-editable-session-reducer.md",
      "canonical_case_leads": [
        "CMD51-046",
        "CMD51-047",
        "CMD51-043",
        "CMD51-204",
        "CMD51-067",
        "CMD51-069",
        "CMD51-070",
        "CMD51-087"
      ],
      "execution_status": "not-executed-by-this-authoring"
    },
    {
      "id": "WP28",
      "title": "Runnable Bubble Tea native editing and Save As composition",
      "dependencies": [
        "WP18",
        "WP27",
        "WP16"
      ],
      "subtasks": [
        "T082",
        "T083",
        "T084"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "internal/tui/**",
        "cmd/wordling/*.go",
        "docs/research/continuation/editable-session/**"
      ],
      "create_intent": [
        "docs/research/continuation/editable-session/"
      ],
      "requirement_refs": [
        "FR-002",
        "FR-004",
        "FR-005",
        "FR-006",
        "NFR-001",
        "NFR-002",
        "NFR-004",
        "C-001",
        "C-002"
      ],
      "compatibility_refs": [
        "FC-001",
        "FC-002",
        "FC-003",
        "FC-004",
        "FC-007",
        "FC-009"
      ],
      "prompt": "tasks/WP28-editable-bubbletea-session.md",
      "canonical_case_leads": [
        "CMD51-046",
        "CMD51-047",
        "CMD51-043",
        "CMD51-204",
        "CMD51-069",
        "CMD51-070",
        "CMD51-087"
      ],
      "execution_status": "not-executed-by-this-authoring"
    },
    {
      "id": "WP29",
      "title": "Executable native edit original-app differential acceptance",
      "dependencies": [
        "WP28",
        "WP23",
        "WP14"
      ],
      "subtasks": [
        "T085",
        "T086",
        "T087"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "scripts/reference/wordling_edits.py",
        "tests/compatibility/editing/**",
        "docs/research/continuation/editing-differential/**"
      ],
      "create_intent": [
        "scripts/reference/wordling_edits.py",
        "tests/compatibility/editing/",
        "docs/research/continuation/editing-differential/"
      ],
      "requirement_refs": [
        "FR-002",
        "FR-004",
        "FR-005",
        "FR-006",
        "FR-008",
        "FR-015",
        "NFR-001",
        "NFR-002",
        "NFR-003",
        "NFR-004",
        "NFR-005",
        "C-001",
        "C-002",
        "C-004",
        "C-005",
        "C-006"
      ],
      "compatibility_refs": [
        "FC-001",
        "FC-002",
        "FC-003",
        "FC-004",
        "FC-006",
        "FC-007",
        "FC-008",
        "FC-009"
      ],
      "prompt": "tasks/WP29-native-edit-differential.md",
      "canonical_case_leads": [
        "CMD51-046",
        "CMD51-047",
        "CMD51-048",
        "CMD51-149",
        "CMD51-200",
        "CMD51-201",
        "CMD51-202",
        "CMD51-203",
        "CMD51-204",
        "CMD51-045",
        "CMD51-043",
        "CMD51-211"
      ],
      "execution_status": "not-executed-by-this-authoring"
    }
  ],
  "lane_strategy": {
    "existing_wp_metadata_changes": false,
    "codebase_wide_exemptions": [],
    "predicted_groups": {
      "lane-b": [
        "WP03",
        "WP24"
      ],
      "lane-e": [
        "WP15",
        "WP25",
        "WP26"
      ],
      "lane-g": [
        "WP17",
        "WP27"
      ],
      "lane-h": [
        "WP18",
        "WP28"
      ],
      "lane-k": [
        "WP23"
      ],
      "lane-l": [
        "WP29"
      ]
    },
    "ownership_policy": "installed runtime exempts dependency-ordered narrow overlap; concurrent overlap still fails; mandatory canonical preflight on promoted drafts",
    "primary_glob_warnings": "honest zero-match soft warnings for approved sources in code lanes; no fake new-file create_intent",
    "canonical_registry_updates": "not owned by WP23\u201329; local results only, no late lane-c -> lane-h cycle"
  },
  "retained_unqueued_implementation": [
    "New native documents and complete prefix construction; actual replacement, original backups/Fast Save/recovery/locking and complete path/file-list workflows.",
    "Hard-return/layout editing, all remaining attributes/characters/Compose input, block/search/replace/copy/move/protected-text/two-screen/help/menu/mouse/repeat/keyboard behavior beyond supported branches.",
    "All full formatting/pagination/layout/printing/preview, structured documents/graphics/equations, macro/merge/data/language/resource/conversion/utility and platform obligations retained by38 requirements and91 groups.",
    "Complete reference/menu/appendix/utility/workbook-step reconciliation beyond reviewed first leaves; no remaining obligation becomes excluded.",
    "Canonical conformance promotion/integration arrangement and further reviewed packages after this tranche; no automatic accept/merge."
  ],
  "external_or_qualification_gaps": [
    "Historical DOS corroboration; matched graphics printer/fonts/preview metrics; non-US language/resource profiles; original worksheet/converter producers and rights/access.",
    "Physical terminal/desktop original-chord delivery and physical-to-paint timing; synthetic PTY/model tests cannot qualify those.",
    "Unresolved native relationships/fields block only their affected writer branch until probed; absence of external resources does not block independent supported ASCII/Bold work."
  ],
  "ownership_runtime_authority": [
    "installed specify_cli/ownership/validation.py validate_no_overlap/validate_all with dependencies",
    "installed specify_cli/cli/commands/agent/mission_finalize.py _validate_ownership_manifests passes actual dependencies",
    "installed specify_cli/lanes/compute.py compute_lanes collapses real shared scopes; no runtime patch selected"
  ],
  "zero_primary_match_dispositions": [
    {
      "wp": "WP23",
      "pattern": "docs/research/continuation/native-edits/**",
      "disposition": "planned-new evidence directory",
      "create_intent": "docs/research/continuation/native-edits/"
    },
    {
      "wp": "WP24",
      "pattern": "internal/storage/**",
      "disposition": "approved existing source in dependency lane",
      "proof": "WP03 7deeaf6d7b62ce291358eceb81cb08c6f82ce512; approved_code_source_proof/WP03; real storage_linux.go refactor required; not create_intent"
    },
    {
      "wp": "WP25",
      "pattern": "internal/document/**",
      "disposition": "approved existing source in dependency lane",
      "proof": "WP15 44f1a6dada2d90224f0ba856e240a018154646e7; approved_code_source_proof/WP15; not create_intent"
    },
    {
      "wp": "WP26",
      "pattern": "internal/document/**",
      "disposition": "approved existing source plus gated WP25 extension",
      "proof": "WP15 44f1a6dada2d90224f0ba856e240a018154646e7 and actual approved WP25 required before WP26; not create_intent"
    },
    {
      "wp": "WP27",
      "pattern": "internal/editor/**",
      "disposition": "existing earlier authoring ownership; prerequisite output still pending at this checkpoint",
      "proof": "WP17 is in progress; no current approved WP17 source claim. WP27 cannot execute until actual WP17 approval/source exists; not create_intent"
    },
    {
      "wp": "WP28",
      "pattern": "internal/tui/**",
      "disposition": "earlier WP18 output pending at this checkpoint",
      "proof": "WP18 not yet executed/approved at authoring. Actual WP18 approval/source required before WP28; not create_intent"
    },
    {
      "wp": "WP28",
      "pattern": "cmd/wordling/*.go",
      "disposition": "earlier WP18 executable source pending at this checkpoint",
      "proof": "WP18 must create and receive approval for actual command Go sources before WP28; glob truthfully owns only command Go sources, avoids false string-prefix match to wordling-input-probe; not create_intent"
    },
    {
      "wp": "WP28",
      "pattern": "docs/research/continuation/editable-session/**",
      "disposition": "planned-new evidence directory",
      "create_intent": "docs/research/continuation/editable-session/"
    },
    {
      "wp": "WP29",
      "pattern": "tests/compatibility/editing/**",
      "disposition": "planned-new test directory",
      "create_intent": "tests/compatibility/editing/"
    },
    {
      "wp": "WP29",
      "pattern": "docs/research/continuation/editing-differential/**",
      "disposition": "planned-new evidence directory",
      "create_intent": "docs/research/continuation/editing-differential/"
    }
  ],
  "canonical_preflight_observation": {
    "result": "validation_passed",
    "wp_count": 29,
    "bootstrap_new": 7,
    "bootstrap_existing": 22,
    "lanes": 13,
    "independent_wps_collapsed": 0,
    "ordered_scope_merges": 5,
    "requirement_extraction_warnings": [],
    "post_integration_acceptance_warnings": [],
    "qualifier": "Actual validate-only observation; not execution/approval or a preclaimed mutating-finalizer result."
  }
}
```
<!-- NATIVE_EDIT_TRANCHE_LEDGER_END -->

### Promotion and independent validation boundary

Draft authoring occurs outside primary to avoid lifecycle auto-committing a
partial queue. Root snapshots current old prompt/spec/plan hashes, promotes only
tasks.md, this appended continuation.md and new WP23–29 prompts at a quiet point,
then runs canonical finalize-tasks --validate-only. Only a passing preflight
permits the mutating finalizer; preserve its real status/mapping/lane outputs.
Use supported --refresh-planning-commit when needed for this legitimate additive
planning amendment after execution has begun. Never rewrite history or patch a
guard to force acceptance. Old lifecycle events and approvals stay unchanged.

Fresh independent analysis must use the final spec/plan/tasks hashes and report
real ownership, requirement, branch, source and acceptance gaps. Runtime alone
owns lifecycle initialization and review verdicts. None of this authoring claims
new WPs implemented, original probes executed, terminal/resources qualified, or
full mission acceptance. The continued full-scope obligation ledger governs
later queues; completion of29 packages cannot close M1 while gaps remain.


<!-- CONFORMANCE_TRANCHE_BEGIN -->
## Versioned current conformance tranche: WP30–WP31 (unexecuted planning amendment)

This append preserves every earlier checkpoint and full M1 obligation. Approved
architecture separates immutable original-reference catalogue snapshots from a new
versioned current conformance registry. It does not change native/companion formats,
rename production code, migrate ownership or reduce the parity acceptance boundary.
WP30 tooling depends on WP13/WP18/WP20/WP21; it can default product states unverified
without WP29. WP31 depends on WP30/WP29 and ingests only actual reviewed bounded
executable/original comparison evidence. Both are code_change with real executable
validator/ingestion/test deliverables and sequential ownership in the new namespace.

Original source identity is approved WP13 commit
18d6afe95ffcd676fc3f9e964dcad884c9a8c289, with 244 scenarios/91 groups:
command-scenarios.json SHA256 8161fe7e5f032aa459c8f33a149a00f6e7263cd153f613533d297eeca9ec8d4a;
feature-inventory.json SHA256 633cad8fbcc3e59a13bf0003566bfdb2f9925c26a5899a54a989a65da91138d5.
Primary older236-case snapshots are not equivalent. Historical catalogues/generated
views and original-only status labels stay frozen; current README/ADR/index explain
revision/date and identify docs/conformance/v1/ as current conformance authority.
Existing old renderers require unimplemented/pending historical statuses; the new
schema extends evidence reporting rather than laundering original-only observations.

Retain all38 obligations,91 groups, all inherited cases and discovered leaves,
versioned case extensions, resource/locale/physical gaps, original workflows/utilities
and full SC-001–005. New extension IDs need collision checks, exact parent/source
locators and revision lineage. Current records separate documentary, original-observed,
component, executable integration, differential and physical/resource qualification.
Positive claims bind exact code/review/executable invocation/raw hashes/resources/
comparator/case revision/scope. Unproved or failed branches remain open; no source-only,
helper-only or partial editing pass closes a parent group/FR/NFR/FC or full scenario.
WP31 produces future normal acceptance readiness bindings only: it does not edit the
runtime acceptance matrix, mark requirements passing, accept/merge M1 or start M2/PDF.

<!-- CONFORMANCE_TRANCHE_LEDGER_BEGIN -->
```json
{
  "schema_version": 1,
  "mission": "wp51-parity-01M64CVY",
  "phase": "unexecuted next-tranche planning draft",
  "parity_accepted": false,
  "all_m1_obligations_closed": false,
  "queue_exhaustion_authorizes_acceptance": false,
  "retained_obligations": 38,
  "retained_inventory_groups": 91,
  "approved_source_scenarios": 244,
  "approved_source_commit": "18d6afe95ffcd676fc3f9e964dcad884c9a8c289",
  "new_subtasks": [
    "T088",
    "T089",
    "T090",
    "T091",
    "T092",
    "T093"
  ],
  "packages": [
    {
      "wp": "WP30",
      "dependencies": [
        "WP13",
        "WP18",
        "WP20",
        "WP21"
      ],
      "owned_files": [
        "docs/conformance/v1/**",
        "scripts/conformance/v1/**",
        "tests/conformance/v1/**",
        "README.md",
        "docs/decisions/0004-conformance-evidence-layers.md"
      ],
      "create_intent": [
        "docs/conformance/v1/",
        "scripts/conformance/v1/",
        "tests/conformance/v1/",
        "docs/decisions/0004-conformance-evidence-layers.md"
      ],
      "execution_mode": "code_change",
      "full_requirement_acceptance": false
    },
    {
      "wp": "WP31",
      "dependencies": [
        "WP30",
        "WP29"
      ],
      "owned_files": [
        "docs/conformance/v1/**",
        "scripts/conformance/v1/**",
        "tests/conformance/v1/**"
      ],
      "create_intent": [
        "docs/conformance/v1/",
        "scripts/conformance/v1/",
        "tests/conformance/v1/"
      ],
      "execution_mode": "code_change",
      "full_requirement_acceptance": false
    }
  ],
  "expected_topology": {
    "new_lane": "lane-m",
    "members": [
      "WP30",
      "WP31"
    ],
    "depends_on_lanes": [
      "lane-c",
      "lane-h",
      "lane-l",
      "lane-planning"
    ],
    "old_lane_assignments_retained": true,
    "qualifier": "Expected pure in-memory proof; no canonical finalizer or execution claimed."
  }
}
```
<!-- CONFORMANCE_TRANCHE_LEDGER_END -->

Root promotes only this additive tasks/continuation amendment and the two new prompts
at a lifecycle quiet point after source-prefix/hash comparison. Run normal canonical
finalize-tasks --validate-only; only a real passing preflight permits finalization,
with supported --refresh-planning-commit when required for this additive amendment.
Then independent analysis binds final hashes. No old29 prompt/spec/plan/approved status
is rewritten. No private merge primitive, installed-tool patch, exemption or artificial
planning classification is needed. Completion of31 packages still cannot accept M1
while the complete obligation/coverage/resource ledger contains unresolved gaps.
<!-- CONFORMANCE_TRANCHE_END -->


### WP30–WP31 actual canonical preflight and ownership diagnostics

Canonical validate-only passed against the promoted31 prompts:31 WPs,93 subtasks,
14 computed lanes,2 new bootstrap previews/29 existing; no requirement extraction or
post-integration acceptance warnings, no ownership errors and zero independent
collapses. All old29 lane assignments, prompt metadata/bodies and spec/plan bytes
were preserved. Only new30/31 branch_strategy metadata would normalize. This is
authoring validation, not execution, review, physical qualification or M1 acceptance.

All16 zero-match ownership warnings were inspected and dispositioned individually:

| WP | Declared path | Disposition |
| --- | --- | --- |
| WP23 | `docs/research/continuation/native-edits/**` | Historical existing tranche ownership; absent from primary planning checkout. Source-lane path actually present: `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-k`. |
| WP24 | `internal/storage/**` | Historical existing tranche ownership; absent from primary planning checkout. Source-lane path actually present: `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-b`, `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h`, `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-c`, `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g`, `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-k`. |
| WP25 | `internal/document/**` | Historical existing tranche ownership; absent from primary planning checkout. Source-lane path actually present: `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h`, `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e`, `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g`. |
| WP26 | `internal/document/**` | Historical existing tranche ownership; absent from primary planning checkout. Source-lane path actually present: `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h`, `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e`, `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g`. |
| WP27 | `internal/editor/**` | Historical existing tranche ownership; absent from primary planning checkout. Source-lane path actually present: `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h`, `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g`. |
| WP28 | `internal/tui/**` | Historical existing tranche ownership; absent from primary planning checkout. Source-lane path actually present: `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h`. |
| WP28 | `cmd/wordling/*.go` | Historical existing tranche ownership; absent from primary planning checkout. Source-lane path actually present: `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h`. |
| WP28 | `docs/research/continuation/editable-session/**` | Historical existing tranche ownership; absent from primary planning checkout. Declared planned-new/in-flight surface with matching create_intent; no claim that implementation already exists. |
| WP29 | `tests/compatibility/editing/**` | Historical existing tranche ownership; absent from primary planning checkout. Declared planned-new/in-flight surface with matching create_intent; no claim that implementation already exists. |
| WP29 | `docs/research/continuation/editing-differential/**` | Historical existing tranche ownership; absent from primary planning checkout. Declared planned-new/in-flight surface with matching create_intent; no claim that implementation already exists. |
| WP30 | `docs/conformance/v1/**` | Genuine planned-new current namespace; directory create_intent declared; WP31 sequentially reuses WP30 output. |
| WP30 | `scripts/conformance/v1/**` | Genuine planned-new current namespace; directory create_intent declared; WP31 sequentially reuses WP30 output. |
| WP30 | `tests/conformance/v1/**` | Genuine planned-new current namespace; directory create_intent declared; WP31 sequentially reuses WP30 output. |
| WP31 | `docs/conformance/v1/**` | Genuine planned-new current namespace; directory create_intent declared; WP31 sequentially reuses WP30 output. |
| WP31 | `scripts/conformance/v1/**` | Genuine planned-new current namespace; directory create_intent declared; WP31 sequentially reuses WP30 output. |
| WP31 | `tests/conformance/v1/**` | Genuine planned-new current namespace; directory create_intent declared; WP31 sequentially reuses WP30 output. |

The new ADR literal path is genuinely new and explicitly declared in create_intent;
root README already exists. Old10 source-lane/planned warnings do not license source
copying, fake ownership or path renames. No empty directory was created to suppress
warnings. Shared new scopes are dependency-ordered WP30→WP31; installed validator
permits this truthful narrow sequential overlap without a codebase-wide exemption.

Actual pure graph agrees with canonical preview: lane-m={WP30,WP31}, depending on
lane-c, lane-h, lane-l and lane-planning. WP30 individual prerequisites exclude WP29;
the lane aggregate includes lane-l because WP31 consumes WP29. Runtime remains the
scheduling authority. These diagnostic dispositions amend only this new checkpoint;
every historical prefix/old prompt/spec/plan remains intact.


### WP30–WP31 actual finalization boundary

Canonical mutating finalize-tasks completed successfully at task commit
`4f2f0fb2216ce7b355972cd8fef58c559844e096`:31 WPs,2 metadata updates/new
bootstrap entries,29 existing,14 lanes and zero independent scope collapses. Only
new WP30/WP31 branch_strategy metadata normalized; old29 prompts were reported
unchanged. Actual warnings match the16 dispositions above; requirement extraction
and post-integration acceptance warning arrays were empty. Runtime created the new
planned-state bookkeeping; this is not implementation or review approval. The
finalizer also committed its existing dossier projection. It left this authored
continuation append outside its commit scope, so the supported spec-commit artifact
path commits this exact append before recording an updated planning snapshot.
Full M1 remains open, and no implementation/VM/acceptance or M2 work occurred here.


<!-- MACRO_TRANCHE_BEGIN -->
## Native WPM and macro interaction continuation: WP32–WP38 (unexecuted draft)

Existing evidence supports starting a separate WPM contract/reader and bounded
injected-sink evaluator while WP23 exclusively uses the original VM. This is an
additive queue, not a reduction of all38 requirements,91 inventory groups, discovered
nested leaves, complete M1 or any original native/companion format obligation.
Full FR-012 remains open. PDF stays M2 after real M1 acceptance.

WP09 has20 macro observations and15 merge observations. A read-only audit checked
all46 original WPM source exports (22 distinct hashes) against sealed manifest
size/hash entries across10 runs and corroborated tuple1/1/1/1, four-entry40-byte
index, description pointer56, observed body70/75, even relative body length and
terminal0000. FLOW length169/body75 forbids absolute even-alignment assumptions.
SDK WP92–99/PDF105–112 documents separate WPM prefix/index/word grammar. WPM
description bytes are not the two-byte macro word stream; nested VARIABLE operands
consume inner tildes. Native DOC grammar/type1 refusal must remain intact.

Audit source hashes: automation.md2529b6218b36fccba2c143c8158017ae853d10e8fe3d7afc1958d6407d50e6f6;
toolkit.txt8ed26dae470713efd51c62de51686168a0ee0127efd428f50c5a622862269c8f;
reference.txtf1d786f3ea0697f652bdfb2c13cb7745a01e9fbe9abb64042e517f1a85c4304c.
These identify existing research, not newly executed compatibility tests.

WP32 is genuinely planning-only and depends only on WP01/09/10 planning outputs.
It owns only two new contract/fixture-ledger files; no executable validator is hidden.
WP33 reader,34 rooted ReadMacro,35 evaluator,36 editor adapter,37 runnable TUI and38
original probe runner are honest code_change packages. WP34 reuses approved storage
acquisition; existing PreparePublication remains DOC-specific. WPM filesystem saving
is not added here, no transaction is duplicated and no source parser is weakened.

Production consumer path is WPM codec→storage ReadMacro→actual editor reducer→actual
Bubble Tea executable. VM imports neither storage/editor/document nor TUI; injected
native command sink/resolver carry ordered effects/errors. Codec→storage is permitted;
storage→VM→editor→storage is forbidden. Ordinary editor/document/writer paths own real
document state/output, not the macro interpreter. WP33 no-edit Export and WP35 sink
traces are component evidence; they do not close CMD51-199 or executable FR-012.

WP38 original runs use fresh scratch copies only after explicit WP23 VM release;
authoring is possible now, runtime ownership is not assumed. It needs planning
WP09/11/32 and hash-pinned existing pre-mission QMP/guest/probe helpers, not WP23
code. REF379/PDF396 documents Macro(Alt-F10), Repeat(Esc), Cancel(F1); Ctrl-Break
must not become an invented macro alias. Existing same-buffer/Doc2 repeat recipes
prove only their captured states. Reviewed new run/stop/buffer/dirty/error evidence
gates WP36/37 before enabling those branches. Failed/unavailable probes stay explicit
open/unsupported; component error injection is not integrated search compatibility.

WP36 depends on WP27/34/35/38; WP37 on WP28/36/38. Both must consume real pending,
source/revision/dirty/ordinary command APIs and compare actual native document output
with original oracles. A helper/sink screen result cannot satisfy this. Neither adds
WPM authoring or grants source-format writes. Recording/editing/conversion, full
merge language, other keys/operators, non-ASCII/non-US/resource/physical/historical
DOS qualification and every remaining M1 obligation stay explicit future work.

<!-- MACRO_TRANCHE_LEDGER_BEGIN -->
```json
{
  "schema_version": 1,
  "mission": "wp51-parity-01M64CVY",
  "phase": "temporary unexecuted macro tranche draft",
  "parity_accepted": false,
  "all_m1_obligations_closed": false,
  "queue_exhaustion_authorizes_acceptance": false,
  "retained_obligations": 38,
  "retained_inventory_groups": 91,
  "retained_nested_leaf_scope": true,
  "subtasks": [
    "T094",
    "T095",
    "T096",
    "T097",
    "T098",
    "T099",
    "T100",
    "T101",
    "T102",
    "T103",
    "T104",
    "T105",
    "T106",
    "T107",
    "T108",
    "T109",
    "T110",
    "T111",
    "T112",
    "T113",
    "T114"
  ],
  "packages": [
    {
      "wp": "WP32",
      "dependencies": [
        "WP01",
        "WP09",
        "WP10"
      ],
      "execution_mode": "planning_artifact",
      "owned_files": [
        "kitty-specs/wp51-parity-01M64CVY/contracts/macro-framing.md",
        "kitty-specs/wp51-parity-01M64CVY/contracts/macro-fixtures.json"
      ],
      "create_intent": [
        "kitty-specs/wp51-parity-01M64CVY/contracts/macro-framing.md",
        "kitty-specs/wp51-parity-01M64CVY/contracts/macro-fixtures.json"
      ],
      "full_requirement_acceptance": false
    },
    {
      "wp": "WP33",
      "dependencies": [
        "WP32",
        "WP02"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "internal/macro/wpm/**"
      ],
      "create_intent": [
        "internal/macro/wpm/"
      ],
      "full_requirement_acceptance": false
    },
    {
      "wp": "WP34",
      "dependencies": [
        "WP24",
        "WP33"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "internal/storage/**"
      ],
      "create_intent": [],
      "full_requirement_acceptance": false
    },
    {
      "wp": "WP35",
      "dependencies": [
        "WP33"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "internal/macro/runtime/**"
      ],
      "create_intent": [
        "internal/macro/runtime/"
      ],
      "full_requirement_acceptance": false
    },
    {
      "wp": "WP36",
      "dependencies": [
        "WP27",
        "WP34",
        "WP35",
        "WP38"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "internal/editor/**"
      ],
      "create_intent": [],
      "full_requirement_acceptance": false
    },
    {
      "wp": "WP37",
      "dependencies": [
        "WP28",
        "WP36",
        "WP38"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "internal/tui/**",
        "cmd/wordling/*.go",
        "docs/research/continuation/macro-executable/**"
      ],
      "create_intent": [
        "docs/research/continuation/macro-executable/"
      ],
      "full_requirement_acceptance": false
    },
    {
      "wp": "WP38",
      "dependencies": [
        "WP09",
        "WP11",
        "WP32"
      ],
      "execution_mode": "code_change",
      "owned_files": [
        "scripts/reference/macro_session.py",
        "docs/research/continuation/macro-session/**"
      ],
      "create_intent": [
        "scripts/reference/macro_session.py",
        "docs/research/continuation/macro-session/"
      ],
      "full_requirement_acceptance": false
    }
  ]
}
```
<!-- MACRO_TRANCHE_LEDGER_END -->

Expected new lanes: n=WPM codec33, o=VM35, p=original probes38; storage34 joins b,
editor36 joins g and TUI37 joins h through real dependency-ordered narrow ownership.
All old14 lane IDs and old31 prompt/spec/plan bytes must survive installed pure
ownership/compute validation. No codebase-wide exemptions, fake create_intent or
missing dependency is permitted. Primary zero-match globs for approved code are
dispositioned against actual source lanes, not disguised as newly created packages.

Root may promote only additive tasks/continuation and seven new prompts at a
lifecycle quiet point after current independent review releases its claim. First
compare all snapshot hashes and old byte prefixes, then run canonical finalize-tasks
--validate-only; only a real pass permits normal mutating finalization, with supported
planning-snapshot refresh if required. Preserve real diagnostics and fresh independent
analysis; no private runtime calls, tool patch or direct state edits. This draft
claims no finalizer, execution, review approval, acceptance, merge or M2 start.
<!-- MACRO_TRANCHE_END -->


### Temporary installed pure validation checkpoint

Installed ownership validate_all(dependencies), validate_glob_matches and compute_lanes pass:38 WPs,114 subtasks,17 lanes versus old14; zero ownership/glob errors and zero independent WP collapses. All31 old WP lane IDs match both pure old computation and existing lanes.json; old lane-m stays lane-m. Nine scope merges are dependency-ordered (six inherited, three new storage/editor/TUI extensions). Exact draft files and proof are temporary only; no finalizer/lifecycle/implementation/approval claimed.

New mapping:32=planning,33=n,34=b,35=o,36=g,37=h,38=p. New lane dependencies are acyclic; macro codec/VM import direction remains a code-review gate. Root must rerun canonical validation after promotion.

The installed mode heuristic emits21 advisory warnings because internal/, cmd/ and scripts/ are outside its src/ or tests/ naming convention:15 inherited plus new33–38. These are real Go/Python code changes, so code_change is retained. No fake tests directory, planning classification or exemption suppresses them. WP32 emits no such warning.

All24 zero-match glob warnings were inspected individually against actual source lanes. The two new contract literal paths and new probe script are planned-new files explicitly declared in create_intent; their info notes are expected. Existing create_intent metadata is untouched.

| WP | Pattern | Disposition |
| --- | --- | --- |
| WP23 | `docs/research/continuation/native-edits/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-k` |
| WP24 | `internal/storage/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-b`, `wp51-parity-01M64CVY-lane-c`, `wp51-parity-01M64CVY-lane-g`, `wp51-parity-01M64CVY-lane-h`, `wp51-parity-01M64CVY-lane-i`, `wp51-parity-01M64CVY-lane-k`, `wp51-parity-01M64CVY-lane-m` |
| WP25 | `internal/document/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-e`, `wp51-parity-01M64CVY-lane-g`, `wp51-parity-01M64CVY-lane-h`, `wp51-parity-01M64CVY-lane-i`, `wp51-parity-01M64CVY-lane-m` |
| WP26 | `internal/document/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-e`, `wp51-parity-01M64CVY-lane-g`, `wp51-parity-01M64CVY-lane-h`, `wp51-parity-01M64CVY-lane-i`, `wp51-parity-01M64CVY-lane-m` |
| WP27 | `internal/editor/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-g`, `wp51-parity-01M64CVY-lane-h`, `wp51-parity-01M64CVY-lane-i`, `wp51-parity-01M64CVY-lane-m` |
| WP28 | `internal/tui/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-h`, `wp51-parity-01M64CVY-lane-i`, `wp51-parity-01M64CVY-lane-m` |
| WP28 | `cmd/wordling/*.go` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-h`, `wp51-parity-01M64CVY-lane-i`, `wp51-parity-01M64CVY-lane-m` |
| WP28 | `docs/research/continuation/editable-session/**` | Genuinely planned-new owned namespace with declared create_intent; no empty directory created. |
| WP29 | `tests/compatibility/editing/**` | Genuinely planned-new owned namespace with declared create_intent; no empty directory created. |
| WP29 | `docs/research/continuation/editing-differential/**` | Genuinely planned-new owned namespace with declared create_intent; no empty directory created. |
| WP30 | `docs/conformance/v1/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-m` |
| WP30 | `scripts/conformance/v1/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-m` |
| WP30 | `tests/conformance/v1/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-m` |
| WP31 | `docs/conformance/v1/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-m` |
| WP31 | `scripts/conformance/v1/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-m` |
| WP31 | `tests/conformance/v1/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-m` |
| WP33 | `internal/macro/wpm/**` | Genuinely planned-new owned namespace with declared create_intent; no empty directory created. |
| WP34 | `internal/storage/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-b`, `wp51-parity-01M64CVY-lane-c`, `wp51-parity-01M64CVY-lane-g`, `wp51-parity-01M64CVY-lane-h`, `wp51-parity-01M64CVY-lane-i`, `wp51-parity-01M64CVY-lane-k`, `wp51-parity-01M64CVY-lane-m` |
| WP35 | `internal/macro/runtime/**` | Genuinely planned-new owned namespace with declared create_intent; no empty directory created. |
| WP36 | `internal/editor/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-g`, `wp51-parity-01M64CVY-lane-h`, `wp51-parity-01M64CVY-lane-i`, `wp51-parity-01M64CVY-lane-m` |
| WP37 | `internal/tui/**` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-h`, `wp51-parity-01M64CVY-lane-i`, `wp51-parity-01M64CVY-lane-m` |
| WP37 | `cmd/wordling/*.go` | Existing approved/in-flight real source lane; not create_intent. Inspect actual dependency approval before execution.; actual source: `wp51-parity-01M64CVY-lane-h`, `wp51-parity-01M64CVY-lane-i`, `wp51-parity-01M64CVY-lane-m` |
| WP37 | `docs/research/continuation/macro-executable/**` | Genuinely planned-new owned namespace with declared create_intent; no empty directory created. |
| WP38 | `docs/research/continuation/macro-session/**` | Genuinely planned-new owned namespace with declared create_intent; no empty directory created. |


### Macro tranche actual canonical validate-only preflight

After fresh hash/prefix checks, root-authorized promotion changed only tasks.md,
continuation.md and new WP32–38 prompts. All31 old prompt bytes and spec/plan remained
unchanged; no bookkeeping delta required overwriting an old prompt. Canonical
`spec-kitty agent mission finalize-tasks --mission wp51-parity-01M64CVY --validate-only --json`
returned validation_passed:38 WPs,114 authored subtasks,7 new/31 existing bootstrap
previews,17 lanes,zero updated prompts,zero independent collapses and empty requirement
extraction/post-integration acceptance warning arrays. Its24 glob warnings match the
individual dispositions above exactly;9 dependency-ordered scope merges include the
three new storage/editor/TUI extensions. Old14 lane IDs/old31 assignments match the
existing manifest and installed pure recomputation. This is real authoring preflight,
not mutating finalization, initialization, implementation, approval or acceptance.

Canonical raw output SHA256: `bcddcd3ae8bea434f4fc671b9f9179c11b1ab659d8daf6d6458efa7dbabcd855`.
No mutating finalizer has run at this checkpoint; root owns its serialization after
the active WP30 fix/review transition. Native formats, full38 obligations/91 groups
and uncovered nested families remain unchanged.

The installed pure ownership execution-mode heuristic additionally emitted these21
advisories; canonical JSON lists glob warnings separately. Each points to real Go or
Python source outside the heuristic src/ or tests/ convention. Retain code_change;
never suppress an advisory with planning_artifact, fake paths or exemptions. These
are advisory classifications, not missing executable deliverables:

```json
[
  "WP02: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/wp51/']",
  "WP03: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/storage/']",
  "WP13: code_change WP does not own any files under src/ or tests/. owned_files: ['scripts/reference/session1.py', 'docs/research/continuation/session1/', 'docs/research/command-scenarios.json', 'docs/research/command-scenarios.md', 'docs/research/scenario-coverage.md', 'docs/research/workbook-map.md', 'docs/research/feature-inventory.json', 'docs/research/feature-inventory.md']",
  "WP14: code_change WP does not own any files under src/ or tests/. owned_files: ['scripts/reference/text_layout.py', 'docs/research/continuation/text-layout/']",
  "WP15: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/document/']",
  "WP16: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/input/', 'cmd/wordling-input-probe/', 'docs/research/continuation/terminal-input/']",
  "WP17: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/editor/']",
  "WP18: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/tui/', 'cmd/wordling/', 'docs/research/continuation/composed-session/']",
  "WP22: code_change WP does not own any files under src/ or tests/. owned_files: ['scripts/reference/character_identity.py', 'docs/research/continuation/character-identity/']",
  "WP23: code_change WP does not own any files under src/ or tests/. owned_files: ['scripts/reference/native_edits.py', 'docs/research/continuation/native-edits/**', 'docs/decisions/0003-supported-native-mutations.md']",
  "WP24: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/storage/**']",
  "WP25: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/document/**']",
  "WP26: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/document/**']",
  "WP27: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/editor/**']",
  "WP28: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/tui/**', 'cmd/wordling/*.go', 'docs/research/continuation/editable-session/**']",
  "WP33: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/macro/wpm/**']",
  "WP34: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/storage/**']",
  "WP35: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/macro/runtime/**']",
  "WP36: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/editor/**']",
  "WP37: code_change WP does not own any files under src/ or tests/. owned_files: ['internal/tui/**', 'cmd/wordling/*.go', 'docs/research/continuation/macro-executable/**']",
  "WP38: code_change WP does not own any files under src/ or tests/. owned_files: ['scripts/reference/macro_session.py', 'docs/research/continuation/macro-session/**']"
]
```


### Macro tranche actual canonical finalization checkpoint

Root-authorized mutating finalize-tasks completed successfully at task commit
`81526314682cf2229846fea849ac4045d74c266b`:38 WPs,7 new/31 existing bootstrap records,17 lanes,
zero metadata updates reported,zero independent collapses and empty requirement
extraction/post-integration acceptance warning arrays. Actual24 glob warnings match
the durable individual dispositions above;21 mode-heuristic advisories remain as
recorded. Existing old31 prompt/spec/plan bytes remain identical to the protected
snapshot; original tasks/continuation prefixes are preserved. Actual lane mapping
exactly matches installed pure proof, retaining all old14 IDs including lane-m.

Canonical finalization committed tasks/new prompts/runtime-owned initialization and
its existing dossier projection; it left the exact authored continuation append
outside its commit scope. The supported spec-commit path commits this continuation
before a supported refresh-planning-commit records a snapshot containing all nine
amendment artifacts. No manual lifecycle/frontmatter edits, analysis record, VM
execution or new implementation is part of this authoring checkpoint. Full38
obligations/91 groups/nested leaves and all full M1 gaps remain open; bootstrap
planned state is not review approval, product compatibility or acceptance.


### In-implementation FC20 prerequisite discovered by WP35

The independent-approved WP32 ledger identifies QUIT FC20 in206 HANDLER byte139,210 ONERROR byte141,212 CHILD byte141/PARENT byte175 and213 PARENT byte141. Existing error-handler branches skip every site; neither token identity nor manual wording proves normal execution. WP35 correctly retains static unsupported-instruction refusal, including dead branches, rather than installing a reached-only exception. Its required handler fixtures need a narrowly qualified normal-root/nested-child QUIT context before full bounded implementation review.

WP39 supplies two fresh-copy observations per context, using reviewed WP38 reference helpers after its approval. It owns a new reference-only runner and evidence namespace; no product codec/writer, current conformance registry, historical catalogue or WP32 approved artifact changes. Its reviewed code-lane handoff is consumed directly by WP35. Adding WP39 as WP35's research prerequisite is explicit; all other38 prompt bytes remain unchanged, as do spec/plan and full38 obligations/91 groups. No active-handler QUIT, general stop/rollback/variable scope or full macro behavior is inferred. Existing approved Result API remains unchanged: actual sink receipts own document/session partial effects, and VM counters remain charged work.

This is a temporary authored draft until canonical validation/finalization, planning refresh and independent analysis actually complete. No new implementation, original run, approval or acceptance is claimed here. Existing original VM ownership remains explicit and exclusive.


WP39 actual canonical validate-only preflight passed:39 WPs/117 subtasks,1 new/38 initialized bootstrap records,18 lanes and no requirement-extraction/post-integration warnings. Its existing24 glob advisories are byte-identical to the prior finalized macro-tranche list and retain their individual source-lane/planned-new dispositions; the25th is the genuinely planned-new macro-quit evidence namespace declared in create_intent. The pure installed API returns zero ownership/glob errors and confirms all17 existing lane IDs unchanged, new WP39=lane-q and an acyclic WP38→WP39→WP35 dependency. The22 execution-mode advisories retain the previous21 dispositions plus new WP39: real scripts/reference Python is code_change despite the heuristic recognizing only src/ and tests/. No fake tests path, codebase-wide exemption or planning classification suppresses these warnings. The new WP39 branch-strategy wording is canonically standardized by finalization; no old prompt rewrite is required beyond the explicitly authored WP35 prerequisite. All37 other existing prompts/spec/plan are hash-unchanged. This checkpoint is preflight only; actual mutating finalization and planning refresh remain separate recorded actions.

Actual canonical finalization completed at `b251df97e57275f643554a6518b089a2aa6f140b`:39 WPs,1 new/38 existing bootstrap records,18 lanes; only new WP39 needed canonical metadata standardization. All37 other protected existing prompts/spec/plan remain byte-identical; WP35 has the explicit authored prerequisite only. Actual lane mapping equals the pure acyclic proof and preserves all old lane IDs. The exact continuation amendment is committed through spec-commit before the supported planning refresh. Independent current-task analysis is still required; no implementation, original QUIT result or approval is implied by bootstrap state.


### WP26 discovered immediate code-history prerequisite

Direct pair Delete/Backspace has body/gap proof in approved WP23's run_deletions, but the trace saves and enters interoperability without immediate F1. Approved04 EC045 deletes the opening code and then B/C with no interleaving before its Save/F1; newest plain BC therefore does not classify the preceding code deletion's history effect or older-entry retention. Existing normal-question No/F1/Escape proves body/directional skip, not history under a prior entry. WP26 correctly refuses to fabricate a code-deletion History effect.

A separate missing branch is closing-only blocked BoldOff repair: wp23-a-blocks-r1/r2 case block-4-1-y, CMD51-203, sourceN0024→finalN0025, Reveal selection[g4,g5), AltF4/Right/Backspace/Yes. Body remains A On BC Off D, outgoing g5/D-highlightcol15, indexed packet6 flag0→8, descriptor1172/counter1 retained. Its subsequent P0028 stream is unchanged-body+Z interoperability, not an immediate history proof. The observed opening-only follow-history repair Restore inserts literal Off+On; no closing symmetry follows.

WP40 is the new prerequisite, with T118–120 and disjoint reference code/evidence ownership. It adds eight direct boundary/view contexts and one closing-only blocked-repair auxiliary context, each two fresh original guests: maximum18. Each starts with a distinct plain-history sentinel created in the same document; view is set before seeding, and declared Right navigation separates its group before the target action. Thus the observation may classify entries/retention in this separated state; uninterrupted ASCII→code grouping remains unqualified. Normal direct deletion is Yes; Reveal bypasses its question. No code-question/blocked-operation cancellation matrix with prior history is added. Undelete preview's own F1 cancel is a distinct observed probe step.

First F1 after the target action precedes any Save, clear, retrieve or pane change. The entire overlaid preview row is not an entry string; hidden code fragments need actual Restore/native/cursor-marker evidence. Multiple indistinguishable entries or other unsupported outcomes remain explicit blockers rather than inferred empty history. WP40 consumes approved23 reference APIs and approved39 captured-state exit handling only after39 approval, avoiding the legacy Exit-doc1/doc2 assumption; original scratch/native data comes from original commands, not a host document writer.

Research depends only on04/13/23/39, never25/26/document/UI. WP26 explicitly depends on40 and consumes its owned handoff directly: no code→planning→code backedge, no edit to approved04 contracts. All current39 packages/117 subtasks remain, other38 prompts/spec/plan stay exact, and full38 obligations/91 groups remain open. The broader future native-lifecycle plan stays temporary with proposal labels; number40 belongs to this prerequisite. This is temporary authoring only until canonical validation/finalization/refresh and independent current-task analysis actually complete; no new run, implementation or approval is claimed.


Temporary installed-API proof for this amendment reports40 WPs/120 subtasks/19 lanes, new40=lane-r, all18 existing lane IDs preserved, zero ownership/glob errors and zero independent work-package collapses. Existing22 mode and25 glob advisories are unchanged; the new23rd mode advisory is the real Python reference source outside the heuristic src/tests convention, so code_change remains correct. The new26th glob advisory is the genuinely planned-new code-pair-history namespace declared in create_intent. The new literal runner path is likewise declared planned-new; no fake test directory, planning classification or codebase-wide exemption suppresses an advisory. This remains a pure temporary proof, not canonical validation/finalization or permission to run a guest.

Actual canonical WP40 validate-only preflight passed:40 WPs/120 subtasks,1 new/39 existing bootstrap records,19 lanes,zero independent collapses and empty requirement-extraction/post-integration warning arrays. Existing25 glob advisories are byte-identical to the prior39 preflight; new26th is the planned-new code-pair-history namespace with create_intent. All38 protected existing prompts/spec/plan remain byte-identical; only26 gains its explicit source-history prerequisite. Pure installed ownership/lane proof retains all18 prior IDs/new40=lane-r and23 mode advisories with the new real Python path disposition recorded above. This is preflight only; mutating finalization, exact continuation commit, supported planning refresh and independent analysis remain separately recorded.

Actual canonical finalization completed at `7412599b9c99c038310ea778cd9e4a2dc93759ce`:40 WPs/120 subtasks,1 new/39 initialized bootstrap records,19 lanes,zero prompt metadata updates and zero independent collapses. Canonical lane assignments match the pure installed proof, retaining all old18 IDs/new40lane-r. Protected spec/plan/other38 prompts remain exact. The continuation is committed through spec-commit before the supported planning refresh so every amendment artifact is in the recorded planning tree. Independent current-task analysis is still required; no original history result, code completion or acceptance is inferred.


### Inert archival Go source during planning propagation

WP40 actual lane discovery exposed a pre-existing packaging error: WP34 cycle1's data-only `image_alias_test.go` became a live Go package after planning snapshotc82fdb2 propagated. It imports implementation dependencies absent from the reference lane, causing broad Go test/vet setup failures even while actual inherited storage/reader packages pass. This is not a no-packages diagnostic and is not a new product source defect; retain those raw failures honestly.

Root coordination commit97285cf renames only that archival copy to `image_alias_test.go.txt`, with100% identical1618bytes/SHAf0fd99fa6d048da330255fa596d123fda37bdb29b623556b147b9b44eebadb18 and original Git blob retained. Original review manifest is archived unchanged, current manifest changes only the filename, and archival-source-packaging.json binds both paths and exact replay instructions using the historical overlay's temporary path. No native output, product source or review verdict changes. WP33's isolated evidence already has its own nested go.mod and is not discovered by enclosing go ./...; its deliberate source fixture remains unchanged.

The supported planning refresh after this recorded artifact-packaging amendment is required before35/40 full broad checks. Affected lanes keep their original baseline/fuzz evidence and refresh only planning metadata, then verify unchanged Go/test/corpus blobs plus actual discovery/build/test/vet. No acceptance-fuzz budget is repeated for an unchanged implementation/corpus merely because archived data stopped being treated as a package. Current task/spec/plan/charter identities are unchanged, so READY task-coherence analysis remains bound; this note grants no scope, test bypass or mission acceptance.


## Native lifecycle prerequisite tranche — proposed authoring checkpoint

Architecture cycle2 is DESIGN-READY with zero unresolved findings, not product approval. Proposed WP41 (A) adds distinct source-less absent-target storage requests through the existing transaction, preserving all loaded guards/cross-directory Save/34 Macro immutability. Proposed WP42 (B) owns original-resaved field qualification; WP43 (D) owns original genesis/default/state research. T121–129 are new; old40WPs/120subtasks/19lanes and prompts/spec/plan stay unchanged. Pure validation and exact protected hashes accompany the temporary draft; root must use supported validation/finalization and independent task analysis before dispatch.

Research42/43 use disjoint real Python+evidence namespaces and approved23/14/39 helpers, actual shared lock, offline frozen finite plans then explicit root oracle grant. Current planned caps42=12 and43=10 total guest attempts include failed/incomplete attempts and are not a grant; no live guest launched during authoring. No native schema/template/default/field permission is invented. Private original resources stay private. B/D do not depend on consuming document/editor/UI code.

Future C (document resave admission) waits actual B; E (native constructor) waits C, actual D schema refinement and approved document/storage prerequisites. Future F/G wait actual approved27/36 and28/37 consumer APIs; later sourced SaveAs preserves original loaded guard or New first anchor while displayed name/receipt may update. No source rebasing is planned. H follows actual executable proof into existing31 schema. Search, hard returns/flow, attribute creation, overwrite/backup/recovery and all resource/platform/language/layout/native/companion duties remain separate M1 work. All38 obligations/91groups/36lessons/nested leaves remain open; no task queue exhaustion/fullM1/M2 claim.

Expected41 continues existing storage lane-b;42/43 each need new research lanes determined by canonical compute. Code_change/new Python outside conventional src/tests may yield honest mode advisories; new evidence globs/literal runners have real create_intent. No bypass/scope exemption or fake tests-only ownership is selected. Any actual dependency/lane conflict blocks promotion until explicitly corrected.

Independent sealed alias investigation confirms three P2 failures on unchanged70e02f7 in one prepared-request ownership class. WP41/T121–123 explicitly repairs capture of accepted source/destination/stable opened-directory capability and introduces NewPublication through that repaired transaction. Rebound receiver must refuse before IO, same-capability copies retain real Close lifetime, original-source/absence guards remain mandatory, synchronous cross-directory Save/no-replace/uncertainty behavior remains. Exact red overlay failures→green permanent regressions and actual inherited consumer compatibility are required. This architecture/task delta awaits independent analysis; prior cycle2 readiness did not cover it, historical reviews and drafts stay sealed. No source fix or product approval is claimed. WP42/43 content and all47 protections remain unchanged.


## WP27 storage prerequisite amendment — captured loaded-source publication

WP27 now explicitly depends on approved WP41 in addition to WP17/24/25/26. Independent investigation found accepted source, destination and opened-directory authority could follow whole public-wrapper replacement; WP41 repaired that single prepared-request capture class while strengthening the existing WP24 public API. Source `5ad84e4` plus packaging receipt `0df934c`, independent review `0e383d5`, approval event `01M689XXRTW64NPDR38M7Z73K6` are the prerequisite authority. WP27 must consume the repaired loaded-source candidate path, privately own loaded-source/queued-intent/result observations and test public-wrapper/getter isolation, preserving revision/operation binding, actual Close and guard/outcome semantics. Original loaded guard, displayed name and last-publication receipt stay distinct; later Save As does not rebase the source guard. This is an explicit dependency/acceptance clarification, not new-publication or constructor scope. All other prompts, subtasks, requirements and ownership remain unchanged; all38 obligations/91 groups/full M1 and later modernization boundary remain open. Historical WP41–43 authoring/protection receipts remain exact historical evidence; this separate WP27 amendment is intentional and requires canonical finalization/planning refresh and independent current-task analysis before implementation.


## Proposed reordered-prefix continuation WP44–WP45 — temporary authored append

Planner-priti resolved with tasks action governance. Baseline protected planning
snapshot f70b0441052b62bb37dce4c4f6c418a30f140739, planning commit
1c476d4424812f585f535fcaf3935f4dde2d13ff, tasks SHA256
e68723af8470d38173f11ea5942c740ebb3eb5b3aa13d40851f100f206d79cf2.
All43 old prompts and all spec/plan/charters/manual prefixes stay byte-identical;
only tasks.md and continuation.md gain appends plus new44/45 prompts. Runtime
review/status metadata may advance independently; root must resnapshot actual
current metadata before any quiet-point promotion and never overwrite old prompts.

Frozen revision2 architecture decision e937280d61c849786ffddb894b6fe95c30272557df77dc5ab164ad1386521a2f,
manifest1da96b9017561ba65913b8204687e63081293fc701e855bf2cb9f91ea1d3987c,
seals8c1d987743c328b9948235c34e6f8d9b7610982df33f4dd9285ced27fa42defa,
independent cycle2 reportb5a7e37c97cca3a0c24a3d5f3d4f792f9898e11973657ca7c7c0865c094bf44e /
seals8dedd710a5c96c992ffd26c63680ca851edab74ab8ae11c2d38ea9f7cf6418ac
are exact proposed copies under docs/research/continuation/reordered-prefix-design/.
Current decision/review are design-ready with R1 resolved, zero architecture
findings; history/revision1 and full cycle1 rejection/proof remain. Exact-byte
promotion-receipt.json changes placement only, with zero content replacements;
build-manifest.py remains historical revision1-only, not a revision2 generator.
No design/implementation/native/product/M1 approval or VM grant is invented.

WP44 depends directly25/26/42 and owns only internal/document/**, sequential on
existing lane-e. It adds one private structural72-field admission order6/7/15/12/8
with actual e724/counter01 and original00/emitter08 policy, preserves old-order
rules and all25/26 operation/identity/history/provenance/CountKnown guards, and
refuses FIN1172/02, unobserved1172/01/e724/02 and all564/deleted/slack families.
Actual public Go producer classes are measured by whole bytes after production;
every command/provenance test is retained, two fresh original witnesses per
native class plus any matched original controls are frozen/count-budgeted before
requesting root release. Captured FastSaveNo, exact indexed00→08 difference only,
actual admitted e724/01 pre-print original snapshot→second Go edit, complete PRN
and independent reopen/refusal are mandatory. Counter02/post-print or unadmitted
pre-print results cannot substitute; no normalization or skipped acceptance.

WP45 depends directly23/14/22/39/42 and owns new runner/evidence paths. Actual
installed conservative ownership computation places42→45 sequentially on existing
lane-s because resaved-prefix/** overlaps resaved-prefix-relationships/**. Stage1 audits all72 current images/SDK typed fields, active roots,
old/current indexes/aliases/residual extents first.63 literal matches are provenance
only, not deadness/reference authority; truncated70-byte font-tail and unowned4
printer-tail bytes need actual field/reference argument or remain blocked. A
negative/unresolved read-only handoff is valid. Stage2 is conditional on an actual
discriminable remaining original behavior, separately reviewed/frozen/root-granted:
max4 total attempts including failures, existing max2Bold G3/FIN ×two fresh only.
No source rewriting, automatic VM, uncounted calibration or consumer dependency.

Actual installed pure-compute proof is45 work packages/135 authored subtasks/21 lanes,
old21 identities unchanged,44 on lane-e,45 on existing lane-s after42. Initial static
22/lane-u prediction was wrong and is preserved in the temporary superseded-history
archive; frozen architecture's predicted22 remains historical, not finalization.
Existing document overlap is dependency-ordered via25/26; added cross-lane s→e has
no reverse path. Research lane-s depends d/j/k/q; no e→s prerequisite exists. New
path ownership is truthful even though conservative prefix matching co-locates it.
No independent collapse, namespace workaround, ownership migration, fake planning
classification, exemption, private tool patch or lane-cycle bypass is proposed.
Installed pure computation is not canonical finalization. Approved42 source stays
pinned d77c5f550b821e2c2e18ec8b794ede9a5bc26d22, never a moving lane-s/45 tip.
Root owns later primary promotion, actual canonical preflight/finalize/planning
commit refresh and independent current-task analysis; none ran in this draft.

New45 namespace/create-intent is genuine; no empty directory or production script
has been created in the repository. Runtime warnings must be inspected at actual
preflight, not dismissed in advance.43 approved source remains untouched. This tranche authors no E; any future E consumes real C/43/schema/storage prerequisites; current27/28/UI/old
contracts remain unchanged. All38/91/36/nested leaves/fullM1 and SC001–005 remain;
no parent/FR/registry/acceptance-matrix closure, accept/merge or M2/PDF.


## WP36 T108 Save/history clarification and explicit WP29 prerequisite

Independent P2R1 diagnosis (report2b09ff85a9d0a10d358617d718e06a6c2a7d66f84f9f5fa3ddf8c09e53ba0ffa;seals2c358c8a52f8d5ebb4cd7b32e754b4caf64e8dcebba996c736eda18f5404464f) proves approved27/28 ordinary F10 is incorrectly blocked by optional bounded-history qualification. The retained ninth actual WP29 PTY run and independent public reducer fail after exact40 paired deletion; both original23 immediate-F10 repetitions establish the ordinary filename/save path without establishing post-Save hidden history. Current successful Save also silently retains prior eligibility if Separate fails. This is a narrow editor-only T108 requirement clarification, not document/history reset, generic error bypass, UI ownership or unreviewed44 admission. Preserve native/cursor/source/dirty/fragments/provenance, immutable forks and unique Transition controls; after F10 conservatively withhold current-session unsupported history continuation across filename cancel/failure/stale/uncertain/success while retaining old immutable evidence.

WP29 now directly depends on WP36 (29 dependency list includes36; prerequisite flow36G→29L). WP36 depends on neither29 nor28/UI; source36 repair consumes immutable diagnosis evidence promoted separately by root. After independent36 repair approval, WP29 performs supported normal reentry/composition with actual28 and approved36, fresh full-closure rebuild/real immediate-F10 PTY green proof, then native/original differential work. Its blocked raw9th/eight earlier records remain; full-history/extra edit/navigation/Restore or manual source overlays cannot replace the immediate recipe.

No new WPs/task IDs/ownership or dependency44 change. Existing45WPs/135subtasks/21lane IDs and all38 obligations/91groups/36lessons/fullM1 stay retained. T108's current done status is not hand-edited by this amendment; root will reopen it through supported CLI under coordination before repair/review. Scoped diagnosis and exact inert repro/seals/metadata are proposed as an explicit separately promoted planning amendment with path-only receipt, not hidden code-owned planning edits. Actual canonical finalization/planning refresh and independent current-task analysis remain root's later gates; this temporary proposal grants no implementation verdict, task lifecycle, VM or full-M1/M2 acceptance.

## Future WP46 proposal — closed native constructor after actual approved C

WP46/T136–T138 is a temporary future E proposal, not a canonical task or implementation/guest permission. It depends explicitly on actual approved25/26/43/44, sequentially owns existing internal/document/** lane-e and has no storage/editor/TUI/research-consumer reverse edge. Actual44 source/private admission integration is unresolved until its independent implementation approval and later claim; architecture readiness or a moving lane tip cannot substitute. This proposal is resnapshotted on clean4a83b601 with45 current prompts and21 lane IDs protected, including the canonically analyzed36T108 Save/history requirement amendment and29 prerequisite36. All14 actual C classes/control interoperability must be independently approved before46 implementation; partial family qualification is insufficient. Root still performs canonical promotion/validation/current-task analysis before claim.

E architecture cycle2 is DESIGN-READY, with exact decision39a400e3/schemafa2047ed/manifesta002c62f/sealscab109b9 and reviewf5ef665e/sealscb308fdd. Its independent R1 correction selects independently authored private immutable typed serialization metadata and explicit one-profile DOS text initialization120/1/0/0. All72 fields/index encodings remain individually explained. No mandatory runtime proprietary SET/PRS/provider or generic font/hash/metrics algorithm, prefix template, raw config override, resource IO or automatic extra research/VM is introduced. Original43 source90ea1d4f and reviewd0736d0/event01M68ERSV6994PNYGGZJ1CF606 establish original-only inputs; generated New output and actual interoperability remain mandatory.

The future package preserves immutable New/Loaded birth, private revisions/history/receipts and lifetime New NoLoadedOriginal, with Loaded OriginalExport unchanged. Real New empty/ASCII candidates must traverse original Retrieve/edit/FastSaveNo/admitted pre-print Save and real Go reopen/re-edit, complete logical-control-matched PRN, normalDOS/owned stop/extraction/master/shared-lock release. Actual whole-native classes, two fresh per class and counted controls/exact total failure-inclusive budget freeze before separate root grant. Later editor publication uses41's actual source-less transaction/first matching Read-bind; this package does not implement it or migrate later guards.

Prior full architecture revision, cycle1 rejection/R1 receipt and cycle2 approval are proposed as exact separately reviewed planning evidence; path-only copy receipt and repository-relative ADR preserve their hashes and history. No design/product/full-M1 approval is inferred from a prompt or queue. All38 obligations/91groups/36lessons/discovered leaves, broader resource/layout/format/companion/platform/language/UI/overwrite/recovery duties remain open; M2/PDF waits for genuine M1 acceptance.

## Constructor consumers: startup New and authentic first source binding

WP47/T139–T141 and WP48/T142–T144 are a future two-owner continuation of actual46, not broader codec/storage rewrite or full M1 acceptance. Independently design-ready N1 decision2c5c875f and review3f907b58 resolve actual41 final Identity/capability/receipt constraints. Pure editor47 (existing editor scope) consumes actual independently approved46 New/origin identity and41 plus36 history/transition safeguards; live host48 (existing TUI/cmd scope) waits actual37 and47. Source-less transaction→actual same-capability Read first-bind preserves the live New native object and lifetimeNoLoadedOriginal, then retains first source across later sourced SaveAs. A template, nil-source heuristic, ordinary Retrieve/Parse or fabricated receipt cannot substitute.

Startup unmodifiedness, saved revision, committed name, first source, native birth and last receipt remain separate. Successful publication is not clean until authentic matching rooted Read; full final41 Identity and bytes are checked after its cleanup semantics. Published-unbound allows explicit same-receipt Read-only retry; unknown/possibly-effective publication has no automatic republish/re-Observe reconciliation. Pending/late/Close/fork/counter/candidate/public-wrapper handling uses private accepted request authority; DirectoryID/inode/counters alone cannot mint it. Actual46 code/API remains a hard future prerequisite, no architecture verdict silently approves it.

Scope is captured43 fresh-start empty/ASCII F10/name/F1/retry, with actual host safety distinctions. Post-F7 typing/global-history/second-screen reset, unqualified macro-new target, hard-return/paragraph/flow/layout/printing, overwrite/backup/recovery and remaining commands remain separate M1 duties. Host48 must use the actual production executable and41 storage, not helper output; exact original/native evidence reuse requires actual bytes/profile/command preconditions, otherwise measured finite two-fresh/control plan and separate root grant. Current conformance ingestion remains separate31/future ownership. All38 obligations/91groups/36lessons/discovered leaves and M2/PDF boundary remain unchanged.

This temporary draft does not mutate current tasks/status/events/lanes or authorize source/VM work. Independent task review, installed ownership/lane validation, root canonical finalization/full planning snapshot/refresh and independent actual CURRENT analysis precede claims. Architecture/history/review promotion is separately exact/path-only; no source-owned planning edits or runtime mirroring.

## Next original layout rule handoff before product rendering

Future WP49/T145–T147 is an offline-first research continuation of approved07/14/21/43, independent of consuming constructor/editor/TUI code. Existing native/settings/fullPRN/profile evidence must support any closed typed rule, field units/resource precondition and unsupported predicate. Complete printer-stream initialization/termination, original character/code boundaries and native differences around the complete port-configuration/print/following-Save protocol remain explicit, without print-alone causation. No guessed10cpi/6lpi/physical glyph/default semantics, copied output emitter or blanket resource-provider requirement is introduced. An honest unresolved/read-only result is valid and never enables layout, mutation or preview.

The first stage has zero guest permission. Only a concrete discriminating missing fact can justify a separately sealed/reviewed/root-granted finite Stage2 of at most4 fresh attempts including failures/twofresh per needed case/control; otherwise NOStage2 conclusion remains. Actual stopped-owned custody/transitive preflight/fullraw/master/firstfault controls apply. Later pure layout/emitter and editable Return/Enter/history are separately scoped after real evidence/architecture. All38/91/36/nested-leaf/fullM1 obligations, original formats and M2/PDF boundary remain. This temporary task is not canonical/source/VM permission until independent review, installed validation, root finalization/full planning snapshot/refresh and actual current-task analysis.


## WP50 next native-merge reader tranche — task proposal only

Append one coherent WP50/T148–T150, depending actual approved02/09/13/14/21 and owning only genuinely new internal/merge/native/**. This is temporary task authoring; canonical validation/finalization, exact planning refresh, independent current-task analysis READY and claim remain root-controlled later steps. No WP51 is authored. Active47/48/49, New46, document writer, WPM compiler and shared lane tips supply no borrowed merge authority.

Sealed read-only reconnaissance proves15 original merge contexts ×2 repetitions,104 exports/35 native hashes, with original run/capture/archive/profile seals and exact approved e7de0804 parser no-edit witnesses. The task-planning review bundle retains exact inert copies and a source path map. Actual original behavior, implemented outer framing, this future semantic reader, pure execution and actual cmd/wordling merge remain different evidence levels.

The bounded reader preserves complete native bytes and absolute source-owned spans through wp51.Parse; explicit Primary/Secondary/Result roles cannot turn result framing into program admission. It inspects11 original DE values and outside-frame FIELD/IF BLANK/NEST tilde operands. END RECORD(count2) with only one END FIELD, genuinely empty fields and native0A/D4/0C interstitials must be proved from existing source/manual evidence or kept as typed blockers; no guessed strip/decrement/layout rules. No native serializer, sidecar/shadow document, interpreter/WPM VM, storage/editor/TUI or original guest action is included.

T150 requires production public-API source/span witnesses over all104 exports, immutable/source/wrapper/role guarantees and negative/malformed/semantic/unknown/boundary/race/resource/actual60s+600s fuzz/mutant evidence. Unknown retained bytes cannot silently count as execution success. First consumer is a separately planned/reviewed pure merge executor conditional on this admission contract; do not invent a task/ID/lifecycle for it now. Later merged-native output field/offset/cache/flag authority and actual original verification remain prerequisites before native output/editor/UI integration.

All38 obligations/91groups/36lessons/nested leaves and SC001–005 remain open obligations; WB23/24 and merge-related WB25/28 are not covered by scratch-file component inspection. All existing coverage/remaining-field contracts remain unchanged. No parent/FR/canonical verified-status closure, no accept/merge from queue exhaustion, no M2/PDF start, no original/resource/physical qualification silently removed.

Retained specific New46 follow-up (scope fact only, not WP50 prerequisite/merge-byte authority): approved46 source44aab36a, independent reviewc5898570, approval event01M693SP6NGQX478A0VA67KMJX retains the newly observed H1 empty-print-plus-following-Save native result e724/counter02 FIN. Current C44 correctly reopens that result losslessly READONLY with UnsupportedMetadata74+1; editing admission is not qualified. Both fresh v3 controls and Go New candidates qualify this bounded observation. H2 is not observed. A separate future closed-family/mutation original differential and admission review must address H1; do not widen C44, launch a VM or add that scope to50. The46 ledger retains old8 plus new4 qualified and1 historical incomplete, cumulative13; this bookkeeping is not a new grant or broader original qualification.
