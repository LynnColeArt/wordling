#!/usr/bin/env python3
"""Predeclared deterministic bounded malformed audit; does not launch original."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import struct
import time
import tracemalloc
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_edits as n

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output)
 if out.exists():raise FileExistsError('Preserve earlier result')
 plan=json.loads((HERE/'bounds-plan.json').read_text());print(plan)
 seeds=[n.ORIGIN.read_bytes()]
 for path in sorted((HERE/'runs').glob('wp23-a-modes-r1/*.WP5')):seeds.append(path.read_bytes())
 seeds += [b'',b'\xffWPC',seeds[0][:324]+bytes.fromhex('c30cc3c30cc3c40cc4c40cc4'),seeds[0][:324]+bytes.fromhex('d0010800c30cc3080001d0')]
 # Measure maximum accepted body and alias-heavy diagnostic traversal before fuzz.
 B=n.LIMIT-n.TOKEN_LIMIT;alias=bytearray(n.LIMIT);alias[:16]=seeds[0][:16];struct.pack_into('<I',alias,4,B)
 for j in range(8):
  offset=16+50*j;struct.pack_into('<HHHI',alias,offset,65531,5,50,offset+50 if j<7 else 0)
  for k in range(1,5):struct.pack_into('<HII',alias,offset+10*k,7,B-16,16)
 alias[B:]=b'A'*n.TOKEN_LIMIT
 tracemalloc.start();astart=time.monotonic();diagnostic=n.inspect(alias,False);alias_elapsed=time.monotonic()-astart;_,alias_peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 assert diagnostic['coverage_issues'] and len(diagnostic['blocks'])==8
 del diagnostic
 # Maximum accepted token body has disjoint complete prefix ownership.
 tracemalloc.start();start=time.monotonic();n.inspect(seeds[0][:324]+b'A'*n.TOKEN_LIMIT,True);elapsed=time.monotonic()-start;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 rng=random.Random(230067);start=time.monotonic();iterations=0;refusals=0;accepted=0
 while time.monotonic()-start<20:
  raw=bytearray(rng.choice(seeds));choice=rng.randrange(5)
  if choice==0:raw=raw[:rng.randrange(len(raw)+1)]
  elif choice==1 and raw:
   for _ in range(rng.randrange(1,5)):raw[rng.randrange(len(raw))]=rng.randrange(256)
  elif choice==2:raw.extend(bytes(rng.randrange(256) for _ in range(rng.randrange(33))))
  elif choice==3 and len(raw)>=16:raw[4:8]=rng.choice((0,15,16,65535,65536,0xffffffff)).to_bytes(4,'little')
  elif choice==4:raw=bytearray(rng.choice((b'A'*(n.TOKEN_LIMIT+1),bytes(n.LIMIT+1))))
  before=bytes(raw)
  try:n.inspect(raw,True)
  except ValueError:refusals+=1
  else:accepted+=1
  if bytes(raw)!=before:raise AssertionError('Inspector mutated caller-owned bytes')
  iterations+=1
 result={'seed':230067,'budget_seconds':20,'elapsed_seconds':time.monotonic()-start,'iterations':iterations,'typed_research_refusals':refusals,'admitted_unchanged_or_supported_mutations':accepted,'input_bytes_limit':n.LIMIT,'token_limit':n.TOKEN_LIMIT,'index_blocks_diagnostic':8,'index_blocks_mutation':2,'alias_heavy_diagnostic_measurement':{'elapsed_seconds':alias_elapsed,'peak_python_traced_bytes':alias_peak,'packet_extents':32,'note':'malformed overlap diagnostic only; mutation refused'},'maximum_token_measurement':{'elapsed_seconds':elapsed,'peak_python_traced_bytes':peak,'note':'Python temporary allocation, not product SLO or OS RSS guarantee'},'source_sha256':n.sha(ROOT/'scripts/reference/native_edits.py'),'seed_sha256':[hashlib.sha256(x).hexdigest() for x in seeds],'assertions':['no unexpected exceptions','caller bytes unchanged','budget/truncation/overflow/pair/opaque seeds exercised'],'wordling_serializer_tested':False}
 out.write_text(json.dumps(result,indent=2)+'\n');print(iterations,'iterations passed')
if __name__=='__main__':main()
