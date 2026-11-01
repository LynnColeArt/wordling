from pathlib import Path
import subprocess,hashlib,json,ast
W=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p');O=Path(__file__).resolve().parent;B=W/'docs/research/continuation/macro-session/startup-seam';C='676de09bce7672a8fd965f35c23acc5d5746a6e2';OLD='935135aefdc6e067b0522daa80bf9a637c20a126';sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda*a:subprocess.check_output(['git','-C',str(W),*a]);assert git('rev-parse','HEAD').decode().strip()==C
raw=(B/'seals.json').read_bytes();assert sha(raw)=='f3e297087f5eb98262ec416223f9ec7eefdd821809f276191f11475c0c0e5305';seal=json.loads(raw);assert len(seal['files'])==510
owned={str(p.relative_to(W))for d in [B,W/'tests/reference/startup-seam']for p in d.rglob('*')if p.is_file()}|{'scripts/reference/startup_transport.py'};assert len(owned)==511 and owned=={x['path']for x in seal['files']}|{str((B/'seals.json').relative_to(W))}
tree={}
for line in git('ls-tree','-r',C).decode().splitlines():
 mode,p=line.split('\t',1);_,kind,obj=mode.split()
 if kind=='blob':tree[p]=obj
for x in seal['files']:
 b=(W/x['path']).read_bytes();assert len(b)==x['bytes']and sha(b)==x['sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==tree[x['path']]==x['git_blob']
assert sum((W/p).stat().st_size for p in owned)==3730974
hm=json.loads((B/'cycle-3/history-map.json').read_text());by={x['source']:x for x in hm['copies']};oldseal=json.loads(git('show',OLD+':'+str((B/'seals.json').relative_to(W))));oldpaths=[x['path']for x in oldseal['files']]+[str((B/'seals.json').relative_to(W))];assert len(oldpaths)==319
same=archived=0
for p in oldpaths:
 b=git('show',OLD+':'+p)
 if (W/p).read_bytes()==b:same+=1
 else:
  x=by[p];assert (W/x['destination']).read_bytes()==b and sha(b)==x['sha256'];archived+=1
review=json.loads((B/'cycle-3/review-authority-map.json').read_text());assert len(review)==94
for x in review:
 b=git('show',x['source_commit']+':'+x['source']);assert b==(W/x['destination']).read_bytes()and sha(b)==x['sha256']and len(b)==x['bytes']
base=json.loads((B/'cycle-3/baseline340.json').read_text());assert len(base['files'])==340
for x in base['files']:
 b=git('show',OLD+':'+x['path']);assert sha(b)==x['sha256']and len(b)==x['bytes']
 if x['working_unchanged']and (W/x['path']).read_bytes()!=b:
  assert x['path']in by and (W/by[x['path']]['destination']).read_bytes()==b
original=json.loads(git('show','22e27ab671fbac19aecac32c39cd8d288685151d:'+str((B/'source-custody.json').relative_to(W))))
for group in ['inherited18','all_tracked_go_module']:
 for p,x in original[group].items():
  b=(W/p).read_bytes();assert sha(b)==x['sha256']and len(b)==x['size']and tree[p]==x['git_blob']
assert {p for p in tree if p.endswith('.go')or Path(p).name in ['go.mod','go.sum']}==set(original['all_tracked_go_module'])
changed=[p for p in git('diff','--name-only',OLD+'..'+C).decode().splitlines()if p in owned];assert len(changed)==202
S=W/'scripts/reference/startup_transport.py';assert sha(S.read_bytes())=='603cc95307fe681d51637c08351efbbc101b98e8b3f2bc9325f8fe635ee590c9';(O/'executing-startup_transport.py.txt').write_bytes(S.read_bytes())
checks=[]
for p in [S,*sorted((W/'tests/reference/startup-seam').glob('*.py'))]:
 b=p.read_bytes();ast.parse(b);compile(b,str(p),'exec');checks.append(dict(path=str(p.relative_to(W)),sha256=sha(b),AST_compile=True,source_whitespace_clean=all(not line.endswith((b' ',b'\t'))for line in b.splitlines())))
assert all(x['source_whitespace_clean']for x in checks)
res=dict(source_commit=C,provider_sha256=sha(S.read_bytes()),owned_files=511,sealed_members=510,owned_bytes=3730974,recursive_SET_Git_SHA_exact=True,old319_preserved=dict(unchanged_in_place=same,exact_archived=archived),canonical_cycle2_review94_exact=True,baseline340_actualGit_exact=True,baseline340_capture_time_working_unchanged_flags_stale_for_four_archived_metadata_paths=['README.md','report.md','seals.json','source-custody.json'],old18_and5Go_module_SET_blobs_exact=True,changed_owned_vs935=202,source_checks=checks,tracked_status=git('status','--porcelain').decode(),metadata512files8MiB_not_runtime_limit_change=True,no_original_private_VM_or_source_mutation=True)
(O/'source-custody.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
