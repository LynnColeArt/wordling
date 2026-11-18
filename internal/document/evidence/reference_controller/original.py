"""One registered original-subsystem leaf; WP104 stops at OWNED_UNREADY.

CONTROL is authored harmless software, never original qualification. This module
cannot mint ROOT decisions and never imports the trusted ROOT coordinator.
"""
from dataclasses import dataclass, asdict
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import time
from .errors import Opaque, Refusal
from .bootstrap import OriginalSourcePolicy, validate_policy, validate_provider
from .account import (OperationLimits, DIMENSIONS, _reserve_cleanup_hold,
                      _take_cleanup_hold, _source_live_observation)
from .ownership import ParentLease, OwnedLedger, _call, _identity, _components, _DIR, _FILE, _emergency_close

_KEY = object()
_ACTIVE = {}
# Deployment-time immutable source stamp; no CLI/JSON/domain selector can change it.
CONTROL_VARIANT = 'baseline'
CONTROL_BASES = {'baseline':'/tmp/wordling-reference-CONTROL-v1',
    'M01':'/tmp/wordling-reference-CONTROL-v1-M01','M02':'/tmp/wordling-reference-CONTROL-v1-M02',
    'M03':'/tmp/wordling-reference-CONTROL-v1-M03','M04':'/tmp/wordling-reference-CONTROL-v1-M04',
    'M05':'/tmp/wordling-reference-CONTROL-v1-M05','M06':'/tmp/wordling-reference-CONTROL-v1-M06',
    'M07':'/tmp/wordling-reference-CONTROL-v1-M07','M08':'/tmp/wordling-reference-CONTROL-v1-M08'}
CONTROL_BASE = CONTROL_BASES[CONTROL_VARIANT]
CONTROL_ROOT = CONTROL_BASE+'/wp104/'
# Unreleased finite extension proposal: independent review required before admin.
CONTROL_CAMPAIGN_NS = 1200000000000
ORIGINAL_GUARD = '/home/lynn/projects/wordling/research/cache/reference/session1.lock'
# Historical public metadata only (code-pair-history/final-preflight.json rows0..4).
# These are exact refusal targets, not assertions of current resource fitness.
ORIGINAL_INPUTS = {'boot': ('/home/lynn/projects/wordling/research/cache/reference/master/boot.img', 1474560, 'e7b599780eef4f0a068a47185aca00f30b37971a85c54084c881729e544ed4ca'), 'disk': ('/home/lynn/projects/wordling/research/cache/reference/master/harddisk.img', 67108864, 'ba1a6a5f475c0f6487697be10654566d164bb8c4d091ed8709d48260e9dc72e1'), 'qemu': ('/usr/bin/qemu-system-i386', 26359752, '28fa14f1c45fca7422e3ec5737768b33b705de2f31014a76e658d4263464a6a5'), 'bios': ('/usr/share/seabios/bios-256k.bin', 262144, '1a9ea4f17bcfb27bda5728e2c21d9fa074cf7947b9b4910bb28213a735c96735'), 'vga': ('/usr/share/seabios/vgabios-stdvga.bin', 39424, '4eecd8e752efc02c6c0fe87eb92bf66934cb9ea67b0e1bc41e86f8430c8bf8a0')}
ORIGINAL_STORE = '/home/lynn/projects/wordling/research/cache/reference/original-issuer-v1'
ORIGINAL_LEDGERS = '/home/lynn/projects/wordling/research/cache/reference/original-ledgers-v1'
MASTER = b'WORDLING ROOT CONTROL V1\n'
LIMITS = dict(seconds=30, cleanup_seconds=2, source_io=67108864, prepared_bytes=65536,
              commands=2, output_bytes=4096, control_messages=1200,
              control_wire_bytes=33554432, polls=8192)


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('ascii')


