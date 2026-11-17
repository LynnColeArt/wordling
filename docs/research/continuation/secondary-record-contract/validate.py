"""Finite owned WP53 source/check/helper evidence runner; NO guest operations."""
from pathlib import Path
import hashlib, importlib.util, json, os, subprocess, sys, tempfile, time
ROOT=Path(__file__).resolve().parents[4]; O=Path(__file__).resolve().parent; E=O/'evidence'
sp=importlib.util.spec_from_file_location('checker',ROOT/'scripts/reference/secondary_record_contract.py');C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)

def run(name,args,timeout=240,env=None):
 start=time.monotonic();p=subprocess.run(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout,env=env)
 (E/(name+'.log')).write_bytes(p.stdout);row={'argv':args,'cwd':str(ROOT),'exit':p.returncode,'seconds':time.monotonic()-start,'log_sha256':C.digest(p.stdout)}
 if p.returncode:raise RuntimeError(row)
 return row

def main():
 commands=[]
 env=dict(os.environ,WP53_TEST_RECEIPT=str(E/'negative-cases-final.json'))
 commands.append(run('tests-frozen',[sys.executable,str(O/'test_runner.py')],env=env))
 commands.append(run('configured',[sys.executable,'scripts/review_checks.py','--junitxml='+str(E/'configured.xml')],timeout=300))
 commands.append(run('inherited-race',['go','test','-race','-timeout=90s','./...'],timeout=180))
 with C.Session(ROOT) as s:
  for args in [['gofmt','-l','internal/secondary-contract/main.go','internal/secondary-contract/main_test.go'],['go','build','./...'],['go','test','-count=1','./...'],['go','vet','./...'],['go','test','-race','-count=1','./...']]:
   out=s.run(args);(E/('helper-check-'+str(len(s.receipt['commands']))+'.log')).write_bytes(out)
   if args[0]=='gofmt':C.require(out==b'','Gofmt')
  s.build_proof();(E/'helper-validation.json').write_text(json.dumps(s.receipt,indent=2)+'\n')
 for n,flag in [('audit-write-1',[]),('audit-write-2',[]),('audit-check',['--check'])]:
  args=[sys.executable,'scripts/reference/secondary_record_contract.py','audit','--output',str(E/'original-audit.json'),*flag]
  if n=='audit-write-2':args+=['--receipt',str(E/'composition.json'),'--junitxml',str(E/'originals.xml')]
  commands.append(run(n,args))
 commands.append(run('diff-check',['git','diff','--check']))
 (E/'validation.json').write_text(json.dumps({'commands':commands,'no_long_fuzz_or_original':True},indent=2)+'\n')
 print(json.dumps({'completed':len(commands),'all_exit_zero':True}))
if __name__=='__main__':main()
