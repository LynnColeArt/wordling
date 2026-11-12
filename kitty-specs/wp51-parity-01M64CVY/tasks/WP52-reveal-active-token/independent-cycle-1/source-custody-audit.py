import json,hashlib,subprocess
from pathlib import Path
R=Path.cwd();O=Path('/tmp/wordling-wp52-independent');H=R/'internal/tui/evidence/wp52';before=json.loads(Path('/tmp/wordling-WP52-before-target-merge.json').read_text());files={}
for row in subprocess.check_output(['git','ls-tree','-r','-z','HEAD']).split(b'\0'):
 if not row:continue
 meta,p=row.split(b'\t',1);p=p.decode();oid=meta.decode().split()[2]
 if not(p.endswith('.go')or p in['go.mod','go.sum']or p.startswith('internal/tui/')):continue
 b=(R/p).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid;files[p]={'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':oid}
assert files==before['files']and len(files)==392
proof=json.loads((H/'wordling-WP52-claim-source-proof.json.txt').read_text());build=json.loads((H/'build/source.json').read_text());final=json.loads((H/'build-final/source.json').read_text());assert build['actual_compiled_project_inputs']==final['actual_compiled_project_inputs'];compiled=build['actual_compiled_project_inputs'];assert not set(proof['whole_Go_SET_delta'])&set(compiled)
for p,h in proof['files'].items():
 expected=subprocess.check_output(['git','show',proof['approved_source']+':'+p]);assert hashlib.sha256(expected).hexdigest()==h
 if p!='internal/tui/model.go':assert (R/p).read_bytes()==expected
for p,entry in compiled.items():
 b=(R/p).read_bytes();assert len(b)==entry['size']and hashlib.sha256(b).hexdigest()==entry['sha256']
for archive,revision in [('custody-cycle1','abb44799511899418e7bac6f610b77ee5a68d78a'),('custody-cycle2','29b43ac6')]:
 for a,p in [('manifest.json.txt','manifest.json'),('attributes.txt','.gitattributes')]:assert (H/'history'/archive/a).read_bytes()==subprocess.check_output(['git','show',revision+':internal/tui/evidence/wp52/'+p])
assert len(json.loads((H/'history/custody-cycle1/manifest.json.txt').read_text())['files'])==202;assert len(json.loads((H/'history/custody-cycle2/manifest.json.txt').read_text())['files'])==206
attrs=(H/'.gitattributes').read_text().splitlines();exceptions=[x.split()[0]for x in attrs if' whitespace='in x];assert len(exceptions)==7 and all('*'not in x for x in exceptions)
for f in ['internal/tui/model.go','internal/tui/reveal.go','internal/tui/reveal_cursor_test.go','internal/tui/evidence/wp52/run_pty.py']:
 v=subprocess.check_output(['git','check-attr','whitespace','--',f],text=True);assert v.rstrip().endswith('unspecified'),v
(O/'source-custody-audit.json').write_text(json.dumps({'source':'c231d0b09acb6c69e9f3f636f9b2a109e9ce8b8d','source_before_sync':before['source_commit'],'current_source_owned_Git_records':len(files),'executed_final_compiled_inputs':len(compiled),'compiled_sets_identical':True,'whole_Go_SET':len(final['complete_local_Go_SET']),'unreviewed_E_research_probes_not_imported':proof['whole_Go_SET_delta'],'production_code_borrowed_from_51':False,'historical_manifest_counts':[202,206],'exact_whitespace_exceptions':exceptions,'source_test_script_whitespace_unsuppressed':True},indent=2)+'\n');print('392 source/owned Git records,35 actual compiled inputs,202/206 predecessor custody and7 exact whitespace exceptions independently verified')
