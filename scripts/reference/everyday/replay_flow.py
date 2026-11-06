#!/usr/bin/env python3
"""Repeat the discovered multi-page native flow with explicit content checkpoints."""
import sys
from run import perform

SAMPLE = 'A faithful reconstruction needs more than a blue screen. Menus, prompts, wrapping, and cursor movement must work together.'
steps = [
    ['start'], ['key', 'f3'], ['wait', '03/09/92'], ['capture', '01-release'],
    ['key', 'ret'], ['wait', 'Doc 1'], ['type', SAMPLE], ['key', 'ret,ret'],
    ['type', 'Plain '], ['key', 'f8'], ['type', 'UNDER'], ['key', 'f8'],
    ['type', ' after'], ['key', 'ret,tab'], ['type', 'Tab alpha alpha'], ['key', 'ret'],
    ['type', 'X' * 75], ['key', 'ret'], ['repeat-key', 'ret', 110],
    ['type', 'LAST PAGE alpha'], ['wait', 'LAST PAGE alpha'], ['capture', '02-three-pages'],
    ['save', 'C:\\OUT\\FLOW.WP'], ['wait', 'C:\\OUT\\FLOW.WP'],
    ['type', ' EDIT'], ['wait', 'LAST PAGE alpha EDIT'], ['save', '', 'y'],
    ['key', 'f7'], ['wait', 'Save document?'], ['key', 'n'], ['wait', 'Exit WP?'],
    ['key', 'n'], ['wait', 'Doc 1'], ['key', 'shift-f10'], ['wait', 'Document to be retrieved:'],
    ['type', 'C:\\OUT\\FLOW.WP'], ['key', 'ret'], ['wait', 'A faithful reconstruction'],
    ['capture', '03-retrieved'], ['key', 'end,down,down,down,down'],
    ['capture', '04-desired-horizontal'], ['key', 'pgdn'], ['wait', 'Pg 2'],
    ['capture', '05-page-two'], ['key', 'pgdn'], ['wait', 'Pg 3'], ['capture', '06-page-three'],
    ['key', 'home,home,down'], ['wait', 'LAST PAGE alpha EDIT'], ['type', ' MORE'],
    ['wait', 'LAST PAGE alpha EDIT MORE'], ['save', '', 'y'],
    ['top'], ['key', 'f2'], ['wait', 'Srch:'], ['type', 'alpha'], ['key', 'f2'],
    ['absent', 'Srch:'], ['capture', '07-first-search'], ['key', 'f2'], ['wait', 'Srch:'],
    ['key', 'f2'], ['absent', 'Srch:'], ['capture', '08-repeat-search'],
    ['key', 'shift-f2'], ['wait', 'Srch:'], ['key', 'shift-f2'], ['absent', 'Srch:'],
    ['capture', '09-backward-search'], ['top'], ['key', 'f2'], ['wait', 'Srch:'],
    ['type', 'Menus, prompts'], ['key', 'f2'], ['absent', 'Srch:'], ['capture', '10-wrap-search'],
    ['key', 'alt-f3'], ['wait', 'Reveal Codes to restore'], ['top'],
    ['key', 'f2'], ['wait', 'Srch:'], ['key', 'f8'], ['key', 'f2'], ['absent', 'Srch:'],
    ['capture', '11-underline-search'], ['key', 'alt-f3'], ['save', '', 'y'],
    ['capture', '12-final-save'], ['stop'], ['export'],
]

if __name__ == '__main__':
    perform(sys.argv[1], steps)
