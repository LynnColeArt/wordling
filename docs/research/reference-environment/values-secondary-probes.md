# FOR EACH values, nested NEXT, file BREAK and secondary pages — 2026-10-30

These bounded probes run the fingerprinted original WP 5.1 03/09/92 executable
under the same offline FreeDOS/Standard Printer profile. Every recipe starts
from a fresh image copy. The original app authors all WPM and document fixtures;
Wordling is not exercised. Calibration hypotheses and observed behavior are
kept distinct, particularly for quoted strings and file-level BREAK.

## Values and nested iteration

| Case | Original-app result |
| --- | --- |
| CMD51-226 | Quoted then unquoted FOR EACH string lists produce `"red"/"blue sky"/"red"/RAW:red/blue sky/red/DONE`. Quotes remain in the quoted section; spaces and duplicates survive both forms. |
| CMD51-227 | With B=4, FOR EACH values `1+2`, VARIABLE B + 4, and VARIABLE B + 1 produce `3/8/5/DONE`. Arithmetic and variable-containing expressions are evaluated. |
| CMD51-228 | NEXT at J=2 in an inner FOR yields `11/13/R21/23/RDONE`; J=3 and both outer iterations survive. |

REF51 p. 822 (PDF 839) describes FOR EACH value/expression lists, including
variables and commands. NEXT at pp. 839–840 (PDF 856–857) advances the current
loop while retaining its required end marker. The quoted-value case is an
explicit oracle investigation: ordinary quote-removal assumptions did not match
this executable. These examples do not establish general string escaping,
empty-value rules or expression-evaluation timing for every command.

## File-level BREAK is context-dependent

These cases contain no enclosing IF or loop at the BREAK point:

| Case/context | Result |
| --- | --- |
| CMD51-229, top-level macro | BREAK is ignored: `ABDONE`. |
| CMD51-230, nested macro | BREAK is also ignored in this fixture: `PCCHILDBADRDONE`. The child remainder executes before normal return. |
| CMD51-231, root primary merge | BREAK skips BAD and ends the current copy; Alice and Bob both produce output, separated by one hard page. |
| CMD51-232, secondary merge | Bob is absent, but an already-started partial second copy remains: `Hello Alice`, hard return, hard page, `Hello ` (with space), hard return. |
| CMD51-236, nested primary merge | BREAK returns to the parent and skips CHILDBAD. Both parent R continuation markers appear. |

REF51 pp. 800–801 (PDF 817–818) gives loop/IF/file precedence and describes
file-level behavior. Its general nested-file wording must not be applied blindly
to the nested-macro fixture: the original editor's captured source contains the
BREAK token, yet that child continues. The nested-primary fixture separately
confirms early return. This pass records the distinction without asserting a
cause or behavior for other releases.

The secondary termination case is likewise an explicit investigation. A
persistent partial copy is part of the observed output, including its trailing
space and hard return. The evidence does not assume transactional rollback or
infer exactly which internal stage inserts that final return.

## Page controls across nested secondary files

The root data file contains Alice, a record with NEST SECONDARY CHILD followed
by IGNORED, then Bob and Eve. CHILD contains Carol and Dave. The primary is
`Hello {FIELD}1` plus a hard return. No explicit hard-page character appears in
the primary. All three cases produce Alice, Carol, Dave, Bob, Eve; the nesting
record is replaced and its suffix ignored.

| Case | Settings | Exact separators and final page |
| --- | --- | --- |
| CMD51-233 | Root OFF, child ON | Separators before Dave, Bob and Eve: three controls, page 4. Child ON remains active after return. |
| CMD51-234 | Root ON, child OFF | Only the separator before Carol remains: one control, page 2. Child OFF remains active after return. |
| CMD51-235 | Root ON, child OFF, Bob explicitly restores ON | Separators before Carol and Eve: two controls, page 3. Restoration in Bob affects the following boundary. |

REF51 p. 839 (PDF 856) describes NEST SECONDARY, replacement of the nesting
record, ignored following field text and resumption at the next parent record.
PAGE OFF/PAGE ON at pp. 847–848 (PDF 864–865) applies globally until the opposite
command executes. These cases pin exact boundary positions rather than guessing
that a setting is restored with the parent data-file context. They complement
the earlier [nested-primary page tests](iteration-nesting-probes.md).

## Repetition, provenance and native assertions

Both repetitions passed all eleven recipes: **22 executions and 126 runtime
checks**. All 33 native output pairs are byte-identical; all 22 independent
body/text assertions pass. The catalogue contains 236 scenarios, 53 partially
observed and 183 not run. No Wordling implementation is exercised.

Runs: [values-01](../reference-runs/2026-10-30-values-01/run.json) and
[values-02](../reference-runs/2026-10-30-values-02/run.json).
[Repeated native output comparison](values-output-comparison.json) includes every
native macro, primary, secondary, nested child and merged result.
[Independent body/text assertions](values-native-validation.json) validate exact
quotes, spaces, continuation markers and formatter-aware hard-page positions.

Each run retains its exact scripts, scenario/environment snapshots, keystroke
trace, stable screen and raw VGA captures, and checksummed native artifacts. WP
exits normally before QEMU stops and offline extraction begins. No native file
is normalized or rewritten. Proprietary programs/resources and diagnostic
calibration attempts remain in the private ignored cache.

The first calibration expected quote removal and early return from a nested
macro BREAK; both expectations were rejected by the executable. The revised
fixtures retain those observed differences. A separate nested-primary test
prevents a macro observation from being generalized to all nested files. The
three earlier native-audit suites were rechecked after adding this suite: all
60 assertions still passed.

```sh
python3 scripts/reference/smoke.py your-unique-run \
  CMD51-226 CMD51-227 CMD51-228 CMD51-229 CMD51-230 CMD51-231 \
  CMD51-232 CMD51-233 CMD51-234 CMD51-235 CMD51-236

python3 scripts/reference/verify_advanced_bodies.py \
  2026-10-30-values-01 2026-10-30-values-02 --suite values \
  --output /tmp/wordling-values-native-check-your-unique-id.json
```

Remaining branches include empty/escaped string values, evaluation timing and
errors, NEXT in other nested loop types, IF-only BREAK, termination with other
partial-copy templates, deeper/cyclic data nesting and error paths, and page
controls combined with nested primaries and printer-sensitive layout. Historical
MS-DOS and graphics/font profiles remain separate obligations. All Wordling
implementation and differential conformance remain untested.
