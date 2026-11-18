from pathlib import Path
import collections, hashlib, json, os, subprocess, tarfile, tempfile, time
R=Path('/home/lynn/projects/wordling');E=Path('/tmp/wordling-mission1-closeout-20261118/wp106-review')
HEAD='8b15d9dc283ad2b3f5013772cd5d9f35c481644d';OLD='9f255248b91f0a695d2affd214f37f50d661a03a'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def digest(b):return hashlib.sha256(b).hexdigest()
source='internal/document/everyday.go';tests='internal/document/retrieve_italics_test.go'
fixed=git('show',HEAD+':'+source);old=git('show',OLD+':'+source);test=git('show',HEAD+':'+tests)
assert digest(fixed)=='c0d32c0ddfd84fd5d7885f2fffa6fae9f86f0eccfad1db7492001f7c7f33e577'
assert digest(old)=='047bd9f4c9b45f21dda88f896167b74bd4eba883f07c9c80dcf80465d23e30ab'
assert digest(test)=='756bd61f4ce8a41824b85dc24ea1396af9f55cc2a960f58ed29c92b42312fafe'
assert test==git('show','fac6f3d46e864e82d66a110e848795ef1c900535:'+tests)
worktrees=git('worktree','list','--porcelain');results=[]
env=dict(os.environ,GOPROXY='off',GOSUMDB='off',GOTOOLCHAIN='local')
def run(name,argv,cwd):
 start=time.monotonic();p=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,timeout=120)
 (E/(name+'.stdout')).write_bytes(p.stdout);(E/(name+'.stderr')).write_bytes(p.stderr)
 events=[]
 for line in p.stdout.decode().splitlines():
  if line.startswith('{'):
   try:events.append(json.loads(line))
   except json.JSONDecodeError:pass
 testevents=[x for x in events if x.get('Test')and x.get('Action')in('pass','fail','skip')]
 names={x['Test']for x in testevents};leaf=[x for x in testevents if not any(n.startswith(x['Test']+'/')for n in names)]
 logs=collections.defaultdict(str)
 for x in events:
  if x.get('Test')and x.get('Output'):logs[x['Test']]+=x['Output']
 failing_leaf=[x['Test']for x in leaf if x['Action']=='fail']
 d=dict(name=name,argv=argv,cwd=str(cwd),exit=p.returncode,seconds=time.monotonic()-start,
   named=dict(collections.Counter(x['Action']for x in testevents)),leaf=dict(collections.Counter(x['Action']for x in leaf)),
   failing_leaf_count=len(failing_leaf),failing_leaf_all_UnsupportedBody=bool(failing_leaf)and all('UnsupportedBody'in logs[n]for n in failing_leaf),
   source_sha=digest((cwd/source).read_bytes()),test_sha=digest((cwd/tests).read_bytes()),stdout_sha=digest(p.stdout),stderr_sha=digest(p.stderr))
 (E/(name+'.run.json')).write_text(json.dumps(d,indent=2)+'\n');results.append(d);print(json.dumps(d),flush=True)
 return d
with tempfile.TemporaryDirectory(prefix='wordling-WP106-independent-',dir='/tmp')as tmp:
 root=Path(tmp);archive=root/'source.tar';tree=root/'tree';tree.mkdir()
 with archive.open('wb')as dest:subprocess.run(['git','archive','--format=tar',HEAD,'go.mod','go.sum','internal','docs/research/reference-runs/mission1-appearance','docs/research/reference-runs/2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5'],cwd=R,stdout=dest,check=True)
 with tarfile.open(archive)as t:t.extractall(tree,filter='data')
 assert (tree/source).read_bytes()==fixed and (tree/tests).read_bytes()==test
 a=run('independent-focused-green',['/usr/local/go/bin/go','test','-mod=readonly','-count=1','-json','./internal/document','-run','TestRetrieveItalics|TestEveryday.*Insert|TestFontAppearance'],tree)
 assert a['exit']==0
 extra=tree/'internal/document/wp106_independent_review_test.go'
 extra.write_text('''package document_test
import (
 "fmt"
 "testing"
 "github.com/lynncoleart/wordling/internal/document"
)
func TestReviewRetrieveItalicsCrossingAttributes(t *testing.T) {
 body := cat(boldOn, retrieveItalicOn, []byte("a"), boldOff, []byte("b"), retrieveItalicOff)
 for _, copy := range []bool{false,true} { t.Run(fmt.Sprintf("copy=%v",copy),func(t *testing.T) {
  retrieveItalicsInserted(t,copy,retrieveItalicsParse(t,[]byte("AB")),1,retrieveItalicsParse(t,body),body,6)
 }) }
}
func TestReviewRetrieveItalicsSelfSource(t *testing.T) {
 body := cat([]byte("L"),retrieveItalicOn,[]byte("x"),retrieveItalicOff,[]byte("R"))
 for _, copy := range []bool{false,true} { t.Run(fmt.Sprintf("copy=%v",copy),func(t *testing.T) {
  d := retrieveItalicsParse(t,body)
  retrieveItalicsInserted(t,copy,d,0,d,body,5)
  c,_ := d.CursorAt(2)
  retrieveItalicsRefused(t,copy,d,c,d,document.UnsupportedBody)
 }) }
}
''')
 b=run('independent-extra-native-green',['/usr/local/go/bin/go','test','-mod=readonly','-count=1','-json','./internal/document','-run','TestReviewRetrieveItalics'],tree)
 assert b['exit']==0
 extra.unlink();(tree/source).write_bytes(old)
 c=run('independent-exact-final-red-replay',['/usr/local/go/bin/go','test','-mod=readonly','-count=1','-json','./internal/document','-run','TestRetrieveItalics'],tree)
 assert c['exit']==1 and c['leaf']=={'pass':42,'fail':50} and c['failing_leaf_all_UnsupportedBody'],c
 isolated=str(root)
assert not Path(isolated).exists();assert git('worktree','list','--porcelain')==worktrees
assert (R/source).read_bytes()==fixed and (R/tests).read_bytes()==test
(E/'independent-check-summary.json').write_text(json.dumps(dict(fixed_head=HEAD,old_source=OLD,results=results,isolation_removed=True,registered_worktrees_unchanged=True,primary_source_test_unchanged=True,operational_reference_actions=0,Mac_actions=0),indent=2)+'\n')
print('Temporary source archive removed; registered worktrees and primary Go source/tests unchanged.',flush=True)
