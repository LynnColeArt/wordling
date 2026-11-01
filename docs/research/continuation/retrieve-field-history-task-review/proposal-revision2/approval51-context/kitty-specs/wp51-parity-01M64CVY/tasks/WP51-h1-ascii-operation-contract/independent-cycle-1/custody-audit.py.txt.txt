import json,hashlib,subprocess
from pathlib import Path
R=Path.cwd();H=R/'internal/document/evidence/h1-admission-contract';O=Path('/tmp/wordling-wp51-independent');checked={}
def audit(row,revision='HEAD'):
 p=row.get('path');b=(R/p).read_bytes();size=row.get('size',row.get('bytes'));assert len(b)==size and hashlib.sha256(b).hexdigest()==row['sha256'],p;oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert oid==subprocess.check_output(['git','rev-parse',revision+':'+p],text=True).strip(),p
 if 'git_blob'in row:assert oid==row['git_blob'],p
 checked[p]=row['sha256']
counts={}
for name in ['protected-baseline.json','cycle2-seals.json','postrun/wp51-h1-phase01/postrun-manifest.json']:
 d=json.loads((H/name).read_text());rows=d['files'];rows=[{'path':k,**v}for k,v in rows.items()]if isinstance(rows,dict)else rows
 for row in rows:audit(row)
 counts[name]=len(rows)
p=json.loads((H/'preflight.json').read_text())['plan'];assert len(p['sources'])==366
for pin in p['sources']:audit(pin,'0b4f9d14ae448ce94906d1c1090e69bd7b1e1a4f')
run=H/'runs/wp51-h1-phase01';report=json.loads((run/'run.json').read_text());ledger=json.loads((run/'aggregate-ledger.json').read_text());assert len(report['results'])==len(ledger['attempts'])==1 and ledger['halted']and not report['complete']and not report['oracle_released'];row=report['results'][0];assert row['outcome']=='incomplete'and row['guest_stopped']and not row['normal_DOS']and row['error_code']=='UnknownFrame'and row['extraction_skipped']and'exports'not in row
for pin in p['sources']:
 path=run/'runner-source'/pin['path'];path=path.with_name(path.name+'.txt')if path.suffix in ['.go','.py']else path;assert hashlib.sha256(path.read_bytes()).hexdigest()==pin['sha256']
wire=[json.loads(x)for x in(run/row['id']/'qmp-wire.jsonl').read_text().splitlines()];messages=[(e,json.loads(bytes.fromhex(e['raw_hex'])))for e in wire];quit=[e for e,m in messages if e['direction']=='tx-buffer'and m.get('execute')=='quit'];shutdown=[e for e,m in messages if e['direction']=='rx'and m.get('event')=='SHUTDOWN'and m.get('data',{}).get('reason')=='host-qmp-quit'];assert len(quit)==len(shutdown)==1;assert quit[0]['monotonic']<=row['stop_proof']['observations'][-1]['observation_complete_monotonic'];assert row['master_after']==p['master'];entry=ledger['attempts'][0];assert hashlib.sha256((run/row['id']/'result.json').read_bytes()).hexdigest()==entry['result_file_sha256'];assert not any((run/x['id']).exists()for x in p['attempts'][1:]);assert not any((run/row['id']/name).exists()for name in ['H51S0.WP5','H51S1.WP5','H51FIN.WP5','H51PRN.PRN','input-after.WP5'])
rootrelease=(H/'postrun/wp51-h1-phase01/root-host-safety-release.json').read_bytes();assert rootrelease==Path('/tmp/wordling-WP51-phase01-root-safety-release.json').read_bytes();assert hashlib.sha256(rootrelease).hexdigest().startswith('3621a168')
# Grant/root release checked as metadata snapshots; NEVER read live private ledger/failed HD.
grant=(H/'postrun/wp51-h1-phase01/root-grant.json').read_bytes();assert hashlib.sha256(grant).hexdigest()=='fd8d9cb0b7dbf5091dc1f0c2b75e06f08ac1bdaa36af240211c80c2957868a12';s=json.loads(rootrelease);assert s['root_logical_reservation_released']and not s['qualified']and not s['normal_DOS']and not s['exports_completed']and s['new_attempts_spent']==1
(O/'custody-audit.json').write_text(json.dumps({'checked_file_counts':counts,'executing_source_pins':366,'runner_archives_exact':366,'distinct_public_paths_checked':len(checked),'attempts':1,'incomplete':1,'qualified':0,'abandoned_unstarted':7,'normal_DOS':False,'new_native_exports':0,'actual_normal_QMP_positive_stop':True,'driver_oracle_released':False,'root_host_safety_release_only':True,'private_failed_HD_access':False},indent=2)+'\n');print(json.dumps(counts))
