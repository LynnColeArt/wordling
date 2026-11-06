#!/usr/bin/env python3
"""WP25 sealed12 serial scheduling only; original semantics live in invoke.py.

No guest/input/settings/global mutations here. A failed premise stops that recipe
family; independent families continue. Controls must both qualify before Go Q.
"""
from datetime import datetime,timezone
import hashlib,json,sys,traceback
from pathlib import Path
import invoke
HERE=Path(__file__).resolve().parent
status={'started_at':datetime.now(timezone.utc).isoformat(),'scope':'root-authorized finite12 guests; no additional variants','source_commit':'14d8f21d38b42a38bdc61bd1e2af7dd263b20bf2','scheduler_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'attempts':[],'skipped':[]}
plan=json.loads((invoke.CANDIDATES/'sealed-plan.json').read_text())
for relative,expected in plan['source_hashes'].items():
 if hashlib.sha256((invoke.ROOT/relative).read_bytes()).hexdigest()!=expected:raise ValueError('Pinned producer/API/parser source changed: '+relative)
for case in plan['cases']:
 if hashlib.sha256((invoke.CANDIDATES/case['name']/'candidate.WP5').read_bytes()).hexdigest()!=case['candidate_sha256']:raise ValueError('Changed emitted candidate')

def persist():invoke.write(HERE/'batch-result.json',status)
def pair(kind,name):
 for repeat in (1,2):
  row={'kind':kind,'name':name,'repeat':repeat,'started_at':datetime.now(timezone.utc).isoformat()};status['active']=row;persist()
  try:invoke.invoke(kind,name,repeat)
  except Exception as e:
   row.update(result='failed',error=str(e),traceback=traceback.format_exc());status['attempts'].append(row);status.pop('active',None)
   if repeat==1:status['skipped'].append({'kind':kind,'name':name,'repeat':2,'reason':'affected family stopped after failed required premise'})
   persist();print('STOPPED FAMILY',kind,name,str(e),flush=True);return False
  row.update(result='completed',finished_at=datetime.now(timezone.utc).isoformat());status['attempts'].append(row);status.pop('active',None);persist()
 return True

persist()
for name in ('ascii-modes','bold-insert-g1','bold-typeover-g2','bold-typeover-g5'):pair('candidate',name)
if pair('control','two-pair-typeover-Q'):
 try:invoke.seal_control()
 except Exception as e:status['control_seal_error']=str(e);status['skipped'].append({'kind':'candidate','name':'two-pair-typeover-Q','repeats':[1,2],'reason':'control streams could not qualify'});persist()
 else:pair('candidate','two-pair-typeover-Q')
else:status['skipped'].append({'kind':'candidate','name':'two-pair-typeover-Q','repeats':[1,2],'reason':'original control premise failed'})
status['finished_at']=datetime.now(timezone.utc).isoformat();persist()
raise SystemExit(0 if len(status['attempts'])==12 and all(r['result']=='completed' for r in status['attempts']) and not status['skipped'] else 1)
