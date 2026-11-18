"""DRAFT ONLY: WP108 AST/source DATA contracts; no operational helper import.
Structural gates are reported separately from semantic RED and runtime acceptance.
"""
import ast
import hashlib
from pathlib import Path
import unittest

FROZEN_PLANNING_INPUT = 'b58d9f63e1bed9af9c2bc0cd4630ece54ec7c7cf'
PROTECTED_INPUT_PINS = {'internal/document/evidence/reference_controller/__init__.py': {'size': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'internal/document/evidence/reference_controller/__main__.py': {'size': 53, 'sha256': '6af9591eeca0682fbbc17fc76990ba473c7b51ab571000fa03ac8ff389bbe909'}, 'internal/document/evidence/reference_controller/bootstrap.py': {'size': 20254, 'sha256': '0b6807bbfdbdd210f5f5cd4be98f6c77aeaa4bec8c9531721e356d60005ed91c'}, 'internal/document/evidence/reference_controller/errors.py': {'size': 586, 'sha256': '4938c671c4fdc8c903ae21785da925b19980a1af6686dd83e9f1f9892f2e8a35'}, 'internal/document/evidence/reference_controller/account.py': {'size': 17664, 'sha256': '371fb252ffeb29b387e5b0692a4659f7fa89861c558a6829167eaadeda7ee330'}, 'internal/document/evidence/reference_controller/ownership.py': {'size': 13950, 'sha256': '0bf9b97ae2a572a84c25cc9ae2117ad8afd77c7d405c0f43f7fe660f492308df'}, 'internal/document/evidence/reference_controller/records.py': {'size': 6724, 'sha256': '95be75afce1c45a8b9a230675113e02c97a3ddc20be5b90bf5e4001ce5b74e99'}, 'internal/document/evidence/reference_controller/issuance.py': {'size': 28688, 'sha256': 'e804f433668edab5129ab455e2c903392a4d064f5acbbd035a4dd9a561f41528'}, 'internal/document/evidence/reference_controller/cli.py': {'size': 6349, 'sha256': '20620e410fcab75e120231e5563048db0a9e3d225ac1cab5348d49093f3e0b53'}, 'internal/document/evidence/reference_controller/controller.py': {'size': 26867, 'sha256': '8c4f7de700ff3c236f1db93fdbcb4ffe02b298646286f0659bfbf6f6a68c142c'}, 'internal/document/evidence/reference_controller/protocol.py': {'size': 8458, 'sha256': 'c252502c4ffd249d0b01a5cd94282f795d0628ee2f7cb3946cc1ede77b74bf33'}, 'internal/document/evidence/reference_controller/publisher.py': {'size': 7669, 'sha256': '2d34b9018392551d6575f1e52ade6b3d1fdc9c7edf721cc61d1bc8bbda6d4f7d'}, 'scripts/reference/startup_transport.py': {'size': 35479, 'sha256': '299dd2e68bd90c08803ac8155d9593e30f5a607a093c1a95075abaefaf475d77'}, 'scripts/reference/startup_family/__init__.py': {'size': 2445, 'sha256': 'bed41656c52eebee508e553b37675506fb857bb927a59cfdb6ba31a3a6f5d07a'}, 'scripts/reference/startup_family/artifacts.py': {'size': 19841, 'sha256': 'b65f468e67728894089dd94a20db712602e7c27edbb6b119a695ef292ae55c2d'}, 'scripts/reference/startup_family/engine.py': {'size': 37641, 'sha256': '287951bdeedf2e61195e2098054817ada76ba65b5bba1db8be44b65dd436bd74'}, 'scripts/reference/startup_family/lifetime.py': {'size': 114202, 'sha256': '3a6130bef6516648189f61ba4dd2dbc8cdf3360249307b71d062ef4c5ce98050'}, 'internal/document/evidence/retrieve-field-observations/peer.py': {'size': 3124, 'sha256': '52beeb081e919fe1fed0d3f861b9f317a6ca8ff75f02a2b03c12ebc0f24d323e'}, 'internal/document/evidence/retrieve-field-observations/boundaries.py': {'size': 5604, 'sha256': '2ece63c6be1b0f0ef108289eb02dc4b8961d8cf7dda37163f92d2217a7e8844a'}, 'scripts/reference/qmp.py': {'size': 5196, 'sha256': 'dcb3aaa83c72b695f63a86529b25bc70fe26dd7e197fc27052effe8218f82304'}, 'internal/document/evidence/reference_controller/pyproject.toml': {'size': 840, 'sha256': 'c49deef4fb645870466c68da509e84b78ba51ae0f4ee27715f76935401422c58'}, 'internal/document/evidence/reference_controller/tests/harmless_fixture.c': {'size': 5798, 'sha256': 'f37add43898cb78f913e7a9ab0b43c732fed2eda4af6eb6bcb181c52eb5c88d7'}, 'internal/document/evidence/reference_controller/tests/controller_roster.json': {'size': 2286, 'sha256': 'f4184623a3334cde4e981ae6998b9c6e578c2201660e6e57f8b17e8a50c445cb'}}


def source_tree(name):
    return ast.parse(Path(__file__).with_name(name).read_text(), filename=name)


def function(tree, name, class_name=None):
    owner = tree
    if class_name is not None:
        matches = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name]
        if len(matches) != 1:
            raise AssertionError("STRUCTURAL_SOURCE_FLOOR: exactly one class " + class_name)
        owner = matches[0]
    matches = [n for n in owner.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(matches) != 1:
        raise AssertionError("STRUCTURAL_SOURCE_FLOOR: exactly one function " + name)
    return matches[0]


def current_keyword(node):
    return any(arg.arg == "current_test" and isinstance(default, ast.Constant) and default.value is None
        for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults))


