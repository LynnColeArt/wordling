#!/usr/bin/env python3
"""Append immutable offline witnesses from ALREADY captured raw app bytes.
Original optional full-style matrices were live aliases; they are not rewritten.
The independently copied role/text/cursor/offset records must still match raw.
"""
import hashlib,json
from pathlib import Path
from run_pty import Styled
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 target=HERE/'raw-replay.json';assert not target.exists()
 original=HERE/'pty-07/result.json';receipt=json.loads(original.read_bytes());result={'schema':'wordling.wp52.immutable-offline-raw-replay/v1','captured_receipt_sha256':sha(original.read_bytes()),'observer_source_sha256':sha((HERE/'run_pty.py').read_bytes()),'sealer_sha256':sha(Path(__file__).read_bytes()),'not_new_application_execution':True,'old_full_matrices':'live-aliased optional diagnostic values; excluded from accepted assertions','processes':{}}
 for r in receipt['results']:
  raw=(HERE/'pty-07'/('native-r'+str(r['repeat']))/'wire-output.bin').read_bytes();assert sha(raw)==r['raw_wire_sha256'];rows=[]
  for w in r['witnesses']:
   t=Styled();t.feed(raw[:w['wire_bytes']]);assert not t.unknown and t.rows()==w['rows'] and [t.x,t.y]==w['cursor'] and t.roles(3)==w['roles']
   # Serialize immediately, never retain a mutable matrix from a live observer.
   rows.append(json.loads(json.dumps({'wire_bytes':w['wire_bytes'],'gap':w['gap'],'view':w['view'],'cursor':[t.x,t.y],'rows':t.rows(),'styles':t.styles,'roles':t.roles(3)})))
  result['processes'][str(r['repeat'])]=rows
 target.write_text(json.dumps(result,separators=(',',':'))+'\n')
if __name__=='__main__':main()
