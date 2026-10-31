#!/usr/bin/env python3
"""Bounded compiling mutations of the live composition; never edit source."""
import hashlib,json,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
cases=[
 ('wrapper-address','runtime.go','request.Directory == nil || *request.Directory != *r.directory','request.Directory != r.directory','TestCapturedDirectoryCapabilityNotWrapperOrInode'),
 ('snapshot-instead-of-candidate','runtime.go','result.Outcome, result.Err = request.Directory.Publish(publication, id)','result.Outcome, result.Err = request.Directory.Save(request.Document, request.Destination, request.Decision)','TestLiveEditingAndCandidatePublication'),
 ('selected-delete-alias','model.go','case tea.KeyDelete:\n\t\t\tevent.Command = editor.Delete','case tea.KeyDelete:\n\t\t\tevent.Command = editor.Backspace','TestLiveBlockAnswersAndOverlay'),
 ('no-virtual-block','model.go','blockStart, blockEnd = overlay.FragmentStart, overlay.FragmentEnd','blockStart, blockEnd = -1, -1','TestLiveBlockAnswersAndOverlay'),
 ('candidate-borrowed','runtime.go','request.Candidate = append([]byte(nil), request.Candidate...)','// mutant borrows candidate','TestPreparedCandidateOwnsInputAndCorrectPublicationID'),
 ('published-generic-error-forgotten','runtime.go','result.Err != nil && result.Outcome.State == storage.Published','false','TestActualPublishedGenericErrorRetainsUncertainty'),
]
rows=[];archive=HERE/'mutants';archive.mkdir(exist_ok=True)
for name,file,old,new,test in cases:
 target=ROOT/'internal/tui'/file;source=target.read_text();assert source.count(old)==1,(name,source.count(old))
 mutant=source.replace(old,new)
 # The snapshot mutation still prepares the request; preserve compilation.
 if name=='snapshot-instead-of-candidate':mutant=mutant.replace('publication, err :=','_, err :=')
 frozen=archive/(name+'.go.txt');frozen.write_text(mutant)
 with tempfile.TemporaryDirectory(prefix='wp28-mutant-') as temp:
  overlay=Path(temp)/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(target):str(frozen)}}))
  argv=['go','test','-overlay',str(overlay),'./internal/tui','-run','^'+test+'$','-count=1','-v'];p=subprocess.run(argv,cwd=ROOT,capture_output=True)
  (archive/(name+'.txt')).write_bytes(p.stdout+p.stderr)
  killed=p.returncode!=0 and b'--- FAIL:' in p.stdout and b'build failed' not in p.stdout+p.stderr
  rows.append({'name':name,'source':str(target.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'argv':argv,'exit':p.returncode,'behaviorally_killed':killed})
  assert killed,(name,p.stdout,p.stderr)
(HERE/'mutation-results.json').write_text(json.dumps(rows,indent=2)+'\n');print('Six compiling changed-boundary semantic mutants killed')
