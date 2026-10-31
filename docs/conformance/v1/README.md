# Current conformance: maintainer CLI and evidence protocol

This layer is the current conformance authority for maintainers. Start at the
[generated index](index.md). The [registry](registry.json) contains the exact
historical source and retained documentary/resource ledgers plus current additions.
The [schema](schema.json) and stdlib semantic validator together define schema v1.
Schema versions describe project evidence tooling; native documents and companions
keep their original formats, with no Wordling wrapper or required sidecar.

Run from the repository root, with Python 3.9 or later:

```sh
python3 scripts/conformance/v1/conformance.py check
python3 scripts/conformance/v1/conformance.py validate --registry /path/to/proposed-registry.json
python3 scripts/conformance/v1/conformance.py import
python3 scripts/conformance/v1/conformance.py regenerate
python3 -m unittest discover -s tests/conformance/v1 -v
```

`check` validates the current registry, schema contract and deterministic index. It
writes nothing, does not check out Git files, run product code, invoke a comparator,
start a VM or change Git state. `validate` checks a proposed registry without
writing it. Both return JSON and exit 0 for valid integrity, 1 for invalid/missing
sources or claims. A valid integrity result never means M1 parity passed.

`import` explicitly creates the default schema/registry/index from pinned Git
blobs. It is idempotent and refuses to replace any nonidentical existing output;
this prevents erasing later evidence. `regenerate` validates the existing registry
and schema first, then atomically replaces only the index when necessary. It
preserves evidence/additions. Check failures write nothing. All output paths are
fixed within this owned namespace; output symlinks and root escapes are refused.

Git access uses argument arrays, full 40-character commit SHAs, safe relative
paths, read-only `cat-file`, no optional locks/replacement objects, 15-second
command timeouts and an 8 MiB per-blob/registry budget. No caller-provided branch,
option-like revision, shell command, executable or comparator script is executed.
Existing inherited working files must match pinned Git bytes; missing historical
review metadata can be read directly from its pinned Git object. Source changes
require a separately reviewed explicit schema/source-lock update, not a check-mode
checkout, automatic baseline replacement or modification of historical evidence.

## Historical source versus current evidence

Approved original catalogue: WP13 `18d6afe95ffcd676fc3f9e964dcad884c9a8c289`,
244 cases and 91 groups. The old 236-case primary snapshot is rejected. Source
SHA-256, commit and path for all inputs are in `source_snapshots`. Frozen original
rows retain exact titles, ordered associations, baselines, locators and original-only
statuses. Old generated research views contain historical present-tense statements;
links from the current README identify that temporal scope. Those statements are
neither current product verdicts nor a second current conformance authority.

All 38 obligations and 91 groups remain open. WP21's 29 reference leaves,
55 numbered workbook steps, 12 contexts, 9 menu alternatives, 36 lesson dispositions,
44 local case proposals and remaining version/coverage gaps are retained in full.
WP20's full resource ledger includes 23 formats, 30 locales, 6 field conflicts,
14 graphics input families and physical-printer/owner-decision gaps. Presence is
not qualification. These numbers are known minimum coverage, not exhaustive scope.

Schema v1 accepts bounded evidence rows only. It deliberately cannot close entire
scenarios, groups, requirements or M1: the source does not establish complete
command/resource breadth. No count, green validator or partial editing pass changes
that. Discovered leaves go in `additional_obligations` as stable `ADD51-####` rows
with exact parents/source locators/remaining work and `status: open`.

New authored cases use stable `EXT51-####` IDs, revision 1, inherited case parents,
feature/requirement links, known baseline, exact source locators and explicit
preconditions/steps/expected outputs. A correction uses a new stable ID with
`supersedes: {id, sha256}` referring to the prior extension's exact canonical
revision, retained earlier in the array. IDs never overwrite inherited cases or
silently replace existing revisions. Local CP/probe names remain proposals until
this authored case contract exists. This is the canonical extension mechanism for
older contracts requiring case expansion before acceptance; it preserves those
behavioral requirements rather than reclassifying local smoke probes as full cases.

Immutable fields are compared as typed canonical JSON trees, not Python's coercing
`==`: false cannot become 0 and a pinned integer locator cannot become a float.
All three mission defaults must specifically be boolean false. This enforces this
version's declared immutable-source contract, not a general rule about JSON Schema
numeric notation. Proposals are rejected unchanged, never normalized to hide drift.

Case revision is SHA-256 of UTF-8 JSON with sorted keys, compact separators,
`ensure_ascii=False`, followed by LF. This differs from the source-file SHA, whose
exact bytes are pinned separately.

## Current evidence and positive-claim integrity

