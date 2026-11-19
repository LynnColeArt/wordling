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
import tempfile
import zipfile
import base64
import csv
import io
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





def canonical_current_data():
    """Load only the sibling dormant source; no reader action is invoked."""
    path = Path(__file__).with_name('current_test_qualification.py').absolute()
    name = 'current_test_qualification'
    if name in sys.modules:
        module = sys.modules[name]
        if Path(module.__file__).absolute() != path:
            raise RuntimeError('DATA_TEST_FOREIGN_CURRENT_HELPER')
        return module
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or type(spec.loader).__name__ != 'SourceFileLoader':
        raise RuntimeError('DATA_TEST_CURRENT_LOADER_SETUP_FAILURE')
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    # Import must be dormant, including clock and inspected-path I/O.
    import os
    import time
    with mock.patch.object(os, 'open', side_effect=AssertionError('IMPORT_OPEN')), \
         mock.patch.object(time, 'monotonic', side_effect=AssertionError('IMPORT_CLOCK')):
        spec.loader.exec_module(module)
    return module


class StaticReaderDataTests(unittest.TestCase):
    """Supplementary post-RED synthetic DATA; no actual static inspection action.

    Mock descriptors/stat rows are algorithm input, never a Preparation/context or
    evidence of kernel containment. Actual inspection is separately held.
    """
    @classmethod
    def setUpClass(cls):
        cls.c = canonical_current_data()
        import struct
        import stat
        from types import SimpleNamespace
        cls.struct, cls.stat, cls.Namespace = struct, stat, SimpleNamespace

    def setUp(self):
        # Inspected input syscalls are denied unless that individual test supplies
        # synthetic replies. Repository fixture/source reads use normal loaders.
        for name in ('open', 'read', 'pread', 'readlink'):
            patcher = mock.patch.object(self.c.os, name, side_effect=AssertionError('UNMOCKED_INSPECTED_IO:' + name))
            patcher.start()
            self.addCleanup(patcher.stop)

    def plan(self):
        # Fixed tracked repository source DATA, not public reference discovery.
        root = Path(__file__).absolute().parents[5]
        raw = (root / 'docs/research/continuation/test-runtime-qualification-v2/source-stage/static-inspection-design/r7/static-inspection-proposal-r7.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), '58a299ac5acebfd20b5c3ad1ad42a69985e6160ed13ab1ea97e722e451fd4fbd')
        value = json.loads(raw)
        self.c.static_plan_layout_data(value)
        return value

    def inventory(self):
        with mock.patch.object(self.c.time, 'monotonic', return_value=0):
            return self.c._StaticInventory(self.plan(), 18094)

    def header(self, **changes):
        values = dict(kind=3, machine=62, version=1, phoff=64, phsize=56, count=1)
        values.update(changes)
        return self.struct.pack('<16sHHIQQQIHHHHHH', b'\x7fELF\x02\x01\x01' + b'\0' * 9,
            values['kind'], values['machine'], values['version'], 0, values['phoff'], 0, 0,
            64, values['phsize'], values['count'], 0, 0, 0)

    def program(self, kind=1, position=0, address=0, size=256, memory=256, alignment=1):
        return self.struct.pack('<IIQQQQQQ', kind, 5, position, address, 0, size, memory, alignment)

    def info(self, inode=1, mode=None, size=0):
        return self.Namespace(st_dev=1, st_ino=inode, st_size=size, st_mtime_ns=1,
            st_ctime_ns=1, st_mode=(self.stat.S_IFDIR | 0o755) if mode is None else mode,
            st_uid=1000, st_gid=1000)

    def test_header_positive_and_native_format_refusals(self):
        self.assertEqual(self.c.elf_header_data(self.header(), 256)['phcount'], 1)
        for raw in (b'BAD' + self.header()[3:], self.header(machine=183), self.header(count=0),
                    self.header(count=65), self.header(phoff=240), self.header(phsize=64)):
            with self.assertRaises(self.c.Incomplete):
                self.c.elf_header_data(raw, 256)

    def test_program_positive_interval_alignment_and_duplicates(self):
        self.assertEqual(self.c.elf_program_data(self.program(), 256)[0]['size'], 256)
        for raw in (self.program(size=257, memory=257), self.program(size=2, memory=1),
                    self.program(alignment=3), self.program(position=1, address=0, size=1, alignment=2),
                    self.program(kind=3) * 2, self.program(kind=2) * 2):
            with self.assertRaises(self.c.Incomplete):
                self.c.elf_program_data(raw, 256)

    def test_dynamic_requires_real_terminator(self):
        raw = self.struct.pack('<qQqQ', 1, 2, 0, 0)
        self.assertEqual(self.c.elf_dynamic_data(raw), [(1, 2)])
        with self.assertRaisesRegex(self.c.Incomplete, '^ELFDynamicTerminator$'):
            self.c.elf_dynamic_data(raw[:16])

    def test_string_positive_and_exact_terminator_guard(self):
        self.assertEqual(self.c.elf_string_data(b'libc.so.6\0', 0), 'libc.so.6')
        with self.assertRaisesRegex(self.c.Incomplete, '^ELFStringTerminator$'):
            self.c.elf_string_data(b'libc.so.6', 0)
        with self.assertRaisesRegex(self.c.Incomplete, '^ELFStringAscii$'):
            self.c.elf_string_data(b'\xff\0', 0)

    def test_mapping_positive_and_ambiguity_guard(self):
        row = dict(kind=1, offset=10, address=100, size=20)
        self.assertEqual(self.c.elf_string_table_offset([row], 101, 3), 11)
        with self.assertRaisesRegex(self.c.Incomplete, '^ELFStringTableMappingAmbiguous$'):
            self.c.elf_string_table_offset([row, row], 101, 3)

    def test_exact_76_typed_roster_and_changed_plan_rejected(self):
        plan = self.plan()
        self.assertEqual(len(self.c.static_plan_layout_data(plan)), 76)
        bad = copy.deepcopy(plan)
        bad['fixed_item_order'].pop()
        with self.assertRaisesRegex(self.c.GlobalStop, '^StaticPlanRosterConservation$'):
            self.c.static_plan_layout_data(bad)
        with self.assertRaisesRegex(self.c.GlobalStop, '^StaticPlanIdentity$'):
            self.c.static_plan_bytes_data(b'{}')

    def test_listed_alias_chain_is_lexical_and_unlisted_is_refused(self):
        names = {'/DATA/a', '/DATA/b', '/DATA/c'}
        second = self.c.alias_target_data('/DATA/a', 'b', [], names)
        self.assertEqual(second, '/DATA/b')
        self.assertEqual(self.c.alias_target_data(second, 'c', [], names), '/DATA/c')
        with self.assertRaisesRegex(self.c.Incomplete, '^StaticUnlistedAliasTarget:'):
            self.c.alias_target_data('/DATA/a', '../../OUTSIDE', [], names)

    def test_unlisted_path_refused_before_any_open(self):
        inv = self.inventory()
        with mock.patch.object(self.c.time, 'monotonic', return_value=0), \
             mock.patch.object(self.c.os, 'open', side_effect=AssertionError('UNLISTED_OPEN')) as opened:
            with self.assertRaisesRegex(self.c.Incomplete, '^StaticUnlistedPath:'):
                inv.path_info('/DATA/UNLISTED')
        opened.assert_not_called()

    def test_parent_swap_at_open_is_not_hidden_by_final_nofollow(self):
        inv = self.inventory()
        inv.names = {'/DATA', '/DATA/file'}
        inv.directories = {'/DATA'}
        observed = self.info(inode=1)
        changed = self.info(inode=2)
        opened = []
        def fake_open(name, flags, **kwargs):
            opened.append((name, flags, kwargs))
            self.assertTrue(flags & self.c.os.O_NOFOLLOW)
            return 10 if name == '/' else 11
        with mock.patch.object(self.c.time, 'monotonic', return_value=0), \
             mock.patch.object(self.c.os, 'open', side_effect=fake_open), \
             mock.patch.object(self.c.os, 'stat', return_value=observed) as inspected, \
             mock.patch.object(self.c.os, 'fstat', return_value=changed), \
             mock.patch.object(self.c.os, 'close') as closed:
            with self.assertRaisesRegex(self.c.Incomplete, '^StaticParentChanged:/DATA$'):
                inv.path_info('/DATA/file', open_file=True)
        self.assertEqual([row[0] for row in opened], ['/', 'DATA'])
        self.assertFalse(inspected.call_args.kwargs['follow_symlinks'])
        self.assertEqual(set(call.args[0] for call in closed.call_args_list), {10, 11})

    def test_short_metadata_read_charged_and_refused(self):
        inv = self.inventory()
        with mock.patch.object(self.c.time, 'monotonic', return_value=0), \
             mock.patch.object(self.c.os, 'pread', return_value=b'X'):
            with self.assertRaisesRegex(self.c.Incomplete, '^StaticShortMetadataRead$'):
                inv.pread(99, '/DATA/file', 64, 0)
        self.assertEqual(inv.requested, 18094 + 64)
        self.assertEqual(inv.actual, 18094 + 1)

    def test_read_bound_is_checked_before_io(self):
        inv = self.inventory()
        inv.requested = 268435456
        with mock.patch.object(self.c.time, 'monotonic', return_value=0), \
             mock.patch.object(self.c.os, 'pread', side_effect=AssertionError('OVER_BUDGET_READ')) as read:
            with self.assertRaisesRegex(self.c.GlobalStop, '^StaticReadByteBound$'):
                inv.pread(99, '/DATA/file', 1, 0)
        read.assert_not_called()

    def test_file_stability_refusal_closes_descriptor(self):
        inv = self.inventory()
        before = self.info(mode=self.stat.S_IFREG | 0o644, size=1)
        changed = self.info(inode=2, mode=before.st_mode, size=1)
        with mock.patch.object(self.c.time, 'monotonic', return_value=0), \
             mock.patch.object(inv, 'path_info', side_effect=[(before, 99, '/DATA/f', []), (changed, None, '/DATA/f', [])]), \
             mock.patch.object(self.c.os, 'read', return_value=b'x'), \
             mock.patch.object(self.c.os, 'fstat', return_value=before), \
             mock.patch.object(self.c.os, 'close') as closed:
            with self.assertRaisesRegex(self.c.Incomplete, '^StaticFileChangedDuringRead:'):
                inv.item(dict(kind='loader_data', path='/DATA/f'))
        closed.assert_called_once_with(99)

    def test_item_failure_continues_only_fixed_independent_roster(self):
        inv = self.inventory()
        entries = inv.plan['fixed_item_order']
        def item(entry):
            if entry == entries[0]:
                raise self.c.Incomplete('SYNTHETIC_MISSING')
            return dict(**entry, status='OBSERVED_UNACCEPTED_METADATA')
        with mock.patch.object(self.c.time, 'monotonic', return_value=0), mock.patch.object(inv, 'item', side_effect=item) as read:
            result = inv.run()
        self.assertEqual(read.call_count, 76)
        self.assertEqual(result['status'], 'INCOMPLETE')
        self.assertEqual(result['items'][0]['reason'], 'SYNTHETIC_MISSING')
        self.assertFalse(result['permission_granted'])

    def test_global_failure_preserves_partial_and_stops_all_branches(self):
        inv = self.inventory()
        first = dict(**inv.plan['fixed_item_order'][0], status='OBSERVED_UNACCEPTED_METADATA')
        with mock.patch.object(self.c.time, 'monotonic', return_value=0), \
             mock.patch.object(inv, 'item', side_effect=[first, self.c.GlobalStop('SYNTHETIC_GLOBAL')]) as read:
            result = inv.run()
        self.assertEqual(read.call_count, 2)
        self.assertEqual(result['items'], [first])
        self.assertEqual(result['unexamined_items'], 75)
        self.assertEqual(result['global_stop']['reason'], 'SYNTHETIC_GLOBAL')
        self.assertEqual(result['status'], 'INCOMPLETE')

    def test_data_cannot_construct_context_or_start_finite_actions(self):
        with mock.patch.object(self.c.time, 'monotonic', side_effect=AssertionError('ACTION_CLOCK')), \
             mock.patch.object(self.c.os, 'open', side_effect=AssertionError('ACTION_IO')):
            self.assertFalse(self.c._actual_context({'disposition': 'UNACCEPTED_VALIDATOR_DATA'}))
            with self.assertRaisesRegex(TypeError, '^CurrentTestGenuineProducerUnavailable$'):
                self.c._CurrentContext()
            for action in (self.c.capture_reference, self.c.prepare_disposable, self.c.prepare_final,
                           self.c.test_admin, self.c.test_healthy):
                with self.assertRaisesRegex(RuntimeError, '^CurrentTestExecutionClosureUnresolved$'):
                    action()
            self.assertFalse(self.c.current_status()['permission_granted'])




class Static02PartialFactsDataTests(unittest.TestCase):
    """Additional post-STATIC01 DATA contract, never real BASE observations.

    Append to the existing owned DATA test file after review. Uses its existing
    canonical_current_data loader. No new production API or accepted role is
    required for initial semantic RED. Mock descriptor replies are test DATA only.
    """
    @classmethod
    def setUpClass(cls):
        cls.c = canonical_current_data()
        import struct
        import stat
        from types import SimpleNamespace
        cls.struct, cls.stat, cls.Namespace = struct, stat, SimpleNamespace

    def fixture(self, mapping='ONE', strsz=8):
        count = 3 if mapping == 'MULTIPLE' else 2
        raw = bytearray(512)
        raw[:64] = self.struct.pack('<16sHHIQQQIHHHHHH', b'\x7fELF\x02\x01\x01' + b'\0' * 9,
            3, 62, 1, 0, 64, 0, 0, 64, 56, count, 0, 0, 0)
        load = self.struct.pack('<IIQQQQQQ', 1, 5, 0, 0x1000, 0, 512, 512, 1)
        dynamic = self.struct.pack('<IIQQQQQQ', 2, 4, 256, 0, 0, 64, 64, 1)
        raw[64:64 + 56 * count] = load + (load if mapping == 'MULTIPLE' else b'') + dynamic
        address = 0x9999 if mapping == 'ZERO' else 0x1000 + 400
        raw[256:320] = self.struct.pack('<qQqQqQqQ', 5, address, 10, strsz, 1, 0, 0, 0)
        raw[400:408] = b'libx.so\0'
        return bytes(raw)

    def observe(self, payload, target='BASE', unstable=False):
        root = Path(__file__).absolute().parents[5]
        plan = self.c.static_plan_bytes_data((root / self.c._PLAN_REL).read_bytes())
        name = {'BASE': '/home/lynn/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12',
            'cc1': '/usr/libexec/gcc/x86_64-linux-gnu/13/cc1', 'OTHER': '/usr/bin/python3.12'}[target]
        with mock.patch.object(self.c.time, 'monotonic', return_value=0):
            inv = self.c._StaticInventory(plan, 0)
        before = self.Namespace(st_dev=1, st_ino=2, st_size=len(payload), st_mtime_ns=3,
            st_ctime_ns=4, st_mode=self.stat.S_IFREG | 0o755, st_uid=1000, st_gid=1000)
        after = self.Namespace(**vars(before))
        if unstable:
            after.st_ino = 99
        original_item = inv.item
        def item(entry):
            if entry['path'] == name and entry['kind'] == 'ELF_seed':
                return original_item(entry)
            return dict(**entry, status='OBSERVED_UNACCEPTED_METADATA')
        reads = []
        def pread(fd, size, offset):
            self.assertEqual(fd, 99)
            reads.append((offset, size))
            # Refused mappings/large strings must not trigger any strtab read.
            return payload[offset:offset + size]
        with mock.patch.object(self.c.time, 'monotonic', return_value=0), \
             mock.patch.object(self.c.os, 'open', side_effect=AssertionError('UNEXPECTED_INSPECTED_OPEN')), \
             mock.patch.object(self.c.os, 'readlink', side_effect=AssertionError('UNEXPECTED_READLINK')), \
             mock.patch.object(inv, 'path_info', side_effect=[(before, 99, name, []), (after, None, name, [])]), \
             mock.patch.object(self.c.os, 'read', return_value=payload), \
             mock.patch.object(self.c.os, 'pread', side_effect=pread), \
             mock.patch.object(self.c.os, 'fstat', return_value=before), \
             mock.patch.object(self.c.os, 'close') as closed, \
             mock.patch.object(inv, 'item', side_effect=item):
            inventory = inv.run()
        closed.assert_called_once_with(99)
        row = next(r for r in inventory['items'] if r['path'] == name and r['kind'] == 'ELF_seed')
        self.assertFalse(inventory['permission_granted'])
        self.assertFalse(inventory['current_context_created'])
        return row, inventory, reads

    def partial(self, row, payload, stability):
        self.assertEqual(row['status'], 'INCOMPLETE')
        # Current canonical run/item reaches real parser refusal and returns its
        # bare INCOMPLETE row. The assertIn below is the intended semantic RED.
        self.assertIn('file_observation', row, 'STATIC02_PARSE_REFUSAL_DISCARDED_KNOWN_FILE_FACTS')
        facts = row['file_observation']
        self.assertEqual(facts['stream_sha256'], hashlib.sha256(payload).hexdigest())
        self.assertEqual(facts['stream_bytes'], len(payload))
        self.assertTrue(facts['stream_hash_complete'])
        self.assertEqual(facts['stability'], stability)
        self.assertNotIn('ELF', row, 'parse-refused partial row must not enter safe graph pool')
        return row['ELF_diagnostic']

    def test_positive_existing_stable_parser_control(self):
        raw = self.fixture()
        row, _, reads = self.observe(raw)
        self.assertEqual(row['status'], 'OBSERVED_UNACCEPTED_METADATA')
        self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual(row['ELF']['needed'], ['libx.so'])
        self.assertIn((400, 8), reads)

    def test_zero_mapping_preserves_stable_identity_and_diagnostic(self):
        raw = self.fixture(mapping='ZERO')
        row, _, reads = self.observe(raw)
        self.assertEqual(row['reason'], 'ELFStringTableMappingAmbiguous')
        diagnostic = self.partial(row, raw, 'STABLE_IDENTITY')
        self.assertEqual(diagnostic['mapping']['state'], 'ZERO')
        self.assertEqual(diagnostic['mapping']['count'], 0)
        self.assertEqual(diagnostic['dynamic']['strtab_va'], 0x9999)
        self.assertEqual(diagnostic['dynamic']['strsz'], 8)
        self.assertFalse(diagnostic['strtab_read_performed'])
        self.assertEqual(reads, [(0, 64), (64, 112), (256, 64)])

    def test_multiple_mapping_is_distinct_and_never_selects_first(self):
        raw = self.fixture(mapping='MULTIPLE')
        row, _, reads = self.observe(raw)
        self.assertEqual(row['reason'], 'ELFStringTableMappingAmbiguous')
        diagnostic = self.partial(row, raw, 'STABLE_IDENTITY')
        self.assertEqual(diagnostic['mapping']['state'], 'MULTIPLE')
        self.assertEqual(diagnostic['mapping']['count'], 2)
        self.assertFalse(diagnostic['strtab_read_performed'])
        self.assertEqual(reads, [(0, 64), (64, 168), (256, 64)])

    def test_strsz_refusal_preserves_value_without_larger_read(self):
        raw = self.fixture(strsz=67108865)
        row, _, reads = self.observe(raw, target='cc1')
        self.assertEqual(row['reason'], 'ELFStringTableBound')
        diagnostic = self.partial(row, raw, 'STABLE_IDENTITY')
        self.assertEqual(diagnostic['dynamic']['strsz'], 67108865)
        self.assertFalse(diagnostic['strtab_read_performed'])
        self.assertEqual(reads, [(0, 64), (64, 112), (256, 64)])

    def test_parse_refusal_hash_does_not_become_stable_identity_after_change(self):
        raw = self.fixture(mapping='ZERO')
        row, inventory, _ = self.observe(raw, unstable=True)
        self.partial(row, raw, 'UNSTABLE_IDENTITY')
        self.assertNotIn('stable_identity', row['file_observation'])
        self.assertEqual(inventory['status'], 'INCOMPLETE')
        self.assertEqual(inventory['graph'], [])

    def test_nonselected_seed_preserves_original_bare_refusal(self):
        # Added after the original observed RED, to conserve the approved narrow
        # BASE/cc1 retention scope. This name is synthetic DATA, never opened.
        self.assertEqual(self.c._DIAGNOSTIC_NAMES, frozenset((
            '/home/lynn/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12',
            '/usr/libexec/gcc/x86_64-linux-gnu/13/cc1')))
        row, inventory, _ = self.observe(self.fixture(mapping='ZERO'), target='OTHER')
        self.assertEqual(row, dict(kind='ELF_seed', path='/usr/bin/python3.12',
            status='INCOMPLETE', reason='ELFStringTableMappingAmbiguous'))
        self.assertEqual(inventory['graph'], [])




class Static03StringTableDataTests(unittest.TestCase):
    """Unaccepted synthetic metadata, never physical BASE/cc1 input or a role."""
    @classmethod
    def setUpClass(cls):
        cls.c = canonical_current_data()
        import struct
        cls.struct = struct

    def row(self, address, offset, size, memory=None):
        return dict(kind=1, flags=4, address=address, offset=offset, size=size,
            memory=size if memory is None else memory)

    def checked_offset(self, programs, address, size):
        try:
            return self.c.elf_string_table_offset(programs, address, size)
        except self.c.Incomplete as error:
            self.fail('STATIC03_CANONICAL_CONTIGUOUS_FILE_COVERAGE_REQUIRED:' + str(error))

    def test_recorded_adjacent_filebacked_union_reaches_canonical_mapping(self):
        # Literal integer DATA from the independently preserved STATIC02 report;
        # expected1496 is VA4191704 minus recorded common bias4190208.
        programs = [self.row(4190208, 0, 4096), self.row(4194304, 4096, 134512)]
        self.assertEqual(self.checked_offset(programs, 4191704, 42266), 1496)

    def test_recorded_large_cc1_logical_table_is_not_a_whole_copy_request(self):
        programs = [self.row(4194304, 0, 2135512)]
        self.assertEqual(self.checked_offset(programs, 5062960, 1199001), 868656)

    def test_union_rejects_each_gap_bias_overlap_memsz_and_u64_wrap_variant(self):
        # Six logical DATA cases, charged separately in the command manifest.
        cases = [
            ('VA_GAP', [self.row(100, 0, 16), self.row(117, 17, 32)], 108, 20),
            ('FILE_GAP_BIAS_CHANGE', [self.row(100, 0, 16), self.row(116, 17, 32)], 108, 20),
            ('PARTIAL_CONFLICTING_OVERLAP', [self.row(100, 0, 40), self.row(116, 200, 32)], 108, 20),
            ('PARTIAL_IDENTICAL_BIAS_OVERLAP', [self.row(100, 0, 40), self.row(116, 16, 32)], 108, 20),
            ('MEMSZ_ONLY_TAIL', [self.row(100, 0, 16, memory=64)], 108, 20),
            ('ELF64_NONWRAP', [self.row(2**64 - 4, 0, 16)], 2**64 - 2, 8),
        ]
        for name, programs, address, size in cases:
            with self.subTest(logical_DATA_case=name):
                with self.assertRaises(self.c.Incomplete):
                    self.c.elf_string_table_offset(programs, address, size)
        # Existing StaticReaderDataTests retains duplicate/identical-overlap
        # refusal. None of those old negatives is removed or relabeled positive.

    def sparse_elf(self, relative=1000000, raw_string=None):
        # A sparse byte-reply fixture: no1199001-byte table is allocated or read.
        table_size, file_size, table_offset = 1199001, 2200000, 400
        if raw_string is None:
            raw_string = b'libOK.so\0' + b'X' * (4096 - 9)
        header = self.struct.pack('<16sHHIQQQIHHHHHH', b'\x7fELF\x02\x01\x01' + b'\0' * 9,
            3, 62, 1, 0, 64, 0, 0, 64, 56, 2, 0, 0, 0)
        programs = (self.struct.pack('<IIQQQQQQ', 1, 4, 0, 4096, 0, file_size, file_size, 1)
            + self.struct.pack('<IIQQQQQQ', 2, 4, 256, 0, 0, 64, 64, 1))
        dynamic = self.struct.pack('<qQqQqQqQ', 5, 4096 + table_offset, 10, table_size, 1, relative, 0, 0)
        replies = {(0, 64): header, (64, 112): programs, (256, 64): dynamic}
        reads = []
        def pread(fd, count, position):
            self.assertEqual(fd, 99)
            self.assertLessEqual(count, 4096, 'WHOLE_LOGICAL_TABLE_COPY_FORBIDDEN')
            reads.append((position, count))
            if (position, count) in replies:
                return replies[(position, count)]
            self.assertEqual(position, table_offset + relative)
            self.assertLess(relative, table_size, 'OUTSIDE_LOGICAL_TABLE_READ')
            self.assertEqual(count, min(4096, table_size - relative))
            self.assertGreaterEqual(len(raw_string), count)
            return raw_string[:count]
        root = Path(__file__).absolute().parents[5]
        plan = self.c.static_plan_bytes_data((root / self.c._PLAN_REL).read_bytes())
        with mock.patch.object(self.c.time, 'monotonic', return_value=0):
            inv = self.c._StaticInventory(plan, 0)
        return inv, pread, reads, file_size

    def parse_sparse(self, relative=1000000, raw_string=None):
        inv, pread, reads, size = self.sparse_elf(relative, raw_string)
        diagnostic = {}
        with mock.patch.object(self.c.time, 'monotonic', return_value=0), \
             mock.patch.object(self.c.os, 'open', side_effect=AssertionError('UNEXPECTED_PUBLIC_OPEN')), \
             mock.patch.object(self.c.os, 'pread', side_effect=pread):
            result = inv.elf(99, '/home/lynn/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12', size, diagnostic)
        return result, reads, inv, diagnostic

    def test_large_logical_table_fetches_only_referenced_string_window(self):
        try:
            result, reads, inv, diagnostic = self.parse_sparse()
        except self.c.Incomplete as error:
            self.fail('STATIC03_REFERENCED_WINDOW_REQUIRED:' + str(error))
        self.assertEqual(result['needed'], ['libOK.so'])
        self.assertEqual(reads, [(0, 64), (64, 112), (256, 64), (1000400, 4096)])
        self.assertEqual(inv.actual, 4336)
        self.assertTrue(diagnostic['strtab_read_performed'])

    def test_suffix_window_stops_at_logical_table_end(self):
        try:
            result, reads, _, _ = self.parse_sparse(relative=1198997, raw_string=b'a\0xx')
        except self.c.Incomplete as error:
            self.fail('STATIC03_SUFFIX_WINDOW_REQUIRED:' + str(error))
        self.assertEqual(result['needed'], ['a'])
        self.assertEqual(reads[-1], (1199397, 4))

    def test_missing_nul_is_refused_inside_canonical_4096_window(self):
        with self.assertRaisesRegex(self.c.Incomplete, '^ELFStringTerminator$'):
            self.parse_sparse(raw_string=b'A' * 4096)

    def test_string_offset_at_table_end_refused_before_window_read(self):
        with self.assertRaisesRegex(self.c.Incomplete, '^ELFStringOffset$'):
            self.parse_sparse(relative=1199001)




class Static04InterpreterGraphDataTests(unittest.TestCase):
    """Pure graph DATA fixtures only: no observed file, actor or live context.

    Uses the existing canonical run()/graph API for initial semantic RED. The
    mocked item rows are metadata inputs, never a forged Preparation/Case/role.
    """
    @classmethod
    def setUpClass(cls):
        cls.c = canonical_current_data()

    def observed(self, scenario='ALIAS', reverse=False):
        import copy
        root = Path(__file__).absolute().parents[5]
        plan = self.c.static_plan_bytes_data((root / self.c._PLAN_REL).read_bytes())
        source = '/usr/bin/python3.12'
        logical = '/lib64/ld-linux-x86-64.so.2'
        target = '/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2'
        alternate_alias = '/usr/lib64/ld-linux-x86-64.so.2'
        alternate_seed = '/usr/lib/x86_64-linux-gnu/libm.so.6'
        def elf(path, interpreter=None):
            return dict(kind='ELF_seed', path=path, resolved=path, aliases=[],
                mode=0o755, uid=0, gid=0, size=256, sha256='1' * 64,
                status='OBSERVED_UNACCEPTED_METADATA', ELF=dict(kind=3, machine=62,
                    program_headers=1, interpreter=interpreter, needed=[], soname=None, rpath=None, runpath=None))
        source_row = elf(source, target if scenario == 'DIRECT' else logical)
        target_row = elf(target)
        alias_row = dict(kind='alias', path=logical, resolved=target, mode=0o755, uid=0, gid=0,
            status='OBSERVED_UNACCEPTED_METADATA', aliases=[dict(logical=logical,
                text=target, target=target, mode=0o777, uid=0, gid=0)])
        rowmap = {('ELF_seed', source): source_row, ('ELF_seed', target): target_row,
                  ('alias', logical): alias_row}
        if scenario.startswith('ALIAS_BAD_'):
            bad = scenario.removeprefix('ALIAS_BAD_')
            if bad == 'MISSING':
                rowmap.pop(('alias', logical))
            elif bad == 'MALFORMED':
                alias_row['resolved'] = 12
            elif bad == 'MALFORMED_CHAIN':
                alias_row['aliases'][0]['target'] = 12
            else:
                alias_row['status'] = bad
                if bad == 'INCOMPLETE':
                    alias_row['file_observation'] = dict(stability='UNSTABLE_IDENTITY')
        if scenario.startswith('TARGET_BAD_'):
            bad = scenario.removeprefix('TARGET_BAD_')
            if bad == 'MISSING':
                rowmap.pop(('ELF_seed', target))
            elif bad == 'MALFORMED':
                target_row['sha256'] = 'NOT_A_CANONICAL_DIGEST'
            elif bad == 'MALFORMED_ELF':
                target_row['ELF']['machine'] = '62'
            else:
                target_row['status'] = bad
                if bad == 'INCOMPLETE':
                    target_row['file_observation'] = dict(stability='UNSTABLE_IDENTITY')
        if scenario == 'DUPLICATE_ALIAS':
            other = copy.deepcopy(alias_row)
            other['status'] = 'INCOMPLETE'
            other['file_observation'] = dict(stability='UNSTABLE_IDENTITY')
            if reverse:
                rowmap[('alias', logical)] = other
                rowmap[('alias', alternate_alias)] = alias_row
            else:
                rowmap[('alias', alternate_alias)] = other
        if scenario in ('DUPLICATE_TARGET', 'PARTIAL_DUPLICATE_TARGET'):
            other = copy.deepcopy(target_row)
            other['sha256'] = '2' * 64
            if scenario == 'PARTIAL_DUPLICATE_TARGET':
                other['status'] = 'INCOMPLETE'
                other['file_observation'] = dict(stability='UNSTABLE_IDENTITY')
            if reverse:
                rowmap[('ELF_seed', target)] = other
                rowmap[('ELF_seed', alternate_seed)] = target_row
            else:
                rowmap[('ELF_seed', alternate_seed)] = other
        if scenario == 'UNLISTED_ALIAS':
            source_row['ELF']['interpreter'] = '/DATA/UNLISTED_LOADER'
            alias_row['path'] = '/DATA/UNLISTED_LOADER'
        if scenario == 'MALFORMED_SOURCE':
            source_row['sha256'] = 'NOT_A_CANONICAL_DIGEST'
        def item(entry):
            return copy.deepcopy(rowmap.get((entry['kind'], entry['path']),
                dict(**entry, status='INCOMPLETE', reason='SYNTHETIC_UNUSED_DATA_ONLY')))
        with mock.patch.object(self.c.time, 'monotonic', return_value=0):
            inventory = self.c._StaticInventory(plan, 0)
        with mock.patch.object(self.c.time, 'monotonic', return_value=0), \
             mock.patch.object(inventory, 'item', side_effect=item), \
             mock.patch.object(self.c.os, 'open', side_effect=AssertionError('GRAPH_PUBLIC_OPEN')), \
             mock.patch.object(self.c.os, 'stat', side_effect=AssertionError('GRAPH_PUBLIC_STAT')), \
             mock.patch.object(self.c.os, 'readlink', side_effect=AssertionError('GRAPH_PUBLIC_READLINK')):
            result = inventory.run()
        edges = [row for row in result['graph'] if row.get('source') == source and 'interpreter' in row]
        self.assertFalse(result['permission_granted'])
        self.assertFalse(result['reference_qualification'])
        self.assertFalse(result['current_context_created'])
        return edges, target

    def refused(self, scenario, reverse=False):
        edges, _ = self.observed(scenario, reverse)
        self.assertEqual(len(edges), 1)
        self.assertIsNone(edges[0]['target'])
        self.assertTrue(edges[0]['status'].startswith('INCOMPLETE'))
        self.assertFalse(edges[0].get('permission_granted', False))

    def test_existing_direct_safe_seed_control(self):
        edges, _ = self.observed('DIRECT')
        self.assertFalse(any(row['status'].startswith('INCOMPLETE') for row in edges))

    def test_existing_run_graph_resolves_only_completed_declared_alias_metadata(self):
        edges, target = self.observed()
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]['target'], target, 'STATIC04_SAFE_OBSERVED_ALIAS_GRAPH_REQUIRED')
        self.assertEqual(edges[0]['status'], 'DECLARED_UNACCEPTED_DATA')
        self.assertFalse(edges[0]['permission_granted'])
        self.assertFalse(edges[0]['reference_qualification'])
        self.assertFalse(edges[0]['current_context_created'])
        self.assertFalse(self.c._actual_context(edges[0]))

    def test_alias_zero_partial_foreign_receipt_and_malformed_refuse(self):
        for status in ('MISSING', 'INCOMPLETE', 'UNACCEPTED_VALIDATOR_DATA', 'MALFORMED', 'MALFORMED_CHAIN'):
            with self.subTest(DATA_variant=status):
                self.refused('ALIAS_BAD_' + status)

    def test_target_zero_partial_foreign_receipt_and_malformed_refuse(self):
        for status in ('MISSING', 'INCOMPLETE', 'UNACCEPTED_VALIDATOR_DATA', 'MALFORMED', 'MALFORMED_ELF'):
            with self.subTest(DATA_variant=status):
                self.refused('TARGET_BAD_' + status)

    def test_alias_ambiguity_refuses_partial_duplicate_in_both_orders(self):
        for reverse in (False, True):
            with self.subTest(DATA_variant='partial_first' if reverse else 'partial_last'):
                self.refused('DUPLICATE_ALIAS', reverse)

    def test_target_ambiguity_refuses_complete_and_partial_duplicates(self):
        self.refused('DUPLICATE_TARGET')
        for reverse in (False, True):
            with self.subTest(DATA_variant='partial_first' if reverse else 'partial_last'):
                self.refused('PARTIAL_DUPLICATE_TARGET', reverse)

    def test_unlisted_alias_and_malformed_source_refuse_without_lookup(self):
        for scenario in ('UNLISTED_ALIAS', 'MALFORMED_SOURCE'):
            with self.subTest(DATA_variant=scenario):
                self.refused(scenario)




