"""Ordinary installed public API: genuine consumer, no source loader or patched IO."""
import copy
import json
import sys
from reference_controller.bootstrap import load_policy, validate_policy
from reference_controller.controller import ReferenceController, LeafPlan
from reference_controller.issuance import TestIssuer, TestGrant
from reference_controller.errors import Refusal

root=sys.argv[1]
source=load_policy();plan=LeafPlan();source.plan_hash=plan.digest();issuer=TestIssuer()
p=issuer.reserve(source,root,'wp70-v1','api-contract','TEST-api-controller',root+'-ledger')
grant=issuer.issue(p)

def refusal(f,code=None):
    try:f()
    except Refusal as e:
        if code is not None:assert e.code==code,(e.code,code)
        return
    raise AssertionError('public authority substitute accepted')

refusal(lambda:copy.copy(grant),'CapabilityNotCopyable')
refusal(lambda:TestIssuer().activate(grant),'InvalidTestGrant')
forged=object.__new__(TestGrant)
forged.__dict__.update(grant.__dict__)
refusal(lambda:ReferenceController.open_leaf(source,plan,forged),'InvalidTestGrant')
refusal(lambda:validate_policy(copy.copy(source)),'UnverifiedPolicyData')
refusal(lambda:ReferenceController.open_leaf('/never/stat/source',{},{}),'SourcePrelaunchBlocked')
controller=ReferenceController.open_leaf(source,plan,grant)
try:
    report=controller.run_leaf()
    assert report['status']=='TEST_LEAF_COMPLETE'
    refusal(controller.run_leaf,'ControllerRunOnce')
    def data_only(v):
        assert type(v) in (dict,list,str,int,bool,float,type(None)),type(v)
        if type(v) is dict:
            for k,x in v.items():assert type(k) is str;data_only(x)
        elif type(v) is list:
            for x in v:data_only(x)
    data_only(report)
finally:
    containment=controller.close()
assert containment['account']['closed'] is True
refusal(lambda:ReferenceController.open_leaf(source,plan,grant),'InvalidTestGrant')
print(json.dumps(dict(status='API_CONTRACT_PASS',report=report,containment=containment),sort_keys=True))
