"""Reuse actual approved51 PUBLIC read-only binary; no native decoder or permission mint."""
from pathlib import Path
import json
import approved,oracle
from boundaries import read,process,parse,require
BASE='internal/document/evidence/h1-admission-contract/';INPUT='docs/research/continuation/native-genesis/runs/wp43-genesis-01-ascii-first-retrieve/r1/G43TEXT.WP5'
def closure():
 c=json.loads(read(approved.ROOT/(BASE+'compiled-source.json')));require(c['exit']==0 and c['build_vcs_stamp'].startswith('disabled explicitly'),'ProbeCompilation','actual prior source-bound compile witness')
 for package in c['packages']:
  directory=Path(package['Dir']);live=sorted(p.name for p in directory.glob('*.go')if not p.name.endswith('_test.go'));require(live==sorted(package['GoFiles']),'ProbeSourceSET','actual compile source set unchanged')
  for f in package['files']:require(oracle.sha(read(approved.ROOT/f['path']))==f['sha256'],'ProbeCompiledSourceDrift',f['path'])
 pin=c['binary'];return c

def inspect(path):
 c=closure();binary=approved.ROOT/(BASE+'bin/readonly-probe');raw=read(binary,4<<20);pin=c['binary'];want=pin.get('sha256');require(oracle.sha(raw)==want,'ProbeBinaryDrift','actual compiled read-only probe binary')
 p=Path(path);data=read(p,65536);out,_=process([str(binary),str(p)],approved.ROOT,timeout=30,stdout_limit=1<<20);rows=parse(out);require(type(rows)is list and len(rows)==1 and rows[0]['Bytes']==len(data)and rows[0]['SHA256']==oracle.sha(data)and rows[0]['Parsed']and rows[0]['ExportExact']and rows[0]['OriginalExact'],'NativeProbeResult','Parse/Inspect/Export/OriginalExport byte ownership');return rows[0]
def initial():
 path=approved.ROOT/INPUT;raw=read(path,65536);require(len(raw)==332 and oracle.sha(raw)==oracle.INPUT_SHA,'InitialInputIdentity','exact original43 native bytes');other=approved.ROOT/INPUT.replace('/r1/','/r2/');require(raw==read(other,65536),'InitialInputRepetition','two fresh original43 exact');r=inspect(path);require(r['BodyHex']=='4734334153434949','InitialBody','actual public body span');return dict(input=r,all72=fields72(r),compiled_closure=closure(),native_mutations=0,admission_permission_granted=False)

def fields72(row):
 # Actual approved51 public read-only field projection, not a copied decoder/predicate.
 import importlib.util
 path=approved.ROOT/(BASE+'stage1.py');raw=read(path,65536);old,_=process(['git','show',approved.SOURCE51+':'+BASE+'stage1.py'],approved.ROOT,stdout_limit=65536);require(raw==old,'FieldSourceDrift','actual51 field projection')
 spec=importlib.util.spec_from_file_location('wp55_approved51_readonly_fields',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);result=module.facts(row);require(len(result['all72_fields'])==72,'FieldRoster','actual72 explicit field projections');return result
