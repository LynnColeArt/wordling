#!/usr/bin/env python3
"""Read-only conformance checks and explicit deterministic imports (stdlib only)."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

MISSION = 'kitty-specs/wp51-parity-01M64CVY/'
DIRECTORY = 'docs/conformance/v1/'
LEVELS = ['documentary', 'original_observation', 'component',
          'executable_integration', 'differential', 'physical_qualification']
STATES = ['unverified', 'blocked', 'fail', 'pass']
MAX_BLOB = 8 * 1024 * 1024
SOURCE_LOCKS = [
  {
    "path": "docs/research/command-scenarios.json",
    "commit": "18d6afe95ffcd676fc3f9e964dcad884c9a8c289",
    "sha256": "8161fe7e5f032aa459c8f33a149a00f6e7263cd153f613533d297eeca9ec8d4a"
  },
  {
    "path": "docs/research/feature-inventory.json",
    "commit": "18d6afe95ffcd676fc3f9e964dcad884c9a8c289",
    "sha256": "633cad8fbcc3e59a13bf0003566bfdb2f9925c26a5899a54a989a65da91138d5"
  },
  {
    "path": "kitty-specs/wp51-parity-01M64CVY/spec.md",
    "commit": "db3ea8e4f45211c8517c24d3944e5b3e843dc54d",
    "sha256": "4255ca47a7e85912094e493dfe68473c2520db722402de081c927367951c6ed7"
  },
  {
    "path": "docs/compatibility.md",
    "commit": "027f1e49a0dbd9cfb1429af0d7a92a6bb5403eb2",
    "sha256": "98014cd41863f1d38186b45391408455f9410fd35ab88ff1f75bfc03c8a5f27a"
  },
  {
    "path": "docs/research/sources.json",
    "commit": "91c6bd605fe797be4c6f824dd5916460af49e3e3",
    "sha256": "850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"
  },
  {
    "path": "docs/research/reference-baseline.json",
    "commit": "027f1e49a0dbd9cfb1429af0d7a92a6bb5403eb2",
    "sha256": "6ba2f6bd8fa77e4b309b1a81203705c060285707ab07ec6f3432dfa194075ba5"
  },
  {
    "path": "kitty-specs/wp51-parity-01M64CVY/contracts/coverage-leaves.md",
    "commit": "d7b94b1ffde842498422b38e0acc85e2ba794dcd",
    "sha256": "0a095521e8f378351b12c64c0b326c141946f653c9dfce1fec801110e60e8118"
  },
  {
    "path": "kitty-specs/wp51-parity-01M64CVY/contracts/resource-readiness.md",
    "commit": "aa61527948b065c1cb7a4a9a08f0de346544b2c5",
    "sha256": "39f982db595d35b754075b4d94c76bfd70659c61e3f24f454374c66c8c0fc0bd"
  },
  {
    "path": "kitty-specs/wp51-parity-01M64CVY/tasks/WP13-original-session-probes/review-cycle-2.md",
    "commit": "7e73d92a756f1e6676234ae736690824e2efa249",
    "sha256": "13c7d19fee80fb05a26f400293600fde232ec47e6ff2444f9efc87973b7c9167"
  },
  {
    "path": "kitty-specs/wp51-parity-01M64CVY/tasks/WP20-resource-readiness/review-cycle-1.md",
    "commit": "bce35742d03823aad8815317764efdb18cc73858",
    "sha256": "37dc1bea12364d3ccf47bbfaef56deb361b009b08c159bff6591cd014abb332e"
  },
  {
    "path": "kitty-specs/wp51-parity-01M64CVY/tasks/WP21-coverage-leaves/review-cycle-1.md",
    "commit": "2aa9bb75e464e1290c639070a934707b84e3536c",
    "sha256": "1e5e48e9e521109c89a3a748e9223bc750d7db52363608e5a859d52c15180348"
  },
  {
    "path": "kitty-specs/wp51-parity-01M64CVY/tasks/WP18-bubbletea-session/review-cycle-2.md",
    "commit": "15cc3c9be27495fa3a4ebece23a7d3a4be046d2e",
    "sha256": "0a969e741e57552a944cf18380db39882e7ac063c706e19b4265f854b40ad5ca"
  },
  {
    "commit": "027f1e49a0dbd9cfb1429af0d7a92a6bb5403eb2",
    "path": "docs/research/reference-environment/environment.json",
    "sha256": "30123ddc32289702c8240bf4e5bef65d0ff979c5d48b558f544271b14c00bfc2"
  },
  {
    "commit": "027f1e49a0dbd9cfb1429af0d7a92a6bb5403eb2",
    "path": "docs/research/reference-environment/resource-profile.json",
    "sha256": "e9498fb1833fac66509b792dacd5ccf3915f26f2a24ff1f0f8cbe72d7aa9645b"
  }
]


class Invalid(ValueError):
    """A checkable record, provenance or claim failure."""


def require(condition, message):
    if not condition:
        raise Invalid(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()


def revision(value):
    raw = (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n').encode()
    return digest(raw)


def fields(value, keys, where):
    require(isinstance(value, dict) and set(value) == set(keys), f'{where}: invalid fields')


def text(value, where):
    require(isinstance(value, str) and bool(value.strip()), f'{where}: nonempty text required')


def unique(rows, where):
    require(isinstance(rows, list), f'{where}: list required')
    result = {}
    for row in rows:
        require(isinstance(row, dict), f'{where}: object required')
        key = row.get('id')
        text(key, where + '.id')
        require(key not in result, f'{where}: duplicate {key}')
        result[key] = row
    return result


def safe_path(value):
    text(value, 'path')
    p = PurePosixPath(value)
    require(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts
            and str(p) == value and ':' not in value and '\\' not in value
            and not value.startswith('-'), f'unsafe repository path: {value!r}')
    return value


def local(root, path):
    safe_path(path)
    p = root / path
    require(p.resolve().is_relative_to(root), f'path escapes root: {path}')
    require(not any(x.is_symlink() for x in [p, *p.parents] if x.is_relative_to(root)),
            f'symlink refused: {path}')
    return p


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_NO_REPLACE_OBJECTS='1')
    p = subprocess.run(['git', '--no-optional-locks', '-C', str(root), *args],
                       capture_output=True, env=env, timeout=15)
    require(p.returncode == 0, f'Git read failed: {args[0]}')
    return p.stdout


def blob(root, ref):
    fields(ref, ['commit', 'path', 'sha256'], 'blob reference')
    require(isinstance(ref['commit'], str) and re.fullmatch('[0-9a-f]{40}', ref['commit']),
            'blob reference requires full immutable commit SHA')
    safe_path(ref['path'])
    require(isinstance(ref['sha256'], str) and re.fullmatch('[0-9a-f]{64}', ref['sha256']),
            'blob reference requires SHA-256')
    git(root, 'cat-file', '-e', ref['commit'] + '^{commit}')
    spec = ref['commit'] + ':' + ref['path']
    size = int(git(root, 'cat-file', '-s', spec))
    require(size <= MAX_BLOB, 'blob exceeds 8 MiB evidence budget')
    raw = git(root, 'cat-file', 'blob', spec)
    require(digest(raw) == ref['sha256'], f"hash mismatch: {ref['path']}")
    return raw


def load_json(raw):
    def pairs(items):
        result = {}
        for k, v in items:
            require(k not in result, f'duplicate JSON key: {k}')
            result[k] = v
        return result
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(Invalid('nonfinite JSON number')))


def ledger(raw):
    blocks = re.findall(rb'```json\n(.*?)\n```', raw, re.S)
    require(len(blocks) == 1, 'expected one documentary ledger')
    return load_json(blocks[0])


def sources(root):
    result = {}
    for lock in SOURCE_LOCKS:
        raw = blob(root, lock)
        # An inherited working file must match its frozen Git source. Missing review
        # metadata may legitimately live only on the coordination/primary commit.
        p = local(root, lock['path'])
        if p.exists():
            require(p.read_bytes() == raw, f"working source drift: {lock['path']}")
        result[lock['path']] = raw
    return result


def build(root):
    src = sources(root)
    cases = load_json(src['docs/research/command-scenarios.json'])
    features = load_json(src['docs/research/feature-inventory.json'])
    require(len(cases) == 244 and len(features) == 91, 'approved source count mismatch')
    feature_map = unique(features, 'features')
    unique(cases, 'cases')
    for case in cases:
        require(case['implementation_status'] == 'not-implemented', 'historical source status changed')
        require(set(case['feature_ids']) <= feature_map.keys(), 'historical unknown feature')
    for feature in features:
        linked = [c['id'] for c in cases if feature['id'] in c['feature_ids']]
        require(feature['command_scenario_ids'] == linked, 'historical ordered back-link mismatch')
    reqs = []
    for path in [MISSION + 'spec.md', 'docs/compatibility.md']:
        for line in src[path].decode().splitlines():
            match = re.match(r'^\| ((?:FR|NFR|C|FC)-\d{3}) \| (.*?) \|', line)
            if match:
                reqs.append({'id': match[1], 'description': match[2], 'status': 'open'})
    require(len(unique(reqs, 'requirements')) == 38, 'obligation source count mismatch')
    return {
        'schema_version': 1,
        'source_snapshots': SOURCE_LOCKS,
        'mission': {'id': 'wp51-parity-01M64CVY', 'parity_accepted': False,
                    'all_m1_obligations_closed': False, 'queue_exhaustion_authorizes_acceptance': False},
        'historical': {'cases': cases, 'features': features},
        'requirements': sorted(reqs, key=lambda r: r['id']),
        'groups': [{'id': f['id'], 'status': 'open'} for f in features],
        'discovery': ledger(src[MISSION + 'contracts/coverage-leaves.md']),
        'resources': ledger(src[MISSION + 'contracts/resource-readiness.md']),
        'extensions': [], 'additional_obligations': [], 'evidence': [],
    }


SCHEMA = {
    'schema_version': 1,
    'title': 'Wordling bounded current conformance integrity contract',
    'validation': 'scripts/conformance/v1/conformance.py (stdlib semantic validator)',
    'root_fields': ['schema_version', 'source_snapshots', 'mission', 'historical',
                    'requirements', 'groups', 'discovery', 'resources', 'extensions',
                    'additional_obligations', 'evidence'],
    'immutable_fields': ['source_snapshots', 'mission', 'historical', 'requirements',
                         'groups', 'discovery', 'resources'],
    'levels': LEVELS, 'states': STATES,
    'extension_fields': ['id', 'revision', 'supersedes', 'title', 'feature_ids',
                         'requirement_ids', 'parent_case_ids', 'baseline_id',
                         'source_locators', 'preconditions', 'steps', 'expected'],
    'additional_obligation_fields': ['id', 'title', 'feature_ids', 'requirement_ids',
                                    'source_locators', 'remaining', 'status'],
    'nonpassing_evidence_fields': ['id', 'level', 'state', 'case_id', 'case_revision', 'scope', 'note'],
    'passing_evidence_fields': ['id', 'level', 'state', 'case_id', 'case_revision',
                                'scope', 'run', 'review'],
    'profile_policy': 'v1 admits the pinned selected original profile only; physical qualification remains unproved',
    'closure_policy': 'v1 admits bounded evidence only; whole parents and mission stay open',
    'case_revision': 'SHA-256 of sorted-key compact UTF-8 JSON + LF, ensure_ascii=false',
    'evidence_protocol': 'See README.md in this directory: committed run + independent review + raw witnesses',
}


# Portable structural schema; executable validation additionally checks immutable
# source equality, lineage, evidence hashes, review identity and comparator results.
SCHEMA.update({
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'type': 'object', 'required': SCHEMA['root_fields'], 'additionalProperties': False,
    'properties': {key: {'type': 'array' if key in [
        'source_snapshots', 'requirements', 'groups', 'extensions',
        'additional_obligations', 'evidence'] else 'object'}
        for key in SCHEMA['root_fields'] if key != 'schema_version'},
})
SCHEMA['properties']['schema_version'] = {'const': 1}
SCHEMA['properties']['extensions']['items'] = {
    'type': 'object', 'required': SCHEMA['extension_fields'], 'additionalProperties': False,
    'properties': {
        'id': {'type': 'string', 'pattern': '^EXT51-[0-9]{4}$'},
        'revision': {'const': 1}, 'supersedes': {'type': ['object', 'null']},
        **{key: {'type': 'string', 'minLength': 1} for key in ['title', 'baseline_id']},
        **{key: {'type': 'array', 'minItems': 1} for key in [
            'feature_ids', 'requirement_ids', 'parent_case_ids', 'source_locators',
            'preconditions', 'steps', 'expected']},
    },
}
SCHEMA['properties']['evidence']['items'] = {
    'type': 'object', 'required': ['id', 'level', 'state', 'case_id', 'case_revision', 'scope'],
    'properties': {'id': {'type': 'string', 'minLength': 1},
                   'level': {'enum': LEVELS}, 'state': {'enum': STATES},
                   'case_id': {'type': 'string'},
                   'case_revision': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'},
                   'scope': {'type': 'string', 'minLength': 1}},
    'description': 'Pass requires committed run/review envelope; nonpass requires note. CLI enforces exact fields.',
}


def links(row, key, allowed):
    vals = row.get(key)
    require(isinstance(vals, list) and vals and len(vals) == len(set(vals))
            and all(isinstance(x, str) and x in allowed for x in vals),
            f"{row.get('id')}: invalid {key}")


def locators(row, source_map):
    vals = row.get('source_locators')
    require(isinstance(vals, list) and vals, f"{row.get('id')}: missing source_locators")
    for loc in vals:
        fields(loc, ['source_id', 'printed_start', 'printed_end', 'pdf_start', 'pdf_end'], 'locator')
        require(loc['source_id'] in source_map, 'unknown source locator')
        nums = [loc[k] for k in ['printed_start', 'printed_end', 'pdf_start', 'pdf_end']]
        require(all(type(n) is int and n > 0 for n in nums) and nums[0] <= nums[1]
                and nums[2] <= nums[3] <= source_map[loc['source_id']]['pdf_pages'], 'invalid locator range')
        offset = {'REF51': 17, 'WB51': 9, 'SDK51': 13}.get(loc['source_id'])
        if offset is not None:
            require(nums[0] + offset == nums[2] and nums[1] + offset == nums[3], 'printed/PDF locator mismatch')


def extensions(rows, base, source_map):
    seen = unique(rows, 'extensions')
    require(not set(seen) & set(c['id'] for c in base['historical']['cases']), 'inherited ID collision')
    families = {}
    for row in rows:
        fields(row, SCHEMA['extension_fields'], row['id'])
        require(re.fullmatch(r'EXT51-\d{4}', row['id']), 'extension ID must be EXT51-####')
        # One current immutable revision per ID; a new revision links a previous
        # extension case revision via a new stable ID, preventing silent replacement.
        require(type(row['revision']) is int and row['revision'] == 1, 'extension revision must start at 1; use a new ID with lineage')
        text(row['title'], 'extension title')
        links(row, 'feature_ids', set(f['id'] for f in base['historical']['features']))
        links(row, 'requirement_ids', set(r['id'] for r in base['requirements']))
        links(row, 'parent_case_ids', set(c['id'] for c in base['historical']['cases']))
        parents = [c for c in base['historical']['cases'] if c['id'] in row['parent_case_ids']]
        require(set(row['feature_ids']) <= {f for c in parents for f in c['feature_ids']},
                'extension uses semantically unrelated parent feature association')
        require(row['baseline_id'] == base['historical']['cases'][0]['baseline_id'], 'unknown baseline')
        locators(row, source_map)
        for key in ['preconditions', 'steps', 'expected']:
            require(isinstance(row[key], list) and row[key], f'missing {key}')
            for value in row[key]:
                text(value, key)
        if row['supersedes'] is not None:
            fields(row['supersedes'], ['id', 'sha256'], 'extension lineage')
            previous = families.get(row['supersedes']['id'])
            require(previous is not None and revision(previous) == row['supersedes']['sha256'], 'invalid extension lineage')
        families[row['id']] = row
    return seen


def witness(root, ref):
    return blob(root, ref)


def passing(root, evidence, case):
    fields(evidence, SCHEMA['passing_evidence_fields'], evidence['id'])
    require(evidence['level'] in ['component', 'executable_integration', 'differential', 'physical_qualification'],
            'documentary/original-only pass must remain historical or independently modeled')
    run = load_json(witness(root, evidence['run']))
    required = ['kind', 'case_id', 'case_revision', 'scope', 'implementation_commit',
                'implementer', 'executed', 'argv', 'exit_code', 'executable_sha256',
                'baseline_id', 'profile', 'inputs', 'outputs', 'checks']
    fields(run, required, 'run')
    require(run['case_id'] == case['id'] and run['case_revision'] == revision(case)
            and run['scope'] == evidence['scope'], 'run case revision/scope mismatch')
    code = run['implementation_commit']
    require(isinstance(code, str) and re.fullmatch('[0-9a-f]{40}', code), 'missing implementation commit')
    git(root, 'cat-file', '-e', code + '^{commit}')
    require(run['executed'] is True and type(run['exit_code']) is int and run['exit_code'] == 0,
            'nonexecuted or unsuccessful run cannot pass')
    require(isinstance(run['argv'], list) and run['argv'] and all(isinstance(x, str) and x for x in run['argv']), 'missing executable invocation')
    require(isinstance(run['executable_sha256'], str) and re.fullmatch('[0-9a-f]{64}', run['executable_sha256']), 'missing executable hash')
    kind = {'component': 'component-test', 'executable_integration': 'product-execution',
            'differential': 'product-differential', 'physical_qualification': 'physical-qualification'}[evidence['level']]
    require(run['kind'] == kind, 'helper/original-only run cannot promote evidence level')
    if kind.startswith('product-'):
        require(Path(run['argv'][0]).name == 'wordling', 'product evidence must invoke wordling executable')
    require(run['baseline_id'] == case['baseline_id'], 'run baseline mismatch')
    fields(run['profile'], ['environment', 'resources', 'qualification'], 'run profile')
    for key in ['environment', 'resources']:
        refs = run['profile'][key]
        require(isinstance(refs, list) and refs, f'missing {key} profile witnesses')
        expected_path = 'docs/research/reference-environment/' + ('environment.json' if key == 'environment' else 'resource-profile.json')
        expected = next(x for x in SOURCE_LOCKS if x['path'] == expected_path)
        require(len(refs) == 1 and refs[0].get('path') == expected_path
                and refs[0].get('sha256') == expected['sha256'], 'unknown environment/resource profile; reviewed profile extension required')
        for ref in refs:
            witness(root, ref)
    require(run['profile']['qualification'] in ['unqualified', 'qualified'], 'unknown profile qualification')
    if evidence['level'] == 'physical_qualification':
        require(run['profile']['qualification'] == 'qualified', 'unqualified resource cannot pass physical qualification')
    require(run['profile']['qualification'] == 'unqualified',
            'selected historical profile has no physical qualification; reviewed extension required')
    refs = {}
    raw_bytes = {}
    for key in ['inputs', 'outputs']:
        require(isinstance(run[key], list) and run[key], f'missing raw {key}')
        for ref in run[key]:
            raw = witness(root, ref)
            name = ref['commit'] + ':' + ref['path']
            require(name not in refs, 'duplicate raw evidence reference')
            refs[name] = ref['sha256']
            raw_bytes[name] = raw
    require(isinstance(run['checks'], list) and run['checks'], 'missing comparator checks')
    used = set()
    for check in run['checks']:
        fields(check, ['name', 'passed', 'comparator', 'method', 'left', 'right', 'tolerance'], 'comparator check')
        text(check['name'], 'check name')
        require(check['passed'] is True, 'failed comparator cannot pass')
        comparator = witness(root, check['comparator'])
        require(comparator, 'empty comparator')
        require(check['tolerance'] == 'exact', 'v1 supports exact comparison only')
        require(check['left'] in refs and check['right'] in refs, 'check references unknown raw witness')
        require(check['left'] != check['right'], 'self-comparison cannot pass')
        left, right = raw_bytes[check['left']], raw_bytes[check['right']]
        if check['method'] == 'byte_equal':
            matched = left == right
        elif check['method'] == 'json_equal':
            matched = encoded(load_json(left)) == encoded(load_json(right))
        else:
            raise Invalid('unsupported comparator method; reviewed extension required')
        require(matched, 'recomputed comparator failed (declared pass is insufficient)')
        used.update([check['left'], check['right']])
    require(used == set(refs), 'raw input/output omitted from comparator checks')
    review = evidence['review']
    fields(review, ['artifact', 'reviewer'], 'independent review')
    text(run['implementer'], 'implementer')
    text(review['reviewer'], 'reviewer')
    require(review['reviewer'] != run['implementer'], 'self-review cannot pass')
    review_text = witness(root, review['artifact']).decode()
    require(re.search(r'Approved by ' + re.escape(review['reviewer']) + r': ' + code + r'\b', review_text),
            'independent review does not approve exact implementation commit')


def validate(root, value):
    fields(value, SCHEMA['root_fields'], 'registry')
    require(type(value['schema_version']) is int and value['schema_version'] == 1, 'unsupported schema_version')
    baseline = build(root)
    for key in SCHEMA['immutable_fields']:
        require(value[key] == baseline[key], f'{key}: immutable coverage/source/open-parent contract mismatch')
    source_map = unique(load_json(sources(root)['docs/research/sources.json']), 'sources')
    ext = extensions(value['extensions'], baseline, source_map)
    added = unique(value['additional_obligations'], 'additional_obligations')
    for row in added.values():
        fields(row, SCHEMA['additional_obligation_fields'], row['id'])
        require(re.fullmatch(r'ADD51-\d{4}', row['id']), 'additional obligation ID must be ADD51-####')
        require(row['status'] == 'open', 'additional obligation closure unavailable in v1')
        for key in ['title', 'remaining']:
            text(row[key], key)
        links(row, 'feature_ids', set(f['id'] for f in baseline['historical']['features']))
        links(row, 'requirement_ids', set(r['id'] for r in baseline['requirements']))
        locators(row, source_map)
    cases = {**unique(baseline['historical']['cases'], 'cases'), **ext}
    for e in unique(value['evidence'], 'evidence').values():
        require(e.get('level') in LEVELS and e.get('state') in STATES, 'unknown evidence level/state')
        require(e.get('case_id') in cases, f"{e['id']}: unknown evidence case")
        case = cases[e['case_id']]
        require(e.get('case_revision') == revision(case), f"{e['id']}: stale case_revision")
        text(e.get('scope'), 'evidence scope')
        if e['state'] == 'pass':
            passing(root, e, case)
        else:
            fields(e, SCHEMA['nonpassing_evidence_fields'], e['id'])
            text(e['note'], 'nonpassing evidence note')
    return value


def render(value):
    counts = {level: {state: 0 for state in STATES} for level in LEVELS}
    for row in value['evidence']:
        counts[row['level']][row['state']] += 1
    d = value['discovery']
    r = value['resources']
    lines = ['# Current Wordling conformance — schema v1', '',
             'Current authority for maintainers; generated by the public CLI. Full M1 remains open.', '',
             'The immutable original-reference catalogue is the approved WP13 historical snapshot',
             '`18d6afe95ffcd676fc3f9e964dcad884c9a8c289`: **244 scenarios / 91 groups**.',
             'Its original-only/unimplemented labels describe that snapshot, not current product status.',
             'The older 236-case primary snapshot is not interchangeable.', '',
             '**38 obligations / 91 groups remain open.** No schema check or bounded evidence row',
             'closes a parent. Known breadth is incomplete; discoveries expand these obligations.', '',
             '## Current bounded evidence', '', '| Level | Unverified | Blocked | Fail | Pass |',
             '| --- | --- | --- | --- | --- |']
    for level, c in counts.items():
        lines.append('| ' + level + ' | ' + ' | '.join(str(c[s]) for s in STATES) + ' |')
    lines += ['', 'Zero rows means no current claim imported, not an executed pass or absence of obligations.',
              'Historical documentary/original observations remain separately preserved in registry.json.', '',
              '## Documentary leaves and qualification gaps', '',
              f"Retained: {len(d['reference_leaves'])} reference leaves, {len(d['workbook_steps'])} numbered workbook steps,",
              f"{len(d['workbook_context'])} context obligations, {len(d['menu_alternatives'])} menu alternatives,",
              f"{len(d['lessons'])} lesson dispositions, {len(d['case_proposals'])} unexecuted case proposals.",
              f"Retained resource records: {len(r['formats'])} formats, {len(r['locales'])} locales,",
              f"{len(r['field_conflicts'])} unresolved field conflicts, {len(r['retained_graphics_inputs'])} graphics input families.",
              'Resource presence is not qualification. Physical printer: ' + r['physical_printer']['status'] + '.', '',
              f"Current additions: {len(value['extensions'])} case extensions; {len(value['additional_obligations'])} discovered obligations.", '',
              '## Open requirement register', '', '| Obligation | State |', '| --- | --- |']
    lines += [f"| {x['id']} | open |" for x in value['requirements']]
    lines += ['', '## Source snapshots', '', '| Path | Commit | SHA-256 |', '| --- | --- | --- |']
    lines += [f"| `{x['path']}` | `{x['commit']}` | `{x['sha256']}` |" for x in value['source_snapshots']]
    lines += ['', 'See [CLI/evidence protocol](README.md), [schema](schema.json), [registry](registry.json)',
              'and [ADR 0004](../../decisions/0004-conformance-evidence-layers.md).', '',
              'Future normal acceptance-matrix work must link exact registry/case/code/evidence revisions',
              'and complete SC-001–005 coverage. This tool never edits that matrix or lifecycle state.',
              'Native and companion formats remain original. PDF remains optional M2 after genuine M1 acceptance.', '']
    return '\n'.join(lines).encode()


def write_outputs(root, outputs):
    # Preflight every destination before writing anything; only owned fixed paths.
    destinations = [(local(root, path), raw) for path, raw in outputs.items()]
    for p, _ in destinations:
        require(not p.exists() or p.is_file(), f'output is not a file: {p}')
    for p, raw in destinations:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists() and p.read_bytes() == raw:
            continue
        with tempfile.NamedTemporaryFile(dir=p.parent, delete=False) as tmp:
            try:
                tmp.write(raw)
                tmp.flush()
                os.fsync(tmp.fileno())
                name = tmp.name
            except BaseException:
                Path(tmp.name).unlink(missing_ok=True)
                raise
        try:
            os.replace(name, p)
        finally:
            Path(name).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[3])
    sub = parser.add_subparsers(dest='command', required=True)
    for cmd in ['import', 'regenerate', 'check', 'validate']:
        p = sub.add_parser(cmd)
        if cmd == 'validate':
            p.add_argument('--registry', type=Path, required=True)
    args = parser.parse_args()
    try:
        root = args.root.resolve(strict=True)
        registry_path = local(root, DIRECTORY + 'registry.json')
        schema_path = local(root, DIRECTORY + 'schema.json')
        index_path = local(root, DIRECTORY + 'index.md')
        if args.command == 'import':
            value = validate(root, build(root))
            outputs = {DIRECTORY + 'registry.json': encoded(value),
                       DIRECTORY + 'schema.json': encoded(SCHEMA), DIRECTORY + 'index.md': render(value)}
            for name, raw in outputs.items():
                p = local(root, name)
                require(not p.exists() or p.read_bytes() == raw,
                        f'import refuses to replace existing nonidentical {name}; use regenerate to retain evidence')
            write_outputs(root, outputs)
        else:
            path = args.registry if args.command == 'validate' else registry_path
            require(path.stat().st_size <= MAX_BLOB, 'registry exceeds 8 MiB budget')
            value = validate(root, load_json(path.read_bytes()))
            if args.command != 'validate':
                require(load_json(schema_path.read_bytes()) == SCHEMA, 'schema contract drift')
                if args.command == 'check':
                    require(index_path.read_bytes() == render(value), 'index drift: run explicit regenerate')
                else:
                    write_outputs(root, {DIRECTORY + 'index.md': render(value)})
        print(json.dumps({'result': 'valid', 'command': args.command, 'cases': 244,
                          'groups': 91, 'obligations': 38, 'evidence_rows': len(value['evidence']),
                          'full_m1_accepted': False}, sort_keys=True))
        return 0
    except (Invalid, OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        print(json.dumps({'result': 'invalid', 'error': str(exc)}, sort_keys=True))
        return 1


if __name__ == '__main__':
    sys.exit(main())
