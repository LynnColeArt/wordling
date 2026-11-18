# WP110 scratch acceptance-test preparation

**Prepared tests only; waiting for ROOT’s live writer turn.** Actual claimed WP110 and its OPEN generate Op remain as registered. This stage does not close/relabel the Op, commit RED, create an implementation, approve WP110 or claim an official baseline. No production edit or private-envelope prototype occurred anywhere.

Actual profile `implementer-ivan` was resolved read-only; explicit `implement` governance and cited043/044/045/051/dependency-hygiene context were loaded separately. The committed preparation Op remains action **generate** (`01M7R3NGKCNEE16DPQDXJT6QW0`). Full committed governance text, canonical task, staging contract and Rena combined scope were read. ROOT/native109 retains live index/source ownership; no other Op was dispatched or completed.

## Frozen source and isolation

- Frozen input Git: `6d594d15fe16aae66fd6243b24be2e4eebacccc6`. All production members come directly from that Git tree. No uncommitted107 helper or later production overlay entered the test closure.
- A bounded Git archive contains500 files: Go source/tests, go.mod/go.sum, third_party, testdata and the exact embedded proofreading resources (4,555,746 source bytes). Four small explicitly pinned pre-existing fixture files supplement it: ORIGIN.WP5, PRIMARY.WP5, SECOND.WP5 and M38.WPM. The very large documentary/evidence tree was not copied. This is a focused test closure, not a full-tree Go baseline.
- Every unchanged archive member was checked both against its initial SHA256 and its exact Git blob identity. Exactly the three declared legacy test files differ; the new owned test is additional. All production Go hashes are identical before/after every run. Gofmt reports no changed draft file.
- No Git worktree, .git directory, branch/ref/index mutation or live primary write was created by this stage. Raw worktree observations retain another actor’s primary HEAD progression; registered paths/branches match. No concurrent actor checkout was touched.
- Final run explicitly uses task-local GOCACHE/GOTMPDIR, GOTOOLCHAIN=local, GOPROXY=off, GOSUMDB=off and -mod=readonly. Earlier exploratory runs used the existing Go build/module caches; authored source/tests/evidence stayed under this scratch root. No dependencies were added or upgraded. Go1.26.4 linux/amd64 and executable hash are recorded in each run receipt.

## Stage for the later official RED commit

Only the new test plus three narrow legacy diffs are staged; production changes remain forbidden until ROOT captures the official baseline and commits genuine RED in the primary checkout.

| Draft full-file result | SHA256 |
|---|---|
| `internal/tui/io_completion_ownership_test.go` | `9c6464633b11d603bc3cc070a00cdd630aefd67edb4906e817f6752777b95596` |
| `internal/tui/original_test.go` | `d9fe0bce09c173e1ca9f904ede736ae979004c75c28d819930fc162619d7b8bd` |
| `internal/tui/editable_test.go` | `499aedcc2c8160265a8c9126671a49de74eb89436fccac698ba6ec812a0d80be` |
| `internal/tui/model_test.go` | `323f1827d74796a14827124f303a8bd8f97a335f7f4ea7ba679286ab4190eaf3` |

| Narrow legacy patch | SHA256 |
|---|---|
| `stage/legacy/original_test.go.diff` | `cf67f75f704973c12555ff4ef209e7a06defe5f52e2442fc6bf5efab6d3464d4` |
| `stage/legacy/editable_test.go.diff` | `340282d385c9f4887c68f8fbd18926e456a59c6dbd0b8f9d00866941d2470e45` |
| `stage/legacy/model_test.go.diff` | `3bf0d8fd292a8733f198c0546fdf8403ca91b6fefc975990bad8664f4d538326` |

The new test compiles on actual pre-code6d without any future private receipt type. It reuses the existing press/key/drain helpers; its finite fixture/queue helpers use Open and actual Model.Update key sequences, assert the intended real pending Kind and hold the returned opaque tea.Cmd. No positive storage Result or owned receipt is manufactured. Foreign positive controls execute another real Runtime callback and independently require its Completed result to succeed.

