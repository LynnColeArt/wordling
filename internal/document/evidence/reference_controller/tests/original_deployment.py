"""Finite offline ordinary-wheel preparation; never issues a ROOT decision."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
SOURCE = Path(__file__).resolve().parents[1]
E_NAMES = ('__init__.py', '__main__.py', 'bootstrap.py', 'errors.py', 'account.py',
           'ownership.py', 'records.py', 'issuance.py', 'cli.py', 'controller.py',
           'protocol.py', 'publisher.py')
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
    """RED baseline uses the current normal TEST wheel, with no source overlay."""
    end = time.monotonic() + 90
    target.mkdir(mode=0o700)
    stage = target/'stage'
    stage.mkdir()
    package = stage/'reference_controller'
    package.mkdir()
    for name in E_NAMES:
        shutil.copyfile(SOURCE/name, package/name)
    family = stage/'startup_family'
    family.mkdir()
    for name in P_NAMES:
        shutil.copyfile(ROOT/'scripts/reference/startup_family'/name, family/name)
    for name in ('startup_transport.py', 'qmp.py'):
        shutil.copyfile(ROOT/'scripts/reference'/name, stage/name)
    for name in ('peer.py', 'boundaries.py'):
        shutil.copyfile(ROOT/'internal/document/evidence/retrieve-field-observations'/name, stage/name)
    shutil.copyfile(SOURCE/'pyproject.toml', stage/'pyproject.toml')
    data = package/'testdata'
    data.mkdir()
    command(['/usr/bin/cc', '-std=c11', '-O2', '-static', '-o', str(data/'fixture'),
             str(SOURCE/'tests/harmless_fixture.c')], target, end, target/'compile-test-fixture')
    (data/'master.bin').write_bytes(b'Wordling5.2 TEST master bytes\n'*1024)
    wheels = target/'wheels'
    wheels.mkdir()
    command(['/usr/bin/python', '-B', '-m', 'pip', 'wheel', '--no-index', '--no-deps',
             '--no-build-isolation', '--wheel-dir', str(wheels), str(stage)], target, end, target/'wheel')
    wheel, = wheels.glob('*.whl')
    environment = target/'venv'
    command([sys.executable, '-I', '-B', '-m', 'venv', '--copies', '--without-pip',
             str(environment)], target, end, target/'venv-create')
    interpreter = environment/'bin/python'
    command(['/usr/bin/python', '-B', '-m', 'pip', '--python', str(interpreter),
             'install', '--no-index', '--no-deps', '--no-compile', str(wheel)],
            target, end, target/'install')
    return interpreter


def invoke(interpreter, code):
    result = subprocess.run([str(interpreter), '-I', '-B', '-c', code],
                            cwd=interpreter.parent.parent, env=dict(PATH='/usr/bin:/bin',
                            LANG='C.UTF-8', HOME=str(interpreter.parent.parent)),
                            capture_output=True, timeout=30)
    if len(result.stdout)+len(result.stderr)>65536:
        raise RuntimeError('ConsumerOutputBound')
    return result
