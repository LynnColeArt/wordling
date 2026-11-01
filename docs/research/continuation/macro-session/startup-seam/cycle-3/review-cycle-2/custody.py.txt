from pathlib import Path
import subprocess,hashlib,json
W=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p');R=Path('/home/lynn/projects/wordling');O=Path(__file__).resolve().parent;C='935135aefdc6e067b0522daa80bf9a637c20a126';OLD='22e27ab671fbac19aecac32c39cd8d288685151d';B=W/'docs/research/continuation/macro-session/startup-seam';sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda *a:subprocess.check_output(['git','-C',str(W),*a]);assert git('rev-parse','HEAD').decode().strip()==C
sealraw=(B/'seals.json').read_bytes();assert sha(sealraw)=='5a9b8aa08858152d894b17f22ebf87e6eb5643cf99ae25f55ca49f797882568d';s=json.loads(sealraw);assert len(s['files'])==318;owned={str(p.relative_to(W))for d in [B,W/'tests/reference/startup-seam']for p in d.rglob('*')if p.is_file()}|{'scripts/reference/startup_transport.py'};assert len(owned)==319 and owned=={x['path']for x in s['files']}|{str((B/'seals.json').relative_to(W))}
tree={}
for line in git('ls-tree','-r',C).decode().splitlines():
 m,p=line.split('\t',1);mode,kind,obj=m.split()
 if kind=='blob':tree[p]=obj
for x in s['files']:
 b=(W/x['path']).read_bytes();assert len(b)==x['bytes']and sha(b)==x['sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==tree[x['path']]==x['git_blob']
assert sum((W/p).stat().st_size for p in owned)==2128776
copies=json.loads((B/'cycle-2/history-map.json').read_text())['copies'];by={x['source']:x for x in copies};oldraw=git('show',OLD+':'+str((B/'seals.json').relative_to(W)));oldseal=json.loads(oldraw);oldpaths=[x['path']for x in oldseal['files']]+[str((B/'seals.json').relative_to(W))];assert len(oldpaths)==157
same=archived=0
for p in oldpaths:
 b=git('show',OLD+':'+p)
 if(W/p).read_bytes()==b:same+=1
 else:
  if p in by:
   row=by[p];assert (W/row['destination']).read_bytes()==b and sha(b)==row['sha256']
  else:
   assert p=='tests/reference/startup-seam/capture_cli.py';assert (B/'cycle-2/history/capture_cli.py.txt').read_bytes()==b
  archived+=1
review=json.loads((B/'cycle-2/review-authority-map.json').read_text());assert len(review)==48
for x in review:
 b=git('show',x['source_commit']+':'+x['source']);assert b==(W/x['destination']).read_bytes()and sha(b)==x['sha256']and len(b)==x['bytes']
base=json.loads((B/'cycle-2/baseline178.json').read_text());assert len(base['paths'])==178
original=json.loads(git('show',OLD+':'+str((B/'source-custody.json').relative_to(W))))
for p,x in original['inherited18'].items():
 b=(W/p).read_bytes();assert len(b)==x['size']and sha(b)==x['sha256']and tree[p]==x['git_blob']
for p,x in original['all_tracked_go_module'].items():
 b=(W/p).read_bytes();assert len(b)==x['size']and sha(b)==x['sha256']and tree[p]==x['git_blob']
go_current={p for p in tree if p.endswith('.go')or Path(p).name in ['go.mod','go.sum']};assert go_current==set(original['all_tracked_go_module'])
changed=[p for p in git('diff','--name-only',OLD+'..'+C).decode().splitlines()if p=='scripts/reference/startup_transport.py'or p.startswith('tests/reference/startup-seam/')or p.startswith('docs/research/continuation/macro-session/startup-seam/')];assert len(changed)==172;provider=(W/'scripts/reference/startup_transport.py').read_bytes();assert sha(provider)=='ea4095a3419ea94ea8943a4f50ce785982847df00496ce9efcbfdb184965150b';(O/'executing-startup_transport.py.txt').write_bytes(provider)
res=dict(source_commit=C,provider_sha256=sha(provider),owned319_closed_SET_and318_current_seals_Git_SHA_exact=True,owned_bytes=2128776,changed_owned_vs22e=172,old157_preserved=dict(byte_unchanged_in_place=same,superseded_byte_exact_copies=archived,total=157),canonical_cycle1_review48_byte_exact=True,nested_history_seal_included=True,exact_current_root_seal_only_excluded=True,old18_unchanged=True,old5_Go_module_SET_and_blobs_exact=True,packaging512files8MiB_NOT_runtime_cap_change=True,working_status=git('status','--porcelain').decode(),no_source_mutation_by_reviewer=True,no_original_VM_private_source_access=True)
(O/'source-custody.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
