"""Reproducible lawful large TEST executable, public policy and measured custody."""
from pathlib import Path
import dataclasses
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[3]
FACADE=ROOT/'scripts/reference/startup_transport.py'
spec=importlib.util.spec_from_file_location('large_policy_probe',FACADE)
st=importlib.util.module_from_spec(spec);spec.loader.exec_module(st)


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while raw:=stream.read(65536):h.update(raw)
    return h.hexdigest()


def request(path):
    return st.SourceRequest(str(path),path.stat().st_size,digest(path))


def projection(value):
    if dataclasses.is_dataclass(value):
        return {f.name:projection(getattr(value,f.name)) for f in dataclasses.fields(value)
                if f.name!='successor'}
    if isinstance(value,(tuple,list)):return [projection(x) for x in value]
    if isinstance(value,dict):return {k:projection(v) for k,v in value.items()}
    return value


def main():
    started=time.monotonic()
    closure={str(p.relative_to(ROOT)):dict(bytes=p.stat().st_size,sha256=digest(p))
             for p in [FACADE,*sorted((FACADE.parent/'startup_family').glob('*.py')),Path(__file__).resolve()]}
    with tempfile.TemporaryDirectory(prefix='large-public-TEST-') as temporary:
        root=Path(temporary);python=Path(sys.executable).resolve();large=root/'public-python-padded'
        original=request(python)
        with python.open('rb') as source,large.open('wb') as target:
            while raw:=source.read(65536):target.write(raw)
            for _ in range(17):target.write(b'\0'*65536)
        large.chmod(0o755)
        known=request(large);info=large.stat()
        assert 8388608<known.expected_size<=67108864 and info.st_nlink==1
        control_argv=[str(large),'-c','print("lawful TEST executable")']
        control=subprocess.run(control_argv,cwd=root,env={},capture_output=True,timeout=3)
        assert control.returncode==0 and control.stdout==b'lawful TEST executable\n'
        try:st.ArtifactSpec.capture(large);raise AssertionError('old default accepted large tool')
        except st.Failure as error:old_refusal=error.code
        session=st.open_session(st.NewWorkspace(str(root/'success')),st.StreamPolicy.test_v1(),
                                st.ManagedPolicy.test_v1(3))
        try:
            source=session.capture(known);tool=session.tool(source)
            argv=(str(large),'-c','import time;print("TEST retained identity");time.sleep(.3)')
            process=session.launch(st.LaunchSpec(tool,argv))
            identity=process.verify_current()
            children=Path('/proc/self/task',str(os.getpid()),'children').read_text().split()
            assert len(children)==1
            worker=int(children[0])
            parent=Path('/proc',str(worker),'stat').read_text().rsplit(')',1)[1].split()
            assert int(parent[1])==os.getpid()
            fd_sample=dict(coordinator=len(os.listdir('/proc/self/fd')),
                           supervisor=len(os.listdir(Path('/proc',str(worker),'fd'))),
                           foreground=len(os.listdir(Path('/proc',str(identity.pid),'fd'))),
                           sampled_monotonic=time.monotonic())
            result=process.finish()
            assert result.exit_code==0 and result.reaped and not result.signals_issued
        finally:outcome=session.close()
        mutation_session=st.open_session(st.NewWorkspace(str(root/'changed')),st.StreamPolicy.test_v1(),
                                         st.ManagedPolicy.test_v1(3))
        try:
            changed=mutation_session.tool(mutation_session.capture(known))
            with large.open('r+b') as target:
                target.seek(-1,2);target.write(b'X');target.flush();os.fsync(target.fileno())
            try:
                mutation_session.launch(st.LaunchSpec(changed,(str(large),'-c','pass')))
                raise AssertionError('changed large executable launched')
            except st.StartupFailure as error:
                assert error.code=='SourceChanged'
                changed_refusal=projection(error.observation)
                assert changed_refusal['launch_state']=='NOT_ATTEMPTED'
        finally:changed_outcome=mutation_session.close()
        assert request(python)==original
        value=dict(source_closure_before=closure,tool_request=projection(known),
                   tool_mode=info.st_mode,tool_nlink=info.st_nlink,padding_bytes=17*65536,
                   direct_control=dict(argv=control_argv,exit=control.returncode,stdout=control.stdout.decode()),
                   old_default_refusal=old_refusal,new_identity=projection(identity),
                   real_FD_sample=fd_sample,exit=projection(result),outcome=projection(outcome),
                   changed_source_refusal=changed_refusal,changed_outcome=projection(changed_outcome),
                   public_python_unchanged=True,original_guests=0,seconds=time.monotonic()-started)
        raw=json.dumps(value,sort_keys=True,indent=2).encode()+b'\n'
        assert len(raw)<=65536
        sys.stdout.buffer.write(raw)


if __name__=='__main__':main()
