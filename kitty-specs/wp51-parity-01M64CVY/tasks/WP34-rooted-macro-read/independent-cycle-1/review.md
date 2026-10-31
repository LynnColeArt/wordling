# WP34 independent review, cycle1

Reviewer codex/reviewer-renata, independent of the implementation author.
Fixed source `079393305a054a45cfbf631d9ecafa0e2b82e5b7`, actual lane-b. Runtime prompt
`86072ce74fca4f0181a6d15d8573584c`. Verdict: REQUEST CHANGES, one P2 finding.

## P2: Image accessor exposes the owned snapshot for whole-value replacement

`internal/storage/macro_linux.go:15` returns `m.image` directly. Although wpm.Image's
fields are private and its view methods copy, the exported Go type can legally be
assigned through the returned pointer. Both `*m.Image() = wpm.Image{}` and
`*m.Image() = *anotherParsedImage` mutate the acquired Macro's native content while
m.Identity() retains its original source/hash. Macro.Export can consequently be
empty or different native bytes with an unchanged stored identity. This violates
the declared immutable acquisition/source binding, independently of later external
filesystem freshness (which is correctly not guaranteed).

The temporary public-API Go overlay reproducer runs the actual unchanged source:

```
go test -count=1 -overlay=/tmp/wordling-wp34-independent/overlay.json \
  -run '^TestReviewerMacroImage' ./internal/storage
```

Both tests fail their actual assertions (not compilation/setup): zero-value
assignment changes the snapshot, and assigning another valid parsed native Image
rebinds its bytes without changing source identity. The overlay adds only a virtual
reviewer test file from /tmp; no implementation, codec, original corpus or tracked
evidence file is edited. Exact reproducer and raw output accompany this report.

Remediation: preserve WP32's accessor signature while returning an independent
Image value wrapper/copy so whole-value assignment through any returned pointer
cannot alter the Macro's owned image. Approved codec methods already preserve
underlying private bytes; no codec rewrite or new filesystem engine is needed.
Add both public-API assignment regressions, retain original source/name/directory/
hash and copy-isolation checks, and rerun meaningful changed checks and race.

## Verification that passed

- Actual code-lane fresh go build ./..., go test -count=1 ./..., go vet ./... and
  go test -race -count=1 ./... pass. Three real packages; no Go discovery skips.
- Configured review_checks produces genuine7-case passing JUnit,0 failures/errors/
  skips. Changed-Go formatting and exact owned-commit whitespace checks pass.
- All15 artifact-manifest entries match actual committed Git blob bytes/lengths/
  SHA256; manifest SHA b6c948adfd85d75d57d935e48727e45f758c28bad543fbdeb1427f8e8201371d.
- All46 original WPM files/22 distinct hashes match pinned ledger and actual Git
  blobs. All4 inherited source-proof entries match their approved commits.
  DOC reader, stable acquisition/publication paths, WPM codec and fixture ledger
  remain unchanged. Only16 declared storage-owned paths change in this commit.
- Source review confirms ReadMacro reuses validName/readStable/no-follow/pinned
  directory/bounded acquisition and delegates to approved wpm.Parse. Malformed vs
  unsupported codec causes survive NativeRefused wrapping; filesystem/stale/path/
  input-limit errors stay distinct, without partial Macro results. DOC Read and
  PreparePublication continue rejecting WPM; ReadMacro rejects DOC.
- Actual fault tests cover read/close/stat/lookup failures, real source mutation/
  replacement/symlink changes after open, FIFO/unsafe-name/size refusal, closed
  directory, pinned root renames and concurrent reads. Inherited publication/
  source-guard safety tests pass. No macro-write/publication permission added.
- Retained60-second changed-name-boundary fuzz reports2,316,888 executions/PASS;
  six isolated wrapper mutants are killed. Those evidence records are inspected,
  not redundant new fuzz/mutation runs by reviewer. The immutable codec's prior
  parser fuzz is not claimed as this wrapper's validation.

## Scope/governance and retained gaps

Read full canonical prompt, AGENTS, reviewer profile/action context, charter and
compatibility/roadmap; actual WP32 API from4eb851e and approved24/33 dependencies.
The charter has no authored Code Review Checklist section. Enumerated contracts:
macro-framing's exact storage API is in scope and signature matches; native,
files-platform and language boundaries remain unchanged; automation execution,
layout/resource/structured/coverage contracts gain no implementation from this WP.
The one defect is behavioral ownership despite the correct API spelling.

Anti-pattern checklist: real public acquisition/fault tests call production wrapper;
no detached filesystem or synthetic pass; all refusals fail loudly; frozen source
and locked native/rights decisions preserved; narrow storage ownership only. Zero
production callers of ReadMacro exist yet, as explicitly staged for WP36/37; product
integration is NOT RUN. This foundation cannot close FR006/FR012 or parent scope.
No new VM/original run or product macro execution occurs in this review; WP25 owns
the reference oracle independently. Full38 obligations/91 groups remain M1 scope;
PDF is M2 after actual M1 acceptance. No accept/merge or original format change.

Source lane remains unchanged except runtime-created .spec-kitty coordination.
No implementation fix is performed by the reviewer. The actionable ownership
finding requires correction before independent approval.
