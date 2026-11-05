"""One finite closed public installed campaign; no mutant qualification on red baseline."""
import argparse
import fcntl
import hashlib
import json
import os
import re
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time
from runtime_qualification import preflight, evidence_budget, write_json, bounded_json_loads, error_tag, emit_diagnostic, pin
from controller_deployment import deploy, MASTER
from runtime_qualification import CAMPAIGN_MUTANTS as MUTANTS, CAMPAIGN_CONFIGURED
from runtime_qualification import (current_campaign, campaign_bootstrap,
    _campaign_runtime, _campaign_case_root, _actual_campaign, _entry_data_boundary, _entry_data_initialize, _entry_data_actual, _EntryDataBoundary)

S=Path(__file__).resolve().parent.parent
REPO=S.parents[3]
_CURRENT_SCOPE=None


def stable(grant):
    h=hashlib.sha256()
    for v in ('wordling.spent-ticket/v1','wordling.TEST.ledger/v1','wp70-v1',grant):
        b=v.encode('ascii');h.update(len(b).to_bytes(4,'big')+b)
    return h.hexdigest()


def json_lines(raw):
    """Bytes splitlines semantics, retaining one bounded line at a time."""
    start=0;end=len(raw)
    while start<end:
        stop=start
        while stop<end and raw[stop] not in (10,13):stop+=1
        yield raw[start:stop]
        if stop<end and raw[stop]==13 and stop+1<end and raw[stop+1]==10:stop+=1
        start=stop+1


def final_json(raw,temporary=False):
    # Preserve the last successfully decoded VALUE (also scalars), original
    # duplicate-key semantics and original caught errors. Guard failures still
    # propagate. Retain a span, not every decoded diagnostic tree.
    last=None;offset=0
    for line in json_lines(raw):
        try:
            value,token=(_CURRENT_SCOPE.decode(line,temporary=True) if _CURRENT_SCOPE is not None else (bounded_json_loads(line,2097152),None))
            del value
            if token is not None:_CURRENT_SCOPE.release_temporary(token)
            last=(offset,len(line))
        except (ValueError,UnicodeError):pass
        offset+=len(line)
        if offset<len(raw) and raw[offset]==13:offset+=1
        if offset<len(raw) and raw[offset]==10:offset+=1
    if last is None:return (None,None) if temporary else None
    piece=raw[last[0]:last[0]+last[1]]
    value,token=(_CURRENT_SCOPE.decode(piece,temporary=temporary) if _CURRENT_SCOPE is not None else (bounded_json_loads(piece,2097152),None))
    return (value,token) if temporary else value


