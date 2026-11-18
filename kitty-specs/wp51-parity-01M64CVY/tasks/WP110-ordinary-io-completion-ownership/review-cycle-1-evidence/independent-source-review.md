# WP110 independent source review

**APPROVE. No blocking findings.** This approves ordinary Runtime queued-completion ownership at fixed candidate `253f9684c7ce47b2b3ab20184db22b3ecd560373`, source/tests `e037785e319d2a64395fdaf623cdfee96cb4b61e`. It is not WP107 integration, WP108 qualification, original/native interoperability, final platform testing, prerelease or M1 acceptance.

Reviewer: `reviewer-renata`, independent of implementer `WBworkbook_b07`. I previously reviewed the task scope but authored none of this Go implementation. Inputs were the actual canonical WP110 T356–358 task, approved combined scope, existing resolved reviewer/action-review governance, implementation report, frozen Git source/evidence and real in_review claim `01M7R7HRW1W1JXJ4BCGAF09QZ2`. The owned route emits no generated executor prompt; none is fabricated. ROOT owns all durable verdict/status capture.

## Source and safety assessment

The full Go diff from pre-code ff74284f changes only model.go/runtime.go production, the new ownership test and the three explicitly authorized legacy test files. No editor/storage/first-save/macro/proof production owner, API, format, resource, dependency or intrinsic ceiling changes.

Model.reduce preserves specialized first-save/ReadMacro/proof routing. Every ordinary request enters queueOrdinary, which retains a real nonzero-sized receipt allocation in a newly copied immutable Model slice. The captured existing dispatcher remains the sole IO/outcome producer. Runtime.mu permits one callback start and seals an unchanged copied result, including stopping/capacity refusals. Raw Runtime.command observations remain unbound diagnostics/specialized messages.

The existing UI transition gate runs first. Before unsettled removal, reconciliation or Session delivery, completeOrdinary requires exact pointer membership in the current Model queue. takeOrdinary checks actual Runtime owner, started state, stored result and unused delivery under the mutex. Authentic consumption copies the outcome, marks delivery, releases the retained result and removes only that queue entry. Numeric keys, same root/path/inode, foreign callbacks, copied metadata, unexecuted identities, bare Results and redelivery cannot supply queue custody.

The pointer is per issued request, not merely per Runtime. There is no new Runtime registry, public issuer/query or mutable caller result provider. Existing 1024 execution admission, source/capability checks, worker wait/Close lifetime and copied diagnostics remain intact. Model slices are copied before modification; stale Model authority cannot consume a valid receipt. Genuine own late publication still reconciles the filesystem, while UI cancel never pretends to cancel already executed IO. Errors are not changed into alleged authentic uncertainty.

I inspected every ordinary constructor/caller and verified all29 census line/file hashes against fixed Git source (line hashes include their actual newline). All five raw outcome constructors are sealed at the same queue boundary. The only other live Model command caller is specialized ReadMacro. ProofReply owner/kind/proofAdd and bare-proof refusal remain preserved. completeIO has only the intended specialized proof and authenticated ordinary entry routes. This is not a ReadSelection-only fix or dead helper.

The ten real ordinary kinds are Read, Observe, WriteSnapshot, PublishCandidate, ReadSelection, ReadMergePrimary, ReadMergeSecondary, ObserveWorkspace, PublishEveryday and AppendWorkspace. Public key-driven tests assert each actual queued Pending.Kind. The expanded RED evidence correctly distinguishes generic Read's prior foreign UI/native/source/Birth adoption from ReadSelection's prior PendingIO loss with Session/native data retained. Neither is a disk-corruption claim.

The legacy changes are narrow and justified. original_test.go now rejects a fabricated bare uncertainty while retaining real pending work, then verifies actual publication. editable_test.go verifies an untouched genuine publication, separately refuses an unbound forged error during new held work and verifies both real destinations. It no longer edits a successful callback's Err and calls that authentic uncertainty. model_test.go verifies opaque genuine Close refusal, zero IO/Completed growth and pending settlement. Existing diagnostic concurrency/capacity/duplicate and persistent-state tests remain. No fake owned positive or new real uncertain disk fault is claimed; independently scoped storage uncertainty and genuine error/reconciliation handling remain required.

History72369dbef52b1528e61b840669199efb9466f471 is accurately retained as an earlier ordinary duplicate-dispatch point fix, not mislabeled as only specialized-envelope history. One identified prior fix alone establishes neither3+ recurrences nor2+ shipped reactive PRs or contested ownership. The current correction is structural across every known ordinary mask; no further trigger evidence was established by this review. Actual future trigger evidence still requires the prescribed doctrine intervention.

## Independent executions and exact RED chronology

