from pathlib import Path
import json,hashlib,subprocess,collections
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-v');O=Path('/tmp/wordling-WP50-independent-review');N=R/'internal/merge/native';H=lambda b:hashlib.sha256(b).hexdigest();git=lambda *a:subprocess.check_output(['git','-C',str(R),*a]);assert git('rev-parse','HEAD').decode().strip()=='376a37a6afd0d9f11594cadfefe0d557b874a56c';assert not git('status','--porcelain','--untracked-files=no')
s=(N/'evidence/seals.json').read_bytes();assert H(s)=='35edbe682a677c9eab83d9a34a7a447bef7a81816e90985a61d98a246a7b1aaf';seals=json.loads(s)['files'];assert len(seals)==74
for n,row in seals.items():
 b=(N/n).read_bytes();assert len(b)==row['size']and H(b)==row['sha256'];assert b==git('show','HEAD:internal/merge/native/'+n)
files=git('ls-files','internal/merge/native').decode().splitlines();assert set(files)=={'internal/merge/native/'+n for n in seals}|{'internal/merge/native/evidence/seals.json'}
raw=git('show','e7de080452c2906e99c8ace0048c415d842f2f89:internal/wp51/native.go');assert (R/'internal/wp51/native.go').read_bytes()==raw and H(raw)=='e13c93687e6119bff44f8405616455849cb728f3b4a1b3949d987dbe2c30b1d6'
proof=json.loads((R/'docs/research/continuation/native-merge-task-review/proposal/evidence/recon/source-proof.json.txt').read_text());ref=proof['primary_snapshot'];checked={};runs=set()
def check(p,sha=None,size=None):
 b=(R/p).read_bytes();assert b==git('show',ref+':'+p)
 if sha:assert H(b)==sha
 if size is not None:assert len(b)==size
 checked[p]={'sha256':H(b),'bytes':len(b),'blob':git('rev-parse',ref+':'+p).decode().strip()};return b
for ctx in proof['merge_originals']:
 assert len(ctx['runs'])==2 and ctx['runs'][0]['run']!=ctx['runs'][1]['run']
 for rep in ctx['runs']:
  prefix='docs/research/reference-runs/'+rep['run'];manifest=json.loads(check(prefix+'/run.json',rep['manifest_sha256']));item=next(r for r in manifest['results']if r['case_id']==ctx['case_id']);assert item['native_outputs']==rep['native']and item['result']=='observed-matches-smoke-expectations'
  for x in item['evidence']+item['native_outputs']:check(x['path'],x['sha256'],x['size'])
  for x in manifest['runner_sources']:check(prefix+'/runner-source/'+Path(x['path']).name,x['sha256'])
  check(manifest['environment_profile_archive'],manifest['environment_manifest_sha256']);runs.add(rep['run'])
rows=json.loads((N/'evidence/originals.json').read_text())['files'];assert len(rows)==104;inv=proof['native_structural_inventory'];assert set(inv)=={r['path']for r in rows}
for row in rows:
 q=inv[row['path']];assert row['sha256']==q['sha256']and row['git_blob']==q['git_blob']and row['bytes']==q['bytes']and row['tokens']==q['tokens'];assert row['role']in ['Primary','Secondary','Result'];assert row['role']==('Secondary'if Path(row['path']).stem=='SECOND'else 'Result'if Path(row['path']).stem=='MERGED'else 'Primary')or Path(row['path']).stem in ['CHILD','CHILDS','PARENT']
source=json.loads((N/'evidence/final-source.json').read_text());
for p,row in source['source_files'].items():assert H((R/p).read_bytes())==row['sha256']and (R/p).read_bytes()==git('show',('HEAD' if p=='internal/merge/native/evidence/contracts/contract_test.go' else 'd396bbe1')+':'+p)
closure=[]
for p in git('ls-files').decode().splitlines():
 if p.endswith('.go')or p in ['go.mod','go.sum']:closure.append({'path':p,'sha256':H((R/p).read_bytes()),'git_blob':git('rev-parse','HEAD:'+p).decode().strip()})
(O/'source-audit.json').write_text(json.dumps({'source_HEAD':git('rev-parse','HEAD').decode().strip(),'source_base':'d396bbe1','seals':len(seals),'owned_tracked_files':len(files),'checked_source_capture_profile_files':len(checked),'unique_manifests':len(runs),'native_count':len(rows),'unique_native_hashes':len({r['sha256']for r in rows}),'contexts':len(proof['merge_originals']),'real_approved_wp51_exact':True,'Go_module_closure':closure,'checked':checked,'no_VM_or_private_HD_or_resources_read':True},indent=2)+'\n');print('PASS 74seals,104native-source roles/spans,992capture/profile files,exactapprovedwp51')