class Case:
    def __init__(self,name,folder,interpreter,inventory,root):
        self._readonly_fields(current_campaign(),name,folder,interpreter,inventory,root)
        folder.mkdir(parents=True)

    def _readonly_fields(self,campaign,name,folder,interpreter,inventory,root):
        global _CURRENT_SCOPE
        if not _actual_campaign(campaign)and not _entry_data_actual(campaign):raise RuntimeError('ActualReadonlyCaseProducerRequired')
        self.start=time.monotonic();self.campaign=campaign;self.end=min(self.start+30,self.campaign.traffic_end/1000000000)
        self.name,self.folder,self.interpreter,self.inventory,self.root=name,folder,interpreter,inventory,root
        if _CURRENT_SCOPE is not None:raise RuntimeError('OverlappingCaseScope')
        self.scope=self.campaign.begin_case(name,folder,interpreter,inventory,root,self.start)
        _CURRENT_SCOPE=self.scope
        self.output=0;self.calls=[];self.release_probe=None

    def check_clock(self):
        if time.monotonic()>=self.end:raise RuntimeError('CaseDeadline')

    def close_after_frame(self):
        global _CURRENT_SCOPE
        if _CURRENT_SCOPE is not self.scope:raise RuntimeError('CaseScopeIdentity')
        _CURRENT_SCOPE=None;self.scope.close_after_frame();self.campaign.end_case(self.scope)

    def checkpoint_seen(self,out,wanted):
        for line in json_lines(out):
            value,token=final_json(bytes(line),temporary=True)
            try:
                if value and value.get('checkpoint')==wanted:return True
            finally:
                del value
                if token is not None:self.scope.release_temporary(token)
        return False

    def retain_call(self,path,result):
        # The complete literal whole remains in its reserved file. Aggregate
        # state carries only finite source-owned references, never its tree.
        if len(self.calls)>=5:raise RuntimeError('CaseCallCardinality')
        self.calls.append(dict(path=str(path),**pin(path),exit=result['exit'],failure=result['failure']))

    def run(self,argv,label,kill_checkpoint=None,probe_release=False,env_extra=None,cwd=None,*,fsize=2097152):
        try:
            preflight(self.interpreter,self.inventory)
            token=self.scope.begin_capture(2097152-self.output)
            _entry_data_boundary(self)
            result=self._capture(argv,label,kill_checkpoint,probe_release,env_extra,cwd,fsize)
            # _capture has returned: its bytearrays/selector/receipt locals no
            # longer retain the copied ordinary bytes returned to this caller.
            self.scope.end_capture(token,result)
            return result
        except BaseException:
            self.campaign.fatal('CaseCaptureFailure');raise

    def _capture(self,argv,label,kill_checkpoint=None,probe_release=False,env_extra=None,cwd=None,fsize=2097152):
        if not _actual_campaign(self.campaign):raise RuntimeError('ProductionCaptureIdentityRequired')
        self.check_clock()
        allowed=self.end-time.monotonic()
        if allowed<=0:raise RuntimeError('CaseDeadline')
        env=dict(PATH='/usr/bin:/bin',HOME=str(Path(self.campaign.descriptor['root'])/'home'),LANG='C.UTF-8',LC_ALL='C.UTF-8')
        if env_extra:env.update(env_extra)
        cwd=cwd or Path(self.campaign.descriptor['root'])
        base=self.folder/label
        spec=dict(argv=argv,cwd=str(cwd),env=env,remaining_seconds=allowed,kill_checkpoint=kill_checkpoint,
                  live_combined_remaining=2097152-self.output,file_ceiling=fsize)
        write_json(base.with_suffix('.command.json'),spec)
        budget=evidence_budget();budget.reserve([base.with_suffix('.whole.json')],'pair',65536)
        allocation,handles=budget.raw_group([base.with_suffix('.stdout'),base.with_suffix('.stderr')],'functional_raw',2097152,shared=str(self.folder))
        try:
            self.check_clock()
            p=self.campaign.launch(self.campaign.case_slot(label),argv,cwd,env,int(self.end*1000000000),fsize=fsize)
        except BaseException as error:
            self.campaign.fatal('CaseLaunchFailure')
            for handle in handles.values():handle.close()
            result=dict(argv=argv,exit=None,failure='PopenOrGateFailure:'+type(error).__name__,child_started='UNKNOWN/no returned authorized handle',combined_case_output=self.output)
            budget.document(base.with_suffix('.whole.json'),result,'pair',pre_reserved=True);self.retain_call(base.with_suffix('.whole.json'),result)
            raise RuntimeError('CasePopenFailure') from None
        sel=selectors.DefaultSelector();out=bytearray();err=bytearray();sel.register(p.stdout,selectors.EVENT_READ,out);sel.register(p.stderr,selectors.EVENT_READ,err)
        begin=time.monotonic();killed=False;failure=None;checked=False
        try:
            while sel.get_map() or p.poll() is None:
                if time.monotonic()>=self.end:raise TimeoutError('CaseDeadline')
                for key,_ in sel.select(.02):
                    raw=os.read(key.fileobj.fileno(),65536)
                    if not raw:sel.unregister(key.fileobj);continue
                    handle=handles[base.with_suffix('.stdout' if key.data is out else '.stderr')]
                    budget.retain(allocation,key.data,handle,raw)
                    self.output=allocation['used']
                if kill_checkpoint and not killed:
                    if self.checkpoint_seen(out,kill_checkpoint):
                        self.campaign.signal_child(p,signal.SIGKILL);killed=True
                if probe_release and not checked and b'"checkpoint": "audited"' in out:
                    physical=Path(self.root+'-ledger')/(stable(self.name)[:48]+'.physical')
                    lock=Path(self.root)/'issuer.lock'
                    def available(path):
                        fd=os.open(path,os.O_RDWR|os.O_NOFOLLOW|os.O_CLOEXEC)
                        try:
                            try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);return True
                            except BlockingIOError:return False
                        finally:os.close(fd)
                    self.release_probe=dict(physical_free=available(physical),logical_free=available(lock))
                    checked=True
            p.wait(timeout=max(.001,min(1,self.end-time.monotonic())))
        except BaseException as e:
            failure=error_tag(e)
            self.campaign.fatal('CaseCaptureFailure')
        finally:
            if p.poll() is None:
                self.campaign.fatal('CaseUnsettledChild')
                # The first fault fixes the cleanup end. Registered direct-child
                # pidfd is the sole signal capability; protected P workers are
                # never group targets and no timeout starts a new grace period.
                cleanup_end=self.campaign.cleanup_end
                try:
                    if time.monotonic_ns()<cleanup_end:
                        self.campaign.signal_child(p,signal.SIGTERM)
                        try:p.wait(timeout=min(.25,max(0,(cleanup_end-time.monotonic_ns())/1000000000)))
                        except subprocess.TimeoutExpired:
                            if time.monotonic_ns()<cleanup_end:
                                self.campaign.signal_child(p,signal.SIGKILL)
                                try:p.wait(timeout=max(0,(cleanup_end-time.monotonic_ns())/1000000000))
                                except subprocess.TimeoutExpired:failure=failure or 'UNKNOWN_DIRECT_CHILD_CLEANUP'
                except BaseException as cleanup_error:failure=failure or error_tag(cleanup_error)
                if p.returncode is None:failure=failure or 'UNKNOWN_DIRECT_CHILD_CLEANUP'
            sel.close();p.stdout.close();p.stderr.close()
            for handle in handles.values():handle.close()
            self.output=allocation['used']
            result=dict(argv=argv,exit=p.returncode,elapsed=time.monotonic()-begin,killed_at_checkpoint=killed,
                        failure=failure,combined_case_output=self.output,release_probe=self.release_probe,
                        gate=self.campaign.child_facts(p),partial_prefix=failure is not None,
                        unretained_suffix='UNKNOWN' if failure is not None else None)
            budget.document(base.with_suffix('.whole.json'),result,'pair',pre_reserved=True);self.retain_call(base.with_suffix('.whole.json'),result)
        if failure:raise RuntimeError(failure)
        self.check_clock()
        self.campaign.complete_child(p,base.with_suffix('.whole.json'))
        return p.returncode,bytes(out),bytes(err)

    def base(self):return [str(self.interpreter),'-I','-B','-m','reference_controller']
    def admin(self):
        r=self.run(self.base()+['test-admin','--root',self.root,'--generation','wp68-v1' if self.name=='foundation-contract' else 'wp70-v1'],'admin')
        assert r[0]==0,'ADMIN_FAILED'

    def leaf(self,scenario='healthy',checkpoint=None,extra=None,grant=None,label='leaf',**kw):
        argv=self.base()+['test-leaf','--root',self.root,'--generation','wp70-v1','--grant-id',grant or self.name,'--scenario',scenario]
        if checkpoint:argv+=['--leaf-checkpoint',checkpoint]
        if extra:argv=extra+argv
        return self.run(argv,label,**kw)

    def positive(self,result):
        code,out,err=result;r=final_json(out)
        assert code==0 and r and r.get('status')=='TEST_LEAF_COMPLETE', 'PUBLIC_FULL_LEAF_NOT_COMPLETE:'+str(r)
        assert r['test_only'] and not r['original_qualification'] and r['run_leaf']
        assert r['physical_released'] and r['notified'] and r['positive_absence']
        assert r['release_ns']<=r['notify_ns']<=r['audit_ns']
        assert r['containment']['closed'] and r['account']['closed'] and not r['containment']['unresolved_safety_hold']
        assert r['account']['ledger_commits']==8 and r['account']['spent']['commands']==3
        assert r['account']['spent']['wire_bytes']==33554432+65536,'CUMULATIVE_WIRE_RESET'
        assert r['account']['spent']['source_io']>=3221225472
        assert r['rpc_calls']<=384 and r['account']['origin_ns']<r['release_ns']<r['account']['end_ns']
        p=r['provider_diagnostics'];assert p['supervisor_pid']==p['helper_supervisor_pid']
        assert len({p['original_pid'],p['mutator_pid'],p['helper_pid'],p['supervisor_pid']})==4
        assert p['mutation_epochs'][1]==p['mutation_epochs'][0]+1
        assert p['stage_order']<p['quit_order']<p['stop_order']
        assert r['protocol']['transactions']==3 and r['protocol']['received']<=65536
        assert r['exit_limits']==dict(identity_at_exit_unproved=True,daemon_state='UNKNOWN',normal_DOS=False)
        wanted=[MASTER+b'PREPARED\nSTOPPED\n',b'']
        for d,expected in zip(r['outputs'],wanted):
            assert '/' not in d['name'] and len(d['name'])<=64
            path=Path(self.root+'-ledger')/d['name'];raw=path.read_bytes()
            assert raw==expected and d['size']==len(expected) and d['sha256']==hashlib.sha256(expected).hexdigest()
            assert d['full_expected_bytes'] and d['durable_readback']
        assert r['outputs'][0]['chunks']>=2 and r['outputs'][1]['chunks']==1
        events=[]
        for line in json_lines(out):
            x=final_json(line)
            if x and 'event' in x:events.append(x.get('event'))
        assert events==['PHYSICAL_TEST_RELEASED','TEST_AUDIT_STARTED'],'RELEASE_NOTICE_ORDER'
        return r


