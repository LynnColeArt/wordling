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
class Hostile:
    def __getattribute__(self,name): raise AssertionError('foreign source/plan inspected')
try: open_original_leaf(Hostile(),Hostile(),grant)
except Refusal as e: assert e.code=='SourcePrelaunchBlocked',e.code
else: raise AssertionError('GENUINE_TEST_GRANT_ACCEPTED_AS_ORIGINAL')
assert prior==(marker.read_bytes(),marker.stat().st_ctime_ns),'TEST_MARKER_CHANGED_AT_ORIGINAL_BOUNDARY'
try: book=issuer.activate(grant)
except Refusal as e:
    if e.code=='InvalidTestGrant':
        raise AssertionError('GENUINE_TEST_GRANT_CONSUMED_BY_ORIGINAL') from e
    raise
issuer.finish(book)
assert book.observation()['closed']
print(json.dumps(dict(schema='wordling.genuine-TEST-original-boundary/v1',variant=CONTROL_VARIANT,
    original_refusal='SourcePrelaunchBlocked',resource_refusal='NotTestNamespace',
    genuine_test_activation_after_refusal=True,marker_sha256=hashlib.sha256(prior[0]).hexdigest(),
    marker_ctime_ns=prior[1],original_actions=0)))
'''
