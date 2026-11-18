"""DRAFT ONLY: proposed WP108 canonical DATA-validator tests, never operational qualification.

Do not run/adopt before ROOT quiet-point review and real pre-code baseline/RED commit.
The synthetic /DATA records below are UNACCEPTED_VALIDATOR_DATA. They are not BASE
observations, expected operational inputs, a context, Preparation, grant or role.
Only setUpClass imports the canonical helper during a later authorized DATA run.
No coordinator/operational TEST/P module is imported or constructed by this draft.
"""
import copy
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import sys
import unittest
from unittest import mock


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")).hexdigest()


def data_pin(raw, mode=0o644):
    return dict(size=len(raw), sha256=hashlib.sha256(raw).hexdigest(), mode=mode, uid=1000, gid=1000)


PROVIDER_DATA = [{'installed_name': 'startup_transport.py', 'repository_path': 'scripts/reference/startup_transport.py', 'source_path': '/DATA/source/scripts/reference/startup_transport.py', 'approved_commit': 'eba8382f5101bfa464d4c30e19ea5183f3bb6469', 'size': 35479, 'sha256': '299dd2e68bd90c08803ac8155d9593e30f5a607a093c1a95075abaefaf475d77'}, {'installed_name': 'startup_family/__init__.py', 'repository_path': 'scripts/reference/startup_family/__init__.py', 'source_path': '/DATA/source/scripts/reference/startup_family/__init__.py', 'approved_commit': 'eba8382f5101bfa464d4c30e19ea5183f3bb6469', 'size': 2445, 'sha256': 'bed41656c52eebee508e553b37675506fb857bb927a59cfdb6ba31a3a6f5d07a'}, {'installed_name': 'startup_family/artifacts.py', 'repository_path': 'scripts/reference/startup_family/artifacts.py', 'source_path': '/DATA/source/scripts/reference/startup_family/artifacts.py', 'approved_commit': 'eba8382f5101bfa464d4c30e19ea5183f3bb6469', 'size': 19841, 'sha256': 'b65f468e67728894089dd94a20db712602e7c27edbb6b119a695ef292ae55c2d'}, {'installed_name': 'startup_family/engine.py', 'repository_path': 'scripts/reference/startup_family/engine.py', 'source_path': '/DATA/source/scripts/reference/startup_family/engine.py', 'approved_commit': 'eba8382f5101bfa464d4c30e19ea5183f3bb6469', 'size': 37641, 'sha256': '287951bdeedf2e61195e2098054817ada76ba65b5bba1db8be44b65dd436bd74'}, {'installed_name': 'startup_family/lifetime.py', 'repository_path': 'scripts/reference/startup_family/lifetime.py', 'source_path': '/DATA/source/scripts/reference/startup_family/lifetime.py', 'approved_commit': '7869159b5d8e3ab1e26ec3e4dae2313264deb6f0', 'size': 114202, 'sha256': '3a6130bef6516648189f61ba4dd2dbc8cdf3360249307b71d062ef4c5ce98050'}, {'installed_name': 'peer.py', 'repository_path': 'internal/document/evidence/retrieve-field-observations/peer.py', 'source_path': '/DATA/source/internal/document/evidence/retrieve-field-observations/peer.py', 'approved_commit': 'e7e59b3e1fbb757014de1789c03f72ed45efec45', 'size': 3124, 'sha256': '52beeb081e919fe1fed0d3f861b9f317a6ca8ff75f02a2b03c12ebc0f24d323e'}, {'installed_name': 'boundaries.py', 'repository_path': 'internal/document/evidence/retrieve-field-observations/boundaries.py', 'source_path': '/DATA/source/internal/document/evidence/retrieve-field-observations/boundaries.py', 'approved_commit': 'e7e59b3e1fbb757014de1789c03f72ed45efec45', 'size': 5604, 'sha256': '2ece63c6be1b0f0ef108289eb02dc4b8961d8cf7dda37163f92d2217a7e8844a'}, {'installed_name': 'qmp.py', 'repository_path': 'scripts/reference/qmp.py', 'source_path': '/DATA/source/scripts/reference/qmp.py', 'approved_commit': '18d6afe95ffcd676fc3f9e964dcad884c9a8c289', 'size': 5196, 'sha256': 'dcb3aaa83c72b695f63a86529b25bc70fe26dd7e197fc27052effe8218f82304'}]
TOOL_SELECTION_DATA_PIN = {'size': 86493, 'sha256': '635be258e00b4829b58ac12136088220a305d77755641d76ba425a41f90218fe'}


