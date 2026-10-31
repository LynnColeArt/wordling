#!/usr/bin/env python3
"""Reproducible Linux-only measurement of approved bounded application code.

Run from repo root: python3 tests/performance/measure.py NEW_OUTPUT_DIRECTORY
No VM, cache dropping, host tuning, native writer or production modification.
"""
import errno
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import pty
import select
import shutil
import signal
import struct
import subprocess
import sys
import tempfile
import termios
import time

ROOT=Path(__file__).resolve().parents[2]
SAMPLES=31
WARMUP=3
PTY_RUNS=12
CPU=max(os.sched_getaffinity(0))
ENV=dict(os.environ,GOMAXPROCS='1',TERM='xterm-256color',LANG='C.UTF-8')

def digest(path):
 raw=Path(path).read_bytes();return {'path':str(Path(path).relative_to(ROOT)) if Path(path).is_relative_to(ROOT) else str(path),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def write(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n')
def command(args,**kw):return subprocess.check_output(args,cwd=ROOT,text=True,**kw)
def pin():os.sched_setaffinity(0,{CPU})
def quantiles(values):
 if not values or any(not isinstance(x,(int,float)) or not math.isfinite(x) or x<0 for x in values):raise ValueError('nonempty nonnegative finite samples required')
 ordered=sorted(values)
 return {'count':len(values),'min':min(values),'max':max(values),**{'p'+str(q):ordered[max(0,math.ceil(len(ordered)*q/100)-1)] for q in [50,95,99]}}
def ratio(a,b):
 for key in ['name','unit','status','boundary']:
  if a[key]!=b[key]:raise ValueError('incomparable measurement: '+key)
 if a['status']!='accepted':raise ValueError('refusals cannot establish successful scaling')
 return b['ns']['p50']/a['ns']['p50']
def summarize(data):
 rows=[]
 for phase in data['phases']:
  if phase.get('skipped'):rows.append({'name':phase['name'],'skipped':phase['skipped']});continue
  groups={}
  for sample in phase['samples']:groups.setdefault(sample.get('error',''),[]).append(sample)
  for error,samples in groups.items():
   rows.append({'name':phase['name'],'unit':'ns','boundary':phase['name'],'status':'refused' if error else 'accepted','error':error,'ns':quantiles([s['ns'] for s in samples]),'alloc_bytes':quantiles([s['alloc_bytes'] for s in samples]),'allocs':quantiles([s['allocs'] for s in samples]),'warmup_retained':len(phase['warmup'])})
 return rows

def status(pid):
 raw=Path('/proc/'+str(pid)+'/status').read_text()
 return {line.split(':')[0]:line.split(':',1)[1].strip() for line in raw.splitlines() if line.startswith(('VmRSS:','VmHWM:','Cpus_allowed_list:','Threads:'))}

def pty_run(binary,folder,fixture,index):
 folder.mkdir();work=folder/'files';work.mkdir();native=fixture.read_bytes();(work/'SOURCE').write_bytes(native)
 master,slave=pty.openpty();fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',25,100,0,0));before=termios.tcgetattr(slave)
 argv=[str(binary),'-root',str(work.resolve()),'-profile','local-flat'];wire=bytearray();timings=[];injected=[];rss={}
 started=time.perf_counter_ns();proc=subprocess.Popen(argv,stdin=slave,stdout=slave,stderr=subprocess.PIPE,env=ENV,preexec_fn=pin)
 def until(cue,start,label,offset=0):
  deadline=time.monotonic()+10
  while cue not in wire[offset:]:
   if time.monotonic()>deadline:raise TimeoutError(label+' output deadline')
   if select.select([master],[],[],.05)[0]:
    try:part=os.read(master,65536)
    except OSError as e:
     if e.errno==errno.EIO:raise RuntimeError('PTY closed before '+label)
     raise
    if not part:raise RuntimeError('PTY EOF before '+label)
    wire.extend(part)
  elapsed=time.perf_counter_ns()-start;timings.append({'name':label,'ns':elapsed,'cue_hex':cue.hex(),'wire_offset_before':offset})
 def send(raw,cue,label):
  offset=len(wire);start=time.perf_counter_ns();os.write(master,raw);injected.append({'label':label,'hex':raw.hex()});until(cue,start,label,offset)
 try:
  until(b'UNQUALIFIED',started,'process_spawn_to_first_view_bytes')
  rss['blank']=status(proc.pid)
  os.write(master,b'\x1b[?31u');injected.append({'label':'synthetic keyboard enhancement response, no physical proof','hex':'1b5b3f333175'})
  send(b'\x1b[21;2~',b'Document to be retrieved:','protocol_shift_f10_to_prompt_bytes')
  send(b'SOURCE',b'SOURCE','protocol_filename_to_echo_bytes')
  send(b'\r',b'Editing | SOURCE','protocol_enter_to_retrieved_view_bytes')
  rss['loaded']=status(proc.pid)
  send(b'\x1b[13;3~',b'Press Reveal Codes','protocol_alt_f3_to_reveal_bytes')
  send(b'\x1b[21~',b'Document to be saved:','protocol_f10_to_save_prompt_bytes')
  send(b'COPY',b'COPY','protocol_newname_to_echo_bytes')
  send(b'\r',b'NewNamePublished','protocol_enter_to_publication_view_bytes')
  assert (work/'COPY').read_bytes()==native
  rss['published']=status(proc.pid)
  send(b'\x1b[18~',b'Save document?','protocol_f7_to_prompt_bytes')
  send(b'n',b'Exit WP?','protocol_no_to_exit_prompt_bytes')
  os.write(master,b'y');injected.append({'label':'Yes final exit','hex':'79'})
  deadline=time.monotonic()+10
  while True:
   pid,waitstatus,usage=os.wait4(proc.pid,os.WNOHANG)
   if pid:proc.returncode=os.waitstatus_to_exitcode(waitstatus);break
   if time.monotonic()>deadline:raise TimeoutError('process exit')
   time.sleep(.001)
  assert proc.returncode==0,proc.stderr.read()
  assert termios.tcgetattr(slave)==before
  assert (work/'SOURCE').read_bytes()==native
  assert not list(work.glob('.wordling-candidate-*'))
  result={'index':index,'cache_label':'first_observed_process' if index==0 else 'OS_warm_process_not_cold_cache','argv':argv,'timings':timings,'rss':rss,'process_peak_rss_kib_wait4':usage.ru_maxrss,'exit_code':proc.returncode,'source_bytes_exact':True,'published_bytes_exact':True,'terminal_restored':True,'injected':injected}
  write(folder/'result.json',result);(folder/'wire.bin').write_bytes(wire);return result
 finally:
  if proc.returncode is None:
   proc.kill();proc.wait()
  os.close(master);os.close(slave)

def run(output):
 output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
 plan={'samples':SAMPLES,'warmup_separately_retained':WARMUP,'pty_fresh_processes':PTY_RUNS,'clock':'Go time.Now/time.Since monotonic; Python perf_counter_ns monotonic','quantiles':'nearest-rank, all retained values including outliers; accepted/refused distributions separated','profile':'operator-selected local-flat absolute temp directory, actual local filesystem metadata below','sizes_bytes':[4096,65536,1048576,16777216,16777217],'scaling_recipe':'original plain prefix through body offset324, replace body with ASCII x to exact total size; synthetic outer-framing only, no original capacity assertion','cpu_affinity':[CPU],'GOMAXPROCS':'1','host_context':'WP23 QEMU original suite and other coding/tests may run concurrently; no idle/quiet/isolated host claim','boundaries':{'native_parse':'wp51.Parse(memory), includes copy/outer framing; not editor latency','rooted_read_native_parse':'Directory.Read SOURCE warm local page cache; includes filesystem+copy+native parser','document_construction':'document.Parse(memory), including native parse and token/gap indexing; refusal retained','all_token_traversal':'Token for each accepted token, including raw token copies and sum invariant','no_edit_export':'Document.Export fresh exact copy; byte equality checked outside timer','runtime_open_close':'tui.Open actual local directory and blank Session, then Runtime.Close','composition_open_retrieve_close':'fresh Runtime, model protocol events+actual read Cmd/completion+Close, not startup executable','reducer_reveal_event':'actual loaded Session.Reduce Reveal, no IO intent','model_update_reveal':'actual Model.Update AltF3, no View','model_view_100x25':'actual Model.View after100x25 resize; content creation+clipping, no terminal delivery','composition_newname_publication':'actual F10/text/Enter, Observe+Save Cmd completions, including native file publication; exact bytes audited outside timer','PTY':'actual cmd/wordling process; synthetic PTY byte write start to observed cue bytes at master fd; includes runtime/parser/frame scheduler/OS+Python select overhead, excludes physical keys/display paint'},'memory':'per-fixture Go child proc VmRSS before/after forced GC is harness resident footprint (multiple retained layers), ru_maxrss whole-child highwater includes setup and measurement; actual app separate PTY blank/loaded/published VmRSS and wait4 peak. Alloc deltas runtime.MemStats around callback, not peak heap/RSS. No forced GC inside timed callback. Warmups raw. Input acquisition/setup outside per-phase timers.','cache':'first process labelled first observed, later OS-warm; no drop_caches, no true cold-cache claim; build before measurements warms filesystem','build_variants':[['go','build','-o','BINARY','./cmd/wordling'],['go','build','-ldflags=-s -w','-o','BINARY','./cmd/wordling']],'thresholds':'none accepted; proposals after observation only'}
 write(output/'design.json',plan)
 env={'started_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'uname':platform.uname()._asdict(),'cpuinfo':Path('/proc/cpuinfo').read_text(),'meminfo':Path('/proc/meminfo').read_text(),'loadavg_before':Path('/proc/loadavg').read_text(),'affinity_parent':sorted(os.sched_getaffinity(0)),'affinity_children':[CPU],'go_version':command(['go','version']),'go_env':json.loads(command(['go','env','-json'])),'modules':command(['go','list','-m','all']),'git_head':command(['git','rev-parse','HEAD']).strip(),'git_status':command(['git','status','--short']),'mount':command(['findmnt','-T',str(output),'-J']),'python':sys.version,'tty':'synthetic Linux PTY100x25, xterm-256color/C.UTF-8, injected capability response','concurrent_context':plan['host_context'],'source_hashes':[]}
 for path in sorted(set(command(['git','ls-files','internal','cmd','go.mod','go.sum']).splitlines()+[str(p.relative_to(ROOT)) for p in (ROOT/'tests/performance').glob('*') if p.is_file()])):env['source_hashes'].append(digest(ROOT/path))
 for rev in ['72369db','d491d95']:
  check=subprocess.run(['git','merge-base','--is-ancestor',rev,'HEAD'],cwd=ROOT,capture_output=True);env.setdefault('dependency_ancestry',[]).append({'revision':rev,'exit_code':check.returncode});assert check.returncode==0, 'Dependency revision absent: '+rev
 write(output/'environment.json',env)
 with tempfile.TemporaryDirectory(prefix='wp19-build-') as temp:
  temp=Path(temp);build=[]
  for name,flags,target in [('default',[],'./cmd/wordling'),('stripped',['-ldflags=-s -w'],'./cmd/wordling'),('measure',[],'./tests/performance')]:
   binary=temp/name;argv=['go','build',*flags,'-o',str(binary),target];t=time.perf_counter_ns();subprocess.run(argv,cwd=ROOT,env=ENV,check=True);elapsed=time.perf_counter_ns()-t
   build.append({'name':name,'argv':argv,'build_ns':elapsed,'binary':digest(binary),'build_info':command(['go','version','-m',str(binary)]),'file':command(['file',str(binary)]),'size':command(['size',str(binary)])})
  write(output/'builds.json',build)
  (output/'fixtures').mkdir();fixtures=[]
  ledger=json.loads((ROOT/'kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json').read_text())
  for item in ledger['fixtures']:
   source=ROOT/item['path'];assert digest(source)['sha256']==item['sha256'];assert source.stat().st_size==item['size_bytes'];target=output/'fixtures'/item['id'];shutil.copyfile(source,target);fixtures.append({'id':item['id'],'origin':'approved-original-native-fixtures','source':item['path'],'native':digest(target)})
  text=ROOT/'docs/research/continuation/text-layout/runs/wp14-r01-L1-WRAP-L3-LR/BASEA.WP5'
  if not text.is_file():raise FileNotFoundError('Exact selected WP14 fixture missing: '+str(text))
  target=output/'fixtures'/'wp14-text';shutil.copyfile(text,target);fixtures.append({'id':'wp14-text','origin':'approved-WP14-text-original','source':str(text.relative_to(ROOT)),'native':digest(target)})
  plain=(output/'fixtures/plain').read_bytes();offset=int.from_bytes(plain[4:8],'little')
  for size in plan['sizes_bytes']:
   target=output/'fixtures'/('synthetic-'+str(size));target.write_bytes(plain[:offset]+b'x'*(size-offset));fixtures.append({'id':target.name,'origin':'synthetic-ASCII-scaling-not-original-capacity','recipe':plan['scaling_recipe'],'native':digest(target)})
  write(output/'fixtures.json',fixtures);(output/'raw').mkdir();summaries=[]
  for item in fixtures:
   target=output/'raw'/(item['id']+'.json');argv=[str(temp/'measure'),'-fixture',str(ROOT/item['native']['path']),'-samples',str(SAMPLES),'-warmup',str(WARMUP),'-output',str(target)];subprocess.run(argv,cwd=ROOT,env=ENV,preexec_fn=pin,check=True)
   raw=json.loads(target.read_text());assert raw['source_unchanged'];summaries.append({'fixture':item['id'],'size':raw['size'],'sha256':raw['sha256'],'phases':summarize(raw),'rss':raw['rss'],'peak_rss_kib':raw['process_peak_rss_kib']});print(item['id'],'measured',flush=True)
  write(output/'summaries.json',summaries)
  (output/'pty').mkdir();pty_results=[pty_run(temp/'default',output/'pty'/('process-'+str(i)),output/'fixtures/plain',i) for i in range(PTY_RUNS)]
  groups={}
  for r in pty_results[1:]:
   for t in r['timings']:groups.setdefault(t['name'],[]).append(t['ns'])
  write(output/'pty-summary.json',{'first_process':pty_results[0]['timings'],'OS_warm_11_processes':{name:quantiles(values) for name,values in groups.items()},'limits':'synthetic fd-byte observation only, no physical input-to-photon or historical/original timing comparison'})
 env['finished_at']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());env['loadavg_after']=Path('/proc/loadavg').read_text();write(output/'environment.json',env)
 files=[digest(p) for p in sorted(output.rglob('*')) if p.is_file()];write(output/'artifacts.json',{'files':files});print('measurement complete',flush=True)

if __name__=='__main__':run(sys.argv[1])
