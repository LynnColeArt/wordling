import json,struct,re,hashlib,subprocess
from pathlib import Path
from collections import Counter
ROOT=Path.cwd();HERE=ROOT/'docs/research/continuation/text-layout';analysis=json.loads((HERE/'analysis.json').read_text())
widths=(4,9,11,3,3,5,6,7,4,5,6,6,8,10,10,12)
def frames(data):
 p=struct.unpack_from('<I',data,4)[0];out=[]
 while p<len(data):
  lead=data[p];n=1 if lead<192 else widths[lead-192] if lead<208 else struct.unpack_from('<H',data,p+2)[0]+4
  chunk=data[p:p+n];assert len(chunk)==n
  if n>1:assert chunk[-1]==lead
  out.append((p,chunk));p+=n
 assert p==len(data)
 return out
facts=[];resources=0;states=0;native=0;streams=0;rawvga=0
for pair in analysis['repeated_variants']:
 for rid in pair['run_ids']:
  path=HERE/'runs'/rid;r=json.loads((path/'run.json').read_text());assert r['clean_original_exit']
  # Decode every captured VGA buffer independently of screen.txt, preserving
  # 25 rows with the capture's CP437 rstrip policy.
  for vram in path.glob('*/vram.bin'):
   data=vram.read_bytes();assert len(data)==4000
   text='\n'.join(data[row*160:row*160+160:2].decode('cp437').rstrip() for row in range(25))+'\n'
   assert text==(vram.with_name('screen.txt')).read_text(),vram
   rawvga+=1
  cue={'settings-help-release':['WP 5.1   03/09/92'],'settings-paper-selected':['8.5" x 11"','Standard'], 'settings-initial-base-font-selected':['Courier 10cpi'], 'settings-line-spacing-single':['Line Height','0.2"','Line Spacing','1','Hyphenation','No','Justification','Left'], 'settings-leading-zero':['Baseline Placement for Typesetters','No','Primary','Secondary','0"'],'settings-number-position-bottom-center':['Bottom Center','New Page Number','1','^B']}
  for label,needles in cue.items():
   text=(path/label/'screen.txt').read_text();assert all(x in text for x in needles),(rid,label)
  assert (path/'clean-exit/screen.txt').read_text().splitlines()[0]=='C:\\WP51>'
  # Read actual stopped disks, not merely analyzer's private archive cache.
  ar=next(x for x in analysis['runs'] if x['run_id']==rid)
  image=Path('/home/lynn/projects/wordling/research/cache/reference/text-layout-runs')/rid/'harddisk.img'
  for resource in ar['private_resource_audit']:
   name=resource['guest_path'].split('\\')[-1]
   raw=subprocess.check_output(['mtype','-i',str(image)+'@@1048576','::WP51/'+name])
   assert hashlib.sha256(raw).hexdigest()==resource['sha256'] and len(raw)==resource['bytes']
   resources+=1
  for state in r['states']:
   states+=1;stream=(path/state['print_stream']).read_bytes();streams+=1
   assert stream and b'\x1b' not in stream and b'\x0c' not in stream
   job=(path/('settings-print-'+state['id']+'-job-status')/'screen.txt').read_text()
   assert 'Job Number: None' in job and 'No print jobs' in job and 'Additional Jobs Not Shown: 0' in job
   aa=[]
   for name in ['native_before_print','native_after_print']:
    native+=1;data=(path/state[name]).read_bytes();fs=frames(data);aa.append(data)
    annotation=json.loads((path/(Path(state[name]).name+'.annotation.json')).read_text())
    assert [(p,b.hex()) for p,b in fs]==[(x['offset'],x['hex']) for x in annotation['tokens']]
   fs=frames(aa[-1]);counts=Counter(b[0] for _,b in fs if len(b)==1);page=line=1;rows=[];s=''
   for p,b in fs:
    if len(b)!=1:continue
    c=b[0]
    if 32<=c<=126:s+=chr(c)
    elif c in (10,13,144):
     if s:rows.append((s,page,line))
     s='';line+=1
    elif c in (11,12,140,145,146):
     if s:rows.append((s,page,line))
     s='';page+=1;line=1
   if s:rows.append((s,page,line))
   variant=r['variant'];sid=state['id']
   if variant=='L1-HR':assert counts[10]==1 and rows==[('alpha',1,1),('beta',1,2)]
   if variant=='L1-WRAP-L3-LR':assert counts[13]==(6 if sid=='BASE' else 7)
   if variant.startswith('L2-HP'):
    assert counts[12]==1;assert next(x for x in rows if 'BEFORE' in x[0])[1:]==(1,7 if sid=='CHANGE' else 1)
    assert next(x for x in rows if 'AFTER' in x[0])[1]==2
   if variant in ('L2-AUTO','L2-DORMANT'):
    starts=[x[0] for x in rows if x[2]==1];assert starts==(['P001','P043','P084'] if sid=='CHANGE' else ['P001','P044','P087'])
    assert counts[153]==(1 if sid=='DORMANT' else 0)
    assert counts[140]==2
    if sid=='DORMANT':assert stream==(path/'BASE.PRN').read_bytes()
   if variant.startswith('L4-'):
    tabs=[b for _,b in fs if b[:2]==b'\xd0\x04'];assert len(tabs)==1
    sentinel=struct.unpack_from('<H',tabs[0],206)[0]
    assert sentinel==(65535 if variant=='L4-ABS' else 1200)
    targets=[struct.unpack_from('<H',b,4)[0] for _,b in fs if b[0]==193]
    want=[2700,3900]*2 if variant=='L4-REL' and sid=='CHANGE' else [2400,3600]*2
    assert targets==want,(rid,sid,targets)
   # Baseline field meanings checked against pinned SDK text, not stream LF.
   lineheight=next(b for _,b in fs if b[:2]==b'\xd0\x00');assert struct.unpack_from('<H',lineheight,6)[0]==240
   spacing=next(b for _,b in fs if b[:2]==b'\xd0\x02');assert struct.unpack_from('<H',spacing,6)[0]==256
   facts.append({'run_id':rid,'state':sid,'outer_single_counts':dict(counts),'page_starts':[x[0] for x in rows if x[2]==1],'stream_length':len(stream),'stream_controls':dict(Counter(x for x in stream if x<32)),'native_changed_offsets':[i for i,(a,b) in enumerate(zip(*aa)) if a!=b]})
print(json.dumps({'accepted_runs':18,'states':states,'native_files':native,'streams':streams,'raw_vga_screen_pairs':rawvga,'stopped_disk_resource_fingerprints':resources,'facts':facts},indent=2))
