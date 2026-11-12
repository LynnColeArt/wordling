import json,hashlib,subprocess
from pathlib import Path
R=Path.cwd();O=Path('/tmp/wordling-wp51-independent');H=R/'internal/document/evidence/h1-admission-contract';snapshot=json.loads(Path('/tmp/wordling-WP51-before-target-merge.json').read_text());rows={}
for entry in subprocess.check_output(['git','ls-tree','-r','-z','HEAD']).split(b'\0'):
 if not entry:continue
 meta,name=entry.split(b'\t',1);name=name.decode();oid=meta.decode().split()[2]
 if not(name.endswith('.go')or name in ['go.mod','go.sum']or name.startswith('internal/document/evidence/h1-admission-contract/')):continue
 b=(R/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid;rows[name]={'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':oid}
assert rows==snapshot['files']and len(rows)==1156
compiled=json.loads((H/'compiled-source.json').read_text());assert hashlib.sha256((O/'readonly-probe').read_bytes()).hexdigest()==compiled['binary']['sha256']
for pkg in compiled['packages']:
 for e in pkg['files']:
  b=(R/e['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==e['sha256']
source=(H/'probe/main.go').read_text()
for forbidden in ['.New(','.InsertASCII(','.TypeoverASCII(','.Delete(','.Restore(','.NewHistory(','.PreparePublication(','.Publish(']:assert forbidden not in source,forbidden
(O/'source-sync-audit.json').write_text(json.dumps({'source':'5975c5f72775f3b3c07675ecb806c460886c9027','pre_target_source':snapshot['source_commit'],'source_owned_records_exact_Git':len(rows),'readonly_rebuilt_binary_byte_exact':compiled['binary'],'compiled_packages':[x['ImportPath']for x in compiled['packages']],'forbidden_semantic_calls_absent':True},indent=2)+'\n');print('1156 exact before/after source+owned Git records; rebuilt read-only probe binary exact')
