"""Initial tests-first public import contract; no source loader or fake authority."""
import unittest

class FoundationContract(unittest.TestCase):
    def test_original_entry_is_separately_blocked(self):
        from reference_controller.issuance import RootTicketIssuer
        from reference_controller.errors import Refusal
        with self.assertRaises(Refusal):
            RootTicketIssuer.issue(None)

    def test_record_schema_is_original_finite_v1(self):
        from reference_controller.records import SCHEMA
        self.assertEqual(SCHEMA, "wordling.reference-controller.ledger/v1")

    def test_closed_full_phase_dimensions(self):
        from reference_controller.account import PHASES
        self.assertEqual(set(PHASES), {"issuer", "ledger", "protocol", "P", "helper", "chunk", "binary", "audit"})