def group_signal_calls(node):
    return [n for n in ast.walk(node) if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute) and n.func.attr == "killpg"]


class CurrentPurposeStructuralTests(unittest.TestCase):
    def test_current_purpose_keyword_admission_has_concrete_source_floor(self):
        tree = source_tree("runtime_qualification.py")
        for name, owner in (("__init__", "Preparation"), ("__init__", "EvidenceBudget"),
                            ("admit_capacity", None), ("verify_tool_selection", None)):
            with self.subTest(function=name, owner=owner):
                self.assertTrue(current_keyword(function(tree, name, owner)),
                    "STRUCTURAL_API_NOT_ADOPTED: never count this as semantic RED")

    def test_keyword_gate_rejects_a_synthetic_ast_removal(self):
        # AST DATA self-control only, never a prototype or executed function.
        positive = ast.parse("def boundary(*, current_test=None): pass").body[0]
        negative = ast.parse("def boundary(): pass").body[0]
        self.assertTrue(current_keyword(positive))
        self.assertFalse(current_keyword(negative))

    def test_direct_owner_retains_pidfd_floor_and_has_no_group_signal(self):
        owner = function(source_tree("runtime_qualification_supervisor.py"), "_supervise_owner")
        direct = [n for n in ast.walk(owner) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute) and n.func.attr == "pidfd_send_signal"]
        self.assertGreaterEqual(len(direct), 1, "non-vacuous direct held pidfd cleanup floor")
        self.assertEqual(group_signal_calls(owner), [], "protected P workers are not group signal targets")

    def test_direct_owner_ast_gate_detects_group_signal_mutant(self):
        # Synthetic AST DATA; no process/signal is executed.
        mutant = ast.parse("def owner(fd, p):\n signal.pidfd_send_signal(fd, 15)\n os.killpg(p, 15)\n").body[0]
        self.assertEqual(len(group_signal_calls(mutant)), 1)

    def test_tool_consumer_keeps_one_canonical_record_validator_call_floor(self):
        node = function(source_tree("runtime_qualification.py"), "verify_tool_selection")
        calls = [n for n in ast.walk(node) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name) and n.func.id == "check_selection_records"]
        self.assertGreaterEqual(len(calls), 1, "no alternate parallel record validator")


class ProtectedInputDataTests(unittest.TestCase):
    def test_all23_operational_inputs_stay_at_frozen_target_bytes(self):
        # Read-only source bytes, no import/exec/Git subprocess/BASE investigation.
        root = Path(__file__).resolve().parents[5]
        self.assertEqual(len(PROTECTED_INPUT_PINS), 23, "non-vacuous protected source/data floor")
        for name, wanted in PROTECTED_INPUT_PINS.items():
            with self.subTest(path=name):
                data = (root / name).read_bytes()
                self.assertEqual(dict(size=len(data), sha256=hashlib.sha256(data).hexdigest()), wanted)


if __name__ == "__main__":
    unittest.main()
