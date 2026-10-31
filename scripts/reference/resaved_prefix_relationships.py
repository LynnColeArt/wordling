#!/usr/bin/env python3
"""WP45 offline, source-bound relationship research; never a native writer/VM runner."""
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/research/continuation/resaved-prefix-relationships'
APPROVED42 = 'd77c5f550b821e2c2e18ec8b794ede9a5bc26d22'
SCOPE = 'wordling.wp45.offline-relationships/v1'
LIMIT = 65536
MAX_PREFIX = 564
MAX_BLOCKS = 8
MAX_MATCHES = 4096
STAGES = ['W42S0.WP5', 'W42G1.WP5', 'W42G2.WP5', 'W42G3.WP5', 'W42EDIT.WP5', 'W42FIN.WP5']
PROMOTION = {
 'decision.md': 'e937280d61c849786ffddb894b6fe95c30272557df77dc5ab164ad1386521a2f',
 'manifest.json': '1da96b9017561ba65913b8204687e63081293fc701e855bf2cb9f91ea1d3987c',
 'seals.json': '8c1d987743c328b9948235c34e6f8d9b7610982df33f4dd9285ced27fa42defa',
 'reviews/cycle-2/report.md': 'b5a7e37c97cca3a0c24a3d5f3d4f792f9898e11973657ca7c7c0865c094bf44e',
 'reviews/cycle-2/seals.json': '8dedd710a5c96c992ffd26c63680ca851edab74ab8ae11c2d38ea9f7cf6418ac',
}

class Refusal(ValueError):
    def __init__(self, code, detail):
        self.code = code
        super().__init__(detail)

def require(ok, code, detail):
    if not ok:
        raise Refusal(code, detail)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def git_bytes(path):
    return subprocess.check_output(['git', 'show', APPROVED42 + ':' + path], cwd=ROOT, timeout=15)

def binding(path, approved=True):
    p = ROOT / path
    expected = git_bytes(path) if approved else None
    require(expected is None or len(expected) <= 4*1024*1024, 'SourceLimit', path)
    with p.open('rb') as stream:
        raw = stream.read((len(expected) if expected is not None else 4*1024*1024) + 1)
    require(len(raw) <= 4*1024*1024, 'SourceLimit', path)
    require(not approved or raw == expected, 'ImmutableSourceMismatch', path)
    blob = subprocess.check_output(['git', 'hash-object', str(p)], cwd=ROOT, text=True, timeout=15).strip()
    return {'path': path, 'size': len(raw), 'sha256': digest(raw), 'git_blob': blob,
            'authority': APPROVED42 if approved else 'current-owned-or-promoted'}

def custody():
    # Resolve the original immutable plan's explicit helper closure, not lane-s's tip.
    old = json.loads(git_bytes('docs/research/continuation/resaved-prefix/frozen-plan.json'))
    paths = {x['path'] for x in old['sources']}
    paths.update(['scripts/reference/resaved_prefix.py',
                  'docs/research/continuation/resaved-prefix/family-admission.json',
                  'docs/research/continuation/resaved-prefix/field-ledger.json',
                  'docs/research/continuation/resaved-prefix/contract.md',
                  'docs/research/continuation/resaved-prefix/evidence/matrix-summary.json'])
    sources = [binding(p) for p in sorted(paths)]
    for path, expected in PROMOTION.items():
        rel = 'docs/research/continuation/reordered-prefix-design/' + path
        b = binding(rel, False)
        require(b['sha256'] == expected, 'PromotionMismatch', rel)
        sources.append(b)
    sources.append(binding('scripts/reference/resaved_prefix_relationships.py', False))
    # Validate already-pinned private manuals in streaming form; no acquisition
    # or redistribution. Their exact size is an independent bounded precondition.
    catalog = json.loads((ROOT/'docs/research/sources.json').read_text())
    for item in catalog:
        if item['id'] in ['SDK51', 'REF51']:
            path = Path('/home/lynn/projects/wordling/research/cache')/item['filename']
            require(path.stat().st_size == item['bytes'], 'ManualIdentity', item['id']+' size differs')
            with path.open('rb') as stream:
                observed = hashlib.file_digest(stream, 'sha256').hexdigest()
            require(observed == item['sha256'], 'ManualIdentity', item['id']+' bytes differ')
            sources.append({'path': str(path), 'size': item['bytes'], 'sha256': observed,
                            'git_blob': None, 'authority': 'pinned private '+item['id']+' source; metadata only'})
    return sources

