from pathlib import Path
import json,hashlib,sys,subprocess
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-l');sys.path.insert(0,str(R/'scripts/reference'));import wordling_edits as w
O=Path('/tmp/wordling-wp29-independent');P=json.loads((w.SUCCESSOR/'plan.json').read_text());ledger=json.loads((w.ORACLE/'ledger.json').read_text());old=json.loads((w.OUT/'oracle/ledger.json').read_text());manifest=json.loads((w.OUT/'final/artifact-manifest.json').read_text())
assert manifest['count']==len(manifest['records'])==7364 and manifest['total_bytes']==sum(r['size']for r in manifest['records'])==1043070144
assert old['halted'] and [x['outcome']for x in old['attempts']]==['accepted','accepted','incomplete-or-failed'];assert len(ledger['attempts'])==16 and ledger['prior_spent_attempts']==3 and ledger['cumulative_cap']==19 and not ledger['halted']
assert w.identity(w.OUT/'oracle/ledger.json')['sha256']==w.OLD_LEDGER
seen=set();rows=[]
for i,leaf in enumerate(P['original_leaves']):
 d=w.ORACLE/'runs'/('wp29-s01-'+leaf['id']);r=json.loads((d/'run.json').read_text());pre=json.loads((d/'owned-prelaunch.json').read_text());complete=json.loads((d/'leaf-complete.json').read_text());case=r['cases'][0];a=ledger['attempts'][i]
 assert a['leaf']==leaf and a['outcome']=='accepted'
 assert pre['exact_qemu_argv']==r['qemu_argv'] and pre['frozen_product']==P['product']
 assert complete['actual_leaf_argv']==pre['actual_leaf_argv']==a['argv']
 assert pre['actual_leaf_argv'][2:4]==['--leaf',leaf['id']]
 assert 'wp29-s01-'+leaf['id'] in pre['private_fresh_work'] and pre['private_fresh_work'] not in seen;seen.add(pre['private_fresh_work'])
 assert pre['root_grant']['max_attempts']==16 and pre['root_grant']['plan_sha256']==w.identity(w.SUCCESSOR/'plan.json')['sha256']
 assert pre['root_grant']['runner_sha256']=='89834b2f34437cc7918b16f185b6bc945fdc470c85a00682266fbd9dc616f3ac'
 assert w.identity(d/'runner-source/wordling_edits.py')['sha256']==pre['root_grant']['runner_sha256']
 for pin in r['runner_sources']:assert w.identity(d/pin['path'])=={k:pin[k]for k in ['size','sha256']}
 assert (d/'inputs/candidate.WP5').read_bytes()==(R/leaf['folder']/'files/CANDIDA').read_bytes()
 wire=[json.loads(x)for x in (d/'qmp-wire.jsonl').read_text().splitlines()];tx=[x for x in wire if x['direction']=='tx-buffer' and json.loads(bytes.fromhex(x['raw_hex'])).get('execute')=='quit'];assert len(tx)==1
 stop=r['owned_adapter']['stop'];assert stop['observations'][0]['monotonic']>=tx[-1]['monotonic'];assert not stop['observations'][-1]['socket_exists'] and (stop['observations'][-1]['process'] is None or stop['observations'][-1]['process']['state']=='Z')
 assert any(x['direction']=='rx'and b'host-qmp-quit'in bytes.fromhex(x['raw_hex'])for x in wire)
 assert r['clean_exit'] and r['guest_stopped'] and r['seed_unchanged'] and r['master_unchanged'] and r['master_before']==r['master_after']
 assert 'append-ascii-at-end'==r['candidate']['expected']['subsequent_edit']['command'] if 'expected'in r['candidate'] else True
 rows.append({'leaf':leaf['id'],'source_before_launch_bound':True,'actual_private_disks_unique':True,'exact_owned_argv':True,'normalDOS_QMPquit_then_positive_stop':True,'full_run_artifacts':len(r['artifacts'])})
sync=json.loads(Path('/tmp/wordling-WP29-stale-sync.json').read_text());assert sync['source_before']==sync['source_after'] and sync['owned_Git_blob_SET_before']==sync['owned_Git_blob_SET_after'] and sync['whole_merge_exit']==0
for n,h in sync['source_after'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h
for ref in ['6afecc04c96ced2f16dcf2601baa7a070a9045fe','6deb515079b4ed8ca2eaad6ced47b17a094977dc']:
 for n,h in sync['source_after'].items():assert hashlib.sha256(subprocess.check_output(['git','show',ref+':'+n],cwd=R)).hexdigest()==h
(O/'custody.json').write_text(json.dumps({'manifest_count':len(manifest['records']),'manifest_bytes':manifest['total_bytes'],'actual_fresh_successor':16,'immutable_old_controls':2,'immutable_old_incomplete':1,'cumulative19':True,'sync_exact_sources':len(sync['source_after']),'sync_owned_blob_set':len(sync['owned_Git_blob_SET_after']),'source_sync_unchanged':True,'rows':rows},indent=2)+'\n');print('PASS independent16 kernel/QMP/source/candidate/leaf custody; cumulative19 and exact source/owned Git sync')
