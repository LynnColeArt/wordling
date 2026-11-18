"""Finite offline ordinary-wheel preparation; never issues a ROOT decision."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
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
STDLIB = Path('/usr/lib/python3.12')
PACKAGES = ('python3.12','python3.12-minimal','python3.12-venv','libpython3.12-minimal',
            'libpython3.12-stdlib','libpython3.12-dev','libpython3.12t64',
            'python3-gdbm','python3-tk')
ALIASES = {
    '_sysconfigdata__linux_x86_64-linux-gnu.py':STDLIB/'_sysconfigdata__x86_64-linux-gnu.py',
    'config-3.12-x86_64-linux-gnu/libpython3.12.so':Path('/usr/lib/x86_64-linux-gnu/libpython3.12.so.1.0'),
}


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


def managed_base(destination, evidence, end):
    """Reviewed ordinary base copy, with exact package provenance and no hooks.

    No -S, ._pth, environment/prefix/path/loader/source modification. The host
    remains untouched; the later ordinary venv discovers this base normally.
    """
    listing = command(['/usr/bin/dpkg-query','-L',*PACKAGES],evidence,end,evidence/'stdlib-packages')
    owned = set(listing.stdout.decode('utf8').splitlines())
    versions = command(['/usr/bin/dpkg-query','-W','-f=${binary:Package} ${Version}\n',*PACKAGES],
                       evidence,end,evidence/'stdlib-package-versions').stdout.decode('utf8')
    rows, excluded = {}, []
    for path in sorted(STDLIB.rglob('*')):
        relative = path.relative_to(STDLIB)
        if ('__pycache__' in relative.parts or path.suffix in ('.pyc','.pyo') or
                any(n in relative.parts for n in ('site-packages','dist-packages'))):
            if path.is_file() or path.is_symlink():
                excluded.append(dict(path=str(path),reason='cache-or-third-party-addon-root'))
            continue
        if relative.as_posix() == 'sitecustomize.py':
            if (not path.is_symlink() or path.resolve()!=Path('/etc/python3.12/sitecustomize.py') or
                    pin(path.resolve())['sha256']!='43d81125d92376b1a69d53a71126a041cc9a18d8080e92dea0a2ae23be138b1e'):
                raise RuntimeError('UnprovedDistroCustomization')
            excluded.append(dict(path=str(path),reason='exact-reviewed-Apport-hook',target=str(path.resolve()),pin=pin(path.resolve())))
            continue
        if path.is_dir() and not path.is_symlink():
            continue
        if str(path) not in owned or path.suffix=='.pth':
            raise RuntimeError('UnknownStdlibAddition:'+str(path))
        source = path
        alias = None
        if path.is_symlink():
            if relative.as_posix() not in ALIASES or path.resolve()!=ALIASES[relative.as_posix()]:
                raise RuntimeError('UnknownStdlibAlias:'+str(path))
            alias = dict(path=str(path),target=str(path.readlink()),resolved=str(path.resolve()))
            source = path.resolve()
        st = source.lstat()
        if not stat.S_ISREG(st.st_mode) or st.st_size>67108864:
            raise RuntimeError('StdlibSourceType')
        rows['lib/python3.12/'+relative.as_posix()] = dict(source=str(source),pin=pin(source),
                 mode=stat.S_IMODE(st.st_mode),identity=[st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns],alias=alias)
    st = BASE.lstat()
    if not stat.S_ISREG(st.st_mode):
        raise RuntimeError('BaseExecutableType')
    rows['bin/python3.12'] = dict(source=str(BASE),pin=pin(BASE),mode=stat.S_IMODE(st.st_mode),
        identity=[st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns],alias=None)
    for package in PACKAGES:
        path = Path('/usr/share/doc')/package/'copyright'
        source = path.resolve()
        st = source.lstat()
        if not stat.S_ISREG(st.st_mode):
            raise RuntimeError('RuntimeLicense')
        rows['share/licenses/'+package+'/copyright'] = dict(source=str(source),pin=pin(source),
            mode=stat.S_IMODE(st.st_mode),identity=[st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns],alias=None)
    total = sum(row['pin']['size'] for row in rows.values())
    if len(rows)>768 or total>67108864:
        raise RuntimeError('ManagedBaseCopyFit')
    # This complete source map is frozen BEFORE copying/invoking the new base.
    record = dict(schema='wordling.managed-system312-copy/v1',packages=versions,included=rows,
                  excluded=excluded,file_count=len(rows),bytes=total,io_upper_bound=6*total,
                  deadline_seconds=90,customization_waived=False)
    (evidence/'managed-base-inputs.json').write_text(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n')
    destination.mkdir(mode=0o700)
    for relative,row in rows.items():
        if time.monotonic()>=end:
            raise RuntimeError('PreparationDeadline')
        source = Path(row['source'])
        st = source.lstat()
        if [st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns]!=row['identity'] or pin(source)!=row['pin']:
            raise RuntimeError('ManagedBaseSourceChanged')
        path = destination/relative
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as output, source.open('rb') as original:
            shutil.copyfileobj(original,output,16384)
        path.chmod(row['mode'])
        if pin(path)!=row['pin'] or pin(source)!=row['pin']:
            raise RuntimeError('ManagedBaseBytesChanged')
        if row['alias'] is not None:
            alias = Path(row['alias']['path'])
            if str(alias.readlink())!=row['alias']['target'] or alias.resolve()!=source:
                raise RuntimeError('ManagedBaseAliasChanged')
    shutil.copyfile(evidence/'managed-base-inputs.json',destination/'wordling-managed-base-copy.json')
    # The actual managed base must prove ordinary discovery before it creates
    # a venv. This diagnostic imports stdlib only; no route/P/CONTROL modules.
    code = "import json,os,sys,sysconfig; print(json.dumps(dict(prefix=sys.prefix,base_prefix=sys.base_prefix,stdlib=sysconfig.get_path('stdlib'),customization=[n for n in ('sitecustomize','usercustomize','_distutils_hack') if n in sys.modules],primitives={n:hasattr(os,n) for n in ('pidfd_open','P_PIDFD','fork','waitid','waitpid')})))"
    observation = json.loads(command([str(destination/'bin/python3.12'),'-I','-B','-c',code],
                                   evidence,end,evidence/'managed-base-cold').stdout)
    if (observation['prefix']!=str(destination) or observation['base_prefix']!=str(destination) or
            observation['stdlib']!=str(destination/'lib/python3.12') or observation['customization'] or
            not all(observation['primitives'].values())):
        raise RuntimeError('ManagedBaseColdDiscovery')
    return destination/'bin/python3.12'


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
    selected = managed_base(target/'base',target,end)
    command([str(selected), '-I', '-B', '-m', 'venv', '--copies', '--without-pip',
             str(environment)], target, end, target/'venv-create')
    interpreter = environment/'bin/python'
    command(['/usr/bin/python', '-B', '-m', 'pip', '--python', str(interpreter),
             'install', '--no-index', '--no-deps', '--no-compile', str(wheel)],
            target, end, target/'install')
    alias = environment/'lib64'
    if not alias.is_symlink() or alias.readlink()!=Path('lib') or alias.resolve()!=environment/'lib':
        raise RuntimeError('UnprovedVenvLib64Alias')
    members = {str(p.relative_to(environment/'lib')):pin(p) for p in (environment/'lib').rglob('*') if p.is_file()}
    if any(p.is_symlink() for p in (environment/'lib').rglob('*')):
        raise RuntimeError('VenvAliasSourceLink')
    alias.unlink()  # exclusively owned artifact, exact reviewed ordinary alias only
    shutil.copytree(environment/'lib',alias)
    if members!={str(p.relative_to(alias)):pin(p) for p in alias.rglob('*') if p.is_file()}:
        raise RuntimeError('VenvAliasBytesChanged')
    (environment/'wordling-venv-lib64-copy.json').write_text(json.dumps(dict(schema='wordling.venv-lib64-copy/v1',
        source='lib',former_link='lib64 -> lib',members=members),sort_keys=True,separators=(',',':'))+'\n')
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
    managed = selected.parent.parent
    roots = (managed,environment)
    for root in roots:
        if any(p.is_symlink() for p in root.rglob('*')):
            raise RuntimeError('ManagedRuntimeSymlink')
    paths = {Path(n) for n in observation['paths']} | {p for root in roots for p in root.rglob('*') if p.is_file()}
    inventory = {}
    for path in sorted(paths):
        if path.is_symlink():raise RuntimeError('InventorySymlink:'+str(path))
        st=path.stat();inventory[str(path)] = dict(pin(path),mode=st.st_mode&0o7777,uid=st.st_uid)
    inventory_path = environment/'wordling-original-inventory.json'
    directories = {str(p):dict(mode=stat.S_IMODE(p.stat().st_mode),uid=p.stat().st_uid)
                   for root in roots for p in (root,*root.rglob('*')) if p.is_dir()}
    absent = [str(managed/'lib/python312.zip')]
    inventory_path.write_text(json.dumps(dict(schema='wordling.original-inventory/v1',files=inventory,
                       directories=directories,absent=absent),sort_keys=True,separators=(',',':'))+'\n')
    if len(inventory)>1024 or inventory_path.stat().st_size>262144 or sum(x['size'] for x in inventory.values())>268435456:
        raise RuntimeError('CompleteRuntimeCatalogFit')
    bundle = dict(schema='wordling.original-review-bundle/v1',phase='WP104',
        deployment=pin(environment/'wordling-original-deployment.json')['sha256'],
        inventory=pin(inventory_path)['sha256'],plans=pin(environment/'wordling-original-plans.json')['sha256'],
        source=source_hash,candidate=candidate,reviews=[])
    (environment/'wordling-original-review-bundle.json').write_text(json.dumps(bundle,sort_keys=True,indent=2)+'\n')
    (target/'preparation.json').write_text(json.dumps(dict(wheel=pin(wheel),authored_control_source=pin(SOURCE/'tests/original_control_fixture.c'),metadata=pin(SOURCE/'original-pyproject.toml'),bundle=pin(environment/'wordling-original-review-bundle.json'),inventory_files=len(inventory),inventory_bytes=sum(x['size'] for x in inventory.values()),original_qualification=False,root_invocations=0,control_leaves=0),sort_keys=True,indent=2)+'\n')
    cold_proof(interpreter,target)
    return interpreter


def preflight(interpreter):
    """Trusted caller checks the complete frozen cold closure BEFORE imports."""
    environment = interpreter.parent.parent
    data = json.loads((environment/'wordling-original-inventory.json').read_text())
    inventory = data['files']
    managed = environment.parent/'base'
    roots = (managed,environment)
    actual = {str(p) for root in roots for p in root.rglob('*') if p.is_file() and p.name not in
              ('wordling-original-inventory.json','wordling-original-review-bundle.json')}
    if actual != {n for n in inventory if any(Path(n).is_relative_to(root) for root in roots)}:
        raise RuntimeError('ColdInventoryExtraFile')
    actual_dirs = {str(p):dict(mode=stat.S_IMODE(p.stat().st_mode),uid=p.stat().st_uid)
                   for root in roots for p in (root,*root.rglob('*')) if p.is_dir()}
    if actual_dirs != data['directories'] or any(Path(n).exists() or Path(n).is_symlink() for n in data['absent']):
        raise RuntimeError('ColdInventoryExtraMember')
    if any(p.is_symlink() or p.name=='__pycache__' or p.suffix in ('.pyc','.pth') for root in roots for p in root.rglob('*')):
        raise RuntimeError('ColdCustomizationOrCache')
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


def cold_proof(interpreter, evidence):
    """Real cold stdlib-only diagnostics and destructive-input refusals.

    No route/P/ROOT/CONTROL module is imported or invoked. Test-created files
    are removed and original bytes restored before a final sealed preflight;
    no live context/grant exists whose fault/history could be reset.
    """
    preflight(interpreter)
    base = interpreter.parent.parent.parent/'base'
    environment = interpreter.parent.parent
    ambient = evidence/'ambient'
    ambient.mkdir()
    (ambient/'json.py').write_text("raise AssertionError('ambient import executed')\n")
    (ambient/'sitecustomize.py').write_text("raise AssertionError('ambient customization executed')\n")
    code = """import json,os,select,socket,sys,sysconfig