class SourceCensusDataTests(unittest.TestCase):
    """SOURCE-only census DATA. Initial RED invokes the already-existing item API.

    All /DATA paths below are synthetic. Actual descriptor controls use only one
    owned TemporaryDirectory under /tmp, remove it on exit, and never call main.
    New pure helper tests run only AFTER those helpers exist; missing APIs are setup.
    """
    @classmethod
    def setUpClass(cls):
        cls.c = canonical_current_data()

    def fixture(self):
        import stat
        from types import SimpleNamespace
        c = self.c
        directory = SimpleNamespace(st_dev=1, st_ino=1, st_mode=stat.S_IFDIR | 0o700,
            st_uid=1000, st_gid=1000, st_size=0, st_mtime_ns=1, st_ctime_ns=1)
        regular = SimpleNamespace(st_dev=1, st_ino=2, st_mode=stat.S_IFREG | 0o600,
            st_uid=1000, st_gid=1000, st_size=3, st_mtime_ns=1, st_ctime_ns=1)
        name = '/DATA/census'
        plan = dict(id='SOURCE_CENSUS01', declared_logical_aliases=[],
            declared_exact_ancestor_metadata=['/', '/DATA', name],
            declared_metadata_only_directories=[name], declared_ELF_seed_files=[],
            declared_nonexecuted_loader_data_files=[],
            fixed_item_order=[dict(kind='census_root', path=name)],
            census_options=dict(disposition='UNACCEPTED_SYNTHETIC_SOURCE_DATA',
                roots=[name], records=8, reads=65536, output=4096, operations=1024,
                deadline=30, depth=2, working=65536))
        with mock.patch.object(c.time, 'monotonic', return_value=0):
            inv = c._StaticInventory(plan, 0)
        emitted = []
        inv._census_emit = emitted.append  # lower DATA sink, never a live actor/role
        def path_info(path, open_file=False, *, open_directory=False):
            if path == name:
                return directory, 70 if open_directory else None, name, []
            if path == name + '/member.bin':
                return regular, 71 if open_file else None, path, []
            raise c.Incomplete('SYNTHETIC_UNLISTED:' + path)
        class Scan:
            def __enter__(self): return iter([SimpleNamespace(name='member.bin')])
            def __exit__(self, *args): return False
        stack = __import__('contextlib').ExitStack()
        stack.enter_context(mock.patch.object(c.time, 'monotonic', return_value=0))
        stack.enter_context(mock.patch.object(inv, 'path_info', side_effect=path_info))
        stack.enter_context(mock.patch.object(c.os, 'scandir', side_effect=lambda fd: Scan()))
        stack.enter_context(mock.patch.object(c.os, 'read', side_effect=[b'abc']))
        stack.enter_context(mock.patch.object(c.os, 'fstat', side_effect=lambda fd: directory if fd == 70 else regular))
        stack.enter_context(mock.patch.object(c.os, 'stat', side_effect=lambda path, **kw: regular if path == 'member.bin' else directory))
        stack.enter_context(mock.patch.object(c.os, 'readlink', side_effect=AssertionError('UNDECLARED_SYNTHETIC_READLINK')))
        stack.enter_context(mock.patch.object(c.os, 'close'))
        stack.enter_context(mock.patch.object(c.os, 'open', side_effect=AssertionError('UNDECLARED_SYNTHETIC_OPEN')))
        return inv, emitted, stack, name

    def test_existing_directory_metadata_positive_control(self):
        inv, rows, stack, name = self.fixture()
        with stack:
            row = inv.item(dict(kind='directory', path=name))
        self.assertEqual(row['status'], 'OBSERVED_UNACCEPTED_METADATA')
        self.assertEqual(row['path'], name)
        self.assertEqual(rows, [])

    def test_existing_item_boundary_requires_census_membership_not_bare_metadata(self):
        inv, rows, stack, name = self.fixture()
        with stack:
            row = inv.item(dict(kind='census_root', path=name))
        self.assertIn('census', row, 'SOURCE_CENSUS_MEMBERSHIP_REQUIRED')
        self.assertEqual(row['census']['records'], 1)
        self.assertEqual(row['census']['file_bytes'], 3)
        # Literal canonical membership preimage, independently derived from
        # this synthetic one-member fixture before any production postimage.
        membership_preimage = b'{"gid":1000,"mode":384,"name":"member.bin","sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","size":3,"type":"file","uid":1000}\n'
        self.assertEqual(hashlib.sha256(membership_preimage).hexdigest(),
            'fb686eb8a388c35e3a7f8f760fe4f976ef6948664fccd9b8a3de8ae9bbf83db2')
        self.assertTrue(row['census']['membership_complete'])
        self.assertEqual(row['census']['membership_sha256'],
            'fb686eb8a388c35e3a7f8f760fe4f976ef6948664fccd9b8a3de8ae9bbf83db2')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['path'], name + '/member.bin')
        self.assertEqual(rows[0]['sha256'], hashlib.sha256(b'abc').hexdigest())
        self.assertFalse(row['permission_granted'])
        self.assertFalse(row['reference_qualification'])

    def test_postcode_regular_hash_read_charge_precedes_actual_io(self):
        inv, rows, stack, name = self.fixture()
        inv.plan['census_options']['reads'] = 2
        with stack, mock.patch.object(self.c.os, 'read', side_effect=AssertionError('UNCHARGED_READ')):
            with self.assertRaisesRegex(self.c.GlobalStop, '^CensusReadBound$'):
                inv.item(dict(kind='census_root', path=name))
        self.assertEqual(rows, [])

    def test_postcode_no_ambient_alias_or_parent_search(self):
        for text in ('/DATA/OUTSIDE', '../OUTSIDE'):
            with self.subTest(text=text):
                result = self.c.census_alias_data('/DATA/census/link', text,
                    ['/DATA/census'], [])
                self.assertEqual(result['status'], 'INCOMPLETE_UNLISTED_CENSUS_ALIAS')
                self.assertFalse(result['follow'])

    def test_postcode_parent_and_membership_snapshots_are_both_required(self):
        baseline = dict(dev=1, ino=1, mode=0o700, uid=1000, gid=1000, size=0, mtime_ns=1, ctime_ns=1)
        for changed in ('inode', 'names'):
            before, after = copy.deepcopy(baseline), copy.deepcopy(baseline)
            if changed == 'inode': after['ino'] = 2
            row = self.c.census_snapshot_data(before, after, ['member.bin'],
                ['other.bin'] if changed == 'names' else ['member.bin'])
            self.assertEqual(row['status'], 'INCOMPLETE_UNSTABLE_CENSUS')
            self.assertFalse(row['stable_identity'])

    def test_postcode_package_zero_multiple_and_foreign_names_never_select_first(self):
        for names in ([], ['pip-1.dist-info', 'pip-2.dist-info'], ['pipper-1.dist-info']):
            with self.subTest(names=names):
                row = self.c.census_package_data('pip', names)
                self.assertEqual(row['status'], 'INCOMPLETE_PACKAGE_SELECTION')
                self.assertIsNone(row['selected'])
        self.assertEqual(self.c.census_package_data('pip', ['pip-1.dist-info'])['selected'], 'pip-1.dist-info')

    def test_postcode_literal_header_and_unknown_macro_are_distinct(self):
        positive = self.c.census_header_data(b'#include <sys/socket.h>\n#include "local.h"\n')
        self.assertEqual(positive['tokens'], ['sys/socket.h', 'local.h'])
        self.assertFalse(positive['unresolved'])
        self.assertEqual(positive['includes'], [dict(token='sys/socket.h', kind='angle'),
            dict(token='local.h', kind='quoted')])
        left = self.c._census_header_candidates_data(
            dict(token='config.h', kind='quoted', parent='/DATA/one'), ['/DATA/system'])
        right = self.c._census_header_candidates_data(
            dict(token='config.h', kind='quoted', parent='/DATA/two'), ['/DATA/system'])
        angle = self.c._census_header_candidates_data(
            dict(token='config.h', kind='angle', parent=None), ['/DATA/system'])
        self.assertEqual(left['candidates'], ['/DATA/one/config.h', '/DATA/system/config.h'])
        self.assertEqual(right['candidates'], ['/DATA/two/config.h', '/DATA/system/config.h'])
        self.assertEqual(angle['candidates'], ['/DATA/system/config.h'])
        self.assertNotEqual(left['identity'], right['identity'])
        self.assertNotEqual(left['identity'], angle['identity'])
        # Reuse the existing synthetic descriptor fixture for a stable empty
        # header. Presence and scoped-name cleanup cannot depend on byte growth.
        inv, rows, stack, name = self.fixture()
        with stack:
            self.c.os.fstat(71).st_size = 0
            prior_names, prior_dirs = set(inv.names), set(inv.directories)
            state = self.c._CensusState(inv)
            includes, present = self.c._census_file_fact(state, name + '/member.bin', header=True)
        self.assertTrue(present)
        self.assertEqual(includes, [])
        self.assertEqual(state.file_bytes, 0)
        self.assertEqual(state.memory, 0)
        self.assertEqual(inv.names, prior_names)
        self.assertEqual(inv.directories, prior_dirs)
        for raw in (b'#include HEADER\n', b'#include "../escape.h"\n', b'#include <' + b'x' * 4097 + b'>\n'):
            self.assertTrue(self.c.census_header_data(raw)['unresolved'])

    def test_postcode_record_work_and_memory_bounds_are_independent(self):
        for key, error in (('records', 'CensusRecordBound'), ('operations', 'CensusOperationBound'),
                           ('working', 'CensusMemoryBound')):
            inv, rows, stack, name = self.fixture()
            inv.plan['census_options'][key] = 0
            with stack:
                with self.assertRaisesRegex(self.c.GlobalStop, '^' + error + '$'):
                    inv.item(dict(kind='census_root', path=name))

    def test_postcode_output_bound_and_failed_sink_preserve_no_false_success(self):
        inv, rows, stack, name = self.fixture()
        inv.plan['census_options']['output'] = 1
        with stack:
            with self.assertRaisesRegex(self.c.GlobalStop, '^CensusOutputBound$'):
                inv.item(dict(kind='census_root', path=name))
        self.assertEqual(rows, [])
        inv, rows, stack, name = self.fixture()
        inv._census_emit = mock.Mock(side_effect=OSError('OWNED_SYNTHETIC_SINK_FAILURE'))
        with stack:
            with self.assertRaisesRegex(OSError, 'OWNED_SYNTHETIC_SINK_FAILURE'):
                inv.item(dict(kind='census_root', path=name))

    def actual_fixture(self):
        import tempfile
        task = tempfile.TemporaryDirectory(prefix='wordling-wp108-source-census-FD-', dir='/tmp')
        self.addCleanup(task.cleanup)
        tree = Path(task.name) / 'tree'
        tree.mkdir(mode=0o700)
        (tree / 'member.bin').write_bytes(b'abc')
        return tree

    def owned_census(self, tree, rows):
        # Same canonical lower item API with a smaller source-DATA plan, no
        # production-only test hook, context, main or fixed public plan load.
        ancestors = [str(x) for x in reversed(tree.parents)] + [str(tree)]
        plan = dict(id='SOURCE_CENSUS01', declared_logical_aliases=[],
            declared_exact_ancestor_metadata=ancestors,
            declared_metadata_only_directories=[str(tree)],
            declared_ELF_seed_files=[], declared_nonexecuted_loader_data_files=[],
            fixed_item_order=[dict(kind='census_root', path=str(tree))],
            census_options=dict(disposition='UNACCEPTED_SYNTHETIC_SOURCE_DATA',
                roots=[str(tree)], records=8, reads=65536, output=4096,
                operations=4096, deadline=30, depth=2, working=65536))
        inv = self.c._StaticInventory(plan, 0)
        inv._census_emit = rows.append
        return inv.item(dict(kind='census_root', path=str(tree)))

    def test_postcode_owned_real_FD_hash_membership_and_cleanup(self):
        tree = self.actual_fixture()
        # This lower canonical DATA helper accepts only a held owned fixture root,
        # not a current context/reference. Production fixed plan is never loaded.
        rows = []
        result = self.owned_census(tree, rows)
        self.assertEqual(result['census']['records'], 1)
        self.assertEqual(rows[0]['sha256'], hashlib.sha256(b'abc').hexdigest())
        self.assertFalse(result['permission_granted'])
        self.assertFalse(result['reference_qualification'])
        self.assertFalse(self.c._actual_context(result))

    def test_postcode_owned_real_FD_symlink_never_follows_external_target(self):
        tree = self.actual_fixture()
        (tree / 'link').symlink_to('../OUTSIDE')
        rows = []
        result = self.owned_census(tree, rows)
        links = [r for r in rows if r['path'].endswith('/link')]
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]['status'], 'INCOMPLETE_UNLISTED_CENSUS_ALIAS')
        self.assertFalse(links[0]['follow'])
        self.assertFalse(result['reference_qualification'])

    def test_postcode_owned_real_FD_parent_swap_is_refused(self):
        tree = self.actual_fixture()
        real_open = self.c.os.open
        changed = False
        def swap(path, flags, *args, **kwargs):
            nonlocal changed
            if path == 'member.bin':
                self.assertTrue(flags & self.c.os.O_NOFOLLOW, 'CENSUS_MEMBER_NOFOLLOW_REQUIRED')
            if path == 'member.bin' and not changed:
                changed = True
                (tree / 'member.bin').rename(tree / 'old.bin')
                (tree / 'member.bin').symlink_to('../OUTSIDE')
            return real_open(path, flags, *args, **kwargs)
        rows = []
        with mock.patch.object(self.c.os, 'open', side_effect=swap):
            result = self.owned_census(tree, rows)
        self.assertTrue(changed)
        self.assertEqual(result['status'], 'INCOMPLETE')
        self.assertFalse(result['permission_granted'])
        self.assertFalse(any(r.get('sha256') == hashlib.sha256(b'OUTSIDE').hexdigest() for r in rows))

    def test_postcode_census_receipt_remains_unaccepted_and_ops_blocked(self):
        self.assertEqual(self.c.current_status()['live_contexts'], 0)
        with self.assertRaisesRegex(TypeError, 'CurrentTestGenuineProducerUnavailable'):
            self.c._CurrentContext()
        for name in ('capture_reference', 'prepare_disposable', 'prepare_final', 'test_admin', 'test_healthy'):
            with self.assertRaisesRegex(RuntimeError, 'CurrentTestExecutionClosureUnresolved'):
                getattr(self.c, name)()




