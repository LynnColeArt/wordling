"""One three-variant pure DATA regression; never queries proc or mints capture."""
import hashlib
import importlib.util
import json
from pathlib import Path
import time
import runtime_qualification as final

ROOT=Path('/tmp/wordling-WP70-own-maps-deleted-DATA-controls-01')
V4=Path('/tmp/wordling-WP70-runtime-qualification-source-freeze-v4/runtime_qualification.py.txt')


def main():
    start=time.monotonic();ROOT.mkdir(mode=0o700,exist_ok=False)
    # Exact old owned helper copy, imported only to run its pure DATA predicate.
    # No old checker/OS/proc path or CLI main is executed.
    old_copy=ROOT/'V4_helper_literal.py';old_copy.write_bytes(V4.read_bytes())
    spec=importlib.util.spec_from_file_location('V4_deleted_DATA',old_copy);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    launch=['/PINNED/DATA/python','-I','-B'];actor=123
    initial=f'{actor} execve("/PINNED/DATA/python", ["/PINNED/DATA/python", "-I", "-B"], 0x0) = 0\n'
    exact=initial+f'{actor} openat(AT_FDCWD</DATA>, "/proc/self/maps", O_RDONLY) = 3</proc/{actor}/maps>\n'
    deleted=exact.removesuffix('>\n')+' (deleted)>\n'
    results=[]
    red=old.historical_data_review(deleted,launch);assert len(red['transient'])==1 and red['production_authority'] is False
    results.append(dict(id='genuine_V4_deleted_suffix_RED',status='EXPECTED_RED',result=red))
    try:final.historical_data_review(deleted,launch)
    except RuntimeError as e:results.append(dict(id='final_deleted_suffix_refused',status='PASS',reason=str(e)))
    else:raise AssertionError('DeletedSuffixAccepted')
    positive=final.historical_data_review(exact,launch);assert len(positive['transient'])==1 and positive['transient'][0]['kernel_result']=='3</proc/123/maps>' and not positive['production_authority']
    results.append(dict(id='final_exact_descriptor_positive',status='PASS',result=positive))
    assert len(final._CAPTURES)==len(old._CAPTURES)==0
    (ROOT/'results.json').write_text(json.dumps(dict(group='exact_kernel_descriptor',variants=results,source_V4_sha256=hashlib.sha256(V4.read_bytes()).hexdigest(),source_final_sha256=hashlib.sha256(Path(final.__file__).read_bytes()).hexdigest(),elapsed=time.monotonic()-start,production_captures=0,actual_proc_queries=0,TCB=False,P=False),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',groups=1,variants=3,expected_RED=1,elapsed=time.monotonic()-start)))
    return 0

if __name__=='__main__':
    try:result=main()
    except BaseException:
        import traceback;traceback.print_exc();result=2
    raise SystemExit(result)
