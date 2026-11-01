"""Focused subprocess lifetime faults, executed from inert copies, no source edit."""
from pathlib import Path
import ast,hashlib,json,os,subprocess,sys,time
R=Path(__file__).resolve().parents[5];F=Path(__file__).resolve().parent;E=F/'evidence';S=R/'scripts/reference/secondary_record_contract.py';source=S.read_text();rows=[]
mutants=[('reaped-leader-gate',
 [('''        except BaseException:
            _terminate_owned_group(process)
            raise
        finally:''','''        except BaseException:
            if process.poll() is None:
                _terminate_owned_group(process)
            raise
        finally:''')],
 'test_exited_leader_timeout','did not become reapable'),
 ('skip-escalation-for-exited-leader',
 [('''        _owned_group_pin(process)
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        _drain_killed_pipes(process)''','''        if _owned_group_pin(process) is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        _drain_killed_pipes(process)''')],
 'test_exited_leader_ignores_TERM','HelperTimeout')]
for name,changes,test,message in mutants:
 text=source
 for old,new in changes:assert text.count(old)==1,(name,old);text=text.replace(old,new)
 ast.parse(text);path=E/('mutant-'+name+'.py.txt');path.write_text(text)
 receipt=E/('mutant-'+name+'.json');env={**os.environ,'WP53_CHECKER_SOURCE':str(path),'WP53_CLEANUP_RECEIPT':str(receipt)}
 argv=[sys.executable,str(F/'test_cleanup.py'),'-k',test];started=time.monotonic();p=subprocess.run(argv,cwd=R,capture_output=True,timeout=15,env=env)
 log=p.stdout+p.stderr;(E/('mutant-'+name+'.log')).write_bytes(log)
 assert p.returncode==1 and b'FAILED (failures=1)'in log and message.encode()in log,(name,p.returncode,log)
 data=json.loads(receipt.read_text());assert data['results'][0].get('RED_emergency_cleanup_only_recorded_owned_group')
 rows.append({'name':name,'argv':argv,'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'exit':p.returncode,'seconds':time.monotonic()-started,'killed_by_OS_semantic_assertion':True,'no_source_or_native_mutation':True})
assert S.read_text()==source
(E/'mutants.json').write_text(json.dumps({'final_checker_sha256':hashlib.sha256(source.encode()).hexdigest(),'mutants':rows},indent=2)+'\n')
print(json.dumps({'executed':len(rows),'killed':len(rows),'actual_source_unchanged':True}))
