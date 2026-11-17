"""Measured closed-shape and oversized-input costs, never original candidates."""
from pathlib import Path
import importlib.util,json,subprocess,tempfile,time
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;E=O/'evidence';sp=importlib.util.spec_from_file_location('c',R/'scripts/reference/secondary_record_contract.py');C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
rows=[]
with C.Session(R)as session:
 p=session.provenance/'git'/C.READER/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-207/SECOND.WP5.txt';original=p.read_bytes()
 for name,raw in [('observed',original),('near-token-bound',original[:324]+b'R'*65000+original[329:]),('over-input-bound',b'R'*(C.MAX_INPUT+1))]:
  with tempfile.TemporaryDirectory()as d:
   d=Path(d);out=d/'stdout.json';err=d/'stderr.log';stats=d/'time.txt'
   args=['/usr/bin/time','-v','-o',str(stats),str(session.binary),'Secondary'];start=time.monotonic()
   with tempfile.TemporaryFile()as f:
    f.write(raw);f.seek(0)
    with out.open('wb')as stdout,err.open('wb')as stderr:
     p=subprocess.run(args,stdin=f,stdout=stdout,stderr=stderr,timeout=30,cwd=session.cwd)
   text=stats.read_text();(E/('resource-'+name+'.log')).write_text(text+'\n'+err.read_text())
   info=C.load_json(C.limited_read(out,C.MAX_JSON))if p.returncode==0 else None
   if info:
    shape=C.secondary_shape(info,session.authority['known_secondary_D4_00']);assert len(shape)==2
   else:assert name=='over-input-bound'and b'InputLimit'in err.read_bytes()
   rows.append({'name':name,'input_bytes':len(raw),'input_sha256':C.digest(raw),'exit':p.returncode,'seconds':time.monotonic()-start,'stdout_bytes':out.stat().st_size,'stdout_sha256':C.archive_digest(out),'token_count':len(info['tokens'])if info else None,'max_RSS_KiB':int(next(x.split(':',1)[1]for x in text.splitlines()if'Maximum resident set size'in x)),'helper_sha256':session.receipt['binary_sha256'],'argv':args,'cwd':str(session.cwd)})
with tempfile.TemporaryDirectory() as d:
 d=Path(d);native=d/'synthetic.wp5';native.write_bytes(original[:324]+b'R'*65000+original[329:]);report=d/'report.json';stats=d/'time.txt'
 args=['/usr/bin/time','-v','-o',str(stats),'python3',str(R/'scripts/reference/secondary_record_contract.py'),'inspect','--input',str(native),'--role','Secondary','--output',str(report)]
 start=time.monotonic();p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=R,timeout=120)
 text=stats.read_text();(E/'resource-public-cli.log').write_bytes(text.encode()+b'\n'+p.stdout);assert p.returncode==0
 info=C.load_json(C.limited_read(report,C.MAX_JSON));assert len(info['closed_shape'])==2
 rows.append({'name':'public-CLI-near-token-bound','argv':args,'cwd':str(R),'input_bytes':native.stat().st_size,'input_sha256':C.archive_digest(native),'report_bytes':report.stat().st_size,'report_sha256':C.archive_digest(report),'exit':p.returncode,'seconds':time.monotonic()-start,'max_RSS_KiB':int(next(x.split(':',1)[1]for x in text.splitlines()if'Maximum resident set size'in x)),'RSS_scope':'GNU time process-tree maximum; not simultaneous sum or historical DOS claim'})
(E/'resources.json').write_text(json.dumps({'Linux_safeguards_not_DOS_limits':True,'rows':rows,'output_cap':C.MAX_JSON,'diagnostic_cap':C.MAX_DIAGNOSTIC,'full_command_deadline_seconds':600,'helper_deadline_seconds':120,'synthetic_deadline_seconds':30,'provenance_input_cap':8<<20,'compiler_archive_stream_cap':32<<20},indent=2)+'\n')
print(json.dumps(rows,indent=2))
