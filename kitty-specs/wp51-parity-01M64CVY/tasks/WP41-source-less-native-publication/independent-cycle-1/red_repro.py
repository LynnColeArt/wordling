from pathlib import Path
import subprocess,json,hashlib
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-b');T=Path('/tmp/wordling-wp41-independent/old-module');T.mkdir(exist_ok=False)
def git(p):return subprocess.check_output(['git','show','70e02f7:'+p],cwd=R)
names=subprocess.check_output(['git','ls-tree','-r','--name-only','70e02f7','--','internal/storage','internal/wp51','internal/macro/wpm'],cwd=R,text=True).splitlines();names=[p for p in names if p.endswith('.go')]
contract='kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json';c=json.loads(git(contract));plain=next(x['path']for x in c['fixtures']if x['id']=='plain');names+=['go.mod','go.sum',contract,plain]
seals={}
for p in names:
 b=git(p);target=T/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b);seals[p]=hashlib.sha256(b).hexdigest()
original=Path('/tmp/wordling-publication-alias-independent/publication_alias_test.go.txt').read_bytes();(T/'internal/storage/independent_review_alias_test.go').write_bytes(original)
p=subprocess.run(['go','test','-race','-count=1','./internal/storage','-run','^TestIndependentPrepared','-v'],cwd=T,capture_output=True,text=True)
Path('/tmp/wordling-wp41-independent/aliases-red.log').write_text(p.stdout+p.stderr)
assert p.returncode==1 and p.stdout.count('--- FAIL: TestIndependentPrepared')==3 and 'DATA RACE'not in p.stdout+p.stderr,p.stdout+p.stderr
Path('/tmp/wordling-wp41-independent/old-source-seals.json').write_text(json.dumps({'source':'70e02f7','command':['go','test','-race','-count=1','./internal/storage','-run','^TestIndependentPrepared','-v'],'exit':p.returncode,'source_sha256':seals,'repro_sha256':hashlib.sha256(original).hexdigest()},indent=2)+'\n')
print('Three original independent behavioral assertions fail on exact unchanged70e02f7 under race; no data race.')
