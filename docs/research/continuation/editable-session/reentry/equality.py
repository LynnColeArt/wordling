#!/usr/bin/env python3
"""Full path-set and hash comparison, not only hashes of previously named files."""
from pathlib import Path
import json,hashlib,subprocess,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent;E=HERE.parent
baseline=json.loads((E/'pty-final-02/inputs.json').read_text())['working_source_inputs']
now={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('internal/**/*.go')}
now.update({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'cmd/wordling').glob('*.go')});now.update({p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['go.mod','go.sum']})
assert set(now)==set(baseline),{'added':sorted(set(now)-set(baseline)),'removed':sorted(set(baseline)-set(now))}
for p,h in now.items():assert h==baseline[p]['sha256'],p
raw=subprocess.check_output(['go','list','-deps','-json','./cmd/wordling'],cwd=ROOT,text=True);dec=json.JSONDecoder();actual=[]
while raw.strip():
    v,n=dec.raw_decode(raw.lstrip());raw=raw.lstrip()[n:]
    if v['ImportPath'].startswith('github.com/lynncoleart/wordling/'):
        d=Path(v['Dir']);actual.append({'import':v['ImportPath'],'directory':str(d),'go_files':{p:hashlib.sha256((d/p).read_bytes()).hexdigest() for p in v['GoFiles']}})
expected=[{k:v for k,v in x.items() if k!='module'}for x in json.loads((E/'actual-build-package-inputs.json').read_text())];assert actual==expected
old=set(next(c.findtext('system-out').splitlines() for c in ET.parse(E/'validation-final.xml').findall('.//testcase') if c.attrib['name']=='go-package-discovery'))
new=set(subprocess.check_output(['go','list','./...'],cwd=ROOT,text=True).splitlines())
assert new-old=={'github.com/lynncoleart/wordling/docs/research/continuation/resaved-prefix/readerbridge'} and old-new==set()
print(json.dumps({'source_inputs_count':len(now),'source_paths_and_hashes_exact':True,'compiled_local_packages_count':len(actual),'compiled_source_paths_and_hashes_exact':True,'source_inputs':now,'compiled_packages':actual,'package_count_old':len(old),'package_count_current':len(new),'added_packages':sorted(new-old),'removed_packages':sorted(old-new)},indent=2))
