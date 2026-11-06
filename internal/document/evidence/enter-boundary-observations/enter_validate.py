"""Sequential frozen terminal-BLOCKED0 research validation; no original action."""
from pathlib import Path
import ast,contextlib,io,json,resource,sys,time,unittest,xml.etree.ElementTree as ET
sys.dont_write_bytecode=True
from enter_sources import B,HERE,ROOT,verify,sha
OUT=HERE/'checks'
def write(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def command(name,argv,timeout=120,limit=2<<20):
 start=time.monotonic();out,err,code=B.process(argv,ROOT,timeout=timeout,stdout_limit=limit,check=False);(OUT/(name+'.stdout.log')).write_bytes(out);(OUT/(name+'.stderr.log')).write_bytes(err);r=dict(name=name,argv=argv,cwd=str(ROOT),exit=code,seconds=time.monotonic()-start,stdout_bytes=len(out),stderr_bytes=len(err),stdout_sha256=sha(out),stderr_sha256=sha(err));B.require(code==0,'ValidationCommand',r);return r
class XMLResult(unittest.TextTestResult):
 def __init__(self,*a,**k):super().__init__(*a,**k);self.xml=ET.Element('testsuite',name='wp57-terminal-source-prerequisite')
 def startTest(self,test):super().startTest(test);self.case=ET.SubElement(self.xml,'testcase',name=str(test));self.start=time.monotonic()
 def stopTest(self,test):self.case.set('time',str(time.monotonic()-self.start));super().stopTest(test)
 def addFailure(self,test,error):super().addFailure(test,error);ET.SubElement(self.case,'failure').text=self._exc_info_to_string(error,test)
 def addError(self,test,error):super().addError(test,error);ET.SubElement(self.case,'error').text=self._exc_info_to_string(error,test)
 def addSkip(self,test,why):super().addSkip(test,why);ET.SubElement(self.case,'skipped').text=why
def historical():
 x=B.parse(B.read(OUT/'prior-inputs.json'));pins=x['files'];B.require(len(pins)==1926,'Prior1926',len(pins));batches=[];batch=[];size=0
 for p,pin in pins.items():
  if size+pin['size']>16<<20 and batch:batches.append(batch);batch=[];size=0
  batch.append((p,pin));size+=pin['size']
 if batch:batches.append(batch)
 for batch in batches:
  req=''.join(x['head']+':'+p+'\n'for p,_ in batch).encode();raw,_=B.process(['git','cat-file','--batch'],ROOT,req,stdout_limit=32<<20);pos=0
  for p,pin in batch:
   end=raw.index(b'\n',pos);blob,kind,n=raw[pos:end].split();n=int(n);pos=end+1;b=raw[pos:pos+n];pos+=n;B.require(raw[pos:pos+1]==b'\n','HistoricalGitFrame',p);pos+=1;B.require(kind==b'blob'and blob.decode()==pin['git_blob']and n==pin['size']and sha(b)==pin['sha256'],'HistoricalGitDrift',p);B.require(B.read(ROOT/p,16<<20)==b,'HistoricalWorkingDrift',p)
  B.require(pos==len(raw),'HistoricalGitFrame','end')
 expected={p for p in pins if p.endswith('.go')or p in ['go.mod','go.sum']};actual={str(p.relative_to(ROOT))for p in ROOT.rglob('*.go')if '.git'not in p.parts}|{'go.mod','go.sum'};B.require(expected==actual,'GoModuleSET','no new/default-discovered Go/module source')
 return dict(files=1926,bytes=sum(r['size']for r in pins.values()),all_Git_working_exact=True,Go_module_files=len(actual),Go_module_SET_exact=True,batches=len(batches),batch_payload_max=16<<20,scope='historical preservation, separate from45/8MiB executed safety source budget')
def main():
 started=time.monotonic();frozen={p.name:sha(B.read(p))for p in [*HERE.glob('*.py'),HERE/'README.md',HERE/'sources.json',HERE/'limits.json']};write('source-freeze.json',frozen)
 for p in HERE.glob('*.py'):
  s=p.read_text();ast.parse(s);B.require(all(line.rstrip()==line for line in s.splitlines())and s.endswith('\n')and not s.endswith('\n\n'),'SourceWhitespace',p.name)
 log=io.StringIO()
 with contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):result=unittest.TextTestRunner(stream=log,verbosity=2,resultclass=XMLResult).run(unittest.defaultTestLoader.discover(str(HERE),pattern='test_*.py'))
 (OUT/'final-tests.log').write_text(log.getvalue());result.xml.set('tests',str(result.testsRun));result.xml.set('failures',str(len(result.failures)));result.xml.set('errors',str(len(result.errors)));result.xml.set('skipped',str(len(result.skipped)));ET.indent(result.xml);ET.ElementTree(result.xml).write(OUT/'final-tests.xml',encoding='utf-8',xml_declaration=True);B.require(result.wasSuccessful()and not result.skipped,'FinalTests','actual public/component tests; see raw log')
 receipts=[]
 for name in ['preflight-a','preflight-b']:receipts.append(command(name,[sys.executable,'-B',str(HERE/'enter_oracle.py'),'preflight']))
 B.require(B.read(OUT/'preflight-a.stdout.log')==B.read(OUT/'preflight-b.stdout.log'),'Determinism','actual public preflight')
 receipts.append(command('measured-preflight',['/usr/bin/time','-f','elapsed=%e maxrss_KiB=%M',sys.executable,'-B',str(HERE/'enter_oracle.py'),'preflight']))
 receipts.append(command('native72',[sys.executable,'-B',str(HERE/'enter_oracle.py'),'native-check']))
 receipts.append(command('configured-seven',[sys.executable,'scripts/review_checks.py','--junitxml='+str(OUT/'configured-seven.xml')],timeout=240));xml=ET.parse(OUT/'configured-seven.xml').getroot();B.require(all(xml.attrib[k]==v for k,v in dict(tests='7',failures='0',errors='0',skipped='0').items()),'Configured7','actual7/no skips')
 receipts.append(command('actual-GoFiles',['go','list','-json','./...']))
 proof=historical();write('historical1926-proof.json',proof);authority=verify();B.require(all(sha(B.read(HERE/n))==h for n,h in frozen.items()),'SourceFrozen','source restored/frozen through final checks');B.require(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024<=512<<20,'RSSBudget','host validator512MiB ceiling')
 mutants=B.parse(B.read(OUT/'mutants.json'));report=dict(status='TERMINAL SourceContractPrereq BLOCKED0',tests=result.testsRun,failures=0,errors=0,skips=0,configured_checks=7,configured_skips=0,mutants=mutants,source_files=len(authority['files']),source_bytes=sum(r['size']for r in authority['files'].values()),historical_proof=proof,commands=receipts,source_freeze=frozen,new_original_tickets_spent=0,actual_original_launched=0,original_reference_guard_or_ledger_opened=False,private_master_or_failed_HD_read=False,new_Go_helper=False,Go_race='not repeated: unchanged existing probe/public source; genuine inherited7 run',parser600s_fuzz='not repeated: no native code change',pending_fixture_workers=0,host_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,elapsed_seconds=time.monotonic()-started,identity=dict(tool='codex',profile='researcher-robbie',role='researcher',model=None),full_M1_accepted=False)
 write('final-validation.json',report);print(json.dumps({k:report[k]for k in ['status','tests','configured_checks','source_files','source_bytes','actual_original_launched','elapsed_seconds']},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
