from pathlib import Path
import importlib.util,json,subprocess,hashlib
r=Path.cwd();o=Path('/tmp/wordling-wp48-independent');binary=o/'wordling';build=['go','build','-o',str(binary),'./cmd/wordling'];p=subprocess.run(build,capture_output=True);(o/'build.stdout').write_bytes(p.stdout);(o/'build.stderr').write_bytes(p.stderr);assert p.returncode==0
s=importlib.util.spec_from_file_location('wp48',r/'docs/research/continuation/new-session/pty_test.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
output=o/'live';output.mkdir();results=[]
for name,seed in [('empty',None),('ascii-repeat-save',None),('reopen-ascii-edit',output/'ascii-repeat-save/files/FIRST'),('existing-refusal',None),('signal-saved',None)]:results.append(m.run(binary,output,name,seed))
(o/'live-results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'build':build,'whole_exit':0,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'real_app_processes':len(results),'all_termios':all(x['termios_restored'] for x in results),'failures':[x['failure'] for x in results]}))
