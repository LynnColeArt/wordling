# WP109 / WP107 producer amendment independent review

**APPROVE_TASK_SOURCE_SCOPE.** No blocking findings. Approval is for the exact proposed native producer task and WP107 dependency/chronology amendment, not implementation, registration, a source fix or operational/original/M1 acceptance.

Exact proposal bytes:

- WP109-copy-italics-native-producer.md: SHA256 `53e27e2f5bd8703b21f6c8dab22dad07771766177ed2e56ea91bb9f5d8c39ca4`
- Amended WP107-retrieve-italics-public-integration.md: SHA256 `64dea6c83601df23eecceea071ff8d66aeb612fa746261a6194742394b888045`
- Preserved WP107-before-amendment.md: SHA256 `410721dfb98287d250727bcbae2b2b45ec4879d280704a173689c0a98de62a79`
- source-pins.json: SHA256 `3f835d93b6a43e985dfed40c7d2a602ff02e18ef65326c9f0cc332fc2be6718e`
- projection.json: SHA256 `49fcbd36c9681c5ad9362405b045a983e384c4e9853a60c2453aed6ae298138c`

Directory: `/tmp/wordling-mission1-closeout-20261118/copy-italics-source-amendment/`. Reviewer: reviewer-renata with existing resolved read-only governance/profile context. I did not author these proposed task amendments or any producer implementation. ROOT owns normal planning Op/adoption/index/status; no live writes occurred here.

## Actual source feasibility and ownership

The defect is a distinct real source producer. `internal/editor/block_copy.go:beginBlockCopy` calls native `CopyEverydayBlock`; the same preparation path also serves beginBlockAppend. The native source file tracks Bold/Underline at selection boundaries and admits only their ON/OFF owners in its selected body. `internal/document/everyday.go:InsertDocument/InsertBlockCopy` is a later consumer that WP106 fixed; its approved source SHA remains `c0d32c0ddfd84fd5d7885f2fffa6fae9f86f0eccfad1db7492001f7c7f33e577`. Directly testing prepared fragments therefore cannot prove the real block producer accepts Italics.

The preserved public repro is genuine source-bound evidence: the actual selected rooted entry is acquired through public editor events/I/O, Reveal/Block/Right selects tokens0..7 of pinned ITALICS.WP, and Move1/Copy2 reaches UnsupportedBody at token0/span324+3 before InsertBlockCopy. Its raw Go JSON has the intended single test failure and no setup/compile failure; repro test SHA `bd67555599a4a7777c0f0dc036cf863b8246fb3325c607a013351c6418c865e2` matches. The four source hashes match the f6abda6b snapshot and the new source-pins candidate30943680; current source binding and original107 hash checks match all5 records. I inspected the existing repro; I did not rerun it or treat it as WP109's future committed native RED.

The proposed sole production owner `internal/document/block_copy.go` is sufficient for this bounded extension: existing checkEverydayCursor checks source validity/revision/gap and CheckMutation; the latter already validates independent Italics balance. Existing parsed Italics kinds/three-byte owners and historical detached prefix constructor are available. Adding a third independent edge state, admitting its exact selected raw owners and supplying only necessary edge wrappers fits that owner without touching document.go, admission, insertion, editor/TUI/storage, resources or native framing/API. Unrelated Redline/Strikeout remain conservatively outside the selected copy allowlist.

The consumer inventory is an appropriate bounded response to the discovered prepared-fragment/public-producer gap: all active production Italics uses plus producer/admission/reader/editor routes need exact hashes/callers/dispositions. Include both beginBlockCopy and its shared beginBlockAppend caller in that inventory. This is a finite census/check, not permission to edit those consumers or refactor the attribute system. The proposal preserves the actual recurring/contested-boundary trigger distinction and requires review of any separately demonstrated owner.

## Acceptance and conservative safety

T353 genuinely requires native tests/UnsupportedBody RED committed with byte-identical old production before any producer edit. Supporting exploratory public failure is retained as its actual chronology, not rebranded as that future native RED. Tests must exercise whole/partial runs, both edges, exact ON/OFF adjacent selections and owner-only selections where the existing contract admits them, leading/trailing text, multiple/reversed selections, independent Bold/Underline/all-three and legal crossing state. Independent literal byte/actual Kind expectations are required; implementation flags are not the oracle.

