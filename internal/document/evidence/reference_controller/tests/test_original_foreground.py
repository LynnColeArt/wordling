"""Public installed source/plan negatives; positive CONTROL requires ROOT later.

No test here invokes coordinate_one, administer_one, private mint or P launch.
"""
import json
import unittest
from original_deployment import InstalledDeployment, invoke


class OriginalForegroundContracts(InstalledDeployment):
    def test_installed_public_policy_and_finite_plans_are_data_only(self):
        result = invoke(self.interpreter, '''
import json,pathlib,sys
from reference_controller.bootstrap import load_original_policy,validate_policy
from reference_controller.original import OriginalLeafPlan,validate_roster
p=load_original_policy()
validate_policy(p)
rows=json.loads((pathlib.Path(sys.prefix)/'wordling-original-plans.json').read_text())['rows']
bundle=json.loads((pathlib.Path(sys.prefix)/'wordling-original-review-bundle.json').read_text())
validate_roster(p,rows,bundle['candidate'])
plans=[OriginalLeafPlan.from_row(r) for r in rows.values() if r['action']=='leaf']
assert len(plans)==21
assert all(x.domain=='CONTROL' for x in plans)
assert bundle['reviews']==[]
print(json.dumps(dict(plans=len(plans),root_invocations=0,control_leaves=0)))
''')
        self.assertEqual(result.returncode,0,result.stderr.decode())
        self.assertEqual(json.loads(result.stdout)['root_invocations'],0)

    def test_foreign_root_decisions_do_not_inspect_source_or_plan(self):
        result = invoke(self.interpreter, '''
from reference_controller.issuance import RootTicketIssuer
from reference_controller.errors import Refusal
class Hostile:
    def __getattribute__(self,name): raise AssertionError('caller inspected')
for decision in ({},object(),Hostile()):
    try: RootTicketIssuer().issue(decision,Hostile(),Hostile())
    except Refusal as e: assert e.code=='RootDecisionRequired',e.code
    else: raise AssertionError('raw ROOT data accepted')
''')
        self.assertEqual(result.returncode,0,result.stderr.decode())

    def test_wrong_plan_fields_refuse_offline(self):
        result = invoke(self.interpreter, '''
from dataclasses import replace
import json,pathlib,sys
from reference_controller.original import OriginalLeafPlan
from reference_controller.errors import Refusal
rows=json.loads((pathlib.Path(sys.prefix)/'wordling-original-plans.json').read_text())['rows']
plan=OriginalLeafPlan.from_row(rows['C104-OWNED'])
for field,value in [('domain','ORIGINAL'),('profile','ORIGINAL-WP51-V1'),('repetition',True),('group','../escape'),('grant_id','a'*64),('candidate','0'*64),('source','0'*64),('case','OTHER')]:
    try: replace(plan,**{field:value}).validate()
    except Refusal: pass
    else: raise AssertionError('unbound plan accepted:'+field)
''')
        self.assertEqual(result.returncode,0,result.stderr.decode())


if __name__ == '__main__':
    unittest.main()
