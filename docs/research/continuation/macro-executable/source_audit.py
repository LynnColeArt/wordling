"""Read-only compiled-source/corpus audit, no product validator or lifecycle action."""
import hashlib,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[4]
OUT=pathlib.Path(__file__).parent/'evidence'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 baseline=json.loads((OUT/'approved-composition.json').read_text());checked=[]
 for row in baseline['records']:
  path=row['path']
  if path.startswith(('internal/tui/','cmd/wordling/')):continue
  raw=(ROOT/path).read_bytes();assert sha(raw)==row['sha256'],path
  original=subprocess.check_output(['git','show',row['approved_source']+':'+path],cwd=ROOT)
  assert raw==original,path
  checked.append(row)
 # Also compare sets, so an extra dependency Go file is not hidden by byte-only proof.
 for prefix,pin in baseline['source_pins'].items():
  if prefix=='internal/tui':continue
  expected=set(subprocess.check_output(['git','ls-tree','-r','--name-only',pin,'--',prefix],cwd=ROOT,text=True).splitlines())
  expected={x for x in expected if x.endswith('.go')}
  actual={str(p.relative_to(ROOT)) for p in (ROOT/prefix).rglob('*.go')}
  assert expected==actual,(prefix,expected^actual)
 raw=subprocess.check_output(['go','list','-json','./...'],cwd=ROOT,text=True);decoder=json.JSONDecoder();packages=[]
 while raw.strip():
  obj,n=decoder.raw_decode(raw.lstrip());raw=raw.lstrip()[n:];packages.append(obj)
 files={}
 for obj in packages:
  for key in ['GoFiles','CgoFiles','TestGoFiles','XTestGoFiles','EmbedFiles','TestEmbedFiles','XTestEmbedFiles']:
   for name in obj.get(key,[]):
    p=pathlib.Path(obj['Dir'])/name;rel=str(p.relative_to(ROOT));files[rel]={'sha256':sha(p.read_bytes()),'size':p.stat().st_size,'role':key}
 for name in ['go.mod','go.sum']:files[name]={'sha256':sha((ROOT/name).read_bytes())}
 pre=json.loads((ROOT/'docs/research/continuation/macro-executable/runs/final01/prelaunch.json').read_text())
 test_changes=[]
 for path,row in pre['source_inputs'].items():
  if sha((ROOT/path).read_bytes())!=row['sha256']:
   assert path=='internal/tui/macro_lifetime_test.go',path
   test_changes.append(path)
 records={'head_at_audit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'unchanged_dependency_records':checked,'packages':[{'ImportPath':x['ImportPath'],'GoFiles':x.get('GoFiles',[]),'TestGoFiles':x.get('TestGoFiles',[]),'XTestGoFiles':x.get('XTestGoFiles',[])} for x in packages],'compiled_inputs':files,'PTY_binary':pre['binary'],'PTY_product_inputs_unchanged':True,'PTY_later_test_only_changes':test_changes,'no_dependency_tip_refresh':True}
 (OUT/'final-source-closure.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps({'dependency_files_exact':len(checked),'packages':len(packages),'compiled_inputs_including_tests_modules':len(files),'PTY_product_inputs_unchanged':True,'later_test_only_changes':test_changes}))
if __name__=='__main__':main()