def exercise(name,source,interpreter,inventory,root,folder,scenario_override=None):
    c=Case(name,folder,interpreter,inventory,root)
    try:result=_exercise(c,name,source,interpreter,inventory,root,folder,scenario_override)
    except BaseException:
        # An escaping traceback can retain _exercise/capture locals. Keep all
        # credit charged and abort; never release and enter another Case.
        c.campaign.fatal('EscapingCaseFrame');raise
    c.close_after_frame()
    return result


def _exercise(c,name,source,interpreter,inventory,root,folder,scenario_override=None):
    start=c.start
    try:
        c.admin()
        if name=='original-disabled':
            code,out,_=c.run(c.base()+['original','--grant-file','/tmp/never-inspect-Original-path'],'disabled')
            assert code==2 and final_json(out)['reason'].startswith('SourcePrelaunchBlocked')
        elif name=='api-contract':
            code,out,_=c.run([str(interpreter),'-I','-B',str(source/'tests/controller_api_probe.py'),root],'api')
            assert code==0 and final_json(out)['status']=='API_CONTRACT_PASS','API_CONTRACT_FAILED'
        elif name=='foundation-contract':
            for sub in ('copied-permit','wrong-issuer-permit','consumed-permit','full-phase-book'):
                code,_,_=c.run([str(interpreter),'-I','-B',str(source/'tests/api_cases.py'),sub,root],'foundation-'+sub)
                assert code==0,'FOUNDATION_PUBLIC_REFUSAL_OR_FULLSPEND'
        elif name.startswith('issuer-'):
            count=76 if name=='issuer-admitted-76' else 77 if name=='issuer-refused-77' else 0
            for i in range(count):(Path(root)/('%064x.spent'%i)).write_bytes(b'PERMANENT-FOREIGN-TEST')
            if name=='issuer-one-write-partial':
                marker=Path(root)/(stable(name)+'.spent')
                code,out,err=c.leaf(extra=['/usr/bin/strace','-qq','-yy','-e','trace=write'],fsize=1)
                assert code==2 and final_json(out)['reason']=='MarkerWriteAttempts' and b'INJECTED' not in err and re.search(rb'(?m)^write\([0-9]+<'+re.escape(str(marker).encode('utf8'))+rb'>, "wordling\.TEST\.spent/v1\\n[^"\n]*"(?:\.\.\.)?, 153\) = 1$',err) is not None
                assert marker.read_bytes()==b'w'
                assert not list(Path(root+'-ledger').iterdir())
            elif count==77:
                code,out,_=c.leaf();assert code==2 and final_json(out)['reason']=='IssuerTailFit'
                assert len(list(Path(root).glob('*.spent')))==77 and not list(Path(root+'-ledger').iterdir())
            else:c.positive(c.leaf())
        elif name in ('permanent-replay','changed-plan-same-id'):
            c.positive(c.leaf())
            parent=Path(root+'-ledger');before={str(p.relative_to(parent)):(p.read_bytes(),p.stat().st_ctime_ns) for p in parent.iterdir() if p.is_file()}
            code,out,_=c.leaf('bad-stage' if name=='changed-plan-same-id' else 'healthy',label='replay')
            assert code==2 and final_json(out)['status']=='REFUSED'
            assert before=={str(p.relative_to(parent)):(p.read_bytes(),p.stat().st_ctime_ns) for p in parent.iterdir() if p.is_file()},'REPLAY_EFFECT'
        elif name.startswith('loss-'):
            point=name[5:];code,out,_=c.leaf(checkpoint=point,kill_checkpoint=point)
            assert code==-signal.SIGKILL and any(final_json(x).get('checkpoint')==point for x in out.splitlines() if final_json(x))
            code,out,_=c.leaf(label='replay');assert code==2 and final_json(out)['status']=='REFUSED','LOST_CAPABILITY_RECONSTRUCTED'
            assert (Path(root)/(stable(name)+'.spent')).exists()
        elif name=='release-order':
            c.positive(c.leaf(checkpoint='audited',probe_release=True))
            assert c.release_probe==dict(physical_free=True,logical_free=False),'ACTUAL_RELEASE_BEFORE_AUDIT'
        elif name=='publisher-no-clobber':
            path=Path(root+'-ledger')/(stable(name)[:48]+'.bin');path.write_bytes(b'FOREIGN-FULL-PRIOR-BYTES');before=(path.read_bytes(),path.stat().st_ctime_ns)
            code,out,_=c.leaf();r=final_json(out);assert code==2 and not r['physical_released']
            assert before==(path.read_bytes(),path.stat().st_ctime_ns),'FOREIGN_PUBLICATION_CHANGED'
        elif name.startswith('kernel-publication-'):
            which=name[len('kernel-publication-'):]
            inject={'zero':'pwrite64:retval=0:when=6','fsync':'fsync:error=EIO:when=17','readback':'pread64:retval=0:when=15'}[which]
            code,out,err=c.leaf(extra=['/usr/bin/strace','-qq','-yy','-e','trace='+inject.split(':')[0],'-e','inject='+inject])
            r=final_json(out);assert code==2 and r and b'INJECTED' in err,'PUBLICATION_FAULT_NOT_APPLIED'
            assert not r['physical_released'],'OUTPUT_COMMIT_RELEASED'
        elif name=='hostile-path-cwd':
            hostile=folder/'hostile';hostile.mkdir();evidence_budget().literal(hostile/'startup_transport.py',b'raise RuntimeError("HOSTILE IMPORT")\n')
            c.positive(c.leaf(env_extra=dict(PYTHONPATH=str(hostile)),cwd=hostile))
        elif name in ('deployment-cached','deployment-foreign'):
            site=interpreter.parent.parent/'lib/python3.12/site-packages'
            if name=='deployment-cached':
                code,_,_=c.run([str(interpreter),'-I','-B','-c','import py_compile;py_compile.compile('+repr(str(site/'reference_controller/controller.py'))+',doraise=True)'],'make-real-cache')
                assert code==0
            else:(site/'foreign.pth').write_text('import os;os.abort()\n')
            try:preflight(interpreter,inventory)
            except RuntimeError:pass
            else:raise AssertionError('UNSAFE_DEPLOYMENT_LAUNCHED')
        else:
            scenario=scenario_override or ('healthy' if name=='healthy-b' else name)
            result=c.leaf(scenario)
            if scenario in ('healthy','partial-progress'):c.positive(result)
            elif scenario=='quit-exit-race' and result[0]==0:c.positive(result)
            else:
                r=final_json(result[1]);assert result[0]==2 and r and r['status']=='REFUSED','PROHIBITED_LEAF_COMPLETED'
                assert not r.get('physical_released',False),'UNPROVED_STOP_RELEASED'
        return dict(case=name,status='PASS',elapsed=time.monotonic()-start,calls=c.calls)
    except BaseException as error:
        return dict(case=name,status='FAIL',reason=error_tag(error),elapsed=time.monotonic()-start,calls=c.calls)




