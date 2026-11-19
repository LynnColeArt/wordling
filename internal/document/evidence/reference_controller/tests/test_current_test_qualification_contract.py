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




def static_parent_floor(node):
    names = [n for n in ast.walk(node) if isinstance(n, ast.Attribute)]
    opens = [n for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'open']
    return (sum(n.attr == 'O_NOFOLLOW' for n in names) >= 2
        and any(any(k.arg == 'dir_fd' for k in n.keywords) for n in opens)
        and any(n.attr == 'fstat' for n in names))


class StaticReaderStructuralTests(unittest.TestCase):
    def test_reader_has_no_execution_or_unbounded_discovery_api(self):
        tree = source_tree('current_test_qualification.py')
        imported = {n.name for node in ast.walk(tree) if isinstance(node, ast.Import) for n in node.names}
        self.assertEqual(imported, {'hashlib', 'json', 'os', 'posixpath', 'stat', 'struct', 'sys', 'time'})
        self.assertEqual([node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)], ['pathlib'])
        forbidden = {'resolve', 'walk', 'listdir', 'scandir', 'glob', 'rglob', 'system', 'popen', 'fork', 'killpg',
                     'execv', 'execve', 'spawnv', 'Popen', 'run', 'check_output'}
        calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
        self.assertEqual([n.func.attr for n in calls if isinstance(n.func, ast.Attribute)
            and n.func.attr in forbidden - {'scandir'} and not (n.func.attr == 'run' and isinstance(n.func.value, ast.Call)
                and isinstance(n.func.value.func, ast.Name) and n.func.value.func.id == '_StaticInventory')], [])
        self.assertEqual([n.func.id for n in calls if isinstance(n.func, ast.Name) and n.func.id in {'eval', 'exec', 'compile', '__import__'}], [])

    def test_both_inspected_and_repository_plan_parents_have_anchored_floor(self):
        tree = source_tree('current_test_qualification.py')
        self.assertTrue(static_parent_floor(function(tree, 'path_info', '_StaticInventory')))
        self.assertTrue(static_parent_floor(function(tree, '_load_static_plan')))

    def test_parent_floor_detects_actual_source_ast_nofollow_removal(self):
        node = function(source_tree('current_test_qualification.py'), 'path_info', '_StaticInventory')
        self.assertTrue(static_parent_floor(node))
        class Remove(ast.NodeTransformer):
            def visit_Attribute(self, value):
                return ast.Constant(value=0) if value.attr == 'O_NOFOLLOW' else self.generic_visit(value)
        self.assertFalse(static_parent_floor(Remove().visit(node)))



STATIC04_CONSERVED_AST_PINS = [('elf_string_table_offset', None, '764efeeb4879dcf29a594e68906906ba86acbfec6324b105d04d36270a194e28'), ('elf_string_data', None, 'd829a5c3e103562330b3518cfad64ea799f081578e68719eb3b4bd1fcad16eb8'), ('check', '_StaticInventory', '92ed826fa3f27fe64bd3a15892020e4a3e3ad4f12ad786130511b26fd6978b00')]


class Static02PlanStructuralTests(unittest.TestCase):
    """Structural conservation only; never initial semantic RED or authority."""
    def plans(self):
        import json
        root = Path(__file__).absolute().parents[5]
        old = json.loads((root / 'docs/research/continuation/test-runtime-qualification-v2/source-stage/static-inspection-design/static03/static03-reader-plan.json').read_text())
        new = json.loads((root / 'docs/research/continuation/test-runtime-qualification-v2/source-stage/static-inspection-design/static04/reader-plan.json').read_text())
        return old, new

    def test_all_old_117_typed_items_retained_in_relative_order(self):
        old, new = self.plans()
        def tuples(plan):
            return [(r['kind'], r['path']) for r in plan['fixed_item_order']]
        before, after = tuples(old), tuples(new)
        self.assertEqual(len(before), 117)
        self.assertEqual(len(after), 135)
        positions = [after.index(item) for item in before]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(len(after), len(set(after)))

    def test_exact_typed_roster_mirror_and_original_resource_caps(self):
        old, new = self.plans()
        keys = [('ancestor', 'declared_exact_ancestor_metadata'), ('alias', 'declared_logical_aliases'),
            ('directory', 'declared_metadata_only_directories'), ('ELF_seed', 'declared_ELF_seed_files'),
            ('loader_data', 'declared_nonexecuted_loader_data_files')]
        expected = [dict(kind=kind, path=n) for kind, key in keys for n in new[key]]
        self.assertEqual(new['fixed_item_order'], expected)
        for key in old['bounds']:
            if key not in {'ancestor_metadata_count', 'alias_count', 'seed_count', 'fixed_item_count'}:
                self.assertEqual(new['bounds'][key], old['bounds'][key])
        self.assertEqual(new['component_operation_cap'], 38912)
        self.assertEqual(new['argv'], old['argv'])
        self.assertEqual(new['env'], old['env'])

    def test_window_string_decoder_and_operation_ceiling_source_bodies_conserved(self):
        # Exact AST SHA values below come from fixed bc83 source, not postimage.
        tree = source_tree('current_test_qualification.py')
        for name, owner, wanted in STATIC04_CONSERVED_AST_PINS:
            node = function(tree, name, owner)
            self.assertEqual(hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest(), wanted)




