#!/usr/bin/env python3
"""Verify this offline proposal and source/asset seals; never invokes run/VM."""
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
spec=importlib.util.spec_from_file_location('wp48_z_offline_audit',HERE/'adapter.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
frozen=json.loads((HERE/'preflight.json').read_text());assert frozen['VM_launched']is False and frozen['root_grant_required']is True;assert frozen['plan_sha256']==a.canonical(frozen['plan']);a.verify_plan(frozen['plan'])
for name,row in json.loads((HERE/'seals.json').read_text())['files'].items():
 raw=(ROOT/name).read_bytes();assert len(raw)==row['size']and hashlib.sha256(raw).hexdigest()==row['sha256'],name
 if '--git'in sys.argv:assert subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT)==raw,('Gitblob',name)
for pin in frozen['plan']['sources']:
 raw=(ROOT/pin['path']).read_bytes();assert len(raw)==pin['size']and hashlib.sha256(raw).hexdigest()==pin['sha256'],pin['path']
 if '--git'in sys.argv:assert subprocess.check_output(['git','show','HEAD:'+pin['path']],cwd=ROOT)==raw,('source Gitblob',pin['path'])
request=json.loads((HERE/'grant-request.json').read_text());assert request['authorized']is False and request['plan_sha256']==frozen['plan_sha256'];assert request['attempt_ids']==a.ids()and request['maximum_attempts_including_failures']==4
if '--prelaunch'in sys.argv:
 p=frozen['plan'];paths=[Path(p['ledger']),Path(p['socket']),Path(p['socket']).parent/'qemu.pid',ROOT/p['public_output'],*[Path(x['private_work'])for x in p['attempts']]];assert not any(x.exists()for x in paths),'prelaunch path collision'
print(json.dumps({'offline_proposal_exact':True,'plan_sha256':frozen['plan_sha256'],'source_pins':len(frozen['plan']['sources']),'owned_files':len(json.loads((HERE/'seals.json').read_text())['files']),'Gitblobs_checked':'--git'in sys.argv,'original_attempts_executed':0,'proposed_cap_including_failures':4,'root_grant':False,'old_product_and_raw_evidence_preserved':True}))
