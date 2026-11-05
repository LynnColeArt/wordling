"""One actual harmless TEST leaf, one retained P Session, one same-origin book."""
from dataclasses import dataclass, asdict
import hashlib
import json
import os
import stat
import time
from .errors import Opaque, Refusal
from .bootstrap import validate_policy, validate_provider
from .account import OperationLimits, _source_live_observation, DIMENSIONS
from .issuance import TestGrant, TestIssuer
from .ownership import ParentLease, OwnedLedger, _call

_KEY = object()
_ACTIVE = set()
MASTER_UNIT = b'Wordling5.2 TEST master bytes\n'
MASTER_COUNT = 1024
SUFFIX = b'PREPARED\nSTOPPED\n'
SCENARIOS = ('healthy', 'foreign-peer', 'inherited-peer', 'early-exit', 'bad-greeting',
             'long-line', 'events-65', 'no-lf', 'partial-progress', 'late-greeting',
             'bad-stage', 'bad-quit', 'quit-eof', 'quit-exit-race', 'helper-failure',
             'missing-output', 'unexpected-absence', 'changed-input', 'wrong-output')
CHECKPOINTS = ('handoff', 'prelaunch', 'stop-retained', 'exported', 'published',
               'physical-released', 'audited', 'report')


@dataclass(frozen=True)
class LeafPlan:
    scenario: str = 'healthy'
    checkpoint: str | None = None
    measurement_completion: str = 'bounded-original-v2'

    def __post_init__(self):
        if (type(self.scenario) is not str or self.scenario not in SCENARIOS or
                (self.checkpoint is not None and type(self.checkpoint) is not str) or
                self.checkpoint not in (None,)+CHECKPOINTS or
                type(self.measurement_completion) is not str or
                self.measurement_completion!='bounded-original-v2'):
            raise Refusal('InvalidLeafPlan')

    def digest(self):
        return hashlib.sha256(json.dumps(asdict(self),sort_keys=True,
                                        separators=(',',':')).encode('ascii')).hexdigest()


def _require_context(context):
    if type(context) is not ReferenceController or context not in _ACTIVE or context._closed:
        raise Refusal('InvalidController')


class _StoppedRun(Opaque):
    def __init__(self,key,context,exit_observation):
        if key is not _KEY:
            raise Refusal('StoppedAuthorityRequired')
        self.context, self.session, self.process = context, context._session, context._process
        self.source, self.plan = context._source.source_hash, context._plan.digest()
        self.exit = exit_observation
        self.order = context._order


