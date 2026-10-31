"""Finite WP54 validation and truthful raw command/exit custody; no lifecycle or guest."""
from pathlib import Path
import ast,hashlib,json,os,resource,subprocess,sys,time,unittest,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];CHECKS=HERE/'checks'
class JUnit(unittest.TextTestResult):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.cases=[]
 def startTest(self,test):self.started=time.monotonic();super().startTest(test)
 def stopTest(self,test):self.cases.append((test.id(),time.monotonic()-self.started));super().stopTest(test)
def command(name,argv,timeout=60):
 started=time.monotonic();p=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=timeout);(CHECKS/(name+'.stdout.log')).write_bytes(p.stdout);(CHECKS/(name+'.stderr.log')).write_bytes(p.stderr)
 row=dict(name=name,argv=list(map(str,argv)),cwd=str(ROOT),returncode=p.returncode,seconds=time.monotonic()-started,stdout_bytes=len(p.stdout),stderr_bytes=len(p.stderr));rows.append(row)
 if p.returncode:raise RuntimeError('failed actual command '+name+' exit '+str(p.returncode))
 return p
rows=[]
def main():
 CHECKS.mkdir(exist_ok=True)
 # Source-only checks deliberately exclude raw logs/screens, whose whitespace must remain exact.
 files=sorted(HERE.glob('*.py'));source=[]
 for p in files:
  raw=p.read_bytes();tree=ast.parse(raw,filename=str(p));compile(tree,str(p),'exec');assert not any(line.endswith((b' ',b'\t'))for line in raw.split(b'\n')),(p,'source trailing whitespace');assert raw.endswith(b'\n'),p
  source.append(dict(path=str(p.relative_to(ROOT)),size=len(raw),sha256=hashlib.sha256(raw).hexdigest(),AST_compile=True,source_whitespace=True))
 (CHECKS/'source-checks.json').write_text(json.dumps(dict(files=source,raw_logs_excluded_from_whitespace_checks=True,no_Go_source_or_module_changed=True),indent=2)+'\n')
 command('source-reproducible',[sys.executable,str(HERE/'source_builder.py'),'--check'])
 sys.path.insert(0,str(HERE));suite=unittest.defaultTestLoader.discover(str(HERE),pattern='test_*.py')
 with (CHECKS/'final-tests.log').open('w')as stream:result=unittest.TextTestRunner(stream=stream,resultclass=JUnit,verbosity=2).run(suite)
 root=ET.Element('testsuite',name='WP54-public-offline-contract',tests=str(result.testsRun),failures=str(len(result.failures)),errors=str(len(result.errors)),skipped=str(len(result.skipped)));failed={t.id():s for t,s in result.failures+result.errors};skipped={t.id():s for t,s in result.skipped}
 for name,duration in result.cases:
  case=ET.SubElement(root,'testcase',name=name,time=f'{duration:.6f}')
  if name in failed:ET.SubElement(case,'failure').text=failed[name]
  if name in skipped:ET.SubElement(case,'skipped').text=skipped[name]
 ET.indent(root);ET.ElementTree(root).write(CHECKS/'offline.xml',encoding='utf-8',xml_declaration=True)
 if not result.wasSuccessful():raise RuntimeError('actual public/IO contract tests failed')
 a=command('actual-check',[sys.executable,str(HERE/'oracle.py'),'check','--output',str(CHECKS/'actual-source-report.json')])
 b=command('determinism-check',[sys.executable,str(HERE/'oracle.py'),'check']);assert a.stdout==b.stdout,'nondeterministic report'
 command('blocked-plan',[sys.executable,str(HERE/'oracle.py'),'plan','--output',str(CHECKS/'blocked-plan.json')])
 # Mandatory configured seven checks, once; honors real package discovery/skips.
 command('configured-seven',[sys.executable,'scripts/review_checks.py','--junitxml',str(CHECKS/'configured-seven.xml')],timeout=900)
 data=json.loads(a.stdout);assert data['source_audit']['verified_unique_objects']==1347 and data['source_audit']['inventory_screens']==1085
 (CHECKS/'resources.json').write_text(json.dumps(dict(actual_source_report_bytes=len(a.stdout),git_objects=1347,actual_verified_source_bytes=data['source_audit']['verified_bytes'],maximum_children_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,source_bound_native_probe='not needed/not executed',Go_race='not run: no affected Go boundary or added Go code',bounded_runtime_contract=dict(source_bytes=40*1024*1024,git_stdout_bytes=48*1024*1024,git_stderr_bytes=1024*1024,git_timeout_seconds=30,packet_bytes=32768,packet_depth=32,packet_nodes=4096,frame_text_bytes=8192,VGA_bytes=4000,cursor_JSON_bytes=8192,report_bytes=2*1024*1024),determinism_exact=True),indent=2)+'\n')
 # Actual imported project/helper files, no snapshot-module execution or production overlay.
 import oracle
 _,decoder,_=oracle.context()
 modules=[]
 for name,m in sorted(sys.modules.items()):
  file=getattr(m,'__file__',None)
  if file:
   p=Path(file)
   if p.is_file()and (HERE in p.parents or p==ROOT/'scripts/reference/qmp.py'):modules.append(dict(module=name,path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 # QMP is imported with spec loader and may not register in sys.modules; record actual API pin explicitly.
 (CHECKS/'execution-closure.json').write_text(json.dumps(dict(python=sys.version,executable=sys.executable,project_modules=modules,actual_helper=decoder.provenance(),archived_code_imported=False,Go_or_native_binary_built=False,real_QMP_enter_or_guest_connection=False),indent=2)+'\n')
 print('PASS actual public tests, source custody, determinism, configured seven; Stage2 remains BLOCKED')
if __name__=='__main__':
 try:main()
 finally:(CHECKS/'commands.json').write_text(json.dumps(rows,indent=2)+'\n')
