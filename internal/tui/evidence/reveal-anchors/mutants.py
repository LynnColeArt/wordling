#!/usr/bin/env python3
"""Finite semantic mutations of copied actual H source; never edit live source."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile,time
ROOT=pathlib.Path(__file__).resolve().parents[4];HERE=pathlib.Path(__file__).resolve().parent
model=(ROOT/'internal/tui/model.go').read_text();inspection=(ROOT/'internal/tui/reveal_inspection.go').read_text()
roster=[
 ('upper-row','model.go','lines[0] = revealBase + frame.normal','lines[1] = revealBase + frame.normal',True),
 ('lower-row','model.go','lines[13] = frame.reveal','lines[3] = frame.reveal',False),
 ('footer-row','model.go','lines[24] = renderReveal','lines[23] = renderReveal',False),
 ('footer35-45','model.go','" to restore screen" + strings.Repeat(" ", 44)','" to restore scree" + strings.Repeat(" ", 45)',False),
 ('footer-role','model.go','{text: "Reveal Codes", role: revealCode}','{text: "Reveal Codes", role: revealBase}',False),
 ('lower-caret-width','model.go','min(frame.x, m.width-1), 0','min(frame.x+6, m.width-1), 0',False),
 ('fixed-witness','model.go','lines[13] = frame.reveal','lines[13] = "A[BOLD]BC[bold]D"',True),
 ('live-frozen-layout','reveal_inspection.go','frame := *m.macroFrozen','frame := *m.macroFrozen\n\t\tframe.anchors = false',False),
 ('hide-unsupported-error','reveal_inspection.go','frame.anchors = m.anchorEligible(s, frame)','frame.err = nil\n\tframe.inspection.Partial = false\n\tframe.anchors = m.anchorEligible(s, frame)',False),
 ('hide-unknown-history','model.go',' || !s.HistoryCountKnown','',False),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(argv,cwd,label,timeout=300):
 start=time.monotonic();r=subprocess.run(argv,cwd=cwd,capture_output=True,timeout=timeout,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));(HERE/(label+'.stdout')).write_bytes(r.stdout);(HERE/(label+'.stderr')).write_bytes(r.stderr);return {'argv':argv,'cwd':str(cwd),'exit':r.returncode,'elapsed':time.monotonic()-start,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest()}
def main():
 results=[]
 for name,file,old,new,pty in roster:
  folder=pathlib.Path(tempfile.mkdtemp(prefix='wordling-WP69-mutant-'+name+'-'));shutil.copyfile(ROOT/'go.mod',folder/'go.mod');shutil.copyfile(ROOT/'go.sum',folder/'go.sum')
  shutil.copytree(ROOT/'internal',folder/'internal',ignore=shutil.ignore_patterns('evidence','__pycache__'));shutil.copytree(ROOT/'cmd',folder/'cmd');(folder/'docs').symlink_to(ROOT/'docs',target_is_directory=True)
  target=folder/'internal/tui'/file;s=target.read_text();assert s.count(old)==1,(name,s.count(old));target.write_text(s.replace(old,new));row={'name':name,'actual_mutated_source_sha256':sha(target),'original_sha256':sha(ROOT/'internal/tui'/file),'source_path':str(target),'actual_inputs':{str(x.relative_to(folder)):sha(x) for x in (folder/'internal/tui').glob('*.go')}}
  (HERE/(name+'.diff.txt')).write_text(old+'\n=>\n'+new+'\n')
  # Compile validity is distinct from semantic rejection.
  row['compile']=run(['go','test','./internal/tui','-run','^$'],folder,name+'-compile');assert row['compile']['exit']==0,row
  row['model']=run(['go','test','-count=1','./internal/tui','-run','^TestAnchor'],folder,name+'-model');row['semantic_model_kill']=row['model']['exit']!=0
  if pty:
   binary=folder/'wordling';row['build']=run(['go','build','-o',str(binary),'./cmd/wordling'],folder,name+'-build');assert row['build']['exit']==0
   row['binary_sha256']=sha(binary);row['pty']=run([sys.executable,'-B',str(HERE/'run_pty.py'),str(binary),str(HERE/(name+'-pty'))],ROOT,name+'-pty',65);row['semantic_pty_kill']=row['pty']['exit']!=0
  results.append(row);(HERE/'mutant-results.json').write_text(json.dumps(results,indent=2)+'\n');print(name,row['semantic_model_kill'],row.get('semantic_pty_kill'),flush=True)
  if not row['semantic_model_kill'] or pty and not row['semantic_pty_kill']:return 1
 return 0
if __name__=='__main__':raise SystemExit(main())