names=('pidfd_open','fork','pipe2','waitid','waitpid','P_PID','WEXITED','WNOHANG','WNOWAIT','CLD_EXITED','P_PIDFD','O_NOFOLLOW','O_CLOEXEC','O_DIRECTORY')
print(json.dumps(dict(prefix=sys.prefix,exec_prefix=sys.exec_prefix,base_prefix=sys.base_prefix,executable=sys.executable,stdlib=sysconfig.get_path('stdlib'),paths=sys.path,json_origin=json.__file__,customization=[n for n in ('sitecustomize','usercustomize','_distutils_hack') if n in sys.modules],os={n:hasattr(os,n) for n in names},socket={n:hasattr(socket,n) for n in ('AF_UNIX','SOL_SOCKET','SO_PEERCRED','SO_ERROR')},poll={n:hasattr(select,n) for n in ('poll','POLLHUP','POLLERR')},flags=dict(isolated=sys.flags.isolated,ignore_environment=sys.flags.ignore_environment,no_user_site=sys.flags.no_user_site,dont_write_bytecode=sys.dont_write_bytecode),operational_modules=[n for n in sys.modules if n.startswith(('reference_controller','startup_transport','startup_family','wordling_reference_startup'))])))"""
    env = dict(PATH='/usr/bin:/bin',LANG='C.UTF-8',HOME=str(ambient),PYTHONPATH=str(ambient),
               PYTHONHOME=str(ambient),PYTHONUSERBASE=str(ambient))
    result = subprocess.run([str(interpreter),'-I','-B','-c',code],cwd='/tmp',env=env,
                            capture_output=True,timeout=30)
    (evidence/'cold-adversarial.stdout').write_bytes(result.stdout)
    (evidence/'cold-adversarial.stderr').write_bytes(result.stderr)
    if result.returncode or len(result.stdout)>65536 or len(result.stderr)>65536:
        raise RuntimeError('ColdProofFailed')
    observation = json.loads(result.stdout)
    expected_paths = [str(base/'lib/python312.zip'),str(base/'lib/python3.12'),
                      str(base/'lib/python3.12/lib-dynload'),str(environment/'lib/python3.12/site-packages')]
    if (observation['prefix']!=str(environment) or observation['exec_prefix']!=str(environment) or
            observation['base_prefix']!=str(base) or observation['executable']!=str(interpreter) or
            observation['stdlib']!=str(base/'lib/python3.12') or observation['paths']!=expected_paths or
            observation['json_origin']!=str(base/'lib/python3.12/json/__init__.py') or
            observation['customization'] or observation['operational_modules'] or
            not all(all(observation[n].values()) for n in ('os','socket','poll','flags'))):
        raise RuntimeError('ColdProofIdentity')
    refusals = []
    def refuse(label, setup, cleanup):
        setup()
        try:
            try:
                preflight(interpreter)
            except RuntimeError as error:
                refusals.append(dict(case=label,reason=str(error)))
            else:
                raise RuntimeError('ColdNegativeSurvived:'+label)
        finally:
            cleanup()
        preflight(interpreter)
    extra = base/'lib/python3.12/CONTROL_unreviewed.py'
    refuse('extra-stdlib',lambda:extra.write_bytes(b'# CONTROL extra\n'),lambda:extra.unlink())
    original = base/'lib/python3.12/json/__init__.py'
    before = original.read_bytes()
    refuse('changed-stdlib',lambda:original.write_bytes(before+b'\n# CONTROL changed\n'),lambda:original.write_bytes(before))
    link = base/'CONTROL-unreviewed-link'
    refuse('symlink',lambda:link.symlink_to('lib/python3.12/os.py'),lambda:link.unlink())
    cache = base/'CONTROL.pyc'
    refuse('cache',lambda:cache.write_bytes(b'CONTROL not bytecode'),lambda:cache.unlink())
    archive = base/'lib/python312.zip'
    refuse('unexpected-startup-archive',lambda:archive.write_bytes(b'CONTROL not archive'),lambda:archive.unlink())
    (evidence/'cold-proof.json').write_text(json.dumps(dict(schema='wordling.cold-runtime-proof/v1',
        observation=observation,negative_refusals=refusals,final_preflight='passed',
        root_invocations=0,control_leaves=0,original_actions=0),sort_keys=True,indent=2)+'\n')


class InstalledDeployment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='wordling-original-admission-')
        cls.interpreter = deploy(Path(cls.temporary.name)/'deployment')

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()
