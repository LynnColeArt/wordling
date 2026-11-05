"""Closed prospective DATA/file and harmless toy-OS controls, disabled by default.
No candidate/fixture/P/provider import, issuer/store/grant or production capture.
Exact programs/source/roster must be frozen and ROOT separately authorize execution.
"""
import argparse
import copy
import ast
import hashlib
import json
import os
from pathlib import Path
import signal
import time
import runtime_qualification as q

CONTROL_ORIGIN=time.monotonic()
ROOT=Path('/tmp/wordling-WP70-v11-retention-controls')
_CONTROL_HANDLES=[]
TOYS={
 'Popen-failure-with-survivor-reserve':None,
 'earlier4096-output-threechannel-overflow':"import os;os.write(1,b'x'*1500);os.write(2,b'y'*1500);fd=int(os.environ['WORDLING_PREPARATION_CONTROL_FD']);os.write(fd,b'{\"event\":\"idle\"}\\n'*128)",
 'metadata-failure-coordinator-abort':"import os;os.write(int(os.environ['WORDLING_PREPARATION_CONTROL_FD']),b'{\"event\":\"abort\"}\\n')",
 'coordinator-SIGKILL-retainedleader':"import subprocess,time;subprocess.Popen(['/usr/bin/python3','-B','-c','import time;time.sleep(10)']);time.sleep(10)",
 'ignoredTERM-shareddeadline-escalation':"import signal,subprocess,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);subprocess.Popen(['/usr/bin/python3','-B','-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(10)']);time.sleep(10)",
 'preflight-refusal-no-child-effect':None,
 'census-unavailable-recovery':"import signal,subprocess,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);subprocess.Popen(['/usr/bin/python3','-B','-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(10)']);time.sleep(10)",
 'unterminated-control-recovery':"import os;os.write(int(os.environ['WORDLING_PREPARATION_CONTROL_FD']),b'z'*16385)",
 'parse-failure-coordinator-abort':None,
}


