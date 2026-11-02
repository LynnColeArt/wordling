"""Real installed public sequencing regressions, with distinct permanently spent IDs.

No source import loader, synthetic account, private-state writes or mocked IO.
Each test checks complete durable bytes/ctime, full reservations and real cleanup.
"""
import json
import sys
import unittest
from pathlib import Path
from reference_controller.bootstrap import load_policy
from reference_controller.account import OperationLimits
from reference_controller.issuance import TestIssuer
from reference_controller.ownership import ParentLease, OwnedLedger
from reference_controller.errors import Refusal

ROOT = sys.argv.pop(1)


class UpdateOrder(unittest.TestCase):
    def setUp(self):
        self.issuer = TestIssuer()
        self.book = self.issuer.activate(self.issuer.issue(self.issuer.reserve(
            load_policy(), ROOT, 'wp68-v1', self._testMethodName,
            'TEST-order', ROOT+'-ledger')))
        self.parent = ParentLease.acquire(self.book.parent_path,
            self.book.reserve_ledger_operation('acquire-parent', self.book.parent_path,
                                               OperationLimits(fds=4)))
        self.ledger = OwnedLedger.create(self.parent, self.book.basename,
            self.book.reserve_ledger_operation('create-ledger',
                (self.parent, self.book.basename), OperationLimits(fds=1)))
        self.path = Path(self.book.parent_path)/self.book.basename

    def tearDown(self):
        for resource in (self.ledger, self.parent):
            resource.close(self.book.reserve_ledger_operation('cleanup-close', resource,
                                                           resource.close_requirements()))
        self.issuer.finish(self.book)
        self.assertTrue(self.book.observation()['closed'])
        with self.assertRaises(Refusal):
            self.book.reserve_phase('audit', self.issuer, dict(work=1))

    def update(self, state):
        permit = self.book.reserve_ledger_operation('update-record', self.ledger,
            OperationLimits(syscalls=1024, work=262144, io=16385))
        return self.book.record(state, {'test':self._testMethodName}, permit), permit

    def prior(self):
        return self.path.read_bytes(), self.path.stat().st_ctime_ns

    def stale(self, record, permit, before):
        spent = self.book.observation()['spent']
        commits = self.book.observation()['ledger_commits']
        refusal = None
        try:
            self.ledger.write_json(record, permit)
        except Refusal as exc:
            refusal = exc.code
        after = self.prior()
        print(json.dumps(dict(test=self._testMethodName, refusal=refusal,
            before_hex=before[0].hex(), after_hex=after[0].hex(),
            before_ctime=before[1], after_ctime=after[1], account=self.book.observation())), flush=True)
        self.assertEqual(refusal, 'InvalidPermit', 'STALE_UPDATE_BOUNDARY')
        self.assertEqual(before, after, 'STALE_UPDATE_EFFECT')
        self.assertEqual(spent, self.book.observation()['spent'], 'RESERVATION_REFUNDED')
        self.assertEqual(commits, self.book.observation()['ledger_commits'])
        self.assertEqual(spent['prepared_bytes'], 2*(4*8192+1048576))
        self.assertEqual(spent['journal_events'], 2)
        self.assertEqual(spent['journal_bytes'], 16384)
        with self.assertRaises(Refusal):
            self.book.reserve_phase('audit', self.issuer, dict(work=1))

    def test_newer_then_older(self):
        older, p1 = self.update('AUTHORIZED')
        newer, p2 = self.update('COMPLETE')
        self.ledger.write_json(newer, p2)
        self.assertEqual(self.path.read_bytes(), (json.dumps(newer, ensure_ascii=True, indent=2)+'\n').encode('ascii'))
        self.assertEqual(json.loads(self.path.read_bytes())['sequence'], 2)
        self.stale(older, p1, self.prior())

    def test_older_before_newer(self):
        older, p1 = self.update('AUTHORIZED')
        newer, p2 = self.update('COMPLETE')
        before = self.prior()
        self.stale(older, p1, before)
        with self.assertRaises(Refusal):
            self.ledger.write_json(newer, p2)
        self.assertEqual(before, self.prior())
        self.assertEqual(self.book.observation()['ledger_commits'], 0)

    def test_sequential(self):
        for expected, state in enumerate(('AUTHORIZED', 'COMPLETE'), 1):
            record, permit = self.update(state)
            self.ledger.write_json(record, permit)
            self.assertEqual(self.path.read_bytes(), (json.dumps(record, ensure_ascii=True, indent=2)+'\n').encode('ascii'))
            self.assertEqual(json.loads(self.path.read_bytes())['sequence'], expected)
            self.assertEqual(self.book.observation()['ledger_commits'], expected)
        before = self.prior()
        with self.assertRaises(Refusal):
            self.ledger.write_json(record, permit)
        self.assertEqual(before, self.prior())


if __name__ == '__main__':
    unittest.main(verbosity=2)
