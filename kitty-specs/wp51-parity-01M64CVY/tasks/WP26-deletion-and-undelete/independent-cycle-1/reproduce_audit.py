"""Independent replay: redirect only the two known derived output writes to /tmp."""
from pathlib import Path
import importlib.util,json
root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e')
out=Path('/tmp/wordling-wp26-independent')
file=root/'internal/document/evidence/wp26/audit.py'
spec=importlib.util.spec_from_file_location('review_wp26',file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
original=Path.write_text
dest={m.HERE/'document-reopen.json':out/'document-reopen.json',m.HERE/'audit-result.json':out/'audit-result.json'}
def redirected(self,text,*args,**kwargs):return original(dest.get(self,self),text,*args,**kwargs)
# Run from actual lane root. Run broad Go discovery checks only AFTER this
# replay completes: approved classifier creates/removes temporary reader packages.
import os
os.chdir(root);Path.write_text=redirected
try:result=m.run()
finally:Path.write_text=original
(out/'audit-result.json').write_text(json.dumps(result,indent=2)+'\n')