def _entry_data_frame(c,vector):
    """DATA references die with this frame BEFORE the genuine scope closes."""
    host=c.campaign
    if vector==2:
        raw_name=c.scope.hold(33024)
        raw=b'["'+b'x'*8188+b'","'+b'y'*8189+b'"]'
        c.scope.arena.shrink(raw_name,len(raw)+256);value,_=c.scope.decode(raw)
    observed=None
    try:c.run([], 'DATA-boundary')
    except BaseException as error:
        observed=dict(exception=type(error).__name__,fatal=host.aborted,reason=host.reason,boundary=host.boundary,
          inventory_hold=host.arena.holds.get('active-runtime188'),inventory_owners=c.scope.names.count('active-runtime188'),arena_used=host.arena.used,
          no_production=current_campaign_is_absent(),capture_holds=sum(n==5505024 for n in host.arena.holds.values()),hold_count=len(host.arena.holds))
    if observed is None:raise RuntimeError('EntryDataUnexpectedCaseSuccess')
    if vector in (1,2):
        wanted=2097152+host.baseline_expected_charge+5505024+(148000 if vector==2 else 0)
        if observed['exception']!='_EntryDataBoundary'or not observed['fatal']or observed['boundary']is None or observed['inventory_hold']is not None or observed['arena_used']!=wanted or observed['capture_holds']!=1:raise RuntimeError('EntryDataOrderingObservation')
    else:
        if observed['exception']!='RuntimeError'or not observed['fatal']or observed['reason']!='RuntimeInventoryAcquisitionFailure'or observed['boundary']is not None or observed['capture_holds']or observed['inventory_hold']!=host.inventory_expected_initial or observed['inventory_owners']!=1 or observed['arena_used']!=8180641:raise RuntimeError('EntryDataAcquisitionOwnership')
    if not observed['no_production']:raise RuntimeError('EntryDataProductionLeak')
    return observed


