from pathlib import Path
import hashlib,json
P=Path('/tmp/wordling-native-constructor-tasks');O=Path('/tmp/wordling-native-constructor-tasks-review/cycle-2');H=P/'history/task-review-revision-1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(P/'seals.json')=='fca9ae3b7731b43108276e32bec87d69f1a06f215392fc7e27367e7bc0624463'
s=json.load(open(P/'seals.json'));assert len(s['files'])==139
for n,h in s['files'].items():assert sha(P/n)==h,n
assert sha(H/'seals.json')=='abedfd12db1ed5c13d6311159e7b321bb7d1c6e9b94fd13c51f22ecc5d458132';old=json.load(open(H/'seals.json'));assert len(old['files'])==64
changed=[]
for n,h in old['files'].items():
 assert sha(H/n)==h,n
 if sha(P/n)!=h:changed.append(n)
assert set(changed)=={'changes.diff','draft-manifest.json','continuation.append.md','kitty-specs/wp51-parity-01M64CVY/continuation.md','lanes-preview.json'},changed
l=json.load(open(P/'lanes-preview.json'));q=json.load(open(H/'lanes-preview.json'));l.pop('computed_at');q.pop('computed_at');assert l==q
for n in ['continuation.append.md','kitty-specs/wp51-parity-01M64CVY/continuation.md']:
 before=(H/n).read_text();after=(P/n).read_text();assert before.count('approved36T108 Save/history repair')==1;assert before.replace('approved36T108 Save/history repair','canonically analyzed36T108 Save/history requirement amendment')==after
assert sha(P/'pure-validation.json')=='8a5495000e9ac85aa98b64aa28c0b110175f2e2b5ce12fb95a433bc2d22cf816';assert sha(P/'draft-manifest.json')=='bf888d29dbcea4f4f172f0795c21d81cebbd67b638ebc0ffaeac16d46001559e';assert sha(P/'task-review-R1-receipt.json')=='4f93025c7fed24f3dc856f067ced82d538f12de6046488afdb7f0c018407c697'
r=json.load(open(P/'task-review-R1-receipt.json'))
for n,h in r['review_files_sha256'].items():assert sha(Path('/tmp/wordling-native-constructor-tasks-review')/n)==h;assert sha(P/'reviews/task-cycle-1'/n)==h
src=(P/'verify.py').read_text()
for n in ['pure-validation.json','lanes-preview.json']:
 a="(o/'"+n+"').write_text";b="(Path('/tmp/wordling-native-constructor-tasks-review/cycle-2')/'"+n+"').write_text";assert src.count(a)==1;src=src.replace(a,b)
(O/'verify-temp-output.py').write_text(src);(O/'audit.json').write_text(json.dumps({'139_current_seals_exact':True,'64_old_archive_exact':True,'changed_old_paths':changed,'lanes_preview_only_computed_at_changed':True,'only_R1_wording_in_content':True,'prior_review_exact':True,'prompt_design_proof_unchanged':True},indent=2)+'\n')