def DATA():
    start=time.monotonic();end=start+30;ROOT.mkdir(mode=0o700,exist_ok=False)
    expected=q.load_expected();selection=q.bounded_json_loads(Path(__file__).with_name('runtime_tool_selection.json').read_bytes(),1048576,True)
    results=[]
    def check(name,fn,want=None):
        if time.monotonic()>=end:raise RuntimeError('DATAAggregateDeadline')
        try:fn();actual=None
        except RuntimeError as error:actual=str(error)
        if actual!=want:raise AssertionError((name,want,actual))
        results.append(dict(id=name,status='PASS',reason=actual))
    # Fixed synthetic startup projection; no interpreter execution or candidate path lookup.
    interpreter=ROOT/'venv/bin/python';base=dict(version=[3,12,14],executable=str(interpreter),prefix=str(interpreter.parent.parent),exec_prefix=str(interpreter.parent.parent),base_prefix=str(q.PREFIX),base_exec_prefix=str(q.PREFIX),sys_path=[str(q.PREFIX/'lib/python312.zip'),str(q.PREFIX/'lib/python3.12'),str(q.PREFIX/'lib/python3.12/lib-dynload'),str(interpreter.parent.parent/'lib/python3.12/site-packages')],flags=dict(debug=0,inspect=0,interactive=0,optimize=0,dont_write_bytecode=1,no_user_site=1,no_site=0,ignore_environment=1,verbose=0,bytes_warning=0,quiet=0,hash_randomization=1,isolated=1,dev_mode=False,utf8_mode=0,warn_default_encoding=0,safe_path=True,int_max_str_digits=4300),default_excepthook=True,customize=dict(sitecustomize=False,usercustomize=False,_distutils_hack=False),features={n:True for n in q.FEATURES+('socket.AF_UNIX','socket.SOL_SOCKET','socket.SO_PEERCRED','socket.SO_ERROR','select.poll','select.POLLHUP','select.POLLERR')},modules={},maps={},project=None)
    for role in ('module','map'):
        for row in selection['new_tool_records']:
            obs=copy.deepcopy(base);name=row['path']
            if role=='module':obs['modules']={'synthetic_selected_tool':{'__file__':dict(exists=True,path=name,size=row['size'],sha256=row['sha256'])}};want='UnexpectedModuleOrigin:synthetic_selected_tool:'+name
            else:obs['maps']={name:dict(size=row['size'],sha256=row['sha256'])};want='UnexpectedMappedELF:'+name
            check(role+':'+name,lambda obs=obs:q.compare_observation(obs,interpreter,expected,{},False),want)
    initial='7 execve("/DATA/tool", ["/DATA/tool"], 0x0) = 0\n';proc='7 openat(AT_FDCWD</DATA>, "/proc/self/maps", O_RDONLY) = 3</proc/7/maps>\n';launch=['/DATA/tool']
    frames=[('exact-initial-selfmaps-positive',initial+proc,None),('failed-initial-exec',initial.replace(' = 0\n',' = -1 ENOENT (missing)\n')+proc,'WrongOrFailedInitialPinnedExec'),('missing-initial-exec',proc,'WrongOrFailedInitialPinnedExec'),('wrong-initial-argv',initial.replace('["/DATA/tool"]','["wrong"]')+proc,'WrongOrFailedInitialPinnedExec'),('successful-reexec-beforemaps',initial+initial+proc,'UnapprovedProcOrigin'),('foreignmaps',initial+proc.replace('/proc/7/','/proc/8/'),'UnapprovedProcOrigin'),('lineaged-descendantmaps',initial+'7 clone(child_stack=NULL, flags=SIGCHLD) = 8\n'+proc.replace('7 ','8 ',1).replace('/proc/7/','/proc/8/'),'UnapprovedProcOrigin'),('literalflagswrong',initial+proc.replace('O_RDONLY','O_RDWR'),'UnapprovedProcOrigin'),('device-path-only-/dev/null',initial+'7 openat(AT_FDCWD</DATA>, "/dev/null", O_RDWR) = 3</dev/null>\n',None),('legacy-yy-device-refusal',initial+'7 openat(AT_FDCWD</DATA>, "/dev/null", O_RDWR) = 3</dev/null<char 1:3>>\n','MissingKernelResolvedOpenOrigin'),('unfinished-resumed-joined',initial+'7 openat(AT_FDCWD, "/proc/self/maps", O_RDONLY <unfinished ...>\n7 <... openat resumed>) = 3</proc/7/maps>\n',None),('unmatched-resumed',initial+'8 <... openat resumed>) = 3</proc/7/maps>\n','UnmatchedResumedTrace'),('truncated-tail',(initial+proc)[:-1],'TruncatedTraceTail'),('historical-unlisted-successful-code',initial+'7 openat(AT_FDCWD, "/UNLISTED", O_RDONLY) = 3</UNLISTED>\n','HistoricalUnknownStableOrigin:/UNLISTED'),('failed-open-retained-noauthority',initial+'7 openat(AT_FDCWD, "/UNLISTED", O_RDONLY) = -1 ENOENT (missing)\n',None),('successful-fork-control-retained',initial+'7 fork() = 8\n',None),('setsid-refusal',initial+'7 setsid() = 7\n','UnsupportedToolContainmentOrOrigin:setsid'),('setpgid-refusal',initial+'7 setpgid(0, 0) = 0\n','UnsupportedToolContainmentOrOrigin:setpgid'),('memfd-refusal',initial+'7 memfd_create("DATA", 0) = 3\n','UnsupportedToolContainmentOrOrigin:memfd_create')]
    for name,raw,want in frames:check('G1:'+name,lambda raw=raw:q.historical_data_review(raw,launch,['/DATA/tool','/dev/null']),want)
    check('G1:opaque-currentcapture-missing',lambda:object.__new__(q.Preparation).tool_origins('/DATA/NOQUERY','DATA',{'complete':True}),'MissingGenuineOwnedCapture')
    # Real pure pretool catalog invariant; only changed shallow rows copied.
    check('G3:old20278rows-exact-plus200',lambda:q.check_selection_records(expected,selection))
    def changed_file(path,key,value):
        e=dict(expected);e['files']=dict(expected['files']);e['files'][path]=dict(e['files'][path]);e['files'][path][key]=value;return e
    e=dict(expected);e['files']=dict(expected['files']);e['files']['/usr/EXTRA201ST']=dict(next(iter(e['files'].values())))
    check('G3:extra201st',lambda:q.check_selection_records(e,selection),'LegacyExternalSubsetChanged')
    first=selection['new_tool_records'][0]['path'];e=dict(expected);e['files']=dict(expected['files']);del e['files'][first]
    check('G3:missingselected',lambda:q.check_selection_records(e,selection),'ToolRecordMismatch')
    for key,value in [('sha256','0'*64),('mode',0),('uid',99),('gid',99)]:
        e=changed_file(first,key,value);check('G3:changed'+('hash' if key=='sha256' else key),lambda e=e:q.check_selection_records(e,selection),'ToolRecordMismatch')
    for name,field in [('runtimeELFgrowth','runtime_elf'),('runtimeDATAgrowth','runtime_mapped_data')]:
        e=dict(expected);e[field]=expected[field]+[first];check('G3:'+name,lambda e=e:q.check_selection_records(e,selection),'ToolRuntimeRoleGrowth')
    e=dict(expected);e['approved_providers']=dict(expected['approved_providers'],FORGED='0'*40);check('G3:providerclassgrowth',lambda:q.check_selection_records(e,selection),'ToolRuntimeRoleGrowth')
    pair=selection['opaque_cache_pairs'][1];header=bytes.fromhex('cb0d0d0a')+bytes(4)+pair['header_mtime'].to_bytes(4,'little')+pair['header_size'].to_bytes(4,'little');statdata=dict(size=pair['header_size'],mtime_ns=pair['header_mtime']*1000000000)
    e=changed_file(pair['cache'],'sha256','0'*64);check('G3:opaque-cachebyteschanged',lambda:q.check_selection_records(e,selection),'ToolRecordMismatch')
    e=changed_file(pair['source'],'sha256','0'*64);check('G3:sourcecounterpartchanged',lambda:q.check_selection_records(e,selection),'ToolRecordMismatch')
    for name,h,st in [('magicchanged',b'BAD!'+header[4:],statdata),('flagschanged',header[:4]+b'\x01\0\0\0'+header[8:],statdata),('timestampchanged',header[:8]+bytes(4)+header[12:],statdata),('source-sizechanged',header,dict(statdata,size=statdata['size']+1))]:check('G3:'+name,lambda h=h,st=st:q.check_tool_pair(h,st,pair),'ToolCacheHeader' if name in ('magicchanged','flagschanged') else 'ToolCacheMetadata')
    model=dict(selection);model['opaque_cache_pairs']=selection['opaque_cache_pairs'][:-1];check('G3:pairmissing',lambda:q.check_selection_records(expected,model),'Exact54ToolCachePairs')
    check('G3:copy-policyforeign',lambda:object.__new__(q.Preparation).tool_origins('/DATA/NOQUERY','DATA',dict(selection)),'MissingGenuineOwnedCapture')
    # Exact immutable reference leaf/control DATA, all paths in newly owned ROOT.
    ref=ROOT/'reference.DATA';ref.write_bytes(b'EXACT');wanted=dict(size=5,sha256=hashlib.sha256(b'OTHER').hexdigest(),mode=ref.stat().st_mode&0o777,uid=os.getuid(),gid=os.getgid())
    check('G3:referencechanged',lambda:q.same(ref,wanted),'ChangedInput:'+str(ref))
    root=dict(root=str(ROOT),count=1,bytes=5,members=[dict(relative='reference.DATA',path=str(ref),bytes=5,mode=ref.stat().st_mode&0o777,uid=os.getuid(),gid=os.getgid(),sha256=hashlib.sha256(b'EXACT').hexdigest())],policy='DATA')
    cyc=copy.deepcopy(root);cyc['members'][0]['reference']='SELF';check('G3:referencecycle',lambda:q.check_reference_shape(dict(canonical_reference_roots=[cyc])),'ReferenceSchema')
    check('G3:referenceambiguous',lambda:q.check_reference_shape(dict(canonical_reference_roots=[root,root])),'ReferenceAmbiguous')
    check('G3:referenceoutofbound',lambda:q.check_reference_shape(dict(canonical_reference_roots=[root]*65)),'ReferenceCardinality')
    # All eighteen writer roles exercise the same real reserve/stream implementation.
    kinds=['construction_raw','functional_raw','command','whole','origin','transient','inventory','deployment','build_freeze','compiled_data','custody','aggregate','misc','input_refs','catalog_seal','review_allocation','control_allocation','failure_disposition']
    kindmap={'command':'pair','whole':'pair','build_freeze':'build','compiled_data':'compiled','input_refs':'input','catalog_seal':'catalog','review_allocation':'review','control_allocation':'control','failure_disposition':'failure'}
    codec_book=q.EvidenceBudget([ROOT]);codec_allocation,codec_handles=codec_book.raw_group([ROOT/'metadata-codec-payloads.jsonl'],'control',131072)
    codec_handle=next(iter(codec_handles.values()));_CONTROL_HANDLES.append(codec_handle)
    def record_codec(record):
        q.measure_json(record,8192)
        data=bytearray()
        for part in q._json_parts(record):
            piece=part.encode('ascii')
            if len(data)+len(piece)+1>8192:raise RuntimeError('CodecRecordBound')
            data.extend(piece)
        data.extend(b'\n')
        q.EvidenceBudget.retain(codec_allocation,bytearray(),codec_handle,bytes(data));os.fsync(codec_handle.fileno())
    for label in kinds:
        kind=kindmap.get(label,label)
        for edge in ('exact','plus-one'):
            folder=ROOT/(label+'-'+edge);folder.mkdir();book=q.EvidenceBudget([folder],earlier_document_cap=4096);path=folder/'DATA.json'
            if kind in ('construction_raw','functional_raw'):
                def raw_case(book=book,path=path,kind=kind,edge=edge):
                    allocation,handles=book.raw_group([path],kind,4096)
                    try:q.EvidenceBudget.retain(allocation,bytearray(),handles[path],b'x'*(4096 if edge=='exact' else 4097))
                    finally:handles[path].close()
                check('writer:'+label+':'+edge,raw_case,None if edge=='exact' else 'PreparationLiveOutputBound')
            else:
                value='x'*(4093 if edge=='exact' else 4094)
                check('codec-class-preflight:'+label+':'+edge,lambda value=value:q.measure_json(value,4096),None if edge=='exact' else 'MetadataEncodedBound')
                if edge=='exact':record_codec(dict(kind=kind,scope='REAL CODEC PREFLIGHT ONLY; document consumes sameproducer; no claim thiscaseemitted via document',encoded_payload=''.join(q._json_parts(value))+'\n'))
    # Numerical/class/global preallocation and framing boundaries.
    for name,basefiles,basebytes,count,amount,want in [('filecount-exact',q.EVIDENCE_FILES-1,0,1,0,None),('filecount-plusone',q.EVIDENCE_FILES,0,1,0,'EvidenceTotalCapacity'),('class-total-exact',0,0,1,q.CLASS_LIMITS['failure'][0],None),('class-total-plusone',0,0,1,q.CLASS_LIMITS['failure'][0]+1,'EvidenceClassCapacity'),('global-total-exact',0,q.EVIDENCE_LIMIT-1,1,1,None),('global-total-plusone',0,q.EVIDENCE_LIMIT,1,1,'EvidenceTotalCapacity')]:
        folder=ROOT/name;folder.mkdir();book=q.EvidenceBudget([folder],basebytes,basefiles);check('bound:'+name,lambda book=book,folder=folder,amount=amount:book.reserve([folder/'DATA'],'failure',amount),want)
    b=q.EvidenceBudget([ROOT]);b.reserve([ROOT/'old.DATA'],'pair',64);check('bound:replacement-two-generation-coexistence',lambda:b.reserve([ROOT/'old.DATA'],'pair',64),'EvidenceNoClobberReservation')
    b=q.EvidenceBudget([ROOT]);b.reserve([ROOT/'full.DATA'],'pair',q.CLASS_LIMITS['pair'][0]);check('bound:no-borrowing-otherclass',lambda:b.reserve([ROOT/'more.DATA'],'pair',1),'EvidenceClassCapacity')
    extra=[('trace-record-plusone',lambda:q.parse_trace('7 fork() = 8\n'*16385),'TraceRecordCardinality'),('trace-line-plusone',lambda:q.parse_trace('7 '+('x'*16384)+'\n'),'TraceLexemeBound'),('JSON-depth-plusone',lambda:q.bounded_json_loads('['*17+'0'+']'*17),'JSONDepthBound'),('JSON-token-plusone',lambda:q.bounded_json_loads('['+','.join('0' for _ in range(32769))+']'),'JSONTokenBound'),('JSON-string-plusone',lambda:q.bounded_json_loads('"'+'x'*8193+'"'),'JSONStringBound'),('argv-count-plusone',lambda:q._exec_argv(', ['+','.join('""' for _ in range(257))+']',0),'ExecArgvBound'),('encoder-chunk-plusone',lambda:list(q._json_parts('x'*16385)),'MetadataStringBound'),('prepared-memory-charge-plusone',lambda:q._trace_allocation_bound('x'*(q.CONSTRUCTION_RAW_LIMIT*2)+'\n'*16384),'PreparedMemoryCharge')]
    for name,fn,want in extra:check('bound:'+name,fn,want)
    for name in ['reserved-receipt-positive-1','reserved-receipt-positive-2','reserved-receipt-positive-3']:
        folder=ROOT/name;folder.mkdir();book=q.EvidenceBudget([folder]);path=folder/'whole.json';book.reserve([path],'custody',65536);check('bound:'+name,lambda book=book,path=path:book.document(path,dict(status='RESERVED_RECEIPT_POSITIVE_ONLY',details='NO FAILURE IN THIS DATA CASE'),'custody',True))
    b=q.EvidenceBudget([ROOT],q.EVIDENCE_LIMIT,q.EVIDENCE_FILES);check('bound:missing-survivor-reserve-no-Popen',lambda:b.reserve([ROOT/'nochild.whole.json'],'custody',65536),'EvidenceTotalCapacity')
    # Three declared Unicode edges and one revised keys+values node edge.
    check('Unicode:nonBMP-12byte-escape-positive',lambda: (_ for _ in ()).throw(RuntimeError('UnicodeBound')) if ''.join(q._json_parts('\U0001f600'))!='"\\ud83d\\ude00"' else None)
    check('Unicode:control-character-escaping-bound',lambda: (_ for _ in ()).throw(RuntimeError('UnicodeBound')) if ''.join(q._json_parts('\x00'))!='"\\u0000"' else None)
    check('Unicode:lone-surrogate-refusal',lambda:list(q._json_parts('\ud800')),'MetadataLoneSurrogate')
    check('bound:expected-node-limit-plusone',lambda:q.bounded_json_loads('['+','.join('0' for _ in range(524288))+']',8388608,True),'JSONNodeBound')
    # F7 exact/+1 fences through the genuine lexical consumer.
    for count in (1024,1025):
        raw=initial+'7 openat(AT_FDCWD, "/DATA/known", '+('F'*count)+') = 3</DATA/known>\n'
        check('F7:flags-'+str(count),lambda raw=raw:q.parse_trace(raw),None if count==1024 else 'TraceFlagsBound')
    for name,flags,want in [('flags-UTF8-1024','\u00e9'*512,None),('flags-UTF8-1025','\u00e9'*512+'x','TraceFlagsBound')]:
        raw=initial+'7 openat(AT_FDCWD, "/DATA/known", '+flags+') = 3</DATA/known>\n'
        check('F7:'+name,lambda raw=raw:q.parse_trace(raw),want)
    for count in (20,21):
        raw=initial+'7 fork() = '+('1'*count)+'\n'
        check('F7:integer-'+str(count),lambda raw=raw:q.parse_trace(raw),None if count==20 else 'TraceIntegerBound')
    # F8 completeliteral text/AST, never executing assertions or fake sys.prefix.
    import controller_deployment as deployment_source
    template=ast.parse(q.QUALIFY_LITERAL)
    def without_V(tree):return ast.dump(ast.Module(body=[n for n in tree.body if not isinstance(n,ast.Assign) or not any(isinstance(t,ast.Name) and t.id=='V' for t in n.targets)],type_ignores=[]),include_attributes=False)
    contexts=[q.TARGET,Path('/tmp/wordling-WP70-binding-DATA'),Path('/tmp/wordling-WP70-binding-DATA/deployment-cached-deployment'),Path('/tmp/wordling-WP70-binding-DATA/deployment-foreign-deployment')]
    roster=q.bounded_json_loads(Path(__file__).with_name('controller_roster.json').read_bytes())
    contexts += [Path('/tmp/wordling-WP70-binding-DATA/mutants')/n/'runtime' for n in roster['mutants']]
    assert len(contexts)==12
    for index,target in enumerate(contexts):
        def binding(target=target):
            tree=ast.parse(q.qualification_literal(target));assert without_V(tree)==without_V(template)
            node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='V' for t in n.targets))
            assert ast.literal_eval(node.value.args[0])==str(target/'venv')
        check('F8:complete-target-binding-'+str(index),binding)
    # Static actual producer, no deployment/compile invocation.
    def build_cap_source():
        source=ast.parse(Path(deployment_source.__file__).read_text());found=[]
        for n in ast.walk(source):
            if isinstance(n,ast.keyword) and n.arg=='combined_output':found.append(ast.dump(n.value,include_attributes=False))
        assert found==[ast.dump(ast.Attribute(value=ast.Name(id='context',ctx=ast.Load()),attr='output_cap',ctx=ast.Load()),include_attributes=False)]
    check('F3:build-freeze-current-context-cap',build_cap_source)
    # New controls use actual diagnostic producer+emitter; originaltraceback UNKNOWN.
    fd=os.open(ROOT/'diagnostic-emission.raw',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    try:
        baseline=q.generated_diagnostic(RuntimeError(''),256);capacity=baseline['content_capacity']
        class NoFormat:
            def __repr__(self):raise AssertionError('arbitraryreprcalled')
        diagnostics=[('exact',RuntimeError('x'*capacity),False),('plus-one',RuntimeError('x'*(capacity+1)),True),('nonBMP',RuntimeError('\U0001f600'*256),True),('controls',RuntimeError('\x00\n'*256),True),('surrogate',RuntimeError('\ud800'*256),True),('unknown-nonstr',RuntimeError(NoFormat()),True)]
        for name,error,omitted in diagnostics:
            def diagnostic_case(error=error,omitted=omitted):
                record=q.generated_diagnostic(error,256);assert record['bytes']<=256 and record['omitted']==omitted and record['original_traceback']=='UNKNOWN'
                if omitted:assert record['text'].endswith('[OMITTED; original traceback UNKNOWN]')
                # Same producer, explicit earliercap, actual own-file emission.
                emitted=q.emit_diagnostic(error,fd=fd,maximum=256);assert emitted==record
            check('F2:generated-emission-'+name,diagnostic_case)
    finally:os.close(fd)
    from runtime_qualification_supervisor import ControlFrames
    check('F5:pending-exact256',lambda:ControlFrames().feed(b'x'*256))
    check('F5:pending-plusone257',lambda:ControlFrames().feed(b'x'*257),'SupervisorPendingFrameBound')
    def pending_EOF():
        decoder=ControlFrames();decoder.feed(b'x');decoder.finish()
    check('F5:unterminated-EOF',pending_EOF,'SupervisorIncompleteControlFrame')
    if len(results)!=530:raise AssertionError(('DATA-roster-count',len(results)))
    output=dict(groups=5,variants=results,synthetic_DATA=True,candidate_runtime=False,production_capture=False,P=False,elapsed=time.monotonic()-start)
    book=q.EvidenceBudget([ROOT])
    q.measure_json(output,262144);book.document(ROOT/'results.json',output,'control')
    codec_handle.close()
    print(json.dumps(dict(groups=5,variants=len(results),status='PASS',result_sha256=hashlib.sha256((ROOT/'results.json').read_bytes()).hexdigest(),elapsed=time.monotonic()-start,TCB=False,P=False)))



def signal_metadata_controls():
    """Three synthetic metadata-only codec boundaries; no PID/capture/authority."""
    guardian_source=Path(__file__).with_name('runtime_qualification_supervisor.py')
    tree=ast.parse(guardian_source.read_text())
    records=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='dict' and any(k.arg=='event' and isinstance(k.value,ast.Constant) and k.value.value=='before_group_signal' for k in n.keywords)]
    assert len(records)==1
    field=next(k.value for k in records[0].keywords if k.arg=='signal')
    assert ast.dump(field,include_attributes=False)==ast.dump(ast.Call(func=ast.Name(id='int',ctx=ast.Load()),args=[ast.Name(id='sig',ctx=ast.Load())],keywords=[]),include_attributes=False)
    variants=[('old-SIGTERM-enum-refusal',signal.SIGTERM,'MetadataType'),('recorded-TERM-exact-int',int(signal.SIGTERM),None),('recorded-KILL-exact-int',int(signal.SIGKILL),None)]
    for name,value,want in variants:
        # Synthetic shape deliberately has no leader/PID/owned-child/stop fields.
        record=dict(leader_identity_events=[dict(event='before_group_signal',signal=value)])
        try:
            q.measure_json(record,4096);payload=''.join(q._json_parts(record))+'\n';actual=None
        except RuntimeError as error:actual=str(error);payload=None
        assert actual==want,(name,actual,want)
        print(json.dumps(dict(metadata_case=name,status='PASS',reason=actual,encoded_payload=payload,synthetic_DATA=True,production_capture=False,P=False)),flush=True)
    print(json.dumps(dict(status='SIGNAL_METADATA_COMPLETE',variants=3,synthetic_DATA=True,P=False)),flush=True)


