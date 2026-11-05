"""Source-owned bounded transport around the unchanged approved peer/QMP codec."""
from contextlib import contextmanager
from dataclasses import dataclass
import os
import time
import peer
import qmp
from .errors import Refusal


@dataclass(frozen=True)
class _Endpoint:
    SOCKET: str


def _structure_bound(raw):
    # A predecode work/depth filter, NOT another JSON decoder. The real QMP
    # read/execute alone decode. Counting all nonspace bytes conservatively
    # bounds values+keys; long strings can therefore be conservatively refused.
    depth = nonspace = 0
    quoted = escaped = False
    for byte in raw:
        if byte not in b' \t\r\n':
            nonspace += 1
            if nonspace > 2048:
                raise Refusal('ProtocolNodes')
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            depth += 1
            if depth > 16:
                raise Refusal('ProtocolDepth')
        elif byte in (93, 125):
            depth -= 1
            if depth < 0:
                raise Refusal('ProtocolStructure')


class _Stream:
    """No buffered read-ahead: each actual socket receive is bounded<=64B."""
    def __init__(self, actual_peer_stream, actual_socket, audit):
        self.peer, self.socket, self.audit = actual_peer_stream, actual_socket, audit
        self.pending = bytearray()

    def readline(self):
        a = self.audit
        self.peer.check()
        a.clock()
        line = bytearray()
        while True:
            if not self.pending:
                a.clock()
                maximum = min(64, 4096-len(line), 65536-a.received)
                if maximum <= 0:
                    raise Refusal('ProtocolLineOrWireLimit')
                a.meter.charge(a, syscalls=1, polls=1, work=1)
                raw = self.socket.recv(maximum)
                a.received += len(raw)  # Retain observed late bytes as diagnostics.
                a.clock()
                a.meter.charge(a, wire_bytes=len(raw), source_io=len(raw), work=len(raw))
                if not raw:
                    raise Refusal('ProtocolEOF', partial=bool(line))
                self.pending.extend(raw)
            position = self.pending.find(b'\n')
            count = len(self.pending) if position < 0 else position+1
            if len(line)+count > 4096:
                raise Refusal('ProtocolLineLimit')
            line.extend(self.pending[:count])
            del self.pending[:count]
            if line.endswith(b'\n'):
                a.meter.charge(a, messages=1)
                a.lines += 1
                if a.lines > 65:
                    raise Refusal('ProtocolEventLimit')
                a.meter.charge(a, work=len(line))
                _structure_bound(line)
                self.peer.check()
                a.clock()
                return bytes(line)
            if len(line) == 4096:
                raise Refusal('ProtocolLineLimit')

    def write(self, raw):
        a = self.audit
        a.clock()
        if type(raw) is not bytes or not 0 < len(raw) <= 4096:
            raise Refusal('ProtocolWriteLimit')
        a.meter.charge(a, wire_bytes=len(raw), messages=1, syscalls=1, work=len(raw))
        a.sent_attempted += len(raw)
        count = self.peer.write(raw)
        a.clock()
        if count != len(raw):
            raise Refusal('ProtocolShortWrite', partial=True)
        return count

    def flush(self):
        a = self.audit
        a.clock()
        a.meter.charge(a, syscalls=1, work=1)
        self.peer.flush()
        a.clock()


class _Codec(qmp.QMP):
    def __init__(self, audit):
        self.audit = audit
        self.greeting = True

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, value):
        # peer.connect assigns stream AFTER factory. This setter wraps that
        # actual assignment, before its FIRST q.read; no inherited __enter__.
        self._stream = _Stream(value, self.socket, self.audit)

    def read(self):
        result = qmp.QMP.read(self)
        if self.greeting:
            self.greeting = False
            if type(result) is not dict or 'QMP' not in result:
                raise Refusal('ProtocolGreeting')
            self.audit.greeting_ns = time.monotonic_ns()
        return result

    def execute(self, command, arguments=None):
        a = self.audit
        if command not in ('qmp_capabilities', 'query-test-stage', 'quit') or arguments is not None:
            raise Refusal('ProtocolCommand')
        if command == 'quit' and not a.quit_armed:
            raise Refusal('QuitAuthorityRequired')
        a.clock()
        a.transactions += 1
        if a.transactions > 3:
            raise Refusal('ProtocolTransactions')
        a.lines = 0
        a.transaction_end_ns = min(a.context._book.end_ns,time.monotonic_ns()+2000000000)
        return qmp.QMP.execute(self, command, arguments)


class _Audit:
    def __init__(self, context):
        from .controller import _require_context
        _require_context(context)
        self.context = context
        self.meter = context._book.reserve_phase('protocol', self,
            dict(wire_bytes=65536, messages=256, source_io=4194304, syscalls=32768,
                 work=4194304, polls=4096, prepared_bytes=1048576), duration_ns=20000000000)
        self.received = self.sent_attempted = self.transactions = self.lines = 0
        self.greeting_ns = None
        self.quit_armed = False
        self.transaction_end_ns = min(context._book.end_ns,time.monotonic_ns()+2000000000)
        self.path = context._workspace+'/qmp.sock'
        identity = context._p('identity')
        self.identity = identity
        self.owned = dict(pid=identity.pid, startticks=identity.startticks, socket=self.path)

    def clock(self):
        self.meter.check(self)
        if time.monotonic_ns() >= min(self.context._book.end_ns,self.transaction_end_ns,
                                      self.context._owned_ns+60000000000):
            raise Refusal('ProtocolDeadline')

    def same_identity(self, captured):
        if captured != self.owned:
            raise Refusal('ProtocolOwnerBinding')
        self.clock()
        current = self.context._p('identity')
        expected = self.identity
        if ((current.pid, current.startticks, current.exe_devino, current.exe_hash,
             current.argv, current.session_id, current.owner_epoch) !=
                (expected.pid, expected.startticks, expected.exe_devino, expected.exe_hash,
                 expected.argv, expected.session_id, expected.owner_epoch)):
            raise Refusal('ProtocolOwnerChanged')
        # Actual retained P lease is authority. These bounded kernel facts add
        # causal parent checking; caller PID/stat facts never replace that lease.
        self.meter.charge(self, syscalls=3, source_io=4096, work=4096)
        fd = os.open('/proc/%d/stat' % current.pid, os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
        try:
            raw = os.read(fd, 4096)
        finally:
            os.close(fd)
        self.clock()
        fields = raw.rsplit(b')', 1)[1].split()
        if (len(raw) >= 4096 or int(fields[1]) != self.context._worker_pid or
                int(fields[19]) != current.startticks):
            raise Refusal('ProtocolCausalParent')

    def facts(self):
        return dict(received=self.received, sent_attempted=self.sent_attempted,
                    transactions=self.transactions, greeting_ns=self.greeting_ns,
                    line_limit=4096, event_limit=64, transaction_wire_limit=65536)


@contextmanager
def connect(context):
    audit = _Audit(context)
    # The unchanged peer.connect always selects10s, even on a fast local peer.
    # Admission reserves that full interval plus fixed required tail, never patches it.
    if context._book.end_ns-time.monotonic_ns() < 20000000000:
        raise Refusal('ConnectTailFit')
    try:
        with peer.connect(_Endpoint(audit.path), lambda: _Codec(audit),
                          audit.owned, audit.same_identity) as codec:
            yield codec, audit
        audit.meter.close(audit)
    except BaseException:
        context._book.halt('ProtocolFault')
        context._protocol_facts = audit.facts()
        raise
