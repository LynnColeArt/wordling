#!/usr/bin/env python3
"""Source-bound compatibility and closed TEST entrypoints; no original permission."""
from __future__ import annotations
import argparse
import dataclasses
import hashlib
import importlib.util
from importlib import _bootstrap
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

_PACKAGE = 'wordling_reference_startup_v1'
_FILES = ('__init__.py', 'engine.py', 'artifacts.py', 'lifetime.py')


def _load_family():
    # The module import lock serializes both ordinary and file-spec alias loads.
    with _bootstrap._ModuleLockManager(_PACKAGE):
        here = Path(__file__).absolute()
        for path in (here, *here.parents):
            if path.is_symlink():
                raise ImportError('startup source symlink')
        root = here.parent / 'startup_family'
        info = root.stat()
        if root.is_symlink() or not stat.S_ISDIR(info.st_mode):
            raise ImportError('startup package directory')
        closure = {}
        for name in _FILES:
            source = root / name
            if source.is_symlink() or not stat.S_ISREG(source.stat().st_mode):
                raise ImportError('startup module source')
            closure[name] = hashlib.sha256(source.read_bytes()).hexdigest()
        binding = (str(root), info.st_dev, info.st_ino, closure)
        existing = sys.modules.get(_PACKAGE)
        if existing is not None:
            if (getattr(existing, '_source_binding', None) != binding
                    or getattr(existing, 'API_VERSION', None) != 1):
                raise ImportError('startup source authority collision')
            expected = {_PACKAGE: '__init__.py', _PACKAGE+'.engine': 'engine.py',
                        _PACKAGE+'.artifacts': 'artifacts.py', _PACKAGE+'.lifetime': 'lifetime.py'}
            for key, name in expected.items():
                module = sys.modules.get(key)
                if module is None or module.__spec__.origin != str(root/name):
                    raise ImportError('startup module origin collision')
            if list(existing.__path__) != [str(root)]:
                raise ImportError('startup package path collision')
            return existing
        before = set(sys.modules)
        if any(key.startswith(_PACKAGE+'.') for key in before):
            raise ImportError('startup orphan module collision')
        spec = importlib.util.spec_from_file_location(_PACKAGE, root/'__init__.py',
                                                    submodule_search_locations=[str(root)])
        package = importlib.util.module_from_spec(spec)
        sys.modules[_PACKAGE] = package
        try:
            spec.loader.exec_module(package)
            package._source_binding = binding
            # Re-enter only validation: this catches changed sources/origins during initialization.
            return _load_family()
        except BaseException:
            for key in set(sys.modules)-before:
                if key == _PACKAGE or key.startswith(_PACKAGE+'.'):
                    del sys.modules[key]
            raise


_family = _load_family()
for _name in ('Failure', 'Limits', 'Identity', 'Result', 'EndpointSpec', 'decode_json',
              'ArtifactSpec', 'CommandSpec', 'Attempt', 'SourceRequest', 'StreamPolicy',
              'SourceObservation', 'SourceLease', 'WorkingLease', 'ExecutableLease', 'MutationSpec', 'LaunchSpec',
              'ResourceArgument', 'NewWorkspace', 'ManagedPolicy', 'StartupFailure', 'Session',
              'ProcessLease', 'CheckedChannel', 'IdentityObservation', 'ReadyObservation',
              'IOObservation', 'Snapshot', 'MutationResult', 'ExitObservation', 'PartialOutcome',
              'SessionOutcome', 'SharedEnvelopePolicy', 'UsageObservation', 'StoppedReadLease', 'DerivedArtifactLease',
              'OutputSpec', 'OutputArgument', 'JobBudget', 'DerivationSpec', 'OutputObservation', 'DerivedBatch', 'ArtifactChunk', 'open_session'):
    globals()[_name] = getattr(_family, _name)


def source_binding():
    return _family.source_binding()


