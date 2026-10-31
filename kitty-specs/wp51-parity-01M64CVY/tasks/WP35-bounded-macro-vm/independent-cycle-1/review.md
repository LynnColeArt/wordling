# WP35 independent review, cycle1

Reviewer codex/reviewer-renata, independent of implementation author. Actual lane-o
source127f211ad51a6cc2b8ba24d7f7b9d1a66eb54e18 + evidence425aeb08a207193bf52499d19cd3b57ffd81c44e.
Runtime prompt2d694cc4c5754e6eb64adf3da834eb6d. Verdict: REQUEST CHANGES, one P2
bounded-work finding. See review-feedback-1.md and the exact inert-archived overlay
reproducer. No implementation fix performed by reviewer.

## Blocking finding

startEach (loops.go35–45) eagerly evaluates/copies every list item in one charged
execute step. A public native8,204-word source with outer4096-word value and1024
inner VARIABLE references materializes4,194,304 words/16,845,504 allocated bytes
with ONE remaining run/slice unit: running Steps8205→running Steps8206, quota1,
Steps limit8206/OutputWords1. This bypasses actual statement/word work accounting,
not merely an arbitrary timing or memory preference. Exact repeated reproducer
fails actual test assertion, exit1; source/codec/native inputs unchanged.
Approved contract requires actual work bounds. A numeric counter-only fuzz invariant
can remain true while this real evaluation/copy work escapes it. Repair must bound
aggregate work/allocation and slicing, retaining supported semantics and typed
limit outcomes; no scope/budget waiver or source rewrite by reviewer.

## Verification that passed

- Fresh actual-lane build, go test -count=1 ./..., vet, race-count1 all pass.
  Genuine configured JUnit:7 passes,0 errors/failures/skips. Discovery consists of
  runtime/wpm/wp51; root's archival naming correction introduces no product code.
- Independent20s FuzzCompilerMachine smoke passes1,693,212 executions, two workers.
  Author's60s/600s logs, measured resources and12 killed mutants inspected;
  none covers the exposed high aggregate value-expansion work. No660s duplicate run.
- All51 final and10 metadata-refresh artifact seals match actual committed Git
  blob/length/SHA; frozen actual source/test/corpus/module/codec hashes match.
  Approved32/33/39 sources/review authority bindings match their exact Git blobs.
  Production files remain identical to127f211; review makes no source mutation.
- Native20 historical macro cases and4approved39 replays run real Parse→Compile→
  Machine→observable sink, with exact recorded native/source hashes.15 merge cases
  excluded.131 recording prefix,132 host Repeat client and178 query/manualREADY
  projections are explicit component context, not fake integrated features.
- Source review confirms context/wpm/pure standard helpers only: no host IO,
  storage/editor/document/TUI dependency, shadow document or native serializer.
  Image/Program wrappers, policies, callbacks, pending names/results and owned
  Failure values copy; independent runs do not share mutable variables/handlers.
  Conditions are explicit and distinct from host errors; receipts retain partial
  outcome externally and no rollback is promised. Pending wrong/duplicate/late
  resumes and callback reentry refuse. Static unknown/dead-branch and active-
  handler refusal is retained; nested children preflight before child effects.
- Normal-file QUIT remains tied to declared DISPLAY OFF/unfired handler context;
  actual39 root/child stop-all traces are separate from unreached parent136 and
  unqualified active-handler/structured/broader contexts. No original VM used here.

## Anti-pattern checklist and retained scope

1. Dead code: N/A product integration for this staged foundation; actual external
   public-API tests/corpus consume the machine. Editor36/TUI37 remain queued;
   zero product call-site claims or fullFR012 closure are fabricated.
2. Synthetic fixture: PASS. Real source images run production code and emit ordered
   sink receipts. Derived adversarial inputs are labeled component tests, not
   original-native/product acceptance results.
3. Silent empty returns: PASS. Malformed/unknown/host/condition/pending/limit paths
   use typed diagnostics/outcomes; nil/zero values are not accepted instances.
4. FR coverage: FAIL for NFR003 bounded work due to the P2 above. Other scoped
   native retention/receipt safety/evidence/FR012 component assertions pass;
   full FRs remain open and no product macro/merge feature is accepted.
5. Frozen surface: PASS. Codec/native/module/source authorities unchanged; owned
   implementation/evidence only. Supported planning propagation is not source drift.
6. Locked decision: FAIL for actual statement/word-work budget contract. Native
   formats/rights/architecture boundaries otherwise preserved.
7. Shared ownership: N/A implementation overlap; runtime35 namespace only,
   approved dependencies consumed without modification.
8. Production fragility: FAIL for bounded allocation/work safety in startEach;
   no new panic/host IO or invented original error handling identified.

Read canonical prompt, actual approved32 API/grammar/budgets and33/39 evidence,
project AGENTS/charter/compatibility/roadmap/reviewer doctrine. No authored Code
Review Checklist exists; canonical review/event seam applied. Original-only cases
are not Wordling native output; source-level interpreter tests are component only.
Source lane unchanged except runtime-created .spec-kitty coordination. All38
obligations/91 groups/nested leaves remain M1, PDF M2 after full acceptance.
