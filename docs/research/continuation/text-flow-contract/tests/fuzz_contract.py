"""Declared seed4901/500 bounded new-wrapper diagnostics; no native file or guest."""
from pathlib import Path
import json,random,sys,time,tracemalloc
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'scripts/reference'))
import text_flow_contract as t

def main():
    c=t.Custody();tokenizer,analyzer=t.helpers(c);catalog=c.json(t.BASE+'/analysis.json');seeds=[]
    for pair in catalog['repeated_variants']:
        run=c.json(t.BASE+'/runs/'+pair['run_ids'][0]+'/run.json')
        for state in run['states']:seeds.append(c.read(t.BASE+'/runs/'+run['run_id']+'/'+state['native_after_print']))
    defs=c.json('docs/research/continuation/native-edits/field-ledger.json',t.WP43)['field_coverage'];rng=random.Random(4901);accepted=refused=0;codes={};started=time.perf_counter();tracemalloc.start();peak_time=0
    for i in range(500):
        raw=rng.choice(seeds);B=int.from_bytes(raw[4:8],'little');body=bytearray(raw[B:B+2048])
        if i%5==0:body=body[:rng.randrange(len(body)+1)]
        elif i%5==1:body.extend(rng.randbytes(rng.randrange(min(256,2048-len(body))+1)))
        else:
            for _ in range(1+rng.randrange(3)):
                if body:body[rng.randrange(len(body))]^=1<<rng.randrange(8)
        at=time.perf_counter()
        try:
            d=t.observe_native(raw[:B]+body,tokenizer,analyzer);t.prefix_font_fields(raw[:B]+body,tokenizer,defs);assert d['generator_permission']is False;accepted+=1
        except ValueError as e:
            refused+=1;code=getattr(e,'code',type(e).__name__);codes[code]=codes.get(code,0)+1
        peak_time=max(peak_time,time.perf_counter()-at)
    _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    result={'seed':4901,'iterations':500,'read_only_diagnostics':accepted,'refusals':refused,'codes':codes,'wall_seconds':time.perf_counter()-started,'maximum_observed_diagnostic_seconds':peak_time,'Python_tracemalloc_peak_bytes':peak,'body_bytes_max':2048,'mutations_max':3,'scope':'synthetic wrapper/unchanged outer-token diagnostic only; no original, product decoder, geometry/RSS/DOS or permission proof','guest_attempts':0}
    (t.OUT/'evidence/fuzz.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
