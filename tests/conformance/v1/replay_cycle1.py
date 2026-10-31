#!/usr/bin/env python3
"""Replay exact independent I1/I2 proposals through a chosen public CLI.

Only isolated temporary Git refs are written. Original 95b3d88 inputs are retained;
old positive controls lacking build provenance are intentionally not grandfathered.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT/'docs/conformance/v1/verification/cycle-1/external'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cli', type=Path, default=ROOT/'scripts/conformance/v1/conformance.py')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    rows = []
    def run(root, proposal, label):
        before = proposal.read_bytes()
        result = subprocess.run([sys.executable, str(args.cli), '--root', str(root),
                                 'validate', '--registry', str(proposal)],
                                capture_output=True, text=True, timeout=60)
        assert before == proposal.read_bytes()
        rows.append({'label': label, 'input_sha256': hashlib.sha256(before).hexdigest(),
                     'exit_code': result.returncode, 'stdout': result.stdout,
                     'stderr': result.stderr, 'input_unchanged': True})
    with tempfile.TemporaryDirectory(prefix='wp30-cycle1-external-') as temp:
        repo = Path(temp)
        subprocess.run(['git', 'init', '-q', str(repo)], check=True)
        common = subprocess.check_output(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, text=True).strip()
        (repo/'.git/objects/info/alternates').write_text(str((ROOT/common/'objects').resolve())+'\n')
        subprocess.run(['git', 'fetch', '-q', str(INPUT/'independent-positive-fixture.bundle'),
                        'refs/heads/main:refs/heads/independent-fixture'], cwd=repo, check=True)
        base = json.loads((ROOT/'docs/conformance/v1/registry.json').read_text())
        for label, name in [('old-unbound-control', 'baseline-run.json'),
                            ('I1-declared-executable-only-changed', 'negative-run.json')]:
            raw = (INPUT/'independent-positive-fixture'/name).read_bytes()
            record = json.loads(raw)
            # Commit the exact retained run bytes, not a normalized substitute.
            (repo/'retained-run.json').write_bytes(raw)
            subprocess.run(['git', 'add', '--', 'retained-run.json'], cwd=repo, check=True)
            subprocess.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                            '-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-qm', label],
                           cwd=repo, check=True, env=dict(os.environ, GIT_AUTHOR_DATE='2000-01-01T00:00:00+00:00',
                                                         GIT_COMMITTER_DATE='2000-01-01T00:00:00+00:00'))
            commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
            evidence_commit = record['inputs'][0]['commit']
            review = subprocess.check_output(['git', 'cat-file', 'blob', evidence_commit+':review.md'], cwd=repo)
            value = dict(base, evidence=[{'id': 'E-FIXTURE', 'level': 'differential', 'state': 'pass',
                         'case_id': record['case_id'], 'case_revision': record['case_revision'],
                         'scope': record['scope'],
                         'run': {'commit': commit, 'path': 'retained-run.json',
                                 'sha256': hashlib.sha256(raw).hexdigest()},
                         'review': {'artifact': {'commit': evidence_commit, 'path': 'review.md',
                                     'sha256': hashlib.sha256(review).hexdigest()},
                                    'reviewer': 'fixture-reviewer'}}])
            proposal = repo/'proposal.json'
            proposal.write_text(json.dumps(value))
            run(repo, proposal, label)
    for name, label in [('independent-coerced-boolean-registry.json', 'I2-false-to-zero'),
                         ('independent-coerced-source-registry.json', 'I2-integer-page-to-float')]:
        run(ROOT, INPUT/name, label)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({'review_source_commit': '95b3d88af6d13e40c59947f67015f6a8fc82c244',
                                     'cli_sha256': hashlib.sha256(args.cli.read_bytes()).hexdigest(),
                                     'rows': rows}, indent=2)+'\n')
    print(json.dumps({'results': [(x['label'], x['exit_code']) for x in rows]}))


if __name__ == '__main__':
    main()
