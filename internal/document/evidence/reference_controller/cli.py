"""Closed public local TEST administration and actual ledger transactions.

This foundation command is not run_leaf and has no original execution route.
"""
import argparse
import hashlib
import json
import os
import time
import sys
from dataclasses import asdict, is_dataclass
from .errors import Refusal
from .account import OperationLimits
from .issuance import TestIssuer, provision_test_store, _CHECKPOINTS
from .ownership import ParentLease, OwnedLedger


def _emit(value):
    raw = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
    if len(raw) > 16384:
        raise Refusal('OutputLimit')
    print(raw, flush=True)


def transaction(policy, root, generation, grant_id, leaf, checkpoint):
    issuer = TestIssuer()
    permit = issuer.reserve(policy, root, generation, grant_id, leaf, root + '-ledger')
    book = parent = ledger = None
    try:
        grant = issuer.issue(permit, checkpoint)
        book = issuer.activate(grant)
        checkpoint('activated')
        parent = ParentLease.acquire(book.parent_path, book.reserve_ledger_operation(
            'acquire-parent', book.parent_path, OperationLimits(fds=4)))
        checkpoint('parent-acquired')
        ledger = OwnedLedger.create(parent, book.basename, book.reserve_ledger_operation(
            'create-ledger', (parent, book.basename), OperationLimits(fds=1)))
        checkpoint('ledger-created')
        for state in ('AUTHORIZED', 'COMPLETE'):
            p = book.reserve_ledger_operation('update-record', ledger,
                    OperationLimits(syscalls=1024, work=262144, io=16385))
            ledger.write_json(book.record(state, dict(test_only=True), p), p)
            if state == 'AUTHORIZED':
                checkpoint('ledger-charged')
        audit = book.reserve_phase('audit', issuer, dict(work=4096))
        observation = book.observation()
        payload = json.dumps(observation, sort_keys=True).encode('ascii')
        audit.charge(issuer, work=len(payload))
        digest = hashlib.sha256(payload).hexdigest()
        audit.close(issuer)
        ledger.close(book.reserve_ledger_operation('cleanup-close', ledger,
                      ledger.close_requirements()))
        ledger = None
        parent.close(book.reserve_ledger_operation('cleanup-close', parent,
                      parent.close_requirements()))
        parent = None
        issuer.finish(book)
        checkpoint('complete')
        _emit(dict(status='TEST_TRANSACTION_COMPLETE', ledger=book.parent_path + '/' + book.basename,
                   audit_sha256=digest, account=book.observation()))
        return 0
    finally:
        if book is not None:
            for resource in (ledger, parent):
                if resource is not None:
                    try:
                        resource.close(book.reserve_ledger_operation('cleanup-close', resource,
                            resource.close_requirements()))
                    except (Refusal, OSError):
                        book.halt('CleanupIncomplete')
            if book in issuer._stores:
                issuer.finish(book)



def leaf_transaction(policy, args):
    from .controller import ReferenceController, LeafPlan
    plan = LeafPlan(args.scenario, args.leaf_checkpoint)
    policy.plan_hash = plan.digest()
    issuer = TestIssuer()
    issuance = issuer.reserve(policy,args.root,args.generation,args.grant_id,args.leaf,args.root+'-ledger')
    controller = None
    report = None
    try:
        grant = issuer.issue(issuance)
        controller = ReferenceController.open_leaf(policy,plan,grant)
        report = controller.run_leaf()
        containment = controller.close()
        report['containment'] = containment
        report['account'] = containment['account']
        _emit(report)
        return 0
    except Exception as error:
        partial = getattr(error,'observation',None)
        if controller is not None:
            report = controller._report('REFUSED')
            if not controller._closed:
                try:
                    report['containment'] = controller.close()
                except Exception as closing:
                    report['cleanup_failure'] = getattr(closing,'code',type(closing).__name__)
        else:
            report = dict(status='REFUSED',test_only=True,original_qualification=False)
        report['reason'] = getattr(error,'code',type(error).__name__)
        if is_dataclass(partial):
            report['partial'] = asdict(partial)
        report['account'] = issuance._book.observation()
        _emit(report)
        return 2


def main(policy):
    if len(sys.argv)>1 and sys.argv[1]=='original':
        from .issuance import RootTicketIssuer
        RootTicketIssuer().issue()
    parser = argparse.ArgumentParser(prog='python -I -B -m reference_controller')
    commands = parser.add_subparsers(dest='command', required=True)
    admin = commands.add_parser('test-admin')
    admin.add_argument('--root', required=True)
    admin.add_argument('--generation', required=True)
    trans = commands.add_parser('test-transaction')
    trans.add_argument('--root', required=True)
    trans.add_argument('--generation', required=True)
    trans.add_argument('--grant-id', required=True)
    trans.add_argument('--leaf', default='TEST-ledger')
    trans.add_argument('--checkpoint', choices=_CHECKPOINTS)
    from .controller import SCENARIOS, CHECKPOINTS
    leaf = commands.add_parser('test-leaf')
    leaf.add_argument('--root',required=True)
    leaf.add_argument('--generation',required=True)
    leaf.add_argument('--grant-id',required=True)
    leaf.add_argument('--leaf',default='TEST-one-leaf')
    leaf.add_argument('--scenario',choices=SCENARIOS,default='healthy')
    leaf.add_argument('--leaf-checkpoint',choices=CHECKPOINTS)
    args = parser.parse_args()
    if args.command=='test-leaf':
        return leaf_transaction(policy,args)
    if args.command == 'test-admin':
        result = provision_test_store(policy, args.root, args.generation)
        os.mkdir(args.root + '-ledger', 0o700)
        _emit(result)
        return 0
    def checkpoint(name):
        if args.checkpoint == name:
            _emit(dict(checkpoint=name, test_only=True))
            time.sleep(0.4)
    return transaction(policy, args.root, args.generation, args.grant_id, args.leaf, checkpoint)
