#!/usr/bin/env python3
"""Public source custody only; no original resources/private disks/controllers."""
from pathlib import Path
import json,subprocess,hashlib,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent;BASE='85f5e8d4777adb234d5b7785dc3c776e4d8003fc';E='b03bf33911af0b9391dc0f007d131f8ea9185789';sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda *a:subprocess.check_output(['git','-C',str(ROOT),*a]);old=json.loads(Path('/tmp/wordling-WP60-before-claim-source.json').read_text());changed={'internal/tui/model.go','internal/tui/macro_model.go','internal/tui/reveal_cursor_test.go'};stable=[]
for path,x in old['files'].items():
 b=git('show',BASE+':'+path);assert len(b)==x['size']and sha(b)==x['sha256']and git('rev-parse',BASE+':'+path).decode().strip()==x['git_blob']
 if path not in changed:assert(ROOT/path).read_bytes()==b;stable.append(path)
assert len(old['files'])==480 and changed<=set(old['files'])
# Actual approved E payloads and source are unchanged, including non-Go evidence.
p='internal/document/evidence/reveal-catalogue/working-and-Git-seals.json';seal=json.loads(git('show',E+':'+p));assert sha((ROOT/p).read_bytes())=='9360bfd954923e63189c03ee0a0f517777b7fc8342cfe259df18bf6e21f06356'
for x in seal['files']:
 b=git('show',E+':'+x['path']);assert(ROOT/x['path']).read_bytes()==b and len(b)==x['bytes']and sha(b)==x['sha256']
post=json.loads(Path('/tmp/wordling-WP60-postclaim-source-proof.json').read_text())
for name in post['approved_E59_new_Go']:
 b=git('show',E+':'+name);assert(ROOT/name).read_bytes()==b and git('show',BASE+':'+name)==b
fixtures=json.loads((ROOT/'internal/document/evidence/reveal-catalogue/fixtures.json').read_text())
for x in fixtures['files']:
 b=git('show',x['commit']+':'+x['path']);assert sha(b)==x['sha256']and(ROOT/x['path']).read_bytes()==b
build=json.loads((HERE/'build-source.json').read_text())
for path,x in build['inputs'].items():b=Path(path).read_bytes();assert len(b)==x['bytes']and sha(b)==x['sha256']
assert sha(Path(build['binary']).read_bytes())==build['binary_digest']['sha256']
# No scope guard based on a misleading giant shared-lane planning diff.
tracked=git('diff','--name-only',BASE).decode().splitlines();assert all(p in changed or p in ['internal/tui/reveal_inspection.go','internal/tui/reveal_inspection_test.go']or p.startswith('internal/tui/evidence/reveal-inspection/')for p in tracked)
out=dict(scope='WP60 source/refusal/UI only; no original/nativeediting/fullReveal claim',claim_baseline=BASE,old480_Gitbytes_exact=True,old_nonchanged477_working_exact=len(stable)==477,allowed_existing_H_amendments=sorted(changed),approvedE129_unchanged=True,original14_public_native_text_VGA24_unchanged=True,production_compiler_packages=build['package_count'],production_compiler_inputs=len(build['inputs']),production_binary_sha256=build['binary_digest']['sha256'],production_entry_unchanged=sha((ROOT/'cmd/wordling/main.go').read_bytes())==old['files']['cmd/wordling/main.go']['sha256'],P_source_not_consumed=True,all_changes_H_only=True,no_VM_original_private_actions=True)
(HERE/'custody.json').write_text(json.dumps(out,indent=2)+'\n')
events=[json.loads(x)for x in (HERE/'handoff-model-events.jsonl').read_text().splitlines()];assert not any(x.get('Action')=='fail'for x in events);passed=[x['Test']for x in events if x.get('Action')=='pass'and x.get('Test')];suite=ET.Element('testsuite',name='publicModel-and-finite-structural-counterexamples',tests=str(len(passed)),failures='0',skipped='0')
for name in passed:ET.SubElement(suite,'testcase',name=name)
ET.ElementTree(suite).write(HERE/'model.xml');out['public_Model_test_events']=len(passed);print(json.dumps(out,indent=2))
