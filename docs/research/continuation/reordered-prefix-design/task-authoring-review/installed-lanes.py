from pathlib import Path
import json,yaml,hashlib,dataclasses
from specify_cli.lanes.compute import compute_lanes,find_overlap_pairs
from specify_cli.ownership.models import OwnershipManifest
import specify_cli.lanes.compute as module
P=Path('/home/lynn/projects/wordling');O=Path('/tmp/wordling-prefix-expansion-tasks');T=Path('/tmp/wordling-prefix-expansion-tasks-review');M=Path('kitty-specs/wp51-parity-01M64CVY');front={};bodies={}
for p in (O/M/'tasks').glob('WP*.md'):
 text=p.read_text();f=yaml.safe_load(text.split('---',2)[1]);front[f['work_package_id']]=f;bodies[f['work_package_id']]=text.split('---',2)[2]
deps={k:f['dependencies'] for k,f in front.items()};own={k:OwnershipManifest.from_frontmatter(f) for k,f in front.items()};r=compute_lanes(deps,own,'wp51-parity-01M64CVY',target_branch='feat/wp51-parity',wp_bodies=bodies,mission_id='01M64CVYYRTDKBCYZ56H6XNTEQ');d=dataclasses.asdict(r);(T/'installed-lanes.json').write_text(json.dumps(d,indent=2,default=str)+'\n');print('lanes',len(r.lanes));print('45overlap',[p for p in find_overlap_pairs(own) if 'WP45' in p]);mapping={w:l.lane_id for l in r.lanes for w in l.wp_ids};old=json.loads((P/M/'lanes.json').read_text());prior={w:l['lane_id'] for l in old['lanes'] for w in l['wp_ids']};assert all(mapping[k]==v for k,v in prior.items());assert mapping['WP44']=='lane-e' and mapping['WP45']=='lane-s';print('all43oldmappings stable,44e45s')
proof={'scope':'pure installed compute_lanes only; no canonical finalizer or mutation','installed_module':module.__file__,'installed_module_sha256':hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),'WP_count':45,'subtasks':sum(len(f['subtasks'])for f in front.values()),'lane_count':len(r.lanes),'old43mapping_stable':True,'mapping':mapping,'WP45_overlap_pairs':[p for p in find_overlap_pairs(own)if 'WP45'in p],'not_canonical':True}
(T/'installed-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
