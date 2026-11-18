# WP106 independent source review

**APPROVE — bounded native WP106 source. No blocking findings.**

Reviewer: `reviewer-renata`. Reviewed fixed implementation `8b15d9dc283ad2b3f5013772cd5d9f35c481644d`, production commit `f7f5db648da53edbe1392e67a091397ea40019af`, against pre-core `9f255248b91f0a695d2affd214f37f50d661a03a`; official baseline is `3ba3669662e4591223325b63e2218bd22c8b7d95`. I authored earlier task/architecture proposals, but did not implement this Go change. Implementation author is `native_italics_impl`. The reviewer profile and action-scoped governance were resolved read-only; receipts are `profile.txt` and `governance.json` beside this report.

## Source and contract assessment

The complete production diff is seven insertions/four deletions in `internal/document/everyday.go`, adding an independent Italics balance flag to the existing Bold/Underline insertion scan. It admits only the existing parsed Italics ON/OFF token kinds and preserves their exact raw bytes. Duplicate ON, unmatched OFF and unclosed source states still refuse before publication. Independent attributes can cross without an invented stack rule. Both InsertDocument and InsertBlockCopy use the same implementation; only their existing cursor semantics differ.

The receiver safety boundary remains the existing `publishBodyWithWordRestore` candidate construction and `next.CheckMutation` gate. A balanced Italics source at an inactive receiver boundary succeeds; the same source inside active receiver Italics fails atomically, including empty pairs and sources with ordinary text around the pair. Ordinary text inside active Italics retains its earlier behavior. No second receiver state machine, file-name exception, hardcoded source fixture admission, parser expansion, resource expansion or prefix workaround was introduced.

The native tests verify exact receiver/source byte conservation on refusals, source ownership, valid and foreign/stale cursors, invalid/empty input, byte/token limits, source balance, receiver boundary gaps, independent Bold/Underline combinations, insertion versus block-copy carets, revision and birth identity, history remapping, export provenance, parse/no-edit round trip and real New document prefix ownership. New document assertions locate the real flag owner rather than borrowing a loaded fixture offset. Existing pinned original ITALICS.WP/ITALICS.PRN bytes are used for native token and layout projection; this is not a new original execution or interoperability qualification.

The canonical WP106 task, adopted receiver contract and relevant mission contract set were compared with actual source/tests. Native framing/editing require exact token ownership and conservative refusal; session requires immutable cursor/history/provenance; these hold. The files/platform and resource/layout boundaries remain intact. Automation, macros, language, graphics and broader resource/coverage requirements are unchanged. No dependency, module, parser enum, platform implementation, catalogue, matrix or acceptance claim changed. The only changed Go files in the fixed range are `everyday.go` and the new `retrieve_italics_test.go`.

## Independent verification

All executions used a disposable Git archive under `/tmp`, `/usr/local/go/bin/go` (Go 1.26.4), `GOTOOLCHAIN=local`, `GOPROXY=off`, `GOSUMDB=off` and `-mod=readonly`; no dependency acquisition or primary checkout modification occurred.

| Independent check | Result |
| --- | --- |
| Fixed source: `go test -mod=readonly -count=1 -json ./internal/document -run 'TestRetrieveItalics|TestEveryday.*Insert|TestFontAppearance'` | Exit 0; 102 named pass / 93 leaf pass, no skips |
| Reviewer-only native cases: crossing Bold/Italics source and source/receiver aliasing, both insertion APIs | Exit 0; 6 named pass / 4 leaf pass |
| Exact final test bytes against exact pre-core everyday.go: `go test -mod=readonly -count=1 -json ./internal/document -run TestRetrieveItalics` | Expected exit 1; 55 named fail / 46 pass; 50 leaf fail / 42 pass. Every failing leaf reports UnsupportedBody |