def helpers():
    # Custody is checked before importing inherited executable Python.
    module = importlib.import_module('resaved_prefix')
    return module, module.inspector()

def field_domain(field):
    name = field['name']
    if name == 'body start':
        return 'absolute-file/body-boundary'
    if name == 'font string pool offset':
        return 'pool-local'
    if 'AFC' in name:
        return 'font-row-index/sentinel'
    if name == 'graphics count':
        return 'graphics-count'
    refs = field['references']
    if any(x in refs.lower() for x in ['resource', 'prs', 'descriptor', 'hash']):
        return 'resource/cache'
    return 'scalar-or-literal/no-declared-pointer'

def fields(raw, info):
    ledger = json.loads((ROOT / 'docs/research/continuation/native-edits/field-ledger.json').read_text())['field_coverage']
    require(len(ledger) == 72, 'FieldDefinitionMismatch', 'exact inherited72 fields required')
    result = []
    for f in ledger:
        owners = [{'offset': 0, 'length': 16, 'type': 'header'}] if f['owner'] == 'header' else [p for p in info['packets'] if p['type'] == int(f['owner'].split('-')[1])]
        require(len(owners) == 1, 'OwnerMultiplicity', f['owner'])
        owner = owners[0]
        a, n = owner['offset'] + f['offset'], f['width']
        require(0 <= f['offset'] <= owner['length'] - n, 'FieldExtent', f['name'])
        b = raw[a:a+n]
        representation = f['representation']
        endian = 'single-byte-elements' if representation == 'array u8' else 'little' if 'le' in representation or representation.startswith('u8') else 'not-scalar'
        value = [int.from_bytes(b[i:i+2], 'little') for i in range(0,n,2)] if representation.startswith('2xu16le') else int.from_bytes(b, 'little', signed=representation == 'i16le') if endian == 'little' and n <= 4 else None
        result.append({'owner': f['owner'], 'owner_extent': [owner['offset'], owner['length']],
                       'name': f['name'], 'offset': a, 'width': n, 'relative_offset': f['offset'],
                       'representation': representation, 'endian': endian, 'value': value,
                       'raw_hex': b.hex(), 'base_domain': field_domain(f), 'units': f['units'],
                       'reference_authority': f['references'],
                       'authority': 'approved23 field ledger + SDK WP3–18/103–105; applied only to live owner'})
    # Each byte in each typed live owner is covered exactly once.
    for p in [{'type': 'header', 'offset': 0, 'length': 16}] + [p for p in info['packets'] if p['type'] != 65535]:
        owner = 'header' if p['type'] == 'header' else 'packet-' + str(p['type'])
        coverage = [0] * p['length']
        for f in result:
            if f['owner'] == owner:
                for i in range(f['relative_offset'], f['relative_offset'] + f['width']):
                    coverage[i] += 1
        require(all(x == 1 for x in coverage), 'FieldCoverage', owner)
    return result

