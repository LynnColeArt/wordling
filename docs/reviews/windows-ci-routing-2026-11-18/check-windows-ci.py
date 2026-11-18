import json, os, pathlib, subprocess, tempfile, types, yaml
root=pathlib.Path('/home/lynn/projects/wordling')
w=yaml.load((root/'.github/workflows/native-prerelease.yml').read_text(),Loader=yaml.BaseLoader)
assert w['on'].get('push',{}).get('branches')==['validation/windows-native'],'exact Windows validation push trigger missing'
i=w['on']['workflow_dispatch']['inputs']['platform'];assert i['type']=='choice' and i['default']=='all' and i['options']==['all','windows']
assert 'pull_request' in w['on']
body=next(s['run'] for s in w['jobs']['build']['steps'] if s.get('name')=='Build normal binaries and fixture-free native smoke tests')
subprocess.run(['bash','-n'],input=body,text=True,check=True)
class Missing(types.SimpleNamespace):
 def __getattr__(self,k):return ''
def expression(s,event,ref,platform):
 s=s.removeprefix('${{').removesuffix('}}').strip().replace('&&',' and ').replace('||',' or ')
 return eval(s,{'__builtins__':{},'fromJSON':json.loads,'github':Missing(event_name=event,ref=ref),'inputs':Missing(platform=platform)})
all_targets=['linux/amd64','windows/amd64','windows/arm64','darwin/amd64','darwin/arm64']
cases=[('pull_request','refs/pull/42/merge','','all'),('workflow_dispatch','refs/heads/feat/wp51-parity','all','all'),('workflow_dispatch','refs/heads/feat/wp51-parity','','all'),('workflow_dispatch','refs/heads/feat/wp51-parity','windows','windows'),('push','refs/heads/validation/windows-native','','windows'),('push','refs/heads/elsewhere','','untriggered')]
for event,ref,platform,expected in cases:
 if expected=='untriggered':assert ref.removeprefix('refs/heads/') not in w['on']['push']['branches'];print('PASS unrelated push does not trigger');continue
 windows=expression(w['env']['WINDOWS_ONLY'],event,ref,platform)
 runners=expression(w['jobs']['native']['strategy']['matrix']['os'],event,ref,platform)
 assert windows==(expected=='windows');assert runners==(['windows-latest'] if windows else ['windows-latest','macos-latest'])
 with tempfile.TemporaryDirectory(prefix='wordling-workflow-check-') as tmp:
  p=pathlib.Path(tmp);log=p/'calls.jsonl'
  (p/'python3').write_text('#!/usr/bin/python3\nimport json,os,sys\nwith open(os.environ["ARGV_LOG"],"a") as f:f.write(json.dumps(sys.argv[1:])+"\\n")\n');(p/'python3').chmod(0o755)
  (p/'cp').write_text('#!/bin/sh\nexit 0\n');(p/'cp').chmod(0o755)
  subprocess.run(['bash','-e','-o','pipefail','-c',body],cwd=p,env=dict(os.environ,PATH=tmp+':'+os.environ['PATH'],WINDOWS_ONLY=str(windows).lower(),ARGV_LOG=str(log)),check=True)
  calls=[json.loads(x) for x in log.read_text().splitlines()];args=calls[0]
  assert args[:3]==['scripts/build-prerelease.py','--output','bin/prerelease']
  targets=[args[n+1] for n,a in enumerate(args) if a=='--target'];assert targets==(all_targets[:3] if windows else all_targets),targets
  assert calls[1]==['bin/prerelease/verify-native.py','bin/prerelease']
 print('PASS',event,ref,platform or '<default>',targets,runners)
assert w['permissions']=={'contents':'read'}
assert w['jobs']['build']['steps'][2]['run']=='go test -count=1 ./...\ngo vet ./...\ngo test -race -count=1 ./internal/storage ./internal/tui\n'
print('PASS Linux regression and read-only token permissions preserved')
