"""Disjoint durable TEST issuance. Original execution is permanently disabled here."""
import fcntl
import hashlib
import json
import os
import stat
import time
from .errors import Opaque, Refusal
from .bootstrap import validate_policy
from .account import DIMENSIONS, _reserve_cleanup_hold, _bind_cleanup_hold, _take_cleanup_hold, _KEY as ACCOUNT_KEY, _new_book, _issuer_reservation, _activate
from .ownership import _DIR, _FILE, _call, _identity, _components, _record_coordinator

_KEY = object()
_KIND = 'wordling.TEST.ledger/v1'
_METADATA = 'issuer.json'
_LOCK = 'issuer.lock'
_MAX_MARKERS = 256
_CHECKPOINTS = ('pre-marker', 'marker-created', 'binding-written', 'durable-committed', 'activated',
                'parent-acquired', 'ledger-created', 'ledger-charged', 'complete')


def _ascii(value):
    if type(value) is not str or not 0 < len(value) <= 128 or not value.isascii():
        raise Refusal('InvalidStableIdentity')
    return value


def stable_key(kind, generation, grant_id):
    values = ('wordling.spent-ticket/v1', kind, generation, grant_id)
    h = hashlib.sha256()
    for value in values:
        raw = _ascii(value).encode('ascii')
        h.update(len(raw).to_bytes(4, 'big') + raw)
    return h.hexdigest()


