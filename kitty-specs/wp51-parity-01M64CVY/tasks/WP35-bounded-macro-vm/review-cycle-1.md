---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-10-31T04:38:35Z'
reviewer_agent: codex
wp_id: WP35
---

# WP35 cycle1 — changes requested

## P2: eager FOR EACH expansion bypasses run and slice work budgets

**File:** internal/macro/runtime/loops.go:35–45 (`startEach`), with
machine.go's single charged `execute` step and expression.go's copied value views.

The public native compiler accepts a nested FOR EACH where the outer variable has
4096 literal words and the inner list repeats VARIABLE I1024 times. `startEach`
evaluates and copies all inner values synchronously without charging any of those
1024 evaluations/4,194,304 expanded words to the run or slice. The per-item
VariableWords check limits each value but does not bound aggregate work/allocation.

Exact unchanged-source public-API overlay reproduction:

```
go test -count=1 -v   -overlay=/tmp/wordling-wp35-review/resource-overlay.json   -run '^TestReviewerForEachExpansionRespectsWordWorkBudget$' ./internal/macro/runtime
```

It fails actual assertions, not setup/compilation. The original image is8204 words;
limits are Steps8206, SliceSteps1 and OutputWords1 (other limits default). After
compilation debt and outer setup, the machine is running at8205 charged steps with
ONE remaining run/slice unit. The next Step returns running at8206, but eagerly
materializes4,194,304 value words and allocates16,845,504 bytes in that call. Source
and limits remain unchanged. The1024x4096 probe is deliberately modest; expansion
multiplies list length by value length under the accepted input/value maxima.

This violates approved WP32's requirement that Step charge actual statement/word
work and honor bounded slices/run limits. It also defeats the small run/output
budget before the later UI consumer can regain control. Passing numeric counter
assertions do not establish that actual evaluation work was charged.

**Required repair:** enforce bounded aggregate list evaluation/copy work before
unbounded allocation and respect the remaining run/slice budget. Use bounded
continuation/private evaluation state or another genuinely bounded strategy that
preserves the admitted original semantics and immutable values. Apply the same
reasoning to repeated value expansion/control evaluation, not only this one test.
Refuse with a typed implementation-limit outcome when necessary before the excess
work/effects. Do not raise limits, relabel actual copies as free, weaken assertions
or delete the supported feature to evade the work contract. No native/API widening
or new original semantics are requested.

**Acceptance:** retained public-API regression must distinguish the old defect from
the fixed bounded behavior; include long-value/many-item and repeated/non-emitting
forms near declared budgets. Verify counters, terminal/waiting/source invariants,
slice responsiveness, bounded allocations and no extra sink effects. Preserve all
20 historical component traces,4 approved39 replays, copy/handler/resume/condition
safety and pure dependency boundary. Re-run meaningful real checks/race and a
measured focused fuzz budget after the code changes. Existing660s fuzz was passing
for the reviewed old source; it does not prove this newly exposed path safe.

Evidence/raw command/reproducer/source seals are in independent-cycle-1. Reviewer
performed no product/source fix. Full38 obligations/91 groups remain open; this
feedback does not accept/merge, change native formats or start M2.
