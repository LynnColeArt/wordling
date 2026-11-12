"""Surviving preparation cleanup owner. No timeout process kills this owner.

All preparation tools inherit one owned coordinator group. Only that coordinator
is a new session. The independent owner stays outside it, adopts orphaned OWN
children, signals/reaps only that retained group and its own adopted descendants.
No P/issuer/grant or arbitrary caller PID is accepted.
"""
import argparse
import ctypes
import json
import math
import hashlib
import os
from pathlib import Path
import selectors
import signal
import socket
import subprocess
import time
try:
    from runtime_qualification import (EvidenceBudget, admit_capacity, load_expected, bounded_json_loads, generated_diagnostic, emit_diagnostic, pin)
except ModuleNotFoundError as error:
    # Isolated harmless controls use the standard loader at this ONE fixed
    # canonical sibling; no sys.path change, custom loader or module alias.
    if error.name!='runtime_qualification':raise
    import importlib.util
    import sys
    if '--qualify-r11'in sys.argv[1:]:
        if sys.pycache_prefix is not None or any((Path(__file__).parent/'__pycache__').glob('runtime_qualification.*.pyc')):raise RuntimeError('R11CachedSourceExcluded')
    spec=importlib.util.spec_from_file_location('runtime_qualification',Path(__file__).with_name('runtime_qualification.py'))
    module=importlib.util.module_from_spec(spec);sys.modules['runtime_qualification']=module;spec.loader.exec_module(module)
    from runtime_qualification import (EvidenceBudget, admit_capacity, load_expected, bounded_json_loads, generated_diagnostic, emit_diagnostic, pin)


class ControlFrames:
    """Bound pending frame BEFORE growth; original pipe bytes stay literal elsewhere."""
    def __init__(self):self.pending=bytearray();self.frames=0
    def feed(self,raw):
        messages=[]
        for byte in raw:
            if byte==10:
                self.frames+=1
                if self.frames>256:raise RuntimeError('SupervisorControlBound')
                messages.append(bounded_json_loads(bytes(self.pending),256));self.pending.clear()
            else:
                if len(self.pending)>=256:raise RuntimeError('SupervisorPendingFrameBound')
                self.pending.append(byte)
        return messages
    def finish(self):
        if self.pending:raise RuntimeError('SupervisorIncompleteControlFrame')
    def summary(self):
        return dict(bytes=len(self.pending),sha256=hashlib.sha256(self.pending).hexdigest(),contents='omitted diagnostic; literal retained control.raw is authoritative; unretained suffix UNKNOWN')


