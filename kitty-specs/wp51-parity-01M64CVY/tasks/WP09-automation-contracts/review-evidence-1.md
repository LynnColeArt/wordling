# WP09 independent review evidence

Reviewer: reviewer-renata, independent Codex review agent; 2026-10-30.
Reviewed commit: fc328857796ea691906b674df26d92d41f9a274b.
Recommendation: approve bounded contract research. No blocking findings.

## Scope and criteria

Read the full runtime prompt e7b24b29bbcb44a5ab99433e3957b004 and T025–T027 criteria; refreshed resolver-backed reviewer-renata, software-dev review governance and code-review-checklist selector (no authored section exists). Review/verdict skills, repository AGENTS.md, mission spec/plan/research/domain model and compatibility/roadmap apply. This review reuses the established native/layout boundaries rather than changing them.

T025 passes: 35 exact canonical cases distinguish macro record, values, loop, file and nested contexts from primary, secondary and nested merge contexts. Context/feature/locator/status associations match canonical metadata. Results retain literal quoted strings, ordered duplicates, expressions, NEXT/BREAK loop levels, local/default child error handling and parent continuation. Mechanisms beyond observable behavior remain explicitly unproven.

T026 passes: 70 original-only result repetitions across 10 sealed manifests retain source/companion/results, captures, runner and archived environment identity. Formatter-aware page inspection preserves exact boundaries; root-primary BREAK continues records, nested-primary BREAK returns, root-secondary BREAK retains a partial second copy ending in space plus hard return. Nested secondary replaces its record and resumes with Bob/Eve; PAGE state survives calls and explicit restoration affects the following boundary. The early explicit-hard-page merge correctly retains blank pages/final page4. These are bounded merge separators, not general layout fidelity.

T027 passes: bounded WPM framing/read/no-edit, replay, macro control, merge evaluation, writer/editor/conversion and missing-probe slices retain FR-003/012 and original companion formats. Stop-running, round-trip, conversion and untested expression/error/control combinations remain unrun. Static/dynamic unsupported inputs, unknown bytes, unsafe writes, cycles and measured resource budgets receive explicit refusal/test work. No original observations, language-wide mechanism or Wordling parity is invented.

The implementation commit changes only owned contracts/automation.md; current bytes equal that commit. Shared planning lane coordination: root assigned independent WP09 review and owns sequencing/WP12; the contract is exclusively WP09-owned. This review authors only its evidence record. It changes no implementation, source registry, raw evidence, task queue or other WP status.

## Checks executed

1. Complete embedded PY_AUDIT: PASS, 43 pinned inputs, 35 semantic case/context associations, canonical/repeated source/capture/native metadata and 70 exact native result repetitions. Selected results reference 1840 distinct evidence paths and 190 native exports. All raw file/hash/repetition assertions pass, as do archived runner/environment checks and pending-case statuses.
2. Genuine configured gate `python3 scripts/review_checks.py --junitxml /tmp/wp09-independent-review.xml`: inventory, scenarios, review-adapter and Go package discovery PASS. Build/test/vet honestly SKIP for no Go packages in this planning checkout; these skips do not test approved separate code lanes. No bypass/force flags used.
3. Independent bounded native walker (below), importing no project document inspector: all70 expected results match; 36 D4/00 formatter envelopes validated and skipped by their lengths/trailers. Exact macro bodies and native document tuples validated. Actual secondary-break trailing space and final hard return match byte-for-byte, not normalized screen text.
4. Independently checked ABC WPM header tuple 1/1/1/1, four-entry index (FFFB,4,40,0), body offset70 and exact ten bytes 0cfc4100420043000000. Document tuple 1/10/0/1 stays separate; no claim this decodes every WPM token.
5. Read the corresponding archived-run recipe families and source/result captures, including value_secondary, history_loops, iteration_nesting, advanced and extended recipe behavior. Source-command insertion/argument traces agree with the matrix: quoted/unquoted lists, arithmetic VARIABLE expressions, inner NEXT/BREAK, local and unhandled child errors, root/child macro BREAK, root/child primary BREAK, root secondary partial result and PAGE timing. CMD51-178 explicitly includes manual READY after stopped search; the contract correctly distinguishes that from the pre-interactive BEFORE result.
6. Actual pinned manual extraction: REF PDF817–818 BREAK precedence;837–839 FOR/FOR EACH;842 IF BLANK;853–857 macro and merge nesting/NEXT;860–862 handler actions;864–865 global PAGE;893 WHILE. SDK PDF105–106 corroborates WPM prefix/index/two-byte units and terminal nulls. The nested macro BREAK discrepancy remains described as observation without invented cause. Source hashes match the registry and PDFs remain private/ignored.
7. Negative audit mutation reassigning valid merge case CMD51-134 to macro-loop fails semantic context-to-feature binding. Current artifact equals fc32885 and sole commit path is the owned contract.

