from pathlib import Path
import hashlib,json,subprocess,importlib.util,sys,xml.etree.ElementTree as ET
sys.dont_write_bytecode=True
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-w');O=Path('/tmp/wordling-WP53-independent-review');D=R/'docs/research/continuation/secondary-record-contract';H=lambda b:hashlib.sha256(b).hexdigest();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert head=='8a0a78a3319741b4f98d3db58d69ad8c875de350'
rows=json.loads((D/'evidence/seals.json').read_text())['files']
for path,x in rows.items():
 b=(R/path).read_bytes();assert len(b)==x['bytes']and H(b)==x['sha256'];assert subprocess.check_output(['git','hash-object','--',path],cwd=R,text=True).strip()==x['git_blob'];assert subprocess.check_output(['git','rev-parse',head+':'+path],cwd=R,text=True).strip()==x['git_blob']
rootpins=json.loads(Path('/tmp/wordling-WP53-before-target-merge.json').read_text())['files']
for path,x in rootpins.items():
 b=(R/path).read_bytes();assert len(b)==x['size']and H(b)==x['sha256'];assert subprocess.check_output(['git','rev-parse',head+':'+path],cwd=R,text=True).strip()==x['git_blob']
changed=subprocess.check_output(['git','diff','--name-only','b858d14446daccffd89fa355ea9bda5c4daa226a',head],cwd=R,text=True).splitlines();assert len(changed)==80;assert all(x=='scripts/reference/secondary_record_contract.py'or x.startswith('docs/research/continuation/secondary-record-contract/')for x in changed)
s=importlib.util.spec_from_file_location('checker',R/'scripts/reference/secondary_record_contract.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
with C.Session(R)as ss:
 report=C.audit(ss);receipt=ss.build_proof();assert report==json.loads((D/'evidence/original-audit.json').read_text());assert report['native_inputs']==30 and report['native_bytes']==14484;assert receipt['binary_sha256']=='2c3e3b929a4d097a9121326e670cdb09d633ff14f802e401e2dafc58113d2066'
 for name,args in [('helper-build',['go','build','./...']),('helper-vet',['go','vet','./...']),('helper-race',['go','test','-race','-count=1','./...'])]:(O/(name+'.log')).write_bytes(ss.run(args))
 (O/'fresh-original-audit.json').write_text(json.dumps(report,indent=2)+'\n');(O/'fresh-composition.json').write_text(json.dumps(receipt,indent=2)+'\n')
# Historical full diff whitespace remains honestly failed; nonlog paths pass.
p=subprocess.run(['git','diff','--check','b858d14446daccffd89fa355ea9bda5c4daa226a',head],cwd=R,capture_output=True);(O/'committed-diff.log').write_bytes(p.stdout+p.stderr);assert p.returncode==2
nonlog=[x for x in changed if not x.endswith('.log')];q=subprocess.run(['git','diff','--check','b858d14446daccffd89fa355ea9bda5c4daa226a',head,'--',*nonlog],cwd=R,capture_output=True);assert q.returncode==0
v={'head':head,'owned_seals':len(rows),'root_working_and_Git_snapshot':len(rootpins),'owned_changed_paths':len(changed),'inherited_Go_module_set':len(json.loads((D/'authority.json').read_text())['inherited_go_module_files']),'fresh_original_audit_equal':True,'native_inputs':report['native_inputs'],'native_bytes':report['native_bytes'],'compiled_packages':len(receipt['packages']),'binary':receipt['binary_sha256'],'committed_diff_check_exit':p.returncode,'nonlog_paths':len(nonlog),'nonlog_diff_check_exit':q.returncode,'tracked_source_status':subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=R,text=True)};assert not v['tracked_source_status'];(O/'source-audit.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v,indent=2))
