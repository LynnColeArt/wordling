"""Surviving aggregate owner for the narrow two-case F2 successor roster."""
import json
from pathlib import Path
from runtime_qualification_supervisor import supervise

def main():
    script=Path(__file__).with_name('runtime_helper_f2_controls.py')
    env=dict(PATH='/usr/bin:/bin',HOME='/tmp',LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
    result=supervise(['/usr/bin/python3','-B',str(script)],'/tmp',env,Path('/tmp/wordling-WP70-helper-controls-cycle2-02-guard'),seconds=30)
    print(json.dumps(result));return 0 if result['exit']==0 and result['cleanup_qualified'] and result['coordinator_reaped_last'] and not result['partial_prefix'] else 2

if __name__=='__main__':
    try:result=main()
    except SystemExit as e:result=e.code
    except BaseException:
        import traceback;traceback.print_exc();result=2
    raise SystemExit(result)
