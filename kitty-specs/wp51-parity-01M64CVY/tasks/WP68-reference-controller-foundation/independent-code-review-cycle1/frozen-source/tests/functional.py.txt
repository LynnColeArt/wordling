"""Closed 48-case foundation acceptance, real public CLI/API and owned child OS IO."""
import hashlib
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import time
from deployment import preflight, run, remaining

API = {'canonical-json','float-finite','float-nan','float-infinite','custom-hooks-and-types',
       'oversized-integer','boolean-sequence','surrogate','repeated-alias','cycle','depth',
       'huge-container','huge-string','encoded-bound','copied-permit','wrong-issuer-permit',
       'consumed-permit','full-phase-book','unauthorized-book','parent-symlink',
       'ancestor-retarget','foreign-ledger','linked-ledger','fd-reuse','expired-operation',
       'stable-id-different-binding','original-disabled'}


def key(grant):
    h=hashlib.sha256()
    for value in ('wordling.spent-ticket/v1','wordling.TEST.ledger/v1','wp68-v1',grant):
        b=value.encode('ascii'); h.update(len(b).to_bytes(4,'big')+b)
    return h.hexdigest()


def plans(source,interpreter,roots,names):
    base=[str(interpreter),'-I','-B','-m','reference_controller']
    out={}
    for name in names:
        root=roots[name]
        out[name]=dict(admin=base+['test-admin','--root',root,'--generation','wp68-v1'],
            transaction=base+['test-transaction','--root',root,'--generation','wp68-v1','--grant-id',name],
            api=[str(interpreter),'-I','-B',str(source/'tests/api_cases.py'),name,root])
        if name.startswith('loss-'):
            out[name]['loss']=out[name]['transaction']+['--checkpoint',name[5:]]
        if name=='source-generation-kind-lock':
            out[name]['identity_controls']={role:dict(root=root+'-'+role,admin=base+['test-admin','--root',root+'-'+role,'--generation','wp68-v1'],transaction=base+['test-transaction','--root',root+'-'+role,'--generation','wp68-v1','--grant-id','identity-'+role,'--checkpoint','binding-written']) for role in ('lock','metadata','marker')}
            out[name]['typed_metadata']=dict(root=root+'-typed',admin=base+['test-admin','--root',root+'-typed','--generation','wp68-v1'],transaction=base+['test-transaction','--root',root+'-typed','--generation','wp68-v1','--grant-id','typed-metadata'])
        if name=='same-id-race':
            out[name]['distinct_holder']=out[name]['transaction'][:-1]+[name+'-holder','--checkpoint','marker-created']
            out[name]['distinct_contender']=out[name]['transaction'][:-1]+[name+'-contender']
        if name=='loss-marker-created':
            out[name]['pre_marker']=out[name]['transaction'][:-1]+[name+'-premarker','--checkpoint','pre-marker']
        if name.startswith('kernel-'):
            inject={'kernel-fsync-failure':'fsync:error=EIO:when=1',
                    'kernel-write-zero':'write:retval=0:when=1',
                    'kernel-readback-short':'pread64:retval=0:when=4',
                    'kernel-postcall-expiry':'fsync:delay_enter=2100000us:when=1'}[name]
            syscall=inject.split(':')[0]
            out[name]['fault']=['/usr/bin/strace','-qq','-e','trace='+syscall,'-e','inject='+inject]+out[name]['transaction']
    return out


