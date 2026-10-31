"""Sequential finite final public/OS/Go validation. No reference guest or lifecycle."""
from pathlib import Path
import ast,contextlib,io,json,resource,sys,tempfile,time,unittest,xml.etree.ElementTree as ET
sys.dont_write_bytecode=True
from boundaries import process,read,parse,sha,require,canonical
from source import HERE,ROOT,Sources
import bridge
OUT=HERE/'checks'
def write(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def command(name,argv,cwd=ROOT,timeout=180):
 start=time.monotonic();out,err,code=process(argv,cwd,timeout=timeout,allow_nonzero=True);(OUT/(name+'.stdout.log')).write_bytes(out);(OUT/(name+'.stderr.log')).write_bytes(err);r=dict(name=name,argv=list(map(str,argv)),cwd=str(cwd),whole_exit=code,seconds=time.monotonic()-start,stdout_bytes=len(out),stderr_bytes=len(err),stdout_sha256=sha(out),stderr_sha256=sha(err));require(code==0,'ValidationCommand',r);return r
class Result(unittest.TextTestResult):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.xml=ET.Element('testsuite',name='wp56-public-source-phase-and-host-boundaries')
 def startTest(self,test):super().startTest(test);self.case=ET.SubElement(self.xml,'testcase',name=str(test));self.started=time.monotonic()
 def stopTest(self,test):self.case.set('time',str(time.monotonic()-self.started));super().stopTest(test)
 def addFailure(self,test,err):super().addFailure(test,err);ET.SubElement(self.case,'failure').text=self._exc_info_to_string(err,test)
 def addError(self,test,err):super().addError(test,err);ET.SubElement(self.case,'error').text=self._exc_info_to_string(err,test)
 def addSkip(self,test,why):super().addSkip(test,why);ET.SubElement(self.case,'skipped').text=why
def protect():
 x=parse(read(OUT/'prior-inputs.json',4<<20));rows=x['files'];require(len(rows)==1834,'PriorRoster',len(rows));batches=[];batch=[];size=0
 for p,pin in rows.items():
  if size+pin['size']>16<<20 and batch:batches.append(batch);batch=[];size=0
  batch.append((p,pin));size+=pin['size']
 if batch:batches.append(batch)
 for batch in batches:
  raw,_=process(['git','cat-file','--batch'],ROOT,input_bytes=''.join(x['head']+':'+p+'\n'for p,_ in batch).encode(),stdout_limit=32<<20);pos=0
  for p,pin in batch:
   end=raw.index(b'\n',pos);blob,kind,n=raw[pos:end].split();n=int(n);pos=end+1;b=raw[pos:pos+n];pos+=n;require(raw[pos:pos+1]==b'\n','PriorFrame',p);pos+=1;require(kind==b'blob'and blob.decode()==pin['git_blob']and len(b)==pin['size']and sha(b)==pin['sha256'],'PriorGit',p);require(read(ROOT/p,16<<20)==b,'PriorWorking',p)
  require(pos==len(raw),'PriorFrame','trailing output')
 return dict(files=len(rows),all_Git_working_exact=True,head=x['head'],snapshot_sha256=sha(read(OUT/'prior-inputs.json',4<<20)),historical_preservation_bytes=sum(r['size']for r in rows.values()),batches=len(batches),batch_payload_max_bytes=16<<20,scope='historical1834 preservation audit, separate from511 semantic source authority/64MiB bound')
def main():
 started=time.monotonic();files=[*HERE.glob('*.py'),*HERE.glob('*.go.txt'),HERE/'README.md',HERE/'authority.json',HERE/'reader-inputs.json',HERE/'limits.json',HERE/'manual-locators.json'];frozen={p.name:sha(read(p,4<<20))for p in files};write('source-freeze.json',frozen)
 for p in HERE.glob('*.py'):
  s=p.read_text();ast.parse(s);require(all(line.rstrip()==line for line in s.splitlines()),'SourceWhitespace',p)
 log=io.StringIO()
 with contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):result=unittest.TextTestRunner(stream=log,verbosity=2,resultclass=Result).run(unittest.defaultTestLoader.discover(str(HERE),pattern='test_*.py'))
 (OUT/'final-tests.log').write_text(log.getvalue());result.xml.set('tests',str(result.testsRun));result.xml.set('failures',str(len(result.failures)));result.xml.set('errors',str(len(result.errors)));result.xml.set('skipped',str(len(result.skipped)));ET.indent(result.xml);ET.ElementTree(result.xml).write(OUT/'final-tests.xml',encoding='utf-8',xml_declaration=True);require(result.wasSuccessful()and not result.skipped,'PublicTests','see final-tests.log')
 commands=[]
 commands.append(command('measured-public-check',['/usr/bin/time','-f','elapsed=%e maxrss_KiB=%M',sys.executable,'-B',str(HERE/'qualify.py'),'check']))
 full=parse(read(OUT/'measured-public-check.stdout.log',4<<20));require(len(full['native_snapshots'])==64 and len(full['complete_PRN'])==32,'CorpusCardinality','64native32wholePRN')
 commands.append(command('catalog-a',[sys.executable,'-B',str(HERE/'qualify.py'),'catalog']));commands.append(command('catalog-b',[sys.executable,'-B',str(HERE/'qualify.py'),'catalog']));require(read(OUT/'catalog-a.stdout.log',4<<20)==read(OUT/'catalog-b.stdout.log',4<<20),'Determinism','actual public catalog')
 commands.append(command('configured-seven',[sys.executable,'scripts/review_checks.py','--junitxml='+str(OUT/'configured-seven.xml')],timeout=600));xml=ET.parse(OUT/'configured-seven.xml').getroot();require(xml.attrib['tests']=='7'and xml.attrib['failures']=='0'and xml.attrib['errors']=='0'and xml.attrib['skipped']=='0','ConfiguredSeven','actual7/no skips')
 commands.append(command('actual-GoFiles',['go','list','-json','./...']))
 with tempfile.TemporaryDirectory(prefix='wordling-wp56-helper-checks-')as d:
  cwd=Path(d)
  for path in bridge.inputs():
   p=cwd/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(read(ROOT/path,4<<20))
  probe=cwd/'probe';probe.mkdir();(probe/'main.go').write_bytes(read(HERE/'inspect.go.txt',1<<20));(probe/'main_test.go').write_bytes(read(HERE/'inspect_test.go.txt',1<<20));example=parse(read(OUT/'catalog-a.stdout.log',4<<20))['examples']['native']['native'];(probe/'fixture.WP5').write_bytes(read(ROOT/example,1<<20))
  commands.append(command('bridge-gofmt',['gofmt','-d','probe/main.go','probe/main_test.go'],cwd));require((OUT/'bridge-gofmt.stdout.log').stat().st_size==0,'BridgeFormat','gofmt')
  for name,args in [('build',['go','build','-o','helper','./probe']),('test',['go','test','-timeout=60s','-v','./probe']),('vet',['go','vet','./probe']),('race',['go','test','-race','-timeout=60s','-v','./probe']),('GoFiles',['go','list','-deps','-json','./probe'])]:commands.append(command('bridge-'+name,args,cwd,timeout=180))
 write('prior-source-proof.json',protect());s=Sources();write('authority-proof.json',dict(files=len(s.rows),bytes=s.total,all_Git_working_exact=True))
 require(all(sha(read(HERE/n,4<<20))==v for n,v in frozen.items()),'FrozenSource','source changed during final validation')
 shape=parse(read(ROOT/'docs/research/continuation/text-flow-contract/offline-result.json',16<<20));stack=[(shape,1)];nodes=0;depth=0
 while stack:
  v,d=stack.pop();nodes+=1;depth=max(depth,d)
  if isinstance(v,dict):stack.extend((x,d+1)for x in v.values())
  elif isinstance(v,list):stack.extend((x,d+1)for x in v)
 report=dict(tests=result.testsRun,failures=0,errors=0,skips=0,configured_checks=7,configured_skips=0,native_snapshots=64,complete_PRN=32,source_objects=len(s.rows),source_bytes=s.total,prior_files=1834,mutants=parse(read(OUT/'mutants.json',1<<20)),source_frozen=frozen,source_AST_whitespace='pass; original/raw evidence not normalized or blanket lint-clean',commands=commands,approved49_JSON_shape=dict(bytes=(ROOT/'docs/research/continuation/text-flow-contract/offline-result.json').stat().st_size,nodes=nodes,depth=depth,limits_nodes=750000,limits_depth=48),runtime_display_ready=False,new_guests=0,host_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,elapsed_seconds=time.monotonic()-started,parser600s_fuzz='not repeated: unchanged codec; public source/phase/host boundary and inert bridge tested',identity=dict(tool='codex',profile='researcher-robbie',role='researcher',model=None),M1_accepted=False)
 write('final-validation.json',report);print(json.dumps({k:report[k]for k in ['tests','configured_checks','native_snapshots','complete_PRN','source_objects','prior_files','elapsed_seconds']},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
