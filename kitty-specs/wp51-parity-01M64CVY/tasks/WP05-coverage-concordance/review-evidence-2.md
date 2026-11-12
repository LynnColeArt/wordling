# WP05 independent review — cycle 2

Assessment: approve corrected contract commit `2aa20cf141e264abdca78ce512963fd7b95f1d61`. R1 from review-feedback-1.md is resolved. The authoritative verdict is the canonical review_result event. Reviewer-renata/action governance were resolved; reviewer remains independent from the author. No source, canonical registry or implementation edited by this reviewer.

## R1 closure and same-class checks

The nine G01–G09 priority-gap rows now use actual canonical leads with exact titles and explicit limits. Mouse selection does not imply setup/type coverage; bold does not imply Overstrike; display options do not imply every Screen branch; DOS/startup/shared-file context does not imply diagnostics/PIF. The same-class correction extends to seven V02–V08 version lead rows, removing unrelated macro/find/display IDs and qualifying the remaining leads. Unrepresented dedicated scenarios remain explicitly absent.

The audit now binds **16** prose lead sets to explicit feature IDs, canonical titles, inventory back-links and exact human table cells. Full IDs replace ambiguous slash abbreviations. A source hash or globally existing ID alone cannot satisfy these checks.

Executed results:

- Corrected complete embedded audit: `WP05 inputs, 431 dispositions, source locators and canonical links validated`.
- Independent wrong-feature negative: substituted valid CMD51-143 and its correct Draw-a-double-line title for CMD51-153 in both human cell and machine ledger, leaving the declared mouse feature unchanged. The audit rejects specifically at `('G04', 'CMD51-143', 'WP51-004')`; the check is semantic association, not merely ID existence/title equality or prose/ledger self-comparison.
- Independently checked every human Markdown table row before the machine ledger that has both feature and case IDs: **438 rows pass** case-feature intersection. This includes the repaired priority/version rows and the existing source concordance examples.
- Actual `python3 scripts/review_checks.py --junitxml=/tmp/wordling-wp05-review-cycle2.xml`: inventory, scenarios, adapter tests and Go discovery pass; build/test/vet explicitly skip because this primary planning checkout contains no Go packages. No result from another implementation lane is claimed.
- `git diff --check 0a77f4e..2aa20cf`: pass. The corrective commit changes only the owned coverage-concordance.md; additional lifecycle/review artifacts in the broader range are workflow records, not implementation scope.

Prior valid source review is retained without unnecessary duplicate PDF work. The hash-pinned 431 dispositions, 91 group links, actual five reference-contents counts, all36 step-unmapped/not-run lessons, 126 SDK keys, nine documentary discrepancy dispositions and visually verified Japanese TOC/body pagination distinction remain intact. No claim of complete manual study, executed workbook lessons, newly supported variant, application parity or clean incomparable baseline was introduced.

## Exact reproducible review commands

From `/home/lynn/projects/wordling`:

```sh
python3 - <<'PY'
from pathlib import Path
import json,re
path=Path('kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md')
s=path.read_text()
code=s.rsplit("python3 - <<'PY'\n",1)[1].split('\nPY',1)[0]
exec(compile(code,'<WP05 corrected audit>','exec'))
mutated=s.replace('CMD51-153 (Select and cancel text using the mouse)','CMD51-143 (Draw a double line)').replace('"case_id":"CMD51-153"','"case_id":"CMD51-143"').replace('"canonical_title":"Select and cancel text using the mouse"','"canonical_title":"Draw a double line"')
negative=code.replace('text = p.read_text()','text = candidate_text')
try:
    exec(compile(negative,'<WP05 wrong-feature negative>','exec'),{'candidate_text':mutated})
except AssertionError as e:
    assert e.args and e.args[0]==('G04','CMD51-143','WP51-004'),e.args
    print('PASS wrong-feature substitution rejected:',e.args[0])
else:
    raise AssertionError('wrong-feature substitution unexpectedly passed')
cases={x['id']:x for x in json.loads(Path('docs/research/command-scenarios.json').read_text())}
count=0
for num,line in enumerate(s.split('<!-- WP05_AUDIT_BEGIN -->')[0].splitlines(),1):
    if not line.startswith('| '):continue
    groups=set(re.findall(r'(?:WP51|FMT51)-\d{3}',line))
    ids=set(re.findall(r'CMD51-\d{3}',line))
    if not groups or not ids:continue
    count+=1
    for cid in ids:
        assert groups.intersection(cases[cid]['feature_ids']),(num,cid,groups,cases[cid]['feature_ids'])
print('PASS independent human-table feature membership:',count,'rows')
PY
python3 scripts/review_checks.py --junitxml=/tmp/wordling-wp05-review-cycle2.xml
git diff --check 0a77f4e..2aa20cf
```

No unresolved findings. WP05 acceptance covers a documentary concordance and actionable owned research proposals only; full M1 coverage and implementation acceptance remain pending.