def roles_projection(expected):
    names = ("links", "directories", "closed_roots", "runtime_elf", "runtime_mapped_data",
             "tool_startup_hook_sets", "approved_providers", "source_binding")
    return {name: expected[name] for name in names}


def v2_unaccepted_data():
    """A record-consistency example, deliberately incapable of real role admission."""
    runtime = "/DATA/runtime/python"
    tool = "/DATA/tool/python"
    tool_source = "/DATA/tool/source.py"
    tool_cache = "/DATA/tool/source.pyc"
    files = {runtime: data_pin(b"SYNTHETIC RUNTIME DATA", 0o755),
             tool: data_pin(b"SYNTHETIC TOOL DATA", 0o755),
             tool_source: data_pin(b"# TOOL SOURCE DATA\n"),
             tool_cache: data_pin(b"OPAQUE TOOL BYTES; NOT SOURCE EQUIVALENCE")}
    for row in PROVIDER_DATA:
        files[row["source_path"]] = dict(size=row["size"], sha256=row["sha256"], mode=0o644, uid=1000, gid=1000)
    expected = dict(schema="wordling.runtime-qualification-expected/v2",
        disposition="UNACCEPTED_VALIDATOR_DATA", files=files, links={}, directories={},
        closed_roots=["/DATA"], runtime_elf=[runtime], runtime_mapped_data=[],
        tool_startup_hook_sets={}, approved_providers={row["repository_path"]: row["approved_commit"] for row in PROVIDER_DATA},
        source_binding=PROVIDER_DATA, payload_bytes=sum(row["size"] for row in files.values()))
    selection = dict(schema="wordling.tool-selection/v2", disposition="UNACCEPTED_VALIDATOR_DATA",
        files_sha256=digest(files), roles_sha256=digest(roles_projection(expected)),
        new_tool_records=[dict(path=n, **files[n]) for n in (tool, tool_source, tool_cache)],
        runtime_elf=expected["runtime_elf"], runtime_mapped_data=[],
        approved_providers=expected["approved_providers"],
        tool_ELF_graphs=[dict(path=tool, needed=[], loaders=[])], shell_aliases=[],
        opaque_cache_pairs=[dict(source=tool_source, cache=tool_cache,
            classification="OPAQUE_TOOL_BYTES", body_source_equivalence=False)])
    return expected, selection