def diagnose(raw, inspector):
    """Additional bounded interpretation over unchanged approved field inspector.

    Arbitrary malformed seeds are diagnostics only, never sealed corpus members.
    No deleted bytes are decoded as a complete live packet.
    """
    require(len(raw) <= LIMIT, 'InputLimit', 'at most65536 bytes')
    info = inspector.inspect(raw, False)
    require(16 <= info['body_offset'] <= MAX_PREFIX, 'PrefixLimit', 'observed research prefix <=564')
    require(len(info['blocks']) <= MAX_BLOCKS, 'IndexLimit', 'at most8 blocks')
    B = info['body_offset']
    fs = fields(raw, info)
    owners = [p for p in info['packets'] if p['type'] != 65535]
    lookup = {p['type']: p for p in owners}
    require(set(lookup) == {6, 7, 8, 12, 15}, 'UnsupportedOwner', 'closed observed live types only')
    nodes = [{'id': 'header', 'kind': 'header', 'extent': [0, 16]},
             {'id': 'body', 'kind': 'body', 'extent': [B, len(raw)-B]}]
    edges = [{'source': 'header', 'field_extent': [4, 4], 'endian': 'little', 'width': 4,
              'base_domain': 'absolute-file', 'target': 'body', 'target_offset': B,
              'bounds_valid': B <= len(raw), 'authority': 'SDK WP3–8/PDF16–21'}]
    index_fields = []
    previous = 'header'
    for block in info['blocks']:
        off = block['offset']; ident = 'index@' + str(off)
        nodes.append({'id': ident, 'kind': 'active-index', 'extent': [off, 50]})
        edges.append({'source': previous, 'field_extent': None if previous == 'header' else [int(previous.split('@')[1])+6, 4],
                      'endian': 'little', 'width': 0 if previous == 'header' else 4,
                      'base_domain': 'implicit-file-prefix-start' if previous == 'header' else 'absolute-file',
                      'target': ident, 'target_offset': off, 'bounds_valid': 16 <= off <= B-50,
                      'authority': 'SDK WP7/PDF20: fixed first block at16, then next link'})
        previous = ident
        for rel, width, name in [(0, 2, 'header-index-marker'), (2, 2, 'index-count'), (4, 2, 'index-block-size'), (6, 4, 'next-index')]:
            index_fields.append({'offset': off+rel, 'width': width, 'endian': 'little',
                                 'value': int.from_bytes(raw[off+rel:off+rel+width], 'little'),
                                 'name': name, 'owner': ident,
                                 'base_domain': 'absolute-prefix' if rel == 6 else 'index-framing-scalar',
                                 'authority': 'SDK WP7/PDF20 and unchanged approved inspector'})
        for slot in block['entries']:
            at = off + 10 * slot['slot']
            nodes.append({'id': 'slot@'+str(at), 'kind': 'active-index-entry',
                          'extent': [at, 10], 'type': slot['type'], 'payload_length': slot['length'], 'payload_offset': slot['offset']})
            for rel, width, name in [(0, 2, 'type'), (2, 4, 'payload-length'), (6, 4, 'payload-offset')]:
                index_fields.append({'offset': at+rel, 'width': width, 'endian': 'little',
                                     'value': int.from_bytes(raw[at+rel:at+rel+width], 'little'),
                                     'name': name, 'owner': 'slot@'+str(at),
                                     'base_domain': 'absolute-prefix' if rel == 6 else 'index-framing-scalar',
                                     'bounds_valid': slot['type'] == 0 or 16 <= slot['offset'] <= B-slot['length'],
                                     'semantic_status': 'unused' if slot['type'] == 0 else 'deleted-extent-only' if slot['type'] == 65535 else 'active-owner',
                                     'authority': 'SDK WP7–8/PDF20–21'})
            if slot['type'] == 65535:
                nodes.append({'id': 'deleted@'+str(at), 'kind': 'opaque-deleted-extent', 'extent': [slot['offset'], slot['length']]})
                edges.append({'source': 'slot@'+str(at), 'field_extent': [at+6, 4], 'width': 4,
                              'endian': 'little', 'base_domain': 'absolute-prefix',
                              'target': 'deleted@'+str(at), 'target_offset': slot['offset'],
                              'bounds_valid': 16 <= slot['offset'] <= B-slot['length'],
                              'authority': 'SDK WP8/PDF21 physical extent locator, NOT active semantic reference'})
            if slot['type'] not in [0, 65535]:
                edges.append({'source': 'slot@'+str(at), 'field_extent': [at+6, 4],
                              'endian': 'little', 'width': 4, 'base_domain': 'absolute-prefix',
                              'target': 'packet-'+str(slot['type']), 'target_offset': slot['offset'],
                              'bounds_valid': 16 <= slot['offset'] <= B-slot['length'],
                              'authority': 'SDK WP7–8/PDF20–21: active indexed owner'})
    edges.append({'source': previous, 'field_extent': [info['blocks'][-1]['offset']+6, 4],
                  'width': 4, 'endian': 'little', 'base_domain': 'absolute-file', 'target': None,
                  'target_offset': 0, 'bounds_valid': True, 'authority': 'SDK WP7/PDF20 terminal next=0'})
    for p in owners:
        nodes.append({'id': 'packet-'+str(p['type']), 'kind': 'active-payload', 'extent': [p['offset'], p['length']]})
    font, pool = lookup[15], lookup[7]
    ptr = int.from_bytes(raw[font['offset']+18:font['offset']+20], 'little')
    pool_valid = ptr < pool['length'] and 0 in raw[pool['offset']+ptr:pool['offset']+pool['length']]
    require(pool_valid, 'PoolReference', 'pool-local pointer/name bounds')
    edges.append({'source': 'packet-15', 'field_extent': [font['offset']+18, 2],
                  'width': 2, 'endian': 'little', 'base_domain': 'pool-local',
                  'target': 'packet-7', 'target_offset': pool['offset']+ptr,
                  'bounds_valid': True, 'authority': 'SDK WP103–105/PDF116–118'})
    afc = raw[font['offset']+50:font['offset']+86]
    require(font['length'] == 86 and all(x in [0, 254, 255] for x in afc), 'AFCReference', 'one-row AFC or documented sentinel')
    for i, v in enumerate(afc):
        edges.append({'source': 'packet-15', 'field_extent': [font['offset']+50+i, 1], 'width': 1,
                      'endian': 'single-byte', 'base_domain': 'font-row-index', 'value': v,
                      'target': 'packet-15' if v == 0 else None,
                      'target_offset': font['offset'] if v == 0 else None, 'bounds_valid': True,
                      'meaning': 'row0' if v == 0 else 'none' if v == 255 else 'unavailable',
                      'authority': 'SDK WP103–105/PDF116–118; no body pointer'})
    if info['body_grammar_refusal'] is None:
        edges.append({'source': 'body', 'field_extent': None, 'width': 0, 'endian': 'implicit',
                      'base_domain': 'font-row-index', 'target': 'packet-15',
                      'target_offset': font['offset'], 'bounds_valid': font['length'] == 86,
                      'authority': 'SDK WP103/PDF116: initial base row0 without D1/01; scoped to actual ASCII/Bold grammar'})
        for token in info['tokens']:
            if token['kind'] in ['BoldOn', 'BoldOff']:
                edges.append({'source': 'body', 'field_extent': [B+token['body_offset']+1, 1],
                              'width': 1, 'endian': 'single-byte', 'base_domain': 'attribute-index',
                              'target': 'packet-15', 'target_offset': font['offset']+50+12,
                              'bounds_valid': True, 'value': afc[12],
                              'authority': 'SDK WP105/PDF118: attribute12 indexes AFC; FF no new font, not body-position pointer'})
    # Resource/cache and scalar values are not converted into guessed byte pointers.
    for f in fs:
        if f['base_domain'] == 'resource/cache':
            edges.append({'source': f['owner'], 'field_extent': [f['offset'], f['width']],
                          'width': f['width'], 'endian': f['endian'], 'base_domain': 'resource/cache',
                          'value_hex': f['raw_hex'], 'target': 'external-pinned-resource/opaque-cache',
                          'target_offset': None, 'bounds_valid': None, 'authority': f['reference_authority'],
                          'unresolved': 'no external-resource internal-offset or cache algorithm inferred'})
    regions = importlib.import_module('resaved_prefix').regions(info)
    require(regions and regions[0]['offset'] == 0 and sum(x['length'] for x in regions) == B,
            'IntervalCoverage', 'whole prefix partition required')
    residuals = []
    for p in info['packets']:
        if p['type'] == 65535:
            residuals.append({'offset': p['offset'], 'length': p['length'], 'kind': 'deleted', 'index_offset': p['index_offset']})
    residuals += [{'offset': x['offset'], 'length': x['length'], 'kind': 'unowned'} for x in regions if not x['owners']]
    for residual in residuals:
        a, n = residual['offset'], residual['length']
        require(0 <= a <= B-n, 'ResidualBounds', 'residual prefix extent')
        residual['raw_hex'] = raw[a:a+n].hex()
        residual['sha256'] = digest(raw[a:a+n])
        residual['interpretation'] = 'opaque; no live-field authority or deadness inferred'
        residual['body_numeric_candidates'] = [
            {'offset': a+i, 'width': width, 'endian': 'little', 'value': int.from_bytes(raw[a+i:a+i+width], 'little'),
             'base_domain': 'unknown/hypothetical-absolute', 'meaning': 'raw numeric coincidence only'}
            for width in [2, 4] for i in range(max(0, n-width+1))
            if B <= int.from_bytes(raw[a+i:a+i+width], 'little') < len(raw)]
    return {'body_offset': B, 'body_hex': info['body_hex'], 'body_grammar_refusal': info['body_grammar_refusal'], 'body_tokens': info['tokens'], 'blocks': info['blocks'],
            'packets': [{k:v for k,v in p.items() if k != 'hex'} for p in info['packets']],
            'fields': fs, 'index_fields': index_fields, 'active_root_graph': {'nodes': nodes, 'edges': edges},
            'intervals': regions, 'residuals': residuals,
            'body_reference_absence_proven': False, 'mutation_permission': False}

