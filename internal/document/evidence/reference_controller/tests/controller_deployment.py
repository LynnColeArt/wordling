"""Finite trusted offline build/install; runtime modules load only from normal wheels."""
import hashlib
import base64
import csv
import io
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import time
import zipfile
from runtime_qualification import (BASE, Preparation, load_expected, pin, preflight,
    strict_layout, compare_observation, probe, rights, bounded_json_loads, qualification_literal, _actual_cold_r11)

from runtime_qualification import E_FILES, PROVIDERS, SOURCE_NAMES
MASTER=b'Wordling5.2 TEST master bytes\n'*1024


def static_elf(path):
    raw=path.read_bytes()
    assert raw[:6]==b'\x7fELF\x02\x01','expected native64bit little-endian ELF'
    offset=struct.unpack_from('<Q',raw,32)[0]
    size,count=struct.unpack_from('<HH',raw,54)
    assert count<=64 and offset+size*count<=len(raw)
    assert all(struct.unpack_from('<I',raw,offset+i*size)[0]!=3 for i in range(count)), 'dynamic interpreter not allowed'


def _campaign_review_wheel(wheel,expected_payloads,context):
    """Bounded wheel-copy frame; every binary/CSV/ZipInfo dies on return."""
    if len(expected_payloads)!=22:raise RuntimeError('CampaignPayloadCardinality')
    context.guard_wheel(wheel)
    dist='wordling_reference_controller_test-0.2.0.dist-info'
    metadata={dist+'/'+n for n in ('METADATA','WHEEL','top_level.txt','RECORD')}
    with zipfile.ZipFile(wheel) as z:
        names=z.namelist()
        if len(names)>32 or len(names)!=len(set(names)) or set(names)!=set(expected_payloads)|metadata:raise RuntimeError('WheelClosedMemberSet')
        for info in z.infolist():context.guard_wheel_member(info,record=info.filename==dist+'/RECORD')
        for name,(source,wanted) in expected_payloads.items():
            if pin(source)!=wanted or z.getinfo(name).file_size!=wanted['size']:raise RuntimeError('WheelReviewedPayload:'+name)
            with source.open('rb') as original,z.open(name) as member:
                while True:
                    left=original.read(16384);right=member.read(16384)
                    if left!=right:raise RuntimeError('WheelReviewedPayload:'+name)
                    if not left:break
            if pin(source)!=wanted:raise RuntimeError('WheelReviewedPayloadChanged:'+name)
        # Bounded reads avoid ZipExtFile.read(-1)'s compressed/output join
        # copies. The metadata membership checks preserve the original bytes.
        meta=bytearray()
        with z.open(dist+'/METADATA') as member:
            while True:
                part=member.read(16384)
                if not part:break
                if len(meta)+len(part)>1048576:raise RuntimeError('CampaignWheelMetadataBound')
                meta.extend(part)
        if b'Name: wordling-reference-controller-test\n' not in meta or b'Version: 0.2.0\n' not in meta or b'Requires-Python: >=3.12\n' not in meta:raise RuntimeError('WheelProjectMetadata')
        del meta,part
        record_raw=z.read(dist+'/RECORD')  # Member was bounded64KiB BEFORE read.
        rows=[]
        with io.StringIO(record_raw.decode('utf8')) as record:
            for row in csv.reader(record):
                if len(rows)>=32 or len(row)!=3 or any(len(field)>512 for field in row):raise RuntimeError('CampaignWheelRecordBound')
                rows.append(row)
        del record_raw
        if len(rows)!=len(names) or {r[0] for r in rows}!=set(names):raise RuntimeError('WheelRecordSet')
        for name,digest,size in rows:
            if name==dist+'/RECORD':
                if digest or size:raise RuntimeError('WheelRecordSelf')
            else:
                h=hashlib.sha256();count=0
                with z.open(name) as member:
                    while True:
                        part=member.read(16384)
                        if not part:break
                        count+=len(part)
                        if count>1048576:raise RuntimeError('CampaignWheelMemberBound')
                        h.update(part)
                wanted='sha256='+base64.urlsafe_b64encode(h.digest()).rstrip(b'=').decode('ascii')
                if digest!=wanted or size!=str(count):raise RuntimeError('WheelRecordBinding')