def canonical_helper():
    """Normal loader at the one adopted sibling path; never an editable overlay."""
    path = Path(__file__).with_name("runtime_qualification.py").resolve()
    if "runtime_qualification" in sys.modules:
        module = sys.modules["runtime_qualification"]
        if Path(module.__file__).resolve() != path:
            raise RuntimeError("DATA_TEST_FOREIGN_HELPER")
        return module
    spec = importlib.util.spec_from_file_location("runtime_qualification", path)
    if spec is None or type(spec.loader).__name__ != "SourceFileLoader" or spec.origin != str(path):
        raise RuntimeError("DATA_TEST_CANONICAL_LOADER_SETUP_FAILURE")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CurrentToolSelectionDataTests(unittest.TestCase):
    """SEMANTIC DATA target; no accepted reference/context/BASE is fabricated."""
    @classmethod
    def setUpClass(cls):
        cls.q = canonical_helper()

    def checked(self, expected, selection):
        try:
            return self.q.check_selection_records(expected, selection)
        except RuntimeError as error:
            self.fail("CANONICAL_V2_RECORD_SEMANTICS: " + str(error))
        except Exception as error:
            self.fail("NONSEMANTIC_SETUP_OR_UNEXPECTED_ERROR: " + type(error).__name__ + ": " + str(error))

    def refused(self, expected, selection, wanted):
        try:
            self.q.check_selection_records(expected, selection)
        except RuntimeError as error:
            self.assertEqual(str(error), wanted, "wrong guard is not a semantic kill")
        except Exception as error:
            self.fail("NONSEMANTIC_SETUP_OR_UNEXPECTED_ERROR: " + type(error).__name__ + ": " + str(error))
        else:
            self.fail("canonical data validator accepted selected invalid record set")

    def test_v2_record_validation_avoids_historical_cardinality(self):
        expected, selection = v2_unaccepted_data()
        self.assertEqual(self.checked(expected, selection), dict(
            schema="wordling.tool-selection-data-validation/v2", disposition="UNACCEPTED_VALIDATOR_DATA",
            files_sha256=selection["files_sha256"], roles_sha256=selection["roles_sha256"],
            tool_records=3, provider_records=8))

    def test_tool_only_record_cannot_grow_runtime_roles(self):
        expected, selection = v2_unaccepted_data()
        tool = selection["new_tool_records"][0]["path"]
        expected["runtime_elf"] = expected["runtime_elf"] + [tool]
        selection["runtime_elf"] = expected["runtime_elf"]
        selection["roles_sha256"] = digest(roles_projection(expected))
        self.refused(expected, selection, "CurrentToolRuntimeRoleGrowth")

    def test_current_lifetime_bytes_cannot_carry_old_provider_label(self):
        expected, selection = v2_unaccepted_data()
        selection["approved_providers"] = dict(selection["approved_providers"])
        selection["approved_providers"]["scripts/reference/startup_family/lifetime.py"] = "eba8382f5101bfa464d4c30e19ea5183f3bb6469"
        self.refused(expected, selection, "CurrentProviderProvenance")

    def test_observed_expected_postimage_does_not_replace_preaccepted_digest(self):
        expected, selection = v2_unaccepted_data()
        name = expected["runtime_elf"][0]
        expected["files"][name] = dict(expected["files"][name], sha256="0" * 64)
        self.refused(expected, selection, "CurrentReferenceFilesDigest")

    def test_changed_selected_tool_bytes_are_not_adopted(self):
        expected, selection = v2_unaccepted_data()
        selection["new_tool_records"][0]["sha256"] = "0" * 64
        self.refused(expected, selection, "CurrentToolRecordMismatch")

    def test_cache_header_or_label_cannot_claim_body_source_equivalence(self):
        expected, selection = v2_unaccepted_data()
        selection["opaque_cache_pairs"][0]["body_source_equivalence"] = True
        self.refused(expected, selection, "CurrentToolCacheEquivalence")

    def test_role_postimage_must_match_separately_bound_projection(self):
        expected, selection = v2_unaccepted_data()
        expected["closed_roots"] = expected["closed_roots"] + ["/DATA/FOREIGN"]
        self.refused(expected, selection, "CurrentReferenceRoleDigest")

    def test_mixed_v1_expected_and_v2_selection_is_not_reinterpreted(self):
        expected, selection = v2_unaccepted_data()
        expected["schema"] = "wordling.runtime-qualification-expected/v1"
        self.refused(expected, selection, "CurrentToolSelectionSchema")


