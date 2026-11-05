#!/usr/bin/env python3
"""Strict approved40 import audit with explicitly bijective checkout relocation."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'docs/research/continuation/code-pair-history'))
# This module itself is named audit.py: import the approved file explicitly.
import importlib.util
spec=importlib.util.spec_from_file_location('approved40_audit',ROOT/'docs/research/continuation/code-pair-history/audit.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
OLD='/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-r'
NEW=str(ROOT)
relocated=[]
def equal(a,b,path=''):
 if type(a)!=type(b):raise AssertionError(path)
 if isinstance(a,dict):
  assert a.keys()==b.keys(),path
  for k in a:equal(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  assert len(a)==len(b),path
  for i,(x,y)in enumerate(zip(a,b)):equal(x,y,path+'/'+str(i))
 elif a!=b:
  # Only real reader file path fields; same repository-relative artifact.
  assert path.endswith('/path')and '/reader/files/'in path and isinstance(a,str)and isinstance(b,str),path
  assert b.startswith(OLD+'/')and a==NEW+b[len(OLD):],(path,a,b)
  relative=b[len(OLD)+1:];raw=(ROOT/relative).read_bytes()
  blob=subprocess.check_output(['git','show','7fff6a0191413e2b0cd13b6648325815bcef5561:'+relative],cwd=ROOT)
  assert raw==blob,path
  relocated.append({'field':path,'from':b,'to':a,'repository_relative':relative,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
def run():
 ledger=json.loads((source.OUT/'observations.json').read_text())
 equal(source.observe(),ledger['observations'])
 seals=json.loads((source.OUT/'final-seals.json').read_text())
 unique={};total=0
 for item in seals['files']:
  p=ROOT/item['path'];raw=p.read_bytes();assert len(raw)==item['size']and hashlib.sha256(raw).hexdigest()==item['sha256'],item['path']
  if item['git_blob']not in unique:
   unique[item['git_blob']]=subprocess.check_output(['git','cat-file','blob',item['git_blob']],cwd=ROOT)
  assert raw==unique[item['git_blob']],item['path'];total+=len(raw)
 return {'approved_source':'7fff6a0191413e2b0cd13b6648325815bcef5561','original_audit_exit':1,'original_audit_code':'RecordedSemanticChanged','original_audit_error':'Actual native/menu/cursor/print findings differ from recorded original facts','reason':'exact reader artifact checkout root differs; all other fields compared strictly','relocations':relocated,'seal_entries':len(seals['files']),'seal_bytes':total,'unique_git_blobs':len(unique),'no_approved_source_or_raw_changes':True}
if __name__=='__main__':print(json.dumps(run(),indent=2))