def _campaign_review_installed_wheel(wheel,site,context):
    """All installed-wheel buffers and decoder-independent rows stay here."""
    context.guard_wheel(wheel)
    with zipfile.ZipFile(wheel) as z:
        names=z.namelist()
        if len(names)>32 or len(names)!=len(set(names)) or any(n.startswith('/') or '..' in Path(n).parts for n in names):raise RuntimeError('WheelMembers')
        for info in z.infolist():context.guard_wheel_member(info,record=info.filename.endswith('/RECORD'))
        metadata={n.split('/')[0] for n in names if '.dist-info/' in n}
        if len(metadata)!=1:raise RuntimeError('WheelMetadata')
        dist=metadata.pop()
        if dist!='wordling_reference_controller_test-0.2.0.dist-info':raise RuntimeError('WheelDistribution')
        allowed=set(SOURCE_NAMES)|{'reference_controller/testdata/fixture','reference_controller/testdata/master.bin'}|{dist+'/'+n for n in ('METADATA','WHEEL','top_level.txt','RECORD','LICENSE')}
        if len(allowed)>32 or not set(names)<=allowed or not set(SOURCE_NAMES)<=set(names):raise RuntimeError('WheelClosedSet')
        for name in names:
            if name.endswith('/RECORD'):continue
            with (site/name).open('rb') as original,z.open(name) as member:
                while True:
                    left=original.read(16384);right=member.read(16384)
                    if left!=right:raise RuntimeError('InstalledWheelMember:'+name)
                    if not left:break
        extras={dist+'/'+n for n in ('INSTALLER','REQUESTED','direct_url.json')}
        actual=set()
        for p in site.rglob('*'):
            if p.is_file():
                relative=str(p.relative_to(site))
                if len(actual)>=32 or len(relative)>256 or not relative.isascii():raise RuntimeError('CampaignInstalledNamesBound')
                actual.add(relative)
        if actual!=set(names)|extras:raise RuntimeError('InstalledClosedSet')
        for filename,expected in (('INSTALLER',b'pip\n'),('REQUESTED',b'')):
            with (site/dist/filename).open('rb') as stream:raw=stream.read(len(expected)+1)
            if raw!=expected:raise RuntimeError('InstallerMetadata')
        record_path=site/dist/'RECORD'
        if record_path.is_symlink() or record_path.stat().st_size>65536:raise RuntimeError('CampaignInstalledRecordByteBound')
        with record_path.open('rb') as stream:raw=stream.read(65537)
        if len(raw)>65536:raise RuntimeError('CampaignInstalledRecordByteBound')
        seen=set()
        with io.StringIO(raw.decode('utf8'),newline='') as record:
            for row in csv.reader(record):
                if len(seen)>=32 or len(row)!=3 or any(len(field)>512 for field in row):raise RuntimeError('CampaignInstalledRecordBound')
                name,digest_field,size_field=row
                if name in seen or name not in actual:raise RuntimeError('InstalledRecordSet')
                seen.add(name)
                if name==dist+'/RECORD':
                    if digest_field or size_field:raise RuntimeError('RecordSelf')
                else:
                    value=pin(site/name)
                    wanted='sha256='+base64.urlsafe_b64encode(bytes.fromhex(value['sha256'])).rstrip(b'=').decode('ascii')
                    if digest_field!=wanted or size_field!=str(value['size']):raise RuntimeError('InstalledRecordBinding')
        if seen!=actual:raise RuntimeError('InstalledRecordSet')


def _campaign_inventory_paths(environment,observation,context):
    """Copy bounded observed path strings; no decoded-tree borrow escapes."""
    paths=set()
    for p in environment.rglob('*'):
        if p.is_file():context.add_inventory_path(paths,p)
    for fields in observation['modules'].values():
        for value in fields.values():
            if value['exists']:
                text=value['path']
                if type(text) is not str or len(text)>512 or not text.isascii():raise RuntimeError('CampaignObservedPathBound')
                context.add_inventory_path(paths,Path(text.encode('ascii').decode('ascii')))
    for text in observation['maps']:
        if type(text) is not str or len(text)>512 or not text.isascii():raise RuntimeError('CampaignObservedPathBound')
        context.add_inventory_path(paths,Path(text.encode('ascii').decode('ascii')))
    if len(paths)!=188:raise RuntimeError('CampaignExact188Inventory')
    return paths


