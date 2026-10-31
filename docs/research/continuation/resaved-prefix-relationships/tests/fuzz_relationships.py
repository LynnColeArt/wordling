"""Finite measured diagnostic mutation corpus; budget4501/1000/64 Go samples."""
import json
from pathlib import Path
import random
import sys
import tempfile
import time
import tracemalloc

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import resaved_prefix_relationships as tool

def main():
    tool.custody();inherited,inspector=tool.helpers();rng=random.Random(4501)
    rows=tool.corpus();seeds=[(ROOT/x['binding']['path']).read_bytes() for x in rows]
    started=time.perf_counter();tracemalloc.start();max_latency=0;accepted=refused=go_accepted=go_refused=0;categories={}
    # Compile the unchanged reader before measurement samples; no original VM.
    inherited.bridge()
    with tempfile.TemporaryDirectory(prefix='wordling-wp45-fuzz-') as directory:
        path=Path(directory)/'synthetic-input'
        for i in range(1000):
            raw=bytearray(seeds[rng.randrange(len(seeds))])
            if i%8==0:raw=raw[:rng.randrange(len(raw)+1)]
            elif i%8==1:raw.extend(b'X'*rng.randrange(65537-len(raw)))
            else:
                for _ in range(1+rng.randrange(4)):
                    if raw:raw[rng.randrange(len(raw))]^=1<<rng.randrange(8)
            at=time.perf_counter()
            try:
                result=tool.diagnose(bytes(raw),inspector)
                assert result['mutation_permission'] is False and result['body_reference_absence_proven'] is False
                accepted+=1
            except ValueError as error:
                refused+=1;code=getattr(error,'code',type(error).__name__);categories[code]=categories.get(code,0)+1
            max_latency=max(max_latency,time.perf_counter()-at)
            if i<64:
                path.write_bytes(raw);reader=inherited.actual_reader(path)
                if reader['accepted']:
                    assert reader['exact_export'] and reader['sha256']==tool.digest(raw);go_accepted+=1
                else:go_refused+=1
    current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    data={'seed':4501,'iterations':1000,'diagnostics_returned_read_only':accepted,'diagnostic_refusals':refused,'refusal_categories':categories,'actual_go_reader_samples':64,'actual_go_reader_accepted_exact':go_accepted,'actual_go_reader_refused':go_refused,'wall_seconds':time.perf_counter()-started,'max_diagnostic_seconds':max_latency,'python_tracemalloc_peak_bytes':peak,'VM_launched':False,'mutation_permission':False,'scope':'synthetic finite diagnostics only; not new original evidence/product decoder fuzz/peak RSS or DOS capacity'}
    out=ROOT/'docs/research/continuation/resaved-prefix-relationships/evidence/fuzz.json';out.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
if __name__=='__main__':main()
