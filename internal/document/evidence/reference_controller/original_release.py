"""The single DIRECT trusted-host ROOT entry; importing this module does no IO.

Calling coordinate_one is a deliberate ROOT action in the reviewed host workflow.
Neither its arguments nor opaque objects authenticate an arbitrary host actor.
Ordinary leaf/TEST/child call graphs may never invoke this entry or its mint.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import time
from .errors import Opaque, Refusal

_KEY = object()
_DECISIONS = {}
_STARTS = {}
_BUNDLE = 'wordling-original-review-bundle.json'
_INVENTORY = 'wordling-original-inventory.json'
_PLANS = 'wordling-original-plans.json'


def _identity(st):
    return st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns,st.st_uid,st.st_mode,st.st_nlink


def _read(path, maximum):
    st = path.lstat()
    if (not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_uid != os.getuid() or
            st.st_size > maximum or st.st_size < 0):
        raise Refusal('ReleaseFile')
    with path.open('rb') as stream:
        raw = stream.read(maximum+1)
    if len(raw) > maximum or _identity(path.lstat()) != _identity(st):
        raise Refusal('ReleaseFileChanged')
    return raw


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise Refusal('DuplicateReleaseKey')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


def _pin(path, expected, end):
    st = path.lstat()
    if (not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size > 67108864 or
            set(expected) != {'size','sha256','mode','uid'} or
            st.st_size != expected['size'] or stat.S_IMODE(st.st_mode) != expected['mode'] or
            st.st_uid != expected['uid']):
        raise Refusal('DeploymentInventory')
    digest, count = hashlib.sha256(), 0
    with path.open('rb') as stream:
        while True:
            if time.monotonic_ns() >= end:
                raise Refusal('ReleaseDeadline')
            raw = stream.read(16384)
            if not raw:
                break
            digest.update(raw)
            count += len(raw)
            if count > expected['size']:
                raise Refusal('DeploymentInventory')
    if digest.hexdigest() != expected['sha256'] or _identity(path.lstat()) != _identity(st):
        raise Refusal('DeploymentInventoryChanged')


def _checked_bundle(accepted_digest, start):
    # This validates already-reviewed data. It does NOT authenticate the actor.
    prefix = Path(sys.prefix)
    if (not sys.flags.isolated or not sys.dont_write_bytecode or sys.prefix == sys.base_prefix or
            Path(sys.executable).is_symlink() or 'sitecustomize' in sys.modules or
            'usercustomize' in sys.modules):
        raise Refusal('UnsafeInterpreter')
    raw = _read(prefix/_BUNDLE, 262144)
    if type(accepted_digest) is not str or _digest(raw) != accepted_digest:
        raise Refusal('UnacceptedReviewBundle')
    bundle = _json(raw)
    if (type(bundle) is not dict or set(bundle) != {'schema','phase','deployment','inventory','plans','source','candidate','reviews'} or
            bundle['schema'] != 'wordling.original-review-bundle/v1' or bundle['phase'] != 'WP104' or
            type(bundle['reviews']) is not list or not 1 <= len(bundle['reviews']) <= 8 or
            any(type(x) is not str or not 1 <= len(x) <= 256 for x in bundle['reviews'])):
        raise Refusal('UnacceptedReviewBundle')
    inventory_raw = _read(prefix/_INVENTORY, 262144)
    plans_raw = _read(prefix/_PLANS, 262144)
    deployment_raw = _read(prefix/'wordling-original-deployment.json', 262144)
    if any(_digest(raw) != bundle[name] for raw, name in
           [(inventory_raw,'inventory'),(plans_raw,'plans'),(deployment_raw,'deployment')]):
        raise Refusal('ReleaseClosureBinding')
    inventory = _json(inventory_raw)
    if (type(inventory) is not dict or set(inventory) != {'schema','files','directories','absent'} or
            inventory['schema'] != 'wordling.original-inventory/v1' or
            type(inventory['files']) is not dict or not 1 <= len(inventory['files']) <= 1024):
        raise Refusal('DeploymentInventory')
    files = inventory['files']
    end = start+30000000000
    total = 0
    for name, expected in files.items():
        if type(name) is not str or len(name) > 512:
            raise Refusal('DeploymentInventoryPath')
        path = Path(name)
        # Public installed/interpreter/stdlib closure only; never private assets.
        if (not path.is_absolute() or '..' in path.parts or not any(path.is_relative_to(root)
                for root in (prefix, Path(sys.base_prefix), Path('/usr/lib'), Path('/lib')))):
            raise Refusal('DeploymentInventoryPath')
        total += expected.get('size', 268435457)
        if total > 268435456:
            raise Refusal('DeploymentInventoryBound')
        _pin(path, expected, end)
    excluded = {_BUNDLE, _INVENTORY}
    roots = (prefix,Path(sys.base_prefix))
    if any(p.is_symlink() or p.name=='__pycache__' or p.suffix in ('.pyc','.pth') for root in roots for p in root.rglob('*')):
        raise Refusal('DeploymentCustomizationOrLink')
    actual = {str(p) for root in roots for p in root.rglob('*') if p.is_file() and p.name not in excluded}
    expected_installed = {n for n in files if any(Path(n).is_relative_to(root) for root in roots)}
    if actual != expected_installed:
        raise Refusal('DeploymentExtraFile')
    directories = inventory['directories']
    if type(directories) is not dict or len(directories)>512 or type(inventory['absent']) is not list or len(inventory['absent'])>16:
        raise Refusal('DeploymentDirectoryMap')
    actual_dirs = {str(p):dict(mode=stat.S_IMODE(p.stat().st_mode),uid=p.stat().st_uid)
                   for root in roots for p in (root,*root.rglob('*')) if p.is_dir()}
    if actual_dirs != directories or any(Path(n).exists() or Path(n).is_symlink() for n in inventory['absent']):
        raise Refusal('DeploymentExtraMember')
    for module in tuple(sys.modules.values()):
        name = getattr(module, '__file__', None)
        if name and not name.startswith('<') and name not in files:
            raise Refusal('DeploymentUnreviewedModule')
    plans = _json(plans_raw)
    if type(plans) is not dict or set(plans) != {'schema','rows'} or plans['schema'] != 'wordling.original-plans/v1':
        raise Refusal('ReleasePlans')
    return bundle, plans, _digest(raw)


class RootDecision(Opaque):
    def __init__(self, key, invocation, source, plan, accepted):
        if key is not _KEY or invocation not in _STARTS:
            raise Refusal('RootDecisionRequired')
        self._invocation, self._source, self._plan = invocation, source, plan
        self._accepted = accepted
        self._used = False
        self._origin_ns = _STARTS[invocation]


def _decision_binding(decision):
    return (decision._invocation, decision._source, decision._plan, decision._plan.digest(),
            decision._accepted, decision._origin_ns)


def _mint_registered_decision(invocation, source, plan, accepted):
    # The structural gate pins THIS sole caller and tests injected violations.
    decision = RootDecision(_KEY, invocation, source, plan, accepted)
    _DECISIONS[decision] = _decision_binding(decision)
    return decision


def _consume_decision(decision, source, plan):
    if (type(decision) is not RootDecision or decision not in _DECISIONS or
            decision._used or _decision_binding(decision) != _DECISIONS[decision] or
            decision._source is not source or decision._plan is not plan or
            decision._invocation not in _STARTS):
        raise Refusal('RootDecisionRequired')
    decision._used = True  # No refund after any later error, including failed IO.
    if not decision._origin_ns <= time.monotonic_ns() < min(decision._origin_ns+30000000000,source.end_ns):
        raise Refusal('ReleaseDeadline')
    return decision._origin_ns, decision._accepted


def coordinate_one(reviewed_row_id, accepted_bundle_digest, invocation_note):
    """ONE deliberate ROOT action in this interpreter, never a worker factory.

    It must not be invoked by tests/leaf/child code. ROOT externally invokes only
    the independently frozen and reviewed finite row it actually authorizes.
    """
    start = time.monotonic_ns()
    if (type(reviewed_row_id) is not str or not 1 <= len(reviewed_row_id) <= 64 or
            type(invocation_note) is not str or not 1 <= len(invocation_note) <= 512):
        raise Refusal('RootInvocationScope')
    bundle, plans, unused = _checked_bundle(accepted_bundle_digest, start)
    from .bootstrap import load_original_policy
    source = load_original_policy(origin_ns=start)
    if source.source_hash != bundle['source']:
        raise Refusal('ReleaseSourceBinding')
    rows = plans['rows']
    if type(rows) is not dict or len(rows) > 64 or reviewed_row_id not in rows:
        raise Refusal('RootInvocationScope')
    from .original import OriginalLeafPlan, validate_roster, open_original_leaf
    validate_roster(source, rows, bundle['candidate'])
    row = rows[reviewed_row_id]
    if row['action'] == 'control-admin':
        from .original_control_admin import ControlAdministration, administer_one
        plan = ControlAdministration.from_row(row)
    else:
        plan = OriginalLeafPlan.from_row(row)
    if plan.domain != 'CONTROL':
        raise Refusal('OriginalRouteIncomplete')  # WP105/101 and later ROOT release are required.
    if row['action'] == 'leaf' and plan.case == 'C104-EXPIRED':
        from .bootstrap import _shorten_original_end
        _shorten_original_end(source,start+1)  # actual earlier1ns scope, never invented elapsed time
    invocation = object()
    _STARTS[invocation] = start
    leaf = grant = issuer = None
    try:
        decision = _mint_registered_decision(invocation, source, plan,
                                            (accepted_bundle_digest, invocation_note, reviewed_row_id))
        if row['action'] == 'control-admin':
            return administer_one(decision, source, plan)
        from .issuance import RootTicketIssuer
        issuer = RootTicketIssuer()
        grant = issuer.issue(decision, source, plan)
        if plan.domain == 'CONTROL' and plan.case == 'C104-DEATH':
            os._exit(97)  # actual coordinator loss; durable hold is already fsynced
        if plan.domain == 'CONTROL' and plan.case == 'C104-MARKER':
            raise Refusal('ControlMarkerReplyLost',partial=True)
        if plan.domain == 'CONTROL' and plan.case == 'C104-CROSSDOMAIN':
            from dataclasses import replace
            leaf = open_original_leaf(source,replace(plan,domain='ORIGINAL',profile='ORIGINAL-WP51-V1'),grant)
        elif plan.domain == 'CONTROL' and plan.case == 'C104-HANDOFF':
            from dataclasses import replace
            leaf = open_original_leaf(source,replace(plan,context='UNBOUND'),grant)
        else:
            leaf = open_original_leaf(source, plan, grant)
        return leaf.prepare_and_launch()
    finally:
        try:
            if leaf is not None:
                leaf.close()  # containment only: ALWAYS leaves durable unresolved hold in WP104.
            elif grant is not None:
                issuer.abandon(grant)
        finally:
            _STARTS.pop(invocation, None)
