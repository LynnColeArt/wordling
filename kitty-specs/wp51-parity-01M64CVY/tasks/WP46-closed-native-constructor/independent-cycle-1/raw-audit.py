from pathlib import Path
import json,hashlib,subprocess,tempfile,importlib.util
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e');B=R/'internal/document/evidence/wp46';O=Path('/tmp/wordling-wp46-independent');h=lambda b:hashlib.sha256(b).hexdigest()
sync=json.loads((O/'stale-sync.json').read_text());pins=sync['inputs'];assert len(pins)==24012 and sync['whole_merge_exit']==0
# Exact tree identity plus independent Git blob SHA256+size, deduplicating blobs.
trees={}
for ref in [sync['before'],sync['after']]:
 rows=subprocess.check_output(['git','ls-tree','-r','-z',ref],cwd=R).split(b'\0');trees[ref]={p.decode():info.split()[2].decode()for row in rows if row for info,p in [row.split(b'\t',1)]}
unique={}
for n,v in pins.items():
 assert trees[sync['before']][n]==trees[sync['after']][n]==v['git_blob'];assert (R/n).stat().st_size==v['size']and h((R/n).read_bytes())==v['sha256'];assert v['git_blob']not in unique or unique[v['git_blob']]==(v['sha256'],v['size']);unique[v['git_blob']]=(v['sha256'],v['size'])
with tempfile.TemporaryFile()as requests:
 requests.write(('\n'.join(unique)+'\n').encode());requests.seek(0);proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=requests,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for oid,(want,size)in unique.items():
  head=proc.stdout.readline().split();assert head[0].decode()==oid and head[1]==b'blob'and int(head[2])==size;digest=hashlib.sha256();left=size
  while left:chunk=proc.stdout.read(min(left,65536));assert chunk;digest.update(chunk);left-=len(chunk)
  assert proc.stdout.read(1)==b'\n'and digest.hexdigest()==want
 assert proc.stdout.read(1)==b''and proc.wait(timeout=60)==0
sets=[]
for root,manifest in [(R,B/'seals.json'),(B/'empty-successor',B/'empty-successor/seals.json'),(B/'empty-successor-v3',B/'empty-successor-v3/seals.json'),*[(B/'runs'/name,B/'runs'/name/'seals.json')for name in ['wp46-phase01','wp46-phase02','wp46ev2-phase01','wp46ev3-phase01']]]:
 s=json.loads(manifest.read_text())['files']
 for n,v in s.items():assert h((root/n).read_bytes())==v['sha256']and(root/n).stat().st_size==v['size']
 sets.append({'manifest':str(manifest.relative_to(R)),'count':len(s)})
assert h((B/'runs/wp46ev3-phase01/seals.json').read_bytes())=='600725ab9167bd2ecc5cce0eaa3f6bcc664856a3f75fd2fa17261e17ad6780f3'
assert h((B/'final-handoff.md').read_bytes())=='d7c52608443ba0e8080c0d3fb5465cf1dcfd4cf77ff15b3981497d30a707a06a'
# Replay public consumers/field/complete native/PRN comparisons; temporary re-edits only.
spec=importlib.util.spec_from_file_location('wp46_review_oracle',B/'oracle.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
old_results=[]
for name in ['wp46-phase01','wp46-phase02']:
 v=old.result(B/'runs'/name/'run.json');assert len(v['qualified_observations'])==4;old_results.extend(v['qualified_observations'])
spec=importlib.util.spec_from_file_location('wp46_review_v3',B/'empty-successor-v3/adapter.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a);v3=a.result(B/'runs/wp46ev3-phase01/run.json');assert v3['all4_new_complete']and v3['cumulative_spent']==13
assert all(x['closed_relation']['prospective_outcome']=='H1-empty-counter-only-e72402'for x in v3['qualified_new_observations'])
(O/'reader-native-results.json').write_text(json.dumps({'old8':old_results,'new4':v3},indent=2)+'\n');(O/'raw-audit.json').write_text(json.dumps({'source':sync['after'],'code_evidence_source':sync['before'],'24012_working_and_both_tree_Gitbindings_exact':True,'Git_unique_blobs_hashed':len(unique),'sets':sets,'actual_public_reader_Q_72fields_original_native_print_controls':12,'historical_incomplete_requalified':False,'VM_runs':0},indent=2)+'\n');print('PASS24012 source/owned paths plus uniqueGit blobs, allsealedsets,12qualified actual public readers/Q/native/PRN; historicalfailed1unchanged')