def current_campaign_is_absent():
    try:current_campaign()
    except RuntimeError:return True
    return False


def _entry_data_factory(vector,qsha,rsha,end,*,baseline_sha=None):
    host=_entry_data_initialize(vector,qsha,rsha,end,baseline_sha=baseline_sha);record=host.qualified[('baseline',0)]
    c=object.__new__(Case);folder=Path('/tmp/wordling-WP70-helper-io-controls-r11')
    c._readonly_fields(host,'DATA-entry-'+str(vector),folder,record.interpreter,record,str(folder))
    if vector==3:
        padding=8180641-2097152-host.baseline_expected_charge-host.inventory_expected_initial
        if not 0<=padding<=5478221 or host.inventory_expected_additional<=8388608-8180641:raise RuntimeError('R11EntrySameAcquisitionBoundary')
        host.arena.hold('DATA-padding',padding)
    observed=_entry_data_frame(c,vector)
    # The exercise/decoder/refusal frame and its traceback are now gone. No raw
    # or decoded DATA tree escapes in this finite primitive observation.
    c.close_after_frame();del c
    if vector==3:host.arena.release('DATA-padding')
    if host.arena.used!=2097152+host.baseline_expected_charge or len(host.arena.holds)!=2 or host.case is not None:raise RuntimeError('EntryDataPostFrameLeaseSettlement')
    return dict(vector=vector,status='PASS',DATA_only=True,P=False,TEST=False,production_identity=_actual_campaign(host),observed=observed,after_frame_arena=host.arena.used,source_boundary_before_children_or_writers=True)


