"""Actual bounded HOST CLI checks. Fixed public native roster; no VM/resources."""
from pathlib import Path
import argparse,hashlib,json,os,selectors,signal,subprocess,tempfile,time
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent

def run(binary,args,name,want=0):
 cmd=['/usr/bin/time','-v','-o',str(O/(name+'.time')),str(binary),*args]
 start=time.monotonic();p=subprocess.Popen(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);selector=selectors.DefaultSelector();buffers={};reason=None
 for stream in [p.stdout,p.stderr]:os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ);buffers[stream.fileno()]=bytearray()
 try:
  while selector.get_map():
   if time.monotonic()-start>10:reason='deadline';break
   for key,_ in selector.select(.05):
    data=os.read(key.fd,65536)
    if not data:selector.unregister(key.fileobj);continue
    if len(buffers[key.fd])+len(data)>1<<20:reason='output-limit';break
    buffers[key.fd].extend(data)
   if reason:break
  if reason:
   # The unreaped immediate child pins the owned private process-group ID.
   if os.getpgid(p.pid)!=p.pid or os.getsid(p.pid)!=p.pid:raise RuntimeError('unproved own group; no signals')
   os.killpg(p.pid,signal.SIGKILL)
  code=p.wait(timeout=2)
 finally:
  selector.close();p.stdout.close();p.stderr.close()
 out,err=map(bytes,buffers.values());(O/(name+'.stdout')).write_bytes(out);(O/(name+'.stderr')).write_bytes(err)
 row=dict(name=name,argv=cmd,exit=code,elapsed=time.monotonic()-start,stdout_bytes=len(out),stderr_bytes=len(err),fault=reason)
 if reason or code!=want:raise AssertionError(row)
 return row,out

def main():
 a=argparse.ArgumentParser();a.add_argument('--binary',type=Path,required=True);a.add_argument('--sha256',required=True);args=a.parse_args();binary=args.binary.resolve();digest=hashlib.sha256(binary.read_bytes()).hexdigest();assert digest==args.sha256;rows=[];fixtures=json.loads((O/'fixtures.json').read_text())['files']
 for x in fixtures:
  assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
 for kind,label,index,offset in [('L1-HR','[HRt]',14,692),('L2-HP','[HPg]',16,725)]:
  for rep in ['01','02']:
   path=f'docs/research/continuation/text-layout/runs/wp14-r{rep}-{kind}/BASEA.WP5';name=kind+'-'+rep;row,out=run(binary,['-input',path],name);d=json.loads(out);entries=d['elements'];assert d['same_revision']and d['true_eof']and len(entries)==d['total_tokens'];chosen=[x for x in entries if x['text']==label];assert len(chosen)==1 and chosen[0]['token_index']==index and chosen[0]['kind']==0 and chosen[0]['span']=={'Offset':offset,'Length':1};assert sum(x['unsupported']for x in entries)>=9;rows.append(row)
   row,out=run(binary,['-input',path,'-start',str(index),'-count','1'],name+'-window');v=json.loads(out);assert len(v['elements'])==1 and v['elements'][0]['text']==label and not v['true_eof'];rows.append(row)
   row,out=run(binary,['-input',path,'-start',str(d['total_tokens']),'-count','0'],name+'-eof');v=json.loads(out);assert v['true_eof']and v['elements']==[];rows.append(row)
 for kind in ['L4-ABS','L4-REL']:
  row,out=run(binary,['-input',f'docs/research/continuation/text-layout/runs/wp14-r01-{kind}/BASEA.WP5'],kind);assert all(x['text']!='[Tab]'for x in json.loads(out)['elements']);rows.append(row)
 path='docs/research/continuation/text-layout/runs/wp14-r01-L1-HR/BASEA.WP5'
 for name,extra,want in [('negative-start',['-start','-1'],1),('negative-count',['-count','-2'],1),('oversize-window',['-count','4097'],1),('unknown-flag',['-other'],2),('extra-arg',['unexpected'],2)]:
  row,out=run(binary,['-input',path,*extra],name,want);assert not out;rows.append(row)
 with tempfile.TemporaryDirectory(prefix='wp59-cli-')as temp:
  temp=Path(temp);bad=temp/'bad.wp5';bad.write_bytes(b'invalid');large=temp/'large.wp5';large.touch();os.truncate(large,(16<<20)+1);link=temp/'link.wp5';link.symlink_to(R/path);fifo=temp/'fifo.wp5';os.mkfifo(fifo)
  for name,file in [('malformed',bad),('oversize-input',large),('symlink',link),('FIFO',fifo),('directory',temp)]:
   row,out=run(binary,['-input',str(file)],name,1);assert not out;rows.append(row)
 for x in fixtures:assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
 result=dict(binary=str(binary),binary_sha256=digest,scope='HOST readonly CLI only; no UI/PTY/original qualification',cases=rows,all24_source_fixtures_unchanged=True);(O/'public-cli-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'cases':len(rows),'binary':digest,'all_passed':True}))
if __name__=='__main__':main()