The reviewer-only file existed only in the temporary archive and was removed before the RED replay. The final tests equal the supplementary RED commit's exact bytes. The first archive attempt omitted an existing tracked fixture required by an older shared test helper; it produced file-not-found setup failures, not a product finding or causal RED. That raw attempt and its correction are preserved in `isolation-setup-*`; the corrected archive included the exact tracked fixture. Temporary isolation was removed, the registered worktree list stayed unchanged, and primary source/test hashes stayed fixed.

Raw commands, output hashes, counts and cleanup assertions are in `independent-check-summary.json` and the corresponding `.run.json`, `.stdout` and `.stderr` files. `independent-checks.py` preserves the reproduction logic.

## Author evidence independently checked

All 127 files listed by the fixed evidence manifest matched their hashes, with zero errors. The manifest identifies production `f7f5db648da53edbe1392e67a091397ea40019af`. I independently recomputed the raw Go event counts, baseline JUnit counts and Git chronology in `independent-evidence-audit.json`.

The initial native RED `084659958620c5c583874bc4347502e96bc36c50` precedes the source implementation. The later supplementary RED `fac6f3d46e864e82d66a110e848795ef1c900535` transparently adds the final New/birth/projection assertions after exploratory work while restoring exact pre-core source; it is not presented as predating that exploratory edit. Final production and final tests match the reviewed hashes. The independent exact-source replay above establishes the causal failure without inventing chronology.

Author raw results are 101 named / 92 leaf native passes; full Go tests 3,263 named passes plus four existing skips (3,048 leaf passes plus four skips); focused race 138 named / 127 leaf passes; Linux vet/build and Windows amd64 application build plus all 16 actual application-production package vet checks exit 0. The full test skips are the pre-existing Advance oracle, Bold PTY oracle roots, Windows native namespace on Linux and separate CharacterRepeat CLI artifacts. No WP106 case is skipped. Broad Windows `./...` utility builds retain the documented pre-existing O_NOFOLLOW/Getrusage helper failures; this is not represented as a clean cross-platform test run. These broad checks were audited from fixed raw artifacts, not redundantly executed by this reviewer. Windows cross-build/vet is not native Windows execution.

The official failure-derived baseline has zero recorded counts; its raw JUnit contains seven passing checks, while the separate raw native baseline has 609 named/580 leaf passes. Those representations are distinct. Likewise, the lifecycle pre-review gate reported no_new_failures with **zero matched targets**; it did not rerun native Go. The real author and independent Go checks supply that evidence.

## Scope and capture

Approval covers the native WP106 contract only. WP107 still owes the genuine rooted public I/O and Runtime Retrieve/New/loaded receiver/save/reopen integration, with the same public tests causally replayed on pre-core source as planned. Later original occupied-Retrieve and native reopen/edit/print/save qualification remain mandatory. This review promotes no audit ledger, CMD51-065, E3, coverage matrix, M1 acceptance or prerelease readiness. Mac testing remains deferred. No Original, VM/private resource, P, TEST, CONTROL or Mac operation occurred in this review.

Parent-owned receipts confirm T344–346 done, for_review and in_review claim. The owned-checkout move-task route records the real review claim but emits no generated executor prompt; the action-review route would allocate the prohibited project/.worktrees location, so no such call was made. No prompt or runtime issuance event is fabricated. The exact canonical task, contracts, frozen Git source and real receipts are the review inputs.

This report/JSON supplies the independent verdict; it does not mutate the live event log or WP state. ROOT must preserve/capture `reviewer-renata` / `approved` / this report reference through the canonical review-result seam using the newly activated per-invocation CLI source, while retaining its owned-checkout handling. The event log remains the authority for recorded status.

## Fixed identities

- everyday.go SHA256: `c0d32c0ddfd84fd5d7885f2fffa6fae9f86f0eccfad1db7492001f7c7f33e577`
- retrieve_italics_test.go SHA256: `756bd61f4ce8a41824b85dc24ea1396af9f55cc2a960f58ed29c92b42312fafe`
- Evidence manifest SHA256: `e3f85965b0ead2cbd71d74c65bed44f2a5b9e6579af0abb69c21d1ad7d360b38`
