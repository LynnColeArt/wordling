"""Installed-package public consumer and adversarial OS acceptance cases.

Executed as an ordinary isolated script. It neither adds sys.path entries nor
loads a source file as a module. The coordinator seals and checks the venv first.
"""
import copy
import json
import os
from pathlib import Path
import sys
import time
import tracemalloc
from reference_controller.bootstrap import load_policy, SourcePolicyData
from reference_controller.account import OperationLimits, LeafAccount, LedgerOperationPermit, PHASES, CUMULATIVE, LIVE, DIMENSIONS, LiveObservation
from reference_controller.errors import Refusal
from reference_controller.issuance import TestIssuer, RootTicketIssuer, stable_key, provision_test_store
from reference_controller.ownership import ParentLease, OwnedLedger, sample_coordinator

case, root = sys.argv[1:3]
policy = load_policy()
issuer = TestIssuer()
permit = issuer.reserve(policy, root, 'wp68-v1', 'api-' + case, 'TEST-api', root+'-ledger')
book = parent = ledger = None


def refused(function, code=None):
    try:
        function()
    except Refusal as exc:
        if code is not None and exc.code != code:
            raise AssertionError((exc.code, code))
        return exc.code
    raise AssertionError('accepted prohibited operation')


def activate():
    global book
    book = issuer.activate(issuer.issue(permit))
    return book


def make_ledger():
    global parent, ledger
    activate()
    parent = ParentLease.acquire(book.parent_path, book.reserve_ledger_operation(
        'acquire-parent', book.parent_path, OperationLimits(fds=4)))
    ledger = OwnedLedger.create(parent, book.basename, book.reserve_ledger_operation(
        'create-ledger', (parent, book.basename), OperationLimits(fds=1)))


def update():
    return book.reserve_ledger_operation('update-record', ledger,
          OperationLimits(syscalls=1024, work=262144, io=16385))


