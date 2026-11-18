"""Finite CONTROL-only administration, callable only with a live ROOT decision.

Deployed under the ordinary name reference_controller.original_control_admin.
Importing this file provisions nothing. No ORIGINAL path, guard or tool is used.
"""
from dataclasses import dataclass, asdict
import hashlib
import json
import os
import stat
import time
from .errors import Refusal

from .original import CONTROL_BASE as BASE, CONTROL_CAMPAIGN_NS
GROUPS = ('owned','marker','handoff','contention','retarget','missing','dirty','expired',
          'source','identity','late','daemon','master','tool','cleanup','exhausted','death','crossdomain')


@dataclass(frozen=True)
class ControlAdministration:
    row_id: str
    domain: str
    profile: str
    candidate: str
    source: str
    groups: tuple

    @classmethod
    def from_row(cls, row):
        if (set(row) != {'id','action','domain','profile','candidate','source','groups','limits'} or
                row['id'] != 'CONTROL-ADMIN-104' or row['action'] != 'control-admin' or
                row['domain'] != 'CONTROL' or row['profile'] != 'CONTROL-V1' or
                type(row['groups']) is not list or tuple(row['groups']) != GROUPS):
            raise Refusal('ControlAdministrationScope')
        return cls(row['id'],row['domain'],row['profile'],row['candidate'],row['source'],tuple(row['groups']))

    def digest(self):
        return hashlib.sha256(json.dumps(asdict(self),sort_keys=True,separators=(',',':')).encode('ascii')).hexdigest()