T354 preserves the unchanged original source bytes/prefix/birth/identities, detached historical prefix ownership, copy-buffer independence, typed cursor/empty/unsupported/opaque/balance/limit failures and final receiver CheckMutation authority. The independent subfunction08 literal/Kind mirror test is explicitly required for any new private local constant. Existing C3/C4 semantics are not expanded to arbitrary attributes, and no new enum/parser constant owner is needed.

The wrapper arithmetic requirement is precise: the existing producer's conservative `last-first+4` bound must not undercount six possible edge wrappers after introducing a third style, while old non-Italics acceptance/refusal is preserved. A blanket replacement with+6 would tighten old inputs; replacing conservative+4 with a smaller actual count could relax them. The task explicitly forbids both silent changes and requires boundary/three-style tests with independent token counts. It also retains byte limits counting synthesized bytes and no intrinsic cap increase. Thus implementation has a testable conservation constraint rather than a permissive “support more attributes” instruction.

The implementation/review must verify resulting fragments are genuinely self-contained under existing native mutation admission as well as exact bytes/Kinds, preserve old non-Italics outputs and account for each wrapper in bounds. This follows the stated self-contained-fragment/mutation-admission DoD and needs no expanded owner.

T355 requires native producer/insertion/history/appearance checks, relevant race, full Go test/vet/build, Windows application production-closure cross-vet/build, truthful skips/helper failures, all-contract dispositions and native source/evidence handoff to a different reviewer. Mac is explicitly deferred, and cross checks cannot claim native Windows execution. No actual tests were run by this task/scope review.

## WP107 conservation and dependencies

The exact diff preserves every original107 requirement/owned test/evidence path, its four existing dependencies106/94/84/85 and existing receiver/native/public/Runtime/save/reopen/loaded/New/foreign/stale/negative safety obligations. Outside frontmatter line wrapping it adds only WP109 as predecessor and the explicit producer amendment appendix.

The added appendix correctly supersedes the former optimistic all-GREEN106-only expectation with observed chronology: genuine current-core public Copy RED remains; final integration GREEN must use independently approved106+109. Exact final integration tests are subsequently replayed on pre109 to distinguish producer-only UnsupportedBody while ordinary106 Retrieve retains GREEN, and on exact pre106/9f for insertion refusal. If a Copy test fails earlier at the producer during pre106 replay, that is identified as such rather than mislabeled as insertion proof; genuine ordinary Retrieve cases establish the latter. Neither setup failures nor fabricated early public RED count. Native106 and future109 each retain their own actual RED-first commitments.

WP109 depends only106, inheriting its actual native ownership chain;107 retains all prior dependencies plus109, never the reverse. ROOT explicitly withholds107 final approval despite any host limitation re-gating an already in_progress claim. Pure projection reports108→109 WPs,313→315 edges,31 lanes and WP109 lane-f. Independent static inspection of its manifests confirms only WP109 is added to lane-f, all existing WP memberships and29 code groups are retained,31 lane IDs remain, and the projected lane dependencies are acyclic. The supplied projection reports no ownership/DAG errors. These are proposal checks, not normal registration or a claim. ROOT must still adopt/finalize normally and preserve old runtime history.

The separately observed foreign callback/unsettled-operation bookkeeping issue in TUI model.go is outside109. Nothing here authorizes editing it or weakening public foreign/stale tests. A real separate110 proposal/repro and independent review remain necessary;107 must retain that obligation rather than excluding its failing acceptance case. This does not require silently adding TUI source to109.

## Shared qualification boundaries

Both tasks retain the original receiver contract and final native insertion authority; no source prefix/resource transfer, normalization, alternate writer, conversion intermediary, fake Result/provider/callback, fabricated runtime receipt or hidden skip is authorized. Authentic original occupied Retrieve/Copy and native reopen/edit/print/save interoperability stay mandatory later. CMD51-065/E3/audit/matrix/M1 are not promoted; all49 families remain required. No original/private reference/VM/TEST/P/CONTROL/Mac or campaign-clock action follows from this task approval.

No primary/source/index/Op/lifecycle changes, registration, tests, builds or probes occurred in this review. Only packet/source/Git-object reads, static hash/diff/manifest comparisons and scratch review writes occurred. ROOT retains adoption and authoritative review/status control.
