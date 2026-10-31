#!/usr/bin/env python3
"""Compiling changed-scope host mutants over owned source only."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent/'mutations';OUT.mkdir()
rows=[
 ('repeat-worker','internal/tui/new_runtime.go','if t.phase != "queued" {','if false && t.phase != "queued" {','^TestNewRuntimeTicketsDuplicateForgeryForkAndStaleUI$',''),
 ('counter-collapse','internal/tui/new_runtime.go','if t := r.firstTickets[key]; key.Valid() && t != nil {','for _, prior := range r.firstTickets { if prior.request.Operation == i.Operation && prior.request.Revision == i.Revision && prior.request.Kind == i.Kind { return prior, func() tea.Msg { return duplicateDispatchMsg{} } } }; if t := r.firstTickets[key]; key.Valid() && t != nil {','^TestNewRuntimeTicketsDuplicateForgeryForkAndStaleUI$',''),
 ('lost-unknown-error','internal/tui/new_model.go','if phase == editor.PublicationUncertain {','if false && phase == editor.PublicationUncertain {','^TestWP48Actual41FaultRuntimeComposition$','overlay'),
 ('wrong-F10-context','internal/tui/model.go','m.session.Snapshot().NewPhase == editor.PublishedUnbound','m.session.Snapshot().NewPhase == editor.PublicationUncertain','^TestNewRuntimeActualPostPublishReadMismatchRetryAndClose$',''),
 ('foreign-root','internal/tui/new_runtime.go','if t.refused == nil && (i.Directory == nil || *i.Directory != *r.directory) {','if false && t.refused == nil && (i.Directory == nil || *i.Directory != *r.directory) {','^TestNewForeignTicketAndIndependentRootNeverRun$',''),
]
results=[]
for name,path,old,new,test,extra in rows:
 out=OUT/name;out.mkdir();raw=(ROOT/path).read_text();assert raw.count(old)==1,(name,raw.count(old));changed=raw.replace(old,new);(out/'source.go.txt').write_text(changed)
 mapping=json.loads((OUT.parent/'overlay/map.json').read_text()) if extra else {'Replace':{}}
 mapping['Replace'][str(ROOT/path)]=str(out/'source.go.txt');(out/'map.json').write_text(json.dumps(mapping,indent=2)+'\n')
 argv=['go','test','-count=1','-overlay',str(out/'map.json'),'./internal/tui','-run',test,'-v'];p=subprocess.run(argv,cwd=ROOT,capture_output=True);(out/'stdout.log').write_bytes(p.stdout);(out/'stderr.log').write_bytes(p.stderr);compiled=b'[build failed]'not in p.stdout+p.stderr and b'setup failed'not in p.stdout+p.stderr;killed=p.returncode!=0 and compiled
 results.append({'name':name,'argv':argv,'exit':p.returncode,'compiled':compiled,'killed':killed,'mutant_sha256':hashlib.sha256(changed.encode()).hexdigest()});assert killed,(name,p.stdout,p.stderr)
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'compiling_mutants_killed':len(results)}))