try:
    if case == 'original-disabled':
        refused(lambda: RootTicketIssuer().issue(object()), 'SourcePrelaunchBlocked')
        assert not list(Path(root).glob('*.spent'))
    elif case == 'wrong-issuer-permit':
        refused(lambda: TestIssuer().issue(permit), 'InvalidIssuancePermit')
        assert not list(Path(root).glob('*.spent'))
    elif case == 'copied-permit':
        refused(lambda: copy.copy(permit), 'CapabilityNotCopyable')
        refused(lambda: ParentLease.acquire(root, {'kind':'acquire-parent'}), 'InvalidPermit')
        forged=object.__new__(LedgerOperationPermit)
        refused(lambda: ParentLease.acquire(root, forged), 'InvalidPermit')
        assert not list(Path(root).glob('*.spent'))
    elif case == 'unauthorized-book':
        refused(lambda: LeafAccount(None, policy, 'TEST', root, 'ledger'), 'IssuerRequired')
        before={p.name:p.read_bytes() for p in Path(root).iterdir()}
        identical=object.__new__(SourcePolicyData)
        identical.__dict__.update(policy.__dict__)
        copied=copy.copy(policy)
        foreign=object.__new__(SourcePolicyData)
        foreign.__dict__.update(policy.__dict__)
        foreign.package=Path('/foreign/deployment')
        for number,fake in enumerate((identical,copied,foreign)):
            refused(lambda: TestIssuer().reserve(fake,root,'wp68-v1','fake-'+str(number),'TEST',root+'-ledger'),'UnverifiedPolicyData')
        assert before=={p.name:p.read_bytes() for p in Path(root).iterdir()}
        assert not list(Path(root+'-ledger').iterdir())
        refused(lambda:TestIssuer().reserve(policy,root,'wp68-v1','outside','TEST','/tmp'),'NotTestNamespace')
        assert not list(Path(root).glob('*.spent'))
    elif case == 'full-phase-book':
        activate()
        before = book.observation()['spent']['work']
        owner = object()
        for phase in PHASES[1:]:
            p = book.reserve_phase(phase, owner, dict(work=2))
            p.charge(owner, work=1)
            p.close(owner)
        assert book.observation()['spent']['work'] == before + 14
        assert book.observation()['origin_ns'] == policy.origin_ns
        for dimension in CUMULATIVE:
            before_dimension=book.observation()['spent'][dimension]
            p=book.reserve_phase('audit',owner,{dimension:1})
            p.charge(owner,**{dimension:1});p.close(owner)
            assert book.observation()['spent'][dimension]==before_dimension+1
        before_live=book.observation()['live']
        for dimension in LIVE:
            for _ in range(2):
                p=book.reserve_phase('audit',owner,{dimension:DIMENSIONS[dimension]})
                refused(lambda:p.charge(owner,**{dimension:0}),'LiveObservationRequired')
                p.close(owner)
            assert dimension not in book.observation()['spent']
        assert book.observation()['live']==before_live
        observation=sample_coordinator(book,owner)
        refused(lambda:copy.copy(observation),'CapabilityNotCopyable')
        identical=object.__new__(LiveObservation)
        for slot in LiveObservation.__slots__:setattr(identical,slot,getattr(observation,slot))
        refused(lambda:book.record_live(identical),'InvalidLiveObservation')
        refused(lambda:book.record_live(object.__new__(LiveObservation)),'InvalidLiveObservation')
        book.record_live(observation)
        refused(lambda:book.record_live(observation),'InvalidLiveObservation')
        foreign_root=root+'-foreign'
        provision_test_store(policy,foreign_root,'wp68-v1')
        foreign_issuer=TestIssuer()
        foreign_book=foreign_issuer.activate(foreign_issuer.issue(foreign_issuer.reserve(
            policy,foreign_root,'wp68-v1','foreign-live','TEST-foreign',foreign_root+'-ledger')))
        foreign_owner=foreign_issuer
        foreign_observation=sample_coordinator(foreign_book,foreign_owner)
        refused(lambda:book.record_live(foreign_observation),'InvalidLiveObservation')
        foreign_book.record_live(foreign_observation)
        refused(lambda:foreign_book.reserve_phase('audit',foreign_owner,dict(source_io=DIMENSIONS['source_io'])),'LeafBudget')
        foreign_issuer.finish(foreign_book)
        stale=sample_coordinator(book,owner)
        time.sleep(2.01)
        refused(lambda:book.record_live(stale),'ExpiredLiveObservation')
        refused(lambda:book.reserve_phase('audit',owner,dict(work=1)),'ExpiredLiveObservation')
    elif case == 'expired-operation':
        activate()
        p = book.reserve_ledger_operation('acquire-parent', book.parent_path,
                    OperationLimits(duration_ns=1,fds=4))
        refused(lambda: ParentLease.acquire(book.parent_path, p))
    elif case == 'parent-symlink':
        deep_root=root+'-depth'
        provision_test_store(policy,deep_root,'wp68-v1')
        deep_parent=Path(deep_root+'-ledger');deep_parent.mkdir()
        for _ in range(30):deep_parent=deep_parent/'d';deep_parent.mkdir()
        deep_issuer=TestIssuer()
        deep_book=deep_issuer.activate(deep_issuer.issue(deep_issuer.reserve(policy,deep_root,'wp68-v1','max-depth','TEST-depth',str(deep_parent))))
        deep_cap=ParentLease.acquire(str(deep_parent),deep_book.reserve_ledger_operation('acquire-parent',str(deep_parent),OperationLimits(fds=33)))
        deep_ledger=OwnedLedger.create(deep_cap,deep_book.basename,deep_book.reserve_ledger_operation('create-ledger',(deep_cap,deep_book.basename),OperationLimits(fds=1)))
        dp=deep_book.reserve_ledger_operation('update-record',deep_ledger,OperationLimits(syscalls=1024,work=262144,io=16385))
        deep_ledger.write_json(deep_book.record('COMPLETE',{},dp),dp)
        assert deep_cap.close_requirements().syscalls==66
        deep_ledger.close(deep_book.reserve_ledger_operation('cleanup-close',deep_ledger,deep_ledger.close_requirements()))
        deep_cap.close(deep_book.reserve_ledger_operation('cleanup-close',deep_cap,deep_cap.close_requirements()))
        deep_issuer.finish(deep_book)
        assert deep_book.observation()['closed'] is True and deep_book.observation()['live']['peak']['fds']<=64
        activate()
        os.rename(book.parent_path, book.parent_path+'-original')
        os.symlink(book.parent_path+'-original', book.parent_path)
        refused(lambda: ParentLease.acquire(book.parent_path, book.reserve_ledger_operation(
                    'acquire-parent', book.parent_path, OperationLimits(fds=4))))
    elif case == 'stable-id-different-binding':
        activate()
        if book in issuer._stores:
            issuer.finish(book)
            assert book.observation()['closed'] is True
            refused(lambda: book.reserve_phase('audit',issuer,dict(work=1)),'AccountClosed')
        book = None
        policy.plan_hash = 'f'*64
        other = TestIssuer()
        changed = other.reserve(policy,root,'wp68-v1','api-'+case,'DIFFERENT-leaf',root+'-ledger')
        refused(lambda: other.issue(changed), 'FilesystemFailure')
    else:
        make_ledger()
        path = Path(book.parent_path)/book.basename
        if case == 'consumed-permit':
            p = update()
            record = book.record('AUTHORIZED', {}, p)
            ledger.write_json(record, p)
            before_data=path.read_bytes();before_ctime=path.stat().st_ctime_ns
            try:
                ledger.write_json(record,p)
            except Refusal as exc:
                if exc.code!='InvalidPermit':raise AssertionError('ONE_USE_BOUNDARY:'+exc.code)
            else:raise AssertionError('ONE_USE_ACCEPTED')
            assert path.read_bytes()==before_data and path.stat().st_ctime_ns==before_ctime
        elif case == 'ancestor-retarget':
            os.rename(book.parent_path, book.parent_path+'-original')
            os.mkdir(book.parent_path, 0o700)
            p = update()
            refused(lambda: ledger.write_json(book.record('AUTHORIZED', {}, p), p), 'ParentRetargeted')
            assert not list(Path(book.parent_path).iterdir())
        elif case == 'foreign-ledger':
            os.rename(path, str(path)+'.original')
            path.write_bytes(b'FOREIGN')
            p = update()
            refused(lambda: ledger.write_json(book.record('AUTHORIZED', {}, p), p), 'LedgerIdentity')
            assert path.read_bytes() == b'FOREIGN'
        elif case == 'linked-ledger':
            os.link(path, str(path)+'.linked')
            p = update()
            refused(lambda: ledger.write_json(book.record('AUTHORIZED', {}, p), p), 'LedgerIdentity')
            assert path.read_bytes() == b''
        elif case == 'fd-reuse':
            fd = ledger._fd  # Observational adversarial OS manipulation, no grant.
            os.close(fd)
            replacement = os.open(str(path)+'.foreign', os.O_CREAT|os.O_EXCL|os.O_RDWR, 0o600)
            assert replacement == fd
            refused(lambda: ledger.close(book.reserve_ledger_operation('cleanup-close',ledger,
                    ledger.close_requirements())), 'ForeignDescriptor')
            os.write(replacement, b'STILL-OWNED-BY-TEST')
            os.close(replacement)
            ledger = None
            store=issuer._stores[book]
            spent_fd=store._files[-1][0]
            os.close(spent_fd)
            foreign_path=Path(book.parent_path)/'foreign-store-fd'
            foreign_fd=os.open(foreign_path,os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600)
            assert foreign_fd==spent_fd
            refused(lambda: issuer.finish(book),'CleanupIncomplete')
            assert book.observation()['fault']=='CleanupIncomplete'
            refused(lambda: book.reserve_phase('audit',issuer,dict(work=1)),'CleanupIncomplete')
            os.write(foreign_fd,b'NOT-CLOSED-BY-ISSUER')
            os.close(foreign_fd)
        else:
            p = update()
            record = book.record('AUTHORIZED', {}, p)
            peak = None
            if case == 'canonical-json':
                record['facts'] = dict(unicode='\u00e9\U0001f642', values=[None,False,True,-2**63,2**63-1], controls='\n\t\x00')
                ledger.write_json(record,p)
                expected=(json.dumps(record,ensure_ascii=True,indent=2)+'\n').encode('ascii')
                assert path.read_bytes()==expected
            else:
                facts = record['facts']
                if case == 'float-finite': facts['value']=1.5
                elif case == 'float-nan': facts['value']=float('nan')
                elif case == 'float-infinite': facts['value']=float('inf')
                elif case == 'oversized-integer': facts['value']=1<<1000000
                elif case == 'boolean-sequence': record['sequence']=True
                elif case == 'surrogate': facts['value']='\ud800'
                elif case == 'repeated-alias':
                    a=[]; facts['value']=[a,a]
                elif case == 'cycle': facts['value']=facts
                elif case == 'depth':
                    a=[]; facts['value']=a
                    for _ in range(10): b=[]; a.append(b); a=b
                elif case == 'huge-container': facts['value']=[None]*257
                elif case == 'huge-string': facts['value']='x'*1000000
                elif case == 'encoded-bound': facts['value']='\U0001f642'*1024
                elif case == 'custom-hooks-and-types':
                    class Hook:
                        def __iter__(self): raise AssertionError('hook called')
                        def __str__(self): raise AssertionError('hook called')
                        def __repr__(self): raise AssertionError('hook called')
                    facts['value']=Hook()
                else: raise AssertionError('unknown case '+case)
                if case=='huge-string': tracemalloc.start()
                reason=refused(lambda: ledger.write_json(record,p))
                if case=='huge-string':
                    _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
                    assert peak < 131072, peak
                assert path.read_bytes()==b''
                print(json.dumps(dict(reason=reason,peak_bytes=peak)))
    print(json.dumps(dict(case=case,status='PASS')))
finally:
    if book is not None:
        for resource in (ledger,parent):
            if resource is not None:
                try:
                    resource.close(book.reserve_ledger_operation('cleanup-close',resource,
                          resource.close_requirements()))
                except (Refusal,OSError): pass
        if book in issuer._stores:
            issuer.finish(book)
            assert book.observation()['closed'] is True
            refused(lambda: book.reserve_phase('audit',issuer,dict(work=1)),'AccountClosed')
