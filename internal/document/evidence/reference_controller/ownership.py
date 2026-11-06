"""Retained directory chains and no-clobber, single-owner bounded ledger IO."""
import os
import stat
import fcntl
from .errors import Opaque, Refusal
from .account import consume, OperationLimits, PhaseReservation, _source_live_observation, _reserve_cleanup_hold, _bind_cleanup_hold, _take_cleanup_hold, _cleanup_requirements
from .records import encode

_DIR = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
_FILE = os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC
_KEY = object()


def _call(meter, owner, function, *args, **kwargs):
    meter.charge(owner, syscalls=1, work=1)
    try:
        result = function(*args, **kwargs)
    except OSError as exc:
        meter._book.halt('FilesystemFailure')
        raise Refusal('FilesystemFailure', partial=True) from exc
    try:
        meter.check(owner)
    except Refusal as exc:
        if function is os.open:
            _emergency_close(meter._book,result)
        raise Refusal(exc.code,partial=True) from exc
    return result


def _identity(st):
    return st.st_dev, st.st_ino, stat.S_IFMT(st.st_mode), st.st_uid


def _components(path):
    if (type(path) is not str or not path.startswith('/') or len(path) > 4096 or
            len(path.encode('utf-8')) > 4096 or '\x00' in path):
        raise Refusal('InvalidParentPath')
    parts = path[1:].split('/')
    if not 0 < len(parts) <= 32 or any(not p or p in ('.', '..') or len(p.encode('utf-8')) > 255 for p in parts):
        raise Refusal('InvalidParentPath')
    return parts


