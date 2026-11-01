import json,hashlib,subprocess
from pathlib import Path
from datetime import datetime
R=Path.cwd();H=R/'docs/research/continuation/new-session/interop-z-01';O=Path('/tmp/wordling-wp48-independent-cycle-2');before=json.loads(Path('/tmp/wordling-WP48-cycle2-before-target-merge.json').read_text());files={}
for item in subprocess.check_output(['git','ls-tree','-r','-z','HEAD']).split(b'\0'):
 if not item:continue
 info,p=item.split(b'\t',1);p=p.decode();oid=info.decode().split()[2]
 if not(p.endswith('.go')or p in ('go.mod','go.sum')or p.startswith(('internal/tui/','cmd/wordling/','docs/research/continuation/new-session/'))):continue
 b=(R/p).read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert blob==oid;files[p]={'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':blob}
assert files==before['files'];assert len(files)==2463
assert subprocess.check_output(['git','diff','--name-only','46afe8f5..HEAD','--','internal','cmd','go.mod','go.sum'])==b''
p=json.loads((H/'preflight.json').read_text())['plan'];run=R/p['public_output'];report=json.loads((run/'run.json').read_text());grant=(run/'grant.json').read_bytes();rootgrant=Path('/tmp/wordling-WP48-z-root-grant.json').read_bytes();assert hashlib.sha256(rootgrant).hexdigest()=='94f128f4b43e302dc9917fdeefda453efe1c7bc33f90c7af96db67b47c8a90ff';assert json.loads(rootgrant)==json.loads(grant);summary=[];last_release=None
for row in report['results']:
 d=run/row['id'];wire=[json.loads(x)for x in(d/'qmp-wire.jsonl').read_text().splitlines()];commands=[]
 for x in wire:
  if x['direction']=='tx-buffer':
   msg=json.loads(bytes.fromhex(x['raw_hex']));commands.append((msg,x))
 quitcmd=[(msg,x)for msg,x in commands if msg.get('execute')=='quit'];assert len(quitcmd)==1
 stop=row['stop_proof'];assert quitcmd[0][1]['monotonic']<=stop['observations'][-1]['observation_complete_monotonic']
 if last_release:assert datetime.fromisoformat(wire[0]['utc'])>datetime.fromisoformat(last_release)
 last_release=row['guard_release_utc'];assert datetime.fromisoformat(last_release)>datetime.fromisoformat(quitcmd[0][1]['utc']);trace=row['trace'];names=[x['capture']for x in trace if'capture'in x];assert names.index('print-C48PRN-submitted')<names.index('clean-exit')
 assert not[x for x in trace if x.get('key')in['ctrl-break']]
 identity=row['owned_start_identity'];assert int(identity['startticks'])>0 and identity['pid']>0 and identity['argv']==row['qemu_argv'];assert row['master_before']==row['master_after']==p['master'];summary.append({'id':row['id'],'pid':identity['pid'],'startticks':identity['startticks'],'quit_wire_utc':quitcmd[0][1]['utc'],'release_utc':last_release,'stop_elapsed_seconds':stop['elapsed_seconds'],'wire_records':len(wire),'trace_captures':len(names),'matched_normal_QMP_and_serial_release':True})
assert len({(x['pid'],x['startticks'])for x in summary})==4
(O/'custody-source-audit.json').write_text(json.dumps({'source':'54763f710c2bebd2ddfdf02f6f783d9df0d98660','before_target_merge':before['source_commit'],'source_owned_SET_Git_exact':len(files),'product_source_diff_from_cycle1':[],'root_grant_raw_sha256':hashlib.sha256(rootgrant).hexdigest(),'archived_grant_sorted_JSON_sha256':hashlib.sha256(grant).hexdigest(),'grant_values_identical':True,'actual_serial_custody':summary},indent=2)+'\n');print('2463 source/owned records exact; actual QMP/positive stop/serial release audited for4 originals')
