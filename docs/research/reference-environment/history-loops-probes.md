# Three-level history, nested macros, loops and PAGE ON — 2026-10-29

Historical eight-recipe pass. Later [iteration/nested-primary probes](iteration-nesting-probes.md)
cover several branches listed as unverified below.

These probes run the fingerprinted original WP 5.1 03/09/92 executable. Each
recipe starts from a fresh copy of the same offline DOS profile. All WPM and
merge fixtures are authored through the original application; Wordling remains
unimplemented. The FreeDOS and text-only printer limitations still apply.

## Recipes and manual basis

| Case | Bounded behavior exercised |
| --- | --- |
| CMD51-043 | Delete ONE, TWO and THREE in separate operations, browse THREE/TWO/ONE, cancel, and verify the native body is unchanged. Reopen history and restore ONE at the current cursor. |
| CMD51-211 | Delete a fourth word. Only FOUR/THREE/TWO remain; another Previous Deletion cycles to FOUR. ONE cannot be recovered. Cancelled browsing preserves the body; restore TWO. |
| CMD51-212 | A child catches a missing nested-file error with its own ON ERROR handler and RETURNs. The parent resumes, then its original handler catches a second missing-file error. Exact output: `PCHILDRPARENT`. |
| CMD51-213 | A child without a handler types C and encounters a missing nested-file error. Its default RETURN ERROR reaches the parent's handler. Exact output: `PCPARENT`; neither continuation sentinel runs. |
| CMD51-214 | FOR from 1 through 3 with step 1, then from 3 through 1 with step -1. Exact output `123/321DONE` checks both directions, inclusive endpoints and termination. |
| CMD51-215 | WHILE 0 skips BAD. A second WHILE emits N and increments it from 0 until N reaches 3. Exact output `012DONE` checks zero-entry and terminating variable-dependent loops. |
| CMD51-216 | A two-record primary starts PAGE OFF, emits its line, then executes PAGE ON. This restores the automatic separating hard page without an explicit hard-page character in the primary. |
| CMD51-217 | Alice/Bob select PAGE OFF; Carol/Dave select PAGE ON through IF BLANK/ELSE. Carol remains on the first page; the restored automatic separator appears before Dave. |

REF51 pp. 697–698 (PDF 714–715) defines three remembered deletions, cursor-based
restoration and oldest-entry eviction. The word fixtures deliberately retain
spaces and move the cursor between deletions. Native BASE/BROWSED files prove
that preview and cancellation do not change the document area.

REF51 pp. 836–837 and 843–845 (PDF 853–854 and 860–862) describes nesting,
RETURN ERROR and handler scope. A nested macro starts with default handling;
parent handlers are not installed inside it. On return, the parent's handler
resumes. The two cases distinguish a locally handled error from an unhandled
child error returned to the parent. Both macros are retained in their original
WPM format, with original-editor source views.

REF51 pp. 820–821 (PDF 837–838) defines FOR's inclusive endpoints and step.
WHILE on p. 876 (PDF 893) requires a pre-existing variable and an update that
makes the condition false. Loop completion markers and exact native output
prevent a partial iteration or aborted macro from counting as success. Host
waits are bounded; a stalled or erroneous run fails and is retained separately.

REF51 pp. 847–848 (PDF 864–865) states that PAGE OFF/PAGE ON apply globally to the
merge until the opposite command executes. IF BLANK is described on p. 825
(PDF 842). The four-record boundary case is an explicit oracle investigation;
it does not guess a new pagination rule from prose alone.

The four-record result is `Hello Alice`, `Hello Bob`, and `Hello Carol` on page 1,
then `Hello Dave` on page 2. Its native body has exactly one hard-page control,
after Carol's hard return. PAGE ON affects the following automatic boundary;
it does not retroactively add a break before the current record. The simpler
PAGE OFF/ON primary also produces one separator and two pages. Neither primary
contains an explicit hard-page character.

## Native evidence and repetition

Both repetitions passed all eight recipes: **16 executions and 124 runtime checks**.
All 22 native output pairs are byte-identical; the independent body/text audit
passes all 24 assertions. The catalogue now has 217 scenarios, 34 partially
observed and 183 not run. No Wordling implementation is tested.

The two complete runs are [history-01](../reference-runs/2026-10-29-history-01/run.json)
and [history-02](../reference-runs/2026-10-29-history-02/run.json).
[Repeated-output comparison](history-output-comparison.json) covers all authored
native files, including child and parent macros, unchanged history bodies,
restored text, primary/secondary files and merge results.

An independent [native-body audit](history-native-validation.json) checks exact
spaces, restored words, macro output and decoded merge text. The formatter-aware
inspector counts hard-page controls outside D4/00 functions and retains formatter
page numbers. No file is normalized or rewritten for comparison. Raw native
bytes, screen/VRAM captures, exact runner sources, scenario snapshots and input
traces remain linked by hashes. Every recipe exits WP before offline extraction.

```sh
python3 scripts/reference/smoke.py your-unique-run \
  CMD51-043 CMD51-211 CMD51-212 CMD51-213 \
  CMD51-214 CMD51-215 CMD51-216 CMD51-217

python3 scripts/reference/verify_advanced_bodies.py \
  2026-10-29-history-01 2026-10-29-history-02 --suite history \
  --output /tmp/wordling-history-native-check-your-unique-id.json
```

The extended audit utility preserves its previous default suite; the earlier
advanced fixtures were rechecked after adding the history suite. These checks
are original-app observations, not Wordling compatibility results.

Remaining branches include history arrow-key selection and grouping edge cases,
low-memory history spill, deeper handler chains and ON NOT FOUND scope, FOR EACH,
BREAK/NEXT, nested loops and loop errors, and page-control effects across nested
primary/secondary files. Historical MS-DOS and printer-dependent layout profiles
remain separate research obligations.
