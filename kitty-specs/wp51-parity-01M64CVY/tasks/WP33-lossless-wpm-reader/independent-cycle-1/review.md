# WP33 independent review, cycle1

Reviewer: codex / reviewer-renata, separate from WP33 author. Source fixed at
`a18f4b8d28c643985604a806404a48dba9893b85` plus evidence packaging
`8fa1ecf2708990e3ca8bd349b9da23fa070f113e`, actual lane-n.
Review prompt:25aab790e6a647e1a001dc9253f957fa.
Recommendation: approve this bounded immutable WPM reader component. No actionable
correctness or safety finding. Full38 obligations/91 groups remain open.

## Scope and design

Read canonical runtime prompt, project charter/compatibility/roadmap, actual
approved WP32 contract4eb851e and applicable reviewer profile. The charter has no
authored Code Review Checklist section; CLI reported that absence explicitly.
Reviewed both WP33 commits:21 owned paths under internal/macro/wpm only. The
312-commit mission-base comparison includes inherited dependency/history; review
attribution is the two owned commits plus exact approved dependency comparisons.
Approved DOC codec e7de080 remains byte-identical. No storage/editor/document/TUI,
filesystem, execution, source writer or product entrypoint is introduced.

Installed public API matches approved WP32: owned Image, copied Export/Description/
BodyWords/Inspect findings, SHA256, checked absolute spans, positive bounded limits,
typed Failure and explicit unknown-from-bytes release evidence. Arithmetic bounds
are checked before addition/access/copy; body traversal is bounded relative to B,
including FLOW169/body75. Opaque prefix slots, description gaps, unknown native
words and suffix bytes retain exact bytes and execution-blocking diagnostics.
Overlapping nonempty prefix extents and speculative chains refuse. Known word
classification never grants operand/execution permission. First-terminal scanning
preserves a subsequent odd suffix; DOC framing is never reused for WPM words.

## Independently executed verification

- go1.26.4 Linux/amd64 actual code lane: go build ./...; fresh go test -count=1
  ./...; go vet ./...; fresh go test -race -count=1 ./...; gofmt -l changed Go.
  All exit0; gofmt emits zero paths.
- Real configured scripts/review_checks.py emits7 passing JUnit cases,0 failures,
  0 errors/0 skips. This is separate from automatic for_review gate's0 selected
  targets; no claim that the transition gate executed these checks.
- Independent20s two-worker FuzzImage smoke:1,546,684 executions, PASS/exit0.
  Retained author60s and600s original-corpus fuzz logs inspected;600s reports
  44,600,056 executions/PASS. These are bounded searches, not universal proof.
- Exact approved32 ledger SHA checked. Owned test manifest is an exact projection
  of all46 approved export records, preserving every included field. All46 actual
  originals match their recorded size/SHA/Gitblob;22 distinct hashes.
- All20 author artifact manifest entries match actual committed Git blobs and
  bytes. Frozen DOC source unchanged; both change commits stay in ownership.
- Additional isolated reviewer tests compile a SHA-identical copy of production
  image.go, use read-only original ABC bytes, and run with race/count1: disjoint
  opaque indexes, second-index alias rejection, zero-length opaque pointer policy,
  shifted description, embedded early zero, first terminal/suffix, exact budget
  edges,1,048,576-word finding dedup and copied findings. All3 tests pass. Isolated
  tests are adversarial component evidence, not additional original-app results.
- Author8 killed mutants, resource/benchmark logs and immutable provenance
  inspected. Measured RSS includes Go subprocesses, as documented; no parser-only
  or universal process-memory claim. No VM or CMD51-199 test run by reviewer.

Fresh commands, output hashes, genuine configured JUnit, original/source/seal audit,
isolated reviewer source and raw tests are retained alongside this report. Initial
review audit used full-record equality but the local fixture file intentionally
projects metadata; corrected fieldwise projection audit passes and is documented
in audit.json. This was a reviewer assertion correction, not a source defect.

## Anti-pattern checklist

1. Dead code: N/A for product integration in this explicitly staged foundation.
   Actual production-import grep has zero external callers today; external public
   API tests invoke real codec. WP34/35 are the contract's queued production
   consumers, then36/37 editor/UI. Integration is NOT RUN; no full feature closure
   or fabricated caller. Approval does not satisfy their later integration gate.
2. Synthetic fixture: PASS.46 original WPM byte streams are actually parsed,
   inspected and exported through public production API; mutations test malformed
   behavior. Tests cannot pass after removing production implementation.
3. Silent empty returns: PASS. Nil/zero Image accessors intentionally return
   empty copies/zero inspection/hash; zero value is explicitly not accepted.
   Parse refusals always return typed Failure and nil Image. No guessed success.
4. FR coverage: PASS for this WP's bounded component scope only. FR002 document
   type separation/unchanged reader, FR003 companion exact preservation, FR012
   native macro word/source boundary; NFR001 no-edit equality, NFR003 malformed/
   resource/fuzz bounds, NFR004 hashes/provenance/actual checks. None of these full
   FRs/NFRs or original macro execution/record/editor/conversion are closed.
5. Frozen surface: PASS. Owned-only changes; raw originals and DOC reader frozen.
6. Locked decisions: PASS. No format mutation, lossy Unicode/CP437, proprietary
   code/resources, original error fabrication or macro execution authority.
7. Shared ownership: N/A source ownership. Codec's namespace belongs solely33;
   later34/35 consumers depend on it without duplicate filesystem/editor engines.
8. Production fragility: PASS. No panic/raise or unchecked recursive/index-chain
   traversal introduced; malformed/limit/unsupported outcomes are explicit.

## Retained limits

Read-only framing and word classification are implemented; operand compilation,
execution, production loading, UI run/repeat/stop, original-editor/disk roundtrip,
WPM saving/recording/conversion, nonASCII/resources and complete M1 remain open.
Physical input and original release identity cannot be inferred from file tuple.
Review does not grant accept/merge or M2 permission. No implementation/evidence
source file changed during review; runtime-created untracked review-lock.json is
coordination metadata, not a code mutation.
