"""Bounded candidate input/provenance and exact interoperability comparison.

Called by native_edits.py after its candidate CLI is wired. No serializer or VM
is executed during preparation; no input/reference stream is modified.
"""
import hashlib
import json
from pathlib import Path
import stat
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_edits as n
from relationships import compare as compare_relationships
from classify_reader import classify

JSON_LIMIT=131072

def bounded(path,limit):
 path=Path(path).resolve()
 if not stat.S_ISREG(path.stat().st_mode):raise ValueError('Regular input required')
 with path.open('rb') as stream:data=stream.read(limit+1)
 if len(data)>limit:raise ValueError('Input budget')
 return path,data

def digest(data):return hashlib.sha256(data).hexdigest()

def prepare(candidate,provenance,expectations):
 path,data=bounded(candidate,n.LIMIT);pp,praw=bounded(provenance,JSON_LIMIT);ep,eraw=bounded(expectations,JSON_LIMIT)
 p=json.loads(praw);e=json.loads(eraw)
 if p.get('rights')!='project-authored scratch' or not p.get('producer') or not p.get('description'):raise ValueError('Lawful producer/fixture provenance required')
 if p.get('source_sha256')!=digest(data) or e.get('candidate_sha256')!=digest(data):raise ValueError('Candidate provenance identity mismatch')
 inspection=n.inspect(data,True)
 if e.get('schema_version')!=1 or e.get('input_body_hex')!=inspection['body_hex']:raise ValueError('Expected input body mismatch')
 if e.get('environment_sha256')!=n.sha(n.PROFILE):raise ValueError('Reference environment mismatch')
 edit=e.get('subsequent_edit',{})
 if edit.get('command')!='append-ascii-at-end' or edit.get('text')!='Z':raise ValueError('Only recorded Home3 Up End then insert Z is supported')
 expected=bytes.fromhex(edit['expected_body_hex']);n.body_tokens(expected)
 reference=e['reference_print'];rp,rdata=bounded(reference['path'],n.LIMIT)
 if digest(rdata)!=reference['sha256'] or len(rdata)!=reference['size'] or not rdata:raise ValueError('Complete reference print identity mismatch')
 return {'candidate_path':path,'candidate_bytes':data,'provenance_path':pp,'provenance_bytes':praw,'expectations_path':ep,'expectations_bytes':eraw,'reference_path':rp,'reference_bytes':rdata,'metadata':{'provenance':p,'expectations':e,'candidate_sha256':digest(data),'candidate_bytes':len(data),'input_body_hex':inspection['body_hex']}}

def run(p,prepared):
 p.retrieve('B:\\CANDIDAT','candidate-retrieved')
 retrieved=p.snapshot('candidate-retrieved-native')
 p.key('home,home,home,up,end');p.capture('candidate-before-subsequent-edit');p.type('Z');p.capture('candidate-after-subsequent-edit')
 edited=p.snapshot('candidate-edited-native')
 name=f'P{p.counter:04d}';p.counter+=1
 n.print_disk(p,name)
 printed=p.snapshot('candidate-postprint-native')
 p.cases.append({'id':'candidate-interop','canonical_leads':['CMD51-046','CMD51-065','CMD51-066','CMD51-145'],'scope':'local candidate interoperability proposal; no whole canonical comparison','source':'inputs/candidate.WP5','retrieved':retrieved,'edited':edited,'after_print':printed,'print_stream':name+'.PRN','expected_input_body_hex':prepared['metadata']['input_body_hex'],'expected_edited_body_hex':prepared['metadata']['expectations']['subsequent_edit']['expected_body_hex']})

def compare(directory,run):
 directory=Path(directory);c=run['cases'][0];e=run['candidate']['expectations'];result={'scope':'original candidate Retrieve/edit/print/Save; not full Wordling/physical verification','accepted':False,'checks':[],'unresolved':[]}
 def check(name,value):
  result['checks'].append({'check':name,'passed':bool(value)})
  if not value:result['unresolved'].append(name)
 check('completed original with captured final DOS',run.get('clean_exit') and (directory/'clean-exit/screen.txt').read_text().splitlines()[0]=='C:\\WP51>')
 cursor=json.loads((directory/'clean-exit/cursor.json').read_text())
 check('actual final DOS hardware cursor',cursor.get('row')==0 and cursor.get('column')==8 and cursor.get('cursor_word')==8)
 check('readonly candidate seed unchanged',run.get('seed_unchanged') is True)
 check('source candidate unchanged on host',n.sha(run['candidate_source_path'])==run['candidate']['candidate_sha256'])
 for name,expected in [('retrieved',e['input_body_hex']),('edited',e['subsequent_edit']['expected_body_hex']),('after_print',e['subsequent_edit']['expected_body_hex'])]:
  path=directory/c[name]
  if not path.exists():check('missing native '+name,False);continue
  try:observed=n.inspect(path.read_bytes(),False)
  except ValueError as error:result['unresolved'].append(name+': '+str(error));continue
  check('exact '+name+' native body',observed['body_hex']==expected)
  # Original metadata/deleted/slack is retained literally and separately refused
  # for mutation. Unknown live field changes prevent interoperability acceptance.
  try:
   relation=compare_relationships(directory/c['source'],path)
  except ValueError as error:result['unresolved'].append(name+' relationship: '+str(error))
  else:result.setdefault('relationships',{})[name]=relation
 reader=classify([directory/c[k] for k in ('retrieved','edited','after_print')]);result['actual_reader']=reader
 check('actual approved reader reopens all original outputs losslessly',all(x['accepted'] and x.get('exact_no_edit_export') for x in reader['files']))
 check('actual empty print job capture',all(text in (directory/('settings-print-'+Path(c['print_stream']).stem+'-job-status')/'screen.txt').read_text() for text in ('Job Number: None','No print jobs','Additional Jobs Not Shown: 0')))
 check('exact complete reference printer bytes',(directory/c['print_stream']).read_bytes()==(directory/'inputs/reference.PRN').read_bytes())
 result['accepted']=not result['unresolved'] and all(x['passed'] for x in result['checks'])
 return result
