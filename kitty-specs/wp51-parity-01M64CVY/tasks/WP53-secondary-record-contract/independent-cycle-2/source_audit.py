from pathlib import Path
import json,hashlib,subprocess,ast,importlib.util,sys
sys.dont_write_bytecode=True
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-w');D=R/'docs/research/continuation/secondary-record-contract';O=Path('/tmp/wordling-WP53-independent-review/cycle-2');H=lambda b:hashlib.sha256(b).hexdigest();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert head=='f70310abb1127a645bf14e984cfcb6da64082713'
v=json.loads((D/'fix-cycle-1/seals.json').read_text());assert H((D/'fix-cycle-1/seals.json').read_bytes())=='ebf2e25d385877245df6c1b3a9cc74dbac7c87090fe62150222efebfc0989c04'
for p,x in v['files'].items():
 b=(R/p).read_bytes();assert len(b)==x['bytes']and H(b)==x['sha256'];assert subprocess.check_output(['git','rev-parse',head+':'+p],cwd=R,text=True).strip()==x['git_blob'];assert subprocess.check_output(['git','hash-object','--',p],cwd=R,text=True).strip()==x['git_blob']
root=json.loads(Path('/tmp/wordling-WP53-cycle2-before-target-merge.json').read_text())['files']
for p,x in root.items():
 b=(R/p).read_bytes();assert len(b)==x['size']and H(b)==x['sha256'];assert subprocess.check_output(['git','rev-parse',head+':'+p],cwd=R,text=True).strip()==x['git_blob']
old='8a0a78a3319741b4f98d3db58d69ad8c875de350';script='scripts/reference/secondary_record_contract.py';before=subprocess.check_output(['git','show',old+':'+script],cwd=R);after=(R/script).read_bytes();assert H(after)=='216d59f01cb596b1e3fca2c0005d86dbad89854231ac8e9923276039e28d67b8';assert(D/'fix-cycle-1/history/secondary_record_contract.py.txt').read_bytes()==before
oldseal=json.loads((D/'evidence/seals.json').read_text());assert H((D/'evidence/seals.json').read_bytes())=='767b72b003ddd924bf866cfb6c889dd8cdbb8b94ba8bc9e75b708944cd3d1d77';unchanged=0
for p,x in oldseal['files'].items():
 if p!=script:assert H((R/p).read_bytes())==x['sha256'];unchanged+=1
A={n.name:ast.dump(n,include_attributes=False)for n in ast.parse(before).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};B={n.name:ast.dump(n,include_attributes=False)for n in ast.parse(after).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};assert all(B[k]==x for k,x in A.items()if k!='bounded');assert set(B)-set(A)=={'_owned_group_pin','_drain_killed_pipes','_terminate_owned_group'}
# Fresh real source-bound helper composition/checks, no repeated original-domain audit.
s=importlib.util.spec_from_file_location('c',R/script);C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
with C.Session(R)as ss:
 for n,args in [('helper-build',['go','build','./...']),('helper-test',['go','test','-count=1','./...']),('helper-vet',['go','vet','./...']),('helper-race',['go','test','-race','-count=1','./...'])]:(O/(n+'.log')).write_bytes(ss.run(args))
 receipt=ss.build_proof();assert receipt['binary_sha256']=='2c3e3b929a4d097a9121326e670cdb09d633ff14f802e401e2dafc58113d2066';(O/'fresh-composition.json').write_text(json.dumps(receipt,indent=2)+'\n')
scopes=['scripts/reference/secondary_record_contract.py','docs/research/continuation/secondary-record-contract'];p=subprocess.run(['git','diff','--check',old,head,'--',*scopes],cwd=R,capture_output=True);assert p.returncode==0;(O/'fix-diff.log').write_bytes(p.stdout+p.stderr)
p=subprocess.run(['git','diff','--check','b858d14446daccffd89fa355ea9bda5c4daa226a',head,'--',*scopes],cwd=R,capture_output=True);assert p.returncode==2;(O/'whole-owned-diff.log').write_bytes(p.stdout+p.stderr)
result={'source_head':head,'fix_source':'eae7f09f214e5b719d3144aa12adef6b7fec9664','packaging':'6f823c316da6b412d25a2537a8196d062103be75','target_only_merge':'40a13aa777cb935cd1e99e733fca8f28d7ca0b7e','current_seals':len(v['files']),'root_working_Git_snapshot':len(root),'historical_seal_rows':len(oldseal['files']),'unchanged_old_rows':unchanged,'exact_old_source_archive':True,'all_existing_functions_except_bounded_AST_identical':True,'new_functions':sorted(set(B)-set(A)),'fresh_compiled_packages':len(receipt['packages']),'helper_binary':receipt['binary_sha256'],'fix_diff_check_exit':0,'whole_owned_diff_check_exit':2,'tracked_status':subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=R,text=True)};assert not result['tracked_status'];(O/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
