# WP47 — New buffer first binding

This is component-level evidence for the editor reducer and actual approved storage41. It does not exercise cmd/wordling, a terminal host, or the original application. WP48 must supply serialized host scheduling, original-key routing and live execution. No original guest was launched for WP47.

## State and authority

`Session.New` uses the approved document46 constructor with HistoricalUS51DosTextStandardPrinter. NewUnpublished retains its native New birth, genesis revision, immutable cursor and history. Empty genesis is unmodified but unsaved. F10 observes a target through the existing rooted Directory and issues PublishNewBuffer only for an absent destination. ExecuteNewPublication uses actual PrepareNewPublication/PublishNew; a successful receipt advances to AwaitFirstRead, not clean or named success. ExecuteFirstRead reads through the SAME captured Directory. Only full Outcome.Identity (including mode and timestamps) plus exact whole bytes permits NewAnchored. Metadata-only mismatch is a conservative Linux safety refusal.

The first storage source anchor is permanent and separate from display name, latest publication receipt and saved revision. Binding does not Parse or Retrieve the native document, rebuild history, change its birth or invent a loaded original. OriginalExport continues to return NoLoadedOriginal. Later sourced SaveAs keeps the first anchor; changing that source invalidates later publication through the existing guard.

RequestKey is an opaque issued correlation value, not a general idempotence promise. The host must execute once per key on the current serialized session. Captured request/reply capabilities bind operation, reducer/document revision, screen, buffer, native birth, rooted acquisition, destination, name and candidate bytes. Defensive wrapper copies preserve the acquisition; independently opening the same path does not acquire the same capability. Forged mirrors, foreign or stale receipts and caller wrapper replacement cannot redirect or falsely complete a transaction.

Successful publication followed by failed/mismatching Read becomes PublishedUnbound. RetryFirstRead is a host safety operation, not an original key alias: it only rereads the captured first receipt/root/name, never republishes. Cancelled/lost publication becomes PublicationUncertain and cannot retry, exit successfully or reconcile from matching bytes. Shared Close cannot be repaired by opening the same path again. A known no-publication failure requires a fresh user save transaction. Existing target replacement remains UnsupportedReplacement.

## Source and API handoff

Production implementation: internal/editor/new_binding.go, with integration in session.go, editing.go and macro_session.go. Public seam: Intent.RequestKey, RequestKey.Valid, ExecuteNewPublication, ExecuteFirstRead, RetryFirstRead and Snapshot.NewPhase/GenesisRevision/FirstPublication. No production storage, document, native reader or TUI changes.

The constructor is startup-only. F7 clear does not construct a new native document or reset global history; editing that cleared nil document remains refused. New-target macros and screen switching are unqualified and refused. Existing WP36 history suspension and stored fragments remain authoritative. No modern undo model, replacement support, unqualified interleaving or broader New-buffer operation is implied.

Prerequisite context: base e7a8b1e9351d791729e083a91b6dc3bcb7ce2d04; approved36 b184049a223e346588641ebf4434cc9d88f4977e; storage41 0df934ce3185d73ec53be6d887fba513b44ab803; approved46 44aab36accdf14a370a67fd73945907871ab7193. N1 decision: docs/research/continuation/first-binding-design/decision.md, SHA256 2c5c875f2a468db0abe24d13c7fb614cc9d8fa8326b2abf78bb255f63274c288; independent review reviews/cycle-1/report.md SHA256 3f907b582e71f7387686bdc9d661686724535102f7d8c583247428fb18c094c7. These source links do not promote parent conformance.

Original context leads remain bounded: CMD51-066, “Name a new document with F10”, WP51-020, REF51 printed565/PDF582; CMD51-240, “Cancel Exit save prompt with F1 across declared contexts”, WP51-029/WP51-007, REF51 printed194/PDF211 and55/PDF72. Approved43 evidence is under docs/research/continuation/native-genesis/analysis; its five contexts were visited after F3 Help/Space and two empty AltF3 visits. They do not establish unvisited startup defaults. ASCII filename F1 and dirty Save-question F1 tests preserve those context distinctions. No canonical case status is changed here.

## Actual validation

- editor-events-final.jsonl: 253 passed Go test nodes, zero failures/skips. Includes public actual-filesystem publication/read, wrapper/capability replacement, cancellation, wrong inode/equal bytes, changed metadata, Close, retained birth/history/anchor, existing-target refusal and genuine euid1000 permission failure followed by a fresh user retry.
- configured-final.xml/log: actual seven configured checks pass, zero skipped (inventory, scenarios, review adapter and actual Go discovery/build/test/vet). These are product-package checks, not empty primary discovery.
- race-editor.log and race-dependencies.log: editor plus actual storage/document race checks pass. Final production sources are identical to the checked sources; later additions are tests only.
- fuzz60.log: final production two-worker 60-second FuzzFirstBindingAuthority run passes, 266098 executions. Test input length above64 is excluded by the harness; this is not an application format limit or a claim that every counted fuzz execution touched the filesystem.
- mutations/results.json: four compiling mutants killed: lost full Read identity, trusted public Published mirror, ignored outer unknown error, and cancellation falsely asserting absence. Maps replace only owned editor code during tests.
- benchmark.log: NewStartupState measured 4648 ns/op, 5112 B/op, 57 allocations on the recorded host. This is a startup observation, not a hard resource or refusal-cost cap. Repeated100 failed Read retries retain a single original first receipt and use fresh request identities without republishing.

`overlay/` adds TEST-only files to expose the actual unchanged41 private operation seam. actual41-fault-ports.log records real filesystem create/write/close/link/link-after/cleanup/write-plus-pin-close paths, distinct from editor-only synthetic error classification tests. Known typed no-effect envelopes may contain OS/cleanup causes; nested typed possible effects dominate, and an unknown OUTER joined sibling stays uncertain. No string classification is used. Public typed error clones cannot mutate sealed observations. There is no separate Flush/Sync hook in41: the close stage was tested, with no durability/fsync claim.

Development diagnostics remain in development/: superseded startup expectations, a temporary test syntax error and preliminary pre-counter-guard fuzz. Earlier editor/configured logs remain historical. Final authoritative filenames above disambiguate them; failures were not normalized into passing records.

## Component output and custody

producer/main.go invokes the real reducer and storage APIs. component-producer.bin is the exact Wordling component executable, not an original proprietary binary. source-and-execution.json records build argv, cwd/GOMOD/GOFLAGS/GOWORK, actual GoFiles, source inputs, binary digest and execution argv. final-source-sealed.json captures all91 final Go/module paths and proves all25 actual compiled producer files unchanged; its single subsequent changed path is test-only. Automatic Go VCS stamp is context metadata, not authority for the compiled working tree. No rebuild or normalization substitutes for the archived executable.

component-native contains the actual empty324B and ASCII329B before/published whole files and full actual identities in outcomes.json. Empty SHA256 b58c9e0fc115f1ff0f491e2fb8efbeb14bed9ade6a365ab4b50994f479d5832b; ASCII SHA256 6d7ce267bfb8be47c84e398ecfa34d7328f9837e9e969d3136e348d78b5e9476. Equality proves this component's publication preservation only, not original qualification or live UI interoperability.

manifest.json seals every owned changed source and evidence file except itself; verify.py checks working bytes and optionally exact committed Git blobs. Raw logs/binary/native files retain original bytes. All38 obligations/91 groups/36 lessons, nested scope, unsupported history/EC045/CountKnown and full M1 remain open; no PDF/M2, registry, proprietary media or mission acceptance claim.
