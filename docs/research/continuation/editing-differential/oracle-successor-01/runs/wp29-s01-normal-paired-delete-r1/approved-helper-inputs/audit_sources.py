#!/usr/bin/env python3
"""Reproduce pinned source/locator/full-field and semantic registry associations."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_edits as n

def audit(associations=None):
 ledger=json.loads((HERE/'field-ledger.json').read_text());source=n.ORIGIN.read_bytes();info=n.inspect(source,True)
 if n.sha(n.ORIGIN)!=ledger['source_fixture']['sha256']:raise ValueError('Field source identity mismatch')
 payloads={'header':source[:16],**{'packet-'+str(p['type']):bytes.fromhex(p['hex']) for p in info['packets']}}
 sizes={'header':16,**{'packet-'+str(p['type']):p['length'] for p in info['packets']}}
 for owner,size in sizes.items():
  covered=[]
  for row in ledger['field_coverage']:
   if row['owner']==owner:
    if row['source_observed_hex']!=payloads[owner][row['offset']:row['offset']+row['width']].hex():raise ValueError('Field source byte association changed')
    if not row['references'] or not row['units'] or not row['mutation_policy']:raise ValueError('Incomplete field relationship')
    covered.extend(range(row['offset'],row['offset']+row['width']))
  if sorted(covered)!=list(range(size)):raise ValueError('Field coverage gap/overlap '+owner)
 for key in ('index_header_fields','general_index_fields'):
  positions=[i for row in ledger[key] for i in range(row['offset'],row['offset']+row['width'])]
  if sorted(positions)!=list(range(10)):raise ValueError('Index field coverage')
 canonical={r['id']:r for r in json.loads((ROOT/'docs/research/command-scenarios.json').read_text())};features={r['id']:r for r in json.loads((ROOT/'docs/research/feature-inventory.json').read_text())}
 associations=associations or json.loads((HERE/'canonical-associations.json').read_text())
 for cid,row in associations.items():
  current=canonical[cid]
  if row['title']!=current['title'] or row['feature_ids']!=current['feature_ids'] or row['source_locators']!=current['source_locators']:raise ValueError('Wrong semantic canonical association '+cid)
  if row['features']!={f:features[f]['title'] for f in current['feature_ids']}:raise ValueError('Wrong semantic feature titles')
 qualification=json.loads((HERE/'two-pair-qualification.json').read_text())
 for witness in qualification['fresh_witnesses']:
  a=(ROOT/witness['source']['path']).read_bytes();b=(ROOT/witness['final']['path']).read_bytes();before=n.inspect(a,True);after=n.inspect(b,True);flag=next(p['offset'] for p in before['packets'] if p['type']==6)
  if after['qualified_pair_count']!=2 or before['body_offset']!=after['body_offset'] or [i for i in range(before['body_offset']) if a[i]!=b[i]]!=[flag]:raise ValueError('Two-pair prefix relationship proof changed')
  if n.sha(ROOT/witness['source']['path'])!=witness['source']['sha256'] or n.sha(ROOT/witness['final']['path'])!=witness['final']['sha256']:raise ValueError('Two-pair original native identity changed')
 pages=0
 for manual in json.loads((HERE/'manual-locators.json').read_text()):
  if n.sha(manual['source_path'])!=manual['sha256']:raise ValueError('Pinned manual changed')
  for locator in manual['pages']:
   page=str(locator['pdf_page_one_based']);data=subprocess.check_output(['pdftotext','-f',page,'-l',page,manual['source_path'],'-'])
   if len(data)!=locator['text_bytes'] or hashlib.sha256(data).hexdigest()!=locator['text_sha256']:raise ValueError('Exact PDF locator extraction changed')
   pages+=1
 return {'field_rows':len(ledger['field_coverage']),'complete_owner_sizes':sizes,'index_schema_bytes':10,'canonical_associations':len(associations),'exact_pdf_page_extractions':pages,'source_fixture_sha256':n.sha(n.ORIGIN),'scope':'source/locator/semantic association audit only, no original behavior inferred from documentary table'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();result=audit();text=json.dumps(result,indent=2)+'\n'
 if a.output:
  out=Path(a.output)
  if out.exists():raise FileExistsError('Preserve earlier audit revision')
  out.write_text(text)
 else:print(text)
