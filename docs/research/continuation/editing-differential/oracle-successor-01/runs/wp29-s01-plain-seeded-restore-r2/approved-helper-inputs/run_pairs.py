#!/usr/bin/env python3
"""Serial fresh-master recipes; history recipes never inherit earlier deletions."""
import argparse
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_edits as n
import followups

def main():
 p=argparse.ArgumentParser();p.add_argument('prefix');p.add_argument('recipes',nargs='*');a=p.parse_args()
 recipes=a.recipes or ['modes','boundaries','deletions','blocks',*['history-'+x for x in ('empty','one','two','save-nav','consume','repair','refuse')]]
 okay=True
 for recipe in recipes:
  for repetition in (1,2):
   r=n.execute(a.prefix+'-'+recipe+'-r'+str(repetition),recipe,followups.RECIPES.get(recipe))
   okay=r['result']=='observed' and okay
 return 0 if okay else 1
if __name__=='__main__':
 n.configure();raise SystemExit(main())