def _token(value):
    return (type(value) is str and 1 <= len(value) <= 64 and
            all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-' for c in value))


@dataclass(frozen=True)
class OriginalLeafPlan:
    row_id: str
    domain: str
    profile: str
    case: str
    context: str
    repetition: int
    group: str
    scenario: str
    candidate: str
    source: str
    grant_id: str
    plan_hash: str

    @classmethod
    def from_row(cls, row):
        if type(row) is not dict or set(row) != {'id','action','domain','profile','case','context',
                'repetition','group','scenario','candidate','source','grant_id','plan_hash','limits'}:
            raise Refusal('OriginalPlanSchema')
        if row['action'] != 'leaf' or row['limits'] != LIMITS:
            raise Refusal('OriginalPlanLimits')
        plan = cls(row['id'], row['domain'], row['profile'], row['case'], row['context'],
                   row['repetition'], row['group'], row['scenario'], row['candidate'],
                   row['source'], row['grant_id'], row['plan_hash'])
        plan.validate()
        return plan

    def validate(self):
        if (not all(_token(x) for x in (self.row_id,self.case,self.context,self.group,self.scenario,self.grant_id)) or
                self.domain not in ('CONTROL','ORIGINAL') or
                self.profile != {'CONTROL':'CONTROL-V1','ORIGINAL':'ORIGINAL-WP51-V1'}[self.domain] or
                type(self.repetition) is not int or not 1 <= self.repetition <= 2 or
                any(type(x) is not str or len(x) != 64 or any(c not in '0123456789abcdef' for c in x)
                    for x in (self.candidate,self.source,self.plan_hash)) or self.digest() != self.plan_hash):
            raise Refusal('OriginalPlanBinding')
        if self.domain == 'CONTROL' and len(os.fsencode(CONTROL_ROOT+self.group+'/w-'+self.grant_id+'/qmp.sock')) >= 108:
            raise Refusal('OriginalEndpointFit')

    def digest(self):
        values = asdict(self)
        values.pop('plan_hash')
        return hashlib.sha256(_canonical(values)).hexdigest()

    @property
    def store_root(self):
        return self.control_root+'/issuer' if self.domain == 'CONTROL' else ORIGINAL_STORE

    @property
    def ledger_parent(self):
        return self.control_root+'/ledgers' if self.domain == 'CONTROL' else ORIGINAL_LEDGERS

    @property
    def workspace(self):
        return (self.control_root+'/w-'+self.grant_id if self.domain == 'CONTROL' else
                '/tmp/wordling-reference-ORIGINAL-v1-'+self.grant_id)

    @property
    def control_root(self):
        self.validate()
        if self.domain != 'CONTROL':
            raise Refusal('OriginalRouteIncomplete')
        return CONTROL_ROOT+self.group


def validate_roster(source, rows, candidate):
    validate_policy(source)
    if type(source) is not OriginalSourcePolicy or type(rows) is not dict or len(rows) > 64:
        raise Refusal('OriginalRoster')
    data = {n:(p,s,h) for n,p,s,h in source.fixtures}
    path, size, digest = data['roster.json']
    raw = Path(path).read_bytes()
    if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
        raise Refusal('OriginalRosterChanged')
    declaration = json.loads(raw)
    if set(declaration) != {'schema','rows'} or declaration['schema'] != 'wordling.control-roster-template/v1':
        raise Refusal('OriginalRoster')
    if set(rows) != {r['id'] for r in declaration['rows']} or len(rows) != len(declaration['rows']):
        raise Refusal('OriginalRoster')
    for declared in declaration['rows']:
        row = rows[declared['id']]
        if any(row.get(k) != v for k,v in declared.items()):
            raise Refusal('OriginalRoster')
        if (row.get('domain') != 'CONTROL' or row.get('profile') != 'CONTROL-V1' or
                row.get('candidate') != candidate or row.get('source') != source.source_hash or
                row.get('limits') != LIMITS):
            raise Refusal('OriginalRoster')
        if row['action'] == 'leaf':
            OriginalLeafPlan.from_row(row)
        elif row['action'] != 'control-admin':
            raise Refusal('OriginalRoster')


class _Guard(Opaque):
    """Same retained pre-existing guard routine; never creates or repairs it."""
    def __init__(self, key, context, path):
        if key is not _KEY:
            raise Refusal('GuardAuthority')
        self.context, self.path, self.chain, self.closed = context, path, [], False
        book = context._book
        count = len(_components(path))+1
        self.hold = _reserve_cleanup_hold(book, self, count)
        self.meter = book.reserve_phase('protocol', self,
                    dict(syscalls=16384,work=65536), duration_ns=30000000000)
        self._acquire_end = min(book.end_ns,time.monotonic_ns()+2000000000)
        self._acquiring = True
        try:
            fd = self.call(os.open, '/', _DIR)
            self.chain.append((fd,'',_identity(self.call(os.fstat,fd))))
            parts = _components(path)
            for index, name in enumerate(parts):
                fd = self.call(os.open, name, _FILE if index == len(parts)-1 else _DIR,
                               dir_fd=self.chain[-1][0])
                self.chain.append((fd,name,_identity(self.call(os.fstat,fd))))
            st = self.call(os.fstat,self.chain[-1][0])
            if (not stat.S_ISREG(st.st_mode) or st.st_uid != os.getuid() or
                    st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != 0o600):
                raise Refusal('GuardIdentity')
            self.call(fcntl.flock,self.chain[-1][0],fcntl.LOCK_EX|fcntl.LOCK_NB)
            self.verify()
            self._acquiring = False
        except BaseException:
            book.halt('GuardAcquisitionFailed')
            self.close()
            raise

    def call(self, function, *args, **kwargs):
        if self._acquiring and time.monotonic_ns() >= self._acquire_end:
            raise Refusal('GuardDeadline')
        self.context._source.verify(self.meter,self)
        result = _call(self.meter,self,function,*args,**kwargs)
        try:
            self.context._source.verify(self.meter,self)
            if self._acquiring and time.monotonic_ns() >= self._acquire_end:
                raise Refusal('GuardDeadline',partial=True)
        except Refusal:
            if function is os.open:
                _emergency_close(self.context._book,result)
            raise
        return result

    def verify(self):
        for index,(fd,name,identity) in enumerate(self.chain):
            st = self.call(os.fstat,fd)
            if _identity(st) != identity:
                raise Refusal('GuardIdentity')
            if index and _identity(self.call(os.stat,name,dir_fd=self.chain[index-1][0],follow_symlinks=False)) != identity:
                raise Refusal('GuardRetargeted')
        st = self.call(os.fstat,self.chain[-1][0])
        if st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != 0o600:
            raise Refusal('GuardIdentity')

    def close(self):
        if self.closed:
            return
        self.closed = True
        meter = _take_cleanup_hold(self.hold,self)
        failed = False
        for fd,_,identity in reversed(self.chain):
            if _identity(_call(meter,self,os.fstat,fd)) != identity:
                self.context._book.halt('CleanupIncomplete')
                failed = True
                continue
            _call(meter,self,os.close,fd)
        if failed:
            raise Refusal('CleanupIncomplete',partial=True)
        # Kernel close is NOT safe discharge; the persistent unresolved hold remains.


class OriginalLeaf(Opaque):
    def __init__(self, key, source, plan, issuer, book):
        if key is not _KEY:
            raise Refusal('SourcePrelaunchBlocked')
        self._source,self._plan,self._issuer,self._book = source,plan,issuer,book
        self._session=self._process=self._guard=self._parent=self._ledger=self._contender=None
        self._ran=self._closed=False
        self._rpc_calls=0
        self._last_usage=None

    def _control_fault_after_guard(self):
        # These literal source-owned CONTROL rows induce actual faults AFTER
        # genuine grant consumption. ORIGINAL can never select these effects.
        if self._plan.domain != 'CONTROL':
            return
        if self._plan.case == 'C104-EXHAUSTED':
            self._p_meter.charge(self,syscalls=16001)
        if self._plan.case == 'C104-RETARGET':
            parent = self._guard.chain[-2][0]
            call = self._guard.call
            call(os.link,'session1.lock','CONTROL-retained.lock',src_dir_fd=parent,dst_dir_fd=parent,follow_symlinks=False)
            call(os.unlink,'session1.lock',dir_fd=parent)
            fd = call(os.open,'session1.lock',_FILE|os.O_CREAT|os.O_EXCL,0o600,dir_fd=parent)
            call(os.close,fd)
            self._guard.verify()  # real retained old FD versus replacement name
        if self._plan.case == 'C104-SOURCE':
            # Last scheduled destructive control: only the reviewed disposable
            # installed copy, never repository/source/private reference bytes.
            if not Path(self._source.package).is_relative_to('/tmp/wordling-WP104-precontrol-v1'):
                raise Refusal('ControlSourceFaultScope')
            path = self._source.package/'reference_controller/original.py'
            fd = _call(self._p_meter,self,os.open,path,os.O_WRONLY|os.O_APPEND|os.O_NOFOLLOW|os.O_CLOEXEC)
            try:
                raw = b'\n# CONTROL source-identity fault\n'
                self._p_meter.charge(self,source_io=len(raw),work=len(raw))
                if _call(self._p_meter,self,os.write,fd,raw) != len(raw):
                    raise Refusal('ControlFaultShortWrite',partial=True)
                _call(self._p_meter,self,os.fsync,fd)
            finally:
                _call(self._p_meter,self,os.close,fd)
            self._source.verify(self._p_meter,self)

    def _control_cleanup_fault(self):
        if self._plan.domain != 'CONTROL' or self._plan.case != 'C104-CLEANUP':
            return
        guardfd = self._guard.chain[-1][0]
        parent = self._guard.chain[-2][0]
        meter = self._p_meter
        fd = _call(meter,self,os.open,'CONTROL-foreign.bin',_FILE|os.O_CREAT|os.O_EXCL,0o600,dir_fd=parent)
        try:
            self._book._created_regular[('control',_identity(_call(meter,self,os.fstat,fd)))] = True
            raw = b'CONTROL FOREIGN BYTES MUST SURVIVE\n'
            meter.charge(self,source_io=len(raw),work=len(raw))
            if _call(meter,self,os.write,fd,raw) != len(raw):
                raise Refusal('ControlFaultShortWrite')
            _call(meter,self,os.fsync,fd)
            _call(meter,self,os.close,guardfd)
            _call(meter,self,os.dup2,fd,guardfd,inheritable=False)
            # Deliberately keep the foreign replacement open. Guard cleanup
            # must refuse it; the bounded coordinator exit closes kernel FDs.
        finally:
            _call(meter,self,os.close,fd)

    def _check(self):
        if self not in _ACTIVE or _ACTIVE[self] != (self._source,self._plan,self._issuer,self._book) or self._closed:
            raise Refusal('OriginalContextRequired')
        self._plan.validate()
        validate_policy(self._source)
        self._book._check()

    def _p(self, name, *args):
        self._check()
        if name not in ('identity','capture','prepare','tool','mutate','launch','usage'):
            raise Refusal('OriginalOperation')
        if self._rpc_calls >= 48:
            raise Refusal('OriginalRPCBound')
        # Every potentially blocking operation must leave the declared2s
        # cleanup tail in the earlier leaf clock; no poll or IO renews it.
        operation_ns = 2000000000 if self._plan.domain == 'CONTROL' else 1000000000
        if self._book.end_ns-time.monotonic_ns() < operation_ns+2000000000:
            raise Refusal('OriginalTailFit')
        self._rpc_calls += 1
        self._source.verify(self._p_meter,self)
        result = self._process.verify_current() if name == 'identity' else getattr(self._session,name)(*args)
        self._source.verify(self._p_meter,self)
        return result

    def _record(self, state):
        permit = self._book.reserve_ledger_operation('update-record',self._ledger,
                    OperationLimits(syscalls=512,work=262144,io=16385))
        self._ledger.write_json(self._book.record(state,dict(domain=self._plan.domain,
              profile=self._plan.profile,stage='OWNED_UNREADY' if state == 'RUNNING' else 'AUTHORIZED_UNREADY',
              original_qualification=False,ready=False,
              safety_hold='UNRESOLVED',physical_released=False),permit),permit)

    def _observe(self):
        usage = self._p('usage')
        if (usage.origin != self._book.origin_ns/1e9 or usage.end != self._book.end_ns/1e9 or
                not usage.journal_durable or usage.control_wire_bytes+usage.reserved_response_bytes > 33554432 or
                usage.control_messages+usage.reserved_response_messages > 1200 or
                usage.journal_events > 128 or usage.journal_bytes > 524288):
            raise Refusal('OriginalUsageBinding')
        if self._last_usage is not None:
            if usage.session_id != self._last_usage.session_id or any(getattr(usage,n)<getattr(self._last_usage,n)
                    for n in ('source_io','prepared_bytes','charged_operations','control_wire_bytes',
                              'control_messages','polls','output_bytes','journal_events','journal_bytes')):
                raise Refusal('OriginalCounterReset')
        rows = usage.actor_fds
        if (len({(pid,ticks) for pid,ticks,_ in rows}) != len(rows) or
                sum(count for _,_,count in rows) != usage.current_fds or
                not any(pid==os.getpid() for pid,_,_ in rows)):
            raise Refusal('OriginalActorBinding')
        # P includes the coordinator, including retained E FDs/RSS. Never add it
        # twice. Observe names/types only, never live resource bytes or authority.
        if usage.current_fds+1 > 64:
            raise Refusal('OriginalObservationHeadroom')
        self._parent._validate(self._p_meter,self)
        directory = _call(self._p_meter,self,os.open,self._plan.workspace,_DIR)
        count = entries = 0
        try:
            self._p_meter.charge(self,syscalls=1,work=16)
            with os.scandir(directory) as stream:
                for entry in stream:
                    entries += 1
                    if entries > 10:
                        raise Refusal('OriginalWorkspaceObservation')
                    self._p_meter.charge(self,syscalls=1,work=1)
                    st = entry.stat(follow_symlinks=False)
                    if stat.S_ISREG(st.st_mode) and st.st_nlink == 1:
                        count += 1
                    elif not stat.S_ISSOCK(st.st_mode):
                        raise Refusal('OriginalWorkspaceObservation')
            if count > 8:
                raise Refusal('OriginalWorkspaceObservation')
        finally:
            _call(self._p_meter,self,os.close,directory)
        self._source.verify(self._p_meter,self)
        current=dict(processes=usage.current_processes,rss_bytes=usage.current_rss,
                     fds=usage.current_fds,files=len(self._book._created_regular)+count+3)
        peaks=dict(processes=usage.peak_processes,rss_bytes=usage.peak_rss,
                   fds=max(usage.peak_fds,usage.current_fds+1),files=current['files'])
        self._book.record_live(_source_live_observation(self._book,self,current,peaks,
             'RETAINED_BOUND_ACTOR_SET',int(usage.observed_monotonic*1e9)))
        self._last_usage=usage
        return usage

    def prepare_and_launch(self):
        try:
            return self._prepare_and_launch()
        except BaseException as error:
            self._book.halt(getattr(error,'code','OriginalLaunchFailure'))
            raise

    def _prepare_and_launch(self):
        self._check()
        if self._ran:
            raise Refusal('OriginalRunOnce')
        self._ran=True
        control = self._plan.domain == 'CONTROL'
        root = self._plan.control_root if control else None
        prepared_cap = 65536 if control else 110100480
        self._p_meter = self._book.reserve_phase('P',self,dict(source_io=3221225472,
                wire_bytes=33554432,messages=1200,commands=2,polls=8192,work=1048576,
                syscalls=16000,prepared_bytes=prepared_cap,output_bytes=4096,
                journal_events=128,journal_bytes=524288),duration_ns=30000000000)
        self._provider = p = validate_provider(self._source)
        self._parent = ParentLease.acquire(self._book.parent_path,self._book.reserve_ledger_operation(
            'acquire-parent',self._book.parent_path,OperationLimits(fds=len(_components(self._book.parent_path))+1)))
        self._ledger = OwnedLedger.create(self._parent,self._book.basename,self._book.reserve_ledger_operation(
            'create-ledger',(self._parent,self._book.basename),OperationLimits(fds=1)))
        # Profile selection is source-owned and still domain-bound, never a TEST selector.
        guard_path = root+'/shared/session1.lock' if control else ORIGINAL_GUARD
        if control and self._plan.case == 'C104-CONTENTION':
            # A real separately opened OFD holds the actual CONTROL fixture
            # guard. Same guard implementation; no registry/selector patch.
            self._contender = _Guard(_KEY,self,guard_path)
        self._guard = _Guard(_KEY,self,guard_path)
        self._control_fault_after_guard()
        self._record('AUTHORIZED')
        workspace = self._plan.workspace
        if len(os.fsencode(workspace+'/qmp.sock')) >= 108:
            raise Refusal('OriginalEndpointFit')
        envelope = p.SharedEnvelopePolicy(self._book.origin_ns/1e9,self._book.end_ns/1e9,
            source_io=67108864 if control else 3221225472,prepared_bytes=prepared_cap,commands=2,output_bytes=4096,
            control_messages=1200,control_wire_bytes=33554432,polls=8192,
            journal_events=128,journal_bytes=524288,
            measurement_completion='bounded-original-v2')
        stream = p.StreamPolicy(file_bytes=1048576 if control else 67108864,
            source_bytes=2097152 if control else 268435456,copied_bytes=prepared_cap,
            resources=1 if control else 4,sources=4 if control else 8,files=8,
            workspace_bytes=1048576 if control else prepared_cap,
            io_bytes=67108864 if control else 3221225472,
            operation_seconds=2 if control else 1,preparation_seconds=2 if control else 1,resource_fds=8)
        managed = p.ManagedPolicy(total_seconds=5,startup_seconds=2,readiness_seconds=10,
            session_seconds=30,command_seconds=2,stream_bytes=1024,output_bytes=4096,polls=8192)
        self._source.verify(self._p_meter,self)
        self._session = p.open_session(p.NewWorkspace(workspace),stream,managed,envelope=envelope)
        self._source.verify(self._p_meter,self)
        self._observe()
        if control:
            data = {n:(path,size,digest) for n,path,size,digest in self._source.fixtures}
            master = data['control-master.bin']
            tool = data['control-fixture']
            # CONTROL administration preprovisions these exact harmless copies; P validates bytes.
            master_source = self._p('capture',p.SourceRequest(root+'/sources/control-master.bin',master[1],master[2]))
            tool_source = self._p('capture',p.SourceRequest(root+'/tools/control-fixture',tool[1],tool[2]))
            self._working = self._p('prepare',master_source,'working.bin')
            self._tool = self._p('tool',tool_source)
            mutation = self._p('mutate',self._working,p.MutationSpec(self._tool,
                (root+'/tools/control-fixture','mutate',p.ResourceArgument('',self._working,''),self._plan.scenario),
                immutable_inputs=(master_source,)))
            if (mutation.status != 'COMMITTED' or not mutation.immutable_inputs_unchanged or mutation.exit_code != 0 or
                    mutation.after_epoch != mutation.before_epoch+1):
                raise Refusal('OriginalMutationUnproved')
            self._working = mutation.successor
            self._observe()
            self._process = self._p('launch',p.LaunchSpec(self._tool,
                (root+'/tools/control-fixture','serve',p.ResourceArgument('',self._working,''),
                 'qmp.sock',self._plan.scenario)),(self._working,))
        else:
            # Source-fixed historical facts; capture is permitted only by a later
            # genuine ORIGINAL release. No stat/read of these paths during load,
            # schema negatives, CONTROL or any WP104 validation.
            inputs = {name:self._p('capture',p.SourceRequest(*facts))
                      for name,facts in ORIGINAL_INPUTS.items()}
            self._tool = self._p('tool',inputs['qemu'])
            working = {name:self._p('prepare',inputs[name],name+'.img')
                       for name in ('boot','disk','bios','vga')}
            self._working = working['disk']
            self._original_working = tuple(working[n] for n in ('boot','disk','bios','vga'))
            self._observe()
            argv = (ORIGINAL_INPUTS['qemu'][0],'-machine','pc-i440fx-8.2','-accel','tcg,thread=single',
                '-cpu','486','-m','16','-vga','std','-bios',p.ResourceArgument('',working['bios'],''),
                '-global',p.ResourceArgument('VGA.romfile=',working['vga'],''),
                '-display','none','-serial','none','-parallel','none','-nic','none',
                '-rtc','base=1992-03-09T12:00:00,clock=vm',
                '-drive',p.ResourceArgument('file=',working['boot'],',format=raw,if=floppy,index=0'),
                '-drive',p.ResourceArgument('file=',working['disk'],',format=raw,if=ide,index=0'),
                '-boot','order=a','-qmp','unix:qmp.sock,server=on,wait=off','-monitor','none')
            self._process = self._p('launch',p.LaunchSpec(self._tool,argv),self._original_working)
        identity = self._p('identity')
        usage = self._observe()
        if usage.original_state != 'OWNED' or usage.current_original_identity is None or (
                usage.current_original_identity.pid,usage.current_original_identity.startticks) != (identity.pid,identity.startticks):
            raise Refusal('OriginalForegroundLost')
        self._guard.verify()
        self._record('RUNNING')
        return dict(status='OWNED_UNREADY',domain=self._plan.domain,profile=self._plan.profile,
                    row=self._plan.row_id,original_qualification=False,ready=False,
                    process=dict(pid=identity.pid,startticks=identity.startticks),
                    safety_hold='UNRESOLVED',physical_released=False)

    def close(self):
        if self._closed:
            return
        self._closed = True
        failure = None
        try:
            if self._session is not None:
                outcome = self._session.close()  # containment, not a normal stop witness.
                if not outcome.supervisor_reaped or outcome.cleanup != 'STOPPED':
                    raise Refusal('OriginalContainmentUnproved',partial=True)
                if self._book._fault is None:
                    self._control_cleanup_fault()
        except BaseException as error:
            failure = error
        self._book.halt('OwnershipOnlyContainment')
        for retained in (self._guard,self._contender,self._ledger,self._parent):
            if retained is None:
                continue
            try:
                if retained is self._guard or retained is self._contender:
                    retained.close()
                else:
                    retained.close(self._book.reserve_ledger_operation('cleanup-close',retained,retained.close_requirements()))
            except BaseException as error:
                failure = failure or error
        try:
            self._issuer.finish(self._book)
        finally:
            _ACTIVE.pop(self,None)
        if failure:
            raise Refusal('OriginalCleanupIncomplete',partial=True) from failure


def open_original_leaf(source_policy, immutable_single_leaf_plan, actual_grant):
    # Exact registered grant BEFORE caller data, attributes, paths or P effects.
    from .issuance import RootTicketIssuer, _original_issuer
    issuer = _original_issuer(actual_grant)
    if type(issuer) is not RootTicketIssuer:
        raise Refusal('SourcePrelaunchBlocked')
    book = issuer.activate(actual_grant,source_policy,immutable_single_leaf_plan)
    leaf = OriginalLeaf(_KEY,source_policy,immutable_single_leaf_plan,issuer,book)
    _ACTIVE[leaf]=(source_policy,immutable_single_leaf_plan,issuer,book)
    return leaf