class ExistingPureControlTests(unittest.TestCase):
    """SYNTHETIC DATA controls, not V19 custody or a real reference result."""
    @classmethod
    def setUpClass(cls):
        cls.q = canonical_helper()

    def legacy_data(self):
        path = Path(__file__).with_name("runtime_tool_selection.json")
        self.assertLessEqual(path.stat().st_size, 1048576)
        raw = path.read_bytes()
        self.assertEqual(dict(size=len(raw), sha256=hashlib.sha256(raw).hexdigest()), TOOL_SELECTION_DATA_PIN)
        selection = json.loads(raw)
        self.assertEqual(selection["schema"], "wordling.tool-selection/v1")
        files = {"/DATA/v1/legacy-" + str(i): data_pin(b"SYNTHETIC LEGACY DATA") for i in range(20279)}
        for row in selection["new_tool_records"]:
            files[row["path"]] = {k: row[k] for k in ("size", "sha256", "mode", "uid", "gid")}
        selected = {row["path"] for row in selection["new_tool_records"]}
        selection["old_external_sha256"] = digest({n: v for n, v in files.items() if n not in selected})
        expected = dict(schema="wordling.runtime-qualification-expected/v1", files=files,
            runtime_elf=selection["old_runtime_elf"], runtime_mapped_data=selection["old_runtime_mapped_data"],
            approved_providers=selection["old_providers"], closed_roots=selection["old_closed_roots"])
        return expected, selection

    def test_existing_v1_cardinality_projection_remains_supported_as_data(self):
        expected, selection = self.legacy_data()
        self.assertIs(self.q.check_selection_records(expected, selection), True)

    def test_existing_v1_extra_record_remains_refused(self):
        expected, selection = self.legacy_data()
        expected["files"]["/DATA/v1/EXTRA"] = data_pin(b"EXTRA")
        with self.assertRaisesRegex(RuntimeError, "^LegacyExternalSubsetChanged$"):
            self.q.check_selection_records(expected, selection)

    def test_existing_relative_exec_framing_guard_is_a_real_data_control(self):
        initial = '7 execve("/DATA/tool", ["/DATA/tool"], 0x0) = 0\n'
        self.assertEqual(len(self.q.parse_trace(initial)), 1)
        relative = initial + '7 execve("relative/tool", ["relative/tool"], 0x0) = 0\n'
        with self.assertRaisesRegex(RuntimeError, "^UnsupportedRelativeOrUnknownExec$"):
            self.q.parse_trace(relative)

    def test_existing_cache_metadata_control_never_authenticates_body(self):
        stamp, size = 1700000000, 42
        pair = dict(magic_hex="cb0d0d0a", header_mtime=stamp, header_size=size)
        header = bytes.fromhex("cb0d0d0a") + bytes(4) + stamp.to_bytes(4, "little") + size.to_bytes(4, "little")
        self.q.check_tool_pair(header, dict(size=size, mtime_ns=stamp * 1000000000), pair)
        with self.assertRaisesRegex(RuntimeError, "^ToolCacheHeader$"):
            self.q.check_tool_pair(b"BAD!" + header[4:], dict(size=size, mtime_ns=stamp * 1000000000), pair)


