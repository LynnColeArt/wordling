#!/usr/bin/env python3
"""Repeat corrected Esc contexts and the direct normal-prefix witness serially."""
import argparse
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import session1


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('prefix');a=p.parse_args()
    branches=[]
    for context in ('named-unchanged','named-changed','unnamed-unchanged','unnamed-changed'):
        branches.extend([(context+'-save-esc','CMD51-241'),(context+'-exit-esc','CMD51-243')])
    branches.append(('prefix-normal','CMD51-020'))
    okay=True
    with session1.exclusive():
        for index,(branch,cid) in enumerate(branches):
            for repetition in (1,2):
                passed=session1.execute(a.prefix+f'-correct-c{index:02d}-r{repetition}',branch,cid)
                okay=passed and okay
    return 0 if okay else 1


if __name__=='__main__':raise SystemExit(main())