def _test_root(path):
    if (type(path) is not str or not path.startswith('/tmp/wordling-reference-TEST-') or
            '/' in path[len('/tmp/'):] or len(path) > 100 or
            any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-' for c in path[len('/tmp/'):] )):
        raise Refusal('NotTestNamespace')
    return path


def _boot():
    fd = os.open('/proc/sys/kernel/random/boot_id', os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        raw = os.read(fd, 65)
        if not 0 < len(raw) <= 64:
            raise Refusal('BootIdentity')
        return raw.decode('ascii').strip()
    finally:
        os.close(fd)


def provision_test_store(policy, root, generation):
    """Bounded local TEST administration; trusted fixed local mounts, no grant."""
    validate_policy(policy)
    _test_root(root)
    _ascii(generation)
    end = min(policy.end_ns, time.monotonic_ns() + 2000000000)
    def check():
        if time.monotonic_ns() >= end:
            raise Refusal('AdminDeadline', partial=True)
    check()
    with open('/proc/self/mountinfo', 'rb') as stream:
        mounts = stream.read(65537)
    if len(mounts) > 65536:
        raise Refusal('MountProbeLimit')
    matching = []
    for line in mounts.decode('utf-8').splitlines():
        left, right = line.split(' - ', 1)
        mount = left.split()[4]
        if root == mount or root.startswith(mount.rstrip('/') + '/'):
            matching.append((len(mount), right.split()[0]))
    if not matching or max(matching)[1] not in ('ext4', 'xfs', 'btrfs', 'tmpfs', 'overlay'):
        raise Refusal('UnprovedLocalFilesystem')
    check()
    os.mkdir(root, 0o700)  # no replacement and no automatic retry after any effect
    rootfd = os.open(root, _DIR)
    try:
        st = os.fstat(rootfd)
        if st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) != 0o700:
            raise Refusal('StoreIdentity', partial=True)
        raw = (json.dumps(dict(schema='wordling.TEST.issuer/v1', kind=_KIND,
                    generation=generation, uid=os.getuid(), boot=_boot(),
                    source=policy.source_hash), sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')
        if len(raw) > 4096:
            raise Refusal('MetadataLimit', partial=True)
        for name, data in ((_METADATA, raw), (_LOCK, b'')):
            check()
            fd = os.open(name, _FILE | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=rootfd)
            try:
                if data and os.write(fd, data) != len(data):
                    raise Refusal('AdminWrite', partial=True)
                os.fsync(fd)
                check()
                if os.pread(fd, len(data) + 1, 0) != data:
                    raise Refusal('AdminReadback', partial=True)
            finally:
                os.close(fd)
        os.fsync(rootfd)
        parentfd = os.open('/tmp', _DIR)
        try:
            os.fsync(parentfd)
        finally:
            os.close(parentfd)
        check()
        return dict(status='TEST_STORE_CREATED', generation=generation, filesystem=max(matching)[1])
    finally:
        os.close(rootfd)


class IssuancePermit(Opaque):
    def __init__(self, key, issuer, book, root, generation, grant_id, meter):
        if key is not _KEY:
            raise Refusal('InvalidIssuancePermit')
        self._issuer, self._book, self._root = issuer, book, root
        self._generation, self._grant_id, self._meter = generation, grant_id, meter
        self._used = False
        self._cleanup_hold=_reserve_cleanup_hold(book,self,8)


class TestGrant(Opaque):
    def __init__(self, key, issuer, permit, store):
        if key is not _KEY:
            raise Refusal('InvalidTestGrant')
        self._issuer, self._permit, self._store = issuer, permit, store
        self._used = False


class TicketStore(Opaque):
    """Live held root chain and nonblocking store lock; never reopens spent IDs."""
    def __init__(self, key, permit):
        if key is not _KEY:
            raise Refusal('InvalidTicketStore')
        self._permit, self._chain, self._files = permit, [], []
        self._closed = False
        self._cleanup_hold=permit._cleanup_hold
        _bind_cleanup_hold(self._cleanup_hold,self)

    def _call(self, function, *args, **kwargs):
        return _call(self._permit._meter, self._permit._meter._owner, function, *args, **kwargs)

    def _validate(self):
        p = self._permit
        p._book.policy.verify(p._meter, p._meter._owner)
        for i, (fd, name, identity) in enumerate(self._chain):
            if _identity(self._call(os.fstat, fd)) != identity:
                raise Refusal('StoreIdentity', partial=True)
            if i and _identity(self._call(os.stat, name, dir_fd=self._chain[i-1][0], follow_symlinks=False)) != identity:
                raise Refusal('StoreRetargeted', partial=True)
        rootfd = self._chain[-1][0]
        for fd, name, identity in self._files:
            held = self._call(os.fstat, fd)
            linked = self._call(os.stat, name, dir_fd=rootfd, follow_symlinks=False)
            if (_identity(held) != identity or _identity(linked) != identity or
                    held.st_nlink != 1 or linked.st_nlink != 1 or
                    stat.S_IMODE(held.st_mode) != 0o600):
                raise Refusal('StoreFileRetargeted', partial=True)

    def _boot(self):
        fd = self._call(os.open, '/proc/sys/kernel/random/boot_id', os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            self._permit._meter.charge(self._permit._meter._owner, source_io=65)
            raw = self._call(os.read, fd, 65)
            if not 0 < len(raw) <= 64:
                raise Refusal('BootIdentity')
            return raw.decode('ascii').strip()
        finally:
            self._call(os.close, fd)

    @classmethod
    def open(cls, key, permit):
        store = cls(key, permit)
        try:
            fd = store._call(os.open, '/', _DIR)
            store._chain.append((fd, '', _identity(store._call(os.fstat, fd))))
            for name in _components(permit._root):
                fd = store._call(os.open, name, _DIR, dir_fd=store._chain[-1][0])
                store._chain.append((fd, name, _identity(store._call(os.fstat, fd))))
            rootfd = store._chain[-1][0]
            rootst = store._call(os.fstat, rootfd)
            if rootst.st_uid != os.getuid() or stat.S_IMODE(rootst.st_mode) != 0o700:
                raise Refusal('StoreIdentity')
            for name in (_LOCK, _METADATA):
                fd = store._call(os.open, name, _FILE, dir_fd=rootfd)
                st = store._call(os.fstat, fd)
                store._files.append((fd, name, _identity(st)))
                if (not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_uid != os.getuid() or
                        stat.S_IMODE(st.st_mode) != 0o600 or st.st_size > 4096):
                    raise Refusal('StoreIdentity')
            store._call(fcntl.flock, store._files[0][0], fcntl.LOCK_EX | fcntl.LOCK_NB)
            permit._meter.charge(permit._meter._owner, source_io=4097)
            data = store._call(os.pread, store._files[1][0], 4097, 0)
            if len(data) > 4096:
                raise Refusal('MetadataLimit')
            permit._meter.charge(permit._meter._owner, work=len(data))
            metadata = json.loads(data)
            if (type(metadata) is not dict or len(metadata) != 6 or
                    set(metadata) != {'schema', 'kind', 'generation', 'uid', 'boot', 'source'} or
                    type(metadata['uid']) is not int or
                    any(type(metadata[k]) is not str for k in ('schema','kind','generation','boot','source'))):
                raise Refusal('StoreMetadataType')
            expected = dict(schema='wordling.TEST.issuer/v1', kind=_KIND,
                            generation=permit._generation, uid=os.getuid(),
                            boot=store._boot(), source=permit._book.policy.source_hash)
            if metadata != expected:
                raise Refusal('StoreQuarantined')
            store._boot_identity = metadata['boot']
            store._validate()
            return store
        except BaseException:
            store._close_on_failure()
            raise

    def _close_on_failure(self):
        book=self._permit._book
        failed=False
        try:
            meter=_take_cleanup_hold(self._cleanup_hold,self)
        except Refusal:
            book.halt('CleanupIncomplete')
            self._closed=True
            return False
        for fd,_,identity in reversed(self._files+self._chain):
            try:
                if _identity(_call(meter,self,os.fstat,fd))!=identity:
                    raise Refusal('ForeignDescriptor')
                _call(meter,self,os.close,fd)
            except (OSError,Refusal):
                failed=True
                book.halt('CleanupIncomplete')
        self._closed=True
        return not failed

    def close(self, book):
        if book is not self._permit._book or self._closed:
            raise Refusal('InvalidTicketStore')
        if not self._close_on_failure():
            raise Refusal('CleanupIncomplete', partial=True)


class RootTicketIssuer:
    def issue(self, *args, **kwargs):
        raise Refusal('SourcePrelaunchBlocked')


class TestIssuer(Opaque):
    def __init__(self):
        self._permits, self._grants, self._stores = set(), set(), {}

    def reserve(self, policy, root, generation, grant_id, leaf, ledger_parent):
        validate_policy(policy)
        _test_root(root)
        _ascii(generation)
        _ascii(grant_id)
        _ascii(leaf)
        _components(ledger_parent)
        if ledger_parent != root+'-ledger' and not ledger_parent.startswith(root+'-ledger/'):
            raise Refusal('NotTestNamespace')
        key = stable_key(_KIND, generation, grant_id)
        book = _new_book(policy, leaf, ledger_parent, key[:48] + '.json')
        permit = IssuancePermit(_KEY, self, book, root, generation, grant_id,
                                _issuer_reservation(book, self, 8))
        self._permits.add(permit)
        baseline=_record_coordinator(book,self,permit._meter)
        if baseline._current['fds']+9>64:
            book.halt('LiveLimit')
            raise Refusal('LiveLimit')
        return permit

    def issue(self, permit, checkpoint=lambda name: None):
        if (type(permit) is not IssuancePermit or permit not in self._permits or
                permit._issuer is not self or permit._used):
            raise Refusal('InvalidIssuancePermit')
        permit._used = True
        permit._book.policy.verify(permit._meter,self)
        store = TicketStore.open(_KEY, permit)
        try:
            rootfd = store._chain[-1][0]
            permit._meter.charge(self, syscalls=2)
            with os.scandir(rootfd) as entries:
                count = 0
                for entry in entries:
                    permit._meter.charge(self, work=1)
                    if entry.name not in (_METADATA, _LOCK):
                        if len(entry.name) != 70 or not entry.name.endswith('.spent') or any(c not in '0123456789abcdef' for c in entry.name[:64]):
                            raise Refusal('UnexpectedStoreEntry')
                        count += 1
                        if count >= _MAX_MARKERS:
                            raise Refusal('StoreCapacity')
            store._validate()
            marker = stable_key(_KIND, permit._generation, permit._grant_id) + '.spent'
            remaining=permit._meter._maxima['syscalls']-permit._meter._used['syscalls']
            attempts=min(16,(remaining-552)//88)
            if attempts<1:
                raise Refusal('IssuerTailFit')
            checkpoint('pre-marker')
            fd = store._call(os.open, marker, _FILE | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=rootfd)
            st = store._call(os.fstat, fd)
            store._files.append((fd, marker, _identity(st)))
            permit._book._created_regular[('ticket',_identity(st))]=True
            if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) != 0o600:
                raise Refusal('MarkerIdentity', partial=True)
            store._call(fcntl.flock, fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            checkpoint('marker-created')
            binding = self._binding(permit, store, marker[:64])
            if len(binding) > 256:
                raise Refusal('BindingLimit', partial=True)
            offset = 0
            for _ in range(attempts):
                if offset == len(binding):
                    break
                permit._meter.charge(self, source_io=len(binding) - offset)
                wrote = store._call(os.write, fd, binding[offset:])
                if not 0 < wrote <= len(binding) - offset:
                    raise Refusal('MarkerShortWrite', partial=True)
                offset += wrote
                store._validate()
            if offset != len(binding):
                raise Refusal('MarkerWriteAttempts', partial=True)
            checkpoint('binding-written')
            store._validate()
            store._call(os.fsync, fd)
            store._validate()
            store._call(os.fsync, rootfd)
            store._validate()
            permit._meter.charge(self, source_io=len(binding) + 1)
            if store._call(os.pread, fd, len(binding) + 1, 0) != binding:
                raise Refusal('MarkerReadback', partial=True)
            store._validate()
            checkpoint('durable-committed')
            permit._meter.check(self)
            grant = TestGrant(_KEY, self, permit, store)
            self._grants.add(grant)
            return grant
        except BaseException:
            store._close_on_failure()
            raise

    def _binding(self, permit, store, stable):
        book = permit._book
        def digest(values):
            h = hashlib.sha256()
            total = 0
            for value in values:
                raw = value.encode('ascii')
                total += 4 + len(raw)
                if len(raw) > 512 or total > 4096:
                    raise Refusal('BindingLimit', partial=True)
                permit._meter.charge(self, work=len(raw) + 4)
                h.update(len(raw).to_bytes(4, 'big') + raw)
            return h.hexdigest()
        envelope = digest((book.leaf, str(book.origin_ns), str(book.end_ns),
                           book.parent_path, book.basename))
        decision = digest(('SOURCE_FIXED_TEST_ONLY', _KIND, permit._grant_id))
        budget = digest(tuple(k + '=' + str(v) for k, v in DIMENSIONS.items()))
        fields = (book._source, book.policy.deployment_hash, book._plan, envelope,
                  decision, budget, permit._root, permit._generation, str(os.getuid()),
                  _KIND, book.leaf, str(book.origin_ns), str(book.end_ns), store._boot_identity)
        binding = digest(fields)
        return ('wordling.TEST.spent/v1\n' + stable + '\n' + binding + '\n').encode('ascii')

    def activate(self, grant):
        if (type(grant) is not TestGrant or grant not in self._grants or
                grant._issuer is not self or grant._used):
            raise Refusal('InvalidTestGrant')
        grant._used = True
        grant._store._validate()
        _record_coordinator(grant._permit._book,self,grant._permit._meter)
        _activate(grant._permit._book, ACCOUNT_KEY)
        book = grant._permit._book
        self._stores[book] = grant._store
        return book

    def finish(self, book):
        if book not in self._stores:
            raise Refusal('InvalidTestAccount')
        store = self._stores.pop(book)
        store.close(book)
        _record_coordinator(book,book,book._cleanup_observation)
        book._closed = True
