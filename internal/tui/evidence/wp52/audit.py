#!/usr/bin/env python3
"""Recompute sealed WP52 evidence offline; --git also proves committed blobs.
No application process, reference VM, private resource copy or expectation repair.
"""
import argparse,hashlib,json,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
from run_pty import Styled
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(git=False):
 manifest=json.loads((HERE/'manifest.json').read_bytes())
 for path,x in manifest['files'].items():
  b=(ROOT/path).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256'],path
  if git:assert subprocess.check_output(['git','show','HEAD:'+path],cwd=ROOT)==b,path
 a=json.loads((HERE/'build/source.json').read_bytes());b=json.loads((HERE/'build-final/source.json').read_bytes())
 assert a['actual_compiled_project_inputs']==b['actual_compiled_project_inputs']
 for path,x in b['actual_compiled_project_inputs'].items():assert sha((ROOT/path).read_bytes())==x['sha256'],path
 go={str(p.relative_to(ROOT)) for prefix in ['internal','cmd'] for p in (ROOT/prefix).rglob('*.go')};assert go==set(b['complete_local_Go_SET'])
 for path,x in b['complete_local_Go_SET'].items():assert sha((ROOT/path).read_bytes())==x['sha256'],path
 for folder,record in [('build',a),('build-final',b)]:assert sha((HERE/folder/'wordling.bin').read_bytes())==record['binary']['sha256']
 assert a['environment']['GOFLAGS']==b['environment']['GOFLAGS']=='' and a['environment']['GOWORK']==b['environment']['GOWORK']==''
 proof=json.loads((HERE/'wordling-WP52-claim-source-proof.json.txt').read_bytes())
 for path,h in proof['files'].items():
  if path!='internal/tui/model.go':assert sha((ROOT/path).read_bytes())==h,path
 assert set(a['actual_compiled_project_inputs'])==set(proof['files'])|{'internal/tui/reveal.go','go.mod','go.sum'}
 assert not any('/evidence/' in p for p in a['actual_compiled_project_inputs'])
 package=a['actual_compiled_packages'];assert all(not p['CgoFiles'] and not p['EmbedFiles'] for p in package)
 assert all(Path(p['Dir']).is_relative_to(ROOT) for p in package)
 xml=ET.parse(HERE/'checks/final-configured.xml').getroot();assert xml.attrib['tests']=='7' and xml.attrib['failures']=='0' and xml.attrib['skipped']=='0'
 mutants=json.loads((HERE/'mutants/result.json').read_bytes());assert len(mutants['mutants'])==6 and all(x['compile_exit']==0 and x['test_exit']!=0 for x in mutants['mutants']) and mutants['exact_source_restored']
 assert (HERE/'checks/gofmt.log').read_bytes()==b'' and (HERE/'checks/diff-lint.log').read_bytes()==b''
 receipts=json.loads((HERE/'pty-07/result.json').read_bytes());assert len(receipts['results'])==2
 replay=json.loads((HERE/'raw-replay.json').read_bytes());assert replay['captured_receipt_sha256']==sha((HERE/'pty-07/result.json').read_bytes()) and replay['observer_source_sha256']==sha((HERE/'run_pty.py').read_bytes())
 for r in receipts['results']:
  folder=HERE/'pty-07'/('native-r'+str(r['repeat']));wire=(folder/'wire-output.bin').read_bytes()
  assert sha(wire)==r['raw_wire_sha256'] and r['returncode']==0 and r['termios_restored'] and r['failure'] is None
  assert r['argv']==[str(HERE/'build/wordling.bin'),'-root',str(folder/'files'),'-profile','local-flat']
  assert r['binary_sha256']==a['binary']['sha256'] and r['color_environment']['NO_COLOR'] is None
  assert r['COPY_sha256']==r['native_sha256']=='c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d'
  assert (folder/'files/COPY').read_bytes()==(folder/'files/ORIGIN').read_bytes()
  assert len(r['witnesses'])==15
  injected=json.loads((folder/'injected.json').read_bytes());assert [x['hex'] for x in injected[4:19]]==['1b5b31333b337e']+['1b5b43']*6+['1b5b44']*6+['1b5b31333b337e']*2
  for w in r['witnesses']:
   t=Styled();t.feed(wire[:w['wire_bytes']]);assert not t.pending and not t.unknown and t.rows()==w['rows'] and [t.x,t.y]==w['cursor']
   # Original optional w['styles'] matrices are aliased diagnostics.
   # Source-bound roles/text/cursor and raw replay are the accepted witness.
   frozen=json.loads((HERE/'raw-replay.json').read_bytes())['processes'][str(r['repeat'])][r['witnesses'].index(w)]
   assert frozen['wire_bytes']==w['wire_bytes'] and f"gap {w['gap']} |" in '\n'.join(w['rows']) and frozen['styles']==[[list(v) for v in row] for row in t.styles]
   if w['view']=='codes':
    g=w['gap'];assert t.roles(3)==w['roles'];assert [i for i,v in enumerate(w['roles']) if v==71]==[[0],list(range(1,7)),[7],[8],list(range(9,15)),[15],[16]][g]
    for rep in [1,2]:
     raw=(ROOT/f'docs/research/continuation/session1/runs/2026-10-31-session1-b01-r{rep}/CMD51-049/codes-gap-{g}/vram.bin').read_bytes()
     for col in range(17 if g==6 else 16):assert raw[13*160+col*2]==ord(t.rows()[3][col]) and raw[13*160+col*2+1]==w['roles'][col]
 assert (HERE/'pty-07/wp52-run_pty.py.txt').read_bytes()==(HERE/'run_pty.py').read_bytes()
 print(json.dumps({'sealed_files':len(manifest['files']),'Git_blob_exact':git,'compiled_inputs':len(a['actual_compiled_project_inputs']),'Go_SET':len(go),'actual_app_PTY_passes':2,'actual_PTY_states':30,'original_captures':28,'original_guests':0,'mutants':6,'configured_checks':7,'full_M1_closed':False}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--git',action='store_true');run(p.parse_args().git)
