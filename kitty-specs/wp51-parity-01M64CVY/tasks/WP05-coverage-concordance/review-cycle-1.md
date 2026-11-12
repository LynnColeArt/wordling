---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-10-30T08:16:52Z'
reviewer_agent: codex
wp_id: WP05
---

# WP05 review — changes requested

Reviewed owned artifact at `0a77f4efec4cd61e4b309b07f30c1f789871fc5f` independently as reviewer-renata with review action governance. No contract/registry/source remediation made by this reviewer. The canonical CLI review_result event owns the verdict.

## Finding R1 — incorrect canonical case links in priority-gap table (P2)

`contracts/coverage-concordance.md:552–558` uses canonical IDs that belong to different feature groups and behaviors than the stated existing leads:

| Row | Recorded case | Actual canonical behavior/group | Correction boundary |
| --- | --- | --- | --- |
| Edit-screen options, WP51-005/077 | CMD51-007/144 | 007 switches independent documents/WP51-006; 144 rewrites display/WP51-018 | Use the actual WP51-005/077 leads (CMD51-154/188), or explicitly identify a genuinely justified cross-group contextual relationship. Neither is a dedicated proof of the uncovered branch. |
| Mouse setup/type, WP51-004 | CMD51-143 | Draw a double line/WP51-017 | The current mouse group links CMD51-153. Mark it as a related pointer-action lead, with setup/type still requiring new scenarios; do not label the line-drawing case a mouse lead. |
| Overstrike, WP51-030 | CMD51-089/090 | 089 cancels summary changes/WP51-090; only 090 is the stated attribute-group lead | Remove/correct 089, retain only qualified attribute leads or explicitly say no exact Overstrike case exists. |
| Screen, WP51-005 | CMD51-007 | Switch independent documents/WP51-006 | Use the correct qualified display lead (CMD51-154) or explain an actual cross-group relationship. |
| Diagnostics/PIF, WP51-082/078/080/081 | CMD51-189/195/196 | 195 traverses prefix packets/FMT51-002; 196 parses nested function text/FMT51-003 | Replace those unrelated parser IDs with appropriate qualified group leads (193/189/191/192 where relevant), or state no dedicated scenario exists. Do not invent coverage of diagnostics/PIF. |

The disclaimer that candidates do not prove complete branches does not make unrelated IDs useful traceability. These are the priority gaps that F-REF/F-APP tell the planner to close first, so incorrect links can send the next package to the wrong contract and test.

The embedded audit checks canonical ID existence globally and validates candidates derived from machine-ledger row group unions. It does **not** validate these additional gap-table associations, despite the prose at lines560–562 saying it checks source association. Amend the owned artifact so those links/qualifications are correct and machine-checked: for example, include gap lead mappings in the embedded ledger and verify each listed case belongs to an explicitly declared source group (or a separately justified contextual group). Expand slash-abbreviated IDs deliberately, or use full IDs, rather than checking only the first `CMD51-` token.

Requested scope is the existing owned artifact only. Do not change canonical registries or evidence statuses to make the assertions pass. Rerun the complete audit and actual project gate, then resubmit review.

## Checks that passed and must be preserved

- Embedded audit validates 431 unique dispositions and pinned input hashes. Actual kind counts: 202 reference features, 21 front entries, 7 indexes, 21 appendices (20 REF51 + one workbook), 9 source-context entries, 36 lessons, 126 SDK sections, 9 menu roots. All 91 parent groups are linked. Canonical related observations retain 53 partial/183 not-run; no whole lesson is claimed executed.
- Independent PDF bbox extraction reproduced five actual REF contents counts 45/48/48/48/13, totaling 202. Numeric starts agree after visual resolution of five duplicate-OCR errors: 105/107 on PDF42 and 458/471/473 on PDF44. Those rendered originals confirm the contract's numbers.
- Checked WB contents PDF4–5 against the lesson starts, and visually checked feature-list PDF488 for the newly qualified lesson13/14 dependency leads. All 36 remain step-unmapped/not-run, not completed lessons.
- Read WBC51 PDF1–2 and DOC51 PDF12 directly: workbook-printer list-print restriction, PRINTER.TST introduction correction and old international-macro page415 context are documentary leads, not executed observations or automatic cross-edition equivalence.
- Applied the PDF skill read-only. Visually confirmed SDK PDF518 contains printed19/footer only; Japanese section starts on PDF519 with printed20. Its type58/59/60 and packet16 distinction is a documentary locale variant, not implemented U.S. reader support.
- Actual project gate passes inventory, scenarios, adapter tests and Go discovery. Build/test/vet are explicitly skipped because this primary planning checkout has no Go packages; another code lane is not represented by that result. JUnit: `/tmp/wordling-wp05-review-junit.xml`.
- Scope diff is one owned Markdown artifact. No raw manual/native evidence, canonical source, implementation, queue or baseline was edited by WP05.

## Reproducible checks

The artifact's embedded Python audit can be extracted and rerun without changes:

```sh
python3 - <<'PY'
from pathlib import Path
s = Path('kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md').read_text()
code = s.rsplit("python3 - <<'PY'\n", 1)[1].split('\nPY', 1)[0]
exec(compile(code, '<WP05 embedded audit>', 'exec'))
PY
python3 scripts/review_checks.py --junitxml=/tmp/wordling-wp05-review-junit.xml
```

Directly inspect disputed mappings from the hash-pinned current registry:

```sh
python3 - <<'PY'
from pathlib import Path
import json
cases = {r['id']: r for r in json.loads(Path('docs/research/command-scenarios.json').read_text())}
for n in (7, 89, 143, 144, 195, 196):
    c = cases[f'CMD51-{n:03}']
    print(c['id'], c['title'], c['feature_ids'])
PY
```

No production behavior is approved or rejected by this documentary review. WP05 remains an initial research package within complete M1; all unrepresented behavior and edition/resource limits remain visible.