def main(label):
    # The real owner creates the fixed roots and gates this same-PID runner.
    # Bootstrap restores CLOEXEC before any child-capable path is entered.
    campaign=campaign_bootstrap();start=campaign.start/1000000000
    if label!=campaign.descriptor['label']:raise RuntimeError('CampaignRunnerLabel')
    E=Path(campaign.descriptor['evidence']);T=Path(campaign.descriptor['root'])
    roster=bounded_json_loads((S/'tests/controller_roster.json').read_bytes())
    # Admission separately proved the actual closed40 namespace. Filter its
    # immutable keys as strings; create Paths only for these40 owned members,
    # without sorting/retaining the evidence subtree or20519 input Paths.
    owned_prefix=str(S)+os.sep
    source={str(Path(name).relative_to(S)):pin(name) for name in campaign.expected['files'] if name.startswith(owned_prefix)}
    roots={n:_campaign_case_root(campaign.descriptor,0,n) for n in roster['functional']}
    mutant_roots={n:_campaign_case_root(campaign.descriptor,index+1,MUTANTS[n][3]) for index,n in enumerate(roster['mutants'])}
    freeze=dict(source=source,roster=roster,cwd=str(T),functional_roots=roots,mutant_roots=mutant_roots,
        argv_template=['<actual-copied-interpreter>','-I','-B','-m','reference_controller','test-leaf','--root','<frozen-root>','--generation','wp70-v1','--grant-id','<case-name>'],
        static_selected_bound_path='/tmp/wordling-WP70-initial-preflight/source-fit-plan-r2.md',
        explicit_environment=dict(PATH='/usr/bin:/bin',HOME=str(T/'home'),LANG='C.UTF-8',LC_ALL='C.UTF-8',SETUPTOOLS_USE_DISTUTILS='stdlib'),
        tool_pins={p:pin(Path(p).resolve()) for p in ('/usr/bin/python','/usr/bin/cc','/usr/bin/strace')},
        counters=dict(rpcs=384,P_wire=33554432,P_messages=1200,P_polls=8192,code_rehash_and_broker_IO=3221225472),
        planned_mutants={n:dict(file=f,old=o,new=v,target=c,semantic_marker=m) for n,(f,o,v,c,m) in MUTANTS.items()})
    for n,(f,old,new,target,marker) in MUTANTS.items():
        text=(S/f).read_text();assert text.count(old)==1,('nonunique mutant',n,text.count(old));compile(text.replace(old,new),f,'exec')
        campaign.check()
    del text
    write_json(E/'frozen-input.json',freeze)
    del freeze
    outcomes=[];mutation=[];whole_exit=1
    try:
        interpreter,inventory=campaign.baseline()
        _,_,baseline_evidence=_campaign_runtime(campaign.descriptor)
        write_json(E/'runtime-before-first-P.json',dict(interpreter=str(interpreter),
            inventory_sha256=pin(baseline_evidence/'deployment-inventory.json')['sha256'],
            deployment_artifact=dict(path=str(baseline_evidence/'deployment.json'),**pin(baseline_evidence/'deployment.json')),
            baseline_readonly=True,frozen_source_unchanged=all(pin(S/p)==v for p,v in source.items())))
        for name in roster['functional']:
            campaign.check()
            i,inv=interpreter,inventory
            if name.startswith('deployment-'):
                context=campaign.prepare(0 if name=='deployment-cached' else 1)
                deploy(context.source,context.repository,context.target,context.evidence,context=context)
                i,inv=campaign.finish_preparation(context)
                del context
            result=exercise(name,S,i,inv,roots[name],E/'functional'/name)
            outcomes.append(result)
            print(json.dumps(dict(case=name,status=result['status'],reason=result.get('reason'))),flush=True)
            # First two actual full positives are critical baseline; do not
            # calibrate through other effects after an actual refusal/failure.
            if len(outcomes)<=2 and result['status']!='PASS':raise RuntimeError('ActualInitialBaselineFailure')
        if any(x['status']!='PASS' for x in outcomes):raise RuntimeError('FunctionalBaselineRed_NO_MUTANT_QUALIFICATION')
        mutation=[]
        for index,name in enumerate(roster['mutants']):
            campaign.check()
            f,old,new,target,marker=MUTANTS[name]
            context=campaign.prepare(index+2)
            deploy(context.source,context.repository,context.target,context.evidence,context=context)
            i,inv=campaign.finish_preparation(context)
            del context
            r=exercise(target,S,i,inv,mutant_roots[name],E/'mutants'/name/'case')
            status='KILLED' if r['status']=='FAIL' and marker in r.get('reason','') else 'SURVIVED' if r['status']=='PASS' else 'UNKNOWN'
            mutation.append(dict(mutant=name,status=status,target=r,marker=marker))
        assert all(x['status']=='KILLED' for x in mutation),'MUTANT_SURVIVOR_OR_UNKNOWN'
        configured=[]
        for name,argv in CAMPAIGN_CONFIGURED:
            c=Case(name,E/'configured'/name,interpreter,inventory,roots['healthy'])
            code,out,err=c.run(argv,'command',cwd=REPO);configured.append(dict(check=name,exit=code));assert code==0
            del code,out,err
            c.close_after_frame()
            del c
        write_json(E/'configured-results.json',configured)
        assert all(pin(S/p)==v for p,v in source.items()),'SourceChangedDuringCampaign'
        whole_exit=0
    except BaseException as error:
        campaign.fatal('CampaignRunnerFailure')
        raw=error_tag(error);evidence_budget().literal(E/'coordinator.stderr',raw.encode('utf8'));print(raw,file=sys.stderr,end='')
    finally:
        write_json(E/'functional-results.json',outcomes)
        write_json(E/'mutant-results.json',mutation)
        d=dict(argv=sys.argv,exit=whole_exit,elapsed=time.monotonic()-start,shared_end_seconds=600,
               functional_executed=len(outcomes),functional_pass=sum(x['status']=='PASS' for x in outcomes),
               original_qualification=False,mutants_qualified=whole_exit==0)
        write_json(E/'whole.json',d);print(json.dumps(d),flush=True)
    return whole_exit

if __name__=='__main__':
    try:
        if sys.argv[1:2]==['--case-entry-data']and len(sys.argv) in (6,7):
            print(json.dumps(_entry_data_factory(int(sys.argv[2]),sys.argv[3],sys.argv[4],int(sys.argv[5]),baseline_sha=sys.argv[6]if len(sys.argv)==7 else None)),flush=True);result=0
        else:
            p=argparse.ArgumentParser();p.add_argument('label');result=main(p.parse_args().label)
    except SystemExit as error:result=error.code
    except BaseException as error:emit_diagnostic(error);result=2
    raise SystemExit(result)
