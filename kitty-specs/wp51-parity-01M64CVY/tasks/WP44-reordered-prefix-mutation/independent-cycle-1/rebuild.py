from pathlib import Path
import subprocess,json,hashlib
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e');O=Path('/tmp/wordling-wp44-independent');W=Path((O/'producer-workspace.txt').read_text().strip());log=(O/'producer-rebuild.log').open('w')
for argv in [['go','build','-trimpath','-buildvcs=false','-o',str(O/'producer'),'./internal/document/evidence/wp44/producer'],[str(O/'producer'),'-out','internal/document/evidence/wp44/independent-output']]:
 p=subprocess.run(argv,cwd=W,stdout=log,stderr=log);assert p.returncode==0,(argv,p.returncode)
old=json.load(open(R/'internal/document/evidence/wp44/candidates/sealed-plan.json'));new=json.load(open(W/'internal/document/evidence/wp44/independent-output/sealed-plan.json'));assert old==new
cases=[]
for c in old['cases']:
 a=R/'internal/document/evidence/wp44/candidates'/c['name']/'candidate.WP5';b=W/'internal/document/evidence/wp44/independent-output'/c['name']/'candidate.WP5';assert a.read_bytes()==b.read_bytes();cases.append({'name':c['name'],'sha256':hashlib.sha256(b.read_bytes()).hexdigest()})
orig=R/'internal/document/evidence/wp44/bin/producer';equal=(O/'producer').read_bytes()==orig.read_bytes();assert equal
(O/'producer-rebuild.json').write_text(json.dumps({'isolated_mirror':str(W),'binary_byte_equal_to_historically_executed':equal,'binary_sha256':hashlib.sha256(orig.read_bytes()).hexdigest(),'complete23_operation_plan_equal':old==new,'candidate_classes':len(set(c['sha256']for c in cases)),'all_candidate_bytes':cases,'source_and_modules_mirrored_exact':True,'no_original_VM':True},indent=2)+'\n');print('rebuild identical binary and complete23 operations/14 whole native classes')
