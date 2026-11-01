"""Same-origin, full-spend bookkeeping; this module performs NO filesystem IO."""
from dataclasses import dataclass, fields
import time
from .errors import Opaque, Refusal

PHASES = ('issuer', 'ledger', 'protocol', 'P', 'helper', 'chunk', 'binary', 'audit')
DIMENSIONS = dict(source_io=4294967296, prepared_bytes=134217728, commands=16,
                  output_bytes=16777216, processes=8, rss_bytes=268435456,
                  fds=64, wire_bytes=67108864, messages=4096, polls=100000,
                  journal_events=512, journal_bytes=33554432, files=64,
                  work=16777216, syscalls=65536)
LIVE = ('processes', 'rss_bytes', 'fds', 'files')
CUMULATIVE = tuple(k for k in DIMENSIONS if k not in LIVE)
_KEY = object()


@dataclass(frozen=True)
class OperationLimits:
    syscalls: int = 256
    work: int = 65536
    io: int = 65536
    fds: int = 0
    duration_ns: int = 2000000000
    max_record_bytes: int = 8192

    def __post_init__(self):
        for f in fields(self):
            v = getattr(self, f.name)
            if type(v) is not int or v < 0 or v.bit_length() > 63:
                raise Refusal('InvalidLimits')
        if (not 0 < self.duration_ns <= 960000000000 or
                not 1 <= self.max_record_bytes <= 262144 or
                self.syscalls > 65536 or self.work > 16777216 or
                self.io > 4294967296 or self.fds > 64):
            raise Refusal('InvalidLimits')


class PhaseReservation(Opaque):
    __slots__ = ('_book', '_owner', '_phase', '_maxima', '_used', '_end', '_closed')

    def __init__(self, key, book, owner, phase, maxima, end):
        if key is not _KEY:
            raise Refusal('InvalidReservation')
        self._book, self._owner, self._phase = book, owner, phase
        self._maxima, self._used = dict(maxima), {k: 0 for k in maxima}
        self._end, self._closed = end, False

    def check(self, owner):
        if (self not in self._book._reservations or self._closed or owner is not self._owner):
            raise Refusal('InvalidReservation')
        if self._phase == 'issuer':
            if self._used['syscalls'] >= self._maxima['syscalls']:
                self._book.halt('OperationLimit')
                raise Refusal('OperationLimit')
            self._used['syscalls'] += 1
        now=self._book._check(self._phase == 'cleanup')
        if now >= self._end:
            self._book.halt('OperationDeadline')
            raise Refusal('OperationDeadline')

    def charge(self, owner, **actual):
        self.check(owner)
        for name, count in actual.items():
            if name in LIVE:
                raise Refusal('LiveObservationRequired')
            if type(count) is not int or count < 0 or name not in self._maxima:
                self._book.halt('InvalidCharge')
                raise Refusal('InvalidCharge')
            if self._used[name] + count > self._maxima[name]:
                self._book.halt('OperationLimit')
                raise Refusal('OperationLimit')
        for name, count in actual.items():
            self._used[name] += count

    def observation(self):
        return dict(phase=self._phase, reserved=dict(self._maxima),
                    actual=dict(self._used), end_ns=self._end, closed=self._closed)

    def close(self, owner):
        self.check(owner)
        self._closed = True


class LedgerOperationPermit(Opaque):
    __slots__ = ('_book', '_kind', '_owner', '_limits', '_meter', '_consumed',
                 '_operation', '_record_sequence')

    def __init__(self, key, book, kind, owner, limits, meter, operation, sequence):
        if key is not _KEY:
            raise Refusal('InvalidPermit')
        self._book, self._kind, self._owner = book, kind, owner
        self._limits, self._meter, self._consumed = limits, meter, False
        self._operation, self._record_sequence = operation, sequence

    @property
    def record_sequence(self):
        return self._record_sequence


