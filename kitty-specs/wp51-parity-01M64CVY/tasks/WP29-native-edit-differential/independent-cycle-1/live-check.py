import sys,json,subprocess
from pathlib import Path
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-l');sys.path.insert(0,str(R/'scripts/reference'));import wordling_edits as w
O=Path('/tmp/wordling-wp29-independent');target,plan=w.selected();b=Path(plan['binary_path']);assert w.identity(b)==plan['binary'];pins=w.pins();(O/'current-source-closure.json').write_text(json.dumps(pins,indent=2)+'\n')
recipes=json.loads((target/'recipes.json').read_text());results=[]
for name in ['normal-paired-delete','closing-repair','three-entry-eviction']:
 recipe=next(x for x in recipes if x['id']==name);folder=O/('live-'+name);result=w.run_app(b,folder,recipe);proof=w.verify_app(folder,recipe);expected=next(x for x in plan['cases']if x['id']==name)
 assert w.identity(folder/'files/CANDIDA')==expected['candidate'] and (folder/'files/CANDIDA').read_bytes()==(R/expected['folder']/'files/CANDIDA').read_bytes()
 results.append({'recipe':name,'fresh_result':result,'proof':proof,'same_frozen_binary':plan['binary'],'old_candidate_exact':True})
(O/'live-results.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS three independent live PTYs: immediate post-pair F10, closing repair, three-entry eviction; exact historical candidates/native-gap markers/termios')
