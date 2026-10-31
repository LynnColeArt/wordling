"""Bounded diagnostic: match actual code-pane highlight to known native tokens.

No inches/cells-to-layout conversion and no inferred normal-view code gap.
Requires an exact one-line ASCII/Bold native-to-original-label match.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_edits as n

def gap(native,screen_directory):
 raw=Path(native).read_bytes();B=int.from_bytes(raw[4:8],'little');tokens=n.body_tokens(raw[B:]);widths=[];parts=[]
 for token in tokens:
  label=bytes.fromhex(token['hex']).decode('ascii') if token['kind']=='ASCII' else ('[BOLD]' if token['kind']=='BoldOn' else '[bold]')
  widths.append(len(label));parts.append(label)
 display=''.join(parts);vga=(Path(screen_directory)/'vram.bin').read_bytes()
 if len(vga)!=4000 or len(display)>79:raise ValueError('Unsupported code-pane window')
 row=vga[13*160:14*160];text=row[0::2].replace(b'\0',b' ').decode('cp437').rstrip()
 if text!=display:raise ValueError('Native/code-pane text mismatch; no position inference')
 columns=[i for i in range(80) if row[2*i+1]==0x47]
 start=0
 for index,width in enumerate(widths):
  if columns==list(range(start,start+width)):return {'gap':index,'active_columns':columns,'basis':'exact raw native token/label and VGA highlight match, not Pos inches'}
  start+=width
 if columns==[start]:return {'gap':len(tokens),'active_columns':columns,'basis':'exact native EOF label boundary and highlighted blank'}
 raise ValueError('Ambiguous/missing original code highlight')

def block_selection(native,screen_directory,start,end):
 raw=Path(native).read_bytes();tokens=n.body_tokens(raw[int.from_bytes(raw[4:8],'little'):]);labels=[]
 for token in tokens:labels.append(bytes.fromhex(token['hex']).decode('ascii') if token['kind']=='ASCII' else ('[BOLD]' if token['kind']=='BoldOn' else '[bold]'))
 expected=''.join(labels[:start])+'[Block]'+''.join(labels[start:]);vga=(Path(screen_directory)/'vram.bin').read_bytes();row=vga[13*160:14*160]
 if row[::2].replace(b'\0',b' ').decode('cp437').rstrip()!=expected:raise ValueError('Actual block-start label differs from native token range')
 position=sum(map(len,labels[:end]))+7;width=len(labels[end]) if end<len(labels) else 1
 columns=[i for i in range(80) if row[2*i+1]==0x47]
 if columns!=list(range(position,position+width)):raise ValueError('Actual block-end highlight differs from native token range')
 return {'start_gap':start,'end_gap':end,'highlight_columns':columns,'basis':'exact source-native labels plus virtual original [Block] start marker and end-token highlight; display marker is not native document code'}

def plain_gap(native,screen_directory):
 import json
 raw=Path(native).read_bytes();body=raw[int.from_bytes(raw[4:8],'little'):];tokens=n.body_tokens(body)
 if any(t['kind']!='ASCII' for t in tokens) or len(body)>79 or body.endswith(b' '):raise ValueError('Not a unique short plain ASCII cursor witness')
 directory=Path(screen_directory);vga=(directory/'vram.bin').read_bytes();cursor=json.loads((directory/'cursor.json').read_text())
 if vga[:160:2].replace(b'\0',b' ').rstrip()!=body or cursor['display_start_word']!=0 or cursor['row']!=0 or not 0<=cursor['column']<=len(body):raise ValueError('Native/actual ASCII row/cursor mismatch')
 return {'gap':cursor['column'],'basis':'entire exact native plain ASCII body equals raw VGA row0, no codes/wrap/scroll, plus hardware cursor; not Pos inches or glyph-only identity'}