def consume(permit, kind, owner):
    """Validate the actual live registry BEFORE any caller record or IO is read."""
    if type(permit) is not LedgerOperationPermit:
        raise Refusal('InvalidPermit')
    try:
        book = permit._book
        valid = (permit in book._permits and not permit._consumed and
                 permit._kind == kind)
        if kind == 'create-ledger':
            valid = valid and type(permit._owner) is tuple and len(permit._owner) == 2
            valid = valid and permit._owner[0] is owner[0] and permit._owner[1] == owner[1]
        elif kind == 'acquire-parent':
            valid = valid and type(owner) is str and permit._owner == owner == book.parent_path
        else:
            valid = valid and permit._owner is owner
    except (AttributeError, TypeError):
        raise Refusal('InvalidPermit') from None
    if not valid:
        book.halt('InvalidPermit')
        raise Refusal('InvalidPermit')
    permit._consumed = True
    book._check(kind == 'cleanup-close')
    permit._meter.check(permit._meter._owner)
    return permit._meter


class LeafAccount(Opaque):
    """A genuine issuer starts this book unauthorised; facts never activate it."""
    def __init__(self, key, policy, leaf, parent_path, basename):
        if key is not _KEY:
            raise Refusal('IssuerRequired')
        self.policy, self.leaf = policy, leaf
        self.parent_path, self.basename = parent_path, basename
        self.origin_ns, self.end_ns = policy.origin_ns, policy.end_ns
        self._source, self._plan = policy.source_hash, policy.plan_hash
        self._spent = {k: 0 for k in CUMULATIVE}
        self._live = dict(baseline=None, current=None, peak=None, coverage='UNKNOWN', observed_ns=None)
        self._live_observations, self._owners = set(), {}
        self._created_regular = {}
        self._cleanup_holds = {}
        self._reservations, self._permits = set(), set()
        self._authorised, self._fault, self._closed = False, None, False
        self._operation = self._sequence = self._commits = 0
        self._ledger = None
        self._cleanup_left = 108
        self._cleanup_close_left = 60
        self._cleanup_work_left = 8128
        self._cleanup = self._reserve('cleanup', self, dict(syscalls=128, work=16384, source_io=4097),
                                      self.end_ns, bootstrap=True)
        self._cleanup_observation=PhaseReservation(_KEY,self,self,'cleanup',
                    dict(syscalls=16,work=8192,source_io=4097),self.end_ns)
        self._reservations.add(self._cleanup_observation)
        self._emergency_closes=0
        self._probe_emergency=PhaseReservation(_KEY,self,self,'cleanup',dict(syscalls=4,work=64),self.end_ns)
        self._reservations.add(self._probe_emergency)

    def _check(self, cleanup=False):
        if self._closed:
            raise Refusal('AccountClosed')
        now=time.monotonic_ns()
        if not cleanup:
            if self._fault:
                raise Refusal(self._fault)
            if now>=self.end_ns:
                self.halt('LeafDeadline')
                raise Refusal('LeafDeadline')
        return now

    def halt(self, code):
        if self._fault is None:
            self._fault = code

    def _reserve(self, phase, owner, maxima, end, bootstrap=False):
        if phase != 'cleanup':
            self._check()
        if not bootstrap and not self._authorised:
            raise Refusal('UnauthorisedAccount')
        if type(maxima) is not dict or not maxima or len(maxima) > len(DIMENSIONS):
            raise Refusal('InvalidReservation')
        for k, n in maxima.items():
            if type(k) is not str or len(k) > 64 or k not in DIMENSIONS or type(n) is not int or n < 0 or n.bit_length() > 63:
                raise Refusal('InvalidReservation')
            if (n > DIMENSIONS[k] if k in LIVE else self._spent[k] + n > DIMENSIONS[k]):
                self.halt('LeafBudget')
                raise Refusal('LeafBudget')
        for k, n in maxima.items():
            if k not in LIVE:
                self._spent[k] += n
        self._owners[id(owner)] = owner
        reservation = PhaseReservation(_KEY, self, owner, phase, maxima, min(end, self.end_ns))
        self._reservations.add(reservation)
        return reservation

    def reserve_phase(self, phase, owner, maxima, *, duration_ns=2000000000):
        if type(phase) is not str or phase not in PHASES or phase == 'issuer' or type(duration_ns) is not int:
            raise Refusal('InvalidPhase')
        if not 0 < duration_ns <= 960000000000:
            raise Refusal('InvalidPhase')
        return self._reserve(phase, owner, maxima, time.monotonic_ns() + duration_ns)

    def reserve_ledger_operation(self, kind, bound_owner, limits):
        if type(limits) is not OperationLimits:
            raise Refusal('InvalidLimits')
        if type(kind) is not str or kind not in ('acquire-parent', 'create-ledger', 'update-record', 'cleanup-close'):
            raise Refusal('InvalidPermitKind')
        self._check(kind == 'cleanup-close')
        if not self._authorised:
            raise Refusal('UnauthorisedAccount')
        caps = {'acquire-parent': 256, 'create-ledger': 256, 'update-record': 1024,
                'cleanup-close': 128}
        if limits.syscalls > caps[kind] or limits.work > 262144:
            raise Refusal('InvalidLimits')
        if kind == 'update-record' and limits.io > 2 * limits.max_record_bytes + 1:
            raise Refusal('InvalidLimits')
        if kind == 'acquire-parent' and (type(bound_owner) is not str or bound_owner != self.parent_path):
            raise Refusal('InvalidParentPath')
        self._operation += 1
        if kind == 'cleanup-close':
            hold=self._cleanup_holds.get(id(bound_owner))
            if hold is None or hold._owner is not bound_owner or hold._used:
                raise Refusal('InvalidCleanupOwner')
            if (limits.syscalls != hold._syscalls or limits.work != hold._work or limits.io != 0):
                raise Refusal('CleanupLimits')
            hold._used=True
            meter = PhaseReservation(_KEY,self,bound_owner,'cleanup',
                            dict(syscalls=hold._syscalls,work=hold._work),self.end_ns)
            self._reservations.add(meter)
        else:
            if kind == 'create-ledger':
                if (type(bound_owner) is not tuple or len(bound_owner) != 2 or
                        type(bound_owner[1]) is not str or bound_owner[1] != self.basename):
                    raise Refusal('InvalidLedgerName')
            if kind == 'update-record':
                if bound_owner is not self._ledger:
                    raise Refusal('InvalidLedger')
                self._sequence += 1
            maxima = dict(syscalls=limits.syscalls, work=limits.work,
                          source_io=limits.io, fds=limits.fds)
            if kind == 'create-ledger':
                maxima['files'] = 1
            if kind == 'update-record':
                        maxima.update(prepared_bytes=4 * limits.max_record_bytes + 1048576,
                              journal_events=1, journal_bytes=limits.max_record_bytes)
            meter = self._reserve('ledger', bound_owner, maxima,
                                  time.monotonic_ns() + limits.duration_ns)
        permit = LedgerOperationPermit(_KEY, self, kind, bound_owner, limits, meter,
                                       self._operation, self._sequence)
        self._permits.add(permit)
        return permit

    def record(self, state, facts, permit):
        if (type(permit) is not LedgerOperationPermit or permit not in self._permits or
                permit._book is not self or permit._kind != 'update-record' or permit._consumed):
            raise Refusal('InvalidPermit')
        return dict(schema='wordling.reference-controller.ledger/v1', leaf=self.leaf,
                    sequence=permit.record_sequence, state=state,
                    source=dict(binding=self._source, plan=self._plan),
                    observed_ns=time.monotonic_ns(), facts=facts)

    def record_live(self, observation):
        if type(observation) is not LiveObservation or observation not in self._live_observations:
            raise Refusal('InvalidLiveObservation')
        if (observation._used or observation._book is not self or
                self._owners.get(id(observation._owner)) is not observation._owner or
                observation._source != self._source):
            raise Refusal('InvalidLiveObservation')
        observation._used=True
        now=time.monotonic_ns()
        if (type(observation._observed_ns) is not int or
                not self.origin_ns<=observation._observed_ns<=now<self.end_ns or
                now-observation._observed_ns>2000000000):
            self.halt('ExpiredLiveObservation')
            raise Refusal('ExpiredLiveObservation')
        self._live['current']=dict(observation._current)
        if self._live['baseline'] is None:
            self._live['baseline']=dict(observation._current)
        previous=self._live['peak'] or {k:0 for k in LIVE}
        self._live['peak']={k:max(previous[k],observation._current[k],observation._peaks[k]) for k in LIVE}
        self._live['coverage']=observation._coverage
        self._live['observed_ns']=observation._observed_ns
        if any(self._live['peak'][k]>DIMENSIONS[k] for k in LIVE):
            self.halt('LiveLimit')
            raise Refusal('LiveLimit')

    def observation(self):
        return dict(leaf=self.leaf, origin_ns=self.origin_ns, end_ns=self.end_ns,
                    source=self._source, plan=self._plan, authorised=self._authorised,
                    spent=dict(self._spent), fault=self._fault, ledger_commits=self._commits,
                    operation=self._operation, closed=self._closed,
                    live={k: dict(v) if type(v) is dict else v for k,v in self._live.items()},
                    live_ceilings={k:DIMENSIONS[k] for k in LIVE})


