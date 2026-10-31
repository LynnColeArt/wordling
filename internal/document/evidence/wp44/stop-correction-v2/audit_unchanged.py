"""Read-only Git/source/accounting audit; never opens failed private disk."""
from pathlib import Path
import hashlib
import json
import subprocess
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'internal/document/evidence/wp44';HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((BASE/'history/pre-stop-poll-bea27c98/seals.json').read_text());changed=[]
for name,row in old['sources_and_evidence'].items():
 blob=subprocess.check_output(['git','show','78acb24dec749dfa4d96057198e0026397ff3675:'+name],cwd=ROOT)
 assert hashlib.sha256(blob).hexdigest()==row['sha256'],name
 if sha(ROOT/name)!=row['sha256']:changed.append(name)
allowed={'internal/document/evidence/wp44/oracle.py','internal/document/evidence/wp44/test_oracle.py','internal/document/evidence/wp44/README.md'}
assert set(changed)<=allowed,changed
failed=BASE/'runs/wp44-phase01';raw=json.loads((failed/'failure-seals.json').read_text())
for name,row in raw['files'].items():assert sha(failed/name)==row['sha256'],name
pre=json.loads((BASE/'history/pre-stop-poll-bea27c98/preflight.json').read_text());new=json.loads((HERE/'preflight.json').read_text());assert pre['cases']==new['cases']
for case in pre['cases']:
 for key in ['candidate','source','provenance']:assert sha(ROOT/case[key])==case[key+'_sha256']
assert pre['producer_execution']==new['producer_execution']
assert not subprocess.check_output(['git','diff','bea27c98e57fee5c341d1b74d4c8877bdcc2d42d','--','internal/document/*.go','internal/document/evidence/wp44/producer','internal/document/evidence/wp44/bin','internal/document/evidence/wp44/candidates'],cwd=ROOT)
old_ledger=Path(new['transition']['predecessor']['private_ledger']['path']);assert sha(old_ledger)=='db43f97d494782f3f76a36eca6f5497cd17ecfbacf1317b7c6dd12f2fa06119f'
assert not Path(new['transition']['successor_ledger_path']).exists()
old_ids={a['id']for a in pre['attempts']};new_ids={a['id']for a in new['attempts']};assert len(new_ids)==48 and not old_ids.intersection(new_ids)
old_works={a['private_work']for a in pre['attempts']};new_works={a['private_work']for a in new['attempts']};assert not old_works.intersection(new_works)and all(not Path(w).exists()for w in new_works)
assert new['historical_spent']==1 and new['new_required_positive_leaves']==48 and new['cumulative_maximum_attempts_including_failures']==49
result={'original485_Git_seals_exact':len(old['sources_and_evidence']),'old_working_deltas_permitted':changed,'all341_failure_files_unchanged':len(raw['files']),'all_cases_and_native_inputs_and_producer_unchanged':True,'Go_fuzz_PTY_budgets_rerun':False,'failed_private_disk_opened_or_extracted':False,'old_private_ledger_unchanged':sha(old_ledger),'successor_private_ledger_not_created':True,'all48_new_IDs_and_private_workpaths_fresh_and_disjoint':True,'historical_spent':1,'new_positive_leaves':48,'cumulative_cap':49,'new_VM_guests':0}
(HERE/'unchanged-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
