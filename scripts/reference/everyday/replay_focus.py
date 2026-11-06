#!/usr/bin/env python3
"""Repeat nested-menu cancellation from explicit fresh editing states."""
import sys
from run import perform

steps = [['start'], ['key', 'f3'], ['wait', '03/09/92'], ['capture', '01-release'], ['key', 'ret'], ['wait', 'Doc 1']]
for index, key in enumerate(['f1', 'esc', 'spc', 'f7'], 2):
    label = str(index).zfill(2) + '-' + key
    steps += [['key', 'alt-equal'], ['wait', 'File Edit Search'], ['key', 'l'], ['wait', 'Footnote'], ['key', 'j'], ['wait', 'Center'], ['capture', label + '-before'], ['key', key], ['capture', label + '-after'], ['key', 'up'], ['capture', label + '-up']]
    if key != 'f7':
        steps += [['key', 'f7'], ['absent', 'File Edit Search']]
steps += [['type', 'FOCUS'], ['wait', 'FOCUS'], ['capture', '06-typing'], ['save', 'C:\\OUT\\FOCUS.WP'], ['capture', '07-saved'], ['stop'], ['export']]
if __name__ == '__main__':
    perform(sys.argv[1], steps)