Executions used disposable Git archives under /tmp, `/usr/local/go/bin/go`, GOTOOLCHAIN=local, GOPROXY=off, GOSUMDB=off, GOWORK=off, -mod=readonly, uncached selected tests and90s timeout. No linked worktree or dependency acquisition occurred.

| Check | Actual independent result |
| --- | --- |
| Fixed-source ordinary ownership plus three narrow legacy tests | Exit0;151 named/140 leaf pass; no skip |
| Reviewer-only adversarial cases under -race | Exit0;25 named/22 leaf pass; no skip |
| Exact initial RED tests on exact full52f26fd0 source | Expected exit1;68 named fail/61 pass;64 leaf fail/56 pass; compiled, empty stderr |

The focused command was `go test -mod=readonly -count=1 -timeout=90s -json ./internal/tui -run '^Test(OrdinaryCompletion|BareUncertainResultKeepsAuthenticPendingWork|ActualPublicationAndUnboundForgedErrorAreDistinct|CloseGatesQueuedIOAndRetainsStartedReceipts)'`. The extra command added `-race` and selected `^TestReviewOrdinary`.

Extra cases exercised actual queue/callback flow: nil receipt refusal for all ten kinds; concurrent Close versus callback and redelivery for all ten; public Completed error-copy mutation before genuine missing-read delivery for Read/ReadSelection. They test conservation and outcome isolation without fabricating a successful receipt. Reviewer-only test source existed solely in the temporary fixed-source archive, was removed before the old-source run and never entered primary source.

The first archive omitted the tracked local Ultraviolet replacement required by go.mod. Go stopped at setup with no test outcomes. Failed raw files, the note and original script are preserved as isolation-setup-missing-vendored-dependency artifacts. The corrected archive includes exact tracked third_party/ultraviolet bytes for each checkpoint. This was neither a product finding nor causal RED. Both temporary archives were removed; registered worktrees and primary source/test hashes stayed unchanged.

Initial committed RED52f26fd0 has model/runtime byte-identical to official pre-code ff74284f and initial test SHA `9c6464633b11d603bc3cc070a00cdd630aefd67edb4906e817f6752777b95596`. The three legacy test files are identical between that RED and final source. Twenty supplementary copied/unexecuted/concurrent checks were transparently added after code/initial120-leaf GREEN. I replayed the exact initial test bytes, not final private-type supplements on old source; no compile/setup failure is counted as RED. Final author evidence records actual working-file hashes while Git HEAD was metadata parente9209822, without pretending the later implementation commit already existed.

Raw commands/output/source hashes, failed-leaf details and cleanup assertions are retained in independent-check-summary.json and corresponding run/stdout/stderr artifacts. independent-checks.py and reviewer-extra-test.go.txt preserve reproduction. The64 failures reproduce the ordinary ownership contract;56 genuine controls pass. They are not relabeled as native UnsupportedBody failures.

## Evidence audit

All181 FINAL-HASHES entries match exact fixed Git size/hash, with zero errors; manifest SHA `86cef5dcfd7c51844b306139ada006c777225b981fa4e7b9f59b769761f39561`. All6 source/test pins match. All8 historical gzip artifacts decompress to their declared raw size/hash and exact original f6e089e6 Git bytes. Deterministic mtime0/empty filename and historical diff-check exit2 are retained; current final diff-check is clean without whitespace exceptions or normalization.

I recomputed author raw Go event counts:

- Initial RED:68 named fail/61 pass;64 leaf fail/56 pass; no skip.
- Final focused:151 named/140 leaf pass; no skip.
- Full Go:3495 named/3264 leaf pass plus4 pre-existing skips.
- TUI/editor/storage race:1646 named/1487 leaf pass plus3 pre-existing skips.

Full vet/build, focused/full tests, race, normal review adapter and Windows production cross-vet/build receipts exit0. Raw normal-adapter JUnit contains7 passing checks. All209 Windows selected-source pins (206 Go/3 embedded text) across16 actual application packages match fixed source. Broad Windows vet/build retains unrelated O_NOFOLLOW and Getrusage/RUSAGE_SELF/Maxrss research-helper failures. These broad checks were audited from source-bound raw evidence, not redundantly rerun here.

Existing skips are Advance layout oracle, Bold PTY roots, separate CharacterRepeat CLI artifacts and Windows-native namespace on Linux; race has the latter three. No ownership case is skipped. Cross checks are not native Windows execution. Final exact-candidate PowerShell/default-shell/overwrite CI and physical input, later Mac and original/native qualification remain open. No pre-review/status output is substituted for real Go evidence, and no unrelated product approval follows.

## Step3.5: all17 contract dispositions and concrete round-trip

All17 files are enumerated, size/hash checked and byte-identical to pre-code input; see contract-round-trip-inventory.json. The following separates actual host-boundary checks from unchanged orthogonal examples.