def _name(name):
    if (type(name) is not str or not 0 < len(name) <= 64 or not name.isascii() or
            name in ('.', '..') or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-' for c in name)):
        raise Refusal('InvalidLedgerName')


class ParentLease(Opaque):
    def __init__(self, key, book, path, chain):
        if key is not _KEY:
            raise Refusal('InvalidParentLease')
        self._book, self.path, self._chain, self._closed = book, path, chain, False

    @classmethod
    def acquire(cls, path, permit):
        meter = consume(permit, 'acquire-parent', path)
        owner = meter._owner
        permit._book.policy.verify(meter,owner)
        parts = _components(path)
        if permit._limits.fds < len(parts) + 1:
            raise Refusal('OperationFDLimit')
        baseline = _record_coordinator(permit._book, owner)
        if baseline._current['fds'] + len(parts) + 1 > 64:
            permit._book.halt('LiveLimit')
            raise Refusal('LiveLimit')
        hold = _reserve_cleanup_hold(permit._book,permit,len(parts)+1)
        chain = []
        try:
            fd = _call(meter, owner, os.open, '/', _DIR)
            chain.append((fd, '', _identity(_call(meter, owner, os.fstat, fd))))
            for part in parts:
                fd = _call(meter, owner, os.open, part, _DIR, dir_fd=chain[-1][0])
                chain.append((fd, part, _identity(_call(meter, owner, os.fstat, fd))))
            lease = cls(_KEY, permit._book, path, chain)
            lease._cleanup_hold=hold
            _bind_cleanup_hold(hold,lease)
            lease._validate(meter, owner)
            _record_coordinator(permit._book, owner)
            return lease
        except BaseException:
            permit._book.halt('ParentAcquisitionFailed')
            _failure_close(hold,[(fd,identity) for fd,_,identity in chain])
            raise

    def _validate(self, meter, owner):
        if self._closed or self._book is not meter._book:
            raise Refusal('InvalidParentLease')
        self._book.policy.verify(meter, owner)
        for index, (fd, name, identity) in enumerate(self._chain):
            if _identity(_call(meter, owner, os.fstat, fd)) != identity:
                raise Refusal('ParentIdentity')
            if index:
                st = _call(meter, owner, os.stat, name, dir_fd=self._chain[index - 1][0], follow_symlinks=False)
                if _identity(st) != identity or not stat.S_ISDIR(st.st_mode):
                    raise Refusal('ParentRetargeted', partial=True)

    def close_requirements(self):
        return _cleanup_requirements(self._cleanup_hold)

    def close(self, permit):
        meter = consume(permit, 'cleanup-close', self)
        owner = meter._owner
        if self._closed:
            raise Refusal('ParentClosed')
        count=len(self._chain)
        if (permit._limits.syscalls < 2*count or permit._limits.work < 2*count):
            raise Refusal('CleanupLimit')
        for fd, _, identity in reversed(self._chain):
            if _identity(_call(meter, owner, os.fstat, fd)) != identity:
                raise Refusal('ForeignDescriptor')
            _call(meter, owner, os.close, fd)
        self._closed = True


class OwnedLedger(Opaque):
    def __init__(self, key, parent, name, fd, identity):
        if key is not _KEY:
            raise Refusal('InvalidLedger')
        self._parent, self._book, self.name = parent, parent._book, name
        self._fd, self._identity, self._closed = fd, identity, False

    @classmethod
    def create(cls, parent, name, permit):
        if type(parent) is not ParentLease:
            raise Refusal('InvalidParentLease')
        meter = consume(permit, 'create-ledger', (parent, name))
        owner = meter._owner
        _name(name)
        if permit._limits.fds < 1:
            raise Refusal('OperationFDLimit')
        baseline = _record_coordinator(permit._book, owner)
        if baseline._current['fds'] + 1 > 64 or len(permit._book._created_regular) + 1 > 64:
            permit._book.halt('LiveLimit')
            raise Refusal('LiveLimit')
        parent._validate(meter, owner)
        hold = _reserve_cleanup_hold(permit._book,permit,1)
        fd = _call(meter, owner, os.open, name, _FILE | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=parent._chain[-1][0])
        identity = None
        try:
            st = _call(meter, owner, os.fstat, fd)
            identity = _identity(st)
            if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) != 0o600:
                raise Refusal('LedgerIdentity', partial=True)
            _call(meter, owner, fcntl.flock, fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = cls(_KEY, parent, name, fd, identity)
            result._cleanup_hold=hold
            _bind_cleanup_hold(hold,result)
            result._validate(meter, owner)
            parent._book._ledger = result
            parent._book._created_regular[('ledger', identity)] = True
            _record_coordinator(permit._book, owner)
            return result
        except BaseException:
            permit._book.halt('LedgerCreationFailed')
            if identity is not None:
                _failure_close(hold,[(fd,identity)])
            raise

    def _validate(self, meter, owner):
        if self._closed:
            raise Refusal('LedgerClosed')
        self._parent._validate(meter, owner)
        st = _call(meter, owner, os.fstat, self._fd)
        linked = _call(meter, owner, os.stat, self.name, dir_fd=self._parent._chain[-1][0], follow_symlinks=False)
        if (_identity(st) != self._identity or _identity(linked) != self._identity or
                st.st_nlink != 1 or linked.st_nlink != 1):
            raise Refusal('LedgerIdentity', partial=True)

    def write_json(self, record, permit):
        meter = consume(permit, 'update-record', self)
        owner = meter._owner
        try:
            raw = encode(record, permit)
            self._validate(meter, owner)
            offset = attempts = 0
            while offset < len(raw):
                attempts += 1
                if attempts > 256:
                    raise Refusal('WriteAttempts', partial=True)
                chunk = raw[offset:offset + 4096]
                meter.charge(owner, source_io=len(chunk))
                count = _call(meter, owner, os.pwrite, self._fd, chunk, offset)
                if type(count) is not int or not 0 < count <= len(chunk):
                    raise Refusal('ShortWrite', partial=True)
                offset += count
                self._validate(meter, owner)
            _call(meter, owner, os.ftruncate, self._fd, len(raw))
            self._validate(meter, owner)
            _call(meter, owner, os.fsync, self._fd)
            self._validate(meter, owner)
            _call(meter, owner, os.fsync, self._parent._chain[-1][0])
            self._validate(meter, owner)
            offset = requests = 0
            while offset < len(raw):
                requests += 1
                if requests > 64:
                    raise Refusal('ReadAttempts', partial=True)
                size = min(4096, len(raw) - offset)
                meter.charge(owner, source_io=size)
                part = _call(meter, owner, os.pread, self._fd, size, offset)
                if part != raw[offset:offset + size]:
                    raise Refusal('ReadbackMismatch', partial=True)
                offset += size
                self._validate(meter, owner)
            meter.charge(owner, source_io=1)
            if _call(meter, owner, os.pread, self._fd, 1, offset):
                raise Refusal('ReadbackTail', partial=True)
            self._validate(meter, owner)
            meter.charge(owner, journal_events=1, journal_bytes=len(raw))
            self._book._committed_sequence = permit.record_sequence
            self._book._commits += 1
            _record_coordinator(self._book, owner)
            return dict(bytes=len(raw), sequence=permit.record_sequence)
        except BaseException:
            self._book.halt('LedgerUpdateFailed')
            raise

    def close_requirements(self):
        return _cleanup_requirements(self._cleanup_hold)

    def close(self, permit):
        meter = consume(permit, 'cleanup-close', self)
        owner = meter._owner
        if permit._limits.syscalls < 2 or permit._limits.work < 2:
            raise Refusal('CleanupLimit')
        if self._closed or _identity(_call(meter, owner, os.fstat, self._fd)) != self._identity:
            raise Refusal('ForeignDescriptor')
        _call(meter, owner, os.close, self._fd)
        self._closed = True


def sample_coordinator(book, owner, reservation=None):
    """Actual coordinator-only kernel sample; diagnostic/HALT, no P authority."""
    meter = reservation
    if meter is None:
        meter = book.reserve_phase('audit', owner,
                    dict(syscalls=64,work=16384,source_io=4097))
    if type(meter) is not PhaseReservation or meter not in book._reservations:
        raise Refusal('InvalidReservation')
    meter.check(owner)
    statusfd = None
    try:
        statusfd = _call(meter,owner,os.open,'/proc/self/status',os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
        meter.charge(owner,source_io=4097)
        raw = _call(meter,owner,os.read,statusfd,4097)
        closing=statusfd
        statusfd=None
        _call(meter,owner,os.close,closing)
        if len(raw)>4096:
            raise Refusal('UnknownLiveMeasurement')
        meter.charge(owner,work=len(raw))
        rss={}
        for line in raw.decode('ascii').splitlines():
            fields=line.split()
            if fields and fields[0] in ('VmRSS:','VmHWM:'):
                if (fields[0] in rss or len(fields)!=3 or fields[2]!='kB' or
                        len(fields[1])>16 or not fields[1].isdigit()):
                    raise Refusal('UnknownLiveMeasurement')
                rss[fields[0]]=int(fields[1])*1024
        if set(rss)!={'VmRSS:','VmHWM:'}:
            raise Refusal('UnknownLiveMeasurement')
        meter.charge(owner,syscalls=4,work=65)
        count=0
        with os.scandir('/proc/self/fd') as entries:
            for _ in entries:
                count+=1
                if count>64:
                    book._live['overflow']={'fds_at_least':count}
                    previous=book._live['peak']
                    if previous is not None:previous['fds']=max(previous['fds'],count)
                    book.halt('LiveLimit')
                    raise Refusal('LiveLimit')
        meter.check(owner)
        current=dict(processes=1,rss_bytes=rss['VmRSS:'],fds=count,
                     files=len(book._created_regular))
        peaks=dict(current);peaks['rss_bytes']=rss['VmHWM:']
        observation=_source_live_observation(book,owner,current,peaks,
                        'COORDINATOR_ONLY',__import__('time').monotonic_ns())
        return observation
    except BaseException:
        book.halt('UnknownLiveMeasurement')
        if statusfd is not None:
            try:
                _emergency_close(book,statusfd)
            except (OSError,Refusal):
                book.halt('CleanupIncomplete')
        raise


def _record_coordinator(book, owner, reservation=None):
    observation=sample_coordinator(book,owner,reservation)
    book.record_live(observation)
    return observation


def _failure_close(hold,records):
    if hold._used:
        hold._book.halt('CleanupIncomplete')
        return
    try:
        meter=_take_cleanup_hold(hold,hold._owner)
        for fd,identity in reversed(records):
            if _identity(_call(meter,hold._owner,os.fstat,fd))!=identity:
                raise Refusal('ForeignDescriptor')
            _call(meter,hold._owner,os.close,fd)
    except (Refusal,OSError):
        hold._book.halt('CleanupIncomplete')


def _emergency_close(book,fd):
    # Only immediate actual os.open results not exposed to any caller, or this
    # frame's never-detached probe fd. No path/stat/reconstructed descriptor.
    if book._emergency_closes>=2:
        book.halt('CleanupIncomplete')
        return
    book._emergency_closes+=1
    try:
        meter=book._probe_emergency
        meter.charge(book,syscalls=1,work=1)
        os.close(fd)
        meter.check(book)
    except (Refusal,OSError):
        book.halt('CleanupIncomplete')
        book._live['cleanup_unknown']=True
