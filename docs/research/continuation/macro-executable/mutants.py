"""Finite behavioral mutants via temporary Go overlays; never changes product files."""
import json, pathlib, subprocess, tempfile, time
ROOT=pathlib.Path(__file__).resolve().parents[4]
OUT=pathlib.Path(__file__).parent/'evidence'/'mutants'
rows=[
 ('stale-ui','TestMacroModelSameRevisionForkAndResizeAuthority',{'internal/tui/model.go':[('if !valid {','if false && !valid {')]}),
 ('zero-sized-authority','TestMacroAuthorityBindsDistinctCursorViewForksBeforeFirstMacro',{'internal/tui/macro_runtime.go':[('type uiTransition struct{ marker byte }','type uiTransition struct{}'),('&uiTransition{1}','&uiTransition{}')],'internal/tui/runtime.go':[('&uiTransition{1}','&uiTransition{}')]}),
 ('duplicate-cpu','TestMacroCompileAndStepDispatchDeliveryExactlyOnce',{'internal/tui/macro_runtime.go':[(' || t.phase != "queued"','')]}),
 ('drop-deferred-child','TestMacroAuthenticNestedReadArrivesWhileHostStopWorkerPending',{'internal/tui/macro_model.go':[('m.macroDeferred = p','m.macroDeferred = nil')]}),
 ('run-after-close','TestMacroCloseAndQueuedCPUReceiptKeepTruthfulOutcome',{'internal/tui/macro_runtime.go':[('if r.stopping {','if false && r.stopping {')]}),
 ('implicit-cout','TestMacroCOUTIsExplicitExactAndSharesOneOpening',{'internal/tui/runtime.go':[('if config.Profile == MacroCOUT {','if true {')]}),
 ('no-cancel-on-close','TestMacroCloseAndQueuedCPUReceiptKeepTruthfulOutcome',{'internal/tui/runtime.go':[('r.macro.cancel()','// cancellation removed by test mutant')]}),
]
def main():
 OUT.mkdir(exist_ok=False);results=[]
 for name,test,changes in rows:
  with tempfile.TemporaryDirectory(prefix='wordling-WP37-mutant-') as tmp:
   replacements={}
   for path,edits in changes.items():
    text=(ROOT/path).read_text()
    for old,new in edits:
     if old not in text:raise ValueError((name,path,old))
     text=text.replace(old,new)
    p=pathlib.Path(tmp)/pathlib.Path(path).name;p.write_text(text)
    (OUT/(name+'-'+p.name+'.txt')).write_text(text)
    replacements[str(ROOT/path)]=str(p)
   overlay=pathlib.Path(tmp)/'overlay.json';overlay.write_text(json.dumps({'Replace':replacements}))
   command=['go','test','-overlay',str(overlay),'-count=1','-timeout=20s','-run','^'+test+'$','./internal/tui']
   started=time.monotonic();p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30)
   raw=p.stdout+p.stderr;(OUT/(name+'.txt')).write_text(raw)
   status='killed' if p.returncode and '--- FAIL:' in raw else 'survived' if not p.returncode else 'invalid'
   results.append({'mutant':name,'test':test,'exit':p.returncode,'status':status,'seconds':time.monotonic()-started,'command':command})
 (OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
 if any(x['status']=='invalid' for x in results):return 1
 return 0
if __name__=='__main__':raise SystemExit(main())
