"""Twelve groups /46 finite DATA variants. No actual capture/TCB authority minted."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import time
import runtime_qualification as q

ROOT=Path('/tmp/wordling-WP70-own-maps-DATA-controls-01')
S=Path(__file__).resolve().parent.parent
OUTCOME=S/'evidence/WP70-TCB-qualification-01'
GROUPS=(
 ('actual_history',('historical_v3_refusal','actual_trace_one_event')),
 ('initial_exec',('missing_initial','wrong_binary','wrong_argv','failed_initial','truncated_initial','maps_before_exec')),
 ('actor_binding',('foreign_return','foreign_actor','unbound_actor','renumbered_missing_capture')),
 ('epochs_descendants',('reexec_same','reexec_different','lineaged_descendant')),
 ('literal_request',('numeric_same','thread_self','dot_alias','other_proc_file')),
 ('exact_flags',('cloexec','readwrite','path_only','write_create')),
 ('exact_syscall',('legacy_open','openat2')),
 ('capture_boundary',('missing_token','json_complete','pid_scalar','boolean','constructed_unregistered_token','partial_json','unknown_tail_json')),
 ('source_use_denial',('exec_proc','module_proc','cache_proc','elf_proc')),
 ('complete_framing',('missing_newline','unfinished','wrong_resumed_actor','unknown_actor_frame')),
 ('later_errors',('later_missing_code','later_error_frame')),
 ('invariants',('joined_positive','failed_map_not_admitted','no_query_static','manifest_no_growth')),
)


def refused(fn):
    try:fn()
    except (RuntimeError,ValueError,SyntaxError) as e:return type(e).__name__+':'+str(e)
    raise AssertionError('ExpectedRefusal')


def main():
    start=time.monotonic();end=start+30;ROOT.mkdir(mode=0o700,exist_ok=False)
    raw=(OUTCOME/'runtime-receipts/deployment/venv.trace').read_text()
    launch=json.loads((OUTCOME/'runtime-receipts/deployment/venv.whole.json').read_text())['logical_argv']
    actor=3604519;other=actor+1
    initial=raw.splitlines()[0]+'\n'
    proc=f'{actor} openat(AT_FDCWD</DATA-CWD>, "/proc/self/maps", O_RDONLY) = 3</proc/{actor}/maps>\n'
    pair=initial+proc
    stable_manifest=(OUTCOME/'expected-inputs.json.gz').read_bytes();manifest_hash=hashlib.sha256(stable_manifest).hexdigest()
    results=[];variants=0
    def check(name):
        if name=='historical_v3_refusal':
            stderr=(OUTCOME/'guardian/stderr.raw').read_text();whole=json.loads((OUTCOME/'external-execution/whole.json').read_text())
            assert 'UnavailableToolOrigin:/proc/3604519/maps' in stderr and whole['exit']==2
            assert hashlib.sha256(raw.encode()).hexdigest()=='b2ad823d594f4e29f2eaa1afd1a785e14886ed00e1c657840fb61d44bc14b166'
            return dict(old_genuine_V3_RED='Retained actual execution, never rerun old checker/proc query')
        if name=='actual_trace_one_event':
            data=q.historical_data_review(raw,launch)
            assert len(data['transient'])==1 and data['transient'][0]['lines']==[22,22]
            assert data['transient'][0]['contents']=='UNKNOWN/not captured' and not data['production_authority']
            return data['transient'][0]
        negative={
          'missing_initial':proc,
          'wrong_binary':initial.replace(launch[0],'/different/pinned-program',1)+proc,
          'wrong_argv':initial.replace('"-I"','"-S"')+proc,
          'failed_initial':initial.removesuffix(' = 0\n')+' = -1 ENOENT (No such file or directory)\n'+proc,
          'truncated_initial':initial.replace('"-I"','"-I"...')+proc,
          'maps_before_exec':proc+initial,
          'foreign_return':initial+proc.replace('3</proc/'+str(actor)+'/maps>','3</proc/'+str(other)+'/maps>'),
          'foreign_actor':initial+proc.replace(str(actor),str(other)),
          'unbound_actor':initial+proc.replace(str(actor),str(actor+99)),
          'reexec_same':initial+initial+proc,
          'reexec_different':initial+f'{actor} execve("/usr/bin/true", ["true"], 0x0) = 0\n'+proc,
          'lineaged_descendant':initial+f'{actor} clone(child_stack=NULL, flags=SIGCHLD) = {other}\n'+initial.replace(str(actor)+' ',str(other)+' ',1)+proc.replace(str(actor),str(other)),
          'numeric_same':initial+proc.replace('"/proc/self/maps"','"/proc/'+str(actor)+'/maps"'),
          'thread_self':initial+proc.replace('/proc/self/maps','/proc/thread-self/maps'),
          'dot_alias':initial+proc.replace('/proc/self/maps','/proc/self/./maps'),
          'other_proc_file':initial+proc.replace('/maps','/status'),
          'cloexec':initial+proc.replace('O_RDONLY','O_RDONLY|O_CLOEXEC'),
          'readwrite':initial+proc.replace('O_RDONLY','O_RDWR'),
          'path_only':initial+proc.replace('O_RDONLY','O_PATH'),
          'write_create':initial+proc.replace('O_RDONLY','O_WRONLY|O_CREAT'),
          'legacy_open':initial+proc.replace('openat(AT_FDCWD</DATA-CWD>, ','open('),
          'openat2':initial+proc.replace('openat(','openat2('),
          'exec_proc':initial+f'{actor} execve("/proc/self/maps", [], 0x0) = 0\n',
          'missing_newline':pair.removesuffix('\n'),
          'unfinished':initial+f'{actor} openat(AT_FDCWD, "/proc/self/maps", O_RDONLY <unfinished ...>\n',
          'wrong_resumed_actor':initial+f'{actor} openat(AT_FDCWD, "/proc/self/maps", O_RDONLY <unfinished ...>\n{other} <... openat resumed>) = 3</proc/{actor}/maps>\n',
          'unknown_actor_frame':initial+proc.removeprefix(str(actor)+' '),
          'later_error_frame':pair+'UNFRAMED UNKNOWN SUCCESS\n',
        }
        if name in negative:return dict(refusal=refused(lambda:q.historical_data_review(negative[name],launch)))
        capture={
          'missing_token':None,'json_complete':dict(complete=True,EOF=True,exit=0,actor=actor),'pid_scalar':actor,
          'boolean':True,'constructed_unregistered_token':q._RunCapture(),'partial_json':dict(partial=True,complete=False),'unknown_tail_json':dict(complete=True,tail='UNKNOWN'),
        }
        if name in capture:
            # No fake positive provenance: an uninitialized owner cannot mint a
            # real capture; rejection occurs before reading ANY supplied path.
            owner=object.__new__(q.Preparation)
            return dict(refusal=refused(lambda:owner.tool_origins('/proc/self/maps','DATA',capture[name])))
        if name=='renumbered_missing_capture':
            synthetic=pair.replace(str(actor),str(actor+10));data=q.historical_data_review(synthetic,launch)
            assert not data['production_authority']
            owner=object.__new__(q.Preparation)
            return dict(synthetic_DATA=True,production_refusal=refused(lambda:owner.tool_origins('/proc/self/maps','DATA',data)))
        if name in ('module_proc','cache_proc','elf_proc'):
            datafile=ROOT/'NONEXECUTABLE-DATA';datafile.write_bytes(b'DATA ONLY')
            v=datafile.parent.parent;interpreter=datafile
            v=interpreter.parent.parent;site=v/'lib/python3.12/site-packages'
            obs=dict(sys_path=[str(q.PREFIX/'lib/python312.zip'),str(q.PREFIX/'lib/python3.12'),str(q.PREFIX/'lib/python3.12/lib-dynload'),str(site)],version=[3,12,14],executable=str(interpreter),prefix=str(v),exec_prefix=str(v),base_prefix=str(q.PREFIX),base_exec_prefix=str(q.PREFIX),flags=dict(debug=0,inspect=0,interactive=0,optimize=0,dont_write_bytecode=1,no_user_site=1,no_site=0,ignore_environment=1,verbose=0,bytes_warning=0,quiet=0,hash_randomization=1,isolated=1,dev_mode=False,utf8_mode=0,warn_default_encoding=0,safe_path=True,int_max_str_digits=-1),default_excepthook=True,customize={},features={'DATA':True},modules={},maps={},project=None)
            field=dict(path='/proc/'+str(actor)+'/maps',exists=True,size=0,sha256='0'*64)
            if name=='elf_proc':obs['maps']={field['path']:dict(size=0,sha256='0'*64)}
            else:obs['modules']={'FORGED-DATA':{'__file__' if name=='module_proc' else '__cached__':field}}
            return dict(refusal=refused(lambda:q.compare_observation(obs,interpreter,dict(files={},runtime_elf=[],runtime_mapped_data=[]),{},False)),synthetic_negative_only=True)
        if name=='later_missing_code':
            changed=pair+f'{actor} openat(AT_FDCWD, "/missing/arbitrary-code.py", O_RDONLY) = 3</missing/arbitrary-code.py>\n'
            return dict(refusal=refused(lambda:q.historical_data_review(changed,launch,{launch[0]})))
        if name=='joined_positive':
            joined=initial+proc.replace(') = 3', ' <unfinished ...>\n'+str(actor)+' <... openat resumed>) = 3')
            data=q.historical_data_review(joined,launch);assert len(data['transient'])==1;return data['transient'][0]
        if name=='failed_map_not_admitted':
            failed=initial+proc.removesuffix(' = 3</proc/'+str(actor)+'/maps>\n')+' = -1 ENOENT (No such file or directory)\n'
            data=q.historical_data_review(failed,launch);assert data['transient']==[];return dict(failed_open_is_not_exception=True)
        if name=='no_query_static':
            tree=ast.parse(Path(q.__file__).read_text());names={'_quoted_argument','_exec_argv','parse_trace','_transient_maps_events','historical_data_review'}
            calls=[]
            for node in tree.body:
                if isinstance(node,ast.FunctionDef) and node.name in names:
                    for call in (n for n in ast.walk(node) if isinstance(n,ast.Call)):
                        if isinstance(call.func,ast.Attribute):
                            assert call.func.attr not in ('resolve','exists','is_file','stat','lstat','open','read','read_text','read_bytes')
                        if isinstance(call.func,ast.Name):assert call.func.id not in ('Path','open','pin','same','eval','exec')
                    calls.append(node.name)
            assert set(calls)==names;return dict(pinned_pure_callgraph=calls,actual_proc_queries=0,filesystem_monkeypatch=False)
        if name=='manifest_no_growth':
            before=hashlib.sha256((OUTCOME/'expected-inputs.json.gz').read_bytes()).hexdigest();registry_before=len(q._CAPTURES)
            data=q.historical_data_review(pair,launch);assert data['production_authority'] is False
            assert before==manifest_hash and registry_before==len(q._CAPTURES)==0
            return dict(stable_manifest_sha256=before,production_capture_count=0,no_growth=True)
        raise AssertionError('UnlistedVariant:'+name)
    for group,names in GROUPS:
        group_results=[]
        for name in names:
            if time.monotonic()>=end:raise RuntimeError('DATAAggregateDeadline')
            result=check(name);variants+=1;group_results.append(dict(variant=name,status='PASS',result=result))
            print(json.dumps(dict(group=group,variant=name,status='PASS')),flush=True)
        results.append(dict(group=group,variants=group_results));(ROOT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    assert len(GROUPS)==12 and variants==46
    print(json.dumps(dict(status='PASS',groups=12,distinct_DATA_variants=variants,elapsed=time.monotonic()-start,production_capture_objects=0,TCB_qualification=False,P=False)))
    return 0

if __name__=='__main__':
    try:result=main()
    except BaseException:
        import traceback;traceback.print_exc();result=2
    raise SystemExit(result)