## Actual exploratory RED and positive controls

Final exact argv is retained in `final-local-cache-r5.json`: `go test -mod=readonly -count=1 -timeout=90s -json ./internal/tui -run ^Test(OrdinaryCompletion|BareUncertainResultKeepsAuthenticPendingWork|ActualPublicationAndUnboundForgedErrorAreDistinct|CloseGatesQueuedIOAndRetainsStartedReceipts)`. Exit1; **120 leaf checks:56 pass,64 fail**. Parent/group/package events are not counted as additional leaf checks. No build/setup failure occurred in this final run; stderr is empty. Source/test/raw/tool hashes bind the result.

| Matrix / boundary | Leaf outcome on6d | Causal observation |
|---|---|---|
| Real foreign Runtime,10 ordinary kinds × different/same root |20 fail|Each foreign callback succeeds in its own Runtime, while the held current callback remains unexecuted; current PendingIO incorrectly becomes0.|
| Own callbacks without interference |10 pass|All ten actual queue/dispatch paths work before any ownership fix.|
| Stale Model, one actual execution, duplicate callback/redelivery |10 fail|Stale UI cannot steal the callback and duplicate invocation stays nonexecuting; raw redelivery still reaches Session and changes Detached. This is distinct from a missing-type compile error.|
| Close/capacity refusals, all10 kinds |20 pass|Close happens before callback; capacity uses enough real diagnostic reads to reach1024 receipts, never assigns issued. Refusal settles its own queued work without IO or Completed growth.|
| Cancel before/after execution, all10 kinds |20 pass|Own late callbacks settle detached work; actual disk publications retain reconciliation and remain on disk. UI cancel does not undo IO.|
| Real missing-file failure and retry |2 fail|The first genuine error settles; old error redelivery changes Detached during the newer pending request. Real retry remains deliverable.|
| Actual stale-source publication failure |3 pass|WriteSnapshot, PublishCandidate and PublishEveryday refuse after real source replacement, preserve loaded bytes/binding and create no destination.|
| Bare keys / uncertainty error / Published outcome ×10 kinds |30 fail|Explicitly unbound negative payloads wrongly consume pending work or inject reconciliation; these are never called genuine owned receipts or real disk-fault evidence.|
| Reordered old success after executed retry |2 pass|Old success does not consume the newer executed-but-undelivered read.|
| Three narrow legacy assertions |1 pass /2 fail|Opaque Close remains correct; the two corrected bare-forgery negatives fail on the old permissive boundary.|

Eight selected unchanged first-save/macro/proofreading/dispatch top-level tests also pass (**13 leaf controls**,16 pass events including parents). Their command/raw/hash receipt is `unchanged-specialized-controls.json`. These source contracts were not edited. The three original unmodified legacy tests pass in a separate narrow comparison run; revised assertions preserve real positive publication and turn the forged positives into explicit unbound negatives. This comparison is not the official baseline.

Initial exploratory mistakes remain disclosed in raw artifacts: the first foreign draft used a10-character workspace output basename, producing two invalid DOS8.3 setup cases; this was corrected to OTHEROUT. An early legacy draft used a nonexistent storage.SaveOutcome name; that compile failure is preserved and is **not RED evidence**. The final four-file hashes and final successful compilation supersede neither raw record. No production fix was tried to make anything green.

## Exact generic Read versus ReadSelection witness

`genuine-Read-same-root-witness.txt` and `genuine-ReadSelection-same-root-witness.txt` contain exact verbatim go-test output from the final task-local-cache run, including before/after native hex, source identity, Birth classification/equality, pending presence, colliding keys and separate Completed counters.

- Generic `Read`, same root, Operation1/Revision1: ownCompleted0/foreignCompleted1, PendingIO0; current pending becomes absent, native bytes acquire SOURCE, source goes nil→foreign real file identity and Birth goes New→Loaded. This is an additional UI/source-adoption mask inside the approved all-ordinary boundary. It is **not a disk-corruption observation**.
- Workspace `ReadSelection`, same root, Operation1/Revision1: ownCompleted0/foreignCompleted1, PendingIO0; native/source/Birth and real Session.Pending remain protected, while Detached is recorded. This matches the earlier minimal repro’s narrower protection/accounting distinction. Do not generalize that distinction to “native always safe.”