def OS(case,shared_end=None):
    if case not in TOYS:raise RuntimeError('ClosedOSRoster')
    import runtime_qualification_supervisor as guardian
    root=ROOT/('OS-'+case);root.mkdir(parents=True,exist_ok=False);book=q.EvidenceBudget([root])
    if shared_end is not None and shared_end-time.monotonic()<2.5:raise RuntimeError('OSAggregateDeadlineBeforeCase')
    if case=='preflight-refusal-no-child-effect':
        denied=q.EvidenceBudget([root],q.EVIDENCE_LIMIT,q.EVIDENCE_FILES)
        try:guardian.supervise(['/usr/bin/python3','-B','-c','raise AssertionError(\"MUST_NOT_START\")'],'/tmp',{},root/'guardian',seconds=.5,budget=denied)
        except RuntimeError as error:assert str(error)=='EvidenceTotalCapacity'
        else:raise AssertionError('PopenAllowedWithoutReserve')
        print(json.dumps(dict(case=case,status='PASS',child_started=False)));return
    argv=['/usr/bin/python3','-B','-c',TOYS[case]] if TOYS[case] else [str(root/'MISSING-OWN-EXECUTABLE')]
    if case=='metadata-failure-coordinator-abort':argv=['/usr/bin/python3','-B',str(Path(__file__)),'--toy-metadata-abort']
    if case=='parse-failure-coordinator-abort':argv=['/usr/bin/python3','-B',str(Path(__file__)),'--toy-parse-abort']
    env=dict(PATH='/usr/bin:/bin',HOME='/tmp',LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
    try:r=guardian.supervise(argv,'/tmp',env,root/'guardian',seconds=.5,output_cap=4096,control='kill-coordinator' if case=='coordinator-SIGKILL-retainedleader' else None,budget=book,fault='census-unavailable-on-cleanup' if case=='census-unavailable-recovery' else None,earlier_end=None if shared_end is None else shared_end-2)
    except RuntimeError as error:
        if case!='Popen-failure-with-survivor-reserve' or str(error)!='SupervisorPopenOrAdmissionFailure':raise
        r=q.bounded_json_loads((root/'guardian/whole.json').read_bytes());assert r['child_started'] is False
    else:
        if case=='census-unavailable-recovery':
            assert r['owned_child_census']=='UNKNOWN' and r['census_fault_injected'] and not r['cleanup_qualified'] and r['unknown_cleanup_hold']
            assert r['kernel_no_children_observed'] and r['owned_children_remaining'] is None
            assert any(x['event']=='before_group_signal' and x['signal']==signal.SIGKILL and x['retained_direct_child'] for x in r['leader_identity_events'])
        else:assert r['coordinator_reaped_last'] and not r['owned_children_remaining'] and r['cleanup_qualified'],r
        if case=='earlier4096-output-threechannel-overflow':assert r['partial_prefix'] and r['retained_bytes']<=4096
        if case=='ignoredTERM-shareddeadline-escalation':assert r['escalated']
        if case in ('metadata-failure-coordinator-abort','parse-failure-coordinator-abort'):
            assert b'\"event\": \"abort\"' in (root/'guardian/control.raw').read_bytes()
            assert not (root/'coordinator/DATA.json').exists()
        if case=='unterminated-control-recovery':assert r['partial_prefix'] and r['control_tail']['bytes']<=256 and (root/'guardian/whole.json').is_file()
    print(json.dumps(dict(case=case,status='PASS',TCB=False,P=False)))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--data',action='store_true');parser.add_argument('--os-case',choices=tuple(TOYS));parser.add_argument('--toy-metadata-abort',action='store_true');parser.add_argument('--toy-parse-abort',action='store_true');parser.add_argument('--os-all',action='store_true');args=parser.parse_args()
    if args.toy_metadata_abort or args.toy_parse_abort:
        folder=ROOT/('OS-parse-failure-coordinator-abort' if args.toy_parse_abort else 'OS-metadata-failure-coordinator-abort')/'coordinator';folder.mkdir()
        book=q.EvidenceBudget([folder],earlier_document_cap=64)
        try:
            if args.toy_parse_abort:q.parse_trace('UNFRAMED DATA\n')
            else:book.document(folder/'DATA.json','x'*100,'control')
        except RuntimeError as error:
            if args.toy_metadata_abort and str(error)!='MetadataEncodedBound':raise
            q.emit_diagnostic(error);q.supervisor_notice('abort');return
        raise AssertionError('MetadataOverflowAccepted')
    if args.os_all and not args.data and not args.os_case:
        end=CONTROL_ORIGIN+30
        ROOT.mkdir(mode=0o700,exist_ok=False)
        if ROOT.stat().st_mode&0o777!=0o700:raise RuntimeError('ControlRootMode')
        signal_metadata_controls()
        for case in TOYS:
            print(json.dumps(dict(case=case,event='BEGIN')),flush=True)
            try:OS(case,end)
            except BaseException as error:
                remaining=list(TOYS)[list(TOYS).index(case)+1:]
                print(json.dumps(dict(case=case,status='FAIL',diagnostic=q.generated_diagnostic(error,512),unreached=remaining,unreached_status='NOT_RUN')),flush=True)
                raise
            if time.monotonic()>end:raise RuntimeError('OSAggregateDeadlineAfterCleanup')
        print(json.dumps(dict(status='OS_ALL_COMPLETE',cases=len(TOYS),TCB=False,P=False)));return
    if args.data and not args.os_case:DATA()
    elif args.os_case and not args.data:OS(args.os_case)
    else:raise SystemExit('DISABLED: exact ROOT control grant required')
if __name__=='__main__':
    try:main()
    except SystemExit:raise
    except BaseException as error:q.emit_diagnostic(error);raise SystemExit(2)
    finally:
        for handle in _CONTROL_HANDLES:handle.close()