class _CleanupHold(Opaque):
    def __init__(self,key,book,owner,count):
        if key is not _KEY: raise Refusal('InvalidCleanupOwner')
        self._book,self._owner,self._count=book,owner,count
        self._syscalls,self._work=2*count,4*count+32
        self._used=False


def _reserve_cleanup_hold(book,owner,count):
    if type(count) is not int or not 0<=count<=64:
        raise Refusal('CleanupLimit')
    syscalls,work=2*count,4*count+32
    if (book._cleanup_left<syscalls or book._cleanup_work_left<work or
            book._cleanup_close_left<count or id(owner) in book._cleanup_holds):
        book.halt('CleanupLimit')
        raise Refusal('CleanupLimit')
    book._cleanup_left-=syscalls
    book._cleanup_work_left-=work
    book._cleanup_close_left-=count
    hold=_CleanupHold(_KEY,book,owner,count)
    book._cleanup_holds[id(owner)]=hold
    return hold


def _bind_cleanup_hold(hold,owner):
    if hold._used: raise Refusal('InvalidCleanupOwner')
    book=hold._book
    if book._cleanup_holds.get(id(hold._owner)) is not hold or id(owner) in book._cleanup_holds:
        raise Refusal('InvalidCleanupOwner')
    del book._cleanup_holds[id(hold._owner)]
    hold._owner=owner
    book._cleanup_holds[id(owner)]=hold



