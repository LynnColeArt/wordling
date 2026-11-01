"""Sealed TEST deployment, with trusted exclusive prelaunch custody."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import time
from .errors import Refusal

_VALIDATED_POLICIES = {}

SOURCE_FILES = ('__init__.py', '__main__.py', 'bootstrap.py', 'errors.py', 'account.py',
                'ownership.py', 'records.py', 'issuance.py', 'cli.py')


class SourcePolicyData:
    """Validated observations only: neither a permit nor a ticket issuer."""
    def __init__(self, manifest, package, identities, deployment_hash):
        self.origin_ns = time.monotonic_ns()
        self.end_ns = self.origin_ns + 30000000000
        self.deployment_hash = deployment_hash
        self.source_hash = manifest['source_hash']
        self.plan_hash = manifest['plan_hash']
        self.package = package
        self._identities = identities

    def verify(self, meter, owner):
        for name, identity in self._identities.items():
            meter.charge(owner, syscalls=1, work=1)
            try:
                st = os.stat(self.package / name, follow_symlinks=False)
            except OSError:
                meter._book.halt('SourceChanged')
                raise Refusal('SourceChanged') from None
            if (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns) != identity:
                meter._book.halt('SourceChanged')
                raise Refusal('SourceChanged')
            meter.check(owner)



def validate_policy(policy):
    if type(policy) is not SourcePolicyData or policy not in _VALIDATED_POLICIES:
        raise Refusal('UnverifiedPolicyData')
    expected = _VALIDATED_POLICIES[policy]
    actual = (policy.origin_ns, policy.end_ns, policy.source_hash,
              policy.deployment_hash, policy.package)
    if actual != expected or type(policy.plan_hash) is not str or len(policy.plan_hash) != 64 or any(c not in '0123456789abcdef' for c in policy.plan_hash):
        raise Refusal('UnverifiedPolicyData')


def load_policy():
    if (not sys.flags.isolated or not sys.flags.ignore_environment or
            not sys.flags.no_user_site or not sys.dont_write_bytecode or
            'sitecustomize' in sys.modules or 'usercustomize' in sys.modules):
        raise Refusal('UnsafeInterpreter')
    package = Path(__file__).parent
    expected = Path(sys.prefix) / ('lib/python%d.%d/site-packages/reference_controller' % sys.version_info[:2])
    if package != expected or package.is_symlink() or sys.prefix == sys.base_prefix:
        raise Refusal('UnsealedSourceRoot')
    path = Path(sys.prefix) / 'wordling-test-deployment.json'
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size > 262144:
        raise Refusal('DeploymentManifest')
    raw = path.read_bytes()
    manifest = json.loads(raw)
    if (type(manifest) is not dict or manifest.get('schema') != 'wordling.test-deployment/v1' or
            manifest.get('executable') != sys.executable or manifest.get('base_prefix') != sys.base_prefix or
            manifest.get('version') != sys.version or type(manifest.get('files')) is not dict or
            set(manifest['files']) != set(SOURCE_FILES)):
        raise Refusal('DeploymentManifest')
    identities, digest = {}, hashlib.sha256()
    total = 0
    for name in SOURCE_FILES:
        p = package / name
        st = p.lstat()
        total += st.st_size
        if (not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size > 65536 or
                total > 65536 or st.st_size != manifest['files'][name]['size']):
            raise Refusal('DeploymentSource')
        data = p.read_bytes()
        h = hashlib.sha256(data).hexdigest()
        if h != manifest['files'][name]['sha256']:
            raise Refusal('DeploymentSource')
        digest.update(name.encode('ascii') + b'\0' + bytes.fromhex(h))
        identities[name] = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
    if digest.hexdigest() != manifest.get('source_hash'):
        raise Refusal('DeploymentSource')
    if (type(manifest.get('plan_hash')) is not str or len(manifest['plan_hash']) != 64 or
            any(c not in '0123456789abcdef' for c in manifest['plan_hash'])):
        raise Refusal('DeploymentPlan')
    for p in package.iterdir():
        if p.name not in SOURCE_FILES:
            raise Refusal('DeploymentExtraFile')
    policy = SourcePolicyData(manifest, package, identities, hashlib.sha256(raw).hexdigest())
    _VALIDATED_POLICIES[policy] = (policy.origin_ns, policy.end_ns, policy.source_hash,
                                    policy.deployment_hash, policy.package)
    return policy


def main():
    try:
        policy = load_policy()
        from .cli import main as command
        return command(policy)
    except (Refusal, OSError, ValueError, KeyError) as exc:
        print(json.dumps(dict(status='REFUSED', reason=str(exc)[:256]), sort_keys=True))
        return 2
