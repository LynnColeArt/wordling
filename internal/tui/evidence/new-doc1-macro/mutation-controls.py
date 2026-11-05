"""Actual H-owned compile-valid faults; no G/live-lane mutation or product flag."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys,time
sys.dont_write_bytecode=True
ROOT=Path.cwd();OUT=ROOT/('internal/tui/evidence/new-doc1-macro/mutants-fixed' if len(sys.argv)>1 else 'internal/tui/evidence/new-doc1-macro/mutants');OUT.mkdir()
variants=[
 ('new-host-admission-removed','macro_model.go','d.Birth().IsNew() && !m.newMacroHostIdle()','false && d.Birth().IsNew() && !m.newMacroHostIdle()'),
 ('prior-issue-history-ignored','macro_model.go','m.runtime.issued == 0 &&','true &&'),
 ('prior-executed-history-ignored','macro_model.go','len(m.runtime.executed) == 0 &&','true &&'),
 ('prior-first-tickets-ignored','macro_model.go','len(m.runtime.firstTickets) == 0 &&','true &&'),
 ('prior-macro-results-ignored','macro_model.go','len(m.runtime.macroResults) == 0','true'),
 ('authentic-notice-cleared','macro_model.go','m.notice != "" || m.reconcile','false || m.reconcile'),
 ('current-ui-token-ignored','macro_runtime.go','r.uiAuthority == nil || r.uiAuthority != token','r.uiAuthority == nil'),
 ('root-IO-executes-twice','runtime.go','if r.executed[key] {','if false && r.executed[key] {'),
 ('worker-executes-twice','macro_runtime.go','t.phase != "queued" {','false {'),
 ('macro-source-receipt-lost','macro_runtime.go','Source: p.Source, Steps:','Source: [32]byte{}, Steps:'),
 ('work-counter-reset','macro_model.go','Steps: p.TotalSteps, Words:','Steps: 0, Words:'),
 ('frozen-frame-ignored','reveal_inspection.go','if m.macroStatus.DisplaySuppressed && m.macroFrozen != nil {\n\t\tframe :=','if false && m.macroStatus.DisplaySuppressed && m.macroFrozen != nil {\n\t\tframe :='),
 ('first-read-queue-deleted','new_model.go','if intent != nil {\n\t\treturn m.queueFirst','if false && intent != nil {\n\t\treturn m.queueFirst'),
 ('shown-menu-falls-through','menu_bar.go','return m, true\n\t}\n\tif menuKey(k)','return m, false\n\t}\n\tif menuKey(k)'),
 ('integration-deleted','macro_model.go','return m.macroStart()','return m, nil'),
]
# A bad H worker can bypass VM and call ordinary Text with constant FLOW output.
# Healthy FLOW PTYs may pass this fault; required distinct ABC must reject it.
p=ROOT/'internal/tui/macro_runtime.go';source=p.read_text();a=source.index('\t\tcase "start":');b=source.index('\t\tcase "step":',a)
fixed='''\t\tcase "start":
 next,_,err:=s.Reduce(editor.Event{Command:editor.CancelOperation})
 o.err=err
 o.session=next
 if err==nil { o.session,_,o.err=next.Reduce(editor.Event{Command:editor.Text,Text:"TRUEFALSETAIL"}) }
 o.progress=editor.MacroProgress{State:"complete",Terminal:true,Source:f.latest.Source,Run:1,Screen:1,TotalSteps:1,TotalWords:13,AppliedWords:13,Completed:1,Repeat:1}
'''
variants.append(('fixed-FLOW-bypasses-VM','macro_runtime.go',source[a:b],fixed))
# Losing the real H owner on a manual key strands an authentic continuation,
# even though G's own active-delivery guard remains intact.
p=ROOT/'internal/tui/macro_model.go';source=p.read_text();needle='if m.macro != nil {\n\t\tif kcode == tea.KeyF1'
variants.append(('manual-key-drops-current-owner','macro_model.go',needle,'if m.macro != nil {\n m.macro=nil; m.macroTicket=nil; m.macroCPU=false; return m,nil,true\n }\n if false {\n\t\tif kcode == tea.KeyF1'))
if len(sys.argv)>1:variants=[v for v in variants if v[0]==sys.argv[1]]
results=[]
for name,file,old,new in variants:
 p=ROOT/'internal/tui'/file;original=p.read_bytes();s=original.decode();assert s.count(old)==1,(name,s.count(old));modified=s.replace(old,new)
 if name=='fixed-FLOW-bypasses-VM':modified=modified.replace('vm "github.com/lynncoleart/wordling/internal/macro/runtime"','')
 record={'name':name,'path':str(p.relative_to(ROOT)),'source_sha256':hashlib.sha256(original).hexdigest(),'mutant_sha256':hashlib.sha256(modified.encode()).hexdigest(),'old':old,'new':new};started=time.monotonic()
 try:
  p.write_text(modified)
  for phase,command in [('compile',['go','test','-timeout=90s','./internal/tui','-run','^$']),('test',['go','test','-timeout=90s','./internal/tui','-count=1'])]:
   run=subprocess.run(command,capture_output=True,text=True,timeout=120);(OUT/(name+'-'+phase+'.txt')).write_text(run.stdout+run.stderr);record[phase]={'argv':command,'exit':run.returncode}
   if phase=='compile' and run.returncode:break
  record['outcome']='compile-invalid' if record['compile']['exit'] else ('semantic-kill' if record['test']['exit'] else 'survived')
  if name in ['integration-deleted','fixed-FLOW-bypasses-VM','shown-menu-falls-through'] and record['compile']['exit']==0:
   binary=Path('/tmp/wordling-WP66-mutant-'+name+'.bin');cmd=['go','build','-o',str(binary),'./cmd/wordling'];build=subprocess.run(cmd,capture_output=True,text=True,timeout=300);(OUT/(name+'-build.txt')).write_text(build.stdout+build.stderr);assert build.returncode==0
   target=OUT/(name+'-PTY');cmd=[sys.executable,str(ROOT/'internal/tui/evidence/new-doc1-macro/run_pty.py'),str(binary),str(target)];run=subprocess.run(cmd,capture_output=True,text=True,timeout=105);(OUT/(name+'-PTY.txt')).write_text(run.stdout+run.stderr);record['PTY']={'argv':cmd,'exit':run.returncode,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'built_actual_mutated_H_source':True};assert run.returncode!=0,'actual production did not notice source fault'
 finally:
  p.write_bytes(original);assert p.read_bytes()==original;record['seconds']=round(time.monotonic()-started,6);results.append(record);(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,record['outcome'],record.get('PTY',{}).get('exit'),flush=True)
assert all(r['outcome']=='semantic-kill' for r in results),'Retain and report actual survivors/compile failures; never count them as kills'
