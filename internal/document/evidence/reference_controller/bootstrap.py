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
    if type(policy) is OriginalSourcePolicy:
        return _validate_original_policy(policy)
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
    if type(policy) is OriginalSourcePolicy:
        _original_module_origins(policy.package)
    else:
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


# Separate ordinary deployment. None of these declarations grants execution;
# the TEST map and its exact-type admission above remain unchanged.
ORIGINAL_E_FILES = E_FILES + ('original.py', 'original_release.py', 'original_control_admin.py')
ORIGINAL_SOURCE_FILES = (tuple('reference_controller/'+n for n in ORIGINAL_E_FILES) +
                         ('startup_transport.py',) + tuple('startup_family/'+n for n in P_FILES) +
                         ('peer.py', 'boundaries.py', 'qmp.py'))
ORIGINAL_DATA_FILES = ('control-fixture', 'control-master.bin', 'roster.json')
_ORIGINAL_POLICIES = {}


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def _sha(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


class OriginalSourcePolicy:
    """Registered deployment data, expressly not a ROOT decision or grant."""
    def __init__(self, manifest, site, identities, deployment_hash, origin_ns):
        self.origin_ns, self.end_ns = origin_ns, origin_ns+30000000000
        self.source_hash, self.plan_hash = manifest['source_hash'], manifest['plan_hash']
        self.package, self._identities = site, identities
        self.deployment_hash = deployment_hash
        self.fixtures = tuple((n, str(site/'reference_controller/originaldata'/n),
                               manifest['data'][n]['size'], manifest['data'][n]['sha256'])
                              for n in ORIGINAL_DATA_FILES)
        self.code_hashes = tuple((n, manifest['files'][n]['sha256']) for n in ORIGINAL_SOURCE_FILES)
        self._manifest = manifest
        self._leaf_bound = False
        extra = [Path(sys.prefix)/'wordling-original-deployment.json'] + [
            site/'reference_controller/originaldata'/n for n in ORIGINAL_DATA_FILES]
        self._extra_identities = tuple((str(path), (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns))
                                      for path in extra for s in (path.lstat(),))

    def verify(self, meter, owner):
        _validate_original_policy(self)
        names = tuple((self.package/name,identity) for name,identity in self._identities.items()) + self._extra_identities
        for name, identity in names:
            meter.charge(owner, syscalls=1, work=3)
            try:
                st = os.stat(name, follow_symlinks=False)
            except OSError:
                meter._book.halt('SourceChanged')
                raise Refusal('SourceChanged') from None
            if (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns) != identity:
                meter._book.halt('SourceChanged')
                raise Refusal('SourceChanged')
            meter.check(owner)


def _original_binding(policy):
    return (_binding(policy), hashlib.sha256(_canonical(policy._manifest)).hexdigest(),
            policy._leaf_bound,policy._extra_identities)


def _bind_original_plan(policy, digest):
    _validate_original_policy(policy)
    if policy._leaf_bound or not _sha(digest):
        raise Refusal('OriginalPlanOnce')
    policy.plan_hash, policy._leaf_bound = digest, True
    _ORIGINAL_POLICIES[policy] = _original_binding(policy)


def _shorten_original_end(policy, end_ns, book=None):
    _validate_original_policy(policy)
    if type(end_ns) is not int or not policy.origin_ns < end_ns <= policy.end_ns:
        raise Refusal('OriginalClockIntersection')
    policy.end_ns = end_ns
    _ORIGINAL_POLICIES[policy] = _original_binding(policy)
    if book is not None:
        if book.policy is not policy:
            raise Refusal('OriginalClockIntersection')
        book.end_ns = min(book.end_ns,end_ns)


def _validate_original_policy(policy):
    if (type(policy) is not OriginalSourcePolicy or policy not in _ORIGINAL_POLICIES or
            set(policy._identities) != set(ORIGINAL_SOURCE_FILES) or
            _original_binding(policy) != _ORIGINAL_POLICIES[policy]):
        raise Refusal('UnverifiedOriginalPolicy')


def _original_module_origins(site):
    expected = {('reference_controller' if n == '__init__.py' else 'reference_controller.'+n[:-3]):
                site/'reference_controller'/n for n in ORIGINAL_E_FILES}
    expected.update({n[:-3]:site/n for n in ('startup_transport.py','peer.py','boundaries.py','qmp.py')})
    expected.update({('wordling_reference_startup_v1' if n == '__init__.py' else
                      'wordling_reference_startup_v1.'+n[:-3]):site/'startup_family'/n for n in P_FILES})
    for name, module in tuple(sys.modules.items()):
        if name == 'startup_family' or name.startswith('startup_family.'):
            raise Refusal('DeploymentForeignModule')
        if name in expected or name.startswith(('reference_controller.', 'wordling_reference_startup_v1.')):
            if name not in expected or getattr(module, '__file__', None) != str(expected[name]):
                raise Refusal('DeploymentForeignModule')


def load_original_policy(*, origin_ns=None):
    """Validate the sealed public deployment; never inspect original resources."""
    now = time.monotonic_ns()
    origin = now if origin_ns is None else origin_ns
    if type(origin) is not int or not now-30000000000 < origin <= now:
        raise Refusal('OriginalOrigin')
    required = ('pidfd_open','fork','pipe2','waitid','waitpid','P_PID','WEXITED','WNOHANG',
                'WNOWAIT','CLD_EXITED','P_PIDFD','O_NOFOLLOW','O_CLOEXEC','O_DIRECTORY')
    if (any(not hasattr(os,n) for n in required) or
            any(not hasattr(socket,n) for n in ('AF_UNIX','SOL_SOCKET','SO_PEERCRED','SO_ERROR')) or
            any(not hasattr(select,n) for n in ('poll','POLLHUP','POLLERR'))):
        raise Refusal('UnsupportedRuntimePrimitives')
    if (not sys.flags.isolated or not sys.flags.ignore_environment or not sys.flags.no_user_site or
            not sys.dont_write_bytecode or 'sitecustomize' in sys.modules or 'usercustomize' in sys.modules or
            '_distutils_hack' in sys.modules or sys.excepthook is not sys.__excepthook__):
        raise Refusal('UnsafeInterpreter')
    site = Path(sys.prefix)/('lib/python%d.%d/site-packages' % sys.version_info[:2])
    if Path(__file__).parent != site/'reference_controller' or sys.prefix == sys.base_prefix:
        raise Refusal('UnsealedSourceRoot')
    path = Path(sys.prefix)/'wordling-original-deployment.json'
    _regular(path, 262144)
    raw = path.read_bytes()
    m = json.loads(raw)
    if (type(m) is not dict or set(m) != {'schema','executable','base_prefix','version','files','data','source_hash','plan_hash'} or
            m['schema'] != 'wordling.original-deployment/v1' or m['executable'] != sys.executable or
            m['base_prefix'] != sys.base_prefix or m['version'] != sys.version or
            type(m['files']) is not dict or set(m['files']) != set(ORIGINAL_SOURCE_FILES) or
            type(m['data']) is not dict or set(m['data']) != set(ORIGINAL_DATA_FILES) or
            not _sha(m['source_hash']) or not _sha(m['plan_hash'])):
        raise Refusal('OriginalDeploymentManifest')
    identities, digest, total = {}, hashlib.sha256(), 0
    for name in ORIGINAL_SOURCE_FILES:
        f = site/name
        st = _regular(f, CODE_FILE_BYTES)
        total += st.st_size
        value = hashlib.sha256(f.read_bytes()).hexdigest()
        if total > CODE_TOTAL_BYTES or {'size':st.st_size,'sha256':value} != m['files'][name]:
            raise Refusal('DeploymentSource')
        digest.update(name.encode('ascii')+b'\0'+bytes.fromhex(value))
        identities[name] = (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
    if digest.hexdigest() != m['source_hash']:
        raise Refusal('DeploymentSource')
    for name in ORIGINAL_DATA_FILES:
        f = site/'reference_controller/originaldata'/name
        st = _regular(f, 1048576)
        if {'size':st.st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} != m['data'][name]:
            raise Refusal('DeploymentData')
    if m['plan_hash'] != m['data']['roster.json']['sha256']:
        raise Refusal('DeploymentPlan')
    if {p.name for p in (site/'reference_controller').iterdir()} != set(ORIGINAL_E_FILES)|{'originaldata'}:
        raise Refusal('DeploymentExtraFile')
    if {p.name for p in (site/'reference_controller/originaldata').iterdir()} != set(ORIGINAL_DATA_FILES):
        raise Refusal('DeploymentExtraFile')
    _original_module_origins(site)
    result = OriginalSourcePolicy(m, site, identities, hashlib.sha256(raw).hexdigest(), origin)
    _ORIGINAL_POLICIES[result] = _original_binding(result)
    return result


def main():
    try:
        policy = load_policy()
        from .cli import main as command
        return command(policy)
    except (Refusal, OSError, ValueError, KeyError) as exc:
        print(json.dumps(dict(status='REFUSED', reason=str(exc)[:256]), sort_keys=True))
        return 2