class ReferenceController(Opaque):
    def __init__(self,key=None):
        if key is not _KEY:
            raise Refusal('ControllerFactoryRequired')
        self._closed = self._ran = self._session_closed = False
        self._book = self._issuer = self._source = self._plan = None
        self._parent = self._ledger = self._physical = None
        self._binaries = ()
        self._session = self._process = self._stopped = self._derived = None
        self._provider = self._p_meter = self._audit = self._chunks = None
        self._outputs = []
        self._protocol_facts = {}
        self._usage_rows = []
        self._last_usage = None
        self._rpc_calls = self._order = 0
        self._stage_order = self._quit_order = None
        self._physical_released = self._notified = False
        self._release_ns = self._notify_ns = self._audit_ns = None
        self._failure = None
        self._stop_objects = set()
        self._close_facts = None

    @classmethod
    def open_leaf(cls,source,immutable_single_leaf_plan,actual_issuergrant):
        # No Original/raw path/JSON grant entry, BEFORE inspecting caller paths.
        if cls is not ReferenceController or type(actual_issuergrant) is not TestGrant:
            raise Refusal('SourcePrelaunchBlocked')
        try:
            issuer = actual_issuergrant._issuer
            if type(issuer) is not TestIssuer:
                raise Refusal('InvalidTestGrant')
            book = issuer.activate(actual_issuergrant)  # Genuine one-use issuer context.
        except (AttributeError,TypeError):
            raise Refusal('InvalidTestGrant') from None
        c = cls(_KEY)
        c._issuer, c._book, c._source = issuer, book, book.policy
        _ACTIVE.add(c)
        try:
            validate_policy(source)
            if (source is not book.policy or type(immutable_single_leaf_plan) is not LeafPlan):
                raise Refusal('ControllerSourcePlan')
            immutable_single_leaf_plan.__post_init__()
            if immutable_single_leaf_plan.digest()!=book._plan:
                raise Refusal('ControllerSourcePlan')
            c._plan = immutable_single_leaf_plan
            # Fixed all-phase reservations BEFORE P import/session/resource effects.
            # 3GiB includes bounded P code-rehash reads, NOT protocol payload capacity.
            c._p_meter = book.reserve_phase('P',c,dict(source_io=3221225472,
                wire_bytes=33554432,messages=1200,commands=3,polls=8192,
                work=1048576,syscalls=16000,prepared_bytes=65536,output_bytes=16384),
                duration_ns=30000000000)
            c._audit = book.reserve_phase('audit',c,dict(work=262144,syscalls=128),
                                         duration_ns=30000000000)
            c._chunks = book.reserve_phase('chunk',c,dict(work=262144,syscalls=64,source_io=65537),
                                          duration_ns=30000000000)
            c._helper = book.reserve_phase('helper',c,dict(work=65536),duration_ns=30000000000)
            c._provider = validate_provider(source)
            c._parent = ParentLease.acquire(book.parent_path,book.reserve_ledger_operation(
                'acquire-parent',book.parent_path,OperationLimits(fds=4)))
            c._ledger = OwnedLedger.create(c._parent,book.basename,book.reserve_ledger_operation(
                'create-ledger',(c._parent,book.basename),OperationLimits(fds=1)))
            from .publisher import prepare
            c._physical,c._binaries = prepare(c)
            # Eight finite future ledger updates plus funded protocol must still fit.
            spent=book.observation()['spent']
            needed=dict(syscalls=32768+8*512,work=4194304+8*262144,
                        source_io=4194304+8*16385,prepared_bytes=1048576+8*(4*8192+1048576),
                        journal_events=8,journal_bytes=8*8192,wire_bytes=65536,messages=256,polls=4096)
            if any(spent[k]+v>DIMENSIONS[k] for k,v in needed.items()):
                raise Refusal('ControllerRosterFit')
            c._workspace=book.parent_path+'/p-'+book.basename[:16]
            if len(os.fsencode(c._workspace+'/qmp.sock'))>=108:
                raise Refusal('ControllerEndpointFit')
            c._fixtures={name:(path,size,digest) for name,path,size,digest in source.fixtures}
            master=c._fixtures['master.bin']
            expected_master=MASTER_UNIT*MASTER_COUNT
            if master[1]!=len(expected_master) or master[2]!=hashlib.sha256(expected_master).hexdigest():
                raise Refusal('TestMasterBinding')
            c._expected_size=master[1]+len(SUFFIX)
            digest=hashlib.sha256()
            for offset in range(0,c._expected_size,16384):
                digest.update(c._expected_part(offset,min(16384,c._expected_size-offset)))
            c._expected_hash=digest.hexdigest()
            c._record('AUTHORIZED')
            c._checkpoint('handoff')
            return c
        except BaseException:
            book.halt('ControllerOpenFailed')
            c.close()
            raise

    def _expected_part(self,offset,size):
        base=len(MASTER_UNIT)*MASTER_COUNT
        if not 0<=size<=16384 or not 0<=offset<=self._expected_size or offset+size>self._expected_size:
            raise Refusal('ExpectedByteRange')
        return bytes(MASTER_UNIT[i%len(MASTER_UNIT)] if i<base else SUFFIX[i-base]
                     for i in range(offset,offset+size))

    def _checkpoint(self,name):
        if self._plan is not None and self._plan.checkpoint==name:
            print(json.dumps(dict(checkpoint=name,test_only=True,leaf=self._book.leaf)),flush=True)
            time.sleep(.4)
            self._book._check()

    def _record(self,state):
        p=self._book.reserve_ledger_operation('update-record',self._ledger,
            OperationLimits(syscalls=512,work=262144,io=16385))
        facts=dict(test_only=True,order=self._order,original_qualification=False,
                   physical_released=self._physical_released,notified=self._notified,
                   rpc_calls=self._rpc_calls,measurement='bounded-original-v2')
        self._ledger.write_json(self._book.record(state,facts,p),p)

    def _p(self,operation,*args):
        _require_context(self)
        if self._rpc_calls>=(384 if operation=='close' else 383):
            raise Refusal('ControllerRPCBound')
        self._source.verify(self._p_meter,self)
        self._p_meter.charge(self,work=1)
        self._rpc_calls+=1
        if operation=='identity':
            result=self._process.verify_current()
        elif operation=='finish':
            result=self._process.finish(*args)
        else:
            names={'capture':'capture','prepare':'prepare','tool':'tool','mutate':'mutate',
                   'launch':'launch','usage':'usage','snapshot':'snapshot','seal':'seal_stopped',
                   'derive':'derive_readonly','chunk':'read_chunk','close':'close'}
            if operation not in names or self._session is None or self._session_closed:
                raise Refusal('ControllerOperation')
            if operation=='close':
                self._session_closed=True  # One terminal attempt, even if its result is lost.
            result=getattr(self._session,names[operation])(*args)
            if operation=='close':
                self._close_facts=result
        self._source.verify(self._p_meter,self)
        return result

    def _workspace_files(self, usage):
        # Observation only, never a reconstructed P/file capability. The actual
        # retained Session created this source-selected no-clobber workspace.
        if usage.current_fds+1>64:
            raise Refusal('ObservationFDHeadroom')
        self._p_meter.charge(self,syscalls=16,work=32)
        fd=os.open(self._workspace.rsplit('/',1)[1],os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,
                   dir_fd=self._parent._chain[-1][0])
        count=entries=0
        try:
            root=os.fstat(fd)
            if not stat.S_ISDIR(root.st_mode) or root.st_uid!=os.getuid():
                raise Refusal('WorkspaceObservation')
            with os.scandir(fd) as stream:
                for entry in stream:
                    entries+=1
                    if entries>10:raise Refusal('WorkspaceObservation')
                    st=entry.stat(follow_symlinks=False)
                    if stat.S_ISREG(st.st_mode):
                        if st.st_nlink!=1:raise Refusal('WorkspaceObservation')
                        count+=1
                    elif not stat.S_ISSOCK(st.st_mode):raise Refusal('WorkspaceObservation')
            if count>8:raise Refusal('WorkspaceObservation')
            return count
        finally:
            os.close(fd)

    def _observe_usage(self):
        u=self._p('usage')
        if (u.origin!=self._book.origin_ns/1e9 or u.end!=self._book.end_ns/1e9 or
                not u.journal_durable or u.control_wire_bytes+u.reserved_response_bytes>33554432 or
                u.control_messages+u.reserved_response_messages>1200):
            raise Refusal('ProviderUsageBinding')
        if self._last_usage is not None:
            previous=self._last_usage
            for name in ('source_io','prepared_bytes','charged_operations','control_wire_bytes',
                         'control_messages','polls','output_bytes','journal_events','journal_bytes'):
                if getattr(u,name)<getattr(previous,name):
                    raise Refusal('ProviderCounterReset')
            if u.session_id!=previous.session_id:
                raise Refusal('ProviderSessionChanged')
        rows=u.actor_fds
        if (len({(p,t) for p,t,_ in rows})!=len(rows) or sum(n for _,_,n in rows)!=u.current_fds or
                not any(p==os.getpid() for p,_,_ in rows)):
            raise Refusal('ProviderActorBinding')
        # P already counts coordinator: never add its RSS/process/FD a second time.
        # Workspace files have a separate frozen8-file P ceiling + actual E files.
        provider_files=self._workspace_files(u)
        current=dict(processes=u.current_processes,rss_bytes=u.current_rss,
                     fds=u.current_fds,files=len(self._book._created_regular)+provider_files)
        peaks=dict(processes=u.peak_processes,rss_bytes=u.peak_rss,
                   fds=u.peak_fds,files=current['files'])
        observation=_source_live_observation(self._book,self,current,peaks,
                    'RETAINED_BOUND_ACTOR_SET',int(u.observed_monotonic*1e9))
        self._book.record_live(observation)
        self._last_usage=u
        self._usage_rows.append(dict(sequence=u.sequence,wire=u.control_wire_bytes,
            reserved_wire=u.reserved_response_bytes,messages=u.control_messages,
            broker_source_io=u.source_io,polls=u.polls,processes=u.current_processes,
            rss=u.current_rss,fds=u.current_fds))
        return u

    def _require_stopped(self):
        s=self._stopped
        if (type(s) is not _StoppedRun or s not in self._stop_objects or s.context is not self or
                s.session is not self._session or s.process is not self._process or
                s.source!=self._source.source_hash or s.plan!=self._plan.digest() or
                self._stage_order is None or self._quit_order is None or
                not self._stage_order<self._quit_order<s.order):
            raise Refusal('StoppedAuthorityRequired')
        return s

    def _finish_and_collect_stop(self):
        if self._stopped is not None or self._quit_order is None:
            raise Refusal('StopOnce')
        self._record('STOP_COLLECTING')
        exited=self._p('finish',2)
        if (not exited.reaped or exited.exit_code!=0 or exited.signals_issued or
                exited.owned_session_remaining or exited.created_pid!=self._identity.pid or
                exited.startticks!=self._identity.startticks):
            raise Refusal('StoppedUnproved')
        self._order+=1
        stopped=_StoppedRun(_KEY,self,exited)
        self._stop_objects.add(stopped)
        self._stopped=stopped
        self._record('STOPPED_ISSUED')
        self._checkpoint('stop-retained')

    def _export_required(self):
        self._require_stopped()
        p=self._provider
        snapshot=self._p('snapshot',self._working)
        if snapshot.size!=self._expected_size or snapshot.sha256!=self._expected_hash:
            raise Refusal('StoppedExpectedBytes')
        self._stopped_snapshot=snapshot
        self._working=snapshot.successor
        sealed=self._p('seal',self._working)
        self._sealed=sealed
        self._record('EXPORTING')
        self._helper.charge(self,work=1)
        self._p_meter.charge(self,commands=1)
        toolpath=self._fixtures['fixture'][0]
        spec=p.DerivationSpec(self._tool,(toolpath,'derive',p.ResourceArgument('',sealed,''),
            p.OutputArgument(0),p.OutputArgument(1),p.OutputArgument(2),self._plan.scenario),
            (p.OutputSpec('export.bin',65536),p.OutputSpec('empty.bin',0),
             p.OutputSpec('absent.bin',0,False)),budget=p.JobBudget(seconds=2,io_bytes=5242880,
             output_bytes=1024,processes=8,rss_bytes=268435456,fds=64))
        self._derived=self._p('derive',(sealed,),spec)
        b=self._derived
        if (len(b.artifacts)!=2 or len(b.outputs)!=3 or b.helper_exit.exit_code!=0 or
                not b.helper_exit.reaped or b.helper_exit.signals_issued or
                b.helper_exit.owned_session_remaining or b.supervisor_pid!=self._worker_pid or
                b.outputs[0].size!=self._expected_size or b.outputs[0].sha256!=self._expected_hash or
                b.outputs[1].size!=0 or b.outputs[1].sha256!=hashlib.sha256(b'').hexdigest() or
                not b.outputs[2].expected_absent or not b.outputs[2].absence_proved):
            raise Refusal('DerivedExpectedOutputs')
        self._checkpoint('exported')
        for binary in self._binaries:
            self._outputs.append(binary.publish())
        self._checkpoint('published')

    def _verify_master(self):
        path,size,expected=self._fixtures['master.bin']
        fd=_call(self._chunks,self,os.open,path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
        digest=hashlib.sha256();total=0
        try:
            before=_call(self._chunks,self,os.fstat,fd)
            for _ in range(9):
                self._chunks.charge(self,source_io=4096,work=4096)
                raw=_call(self._chunks,self,os.read,fd,4096)
                if not raw:break
                total+=len(raw);digest.update(raw)
            after=_call(self._chunks,self,os.fstat,fd)
            linked=_call(self._chunks,self,os.stat,path,follow_symlinks=False)
            fields=lambda st:(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
            if fields(before)!=fields(after) or fields(after)!=fields(linked) or total!=size or digest.hexdigest()!=expected:
                raise Refusal('ImmutableMasterChanged')
        finally:
            _call(self._chunks,self,os.close,fd)

    def run_leaf(self):
        _require_context(self)
        if self._ran:
            raise Refusal('ControllerRunOnce')
        self._ran=True
        p=self._provider
        try:
            self._physical.acquire()
            self._checkpoint('prelaunch')
            envelope=p.SharedEnvelopePolicy(self._book.origin_ns/1e9,self._book.end_ns/1e9,
                source_io=67108864,prepared_bytes=65536,commands=3,output_bytes=16384,
                control_messages=1200,control_wire_bytes=33554432,polls=8192,
                measurement_completion='bounded-original-v2')
            stream=p.StreamPolicy(file_bytes=1048576,source_bytes=2097152,copied_bytes=65536,
                resources=1,sources=4,files=8,workspace_bytes=1048576,io_bytes=67108864,
                operation_seconds=2,preparation_seconds=2,resource_fds=8)
            managed=p.ManagedPolicy(total_seconds=5,startup_seconds=2,readiness_seconds=10,
                session_seconds=30,command_seconds=2,stream_bytes=1024,output_bytes=16384,polls=8192)
            # Public open_session has a keyword-only envelope; the exact approved
            # entry is called directly here, with the already funded SAME book.
            self._source.verify(self._p_meter,self)
            self._rpc_calls+=1
            self._session=p.open_session(p.NewWorkspace(self._workspace),stream,managed,envelope=envelope)
            self._source.verify(self._p_meter,self)
            usage=self._observe_usage()
            workers=[pid for pid,_,_ in usage.actor_fds if pid!=os.getpid()]
            if len(workers)!=1:
                raise Refusal('ProviderWorkerBinding')
            self._worker_pid=workers[0]
            masterpath,mastersize,masterhash=self._fixtures['master.bin']
            toolpath,toolsize,toolhash=self._fixtures['fixture']
            master=self._p('capture',p.SourceRequest(masterpath,mastersize,masterhash))
            toolsource=self._p('capture',p.SourceRequest(toolpath,toolsize,toolhash))
            self._working=self._p('prepare',master,'working.bin')
            self._tool=self._p('tool',toolsource)
            self._p_meter.charge(self,commands=1)
            mutation=self._p('mutate',self._working,p.MutationSpec(self._tool,
                (toolpath,'mutate',p.ResourceArgument('',self._working,'')),immutable_inputs=(master,)))
            if (mutation.status!='COMMITTED' or mutation.after_epoch!=mutation.before_epoch+1 or
                    not mutation.immutable_inputs_unchanged or mutation.exit_code!=0):
                raise Refusal('MutationSuccessor')
            self._mutation=mutation
            self._working=mutation.successor
            self._observe_usage()
            self._p_meter.charge(self,commands=1)
            self._process=self._p('launch',p.LaunchSpec(self._tool,
                (toolpath,'serve',p.ResourceArgument('',self._working,''),'qmp.sock',self._plan.scenario)),
                (self._working,))
            self._identity=self._p('identity')
            self._owned_ns=int(self._identity.observed_monotonic*1e9)
            self._record('RUNNING')
            self._observe_usage()
            from .protocol import connect
            with connect(self) as (codec,audit):
                stage=codec.execute('query-test-stage')
                if stage!={'stage':'WORDLING_TEST_READY'}:
                    raise Refusal('TestStageUnproved')
                self._order+=1;self._stage_order=self._order
                audit.quit_armed=True
                result=codec.execute('quit')
                audit.quit_armed=False
                if type(result) is not dict or result:
                    raise Refusal('QuitReplyUnproved')
                self._order+=1;self._quit_order=self._order
                self._protocol_facts=audit.facts()
            self._finish_and_collect_stop()
            self._observe_usage()
            self._export_required()
            self._observe_usage()
            outcome=self._p('close')
            if not outcome.supervisor_reaped or outcome.first_fault is not None:
                raise Refusal('ProviderContainmentUnproved')
            self._verify_master()
            self._physical.release()
            self._physical_released=True;self._release_ns=time.monotonic_ns()
            self._record('PHYSICAL_RELEASED')
            print(json.dumps(dict(event='PHYSICAL_TEST_RELEASED',leaf=self._book.leaf,
                                  released_ns=self._release_ns,test_only=True)),flush=True)
            self._notified=True;self._notify_ns=time.monotonic_ns()
            self._checkpoint('physical-released')
            self._audit_ns=time.monotonic_ns()
            if not self._release_ns<=self._notify_ns<=self._audit_ns:
                raise Refusal('ReleaseAuditOrder')
            self._record('AUDITING')
            print(json.dumps(dict(event='TEST_AUDIT_STARTED',leaf=self._book.leaf,test_only=True)),flush=True)
            raw=json.dumps(self._outputs,sort_keys=True).encode('ascii')
            self._audit.charge(self,work=len(raw))
            self._audit_digest=hashlib.sha256(raw).hexdigest()
            self._audit.close(self)
            self._checkpoint('audited')
            self._record('COMPLETE')
            self._checkpoint('report')
            return self._report('TEST_LEAF_COMPLETE')
        except BaseException as error:
            self._failure=getattr(error,'code',type(error).__name__)
            self._book.halt(self._failure)
            raise

    def _report(self,status):
        return dict(status=status,test_only=True,original_qualification=False,run_leaf=True,
            leaf=self._book.leaf,measurement_completion='bounded-original-v2',
            source=self._source.source_hash,plan=self._plan.digest(),outputs=list(self._outputs),
            positive_absence=bool(self._derived and self._derived.outputs[2].absence_proved),
            protocol=dict(self._protocol_facts),rpc_calls=self._rpc_calls,
            provider_diagnostics=dict(supervisor_pid=getattr(self,'_worker_pid',None),
                original_pid=self._identity.pid if hasattr(self,'_identity') else None,
                mutator_pid=self._mutation.tool_identity.pid if hasattr(self,'_mutation') else None,
                mutation_epochs=[self._mutation.before_epoch,self._mutation.after_epoch] if hasattr(self,'_mutation') else None,
                helper_pid=self._derived.helper_identity.pid if self._derived else None,
                helper_supervisor_pid=self._derived.supervisor_pid if self._derived else None,
                stage_order=self._stage_order,quit_order=self._quit_order,
                stop_order=self._stopped.order if type(self._stopped) is _StoppedRun else None,
                snapshot_epoch=self._stopped_snapshot.epoch if hasattr(self,'_stopped_snapshot') else None),
            usage=list(self._usage_rows),physical_released=self._physical_released,
            notified=self._notified,release_ns=self._release_ns,notify_ns=self._notify_ns,
            audit_ns=self._audit_ns,failure=self._failure,account=self._book.observation(),
            workspace_file_ceiling=13,last_complete_file_scope='E retained files + observed P workspace; terminal frozen issuer sampler is COORDINATOR_ONLY',
            exit_limits=dict(identity_at_exit_unproved=self._stopped.exit.identity_at_exit_unproved if type(self._stopped) is _StoppedRun else None,
                             daemon_state=self._stopped.exit.daemon_state if type(self._stopped) is _StoppedRun else 'UNKNOWN',normal_DOS=False),
            control_capacity=dict(rpcs=384,wire_bytes=33554432,messages=1200,
                                  code_rehash_and_broker_io_reservation=3221225472))

    def close(self):
        _require_context(self)
        failures=[]
        if self._session is not None and not self._session_closed:
            try:
                self._rpc_calls+=1  # Already reserved terminal close RPC, never another Session.
                self._close_facts=self._session.close()
                self._session_closed=True
                if not self._close_facts.supervisor_reaped:failures.append('SupervisorUnreaped')
            except BaseException as error:
                failures.append(getattr(error,'code',type(error).__name__))
        for resource in (*self._binaries,self._physical):
            if resource is not None and not resource.closed:
                try:resource.close()
                except (Refusal,OSError) as error:failures.append(str(error))
        for resource in (self._ledger,self._parent):
            if resource is not None:
                try:resource.close(self._book.reserve_ledger_operation('cleanup-close',resource,
                                                                     resource.close_requirements()))
                except (Refusal,OSError) as error:failures.append(str(error))
        try:
            self._issuer.finish(self._book)
        except (Refusal,OSError) as error:failures.append(str(error))
        self._closed=True
        _ACTIVE.remove(self)
        if failures:
            self._failure='ControllerCleanupIncomplete'
            raise Refusal('ControllerCleanupIncomplete',partial=True)
        return dict(closed=True,physical_qualified_release=self._physical_released,
                    unresolved_safety_hold=not self._physical_released,account=self._book.observation())