Levels are separate: `documentary`, `original_observation`, `component`,
`executable_integration`, `differential`, `physical_qualification`. States are
`unverified`, `blocked`, `fail`, `pass`. The original WP30 tooling checkpoint had zero current rows:
original observations remain in the immutable historical rows. The current WP31 import is separately source-bound below.

Nonpassing rows have exactly `id`, `level`, `state`, `case_id`, `case_revision`,
`scope`, `note`. Positive rows replace `note` with `run` and `review`. Each `run`
reference is `{commit, path, sha256}` for an actual archived JSON Git blob;
`review` is `{artifact: {commit, path, sha256}, reviewer}`. The review artifact
must approve the exact implementation commit and name a reviewer distinct from
its implementer. Independent reviewers still judge whether evidence is truthful
and adequate; integrity validation cannot establish authenticity from a forged
repository history or substitute for independent semantic review.

The run JSON has exactly these fields:

- `kind`: `component-test`, `product-execution`, `product-differential` or
  `physical-qualification`, matching the requested positive level.
- `case_id`, `case_revision`, `scope`: exact positive-row/case bindings.
- `implementation_commit`, `implementer`, `executed`, `argv`, `exit_code`,
  `executable_sha256`: resolved source commit, nonempty actor/invocation,
  actual successful execution and exact executable identity. Product levels must
  invoke an executable named `wordling`; a helper/original-only kind is rejected.
- `build`: a hashed immutable Git reference to a separate build-provenance JSON
  record. That record has `implementation_commit`, `case_id`, `case_revision`,
  `scope`, `argv`, `entrypoint`, `build_argv`, `build_exit_code`, `environment`,
  `build_log`, `executable`, `review`. Code/case/revision/scope/argv and independent
  review must exactly match this run/evidence. Product entrypoint is `cmd/wordling`
  and must exist at the exact source commit. Build argv/context are captured, never
  executed by validation; exit code must be integer zero. Environment/log/executable
  are separately hashed committed blobs. The validator reads actual executable
  blob bytes and computes their SHA-256, which must equal the run's declared hash.
  A second asserted hash copied into the run is insufficient. Distinct builds may
  produce distinct executable bytes; each requires its own consistent witness.
- `baseline_id`: the case's exact original baseline.
- `profile`: nonempty `environment` and `resources` arrays of hashed committed
  witness references, and `qualification`. v1 recognizes only the pinned selected
  original environment/resource-profile bytes; unknown profile hashes/paths fail.
  Its known physical qualification remains `unqualified`. Physical passes are
  unavailable until a reviewed profile-qualification extension supplies real proof;
  mere installed-resource presence or a caller-supplied qualified flag cannot pass.
- `inputs` and `outputs`: nonempty arrays of distinct hashed committed raw blobs.
- `checks`: nonempty checks with `name`, `passed`, `comparator` (hashed committed
  implementation reference), `method`, `left`, `right`, `tolerance`.

`left`/`right` are distinct `commit:path` names from the raw inputs/outputs.
Every raw reference must participate. v1 supports exact `byte_equal` and
`json_equal` comparisons, recomputed by the validator from verified raw bytes;
`tolerance` is `exact`. `passed: true` is insufficient: unequal recomputed results
fail. JSON comparison compares canonical serialized structures, preserving value
types. Arbitrary external comparison code is never executed. Unsupported semantic
comparators require a separately reviewed extension; preserve a blocked/unverified
result meanwhile. Recorded comparator bytes bind the reviewed producer's method,
but cannot broaden these verifier capabilities.

WP30 imported no live positive product rows. Isolated synthetic Git history
in public tests exercises the positive protocol and corruption guards; it is
explicitly not product execution, compatibility evidence or a resource qualification.
WP31 consumes actual reviewed WP29 evidence; synthetic test envelopes remain excluded.

## Future normal acceptance workflow

A future readiness report may bind matrix criteria to exact registry/case/code,
independent review, original baseline/resources and raw comparison revisions.
It must list missing branches/known leaves/resources and unresolved discrepancies.
Only the normal mission acceptance workflow may write acceptance evidence/state,
and only after complete SC-001–005 and every applicable FR/NFR/C/FC obligation pass.
This CLI never edits acceptance-matrix.json, status events, WP lifecycle or mission
metadata. No full-parity percentage or queue-exhaustion shortcut is provided.
PDF and newly selected conveniences remain optional M2 after genuine M1 acceptance.

## Focused cycle-1 verification

The I1/I2 corrections and exact independent red/green proposals are retained in
[cycle-1 verification](verification/cycle-1/README.md). Old unbound positive controls
are intentionally rejected; upgraded isolated build-bound controls pass. At that WP30 checkpoint,
registry product passes were zero; the current WP31 import is described below. Historical initial verification files stay
unchanged. `run_mutations.py` now writes to a fresh temporary directory by default;
`--output` must name a new/empty replay directory, so review reruns do not rewrite
sealed logs.

