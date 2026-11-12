#!/usr/bin/env python3
"""WP13 I1: fresh quit repetitions with separately captured final DOS state."""
import argparse
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import session1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('prefix')
    args=parser.parse_args()
    okay=True
    with session1.exclusive():
        for index,context in enumerate(('named-unchanged','named-changed','unnamed-unchanged','unnamed-changed')):
            for repetition in (1,2):
                passed=session1.execute(args.prefix+f'-quitfix-q{index:02d}-r{repetition}',context+'-quit','CMD51-244')
                okay=passed and okay
    return 0 if okay else 1


if __name__=='__main__':raise SystemExit(main())
