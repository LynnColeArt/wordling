"""Finite offline ordinary-wheel preparation; never issues a ROOT decision."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[5]
SOURCE = Path(__file__).resolve().parents[1]
E_NAMES = ('__init__.py', '__main__.py', 'bootstrap.py', 'errors.py', 'account.py',
           'ownership.py', 'records.py', 'issuance.py', 'cli.py', 'controller.py',
           'protocol.py', 'publisher.py')
ORIGINAL_NAMES = E_NAMES + ('original.py', 'original_release.py', 'original_control_admin.py')
BASE = Path('/usr/bin/python3.12')
P_NAMES = ('__init__.py', 'artifacts.py', 'engine.py', 'lifetime.py')


def pin(path):
    raw = path.read_bytes()
    return dict(size=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def command(argv, cwd, end, log):
    left = min(30, end - time.monotonic())
    if left <= 0:
        raise RuntimeError('PreparationDeadline')
    env = dict(PATH='/usr/bin:/bin', HOME=str(cwd), LANG='C.UTF-8',
               LC_ALL='C.UTF-8', PYTHONDONTWRITEBYTECODE='1',
               PIP_DISABLE_PIP_VERSION_CHECK='1')
    result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=left)
    if len(result.stdout) + len(result.stderr) > 2097152:
        raise RuntimeError('PreparationOutputBound')
    log.with_suffix('.stdout').write_bytes(result.stdout)
    log.with_suffix('.stderr').write_bytes(result.stderr)
    log.with_suffix('.json').write_text(json.dumps(dict(argv=argv, returncode=result.returncode))+'\n')
    if result.returncode:
        raise RuntimeError('PreparationFailed:'+str(log))
    return result


def deploy(target):
    """Build/install the separate exact source-owned original ordinary wheel.

    This freezes only DATA. No ROOT coordinator, administrator or leaf is run.
    The emitted review bundle has no review refs and is deliberately unreleasable.
    """
    end = time.monotonic() + 90
    target.mkdir(mode=0o700)
    stage = target/'stage'
    stage.mkdir()
    package = stage/'reference_controller'
    package.mkdir()
    for name in ORIGINAL_NAMES:
        source = SOURCE/'tests'/name if name == 'original_control_admin.py' else SOURCE/name
        shutil.copyfile(source, package/name)
    family = stage/'startup_family'
    family.mkdir()
    for name in P_NAMES:
        shutil.copyfile(ROOT/'scripts/reference/startup_family'/name, family/name)
    for name in ('startup_transport.py', 'qmp.py'):
        shutil.copyfile(ROOT/'scripts/reference'/name, stage/name)
    for name in ('peer.py', 'boundaries.py'):
        shutil.copyfile(ROOT/'internal/document/evidence/retrieve-field-observations'/name, stage/name)
    shutil.copyfile(SOURCE/'original-pyproject.toml', stage/'pyproject.toml')
    data = package/'originaldata'
    data.mkdir()
    command(['/usr/bin/cc', '-std=c11', '-O2', '-static', '-o', str(data/'control-fixture'),
             str(SOURCE/'tests/original_control_fixture.c')], target, end, target/'compile-control-candidate')
    shutil.copyfile(SOURCE/'tests/original_control_master.txt',data/'control-master.bin')
    shutil.copyfile(SOURCE/'tests/original_control_roster.json',data/'roster.json')
    wheels = target/'wheels'
    wheels.mkdir()
    command(['/usr/bin/python', '-B', '-m', 'pip', 'wheel', '--no-index', '--no-deps',
             '--no-build-isolation', '--wheel-dir', str(wheels), str(stage)], target, end, target/'wheel')
    wheel, = wheels.glob('*.whl')
    expected_payloads = {str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()
                         and (p.is_relative_to(package) or p.is_relative_to(family) or p.name in
                              ('startup_transport.py','peer.py','boundaries.py','qmp.py'))
                         and not any(part in ('build','egg-info') or part.endswith('.egg-info') for part in p.relative_to(stage).parts)}
    dist = 'wordling_reference_controller_original_route-0.1.0.dist-info'
    metadata = {dist+'/'+n for n in ('METADATA','WHEEL','top_level.txt','RECORD')}
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        if len(names)!=len(set(names)) or set(names)!=expected_payloads|metadata:
            raise RuntimeError('WheelClosedMemberSet')
        for name in names:
            if archive.getinfo(name).file_size>1048576:
                raise RuntimeError('WheelMemberBound')
            if name in expected_payloads and archive.read(name)!=(stage/name).read_bytes():
                raise RuntimeError('WheelPayloadChanged')
    environment = target/'venv'
    command([str(BASE), '-I', '-B', '-m', 'venv', '--copies', '--without-pip',
             str(environment)], target, end, target/'venv-create')
    interpreter = environment/'bin/python'
    command(['/usr/bin/python', '-B', '-m', 'pip', '--python', str(interpreter),
             'install', '--no-index', '--no-deps', '--no-compile', str(wheel)],
            target, end, target/'install')
    observation_code = """import argparse,ast,copy,csv,dataclasses,fcntl,functools,hashlib,importlib.util,json,math,os,pathlib,resource,select,selectors,signal,socket,stat,struct,sys,tempfile,threading,time,types,typing,uuid
