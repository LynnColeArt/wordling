# Iteration control and page settings across nested primaries — 2026-10-29

Historical eight-recipe pass. Later [value/secondary probes](values-secondary-probes.md)
cover several branches listed as unverified below.

These are bounded probes of the fingerprinted WP 5.1 03/09/92 executable, using
fresh copies of the offline FreeDOS/Standard Printer profile. Native macro and
merge fixtures are authored in the original application. Wordling is not tested.

## Recipes

| Case | Fixture and checked result |
| --- | --- |
| CMD51-218 | FOR EACH iterates 15, 10, 15, 5. `15/10/15/5/DONE` preserves order and the repeated value. |
| CMD51-219 | FOR 1..3 executes NEXT when N=2. `1X3XDONE` proves that the remaining body of iteration 2 is skipped. |
| CMD51-220 | FOR 1..5 executes BREAK inside IF N=3 before emitting N. `12DONE` proves exit from the loop, rather than merely from IF. |
| CMD51-221 | Outer FOR I=1..2 contains inner FOR J=1..3; BREAK at J=2. `11R21RDONE` proves that only the inner loop exits and both outer iterations reach their R marker. |
| CMD51-222 | An outer FOR resets J=0, then an inner WHILE J<2 emits I/J pairs and increments J. `10/11/20/21/DONE` verifies reset, nesting, ordering and termination. |
| CMD51-223 | Parent starts PAGE OFF; nested child primary executes PAGE ON. On return, the child's ON setting governs the following parent separator: two pages, one native hard-page code. |
| CMD51-224 | Parent starts PAGE ON; child executes PAGE OFF. Its OFF setting remains active on return: one page, no separating hard-page code. |
| CMD51-225 | Parent explicitly executes PAGE ON after the child turns pages OFF. Two pages and one separator demonstrate explicit restoration. |

## Manual traceability

REF51 p. 822 (PDF 839) defines FOR EACH as a list of values terminated by an
additional tilde and closed by END FOR. Its list is not a range or a set: the
fixture deliberately uses nonsequential and repeated numeric values.

REF51 pp. 839–840 (PDF 856–857) defines NEXT as advancing to the next iteration
without omitting the required END FOR/END WHILE. BREAK precedence and nested
loop levels are described on pp. 800–801 (PDF 817–818). The IF-in-FOR and
inner-FOR fixtures distinguish loop-level control from an IF-only exit or an
exit from both loops. FOR on pp. 820–821 and WHILE on p. 876 supply the mixed-loop
fixture's initialization and termination rules.

REF51 pp. 838–839 (PDF 855–856) defines NEST PRIMARY as a transfer to the named
file followed by return to the parent. The child uses the current secondary
record. Page controls on pp. 847–848 (PDF 864–865) are global to the merge until
the opposite command executes; they are not automatically restored with the
parent primary. All locators refer to the checksum-pinned source register.

## Cross-file pagination fixture

The same secondary supplies Alice and Bob. The parent emits `P` plus field 1,
a hard return, NEST PRIMARY CHILD, then `R` and a hard return. The child emits
`C` plus the same field and a hard return. Both files have an explicit PAGE
setting, but neither contains an explicit hard-page character.

The decoded result for ON after nesting is:

```text
PAlice
CAlice
R
<form feed>
PBob
CBob
R
```

For the child-OFF/no-restoration case the form feed is absent. Parent R markers
prove return after each child call; exact decoded text also checks that record
selection and continuation are correct. Runtime assertions combine page status,
formatter-aware native hard-page counts and ordered record/return markers.

This differs from the earlier [nested macro error-handler observations](history-loops-probes.md):
macro handler state resumes on return, whereas these merge page settings retain
the child's change until explicitly overridden. This is evidence for the future
execution design, not a complete language-runtime specification.

## Repetition and native evidence

Both repetitions passed all eight recipes: **16 executions and 112 runtime checks**.
All 22 native output pairs are byte-identical, and the independent audit passes
all 16 exact body/text assertions. The catalogue now contains 225 scenarios,
42 partially observed and 183 not run; no Wordling implementation is exercised.

Runs: [iteration-01](../reference-runs/2026-10-29-iteration-01/run.json) and
[iteration-02](../reference-runs/2026-10-29-iteration-02/run.json).
[Output comparison](iteration-output-comparison.json) compares every native WPM
and document across repetitions. The [independent body/text audit](iteration-native-validation.json)
checks exact macro output and merge text, including the separator position.

Each run retains exact runner sources, environment and scenario snapshots,
keystroke traces, lossless screen/VRAM evidence and native-file hashes. WP exits
normally before QEMU stops and offline extraction begins. No source or output is
normalized. Proprietary application and resource files remain in the private
ignored cache; published native fixtures contain our authored scratch content.

```sh
python3 scripts/reference/smoke.py your-unique-run \
  CMD51-218 CMD51-219 CMD51-220 CMD51-221 \
  CMD51-222 CMD51-223 CMD51-224 CMD51-225

python3 scripts/reference/verify_advanced_bodies.py \
  2026-10-29-iteration-01 2026-10-29-iteration-02 --suite iteration \
  --output /tmp/wordling-iteration-native-check-your-unique-id.json
```

The audit's existing advanced and history suites were rechecked after adding
this suite. Remaining obligations include string/expression FOR EACH values,
NEXT at deeper loop levels, BREAK's IF-only and file-level rules, nesting limits,
loop errors, and page controls across nested secondary files or deeper primary
chains. Historical MS-DOS and graphics/font-sensitive pagination also remain
separate reference-profile obligations. No Wordling compatibility is claimed.
