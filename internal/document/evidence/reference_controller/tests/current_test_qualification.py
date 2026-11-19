"""Dormant current-TEST DATA boundary and finite static input inspection.

The static reader never executes an input or accepts a reference/role. Operational
current contexts remain unavailable until their separately reviewed real closure.
No TEST/P/Original modules, factories, deployment or probe are imported here.
ELF metadata definitions: https://gabi.xinuos.com/elf/02-eheader.html,
https://gabi.xinuos.com/elf/07-pheader.html and /elf/08-dynamic.html.
"""
import hashlib
import json
import os
from pathlib import Path
import posixpath
import stat
import struct
import sys
import time

_PLAN_SHA = 'c2b36c986ec841628b4e834870f1f381d26ae4a569d3b849cb4612789d03271f'
_PLAN_REL = 'docs/research/continuation/test-runtime-qualification-v2/source-stage/static-inspection-design/static04/reader-plan.json'
_DIAGNOSTIC_NAMES = frozenset((
    '/home/lynn/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12',
    '/usr/libexec/gcc/x86_64-linux-gnu/13/cc1'))
_UNRESOLVED = ('reference roots/source review', 'BASE/stdlib/config/aliases/rights',
    'runtime native loader/dependency/mapped data', 'compiler/offline tools/cache/header closure',
    'actual reference capture and independent acceptance', 'writer/joint-memory/clock/case closure',
    'genuine finite coordinator and accepted current-context producer')
_LIVE_CONTEXTS = set()


class _CurrentContext:
    """No DATA constructor or reconstruction route exists in this checkpoint."""
    __slots__ = ()

    def __new__(cls):
        raise TypeError('CurrentTestGenuineProducerUnavailable')

    def __copy__(self):
        raise TypeError('CurrentTestContextNotCopyable')

    def __deepcopy__(self, memo):
        raise TypeError('CurrentTestContextNotCopyable')

    def __reduce__(self):
        raise TypeError('CurrentTestContextNotSerializable')


def _actual_context(value):
    return type(value) is _CurrentContext and value in _LIVE_CONTEXTS


def current_status():
    return dict(schema='wordling.current-test-dormant-status/v1',
        disposition='UNACCEPTED_DATA_ONLY', unresolved=list(_UNRESOLVED),
        live_contexts=len(_LIVE_CONTEXTS), permission_granted=False)


def _operational_blocked():
    raise RuntimeError('CurrentTestExecutionClosureUnresolved')


# These finite names cannot start a clock or turn a record/schema into a role.
# Real implementations await the closed reference/coordinator source stage.
capture_reference = _operational_blocked
prepare_disposable = _operational_blocked
prepare_final = _operational_blocked
test_admin = _operational_blocked
test_healthy = _operational_blocked


class Incomplete(Exception):
    """A single declared item is unread/unaccepted; never an authority result."""


class GlobalStop(Exception):
    """The entire finite inventory stops; remaining items are not examined."""


def elf_header_data(raw, file_size):
    """Decode bounded ELF64 LE/x86_64 header DATA, without loading any input."""
    if type(raw) is not bytes or len(raw) != 64 or type(file_size) is not int or file_size < 64:
        raise Incomplete('ELFHeaderBound')
    if raw[:7] != b'\x7fELF\x02\x01\x01':
        raise Incomplete('ELFFormatUnsupported')
    fields = struct.unpack('<16sHHIQQQIHHHHHH', raw)
    _, kind, machine, version, _, phoff, _, _, ehsize, phsize, phcount, _, _, _ = fields
    if kind not in (2, 3) or machine != 62 or version != 1 or ehsize != 64:
        raise Incomplete('ELFNativeHeaderUnsupported')
    if phsize != 56 or not 1 <= phcount <= 64 or phoff < 64 or phoff + phsize * phcount > file_size:
        raise Incomplete('ELFProgramHeaderBound')
    return dict(kind=kind, machine=machine, phoff=phoff, phsize=phsize, phcount=phcount)


def elf_program_data(raw, file_size):
    if type(raw) is not bytes or not raw or len(raw) % 56 or len(raw) > 4096:
        raise Incomplete('ELFProgramTableBound')
    rows = []
    for offset in range(0, len(raw), 56):
        kind, flags, position, address, _, size, memory, alignment = struct.unpack_from('<IIQQQQQQ', raw, offset)
        if position > file_size or size > file_size - position or (kind == 1 and size > memory):
            raise Incomplete('ELFSegmentInterval')
        if kind == 1 and alignment not in (0, 1) and (alignment & (alignment - 1) or address % alignment != position % alignment):
            raise Incomplete('ELFLoadAlignment')
        rows.append(dict(kind=kind, flags=flags, offset=position, address=address, size=size, memory=memory))
    if len(rows) > 64:
        raise Incomplete('ELFProgramCount')
    if sum(r['kind'] == 3 for r in rows) > 1 or sum(r['kind'] == 2 for r in rows) > 1:
        raise Incomplete('ELFAmbiguousMetadataSegment')
    return rows


def elf_dynamic_data(raw):
    if type(raw) is not bytes or not raw or len(raw) % 16 or len(raw) > 65536:
        raise Incomplete('ELFDynamicBound')
    entries = []
    for offset in range(0, len(raw), 16):
        tag, value = struct.unpack_from('<qQ', raw, offset)
        if tag == 0:
            return entries
        entries.append((tag, value))
    raise Incomplete('ELFDynamicTerminator')


def elf_string_data(raw, offset):
    if type(raw) is not bytes or len(raw) > 65536 or type(offset) is not int or not 0 <= offset < len(raw):
        raise Incomplete('ELFStringOffset')
    end = raw.find(b'\0', offset, min(len(raw), offset + 4096))
    if end < 0 or end == offset:
        raise Incomplete('ELFStringTerminator')
    value = raw[offset:end]
    if not value.isascii():
        raise Incomplete('ELFStringAscii')
    return value.decode('ascii')


def elf_string_table_offset(programs, address, size, *, diagnostic=None):
    """Prove one contiguous file interval for the WHOLE logical VA table.

    This is the single canonical mapping decision. Its diagnostic is DATA,
    never a second predicate or authority. Memory-only bytes cannot contribute.
    """
    if (type(address) is not int or type(size) is not int or not 0 <= address < 2**64
            or not 0 < size <= 67108864 or size > 2**64 - address):
        _diagnostic_update(diagnostic, mapping=dict(state='NOT_EVALUATED_STRING_BOUND', count=None, candidates=[]))
        raise Incomplete('ELFStringTableBound')
    if type(programs) is not list or not 1 <= len(programs) <= 64:
        raise Incomplete('ELFStringTableProgramBound')
    end = address + size
    relevant = []
    for index, row in enumerate(programs):
        if type(row) is not dict or type(row.get('kind')) is not int:
            raise Incomplete('ELFStringTableProgramBound')
        if row['kind'] != 1:
            continue
        if (any(type(row.get(k)) is not int or not 0 <= row[k] < 2**64
                for k in ('address', 'offset', 'size'))
                or row['size'] > 2**64 - row['address'] or row['size'] > 2**64 - row['offset']):
            raise Incomplete('ELFStringTableSegmentBound')
        start = max(address, row['address'])
        stop = min(end, row['address'] + row['size'])
        if start < stop:
            relevant.append(dict(program_index=index, VA_start=start, VA_end=stop,
                file_offset=row['offset'] + start - row['address'],
                bias=row['address'] - row['offset']))
    relevant.sort(key=lambda row: (row['VA_start'], row['VA_end'], row['program_index']))
    if not relevant:
        _diagnostic_update(diagnostic, mapping=dict(state='ZERO', count=0, candidates=[]))
        raise Incomplete('ELFStringTableMappingAmbiguous')
    first = relevant[0]['file_offset']
    bias = relevant[0]['bias']
    VA_cursor, file_cursor = address, first
    for row in relevant:
        # Inspect EVERY intersection, even after apparent complete coverage.
        # A full first match must not hide a later partial/identical overlap.
        state = None
        if row['VA_start'] < VA_cursor:
            state = 'MULTIPLE'
        elif row['VA_start'] != VA_cursor:
            state = 'VA_GAP'
        elif row['file_offset'] != file_cursor or row['bias'] != bias:
            state = 'FILE_DISCONTIGUOUS'
        if state is not None:
            _diagnostic_update(diagnostic, mapping=dict(state=state, count=len(relevant), candidates=relevant))
            raise Incomplete('ELFStringTableMappingAmbiguous')
        file_cursor += row['VA_end'] - row['VA_start']
        VA_cursor = row['VA_end']
    if VA_cursor != end or file_cursor != first + size:
        _diagnostic_update(diagnostic, mapping=dict(state='VA_GAP', count=len(relevant), candidates=relevant))
        raise Incomplete('ELFStringTableMappingAmbiguous')
    _diagnostic_update(diagnostic, mapping=dict(state='CONTIGUOUS_FILE_BACKED', count=len(relevant),
        candidates=relevant, file_offset=first, logical_size=size, whole_range_proved=True))
    return first


