# Bounded FIELD1 / IFBLANK2 body evaluation

`Compile` accepts an authentic immutable native Primary Program and its expected
Source owner. It validates the entire primary, then captures a private plan for
one of two forms: printable literal + FIELD1 + terminal HR; or IFBLANK2,
nonempty true literal, ELSE, nonempty false literal, ENDIF, nonempty separator,
FIELD1. ASCII20..7E except tilde is permitted in literals. Both branches must
pass whole-primary validation. Numeric operands and their tildes never emit.
The IF/ELSE/ENDIF Match values are command indexes, checked independently of
token positions. Unsupported shapes, PAGE, nesting and extra controls refuse.

`Plan.Evaluate` takes authentic explicit Secondary DATA, its expected Source,
and a one-based record ordinal. FIELD1 emits only its actual Value.Bytes;
IFBLANK2 uses ExplicitlyEmpty. Missing field2 preserves
`*explicit.ExplicitFieldMissing` through the error chain, and is never treated
as empty. This missing-field refusal is Wordling's conservative policy, not a
claim about DOS behavior. Failed calls expose no valid or partial Plan/Result.
Zero handles refuse. Result bytes and nested provenance are defensive copies.
Captured handles support concurrent read-only use; concurrent mutation during
upstream capture remains outside the inherited trusted-caller contract.

Provenance retains actual Primary/Secondary owners, record ordinal, selected
output ranges, original literal/HR/field spans and field/decision accesses with
the enclosing record, EF/HR/EOR/tail/interstitial spans. Unselected branch spans
are validated by Compile but are not claimed as emitted output. Opaque D4/HP
metadata remains unresolved provenance, never inserted into body bytes.

Limits are positive Linux safeguards: PrimaryTokens<=4096, BodyBytes<=65536,
WorkUnits<=1048576. Compile precharges348160 work and48MiB before its ONE
native inspection; total requested/copy allowance64MiB. Evaluate checks
Content.Bounds before Value.Bytes and reserves output/trace/provenance before
allocation, with fixed4MiB/4098trace ceilings. See the retained bounds proof
and observed benchmarks in evidence/verification; requested/copy accounting is
not process RSS or a sandbox. Lower work budgets can refuse at Compile before
inspection; they do not permit deferred or unlimited work.

The real non-test consumer is `evidence/evaluate/main.go`:

```sh
go build -o /tmp/wordling-evaluate ./internal/merge/body/evidence/evaluate
/tmp/wordling-evaluate < request.json
```

A request has exactly `primary` and `secondary` byte payloads (ordinary Go JSON
base64 strings). No paths, instructions, expected output or budget overrides
are accepted. Duplicate/unknown/trailing input refuses. The raw read cap is
3MiB plus sentinel; each decoded source<=1MiB. Actual upstream Parse/View/Admit
and Compile/Evaluate run on these bytes. Diagnostics include computed base64
body bytes and authentic source bounds, with input SHA256s only as diagnostics.
The cumulative ledger reserves256MiB requested/copy bytes and64Mi work across
read, admission, compilation, each record, accessors and report. Record cap32,
total body256KiB, trace16384 and encoded stdout1MiB are additional ceilings;
not all simultaneous maxima fit the conservative reservation. Insufficient fit
refuses before the associated operation. No earlier successful rows are printed
if a later record fails. A short/failed stdout write reports failure and may
leave partial diagnostic bytes; there is no OS pipe rollback guarantee.

Both207/209 original run associations constrain the computed per-record bodies.
These are a decomposition of existing original result observations, not new DOS
runs or complete result equality: automatic original D4/HP copy boundaries are
retained separately and remain unresolved. June1992 manual evidence postdates
the selected March9,1992 executable. Actual208/216/217 PAGE primaries remain
syntactically admitted upstream and are refused by this narrow compiler.

This is an offline maintainer component. It provides no ordinary application
Merge command, native writer, pagination, layout, end-user UI, replacement
editable format or full merge/parity acceptance. Existing native and DATA
readers/qualifiers, modules, fixtures and application paths are unchanged.