def _fixture(case):
    roster = ('success', 'nonzero', 'stdout', 'stderr', 'hang', 'orphan', 'observer-fail', 'readiness')
    if case not in roster:
        raise Failure('unknown-fixture')
    with tempfile.TemporaryDirectory(prefix='startup-test-') as temporary:
        root = Path(temporary)
        fixture = root/'fixture.py'
        fixture.write_text("import os,sys,time,socket\n"
                           "case=sys.argv[1]\n"
                           "if case=='nonzero': print('partial',flush=True); sys.exit(7)\n"
                           "if case=='stdout': os.write(1,b'x'*65536)\n"
                           "if case=='stderr': os.write(2,b'x'*65536)\n"
                           "if case=='hang': time.sleep(10)\n"
                           "if case=='orphan':\n"
                           " if os.fork()==0: time.sleep(10); os._exit(0)\n"
                           "if case=='readiness':\n"
                           " s=socket.socket(socket.AF_UNIX); s.bind(sys.argv[2]); s.listen(1)\n"
                           " c,_=s.accept(); assert c.recv(64)==b'TEST ping\\n'; c.sendall(b'TEST ready\\n'); c.close(); s.close(); time.sleep(.2)\n"
                           "print('TEST complete',flush=True)\n")
        source = ArtifactSpec.capture(fixture)
        tool = ArtifactSpec.capture(Path(sys.executable).resolve())
        command = CommandSpec(tool, (tool.path, '-B', str(fixture), case, str(root/'endpoint')), str(root), sources=(source,))
        limits = Limits(seconds=1.5, stream_bytes=8192)
        with Attempt(root, limits) as attempt:
            attempt.copy(source, 'copy')
            try:
                before = dataclasses.replace(command, argv=(tool.path, '-B', str(fixture), 'nonzero')) if case == 'observer-fail' else None
                result = attempt.run(command, before_spawn=before,
                                     readiness=EndpointSpec(str(root/'endpoint')) if case == 'readiness' else None)
                return dict(ok=True, result=dataclasses.asdict(result), journal=attempt.journal)
            except Failure as error:
                return dict(ok=False, error=error.code, result=dataclasses.asdict(error.result) if error.result else None, journal=attempt.journal)