def alias_target_data(prefix, text, remaining, names):
    """Pure lexical DATA. It never resolves/queries a filesystem target."""
    if type(text) is not str or len(os.fsencode(text)) > 4096:
        raise GlobalStop('StaticAliasTextBound')
    target = posixpath.normpath(text if text.startswith('/') else posixpath.join(posixpath.dirname(prefix), text))
    target = posixpath.normpath(posixpath.join(target, *remaining))
    if target not in names:
        raise Incomplete('StaticUnlistedAliasTarget:' + target)
    return target


def static_plan_layout_data(plan):
    keys = (('ancestor', 'declared_exact_ancestor_metadata'), ('alias', 'declared_logical_aliases'),
            ('directory', 'declared_metadata_only_directories'), ('ELF_seed', 'declared_ELF_seed_files'),
            ('loader_data', 'declared_nonexecuted_loader_data_files'))
    expected = [dict(kind=kind, path=path) for kind, key in keys for path in plan[key]]
    # Historical/current lower DATA grammars are unaccepted. The action reads
    # only the one source-pinned active plan; a DATA id cannot raise any cap.
    count = {'STATIC01': 76, 'STATIC02': 109, 'STATIC03': 117, 'STATIC04': 135}.get(plan.get('id'))
    if count is None or len(expected) != count or plan['fixed_item_order'] != expected:
        raise GlobalStop('StaticPlanRosterConservation')
    return expected


def static_plan_bytes_data(raw):
    if type(raw) is not bytes or len(raw) > 32768 or hashlib.sha256(raw).hexdigest() != _PLAN_SHA:
        raise GlobalStop('StaticPlanIdentity')
    value = json.loads(raw)
    if value['schema'] != 'wordling.wp108-finite-static-inspection-proposal/v2':
        raise GlobalStop('StaticPlanSchema')
    static_plan_layout_data(value)
    return value


def _stamp(value):
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def _rights(value):
    return dict(mode=stat.S_IMODE(value.st_mode), uid=value.st_uid, gid=value.st_gid)


def _identity(value):
    return dict(device=value.st_dev, inode=value.st_ino, size=value.st_size,
        mtime_ns=value.st_mtime_ns, ctime_ns=value.st_ctime_ns, **_rights(value))


def _diagnostic_update(diagnostic, **values):
    if diagnostic is None:
        return
    candidate = dict(diagnostic, **values)
    # Inputs here are already bounded canonical header/program/tag DATA. This
    # extra cap applies inside, never in addition to, the existing output cap.
    raw = json.dumps(candidate, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')
    if len(raw) > 32768:
        raise GlobalStop('StaticDiagnosticByteBound')
    diagnostic.update(values)


def interpreter_edge_data(source_row, original_rows, declared_alias_names, declared_ELF_seed_names):
    """Pure completed-observation DATA lookup, never a live/reference binding.

    Original matching rows are counted BEFORE eligibility filtering. Incomplete
    duplicates cannot disappear into the graph's last-wins needed-edge view.
    No path resolution, revalidation, filesystem access or runtime search occurs.
    """
    name = source_row.get('resolved') if type(source_row) is dict else None
    literal = source_row.get('ELF', {}).get('interpreter') if (type(source_row) is dict
        and type(source_row.get('ELF')) is dict) else None
    edge = dict(source=name, interpreter=literal, target=None,
        status='INCOMPLETE_UNLISTED_OR_AMBIGUOUS_INTERPRETER',
        permission_granted=False, reference_qualification=False, current_context_created=False)
    if (type(original_rows) is not list or len(original_rows) > 135
            or type(declared_alias_names) is not list or len(declared_alias_names) > 135
            or type(declared_ELF_seed_names) is not list or len(declared_ELF_seed_names) > 135
            or any(type(n) is not str for n in declared_alias_names + declared_ELF_seed_names)):
        return edge
    alias_names = set(declared_alias_names)
    seed_names = set(declared_ELF_seed_names)

    def rights(row):
        return (all(type(row.get(k)) is int and 0 <= row[k] < 2**64 for k in ('mode', 'uid', 'gid'))
            and row['mode'] <= 0o7777)

    def string(value):
        return type(value) is str and 0 < len(value) < 4096 and value.isascii()

    def links(row, required=False):
        values = row['aliases']
        return (type(values) is list and int(required) <= len(values) <= 8
            and all(type(link) is dict and len(link) == 6
                and set(link) == {'logical', 'text', 'target', 'mode', 'uid', 'gid'}
                and type(link['logical']) is str and link['logical'] in alias_names
                and type(link['text']) is str and 0 < len(link['text']) <= 4096 and link['text'].isascii()
                and type(link['target']) is str
                and link['target'] in alias_names | seed_names and rights(link) for link in values))

    def elf_values(value):
        return (type(value) is dict and len(value) == 8
            and set(value) == {'kind', 'machine', 'program_headers', 'interpreter', 'needed', 'soname', 'rpath', 'runpath'}
            and type(value['kind']) is int and value['kind'] in (2, 3)
            and type(value['machine']) is int and value['machine'] == 62
            and type(value['program_headers']) is int and 1 <= value['program_headers'] <= 64
            and all(value[k] is None or string(value[k]) for k in ('interpreter', 'soname', 'rpath', 'runpath'))
            and type(value['needed']) is list and len(value['needed']) <= 128
            and all(string(text) for text in value['needed']))

    def complete_seed(row):
        keys = {'kind', 'path', 'resolved', 'aliases', 'mode', 'uid', 'gid', 'status', 'size', 'sha256', 'ELF'}
        return (type(row) is dict and len(row) == 11 and set(row) == keys
            and row['kind'] == 'ELF_seed' and row['status'] == 'OBSERVED_UNACCEPTED_METADATA'
            and type(row['path']) is str and row['path'] in seed_names
            and type(row['resolved']) is str and row['resolved'] in seed_names
            and links(row) and rights(row)
            and type(row['size']) is int and 64 <= row['size'] <= 67108864
            and type(row['sha256']) is str and len(row['sha256']) == 64
            and all(c in '0123456789abcdef' for c in row['sha256'])
            and elf_values(row['ELF']))

    def complete_alias(row):
        keys = {'kind', 'path', 'resolved', 'aliases', 'mode', 'uid', 'gid', 'status'}
        return (type(row) is dict and len(row) == 8 and set(row) == keys
            and row['kind'] == 'alias' and row['status'] == 'OBSERVED_UNACCEPTED_METADATA'
            and type(row['path']) is str and row['path'] in alias_names
            and type(row['resolved']) is str and row['resolved'] in seed_names
            and links(row, required=True) and rights(row))

    def seed_matches(path):
        return [row for row in original_rows if type(row) is dict and row.get('kind') == 'ELF_seed'
            and (row.get('path') == path or row.get('resolved') == path)]

    if not complete_seed(source_row) or type(literal) is not str:
        return edge
    sources = seed_matches(source_row['resolved'])
    if len(sources) != 1 or sources[0] is not source_row:
        return edge
    direct = seed_matches(literal)
    if direct:
        if len(direct) != 1 or not complete_seed(direct[0]):
            return edge
        target = direct[0]['resolved']
    else:
        aliases = [row for row in original_rows if type(row) is dict
            and row.get('kind') == 'alias' and row.get('path') == literal]
        if len(aliases) != 1 or not complete_alias(aliases[0]):
            return edge
        targets = seed_matches(aliases[0]['resolved'])
        if len(targets) != 1 or not complete_seed(targets[0]):
            return edge
        target = targets[0]['resolved']
    edge.update(target=target, status='DECLARED_UNACCEPTED_DATA')
    return edge


def _load_static_plan():
    # A fixed reviewed repository DATA document, never a caller path or role.
    root = Path(__file__).absolute().parents[5]
    path = root / _PLAN_REL
    # Source DATA is a fixed repository input, not a discovered public role.
    # Anchor its parents too: final O_NOFOLLOW alone is insufficient.
    directory = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    fd = None
    try:
        for part in path.parts[1:-1]:
            before = os.stat(part, dir_fd=directory, follow_symlinks=False)
            if not stat.S_ISDIR(before.st_mode):
                raise GlobalStop('StaticSourcePlanParentType')
            following = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory)
            if _stamp(before) != _stamp(os.fstat(following)):
                os.close(following)
                raise GlobalStop('StaticSourcePlanParentChanged')
            os.close(directory)
            directory = following
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory)
        initial = os.fstat(fd)
        size = initial.st_size
        if not stat.S_ISREG(initial.st_mode) or not 0 <= size <= 32768:
            raise GlobalStop('StaticPlanByteBound')
        raw = os.read(fd, size + 1)
        if len(raw) != size or hashlib.sha256(raw).hexdigest() != _PLAN_SHA:
            raise GlobalStop('StaticPlanIdentity')
        if _stamp(initial) != _stamp(os.fstat(fd)):
            raise GlobalStop('StaticSourcePlanChanged')
    finally:
        if fd is not None:
            os.close(fd)
        os.close(directory)
    return static_plan_bytes_data(raw), len(raw)