def supervise(argv,cwd,env,receipt,seconds=120,output_cap=98304,control=None,budget=None,fault=None,earlier_end=None,qualification=None):
    if not 0<seconds<=120 or not 0<output_cap<=98304:raise ValueError('EarlierLimitsOnly')
    if control not in (None,'kill-coordinator') or fault not in (None,'census-unavailable-on-cleanup'):raise ValueError('ClosedHarmlessControl')
    origin=time.monotonic();end=origin+seconds;receipt=Path(receipt)
    if qualification is not None:
        import runtime_qualification as q
        if not q._actual_cold_r11(qualification)or qualification.mode!='owner'or argv!=q._r11_child_argv(qualification.source_sha)or Path(cwd)!=q._R11_QUAL_ROOT or receipt!=q._R11_QUAL_ROOT/'owner'or budget is not qualification.budget or earlier_end!=qualification.end or seconds!=120 or output_cap!=98304 or control is not None or fault is not None:raise RuntimeError('R11ExactQualificationOwner')
        qualification.check();origin=qualification.start;end=qualification.end
    if earlier_end is not None:
        if type(earlier_end) not in (int,float) or not math.isfinite(earlier_end):raise RuntimeError('EarlierClockOnly')
        end=min(end,earlier_end)
        if origin>=end:raise RuntimeError('SupervisorEarlierDeadline')
    if fault is not None and (budget is None or not receipt.absolute().is_relative_to(Path('/tmp/wordling-WP70-v11-retention-controls'))):raise ValueError('ClosedHarmlessFaultScope')
    if budget is None:budget=admit_capacity(load_expected(),receipt)
    receipt.mkdir(mode=0o700,parents=True,exist_ok=False)
    budget.reserve([receipt/'whole.json'],'custody',65536)
    allocation,raw_handles=budget.raw_group([receipt/'stdout.raw',receipt/'stderr.raw',receipt/'control.raw'],'custody',98304)
    stopped=[];old={}
    def terminate(signum,frame):stopped.append(signum)
    try:
        libc=ctypes.CDLL(None,use_errno=True)
        if libc.prctl(36,1,0,0,0)!=0:raise OSError(ctypes.get_errno(),'PR_SET_CHILD_SUBREAPER')
        old={n:signal.signal(n,terminate) for n in (signal.SIGTERM,signal.SIGINT)}
        read,write=os.pipe2(os.O_CLOEXEC)
        env=dict(env,WORDLING_PREPARATION_CONTROL_FD=str(write),WORDLING_PREPARATION_ORIGIN=repr(origin),WORDLING_PREPARATION_END=repr(end))
        try:p=subprocess.Popen(argv,cwd=cwd,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,pass_fds=(write,),start_new_session=True)
        except BaseException:
            os.close(read);os.close(write);raise
        os.close(write)
    except BaseException as error:
        for handle in raw_handles.values():handle.close()
        for n,handler in old.items():signal.signal(n,handler)
        result=dict(reason='SupervisorPopenOrAdmissionFailure',diagnostic=generated_diagnostic(error,512),exit=None,cleanup_qualified=True,child_started=False)
        budget.document(receipt/'whole.json',result,'custody',pre_reserved=True)
        raise RuntimeError('SupervisorPopenOrAdmissionFailure') from None
    sel=selectors.DefaultSelector();out=bytearray();err=bytearray();control_raw=bytearray();decoder=ControlFrames()
    sel.register(p.stdout,selectors.EVENT_READ,out);sel.register(p.stderr,selectors.EVENT_READ,err);sel.register(read,selectors.EVENT_READ,control_raw)
    reason=None;partial=False;escalated=False;reaped=[];identity_events=[];active_end=end;cleanup_start=None;root_reserved=True;group_closed=False;killed=False;census_unknown=False;census_diagnostic=None;kernel_no_children=False;normal_leader_last=False;settled=False
    def observe_children():
        nonlocal census_unknown,census_diagnostic
        if census_unknown:return None
        try:
            if fault=='census-unavailable-on-cleanup' and cleanup_start is not None:raise RuntimeError('INJECTED own-child census unavailable')
            with open('/proc/self/task/'+str(os.getpid())+'/children','rb') as stream:raw=stream.read(4097)
            parts=raw.split()
            if len(raw)>4096 or len(parts)>256 or any(not n.isdigit() or len(n)>12 for n in parts):raise RuntimeError('OwnedChildrenObservationBound')
            return [int(n) for n in parts]
        except BaseException as error:
            census_unknown=True;census_diagnostic=generated_diagnostic(error,512);return None
    def root_exit():
        if not root_reserved:return True
        return os.waitid(os.P_PID,p.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT) is not None
    def signal_owned(sig):
        nonlocal group_closed,census_unknown,census_diagnostic
        if group_closed:return False
        try:
            # Actual unreaped Popen child relationship, NEVER a caller PID fact.
            proof=os.waitid(os.P_PID,p.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT)
        except BaseException as error:
            group_closed=True;census_unknown=True;census_diagnostic=generated_diagnostic(error,512);return False
        identity_events.append(dict(event='before_group_signal',leader=p.pid,signal=int(sig),retained_direct_child=True,waitid_WNOWAIT=None if proof is None else dict(pid=proof.si_pid,code=proof.si_code,status=proof.si_status)))
        try:os.killpg(p.pid,sig)
        except ProcessLookupError:pass
        children=observe_children()
        if children is not None:
            for pid in children:
                try:os.kill(pid,sig)
                except ProcessLookupError:pass
        return True
    def begin(cause):
        nonlocal reason,cleanup_start
        if cleanup_start is None:
            reason=cause;cleanup_start=time.monotonic();signal_owned(signal.SIGTERM)
    def reap_kernel_after_closed():
        nonlocal kernel_no_children,root_reserved
        # Only after the LAST safe group signal: no future PGID use, so own
        # kernel-returned child reaping cannot free a leader needed for signals.
        for _ in range(256):
            try:pid,status=os.waitpid(-1,os.WNOHANG)
            except ChildProcessError:kernel_no_children=True;return
            if not pid:return
            reaped.append(dict(pid=pid,status=status,kernel_owned_child=True))
            if pid==p.pid:
                p.returncode=os.waitstatus_to_exitcode(status);root_reserved=False
                identity_events.append(dict(event='leader_reaped_after_group_signals_CLOSED',leader=pid,leader_last='UNKNOWN because census unavailable'))
    def cleanup_tick(now):
        nonlocal escalated,killed,group_closed,root_reserved,normal_leader_last
        if now-cleanup_start>=.5 and not killed:
            attempted=signal_owned(signal.SIGKILL);killed=True;escalated=bool(attempted)
            if census_unknown:
                group_closed=True;identity_events.append(dict(event='group_signals_CLOSED',leader=p.pid,retained_leader_KILL_attempted=bool(attempted),census='UNKNOWN'))
        children=observe_children()
        if children is None:
            if killed or group_closed:
                group_closed=True;reap_kernel_after_closed()
                if kernel_no_children and not sel.get_map():return True
            return now-cleanup_start>=2
        for pid in children:
            if pid==p.pid:continue
            try:got,status=os.waitpid(pid,os.WNOHANG)
            except ChildProcessError:continue
            if got:reaped.append(dict(pid=got,status=status,kernel_owned_child=True))
        again=observe_children()
        if again is None:return False
        if root_exit() and not [pid for pid in again if pid!=p.pid] and not sel.get_map():
            group_closed=True;p.wait();root_reserved=False;normal_leader_last=True
            identity_events.append(dict(event='leader_reaped_LAST',leader=p.pid,other_owned_children=[],returncode=p.returncode));return True
        return now-cleanup_start>=2
    try:
        while True:
            now=time.monotonic()
            if cleanup_start is None:
                if stopped:begin('SupervisorSignal:'+str(stopped[0]))
                elif now>=min(end,active_end):begin('SharedOrCommandDeadline')
                elif root_exit():begin('CoordinatorExited')
            if cleanup_start is not None and cleanup_tick(now):settled=True;break
            for key,_ in sel.select(.01):
                fd=key.fileobj if isinstance(key.fileobj,int) else key.fileobj.fileno()
                channel='control.raw' if key.data is control_raw else 'stdout.raw' if key.data is out else 'stderr.raw'
                remaining=min(output_cap-allocation['used'],32768-len(key.data))
                raw=os.read(fd,min(4096,remaining+1))
                if not raw:
                    sel.unregister(key.fileobj)
                    if key.data is control_raw:
                        try:decoder.finish()
                        except RuntimeError:partial=True;begin('IncompleteControlFrameAtEOF')
                    continue
                kept=raw[:remaining];budget.retain(allocation,key.data,raw_handles[receipt/channel],kept)
                if len(kept)!=len(raw):partial=True;begin('SupervisorOutputOverflow')
                if key.data is control_raw:
                    try:
                        for message in decoder.feed(kept):
                            if type(message) is not dict:raise RuntimeError('SupervisorControlType')
                            if message.get('event')=='command':
                                if set(message)!={'event','end'} or type(message['end']) not in (int,float) or not math.isfinite(message['end']) or not origin<=message['end']<=end:raise RuntimeError('SupervisorControlClock')
                                active_end=min(end,float(message['end']))
                            elif message.get('event')=='idle':
                                if set(message)!={'event'}:raise RuntimeError('SupervisorControlFields')
                                active_end=end
                            elif message.get('event')=='abort':
                                if set(message)!={'event'}:raise RuntimeError('SupervisorControlFields')
                                begin('CoordinatorAbort')
                            else:raise RuntimeError('UnknownSupervisorControl')
                    except BaseException as error:
                        partial=True;begin('SupervisorControlFailure:'+generated_diagnostic(error,512)['text'])
            if control=='kill-coordinator' and time.monotonic()-origin>=.15 and cleanup_start is None:
                os.kill(p.pid,signal.SIGKILL);control=None
    except BaseException as error:
        partial=True;begin('SupervisorBoundedFailure:'+generated_diagnostic(error,512)['text'])
    finally:
        if cleanup_start is None:begin('SupervisorFinalDisposition')
        # Census refusal can NEVER escape before this retained-group kill path.
        while not settled and time.monotonic()-cleanup_start<2:
            if cleanup_tick(time.monotonic()):settled=True;break
            # Drain bounded remaining pipe prefixes; no decoding/authority after fatal.
            for key,_ in sel.select(.001):
                fd=key.fileobj if isinstance(key.fileobj,int) else key.fileobj.fileno();remaining=min(output_cap-allocation['used'],32768-len(key.data))
                raw=os.read(fd,min(4096,remaining+1))
                if not raw:sel.unregister(key.fileobj);continue
                channel='control.raw' if key.data is control_raw else 'stdout.raw' if key.data is out else 'stderr.raw'
                kept=raw[:remaining];budget.retain(allocation,key.data,raw_handles[receipt/channel],kept)
                if len(kept)!=len(raw):partial=True
        if not group_closed:
            signal_owned(signal.SIGKILL);group_closed=True;killed=True
        if census_unknown:reap_kernel_after_closed()
        final_children=None if census_unknown else observe_children()
        for n,handler in old.items():signal.signal(n,handler)
        sel.close();p.stdout.close();p.stderr.close();os.close(read)
        for handle in raw_handles.values():handle.close()
        result=dict(argv=argv,cwd=str(cwd),env=env,origin=origin,end=end,elapsed=time.monotonic()-origin,reason=reason,exit=p.returncode,escalated=escalated,
            retained_bytes=allocation['used'],output_cap=output_cap,partial_prefix=partial,unretained_suffix='UNKNOWN' if partial else None,control_tail=decoder.summary(),control_raw_reference=dict(path=str(receipt/'control.raw'),**pin(receipt/'control.raw')),
            reaped=reaped,leader_identity_events=identity_events,owned_children_remaining=final_children,owned_child_census='UNKNOWN' if census_unknown else 'OBSERVED',census_diagnostic=census_diagnostic,census_fault_injected=fault is not None,kernel_no_children_observed=kernel_no_children,
            cleanup_seconds=time.monotonic()-cleanup_start,cleanup_qualified=not census_unknown and final_children==[] and not root_reserved,coordinator_reaped_last=normal_leader_last,
            unknown_cleanup_hold=census_unknown or final_children is None or bool(final_children),uncatchable_owner_kill_not_claimed=True)
        budget.document(receipt/'whole.json',result,'custody',pre_reserved=True)
    return result



