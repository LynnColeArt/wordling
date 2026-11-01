#!/usr/bin/env python3
"""Qualify immutable explicit Secondary DATA through the production Go API.

Offline maintainer workflow only: no merge execution/native output/application
route. `audit` checks the complete frozen paired corpus; `inspect` qualifies a
supplied native Secondary. Reports are research diagnostics, never capabilities.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import shutil
from pathlib import Path
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
OWNED = Path('docs/research/continuation/explicit-secondary-data')
INHERITED = '216d59f01cb596b1e3fca2c0005d86dbad89854231ac8e9923276039e28d67b8'
PREFIX = 'github.com/lynncoleart/wordling/'
PACKAGES = {PREFIX + p for p in ('internal/wp51', 'internal/merge/native', 'internal/merge/explicit', 'internal/merge/explicit/evidence/qualify')}
MANIFEST_SHA256 = 'a2d71aff3e9bbef8a9d352e99d6f94ee3c2ed39d5ffb36155a01da56e8d3b901'
MAX_INPUT = 1 << 20
MAX_STDOUT = 64 << 20
MAX_STDERR = 1 << 20
MAX_REPORT = 64 << 20


class Refusal(Exception):
    """Atomic research qualification refusal; no report publication."""


def require(condition, detail):
    if not condition:
        raise Refusal(detail)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path, cap):
    require(not path.is_symlink() and path.is_file(), 'RegularInputRequired')
    with path.open('rb') as stream:
        data = stream.read(cap + 1)
    require(len(data) <= cap, 'InputCap')
    return data


def source_path(root, relative):
    parts = Path(relative)
    require(not parts.is_absolute() and '..' not in parts.parts, 'SourcePath')
    current = root
    for part in parts.parts:
        current = current / part
        require(not current.is_symlink(), 'SourceSymlink')
    return current


def inherited_bounded(root, staging):
    """Import ONLY the exact inherited public function from a declared stage."""
    raw = read(source_path(root, 'scripts/reference/secondary_record_contract.py'), MAX_INPUT)
    require(sha(raw) == INHERITED, 'InheritedBoundedSource')
    path = staging / 'inherited_secondary_record_contract.py'
    with path.open('xb') as stream:
        stream.write(raw)
    path.chmod(0o444)
    spec = importlib.util.spec_from_file_location('wordling_inherited_bounded', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # No Session, authority loader, private function or global mutation.
    return module.bounded


def json_value(raw):
    try:
        return json.loads(raw)
    except (ValueError, RecursionError) as error:
        raise Refusal('InvalidJSON') from error


def stream_hash(path):
    count = 0
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(1 << 20):
            count += len(block)
            require(count <= 32 << 20, 'SourceArchiveCap')
            h.update(block)
    return {'bytes': count, 'sha256': h.hexdigest()}


def diagnostic(raw, expected):
    require(len(raw) <= MAX_STDOUT, 'DiagnosticCap')
    report = json_value(raw)
    require(type(report) is dict and report.get('schema') == 'wordling.explicit-secondary-data.v1'
            and report.get('scope') == 'explicit-field-DATA-only', 'DiagnosticSchema')
    observations = report.get('inputs')
    require(type(observations) is list and len(observations) == len(expected), 'DiagnosticRoster')
    total_bytes = total_values = 0
    for observation, source in zip(observations, expected):
        require(type(observation) is dict and observation.get('name') == source['name']
                and observation.get('role') == source['role'] and observation.get('bytes') == len(source['data'])
                and observation.get('sha256') == sha(source['data']) and observation.get('export_exact') is True,
                'DiagnosticSource')
        total_bytes += len(source['data'])
        require(type(observation.get('findings')) is list, 'DiagnosticFindings')
        records = observation.get('records')
        if source['role'] != 'Secondary':
            require(observation.get('qualified') is False and records is None, 'DiagnosticRole')
            continue
        require(observation.get('qualified') is True and observation.get('generic_supported') is False
                and observation.get('generic_admitted') is False and type(records) is list and 1 <= len(records) <= 4096,
                'DiagnosticQualification')
        for ordinal, record in enumerate(records, 1):
            require(type(record) is dict and record.get('ordinal') == ordinal
                    and type(record.get('fields')) is list and 1 <= len(record['fields']) <= 2,
                    'DiagnosticRecord')
            require(record.get('stored_count') in (2, 3) and type(record.get('tail')) is dict and record['tail'].get('length') == 0
                    and len(record.get('opaque_hex', '')) == 64, 'DiagnosticProvenance')
            for number, field in enumerate(record['fields'], 1):
                require(type(field) is dict and field.get('ordinal') == number, 'DiagnosticField')
                try:
                    value = bytes.fromhex(field['hex'])
                except (ValueError, KeyError, TypeError) as error:
                    raise Refusal('DiagnosticHex') from error
                require(field.get('explicitly_empty') is (len(value) == 0) and type(field.get('content')) is dict
                        and len(value) == field['content'].get('length'), 'DiagnosticPresence')
                total_values += len(value)
            missing = record.get('missing')
            require(missing == {'record': ordinal, 'field': len(record['fields'])+1,
                                'category': 'ExplicitFieldMissing', 'valid': False}, 'DiagnosticMissing')
    require(report.get('total_input_bytes') == total_bytes and report.get('total_value_bytes') == total_values
            and total_values <= total_bytes, 'DiagnosticTotals')
    return report


class Session:
    """One finite invocation; new source authority, inherited public containment."""
    def __init__(self, root, staging):
        self.root = root
        self.staging = staging
        self.started = time.monotonic()
        self.deadline = self.started + 600
        self.receipts = []
        self.bounded = inherited_bounded(root, staging)
        manifest_raw = read(root / OWNED / 'source-manifest.json', MAX_INPUT)
        require(sha(manifest_raw) == MANIFEST_SHA256, 'SourceManifestBinding')
        self.manifest = json_value(manifest_raw)
        require(self.manifest.get('schema') == 'wordling.explicit-source.v1', 'SourceManifestSchema')
        self.check_sources()

    def command(self, argv, *, data=b'', seconds=120, cap=MAX_STDOUT):
        remaining = self.deadline - time.monotonic()
        require(remaining > 0, 'InvocationDeadline')
        start = time.monotonic()
        try:
            code, out, err = self.bounded(argv, self.root, data=data, timeout=min(seconds, remaining), cap=cap)
        except Exception as error:
            self.receipts.append({'argv': list(map(str, argv)), 'cwd': str(self.root),
                                  'stdin_bytes': len(data), 'stdin_sha256': sha(data),
                                  'status': None, 'bounded_error': str(error)[:4096],
                                  'elapsed_seconds': time.monotonic()-start,
                                  'partial_output_unavailable_from_inherited_public_API': True})
            raise Refusal('BoundedHelperFailure:' + str(error)[:4096]) from error
        self.receipts.append({'argv': list(map(str, argv)), 'cwd': str(self.root),
                              'stdin_bytes': len(data), 'stdin_sha256': sha(data),
                              'stdout': out.decode('utf8', errors='replace'), 'stdout_base64': base64.b64encode(out).decode(), 'stdout_sha256': sha(out),
                              'stderr': err.decode('utf8', errors='replace'), 'stderr_base64': base64.b64encode(err).decode(), 'stderr_sha256': sha(err),
                              'status': code, 'elapsed_seconds': time.monotonic()-start})
        require(code == 0, 'HelperExit:' + str(code) + ':' + err[:4096].decode(errors='replace'))
        return out

    def check_sources(self):
        for name, pin in self.manifest['files'].items():
            raw = read(source_path(self.root, name), 32 << 20)
            require(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'SourceSubstitution:' + name)
        pins = json_value(read(self.root / OWNED / 'inherited-pins.json', 2 << 20))
        require(len(pins['roster59']) == 59, 'InheritedRoster59')
        for pin in pins['unchanged_members']:
            raw = read(source_path(self.root, pin['path']), 32 << 20)
            require(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'InheritedSourceChanged:' + pin['path'])
        self.inherited_pins = pins

    def build(self):
        go_path = shutil.which('go')
        require(go_path is not None, 'GoExecutableMissing')
        for name, pin in self.manifest['host_tools'].items():
            path = Path(go_path).resolve() if name == 'go' else Path(pin['path'])
            require(str(path) == str(Path(pin['path']).resolve()) and stream_hash(path) == {'bytes': pin['bytes'], 'sha256': pin['sha256']}, 'HostToolSubstitution:' + name)
        env = json_value(self.command(['go', 'env', '-json', 'GOMOD', 'GOWORK', 'GOVERSION', 'GOROOT', 'GOOS', 'GOARCH', 'CGO_ENABLED']))
        require(Path(env['GOMOD']).resolve() == self.root / 'go.mod' and env['GOWORK'] == 'off'
                and env['GOVERSION'] == 'go1.26.4' and env['GOOS'] == 'linux', 'GoEnvironment')
        raw = self.command(['go', 'list', '-deps', '-export', '-json', './internal/merge/explicit/evidence/qualify'])
        decoder = json.JSONDecoder(); text = raw.decode(); packages = []; at = 0
        while at < len(text):
            while at < len(text) and text[at].isspace():
                at += 1
            if at == len(text):
                break
            package, at = decoder.raw_decode(text, at)
            packages.append(package)
        local = {p['ImportPath'] for p in packages if not p.get('Standard')}
        require(local == PACKAGES, 'ActualLocalPackageClosure')
        compiled = set()
        closure = []
        require(len(packages) <= 256, 'CompiledPackageCap')
        source_count = source_bytes = 0
        for p in packages:
            row = {k: p.get(k) for k in ('ImportPath', 'Standard', 'Dir', 'GoFiles', 'CgoFiles', 'CFiles', 'CXXFiles', 'MFiles', 'HFiles', 'FFiles', 'SFiles', 'SysoFiles', 'Imports', 'Export', 'BuildID')}
            require(not p.get('CgoFiles') and not p.get('CFiles'), 'UnexpectedCgoClosure')
            if not p.get('Standard'):
                for filename in p.get('GoFiles', []):
                    path = Path(p['Dir']) / filename
                    require(path.is_relative_to(self.root), 'LocalSourceOutsideRoot')
                    relative = str(path.relative_to(self.root));compiled.add(relative)
                    pin = self.manifest['files'].get(relative)
                    require(pin and sha(read(path, MAX_INPUT)) == pin['sha256'], 'ActualCompiledSource')
            row['compiled_source_pins'] = {}
            for kind in ('GoFiles', 'CgoFiles', 'CFiles', 'CXXFiles', 'MFiles', 'HFiles', 'FFiles', 'SFiles', 'SysoFiles'):
                for filename in p.get(kind, []):
                    source_count += 1
                    require(source_count <= 4096, 'CompiledSourceCountCap')
                    pin = stream_hash(Path(p['Dir']) / filename)
                    source_bytes += pin['bytes']
                    require(source_bytes <= 128 << 20, 'CompiledSourceByteCap')
                    row['compiled_source_pins'][filename] = pin
            if p.get('Export'):
                row['archive'] = stream_hash(Path(p['Export']))
            closure.append(row)
        expected = {f for f in self.manifest['files'] if f.endswith('.go')}
        require(compiled == expected, 'ActualGoFilesClosure')
        compiler = Path(env['GOROOT']) / 'pkg/tool/linux_amd64/compile'
        binary = self.staging / 'qualify'
        self.command(['go', 'build', '-o', str(binary), './internal/merge/explicit/evidence/qualify'])
        self.binary = binary
        git_head = self.command(['git', 'rev-parse', 'HEAD']).decode().strip()
        git_status = self.command(['git', 'status', '--porcelain', '--untracked-files=all']).decode()
        self.authority = {'git_head_diagnostic': git_head, 'git_status': git_status, 'environment': env, 'packages': closure, 'compiled_local_files': sorted(compiled),
                          'compiler': {'path': str(compiler), **stream_hash(compiler)},
                          'binary': {'path': str(binary), **stream_hash(binary)},
                          'module': self.manifest, 'host_tools': self.manifest['host_tools'], 'inherited_bounded_sha256': INHERITED,
                          'inherited_staged_path': str(self.staging / 'inherited_secondary_record_contract.py'),
                          'launcher': {'path': str(Path(__file__).resolve()), **stream_hash(Path(__file__).resolve())}}
        return binary

    def qualify(self, inputs):
        require(0 < len(inputs) <= 30 and sum(len(x['data']) for x in inputs) <= 30*MAX_INPUT, 'NativeRosterCap')
        for x in inputs:
            require(len(x['data']) <= MAX_INPUT, 'NativeInputCap')
        request = {'inputs': [{**x, 'data': base64.b64encode(x['data']).decode()} for x in inputs]}
        payload = json.dumps(request, separators=(',', ':')).encode()
        raw = self.command([str(self.binary)], data=payload)
        report = diagnostic(raw, inputs)
        self.check_sources()
        return report


def corpus_inputs(session):
    corpus = json_value(read(session.root / OWNED / 'corpus.json', MAX_INPUT))
    roster = session.inherited_pins['roster59']; inputs = []
    for pair in corpus['paired']:
        for role in ('Primary', 'Secondary', 'Result'):
            name = pair['source_paths'][role]
            pin = next(p for p in roster if p['path'] == name)
            raw = read(source_path(session.root, name), MAX_INPUT)
            require(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'OriginalInputBinding')
            inputs.append({'name': name, 'role': role, 'data': raw})
    require(len(inputs) == 30, 'OriginalRoster30')
    return corpus, inputs


def compare_originals(report, corpus):
    by_name = {x['name']: x for x in report['inputs']}
    records = fields = empties = 0
    cohorts = set()
    for pair in corpus['paired']:
        actual = by_name[pair['source_paths']['Secondary']]
        values = [[f['hex'] for f in r['fields']] for r in actual['records']]
        require(values == pair['explicit_values_hex'], 'IndependentFrozenFieldObservation')
        require(len(actual['records']) == len(pair['independent_frozen53_shape']), 'IndependentFrozenRecordCount')
        for r, shape, frozen in zip(actual['records'], pair['literal_shapes'], pair['independent_frozen53_shape']):
            for key, old_key in [('raw', 'raw'), ('end_record', 'end_record'), ('tail', 'tail'), ('opaque', None), ('hardpage', None)]:
                old = frozen[old_key] if old_key else frozen['post_record'][0 if key == 'opaque' else 1]
                require(r[key] == {'offset': old['Offset'], 'length': old['Length']}, 'IndependentFrozenRecordSpan')
            for field, old_field in zip(r['fields'], frozen['fields']):
                for key in ('content', 'end_field', 'separator'):
                    old = old_field[key]
                    require(field[key] == {'offset': old['Offset'], 'length': old['Length']}, 'IndependentFrozenFieldSpan')
            require(r['opaque_hex'] == frozen['post_record'][0]['Hex'], 'IndependentFrozenOpaqueOwner')
            require((r['stored_count'], len(r['fields'])) == tuple(shape), 'IndependentFrozenLiteralShape')
            records += 1; fields += len(r['fields'])
            empties += sum(f['explicitly_empty'] for f in r['fields'])
            cohorts.add(r['opaque_hex'])
    require((records, fields, empties) == (24, 36, 6) and cohorts == set(corpus['selected_opaque_octets']), 'OriginalQualificationTotals')
    return {'records': records, 'explicit_fields': fields, 'explicit_empties': empties,
            'opaque_cohorts': len(cohorts), 'meaning': 'finite roster observation; not runtime limits or merge outputs'}


def report_destination(path, input_path=None, protected=()):
    """Create JSON diagnostics or replace only a prior workflow report.

    Native inputs and the pinned source roster are never output targets.
    This assumes trusted local directories, not a hostile-owner CAS guarantee.
    """
    require(path.suffix.lower() == '.json', 'ReportJSONSuffixRequired')
    require(not path.is_symlink() and path.parent.is_dir(), 'ReportDestination')
    require(not path.exists() or path.is_file(), 'NonregularReportDestination')
    current = path.parent
    while current != current.parent:
        require(not current.is_symlink(), 'ReportParentSymlink')
        current = current.parent
    targets = list(protected)
    if input_path is not None:
        targets.append(input_path)
    for source in targets:
        require(path.resolve() != source.resolve(), 'ReportIsProtectedInput')
        if path.exists() and source.exists():
            require(not os.path.samefile(path, source), 'ReportIsProtectedInput')
    if path.exists():
        previous = json_value(read(path, MAX_REPORT))
        require(type(previous) is dict and previous.get('schema') == 'wordling.explicit-qualification.v1'
                and previous.get('scope') == 'explicit-field-DATA-only'
                and previous.get('no_merge_execution_or_native_output') is True, 'UnrelatedReportDestination')


def protected_report_sources(session):
    names = set(session.manifest['files'])
    names.update(p['path'] for p in session.inherited_pins['roster59'])
    names.update(p['path'] for p in session.inherited_pins['unchanged_members'])
    names.update(('scripts/reference/explicit_secondary_data.py', str(OWNED/'source-manifest.json')))
    return [source_path(session.root, name) for name in sorted(names)]


def atomic_report(path, value):
    require(not path.is_symlink(), 'ReportSymlink')
    require(path.parent.is_dir(), 'ReportParentRequired')
    current = path.parent
    while current != current.parent:
        require(not current.is_symlink(), 'ReportParentSymlink')
        current = current.parent
    encoded = json.dumps(value, indent=2).encode() + b'\n'
    require(len(encoded) <= MAX_REPORT, 'ReportCap')
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.explicit-data-', delete=False) as stream:
            temp = Path(stream.name);stream.write(encoded);stream.flush();os.fsync(stream.fileno())
        os.replace(temp, path);temp = None
        fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try: os.fsync(fd)
        finally: os.close(fd)
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    audit = sub.add_parser('audit');audit.add_argument('--report', required=True, type=Path)
    inspect = sub.add_parser('inspect');inspect.add_argument('--input', required=True, type=Path)
    inspect.add_argument('--role', choices=('Secondary',), required=True)
    inspect.add_argument('--report', required=True, type=Path)
    args = parser.parse_args(argv)
    session = None
    try:
        report_destination(args.report, args.input if args.command == 'inspect' else None)
        with tempfile.TemporaryDirectory(prefix='wordling-explicit-data-') as directory:
            session = Session(ROOT, Path(directory))
            protected = protected_report_sources(session)
            report_destination(args.report, args.input if args.command == 'inspect' else None, protected)
            session.build()
            if args.command == 'audit':
                corpus, inputs = corpus_inputs(session)
            else:
                inputs = [{'name': str(args.input), 'role': args.role, 'data': read(args.input, MAX_INPUT)}]
            report = session.qualify(inputs)
            summary = compare_originals(report, corpus) if args.command == 'audit' else {'inspected': len(inputs)}
            # Every source and runtime API check finishes before publication.
            result = {'schema': 'wordling.explicit-qualification.v1', 'scope': 'explicit-field-DATA-only',
                      'qualified': report, 'summary': summary, 'authority': session.authority,
                      'receipts': session.receipts, 'elapsed_seconds': time.monotonic()-session.started,
                      'limits': {'call_seconds': 120, 'invocation_seconds': 600, 'stdout': MAX_STDOUT,
                                 'stderr': MAX_STDERR, 'native_input': MAX_INPUT, 'reports': 1},
                      'no_merge_execution_or_native_output': True}
            require(time.monotonic() < session.deadline, 'InvocationDeadline')
            report_destination(args.report, args.input if args.command == 'inspect' else None, protected)
            atomic_report(args.report, result)
        print('Qualified explicit DATA; generic merge admission remains blocked.')
        return 0
    except Exception as error:
        if session is not None and args.report.parent.is_dir():
            # Failed-attempt evidence is explicitly NOT a qualification report.
            # A unique atomic sibling preserves both the prior report and reds.
            try:
                failure = {'schema': 'wordling.explicit-failed-attempt.v1', 'qualified': False,
                           'error': str(error)[:4096], 'error_type': type(error).__name__, 'receipts': session.receipts,
                           'elapsed_seconds': time.monotonic()-session.started}
                with tempfile.NamedTemporaryFile(dir=args.report.parent, prefix=args.report.name + '.failed-', suffix='.json', delete=False) as stream:
                    failure_path = Path(stream.name)
                atomic_report(failure_path, failure)
                print('Failed attempt evidence: ' + str(failure_path), file=sys.stderr)
            except (OSError, Refusal):
                print('Failed attempt evidence unavailable', file=sys.stderr)
        print('explicit-secondary-data: ' + str(error)[:4096], file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
