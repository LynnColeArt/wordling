#!/usr/bin/env python3
"""Bounded original CHR1 evidence runner and fixture-only read-only inspection.

No Wordling tokenizer/writer is implemented. VM execution is opt-in and takes
exactly the same primary-cache session1.lock used by the other reference runners.
Offline preflight/self-test/verify never start or stop a guest.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import random
import re
import shutil
import struct
import subprocess
import tempfile
import time
import tracemalloc
import unittest

import guest
import qmp
from smoke import Probe

ROOT = Path(__file__).resolve().parents[2]
PRIMARY = Path('/home/lynn/projects/wordling')
PRIVATE = Path(os.environ.get('WORDLING_REFERENCE_PRIVATE',str(PRIMARY/'research/cache/reference'))).resolve()
MASTER = PRIVATE/'master'
OUT = ROOT/'docs/research/continuation/character-identity'
PROFILE = PRIMARY/'docs/research/reference-environment/environment.json'
BASELINE = 'wp51-dos-us-1992-03-09'
MAX_FIXTURE_BYTES = 65536
MAX_FIXTURE_TOKENS = 4096


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def write(path,value):
    Path(path).write_text(json.dumps(value,indent=2)+'\n')


def configure():
    runtime=PRIVATE/'runtime'
    for module in (guest,qmp):
        module.RUNTIME=runtime
        module.SOCKET=runtime/'qmp.sock'
    guest.MASTER,guest.PROFILE=MASTER,PROFILE


@contextmanager
def exclusive():
    # Caller must have the root coordinator's VM release. Never steal a live lock.
    configure()
    with (PRIVATE/'session1.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        yield


class MalformedFixture(ValueError):
    pass


class UnsupportedFixture(ValueError):
    pass


def inspect_fixture(data):
    """Only annotate these own ASCII/C0 fixtures, not general native documents.

    Preserve raw data externally. Unknown semantics/pairs stay unqualified;
    other framed code classes receive explicit unsupported inspection.
    """
    if len(data)>MAX_FIXTURE_BYTES:
        raise UnsupportedFixture('fixture inspection size policy')
    if len(data)<16 or data[:4]!=bytes.fromhex('ff575043'):
        raise MalformedFixture('fixture header')
    start=struct.unpack_from('<I',data,4)[0]
    if not 16<=start<=len(data):
        raise MalformedFixture('fixture body offset')
    tokens=[];offset=start
    while offset<len(data):
        if len(tokens)>=MAX_FIXTURE_TOKENS:
            raise UnsupportedFixture('fixture token inspection policy')
        lead=data[offset]
        if 32<=lead<=126:
            token={'offset':offset,'length':1,'raw_hex':data[offset:offset+1].hex(),'kind':'ASCII'}
        elif lead==0xc0:
            if len(data)-offset<4 or data[offset+3]!=0xc0:
                raise MalformedFixture('truncated/mismatched C0 at '+str(offset))
            token={'offset':offset,'length':4,'raw_hex':data[offset:offset+4].hex(),
                   'kind':'native-WP-pair','character_number':data[offset+1],
                   'character_set':data[offset+2],'glyph_or_Unicode':'unqualified'}
        else:
            raise UnsupportedFixture('uninterpreted fixture token at '+str(offset))
        tokens.append(token);offset+=token['length']
    return {'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'body_offset':start,
            'body_hex':data[start:].hex(),'tokens':tokens,
            'inspection_scope':'own ASCII/C0 fixture annotation; prefix relationships/other codes not validated'}


def source_inputs():
    paths=[PRIMARY/'docs/research/reference-baseline.json',PROFILE,
           PRIMARY/'docs/research/reference-environment/resource-profile.json',
           PRIMARY/'docs/research/reference-environment/installed-files.json',
           PRIMARY/'docs/research/command-scenarios.json',
           PRIMARY/'kitty-specs/wp51-parity-01M64CVY/contracts/language-data.md',
           PRIMARY/'kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md',
           PRIMARY/'docs/compatibility.md',ROOT/'go.mod',ROOT/'go.sum']
    return [{'path':str(p),'size':p.stat().st_size,'sha256':sha(p)} for p in paths]


def preflight():
    profile=json.loads(PROFILE.read_text())
    baseline=json.loads((PRIMARY/'docs/research/reference-baseline.json').read_text())
    assert baseline['id']==BASELINE and baseline['release_date']=='1992-03-09'
    for name,key in [('harddisk.img','master_disk_sha256'),('boot.img','master_boot_sha256')]:
        if sha(MASTER/name)!=profile[key]:raise ValueError('Master identity mismatch: '+name)
    case=next(c for c in json.loads((PRIMARY/'docs/research/command-scenarios.json').read_text()) if c['id']=='CMD51-138')
    assert case['feature_ids']==['WP51-066']
    return {'baseline_id':BASELINE,'source_inputs':source_inputs(),'scenario':case,
            'master_disk_sha256':sha(MASTER/'harddisk.img'),'master_boot_sha256':sha(MASTER/'boot.img'),
            'scope':'offline fingerprints only; no VM execution','resource_profile':json.loads((PRIMARY/'docs/research/reference-environment/resource-profile.json').read_text())}


def state(p,label):
    return p.capture(label)


def save(p,name):
    p.key('f10');p.q.wait_for('Document to be saved:');state(p,'save-'+name+'-prompt')
    p.type('C:\\OUT\\'+name);p.key('ret');p.q.wait_absent('Document to be saved:')
    state(p,'saved-'+name)
    p.exports.append((name,name+'.WP5'))


def clear(p):
    p.key('f7');p.q.wait_for('Save document?');state(p,'clear-save-'+str(len(p.trace)))
    p.key('n');p.q.wait_for('Exit WP?');p.key('n')
    screen=state(p,'cleared-'+str(len(p.trace)))
    p.check('Clear returns an empty normal document',not screen.splitlines()[0].strip())


def retrieve(p):
    p.key('shift-f10');p.q.wait_for('Document to be retrieved:');state(p,'retrieve-prompt-'+str(len(p.trace)))
    p.type('C:\\OUT\\ORIGIN');p.key('ret');p.q.wait_absent('Document to be retrieved:')
    state(p,'retrieved-'+str(len(p.trace)))


def source_copy(p):
    # Incidental DOS COPY freezes bytes in the guest without inspecting a live disk.
    p.key('ctrl-f1');p.q.wait_for('DOS Command');p.key('2');p.q.wait_for('DOS Command:')
    p.type('COPY C:\\OUT\\ORIGIN C:\\OUT\\SOURCE0');p.key('ret');p.q.wait_for('Press any key')
    state(p,'source-copy');p.key('spc');p.q.wait_for('Doc 1')
    p.exports.append(('SOURCE0','SOURCE0.WP5'))


def recipe(p):
    state(p,'blank');p.type('A');save(p,'BEFORE')
    p.key('ctrl-v');state(p,'compose-prompt')
    p.type('1,36');state(p,'compose-entered')
    p.key('ret');state(p,'compose-terminated')
    p.type('B');state(p,'composed-with-sentinels');save(p,'ORIGIN');source_copy(p)
    clear(p);retrieve(p);save(p,'RETRIEV')
    clear(p);retrieve(p);p.key('home,home,home,up');state(p,'before-leading-edit')
    p.type('X');state(p,'after-leading-edit');save(p,'EDIT')
    p.key('f7');p.q.wait_for('Save document?');p.key('n');p.q.wait_for('Exit WP?');p.key('y')
    p.q.wait_for('C:\\WP51>');state(p,'clean-dos-exit')


def archive_inputs(out,pre):
    source_dir=out/'runner-source';source_dir.mkdir()
    runners=sorted((ROOT/'scripts/reference').glob('*.py'))
    entries=[]
    for path in runners:
        target=source_dir/path.name;shutil.copyfile(path,target)
        entries.append({'path':str(path.relative_to(ROOT)),'archive':str(target.relative_to(out)),'sha256':sha(path),'size':path.stat().st_size})
    for name,path in [('environment.json',PROFILE),('resource-profile.json',PRIMARY/'docs/research/reference-environment/resource-profile.json'),('baseline.json',PRIMARY/'docs/research/reference-baseline.json')]:
        shutil.copyfile(path,out/name)
    write(out/'scenario.json',pre['scenario'])
    return entries



def resource_audit(disk):
    """Read only the stopped copy; publish hashes, never resource contents."""
    profile=json.loads((PRIMARY/'docs/research/reference-environment/resource-profile.json').read_text())['resources']
    rows=[]
    for path,expected in profile.items():
        raw=subprocess.check_output(['mtype','-i',str(disk)+'@@1048576','::/'+path])
        row={'path':path,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
             'initial_size':expected['size'],'initial_sha256':expected['sha256'],
             'mutable_setup':path.endswith('.SET')}
        row['unchanged']=(row['size'],row['sha256'])==(row['initial_size'],row['initial_sha256'])
        if not row['mutable_setup'] and not row['unchanged']:
            raise ValueError('Static reference resource changed: '+path)
        rows.append(row)
    return rows


def annotate_outputs(directory):
    inspections={name:inspect_fixture((directory/name).read_bytes()) for name in ['BEFORE.WP5','ORIGIN.WP5','SOURCE0.WP5','RETRIEV.WP5','EDIT.WP5']}
    expected={'BEFORE.WP5':'41','ORIGIN.WP5':'41c02401c042','SOURCE0.WP5':'41c02401c042','RETRIEV.WP5':'41c02401c042','EDIT.WP5':'5841c02401c042'}
    for name,body in expected.items():
        if inspections[name]['body_hex']!=body:raise AssertionError('Native body expectation not observed: '+name)
    if (directory/'ORIGIN.WP5').read_bytes()!=(directory/'SOURCE0.WP5').read_bytes():
        raise AssertionError('Original source changed after retrieve/edit/new-name saves')
    return inspections


def run(run_id,allow_vm):
    if not allow_vm:raise ValueError('VM launch requires explicit --allow-vm after coordinator release')
    if not re.fullmatch(r'[A-Za-z0-9_-]+',run_id):raise ValueError('Unsafe run ID')
    pre=preflight();configure();out=OUT/'runs'/run_id;work=PRIVATE/'character-identity'/run_id
    if out.exists() or work.exists():raise FileExistsError('Existing run is immutable')
    with exclusive():
        out.mkdir(parents=True);work.mkdir(parents=True)
        run={'schema_version':1,'run_id':run_id,'started_at':datetime.now(timezone.utc).isoformat(),
             'scope':'original-reference-only','wordling_tested':False,'baseline_id':BASELINE,
             'preflight':pre,'runner_sources':archive_inputs(out,pre),
             'runtime':{'socket':str(qmp.SOCKET),'exclusive_lock':str(PRIVATE/'session1.lock')},
             'results':[]}
        result={'case_id':'CMD51-138','local_recipe':'CHR1-compose-retrieve-leading-edit','result':'error','observed_scope':'selected WP pair1,36, ordinary-document Compose/retrieve/new-name save and leading ASCII edit only'}
        p=None;started=False
        try:
            result['qemu_argv']=guest.start(work/'guest');started=True
            with qmp.QMP() as q:
                p=Probe(q,out/'CMD51-138');p.out.mkdir()
                recipe(p)
            guest.stop();started=False
            for source,name in p.exports:
                subprocess.run(['mcopy','-i',str(work/'guest/harddisk.img')+'@@1048576','::OUT/'+source,str(p.out/name)],check=True,capture_output=True)
            result['native_inspections']=annotate_outputs(p.out)
            result['stopped_copy_resource_audit']=resource_audit(work/'guest/harddisk.img')
            result['result']='observed-matches-bounded-CHR1-expectations'
        except Exception as exc:
            result['error']=str(exc)
            if started:
                try:
                    with qmp.QMP() as q:q.capture(out/'error-screen')
                except Exception:pass
        finally:
            if started:guest.stop()
            if p:result['trace'],result['checks']=p.trace,p.checks
            run['master_unchanged']=sha(MASTER/'harddisk.img')==pre['master_disk_sha256'] and sha(MASTER/'boot.img')==pre['master_boot_sha256']
            run['results'].append(result)
            run['artifacts']=[{'path':str(f.relative_to(out)),'size':f.stat().st_size,'sha256':sha(f)} for f in sorted(out.rglob('*')) if f.is_file()]
            run['finished_at']=datetime.now(timezone.utc).isoformat();write(out/'run.json',run)
        print(run_id,result['result'],result.get('error',''),flush=True)
        if result['result']=='error' or not run['master_unchanged']:raise SystemExit(1)


def verify(prefix):
    if not re.fullmatch(r'[A-Za-z0-9_-]+',prefix):raise ValueError('Unsafe evidence prefix')
    manifests=sorted((OUT/'runs').glob(prefix+'*/run.json'))
    if len(manifests)!=2:raise ValueError('Exactly two named fresh accepted repetitions required')
    native=[]
    for path in manifests:
        run=json.loads(path.read_text());out=path.parent
        if run['scope']!='original-reference-only' or run['wordling_tested'] or not run['master_unchanged']:raise ValueError('Wrong scope/source changed')
        result=run['results'][0]
        scenario=json.loads((out/'scenario.json').read_text())
        if scenario['id']!='CMD51-138' or scenario['feature_ids']!=['WP51-066']:
            raise ValueError('Wrong Compose case/feature association')
        if result['case_id']!='CMD51-138' or result['result']!='observed-matches-bounded-CHR1-expectations' or not result['checks'] or not all(c['passed'] for c in result['checks']):raise ValueError('Unaccepted reference run')
        for artifact in run['artifacts']:
            f=out/artifact['path']
            if not f.is_relative_to(out) or not f.is_file() or f.stat().st_size!=artifact['size'] or sha(f)!=artifact['sha256']:raise ValueError('Changed artifact '+str(f))
        for source in run['runner_sources']:
            f=out/source['archive']
            if sha(f)!=source['sha256'] or f.stat().st_size!=source['size']:raise ValueError('Changed runner source')
        resource_rows=result['stopped_copy_resource_audit']
        if not resource_rows or any(not r['unchanged'] for r in resource_rows if not r['mutable_setup']):raise ValueError('Changed static resource')
        actual=annotate_outputs(out/'CMD51-138')
        if actual!=result['native_inspections']:raise ValueError('Changed native annotation')
        captures=out/'CMD51-138'
        for label,cue in [('compose-prompt','Key ='),('compose-entered','Key = 1,36')]:
            if (captures/label/'screen.txt').read_text().splitlines()[-1]!=cue:
                raise ValueError('Changed Compose prompt/entry')
        if 'Key =' in (captures/'compose-terminated/screen.txt').read_text():
            raise ValueError('Compose did not terminate')
        if 'C:\\WP51>' not in (captures/'clean-dos-exit/screen.txt').read_text():
            raise ValueError('Missing clean DOS exit witness')
        native.append({name:x['body_hex'] for name,x in actual.items()})
    if native[0]!=native[1]:raise ValueError('Fresh-repetition native-body disagreement')
    return {'scope':'original-only two-fresh-copy CHR1; no Wordling/Unicode/glyph/print acceptance','runs':[str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p) for p in manifests],'body_equal':True,'native_bodies':native[0]}


def verify_negative(prefix):
    """Mutate temporary evidence copies; never edit the original captures."""
    global OUT
    original=OUT
    verify(prefix)
    checks=[]
    with tempfile.TemporaryDirectory(prefix='wordling-chr1-negative-') as temporary:
        copied=Path(temporary)/'evidence';shutil.copytree(OUT/'runs',copied/'runs')
        OUT=copied
        try:
            verify(prefix)
            manifests=sorted((OUT/'runs').glob(prefix+'*/run.json'))
            path=manifests[0];raw=path.read_bytes();manifest=json.loads(raw)
            mutations=[('wrong-case',lambda r:r['results'][0].update(case_id='CMD51-001')),
                       ('false-original-status',lambda r:r['results'][0].update(result='not-run')),
                       ('changed-native-annotation',lambda r:r['results'][0]['native_inspections']['ORIGIN.WP5'].update(body_hex='41'))]
            for name,mutate in mutations:
                value=json.loads(raw);mutate(value);write(path,value)
                try:verify(prefix)
                except (ValueError,AssertionError):checks.append(name)
                else:raise AssertionError('Verifier accepted mutation '+name)
                finally:path.write_bytes(raw)
            artifact=path.parent/'CMD51-138/ORIGIN.WP5';saved=artifact.read_bytes()
            artifact.write_bytes(saved[:-1]+b'X')
            try:verify(prefix)
            except (ValueError,AssertionError):checks.append('tampered-native-bytes')
            else:raise AssertionError('Verifier accepted changed native bytes')
            finally:artifact.write_bytes(saved)
        finally:OUT=original
    return {'temporary_copy_only':True,'rejected_mutations':checks,'originals_still_valid':bool(verify(prefix))}


class InspectorTests(unittest.TestCase):
    @staticmethod
    def data(body):return bytes.fromhex('ff57504310000000010a000100000000')+body
    def test_original_existing_ascii_fixture(self):
        path=ROOT/'docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5'
        self.assertEqual(sha(path),'a42b87e3441dc422c5a348e5b6838e5949a3dabedddf49e947f784408db0dff6')
        self.assertEqual(inspect_fixture(path.read_bytes())['body_hex'],b'WORDLING TEST'.hex())
    def test_pair_identity_and_undefined_semantics(self):
        for pair in [bytes([0xc0,36,1,0xc0]),bytes([0xc0,255,255,0xc0])]:
            data=self.data(b'A'+pair+b'B');out=inspect_fixture(data)
            self.assertEqual(out['tokens'][1]['raw_hex'],pair.hex());self.assertEqual(out['tokens'][1]['character_number'],pair[1]);self.assertEqual(out['tokens'][1]['character_set'],pair[2]);self.assertEqual(out['tokens'][1]['glyph_or_Unicode'],'unqualified')
            self.assertEqual(b''.join(bytes.fromhex(t['raw_hex']) for t in out['tokens']),data[16:])
    def test_truncation_mismatch_and_unsupported_are_distinct(self):
        for body in [b'\xc0',b'\xc0\x24',b'\xc0\x24\x01',b'\xc0\x24\x01\xc3']:
            with self.assertRaises(MalformedFixture):inspect_fixture(self.data(body))
        for body in [b'\x80',b'\xc3\x0c\xc3']:
            with self.assertRaises(UnsupportedFixture):inspect_fixture(self.data(body))
        with self.assertRaises(UnsupportedFixture):inspect_fixture(self.data(b'x'*(MAX_FIXTURE_TOKENS+1)))
        with self.assertRaises(UnsupportedFixture):inspect_fixture(bytes(MAX_FIXTURE_BYTES+1))
        self.assertEqual(len(inspect_fixture(self.data(b'x'*MAX_FIXTURE_TOKENS))['tokens']),MAX_FIXTURE_TOKENS)
    def test_deterministic_bounded_mutation_inspection(self):
        rng=random.Random(22)
        for unused in range(20000):
            body=rng.randbytes(rng.randrange(65));data=self.data(body)
            try:out=inspect_fixture(data)
            except (MalformedFixture,UnsupportedFixture):continue
            self.assertEqual(out['body_hex'],body.hex())
            self.assertEqual(b''.join(bytes.fromhex(t['raw_hex']) for t in out['tokens']),body)


def self_test():
    started=time.monotonic();suite=unittest.defaultTestLoader.loadTestsFromTestCase(InspectorTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    tracemalloc.start();sample=InspectorTests.data(b'x'*MAX_FIXTURE_TOKENS);inspect_fixture(sample);current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    report={'test_count':result.testsRun,'passed':result.wasSuccessful(),'seconds':time.monotonic()-started,
            'deterministic_random_cases':20000,'fixture_policy_bytes':MAX_FIXTURE_BYTES,'fixture_token_policy':MAX_FIXTURE_TOKENS,
            'max_token_fixture_tracemalloc_peak_bytes':peak,'limits':'Python fixture-only inspector overhead, not Go tokenizer or product budget; synthetic pairs do not establish original observations'}
    print(json.dumps(report,indent=2))
    if not result.wasSuccessful():raise SystemExit(1)


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('self-test');sub.add_parser('preflight')
    p=sub.add_parser('run');p.add_argument('run_id');p.add_argument('--allow-vm',action='store_true')
    p=sub.add_parser('verify');p.add_argument('prefix')
    p=sub.add_parser('verify-negative');p.add_argument('prefix')
    args=parser.parse_args()
    if args.command=='self-test':self_test()
    elif args.command=='preflight':print(json.dumps(preflight(),indent=2))
    elif args.command=='run':run(args.run_id,args.allow_vm)
    elif args.command=='verify':print(json.dumps(verify(args.prefix),indent=2))
    else:print(json.dumps(verify_negative(args.prefix),indent=2))


if __name__=='__main__':main()
