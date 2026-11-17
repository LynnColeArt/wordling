#!/usr/bin/env python3
"""Finite semantic mutants in disposable real Go module compositions only."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT=Path(__file__).resolve().parents[4]
OWNED=ROOT/'docs/research/continuation/explicit-secondary-data'
CORE='internal/merge/explicit/data.go'
CONSUMER='internal/merge/explicit/evidence/qualify/main.go'
core=(ROOT/CORE).read_text();consumer=(ROOT/CONSUMER).read_text()

def replace(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new,1)

def foreign(text):
    text=replace(text,'return Data{&proof{captured, info}}, nil','foreign, _ := native.Parse(captured.Export(), native.DefaultLimits()); foreignView, _ := foreign.View(native.Secondary); foreignInfo, _ := foreignView.Inspect(); info.Records[0].Fields[0].Content = foreignInfo.Records[0].Fields[0].Content\n\treturn Data{&proof{captured, info}}, nil')
    text=replace(text,'b, ok := v.proof.view.Bytes(v.proof.info.Records[v.record].Fields[v.field].Content)','span, _ := v.proof.info.Records[v.record].Fields[v.field].Content.Bounds(); raw := v.proof.view.Export(); b, ok := raw[span.Offset:span.Offset+span.Length], true')
    return text

def alias(text):
    text=replace(text,'type proof struct {','var mutantReturned = map[native.Span][]byte{}\n\ntype proof struct {')
    text=replace(text,'\treturn b, nil\n}\nfunc (v Value) ExplicitlyEmpty', 'key := v.proof.info.Records[v.record].Fields[v.field].Content; if previous, exists := mutantReturned[key]; exists { return previous, nil }; mutantReturned[key] = b; return b, nil\n}\nfunc (v Value) ExplicitlyEmpty')
    return text

mutants=[
 ('missing-is-empty',CORE,lambda s:replace(s,'return Value{}, &ExplicitFieldMissing{recordOrdinal, fieldOrdinal}','return Value{d.proof, 0, 0}, nil'),'TestPresenceSourceCaptureAndCopies'),
 ('count-minus-one-provenance',CORE,lambda s:replace(s,'return d.proof.view.Inspect()','info, ok := d.proof.view.Inspect(); for j := range info.Records { info.Records[j].StoredCount-- }; return info, ok'),'TestFiniteAdmissionMemory'),
 ('source-identity-dropped',CORE,lambda s:replace(s,' || !info.Source.Equal(expected)',''),'TestPresenceSourceCaptureAndCopies'),
 ('foreign-span-numeric-offset',CORE,foreign,'TestLargeAdmissionAndSpanOwnership'),
 ('returned-mutable-alias',CORE,alias,'TestPresenceSourceCaptureAndCopies'),
 ('whole-coverage-dropped',CORE,lambda s:replace(s,'if c.at != c.eof || c.token != len(info.Tokens) || c.command != len(info.Commands) || c.finding != len(info.Findings) {','if false {'),'TestReaderValidRefusals'),
 ('opaque-profile-dropped',CORE,lambda s:replace(s,'if !opaqueProfile(opaque) {','if false && !opaqueProfile(opaque) {'),'TestReaderValidRefusals'),
 ('findings-omitted',CORE,lambda s:replace(s,'return d.proof.view.Inspect()','info, ok := d.proof.view.Inspect(); info.Findings = nil; return info, ok'),'TestFiniteAdmissionMemory'),
 ('generic-blocker-falsified',CONSUMER,lambda s:replace(s,'out.GenericSupported = view.Supported()','out.GenericSupported = true'),'TestActualQualificationPath'),
 ('fixture-digest-shortcut',CORE,lambda s:replace(replace(s,'"bytes"','"bytes"\n "crypto/sha256"'),'whole := captured.Export()','whole := captured.Export(); if fmt.Sprintf("%x", sha256.Sum256(whole)) != "9fb545e4d2091be214d88acd1404e7609de2656319027ee95352f2658b1f7cca" { return Data{}, refused("FixtureShortcut") }'),'TestPresenceSourceCaptureAndCopies'),
 ('workflow-observer-value-replay',CONSUMER,lambda s:replace(s,'empty, e := value.ExplicitlyEmpty()','if f == 1 { b = []byte("Alice") }; empty, e := value.ExplicitlyEmpty()'),'TestActualQualificationPath'),
 ('all-space-accepted',CORE,lambda s:replace(s,'if spaces || f.Ordinal != fi+1','if f.Ordinal != fi+1'),'TestReaderValidRefusals'),
 ('literal-count-pair-dropped',CORE,lambda s:replace(s,'if !((r.StoredCount == 2 && len(r.Fields) == 1) || (r.StoredCount == 3 && len(r.Fields) == 2)) {','if false {'),'TestReaderValidRefusals'),
]

def main():
    before={p:str(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in [CORE,CONSUMER]}
    results=[]
    for name,path,change,test in mutants:
        started=time.monotonic()
        with tempfile.TemporaryDirectory(prefix='wordling-wp67-mutant-') as directory:
            target=Path(directory)
            files=['go.mod','go.sum','internal/wp51/native.go','internal/merge/native/image.go','internal/merge/native/view.go','internal/merge/native/semantic.go']
            files += [str(p.relative_to(ROOT)) for p in (ROOT/'internal/merge/explicit').rglob('*.go')]
            corpus=json.loads((OWNED/'corpus.json').read_text())
            files += ['docs/research/continuation/explicit-secondary-data/corpus.json']
            files += list({pair['source_paths']['Secondary'] for pair in corpus['paired']})
            for f in files:
                q=target/f;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/f,q)
            (target/path).write_text(change((target/path).read_text()))
            package='./internal/merge/explicit/evidence/qualify' if path==CONSUMER else './internal/merge/explicit'
            command=['go','test','-count=1','-run','^'+test+'$',package]
            r=subprocess.run(command,cwd=target,capture_output=True,timeout=30,text=True)
            valid='[build failed]' not in r.stdout+r.stderr and 'undefined:' not in r.stderr and 'syntax error' not in r.stderr
            killed=valid and r.returncode!=0 and '--- FAIL: '+test in r.stdout
            results.append({'name':name,'path':path,'test':test,'argv':command,'cwd':str(target),'status':r.returncode,'compile_valid':valid,'runtime_killed':killed,'stdout':r.stdout,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-started})
            (OWNED/'mutants2-progress.json').write_text(json.dumps(results,indent=2)+'\n')
    after={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in before}
    assert before==after
    out={'source_before':before,'source_after':after,'mutants':results,'all_runtime_killed':all(x['runtime_killed'] for x in results),'no_old_source_mutated':True}
    (OWNED/'mutants2.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'valid':sum(x['compile_valid'] for x in results),'killed':sum(x['runtime_killed'] for x in results),'total':len(results)}))
    return 0 if out['all_runtime_killed'] else 1
if __name__=='__main__':raise SystemExit(main())