def review_wheel(wheel,expected_payloads,context=None):
    """DATA validation only. Caller freezes reviewed source + compiled fixture
    and source-defined MASTER BEFORE wheel construction. Never adopt wheel data.
    """
    if context is not None and (getattr(context,'campaign',None) is not None or getattr(context,'qualification',None) is not None):
        return _campaign_review_wheel(wheel,expected_payloads,context)
    dist='wordling_reference_controller_test-0.2.0.dist-info'
    metadata={dist+'/'+n for n in ('METADATA','WHEEL','top_level.txt','RECORD')}
    with zipfile.ZipFile(wheel) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or set(names)!=set(expected_payloads)|metadata:raise RuntimeError('WheelClosedMemberSet')
        for name,(source,wanted) in expected_payloads.items():
            if pin(source)!=wanted or z.getinfo(name).file_size!=wanted['size']:raise RuntimeError('WheelReviewedPayload:'+name)
            with source.open('rb') as original,z.open(name) as member:
                while True:
                    left=original.read(16384);right=member.read(16384)
                    if left!=right:raise RuntimeError('WheelReviewedPayload:'+name)
                    if not left:break
            if pin(source)!=wanted:raise RuntimeError('WheelReviewedPayloadChanged:'+name)
        meta=z.read(dist+'/METADATA')
        if b'Name: wordling-reference-controller-test\n' not in meta or b'Version: 0.2.0\n' not in meta or b'Requires-Python: >=3.12\n' not in meta:raise RuntimeError('WheelProjectMetadata')
        rows=list(csv.reader(io.StringIO(z.read(dist+'/RECORD').decode('utf-8'))))
        if len(rows)!=len(names) or {r[0] for r in rows}!=set(names):raise RuntimeError('WheelRecordSet')
        for name,digest,size in rows:
            if name==dist+'/RECORD':
                if digest or size:raise RuntimeError('WheelRecordSelf')
            else:
                raw=z.read(name);wanted='sha256='+base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).rstrip(b'=').decode('ascii')
                if digest!=wanted or size!=str(len(raw)):raise RuntimeError('WheelRecordBinding')
    return {name:wanted for name,(_,wanted) in expected_payloads.items()}


