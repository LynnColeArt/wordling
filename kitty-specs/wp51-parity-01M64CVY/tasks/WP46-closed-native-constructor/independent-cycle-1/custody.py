from pathlib import Path
import json,hashlib
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e');B=R/'internal/document/evidence/wp46';O=Path('/tmp/wordling-wp46-independent');h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[]
for phase,executing in [('wp46-phase01','9507242'),('wp46-phase02','9507242'),('wp46ev3-phase01','a10c0a24')]:
 D=B/'runs'/phase;pre=json.loads((D/'prelaunch.json').read_text());p=pre['plan'];r=json.loads((D/'run.json').read_text());assert r['complete']and r['guard_released']and r['oracle_released']and r['master_after']==p['master']and r['master_unchanged'];assert len(r['results'])==4
 ledger=json.loads((D/'aggregate-ledger.json').read_text());assert all(x['outcome']=='complete-observation'for x in ledger['attempts'])
 for pin in p['sources']:
  path=D/'runner-source'/pin['path'];path=path.with_name(path.name+'.txt')if path.suffix in ['.go','.py']else path;assert h(path)==pin['sha256']and path.stat().st_size==pin['size']
 for index,row in enumerate(r['results']):
  d=D/row['id'];leaf=next(x for x in p['attempts']if x['id']==row['id']);assert row['normal_DOS']and row['guest_stopped']and row['exports_complete']and row['stop_method']=='QMP quit; own socket terminated'
  owner=row['owned_start_identity'];assert owner['pid']>0 and int(owner['startticks'])>0 and owner['argv']==row['qemu_argv']==leaf['qemu_argv'];assert owner['private_disks']==[leaf['private_work']+'/'+n for n in ['boot.img','harddisk.img']];assert owner['socket']==p['socket']
  obs=row['stop_proof']['observations'];last=obs[-1];assert last['classification']in ['gone','same-zombie']and not last['socket_present']and last['observation_complete_monotonic']<=last['deadline_monotonic'];assert row['stop_proof']['gone_or_same_zombie']and row['stop_proof']['socket_absent']
  wire=[json.loads(x)for x in (d/'qmp-wire.jsonl').read_text().splitlines()];quits=[x for x in wire if x['direction']=='tx-buffer'and json.loads(bytes.fromhex(x['raw_hex'])).get('execute')=='quit'];assert len(quits)==1 and quits[0]['monotonic']<=last['monotonic'];assert any(b'host-qmp-quit'in bytes.fromhex(x['raw_hex'])for x in wire if x['direction']=='rx')
  for export in row['exports']:assert export['present']and export['exit']==0 and Path(export['path']).stat().st_size==export['size']and h(Path(export['path']))==export['sha256']
  if leaf['mode']=='candidate':assert row['input_after']['sha256']==p['cases'][0 if row['case']=='empty-edit'else 1]['candidate_sha256']if phase!='wp46ev3-phase01'else row['input_after']['sha256']==p['cases'][0]['candidate_sha256']
  normal=(d/'input-normal/screen.txt').read_text();reveal=(d/'input-Reveal-gap0/screen.txt').read_text();assert 'Doc 1'in normal and 'Reveal Codes to restore'in reveal
  if phase=='wp46ev3-phase01':
   assert row['required_output_qualification']['closed_relation']['prospective_outcome']=='H1-empty-counter-only-e72402'
   assert (d/'C46PRN.PRN').read_bytes()==b'\r\r'+b'\r\n'*66
   if leaf['mode']=='candidate':
    # Both accepted complete controls precede any candidate ledger row, same batch.
    assert index>=2 and [x['id']for x in ledger['attempts'][:2]]==[p['attempts'][0]['id'],p['attempts'][1]['id']]
  rows.append({'phase':phase,'leaf':row['id'],'executing_source':executing,'source_archive_exact':True,'kernel_QMP_stop_and_stopped_exports':True,'actual_normal_Reveal_captures':True})
failed=json.loads((B/'runs/wp46ev2-phase01/run.json').read_text());assert not failed['complete']and len(failed['results'])==1 and failed['results'][0]['qualification_error_code']=='EmptyPostprintUnexpected';oldledger=json.loads((B/'runs/wp46ev2-phase01/aggregate-ledger.json').read_text());assert oldledger['halted']and len(oldledger['attempts'])==1
new=json.loads((B/'runs/wp46ev3-phase01/aggregate-ledger.json').read_text());assert not new['halted']and new['old_accepted_complete']==8 and new['old_incomplete']==1 and new['cumulative_maximum_including_failures']==13 and len(new['attempts'])==4
(O/'custody.json').write_text(json.dumps({'observations':rows,'qualified':12,'historical_incomplete':1,'failure_inclusive_total':13,'failed_control_requalified':False,'new_guests':0},indent=2)+'\n');print('PASS12 original observation kernel/QMP/source/input/native/PRN/normalReveal custody; old1incomplete+cumulative13 exact')