def functional(source,interpreter,inventory,rootplans,caseplans,evidence,names):
    results=[]
    started=time.monotonic()
    cwd=interpreter.parent.parent.parent
    def invoke(argv,log):
        if time.monotonic()-started>=300: raise RuntimeError('SuiteDeadline')
        preflight(interpreter,inventory)
        return run(argv,cwd,log)
    for name in names:
        begin=time.monotonic()
        remaining()
        root=rootplans[name]; plan=caseplans[name]; log=evidence/name
        try:
            admin=invoke(plan['admin'],log/'admin')
            assert admin.returncode==0, 'admin failed'
            if name in API:
                r=invoke(plan['api'],log/'api'); assert r.returncode==0,'API failed'
            elif name in ('installed-transaction','distinct-transaction','replay-fresh-process'):
                r=invoke(plan['transaction'],log/'first'); assert r.returncode==0,'transaction failed'
                observed=json.loads(r.stdout)['account']
                assert observed['closed'] is True and observed['ledger_commits']==2
                assert observed['spent']['prepared_bytes']==2*(4*8192+1048576)
                assert observed['live']['peak']['files']==2 and observed['spent']['journal_events']==2
                assert all(k not in observed['spent'] for k in ('processes','rss_bytes','fds','files'))
                assert observed['live']['coverage']=='COORDINATOR_ONLY'
                assert observed['live']['baseline'] is not None
                assert observed['live']['peak']['processes']==1 and observed['live']['peak']['fds']<=64
                assert 0<observed['live']['current']['rss_bytes']<=observed['live']['peak']['rss_bytes']<=268435456
                assert observed['spent']['output_bytes']==32768 and len(r.stdout)<=32768
                assert observed['spent']['journal_bytes']==16384
                if name=='distinct-transaction':
                    second=plan['transaction'][:-1]+[name+'-distinct']
                    r=invoke(second,log/'distinct'); assert r.returncode==0,'distinct refused'
                    assert len(list(Path(root).glob('*.spent')))==2
                if name=='replay-fresh-process':
                    before={str(p):p.read_bytes() for p in Path(root+'-ledger').iterdir()}
                    marker=Path(root)/(key(name)+'.spent')
                    identity=(marker.stat().st_dev,marker.stat().st_ino,marker.stat().st_ctime_ns)
                    r=invoke(plan['transaction'],log/'replay'); assert r.returncode==2,'replay accepted'
                    assert before=={str(p):p.read_bytes() for p in Path(root+'-ledger').iterdir()}
                    assert identity==(marker.stat().st_dev,marker.stat().st_ino,marker.stat().st_ctime_ns),'spent marker replaced'
            elif name.startswith('loss-'):
                if name=='loss-marker-created':
                    preflight(interpreter,inventory)
                    child=subprocess.Popen(plan['pre_marker'],cwd=cwd,env=dict(PATH='/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    assert select.select([child.stdout],[],[],5)[0],'pre-marker checkpoint timeout'
                    event=child.stdout.readline(16385)
                    assert json.loads(event)['checkpoint']=='pre-marker'
                    child.kill();out,err=child.communicate(timeout=2)
                    (log/'pre-marker.stdout').write_bytes(event+out);(log/'pre-marker.stderr').write_bytes(err)
                    (log/'pre-marker.json').write_text(json.dumps(dict(argv=plan['pre_marker'],returncode=child.returncode))+'\n')
                    assert not list(Path(root).glob('*.spent')) and not list(Path(root+'-ledger').iterdir())
                    # Absence is not proof this attempt never ran; this ID is
                    # never retried. The next explicit case ID is different.
                preflight(interpreter,inventory)
                env=dict(PATH='/usr/bin:/bin',HOME=str(cwd),LANG='C.UTF-8',LC_ALL='C.UTF-8')
                child=subprocess.Popen(plan['loss'],cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                assert select.select([child.stdout],[],[],5)[0], 'checkpoint timeout'
                event=child.stdout.readline(16385)
                assert len(event)<=16384 and json.loads(event)['checkpoint']==name[5:]
                child.kill(); stdout,stderr=child.communicate(timeout=2)
                log.mkdir(parents=True,exist_ok=True)
                (log/'loss.stdout').write_bytes(event+stdout);(log/'loss.stderr').write_bytes(stderr)
                (log/'loss.json').write_text(json.dumps(dict(argv=plan['loss'],env=env,returncode=child.returncode,pid=child.pid))+'\n')
                assert child.returncode==-signal.SIGKILL
                assert (Path(root)/(key(name)+'.spent')).exists()
                r=invoke(plan['transaction'],log/'replay'); assert r.returncode==2,'loss reconstructed grant'
            elif name.startswith('kernel-'):
                r=invoke(plan['fault'],log/'fault'); assert r.returncode==2,'fault accepted'
                assert b'INJECTED' in r.stderr or b'DELAYED' in r.stderr,'fault not observed'
                assert (Path(root)/(key(name)+'.spent')).exists()
                assert not list(Path(root+'-ledger').iterdir()),'downstream escaped failed durability'
                r=invoke(plan['transaction'],log/'replay'); assert r.returncode==2,'failed marker reused'
            elif name=='store-capacity':
                for i in range(256):
                    fd=os.open(str(Path(root)/('%064x.spent'%i)),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
                r=invoke(plan['transaction'],log/'capacity'); assert r.returncode==2
                assert b'StoreCapacity' in r.stdout and len(list(Path(root).glob('*.spent')))==256
            elif name in ('boot-quarantine','source-generation-kind-lock'):
                p=Path(root)/'issuer.json'; data=json.loads(p.read_bytes())
                data['boot' if name=='boot-quarantine' else 'source']='quarantined'
                p.write_text(json.dumps(data)+'\n')
                r=invoke(plan['transaction'],log/'quarantine'); assert r.returncode==2 and b'StoreQuarantined' in r.stdout
                assert not list(Path(root).glob('*.spent'))
                if name=='source-generation-kind-lock':
                    typed=plan['typed_metadata']
                    r=invoke(typed['admin'],log/'typed-admin'); assert r.returncode==0
                    metadata_path=Path(typed['root'])/'issuer.json'
                    typed_data=json.loads(metadata_path.read_bytes());typed_data['uid']=float(typed_data['uid'])
                    metadata_path.write_text(json.dumps(typed_data)+'\n')
                    r=invoke(typed['transaction'],log/'typed-metadata');assert r.returncode==2 and b'StoreMetadataType' in r.stdout
                    assert not list(Path(typed['root']).glob('*.spent'))
                    for role,control in plan['identity_controls'].items():
                        r=invoke(control['admin'],log/(role+'-admin')); assert r.returncode==0
                        preflight(interpreter,inventory)
                        child=subprocess.Popen(control['transaction'],cwd=cwd,env=dict(PATH='/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                        assert select.select([child.stdout],[],[],5)[0],'identity checkpoint timeout'
                        event=child.stdout.readline(16385);assert json.loads(event)['checkpoint']=='binding-written'
                        target=Path(control['root'])/({'lock':'issuer.lock','metadata':'issuer.json','marker':key('identity-marker')+'.spent'}[role])
                        retained=Path(control['root']+'-retained-'+role)
                        os.rename(target,retained)
                        fd=os.open(target,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.write(fd,b'FOREIGN');os.close(fd)
                        out,err=child.communicate(timeout=3)
                        (log/(role+'.stdout')).write_bytes(event+out);(log/(role+'.stderr')).write_bytes(err)
                        (log/(role+'.json')).write_text(json.dumps(dict(argv=control['transaction'],returncode=child.returncode))+'\n')
                        assert child.returncode==2 and b'StoreFileRetargeted' in out,'store file replacement accepted'
                        assert target.read_bytes()==b'FOREIGN' and retained.exists()
                        assert not list(Path(control['root']+'-ledger').iterdir())
            elif name=='same-id-race':
                preflight(interpreter,inventory)
                children=[subprocess.Popen(plan['transaction'],cwd=cwd,env=dict(PATH='/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8'),stdout=subprocess.PIPE,stderr=subprocess.PIPE) for _ in range(2)]
                outcomes=[];log.mkdir(parents=True,exist_ok=True)
                for i,child in enumerate(children):
                    out,err=child.communicate(timeout=5);outcomes.append(child.returncode)
                    (log/('race%d.stdout'%i)).write_bytes(out);(log/('race%d.stderr'%i)).write_bytes(err)
                assert sorted(outcomes)==[0,2],outcomes
                assert len(list(Path(root).glob('*.spent')))==1
                (log/'race.json').write_text(json.dumps(dict(argv=plan['transaction'],returncodes=outcomes))+'\n')
                preflight(interpreter,inventory)
                holder=subprocess.Popen(plan['distinct_holder'],cwd=cwd,env=dict(PATH='/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                assert select.select([holder.stdout],[],[],5)[0],'lock holder checkpoint timeout'
                event=holder.stdout.readline(16385);assert json.loads(event)['checkpoint']=='marker-created'
                contender=invoke(plan['distinct_contender'],log/'distinct-contender')
                out,err=holder.communicate(timeout=3)
                (log/'distinct-holder.stdout').write_bytes(event+out);(log/'distinct-holder.stderr').write_bytes(err)
                (log/'distinct-holder.json').write_text(json.dumps(dict(argv=plan['distinct_holder'],returncode=holder.returncode))+'\n')
                assert holder.returncode==0 and contender.returncode==2,'store lock not exclusive across IDs'
                assert not (Path(root)/(key(name+'-contender')+'.spent')).exists()
            elif name=='cached-or-customized-deployment':
                package=interpreter.parent.parent/'lib/python3.13/site-packages/reference_controller'
                cache=package/'__pycache__';cache.mkdir()
                try:
                    try:preflight(interpreter,inventory)
                    except RuntimeError:pass
                    else:raise AssertionError('cache accepted')
                finally:cache.rmdir() # owned negative fixture, not canonical or grant repair
                site=package.parent/'sitecustomize.py';site.write_text("raise RuntimeError('MUST NOT EXECUTE')\n")
                try:
                    try:preflight(interpreter,inventory)
                    except RuntimeError:pass
                    else:raise AssertionError('customization accepted')
                finally:site.unlink()
            elif name=='foreign-source-bootstrap':
                # Real deployment manifest is DATA. Substituting another origin is
                # refused by bootstrap before the CLI imports or store effects.
                p=interpreter.parent.parent/'wordling-test-deployment.json'; old=p.read_bytes()
                data=json.loads(old);data['executable']='/foreign/python';p.write_text(json.dumps(data))
                try:
                    r=run(plan['transaction'],cwd,log/'foreign')
                    assert r.returncode==2 and b'DeploymentManifest' in r.stdout
                    assert not list(Path(root).glob('*.spent'))
                finally:p.write_bytes(old)
                preflight(interpreter,inventory)
                argv=plan['transaction']+['--checkpoint','activated']
                child=subprocess.Popen(argv,cwd=cwd,env=dict(PATH='/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                assert select.select([child.stdout],[],[],5)[0],'source checkpoint timeout'
                event=child.stdout.readline(16385)
                assert json.loads(event)['checkpoint']=='activated'
                changed=interpreter.parent.parent/'lib/python3.13/site-packages/reference_controller/account.py'
                original=changed.read_bytes(); changed.write_bytes(original+b'\n# intentional closed negative source drift\n')
                try:
                    out,err=child.communicate(timeout=3)
                    (log/'drift.stdout').write_bytes(event+out);(log/'drift.stderr').write_bytes(err)
                    (log/'drift.json').write_text(json.dumps(dict(argv=argv,returncode=child.returncode))+'\n')
                    assert child.returncode==2 and b'SourceChanged' in out,'source drift accepted'
                    assert not list(Path(root+'-ledger').iterdir())
                finally:
                    changed.write_bytes(original)
                    if child.poll() is None: child.kill();child.communicate(timeout=2)
            else:raise AssertionError('unimplemented case '+name)
            elapsed=time.monotonic()-begin
            assert elapsed<=30,'case time exceeded'
            results.append(dict(case=name,status='PASS',elapsed_seconds=elapsed))
        except BaseException as exc:
            results.append(dict(case=name,status='FAIL',reason=repr(exc),elapsed_seconds=time.monotonic()-begin))
    (evidence/'functional-results.json').write_text(json.dumps(dict(results=results,elapsed_seconds=time.monotonic()-started),indent=2)+'\n')
    return results
