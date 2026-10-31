#!/usr/bin/env python3
"""Owned WP48 custody/closure audit, not a conformance-status updater."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def digest(raw):return {'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def load(p):return json.loads(p.read_text())
manifest=load(HERE/'manifest.json')
for name,row in manifest['files'].items():
 raw=(ROOT/name).read_bytes();assert digest(raw)==row,name
 if '--git'in sys.argv:assert subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT)==raw,('Git blob',name)
build=load(HERE/'build-final/source.json')
actual={str(p.relative_to(ROOT)):digest(p.read_bytes())for prefix in ['internal','cmd']for p in (ROOT/prefix).rglob('*.go')}
assert actual==build['complete_local_Go_SET'],'Go source SET/SHA changed'
for name,row in build['actual_compiled_project_inputs'].items():assert digest((ROOT/name).read_bytes())==row,name
assert digest((HERE/'build-final/wordling.bin').read_bytes())==build['binary']
for name,row in load(HERE/'native-reference-pins.json').items():
 raw=(ROOT/name).read_bytes();assert digest(raw)=={k:row[k]for k in ['size','sha256']};assert subprocess.check_output(['git','show',row['approved_source']+':'+name],cwd=ROOT)==raw
pre=load(HERE/'prerequisite-source-preflight.json')
for name,sha in pre['actual_document_editor_source_hashes'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
registry=load(ROOT/'docs/research/command-scenarios.json');leads=load(HERE/'case-leads.json')
for row in leads['leads']:
 entry=next(x for x in registry if x['id']==row['id']);assert all(entry[k]==v for k,v in row.items()),('wrong semantic case',row['id'])
print(json.dumps({'owned_files_exact':len(manifest['files']),'Git_blobs_checked':'--git'in sys.argv,'project_compiled_inputs_exact':len(build['actual_compiled_project_inputs']),'complete_local_Go_files':len(actual),'approved_dependencies_exact':len(pre['actual_document_editor_source_hashes']),'native_reference_pins':4,'VM_runs':0,'canonical_status_mutations':0}))
