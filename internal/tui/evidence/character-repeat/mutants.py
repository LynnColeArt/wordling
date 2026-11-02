"""Finite compiled semantic controls in disposable source copies, never live source."""
import sys,os,pathlib,tempfile,shutil,subprocess,time,json,hashlib,difflib
ROOT=pathlib.Path(__file__).resolve().parents[4];HERE=pathlib.Path(__file__).resolve().parent
# Eleven finite controls; omission of a late capacity check alone is unreachable
# under the strict constructor/count grammar and is not claimed killed.
def pty_negative(binary,out):
 import importlib.util
 spec=importlib.util.spec_from_file_location('bounded_transport',ROOT/'internal/tui/evidence/reveal-anchors/run_pty.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
 out.mkdir();p=base.Run(binary,out);error=None;actual=None;missing=None
 try:
  p.launch();assert 'bounded native editing' in p.terminal.text(),'startup setup'
  p.send(b'\x1b','Escape separately',.15)
  end=min(p.end,time.monotonic()+.5)
  while 'Repeat Value =' not in p.terminal.text() and time.monotonic()<end:p.collect(.01)
  missing='Repeat Value =' not in p.terminal.text()
  # This fixed negative oracle proceeds despite the recorded missing prefix.
  p.send(b'5','planned digit despite removed integration',.1);p.send(b'x','planned character',.1)
  assert not p.terminal.unknown,p.terminal.unknown
  actual=p.terminal.rows()[0].rstrip();frame=dict(rows=p.terminal.rows(),cursor=[p.terminal.x,p.terminal.y],roles=list(p.terminal.roles(0)),expected='xxxxx',actual=actual)
  assert actual=='5x' and [p.terminal.x,p.terminal.y]==[2,0],('unrelated negative outcome',frame)
  p.witnesses.append(frame)
  p.send(b'\x1b[18~','F7');assert 'Save document? Yes (No)' in p.terminal.text()
  p.send(b'n','No save');assert 'Exit WP? No (Yes)' in p.terminal.text()
  p.send(b'y','Yes exit',.1);p.proc.wait(timeout=1);assert p.proc.returncode==0
 except Exception as e:error=repr(e)
 finally:
  cleanup=p.close();record=dict(failure=error,missing_prompt=missing,actual_final_text=actual,expected_final_text='xxxxx',semantic_target_failed=error is None and actual!='xxxxx',cleanup=cleanup,argv=p.argv,cwd=str(ROOT),environment={k:p.env.get(k) for k in ['TERM','LANG','COLORTERM','NO_COLOR']},termios_before=repr(p.before),binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),frames=p.witnesses)
  (out/'result.json').write_text(json.dumps(record,indent=2))
 if error or not cleanup['termios_restored']:return 2
 return 1 if record['semantic_target_failed'] else 0
if len(sys.argv)>1 and sys.argv[1]=='pty':
 sys.exit(pty_negative(pathlib.Path(sys.argv[2]).resolve(),pathlib.Path(sys.argv[3]).resolve()))
controls=[
 ('ignore-count','character_repeat.go','characterPayload(c, p.count)','characterPayload(c, 1)','Public'),
 ('hardcode','character_repeat.go','characterPayload(c, p.count)','characterPayload(\'x\', 5)','Public'),
 ('count-digit','character_repeat.go','characterPayload(c, p.count)',"characterPayload('0'+p.count, p.count)",'Public'),
 ('retain-count','character_repeat.go','return m.reduce(editor.Event{Command: editor.Text, Text: characterPayload(c, p.count)})','m.characterRepeat=p\n return m.reduce(editor.Event{Command: editor.Text, Text: characterPayload(c, p.count)})','Public'),
 ('second-digit','character_repeat.go',"p.count == 0 && c >= '1'", "c >= '1'",'Refusals'),
 ('stale-ui','model.go','if !valid {','if !valid && m.characterRepeat.active {m.runtime.mu.Lock();token=m.runtime.uiAuthority;m.runtime.mu.Unlock();valid=true}\n if !valid {','NeutralAndStale'),
 ('opaque-owner','character_repeat.go','if p.active && (p.native != s.NativeRevision','if false && p.active && (p.native != s.NativeRevision','StructuralForeignAndControl'),
 ('pending-dispatch','model.go','if m.characterRepeat.active {\n\t\treturn m.characterPress(*event.Key)\n\t}', 'if m.characterRepeat.active && event.Key.Mod==0 {\n return m.characterPress(*event.Key)\n }','Refusals'),
 ('retain-invalidation','character_repeat.go','m.characterRepeat = characterRepeat{}\n}', 'return\n}','Invalidation'),
 ('view-consumes','model.go','func (m Model) View() tea.View {','func (m Model) View() tea.View {if m.characterRepeat.active {m.runtime.claimUI(m.uiAuthority)}','Public'),
 ('integration-removed','model.go','if next, handled := m.beginCharacterRepeat(*k); handled {','if next, handled := m.beginCharacterRepeat(*k); false && handled {','Public'),
]
def call(folder,label,argv,cwd):
 start=time.monotonic();p=subprocess.run(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300,env={**os.environ,'GOTOOLCHAIN':'local','GOPROXY':'off'})
 (folder/(label+'.stdout')).write_bytes(p.stdout);(folder/(label+'.stderr')).write_bytes(p.stderr)
 return dict(argv=argv,cwd=str(cwd),exit=p.returncode,elapsed=time.monotonic()-start)
rows=[]
for name,file,old,new,target in controls:
 folder=HERE/'mutants'/name;folder.mkdir(parents=True)
 work=pathlib.Path(tempfile.mkdtemp(prefix='wordling-wp73-mutant-'))
 try:
  for p in ROOT.glob('internal/**/*.go'):
   if 'evidence' in p.relative_to(ROOT).parts:continue
   dst=work/p.relative_to(ROOT);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
  dst=work/'cmd/wordling';dst.mkdir(parents=True);shutil.copyfile(ROOT/'cmd/wordling/main.go',dst/'main.go')
  for f in ['go.mod','go.sum']:shutil.copyfile(ROOT/f,work/f)
  path=work/'internal/tui'/file;before=path.read_text();assert before.count(old)==1,(name,before.count(old));after=before.replace(old,new);path.write_text(after)
  (folder/'change.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=file,tofile=file)))
  compile=call(folder,'compile',['go','test','./internal/tui','-run','^$'],work)
  test=call(folder,'target',['go','test','./internal/tui','-run','^TestCharacterRepeat'+target+'$','-count=1'],work) if compile['exit']==0 else None
  record=dict(name=name,compile=compile,test=test,mutated_sha256=hashlib.sha256(after.encode()).hexdigest(),killed=compile['exit']==0 and test is not None and test['exit']==1)
  if name=='integration-removed' and compile['exit']==0:
   record['build']=call(folder,'build',['go','build','-o','/tmp/wordling-wp73-integration-mutant','./cmd/wordling'],work)
   record['binary_sha256']=hashlib.sha256(pathlib.Path('/tmp/wordling-wp73-integration-mutant').read_bytes()).hexdigest()
 finally:shutil.rmtree(work)
 record['disposable_copy_removed']=not work.exists();(folder/'result.json').write_text(json.dumps(record,indent=2));rows.append(record);print(name,record['killed'],flush=True)
(HERE/'mutants.json').write_text(json.dumps(rows,indent=2));sys.exit(0 if all(r['killed'] for r in rows) else 1)
