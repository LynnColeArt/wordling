#!/usr/bin/env python3
"""Finite WP23 source/state/native/stream selection; no VM or product writes."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_edits as n
from analyze import envelope,validate_run,raw_body,observation,BOLD
from audit_sources import audit as source_audit
from relationships import compare as relationships
from print_audit import audit as print_audit
from codepane_cursor import gap
from classify_reader import classify
import candidate_mode

def chain(path,item):
 expected=raw_body(path/item['input']);native={item['input']:observation(path/item['input'])};relations={}
 for key in ('retrieved','edited','after_print'):
  f=path/item[key];wanted=expected if key=='retrieved' else expected+b'Z'
  if raw_body(f)!=wanted:raise ValueError('Shared interoperability native body mismatch')
  native[item[key]]=observation(f);relations[key]=relationships(path/item['input'],f,key)
 stream=path/item['print_stream'];jobs=(path/('settings-print-'+stream.stem+'-job-status/screen.txt')).read_text()
 if not all(text in jobs for text in ('Job Number: None','No print jobs','Additional Jobs Not Shown: 0')):raise ValueError('Shared print incomplete')
 return {'native':native,'relationships':relations,'print_stream':n.record(stream,ROOT),'print_semantics':print_audit(path/item['after_print'],stream)}

def normal_questions(path,aliases):
 path=Path(path);r=envelope(path)
 if r['result']!='observed' or r['recipe']!='normal-questions':raise ValueError('Normal question recipe incomplete/wrong')
 required=[(g,k,a) for g,k in ((1,'delete'),(4,'delete'),(2,'backspace'),(5,'backspace')) for a in ('n','f1','esc')]
 if len(r['cases'])!=len(required):raise ValueError('Missing normal code-question context')
 shared=chain(path,r['cases'][0]['source_interop']);cases=[]
 shared_input=path/r['cases'][0]['source_interop']['input'];aliases.setdefault(n.sha(shared_input),[]).append({'path':shared_input,'manifest':path/'run.json','case_id':'CMD51-200','role':'exact unchanged source input chain after all question captures','chain':shared})
 for c,(g,k,a) in zip(r['cases'],required):
  label=f'normal-question-{k}-g{g}-{a}'
  if (c['id'],c['gap'],c['key'],c['answer'],c['case_id'])!=(label,g,k,a,'CMD51-200' if k=='delete' else 'CMD51-201'):raise ValueError('Wrong normal question semantic association')
  if raw_body(path/c['source'])!=BOLD or raw_body(path/c['final'])!=BOLD:raise ValueError('Question answer changed native body')
  n.inspect((path/c['source']).read_bytes(),True);n.inspect((path/c['final']).read_bytes(),True)
  question=(path/(label+'-question/screen.txt')).read_text();want='Delete '+('[BOLD]' if g in (1,2) else '[bold]')+'? No (Yes)'
  if question.splitlines()[-1]!=want or c['question']!=want:raise ValueError('Wrong actual normal question/default')
  result=(path/(label+'-result/screen.txt')).read_text();confirmed=(path/(label+'-result-confirmed/screen.txt')).read_text()
  if result!=confirmed or any(text in result for text in ('? No (Yes)','Block on','[Block]','Undelete:')):raise ValueError('Question answer did not return to observed editing context')
  if c['question_persisted'] or c['block_persisted'] or c['cleanup']:raise ValueError('False normal question cleanup/persistence metadata')
  outgoing=gap(path/c['final'],path/(label+'-cursor'));saved=gap(path/c['final'],path/(label+'-final'))
  if outgoing!=saved or outgoing['gap']!=g+(1 if k=='delete' else -1):raise ValueError('Wrong directional code-question return gap')
  choices=aliases.get(n.sha(path/c['final']),[]);alias=next((x for x in choices if x['path'].read_bytes()==(path/c['final']).read_bytes()),None)
  if alias is None:raise ValueError('No exact whole-native interoperability alias')
  cases.append({'id':label,'case_id':c['case_id'],'declared':c,'native':{name:observation(path/name) for name in (c['source'],c['final'])},'original_edit_relationship':relationships(path/c['source'],path/c['final'],'original_edit'),'outgoing_code_gap':outgoing,'question_default':want,'question_persisted':False,'block_persisted':False,'interop_alias':{'native':n.record(alias['path'],ROOT),'manifest':n.record(alias['manifest'],ROOT),'case_id':alias['case_id'],'role':alias['role'],'whole_file_bytes_equal':True}})
 return {'run_id':r['run_id'],'recipe':r['recipe'],'manifest_sha256':n.sha(path/'run.json'),'master':r['master_before'],'profile':r['profile_sha256'],'result':'observed','cases':cases,'shared_source_interop':shared}

def candidate(path):
 r=envelope(path)
 if r['result']!='observed' or r['recipe']!='candidate':raise ValueError('Candidate original run incomplete')
 old=json.loads((path/'comparison.json').read_text());now=candidate_mode.compare(path,r)
 if not old['accepted'] or not now['accepted']:raise ValueError('Candidate CLI/comparison did not accept actual interoperability')
 c=r['cases'][0];native={c[k]:observation(path/c[k]) for k in ('source','retrieved','edited','after_print')}
 return {'run_id':r['run_id'],'recipe':'candidate','result':'observed','master':r['master_before'],'profile':r['profile_sha256'],'manifest_sha256':n.sha(path/'run.json'),'comparison_sha256':n.sha(path/'comparison.json'),'cases':[{'id':'candidate-interop','canonical_leads':c['canonical_leads'],'native':native,'print_stream':n.record(path/c['print_stream'],ROOT),'print_semantics':print_audit(path/c['after_print'],path/c['print_stream']),'actual_comparison':now}],'smoke_producer':'original-authored surrogate; no Go serializer tested'}

def signature(case):
 return {'native':{k:v['sha256'] for k,v in case['native'].items()},'print_stream':case.get('print_stream',{}).get('sha256'),'outgoing_code_gap':case.get('outgoing_code_gap')}

def verify():
 sources=source_audit();plan=json.loads((HERE/'selection-plan.json').read_text());runs=[];aliases={};pairs=[]
 for recipe,prefix in plan['required_pairs'].items():
  if recipe in ('normal-questions','candidate'):continue
  for rep in (1,2):
   path=HERE/'runs'/(prefix+'-r'+str(rep));row=validate_run(path)
   if row['result']!='observed' or row['recipe']!=recipe:raise ValueError('Required original recipe incomplete')
   runs.append(row)
   for case in row['cases']:
    item=case['declared']['interop'];f=path/item['input'];aliases.setdefault(n.sha(f),[]).append({'path':f,'manifest':path/'run.json','case_id':case['case_id'],'role':'exact native input with validated original Retrieve/edit/print/Save chain','chain':item})
 for recipe in ('normal-questions','candidate'):
  prefix=plan['required_pairs'][recipe]
  for rep in (1,2):
   path=HERE/'runs'/(prefix+'-r'+str(rep));runs.append(normal_questions(path,aliases) if recipe=='normal-questions' else candidate(path))
 for recipe,prefix in plan['required_pairs'].items():
  values=[r for r in runs if r['recipe']==recipe]
  if len(values)!=2 or values[0]['master']!=values[1]['master'] or values[0]['profile']!=values[1]['profile']:raise ValueError('Required independent fresh pair identity mismatch')
  if [c['id'] for c in values[0]['cases']]!=[c['id'] for c in values[1]['cases']]:raise ValueError('Pair case order mismatch')
  for a,b in zip(values[0]['cases'],values[1]['cases']):
   if signature(a)!=signature(b):raise ValueError('Native/print/cursor repetition mismatch '+a['id'])
  pairs.append({'recipe':recipe,'run_ids':[r['run_id'] for r in values],'manifests':[r['manifest_sha256'] for r in values],'local_subcases':[c['id'] for c in values[0]['cases']],'native_print_cursor_exact':True})
 accounted={r['run_id'] for r in runs}|set(plan['excluded']);actual={p.parent.name for p in (HERE/'runs').glob('*/run.json')}
 if actual!=accounted:raise ValueError('Unaccounted original attempts '+str(actual^accounted))
 excluded=[]
 for rid,reason in plan['excluded'].items():
  r=envelope(HERE/'runs'/rid);excluded.append({'run_id':rid,'result':r['result'],'reason':reason,'manifest_sha256':n.sha(HERE/'runs'/rid/'run.json')})
 reused=json.loads((HERE/'reused-evidence.json').read_text())
 for row in reused:
  artifacts=[row['manifest'],row['runner'],*row['native'],*row['screens'],*([row['raw_vga']] if 'raw_vga' in row else [])]
  for a in artifacts:
   path=ROOT/a['path']
   if path.stat().st_size!=a['size'] or n.sha(path)!=a['sha256']:raise ValueError('Approved reused evidence changed')
 files=sorted((HERE/'runs').glob('*/*.WP5'))+sorted((HERE/'runs').glob('*/inputs/*.WP5'))+sorted((HERE/'diagnostics').glob('*/*.WP5'))
 reader=classify(files)
 if not all(f['accepted'] and f.get('exact_no_edit_export') for f in reader['files']):raise ValueError('Actual Go reader cannot reopen required original export')
 return {'scope':'WP23 finite original evidence/conditional mutation contract only','required_local_witnesses_complete':True,'independent_WP23_contract_approval_required':True,'wordling_tested':False,'production_serializer_implemented':False,'source_audit':sources,'pairs':pairs,'runs':runs,'excluded_attempts':excluded,'reused_approved_evidence':reused,'actual_reader':reader,'counts':{'fresh_accepted_runs':len(runs),'fresh_pairs':len(pairs),'local_case_instances':sum(len(r['cases']) for r in runs),'all_native_exports_classified':len(reader['files'])},'remaining_scope':plan['unselected']+['M1 all38 requirements/91 groups remain open beyond these partial witnesses','higher than two sequential pairs remains full M1 obligation; initial qualification bound only']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output)
 if out.exists():raise FileExistsError('Preserve earlier verification revision')
 result=verify();out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['counts']))