def _take_cleanup_hold(hold,owner):
    book=hold._book
    if (hold._owner is not owner or hold._used or
            book._cleanup_holds.get(id(owner)) is not hold):
        raise Refusal('InvalidCleanupOwner')
    hold._used=True
    meter=PhaseReservation(_KEY,book,owner,'cleanup',
                dict(syscalls=hold._syscalls,work=hold._work),book.end_ns)
    book._reservations.add(meter)
    return meter


def _cleanup_requirements(hold):
    return OperationLimits(syscalls=hold._syscalls,work=hold._work,io=0)

class LiveObservation(Opaque):
    __slots__ = ('_book','_owner','_source','_observed_ns','_current','_peaks','_coverage','_used')

    def __init__(self, key, book, owner, current, peaks, coverage, observed_ns):
        if key is not _KEY:
            raise Refusal('InvalidLiveObservation')
        self._book,self._owner,self._source=book,owner,book._source
        self._observed_ns,self._coverage=observed_ns,coverage
        self._current,self._peaks=dict(current),dict(peaks)
        self._used=False


def _source_live_observation(book, owner, current, peaks, coverage, observed_ns):
    """Source-only observations: actual bound actors, never copied Usage credit."""
    if book._owners.get(id(owner)) is not owner:
        raise Refusal('InvalidLiveOwner')
    for values in (current,peaks):
        if (type(values) is not dict or set(values)!=set(LIVE) or
                any(type(v) is not int or v<0 or v.bit_length()>63 for v in values.values())):
            raise Refusal('UnknownLiveMeasurement')
    if coverage not in ('COORDINATOR_ONLY','RETAINED_BOUND_ACTOR_SET'):
        raise Refusal('UnknownLiveMeasurement')
    observation=LiveObservation(_KEY,book,owner,current,peaks,coverage,observed_ns)
    book._live_observations.add(observation)
    return observation

def _new_book(policy, leaf, parent_path, basename):
    return LeafAccount(_KEY, policy, leaf, parent_path, basename)


def _issuer_reservation(book, owner, fds):
    return book._reserve('issuer', owner,
                         dict(syscalls=1024, work=65536, source_io=65536, fds=fds, files=1, output_bytes=32768),
                         time.monotonic_ns() + 2000000000, bootstrap=True)


def _activate(book, key):
    if key is not _KEY or book._authorised:
        raise Refusal('InvalidHandoff')
    book._check()
    book._authorised = True
