#!/usr/bin/env python3
"""Serial enumeration only. No guest semantics/settings/input/global mutation."""
import json,sys,traceback
from datetime import datetime,timezone
from pathlib import Path
import invoke
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
 plan=invoke.check();status={'scope':'root-authorized14 finite candidate guests; no new original controls','scheduler_sha256':invoke.sha(__file__),'started_at':datetime.now(timezone.utc).isoformat(),'attempts':[],'skipped':[]}
 def persist():invoke.write(HERE/'batch-result.json',status)
 persist()
 for case in plan['unique_whole_byte_candidates']:
  name=case['name']
  for repeat in(1,2):
   row={'name':name,'repeat':repeat,'started_at':datetime.now(timezone.utc).isoformat()};status['active']=row;persist()
   try:invoke.invoke(name,repeat)
   except Exception as e:
    row.update(result='failed',error=str(e),traceback=traceback.format_exc());status['attempts'].append(row);status.pop('active',None)
    if repeat==1:status['skipped'].append({'name':name,'repeat':2,'reason':'affected family stopped on unmet premise'})
    persist();break
   row.update(result='complete',finished_at=datetime.now(timezone.utc).isoformat());status['attempts'].append(row);status.pop('active',None);persist()
 status['finished_at']=datetime.now(timezone.utc).isoformat();persist()
 sys.exit(0 if len(status['attempts'])==14 and all(x['result']=='complete'for x in status['attempts'])and not status['skipped']else 1)