def supervise_r11_qualification(source_sha,*,earlier_end=None):
    import runtime_qualification as q
    start=time.monotonic();end=start+120
    if earlier_end is not None:
        if type(earlier_end)not in (float,int)or not math.isfinite(earlier_end):raise RuntimeError('R11EarlierQualificationEndOnly')
        end=min(end,earlier_end)
    record=q._begin_r11_cold(source_sha,'owner',start,end)
    root=q._R11_QUAL_ROOT
    if root.is_symlink()or not root.is_dir()or {p.name for p in root.iterdir()}!={'source'}or q._R11_TARGET.parent.exists()or q._R11_TARGET.parent.is_symlink():raise RuntimeError('R11FreshQualificationRoots')
    source=root/'source';names={'helper.py.txt','ARGV.json','CAPACITY.json','seal.json'}
    if source.is_symlink()or not source.is_dir()or {p.name for p in source.iterdir()}!=names:raise RuntimeError('R11QualificationSourceFour')
    path=source/'seal.json'
    if path.is_symlink()or path.stat().st_size>65536:raise RuntimeError('R11QualificationSourceSealBound')
    raw=path.read_bytes();seal=record.arena.decode('qualification-source-seal',raw,65536)
    if set(seal)!={'schema','source_prefix_sha256','members'}or seal['schema']!='wordling.wp70.r11-qualification-source4/v1'or seal['source_prefix_sha256']!=source_sha or set(seal['members'])!=names-{'seal.json'}:raise RuntimeError('R11QualificationSourceSeal')
    caps={'helper.py.txt':131072,'ARGV.json':65536,'CAPACITY.json':262144}
    for name,row in seal['members'].items():
        if set(row)!={'size','sha256','mode','uid','gid'}or row['size']>caps[name]or any(row[k]!=v for k,v in dict(mode=384,uid=1000,gid=1000).items()):raise RuntimeError('R11QualificationSourceRole')
        q.same(source/name,row)
    del raw,seal,row;record.arena.release('qualification-source-seal')
    budget=q.admit_capacity(record.expected,root/'owner',qualification=record)
    q._R11_TARGET.parent.mkdir(mode=0o700)
    env=dict(PATH='/usr/bin:/bin',HOME='/tmp',LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1',SETUPTOOLS_USE_DISTUTILS='stdlib',WORDLING_R11_OWNER_PID=str(os.getpid()))
    result=supervise(q._r11_child_argv(source_sha),root,env,root/'owner',budget=budget,earlier_end=end,qualification=record)
    if result['exit']!=0 or not result['cleanup_qualified']or result['unknown_cleanup_hold']or result['partial_prefix']or not result['coordinator_reaped_last']:raise RuntimeError('R11QualificationDispositionUNKNOWN')
    return 0


def supervise_campaign(source_sha):
    import runtime_qualification as q
    return _supervise_owner(q._campaign_owner_admission(source_sha),source_sha)


def _supervise_owner(campaign,source_sha):
    """Closed campaign owner. Only direct registered pidfds are signal authority.

    FD peak: stdio3 + raw3 + selector1 + SCM1 + root pidfd1 + active pidfd1;
    startup adds two private socketpairs and Popen pipes/error temporaries (<32).
    Invalid recvmsg descriptors (at most2) are immediately closed by q.
    owner-live is ONE 1MiB hold in the shared observation8MiB arena, not credit
    from the old pending512KiB, serializer16MiB, or restart1MiB reservations.
    """
    import select
    import runtime_qualification as q
    if (type(source_sha) is not str or len(source_sha)!=64 or
            any(c not in '0123456789abcdef' for c in source_sha)):
        raise RuntimeError('CampaignSourceSHA')
    control=q._actual_harmless_owner(campaign)
    if not control and not q._actual_campaign(campaign):raise RuntimeError('ActualOwnerProducerRequired')
    total_slots=(2 if campaign.group==1 else 1) if control else 199
    descriptor=campaign.descriptor;whole_end=campaign.end;traffic_end=whole_end-2000000000
    if type(whole_end) is not int or type(campaign.start) is not int or time.monotonic_ns()>=traffic_end:
        raise RuntimeError('CampaignOwnerClock')
    # Admission binds source/E before any target/evidence effect. Writer groups
    # are precharged by the genuine private owner record, never caller metadata.
    receipt=Path(descriptor['evidence'])/'owner';budget=None if control else campaign.budget
    paths={n:receipt/n for n in ('stdout.raw','stderr.raw','control.raw')}
    if not control:
        budget.reserve([receipt/'whole.json'],'custody',65536)
        budget.reserve(list(paths.values()),'custody',262144)
    if control:campaign.arena.hold('owner-live',1048576)
    elif campaign.arena.holds.get('joint-owner-source-live')!=1572864:raise RuntimeError('CampaignEarlyJointOwnerReservation')
    # 1MiB joint hold: raw bytearrays<=294912; retired199<=65536;
    # bounded census/split/int scratch<=196608; frame/decode<=65536;
    # selector/Popen/registry/receipt/serializer tails<=262144; margin163840.
    root=None;rootfd=None;active=None;control_owner=None;control_child=None
    release_owner=None;release_child=None;selector=None;raw_handles={}
    buffers={n:bytearray()for n in paths};allocation=None
    old_handlers={};stopped=[];spawn_attempted=False;root_retained=False
    reason=None;diagnostic=None;partial=False;census_unknown=False
    control_eof=False;hello=False;last_seq=0;retired=[];request_count=0;response_count=0
    active_end=traffic_end;cleanup_end=None;first_fault=None;barrier_end=None
    term_sent=False;kill_sent=False;signal_unknown=False;root_reaped_last=False
    reaped_count=0;reaped_digest=hashlib.sha256();final_children=None
    registered_exit_observed=False
    kernel_no_children=False;setup_complete=False;settlement_end=whole_end
    identity_events=[];stdio_eof_observed=False

    def now():return time.monotonic_ns()

    def identity(event,**facts):
        if len(identity_events)>=12:raise RuntimeError('CampaignIdentityMetadataBound')
        identity_events.append(dict(event=event,**facts))

    def root_exit():
        if root is None or not root_retained:return None
        return os.waitid(os.P_PID,root.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT)

    def live_root():
        if root is None or rootfd is None or not root_retained or root.returncode is not None:
            raise RuntimeError('CampaignRetainedRootRequired')
        if root_exit() is not None:raise RuntimeError('CampaignRootExitedBeforeACK')
        q._campaign_live(rootfd)

    def fd_exited(fd):
        poller=select.poll();poller.register(fd,select.POLLIN|select.POLLERR|select.POLLHUP)
        events=poller.poll(0)
        if any(flags&select.POLLNVAL for _,flags in events):raise RuntimeError('CampaignPidfdInvalid')
        return any(flags&select.POLLIN for _,flags in events)

    def census():
        nonlocal census_unknown
        try:
            with open('/proc/self/task/'+str(os.getpid())+'/children','rb')as stream:
                raw=stream.read(4097)
            pieces=raw.split()
            if len(raw)>4096 or len(pieces)>256 or any(not p.isdigit()or len(p)>12 for p in pieces):
                raise RuntimeError('CampaignOwnChildCensusBound')
            return [int(p)for p in pieces]
        except BaseException:
            census_unknown=True;raise

    def reap_other_exited():
        nonlocal reaped_count
        children=census()
        for pid in children:
            if root is not None and root_retained and pid==root.pid:continue
            observed=os.waitid(os.P_PID,pid,os.WEXITED|os.WNOHANG|os.WNOWAIT)
            if observed is None:continue
            # Kernel-own exited child relation only. This numeric value NEVER
            # authorizes a signal; no arbitrary adopted child is signaled.
            got,status=os.waitpid(pid,os.WNOHANG)
            if got:
                if got!=pid or reaped_count>=65536:raise RuntimeError('CampaignOwnReapBound')
                reaped_count+=1;reaped_digest.update((str(got)+':'+str(status)+'\n').encode('ascii'))
        return census()

    def retain(channel,raw):
        nonlocal partial
        maximum=196608 if channel=='control.raw'else 32768
        remaining=min(maximum-len(buffers[channel]),262144-allocation['used'])
        if remaining<0:raise RuntimeError('CampaignOwnerRawState')
        prefix=raw[:remaining]
        if prefix:
            if control:buffers[channel].extend(prefix);allocation['used']+=len(prefix)
            else:budget.retain(allocation,buffers[channel],raw_handles[paths[channel]],prefix)
        if len(prefix)!=len(raw):
            partial=True;raise RuntimeError('CampaignOwnerRawOverflow')

    def transcript(direction,raw,flags=0,credentials=1,fds=0):
        if type(raw) is not bytes or len(raw)>257:raise RuntimeError('CampaignTranscriptPayloadBound')
        if not 0<=flags<=4294967295 or not 0<=credentials<=2 or not 0<=fds<=2:
            raise RuntimeError('CampaignTranscriptAncillaryBound')
        # C headers contain actual received ancillary counts. O/G zero fields
        # mean no receive observation here, not absence of automatic kernel creds.
        header=(direction+' '+str(len(raw))+' '+str(flags)+' '+str(credentials)+' '+str(fds)+'\n').encode('ascii')
        if len(header)>64:raise RuntimeError('CampaignTranscriptHeaderBound')
        retain('control.raw',header);retain('control.raw',raw)

    def send(value,limit,gate=False):
        nonlocal response_count
        if cleanup_end is not None and value.get('k')!='b':raise RuntimeError('CampaignNoACKAfterAbort')
        if now()>=limit:raise RuntimeError('CampaignNoLateACK')
        live_root()
        if not gate:
            response_count=q._campaign_frame_count(response_count)
        channel=release_owner if gate else control_owner
        raw=q._campaign_send(channel,value,limit,maximum=128)
        transcript('G'if gate else'O',raw,credentials=0)
        if now()>=limit:raise RuntimeError('CampaignACKDeadline')

    def receive(limit):
        nonlocal request_count
        terminal_receive=(not control and hello and last_seq==total_slots==199
                          and len(retired)==199 and active is None)
        exited=root_exit()
        if terminal_receive and (root is None or rootfd is None or not root_retained or root.returncode is not None):
            raise RuntimeError('CampaignRetainedRootRequired')
        if exited is None:
            if not terminal_receive:live_root()
        elif not(hello and last_seq==total_slots and len(retired)==total_slots and active is None and exited.si_code==os.CLD_EXITED and exited.si_status==0):
            raise RuntimeError('CampaignRootExitBeforeClosedEOF')
        # The closed199 EOF race may be observed with retained exited root; it
        # never authorizes another ACK or message. Identity has not been reaped.
        try:value,fd,raw=q._campaign_recv(control_owner,(root.pid,os.getuid(),os.getgid()),limit,with_fd=None,maximum=256)
        except q._CampaignFrameError as error:
            # q already closed EVERY received descriptor on malformed data.
            if error.raw==b''and error.credentials_count==0 and error.fds_count==0:
                if not terminal_receive and error.flags==0:return None,None,b''
                if terminal_receive and error.ancillary_empty is True and error.flags in(0,socket.MSG_CMSG_CLOEXEC):
                    transcript('C',b'',error.flags,0,0)
                    return None,None,b''
            transcript('C',error.raw,error.flags,error.credentials_count,error.fds_count)
            raise
        try:
            if terminal_receive:live_root()
            request_count=q._campaign_frame_count(request_count)
        except BaseException:
            if fd is not None:os.close(fd)
            raise
        try:transcript('C',raw,fds=1 if fd is not None else 0)
        except BaseException:
            if fd is not None:os.close(fd)
            raise
        return value,fd,raw

    def begin_fault(cause,error=None,earlier_barrier=None):
        nonlocal reason,diagnostic,partial,first_fault,cleanup_end
        if first_fault is not None:return
        first_fault=now();reason=cause;partial=True
        # ROOT-ratified30+2 inside WHOLE300. Failed normal barrier NEVER renews.
        cleanup_end=min(first_fault+2000000000,active_end+2000000000,whole_end)
        if earlier_barrier is not None:cleanup_end=min(cleanup_end,earlier_barrier)
        try:campaign.fatal('OwnerAbort')
        except BaseException:
            # Local abort still closes every launch/ACK path; do not abandon
            # retained pidfd cleanup if the private latch unexpectedly refuses.
            diagnostic={'text':'GENERATED: campaign fatal latch UNKNOWN'}
        if error is not None:
            try:diagnostic=generated_diagnostic(error,512)
            except BaseException:diagnostic={'text':'GENERATED: diagnostic unavailable'}

    def drain_stdio(seconds):
        nonlocal partial
        if selector is None:return
        try:events=selector.select(seconds)
        except BaseException:
            if first_fault is None:raise
            partial=True;return
        for key,_ in events:
            if key.data=='control':continue
            channel=key.data
            try:
                raw=os.read(key.fileobj.fileno(),min(4096,max(0,32768-len(buffers[channel]))+1))
                if not raw:
                    selector.unregister(key.fileobj);key.fileobj.close()
                else:retain(channel,raw)
            except BaseException:
                if first_fault is None:raise
                partial=True
                # Failed capture plumbing is not authority to abandon registered
                # pidfd cleanup. Close only this unusable OWNED read end.
                try:selector.unregister(key.fileobj)
                except BaseException:pass
                try:key.fileobj.close()
                except BaseException:pass

    def barrier(limit,require_root=True):
        # One deadline for all wait/census/drain work, no extra grace at failure.
        while now()<limit:
            remaining=reap_other_exited()
            others=[pid for pid in remaining if root is None or not root_retained or pid!=root.pid]
            if not others:
                if require_root:live_root()
                return True
            drain_stdio(min(.01,max(0,(limit-now())/1000000000)))
        return False

    def close_active():
        nonlocal active,registered_exit_observed
        if active is not None:
            if fd_exited(active['fd']):registered_exit_observed=True
            os.close(active['fd']);active=None

    def signal_registered(sig):
        nonlocal signal_unknown
        if cleanup_end is None or now()>=cleanup_end:return
        if active is not None:
            try:
                if not fd_exited(active['fd']):
                    q._campaign_live(active['fd'])
                    if now()<cleanup_end:signal.pidfd_send_signal(active['fd'],sig)
            except BaseException:signal_unknown=True
        if rootfd is not None and root is not None and root_retained and now()<cleanup_end:
            try:q._campaign_signal(rootfd,sig,root)
            except BaseException:signal_unknown=True

    def process_message(value,fd,raw):
        nonlocal hello,last_seq,active,active_end,barrier_end,control_eof
        try:
            if value is None:
                # Empty EOF is not generic success; only closed199-slot protocol
                # may wait for actual root exit. It never mints another ACK.
                control_eof=True;selector.unregister(control_owner)
                if not hello or last_seq!=total_slots or len(retired)!=total_slots or active is not None:
                    raise RuntimeError('CampaignPrematureControlEOF')
                return
            if type(value)is not dict or value.get('n')!=descriptor['nonce']:
                raise RuntimeError('CampaignProtocolNonceOrType')
            kind=value.get('k')
            if kind=='H':
                if hello or fd is not None or set(value)!={'k','v','n','q','m'}or type(value['v'])is not int or value['v']!=1:
                    raise RuntimeError('CampaignHELLOShape')
                qpath=str(Path(q.__file__).resolve())
                if value['q']!=campaign.manifest['sources'][qpath]['sha256']or value['m']!=source_sha:
                    raise RuntimeError('CampaignHELLOSource')
                send({'k':'h','n':descriptor['nonce'],'e':whole_end},traffic_end);hello=True
            elif kind=='R':
                if not hello or active is not None or set(value)!={'k','v','n','s','i','e','c'}:
                    raise RuntimeError('CampaignREGISTERShape')
                expected_slot=last_seq+1 if control else q._campaign_slot_order(last_seq+1)
                seq,slot,end=q._campaign_registration_fields(value,descriptor['nonce'],last_seq,expected_slot,now(),traffic_end)
                if value['c']is not True or fd is None:raise RuntimeError('CampaignRegisteredNoChildRefusal')
                q._campaign_live(fd)
                active=dict(fd=fd,seq=seq,slot=slot,end=end);fd=None;last_seq=seq;active_end=end
                send({'k':'A','n':descriptor['nonce'],'s':seq,'i':slot,'e':end},min(traffic_end,end))
            elif kind=='I':
                if (fd is not None or len(raw)>128 or active is None or set(value)!={'k','n','s','i','r'}
                    or type(value['s'])is not int or value['s']!=active['seq']
                    or type(value['i'])is not int or value['i']!=active['slot']
                    or type(value['r'])is not int or not -128<=value['r']<=255):
                    raise RuntimeError('CampaignIDLEBinding')
                if active['slot']>119 and value['r']!=0:raise RuntimeError('CampaignPreparationNonzero')
                if active['slot']<=119 and value['r']not in(0,2,-int(signal.SIGKILL)):raise RuntimeError('CampaignCaseUnexpectedExit')
                if not fd_exited(active['fd']):raise RuntimeError('CampaignIDLEBeforeExecutableExit')
                seq,slot,end=active['seq'],active['slot'],active['end']
                close_active() # Signal lifecycle CLOSED before census barrier and IDLEACK.
                barrier_end=min(end,whole_end,now()+2000000000)
                if not barrier(barrier_end):raise RuntimeError('CampaignIDLEOwnChildBarrier')
                if len(retired)>=199:raise RuntimeError('CampaignRetiredRegistryBound')
                retired.append((seq,slot,end,value['r']))
                send({'k':'i','n':descriptor['nonce'],'s':seq,'i':slot,'e':end},min(traffic_end,end))
                active_end=traffic_end;barrier_end=None
            elif kind=='B':
                if (fd is not None or len(raw)>128 or not hello or set(value)!={'k','n','s','i'}
                    or type(value['s'])is not int or value['s']!=last_seq
                    or type(value['i'])is not int or value['i']!=(active['slot']if active else 0)):
                    raise RuntimeError('CampaignABORTBinding')
                begin_fault('CoordinatorABORT')
                send({'k':'b','n':descriptor['nonce'],'s':last_seq,'i':active['slot']if active else 0},min(cleanup_end,traffic_end))
            else:raise RuntimeError('CampaignUnknownMessage')
        finally:
            if fd is not None:os.close(fd)

    try:
        target=Path(descriptor['root']);evidence=Path(descriptor['evidence'])
        if control:
            allocation={'used':0}
        else:
            target.mkdir(mode=0o700);(target/'home').mkdir(mode=0o700)
            evidence.mkdir(mode=0o700);receipt.mkdir(mode=0o700)
            allocation,raw_handles=budget.raw_group(list(paths.values()),'custody',262144)
        libc=ctypes.CDLL(None,use_errno=True)
        if libc.prctl(36,1,0,0,0)!=0:raise OSError(ctypes.get_errno(),'PR_SET_CHILD_SUBREAPER')
        def stop_handler(signum,frame):
            if not stopped:stopped.append(signum)
        old_handlers={n:signal.signal(n,stop_handler)for n in(signal.SIGTERM,signal.SIGINT)}
        control_owner,control_child=q._campaign_pair()
        release_owner,release_child=q._campaign_pair()
        command=q._harmless_command(campaign.manifest,'root',0) if control else q._campaign_command(campaign.manifest,'root',0)
        launch=(q._harmless_gate_args(campaign.group,source_sha,'root',0,0,release_child.fileno(),descriptor['nonce'],traffic_end,control=control_child.fileno()) if control else q._campaign_gate_args(source_sha,'root',0,0,release_child.fileno(),descriptor['nonce'],traffic_end,control=control_child.fileno()))
        if now()>=traffic_end:raise RuntimeError('CampaignRootLaunchDeadline')
        spawn_attempted=True
        root=subprocess.Popen(launch,cwd=command['cwd'],env=q._campaign_gate_environment(command['env']),stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            close_fds=True,pass_fds=(release_child.fileno(),control_child.fileno()),start_new_session=True)
        root_retained=True;release_child.close();release_child=None;control_child.close();control_child=None
        rootfd=q._campaign_open_child(root)
        identity('root_pidfd_bound',pid=root.pid,retained_unreaped_Popen=True)
        selector=selectors.DefaultSelector();selector.register(root.stdout,selectors.EVENT_READ,'stdout.raw');selector.register(root.stderr,selectors.EVENT_READ,'stderr.raw')
        selector.register(control_owner,selectors.EVENT_READ,'control')
        send({'k':'A','n':descriptor['nonce'],'s':0,'i':0,'e':traffic_end},traffic_end,gate=True)
        release_owner.close();release_owner=None;setup_complete=True
        while first_fault is None:
            current=now()
            if stopped:begin_fault('CampaignOwnerSignal')
            elif current>=min(traffic_end,active_end):begin_fault('CampaignExecutionDeadline')
            else:
                exited=root_exit()
                if exited is not None:
                    if exited.si_code!=os.CLD_EXITED or exited.si_status!=0:
                        begin_fault('CampaignCoordinatorNonzeroOrSignal')
                    elif not hello or last_seq!=total_slots or len(retired)!=total_slots or active is not None:
                        begin_fault('CampaignCoordinatorExitedBeforeClosedProtocol')
                    else:
                        # No more registration/ACK authority after root exit.
                        for key in list(selector.get_map().values()):
                            if key.data=='control':selector.unregister(key.fileobj)
                        control_owner.close();control_owner=None
                        final_limit=min(whole_end,now()+2000000000);settlement_end=final_limit
                        if not barrier(final_limit,False):begin_fault('CampaignFinalOwnChildBarrier',earlier_barrier=final_limit)
                        else:
                            while selector.get_map()and now()<final_limit:drain_stdio(min(.01,max(0,(final_limit-now())/1000000000)))
                            if selector.get_map():begin_fault('CampaignFinalPipeEOF',earlier_barrier=final_limit)
                            else:break
            if first_fault is not None:break
            for key,_ in selector.select(min(.01,max(0,(min(traffic_end,active_end)-now())/1000000000))):
                if key.data=='control':
                    value,fd,raw=receive(min(traffic_end,active_end))
                    process_message(value,fd,raw)
                else:
                    channel=key.data
                    raw=os.read(key.fileobj.fileno(),min(4096,max(0,32768-len(buffers[channel]))+1))
                    if not raw:selector.unregister(key.fileobj);key.fileobj.close()
                    else:retain(channel,raw)
                if first_fault is not None:break
    except BaseException as error:
        begin_fault('CampaignOwnerFailure',error,barrier_end)
    finally:
        # Closing an unreleased gate prevents finalexec; never release on cleanup.
        for endpoint in(release_owner,release_child,control_child):
            if endpoint is not None:
                try:endpoint.close()
                except BaseException:partial=True
        if first_fault is not None:
            if selector is not None:
                for key in list(selector.get_map().values()):
                    if key.data=='control':
                        try:selector.unregister(key.fileobj)
                        except BaseException:partial=True
            if control_owner is not None:
                try:control_owner.close()
                except BaseException:partial=True
                control_owner=None
            while now()<cleanup_end:
                if not term_sent:
                    signal_registered(signal.SIGTERM);term_sent=True
                elif not kill_sent and (now()-first_fault>=500000000 or cleanup_end-now()<=250000000):
                    signal_registered(signal.SIGKILL);kill_sent=True
                try:
                    others=reap_other_exited()
                    running=[p for p in others if root is None or not root_retained or p!=root.pid]
                    exited=None if root is None else root_exit()
                    if not running and (root is None or exited is not None)and(selector is None or not selector.get_map()):break
                    drain_stdio(min(.01,max(0,(cleanup_end-now())/1000000000)))
                except BaseException:
                    # Census refusal cannot skip retained registered-child KILL.
                    # No unknown child is signaled, and this is never qualified.
                    census_unknown=True
                    try:drain_stdio(min(.001,max(0,(cleanup_end-now())/1000000000)))
                    except BaseException:partial=True
        # End every active signaling capability before possibly reaping root.
        try:close_active()
        except BaseException:signal_unknown=True
        if control_owner is not None:
            try:control_owner.close()
            except BaseException:partial=True
        if selector is not None:
            stdio_eof_observed=not any(key.data!='control' for key in selector.get_map().values())
            try:selector.close()
            except BaseException:partial=True
        for pipe in(()if root is None else(root.stdout,root.stderr)):
            if pipe is not None and not pipe.closed:
                try:pipe.close()
                except BaseException:partial=True
        identity_end=cleanup_end if first_fault is not None else settlement_end
        can_reap=False
        if now()<identity_end:
            try:
                final_children=reap_other_exited()
                other_live=[p for p in final_children if root is None or not root_retained or p!=root.pid]
                can_reap=root is not None and root_retained and not other_live and root_exit()is not None
            except BaseException:census_unknown=True;final_children=None
        else:census_unknown=True;final_children=None
        if rootfd is not None:
            try:os.close(rootfd)
            except BaseException:signal_unknown=True
            rootfd=None
        # No registration channel or signaling FD remains. Root identity is now
        # no longer needed, so the actual retained Popen child may be reaped LAST.
        if can_reap and now()<identity_end:
            try:
                root.wait(timeout=0);root_retained=False;root_reaped_last=True
                if now()>=identity_end:raise RuntimeError('CampaignFinalReapDeadline')
                final_children=census()
                if not final_children:
                    try:os.waitid(os.P_ALL,0,os.WEXITED|os.WNOHANG|os.WNOWAIT)
                    except ChildProcessError:kernel_no_children=True
            except BaseException:census_unknown=True
        for signum,handler in old_handlers.items():signal.signal(signum,handler)
        for handle in raw_handles.values():
            try:handle.close()
            except BaseException:partial=True
        qualified=(setup_complete and first_fault is None and not partial and not census_unknown and not signal_unknown
            and len(retired)==total_slots and root_reaped_last and root is not None and root.returncode==0 and kernel_no_children and now()<whole_end)
        result=dict(status='CAMPAIGN_OWNER_OBSERVED'if qualified else'UNKNOWN_CAMPAIGN_HOLD',
            campaign_source_sha=source_sha,manifest_q_sha=campaign.manifest['sources'][str(Path(q.__file__).resolve())]['sha256'],
            requested_final_argv=None if not setup_complete else command['argv'],
            gated_initial_argv=None if not spawn_attempted else launch,
            start=campaign.start,end=whole_end,traffic_end=traffic_end,observed_before_receipt=now(),
            first_fault=first_fault,cleanup_end=cleanup_end,reason=reason,diagnostic=diagnostic,last_active_end=active_end,registered_exit_observed=registered_exit_observed,
            whole_includes_cleanup=True,whole_deadline_observed_before_receipt=now()<whole_end,
            receipt_write_completion_time='UNKNOWN/not retroactively inserted into write-once receipt',
            returned_Popen_handle=root is not None,launch_fact='NO_ATTEMPT'if not spawn_attempted else'UNKNOWN_CONSTRUCTOR_FAILURE'if root is None else'OBSERVED_HANDLE',
            root_pid=None if root is None else root.pid,root_exit=None if root is None else root.returncode,
            coordinator_reaped_last=root_reaped_last,root_identity_events=identity_events,
            retired_slots=retired,request_frames=request_count,response_frames=response_count,
            own_exited_reaped_summary=dict(count=reaped_count,ordered_fact_sha256=reaped_digest.hexdigest(),raw_not_retained=True),
            raw_stdio_eof_observed=stdio_eof_observed,own_children_remaining=final_children,own_child_census='UNKNOWN'if census_unknown else'OBSERVED',
            kernel_no_children_observed=kernel_no_children,cleanup_qualified=qualified,
            unknown_cleanup_hold=not qualified,signal_identity_unknown=signal_unknown,
            raw_channels=({n:dict(bytes=len(buffers[n]),sha256=hashlib.sha256(buffers[n]).hexdigest(),literal_child_bytes_not_persisted=True) for n in buffers} if control else {n:dict(path=str(paths[n]),**pin(paths[n]))for n in paths if paths[n].is_file()}),
            retained_bytes=0 if allocation is None else allocation['used'],shared_raw_cap=262144,
            channel_caps=dict(stdout=32768,stderr=32768,control=196608),
            partial_prefix=partial,unretained_suffix='UNKNOWN'if partial else None,
            physical_release='UNKNOWN/not inferred from owner cleanup',escaped_descendants='UNKNOWN',
            asynchronous_signal_partial_effects='UNKNOWN on failure',no_numeric_or_group_signals=True,
            no_foreign_process_cleanup=True,permission_granted=False)
        # Only this existing one source-owned whole writer, even on failure.
        if control:
            reports=[]
            for line in bytes(buffers['stdout.raw']).splitlines():
                if len(line)>4096 or not line.startswith(b'{'):continue
                try:value=q.bounded_json_loads(line,4096)
                except (ValueError,UnicodeError):continue
                if type(value) is dict:reports.append(value)
                if len(reports)>16:raise RuntimeError('HarmlessGeneratedReportCount')
            result['harmless_observations']=reports
            result['protected_worker_self_cleanup_seen']=b'HARMLESS_PROTECTED_SELF_CLEANUP\n' in buffers['stderr.raw']
            if campaign.group==8:
                death=b'HARMLESS_OS8_PARENT_DEATH\n';clean=b'HARMLESS_PROTECTED_SELF_CLEANUP\n'
                start=buffers['stderr.raw'].find(death);finish=buffers['stderr.raw'].find(clean)
                result['worker_parent_death_observed_before_cleanup']=start>=0 and finish>=start+len(death)
            result['control_group']=campaign.group
            result['no_TEST']=True;result['no_P']=True
        elif receipt.is_dir():budget.document(receipt/'whole.json',result,'custody',pre_reserved=True)
    return result



def _harmless_control_report(group,source_sha,earlier_end):
    import runtime_qualification as q
    owner=q._harmless_owner_admission(group,source_sha,earlier_end)
    result=_supervise_owner(owner,source_sha)
    observations=result['harmless_observations']
    boot=next((r for r in observations if r.get('event')=='bootstrap'),{})
    slots=[r for r in observations if r.get('event')=='slot_exec']
    exits={r.get('index'):r.get('exit') for r in observations if r.get('event')=='slot_exit'}
    settled=bool(result['coordinator_reaped_last'] and result['kernel_no_children_observed'] and result['own_children_remaining']==[] and not result['signal_identity_unknown'])
    checks=[]
    def check(name,observed,expected):checks.append(dict(name=name,observed=observed,expected=expected))
    check('root_same_pid',boot.get('pid'),result['root_pid'])
    check('bootstrap_control_cloexec',boot.get('control_cloexec'),True)
    check('bootstrap_owner_cloexec',boot.get('owner_cloexec'),True)
    check('cleanup_settled',settled,True)
    diagnostic=(result['diagnostic'] or {}).get('text','')
    if group==1:
        check('slot_capability_fds_empty',len(slots)==2 and all(r.get('root_capability_fds')==[] for r in slots),True)
        check('slot_root_env_absent',len(slots)==2 and all(r.get('root_role_env') is False for r in slots),True)
        check('ordinary_exit',exits.get(1),0)
        checkpoint=any(r.get('event')=='direct_pidfd_checkpoint' and r.get('actual_pipe_token')=='CHECKPOINT' for r in observations)
        check('checkpoint_exit',exits.get(2) if checkpoint else None,-int(signal.SIGKILL))
        failure=next((r for r in observations if r.get('event')=='Popen_failure'),{})
        check('popen_constructor_refused',failure.get('returned_handle') is False and failure.get('exception')=='FileNotFoundError',True)
    elif group in (2,3):check('malformed_frame_refused','CampaignAuthenticatedFrame' in diagnostic,True)
    elif group==4:check('nonce_refused','CampaignProtocolNonceOrType' in diagnostic,True)
    elif group==5:
        check('death_before_gate_ack',result['root_exit']==-int(signal.SIGKILL) and any(r.get('event')=='death_before_gate_ACK' and r.get('release_sent') is False for r in observations),True)
        check('no_slot_finalexec',not slots and result['raw_stdio_eof_observed'] and result['raw_channels']['stdout.raw']['bytes']<32768,True)
    elif group==6:
        check('late_gate_refused',result['first_fault'] is not None and result['first_fault']>=result['last_active_end'],True)
        check('no_slot_finalexec',not slots and result['raw_stdio_eof_observed'] and result['raw_channels']['stdout.raw']['bytes']<32768,True)
    elif group==7:
        check('raw_overflow_refused','CampaignOwnerRawOverflow' in diagnostic and result['raw_channels']['stdout.raw']['bytes']==32768,True)
        check('protected_worker_self_cleanup',result['protected_worker_self_cleanup_seen'],True)
    elif group==8:
        ready=any(r.get('event')=='worker_ready_before_death' and r.get('token')=='WORDLING_OS8_WORKER_READY' and r.get('eof') is True for r in observations)
        check('worker_ready_before_death',ready,True)
        check('worker_parent_death_observed_before_cleanup',result['worker_parent_death_observed_before_cleanup'],True)
        check('registered_executable_exit',result['registered_exit_observed'],True)
        check('protected_worker_self_cleanup',result['protected_worker_self_cleanup_seen'],True)
    passed=all(r['observed']==r['expected'] for r in checks)
    report=dict(group=group,status='PASS' if passed else 'UNKNOWN',checks=checks,kernel_facts=result,cleanup=dict(settled=settled,unknown_hold=not settled),no_TEST=True,no_P=True)
    raw=(json.dumps(report,ensure_ascii=True,separators=(',',':'))+'\n').encode('ascii')
    if len(raw)>24576:raise RuntimeError('HarmlessOSGroupReportBound')
    offset=0
    while offset<len(raw):
        written=os.write(1,raw[offset:])
        if written<=0:raise RuntimeError('HarmlessOSGroupReportWrite')
        offset+=written
    return 0 if passed else 2


def _campaign_or_legacy_main():
    import sys
    if '--qualify-r11' in sys.argv[1:]:
        parser=argparse.ArgumentParser();parser.add_argument('--qualify-r11',required=True)
        value=parser.parse_args();return supervise_r11_qualification(value.qualify_r11)
    if '--harmless-campaign-group' in sys.argv[1:]:
        parser=argparse.ArgumentParser();parser.add_argument('--harmless-campaign-group',type=int,required=True);parser.add_argument('--source-sha',required=True);parser.add_argument('--control-end-ns',type=int,required=True)
        value=parser.parse_args()
        return _harmless_control_report(value.harmless_campaign_group,value.source_sha,value.control_end_ns)
    if '--campaign-source-sha'not in sys.argv[1:]:return main()
    parser=argparse.ArgumentParser()
    parser.add_argument('--campaign-source-sha',required=True)
    value=parser.parse_args()
    result=supervise_campaign(value.campaign_source_sha)
    print(json.dumps(result))
    return 0 if result['cleanup_qualified']and not result['unknown_cleanup_hold']else 2



def main():
    a=argparse.ArgumentParser();a.add_argument('--prepare',action='store_true');v=a.parse_args()
    if not v.prepare:raise SystemExit('DISABLED: ROOT exact frozen qualification grant required')
    root=Path('/tmp/wordling-WP70-codex312-qualified-runtime-v14-supervisor')
    argv=['/usr/bin/python3','-B',str(Path(__file__).with_name('runtime_qualification.py')),'--prepare']
    env=dict(PATH='/usr/bin:/bin',HOME='/tmp',LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
    result=supervise(argv,'/tmp',env,root)
    print(json.dumps(result));return 0 if result['exit']==0 and result['cleanup_qualified'] and not result['partial_prefix'] else 2

if __name__=='__main__':
    try:result=_campaign_or_legacy_main()
    except SystemExit as e:result=e.code
    except BaseException as error:
        emit_diagnostic(error);result=2
    raise SystemExit(result)
