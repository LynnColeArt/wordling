#!/usr/bin/env python3
"""Run the sealed public contract assertion through a temporary Go overlay."""
import argparse,json,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args()
root=a.root.resolve()
with tempfile.TemporaryDirectory(prefix='wp27-independent-')as temp:
 overlay=Path(temp)/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(root/'internal/editor/editing_test.go'):str(HERE/'block_backspace_test.go.txt')}}))
 argv=['go','test','-overlay',str(overlay),'./internal/editor','-run','^TestIndependentOriginalBlockBackspace$','-count=1','-v']
 print('Observed source',subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),flush=True)
 raise SystemExit(subprocess.run(argv,cwd=root).returncode)