Reproduce the contract's complete PY_AUDIT block, then the configured gate command above. Exact manual extraction uses `pdftotext -f START -l END -layout research/cache/FILENAME.pdf -`; URLs/hashes are in sources.json. Run the following independent result check from repository root:

```python
from pathlib import Path
import json
p = Path('kitty-specs/wp51-parity-01M64CVY/contracts/automation.md')
t = p.read_text()
a = json.loads(t.split('<!-- WP09_AUDIT_BEGIN -->')[1].split('```json\n')[1].split('\n```')[0])
count = envelopes = 0
for row in a['rows']:
    expected = row['expected']
    for run in (row['run'], row['repeat']):
        path = Path('docs/research/reference-runs') / run / row['case_id'] / expected['filename']
        b = path.read_bytes()
        start = int.from_bytes(b[4:8], 'little')
        assert b[:4] == bytes.fromhex('ff575043')
        assert b[8:12] == bytes([1, 10, 0, 1]) and 16 <= start <= len(b)
        if expected['kind'] == 'body':
            actual = b[start:]
        else:
            cursor = start
            actual = bytearray()
            pages = 0
            while cursor < len(b):
                if b[cursor] == 212:
                    assert b[cursor + 1] == 0
                    size = int.from_bytes(b[cursor + 2:cursor + 4], 'little')
                    end = cursor + size + 4
                    assert size >= 10 and end <= len(b)
                    assert b[end - 4:end] == size.to_bytes(2, 'little') + bytes([0, 212])
                    envelopes += 1
                    cursor = end
                else:
                    value = b[cursor]
                    assert value in (9, 10, 12, 13) or 32 <= value < 127
                    actual.append(value)
                    pages += value == 12
                    cursor += 1
            assert pages == expected['hard_pages']
        assert bytes(actual) == expected['expected_text'].encode('ascii'), (row['case_id'], run)
        count += 1
assert (count, envelopes) == (70, 36)
print('70 exact results; 36 formatter envelopes valid')
```

## Required anti-pattern checklist

1. Dead code: N/A; no production API created.
2. Synthetic-fixture test: PASS; audits read actual sealed original outputs and traces, not manufactured expected-shaped dicts.
3. Silent empty return: N/A; no production path changed.
4. FR coverage: PASS for research scope; FR-003 native companion/preservation boundaries and FR-012 context-specific execution contracts have concrete output/evidence assertions. No product implementation coverage is claimed.
5. Frozen surface: PASS; only exclusively owned new contract in implementation commit.
6. Locked decision: PASS; native formats, unknown-byte retention/refusal, full M1 and source/evidence boundaries retained.
7. Shared-file ownership: PASS; exclusive contract and root/shared-lane coordination recorded above.
8. Production fragility: N/A; no runtime raises or code changes.

Approval does not promote an original partial scenario, pending case, complete language, parser/writer or Wordling behavior to verified.
