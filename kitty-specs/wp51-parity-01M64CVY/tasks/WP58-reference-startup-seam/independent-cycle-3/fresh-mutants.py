"""Finite semantic mutants, tested through actual public APIs with disposable source."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p')
evidence=Path(__file__).resolve().parent/'fresh-mutant-results'
source=(root/'scripts/reference/startup_transport.py').read_text()
old_boundary="""            wait_for(selectors.EVENT_READ)
            owner.verify()
"""
# This semantic mutant removes ALL newly added acceptance checks, retaining the
# old before-wait owner check. Single redundant-check removals are not counted.
new_boundary="""            wait_for(selectors.EVENT_READ)
"""
mutants=(
 ('output-cap',"if len(chunk) > allowed:","if False:",'OSTests.test_stdout_limit'),
 ('before-observer',"self.run(dataclasses.replace(before_spawn, input_bytes=facts))","pass",'OSTests.test_before_observer_failure_no_main_launch'),
 ('foreign-peer',"if pid != owner.pid or uid != os.getuid():","if False:",'OSTests.test_foreign_endpoint_zero_commands'),
 ('source-validation',"            source.verify(limits.file_bytes)","            pass",'OSTests.test_sources_changed_before_launch'),
 ('prior-publication',"os.link(temporary, name, src_dir_fd=self.fd, dst_dir_fd=self.fd, follow_symlinks=False)","os.replace(temporary, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)",'OSTests.test_no_replace_publication_and_prior_json'),
 ('kernel-lifetime',"if identity is not None and observed is not None and observed != identity:","if False:",'AdditionalOSTests.test_kernel_exec_change_after_binding_refuses'),
 ('journal-retarget',"if (os.fstat(self._journal_fd).st_nlink != 1\n                or _stamp(os.stat('attempt.jsonl', dir_fd=self.fd, follow_symlinks=False))[:3] != self._journal_identity):", "if False:",'AdditionalOSTests.test_journal_retarget_after_launch_refuses'),
 ('nested-monitor',"                self._monitor()", "                pass",'AdditionalOSTests.test_callback_cannot_hide_parent_output_or_deadline'),
 ('readiness-monitor',"        monitor()", "        pass",'ReadinessSupervisionTests.test_transient_same_owned_processes_cannot_hide_in_reply'),
 ('readiness-deadline',"min(deadline, readiness_deadline)","deadline",'ReadinessSupervisionTests.test_readiness_budget_expires_after_observed_progress'),
)
acceptance_mutant=source.replace(old_boundary,new_boundary).replace('            checkpoint()\n            owner.verify()\n','            checkpoint()\n').replace("        owner.verify()\n        return True","        return True").replace('                                identity.verify()\n                                ready = matched','                                ready = matched')
mutants=mutants+(("readiness-identity-acceptance",source,acceptance_mutant,'ReadinessIdentityTests.test_fast_exec_full_reply_exit_first'),)
records=[]
for name,before,after,test in mutants:
    assert source.count(before)==1,(name,source.count(before))
    mutated=source.replace(before,after)
    directory=evidence/'mutants'
    directory.mkdir(exist_ok=True)
    (directory/(name+'.py.txt')).write_text(mutated)
    with tempfile.TemporaryDirectory(prefix='startup-mutant-') as temporary:
        path=Path(temporary)/'candidate.py'
        path.write_text(mutated)
        env=dict(os.environ,STARTUP_TRANSPORT_UNDER_TEST=str(path),PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(root/'tests/reference/startup-seam'))
        argv=[sys.executable,'-B','-m','unittest','test_transport.'+test,'-v']
        completed=subprocess.run(argv,cwd=root,env=env,capture_output=True,timeout=12)
        (directory/(name+'.stdout')).write_bytes(completed.stdout)
        (directory/(name+'.stderr')).write_bytes(completed.stderr)
        killed=completed.returncode!=0 and b'FAILED' in completed.stderr and b'SyntaxError' not in completed.stderr and b'ImportError' not in completed.stderr
        records.append(dict(name=name,source_sha256=hashlib.sha256(mutated.encode()).hexdigest(),argv=argv,test=test,exit=completed.returncode,killed=killed))
        print(name,'KILLED' if killed else 'SURVIVED',flush=True)
(evidence/'mutants.json').write_text(json.dumps(records,indent=2)+'\n')
sys.exit(0 if all(record['killed'] for record in records) else 1)