class CurrentReferenceRoleDataTests(unittest.TestCase):
    """Actual canonical record consumer DATA; no live context is fabricated."""
    @classmethod
    def setUpClass(cls):
        cls.q = canonical_helper()

    def data(self, target='/DATA/runtime/python', role='RUNTIME_ALIAS', resolution='CAPTURED_SINGLE_HOP'):
        e, s = v2_unaccepted_data()
        e['links']['/DATA/runtime/alias'] = dict(target=target, resolved=target,
            rights=dict(mode=0o777, uid=1000, gid=1000), role=role, resolution=resolution)
        s['roles_sha256'] = digest(roles_projection(e))
        return e, s

    def test_existing_record_consumer_positive_control(self):
        e, s = v2_unaccepted_data()
        result = self.q.check_selection_records(e, s)
        self.assertEqual(result['disposition'], 'UNACCEPTED_VALIDATOR_DATA')
        self.assertEqual(result['provider_records'], 8)

    def test_existing_record_consumer_rejects_runtime_alias_without_captured_target(self):
        e, s = self.data('/DATA/UNKNOWN_TARGET')
        # Digest consistency is currently accepted; missing target is the
        # semantic gap, before any allocation and without missing APIs.
        with self.assertRaisesRegex(RuntimeError, '^CurrentRuntimeAliasTarget$'):
            self.q.check_selection_records(e, s)

    def test_captured_runtime_alias_is_still_only_unaccepted_DATA(self):
        e, s = self.data()
        self.assertEqual(self.q.check_selection_records(e, s)['disposition'],
            'UNACCEPTED_VALIDATOR_DATA')
        with mock.patch.object(self.q.Path, 'read_bytes', side_effect=AssertionError('ROLE_DATA_READ')):
            with self.assertRaisesRegex(RuntimeError, '^CurrentTestAcceptedContextRequired$'):
                self.q.verify_tool_selection(e)

    def test_external_metadata_alias_never_grows_runtime(self):
        e, s = self.data('/DATA/UNKNOWN_TARGET', 'NONEXECUTED_METADATA', 'LEXICAL_ONLY_NO_FOLLOW')
        before = copy.deepcopy(e['runtime_elf'])
        self.assertEqual(self.q.check_selection_records(e, s)['disposition'], 'UNACCEPTED_VALIDATOR_DATA')
        self.assertEqual(e['runtime_elf'], before)

    def test_malformed_alias_rights_refused_by_existing_consumer(self):
        for key, value in (('mode', True), ('uid', '1000')):
            e, s = self.data()
            e['links']['/DATA/runtime/alias']['rights'][key] = value
            s['roles_sha256'] = digest(roles_projection(e))
            with self.assertRaisesRegex(RuntimeError, '^CurrentReferenceAliasSchema$'):
                self.q.check_selection_records(e, s)

        # Post-RED grammar variants: digest-consistent JSON containers must
        # reach explicit schema refusals before any set/update/dict-key use.
        for bad in ([], {}):
            for field, error in (('closed_roots', 'CurrentReferenceRootSchema'),
                    ('runtime_elf', 'CurrentToolSelectionSchema'),
                    ('tool_startup_hook_sets', 'CurrentToolHookSchema'),
                    ('shell_aliases', 'CurrentToolAliasSchema')):
                with self.subTest(field=field, bad=bad):
                    e, s = self.data()
                    if field == 'shell_aliases':
                        s[field] = [dict(logical=bad, text='x', resolved='/DATA/tool/python',
                            rights=dict(mode=0o777, uid=1000, gid=1000))]
                    elif field == 'tool_startup_hook_sets':
                        e[field] = {'/DATA/hooks': [bad]}
                    else:
                        e[field] = [bad]
                    s['roles_sha256'] = digest(roles_projection(e))
                    with self.assertRaisesRegex(RuntimeError, '^' + error + '$'):
                        self.q.check_selection_records(e, s)

    def test_TOOL_endpoint_cannot_be_relabelled_runtime_alias(self):
        e, s = self.data('/DATA/tool/python')
        with self.assertRaisesRegex(RuntimeError, '^CurrentRuntimeAliasRole$'):
            self.q.check_selection_records(e, s)

    def test_runtime_alias_requires_captured_not_lexical_resolution(self):
        e, s = self.data(resolution='LEXICAL_ONLY_NO_FOLLOW')
        with self.assertRaisesRegex(RuntimeError, '^CurrentRuntimeAliasResolution$'):
            self.q.check_selection_records(e, s)

    def test_raw_role_receipt_cannot_allocate_preparation(self):
        e, s = self.data()
        receipt = self.q.check_selection_records(e, s)
        with mock.patch.object(self.q.os, 'umask', side_effect=AssertionError('PRE_ADMISSION_EFFECT')):
            with self.assertRaisesRegex(RuntimeError, '^CurrentTestIdentity$'):
                self.q.Preparation('/DATA/final', '/DATA/evidence', e, current_test=receipt)
            with self.assertRaisesRegex(RuntimeError, '^CurrentActualOwnerBudgetRequired$'):
                self.q.EvidenceBudget(['/DATA/evidence'], current_owner=receipt)



