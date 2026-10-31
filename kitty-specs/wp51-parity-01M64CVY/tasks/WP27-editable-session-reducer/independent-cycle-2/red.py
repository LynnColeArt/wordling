import json,subprocess
from pathlib import Path
r=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g'); o=Path(__file__).resolve().parent; replace={}
for f in ['session.go','editing.go']:
 p=o/(f+'.txt');p.write_bytes(subprocess.check_output(['git','show','8b0a8ed:internal/editor/'+f],cwd=r));replace[str(r/'internal/editor'/f)]=str(p)
replace[str(r/'internal/editor/editing_test.go')]=str(Path('/home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP27-editable-session-reducer/independent-cycle-1/block_backspace_test.go.txt'))
(o/'old-overlay.json').write_text(json.dumps({'Replace':replace}))
a=['go','test','-overlay',str(o/'old-overlay.json'),'./internal/editor','-run','^TestIndependentOriginalBlockBackspace$','-count=1','-v'];p=subprocess.run(a,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/'red.txt').write_bytes(p.stdout);assert p.returncode==1 and b'approved original selected-block Backspace does not reach required question' in p.stdout
print('old production source rejects exact public Backspace assertion, expected exit1')
