from pathlib import Path
import json,hashlib,subprocess
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e');B=R/'internal/document/evidence/wp44';O=Path('/tmp/wordling-wp44-independent');canonical=lambda j:hashlib.sha256(json.dumps(j,sort_keys=True,separators=(',',':')).encode()).hexdigest();sha=lambda b:hashlib.sha256(b).hexdigest();rows=[];pins=set();pids=set();work=set();wire_events=0
for phase in range(1,8):
 D=B/'runs'/f'wp44-v2-phase{phase:02d}';pre=json.load(open(D/'prelaunch.json'));run=json.load(open(D/'run.json'));plan=pre['plan'];assert canonical(plan)=='8ced3932f91ee2dff2160e0deb222a9bc7e24e20c1225746d6c58e4ca557f2f0';lookup={x['id']:x for x in plan['attempts']};grant=pre['grant'];assert grant['authorized']is True and grant['maximum_aggregate_attempts']==49 and grant['transition_authorization']['authorized_by_root']is True;assert grant['transition_authorization']['historical_spent']==1
 for s in plan['sources']:
  n=s['path'];p=D/'runner-source'/n
  if p.suffix=='.go':p=p.with_name(p.name+'.txt')
  b=p.read_bytes();assert len(b)==s['size']and sha(b)==s['sha256'];assert b==(R/n).read_bytes();pins.add(n)
 for row in run['results']:
  ident=row['id'];L=D/ident;leaf=lookup[ident];assert row['qemu_argv']==leaf['qemu_argv']==row['owned_start_identity']['argv'];identity=row['owned_start_identity'];assert type(identity['pid'])is int and identity['pid']>0 and identity['startticks'].isdigit()and int(identity['startticks'])>0;assert identity['pid']not in pids;pids.add(identity['pid']);assert leaf['private_work']not in work;work.add(leaf['private_work']);assert all(str(Path(leaf['private_work'])/n)==d for n,d in zip(['boot.img','harddisk.img'],identity['private_disks']));assert identity['executable']=='/usr/bin/qemu-system-i386';assert any(a.startswith('unix:'+identity['socket']+',')for a in identity['argv'])
  assert row['normal_DOS'] and(L/'clean-exit/screen.txt').read_text().splitlines()[0]=='C:\\WP51>';assert row['observations']['fast_save']['after']=='no';assert row['stop_method']=='QMP quit; own socket terminated'
  proof=row['stop_proof'];assert proof['pid']==identity['pid']and proof['startticks']==identity['startticks']and proof['socket_absent']and proof['gone_or_same_zombie'];assert 1<=len(row['stop_observations'])<=102
  final=row['stop_observations'][-1];assert final['classification']in['gone','zombie']and final['socket_present']is False;assert final['observation_complete_monotonic']<=final['deadline_monotonic']
  if final['classification']=='zombie':assert final['state']=='Z'and final['startticks']==identity['startticks']
  else:assert final['pid_present']is False
  wire=[json.loads(x)for x in(L/'qmp-wire.jsonl').read_text().splitlines()];decoded=[]
  for x in wire:
   try:q=json.loads(bytes.fromhex(x['raw_hex']))
   except ValueError:continue
   if q.get('execute')=='quit'or q.get('event')=='SHUTDOWN':decoded.append((x['direction'],q))
  assert sum(q.get('execute')=='quit'for _,q in decoded)==1;assert any(q.get('event')=='SHUTDOWN'and q['data']['reason']=='host-qmp-quit'for _,q in decoded);wire_events+=len(decoded)
  case=next(c for c in plan['cases']if c['id']==leaf['case']);asset='candidate'if leaf['mode']=='candidate'else'source';assetname='C44INPUT'if asset=='candidate'else'C44SEED';assert(L/'input-after.WP5').read_bytes()==(R/case[asset]).read_bytes();assert sha((D/'inputs'/case['id']/asset).read_bytes())==case[asset+'_sha256'];assert all(x.get('passed')for x in row['checks'])
  rows.append({'id':ident,'pid':identity['pid'],'preboot60source_archive_verified':True,'normal_DOS':True,'FastSaveNo':True,'exact_frozen_argv':True,'input_asset_exact_after':True,'actual_quit_shutdown_wire':decoded,'terminal_stop_class':final['classification'],'PRE_sha':sha((L/'C44PRE.WP5').read_bytes()),'PRN_sha':sha((L/'C44PRN.PRN').read_bytes())})
assert len(rows)==48 and len(pins)==60
# Post-release final17 seals (not included in the historical859 prelaunch tree).
m=json.load(open(B/'final-review/seals.json'))
for n,w in m['files'].items():
 b=(B/n).read_bytes();assert len(b)==w['size']and sha(b)==w['sha256'];assert subprocess.check_output(['git','-C',str(R),'show','HEAD:'+str((B/n).relative_to(R))])==b
(O/'raw-audit.json').write_text(json.dumps({'actual48runs':rows,'all60_archived_source_pins_each_phase':True,'distinct_owned_PIDs':len(pids),'fresh_private_paths':len(work),'final_Git_seals':len(m['files']),'no_VM_or_failed_disk_access':True},indent=2)+'\n');print('48 exact source/argv/input/QMP/DOS/FastSaveNo/terminal-stop bindings; final',len(m['files']),'Git seals exact')
