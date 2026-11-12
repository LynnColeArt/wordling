import json,hashlib,subprocess,math
from pathlib import Path
root=Path.cwd();base=root/'docs/research/continuation/linux-measurements'
def q(values):
 values=sorted(values);n=len(values);assert n>0 and all(math.isfinite(x) and x>=0 for x in values)
 return dict(count=n,min=values[0],max=values[-1],**{'p'+str(p):values[(n*p+99)//100-1] for p in [50,95,99]})
counts={};total=0
for run in ['run-01','run-02']:
 summaries=json.loads((base/run/'summaries.json').read_text());allrows=[]
 assert len(summaries)==12
 for summary in summaries:
  raw=json.loads((base/run/'raw'/(summary['fixture']+'.json')).read_text());expected=[]
  for phase in raw['phases']:
   if phase.get('skipped'):expected.append({'name':phase['name'],'skipped':phase['skipped']});continue
   assert len(phase['samples'])==31 and len(phase['warmup'])==3
   total+=34
   errors=list(dict.fromkeys(x.get('error','') for x in phase['samples']))
   for error in errors:
    samples=[x for x in phase['samples'] if x.get('error','')==error]
    row=dict(name=phase['name'],unit='ns',boundary=phase['name'],status='refused' if error else 'accepted',error=error,ns=q([x['ns'] for x in samples]),alloc_bytes=q([x['alloc_bytes'] for x in samples]),allocs=q([x['allocs'] for x in samples]),warmup_retained=3)
    expected.append(row)
  assert summary['phases']==expected,summary['fixture']
  assert raw['publications'] in [0,34]
  assert raw['completed_receipts']==(69 if raw['publications'] else 1)
  allrows+=expected
 files=sorted((base/run/'pty').glob('process-*'));assert len(files)==12
 values={}
 for i in range(12):
  folder=base/run/'pty'/('process-'+str(i));r=json.loads((folder/'result.json').read_text());wire=(folder/'wire.bin').read_bytes()
  assert r['index']==i and r['timings'][0]['cue_hex']==b'UNQUALIFIED'.hex()
  assert len(r['timings'])==10
  previous=-1
  for row in r['timings']:
   assert row['wire_offset_before']>=previous and bytes.fromhex(row['cue_hex']) in wire[row['wire_offset_before']:]
   previous=row['wire_offset_before']
   if i:values.setdefault(row['name'],[]).append(row['ns'])
  if run=='run-02':assert int((folder/'gnu-time-peak-kib.txt').read_text())==r['application_peak_rss_kib_gnu_time']
 assert json.loads((base/run/'pty-summary.json').read_text())['OS_warm_11_processes']=={k:q(v) for k,v in values.items()}
 counts[run]={'phase_rows_including_skips':len(allrows),'timed_phase_distributions':sum('ns' in row for row in allrows),'pty_processes':12}
summary={x['fixture']:x for x in json.loads((base/'run-02/summaries.json').read_text())}
for p in json.loads((base/'scaling-curves.json').read_text())['points']:
 row=next(r for r in summary[p['fixture']]['phases'] if r['name']==p['phase'] and r.get('status')==p['status'])
 for percentile in ['p50','p95','p99']:assert p[percentile+'_ns']==row['ns'][percentile]
 assert p['bytes']==summary[p['fixture']]['size'] and p['allocation_p50_bytes']==row['alloc_bytes']['p50']
for p in json.loads((base/'scaling-ratios.json').read_text())['comparisons']:
 a=next(r for r in summary['synthetic-'+str(p['from_bytes'])]['phases'] if r['name']==p['phase'] and r.get('status')=='accepted')
 b=next(r for r in summary['synthetic-'+str(p['to_bytes'])]['phases'] if r['name']==p['phase'] and r.get('status')=='accepted')
 assert p['median_time_ratio']==b['ns']['p50']/a['ns']['p50'] and p['input_ratio']==p['to_bytes']/p['from_bytes']
proof=json.loads((base/'git-blob-proof.json').read_text());assert proof['blob_count']==len(proof['blobs'])==187
for f in proof['blobs']:
 raw=subprocess.check_output(['git','cat-file','blob',f['git_blob']]);current=subprocess.check_output(['git','show','HEAD:'+f['path']]);assert raw==current==(root/f['path']).read_bytes();assert len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256']
for f in json.loads((base/'boundary-notes.json').read_text())['pinned_module_sources']:
 raw=Path(f['path']).read_bytes();assert len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256']
print(json.dumps({'independent_recomputation':'PASS','samples_including_warmups':total,'runs':counts,'git_blobs':187,'curves_ratios_pty_peaks_module_boundaries':'PASS'},indent=2))
