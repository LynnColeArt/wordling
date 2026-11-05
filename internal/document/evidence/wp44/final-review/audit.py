#!/usr/bin/env python3
"""Offline complete WP44 custody audit. No VM or native parser/writer of its own."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=BASE.parents[3]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return sha(json.dumps(value,sort_keys=True,separators=(',',':')).encode())
def require(value,message):
 if not value:raise ValueError(message)
def main():
 require(subprocess.check_output(['git','rev-parse','--show-object-format'],cwd=ROOT,text=True).strip()=='sha1','Git object hash assumption changed')
 tree={}
 for row in subprocess.check_output(['git','ls-tree','-rz','HEAD'],cwd=ROOT).split(b'\0'):
  if row:
   meta,name=row.split(b'\t',1);tree[name.decode()]=meta.split()[2].decode()
 def sealed(path,pin):
  raw=path.read_bytes();require(len(raw)==pin['size'] and sha(raw)==pin['sha256'],f'working seal {path}')
  name=str(path.relative_to(ROOT));oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();require(tree.get(name)==oid,f'actual HEAD Git blob differs {name}')
 seals=json.loads((BASE/'seals.json').read_text())['sources_and_evidence']
 for name,pin in seals.items():sealed(ROOT/name,pin)
 spec=importlib.util.spec_from_file_location('actual_wp44_oracle',BASE/'oracle.py');o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)
 plan=o.check();require(canonical(plan)=='8ced3932f91ee2dff2160e0deb222a9bc7e24e20c1225746d6c58e4ca557f2f0','frozen plan')
 allrows=[];chunkcounts=[];seen=set();cases={};audits=[]
 for i in range(1,8):
  directory=BASE/'runs'/f'wp44-v2-phase{i:02d}';manifest=json.loads((directory/'seals.json').read_text())['files']
  for name,pin in manifest.items():sealed(directory/name,pin)
  pre=json.loads((directory/'prelaunch.json').read_text());run=json.loads((directory/'run.json').read_text());ledger=json.loads((directory/'aggregate-ledger.json').read_text())
  require(canonical(pre['plan'])==canonical(plan)==run['plan_sha256'],'chunk plan divergence')
  require(run['complete'] is True and run['guard_released'] is True and run['oracle_released'] is True and run['master_unchanged'] is True,'chunk incomplete')
  require(run['selected_attempt_ids']==pre['grant']['attempt_ids']==[r['id'] for r in run['results']],'exact granted sequence')
  require(ledger['attempts'][:len(allrows)]==allrows,'aggregate prefix changed')
  chunkledger=ledger['attempts'][len(allrows):];require(len(chunkledger)==len(run['results']),'new rows mismatch')
  for entry,row in zip(chunkledger,run['results']):
   require(entry['id']==row['id'] and entry['result_sha256']==canonical(row) and entry['outcome']==row['outcome']=='complete-observation','ledger checksum does not bind actual row')
   require(row['id'] not in seen,'duplicate attempt');seen.add(row['id'])
   require(row['normal_DOS'] is True and row['guest_stopped'] is True and row['exports_complete'] is True and row['master_after']==plan['master'],'required stop/output/master')
   case=next(x for x in plan['cases'] if x['id']==entry['case']);qual=row['required_output_qualification'];preq=qual['preprint']
   require(preq['admitted'] is True and preq['body_hex']==case['expected_edited_body_hex'] and qual['postprint']['admitted'] is False,'PRE required mutation vs FIN refusal')
   edit=preq['second_real_edit'];require(edit['OriginalExport_exact'] is True and edit['fresh_revision'] is True,'real second edit missing')
   for export in row['exports']:
    p=Path(export['path']);require(p.stat().st_size==export['size'] and sha(p.read_bytes())==export['sha256'],'required raw export changed')
   cases.setdefault(entry['case'],[]).append({'id':entry['id'],'mode':entry['mode'],'repetition':entry['repetition'],'PRE_sha256':preq['sha256'],'PRN_sha256':sha((directory/entry['id']/'C44PRN.PRN').read_bytes()),'second_edit_sha256':edit['sha256']})
  # Replays the actual product consumer and full control checks after release;
  # outputs from its real second edit go to explicit /tmp files, never raw logs.
  audited=o.result(directory/'run.json');require(len(audited['qualified_attempts'])==len(run['results']),'consumer audit count')
  audits.append({'grant':run['grant_id'],'attempts':len(audited['qualified_attempts'])});allrows=ledger['attempts'];chunkcounts.append(len(manifest))
 require(len(allrows)==48 and len(seen)==48 and seen=={x['id'] for x in plan['attempts']},'frozen48 roster not exhausted exactly')
 require(sum(x['mode']=='candidate' for x in allrows)==28 and sum(x['mode']=='control' for x in allrows)==20 and len(cases)==14,'14 whole-native classes,28candidate+20control')
 for case in plan['cases']:
  rows=cases[case['id']];require(sorted(x['repetition'] for x in rows if x['mode']=='candidate')==[1,2],'missing two independent candidates')
  for r in rows:
   twin=next(x for x in rows if x['mode']==r['mode'] and x['repetition']!=r['repetition']);require(r['PRE_sha256']==twin['PRE_sha256'] and r['PRN_sha256']==twin['PRN_sha256'] and r['second_edit_sha256']==twin['second_edit_sha256'],'fresh repetition output divergence')
 private=Path('/home/lynn/projects/wordling/research/cache/reference')
 require((private/'wp44-attempts-v2.json').read_bytes()==(BASE/'runs/wp44-v2-phase07/aggregate-ledger.json').read_bytes(),'private vs public final ledger')
 require(sha((private/'wp44-attempts.json').read_bytes())=='db43f97d494782f3f76a36eca6f5497cd17ecfbacf1317b7c6dd12f2fa06119f','old incomplete ledger changed')
 for name,h in plan['master'].items():require(sha((private/'master'/name).read_bytes())==h,'immutable master changed')
 require(not (ROOT/'runtime/wp44/qmp.sock').exists(),'owned socket remains')
 require(len({x['candidate_sha256'] for x in plan['cases']})==14,'whole native classes not distinct')
 return {'schema':'wordling.wp44.final-custody/v1','plan_sha256':canonical(plan),'executing_commit':'fcf4728749838ebd53dc4db48764909badbff6b1','actual_HEAD_for_Git_blob_proof':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'git_object_method':'git ls-tree HEAD SHA1 object inventory; raw working SHA256+size and SHA1(blob header+raw) match actual listed Git object','source_seals_working_and_actual_Git_blobs':len(seals),'chunk_seals_working_and_actual_Git_blobs':chunkcounts,'executing_source_pins':len(plan['sources']),'current_complete':48,'historical_incomplete_unqualified':1,'cumulative_spent':49,'candidate_observations':28,'new_original_controls':20,'whole_native_classes':14,'all48_exact_frozen_attempts_and_independent_twins':True,'product_reopen_and_real_second_edit_and_full_PRN_replayed':audits,'classes':cases,'old_failed_private_disk_read_or_extracted':False,'no_more_original_runs_or_retries_authorized':True,'current_global_oracle_free_claim':False,'oracle_release':'all7 whole CLIs exited0 and each immediate release check; root subsequently granted WP29; no foreign runtime touched','full_M1_accepted':False,'physical_resources_qualified':False}
if __name__=='__main__':print(json.dumps(main(),indent=2))
