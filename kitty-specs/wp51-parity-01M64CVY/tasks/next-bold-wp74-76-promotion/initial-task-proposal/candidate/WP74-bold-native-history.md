---
work_package_id: WP74
title: E semantic Bold and immutable history
dependencies:
- WP70
- WP46
- WP59
requirement_refs:
- FR-004
- FR-005
- FR-006
- FR-008
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
- C-003
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Existing feat/wp51-parity planning/landing setup retained; actual
  issued source is dependency-specific approved integration, never primary source
  overlay.
subtasks:
- T220
- T221
- T222
phase: Tentative bounded Bold slice; full M1 OPEN
history: []
authoritative_surface: internal/document/
owned_files:
- internal/document/**
create_intent:
- internal/document/bold_authoring.go
- internal/document/bold_authoring_test.go
- internal/document/evidence/bold-authoring/
execution_mode: code_change
agent_profile: implementer-ivan
role: implementer
task_type: implementation
---

# WP74 — E semantic Bold and immutable history

These are TMP-only tentative mechanical identities, NOT finalized tasks, source claims or implementation authority. Historical PROPOSAL ONLY labels in the verbatim annexes retain their historical stage; ADOPTION.md at primary02d8271fd483e1105efa54feb2908e190cb2e597 adopts the exact independently reviewed design for task authoring. All applicable clauses of the verbatim annexes below are mandatory, including finite acceptance, resources and complete custody. A body scope narrower than routing metadata controls actual execution. No scope/API/budget/driver/test change without precise independent amendment. DIFFERENT independent TASK review and ROOT normal finalization/analysis/source claim must precede execution; DIFFERENT CODE review precedes downstream consumption.

Source is actual approved H73 5bd5105e9014a839ea95c5b2efd21548ccd8756b (normal event01M6CYVMQKVCA2Y5SY7WPYNRE9), with inherited H71 cd983c05401a90c1f0c912c60ab6ca23d8bd437b, G65 f110c5a7e113b063081879ea491c1dde5bf79aed and E68fix50789739e70cbf2d59999df27d2acefb25a01489. Primary has planning only: missing primary product paths are not missing approved source. NEVER read/import uncommitted unapproved WP70 prototype as product dependency. No source copying/overlay/host repair. Every future issued claim must rebind actual approved integration and complete CUSTODY before edits; mismatch or failed fit stops before code. Source requirement is an approved integration pin, not an E dependency on a later H consumer or permission for cross-lane backedges.

The whole123-member adopted bundle is `tasks/next-bold-authoring-contract/`, outer1cc12fae4fb2d6fb20ae97207cf57b10032bb701511ab733dc2f01f9e0dbf9ee. Mandatory exact references: ADOPTION.md; revised-proposal/{CONTRACT.md,ARCHITECTURE.md,ACCEPTANCE.md,BOUNDARIES.json,CUSTODY.md}; initial-proposal/{source-bindings.json,evidence-levels.json}; closure-review/REPORT.md and its original whole source/research/review maps. `adopted-whole-map.json` in the task proposal binds all123 files without duplicating the historical payloads. Closure root06163eac993b126dc77d51d1f13fb9b45111876833323db113b37594bca18e29; CUSTODY55fe1adf3426fa51cc9ec6f1b7f7e97826aeda14610a9ffebc51f1146524e3b9; ACCEPTANCE666af52be29eb2ae7641ba5f2a087e527f444b1b2734edc2cb2032e59523a7c5. Closure approves design only.

Evidence interpretation: June1992 intermediate paired insertion is DOCUMENTARY; completed March CMD51-048 smoke02/03 normal+Reveal and CMD51-204 advanced03/04 completed native body are historical witnesses; HOST refusals/capacity/recovery/unknown-history policies are explicit host additions. No fresh Original/native differential claim. Full37M1 obligations plus FC010 M2 gate,91groups/36lessons and SC001–005 remain OPEN. No PDF/M2.

Preserve every inherited test/fixture/evidence byte and protected paths enumerated in BOUNDARIES. Zero old test amendments. Publisher/admission/document/new/deletion/history_observation/editing/input/storage/cmd/modules/macro and73 guards stay frozen except exact owned old amendments. No P/private/VM/reference/parser/compiler/product execution while authoring this proposal. Later code verification uses only actual issued source and the closed finite acceptance; no parser replacement or guessed Go reader APIs.

## Routing and source coordination

WP59 is also an explicit source-coordination predecessor because namespace routing overlaps its approved native catalogue files/evidence; no catalogue API/source modification follows. WP70 is an explicit SOURCE-COORDINATION dependency only: model routes WP74 into the existing E lane shared with active70. It is not a Bold API/product dependency and no prototype may be read or imported. This tentative metadata waits for normal70 resolution/quietpoint and a ROOT-issued source rebind to the actual approved H73 integration, with any subsequently approved unrelated changes fully audited. It does not authorize committing/approving70, overwriting its worktree, or claiming a quietpoint exists. If normal claim routing cannot supply that approved integration safely, STOP for reviewed coordination amendment. Do not create a H73 backedge (it produces an E→H→G→E lane cycle).

`owned_files: [internal/document/**]` is supported namespace routing; zero-match advisories remain honest on planning primary. Only genuinely new files/namespaces are create_intent. This metadata cannot grant any path outside the following CLOSED allowlist:

```json
{
  "name": "E semantic Bold/history",
  "depends_on": [
    "actual approved native/admission/mutation/history source",
    "actual approved H73 5bd5105e9014a839ea95c5b2efd21548ccd8756b full inherited approved source integration point; no moving70 dependency"
  ],
  "amend_existing": [
    "internal/document/history.go",
    "internal/document/README.md"
  ],
  "create_files": [
    "internal/document/bold_authoring.go",
    "internal/document/bold_authoring_test.go"
  ],
  "create_namespaces": [
    "internal/document/evidence/bold-authoring/"
  ],
  "namespace_executable_literals": [
    "internal/document/evidence/bold-authoring/collect.py",
    "internal/document/evidence/bold-authoring/mutants.py"
  ],
  "new_public_api_exact": [
    "type BoldResult struct (opaque immutable; no exported fields)",
    "type BoldSpan struct (opaque immutable; no exported fields)",
    "func (d *Document) BeginBold(c Cursor) (BoldResult, error)",
    "func (d *Document) CloseBold(c Cursor, active BoldSpan) (BoldResult, error)",
    "func (r BoldResult) Document() *Document (copied immutable wrapper; zero returns nil)",
    "func (r BoldResult) Cursor() Cursor (zero returns zero)",
    "func (r BoldResult) Changed() bool (zero returns false)",
    "func (h History) AfterBold(r BoldResult) (History, error)",
    "func (h History) ActiveBold(d *Document) (BoldSpan, bool) (read-only; false for wrong/invalid native owner)",
    "Category constants UnsupportedBoldContext, EmptyBoldSpan, InvalidBoldResult, InvalidBoldSpan"
  ],
  "existing_public_signature_changes": [],
  "private_changes": "historyState adds one private immutable formatting-provenance handle; AfterEdit integrates authentic receipt-bound active advancement/closed-lineage invalidation. Private helpers/types only in the two named production files; no payload ancestry/global maps/reset/unsafe."
}
```

## Three subtasks and completion

### T220

Before source edits complete actual approved-integration rebind, current full custody/fit and public test-first contract; implement opaque immutable BoldResult/BoldSpan and exact BeginBold/CloseBold authentic native operations within closed scope.

### T221

Integrate authentic History.AfterBold/ActiveBold(actualDoc) and receipt-validated private AfterEdit ACTIVE advancement/CLOSED invalidation, atomic immutable ownership, unknown history and stale/replay/foreign refusal; preserve all plain-history behavior.

### T222

Prove the full E acceptance, reachable/dominant bounds, allocations, finite compile-valid semantic mutants and complete raw/protected-path custody; update only own README and submit DIFFERENT CODE review.

Each subtask is mandatory. No status completion follows from this prompt. Full package acceptance and unchanged-protected-source proof are required for DIFFERENT CODE review. E/G do not run H PTYs; H owns the sole 2+1 campaign. All shared caps include every failure/history/nested seal.

## Adopted normative annex: CONTRACT.md

# Proposed contract: bounded F6 Bold authoring before first save

**PROPOSAL ONLY — NOT APPROVED.** Audience: ROOT, the DIFFERENT independent contract reviewer and the future task planner. Normative words in this document define the candidate being reviewed, not present implementation authority. No work-package IDs, runtime lane, source claim, canonical edit or reference grant is reserved. The companion ARCHITECTURE.md, ACCEPTANCE.md, BOUNDARIES.json, source-bindings.json and evidence-levels.json form this proposal. Independent approval, final approved-source rebind, actual task authoring/review/normal gates and issued implementation claims remain required.

## Purpose, source and evidence level

Create real native Bold boundaries with ordinary F6, type through the existing actual ASCII edit path, close a nonempty span, type plain suffixes, inspect Reveal and save through existing rooted workflows. This is one part of FR004/005/006/008 and native/failure/evidence/stack constraints; it does not complete formatting, Reveal Codes or M1. Original native/companion formats remain permanent; PDF stays M2. All37 M1 obligations plus FC010's M2 gate,91groups/36lessons/nestedSC001–005 remain OPEN.

Approved semantic design source is H71 cd983c05401a90c1f0c912c60ab6ca23d8bd437b with inherited G65 f110c5a7e113b063081879ea491c1dde5bf79aed. H73 source5bd5105e9014a839ea95c5b2efd21548ccd8756b is now ACTUALLY approved by normal event01M6CYVMQKVCA2Y5SY7WPYNRE9 (reviewer-renata/codex/modelnull/forcefalse); ROOT proof is bound in source-bindings.json. The proposal was explicitly rebound from its earlier provisional status. Relevant H73 hooks are read/pinned in full; every later issued task must still check actual claimed source against this approved base. No moving70 API is assumed. Existing immutable public outputs, not a fresh original execution, support completed March F6 authoring; June1992 later manual supports intermediate paired insertion. HOST limits/refusals below are explicit additions to bounded admission, not original behavior claims.

## Candidate cohort and phases

The G command is a new `editor.Bold` enumerator APPENDED to Command, preserving every old value. Admission requires actual initialized current Session, Editing, screen1, ordinary Insert, no selection/Home-prefix/prompt/Session notice, no pending operation/target/fromExit/newMacro/macro delivery/repeat setup, genuine constructor New Birth, source=nil, NewUnpublished, valid nonzero genesis/native owners, and `historyValid=true`. No publication/binding/result/destination effect may have occurred; sequence must be0, name/draft/original and saved/published names empty, saved/published revisions and first/last/detached/publication receipts absent, historyUsed=false and first-publication state absent. A matching byte image or borrowed Snapshot cannot supply these identities.

A **new span** may begin only at actual native EOF, Reveal hidden, under unchanged whole mutation admission, and with capacity reserved for BOTH inserted boundaries AND at least ONE recovery ASCII character: current owners<=4096-3 and current native bytes<=65536-7, also within the unchanged E owner ceiling. Begin itself adds2owners/6bytes; this extra HOST reservation guarantees a rejected empty close is recoverable by typing one character and closing. Before the first span, body is printable ASCII only and History owns THIS native with qualified known count0, no stored deletion, observation or unknown grouping. This is the actual constructor/ordinary-text history chain, not NewHistory called on a later image. Before a second span, the History must instead carry this feature's authentic CLOSED provenance, own the current native and still have zero retained deletions. Native body must contain exactly its earlier completed pair plus printable ASCII; caller counters are not authority. No third pair, nesting, loaded context, preexisting foreign Bold or earlier unrelated unknown-history state is admitted.

The only phase authority is private E History formatting provenance with an opaque active BoldSpan. `History.ActiveBold(d)` reports active ONLY when its native owner/span match the actual supplied Document; old retained history after clear/retrieve cannot make another buffer active. A false result is not permission to construct a new span; the complete new-span cohort still applies. H adds no formatting state; G adds no shadow document or public setter. Phases:

| Phase / delivered event | Required result |
| --- | --- |
| First/eligible CLOSED + Bold | E creates BOTH real native boundaries at EOF, cursor immediately before Off; authenticated result/history adopted atomically. Phase becomes ACTIVE-EMPTY. |
| ACTIVE-EMPTY or ACTIVE-NONEMPTY + nonempty printable ASCII Text | Existing InsertASCII at the actual current Off; authentic ASCII receipt advances BOTH History's native owner and the private active span. Phase becomes/remains ACTIVE-NONEMPTY. |
| ACTIVE-NONEMPTY + Bold | E validates actual span/current native/cursor at Off, returns authentic cursor-only close across Off to EOF. No native-byte/revision change; History phase CLOSED, still unknown. |
| ACTIVE-EMPTY + Bold | Explicit HOST refusal; whole Session/native/history/cursor unchanged, no IO and no removal of empty codes. Typing can recover. |
| ACTIVE + Reveal | Existing view toggle only; it does not close, rewrite or rearm the pair. Next Text/close uses the authentic current cursor Reveal flag. |
| ACTIVE + F7 | Existing Save document? question, preserving active ownership and bytes; existing No→ExitQuestion and its F1/No/Escape/Yes branches remain unchanged. No-save normal exit/discard remains available. |
| ACTIVE + any save-producing route | HOST refusal before state/sequence/target/mode mutation or IO intent. Preserve entire input Session. See save table. |
| ACTIVE Editing + any other semantic command | HOST refusal, conserving whole Session. In particular Left/Right/Home/Up/Insert/Block/Delete/Backspace/F1/Enter/Escape/Macro/SwitchDocument/Restore/Previous do not move or lose the span. |
| CLOSED + ordinary commands | Preserve existing semantics. Ordinary EOF ASCII append may retain authentic feature provenance; a real nonappend/overwrite/other native edit irreversibly invalidates future F6 eligibility while retaining unknown history. It never qualifies history. |
| After any Save attempt that invalidates history, after binding/source acquisition, or after `historyValid=false` | ALL later F6 refused BEFORE E candidate creation, even if bytes/counters/gap match. Ordinary Text/save/Reveal retain old behavior. No late requalification or history-owner repair. |

Active Text is nonempty actual printable ASCII, Insert semantics only; it must fit existing16384owner/65536native-byte bounds AND4096presentation-owner ceiling before mutation. No active Typeover, paste expansion, newline/control/Unicode, code injection or split multi-event transaction. One delivered Text may contain multiple printable ASCII bytes within the same finite bounds; existing authoritative insertion remains one native transition. Cursor stays immediately before the SAME closing owner advanced by the authentic receipt. Begin adds exactly2owners and6body bytes using the already interpreted Bold identity, never literal label strings. Close requires at least one inserted character in this span. No empty close, automatic pruning, native flag normalization or active-save semantics are guessed.

Global H message behavior remains existing behavior: actual asynchronous receipts/control/resize/admin messages MUST retain existing handlers and uncertainty. Non-command input (release, repeat rejection, paste/unknown notices, resize, capability/version/environment/color) cannot install/mutate/consume formatting ownership. Unlike73's transient count, a real native pair is NOT abandoned on such a message. Stale Model Update still fails claimUI first. No source/owner reset to recover. F6 is an actual bare nonrepeat F6 Press with zero modifiers and empty Text, routed after existing73 pending-count/menu/uncertainty/IO/macro handling. A pending73 count consumes/refuses F6 by its existing grammar; a shown menu retains its existing unsupported-action behavior. Unsupported F6-shaped modifier/text events cannot alias Text.

H must retain real runtime/currentUI/pending/reconciliation/macro/frozen guards. Its private adapter requires no count/legacy-repeat/shown-menu, unsettled/first IO, macro/ticket/CPU/deferred/frozen or nonzero MacroStatus, and under the existing runtime lock nonstopping/currentUI/no runtime macro plus issued/results/executed/firstTickets/macroResults empty. It does not consult a caller boolean or clear a notice. A benign prior H diagnostic is not an ownership permit or an unconditional veto: do not proactively clear it to qualify; a genuine admitted G operation can clear it through existing m.reduce. This allows nonempty close after a rejected active key or exhausted insertion. Hidden menu diagnostics similarly grant no permission and must not force a trapped active state. Semantic Session notices and IO uncertainty still prohibit admission. State/View cannot consume/rearm format state; honest unknown history keeps the actual legacy native Reveal fallback.

## Authentic native/result/history contract

The exact proposed E API is in BOUNDARIES.json. BoldResult/BoldSpan are opaque immutable values with no exported fields, raw-body inputs, constructors, setters, counters-as-authority or IO rights. Zero/forged/stale/mixed-owner values refuse against the ACTUAL current owner. Pure operations on matching copied immutable prestate may produce independent values; they do not consume a global token or grant UI/IO authority. Replay tests use current closed history/current native, not a demand that old pure values mutate themselves. Private identities must be nonzero-sized and genuinely distinct, not zero-size allocations whose addresses may alias. Receipts retain at most their actual before/after native revisions and current cursor; no persistent ancestry chain/payload cache/global mutable ownership is added.

BeginBold requires actual valid New Birth and real EOF outside Bold; it MUST keep existing private publishBody, prefix/packet/Birth behavior, all full input/output admission and2pair/16384owner/65536byte ceilings. It prechecks delta capacity using bounded subtraction before new body/result construction. It creates a COMPLETE balanced candidate and calls the existing publisher with forceFormat=false. The repair-only waiver is not widened. CloseBold MUST validate complete admission, opaque span/native match, actual On/Off owners/EOF shape and real cursor at Off, and returns an authentic unchanged-document/cursor-crossing receipt. A copied public bool/label/token count cannot close it.

History.AfterBold validates its actual before-native owner and the authentic domain result. First entry requires the genuine qualified zero-deletion cohort; subsequent entry requires the private CLOSED lineage, NOT merely effectUnqualified/count0. It preserves all stored fragments/count/provenance, binds the new current native and active span, marks effect unqualified/count unknown, terminates any grouping knowledge and invalidates unrelated seed qualification. No original stack-empty assertion follows. Closing validates the SAME active span receipt, changes private phase to CLOSED and preserves unknown status; replay against already CLOSED history refuses even though native bytes/revision are unchanged.

History.AfterEdit retains its public signature and all old ASCII receipt validation. New private formatting handling occurs only after that authentic validation. While ACTIVE it accepts only an actual nonreplacement insertion at that span's current Off, checks resultant owner/count/cursor and updates the span to the actual new native with Off shifted by input length; unrelated edits return the OLD history/error, so G discards the tentative native result. CLOSED EOF append can retain lineage; nonappend/overwrite clears future formatting lineage while effect/count remain unknown. Plain existing histories retain EXACT old behavior. No ASCII receipt is fabricated for formatting; public result fields do not supply the proof.

G stages the E result, validates History.AfterBold, then adopts native/cursor/history/provenance together. Begin increments Session.Revision exactly once because native revision changed. Cursor-only close preserves native revision and Session.Revision just like existing cursor moves, but records Bold provenance and advances the genuine reducer transition through the existing Reduce wrapper. No operation/sequence/IO is issued. Failure adopts nothing; complete old Session/native/history/receipt/cursor values survive. Native Bold styles/labels derive from the actual tokens, not H formatting flags.

After the first save's unknown-history waiver sets historyValid=false, Text intentionally skips History.AfterEdit and can leave the retained old handle bound to an older native. This is existing behavior and MUST NOT be “repaired” here. G's early historyValid/source/NewPhase refusal makes later F6 unsupported before any E call. Source acquisition/binding, clear/Doc2, wrong native/history owner and unrelated history unknownness likewise cannot regain the cohort. Post-format Delete/Backspace/Undelete remains the existing explicit unsupported-history outcome. No old history tests may be weakened to disguise that limitation.

## Authoritative save-route table

`boldActiveGuard` is a proposed PRIVATE G policy hook after basic event-payload validation and after the existing Complete dispatch, before any user transition. It is mode-aware; active F7 exit questions are NOT treated as Editing Text. `boldWriteGuard` is a proposed PRIVATE additional intent fence. Neither is a H-only key filter.

| Actual source route | ACTIVE policy | CLOSED policy / invariant |
| --- | --- | --- |
| Editing Save→saveHistoryInterleaving→filename(SaveName) | Refuse before history invalidation or mode/fromExit changes. | Existing unknown-history waiver can set historyValid=false; do not reset fragments. Later F6 permanently refused. |
| ExitSaveQuestion Escape→filename(SaveName), fromExit=true | Refuse before either change. | Existing route remains, including inherited `fromExit` Enter refusal; do NOT implement save-on-exit. |
| ExitSaveQuestion Yes or other attempted save answer | Explicit active save refusal; do not invent a Yes-save branch. | Existing unsupported branch remains unsupported. |
| SaveName Enter (including manufactured defensive active+SaveName state) | Refuse before draft/lastSave/resolve/Observe/sequence effects. | Existing edited-prefill/fromExit/name/path/Observe rules unchanged. |
| ReplaceQuestion Yes | Refuse before target/export/overwrite/begin. | Existing replacement refusals/same-source-only no-op remain; no new overwrite permission. No/Cancel behavior unchanged in actual reachable contexts. |
| generic begin(Observe/WriteSnapshot/PublishCandidate) | Defensive fence before sequence/pending/candidate/IO creation. | Existing immutable candidate/source/publication constraints unchanged. |
| Observe Complete→firstIntent(PublishNewBuffer) or begin(write kind) | Do not suppress actual Complete/receipts. Defensive write fence prevents a new write from inconsistent active+pending state. | Real completion retains existing attached/detached/uncertain handling; no fabricated rollback. Such active+IO conjunction is structurally supplemental, not a positive public setup. |
| firstIntent(PublishNewBuffer) | Fence before native Export/request identity/sequence/phase/intent. | Genuine New Birth/current transition/directory/name/candidate receipt binding unchanged. |
| firstIntent(BindNewSource), retryFirstRead and real completion/control | Never swallow an actual issued receipt or verification retry via a format key policy. | Existing read-only retry/uncertainty/binding rules remain. Active positive cohort cannot have outstanding IO. |
| F7→No→ExitQuestion→Yes, or No/Escape clear | Preserve actual old discard/exit transitions; never publish empty/active pair. | No new document after clear, history reset, hidden save or automatic successful exit. |

User-key active refusals conserve COMPLETE input Session and issue no intent. Real Complete/control events are different: preserve authoritative receipt/detached/uncertainty behavior, not a fictitious whole-state rollback. Defensive impossible-state tests assert no new write and actual receipt handling, not fake completion acceptance. First publication and later no-edit Save As require both complete successful actual IO/read binding and native readback in acceptance.

## Required later decision and verification

The candidate surface, package sequencing, finite acceptance and limits are closed in companion files. No work proceeds under this document alone. Any source/API/budget/old-test discrepancy requires a precisely reviewed amendment, not a namespace loophole. Full original empty-toggle/active-save/loaded/selection/typeover/Doc2/general attributes and post-format Undelete remain explicit M1 gaps. Later manual semantics and HOST policies must never be relabeled March differential qualification.


## Adopted normative annex: ARCHITECTURE.md

# Proposed architecture and independently reviewable sequencing

Proposal only. Existing application context is Linux Bubble Tea → pure editor.Session → immutable document/history → rooted storage. H renders shared native token positions; it does not serialize Bold, own history or buffer pending text. This adds one domain operation family rather than a generic formatting engine.

Production call path (new names are candidate API, not installed source):

```text
real terminal F6 → existing input.Translate
  → H Model.Update.claimUI FIRST
  → existing async/receipt/resize handling
  → existing73 pending character-count / menu / uncertainty / IO / repeat / macro paths
  → private H boldKey (bare F6; host ownership/idle checks)
  → existing m.reduce(Event{Command: editor.Bold})
  → G Reduce existing macro/session ownership and payload gates
  → private mode-aware active/write policy
  → G private bold command
       first/next open: Document.BeginBold(currentCursor)
       active close:   Document.CloseBold(currentCursor, History.ActiveBold(currentDocument) span)
       History.AfterBold(actual BoldResult)
       atomic adopt native + cursor + history + native-dependent revision + provenance
  → existing real Present/View/native publication/read-binding; no H native writer
```

ACTIVE ordinary Text retains G.edit → existing InsertASCII → authentic EditResult → existing History.AfterEdit with new PRIVATE span ownership update → old atomic adoption. The active closing Off is always the last token, after an append-only new span at EOF. Its opaque identity/current revision is updated only from actual ASCII insertion receipts at that Off. No cursor setter, caller span ordinal, matching bytes or copied Snapshot supplies authority.

The E private formatting state has a distinct nonzero identity, current native owner, On/Off token ordinals, nonempty character count and ACTIVE/CLOSED lineage. It stores no raw native/text payload, filesystem capability or parent chain. A receipt transiently binds true before/after native owners and actual result cursor, operation kind and the exact active-span identity consumed by closing. Every persistent update copies state; no shared mutable pointer changes old History/Model values. Opaque handles may be copied as immutable observations, but H currentUI and G reducer ownership continue to determine actual application execution rights.

Native opening uses existing whole admission and existing private publishBody(forceFormat=false). Closing is cursor-only and still produces an authentic operation result; after-close phase is distinct even when native owner is unchanged, so repeating a close receipt cannot open or close again. E/History private provenance, not an exported active bool, distinguishes first known-zero cohort from unrelated unknown history and later closed append-only lineage. Active receipt validation errors discard the tentative pure native result before G adopts anything. CLOSED unrelated ordinary edits can remain safe while permanently removing future F6 eligibility.

G maintains no separate formatting payload or independent pair counter. It reads the opaque active span through History.ActiveBold(actual current Document). A retained history handle for a cleared/foreign native returns no active span and cannot block ordinary legacy Retrieve; invalid history still unconditionally excludes F6. HistoryValid=false is an unconditional early F6 refusal; no stale-handle update after save. The actual generic Observe/write begin and first PublishNewBuffer intent are fenced in addition to all user routes. Completion/read-binding messages retain their existing dispatch/receipt semantics. F7 discard uses existing modal modes; an active span's identity survives F1 return from the exit questions, while actual clear/exit loses eligibility through the existing cleared native/New/history state.

H adds a small private F6 host adapter and production hook, not Model fields or a public setter. It MUST preserve existing message ordering and currentUI failure. Benign H diagnostic text never supplies semantic permission and need not prevent a legitimate close; no diagnostic is manually cleared to qualify. A shown menu intercepts F6 exactly as before.73 pending count consumes/refuses F6 by its original grammar; new nonempty native tokens/revision/unknown history exclude reentering pristine Repeat. Macro/deferred/frozen/uncertain/pending/closed runtime cannot enter F6. No moving70 consumer or provider API is introduced.

Presentation intentionally follows actual inherited source. Unknown history makes H69/H71 anchor/whole-ASCII guards fail; legacyPanes still renders actual Bold styles/codes and active owner. At80x25 legacy normal text is row1, and Reveal's banner/lower row are composed by actual View (not73's healthy-ASCII row0 anchors). F10 dialogs have their existing Reveal-dependent prompt rows. Proposed observers must derive all cues from final actual source and wait for real state, not borrow73's row0/status assumptions. State/View do not install/cache/consume formatting ownership. No new geometry, ruler, printer metrics, original raster/color or physical-key claim.

## Suggested E → G → H packages, without IDs or lane selection

1. **E semantic operation/history:** exact new opaque API and authentic AfterEdit history integration; paired native publisher/admission/source preservation and pure component tests. No UI/Session/storage change. Independent code review before a consumer depends on it.
2. **G command/save policy:** append Bold command; atomic adoption, active event matrix, all save routes/intent fences, post-save/historyValid=false refusal and actual rooted Session/publication tests. Depends on approved E plus existing approved G/New binding. No H adapter yet; independent review must examine every real save route and async distinction.
3. **H application integration:** real key dispatch after existing73 logic, host lifetime/IO/macro guards, actual Model/CLI/reader artifacts and mutations. Depends on approved E+G and actual approved H73/rebound source. 5bd now has the actual normal approval event bound here; later claim/source changes still require rebind.

E/G/H have different exact source namespaces; each package's literal amendments/new files must be registered separately by the future planner. Shared evidence namespaces are forbidden. H model.go is shared with73, requiring sequential coordination after73 approval, never a concurrent writer or copy/overlay. The actual ownership model/lane DAG must be computed and independently inspected: do not choose a broad namespace that silently collapses independent active lanes. E starts from actual approved H73 integration source (including approved inherited E/G), not the moving lane-e checkout. If actual computed routing shares an active70 lane, implementation must wait a normal quietpoint or use an independently registered noncolliding lane proven by the actual model; it may NOT borrow70 prototypes or fabricate a dependency/merge to proceed. No code-to-planning-to-code circular dependency is proposed. IDs, routing, planning snapshots and actual source claims are future normal workflow actions owned by ROOT.

No generic history reset, unbounded framework, plugin/resource provider, new document format, layout/print/preview implementation or reference controller is part of this proposal.


## Adopted normative annex: ACCEPTANCE.md

# Proposed acceptance, prospective finite limits and evidence

No product or test ran while authoring this proposal. All ceilings are prospective; later measurements may fail and must be reported before any reviewed scope/budget change. Do not claim unmeasured fit. Use genuine public APIs/authentic source chains for positives. Private inconsistent-state supplements are labeled and cannot replace real reachability. No fixture recognition, copied native prefix, rendered expected-output input or helper substituted for the app.

## E semantic/history acceptance (at most40 cases,128 explicit operations/case)

- Actual New(profile)→cursorEOF→NewHistory→BeginBold→AfterBold gives a real balanced pair and cursor between, native Birth preserved, native revision changed once, authentic history owner advanced, Qualified/CountKnown false without clearing fragments. Do not create a new History after formatting to make assertions pass. Use no-text and distinct ASCII-prefixed starts.
- Insert one or several distinct printable ASCII characters at current Off through actual InsertASCII; existing AfterEdit authentic validation must advance active span/current native. CloseBold→AfterBold moves across actual Off with SAME native bytes/revision, produces CLOSED history and cannot be replayed to close twice. Reject Close on zero-text span with complete conservation; typing then close succeeds.
- Complete A/BoldBC/plainD and other non-fixture values; a second sequential pair before save succeeds, third refuses. Public source signatures and old enum values remain exact except the listed additions. New native body patterns must match independently interpreted original contract spans, not merely another call to BeginBold.
- Wrong/equal-byte-independent documents, cursors, spans/history/result wrappers, fabricated/zero public result, stale pre-Text span, changed-result fields (opaque), close at wrong gap, non-EOF begin, orphan/nested/third-pair/opaque/unqualified prefix/resources and all output limits refuse without adopting a candidate. No `forceFormat=true` or arbitrary body/code injection path.
- Authentic ASCII result at an unrelated gap cannot advance ACTIVE; history refuses and G will discard native candidate. CLOSED EOF append retains only private eligibility; nonappend/overwrite removes it permanently while history remains unknown. Unrelated effectUnqualified/count0 does NOT become this cohort.
- Known old history behavior stays identical when private formatting provenance is absent. Old tests unchanged. Exact native-byte ceiling may be unreachable under the closed prefix/ASCII/2pair/owner schema: prove the real maximum and dominance statically, exercise reachable owner/pair boundaries, and label unreachable byte checks honestly rather than fabricate an at65536 positive or a mutant kill. Native/history failures return old receiver/history; no global mutable span pointer changes old value copies. A source-bound ActiveBold(currentDoc) returns false for nil/invalid/foreign current native, so retained active history after clear cannot govern another buffer.

## G Session acceptance (at most48 cases,128 events/case)

- Actual editor.New on a real rooted directory, optional ordinary ASCII append, Bold→Text→Bold→plainText through real Reduce. Compare native/body/cursor/phase/revisions/provenance/history knowledge and zero intents. G adopts all validated results once; fake/no history adoption mutant must fail.
- Two sequential pairs before first Save work only at EOF/current authentic private lineage. G new-span admission MUST reserve one future ASCII owner/byte in addition to2boundaries: at current4093owners open→type1→close fits4096; current4094owners must refuse BEFORE opening so no zero-space active trap exists. Real Left/Right outside active may retain bytes but a new span starts only at EOF. Typeover/selection/loaded/Doc2/Home/modal/macro/repeat/unknown owner/prior deletion/unrelated history unknownness refuse. No forged Session positive setup.
- ACTIVE invalid event matrix: Left/Right/Home/Up/Insert/Block/Delete/Backspace/F1/Enter/Escape/Macro/SwitchDocument; empty/nonASCII/control Text, wrong current source/cursor. Exact Session/native/history/IO conservation; no active-state loss or partial native mutation. Text after the refusal can fill span and nonempty Bold closes; generic host diagnostics must not make recovery impossible.
- Save-route table in CONTRACT is tested in full: public active Save; active F7→Escape (no SaveName/fromExit/history change); active F7→F1 return; active F7→No→ExitQuestion→F1 return; active F7→No→Yes actual exit; active F7→No→No/Escape actual clear and subsequent legacy Retrieve remains source-reachable. Zero write/Observe intents for refusals, exact filesystem conservation.
- Public active+SaveName/ReplaceQuestion/pending combinations cannot be manufactured as positives. Labeled private defensive supplements exercise SaveName Enter/Replace Yes/generic begin write kinds/first PublishNewBuffer fence BEFORE sequence/export/target effects. Real Complete/late/detached receipts retain original handling; no fake completion becomes authentic or is swallowed by active policy. Read-only bind/retry stays old behavior.
- After CLOSED Save opens a name prompt, saveHistoryInterleaving sets historyValid=false; cancel by actual F1, append real Text, then Bold MUST refuse before candidate creation even with source=nil/NewUnpublished. Repeat after successful first publication/read binding, failed save and later Text: old history handle can be stale and MUST NOT be requalified/rebound/reset. Preserve native/export/fragments, then ordinary later Save/Reveal stays old behavior.
- Completed nonempty spans use actual Observe→PublishNewBuffer→BindNewSource receipts. Full native file readback and no-edit Save As retain existing name/source/publication/unknown-history rules. Existing `fromExit` save completion and overwrite refusals remain unchanged; no new success branch.

## H public application acceptance (at most40 cases,128 Update/key/IO events/case)

- Genuine Open/New, authentic returned Update/key chain and real rooted IO. Bare F6 reaches the real G/E operation. Wrong modifier/text-bearing/OS-repeat F6, stale copied Models, closed runtime, actual pending/detached/uncertain IO, macro/deferred/frozen state, visible menu and73 pending character-count states cannot bypass existing ownership/dispatch.
- Existing73 Esc5x/alternate/one-shot/negative behavior and all old tests remain unchanged. Pending character Repeat consumes/refuses F6; native Bold creation prevents subsequent pristine character Repeat. Menu display/actions retain existing behavior. Any actual claimed-source difference from approved73 must be rebound/reviewed before code.
- Real normal/Reveal panes use actual tokens, spans and active gap. Unknown-history legacy fallback remains visible, not a false anchor/frame qualification. Repeated State/View cannot consume/update phase. Resize/releases/admin/paste/unknown/control receipts keep original H handling and cannot erase or rearm the native pair. A transient H diagnostic from rejected input must not prevent actual Text/nonempty close.
- Genuine Source/Document wrappers and copied histories cannot steer authority; wrappers are observations, not setters. Existing frozen DISPLAY OFF remains first and no live Bold state is mixed into it. Defensive conjunctions without public reachability are supplements only.

## Exactly two baseline unmodified CLI PTYs plus one integration mutant

Two fresh80x25 real `cmd/wordling` PTYs with independent empty local-flat roots. No new flags, instrumented binary, direct Session injection or fake telemetry. Only normal actual decoder keys are sent, with wait predicates audited against FINAL source before any run:

1. F6, alpha, F6, beta; inspect actual final normal alphabeta and Reveal `[BOLD]alpha[bold]beta`, then return to normal. Only the completed text/code content is compared with BOTH original048 associations. First-F6/prefix/caret/history/rows are documentary or HOST evidence, not new March oracle.
2. Type A, F6, BC, F6, D; inspect actual normal/reveal/native body against BOTH advanced03/04 ORIGIN contract witnesses. This is a completed-pair comparison; no whole-file identity with those originals is assumed. Distinct third values and two-pair boundary are meaningful public Model/component controls, not extra PTYs.

Each case performs actual F10 first publication to an absent name, waits for genuine current IO/read-binding completion, saves no-edit to a second absent name, verifies exact emitted FIRST/SECOND byte identity and actual reader readback, then normal F7/No/Yes exit with termios restoration and real return0. Save dialogs/return cues are source-derived: unknown history keeps legacy view, not73's ASCII row0 anchor; Reveal-dependent prompt row is respected or Reveal is explicitly closed before Save. Observers must not wait for a nonexistent status or infer bound success solely from file appearance.

Independently read all four emitted files through actual `wp51.Parse`, `Image.Inspect().Body`, `Image.Bytes(span)` and document.Parse/Export; compare decoded token/code body to the original-backed expected complete family. Prefix must equal the genuine selected constructor's prefix except the existing indexed packet6 format-bit update; do not copy ORIGIN or normalize the flag to force whole-file equality. Validate source/name/no-edit/receipt metadata through real Model/G tests separately. Expected output is never a binary input. Reader roundtrip is host conservation, not fresh original retrieval/printing proof. The future actual package/compiler/module closure must contain these REAL reader APIs; this proposal pins their source.

Freeze the entire driver/import/terminal observer closure, actual source/binary/module/argv/env and all predicates BEFORE execution; statically audit startup/F6/text/views/F10/save binding/no-edit/F7/cleanup/serialization and all immutable witness locators. Each baseline runs once. Any baseline observer/product/setup failure stops the campaign and is retained; no replacement allowance is implicit. Independent amendment required for any retry. The third/sole mutant PTY uses a compiled product with ONLY actual H F6 integration removed; it must fail the intended real F6/paired-text target after genuine green public and CLI baselines. An unrelated timeout/setup/compile error is not a kill. Owned containment is labeled containment, never normal exit.

## Semantic-mutant discriminators and limits

At most6 compiled E mutants,8 G mutants,6 H mutants, one campaign/package<=180s including its compile/target commands. No rerun-until-green or lost initial survivor. Meaningful examples fixed to the package contract:

- E: omit Off; wrong cursor; accept stale span; allow empty close; accept fake/foreign result/history; clear or falsely qualify history. Require intended public native/history failure after successful mutant compile.
- G: omit atomic history adoption; accept stale history after Save/cancel+Text; miss ExitSaveQuestion Escape; omit each defensive write-fence family; release active ownership after refusal; close without genuine nonempty receipt; reset NewHistory. Each must have an exact prior-green public or labeled defensive target. Retain survivors/redundancy honestly, choose within the finite list before exceeding the cap.
- H: remove production F6 hook (public Model AND one real CLI), bypass claimUI/idle guard, let73 count/menu context execute Bold, suppress a real async receipt or lose pair on resize/admin, install format state from View/State, allow malformed/repeated F6 aliases. No architecture-string test counts as product behavior.

Mutants apply ONLY in disposable exact source checkouts/closures from the actual approved source, never canonical/inherited tests/dependencies. Preserve whole diffs/source hashes/build stdout/stderr/target exits/elapsed/cleanup; no overlays, copied dependency hacks, source outside actual Go discovery or hidden tags. Each new source is independently reviewed before package promotion.

## Prospective resource and artifact budgets

Inherited native limits are unchanged:2pairs/16384owners/65536native bytes. E opening adds2owners/6body bytes and bounds them BEFORE allocation; closing adds0bytes/owners. G new-span admission additionally reserves first-character recovery capacity (before<=4093owners and native bytes<=65529); active Text fits4096presentation owners. No new raw input or byte-limit override is exposed. No cap is described as original DOS capacity.

- E public BeginBold including existing publisher/admission<=16MiB allocated/call; CloseBold<=8MiB; History.AfterBold<=32KiB with constant-size copied metadata and no fragment/native payload duplication. G complete pure Bold Reduce at its4096-owner admitted presentation cohort<=20MiB. Measure actual cold/public paths and count/byte boundary negatives, at most100 samples/case. Do not exclude existing called work to manufacture fit.
- H short real F6/Text/F6 public three-Update sequence (initial/text<=32 ASCII chars each, width80)<=4MiB allocated total; observed legacy View<=256KiB/call on this measured short cohort. Long source/mutation behavior retains its existing bounds; do not falsely extrapolate the short measurement.
- Every build/configured/test command<=300s. Each PTY<=30s plus at most2s owned TERM/KILL/reap, combined live wire+stderr<=2MiB checked before append, max3 attempts total. Successful normal exit must be observed before cleanup. Whole output beyond a cap is a retained failure; no silent truncation presented as complete.
- E evidence<=128regular files/4MiB; G<=128/4MiB; H<=192/8MiB; combined<=448/16MiB including ALL failures/history/nested seals/source/protected-path manifests and native outputs. Use the complete freshly reverified reference+delta custody protocol in CUSTODY.md; a compressed historical manifest copy alone is neither feasible nor fresh. The hierarchy may stop before all per-case maxima are consumed; no guaranteed simultaneous-max fit or evidence externalization.
- At most TWO declared external build binaries (final unmodified CLI and sole CLI mutant),<=64MiB combined, each exact source/compiler/module/build-info/hash bound. All command/raw/failure evidence stays inside its package cap. Do not duplicate inherited gigabytes of payloads; full immutable pathSET/Git+working mode/size/SHA custody reconstructed and freshly reverified under CUSTODY.md and exact approved import closure are required. No new download/host repair/dependency change.

## Required normal validation and review boundary

Each actually issued package must discover its actual Go closure/toolchain/go env/GOMOD/GoFiles, retain full source/protected-old pathSET before/after using CUSTODY.md without copying the 5,167,269-byte inherited manifest into a 4MiB namespace, gofmt ONLY owned changed/new Go files, normal cached-source lint on the exact changed list, actual build/go test ./.../go vet ./... and relevant focused race; configured7 standard mission checks with honest skips/discovery. No unchanged broad fuzz repetition is required; no new binary parser/format is introduced. Meaningful malformed/foreign state and mutation boundaries above are mandatory. If a frozen old test fails, fix within approved source semantics or stop for a precise reviewed scope change; zero old-test amendments are authorized here.

ROOT alone owns later normal lifecycle/publication/quietpoints, DIFFERENT code review, mission acceptance and reference grants. Proposal author cannot self-approve. Actual original app reopen/edit/print/save and general F6/history/empty/active-save functionality remain M1 obligations rather than claims from these host tests.


## Adopted normative annex: CUSTODY.md

# Complete fresh reference+delta custody (F6-CONTRACT-R1 only)

This replaces only the custody encoding/readiness ambiguity at ACCEPTANCE lines61–66. APIs, behavior, source boundaries, test/runtime/evidence caps remain byte-exact or unchanged in meaning. It is a candidate for DIFFERENT closure review, not implementation authority. All commands/raws/failures, including failed measurements, remain inside the original E128/4MiB,G128/4MiB,H192/8MiB and aggregate448/16MiB ceilings. Only an already inherited immutable metadata manifest may be externally referenced. Nothing here externalizes a new failed raw or treats historical working assertions as fresh facts.

## Immutable dictionary and exact schemas

The sole proposed dictionary is approved H73 commit `5bd5105e9014a839ea95c5b2efd21548ccd8756b`, literal path `internal/tui/evidence/character-repeat/before.json.gz`, Git blob `5fd810927242843b1d5c0f2430f56df8abc1428b`. Compressed length5167269/SHA256 `f42869ecf5d5a0c2bdff1eeed7b536b055dd4e1f9868a4efca99bf26d740d6d3`; expanded length31683177/SHA256 `779b7b371a8152089387670e8d706f134e1b171b4fb606ce602cd34e225763a0`. Fetch by exact immutable Git object, verify blob, both hashes/lengths BEFORE JSON interpretation. Missing/different base stops; no fallback substitution or ambient pathname trust.

Actual historical JSON has exactly head/status/files. head is447a46a52d4f8ab28082147f7e8aec47db7ef558, status is a historical five-line untracked string (retained in proof-result); neither is current truth. files is109980 unique rows, exactly path/git/mode/size/sha256. All base rows are regular files; mode includes type+actual permission bits as octal string (e.g.0o100664), git is actual `mode SP oid SP stage`, size integer, sha256 lowercase64hex of complete working bytes. Dictionary rows are reusable encodings ONLY after a fresh current reread proves all five fields equal. Historical untracked entries are not dictionary rows and grant no inclusion exemption.

Canonical rows are sorted by unsigned UTF8 path bytes and serialized JSON with sorted keys, separators comma/colon, ensure_ascii=True, no trailing newline. Required row keys remain the five exact keys; type is explicit in full POSIX st_mode. Git kind comes from git-mode. No implicit absent/type coercion. Literal paths must round-trip UTF8, be relative, with no backslash, NUL, empty/dot/dotdot/.git component; reject duplicate decoded paths and aliasing/hard-link inode reuse between distinct regular paths. Index stage must0. Regular Git100644/100755 plus actual regular inode is the admitted cohort. Symlink/gitlink/FIFO/socket/device/missing/inaccessible/nonregular/path-parent-symlink entries are recorded as a complete metadata failure (literal path, Git record, lstat/type/errno), then STOP before code, rather than follow/omit/pretend regular. No claim that the current example encountered these types. Unsupported filenames/type changes are failure, not silent path normalization.

The delta JSON schema is `wordling-custody-reference-delta/v1`: exact base binding above; phase; head; complete raw status porcelain-v1-z hex; removed sorted unique existing-base paths; upserts complete unique five-field rows for every new or changed row; rows count; canonical_rows_sha256; index_stdout_bytes/SHA256 and reconstruction rule; census_seconds; working_bytes_read. Schema/example are concretely shown by proof.py and example-delta.json.gz. No removed/upsert intersection, redundant/duplicate upserts or unknown keys accepted. Reconstruct base map minus removed plus upserts; validate every row/path and compare count+whole canonical hash. This yields the ENTIRE current tracked set, not just changes. A row reused from base is never an assertion that it was not reread.

## Fresh complete discovery, not historical reuse

For EACH actual future claim and before/after phase, bind actual checkout absolute path, Git common-dir/worktree identity, actual HEAD/parents, index tree/complete stage0 entries and approved dependency ancestry. Discover `git ls-files --stage -z` afresh (no old path-list iteration), independently `git ls-tree -r -z HEAD`, compare exact tracked sets/index metadata and identify every index/HEAD difference. Finish the before census BEFORE first product/test write. Claim must be stable/clean except explicitly classified ordinary claim metadata; all such differences require literal authority, never an automatic exemption.

Walk only each exact discovered tracked path in that checkout: lstat every parent to reject symlink traversal, open regular files without symlink following, fstat and lstat before/after full streaming SHA; compare dev/inode/mode/size/mtime/ctime and total bytes read, reject unstable or repeated inode aliases. Full reread includes every inherited record, all allowed old amendments, normal task/runtime metadata, all old evidence and old manifests themselves. Rediscover index/HEAD/status after the census; if changed STOP and retain the entire failed attempt. Also discover full untracked set via porcelain-v1-z with `--untracked-files=all` and `git ls-files --others --exclude-standard -z`; compare sets. No ignored/private directory enumeration: ignored outputs are prohibited in the source checkout; use declared owned TMP build roots, whose files/bytes/cleanup get explicit manifests. Native output roots are separately explicit owned scopes. Rename is removal+addition plus exact raw status old/new path pair, not a reason to omit either. Changed mode or Git object is an upsert even if bytes equal. Missing tracked paths, index conflicts, unapproved adds/removes/renames/modes/status entries fail closed.

The proof in this packet is a current approved clean H73 metadata example, not a future claim. It freshly discovers all actual tracked paths and hashes EVERY current working file; it does not perform the entire future race-hardened claim preflight above. In particular its implementation demonstrates regular-file schema/reconstruction/cap size, while parent traversal/hard-link/untracked differential guards above remain mandatory future execution work. No product/compiler/native parser runs. Git ls-files raw stdout is retained losslessly through the base+delta reconstructed rows (`git` TAB `path` NUL in byte order), verified byte-for-byte against actual command output and size/SHA. The base Git-show raw is the exact already inherited compressed object; identity is checked, not copied. Other Git command stdout is small and reconstructible from logged fields; stderr is retained whole. These are explicit complete lossless encodings, not output truncation.

Independent verification must resolve the exact base, reconstruct all rows and raw index output, REDISCOVER the full actual claim index/tree/status, and REHASH every actual current inherited working file. Comparing a reconstructed hash only to another reported hash does not validate unchanged rows. An attacker changing a reused row, dropping a new path, supplying stale base, or changing actual bytes without delta must fail the independent current reread. At source handoff, compare each reconstructed before/after row: every inherited protected byte/type/mode/Git change forbidden except literal owned amendments and exact normal metadata receipts; new paths restricted to literal new source/own evidence. Verify all removals/additions against complete set difference. No broad namespace authorization follows from encoding.

## Phases, no self-reference, complete terminal custody

1. Before product/test writes, census the actual claim inherited set and preexisting status, encode/verify before delta, record command argv/cwd/whole stdout/stderr/exit/timing (lossless indexed-stream encoding permitted only as above). Packet outputs are born AFTER this census in the owned namespace, so cannot be falsely listed as inherited. Their additions are captured in the later phase. A failed fit aborts BEFORE code.
2. During implementation, append all raws/failures to the same cap. Count every regular payload including scripts/manifests/deltas/nested seals before each expensive run. The inherited base is not copied or charged again; local reference metadata IS charged. Entire source-file payload copies are unnecessary, but all source/Git hashes remain explicit. No failed raw may become an external reference. Stop before exceeding caps; no new ceiling or retry allowance.
3. Freeze product source; record source HEAD plus literal working/index changes honestly. After-source census rehashes all inherited paths and all then-existing owned files, with exact status. Before/after delta excludes only the census file being produced and future terminal seal, with an explicit phase boundary; those are NOT missing protected paths: they were not yet born. Before the final census, freeze the complete existing payload pathSET and a literal finite list of future terminal generator outputs (census delta, its own command stdout/stderr/receipt, terminal inventory/seal). Every later new path must be on that list and is fully hashed by the terminal seal; never use an open ended namespace exclusion. The terminal command must be successful and whole-exit before sealing; any late failure becomes a listed raw payload before a new terminal seal. Encode their later custody through the terminal inventory. Do not claim that dirty evidence additions or normal lifecycle status is clean. A normal later native transition is a distinct phase with its actual changed metadata/events, never backdated into the earlier source census.
4. Finish every evidence payload and command; terminal seal inventories every regular local payload, including both deltas and all raw/log/failure files, excluding ONLY its exact root seal pathname. No subsequent payload mutation. Terminal seal records its byte count/file count and content hashes; its own size is counted toward cap without embedding its own hash. Store its SHA externally in the handoff message/normal commit receipt. A source commit may precede evidence sealing; evidence commit is created AFTER seal and binds seal Git bytes. Never embed that evidence commit SHA inside its own payload; report it in later runtime receipt. If commit/lifecycle changes source/protected files, use a separately sealed lifecycle packet and raw exact status/delta within the preallocated cap; do not alter earlier seal or call overlap clean.
5. Before launch, preflight actual complete delta+logs+seals cost against remaining cap, with measured slack for planned bounded campaigns. The example proves only today’s feasible encoding; future claim trees may diverge too far. If any actual claim cannot fit complete metadata, all evidence and required campaign within existing caps, STOP before code (or stop current campaign before capacity) and request precise separately reviewed plan adjustment. No fit guarantee for every future tree, no simultaneous-max fit claim.

## Metadata-only negative controls

The actual proof includes wrong/missing/stale base; forged unchanged row; duplicate upsert; omitted row; alias path; and independently changed working-witness hash. Every finite mutation must be rejected, not labeled a product test. Future actual preflight additionally covers missing/type/mode/index/status changes and stable double-discovery. Deletion/new/rename reconstruction is ordinary map set difference, with both sides preserved; the approved example has real additions and changes since the historical pre73 base. See measured counts/bytes in proof-result.json. This representation remains original metadata custody tooling only, not a new product or native-format framework.


## Bound evidence level annex

```json
{
  "March_completed_visible": {"case":"CMD51-048 setup","runs":["2026-10-29-smoke-02","2026-10-29-smoke-03"],"scope":"F6 alpha F6 beta completed normal/Reveal content only;090remainsnot-run; no intermediate/native/history witness"},
  "March_completed_native": {"case":"CMD51-204 authoring setup","runs":["2026-10-29-advanced-03","2026-10-29-advanced-04"],"origin_bytes":334,"origin_sha256":"c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d","body_contract":"41c30cc34243c40cc444","scope":"Existing editing contract interpretation, not a decoder run here; completed A/BoldBC/plainD before delete"},
  "June_documentary": {"edition":"MNUS1WP51X1C-6/92","printed":[37,38],"PDF":[54,55],"OCR_sha256":"f1d786f3ea0697f652bdfb2c13cb7745a01e9fbe9abb64042e517f1a85c4304c","OCR_bytes":5758334,"facts_paraphrase":"Both attribute boundaries inserted, cursor before Off, typing between; F6 or crossing Off turns attribute off.","limitation":"Later than March09 program; OCR duplicated typography; no new PDF visual QA or March intermediate proof"},
  "HOST_contract": ["NewUnpublished Doc1 EOF-only ordinary Insert cohort", "opaque authentic format/history receipt", "explicit unknown history and post-save refusal", "empty-toggle/active-save/unsupported active command refusals", "2pairs and inherited native bounds plus4096presentation-owner cohort", "finite resource/evidence limits", "nonempty close/typing/discard recovery"],
  "still_unqualified": ["March first-toggle/first-character/native intermediate", "empty-toggle pruning", "active-save normalization/post-save attribute behavior", "original formatting/history interleavings", "loaded/typeover/selection/Doc2/general attributes", "fresh Wordling output original reopen/edit/print/save"],
  "manual_publication":"Paraphrase/hash/edition/page locators only; no copied manual paragraphs or native prefixes; copyright remains external",
  "full_M1_open": "37unfinished plusFC010M2gate;91groups36lessons nestedSC001-005; PDFgated"
}

```
