#!/usr/bin/env python3
"""Finite final normal-question pair and actual candidate CLI smoke pair."""
from pathlib import Path
import subprocess
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_edits as n
import normal_questions

def main():
 n.configure();okay=True
 for repetition in (1,2):
  r=n.execute('wp23-c-normal-questions-r'+str(repetition),'normal-questions',normal_questions.run)
  okay=r['result']=='observed' and okay
 for repetition in (1,2):
  result=subprocess.run([sys.executable,'scripts/reference/native_edits.py','candidate','wp23-c-candidate-r'+str(repetition),'--candidate',str(HERE/'runs/wp23-cal-modes-02/N0002.WP5'),'--provenance',str(HERE/'candidate-smoke-provenance.json'),'--expectations',str(HERE/'candidate-smoke-expectations.json')],cwd=ROOT)
  print('candidate CLI repetition',repetition,'exit',result.returncode,flush=True);okay=result.returncode==0 and okay
 return 0 if okay else 1
if __name__=='__main__':raise SystemExit(main())