| Contract | Disposition / concrete implementation evidence |
| --- | --- |
| automation.md | In scope for real ReadMergePrimary/Secondary callbacks with tracked PRIMARY.WP5/SECOND.WP5 and independent queue controls; ReadMacro remains specialized. Macro/merge language/output/effect examples otherwise unchanged, not newly qualified. |
| coverage-concordance.md | Orthogonal documentary source/menu/version/lesson ledger, exact bytes unchanged; callback success closes no parent/lesson/family. |
| coverage-leaves.md | Orthogonal WP21 steps/menu/corrections/status data; no new command or verified scenario mapping. |
| editing.md | In scope for one document/cursor/history chain: full observed Session/native/source/Birth conservation under genuine foreign/stale/bare delivery, with real own callback still deliverable. Literal paired-code/deletion/Undelete behavior is unchanged. |
| files-platform.md | Direct host safety: real Observe/WriteSnapshot/PublishCandidate/workspace publication/append and missing/stale/Close/capacity refusals, actual own late files/reconciliation. UI cancel never means disk rollback. Original Save/overwrite wording/resource/platform semantics remain independently gated. |
| language-data.md | Preserve dedicated proof owner/kind/proofAdd and bare-proof notice, backed by unchanged specialized paths and audited full/race tests. Other character/locale/resource examples orthogonal. |
| layout-resources.md | Orthogonal geometry/printer/resources; WindowSize81/25 is only a stale-UI control, no metric/print qualification. |
| macro-fixtures.json | Orthogonal immutable original observations/opcode/merge fixture expectations; no new original run or full language verdict. |
| macro-framing.md | Preserve ReadMacro capability/source/worker receipt caller; WPM framing/opcode/call-depth/CLI examples unchanged and not executed by this review. |
| native-fixtures.json | Orthogonal native parser corpus/limits; tracked fixture/provenance remains exact, with no format-wide qualification. |
| native-framing.md | Conservation only: private receipt never serializes prefix/body/packets or changes parser/writer bounds, unknown owners, errors or fuzz CLI. Byte/source tests and two-file production diff substantiate this. |
| resource-readiness.md | Orthogonal acquisition/rights/readiness policy. Authored temporary Open roots provide no private/original/ROOT/P/TEST/CONTROL authority. |
| session.md | Directly implements pending IO's foreign/revision/cancel safety: exact queue/one-use check precedes unsettled/reconciliation/Session.20 genuine foreign controls, own/stale/late/retry/duplicate cases test the boundary. Original keys/prompts unchanged; new refusal notices are host diagnostics, not invented original strings. |
| startup-family-successors.md | Orthogonal WorkingLease/successor/epoch API, unchanged; private TUI request identity is no serialized grant, supervisor resource or new public lease. |
| structured-graphics.md | Orthogonal WPG/equation/table/box/resource/native semantics. Safer generic/merge host admission qualifies none of them. |
| mission1-closeout-coverage.json | Approved planning index only, unchanged. Frozen6d catalog/status does not claim these later110 bytes or broader generic Read finding.244/91/36/49/full acceptance remain separate. |
| mission1-closeout-coverage.md | Approved dated narrative only, unchanged;109/110planned and initial ReadSelection-only account are historical, not evergreen product claims. |

Closed-set check: no public/native enum, command, error category or format constant is introduced. ordinaryReceipt/ordinaryReply are private live types without serialized values. All ten existing ordinary IntentKind identities are mirrored by independent public pending-kind assertions and real callback/control cases; the matrix enforces ten unique nonempty rows and the producer/caller census matches source. New one-start/one-delivery behavior is checked using16 actual invocations per kind, unexecuted/copied metadata negatives and reviewer race/alias cases. Specialized first/macro/proof vocabulary and typed boundaries remain preserved. No new runtime constant lacking a test/doc mirror is introduced, and no old literal contract is promoted to original qualification.

## Frozen identities and handoff

- model.go SHA: `2347ea49310aee1c93bc9c47fbb3fb507461a4d50484ce4f0b4526cf81527338`
- runtime.go SHA: `9fe2510c4d0ef799b2a74a5e83db8c91a826f8974e59cd3c1e4af9a5b9011169`
- io_completion_ownership_test.go SHA: `474197d47325987972989955b92bb4419727e648a3afa131e3339e5314519869`

No primary/index/Op/status/lifecycle write, linked worktree, push, reference/private/VM/Original/P/TEST/CONTROL/Mac or qualification-clock action occurred. Only read-only review and authorized isolated Linux product tests took place. All49 families and genuine original/native/public/platform gates remain required. Structured reviewer-renata/approved evidence accompanies this report for ROOT's canonical deterministic capture; this reviewer does not transition live state or approve unrelated108/109/107/M1 work.
