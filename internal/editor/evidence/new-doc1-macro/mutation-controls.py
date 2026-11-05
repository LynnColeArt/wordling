"""Bounded actual-owned-source fault controls. Never imported by the product.
Run from repository root; each mutation is restored before the next. Compile
errors are recorded separately and never counted as semantic kills.
"""
from pathlib import Path
import hashlib,json,subprocess,time
ROOT=Path.cwd()
OUT=ROOT/'internal/editor/evidence/new-doc1-macro/mutants'
OUT.mkdir(exist_ok=True)
variants=[
 ('cancelled-name-stage-reused','session.go','if kind == ReadMacro && s.native != nil && s.native.Birth().IsNew() && !s.newMacro.unedited(s) {','if false && kind == ReadMacro && s.native != nil && s.native.Birth().IsNew() && !s.newMacro.unedited(s) {'),
 ('native-request-unbound','macro_load.go','i.NativeRevision == p.native && i.Repeat == 1','i.Repeat == 1'),
 ('detached-stage-retained','session.go','s = s.advanced()\n\t\ts.newMacro = nil\n\t\ts.detached = receipt(result, false)','s = s.advanced()\n\t\ts.detached = receipt(result, false)'),
 ('admission-removed','session.go','if newTarget && !s.pristineNewMacro() {','if false && newTarget && !s.pristineNewMacro() {'),
 ('target-birth-unbound','new_macro.go','s.native.Birth() == p.birth','true'),
 ('target-source-unbound','new_macro.go','s.newPhase == NewUnpublished && s.source == nil && s.first == nil && s.other == nil','s.newPhase == NewUnpublished && s.first == nil && s.other == nil'),
 ('issued-transition-unbound','new_macro.go','s.transition == p.issued','true'),
 ('ready-transition-unbound','macro_session.go','s.transition != acquired.ready','false'),
 ('ready-source-identity-unbound','macro_session.go','acquired.source.Identity() != o.source.Identity()','false'),
 ('current-transition-unbound','macro_execution.go','s.transition != r.expected','false'),
 ('new-child-io-admitted','macro_execution.go','if r.target != nil {','if false && r.target != nil {'),
 ('new-repeat-broadened','macro_session.go','s.native == nil || s.native.Birth().IsNew() || s.macroOwner','s.native == nil || s.macroOwner'),
 ('new-switch-broadened','macro_session.go','(s.native != nil && s.native.Birth().IsNew()) || s.mode != Editing','s.mode != Editing'),
 ('fixed-text-delivery','macro_execution.go','Text: string(byte(e.Words[0].Value))','Text: "X"'),
 ('source-span-lost','macro_execution.go','MacroReceipt{Effect: e,','MacroReceipt{Effect: vm.Effect{Kind:e.Kind, Words:e.Words},'),
 ('applied-receipt-count-lost','macro_execution.go','r.applied++','r.applied += 0'),
 ('driver-budget-reset','macro_session.go','vm.New(program, run, run, limits)','vm.New(program, run, run, vm.DefaultLimits())'),
 ('first-publication-stale-body','new_binding.go','raw, err := s.native.Export()','raw, err := s.native.Export(); if len(raw)>324 { raw=raw[:324] }'),
 ('new-integration-deleted','session.go','if newTarget && !s.pristineNewMacro() {','if newTarget {'),
]
records=[]
for name,file,old,new in variants:
 p=ROOT/'internal/editor'/file;b=p.read_bytes();s=b.decode();assert s.count(old)==1,(name,s.count(old));changed=s.replace(old,new);started=time.monotonic()
 record={'name':name,'path':str(p.relative_to(ROOT)),'before_sha256':hashlib.sha256(b).hexdigest(),'mutant_sha256':hashlib.sha256(changed.encode()).hexdigest(),'old':old,'new':new}
 try:
  p.write_text(changed)
  for phase,command in [('compile',['go','test','-timeout=90s','./internal/editor','-run','^$']),('test',['go','test','-timeout=90s','./internal/editor','-run','TestNewMacro','-count=1'])]:
   r=subprocess.run(command,capture_output=True,text=True,timeout=120)
   (OUT/(name+'-'+phase+'.txt')).write_text(r.stdout+r.stderr)
   record[phase]={'command':command,'exit':r.returncode}
   if phase=='compile' and r.returncode:break
  record['outcome']='compile-invalid' if record['compile']['exit'] else ('semantic-kill' if record['test']['exit'] else 'survived')
 finally:
  p.write_bytes(b)
  assert p.read_bytes()==b
  record['seconds']=round(time.monotonic()-started,3);records.append(record)
  (OUT/'results.json').write_text(json.dumps(records,indent=2)+'\n')
 print(name,record['outcome'],flush=True)
assert all(r['outcome']=='semantic-kill' for r in records), 'Retain survivors/invalids and strengthen honestly before rerun'
