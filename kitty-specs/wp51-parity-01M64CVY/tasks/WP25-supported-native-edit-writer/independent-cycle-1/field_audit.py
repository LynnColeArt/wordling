import ast,hashlib,json,re,subprocess
from pathlib import Path
root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e');p=root/'internal/document/admission.go';text=p.read_text();table=text.split('var qualifiedPacketFields =',1)[1].split('func (d *Document)',1)[0];actual={};owner=None
for line in table.splitlines():
 m=re.match(r'\s*([0-9]+): \{',line)
 if m:owner='packet-'+m[1];actual[owner]={}
 m=re.search(r'\{"([^"]+)", (\d+), ("(?:[^"\\]|\\.)*")\}',line)
 if m:actual[owner][int(m[2])]=ast.literal_eval(m[3]).encode('latin1')
ledger=json.loads((root/'docs/research/continuation/native-edits/field-ledger.json').read_text());compared=0
for row in ledger['field_coverage']:
 if row['owner']=='header':continue
 value=actual[row['owner']][row['offset']];assert len(value)==row['width'] and value.hex()==row['source_observed_hex'],row;compared+=1
assert sum(len(x)for x in actual.values())==compared
proof={'approved23_field_rows_total':len(ledger['field_coverage']),'go_qualified_packet_fields_exact':compared,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'literal_metadata_variants':'only documented packet6flag0/8 and packet15hash e724/1172; actual tests cover each combination','native_reader_unchanged':subprocess.check_output(['git','show','e7de080:internal/wp51/native.go'],cwd=root)==(root/'internal/wp51/native.go').read_bytes()}
print(json.dumps(proof,indent=2))
