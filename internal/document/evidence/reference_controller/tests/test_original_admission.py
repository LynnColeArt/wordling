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