Foreign publication controls legitimately write their foreign OTHEROUT destination; ownership assertions concern the current held request/UI and its OWNOUT outcome. Current source/native hashes and all real error/publication receipts remain separate.

## Source/design handoff

`ordinary-source-census.json` pins the actual constructor/caller/removal/reconciliation spans. Model.reduce is the ordinary live dispatch route. Runtime has five ordinary raw resultMsg producers covering normal completion plus stopped/capacity ordinary/everyday paths. Its only other live Model command caller is the specialized ReadMacro route. First-save firstReply/ticket, macroIOReply/receipt and proofReply owner/kind authentication stay independent and unchanged.

Host/request custody must be checked before numeric unsettled removal, Reconciliation/detached-warning updates **and** Session delivery, across all ten ordinary kinds and refusal paths. The new table is a non-vacuous behavioral floor: every row must queue its exact real Kind; ten own controls prove valid acquisition. An actual implementation must preserve one execution, bounded1024 receipt lifetime, immutable diagnostics and actual UI transition authority, while no stale Model or copied/unbound payload can steal pending custody. Do not turn Runtime.command diagnostics into an alternative live Model route.

No private type/layout is prescribed or prototyped here. Reviewed source/history show specialized macro/first-save/proof authority plus earlier modal/nested-macro ownership changes; these alone do not establish a repeated ordinary-bookkeeping point-fix history. Record the history accurately and apply DIRECTIVE040’s prescribed structural review if its actual recurrence/contested-class trigger is established before production work. The already-approved solution scope is structural across ordinary producers; a ReadSelection-only patch cannot pass this matrix.

The narrow legacy changes: original_test renames its forged uncertainty positive to a refusal test that preserves an actual pending callback and later verifies real publication; editable_test executes and accepts the genuine publication unchanged, then tests a separately bare forged error while another real publication is held; model_test replaces only a queued Close type assertion with opaque actual delivery plus stronger pending/no-IO/error/receipt checks. Other diagnostic result assertions remain unchanged. Genuine storage-error/late-publication evidence is retained; no real Err was mutated into an “authentic” uncertainty receipt.

## Prior evidence and later work

Root’s frozen f6 foreign-Runtime repro is an input, not this task’s official RED. The hash-bound107 integration draft is also an input only:59 leaf passes/two real Copy+foreign-accounting failures, tied to0d5dc74c… TUI and27a1a53c… editor test bytes. Its older uncorrelated/reconstructed history stays separate. No107 helper was imported into the draft Go package.

ROOT must capture the official clean baseline, adopt these exact reviewed test bytes/diffs, run/commit genuine RED, then explicitly hand off the production writer turn. Full tests/race/vet/build, exact Windows cross checks and later independent implementation review belong after that source stage. This exploratory scratch task claims no full Go baseline, GREEN, native-Windows/Mac result, reference/Original/TEST/P/CONTROL action, source/audit/matrix/CMD51-065/E3/M1 promotion or compatibility acceptance. All49 families and original interoperability obligations remain open.

Archive, tar and task-local compiler scratch were removed after final preservation; no registered worktree was created. The manifest records exact cleanup and stable registered paths/branches. Authored drafts, narrow patches, raw results, pins, governance and reproducibility scripts remain for ROOT’s quiet-point preservation.

The two live production owners still rehash to the frozen6d values at handoff. All12 read-only task/governance/adoption inputs remain unchanged. All three narrow patches were independently applied to exact6d legacy test bytes and reconstruct their pinned full-file draft hashes. `reproduce-prep.py` rebuilds only the pinned scratch closure; its optional --run is separate. Early compiler caches were ordinary tool caches, not a primary source/index mutation.
