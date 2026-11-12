"""Independent bounded ANSI cell replay, no imports from supplied VT observer."""
import re,json,hashlib
from pathlib import Path
R=Path.cwd();H=R/'internal/tui/evidence/wp52';O=Path('/tmp/wordling-wp52-independent')
def decode(raw):
 rows=[[(' ',(37,49,False))for _ in range(80)]for _ in range(25)];x=y=0;fg,bg,bold=37,49,False;i=0
 def blank():return [(' ',(fg,bg,bold))for _ in range(80)]
 while i<len(raw):
  c=raw[i]
  if c==27:
   assert i+1<len(raw),'incompleteESC'
   if raw[i+1]==91:
    m=re.match(rb'\x1b\[([0-?]*[ -/]*)([@-~])',raw[i:]);assert m,raw[i:i+20];body=m[1].decode();f=m[2].decode();i+=m.end();private=body.startswith(('?','>','<','!'))
    if private:
     assert (f in ('h','l','u')or f=='m'and body.startswith('>')or f=='p'and body in ['?2026$','?2027$']or f=='W'and body=='?5'),(body,f)
     if f=='h'and body=='?1049':rows=[blank()for _ in range(25)];x=y=0
     continue
    if f=='q':assert body in ['0 ','1 '];continue
    values=[int(a or 0)for a in body.split(';')]if body else[0];n=values[0]or 1
    if f=='m':
     for v in values:
      if v==0:fg,bg,bold=37,49,False
      elif v==1:bold=True
      elif v==22:bold=False
      elif 30<=v<=37 or 90<=v<=97 or v==39:fg=v
      elif 40<=v<=47 or 100<=v<=107 or v==49:bg=v
      else:raise AssertionError(('unknownSGR',v))
    elif f=='H':y=min(24,n-1);x=min(79,(values[1]or 1)-1 if len(values)>1 else 0)
    elif f=='d':y=min(24,n-1)
    elif f=='G':x=min(79,n-1)
    elif f=='J':assert values[0]==2;rows=[blank()for _ in range(25)]
    elif f=='K':assert values[0]==0;rows[y][x:]=blank()[x:]
    elif f=='M':
     for _ in range(min(n,25-y)):rows.pop(y);rows.append(blank())
    elif f=='L':
     for _ in range(min(n,25-y)):rows.pop();rows.insert(y,blank())
    elif f=='P':k=min(n,80-x);rows[y][x:]=rows[y][x+k:]+blank()[:k]
    else:raise AssertionError(('unknownCSI',body,f))
    continue
   if raw[i+1]==77:
    if y==0:rows.pop();rows.insert(0,blank())
    else:y-=1
    i+=2;continue
   raise AssertionError(('unknownESC',raw[i:i+12]))
  if c==13:x=0
  elif c==10:
   if y==24:rows.pop(0);rows.append(blank())
   else:y+=1
  elif c==8:x=max(0,x-1)
  elif c==9:x=min(79,(x//8+1)*8)
  elif c in [0,7]:pass
  elif 32<=c<=126:
   if x==80:
    x=0
    if y==24:rows.pop(0);rows.append(blank())
    else:y+=1
   rows[y][x]=(chr(c),(fg,bg,bold));x+=1
  else:raise AssertionError(('unknownbyte',c))
  i+=1
 return [''.join(c for c,s in row)for row in rows],[[list(s)for c,s in row]for row in rows],[x,y]
receipt=json.loads((H/'pty-07/result.json').read_text());replay=json.loads((H/'raw-replay.json').read_text());checked=[];aliases=0
for process in receipt['results']:
 wire=(H/f"pty-07/native-r{process['repeat']}/wire-output.bin").read_bytes();offsets=[]
 for index,w in enumerate(process['witnesses']):
  text,styles,cursor=decode(wire[:w['wire_bytes']]);assert text==w['rows']and cursor==w['cursor'];frozen=replay['processes'][str(process['repeat'])][index];assert styles==frozen['styles'];aliases+=styles!=w['styles'];offsets.append(w['wire_bytes'])
  if w['view']=='codes':
   for repetition in [1,2]:
    b=(R/f"docs/research/continuation/session1/runs/2026-10-31-session1-b01-r{repetition}/CMD51-049/codes-gap-{w['gap']}/vram.bin").read_bytes()
    for col in range(17 if w['gap']==6 else 16):
     fg,bg,bold=styles[3][col];role=0x47 if(fg,bg,bold)==(37,41,False)else 0x17 if(fg,bg,bold)==(37,44,False)else 0x1f if(fg,bg,bold)==(97,44,False)else 0;assert b[13*160+col*2]==ord(text[3][col])and b[13*160+col*2+1]==role
  checked.append({'repeat':process['repeat'],'index':index,'offset':w['wire_bytes'],'gap':w['gap'],'view':w['view']})
 assert offsets==sorted(offsets)and len(set(offsets))==15
assert len(checked)==30 and aliases>0
(O/'independent-wire.json').write_text(json.dumps({'states':len(checked),'two_original_runs_matched':True,'old_aliased_matrices_differ':aliases,'supplied_observer_not_imported':True,'wire_prefixes':checked},indent=2)+'\n');print('Independent ANSI replay:30 states; full copied rows/matrices/cursors/raw offsets exact; both original VGA runs match; old alias differences',aliases)
