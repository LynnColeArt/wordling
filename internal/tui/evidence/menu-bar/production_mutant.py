"""Remove actual live bar integration; fresh unchanged cmd must fail PTY oracle."""
from pathlib import Path
import subprocess,json,time
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
p=ROOT/'internal/tui/model.go';original=p.read_text();binary=Path('/tmp/wordling-WP62-build/no-menu-integration');start=time.monotonic()
try:
 assert 'if m.menuState().Visible {'in original;p.write_text(original.replace('if m.menuState().Visible {','if false {',1))
 b=subprocess.run(['go','build','-o',str(binary),'./cmd/wordling'],cwd=ROOT,capture_output=True,timeout=300);(HERE/'production-mutant-build.stdout').write_bytes(b.stdout);(HERE/'production-mutant-build.stderr').write_bytes(b.stderr);assert b.returncode==0
 r=subprocess.run(['python3',str(HERE/'run_pty.py'),str(binary),str(HERE/'pty-mutant')],cwd=ROOT,capture_output=True,timeout=35);(HERE/'production-mutant.stdout').write_bytes(r.stdout);(HERE/'production-mutant.stderr').write_bytes(r.stderr);assert r.returncode!=0
 result=json.loads((HERE/'pty-mutant/r1/result.json').read_text());assert result['failure']and result['termios_restored'];(HERE/'production-mutant.json').write_text(json.dumps(dict(build_exit=b.returncode,pty_exit=r.returncode,semantic_kill=True,termios_restored=True,elapsed=time.monotonic()-start,source_mutation='actual View menu integration deleted; no overlay/test-only flags'),indent=2)+'\n')
finally:p.write_text(original)
