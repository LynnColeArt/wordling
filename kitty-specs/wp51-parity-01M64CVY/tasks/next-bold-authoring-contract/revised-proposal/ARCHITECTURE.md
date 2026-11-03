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