class SourceCensusStructuralTests(unittest.TestCase):
    def test_old_item_body_tail_and_all_STATIC_caps_are_preserved(self):
        tree = source_tree('current_test_qualification.py')
        node = function(tree, 'item', '_StaticInventory')
        self.assertIsInstance(node.body[0], ast.If)
        self.assertEqual(hashlib.sha256(ast.dump(ast.Module(body=node.body[1:], type_ignores=[]),
            include_attributes=False).encode()).hexdigest(), '31860b3484248e348b6f68559a6a64b8e87f47d3b9a23c2dfd8e85d197b5ecb1')
        self.assertIn('census_root', ast.unparse(node.body[0]))

    def test_only_one_bounded_directory_scanner_is_present(self):
        tree = source_tree('current_test_qualification.py')
        scanner = function(tree, '_census_scan_directory')
        allowed = {id(n) for n in ast.walk(scanner)}
        scans = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute) and n.func.attr == 'scandir']
        self.assertEqual(len(scans), 1)
        self.assertTrue(all(id(n) in allowed for n in scans))
        self.assertIn('CensusDirectoryEntryBound', ast.unparse(scanner))
        self.assertIn('CensusMemoryBound', ast.unparse(scanner))

    def test_fixed_census_entrypoint_cannot_accept_arbitrary_paths_or_spawn(self):
        tree = source_tree('current_test_qualification.py')
        node = function(tree, 'closure_source_census')
        self.assertEqual(node.args.args + node.args.posonlyargs + node.args.kwonlyargs, [])
        self.assertIsNone(node.args.vararg)
        self.assertIsNone(node.args.kwarg)
        self.assertEqual(group_signal_calls(node), [])
        self.assertNotIn('CurrentContext(', ast.unparse(node))




class CurrentGenuineContextStructuralTests(unittest.TestCase):
    def test_role_frame_check_is_part_of_one_canonical_consumer(self):
        node = function(source_tree('runtime_qualification.py'), '_current_selection_data')
        calls = [n for n in ast.walk(node) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name) and n.func.id == '_current_role_frames_data']
        self.assertEqual(len(calls), 1)
        role = function(source_tree('runtime_qualification.py'), '_current_role_frames_data')
        forbidden = {'open', 'read', 'read_bytes', 'stat', 'resolve', 'Popen', 'fork'}
        self.assertEqual([n.func.attr for n in ast.walk(role) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute) and n.func.attr in forbidden], [])

    def test_current_preflight_keeps_v1_default_body(self):
        node = function(source_tree('runtime_qualification.py'), 'preflight_inputs', 'Preparation')
        self.assertIsInstance(node.body[0], ast.If)
        self.assertIn('current_test', ast.unparse(node.body[0]))
        self.assertEqual(hashlib.sha256(ast.dump(ast.Module(body=node.body[1:], type_ignores=[]),
            include_attributes=False).encode()).hexdigest(), 'cb8fbe16e61079ab0e6ccec7821c3fb91b03ad059a2bacd36c975580378d7002')

    def test_public_constructor_stays_blocked_and_prep_clock_is_separate(self):
        tree = source_tree('current_test_qualification.py')
        node = function(tree, '__new__', '_CurrentContext')
        self.assertTrue(any(isinstance(n, ast.Raise) for n in ast.walk(node)))
        producer = function(tree, '_produce_current_context')
        self.assertIn('_require_live_root_boundary', ast.unparse(producer))
        self.assertIn('whole_end', ast.unparse(producer))
        self.assertIn('preparation_origin', ast.unparse(producer))


if __name__ == "__main__":
    unittest.main()
