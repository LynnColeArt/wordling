"""Separate retained binary output authority; no raw chunks/path/hash permission API."""
import fcntl
import hashlib
import os
import stat
from .errors import Opaque, Refusal
from .ownership import _FILE, _call, _identity
from .account import _reserve_cleanup_hold, _take_cleanup_hold


class _Retained(Opaque):
    """Source-only funded slot, bound to actual controller/ParentLease/book."""
    def __init__(self, context, suffix, phase):
        from .controller import _require_context
        _require_context(context)
        self.context, self.parent, self.book = context, context._parent, context._book
        self.name = self.book.basename[:-5]+suffix
        if not self.name.isascii() or len(self.name)>64 or '/' in self.name:
            raise Refusal('PublicationName')
        self.meter = self.book.reserve_phase(phase, self,
            dict(syscalls=1024, work=262144, source_io=131073, prepared_bytes=32768,
                 files=1, fds=1), duration_ns=30000000000)
        self.hold = _reserve_cleanup_hold(self.book, self, 1)
        self.fd = self.identity = None
        self.closed = False

    def create(self):
        if self.fd is not None or self.closed:
            raise Refusal('PublicationUsed')
        self.parent._validate(self.meter, self)
        self.fd = _call(self.meter, self, os.open, self.name,
                        _FILE|os.O_CREAT|os.O_EXCL, 0o600, dir_fd=self.parent._chain[-1][0])
        st = _call(self.meter, self, os.fstat, self.fd)
        self.identity = _identity(st)
        if (not stat.S_ISREG(st.st_mode) or st.st_nlink!=1 or
                st.st_uid!=os.getuid() or stat.S_IMODE(st.st_mode)!=0o600):
            raise Refusal('PublicationIdentity', partial=True)
        _call(self.meter, self, fcntl.flock, self.fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
        self.book._created_regular[('publication', self.identity)] = True
        self.validate()

    def validate(self):
        if self.closed or self.fd is None or self.identity is None:
            raise Refusal('PublicationClosed')
        self.parent._validate(self.meter, self)
        st = _call(self.meter, self, os.fstat, self.fd)
        linked = _call(self.meter, self, os.stat, self.name,
                       dir_fd=self.parent._chain[-1][0], follow_symlinks=False)
        if (_identity(st)!=self.identity or _identity(linked)!=self.identity or
                st.st_nlink!=1 or linked.st_nlink!=1):
            raise Refusal('PublicationIdentity', partial=True)

    def close(self):
        if self.closed:
            raise Refusal('PublicationUsed')
        self.closed = True
        meter = _take_cleanup_hold(self.hold, self)
        if self.fd is not None:
            if self.identity is None or _identity(_call(meter,self,os.fstat,self.fd))!=self.identity:
                raise Refusal('PublicationForeignDescriptor')
            _call(meter,self,os.close,self.fd)
            self.fd = None


class _Physical(_Retained):
    def __init__(self, context):
        super().__init__(context, '.physical', 'P')

    def acquire(self):
        self.create()
        _call(self.meter,self,os.fsync,self.fd)
        _call(self.meter,self,os.fsync,self.parent._chain[-1][0])
        self.validate()

    def release(self):
        self.validate()
        self.close()


class _Binary(_Retained):
    def __init__(self, context, index):
        if index not in (0,1):
            raise Refusal('PublicationSlot')
        super().__init__(context, '.bin' if index==0 else '.empty', 'binary')
        self.index, self.cursor = index, 0

    def publish(self):
        c = self.context
        c._require_stopped()
        # Artifact references come ONLY from this retained actual Session's
        # internally held genuine derive result, not caller-provided chunks.
        batch = c._derived
        if batch is None or len(batch.artifacts)!=2:
            raise Refusal('PublicationAuthority')
        artifact = batch.artifacts[self.index]
        if type(artifact) is not c._provider.DerivedArtifactLease:
            raise Refusal('PublicationAuthority')
        expected_size = c._expected_size if self.index==0 else 0
        expected_hash = c._expected_hash if self.index==0 else hashlib.sha256(b'').hexdigest()
        self.create()
        digest = hashlib.sha256()
        attempts = chunks = 0
        while True:
            self.validate()
            chunk = c._p('chunk', artifact, self.cursor, 16384)
            chunks += 1
            if (type(chunk) is not c._provider.ArtifactChunk or type(chunk.data) is not bytes or
                    type(chunk.offset) is not int or chunk.offset!=self.cursor or
                    type(chunk.total_size) is not int or chunk.total_size!=expected_size or
                    chunk.sha256!=expected_hash or type(chunk.eof) is not bool or
                    len(chunk.data)>16384 or self.cursor+len(chunk.data)>expected_size or chunks>5):
                raise Refusal('PublicationChunk')
            self.meter.charge(self,work=len(chunk.data))
            expected = c._expected_part(self.cursor,len(chunk.data)) if self.index==0 else b''
            if chunk.data != expected:
                raise Refusal('PublicationExpectedBytes')
            offset = 0
            while offset<len(chunk.data):
                attempts += 1
                if attempts>256:
                    raise Refusal('PublicationWriteAttempts', partial=True)
                part = chunk.data[offset:offset+4096]
                self.meter.charge(self,source_io=len(part),work=len(part))
                n = _call(self.meter,self,os.pwrite,self.fd,part,self.cursor+offset)
                if type(n) is not int or not 0<n<=len(part):
                    raise Refusal('PublicationShortWrite', partial=True)
                offset += n
                self.validate()
            digest.update(chunk.data)
            self.cursor += len(chunk.data)
            if chunk.eof:
                if self.cursor!=expected_size:
                    raise Refusal('PublicationEOF')
                break
            if not chunk.data:
                raise Refusal('PublicationProgress')
        if digest.hexdigest()!=expected_hash:
            raise Refusal('PublicationHash')
        _call(self.meter,self,os.fsync,self.fd)
        self.validate()
        _call(self.meter,self,os.fsync,self.parent._chain[-1][0])
        self.validate()
        verified = hashlib.sha256()
        offset = reads = 0
        while offset<expected_size:
            reads += 1
            if reads>16:
                raise Refusal('PublicationReadAttempts')
            size = min(4096,expected_size-offset)
            self.meter.charge(self,source_io=size,work=2*size)
            raw = _call(self.meter,self,os.pread,self.fd,size,offset)
            expected = c._expected_part(offset,size) if self.index==0 else b''
            if raw!=expected:
                raise Refusal('PublicationReadback', partial=True)
            verified.update(raw)
            offset += len(raw)
            self.validate()
        self.meter.charge(self,source_io=1)
        if _call(self.meter,self,os.pread,self.fd,1,offset) or verified.hexdigest()!=expected_hash:
            raise Refusal('PublicationReadback', partial=True)
        self.validate()
        result = dict(name=self.name,size=expected_size,sha256=expected_hash,chunks=chunks,
                      full_expected_bytes=True,durable_readback=True)
        self.close()
        return result


def prepare(context):
    """Pre-admit all actual slots/cleanup BEFORE P effects; no output FD yet."""
    return _Physical(context), (_Binary(context,0), _Binary(context,1))
