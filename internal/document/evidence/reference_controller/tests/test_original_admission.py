"""Installed public refusal contracts; no ROOT invocation or CONTROL effects."""
import json
import unittest

from original_deployment import InstalledDeployment, invoke


class InstalledAdmission(InstalledDeployment):
    def test_existing_test_and_no_argument_root_boundaries(self):
        result = invoke(self.interpreter, '''
from reference_controller.issuance import RootTicketIssuer
from reference_controller.controller import ReferenceController
from reference_controller.errors import Refusal
for operation in (lambda: RootTicketIssuer().issue(),
                  lambda: ReferenceController.open_leaf(None, None, {})):
    try: operation()
    except Refusal as error: assert error.code == 'SourcePrelaunchBlocked'
    else: raise AssertionError('raw authority accepted')
''')
        self.assertEqual(result.returncode, 0, result.stderr.decode())

    def test_new_installed_original_entry_refuses_before_caller_access(self):
        result = invoke(self.interpreter, '''
import json
from reference_controller.original import open_original_leaf
from reference_controller.errors import Refusal
class Hostile:
    def __getattribute__(self, name):
        raise AssertionError('caller inspected before grant admission')
for grant in (None, {}, Hostile()):
    try: open_original_leaf(Hostile(), Hostile(), grant)
    except Refusal as error:
        assert error.code == 'SourcePrelaunchBlocked', error.code
    else: raise AssertionError('unregistered authority accepted')
print(json.dumps({'refused': 3, 'root_invocations': 0, 'control_leaves': 0}))
''')
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(json.loads(result.stdout)['refused'], 3)


if __name__ == '__main__':
    unittest.main()

# Deliberate future harmless TEST action, not unittest discovery. ROOT must
# separately release the frozen finite campaign before any caller invokes it.
GENUINE_TEST_BOUNDARY_CODE = r'''
import hashlib,json,os,pathlib
from reference_controller.bootstrap import load_original_policy
from reference_controller.original import CONTROL_VARIANT,CONTROL_ROOT,open_original_leaf
from reference_controller.issuance import TestIssuer,provision_test_store,stable_key
from reference_controller.errors import Refusal
p=load_original_policy()
root='/tmp/wordling-reference-TEST-WP104-'+CONTROL_VARIANT+'-boundary'
provision_test_store(p,root,'WP104-boundary-v1')
os.mkdir(root+'-ledger',0o700)
issuer=TestIssuer()
try: issuer.reserve(p,CONTROL_ROOT+'owned/issuer','WP104-boundary-v1','cross','TEST',root+'-ledger')
except Refusal as e: assert e.code=='NotTestNamespace',e.code
else: raise AssertionError('TEST_TO_CONTROL_RESOURCE_DOMAIN_BYPASS')
grant=issuer.issue(issuer.reserve(p,root,'WP104-boundary-v1','boundary','TEST-boundary',root+'-ledger'))
marker=pathlib.Path(root)/(stable_key('wordling.TEST.ledger/v1','WP104-boundary-v1','boundary')+'.spent')
prior=marker.read_bytes(),marker.stat().st_ctime_ns
used_before=grant._used
assert used_before is False,'ISSUED_TEST_GRANT_ALREADY_USED'
class Hostile:
    def __getattribute__(self,name): raise AssertionError('foreign source/plan inspected')
refusal=None
activation_call=False
frames=[]
try: open_original_leaf(Hostile(),Hostile(),grant)
except Refusal as e:
    refusal=e.code
    tb=e.__traceback__
    while tb is not None:
        code=tb.tb_frame.f_code
        frames.append(dict(filename=code.co_filename,function=code.co_name,line=tb.tb_lineno))
        activation_call=activation_call or code is TestIssuer.activate.__code__
        tb=tb.tb_next
else: raise AssertionError('GENUINE_TEST_GRANT_ACCEPTED_AS_ORIGINAL')
used_after=grant._used
assert prior==(marker.read_bytes(),marker.stat().st_ctime_ns),'TEST_MARKER_CHANGED_AT_ORIGINAL_BOUNDARY'
print(json.dumps(dict(schema='wordling.genuine-TEST-original-boundary/v2',variant=CONTROL_VARIANT,
    actual_original_refusal=refusal,resource_refusal='NotTestNamespace',
    grant_used_before=used_before,grant_used_after=used_after,
    actual_TestIssuer_activate_frame=activation_call,actual_traceback=frames,
    marker_sha256=hashlib.sha256(prior[0]).hexdigest(),marker_ctime_ns=prior[1],original_actions=0)),flush=True)
# No activation is requested by this target. The genuine issued27-source TEST
# permit has only22 of1024 checks left; pretending successful activation would
# be invalid. A mutation's real activation call/used state is the causal fault.
if activation_call or used_after:
    assert activation_call and used_after,'INCOMPLETE_ACTIVATION_CAUSAL_WITNESS'
    raise AssertionError('UNAUTHORIZED_TEST_ACTIVATION_AT_ORIGINAL_GATE')
assert refusal=='SourcePrelaunchBlocked',refusal
'''