def _managed_projection(value):
    if dataclasses.is_dataclass(value):
        return {f.name:_managed_projection(getattr(value,f.name)) for f in dataclasses.fields(value)
                if f.name!='successor'}
    if isinstance(value,dict):
        return {str(k):_managed_projection(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):
        return [_managed_projection(x) for x in value]
    if isinstance(value,bytes):
        return value.hex()
    return value


def _managed_fixture(case):
    """Closed authored TEST consumers; never accepts a reference recipe or path."""
    import signal
    import socket
    import shutil
    import time
    cases=('streaming64m','mutable-success','mutable-failure','handoff','parent-loss','cancel',
           'foreign-endpoint','unknown-launch','process-progress','readiness-deadline-progress',
           'exec-reply-exit','prior-no-clobber','worker-death','stale-handle','wrong-root-load')
    if case not in cases:
        raise Failure('unknown-fixture')
    with tempfile.TemporaryDirectory(prefix='startup-managed-TEST-') as temporary:
        root=Path(temporary)
        def request(path):
            digest=hashlib.sha256()
            with path.open('rb') as stream:
                while raw:=stream.read(65536):
                    digest.update(raw)
            return SourceRequest(str(path),path.stat().st_size,digest.hexdigest())
        if case=='wrong-root-load':
            other=root/'other'
            other.mkdir()
            shutil.copytree(Path(__file__).parent/'startup_family',other/'startup_family',
                            ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copyfile(Path(__file__),other/'startup_transport.py')
            spec=importlib.util.spec_from_file_location('wrong_root_fixture',other/'startup_transport.py')
            module=importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except ImportError as error:
                return dict(ok=False,error='SourceAuthorityCollision',detail=str(error),original_guests=0)
            raise AssertionError('foreign root accepted')
        if case=='parent-loss':
            coordinator=os.fork()
            if coordinator==0:
                try:
                    session=open_session(NewWorkspace(str(root/'workspace')),StreamPolicy.test_v1(),
                                         ManagedPolicy.test_v1(3))
                    python=Path(sys.executable).resolve()
                    tool=session.tool(session.capture(request(python)))
                    process=session.launch(LaunchSpec(tool,(str(python),'-c',
                        'import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(2)')))
                    (root/'created.json').write_text(json.dumps(_managed_projection(process.identity())))
                    time.sleep(4)
                    os._exit(3)
                except BaseException:
                    os._exit(4)
            fd=os.pidfd_open(coordinator)
            try:
                deadline=time.monotonic()+3
                while not (root/'created.json').exists():
                    if time.monotonic()>=deadline:
                        raise AssertionError('coordinator fixture failed')
                    time.sleep(.01)
                identity=json.loads((root/'created.json').read_text())
                signal.pidfd_send_signal(fd,signal.SIGKILL)
                os.waitpid(coordinator,0)
                deadline=time.monotonic()+1.6
                while time.monotonic()<deadline:
                    journal=(root/'workspace/session.jsonl').read_text()
                    try:
                        fields=Path('/proc',str(identity['pid']),'stat').read_text().rsplit(')',1)[1].split()
                        stopped=fields[0]=='Z' or int(fields[19])!=identity['startticks']
                    except FileNotFoundError:
                        stopped=True
                    if stopped and ('"code":"ParentLost"' in journal or '"code":"ControlLost"' in journal):
                        return dict(ok=False,error='ParentLost',created_identity=identity,
                                    authored_child_observed_stopped=True,original_guests=0)
                    time.sleep(.01)
                raise AssertionError('parent loss not contained')
            finally:
                os.close(fd)
                try:
                    pid,status=os.waitpid(coordinator,os.WNOHANG)
                    if not pid:
                        os.kill(coordinator,signal.SIGKILL);os.waitpid(coordinator,0)
                except ChildProcessError:
                    pass
        policy=ManagedPolicy(total_seconds=3,processes=4 if case=='process-progress' else 8)
        session=open_session(NewWorkspace(str(root/'workspace')),StreamPolicy.test_v1(),policy)
        outcome=None;foreign=None
        value=dict(ok=False,case=case,original_guests=0)
        try:
            source=root/'source'
            if case=='streaming64m':
                chunk=bytes(range(256))*256
                with source.open('wb') as stream:
                    for _ in range(1024):
                        stream.write(chunk)
            else:
                source.write_bytes(b'authored TEST')
            source_request=request(source)
            source_lease=session.capture(source_request)
            working=session.prepare(source_lease,'working')
            if case=='streaming64m':
                snapshot=session.snapshot(working)
                with source.open('rb') as left,(root/'workspace/working').open('rb') as right:
                    while raw:=left.read(65536):
                        if raw!=right.read(65536):
                            raise AssertionError('full streamed copy mismatch')
                    if right.read(1):
                        raise AssertionError('copy tail')
                value.update(ok=True,snapshot=_managed_projection(snapshot),full_copy_equal=True)
            elif case=='prior-no-clobber':
                session.prepare(source_lease,'working')
            else:
                python=Path(sys.executable).resolve()
                tool=session.tool(session.capture(request(python)))
                script=root/'fixture.py'
                if case in ('mutable-success','mutable-failure','stale-handle'):
                    script.write_text("import sys,time\nfrom pathlib import Path\n"
                        "p=Path(sys.argv[1]);p.write_bytes(p.read_bytes()+b'!');time.sleep(.2)\n"+
                        ("sys.exit(7)\n" if case=='mutable-failure' else ""))
                    script_lease=session.capture(request(script))
                    mutation=session.mutate(working,MutationSpec(tool,(str(python),'-B',
                        ResourceArgument('',script_lease,''),ResourceArgument('',working,'')),
                        immutable_inputs=(script_lease,)))
                    if case=='stale-handle':
                        session.snapshot(working)
                    else:
                        snapshot=session.snapshot(mutation.successor)
                        value.update(ok=True,mutation=_managed_projection(mutation),
                                     snapshot=_managed_projection(snapshot))
                else:
                    peer=case in ('handoff','process-progress','readiness-deadline-progress','exec-reply-exit')
                    body="import os,sys,time,socket,signal\n"
                    if case=='unknown-launch':
                        body+="os.rename('session.jsonl','retained-journal');time.sleep(1)\n"
                    elif peer:
                        body+="s=socket.socket(socket.AF_UNIX);s.bind('endpoint');s.listen(1)\nc,_=s.accept();c.recv(64)\n"
                        if case=='process-progress':
                            body+=("children=[]\nfor i in range(2):\n p=os.fork()\n"
                                   " if p==0:time.sleep(.5);os._exit(0)\n children.append(p)\n"
                                   "for b in b'TEST ready\\n':\n c.send(bytes([b]));time.sleep(.05)\n"
                                   "for p in children:os.waitpid(p,0)\ntime.sleep(.2)\n")
                        elif case=='readiness-deadline-progress':
                            body+="for b in b'TEST ready\\n':\n c.send(bytes([b]));time.sleep(.05)\n"
                        elif case=='exec-reply-exit':
                            body+=("os.set_inheritable(c.fileno(),True)\n"
                                   "os.execve(sys.executable,(sys.executable,'-c',"
                                   "\"import socket,sys;socket.socket(fileno=int(sys.argv[1])).sendall(b'TEST ready\\\\n')\",str(c.fileno())),{})\n")
                        else:
                            body+="c.sendall(b'TEST ready\\n');c.recv(64);time.sleep(.2)\n"
                    else:
                        body+="time.sleep(.8)\n"
                    script.write_text(body)
                    script_lease=session.capture(request(script))
                    process=session.launch(LaunchSpec(tool,(str(python),'-B',
                        ResourceArgument('',script_lease,''))),(working,))
                    if case=='cancel':
                        partial=process.cancel()
                        value.update(error=partial.first_fault,partial=_managed_projection(partial))
                    elif case=='worker-death':
                        children=Path('/proc/self/task',str(os.getpid()),'children').read_text().split()
                        if len(children)!=1:
                            raise AssertionError('test coordinator child roster')
                        worker=int(children[0])
                        fields=Path('/proc',str(worker),'stat').read_text().rsplit(')',1)[1].split()
                        if int(fields[1])!=os.getpid():
                            raise AssertionError('test worker parent')
                        fd=os.pidfd_open(worker)
                        signal.pidfd_send_signal(fd,signal.SIGKILL)
                        os.close(fd)
                        try:
                            process.verify_current()
                        finally:
                            time.sleep(.9)  # Authored TEST child self-stops; API does not adopt it.
                    elif case=='foreign-endpoint':
                        foreign=os.fork()
                        if foreign==0:
                            try:
                                endpoint=socket.socket(socket.AF_UNIX)
                                endpoint.bind(str(root/'workspace/endpoint'));endpoint.listen(1)
                                endpoint.settimeout(1)
                                connection,_=endpoint.accept()
                                connection.settimeout(.3)
                                try:raw=connection.recv(4096)
                                except socket.timeout:raw=b''
                                (root/'foreign-count').write_text(str(len(raw)))
                                connection.close();endpoint.close();os._exit(0)
                            except BaseException:os._exit(5)
                        channel=process.open_endpoint('endpoint')
                        channel.exchange(b'TEST ping\n',b'TEST ready\n',1)
                    else:
                        channel=process.open_endpoint('endpoint')
                        ready=channel.exchange(b'TEST ping\n',b'TEST ready\n',
                                               .1 if case=='readiness-deadline-progress' else 1)
                        channel.send(b'TEST stop\n',1)
                        channel.close()
                        exited=process.finish()
                        value.update(ok=True,ready=_managed_projection(ready),
                                     exited=_managed_projection(exited),
                                     snapshot=_managed_projection(session.snapshot(working)))
            value['source_unchanged']=request(source)==source_request
        except StartupFailure as error:
            value.update(ok=False,error=error.code,partial=_managed_projection(error.observation))
        finally:
            outcome=session.close()
            value['outcome']=_managed_projection(outcome)
            if foreign is not None:
                os.waitpid(foreign,0)
                value['foreign_bytes']=int((root/'foreign-count').read_text())
        return value


def _envelope_fixture(case):
    """Closed harmless public consumers; no caller argv/path/grant accepted."""
    import time
    import signal
    import socket
    cases=('positive','expired','absolute-progress','source-io','prepared','commands',
           'output','fd','process','rss','wire','observation','response-loss','external-peer')
    if case not in cases:raise Failure('unknown-fixture')
    with tempfile.TemporaryDirectory(prefix='startup-envelope-TEST-') as temporary:
        root=Path(temporary);session=None;held=[];fixture_child_fd=None;value=dict(ok=False,case=case,original_guests=0)
        def request(path):
            digest=hashlib.sha256()
            with path.open('rb') as source:
                while raw:=source.read(65536):digest.update(raw)
            return SourceRequest(str(path),path.stat().st_size,digest.hexdigest())
        now=time.monotonic();fields={}
        if case=='source-io':fields['source_io']=200
        if case=='prepared':fields['prepared_bytes']=10
        if case=='commands':fields['commands']=1
        if case=='output':fields['output_bytes']=1024
        if case=='fd':fields['fds']=40
        if case=='process':fields['processes']=3
        if case=='rss':fields['rss_bytes']=100*1048576
        if case=='wire':fields['control_wire_bytes']=100000
        seconds=.2 if case=='absolute-progress' else 8
        envelope=SharedEnvelopePolicy(origin=now-2 if case=='expired' else now,
            end=now-1 if case=='expired' else now+seconds,**fields)
        try:
            session=open_session(NewWorkspace(str(root/'work')),StreamPolicy(),
                ManagedPolicy(readiness_seconds=.05 if case=='external-peer' else 60),envelope=envelope)
            history=[session.usage()]
            source=root/'source';source.write_bytes(b'authored one-leaf TEST\n')
            captured=session.capture(request(source))
            if case=='observation':
                session.capture(history[0]);raise AssertionError('fact used as capability')
            if case=='fd':
                held=[os.open('/dev/null',os.O_RDONLY) for _ in range(40)]
                session.usage();raise AssertionError('FD ceiling ignored')
            if case=='wire':
                for _ in range(150):session.usage()
                raise AssertionError('wire ceiling ignored')
            if case=='absolute-progress':
                while True:session.usage()
            working=session.prepare(captured,'copy')
            history.append(session.usage())
            python=Path(sys.executable).resolve();tool=session.tool(session.capture(request(python)))
            # Both mutation and foreground charge the same real worker counter.
            mutation=session.mutate(working,MutationSpec(tool,(str(python),'-c',
                'import pathlib,sys,time;time.sleep(.15);p=pathlib.Path(sys.argv[1]);p.write_bytes(p.read_bytes()+b"changed\\n");time.sleep(.1)',
                ResourceArgument('',working,''))))
            working=mutation.successor;history.append(session.usage())
            body='import time;time.sleep(2)'
            if case=='output':body='import os,time;time.sleep(.15);os.write(1,b"x"*4096);time.sleep(.3)'
            if case=='process':body='import os,time;time.sleep(.15)\nif os.fork()==0:time.sleep(.3);os._exit(0)\ntime.sleep(.5);os.wait()'
            if case=='rss':body='import time;time.sleep(.15);a=bytearray(96*1048576);time.sleep(.4)'
            if case=='external-peer':body='import socket,time,os; s=socket.socket(socket.AF_UNIX);s.bind("external");s.listen(1);c,_=s.accept();assert c.recv(4)==b"TEST";c.sendall(b"OK");c.close();s.close();time.sleep(2)'
            process=session.launch(LaunchSpec(tool,(str(python),'-c',body)),resources=(working,))
            if case=='response-loss':
                # Only the positively owned worker observed in the owned journal.
                rows=[json.loads(x) for x in (root/'work/session.jsonl').read_text().splitlines()]
                identity=process.verify_current();fixture_child_fd=os.pidfd_open(identity.pid)
                process.verify_current()
                worker=next(x['supervisor'] for x in rows if x['phase']=='OPENED')
                worker_fd=os.pidfd_open(worker)
                try:signal.pidfd_send_signal(worker_fd,signal.SIGKILL)
                finally:os.close(worker_fd)
                session.usage();raise AssertionError('lost worker result accepted')
            if case=='external-peer':
                client=socket.socket(socket.AF_UNIX);client.settimeout(1)
                until=time.monotonic()+1
                while not (root/'work/external').exists():
                    if time.monotonic()>=until:raise AssertionError('TEST peer absent')
                    time.sleep(.01)
                time.sleep(.12);process.verify_current()
                client.connect(str(root/'work/external'));client.sendall(b'TEST');assert client.recv(2)==b'OK';client.close()
            history.append(session.usage());process.verify_current();stopped=process.finish()
            snap=session.snapshot(working);history.append(session.usage())
            assert (root/'work/copy').read_bytes()==source.read_bytes()+b'changed\n'
            assert stopped.exit_code==0 and snap.successor is not working
            assert all(a.source_io<=b.source_io and a.control_wire_bytes<b.control_wire_bytes
                       and a.charged_operations<=b.charged_operations for a,b in zip(history,history[1:]))
            value.update(ok=True,history=_managed_projection(history),stopped=_managed_projection(stopped),
                         snapshot=_managed_projection(snap),same_worker=True)
        except StartupFailure as error:
            value.update(error=error.code,partial=_managed_projection(error.observation))
            journal=root/'work/session.jsonl'
            if journal.exists():
                with journal.open('rb') as raw_journal:raw=raw_journal.read(32769)
                if len(raw)>32768:raise Failure('cli-journal-limit')
                value['journal']=[json.loads(row) for row in raw.splitlines()]
        finally:
            for fd in held:os.close(fd)
            if fixture_child_fd is not None:
                import select
                if not select.select([fixture_child_fd],[],[],0)[0]:
                    signal.pidfd_send_signal(fixture_child_fd,signal.SIGTERM)
                value['fixture_child_observed_stopped']=bool(select.select([fixture_child_fd],[],[],1)[0])
                os.close(fixture_child_fd)
            if session is not None:value['outcome']=_managed_projection(session.close())
        return value


def _derivation_fixture(case):
    """Closed actual public readonly consumers, with no recipe/path/tool input."""
    import time
    cases=('positive','bounded-positive','bounded-positive-v2','measurement-accessible-v2','measurement-kernel-v2','expected-absence','empty-output','required-missing','unexpected-output','collision',
           'input-mutation','oversized','nonzero','descendant','deadline','io-exhaustion',
           'stale-working','forged-stop','chunk-replay','chunk-cap','output-replace','output-symlink')
    if case not in cases:raise Failure('unknown-fixture')
    with tempfile.TemporaryDirectory(prefix='startup-derivation-TEST-') as temporary:
        root=Path(temporary);session=None;value=dict(ok=False,case=case,original_guests=0)
        def request(path):
            digest=hashlib.sha256()
            with path.open('rb') as stream:
                while raw:=stream.read(65536):digest.update(raw)
            return SourceRequest(str(path),path.stat().st_size,digest.hexdigest())
        try:
            now=time.monotonic();session=open_session(NewWorkspace(str(root/'work')),StreamPolicy(),ManagedPolicy(),
                 envelope=SharedEnvelopePolicy(origin=now,end=now+15,
                    measurement_completion=('bounded-original-v1' if case=='bounded-positive' else
                       'bounded-original-v2' if case in ('bounded-positive-v2','measurement-accessible-v2','measurement-kernel-v2') else 'strict')))
            source=root/'source';source.write_bytes(b'authored readonly TEST\n'*100)
            working=session.prepare(session.capture(request(source)),'working')
            python=Path(sys.executable).resolve();tool=session.tool(session.capture(request(python)))
            original_argv=(str(python),'-c','import time;time.sleep(.25)')
            if case in ('measurement-accessible-v2','measurement-kernel-v2'):
                body='import ctypes,pathlib,sys,time,os,json\nlib=ctypes.CDLL(None,use_errno=True)\ntime.sleep(.3)\nassert lib.prctl(4,0,0,0,0)==0\nend=time.monotonic()+2\nwhile not any(json.loads(row).get("phase")=="MEASUREMENT_PENDING" for row in pathlib.Path(sys.argv[1]).read_text().splitlines()):\n if time.monotonic()>=end:sys.exit(93)\n time.sleep(.0001)\n'
                body+=('assert lib.prctl(4,1,0,0,0)==0\ntime.sleep(.05)\n' if case=='measurement-accessible-v2' else 'os._exit(0)\n')
                original_argv=(str(python),'-c',body,str(root/'work/session.jsonl'))
            process=session.launch(LaunchSpec(tool,original_argv),resources=(working,))
            stopped=process.finish();snap=session.snapshot(working);working=snap.successor
            if case=='forged-stop':session.seal_stopped(stopped);raise AssertionError('facts accepted')
            sealed=session.seal_stopped(working)
            if case=='stale-working':session.snapshot(working);raise AssertionError('mutable restored')
            before=session.usage()
            body='import pathlib,sys,time;time.sleep(.15);p=pathlib.Path(sys.argv[1]);pathlib.Path(sys.argv[2]).write_bytes(p.read_bytes().upper()+b"derived");time.sleep(.1)'
            outputs=(OutputSpec('result',8192),);budget=JobBudget(seconds=3)
            if case=='expected-absence':outputs+=(OutputSpec('absent',0,False),)
            if case=='empty-output':body='import pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_bytes(b"");time.sleep(.1)';outputs=(OutputSpec('result',0),)
            if case=='required-missing':body='import time;time.sleep(.2)'
            if case=='unexpected-output':body+=';pathlib.Path("extra").write_bytes(b"unexpected")'
            if case=='collision':(root/'work/result').write_bytes(b'foreign prior')
            if case=='input-mutation':body='import pathlib,sys,time;time.sleep(.15);p=pathlib.Path(sys.argv[1]);p.chmod(0o600);p.write_bytes(b"partial changed");time.sleep(.2)'
            if case=='oversized':body='import pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_bytes(b"x"*10000);time.sleep(.1)';outputs=(OutputSpec('result',100),)
            if case=='nonzero':body='import pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_bytes(b"partial");sys.exit(7)'
            if case=='descendant':body='import os,time;time.sleep(.15)\nif os.fork()==0:time.sleep(1);os._exit(0)\ntime.sleep(.1)'
            if case=='deadline':body='import time;time.sleep(2)';budget=JobBudget(seconds=.4)
            if case=='io-exhaustion':budget=JobBudget(seconds=3,io_bytes=64)
            spec=DerivationSpec(tool,(str(python),'-c',body,ResourceArgument('',sealed,''),OutputArgument(0)),outputs,budget=budget)
            batch=session.derive_readonly((sealed,),spec)
            after=session.usage()
            if case=='output-replace':
                other=root/'work/other';other.write_bytes(b'foreign replacement');os.replace(other,root/'work/result')
            if case=='output-symlink':
                (root/'work/result').unlink();(root/'work/result').symlink_to(source)
            if case=='chunk-cap':session.read_chunk(batch.artifacts[0],0,16385);raise AssertionError('large chunk accepted')
            digest=hashlib.sha256();actual=bytearray();offset=0;chunks=0
            while True:
                chunk=session.read_chunk(batch.artifacts[0],offset,16384)
                digest.update(chunk.data);actual.extend(chunk.data);offset+=len(chunk.data);chunks+=1
                if chunk.eof:break
            if case=='chunk-replay':session.read_chunk(batch.artifacts[0],0,16);raise AssertionError('replay accepted')
            expected=b'' if case=='empty-output' else source.read_bytes().upper()+b'derived'
            assert bytes(actual)==expected and digest.hexdigest()==hashlib.sha256(expected).hexdigest()
            assert before.charged_operations+1==after.charged_operations and after.helper_charged_operations==1
            assert after.original_state=='STOPPED' and after.helper_state=='STOPPED'
            if case=='expected-absence':assert batch.outputs[1].absence_proved and not (root/'work/absent').exists()
            if case in ('measurement-accessible-v2','measurement-kernel-v2'):
                events=[json.loads(row) for row in (root/'work/session.jsonl').read_text().splitlines()]
                pending=[row for row in events if row.get('phase')=='MEASUREMENT_PENDING']
                complete=[row for row in events if row.get('phase')=='MEASUREMENT_COMPLETED']
                assert len(pending)==len(complete)==1
                assert complete[0]['resolution']==('accessible' if case=='measurement-accessible-v2' else 'kernel-exit')
                assert complete[0]['mode']=='bounded-original-v2' and complete[0]['window']==.100
                assert complete[0]['observed_monotonic']<=complete[0]['end']
                value['measurement']=dict(pending=pending[0],completed=complete[0],per_transaction_only=True)
            value.update(ok=True,outputs=_managed_projection(batch.outputs),helper=_managed_projection(batch.helper_identity),
                supervisor=batch.supervisor_pid,original=_managed_projection(stopped),before=_managed_projection(before),
                after=_managed_projection(after),bytes_compared=len(actual),sha256=digest.hexdigest(),chunks=chunks)
        except StartupFailure as error:
            value.update(error=error.code,partial=_managed_projection(error.observation))
            journal=root/'work/session.jsonl'
            if journal.exists():
                with journal.open('rb') as raw_journal:raw=raw_journal.read(32769)
                if len(raw)>32768:raise Failure('cli-journal-limit')
                value['journal']=[json.loads(row) for row in raw.splitlines()]
            if case=='collision':value['prior_preserved']=(root/'work/result').read_bytes()==b'foreign prior'
        finally:
            if session is not None:value['outcome']=_managed_projection(session.close())
        return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('fixture','managed-fixture','envelope-fixture','derivation-fixture'))
    parser.add_argument('case')
    args = parser.parse_args()
    if args.command=='fixture':
        if args.case not in ('success','nonzero','stdout','stderr','hang','orphan','observer-fail','readiness'):
            parser.error('unknown fixture')
        value = _fixture(args.case)
    elif args.command=='derivation-fixture':
        if args.case not in ('positive','bounded-positive','bounded-positive-v2','measurement-accessible-v2','measurement-kernel-v2','expected-absence','empty-output','required-missing','unexpected-output','collision','input-mutation','oversized','nonzero','descendant','deadline','io-exhaustion','stale-working','forged-stop','chunk-replay','chunk-cap','output-replace','output-symlink'):
            parser.error('unknown derivation fixture')
        value=_derivation_fixture(args.case)
    elif args.command=='envelope-fixture':
        if args.case not in ('positive','expired','absolute-progress','source-io','prepared','commands','output','fd','process','rss','wire','observation','response-loss','external-peer'):
            parser.error('unknown envelope fixture')
        value=_envelope_fixture(args.case)
    else:
        if args.case not in ('streaming64m','mutable-success','mutable-failure','handoff','parent-loss',
                'cancel','foreign-endpoint','unknown-launch','process-progress','readiness-deadline-progress',
                'exec-reply-exit','prior-no-clobber','worker-death','stale-handle','wrong-root-load'):
            parser.error('unknown managed fixture')
        value = _managed_fixture(args.case)
    raw = json.dumps(value, sort_keys=True, default=lambda item: item.hex() if isinstance(item, bytes) else item).encode()
    if len(raw) > 65536:
        raise Failure('cli-result-limit')
    print(raw.decode())
    return 0 if value['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