class _StaticInventory:
    """Finite read-only metadata scope. Not a supervisor, role or validator grant."""
    def __init__(self, plan, source_bytes):
        self.plan = plan
        self.aliases = set(plan['declared_logical_aliases'])
        self.directories = set(plan['declared_exact_ancestor_metadata']) | set(plan['declared_metadata_only_directories'])
        self.names = self.aliases | self.directories | set(plan['declared_ELF_seed_files']) | set(plan['declared_nonexecuted_loader_data_files'])
        self.end = time.monotonic() + 30
        self.requested = source_bytes
        self.actual = source_bytes
        self.per_file = {}
        self.metadata = 0
        self.metadata_total = 0
        self.operations = 0
        self.rows = []
        self.output_reserved = 8192

    def check(self):
        if time.monotonic() >= self.end:
            raise GlobalStop('StaticWholeDeadline')
        self.operations += 1
        if self.operations > 76 * 64 * 8:
            raise GlobalStop('StaticComponentWorkBound')

    def charge(self, name, count, metadata=False):
        self.check()
        if type(count) is not int or count < 0 or count > 65536:
            raise GlobalStop('StaticReadChunkBound')
        previous = self.per_file.get(name, 0)
        if previous + count > 67108864 or self.requested + count > 268435456:
            raise GlobalStop('StaticReadByteBound')
        if metadata and self.metadata + count > 1048576:
            raise Incomplete('ELFMetadataReadBound')
        if metadata and self.metadata_total + count > 16777216:
            raise GlobalStop('StaticTotalMetadataReadBound')
        self.requested += count
        self.per_file[name] = previous + count
        if metadata:
            self.metadata += count
            self.metadata_total += count

    def pread(self, fd, name, count, offset, diagnostic=None):
        self.charge(name, count, metadata=True)
        # A failed charge has not performed I/O. Report the strtab syscall only
        # after its canonical charge succeeds, including a later short read.
        _diagnostic_update(diagnostic, strtab_read_performed=True)
        raw = os.pread(fd, count, offset)
        self.actual += len(raw)
        if len(raw) != count:
            raise Incomplete('StaticShortMetadataRead')
        return raw

    def path_info(self, path, open_file=False, *, open_directory=False):
        """Walk from a held root, no-follow EVERY component before any input read."""
        original = path
        chain = []
        for hop in range(9):
            self.check()
            if path not in self.names or not path.startswith('/') or '..' in Path(path).parts:
                raise Incomplete('StaticUnlistedPath:' + path)
            pieces = [p for p in path.split('/') if p]
            if len(pieces) > 64:
                raise GlobalStop('StaticPathDepthBound')
            directory = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
            restart = None
            try:
                if not pieces:
                    return os.fstat(directory), None, path, chain
                for index, part in enumerate(pieces):
                    self.check()
                    prefix = '/' + '/'.join(pieces[:index + 1])
                    last = index == len(pieces) - 1
                    if prefix not in self.names:
                        raise Incomplete('StaticUnlistedParent:' + prefix)
                    before = os.stat(part, dir_fd=directory, follow_symlinks=False)
                    if stat.S_ISLNK(before.st_mode):
                        if prefix not in self.aliases or hop == 8:
                            raise Incomplete('StaticUnlistedOrDeepAlias:' + prefix)
                        text = os.readlink(part, dir_fd=directory)
                        remaining = pieces[index + 1:]
                        target = alias_target_data(prefix, text, remaining, self.names)
                        after = os.stat(part, dir_fd=directory, follow_symlinks=False)
                        if _stamp(before) != _stamp(after):
                            raise Incomplete('StaticAliasChanged:' + prefix)
                        chain.append(dict(logical=prefix, text=text, target=target, **_rights(before)))
                        restart = target
                        break
                    if not last:
                        if prefix not in self.directories or not stat.S_ISDIR(before.st_mode):
                            raise Incomplete('StaticParentNotDeclaredDirectory:' + prefix)
                        following = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory)
                        if _stamp(os.fstat(following)) != _stamp(before):
                            os.close(following)
                            raise Incomplete('StaticParentChanged:' + prefix)
                        os.close(directory)
                        directory = following
                    else:
                        if open_file or open_directory:
                            if open_directory and not stat.S_ISDIR(before.st_mode):
                                raise Incomplete('StaticNotDirectory:' + original)
                            if open_file and not stat.S_ISREG(before.st_mode):
                                raise Incomplete('StaticNotRegular:' + original)
                            fd = os.open(part, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | (os.O_DIRECTORY if open_directory else 0), dir_fd=directory)
                            if _stamp(os.fstat(fd)) != _stamp(before):
                                os.close(fd)
                                raise Incomplete('StaticFileChangedAtOpen:' + original)
                            return before, fd, path, chain
                        return before, None, path, chain
            finally:
                os.close(directory)
            if restart is None:
                raise GlobalStop('StaticPathTraversalInvariant')
            path = restart
        raise Incomplete('StaticAliasDepthBound')

    def elf(self, fd, name, size, diagnostic=None):
        self.metadata = 0
        _diagnostic_update(diagnostic, phase='header', strtab_read_performed=False)
        raw_header = self.pread(fd, name, 64, 0)
        _diagnostic_update(diagnostic, header_raw_hex=raw_header.hex())
        h = elf_header_data(raw_header, size)
        _diagnostic_update(diagnostic, header=h, phase='program_headers')
        programs = elf_program_data(self.pread(fd, name, h['phsize'] * h['phcount'], h['phoff']), size)
        _diagnostic_update(diagnostic, program_headers=programs)
        result = dict(kind=h['kind'], machine=h['machine'], program_headers=len(programs), interpreter=None,
                      needed=[], soname=None, rpath=None, runpath=None)
        for row in programs:
            if row['kind'] == 3:
                _diagnostic_update(diagnostic, phase='interpreter')
                if not 1 < row['size'] <= 4096:
                    raise Incomplete('ELFInterpreterBound')
                result['interpreter'] = elf_string_data(self.pread(fd, name, row['size'], row['offset']), 0)
            if row['kind'] == 2:
                _diagnostic_update(diagnostic, phase='dynamic')
                entries = elf_dynamic_data(self.pread(fd, name, row['size'], row['offset']))
                singles = {}
                dynamic = dict(strtab_va=None, strsz=None, entries_decoded=len(entries))
                _diagnostic_update(diagnostic, dynamic=dynamic)
                for tag, value in entries:
                    if tag in (5, 10):
                        field = {5: 'strtab_va', 10: 'strsz'}[tag]
                        if tag in singles:
                            _diagnostic_update(diagnostic, duplicate_dynamic_entry=dict(tag=tag, value=value))
                        else:
                            dynamic = dict(dynamic, **{field: value})
                            _diagnostic_update(diagnostic, dynamic=dynamic)
                    if tag in (5, 10, 14, 15, 29):
                        if tag in singles:
                            raise Incomplete('ELFDuplicateDynamicSingleton')
                        singles[tag] = value
                strings = [(tag, value) for tag, value in entries if tag in (1, 14, 15, 29)]
                if len(strings) > 131 or sum(tag == 1 for tag, _ in strings) > 128:
                    raise Incomplete('ELFDynamicStringCount')
                if strings:
                    if 5 not in singles or 10 not in singles:
                        raise Incomplete('ELFDynamicStringTableMissing')
                    _diagnostic_update(diagnostic, phase='string_table_mapping')
                    position = elf_string_table_offset(programs, singles[5], singles[10], diagnostic=diagnostic)
                    # Whole logical coverage and actual frozen-file bounds
                    # precede every referenced window. Never copy the table.
                    if position < 0 or position > size or singles[10] > size - position:
                        raise Incomplete('ELFStringTableFileBound')
                    for tag, value in strings:
                        if type(value) is not int or not 0 <= value < singles[10]:
                            raise Incomplete('ELFStringOffset')
                        window_size = min(4096, singles[10] - value)
                        _diagnostic_update(diagnostic, phase='string_window_read')
                        window = self.pread(fd, name, window_size, position + value, diagnostic)
                        text = elf_string_data(window, 0)
                        if tag == 1:
                            result['needed'].append(text)
                        else:
                            result[{14: 'soname', 15: 'rpath', 29: 'runpath'}[tag]] = text
        _diagnostic_update(diagnostic, phase='complete')
        return result

    def item(self, entry):
        if entry.get('kind') == 'census_root':
            return _census_item_data(self, entry)
        kind, name = entry['kind'], entry['path']
        before, fd, resolved, aliases = self.path_info(name, open_file=kind in ('ELF_seed', 'loader_data'))
        row = dict(kind=kind, path=name, resolved=resolved, aliases=aliases, **_rights(before))
        if fd is None:
            if kind in ('ancestor', 'directory') and not stat.S_ISDIR(before.st_mode):
                raise Incomplete('StaticNotDirectory:' + name)
            if kind == 'alias' and not aliases:
                row['alias_observation'] = 'DECLARED_LOGICAL_NAME_IS_REGULAR_OR_DIRECTORY'
            return dict(row, status='OBSERVED_UNACCEPTED_METADATA')
        try:
            if before.st_size > 67108864:
                raise GlobalStop('StaticFileSizeReadBound')
            digest = hashlib.sha256()
            remaining = before.st_size
            while remaining:
                size = min(65536, remaining)
                self.charge(name, size)
                raw = os.read(fd, size)
                self.actual += len(raw)
                if not raw:
                    raise Incomplete('StaticShortFileRead:' + name)
                remaining -= len(raw)
                digest.update(raw)
            row.update(size=before.st_size, sha256=digest.hexdigest())
            parse_error = None
            diagnostic = {} if kind == 'ELF_seed' and name in _DIAGNOSTIC_NAMES else None
            if kind == 'ELF_seed':
                try:
                    row['ELF'] = self.elf(fd, name, before.st_size, diagnostic)
                except Incomplete as error:
                    if diagnostic is None:
                        raise
                    parse_error = error
                    _diagnostic_update(diagnostic, refusal=str(error)[:512])
            after = os.fstat(fd)
            current = None
            path_failure = None
            try:
                current, _, current_path, _ = self.path_info(name)
            except (Incomplete, FileNotFoundError, NotADirectoryError) as error:
                if parse_error is None:
                    raise
                path_failure = str(error)[:512]
                current_path = None
            stable = (current is not None and _stamp(before) == _stamp(after)
                and _stamp(before) == _stamp(current) and current_path == resolved)
            if parse_error is not None:
                observation = dict(stream_sha256=row['sha256'], stream_bytes=before.st_size,
                    stream_hash_complete=True, stability='STABLE_IDENTITY' if stable else 'UNSTABLE_IDENTITY',
                    identity_before=_identity(before), identity_fd_after=_identity(after),
                    identity_path_after=None if current is None else _identity(current),
                    path_after=current_path, path_refusal=path_failure)
                if stable:
                    observation['stable_identity'] = _identity(before)
                # No completed ELF field or OBSERVED status: retained partial
                # hashes/diagnostics cannot enter run()'s safe graph pool.
                del row['sha256'], row['size']
                row.update(status='INCOMPLETE', reason=str(parse_error)[:512], file_observation=observation)
                if diagnostic is not None:
                    row['ELF_diagnostic'] = diagnostic
                return row
            if not stable:
                raise Incomplete('StaticFileChangedDuringRead:' + name)
            return dict(row, status='OBSERVED_UNACCEPTED_METADATA')
        finally:
            os.close(fd)

    def append(self, row):
        raw = json.dumps(row, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')
        if self.output_reserved + len(raw) + 1 > 262144:
            raise GlobalStop('StaticOutputReservationBound')
        self.output_reserved += len(raw) + 1
        self.rows.append(row)

    def run(self):
        failure = None
        entries = self.plan['fixed_item_order']
        for entry in entries:
            try:
                self.check()
                try:
                    row = self.item(entry)
                except (Incomplete, FileNotFoundError, NotADirectoryError) as error:
                    row = dict(**entry, status='INCOMPLETE', reason=str(error)[:512])
                self.append(row)
            except BaseException as error:
                failure = dict(type=type(error).__name__, reason=str(error)[:512])
                break
        safe = {r['resolved']: r for r in self.rows if r['status'] == 'OBSERVED_UNACCEPTED_METADATA' and 'ELF' in r}
        graph = []
        # Graph serialization is charged before growth, just like item rows.
        # A global fault cannot renew the clock or continue graph work.
        if failure is None:
            try:
                for name, row in safe.items():
                    for needed in row['ELF']['needed']:
                        self.check()
                        matches = [n for n, value in safe.items() if value['ELF']['soname'] == needed or posixpath.basename(n) == needed]
                        edge = dict(source=name, needed=needed, target=matches[0] if len(matches) == 1 else None,
                            status='DECLARED_UNACCEPTED_EDGE' if len(matches) == 1 else 'INCOMPLETE_UNLISTED_OR_AMBIGUOUS_EDGE')
                        raw = json.dumps(edge, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')
                        if self.output_reserved + len(raw) + 1 > 262144:
                            raise GlobalStop('StaticGraphOutputReservationBound')
                        self.output_reserved += len(raw) + 1
                        graph.append(edge)
                    interpreter = row['ELF']['interpreter']
                    if interpreter:
                        self.check()
                        edge = interpreter_edge_data(row, self.rows, self.plan['declared_logical_aliases'],
                            self.plan['declared_ELF_seed_files'])
                        raw = json.dumps(edge, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')
                        if self.output_reserved + len(raw) + 1 > 262144:
                            raise GlobalStop('StaticGraphOutputReservationBound')
                        self.output_reserved += len(raw) + 1
                        graph.append(edge)
            except BaseException as error:
                failure = dict(type=type(error).__name__, reason=str(error)[:512])
        incomplete = failure is not None or len(self.rows) != len(entries) or any(r['status'] == 'INCOMPLETE' for r in self.rows) or any(r['status'].startswith('INCOMPLETE') for r in graph)
        result = dict(schema='wordling.current-test-static-inspection/v1', status='INCOMPLETE' if incomplete else 'UNACCEPTED_STATIC_DATA',
            plan_sha256=_PLAN_SHA, items=self.rows, graph=graph, global_stop=failure,
            unexamined_items=len(entries) - len(self.rows), byte_read_requests=self.requested,
            actual_bytes_read=self.actual, operations=self.operations, output_reserved=self.output_reserved,
            permission_granted=False, reference_qualification=False, current_context_created=False,
            BASE_executed=False, TEST_P_Original_actions=False)
        raw = json.dumps(result, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')
        if len(raw) + 1 > 262144:
            # A violated reservation is a source invariant failure, never a
            # reason to prune a partial inventory into apparent success.
            raise GlobalStop('StaticFinalOutputReservationInvariant')
        return result


def static_inspection():
    """Fixed no-argument DATA action; ROOT must approve exact source before use."""
    plan, source_bytes = _load_static_plan()
    return _StaticInventory(plan, source_bytes).run()



# This separately reviewed SOURCE-only purpose never constructs a current actor.
_CENSUS_PLAN_REL = 'docs/research/continuation/test-runtime-qualification-v2/source-stage/consolidated-five-role-closure/source-census01/design/reader-plan.json'
_CENSUS_PLAN_SHA = '36c8a705b53e6f08bc2fa52f47dea9bed731de1b7f34400ec0f079c7d24cf4c0'
_CENSUS_MAX = dict(records=24576, reads=17179869184, output=8388608,
    operations=7362560, deadline=300, depth=16, working=16777216)


def census_alias_data(logical, text, closed_roots, declared_aliases):
    """Lexical SOURCE DATA only: discovered links never authorize a lookup."""
    if (type(logical) is not str or type(text) is not str or not text.isascii()
            or '\0' in text or len(text) > 4096):
        raise Incomplete('CensusAliasText')
    target = posixpath.normpath(text if text.startswith('/') else posixpath.join(posixpath.dirname(logical), text))
    listed = logical in declared_aliases and target in declared_aliases
    return dict(status='OBSERVED_UNACCEPTED_CENSUS_DATA' if listed else 'INCOMPLETE_UNLISTED_CENSUS_ALIAS',
        target=target, text=text, follow=False, permission_granted=False)


def census_snapshot_data(before, after, before_names, after_names):
    if (type(before) is not dict or type(after) is not dict
            or type(before_names) is not list or type(after_names) is not list
            or max(len(before_names), len(after_names)) > 4096
            or any(type(n) is not str or not n.isascii() or len(n) > 255 for n in before_names + after_names)):
        raise Incomplete('CensusSnapshotData')
    stable = before == after and sorted(before_names) == sorted(after_names)
    return dict(status='UNACCEPTED_CENSUS_DATA' if stable else 'INCOMPLETE_UNSTABLE_CENSUS',
        stable_identity=stable, permission_granted=False, reference_qualification=False)


def census_package_data(distribution, basenames):
    if (distribution not in ('pip', 'setuptools', 'wheel') or type(basenames) is not list
            or len(basenames) > 4096 or any(type(n) is not str or not n.isascii() or len(n) > 255 for n in basenames)):
        raise Incomplete('CensusPackageData')
    matches = []
    for name in basenames:
        match = name == distribution + '.egg-info'
        for suffix in ('.dist-info', '.egg-info'):
            if name.startswith(distribution + '-') and name.endswith(suffix):
                version = name[len(distribution) + 1:-len(suffix)]
                match = bool(version and len(version) <= 128 and version[0].isalnum()
                    and all(c.isalnum() or c in '._+!-' for c in version))
        if match:
            matches.append(name)
    return dict(status='UNACCEPTED_PACKAGE_DATA' if len(matches) == 1 else 'INCOMPLETE_PACKAGE_SELECTION',
        selected=matches[0] if len(matches) == 1 else None, permission_granted=False)


def census_header_data(raw):
    if type(raw) is not bytes or len(raw) > 1048576:
        raise Incomplete('CensusHeaderBound')
    tokens, includes, unresolved = [], [], False
    start = 0
    while start < len(raw):
        stop = raw.find(b'\n', start)
        stop = len(raw) if stop < 0 else stop
        line = raw[start:stop]
        start = stop + 1
        if len(line) > 4096:
            unresolved = True
            continue
        line = line.strip()
        if not line.startswith(b'#'):
            continue
        line = line[1:].lstrip()
        if not line.startswith(b'include'):
            continue
        tail = line[7:].strip()
        if not tail or tail[:1] not in (b'<', b'"'):
            unresolved = True
            continue
        end = b'>' if tail[:1] == b'<' else b'"'
        index = tail.find(end, 1)
        token = tail[1:index] if index >= 0 else b''
        if (not token or len(token) > 512 or not token.isascii() or token.startswith(b'/')
                or any(x in (b'', b'.', b'..') for x in token.split(b'/')) or b'\0' in token):
            unresolved = True
            continue
        if len(tokens) >= 4096:
            raise Incomplete('CensusHeaderTokenBound')
        text = token.decode('ascii')
        tokens.append(text)
        includes.append(dict(token=text, kind='angle' if tail[:1] == b'<' else 'quoted'))
    return dict(tokens=tokens, includes=includes, unresolved=unresolved, permission_granted=False)


def _census_scan_directory(state, fd):
    """The ONLY directory enumeration site; descriptor and names stay bounded."""
    names, lease = [], 0
    try:
        with os.scandir(fd) as iterator:
            while True:
                state.work()
                state.lease(1280, 'CensusMemoryBound')
                try:
                    entry = next(iterator)
                except StopIteration:
                    state.release(1280)
                    break
                try:
                    name = entry.name
                    if (type(name) is not str or not name.isascii() or not 0 < len(name) <= 255
                            or name in ('.', '..') or '/' in name or '\0' in name):
                        raise Incomplete('CensusDirectoryName')
                    if len(names) >= 4096:
                        raise Incomplete('CensusDirectoryEntryBound')
                    charge = 256 + 4 * len(name)
                    if state.name_memory + charge > 8388608:
                        raise GlobalStop('CensusMemoryBound')
                    state.lease(charge, 'CensusMemoryBound')
                    state.name_memory += charge
                    lease += charge
                    names.append(name)
                finally:
                    del entry
                    state.release(1280)
        state.work(len(names) * (len(names).bit_length() + 1))
        state.lease(64 * len(names), 'CensusMemoryBound')
        try:
            names.sort()
            if len(names) != len(set(names)):
                raise Incomplete('CensusRepeatedDirectoryName')
        finally:
            state.release(64 * len(names))
        return names, lease
    except BaseException:
        state.release_names(lease)
        raise


def _census_row_size(value, depth=0):
    """Conservative pre-encoding allocation charge, not a new role validator."""
    if depth > 12:
        raise GlobalStop('CensusOutputDepth')
    if value is None or type(value) is bool:
        return 5
    if type(value) is int:
        return 24
    if type(value) is str:
        return 6 * len(value) + 2
    if type(value) is list:
        if len(value) > 4096:
            raise GlobalStop('CensusOutputShape')
        return 2 + sum(_census_row_size(x, depth + 1) + 1 for x in value)
    if type(value) is dict:
        if len(value) > 64 or any(type(k) is not str for k in value):
            raise GlobalStop('CensusOutputShape')
        return 2 + sum(_census_row_size(k, depth + 1) + _census_row_size(v, depth + 1) + 2 for k, v in value.items())
    raise GlobalStop('CensusOutputShape')


class _CensusState:
    """Bounded read-only SOURCE state. No Preparation/context/capacity grant."""
    def __init__(self, inventory):
        self.inventory = inventory
        options = inventory.plan.get('census_options')
        if type(options) is not dict or options.get('disposition') not in ('UNACCEPTED_SYNTHETIC_SOURCE_DATA', 'UNACCEPTED_SOURCE_DATA'):
            raise GlobalStop('CensusLowerDataOptions')
        self.limits = {}
        for name, maximum in _CENSUS_MAX.items():
            value = options.get(name)
            if type(value) is not int or not 0 <= value <= maximum:
                raise GlobalStop('CensusLowerLimit')
            self.limits[name] = value
        roots = options.get('roots')
        if (type(roots) is not list or not 0 < len(roots) <= 16
                or any(type(n) is not str or not n.isascii() or not n.startswith('/') or len(n) > 512 or '..' in Path(n).parts for n in roots)):
            raise GlobalStop('CensusLowerRoots')
        self.roots = roots
        self.emit_callback = inventory._census_emit
        if not callable(self.emit_callback):
            raise GlobalStop('CensusSinkRequired')
        self.end = min(inventory.end, time.monotonic() + self.limits['deadline'])
        self.operations = self.records = self.reads = self.output = self.memory = self.file_bytes = 0
        self.emitted_records = 0
        self.peak_memory = 0
        self.name_memory = 0
        self.header_queue_bytes = 0
        self.incomplete = False
        self.active_name, self.active_read = None, 0
        self.tracked = set(inventory.plan.get('declared_ELF_seed_files', [])) | set(inventory.plan.get('declared_nonexecuted_loader_data_files', []))
        self.tracked_reads = {}

    def work(self, count=1):
        if type(count) is not int or count < 0:
            raise GlobalStop('CensusWorkShape')
        if time.monotonic() >= self.end:
            raise GlobalStop('CensusWholeDeadline')
        self.operations += count
        if self.operations > self.limits['operations']:
            raise GlobalStop('CensusOperationBound')

    def lease(self, count, reason='CensusMemoryBound'):
        if type(count) is not int or count < 0 or self.memory + count > self.limits['working']:
            raise GlobalStop(reason)
        self.memory += count
        self.peak_memory = max(self.peak_memory, self.memory)

    def release(self, count):
        self.memory -= count
        if self.memory < 0:
            raise GlobalStop('CensusLeaseInvariant')

    def release_names(self, count):
        self.name_memory -= count
        if self.name_memory < 0:
            raise GlobalStop('CensusNameLeaseInvariant')
        self.release(count)

    def charge(self, name, count, metadata=False):
        self.work()
        if type(count) is not int or not 0 <= count <= 65536:
            raise GlobalStop('CensusReadChunkBound')
        old = self.tracked_reads.get(name, 0) if name in self.tracked else self.active_read if name == self.active_name else 0
        if old + count > 67108864 or self.reads + count > self.limits['reads']:
            raise GlobalStop('CensusReadBound')
        if metadata:
            inv = self.inventory
            if inv.metadata + count > 1048576:
                raise Incomplete('ELFMetadataReadBound')
            if inv.metadata_total + count > 16777216:
                raise GlobalStop('StaticTotalMetadataReadBound')
            inv.metadata += count
            inv.metadata_total += count
        if name in self.tracked:
            self.tracked_reads[name] = old + count
        else:
            self.active_name, self.active_read = name, old + count
        self.reads += count
        self.inventory.requested += count

    def encode(self, row, hold=False):
        bound = _census_row_size(row)
        if bound > 65536 or self.output + bound + 1 > self.limits['output']:
            raise GlobalStop('CensusOutputBound')
        self.lease(bound)
        encoded = False
        try:
            raw = json.dumps(row, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')
            if len(raw) > bound:
                raise GlobalStop('CensusEncodingInvariant')
            encoded = True
            if hold:
                return raw, bound
            del raw
            return None
        finally:
            if not hold or not encoded:
                self.release(bound)

    def emit(self, row):
        self.work()
        if self.emitted_records >= self.limits['records']:
            raise GlobalStop('CensusRecordBound')
        raw, lease = self.encode(row, hold=True)
        try:
            self.output += len(raw) + 1
            self.emitted_records += 1
            raw_sink = getattr(self.inventory, '_census_emit_raw', None)
            if raw_sink is None:
                self.emit_callback(row)
            else:
                raw_sink(raw)
        finally:
            del raw
            self.release(lease)

    def member(self):
        self.work()
        if self.records >= self.limits['records']:
            raise GlobalStop('CensusRecordBound')
        self.records += 1

    def file(self, name, before, fd):
        if not 0 <= before.st_size <= 67108864:
            raise GlobalStop('CensusFileSizeBound')
        self.encode(dict(path=name, kind='file', sha256='0' * 64, size=before.st_size, **_rights(before)))
        digest, remaining = hashlib.sha256(), before.st_size
        while remaining:
            amount = min(65536, remaining)
            self.charge(name, amount)
            self.lease(amount)
            chunk = None
            try:
                chunk = os.read(fd, amount)
                self.inventory.actual += len(chunk)
                if not chunk:
                    raise Incomplete('CensusShortFileRead')
                digest.update(chunk)
                remaining -= len(chunk)
            finally:
                del chunk
                self.release(amount)
        self.work()
        after = os.fstat(fd)
        current, _, resolved, _ = self.inventory.path_info(name)
        if _stamp(before) != _stamp(after) or _stamp(before) != _stamp(current) or resolved != name:
            raise Incomplete('CensusFileSnapshotChanged')
        self.file_bytes += before.st_size
        return dict(size=before.st_size, sha256=digest.hexdigest())

    def directory(self, name, before, fd, depth):
        if depth > self.limits['depth']:
            raise Incomplete('CensusDepthBound')
        names, name_lease = _census_scan_directory(self, fd)
        digest = hashlib.sha256()
        complete = True
        try:
            for child in names:
                self.member()
                self.lease(8192)
                row = record = common = facts = None
                full = ''
                try:
                    full = name.rstrip('/') + '/' + child
                    if len(full) > 512:
                        raise Incomplete('CensusPathBound')
                    opened = None
                    record = None
                    was_named = full in self.inventory.names
                    was_directory = full in self.inventory.directories
                    try:
                        self.work()
                        initial = os.stat(child, dir_fd=fd, follow_symlinks=False)
                        row = dict(path=full, **_rights(initial), status='OBSERVED_UNACCEPTED_CENSUS_DATA')
                        common = dict(name=child, **_rights(initial))
                        was_named = full in self.inventory.names
                        was_directory = full in self.inventory.directories
                        self.inventory.names.add(full)
                        if stat.S_ISREG(initial.st_mode):
                            observed, opened, resolved, _ = self.inventory.path_info(full, open_file=True)
                            if _stamp(observed) != _stamp(initial) or resolved != full:
                                raise Incomplete('CensusMemberChangedAtOpen')
                            facts = self.file(full, observed, opened)
                            row.update(kind='file', **facts)
                            record = dict(common, type='file', **facts)
                        elif stat.S_ISDIR(initial.st_mode):
                            self.inventory.directories.add(full)
                            observed, opened, resolved, _ = self.inventory.path_info(full, open_directory=True)
                            if _stamp(observed) != _stamp(initial) or resolved != full:
                                raise Incomplete('CensusDirectoryChangedAtOpen')
                            facts = self.directory(full, observed, opened, depth + 1)
                            row.update(kind='directory', census=facts)
                            if facts['membership_complete']:
                                record = dict(common, type='directory', membership_sha256=facts['membership_sha256'])
                            else:
                                row['status'] = 'INCOMPLETE_UNSTABLE_CENSUS'
                        elif stat.S_ISLNK(initial.st_mode):
                            text = os.readlink(child, dir_fd=fd)
                            current = os.stat(child, dir_fd=fd, follow_symlinks=False)
                            if _stamp(initial) != _stamp(current):
                                raise Incomplete('CensusAliasSnapshotChanged')
                            facts = census_alias_data(full, text, self.roots, self.inventory.aliases)
                            row.update(kind='symlink', **facts)
                            if not facts['status'].startswith('INCOMPLETE'):
                                record = dict(common, type='symlink', text=text)
                        else:
                            raise Incomplete('CensusUnsupportedFileType')
                    except (Incomplete, OSError) as error:
                        row = dict(path=full, status='INCOMPLETE', reason=str(error)[:512])
                    finally:
                        if opened is not None:
                            os.close(opened)
                        # Discovered names are a held-parent SOURCE traversal premise,
                        # never a persistent allowlist or full inventory map.
                        if not was_named:
                            self.inventory.names.discard(full)
                        if not was_directory:
                            self.inventory.directories.discard(full)
                    if record is None:
                        complete = False
                        self.incomplete = True
                    else:
                        raw, frame_lease = self.encode(record, hold=True)
                        try:
                            if len(raw) + 1 > 32768:
                                raise GlobalStop('CensusMembershipFrameBound')
                            digest.update(raw)
                            digest.update(b'\n')
                        finally:
                            del raw
                            self.release(frame_lease)
                    self.emit(row)
                finally:
                    del row, record, common, facts, full
                    self.release(8192)
            again, again_lease = _census_scan_directory(self, fd)
            try:
                held = os.fstat(fd)
                current, _, resolved, _ = self.inventory.path_info(name)
                snapshot = census_snapshot_data(_identity(before), _identity(held), names, again)
                complete = (complete and snapshot['stable_identity'] and _stamp(before) == _stamp(current) and resolved == name)
            finally:
                self.release_names(again_lease)
            facts = dict(membership_complete=bool(complete))
            if complete:
                facts['membership_sha256'] = digest.hexdigest()
            else:
                self.incomplete = True
                facts['membership_prefix_sha256'] = digest.hexdigest()
            return facts
        finally:
            self.release_names(name_lease)

    def root(self, entry):
        name = entry['path']
        if name not in self.roots or entry != dict(kind='census_root', path=name):
            raise GlobalStop('CensusUndeclaredRoot')
        if not self.limits['records']:
            raise GlobalStop('CensusRecordBound')
        self.work()
        before_records, before_bytes = self.records, self.file_bytes
        before, fd, resolved, aliases = self.inventory.path_info(name, open_directory=True)
        if fd is None or resolved != name or aliases:
            if fd is not None:
                os.close(fd)
            raise Incomplete('CensusRootMustBeAnchoredDirectory')
        try:
            facts = self.directory(name, before, fd, 0)
        finally:
            os.close(fd)
        facts.update(records=self.records - before_records, file_bytes=self.file_bytes - before_bytes)
        return dict(kind='census_root', path=name, status='UNACCEPTED_CENSUS_DATA' if facts['membership_complete'] else 'INCOMPLETE',
            census=facts, permission_granted=False, reference_qualification=False, current_context_created=False)


def _census_item_data(inventory, entry):
    if inventory.plan.get('id') != 'SOURCE_CENSUS01':
        raise GlobalStop('CensusPurposeRequired')
    state = getattr(inventory, '_census_state', None)
    if state is None:
        state = _CensusState(inventory)
        inventory._census_state = state
    return state.root(entry)


class _CensusInventory(_StaticInventory):
    """Only the fixed SOURCE entry creates this longer SOURCE budget."""
    def __init__(self, plan, source_bytes):
        origin = time.monotonic()
        super().__init__(plan, source_bytes)
        self.end = origin + 300

    def check(self):
        state = getattr(self, '_census_state', None)
        if state is None:
            raise GlobalStop('CensusStateRequiredBeforeIO')
        state.work()

    def charge(self, name, count, metadata=False):
        self._census_state.charge(name, count, metadata)


def _load_census_plan():
    root = Path(__file__).absolute().parents[5]
    path = root / _CENSUS_PLAN_REL
    directory = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    fd = None
    try:
        for part in path.parts[1:-1]:
            before = os.stat(part, dir_fd=directory, follow_symlinks=False)
            following = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory)
            if not stat.S_ISDIR(before.st_mode) or _stamp(before) != _stamp(os.fstat(following)):
                os.close(following)
                raise GlobalStop('CensusPlanParentChanged')
            os.close(directory)
            directory = following
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory)
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= 32768:
            raise GlobalStop('CensusPlanBytes')
        raw = os.read(fd, before.st_size + 1)
        if (len(raw) != before.st_size or hashlib.sha256(raw).hexdigest() != _CENSUS_PLAN_SHA
                or _stamp(before) != _stamp(os.fstat(fd))
                or _stamp(before) != _stamp(os.stat(path.name, dir_fd=directory, follow_symlinks=False))):
            raise GlobalStop('CensusPlanIdentity')
    finally:
        if fd is not None:
            os.close(fd)
        os.close(directory)
    plan = json.loads(raw)
    if plan['schema'] != 'wordling.wp108-source-census-plan/v1' or plan['id'] != 'SOURCE_CENSUS01':
        raise GlobalStop('CensusPlanSchema')
    return plan, len(raw)



def _census_declare(state, name, directory=False):
    """Scoped source path premise; lease BEFORE making ancestor strings/sets."""
    if (type(name) is not str or not name.isascii() or not name.startswith('/')
            or len(name) > 512 or '..' in name.split('/') or name.count('/') > 64):
        raise Incomplete('CensusDeclaredPath')
    lease = (name.count('/') + 1) * (1024 + 8 * len(name))
    state.lease(lease)
    inv = state.inventory
    names, directories = [], []
    try:
        for parent in Path(name).parents:
            text = str(parent)
            if text not in inv.names:
                inv.names.add(text)
                names.append(text)
            if text not in inv.directories:
                inv.directories.add(text)
                directories.append(text)
        if name not in inv.names:
            inv.names.add(name)
            names.append(name)
        if directory and name not in inv.directories:
            inv.directories.add(name)
            directories.append(name)
        return names, directories, lease
    except BaseException:
        for text in directories:
            inv.directories.discard(text)
        for text in names:
            inv.names.discard(text)
        state.release(lease)
        raise


def _census_restore_declaration(state, declaration):
    names, directories, lease = declaration
    for text in directories:
        state.inventory.directories.discard(text)
    for text in names:
        state.inventory.names.discard(text)
    state.release(lease)


def _census_include_size(include):
    return 512 + 4 * (len(include['token']) + len(include['parent'] or ''))


def _census_header_candidates_data(include, roots):
    """Exact declared candidates and context identity, without filesystem I/O."""
    if (type(include) is not dict or set(include) != {'token', 'kind', 'parent'}
            or include['kind'] not in ('angle', 'quoted')
            or type(include['token']) is not str or not include['token'].isascii()
            or not 0 < len(include['token']) <= 512
            or include['token'].startswith('/') or '\0' in include['token']
            or any(p in ('', '.', '..') for p in include['token'].split('/'))
            or type(roots) is not list or not 0 < len(roots) <= 4):
        raise Incomplete('CensusHeaderContext')
    parent = include['parent']
    if parent is not None and (type(parent) is not str or not parent.isascii()
            or not parent.startswith('/') or len(parent) > 512 or '..' in parent.split('/')):
        raise Incomplete('CensusHeaderContext')
    if include['kind'] == 'quoted' and parent is None:
        raise Incomplete('CensusQuotedHeaderParentRequired')
    if any(type(r) is not str or not r.isascii() or not r.startswith('/')
            or len(r) > 512 or '..' in r.split('/') for r in roots):
        raise Incomplete('CensusHeaderRoots')
    origin = parent if include['kind'] == 'quoted' else None
    search = ([origin] if origin is not None else []) + roots
    candidates = []
    for root in search:
        path = root.rstrip('/') + '/' + include['token']
        if len(path) > 512:
            raise Incomplete('CensusHeaderPathBound')
        if path not in candidates:
            candidates.append(path)
    return dict(identity=(include['kind'], origin, include['token']), candidates=candidates)


def _census_header_lease(state, count):
    if state.header_queue_bytes + count > 2097152:
        raise GlobalStop('CensusHeaderQueueBound')
    state.lease(count)
    state.header_queue_bytes += count


def _census_file_fact(state, name, header=False):
    """One explicitly declared file read; no include/root is found by a walk."""
    inv = state.inventory
    declaration = _census_declare(state, name)
    opened = None
    tokens = []
    transferred = False
    try:
        state.member()
        before, opened, resolved, aliases = inv.path_info(name, open_file=True)
        if resolved != name or aliases:
            raise Incomplete('CensusFileAliasNeedsExplicitClosure')
        facts = state.file(name, before, opened)
        tokens, unresolved = [], False
        if header:
            if before.st_size > 1048576:
                raise Incomplete('CensusHeaderBound')
            # Re-read only a bounded line/chunk view on the same held snapshot;
            # all rereads count, no complete header/table is copied to memory.
            offset, carry = 0, b''
            while offset < before.st_size:
                count = min(4096, before.st_size - offset)
                state.charge(name, count)
                state.lease(262144)
                raw = lines = line = parsed = None
                try:
                    raw = os.pread(opened, count, offset)
                    inv.actual += len(raw)
                    if len(raw) != count:
                        raise Incomplete('CensusHeaderShortRead')
                    offset += count
                    raw = carry + raw
                    lines = raw.split(b'\n')
                    carry = lines.pop()
                    if len(carry) > 4096:
                        unresolved = True
                        carry = b''
                    for line in lines:
                        state.work()
                        parsed = census_header_data(line)
                        unresolved |= parsed['unresolved']
                        for include in parsed['includes']:
                            if len(tokens) >= 4096:
                                raise Incomplete('CensusHeaderTokenBound')
                            value = dict(include, parent=posixpath.dirname(name) if include['kind'] == 'quoted' else None)
                            _census_header_lease(state, _census_include_size(value))
                            tokens.append(value)
                finally:
                    del raw, lines, line, parsed
                    state.release(262144)
            if carry:
                parsed = census_header_data(carry)
                unresolved |= parsed['unresolved']
                for include in parsed['includes']:
                    if len(tokens) >= 4096:
                        raise Incomplete('CensusHeaderTokenBound')
                    value = dict(include, parent=posixpath.dirname(name) if include['kind'] == 'quoted' else None)
                    _census_header_lease(state, _census_include_size(value))
                    tokens.append(value)
            current, _, current_path, _ = inv.path_info(name)
            if _stamp(before) != _stamp(os.fstat(opened)) or _stamp(before) != _stamp(current) or current_path != name:
                raise Incomplete('CensusHeaderSnapshotChanged')
        row = dict(path=name, kind='header' if header else 'declared_file', **_rights(before), **facts,
            status='INCOMPLETE_HEADER_MACRO_OR_SEARCH' if unresolved else 'OBSERVED_UNACCEPTED_CENSUS_DATA')
        state.incomplete |= unresolved
        state.emit(row)
        transferred = True
        return tokens, True
    except (Incomplete, OSError) as error:
        state.incomplete = True
        state.emit(dict(path=name, status='INCOMPLETE', reason=str(error)[:512]))
        return [], False
    finally:
        if not transferred:
            for token in tokens:
                state.release(_census_include_size(token))
                state.header_queue_bytes -= _census_include_size(token)
        if opened is not None:
            os.close(opened)
        _census_restore_declaration(state, declaration)


def _census_packages(state, plan):
    inv = state.inventory
    parent = plan['package_parent']
    declaration = _census_declare(state, parent, directory=True)
    fd = None
    lease = 0
    names = []
    try:
        before, fd, resolved, aliases = inv.path_info(parent, open_directory=True)
        if resolved != parent or aliases:
            raise Incomplete('CensusPackageParentAlias')
        names, lease = _census_scan_directory(state, fd)
        selected = set(plan['exact_package_candidates'])
        for distribution in plan['package_metadata_grammar']['distributions']:
            result = census_package_data(distribution, names)
            state.member()
            state.emit(dict(kind='package_selection', path=parent, distribution=distribution, **result))
            if result['selected'] is None:
                state.incomplete = True
            else:
                selected.add(parent + '/' + result['selected'])
        again, again_lease = _census_scan_directory(state, fd)
        try:
            current, _, current_path, _ = inv.path_info(parent)
            if (not census_snapshot_data(_identity(before), _identity(os.fstat(fd)), names, again)['stable_identity']
                    or _stamp(before) != _stamp(current) or current_path != parent):
                raise Incomplete('CensusPackageParentChanged')
        finally:
            del again
            state.release_names(again_lease)
    except (Incomplete, OSError) as error:
        state.incomplete = True
        state.emit(dict(path=parent, status='INCOMPLETE', reason=str(error)[:512]))
        selected = set(plan['exact_package_candidates'])
    finally:
        del names
        state.release_names(lease)
        if fd is not None:
            os.close(fd)
        _census_restore_declaration(state, declaration)
    for name in sorted(selected):
        declaration = _census_declare(state, name, directory=True)
        new_root = name not in state.roots
        if new_root:
            state.roots.append(name)
        try:
            state.emit(state.root(dict(kind='census_root', path=name)))
        except (Incomplete, OSError) as error:
            state.incomplete = True
            state.emit(dict(path=name, status='INCOMPLETE', reason=str(error)[:512]))
        finally:
            if new_root:
                state.roots.remove(name)
            _census_restore_declaration(state, declaration)


def _census_headers(state, plan):
    roots = plan['header_search_hypotheses']
    queue = []
    seen_scopes, seen_paths = set(), {}
    held = 0
    selection = include = includes = identity = name = value = None
    try:
        for token in plan['direct_header_tokens']:
            include = dict(token=token, kind='angle', parent=None)
            count = _census_include_size(include)
            _census_header_lease(state, count)
            held += count
            queue.append(include)
        index = 0
        while index < len(queue):
            state.work()
            include = queue[index]
            index += 1
            selection = _census_header_candidates_data(include, roots)
            identity = selection['identity']
            if identity in seen_scopes:
                continue
            seen_scopes.add(identity)
            found = 0
            for name in selection['candidates']:
                if name in seen_paths:
                    found += seen_paths[name]
                    continue
                if len(seen_paths) >= 4096:
                    raise Incomplete('CensusHeaderFileCount')
                count = 256 + 4 * len(name)
                _census_header_lease(state, count)
                held += count
                # Context-preserving candidates are all reported; neither parent
                # preference nor multiple fixed roots silently chooses authority.
                includes, present = _census_file_fact(state, name, header=True)
                seen_paths[name] = present
                found += seen_paths[name]
                for value in includes:
                    # file_fact already leased the token/kind/origin parent.
                    held += _census_include_size(value)
                    queue.append(value)
            if found != 1:
                state.incomplete = True
                state.emit(dict(kind='header_search', token=include['token'],
                    include_kind=include['kind'], parent=include['parent'], matches=found,
                    status='INCOMPLETE_HEADER_SEARCH_ORDER_OR_MEMBERSHIP'))
    except Incomplete as error:
        state.incomplete = True
        state.emit(dict(kind='header_closure', status='INCOMPLETE', reason=str(error)[:512]))
    finally:
        # No declaration or header-queue borrow survives this SOURCE stage.
        del queue, seen_scopes, seen_paths, selection, include, includes, identity, name, value
        state.release(held)
        state.header_queue_bytes -= held
        if state.header_queue_bytes != 0:
            raise GlobalStop('CensusHeaderLeaseInvariant')


def closure_source_census():
    """One fixed streamed SOURCE inventory. Never reference/current acceptance."""
    plan, source_bytes = _load_census_plan()
    old, old_bytes = _load_static_plan()
    if plan['retained_STATIC04_plan']['sha256'] != _PLAN_SHA:
        raise GlobalStop('CensusStaticConservation')
    low = dict(old)
    low['id'] = 'SOURCE_CENSUS01'
    roots = [r['path'] for r in plan['closed_tree_roots']]
    low['census_options'] = dict(_CENSUS_MAX, disposition='UNACCEPTED_SOURCE_DATA', roots=roots)
    inv = _CensusInventory(low, source_bytes + old_bytes)
    # Stream only: no full JSON inventory or second source map is retained.
    written, first = 0, True
    def write(raw):
        nonlocal written
        if type(raw) is not bytes or written + len(raw) > 8388608:
            raise GlobalStop('CensusOutputBound')
        sys.stdout.buffer.write(raw)
        written += len(raw)
    def emit_raw(raw):
        nonlocal first
        if written + len(raw) + 1 > 8388608 - 8192:
            raise GlobalStop('CensusOutputBound')
        write((b'' if first else b',') + raw)
        first = False
    inv._census_emit = lambda row: None
    inv._census_emit_raw = emit_raw
    state = _CensusState(inv)
    inv._census_state = state
    state.reads = source_bytes + old_bytes
    state.lease(1048576)  # fixed two plan objects, names/roots, bounded native frame
    write(b'{"schema":"wordling.source-census-unaccepted/v1","items":[')
    failure = None
    try:
        native_entries = old['fixed_item_order'] + [dict(kind='ELF_seed', path=n) for n in plan['new_exact_ELF_seeds']]
        for entry in native_entries:
            declaration = _census_declare(state, entry['path'], directory=entry['kind'] in ('ancestor', 'directory'))
            row = None
            frame_held = False
            try:
                state.member()
                state.lease(2097152)
                frame_held = True
                try:
                    row = inv.item(entry)
                except (Incomplete, OSError) as error:
                    row = dict(**entry, status='INCOMPLETE', reason=str(error)[:512])
                state.incomplete |= row['status'].startswith('INCOMPLETE')
                state.emit(row)
            finally:
                del row
                if frame_held:
                    state.release(2097152)
                _census_restore_declaration(state, declaration)
        for name in roots:
            # Closed-tree descendants are admitted only from a held, stable,
            # declared directory scan, never from an ambient search/role.
            if name not in inv.names:
                raise GlobalStop('CensusRootAncestorClosure')
            try:
                state.emit(inv.item(dict(kind='census_root', path=name)))
            except (Incomplete, OSError) as error:
                state.incomplete = True
                state.emit(dict(path=name, status='INCOMPLETE', reason=str(error)[:512]))
        _census_packages(state, plan)
        _census_headers(state, plan)
        for name in plan['link_input_hypotheses'] + plan['locale_hypotheses']:
            _census_file_fact(state, name)
    except BaseException as error:
        failure = dict(type=type(error).__name__, reason=str(error)[:512])
        state.incomplete = True
    finally:
        state.release(1048576)
    summary = dict(status='INCOMPLETE' if state.incomplete else 'UNACCEPTED_SOURCE_DATA',
        records=state.emitted_records, byte_read_requests=state.reads, actual_bytes_read=inv.actual,
        operations=state.operations, source_component_operations=state.operations,
        peak_working_charge=state.peak_memory, remaining_working_charge=state.memory,
        global_stop=failure, permission_granted=False, reference_qualification=False,
        current_context_created=False, BASE_executed=False)
    write(b'],"summary":' + json.dumps(summary, sort_keys=True, separators=(',', ':')).encode('ascii') + b'}\n')
    sys.stdout.buffer.flush()
    return summary


if __name__ == '__main__':
    if sys.argv[1:] == ['--closure-source-census']:
        value = closure_source_census()
        raise SystemExit(0 if value['status'] == 'UNACCEPTED_SOURCE_DATA' else 2)
    if sys.argv[1:] != ['--static-inspect-v1']:
        raise SystemExit('DORMANT: no current role; only fixed reviewed static DATA inspection is defined')
    value = static_inspection()
    print(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True))
    raise SystemExit(0 if value['status'] == 'UNACCEPTED_STATIC_DATA' else 2)