class CurrentAdmissionNegativeTests(unittest.TestCase):
    """POST-API ADOPTION: initial missing keyword is STRUCTURAL, never semantic RED."""
    @classmethod
    def setUpClass(cls):
        cls.q = canonical_helper()

    def require_current_keyword(self, function):
        parameter = inspect.signature(function).parameters.get("current_test")
        self.assertIsNotNone(parameter, "STRUCTURAL_API_NOT_ADOPTED: not a semantic refusal")
        self.assertEqual(parameter.kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertIsNone(parameter.default)

    def test_v2_data_cannot_enter_tool_consumer_without_live_context(self):
        self.require_current_keyword(self.q.verify_tool_selection)
        expected, _ = v2_unaccepted_data()
        with mock.patch.object(self.q, "same", side_effect=AssertionError("FILE_BOUNDARY_BEFORE_CONTEXT")) as same:
            with self.assertRaisesRegex(RuntimeError, "^CurrentTestAcceptedContextRequired$"):
                self.q.verify_tool_selection(expected)
        same.assert_not_called()

    def test_raw_data_receipt_cannot_select_preparation_role(self):
        self.require_current_keyword(self.q.Preparation)
        expected, selection = v2_unaccepted_data()
        receipt = self.q.check_selection_records(expected, selection)
        self.assertEqual(receipt["disposition"], "UNACCEPTED_VALIDATOR_DATA")
        with mock.patch.object(self.q.os, "umask", side_effect=AssertionError("PROCESS_EFFECT_BEFORE_CONTEXT")) as umask:
            with self.assertRaisesRegex(RuntimeError, "^CurrentTestIdentity$"):
                self.q.Preparation("/DATA/no-allocation", "/DATA/no-evidence", expected, current_test=receipt)
        umask.assert_not_called()

    def test_copied_data_receipt_stays_data_not_a_restored_context(self):
        self.require_current_keyword(self.q.admit_capacity)
        expected, selection = v2_unaccepted_data()
        receipt = copy.deepcopy(self.q.check_selection_records(expected, selection))
        with mock.patch.object(self.q, "same", side_effect=AssertionError("FILE_BOUNDARY_BEFORE_CONTEXT")) as same:
            with self.assertRaisesRegex(RuntimeError, "^CurrentTestIdentity$"):
                self.q.admit_capacity(expected, "/DATA/no-evidence", current_test=receipt)
        same.assert_not_called()

    def test_raw_data_receipt_cannot_select_budget_context(self):
        self.require_current_keyword(self.q.EvidenceBudget)
        expected, selection = v2_unaccepted_data()
        receipt = self.q.check_selection_records(expected, selection)
        with self.assertRaisesRegex(RuntimeError, "^CurrentTestIdentity$"):
            self.q.EvidenceBudget(["/DATA/no-evidence"], current_test=receipt)


    def test_v2_data_cannot_enter_preparation_without_live_context(self):
        self.require_current_keyword(self.q.Preparation)
        expected, _ = v2_unaccepted_data()
        with mock.patch.object(self.q.os, "umask", side_effect=AssertionError("PROCESS_EFFECT_BEFORE_CONTEXT")) as umask:
            with self.assertRaisesRegex(RuntimeError, "^CurrentTestAcceptedContextRequired$"):
                self.q.Preparation("/DATA/no-allocation", "/DATA/no-evidence", expected)
        umask.assert_not_called()

    def test_v2_data_cannot_enter_capacity_without_live_context(self):
        self.require_current_keyword(self.q.admit_capacity)
        expected, _ = v2_unaccepted_data()
        with mock.patch.object(self.q, "same", side_effect=AssertionError("FILE_BOUNDARY_BEFORE_CONTEXT")) as same:
            with self.assertRaisesRegex(RuntimeError, "^CurrentTestAcceptedContextRequired$"):
                self.q.admit_capacity(expected, "/DATA/no-evidence")
        same.assert_not_called()

    def test_lower_data_receipt_is_not_a_live_tool_consumer_context(self):
        self.require_current_keyword(self.q.verify_tool_selection)
        expected, selection = v2_unaccepted_data()
        receipt = self.q.check_selection_records(expected, selection)
        with mock.patch.object(self.q, "same", side_effect=AssertionError("FILE_BOUNDARY_BEFORE_CONTEXT")) as same:
            with self.assertRaisesRegex(RuntimeError, "^CurrentTestIdentity$"):
                self.q.verify_tool_selection(expected, current_test=receipt)
        same.assert_not_called()

    def test_mixed_purposes_are_refused_before_context_or_process_effect(self):
        self.require_current_keyword(self.q.Preparation)
        expected, selection = v2_unaccepted_data()
        receipt = self.q.check_selection_records(expected, selection)
        with mock.patch.object(self.q.os, "umask", side_effect=AssertionError("PROCESS_EFFECT_BEFORE_CONTEXT")) as umask:
            with self.assertRaisesRegex(RuntimeError, "^CurrentTestMixedPurpose$"):
                self.q.Preparation("/DATA/no-allocation", "/DATA/no-evidence", expected,
                    campaign={}, current_test=receipt)
        umask.assert_not_called()



if __name__ == "__main__":
    unittest.main()
