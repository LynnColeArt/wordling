#!/usr/bin/env python3
"""One finite copied-source campaign; live product files remain unchanged."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile,time
ROOT=pathlib.Path(__file__).resolve().parents[4];HERE=pathlib.Path(__file__).resolve().parent
roster=[
 ('whole-scan','ascii_viewport.go','start < total;','start < min(total, 4096);','TestASCIIWhole',False),
 ('viewport-only','ascii_viewport.go','start := 0; start < total;','start := max(0,total-4096); start < total;','TestASCIIWhole',False),
 ('local-active','ascii_viewport.go','e.TokenIndex == p.CursorGap','e.TokenIndex-start == p.CursorGap','TestASCIIFollow',False),
 ('window-eof','ascii_viewport.go','p.CursorGap == f.total','start+count == f.total','TestASCIIFollow',False),
 ('width1-hidden','ascii_viewport.go','e.TokenIndex == p.CursorGap && e.Span.Length > 0','m.width>1 && e.TokenIndex == p.CursorGap && e.Span.Length > 0','TestASCIIFollow',False),
 ('foreign-revision','ascii_viewport.go','m.ascii.checked && m.ascii.revision == s.NativeRevision','m.ascii.checked','TestASCIIContextEdit',False),
 ('view-requalify','model.go','frame := m.visibleFrame()','if d:=m.session.Document(); d!=nil && m.ordinaryViewEligible(s) {m.ascii=qualifyASCII(d,s.NativeRevision)}\n frame := m.visibleFrame()','TestASCIICache',False),
 ('context-reuse','ascii_viewport.go','m.ascii = asciiQualification{}\n\t\treturn','return','TestASCIICache',False),
 ('live-before-frozen','reveal_inspection.go','frame := *m.macroFrozen','frame := m.legacyFrame()','TestASCIIContextEdit',False),
 ('removed-integration','model.go','model.prepareASCIIViewport()','// removed prepareASCIIViewport','TestASCIIFollow',True)
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(argv,cwd,label):
 start=time.monotonic();p=subprocess.run(argv,cwd=cwd,capture_output=True,timeout=300,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));(HERE/(label+'.stdout')).write_bytes(p.stdout);(HERE/(label+'.stderr')).write_bytes(p.stderr);return {'argv':argv,'cwd':str(cwd),'exit':p.returncode,'elapsed':time.monotonic()-start}
def main():
 results=[]
 for name,file,old,new,tests,pty in roster:
  folder=pathlib.Path(tempfile.mkdtemp(prefix='wordling-WP71-mutant-'+name+'-'))
  shutil.copyfile(ROOT/'go.mod',folder/'go.mod');shutil.copyfile(ROOT/'go.sum',folder/'go.sum');shutil.copytree(ROOT/'internal',folder/'internal',ignore=shutil.ignore_patterns('evidence','__pycache__'));shutil.copytree(ROOT/'cmd',folder/'cmd');(folder/'docs').symlink_to(ROOT/'docs',target_is_directory=True)
  target=folder/'internal/tui'/file;source=target.read_text();assert source.count(old)>=1,(name,source.count(old))
  # context and View have two occurrences: mutate only the actual specified
  # eligibility invalidation / public View site rather than unrelated helpers.
  if name=='view-requalify':
   at=source.index('func (m Model) View()');source=source[:at]+source[at:].replace(old,new,1)
  else:source=source.replace(old,new,1)
  target.write_text(source)
  row={'name':name,'file':file,'original_sha256':sha(ROOT/'internal/tui'/file),'mutated_sha256':sha(target),'copy':str(folder),'inputs':{str(p.relative_to(folder)):sha(p) for p in (folder/'internal/tui').glob('*.go')}}
  (HERE/(name+'.diff.txt')).write_text(old+'\n=>\n'+new+'\n')
  row['compile']=run(['go','test','./internal/tui','-run','^$'],folder,name+'-compile')
  if row['compile']['exit']==0:
   row['model']=run(['go','test','-count=1','./internal/tui','-run','^'+tests],folder,name+'-model');row['semantic_model_failure']=row['model']['exit']!=0 and b'--- FAIL: TestASCII' in (HERE/(name+'-model.stdout')).read_bytes()
   if pty:
    binary=folder/'wordling';row['build']=run(['go','build','-o',str(binary),'./cmd/wordling'],folder,name+'-build')
    if row['build']['exit']==0:
     row['binary_sha256']=sha(binary);row['pty']=run([sys.executable,'-B',str(HERE/'run_pty.py'),str(binary),str(HERE/(name+'-pty'))],ROOT,name+'-pty')
     data=json.loads((HERE/(name+'-pty')/'results.json').read_bytes());row['semantic_pty_failure']=row['pty']['exit']!=0 and bool(data) and data[0]['failure'] is not None and data[0]['cleanup']['direct_child_reaped']
  results.append(row);(HERE/'mutant-results.json').write_text(json.dumps(results,indent=2)+'\n');print(name,row.get('semantic_model_failure'),row.get('semantic_pty_failure'),flush=True)
 return 0 if len(results)==10 and all(r['compile']['exit']==0 and r.get('semantic_model_failure') and (r['name']!='removed-integration' or r.get('semantic_pty_failure')) for r in results) else 1
if __name__=='__main__':raise SystemExit(main())