paths=set()
for module in tuple(sys.modules.values()):
 for field in ('__file__','__cached__'):
  name=getattr(module,field,None)
  if name and not name.startswith('<') and pathlib.Path(name).is_file():paths.add(name)
for row in pathlib.Path('/proc/self/maps').read_text().splitlines():
 bits=row.split()
 if len(bits)>5 and bits[-1].startswith('/') and pathlib.Path(bits[-1]).is_file():paths.add(bits[-1])
print(json.dumps(dict(version=sys.version,version_info=list(sys.version_info[:2]),base_prefix=sys.base_prefix,executable=sys.executable,customization=sorted(n for n in ('sitecustomize','usercustomize','_distutils_hack') if n in sys.modules),paths=sorted(paths))))"""
    observation = json.loads(command([str(interpreter),'-I','-B','-c',observation_code],target,end,target/'stdlib').stdout)
    if observation['customization']:
        raise RuntimeError('ColdRuntimeCustomization:'+','.join(observation['customization']))
    site = environment/('lib/python%d.%d/site-packages' % tuple(observation['version_info']))
    names = tuple('reference_controller/'+n for n in ORIGINAL_NAMES)+('startup_transport.py',)+tuple('startup_family/'+n for n in P_NAMES)+('peer.py','boundaries.py','qmp.py')
    installed = {n:pin(site/n) for n in names}
    digest = hashlib.sha256()
    for name in names:
        if pin(stage/name) != installed[name]:raise RuntimeError('InstalledPayloadChanged')
        digest.update(name.encode('ascii')+b'\0'+bytes.fromhex(installed[name]['sha256']))
    data_pins = {n:pin(site/'reference_controller/originaldata'/n) for n in ('control-fixture','control-master.bin','roster.json')}
    source_hash = digest.hexdigest()
    manifest = dict(schema='wordling.original-deployment/v1',executable=str(interpreter),
        base_prefix=observation['base_prefix'],version=observation['version'],files=installed,
        data=data_pins,source_hash=source_hash,plan_hash=data_pins['roster.json']['sha256'])
    (environment/'wordling-original-deployment.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    candidate = hashlib.sha256(json.dumps({n:data_pins[n] for n in ('control-fixture','control-master.bin')},sort_keys=True,separators=(',',':')).encode('ascii')).hexdigest()
    declaration = json.loads((data/'roster.json').read_text())
    limits = dict(seconds=30,cleanup_seconds=2,source_io=67108864,prepared_bytes=65536,commands=2,output_bytes=4096,control_messages=1200,control_wire_bytes=33554432,polls=8192)
    rows = {}
    for template in declaration['rows']:
        row = dict(template,candidate=candidate,source=source_hash,limits=limits)
        if row['action'] == 'leaf':
            fields = dict(row_id=row['id'],domain=row['domain'],profile=row['profile'],case=row['case'],context=row['context'],repetition=row['repetition'],group=row['group'],scenario=row['scenario'],candidate=candidate,source=source_hash,grant_id=row['grant_id'])
            row['plan_hash']=hashlib.sha256(json.dumps(fields,sort_keys=True,separators=(',',':')).encode('ascii')).hexdigest()
        rows[row['id']] = row
    (environment/'wordling-original-plans.json').write_text(json.dumps(dict(schema='wordling.original-plans/v1',rows=rows),sort_keys=True,indent=2)+'\n')
    paths = {Path(n) for n in observation['paths']} | {p for p in environment.rglob('*') if p.is_file()} | {BASE}
    inventory = {}
    for path in sorted(paths):
        if path.is_symlink():raise RuntimeError('InventorySymlink:'+str(path))
        st=path.stat();inventory[str(path)] = dict(pin(path),mode=st.st_mode&0o7777,uid=st.st_uid)
    inventory_path = environment/'wordling-original-inventory.json'
    inventory_path.write_text(json.dumps(dict(schema='wordling.original-inventory/v1',files=inventory),sort_keys=True,indent=2)+'\n')
    bundle = dict(schema='wordling.original-review-bundle/v1',phase='WP104',
        deployment=pin(environment/'wordling-original-deployment.json')['sha256'],
        inventory=pin(inventory_path)['sha256'],plans=pin(environment/'wordling-original-plans.json')['sha256'],
        source=source_hash,candidate=candidate,reviews=[])
    (environment/'wordling-original-review-bundle.json').write_text(json.dumps(bundle,sort_keys=True,indent=2)+'\n')
    (target/'preparation.json').write_text(json.dumps(dict(wheel=pin(wheel),authored_control_source=pin(SOURCE/'tests/original_control_fixture.c'),metadata=pin(SOURCE/'original-pyproject.toml'),bundle=pin(environment/'wordling-original-review-bundle.json'),inventory_files=len(inventory),inventory_bytes=sum(x['size'] for x in inventory.values()),original_qualification=False,root_invocations=0,control_leaves=0),sort_keys=True,indent=2)+'\n')
    return interpreter


def preflight(interpreter):
    """Trusted caller checks the complete frozen cold closure BEFORE imports."""
    environment = interpreter.parent.parent
    inventory = json.loads((environment/'wordling-original-inventory.json').read_text())['files']
    actual = {str(p) for p in environment.rglob('*') if p.is_file() and p.name not in
              ('wordling-original-inventory.json','wordling-original-review-bundle.json')}
    if actual != {n for n in inventory if Path(n).is_relative_to(environment)}:
        raise RuntimeError('ColdInventoryExtraFile')
    for name, expected in inventory.items():
        path = Path(name)
        st = path.lstat()
        if path.is_symlink() or dict(pin(path),mode=st.st_mode&0o7777,uid=st.st_uid)!=expected:
            raise RuntimeError('ColdInventoryChanged')
    sites = tuple(environment.glob('lib/python*/site-packages'))
    if len(sites)!=1:raise RuntimeError('ColdSiteLayout')
    site = sites[0]
    if any(p.is_symlink() or p.suffix in ('.pth','.pyc') or p.name=='__pycache__' for p in site.rglob('*')):
        raise RuntimeError('ColdCustomizationOrCache')


def invoke(interpreter, code):
    preflight(interpreter)
    result = subprocess.run([str(interpreter), '-I', '-B', '-c', code],
                            cwd=interpreter.parent.parent, env=dict(PATH='/usr/bin:/bin',
                            LANG='C.UTF-8', HOME=str(interpreter.parent.parent)),
                            capture_output=True, timeout=30)
    if len(result.stdout)+len(result.stderr)>65536:
        raise RuntimeError('ConsumerOutputBound')
    return result


class InstalledDeployment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='wordling-original-admission-')
        cls.interpreter = deploy(Path(cls.temporary.name)/'deployment')

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()
