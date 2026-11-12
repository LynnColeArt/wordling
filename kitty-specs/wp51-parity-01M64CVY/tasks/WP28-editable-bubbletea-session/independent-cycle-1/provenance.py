from pathlib import Path
import json,hashlib,subprocess
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h');O=R/'docs/research/continuation/editable-session';T=Path('/tmp/wordling-wp28-independent');h=lambda b:hashlib.sha256(b).hexdigest();rows=[]
for n in ['artifact-manifest.json','reentry/manifest.json']:rows+=json.loads((O/n).read_text())['records']
assert len(rows)==190
for row in rows:
 b=(R/row['path']).read_bytes();assert len(b)==row['size'] and h(b)==row['sha256'];assert subprocess.check_output(['git','show','HEAD:'+row['path']],cwd=R)==b;assert subprocess.check_output(['git','rev-parse','HEAD:'+row['path']],cwd=R,text=True).strip()==row['git_blob']
assert len({x['path']for x in rows})==190
old=json.loads((O/'pty-final-02/inputs.json').read_text());eq=json.loads((T/'equality.json').read_text());assert eq['source_inputs_count']==78 and eq['compiled_local_packages_count']==8 and eq['source_paths_and_hashes_exact']and eq['compiled_source_paths_and_hashes_exact']
assert eq['package_count_old']==14 and eq['package_count_current']==15
new=json.loads((T/'pty/inputs.json').read_text());assert new['working_source_inputs']==old['working_source_inputs'];assert new['source_head']=='8916f81f0ea5dd3ff1daafb26ec239b399df7a98'
for p in eq['compiled_packages']:
 assert Path(p['directory']).is_relative_to(R)
 for f,v in p['go_files'].items():assert h((Path(p['directory'])/f).read_bytes())==v
snapshot=[]
for name in ['ascii','block-restore','repair-restore','normal-question','host-signal']:
 orig=json.loads((O/'pty-final-02'/name/'result.json').read_text());f=Path(orig['argv'][0]);assert f.is_file() and h(f.read_bytes())==orig['binary']['sha256']=='0bbbb85f7db33f8e1a422d1efecbf1843158c576b356c6d1f1ba7e8d24f9a8e6'
 current=json.loads((T/'pty'/name/'result.json').read_text());assert current['termios_restored'] and not current['physical_qualified'] and current['returncode']==(1if name=='host-signal'else 0);assert current['binary']==new['binary'];assert current['argv'][0]==str(T/'wordling')
 for filename,v in current['files'].items():
  b=(T/'pty'/name/'files'/filename).read_bytes();assert len(b)==v['size'] and h(b)==v['sha256']
 snapshot.append({'workflow':name,'historical_binary_SHA':orig['binary']['sha256'],'current_binary_SHA':current['binary']['sha256'],'exit':current['returncode'],'termios_restored':True,'wire_SHA':h((T/'pty'/name/'wire-output.bin').read_bytes()),'files':current['files']})
assert(T/'pty/runner.py.txt').read_bytes()==(O/'pty_test.py').read_bytes()
stamp=json.loads((O/'go-worktree-stamp.json').read_text());assert h(Path('/usr/local/go/src/cmd/go/internal/vcs/vcs.go').read_bytes())==stamp['go_vcs_source_sha256'];assert(R/'.git').is_file();assert h((R/'.git').read_bytes())==stamp['marker_sha256']
# Product behavior never consumes build VCS metadata.
for p in(R/'internal').rglob('*.go'):
 if not p.name.endswith('_test.go'):assert 'ReadBuildInfo'not in p.read_text()
(T/'provenance.json').write_text(json.dumps({'HEAD':'8916f81f0ea5dd3ff1daafb26ec239b399df7a98','actual190Git_seals':True,'78_product_module_input_path_sets_and_hashes_exact':True,'8compiled_local_package_Dir_GoFiles_sets_and_hashes_exact':True,'historical_binary_still_exact':True,'fresh5actual_executable_PTY':snapshot,'installed_go_vcs_source_exact':True,'installed_FromDir_test':'vcs-installed.log','stamp_not_read_by_product':True,'module_no_updates':True,'new_VM':False},indent=2)+'\n');print('PASS190actualGit seals/78allsource+module/8compiledclosure/historicalbinary/fresh5PTY/native/installedVCSproof')
