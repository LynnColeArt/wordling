"""Nine source-frozen semantic mutants, fresh offline wheels and genuine consumers.

A mutant counts only when its named behavioral assertion executes and fails.
Build/bootstrap failures are UNKNOWN; they are never counted as a kill.
"""
import json
from pathlib import Path
import shutil
import time
from deployment import FILES, deploy, pin
from functional import plans, functional

MUTANTS = {
 'no-fullspend': ('account.py','            self._spent[k] += n','            pass  # MUTANT: reservation refunded', 'full-phase-book'),
 'forge-permitguard': ('account.py','permit in book._permits and not permit._consumed and','permit in book._permits and', 'consumed-permit'),
 'encode-before-limit': ('records.py','    seen = set()','    import json\n    premature = json.dumps(record)\n    seen = set()', 'huge-string'),
 'ancestor-check': ('ownership.py','if _identity(st) != identity or not stat.S_ISDIR(st.st_mode):','if False:', 'ancestor-retarget'),
 'grant-before-durable': ('issuance.py','            store._call(os.fsync, fd)\n            store._validate()\n            store._call(os.fsync, rootfd)','            pass  # MUTANT: no durability barrier', 'kernel-fsync-failure'),
 'unstable-ticketkey': ('issuance.py',"            marker = stable_key(_KIND, permit._generation, permit._grant_id) + '.spent'","            marker = hashlib.sha256((stable_key(_KIND, permit._generation, permit._grant_id) + permit._book._plan).encode('ascii')).hexdigest() + '.spent'", 'stable-id-different-binding'),
 'replay-unlink': ('issuance.py',"            checkpoint('pre-marker')", "            if os.path.lexists(permit._root + '/' + marker):\n                os.unlink(marker, dir_fd=rootfd)\n            checkpoint('pre-marker')", 'replay-fresh-process'),
 'boot-ignore': ('issuance.py','            if metadata != expected:',"            expected['boot'] = metadata.get('boot')\n            if metadata != expected:", 'boot-quarantine'),
 'source-bootstrap-ignore': ('bootstrap.py','if (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns) != identity:','if False:', 'foreign-source-bootstrap'),
}


def freeze_mutants(source, parent, roots):
    frozen={}
    for name,(file,old,new,case) in MUTANTS.items():
        text=(source/file).read_text()
        if text.count(old)!=1: raise RuntimeError('mutant target not unique '+name)
        changed=text.replace(old,new)
        import hashlib
        frozen[name]=dict(file=file,old=old,new=new,target_case=case,
            source_before=pin(source/file),mutant_sha256=hashlib.sha256(changed.encode()).hexdigest(),
            argv=plans(source,parent/name/'deploy/venv/bin/python',{case:roots[name]},[case])[case],
            behavioral_failure_required=True)
    return frozen


def execute_mutants(source,parent,evidence,frozen,roots):
    results=[]; started=time.monotonic()
    for name,definition in frozen.items():
        directory=parent/name;directory.mkdir(parents=True)
        mutant_source=directory/'source';mutant_source.mkdir()
        for file in FILES+('pyproject.toml',):
            shutil.copyfile(source/file,mutant_source/file)
        (mutant_source/'tests').mkdir()
        shutil.copyfile(source/'tests/roster.json',mutant_source/'tests/roster.json')
        old,new=definition['old'],definition['new']
        path=mutant_source/definition['file'];path.write_text(path.read_text().replace(old,new))
        log=evidence/name
        log.mkdir(parents=True)
        (log/'source-delta.json').write_text(json.dumps(definition,indent=2)+'\n')
        try:
            if pin(path)['sha256']!=definition['mutant_sha256']: raise RuntimeError('mutant source mismatch')
            interpreter,inventory=deploy(mutant_source,directory/'deploy',log/'deployment')
            case=definition['target_case']
            cases=plans(source,interpreter,{case:roots[name]},[case])
            outcomes=functional(source,interpreter,inventory,{case:roots[name]},cases,log,[case])
            outcome=outcomes[0]
            # An API import/loader/build refusal is never a behavioral kill.
            raw=list(log.rglob('*.stderr'))
            trace=b'\n'.join(p.read_bytes() for p in raw)
            expected_assertions={'no-fullspend':'AssertionError', 'forge-permitguard':'ONE_USE_BOUNDARY:OperationLimit',
                'encode-before-limit':'AssertionError', 'ancestor-check':'accepted prohibited operation',
                'unstable-ticketkey':'accepted prohibited operation'}
            if outcome['status']=='PASS':status='SURVIVED'
            elif name in expected_assertions:
                status='KILLED' if expected_assertions[name].encode() in trace else 'UNKNOWN'
            else:
                expected={'grant-before-durable':'downstream escaped failed durability',
                    'replay-unlink':'spent marker replaced','boot-ignore':"AssertionError()",
                    'source-bootstrap-ignore':'source drift accepted'}[name]
                status='KILLED' if expected in outcome.get('reason','') else 'UNKNOWN'
            results.append(dict(mutant=name,status=status,actual=outcome))
        except BaseException as exc:
            results.append(dict(mutant=name,status='UNKNOWN',reason=repr(exc)))
    (evidence/'mutant-results.json').write_text(json.dumps(dict(results=results,elapsed_seconds=time.monotonic()-started),indent=2)+'\n')
    return results