def corpus():
    families = json.loads(git_bytes('docs/research/continuation/resaved-prefix/family-admission.json'))['families']
    result = []
    for family in families:
        for phase in family['phases']:
            require(phase['name'] in STAGES, 'StageMismatch', phase['name'])
            for repetition, witness in enumerate(phase['fresh_witnesses'], 1):
                bound = binding(witness['path'])
                require(bound['sha256'] == witness['sha256'], 'NativeIdentity', witness['path'])
                result.append({'case': family['case'], 'stage': phase['name'], 'repetition': repetition,
                               'binding': bound, 'run_manifest_sha256': family['run_manifest_sha256'],
                               'profile_plan': family['profile_plan']})
    require(len(result) == 72 and len({x['binding']['path'] for x in result}) == 72,
            'CorpusCardinality', 'six cases/six stages/two fresh witnesses')
    return result

def provenance(row, rows, raws):
    """Exhaustive substring candidates in live owners of same case/repetition.

    Max6 stages x five owners x <=90bytes; aliases/repeats are retained.
    Partial font fields are an alignment observation, never a residual type.
    """
    for residual in row['diagnostic']['residuals']:
        needle = bytes.fromhex(residual['raw_hex']); candidates = []
        for other in rows:
            if (other['case'], other['repetition']) != (row['case'], row['repetition']):
                continue
            raw = raws[other['binding']['path']]
            for p in other['diagnostic']['packets']:
                if p['type'] == 65535:
                    continue
                payload = raw[p['offset']:p['offset']+p['length']]
                for i in range(max(0, len(payload)-len(needle)+1)):
                    if payload[i:i+len(needle)] == needle:
                        overlaps = []
                        for f in other['diagnostic']['fields']:
                            start = max(p['offset']+i, f['offset']); end = min(p['offset']+i+len(needle), f['offset']+f['width'])
                            if start < end:
                                overlaps.append({'name': f['name'], 'extent': [start, end-start],
                                                 'full_live_field': start == f['offset'] and end-start == f['width']})
                        candidates.append({'path': other['binding']['path'], 'stage': other['stage'],
                                           'owner_type': p['type'], 'relative_offset': i,
                                           'absolute_offset': p['offset']+i, 'field_intersections': overlaps})
        require(len(candidates) <= MAX_MATCHES, 'ProvenanceLimit', 'at most4096 candidates per residual')
        residual['literal_provenance_candidates'] = candidates
        residual['unique_origin_proven'] = False
    # Previous stages' active index addresses are merely historical locations.
    # Record every current interval crossing them; never add them as active roots.
    old = []
    for other in rows:
        if (other['case'], other['repetition']) != (row['case'], row['repetition']) or STAGES.index(other['stage']) >= STAGES.index(row['stage']):
            continue
        for block in other['diagnostic']['blocks']:
            a = block['offset']; matches = [x for x in row['diagnostic']['intervals'] if x['offset'] < a+50 and a < x['offset']+x['length']]
            old.append({'prior_path': other['binding']['path'], 'historical_extent': [a, 50],
                        'currently_active_same_address': any(b['offset'] == a for b in row['diagnostic']['blocks']),
                        'current_intersections': matches,
                        'same50bytes': raws[other['binding']['path']][a:a+50] == raws[row['binding']['path']][a:a+50],
                        'authority': 'historical location only; current active reachability comes from root graph'})
    row['historical_index_ownership'] = old

