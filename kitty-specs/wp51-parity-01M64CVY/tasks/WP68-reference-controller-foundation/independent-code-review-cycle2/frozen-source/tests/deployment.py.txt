"""Trusted finite test coordinator: offline wheel, copied isolated venv, preflight.

No product modules are imported here. Wheel compilation is normal packaging;
its exact source copy is pinned before building and never used as a runtime root.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import resource
import sys
import time
import venv

BASE = Path('/home/lynn/.local/share/uv/python/cpython-3.13.13-linux-x86_64-gnu/bin/python3.13')
SUITE_END = None
RUN_HOME = None

def configure_home(path):
    global RUN_HOME
    if RUN_HOME is not None: raise RuntimeError('home cannot be reset')
    RUN_HOME = str(path)

def configure_deadline(end):
    global SUITE_END
    if SUITE_END is not None:
        raise RuntimeError('suite deadline cannot be reset')
    SUITE_END = end

def remaining():
    value = 300 if SUITE_END is None else SUITE_END - time.monotonic()
    if value <= 0:
        raise RuntimeError('shared suite deadline')
    return value

FILES = ('__init__.py', '__main__.py', 'bootstrap.py', 'errors.py', 'account.py',
         'ownership.py', 'records.py', 'issuance.py', 'cli.py')


def pin(path):
    data = path.read_bytes()
    return dict(size=len(data), sha256=hashlib.sha256(data).hexdigest())


def run(argv, cwd, log, timeout=30):
    env = dict(PATH='/usr/local/go/bin:/usr/bin:/bin', HOME=RUN_HOME or str(cwd), LANG='C.UTF-8', LC_ALL='C.UTF-8',
               PYTHONDONTWRITEBYTECODE='1', PIP_DISABLE_PIP_VERSION_CHECK='1',
               GOCACHE='/home/lynn/.cache/go-build', GOMODCACHE='/home/lynn/go/pkg/mod',
               GOPATH='/home/lynn/go', GOTOOLCHAIN='local', GOPROXY='off', GOSUMDB='off')
    started = time.monotonic_ns()
    timeout = min(timeout, remaining())
    result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=timeout)
    if len(result.stdout) + len(result.stderr) > 2097152:
        raise RuntimeError('output cap exceeded')
    log.parent.mkdir(parents=True, exist_ok=True)
    log.with_suffix('.stdout').write_bytes(result.stdout)
    log.with_suffix('.stderr').write_bytes(result.stderr)
    log.with_suffix('.json').write_text(json.dumps(dict(argv=argv, cwd=str(cwd), env=env,
        returncode=result.returncode, elapsed_ns=time.monotonic_ns()-started,
        cumulative_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss), indent=2)+'\n')
    return result


def deploy(source, target, evidence):
    target.mkdir(mode=0o700)
    build = target / 'build-input'
    build.mkdir()
    frozen = {}
    for name in FILES + ('pyproject.toml',):
        frozen[name] = pin(source / name)
        (build / name).write_bytes((source / name).read_bytes())
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / 'build-source.json').write_text(json.dumps(frozen, indent=2)+'\n')
    wheels = target / 'wheels'
    wheels.mkdir()
    r = run(['/usr/bin/python', '-B', '-m', 'pip', 'wheel', '--no-deps', '--no-index',
             '--no-build-isolation', '--wheel-dir', str(wheels), str(build)], target, evidence/'build')
    if r.returncode:
        raise RuntimeError('offline wheel failed; raw retained')
    wheel, = wheels.glob('*.whl')
    environment = target / 'venv'
    r = run([str(BASE), '-I', '-B', '-m', 'venv', '--copies', '--without-pip', str(environment)], target, evidence/'venv')
    if r.returncode:
        raise RuntimeError('copied venv failed')
    interpreter = environment / 'bin/python'
    if interpreter.is_symlink():
        raise RuntimeError('copied executable required')
    r = run(['/usr/bin/python', '-B', '-m', 'pip', '--python', str(interpreter), 'install',
             '--no-index', '--no-deps', '--no-compile', str(wheel)], target, evidence/'install')
    if r.returncode:
        raise RuntimeError('offline install failed')
    # Actual ordinary interpreter reports its own standard-library/module origins.
    code = """import argparse, dataclasses, fcntl, hashlib, json, os, pathlib, stat, sys, time, typing
assert 'sitecustomize' not in sys.modules and 'usercustomize' not in sys.modules
print(json.dumps(dict(version=sys.version,base_prefix=sys.base_prefix,executable=sys.executable,
origins=sorted(set(m.__file__ for m in sys.modules.values() if getattr(m,'__file__',None) and not m.__file__.startswith('<'))))))"""
    r = run([str(interpreter), '-I', '-B', '-c', code], target, evidence/'stdlib')
    if r.returncode:
        raise RuntimeError('runtime closure probe failed')
    observation = json.loads(r.stdout)
    package = environment/'lib/python3.13/site-packages/reference_controller'
    digest = hashlib.sha256()
    installed = {}
    for name in FILES:
        installed[name] = pin(package/name)
        if installed[name] != frozen[name]:
            raise RuntimeError('wheel source mismatch')
        digest.update(name.encode('ascii')+b'\0'+bytes.fromhex(installed[name]['sha256']))
    manifest = dict(schema='wordling.test-deployment/v1', files=installed,
        source_hash=digest.hexdigest(), plan_hash=hashlib.sha256((source/'tests/roster.json').read_bytes()).hexdigest(),
        executable=str(interpreter), base_prefix=observation['base_prefix'], version=observation['version'])
    (environment/'wordling-test-deployment.json').write_text(json.dumps(manifest, indent=2)+'\n')
    # The coordinator's separate immutable deployment inventory covers actual
    # stdlib/extension files, interpreter/config and EVERY installed file.
    paths = set(Path(x) for x in observation['origins'])
    paths.update(p for p in environment.rglob('*') if p.is_file())
    paths.add(BASE)
    inventory = {str(p): pin(p) for p in sorted(paths)}
    inventory_path = evidence/'deployment-inventory.json'
    inventory_path.write_text(json.dumps(inventory, indent=2)+'\n')
    if inventory_path.stat().st_size > 262144:
        raise RuntimeError('deployment inventory exceeds cap')
    (evidence/'deployment.json').write_text(json.dumps(dict(wheel=str(wheel), wheel_pin=pin(wheel),
        inventory=pin(inventory_path), interpreter=pin(interpreter), source_hash=manifest['source_hash'],
        premise='exclusive trusted local deployment custody; fixed proven local mount; no hostile owner'), indent=2)+'\n')
    return interpreter, inventory


def preflight(interpreter, inventory):
    envroot = interpreter.parent.parent
    for root in (envroot/'lib/python3.13/site-packages',):
        for p in root.rglob('*'):
            if p.is_symlink() or p.name.endswith(('.pth', '.pyc')) or p.name == '__pycache__':
                raise RuntimeError('unsafe deployment cache/customization/symlink')
            if p.is_file() and str(p) not in inventory:
                raise RuntimeError('unexpected installed file')
    for name, expected in inventory.items():
        p = Path(name)
        if p.is_symlink() or pin(p) != expected:
            raise RuntimeError('deployment changed before interpreter startup')
    if not interpreter.is_file() or interpreter.is_symlink():
        raise RuntimeError('unsafe interpreter')