def deploy(source,repository,target,evidence,context=None):
    if context is None:
        from deployment import remaining
        context=Preparation(target,evidence,load_expected(),earlier_end=time.monotonic()+remaining())
    elif context.target != target:
        raise RuntimeError("PreparationTargetMismatch")
    campaign=getattr(context,'campaign',None) or getattr(context,'qualification',None)
    if campaign is not None:
        qualification=getattr(context,'qualification',None)
        wanted_evidence=context.evidence/'deployment' if qualification is not None else context.evidence
        if qualification is not None:
            if type(context)is not Preparation or not _actual_cold_r11(qualification):raise RuntimeError('R14GenuineColdPreparation')
            qualification.check(context)
        if source!=context.source or repository!=context.repository or evidence!=wanted_evidence:
            raise RuntimeError('CampaignPreparationSourceBinding')
    def source_pin(path):
        # The actual producer derives the variant's sole approved postimage
        # from immutable originals. Copied/mutated bytes never become expected.
        if campaign is not None:return context.source_pin(path)
        return {k:context.expected['files'][str(path)][k] for k in ('size','sha256')}
    evidence.mkdir(parents=True,exist_ok=True)
    def run(argv,cwd,log,tool=False):
        if cwd != target:raise RuntimeError("PreparationCwd")
        return context.run(argv,str(log.relative_to(context.evidence)),tool=tool)
    environment=target/"venv"
    run([str(BASE),"-I","-B","-m","venv","--copies","--without-pip",str(environment)],target,evidence/"venv",tool=True)
    interpreter=environment/"bin/python"
    strict_layout(interpreter)
    run([str(interpreter),'-I','-B','-c',context.qualification_literal()],target,evidence/'qualify-literal-before')
    r=run([str(interpreter),"-I","-B","-c",probe(False)],target,evidence/"stdlib-before")
    before=context.decode_metadata(r.stdout,'stdlib-before',65536) if campaign is not None else bounded_json_loads(r.stdout)
    compare_observation(before,interpreter,context.expected,{},False)
    if campaign is not None:
        for key in ('version_string','base_prefix'):
            if type(before[key]) is not str or len(before[key])>512 or len(before[key].encode('utf8'))>512:raise RuntimeError('CampaignPythonProjectionBound')
        # Independent bounded strings, rather than references into the decoded
        # observation whose lease ends before the direct-map phase begins.
        python=dict(version=before['version_string'].encode('utf8').decode('utf8'),base_prefix=before['base_prefix'].encode('utf8').decode('utf8'))
    else:python=dict(version=before['version_string'],base_prefix=before['base_prefix'])
    del before,r
    if campaign is not None:
        context.release_metadata('stdlib-before')
        context.begin_metadata_maps()
    build=target/'build-input';build.mkdir()
    frozen={}
    for name in E_FILES:
        if campaign is not None and len(frozen)>=20:raise RuntimeError('CampaignFrozenSourceCardinality')
        p=build/'reference_controller'/name;p.parent.mkdir(exist_ok=True);p.write_bytes((source/name).read_bytes())
        frozen['reference_controller/'+name]=pin(p)
        if frozen['reference_controller/'+name] != source_pin(source/name):raise RuntimeError('OwnedSourceDrift:'+name)
        context.check()
    for name,(rel,commit) in context.provider_rows().items():
        if campaign is not None and len(frozen)>=20:raise RuntimeError('CampaignFrozenSourceCardinality')
        raw=(repository/rel).read_bytes()
        # Exact immutable approved Git blob/hash provenance is bound in the
        # reviewed expected manifest; no unbounded Git subprocess during prep.
        if context.expected['approved_providers'].get(rel)!=commit:raise RuntimeError('ApprovedProviderPin')
        p=build/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        frozen[name]=dict(**pin(p),original_path=rel,approved_commit=commit)
        if pin(p)!={k:context.expected['files'][str(repository/rel)][k] for k in ('size','sha256')}:raise RuntimeError('ProviderInputDrift')
        context.check()
    if campaign is not None:
        if len(frozen)!=20:raise RuntimeError('CampaignFrozenSourceCardinality')
        del raw
    for original in (source/'pyproject.toml',source/'tests/harmless_fixture.c',source/'tests/controller_roster.json'):
        if pin(original)!=source_pin(original):raise RuntimeError('StagingInputDrift')
    (build/'pyproject.toml').write_bytes((source/'pyproject.toml').read_bytes())
    fixture_source=build/'fixture.c';fixture_source.write_bytes((source/'tests/harmless_fixture.c').read_bytes())
    data=build/'reference_controller/testdata';data.mkdir()
    (data/'master.bin').write_bytes(MASTER)
    argv=['/usr/bin/cc','-std=c11','-O2','-static','-Wall','-Wextra','-Werror','-o',str(data/'fixture'),str(fixture_source)]
    context.budget.document(evidence/'build-freeze.json',dict(code_sources=frozen,
        pyproject=pin(build/'pyproject.toml'),fixture_source=pin(fixture_source),compile_argv=argv,
        cc=pin(Path('/usr/bin/cc').resolve()),master=pin(data/'master.bin'),cwd=str(target),
        limits=dict(command_seconds=30,cleanup_seconds=2,shared_preparation_seconds=120,combined_output=context.output_cap,created_files=10000,created_bytes=536870912)))
    r=run(argv,target,evidence/'compile',tool=True)
    if r.returncode:raise RuntimeError('fixture compile failed; raw preserved')
    del r
    if campaign is not None and (data/'fixture').stat().st_size>1048576:raise RuntimeError('fixed fixture binary bound exceeded')
    if campaign is not None:context.begin_wheel_copy('fixture-elf')
    static_elf(data/'fixture')
    if campaign is not None:context.end_wheel_copy('fixture-elf')
    if (data/'fixture').stat().st_size>1048576:raise RuntimeError('fixed fixture binary bound exceeded')
    if (data/'master.bin').read_bytes()!=MASTER:raise RuntimeError('SourceMasterChanged')
    # Freeze custody BEFORE wheel creation; installed observations never become expected data.
    if campaign is not None and len(SOURCE_NAMES)!=20:raise RuntimeError('CampaignCode20Cardinality')
    expected_payloads={name:(build/name,pin(build/name)) for name in SOURCE_NAMES}
    expected_payloads.update({'reference_controller/testdata/'+n:(data/n,pin(data/n)) for n in ('fixture','master.bin')})
    expected_data={n:expected_payloads['reference_controller/testdata/'+n][1] for n in ('fixture','master.bin')}
    context.budget.document(evidence/'compiled-data-before-wheel.json',expected_data)
    wheels=target/'wheels';wheels.mkdir()
    r=run(['/usr/bin/python','-B','-m','pip','wheel','--no-deps','--no-index','--no-build-isolation','--no-cache-dir','--config-settings=--build-option=--keep-temp',
           '--wheel-dir',str(wheels),str(build)],target,evidence/'wheel',tool=True)
    if r.returncode:raise RuntimeError('normal offline wheel failed')
    del r
    wheel,=wheels.glob('*.whl')
    if wheel.name!='wordling_reference_controller_test-0.2.0-py3-none-any.whl':raise RuntimeError('ExactWheelFilename')
    if campaign is not None:context.begin_wheel_copy('review-wheel')
    review_wheel(wheel,expected_payloads,context=context)
    if campaign is not None:context.end_wheel_copy('review-wheel')
    del expected_payloads
    prior_env=context.env
    context.env={**prior_env,'PYTHONUSERBASE':str(environment)}
    try:
        r=run(['/usr/bin/python','-s','-B','-m','pip','install','--user','--root=/','--ignore-installed','--no-index',
               '--no-deps','--no-compile','--no-cache-dir',str(wheel)],target,evidence/'install',tool=True)
    finally:
        context.env=prior_env
    if r.returncode:raise RuntimeError('normal offline install failed')
    del r
    strict_layout(interpreter)
    run([str(interpreter),'-I','-B','-c',context.qualification_literal()],target,evidence/'qualify-literal-after')
    site=environment/'lib/python3.12/site-packages'
    code={};digest=hashlib.sha256()
    for name in SOURCE_NAMES:
        if campaign is not None and len(code)>=20:raise RuntimeError('CampaignInstalledCode20Cardinality')
        p=site/name;code[name]=pin(p)
        if p.read_bytes()!=(build/name).read_bytes():raise RuntimeError('installed source mismatch '+name)
        digest.update(name.encode('ascii')+b'\0'+bytes.fromhex(code[name]['sha256']))
    data_pins=expected_data
    for name,wanted in expected_data.items():
        if pin(site/'reference_controller/testdata'/name)!=wanted:raise RuntimeError('InstalledReviewedData:'+name)
    manifest=dict(schema='wordling.test-controller-deployment/v1',files=code,data=data_pins,
        source_hash=digest.hexdigest(),plan_hash=hashlib.sha256((source/'tests/controller_roster.json').read_bytes()).hexdigest(),
        executable=str(interpreter),**python)
    context.payload_document(environment/'wordling-test-deployment.json',manifest)
    # Compare every installed wheel member and exact derived installer metadata;
    # no discovered foreign distribution becomes an admitted source.
    if campaign is not None:
        context.begin_wheel_copy('installed-wheel')
        _campaign_review_installed_wheel(wheel,site,context)
        # Helper frame has returned: ZipFile, ZipInfo, member buffers, CSV
        # readers/rows and all their borrowed fields are dead before release.
        context.end_wheel_copy('installed-wheel')
        direct_path=site/'wordling_reference_controller_test-0.2.0.dist-info/direct_url.json'
        if direct_path.is_symlink() or direct_path.stat().st_size>8192:raise RuntimeError('CampaignDirectURLByteBound')
        with direct_path.open('rb') as stream:direct_raw=stream.read(8193)
        del stream
        if len(direct_raw)>8192:raise RuntimeError('CampaignDirectURLByteBound')
        direct=context.decode_metadata(direct_raw,'direct-url',8192)
        if direct.get('url')!=wheel.as_uri() or direct.get('archive_info',{}).get('hashes',{}).get('sha256')!=pin(wheel)['sha256']:raise RuntimeError('WheelDirectURL')
        del direct,direct_raw
        context.release_metadata('direct-url')
    else:
        with zipfile.ZipFile(wheel) as z:
            names=z.namelist()
            if len(names)!=len(set(names)) or any(n.startswith('/') or '..' in Path(n).parts for n in names):raise RuntimeError('WheelMembers')
            metadata={n.split('/')[0] for n in names if '.dist-info/' in n}
            if len(metadata)!=1:raise RuntimeError('WheelMetadata')
            dist=metadata.pop()
            if dist!='wordling_reference_controller_test-0.2.0.dist-info':raise RuntimeError('WheelDistribution')
            allowed=set(SOURCE_NAMES)|{'reference_controller/testdata/fixture','reference_controller/testdata/master.bin'}|{dist+'/'+n for n in ('METADATA','WHEEL','top_level.txt','RECORD','LICENSE')}
            if not set(names)<=allowed or not set(SOURCE_NAMES)<=set(names):raise RuntimeError('WheelClosedSet')
            for name in names:
                if not name.endswith('/RECORD') and (site/name).read_bytes()!=z.read(name):raise RuntimeError('InstalledWheelMember:'+name)
            extras={dist+'/'+n for n in ('INSTALLER','REQUESTED','direct_url.json')}
            actual={str(p.relative_to(site)) for p in site.rglob('*') if p.is_file()}
            if actual!=set(names)|extras:raise RuntimeError('InstalledClosedSet')
            if (site/dist/'INSTALLER').read_bytes()!=b'pip\n' or (site/dist/'REQUESTED').read_bytes()!=b'':raise RuntimeError('InstallerMetadata')
            seen=set()
            with (site/dist/'RECORD').open(newline='') as record:
              for row in csv.reader(record):
                if len(row)!=3:raise RuntimeError('InstalledRecordShape')
                name,digest_field,size_field=row
                if name in seen or name not in actual:raise RuntimeError('InstalledRecordSet')
                seen.add(name)
                if name==dist+'/RECORD':
                    if digest_field or size_field:raise RuntimeError('RecordSelf')
                else:
                    value=pin(site/name)
                    wanted='sha256='+base64.urlsafe_b64encode(bytes.fromhex(value['sha256'])).rstrip(b'=').decode('ascii')
                    if digest_field!=wanted or size_field!=str(value['size']):raise RuntimeError('InstalledRecordBinding')
            if seen!=actual:raise RuntimeError('InstalledRecordSet')
            direct=bounded_json_loads((site/dist/'direct_url.json').read_text())
            if direct.get('url')!=wheel.as_uri() or direct.get('archive_info',{}).get('hashes',{}).get('sha256')!=pin(wheel)['sha256']:raise RuntimeError('WheelDirectURL')
    del frozen
    installed={str(site/name):dict(**pin(site/name),**rights(site/name)) for name in SOURCE_NAMES}
    if campaign is not None and (len(installed)!=20 or len(expected_data)!=2):raise RuntimeError('CampaignInstalledPayloadCardinality')
    installed.update({str(site/'reference_controller/testdata'/n):dict(**pin(site/'reference_controller/testdata'/n),**rights(site/'reference_controller/testdata'/n)) for n in ('fixture','master.bin')})
    r=run([str(interpreter),'-I','-B','-c',probe(True)],target,evidence/'origins')
    observation=context.decode_metadata(r.stdout,'origins',65536) if campaign is not None else bounded_json_loads(r.stdout)
    del r
    compare_observation(observation,interpreter,context.expected,installed,True)
    # Complete venv inventory is admitted only AFTER exact normal config,
    # aliases, wheel members and source-specific observations have passed.
    if campaign is not None:paths=_campaign_inventory_paths(environment,observation,context)
    else:
        paths={p for p in environment.rglob('*') if p.is_file()}
        paths.update(Path(x['path']) for fields in observation['modules'].values() for x in fields.values() if x['exists'])
        paths.update(Path(n) for n in observation['maps'])
        if len(paths)>1024:raise RuntimeError('DeploymentInventoryCardinality')
    inventory={str(p):dict(**pin(p),**rights(p)) for p in sorted(paths)}
    context.budget.document(evidence/'deployment-inventory.json',inventory)
    context.budget.document(evidence/'deployment.json',dict(wheel=str(wheel),wheel_pin=pin(wheel),
        interpreter=str(interpreter),interpreter_pin=pin(interpreter),source_hash=manifest['source_hash'],
        static_fixture=pin(data/'fixture'),master=data_pins['master.bin'],actual_provider=observation['project']['provider'],
        actual_classes=observation['project']['classes'],cwd=str(target),premise='Trusted exclusive immutable-for-invocation local deployment; actual complete preflight before every launch, not a hostile-owner sandbox'))
    if campaign is not None:
        # Path strings were independently copied by the returned helper frame;
        # no fields/x/ZipInfo/CSV variable in this frame borrows this JSON tree.
        del observation
        context.release_metadata('origins')
    preflight(interpreter,inventory)
    if campaign is None or getattr(context,'qualification',None)is not None:context.preflight_inputs()
    context.check()
    return interpreter,inventory