def administer_one(decision, source, plan):
    from .original_release import _consume_decision
    origin, accepted = _consume_decision(decision,source,plan)
    from .bootstrap import validate_policy
    validate_policy(source)
    if type(plan) is not ControlAdministration or plan.groups != GROUPS or plan.source != source.source_hash:
        raise Refusal('ControlAdministrationScope')
    end = origin+30000000000
    used = dict(syscalls=0,bytes=0,files=0,work=0)
    held = []
    def call(function, *args, **kwargs):
        if time.monotonic_ns() >= end or used['syscalls'] >= 4093 or used['work']+1 > 65536:
            raise Refusal('ControlAdministrationLimit',partial=True)
        used['syscalls'] += 1
        used['work'] += 1
        value = function(*args,**kwargs)
        if time.monotonic_ns() >= end:
            raise Refusal('ControlAdministrationDeadline',partial=True)
        return value
    def source_phase():
        source.verify_administration(end,used)
    source_phase()  # BEFORE any creating effect
    flags = os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC
    def directory(parent, name):
        call(os.mkdir,name,0o700,dir_fd=parent)
        fd = call(os.open,name,flags,dir_fd=parent)
        st = call(os.fstat,fd)
        linked = call(os.stat,name,dir_fd=parent,follow_symlinks=False)
        if (st.st_dev,st.st_ino) != (linked.st_dev,linked.st_ino) or st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) != 0o700:
            call(os.close,fd)
            raise Refusal('ControlAdministrationIdentity',partial=True)
        call(os.fsync,parent)
        return fd
    def file(parent, name, raw, mode):
        if used['files'] >= 128 or used['bytes']+2*len(raw) > 33554432 or len(raw) > 1048576:
            raise Refusal('ControlAdministrationLimit',partial=True)
        used['files'] += 1
        used['bytes'] += 2*len(raw)  # write plus complete readback, no free IO
        fd = call(os.open,name,os.O_RDWR|os.O_NOFOLLOW|os.O_CLOEXEC|os.O_CREAT|os.O_EXCL,mode,dir_fd=parent)
        try:
            if call(os.write,fd,raw) != len(raw):
                raise Refusal('ControlAdministrationShortWrite',partial=True)
            call(os.fsync,fd)
            if call(os.pread,fd,len(raw)+1,0) != raw:
                raise Refusal('ControlAdministrationReadback',partial=True)
            st = call(os.fstat,fd)
            linked = call(os.stat,name,dir_fd=parent,follow_symlinks=False)
            if ((st.st_dev,st.st_ino) != (linked.st_dev,linked.st_ino) or
                    st.st_nlink != 1 or st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) != mode):
                raise Refusal('ControlAdministrationIdentity',partial=True)
            call(os.fsync,parent)
        finally:
            call(os.close,fd)
        if raw:
            source_phase()  # nonempty file phase; empty files belong to bounded group phase
    def read(path, maximum):
        fd = call(os.open,path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
        try:
            before = call(os.fstat,fd)
            raw = call(os.read,fd,maximum+1)
            after = call(os.fstat,fd)
            linked = call(os.stat,path,follow_symlinks=False)
            fields = lambda st:(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
            if len(raw)>maximum or fields(before)!=fields(after) or fields(after)!=fields(linked):
                raise Refusal('ControlAdministrationInputChanged')
            used['bytes'] += len(raw)
            if used['bytes'] > 33554432:
                raise Refusal('ControlAdministrationLimit',partial=True)
            source_phase()  # every bounded blocking input phase
            return raw
        finally:
            call(os.close,fd)
    data = {n:(p,s,h) for n,p,s,h in source.fixtures}
    fixture = read(data['control-fixture'][0],1048576)
    master = read(data['control-master.bin'][0],25)
    if (master != b'WORDLING ROOT CONTROL V1\n' or len(fixture) > 1048576 or
            hashlib.sha256(fixture).hexdigest() != data['control-fixture'][2]):
        raise Refusal('ControlAdministrationInputs')
    if (2*len(GROUPS)+1)*(len(fixture)+len(master))+131072 > 33554432:
        raise Refusal('ControlAdministrationFit')
    boot = read('/proc/sys/kernel/random/boot_id',64).decode('ascii').strip()
    mounts = read('/proc/self/mountinfo',65536).decode('utf-8')
    candidates = []
    for line in mounts.splitlines():
        left,right = line.split(' - ',1)
        mount = left.split()[4]
        if BASE == mount or BASE.startswith(mount.rstrip('/')+'/'):
            candidates.append((len(mount),right.split()[0]))
    if not candidates or max(candidates)[1] not in ('ext4','xfs','btrfs','tmpfs','overlay'):
        raise Refusal('ControlUnprovedLocalFilesystem')
    source_phase()  # accepted source still live after input/hash/mount phases
    try:
        tmp = call(os.open,'/tmp',flags)
        held.append(tmp)
        base = directory(tmp,BASE.rsplit('/',1)[1])
        held.append(base)
        wp = directory(base,'wp104')
        held.append(wp)
        for group in GROUPS:
            fd = directory(wp,group)
            try:
                for name in ('issuer','ledgers','shared','sources','tools','observations'):
                    child = directory(fd,name)
                    try:
                        if name == 'issuer':
                            metadata = dict(schema='wordling.ROOT-CONTROL.issuer/v1',
                                kind='wordling.ROOT-CONTROL.ledger/v1',generation='CONTROL-v1',
                                uid=os.getuid(),source=source.source_hash,
                                boot=boot)
                            file(child,'issuer.json',(json.dumps(metadata,sort_keys=True,separators=(',',':'))+'\n').encode('ascii'),0o600)
                            file(child,'issuer.lock',b'',0o600)
                        elif name == 'shared':
                            if group != 'missing':
                                file(child,'session1.lock',b'',0o600)
                        elif name == 'sources':
                            file(child,'control-master.bin',b'CONTROL wrong source\n' if group=='master' else master,0o600)
                        elif name == 'tools':
                            file(child,'control-fixture',fixture+b'CONTROL mismatch' if group=='tool' else fixture,0o700)
                    finally:
                        call(os.close,child)
            finally:
                call(os.close,fd)
            if group == 'dirty':
                fd = call(os.open,group,flags,dir_fd=wp)
                try:
                    workspace = directory(fd,'w-g7')
                    try:
                        file(workspace,'CONTROL-foreign.bin',b'CONTROL prior foreign bytes\n',0o600)
                    finally:
                        call(os.close,workspace)
                finally:
                    call(os.close,fd)
            source_phase()  # bounded directory/group phase, no next group on loss
        source_phase()
        receipt = dict(schema='wordling.CONTROL-administration/v1',domain='CONTROL',profile='CONTROL-V1',
            original_qualification=False,root_invocation=accepted,source=source.source_hash,
            candidate=plan.candidate,origin_ns=origin,end_ns=end,campaign_end_ns=origin+CONTROL_CAMPAIGN_NS,
            usage_before_receipt=dict(used),receipt_io_bound=8192,
            cleanup_syscalls_bound=3,filesystem=max(candidates)[1],groups=list(GROUPS))
        file(wp,'ROOT-ADMIN-104.json',(json.dumps(receipt,sort_keys=True)+'\n').encode('ascii'),0o600)
        return dict(receipt,usage_before_parent_cleanup=dict(used))
    finally:
        for fd in reversed(held):
            used['syscalls'] += 1
            os.close(fd)  # fixed <=3 retained administration parents; no reuse/recovery.