## Actual WP29 ingestion (WP31)

Maintainers can reproduce the current translation without launching a product or VM:

```sh
python3 scripts/conformance/v1/ingest_wp29.py check
python3 scripts/conformance/v1/ingest_wp29.py audit-custody
python3 scripts/conformance/v1/ingest_wp29.py report
python3 scripts/conformance/v1/ingest_wp29.py validate --proposal /path/to/registry.json
python3 scripts/conformance/v1/ingest_wp29.py write
```

`check` is dry and refuses drift; `report` emits future readiness bindings; `validate`
rejects a proposed import unless it is exactly the source-bound translation plus
unchanged existing unrelated additions. `write` validates all inputs and the existing
registry before explicitly publishing deterministic registry/index/readiness outputs.
Repeated imports do not add identities/counts. Conflicting existing IDs refuse before
writes. All three outputs are staged before replacement; a normal replacement error rolls prior data back. This is not a claim of crash-atomic multi-file filesystem transactions. `prepare-builds` and `prepare-runs --build-commit <full-SHA>` were the explicit
one-time witness sealing steps; they refuse nonidentical existing witnesses. Normal
maintainers use the already committed pinned witnesses, never floating branch heads.

There are 47 positive exact-comparison rows: ten two-process app publication pairs,
eight two-original-run complete-PRN pairs and 29 actual no-edit reopen workers. These
are comparison rows, not scenario counts or compatibility percentages. Four additional
rows preserve historical failure, incomplete comparison, unsupported EC045 and
unqualified physical printing. The [readiness bindings](imports/wp29/readiness.json)
retain all20 acceptance processes, two sourced-fixture builders,16 fresh originals,
two old qualified controls, one old incomplete candidate (19 cumulative attempts),
60 exported native paths/29 workers/31 whole-byte aliases,27 read-only refusals and
two discarded unsaved gap0 admission probes. No old failed attempt is backfilled.

The exact existing Wordling executable A454 is archived as `wordling.bin`; it was
copied byte-for-byte from the surviving historical build, not rebuilt or stripped.
It is project-produced Wordling code, not proprietary original WP program media.
V1 recomputes that immutable binary hash and every admitted exact native/PRN comparison.
Original commands, terminal states, code gaps/history, resources and process custody
remain raw source-bound associations and independently reviewed observations; v1 does
not pretend its byte comparator decodes their semantics. Equal app repetition outputs
establish deterministic publication only; they do not independently prove all prompts,
commands, display geometry or original behavior. Complete PRN equality is the original
text-profile print-to-disk observation, not a Wordling print-engine claim.

Three identity roles are deliberately distinct. The historical build source is70f4a58a;
the reviewed lane snapshot is6deb5150, containing evidence6afecc04; the canonical review
records the primary evidence-only tree67bc334b. The last tree has no product source.
The narrow WP29 approval resolver accepts only the exact hashed canonical review and
sealed independent report naming those source/evidence/binary identities. It verifies
the complete90-path product/module set and hashes at executed70f and approved6deb,
plus captured nine local packages/GoFiles/cwd/GOMOD/GOFLAGS/GOWORK, source archives and
absence of hidden embed/C inputs in those local compiled sources. Other reviews retain
the strict original exact-implementation-commit rule. This is no generic prose approval
parser or new self-approval. Current lane-m's93 approved inputs include later C44 work
and are tested separately; they are never relabeled as the A454 producer. Automatic
Go VCS stamp remains misleading metadata, not compiled source authority.

The materialized v1 comparison witness limit remains8MiB. A single already pinned
17,829,376-byte historical helper verification report is provenance only: its Git and
working SHA/size are verified in64KiB streaming chunks, under a separate64MiB cap.
It is never admitted as a semantic/comparison blob or executed. Original manuals,
program/master images, dictionaries and printer resources remain private/hash-only.

Every whole scenario,38 obligations,91 groups,36 lessons and nested/discovered leaves
remain open. CountKnown=false stays the exact pre-browsed Right-separated context;
EC045 intermediate and arbitrary history interleavings remain unsupported. Two Bold
pairs is an initial qualification bound, not an original format limit. Historical DOS,
physical keyboard/printer delivery, graphics, locales and all wider M1 workflows stay
unqualified. M2/PDF is not started. Readiness bindings are for future normal acceptance;
this tool never writes acceptance-matrix.json, lifecycle or approval state.

`audit-custody` independently streams all7,364 approved raw artifacts (1,043,070,144 bytes) and their Git blobs. It runs no original helper, Go reader, product, compiler or VM. Every path/size/SHA remains bound to the pinned approved manifest.