def check():
    sources = custody()
    inherited, inspector = helpers()
    rows = corpus(); raws = {}
    for row in rows:
        path = ROOT / row['binding']['path']; raw = path.read_bytes(); raws[row['binding']['path']] = raw
        reader = inherited.actual_reader(path)
        require(reader['accepted'] and reader['exact_export'] and reader['sha256'] == digest(raw),
                'ActualReaderMismatch', row['binding']['path'])
        row['actual_go_reader'] = reader
        row['diagnostic'] = diagnose(raw, inspector)
        require(row['diagnostic']['body_offset'] == reader['inspection']['Body']['Offset'],
                'ReaderDisagreement', row['binding']['path'])
    for row in rows:
        provenance(row, rows, raws)
    residuals = [p for row in rows for p in row['diagnostic']['residuals']]
    require(len(residuals) == 126 and all(x['literal_provenance_candidates'] for x in residuals),
            'ProvenanceMismatch', '126 both-run extents/63 paired observations must be accounted')
    data = {'sources': sources, 'images': rows,
            'summary': {'images': 72, 'field_observations': 72*72,
                        'residual_extents_both_runs': len(residuals), 'paired_residual_observations': len(residuals)//2,
                        'decision': 'unresolved-read-only', 'stage2_justified': False,
                        'reason': 'permitted finite same-input success/purge observations cannot distinguish unknown hidden-reference absence; existing42 already covers repeat/X/print under its own settings',
                        'mutation_permission': False, 'body_reference_absence_proven': False,
                        'VM_launched': False, 'oracle_lock_acquired': False, 'guest_attempts': 0,
                        'full_M1_accepted': False}}
    return {'schema': SCOPE, 'data': data, 'data_sha256': digest(encode(data))}

