#!/usr/bin/env python3
"""Offline exact run/source/native audit. Never configures or starts a guest."""
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
POST=Path(__file__).resolve().parent;HERE=POST.parent;ROOT=HERE.parents[4]
spec=importlib.util.spec_from_file_location('wp48_completed_run_audit',HERE/'adapter.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
def load(path):return json.loads(path.read_text())
def digest(raw):return {'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def checked_file(name,row,git=False):
 raw=(ROOT/name).read_bytes();assert digest(raw)=={k:row[k]for k in ['size','sha256']},name
 blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 if 'git_blob'in row:assert blob==row['git_blob'],('blob hash',name)
 if git:assert subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT)==raw,('committed bytes',name)
 return raw
frozen=load(HERE/'preflight.json');p=frozen['plan'];assert a.canonical(p)==frozen['plan_sha256']=='999598eb6453ba50b7815858a475411692eababa486134102d74315640075572'
# Preserve all155 prelaunch records; do not rewrite their original seals.
for name,pin in load(HERE/'seals.json')['files'].items():checked_file(name,pin,'--git'in sys.argv)
a.historical_proposal()
for pin in p['sources']:
 raw=checked_file(pin['path'],pin,'--git'in sys.argv);assert subprocess.check_output(['git','show','308145c77ce4cc0335c3b6b52942e0b7e44340ff:'+pin['path']],cwd=ROOT)==raw,('executing source',pin['path'])
manifest=load(POST/'raw-manifest.json');assert manifest['raw_files']==len(manifest['files'])==1781
for name,pin in manifest['files'].items():checked_file(name,pin,'--git'in sys.argv)
run=ROOT/p['public_output'];report=load(run/'run.json');ledger=load(run/'aggregate-ledger.json');grant=load(run/'grant.json');assert report['complete']is True and report['oracle_released']is True and report['charged_attempts_including_failures']==report['positive_owned_start_identities']==4;assert [x['id']for x in report['results']]==a.ids();assert ledger==load(POST/'private-ledger-snapshot.json');a.ledger_ok(p,ledger);a.grant(report['actual_argv'][1:],p,grant)
owner=load(POST/'private-owner-snapshot.json');assert owner['state']=='complete'and owner['guest_attempts']==4 and owner['plan_sha256']==a.canonical(p)
assert grant['plan_sha256']==a.canonical(p)and report['grant']==grant;assert report['actual_argv']==grant['argv'];assert (POST/'whole-cli.stderr').read_bytes()==b''
controls=a.control_rows(p,ledger['attempts'][:2]);native=[]
for leaf,row,entry in zip(p['attempts'],report['results'],ledger['attempts']):
 directory=run/leaf['id'];actual=load(directory/'result.json');assert actual==row;assert a.canonical(row)==entry['result_sha256']and a.sha(directory/'result.json')==entry['result_file_sha256'];assert row['outcome']=='complete-observation'and row['normal_DOS']and row['guest_stopped']and row['exports_complete']and row['physical_guard_released'];a.custody_record(p,leaf,row);a.old.normal_dos(directory)
 pre=load(directory/'prelaunch.json');assert pre['plan']==p and pre['plan_sha256']==a.canonical(p)and pre['leaf']==leaf and pre['actual_argv']==grant['argv']and pre['recorded_before_fresh_start']is True
 for pin in p['sources']:
  archive=directory/'executing-source'/(pin['path']+'.txt');assert archive.read_bytes()==subprocess.check_output(['git','show','308145c77ce4cc0335c3b6b52942e0b7e44340ff:'+pin['path']],cwd=ROOT),('per-run executing archive',leaf['id'],pin['path'])
 for state,name,pos,reveal in [('input-closed-normal','C48SEED'if leaf['mode']=='control'else'C48INPUT','1',False),('input-prospective-nine-Reveal','C48SEED'if leaf['mode']=='control'else'C48INPUT','1',True),('before-print-closed-main','C48PRE','1.9',False),('print-C48PRN-submitted','C48PRE','1.9',False)]:
  a.strict_frame((directory/state/'screen.txt').read_text(),name,pos=pos,reveal=reveal);cursor=load(directory/state/'cursor.json');assert cursor['row']==0 and cursor['column']==(0 if pos=='1'else 9)
 fresh=a.qualify(directory,leaf,emit_Q=False)
 for key in ['full72_graph_byte_relation','whole_PRN_sha256','whole_PRN_size','control_seed_only_indexed_mustformat_difference']:assert row['qualification'][key]==fresh[key]
 for key,value in fresh['PRE'].items():assert row['qualification']['PRE'][key]==value
 assert row['qualification']['FIN']==fresh['FIN'];assert len(fresh['full72_graph_byte_relation']['PRE_all72'])==len(fresh['full72_graph_byte_relation']['FIN_all72'])==72
 q=a.old.product('-verify',directory/'second-Go-edit.WP5','-require-preprint');assert q['body_hex']==p['body_hex']+'51'and q['sha256']==row['qualification']['PRE']['second_real_edit']['sha256']
 for export in row['exports']:a.old.guard.checked_export_bytes(export['path'],export['size'],export['sha256'])
 if leaf['mode']=='candidate':
  for name in ['input.WP5','input-after.WP5']:assert a.sha(directory/name)==a.CANDIDATE_SHA and(directory/name).stat().st_size==333
  control=controls[leaf['repetition']-1][0]
  for name in ['C48PRE.WP5','C48FIN.WP5','C48PRN.PRN']:assert(directory/name).read_bytes()==(control/name).read_bytes()
 release=load(directory/'stopped-release.json');assert release['guest_stopped']and release['socket_absent']and release['physical_guard_released']and release['before_offline_qualification']
 native.append({'id':leaf['id'],'PRE_sha256':a.sha(directory/'C48PRE.WP5'),'FIN_sha256':a.sha(directory/'C48FIN.WP5'),'PRN_sha256':a.sha(directory/'C48PRN.PRN'),'PRN_bytes':153,'input_class':a.CANDIDATE_SHA if leaf['mode']=='candidate'else'original-generated SEED; indexed08/00 relationship','original_edit_after_retrieve':False})
if (POST/'seals.json').exists():
 for name,pin in load(POST/'seals.json')['files'].items():checked_file(name,pin,'--git'in sys.argv)
print(json.dumps({'actual_original_attempts':4,'qualified_controls':2,'qualified_exact_UI333_candidates':2,'failures':0,'raw_files_exact':1781,'per_run_executing_source_archives_exact':384,'prelaunch_records_preserved':155,'source_pins_exact':96,'Git_blobs_checked':'--git'in sys.argv,'normal_DOS_owned_stop_exports_master_release':True,'PRE_FIN_fullPRN_same_rep_exact':True,'all72_fields_and_entire_graph_checked':True,'original_subsequent_edit_of_UI333':False,'full_M1_accepted':False,'native':native},indent=2))
