#!/usr/bin/env python3
"""Audit actual WP23 artifacts/semantics; partial observations never imply completion."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_edits as n
from codepane_cursor import gap as code_gap,block_selection,plain_gap
from relationships import compare as relationship_compare
from print_audit import audit as print_audit
BOLD=bytes.fromhex('41c30cc34243c40cc444')

def digest(data):return hashlib.sha256(data).hexdigest()
def raw_body(path):
 data=Path(path).read_bytes()
 if len(data)<16:raise ValueError('Native header missing')
 offset=int.from_bytes(data[4:8],'little')
 if not 16<=offset<=len(data):raise ValueError('Body bounds')
 return data[offset:]
def observation(path):
 data=Path(path).read_bytes();row={'path':str(Path(path).relative_to(ROOT)),'size':len(data),'sha256':digest(data),'body_offset':int.from_bytes(data[4:8],'little'),'body_hex':raw_body(path).hex()}
 try:row['inspection']=n.inspect(data,False)
 except ValueError as e:row['inspection_refusal']=str(e)
 try:n.inspect(data,True)
 except ValueError as e:row['mutation_admission']=False;row['mutation_refusal']=str(e)
 else:row['mutation_admission']='conditional-contract-only'
 return row

def validate_run(path):
 path=Path(path).resolve();run=json.loads((path/'run.json').read_text())
 if run['scope']!='original-reference-only' or run['wordling_tested'] is not False:raise ValueError('Scope promoted')
 for a in run['artifacts']:
  raw=(path/a['path']).read_bytes()
  if (len(raw),digest(raw))!=(a['size'],a['sha256']):raise ValueError('Raw artifact changed')
 for a in run['runner_sources']:
  if n.sha(path/a['path'])!=a['sha256']:raise ValueError('Executing source changed')
 if not run['master_unchanged'] or run['master_before']!=run['master_after']:raise ValueError('Master changed')
 if n.sha(path/'environment.json')!=run['profile_sha256']:raise ValueError('Profile archive changed')
 profile=json.loads((path/'environment.json').read_text())
 if run['master_before']!={'boot.img':profile['master_boot_sha256'],'harddisk.img':profile['master_disk_sha256']}:raise ValueError('Wrong master/profile association')
 if run['runtime']!={'socket':str(n.PRIVATE/'runtime/qmp.sock'),'lock':str(n.PRIVATE/'session1.lock')}:raise ValueError('Wrong shared reference runtime/lock')
 if run['result']=='observed':
  disk='file='+str(n.PRIVATE/'native-edit-runs'/run['run_id']/'harddisk.img')+',format=raw,if=ide,index=0'
  if disk not in run['qemu_argv']:raise ValueError('Wrong fresh-copy run identity/drive')
  for setting in run['settings']:
   if n.sha(path/setting['capture'])!=setting['screen_sha256']:raise ValueError('Settings capture association changed')
  resources=json.loads((ROOT/'docs/research/reference-environment/resource-profile.json').read_text())['resources']
  for resource in run['resources']:
   if resource['path']=='WP{WP}.SET':continue # actual changed Other-port setting remains hashed, not normalized
   fixed=resources['WP51/'+resource['path']]
   if (resource['size'],resource['sha256'])!=(fixed['size'],fixed['sha256']):raise ValueError('Original installed resource identity changed')
  selected=json.loads((HERE/'selected-settings.json').read_text())['screen_sha256']
  actual={x['label']:x['screen_sha256'] for x in run['settings'][:5]}
  if actual!=selected:raise ValueError('Original selected initial settings changed')
 if run['result']!='observed':return {'run_id':run['run_id'],'recipe':run['recipe'],'result':run['result'],'error':run.get('error'),'accepted':False}
 if not run.get('clean_exit') or (path/'clean-exit/screen.txt').read_text().splitlines()[0]!='C:\\WP51>':raise ValueError('No actual final DOS capture')
 if not (path/'clean-exit/cursor.json').exists():raise ValueError('Missing final hardware cursor')
 cursor=json.loads((path/'clean-exit/cursor.json').read_text())
 if (cursor.get('row'),cursor.get('column'),cursor.get('cursor_word'))!=(0,8,8):raise ValueError('Incorrect final DOS hardware cursor')
 if any(not c['passed'] for c in run['checks']):raise ValueError('Failed original check')
 cases=[]
 for case in run['cases']:
  source=raw_body(path/case['source']);final=raw_body(path/case['final']);cid=case['case_id'];label=case['id']
  expected=None
  if label=='ascii-modes':
   if cid!='CMD51-046' or source!=b'abc' or raw_body(path/case['intermediate'])!=b'aXc':raise ValueError('ASCII mode source/intermediate association')
   expected=b'aXYc'
  elif label.startswith('boundary-'):
   if cid!='CMD51-047' or source!=BOLD:raise ValueError('Wrong same-feature boundary case/source')
   tokens=[bytes.fromhex(t['hex']) for t in n.body_tokens(source)];index=case['gap']
   if case['mode']=='typeover' and len(tokens[index])==1:tokens[index]=b'X'
   else:tokens.insert(index,b'X')
   expected=b''.join(tokens)
  elif label.startswith('cursor-normal-'):
   if cid!='CMD51-047' or source!=BOLD:raise ValueError('Wrong normal cursor boundary source/case')
   tokens=[bytes.fromhex(t['hex']) for t in n.body_tokens(source)];index=case['gap']
   for marker in (b'X',b'Y'):
    if case['mode']=='typeover' and index<len(tokens) and len(tokens[index])==1:tokens[index]=marker
    else:tokens.insert(index,marker)
    index+=1
   expected=b''.join(tokens)
  elif label=='ascii-intermediate':
   if cid!='CMD51-046' or source!=b'abc':raise ValueError('Wrong intermediate mode source/case')
   expected=b'aXc'
  elif label.startswith('delete-'):
   if cid!=('CMD51-200' if case['key']=='delete' else 'CMD51-201') or source!=BOLD:raise ValueError('Wrong same-feature Delete/Backspace case')
   expected=b'ABCD'
  elif label.startswith('block-'):
   start,end=case['range'];want='CMD51-204' if end-start==4 else ('CMD51-202' if start==1 else 'CMD51-203')
   if cid!=want or source!=BOLD:raise ValueError('Wrong same-feature blocked boundary case')
   expected=b'AD' if case['answer']=='y' and end-start==4 else BOLD
   screen=(path/(label+'-result')/'screen.txt').read_text();block=('Block on' in screen or '[Block]' in screen)
   if block!=(case['answer']!='y'):raise ValueError('Incorrect actual block retention/clear state')
   if block:
    clean=(path/(label+'-F1-block-cleanup')/'screen.txt').read_text()
    if 'Block on' in clean or '[Block]' in clean or 'Undelete:' in clean:raise ValueError('No separate block cleanup proof')
  elif label.startswith('follow-history-'):
   variant=label.removeprefix('follow-history-')
   if run['recipe']!='history-follow-'+variant:raise ValueError('History followup not an isolated fresh recipe')
   if source!=(BOLD if variant=='repair-restore' else b'abc') or cid!=('CMD51-202' if variant=='repair-restore' else 'CMD51-043'):raise ValueError('Wrong isolated history source/case')
   expected={'consecutive':b'abXc','save-only':b'bXc','consume-direct':b'bccX','repair-restore':bytes.fromhex('41c30cc3c40cc4c30cc3584243c40cc444')}[variant]
  elif label.startswith('history-'):
   if not run['recipe'].startswith('history-'):raise ValueError('History inherited earlier grouped deletions')
   if source!=(BOLD if run['recipe'] in ('history-repair','history-refuse') else b'abc'):raise ValueError('History starting source wrong')
   if cid!=('CMD51-202' if run['recipe'] in ('history-repair','history-refuse') else 'CMD51-043'):raise ValueError('History canonical scope wrong')
   expected={'history-empty':b'abc','history-one':b'abc','history-two':b'bc','history-save-nav':b'bc','history-consume':b'bcc','history-repair':BOLD,'history-refuse':BOLD}[run['recipe']]
  else:raise ValueError('Undeclared local subcase')
  if 'history' in case:
   table=json.loads((HERE/'history-expectations.json').read_text())['cases']
   if case['history']!=table[label]:raise ValueError('Wrong literal history order/Restore outcome association')
   for history in case['history']:
    capture=history['label'];opened=(path/(capture+'-opened')/'screen.txt').read_text()
    if ('Undelete:' in opened)!=history['history_prompt']:raise ValueError('History prompt metadata differs from actual state')
    actual=([opened.splitlines()[0]]+[(path/(capture+'-previous-'+str(i))/'screen.txt').read_text().splitlines()[0] for i in range(len(history['preview_first_lines'])-1)]) if history['history_prompt'] else []
    if actual!=history['preview_first_lines']:raise ValueError('History preview differs from actual raw state')
  if expected is not None and final!=expected:raise ValueError('Native semantic result mismatch '+label)
  native={name:observation(path/name) for name in [case['source'],case['final'],*([case['intermediate']] if 'intermediate' in case else []),*case.get('intermediates',[])]}
  if native[case['source']]['mutation_admission']!='conditional-contract-only':raise ValueError('Fresh original source outside admitted field contract')
  interop=case['interop'];outputs=[interop[k] for k in ('retrieved','edited','after_print')]
  for name in outputs:native[name]=observation(path/name)
  if raw_body(path/interop['retrieved'])!=final:raise ValueError('Retrieve changed declared native body')
  if raw_body(path/interop['edited'])!=final+b'Z' or raw_body(path/interop['after_print'])!=final+b'Z':raise ValueError('Subsequent original edit/print/save body mismatch')
  stream=path/interop['print_stream']
  if not stream.exists() or not stream.read_bytes():raise ValueError('Missing full print stream')
  print_label=Path(interop['print_stream']).stem
  jobs=(path/('settings-print-'+print_label+'-job-status')/'screen.txt').read_text()
  if not all(x in jobs for x in ('Job Number: None','No print jobs','Additional Jobs Not Shown: 0')):raise ValueError('No actual print completion capture')
  row={'id':label,'case_id':cid,'declared':case,'native':native,'print_semantics':print_audit(path/interop['after_print'],stream),'relationships':{'original_edit':relationship_compare(path/case['source'],path/case['final'],'original_edit'),**{key:relationship_compare(path/case['final'],path/interop[key],key) for key in ('retrieved','edited','after_print')}},'print_stream':{'path':str(stream.relative_to(ROOT)),'size':stream.stat().st_size,'sha256':n.sha(stream)}}
  if label.startswith('block-'):row['selection_native_gaps']=block_selection(path/case['source'],path/(label+'-selection'),*case['range'])
  if label.startswith('boundary-') or label.startswith('cursor-normal-'):
   screen=(path/(label+('-after-X' if label.startswith('cursor-normal-') else '-after'))/'screen.txt').read_text()
   if ('Typeover' in screen)!=(case['mode']=='typeover'):raise ValueError('Wrong actual mode state association')
  if case.get('view')=='reveal' or label.startswith('block-') or label.startswith('cursor-normal-'):
   row['outgoing_code_gap']=code_gap(path/case['final'],path/(label+'-final'))
   if label.startswith('cursor-normal-'):
    before_save=code_gap(path/case['final'],path/(label+'-reveal-after-Y'));row['after_Y_before_save_code_gap']=before_save
    if before_save!=row['outgoing_code_gap']:raise ValueError('Mode/save changed final cursor witness')
    if row['outgoing_code_gap']['gap']!=case['gap']+2:raise ValueError('XY witness final native gap mismatch')
    row['after_X_gap']={'gap':case['gap']+1,'basis':'normal X then unique Y without save/pane change/navigation; native XY order plus final exact code-pane highlight. Main X-only native is separately captured.'}
  elif case.get('view')=='normal':
   row['outgoing_code_gap']=plain_gap(path/case['final'],path/(label+'-final')) if label.startswith('delete-') else 'requires explicit post-X Reveal/marker witness; not inferred from Pos'
  cases.append(row)
 return {'run_id':run['run_id'],'recipe':run['recipe'],'result':'observed','manifest_sha256':n.sha(path/'run.json'),'master':run['master_before'],'profile':run['profile_sha256'],'cases':cases}

def build(prefix):
 rows=[validate_run(p.parent) for p in sorted((HERE/'runs').glob(prefix+'*/run.json'))];groups=defaultdict(list)
 for row in rows:
  if row['result']=='observed':groups[row['recipe']].append(row)
 pairs=[]
 for recipe,values in groups.items():
  pair={'recipe':recipe,'run_ids':[r['run_id'] for r in values],'complete':len(values)==2,'case_comparisons':[]}
  if len(values)==2:
   a,b=values
   if a['master']!=b['master'] or a['profile']!=b['profile']:raise ValueError('Fresh pair profile mismatch')
   if [x['id'] for x in a['cases']]!=[x['id'] for x in b['cases']]:raise ValueError('Case ordering mismatch')
   for x,y in zip(a['cases'],b['cases']):
    equal=all(x['native'][k]['sha256']==y['native'][k]['sha256'] for k in x['native']) and x['print_stream']['sha256']==y['print_stream']['sha256']
    if not equal:raise ValueError('Raw native/stream repetition differs '+x['id'])
    pair['case_comparisons'].append({'id':x['id'],'native_and_stream_exact':True})
  pairs.append(pair)
 return {'scope':'original-only provisional analysis; no product writer authority','runs':rows,'pairs':pairs,'all_required_work_complete':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('prefix');p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output)
 if out.exists():raise FileExistsError('Preserve earlier analysis revision')
 result=build(a.prefix);out.write_text(json.dumps(result,indent=2)+'\n');print('Analyzed',len(result['runs']),'sealed attempts,',len(result['pairs']),'groups; completion remains false pending required probes')
