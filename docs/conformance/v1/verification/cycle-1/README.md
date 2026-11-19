# WP30 cycle-1 focused integrity corrections — independent rereview pending

Only I1 executable identity and I2 immutable type fidelity are changed. Historical
source catalogue/registry/index bytes, product code, native formats, parent openness,
resource qualification limits and zero current product passes remain unchanged.
No VM or original application was run. No other WP or mission acceptance is changed.

## I1: actual executable bytes and separate build/run provenance

A positive run now references a separately hashed immutable build JSON record.
The build witness binds exact implementation, case/revision, scope, invocation,
independent review, source entrypoint, captured build argv/environment/log and integer
zero build exit code. It references actual executable Git blob bytes; validation
recomputes those bytes' digest and joins it to the run's executable_sha256. A second
free asserted digest in the same run envelope is insufficient. Product source
entrypoint must be cmd/wordling at the implementation commit. No supplied code,
compiler, binary, comparator or shell is executed by validation.

Public tests retain a valid upgraded build-bound synthetic protocol control, reject
an executable hash change while its build witness/raw inputs/review stay fixed, and
exercise missing build, wrong witness hash/binary/source/case/scope/entrypoint/argv/
review/build exit status. They also accept a different executable from a distinct
consistent build context. No identical-binary-across-build-context assumption is
introduced. Fixture binaries and logs are synthetic **tooling integrity controls**,
never product execution or current conformance evidence. As before, integrity cannot
prove the honesty of a repository's authors; independent semantic review remains.

## I2: immutable typed JSON identity

All three mission defaults must be specifically boolean false. Immutable trees are
compared using typed canonical JSON rather than Python deep equality. The exact
pinned page integer cannot become a float; true documentary flags cannot become
numeric1. This is this v1 source/schema contract, not a general JSON Schema rule
about mathematically integral numeric notation. Proposals are rejected without
rewriting or normalizing them; valid import/check/regeneration remains idempotent.

## Independent exact red/green retention

Inputs are copied byte-for-byte from review commit
`95b3d88af6d13e40c59947f67015f6a8fc82c244`: the isolated Git bundle, original
baseline/negative run records and two coercion proposals. Original review files and
prior implementation logs remain untouched. `replay_cycle1.py` runs only the public
CLI; temporary fixture commits use fixed fixture metadata so complete proposed
registry bytes/hash are identical between old/fixed replay. Raw run bytes are never
normalized. See `external-exact-red-before.json` and `external-exact-green-after.json`:
all4 input SHA256 values match, old afe4280 CLI returns0 and corrected CLI returns1.

The old unbound *control* is intentionally rejected too: no missing build provenance
is grandfathered. This is separate from the upgraded valid bound control and the
same-build/wrong-digest negative in the passing public suite. Earlier nondeterministic
replay records are retained as supplementary attempts, not substituted for the
matching-input-hash exact replay pair. This distinction avoids claiming a legitimate
new positive protocol was rejected or that all positives simply fail.

## Actual validation

- Public CLI suite: **15 tests passed**, all initial14 plus exact immutable type checks
  and expanded positive-envelope negatives/alternate-build control.
- Declared project bridge: **7/7 passed**, zero failures/errors/skips.
- Four compiling behavioral mutants killed: trust-passed-boolean, unbound-executable,
  coerce-pinned-types and drop-immutable-coverage. Each passes valid baseline check
  before its targeted behavioral test fails. Current final logs are in mutation-final/;
  earlier replay and development attempts remain separate.
- Read-only Git-call/working-byte checks, source Git seals, Python compile and diff
  scope/whitespace checks pass. No input/source checkout or check-mode write occurs.

Mutation reruns now default to a fresh temporary output directory. Explicit --output
must be empty/new; accidental reruns cannot overwrite sealed logs. Root's two exact
restored initial logs still equal their afe4280 Git blobs.

The cycle-1 verification manifest binds current executing source/test/schema/docs
and replay runner hashes to this correction, while preserving original initial
verification.json as historical evidence for afe4280. Current registry remains
244 original scenarios /91 open groups /38 open obligations, with0 positive rows;
full SC-001–005 and all remaining breadth/resource/physical obligations remain open.
