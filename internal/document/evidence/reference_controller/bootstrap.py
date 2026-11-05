"""Ordinary sealed TEST controller deployment; policy observations never grant work."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import socket
import select
import sys
import time
from .errors import Refusal

_VALIDATED_POLICIES = {}
E_FILES = ('__init__.py', '__main__.py', 'bootstrap.py', 'errors.py', 'account.py',
           'ownership.py', 'records.py', 'issuance.py', 'cli.py', 'controller.py',
           'protocol.py', 'publisher.py')
P_FILES = ('__init__.py', 'artifacts.py', 'engine.py', 'lifetime.py')
SOURCE_FILES = (tuple('reference_controller/'+n for n in E_FILES) +
                ('startup_transport.py',) + tuple('startup_family/'+n for n in P_FILES) +
                ('peer.py', 'boundaries.py', 'qmp.py'))
# Selected CODE catalog only. Frozen issuer IO/work/check/time limits do not change.
CODE_FILE_BYTES = 131072
CODE_TOTAL_BYTES = 524288
DATA_FILES = ('fixture', 'master.bin')


class SourcePolicyData:
    """Retained validated data; original issuer admission remains disabled."""
    def __init__(self, manifest, package, identities, deployment_hash, fixtures):
        self.origin_ns = time.monotonic_ns()
        self.end_ns = self.origin_ns + 30000000000
        self.deployment_hash = deployment_hash
        self.source_hash, self.plan_hash = manifest['source_hash'], manifest['plan_hash']
        self.package, self._identities = package, identities
        self.fixtures = fixtures
        self.code_hashes = tuple((n, manifest['files'][n]['sha256']) for n in SOURCE_FILES)

    def verify(self, meter, owner):
        # Exactly20 source identities:3 charged filesystem/time checks each in
        # the genuine issuer meter. Data are subsequently captured by real P.
        validate_policy(self)
        for name, identity in self._identities.items():
            meter.charge(owner, syscalls=1, work=3)
            try:
                st = os.stat(self.package/name, follow_symlinks=False)
            except OSError:
                meter._book.halt('SourceChanged')
                raise Refusal('SourceChanged') from None
            if (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns) != identity:
                meter._book.halt('SourceChanged')
                raise Refusal('SourceChanged')
            meter.check(owner)


def _binding(policy):
    return (policy.origin_ns, policy.end_ns, policy.source_hash, policy.deployment_hash,
            policy.package, policy.fixtures, policy.code_hashes, tuple(policy._identities.items()))


def validate_policy(policy):
    if type(policy) is not SourcePolicyData or policy not in _VALIDATED_POLICIES:
        raise Refusal('UnverifiedPolicyData')
    if (type(policy._identities) is not dict or len(policy._identities)!=20 or
            set(policy._identities)!=set(SOURCE_FILES) or type(policy.fixtures) is not tuple or
            len(policy.fixtures)!=2 or type(policy.code_hashes) is not tuple or len(policy.code_hashes)!=20 or
            type(policy.origin_ns) is not int or type(policy.end_ns) is not int or
            _binding(policy) != _VALIDATED_POLICIES[policy] or
            type(policy.plan_hash) is not str or len(policy.plan_hash) != 64 or
            any(c not in '0123456789abcdef' for c in policy.plan_hash)):
        raise Refusal('UnverifiedPolicyData')


def _regular(path, maximum):
    st = path.lstat()
    if (path.is_symlink() or not stat.S_ISREG(st.st_mode) or
            st.st_nlink != 1 or not 0 <= st.st_size <= maximum):
        raise Refusal('DeploymentSource')
    return st


def _module_origins(site):
    expected = {'startup_transport':site/'startup_transport.py', 'peer':site/'peer.py',
                'boundaries':site/'boundaries.py', 'qmp':site/'qmp.py'}
    for n in E_FILES:
        key = 'reference_controller' if n == '__init__.py' else 'reference_controller.'+n[:-3]
        expected[key] = site/'reference_controller'/n
    # Only the actual approved facade may create this alias; E never injects it.
    for n in P_FILES:
        key = 'wordling_reference_startup_v1' if n == '__init__.py' else 'wordling_reference_startup_v1.'+n[:-3]
        expected[key] = site/'startup_family'/n
    for key, module in tuple(sys.modules.items()):
        if key=='startup_family' or key.startswith('startup_family.'):
            raise Refusal('DeploymentForeignModule')
        if (key in expected or key.startswith(('reference_controller.',
                                                'wordling_reference_startup_v1.'))):
            if key not in expected or getattr(module, '__file__', None) != str(expected[key]):
                raise Refusal('DeploymentForeignModule')
    for key in ('startup_transport', 'peer', 'boundaries', 'qmp'):
        spec = importlib.util.find_spec(key)
        if spec is None or spec.origin != str(expected[key]):
            raise Refusal('DeploymentForeignOrigin')


def load_policy():
    required=('pidfd_open','fork','pipe2','waitid','waitpid','P_PID','WEXITED','WNOHANG','WNOWAIT','CLD_EXITED','P_PIDFD','O_NOFOLLOW','O_CLOEXEC','O_DIRECTORY')
    if (any(not hasattr(os,name) for name in required) or
            any(not hasattr(socket,n) for n in ('AF_UNIX','SOL_SOCKET','SO_PEERCRED','SO_ERROR')) or
            any(not hasattr(select,n) for n in ('poll','POLLHUP','POLLERR'))):
        raise Refusal('UnsupportedRuntimePrimitives')
    if (not sys.flags.isolated or not sys.flags.ignore_environment or
            not sys.flags.no_user_site or not sys.dont_write_bytecode or
            'sitecustomize' in sys.modules or 'usercustomize' in sys.modules or
            '_distutils_hack' in sys.modules or sys.excepthook is not sys.__excepthook__):
        raise Refusal('UnsafeInterpreter')
    package = Path(__file__).parent
    site = Path(sys.prefix)/('lib/python%d.%d/site-packages' % sys.version_info[:2])
    if package != site/'reference_controller' or package.is_symlink() or sys.prefix == sys.base_prefix:
        raise Refusal('UnsealedSourceRoot')
    path = Path(sys.prefix)/'wordling-test-deployment.json'
    _regular(path, 262144)
    raw = path.read_bytes()
    manifest = json.loads(raw)
    if (type(manifest) is not dict or manifest.get('schema') != 'wordling.test-controller-deployment/v1' or
            manifest.get('executable') != sys.executable or manifest.get('base_prefix') != sys.base_prefix or
            manifest.get('version') != sys.version or type(manifest.get('files')) is not dict or
            set(manifest['files']) != set(SOURCE_FILES) or type(manifest.get('data')) is not dict or
            set(manifest['data']) != set(DATA_FILES)):
        raise Refusal('DeploymentManifest')
    identities, digest, total = {}, hashlib.sha256(), 0
    for name in SOURCE_FILES:
        p = site/name
        st = _regular(p, CODE_FILE_BYTES)
        total += st.st_size
        if total > CODE_TOTAL_BYTES or st.st_size != manifest['files'][name]['size']:
            raise Refusal('DeploymentSource')
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h != manifest['files'][name]['sha256']:
            raise Refusal('DeploymentSource')
        digest.update(name.encode('ascii')+b'\0'+bytes.fromhex(h))
        identities[name] = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
    if digest.hexdigest() != manifest.get('source_hash'):
        raise Refusal('DeploymentSource')
    if (type(manifest.get('plan_hash')) is not str or len(manifest['plan_hash']) != 64 or
            any(c not in '0123456789abcdef' for c in manifest['plan_hash'])):
        raise Refusal('DeploymentPlan')
    fixtures = []
    for name in DATA_FILES:
        p = package/'testdata'/name
        st = _regular(p, 1048576)
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if (st.st_size != manifest['data'][name]['size'] or h != manifest['data'][name]['sha256']):
            raise Refusal('DeploymentData')
        fixtures.append((name, str(p), st.st_size, h))
    if {p.name for p in package.iterdir()} != set(E_FILES)|{'testdata'}:
        raise Refusal('DeploymentExtraFile')
    if {p.name for p in (package/'testdata').iterdir()} != set(DATA_FILES):
        raise Refusal('DeploymentExtraFile')
    _module_origins(site)
    policy = SourcePolicyData(manifest, site, identities, hashlib.sha256(raw).hexdigest(), tuple(fixtures))
    _VALIDATED_POLICIES[policy] = _binding(policy)
    return policy


def validate_provider(policy):
    """Post-import actual public facade/class/alias coupling, never a capability."""
    validate_policy(policy)
    import startup_transport as provider
    _module_origins(policy.package)
    expected = {n:dict(policy.code_hashes)['startup_family/'+n] for n in P_FILES}
    binding = provider.source_binding()
    if (binding['root'] != str(policy.package/'startup_family') or binding['version'] != 1 or
            binding['sha256'] != expected):
        raise Refusal('ProviderSourceMismatch')
    groups = {'artifacts.py': ('SourceRequest','StreamPolicy','NewWorkspace','MutationSpec','LaunchSpec',
        'ResourceArgument','SourceLease','WorkingLease','ExecutableLease','StoppedReadLease',
        'DerivedArtifactLease','OutputSpec','OutputArgument','JobBudget','DerivationSpec'),
        'lifetime.py': ('Session','ProcessLease','ManagedPolicy','SharedEnvelopePolicy',
        'IdentityObservation','UsageObservation','Snapshot','MutationResult','ExitObservation',
        'DerivedBatch','ArtifactChunk','OutputObservation','SessionOutcome')}
    for suffix, names in groups.items():
        for name in names:
            cls = getattr(provider,name)
            module = sys.modules.get(cls.__module__)
            if (module is None or module.__file__ != str(policy.package/'startup_family'/suffix) or
                    getattr(module,name,None) is not cls):
                raise Refusal('ProviderClassMismatch')
    return provider


def main():
    try:
        policy = load_policy()
        from .cli import main as command
        return command(policy)
    except (Refusal, OSError, ValueError, KeyError) as exc:
        print(json.dumps(dict(status='REFUSED', reason=str(exc)[:256]), sort_keys=True))
        return 2
