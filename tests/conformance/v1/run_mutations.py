#!/usr/bin/env python3
"""Run focused compiling mutants through the existing public CLI tests.

Only temporary script copies are changed; product sources/registries stay untouched.
These checks establish test sensitivity, never original-application compatibility.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / 'scripts/conformance/v1/conformance.py'
TEST = ROOT / 'tests/conformance/v1/test_cli.py'
MUTANTS = [
    ('trust-passed-boolean',
     "        require(matched, 'recomputed comparator failed (declared pass is insufficient)')",
     '        pass  # mutant: trust declared pass',
     'test_committed_positive_envelope_and_real_corruption_guards'),
    ('unbound-executable',
     "    require(digest(executable) == run['executable_sha256'], 'executable hash does not match immutable build bytes')",
     '    pass  # mutant: accept an unrelated declared executable digest',
     'test_committed_positive_envelope_and_real_corruption_guards'),
    ('coerce-pinned-types',
     "        require(encoded(value[key]) == encoded(baseline[key]), f'{key}: immutable typed coverage/source/open-parent contract mismatch')",
     "        require(value[key] == baseline[key], f'{key}: immutable typed coverage/source/open-parent contract mismatch')",
     'test_exact_immutable_json_types'),
    ('drop-immutable-coverage',
     "        require(encoded(value[key]) == encoded(baseline[key]), f'{key}: immutable typed coverage/source/open-parent contract mismatch')",
     '        pass  # mutant: permit silently dropped inherited coverage',
     'test_missing_duplicate_and_old_primary_cases'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Explicit new replay directory; default is a fresh temporary directory')
    args = parser.parse_args()
    out = args.output or Path(tempfile.mkdtemp(prefix='wordling-wp30-mutation-replay-'))
    source, tests = CLI.read_text(), TEST.read_text()
    sealed = hashlib.sha256(CLI.read_bytes()).hexdigest()
    records = []
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        raise SystemExit('refusing to overwrite prior mutation evidence; choose a fresh --output directory')
    with tempfile.TemporaryDirectory(prefix='wordling-wp30-mutations-') as tmp:
        tmp = Path(tmp)
        for name, before, after, case in MUTANTS:
            if source.count(before) != 1:
                raise SystemExit('mutation seam no longer unique: ' + name)
            mutant = tmp / 'scripts/conformance/v1' / (name + '.py')
            mutant.parent.mkdir(parents=True, exist_ok=True)
            mutated = source.replace(before, after)
            compile(mutated, str(mutant), 'exec')
            mutant.write_text(mutated)
            test_file = tmp / ('test_' + name + '.py')
            copied = tests.replace('ROOT = Path(__file__).resolve().parents[3]', 'ROOT = Path(' + repr(str(ROOT)) + ')')
            copied = copied.replace("CLI = ROOT / 'scripts/conformance/v1/conformance.py'", 'CLI = Path(' + repr(str(mutant)) + ')')
            test_file.write_text(copied)
            baseline = subprocess.run([sys.executable, str(mutant), '--root', str(ROOT), 'check'],
                                      text=True, capture_output=True, timeout=60)
            if baseline.returncode != 0:
                raise SystemExit('mutant baseline invalid: ' + baseline.stdout + baseline.stderr)
            result = subprocess.run([sys.executable, str(test_file), 'ConformanceCLI.' + case],
                                    text=True, capture_output=True, timeout=60)
            output = result.stdout + result.stderr
            # A syntax/import/setup crash is not a killed behavioral mutant.
            killed = result.returncode != 0 and 'AssertionError' in output and 'FAILED (failures=1)' in output
            (out / (name + '.txt')).write_text(output)
            records.append({'name': name, 'test': case, 'compiles': True,
                            'exit_code': result.returncode, 'killed_by_assertion': killed,
                            'mutant_sha256': hashlib.sha256(mutant.read_bytes()).hexdigest()})
    if hashlib.sha256(CLI.read_bytes()).hexdigest() != sealed:
        raise SystemExit('source mutated unexpectedly')
    (out / 'mutation-results.json').write_text(json.dumps({'source_sha256': sealed,
                                                        'mutants': records}, indent=2) + '\n')
    print(json.dumps({'mutants': records, 'original_source_unchanged': True, 'output': str(out)}, sort_keys=True))
    return 0 if all(x['killed_by_assertion'] for x in records) else 1


if __name__ == '__main__':
    sys.exit(main())