class CurrentWheelSourceDataTests(unittest.TestCase):
    """Post-RED canonical shared wheel guard; two tiny owned files, no role."""
    def test_source_pin_is_checked_before_payload_read_on_both_wheel_routes(self):
        canonical_helper()
        path = Path(__file__).with_name('controller_deployment.py').resolve()
        spec = importlib.util.spec_from_file_location('controller_deployment', path)
        self.assertEqual(type(spec.loader).__name__, 'SourceFileLoader')
        deployment = importlib.util.module_from_spec(spec)
        sys.modules['controller_deployment'] = deployment
        spec.loader.exec_module(deployment)
        payload = b'INDEPENDENT SOURCE DATA\n'
        name = 'reference_controller/source-data.bin'
        dist = 'wordling_reference_controller_test-0.2.0.dist-info'
        bodies = {name: payload,
            dist + '/METADATA': b'Name: wordling-reference-controller-test\nVersion: 0.2.0\nRequires-Python: >=3.12\n',
            dist + '/WHEEL': b'Wheel-Version: 1.0\n',
            dist + '/top_level.txt': b'reference_controller\n'}
        record = io.StringIO(newline='')
        writer = csv.writer(record, lineterminator='\n')
        for member, body in bodies.items():
            writer.writerow([member, 'sha256=' + base64.urlsafe_b64encode(hashlib.sha256(body).digest()).rstrip(b'=').decode('ascii'), str(len(body))])
        writer.writerow([dist + '/RECORD', '', ''])
        bodies[dist + '/RECORD'] = record.getvalue().encode('ascii')
        wanted = dict(size=len(payload), sha256=hashlib.sha256(payload).hexdigest())
        with tempfile.TemporaryDirectory(prefix='wordling-wp108-wheel-DATA-') as temporary:
            directory = Path(temporary)
            source = directory / 'source.bin'
            source.write_bytes(payload)
            wheel = directory / 'inert.whl'
            with zipfile.ZipFile(wheel, 'w', compression=zipfile.ZIP_STORED) as archive:
                for member, body in bodies.items():
                    archive.writestr(member, body)
            self.assertLess(source.stat().st_size + wheel.stat().st_size, 4096)
            self.assertEqual(deployment.review_wheel(wheel, {name: (source, wanted)}), {name: wanted})
            original_open = Path.open
            def no_unfrozen_payload_read(value, *args, **kwargs):
                if value == source:
                    raise AssertionError('UNFROZEN_WHEEL_SOURCE_READ')
                return original_open(value, *args, **kwargs)
            with mock.patch.object(Path, 'open', no_unfrozen_payload_read):
                with self.assertRaisesRegex(RuntimeError, '^WheelReviewedPayload:' + name + '$'):
                    deployment.review_wheel(wheel, {name: (source, dict(wanted, sha256='0' * 64))})
        self.assertFalse(directory.exists())

if __name__ == "__main__":
    unittest.main()
