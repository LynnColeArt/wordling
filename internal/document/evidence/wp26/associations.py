#!/usr/bin/env python3
"""Canonical ID/title/group/locator checks with semantically wrong valid IDs."""
import copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
EXPECTED={
 'CMD51-200':('Delete at a paired bold-code boundary',['WP51-011','WP51-013']),
 'CMD51-201':('Backspace at a paired bold-code boundary',['WP51-011','WP51-013']),
 'CMD51-202':('Delete a block containing only Bold On',['WP51-009','WP51-011','WP51-013']),
 'CMD51-203':('Delete a block containing only Bold Off',['WP51-009','WP51-011','WP51-013']),
 'CMD51-204':('Undelete an entire blocked bold span',['WP51-009','WP51-011','WP51-013']),
 'CMD51-045':('Character deletion restoration differs for paired attributes',['WP51-011']),
 'CMD51-043':('Select among three remembered deletions',['WP51-011']),
 'CMD51-211':('Fourth deletion evicts the oldest Undelete entry',['WP51-011'])}
def validate(rows):
 cases={x['id']:x for x in json.loads((ROOT/'docs/research/command-scenarios.json').read_text())};features={x['id']:x for x in json.loads((ROOT/'docs/research/feature-inventory.json').read_text())};sources={x['id']:x for x in json.loads((ROOT/'docs/research/sources.json').read_text())}
 if len(rows)!=len(EXPECTED)or {x['id']for x in rows}!=set(EXPECTED):raise ValueError('Wrong semantic case set')
 for row in rows:
  title,groups=EXPECTED[row['id']];case=cases[row['id']]
  if title!=row['title']or title!=case['title']:raise ValueError('Wrong semantic title')
  if groups!=row['feature_ids']or groups!=case['feature_ids']:raise ValueError('Wrong feature association')
  if row['locators']!=case['source_locators']or row['requirements']!=case['requirement_ids']:raise ValueError('Wrong source/requirement association')
  if len(groups)!=len(row['feature_titles']):raise ValueError('Wrong feature membership/title')
  for group,label in zip(groups,row['feature_titles']):
   if features[group]['title']!=label or row['id']not in features[group]['command_scenario_ids']:raise ValueError('Wrong feature membership/title')
  for locator in row['locators']:
   source=sources[locator['source_id']]
   if not 1<=locator['pdf_start']<=locator['pdf_end']<=source['pdf_pages']:raise ValueError('Unpinned locator')
  if 'canonical full scenario/FR/feature groups remain unverified'not in row['scope']:raise ValueError('Widened scope')
 return len(rows)
def run():
 rows=json.loads((HERE/'case-associations.json').read_text());count=validate(rows);negatives=[]
 for field,value,error in [('feature_ids',['WP51-020'],'Wrong feature association'),('title','Retrieve inserts at the cursor','Wrong semantic title'),('id','CMD51-065','Wrong semantic case set')]:
  bad=copy.deepcopy(rows);bad[0][field]=value
  try:validate(bad)
  except ValueError as e:
   if str(e)!=error:raise
   negatives.append({'field':field,'valid_but_unrelated_value':value,'rejected':str(e)})
  else:raise ValueError('Semantic negative survived')
 return {'canonical_cases':count,'negative_controls':negatives,'registry_source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['docs/research/command-scenarios.json','docs/research/feature-inventory.json','docs/research/sources.json']},'canonical_statuses_unchanged':True,'full_groups_verified':False}
if __name__=='__main__':print(json.dumps(run(),indent=2))
