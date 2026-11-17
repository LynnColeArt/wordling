#!/usr/bin/env python3
"""Offline evidence verification; never run a benchmark, app or VM."""
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('measure',HERE/'measure.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def verify(base):
 base=Path(base).resolve();counts={}
 for run in ['run-01','run-02']:
  folder=base/run;artifacts=json.loads((folder/'artifacts.json').read_text())['files']
  for item in artifacts:
   path=ROOT/item['path'];actual=m.digest(path)
   if actual!=item:raise ValueError('Changed raw evidence '+item['path'])
  env=json.loads((folder/'environment.json').read_text())
  for item in env['source_hashes']:
   path=ROOT/item['path']
   if item['path'].startswith('tests/performance/'):
    path=base/'runner-versions'/run/(Path(item['path']).name+('.txt' if item['path'].endswith('.go') else ''))
   actual=m.digest(path)
   if actual['bytes']!=item['bytes'] or actual['sha256']!=item['sha256']:raise ValueError('Changed source '+item['path'])
  summaries=json.loads((folder/'summaries.json').read_text());fixtures=json.loads((folder/'fixtures.json').read_text())
  if len(summaries)!=12 or len(fixtures)!=12:raise ValueError('Missing declared fixture')
  for summary,fixture in zip(summaries,fixtures):
   raw=json.loads((folder/'raw'/(fixture['id']+'.json')).read_text())
   if summary['phases']!=m.summarize(raw):raise ValueError('Incorrect summary')
   actual=m.digest(ROOT/fixture['native']['path'])
   if actual!=fixture['native'] or raw['sha256']!=actual['sha256'] or raw['size']!=actual['bytes'] or not raw['source_unchanged']:raise ValueError('Fixture not preserved')
   for phase in raw['phases']:
    if phase.get('skipped'):continue
    if len(phase['samples'])!=31 or len(phase['warmup'])!=3:raise ValueError('Missing samples/warmup')
  for p in sorted((folder/'pty').glob('process-*')):
   result=json.loads((p/'result.json').read_text());native=(folder/'fixtures/plain').read_bytes()
   if result['exit_code']!=0 or not result['terminal_restored'] or not result['source_bytes_exact'] or not result['published_bytes_exact']:raise ValueError('PTY failure')
   for name in ['SOURCE','COPY']:
    if (p/'files'/name).read_bytes()!=native:raise ValueError('PTY native changed')
   wire=(p/'wire.bin').read_bytes()
   for timing in result['timings']:
    if bytes.fromhex(timing['cue_hex']) not in wire[timing['wire_offset_before']:]:raise ValueError('Missing protocol output cue')
   if run=='run-02' and result['application_peak_rss_kib_gnu_time']<=0:raise ValueError('Missing peak measurement')
  counts[run]={'artifacts':len(artifacts),'fixtures':len(fixtures),'pty_processes':len(list((folder/'pty').glob('process-*')))}
 # Validate WP14 fixture against the immutable original manifest, not a new hash.
 original=ROOT/'docs/research/continuation/text-layout/runs/wp14-r01-L1-WRAP-L3-LR'
 witness=next(x for x in json.loads((original/'run.json').read_text())['evidence'] if x['path']=='BASEA.WP5')
 actual=m.digest(original/'BASEA.WP5')
 if actual['bytes']!=witness['bytes'] or actual['sha256']!=witness['sha256']:raise ValueError('WP14 original witness changed')
 return {'passed':True,'runs':counts,'all_raw_samples_retained':True,'source_and_native_bytes_verified':True,'physical_delivery':'unqualified','original_timing_comparison':'not measured; WP14 capture settling/input sleeps are not response-time samples'}

if __name__=='__main__':print(json.dumps(verify(sys.argv[1]),indent=2))