def plan():
    sources = custody()
    return {'schema': SCOPE+'/plan', 'sources': sources, 'mode': 'offline-only',
            'stage1': 'all72 approved42 original images, actual unchanged reader and field inspectors',
            'stage2_proposed': False, 'guest_attempts_authorized': 0,
            'run_enabled': False, 'VM_configured': False, 'oracle_lock_acquired': False,
            'question': 'Can a closed564 family be justified without treating residual resemblance as reference/deadness proof?',
            'stop_condition': 'missing source/field/ownership argument leaves564 read-only; finite normal execution does not prove hidden-reference absence',
            'mutation_permission': False}

def result(path):
    with Path(path).open('rb') as stream:
        raw = stream.read(32*1024*1024+1)
    require(len(raw) <= 32*1024*1024, 'ReportLimit', 'at most32MiB JSON research report')
    try:
        value = json.loads(raw)
    except (ValueError, RecursionError) as error:
        raise Refusal('MalformedReport', str(error)) from error
    expected = check()
    require(value == expected, 'SemanticMismatch', 'recomputed immutable sources/reader/graphs/fields/provenance differ; local rehash is not evidence')
    return {'status': 'verified-unresolved-read-only', 'images': 72, 'data_sha256': expected['data_sha256'],
            'mutation_permission': False, 'stage2_justified': False, 'guest_attempts': 0}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ['check', 'plan']:
        p = sub.add_parser(name); p.add_argument('--output', type=Path)
    p = sub.add_parser('result'); p.add_argument('path', type=Path)
    sub.add_parser('run')
    args = parser.parse_args()
    try:
        if args.command == 'run':
            raise Refusal('Stage2NotJustified', 'offline handoff proposes no guest; separate reviewed plan/root grant required')
        value = check() if args.command == 'check' else plan() if args.command == 'plan' else result(args.path)
        text = json.dumps(value, sort_keys=True, indent=2)+'\n'
        if getattr(args, 'output', None):
            output = args.output.resolve()
            require(output.is_relative_to(OUT.resolve()), 'OutputScope', 'only owned research output paths; native inputs never written')
            output.parent.mkdir(parents=True, exist_ok=True)
            # Publish JSON by replacing its owned directory entry, never by
            # truncating an inode that could also be a hard-linked native input.
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=output.parent,
                                                 prefix='.wp45-json-', delete=False) as stream:
                    temporary = Path(stream.name)
                    stream.write(text)
                os.replace(temporary, output)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
        else:
            sys.stdout.write(text)
    except (Refusal, ValueError, OSError, subprocess.SubprocessError) as error:
        print(json.dumps({'status': 'refused', 'code': getattr(error, 'code', type(error).__name__),
                          'detail': str(error), 'mutation_permission': False, 'guest_attempts': 0}), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
