"""Read-only byte ownership/difference ledger, never a native serializer.

Live fields have SDK meanings. Deleted/unowned extents retain raw provenance,
not guessed inner structures or edit permission. Every actual output is separately
classified by the approved reader and the stricter proposed mutation gate.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import native_edits as n

def compare(before,after,stage=None):
 before=Path(before);after=Path(after);a=before.read_bytes();b=after.read_bytes();x=n.inspect(a);y=n.inspect(b)
 owners=[None]*len(b)
 def mark(start,length,label):
  for pos in range(start,start+length):
   if owners[pos] is not None:raise ValueError('Alias/overlap cannot satisfy relationship audit')
   owners[pos]=label
 for offset,width,label in [(0,4,'signature'),(4,4,'body-start pointer'),(8,1,'product'),(9,1,'file type'),(10,1,'major'),(11,1,'minor'),(12,2,'encryption'),(14,2,'reserved')]:mark(offset,width,'header '+label)
 for block in y['blocks']:
  off=block['offset'];mark(off,2,'index header kind');mark(off+2,2,'index entry count');mark(off+4,2,'index size');mark(off+6,4,'next index absolute pointer')
  for e in block['entries']:
   p=off+10*e['slot'];mark(p,2,'packet type/deleted marker');mark(p+2,4,'packet byte length');mark(p+6,4,'packet absolute pointer')
 fields=json.loads((n.OUT/'field-ledger.json').read_text())['field_coverage']
 for packet in y['packets']:
  kind=packet['type']
  if kind==65535:mark(packet['offset'],packet['length'],'packet65535 raw deleted extent; inner semantics unclaimed');continue
  rows=[row for row in fields if row['owner']=='packet-'+str(kind)]
  if not rows or sum(row['width'] for row in rows)!=packet['length']:raise ValueError('Unsupported output live packet schema')
  for row in rows:mark(packet['offset']+row['offset'],row['width'],row['owner']+' '+row['name'])
 for pos in range(y['body_offset'],len(b)):owners[pos]='body declared ASCII/Bold tokens'
 # Gaps are retained literally and block mutation admission; do not decode them.
 for pos,label in enumerate(owners):
  if label is None:
   if pos>=len(a) or a[pos]!=b[pos]:raise ValueError('Unsupported changed index-unowned output bytes')
   owners[pos]='unchanged source byte at index-unowned output residue; mutation blocked'
 groups=defaultdict(list)
 for pos,label in enumerate(owners):
  if pos>=len(a) or a[pos]!=b[pos]:groups[label].append(pos)
 changed=[]
 for label,positions in groups.items():
  spans=[]
  for p in positions:
   if spans and spans[-1][1]==p:spans[-1][1]=p+1
   else:spans.append([p,p+1])
  changed.append({'owner':label,'changed_ranges_half_open':spans,'byte_count':len(positions)})
 live={}
 for k in (7,15,12,6,8):
  aa=[p for p in x['packets'] if p['type']==k];bb=[p for p in y['packets'] if p['type']==k]
  if len(aa)!=1 or len(bb)!=1:raise ValueError('Live resource multiplicity')
  pa,pb=aa[0],bb[0];ba=bytes.fromhex(pa['hex']);bc=bytes.fromhex(pb['hex'])
  if len(ba)!=len(bc):raise ValueError('Live packet length changed')
  diffs=[i for i,(u,v) in enumerate(zip(ba,bc)) if u!=v]
  allowed={6:{0,8},15:{21,22},7:set(),12:set(),8:set()}[k]
  if set(diffs)-allowed:raise ValueError('Unsupported live field relationship packet '+str(k))
  if k==6 and ((ba[0]^bc[0])&~8):raise ValueError('Unexplained document flag bit')
  if stage and k==6:
   expected_counter=2 if stage=='after_print' else 1
   if ba[8]!=1 or bc[8]!=expected_counter:raise ValueError('Unsupported contextual printer counter relationship')
   expected_flag={'retrieved':8,'edited':0,'after_print':0}.get(stage)
   if expected_flag is not None and bc[0]!=expected_flag:raise ValueError('Unsupported contextual original format flag')
  if stage and k==15:
   expected_hash=bytes.fromhex('1172') if stage=='after_print' else ba[21:23]
   if bc[21:23]!=expected_hash:raise ValueError('Unsupported contextual descriptor hash relationship')
  if k==15 and (ba[21:23] not in (bytes.fromhex('e724'),bytes.fromhex('1172')) or bc[21:23] not in (bytes.fromhex('e724'),bytes.fromhex('1172'))):raise ValueError('Unqualified descriptor hash variant')
  live[str(k)]={'from_offset':pa['offset'],'to_offset':pb['offset'],'changed_packet_relative_bytes':diffs,'before_sha256':hashlib.sha256(ba).hexdigest(),'after_sha256':hashlib.sha256(bc).hexdigest()}
 return {'stage':stage,'before':str(before),'after':str(after),'before_size':len(a),'after_size':len(b),'before_sha256':n.sha(before),'after_sha256':n.sha(after),'header_body_start':[x['body_offset'],y['body_offset']],'changed_destination_bytes':changed,'removed_source_tail_bytes':max(0,len(a)-len(b)),'live_relationships':live,'output_prefix_residue':y['coverage_issues'],'interpretation':'literal relocation/index/deleted/residue ledger; no normalization; deleted and unowned inner semantics remain mutation blockers'}
