"""Bounded ordinary runtime preparation; no grants, Session, fixture execution or TEST leaves.

This coordinator is not execution authorization. ROOT must grant the exact frozen
source/manifest/argv before --prepare. Observations never extend expected inputs.
"""
import argparse
import ast
import base64
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import selectors
import signal
import socket
import stat
import struct
import subprocess
import sys
import time
import zlib

BASE = Path('/home/lynn/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12')
PREFIX = BASE.parent.parent
TARGET = Path('/tmp/wordling-WP70-codex312-qualified-runtime-v14')
FREEZE = Path('/tmp/wordling-WP70-runtime-qualification-source-freeze-v19')
CAMPAIGN_FREEZE = Path('/tmp/wordling-WP70-controller-capture-lifetime-source-freeze-r4')
CAMPAIGN_ADMISSION = Path('/tmp/wordling-WP70-controller-capture-lifetime-finalizer-r4/admission.json')
CAMPAIGN_CARRIER = dict(size=24494,sha256='6aaae4d7a6bbe9b2380a5ddb82c0348a960043e12988b8eb6a0a7fe1d2be15e4',mode=384,uid=1000,gid=1000)
_R5_FREEZE = Path('/tmp/wordling-WP70-controller-provider-reap-source-freeze-r5b')
_R5_ADMISSION = Path('/tmp/wordling-WP70-controller-provider-reap-carrier-r5b/admission.json')
_R5_CARRIER = dict(size=32241,sha256='4b4a935269e30cfec5c3446b9e28ba77844cce5d0c1bb32ec58d801cad3d7975',mode=384,uid=1000,gid=1000)
_R5_TARGET=Path('/tmp/wordling-WP70-codex312-qualified-runtime-v15/runtime')
_R5_PROVIDER=Path(__file__).resolve().parents[5]/'scripts/reference/startup_family/lifetime.py'
_R5_COMMIT='7869159b5d8e3ab1e26ec3e4dae2313264deb6f0'
_R11_FREEZE=Path('/tmp/wordling-WP70-campaign-settlement-source-freeze-r19')
_R11_ADMISSION=Path('/tmp/wordling-WP70-campaign-settlement-carrier-r19/admission.json')
_R11_CARRIER={'size': 11701, 'sha256': '0bcdcd92b0f33a7c3945eb7ac13085e32dd7b7f36fea603d16d021c39f453197', 'mode': 384, 'uid': 1000, 'gid': 1000}
_R11_TARGET=Path('/tmp/wordling-WP70-codex312-qualified-runtime-v17/runtime')
CAMPAIGN_MUTANTS={
 'first-read-guard':('protocol.py','self._stream = _Stream(value, self.socket, self.audit)','self._stream = value','long-line','PROHIBITED_LEAF_COMPLETED'),
 'causal-owner':('protocol.py','dict(pid=identity.pid, startticks=identity.startticks, socket=self.path)','dict(pid=os.getpid(), startticks=identity.startticks, socket=self.path)','healthy','PUBLIC_FULL_LEAF_NOT_COMPLETE'),
 'copied-stop-facts':('controller.py','        self._stopped=stopped','        self._stopped=exited','healthy','PUBLIC_FULL_LEAF_NOT_COMPLETE'),
 'lost-held-stop':('controller.py','        self._stopped=stopped','        self._stopped=None','healthy','PUBLIC_FULL_LEAF_NOT_COMPLETE'),
 'wire-book-reset':('controller.py','        self._last_usage=u',"        self._book._spent['wire_bytes']=0\n        self._last_usage=u",'healthy','CUMULATIVE_WIRE_RESET'),
 'publication-authority':('publisher.py','        artifact = batch.artifacts[self.index]','        artifact = batch.outputs[self.index]','healthy','PUBLIC_FULL_LEAF_NOT_COMPLETE'),
 'output-commit':('publisher.py','        _call(self.meter,self,os.fsync,self.fd)\n        self.validate()\n        _call(self.meter,self,os.fsync,self.parent._chain[-1][0])','        self.validate()','kernel-publication-fsync','OUTPUT_COMMIT_RELEASED'),
 'release-before-audit':('controller.py','            self._physical.release()','            pass  # MUTANT: physical lock held until terminal close','release-order','ACTUAL_RELEASE_BEFORE_AUDIT')}
CAMPAIGN_CONFIGURED=(('inventory',['/usr/bin/python','-B','scripts/render-inventory.py','--check']),('scenarios',['/usr/bin/python','-B','scripts/render-scenarios.py','--check']),('review-adapter',['/usr/bin/python','-B','-m','unittest','discover','-s','scripts','-p','test_review_checks.py']))
E_FILES=('__init__.py','__main__.py','bootstrap.py','errors.py','account.py','ownership.py',
         'records.py','issuance.py','cli.py','controller.py','protocol.py','publisher.py')
PROVIDERS={
 'startup_transport.py':('scripts/reference/startup_transport.py','eba8382f5101bfa464d4c30e19ea5183f3bb6469'),
 'startup_family/__init__.py':('scripts/reference/startup_family/__init__.py','eba8382f5101bfa464d4c30e19ea5183f3bb6469'),
 'startup_family/artifacts.py':('scripts/reference/startup_family/artifacts.py','eba8382f5101bfa464d4c30e19ea5183f3bb6469'),
 'startup_family/engine.py':('scripts/reference/startup_family/engine.py','eba8382f5101bfa464d4c30e19ea5183f3bb6469'),
 'startup_family/lifetime.py':('scripts/reference/startup_family/lifetime.py','eba8382f5101bfa464d4c30e19ea5183f3bb6469'),
 'peer.py':('internal/document/evidence/retrieve-field-observations/peer.py','e7e59b3e1fbb757014de1789c03f72ed45efec45'),
 'boundaries.py':('internal/document/evidence/retrieve-field-observations/boundaries.py','e7e59b3e1fbb757014de1789c03f72ed45efec45'),
 'qmp.py':('scripts/reference/qmp.py','18d6afe95ffcd676fc3f9e964dcad884c9a8c289')}
SOURCE_NAMES=tuple('reference_controller/'+n for n in E_FILES)+tuple(PROVIDERS)

STDLIB = ('argparse','ast','collections','contextlib','copy','dataclasses','errno',
    'fcntl','functools','hashlib','importlib','importlib.util','json','math','os',
    'pathlib','resource','select','selectors','shutil','signal','socket','stat','struct',
    'subprocess','sys','tempfile','threading','time','types','typing','uuid')
FEATURES = ('pidfd_open','P_PIDFD','fork','pipe2','waitid','waitpid','P_PID',
    'WEXITED','WNOHANG','WNOWAIT','CLD_EXITED','O_NOFOLLOW','O_CLOEXEC','O_DIRECTORY')
QUALIFY_LITERAL = '# STATIC REVIEW INPUT ONLY. Pass this literal source via -I -B -c AFTER ROOT grant.\nimport sys, os, json, pathlib, hashlib, stat, site, resource, socket, select, fcntl, dataclasses, typing, argparse, time, inspect, subprocess, struct, signal\nV=pathlib.Path("/tmp/wordling-WP70-codex312-qualified-runtime-v14/venv")\nB=pathlib.Path("/home/lynn/.cache/codex-runtimes/codex-primary-runtime/dependencies/python")\nassert sys.version_info[:3]==(3,12,14)\nassert pathlib.Path(sys.prefix)==V and pathlib.Path(sys.exec_prefix)==V\nassert pathlib.Path(sys.base_prefix)==B and pathlib.Path(sys.base_exec_prefix)==B\nassert pathlib.Path(sys.executable).parent==V/\'bin\'\nassert not pathlib.Path(sys.executable).is_symlink()\nassert sys.flags.isolated and sys.flags.no_user_site and sys.flags.ignore_environment and sys.flags.dont_write_bytecode\nassert sys.excepthook is sys.__excepthook__\nassert not any(x in sys.modules for x in (\'sitecustomize\',\'usercustomize\',\'_distutils_hack\'))\nassert not site.ENABLE_USER_SITE\ncfg=(V/\'pyvenv.cfg\').read_text()\nassert \'include-system-site-packages = false\' in cfg.lower()\nS=V/\'lib/python3.12/site-packages\'\nassert S.is_dir()\nfor p in V.rglob(\'*\'):\n if p.is_symlink():\n  assert p==V/\'lib64\' and p.resolve()==V/\'lib\'\n if p.is_file() and (p.name.endswith((\'.pyc\',\'.pth\',\'._pth\')) or p.name==\'__pycache__\'):\n  raise AssertionError(\'unexpected venv cache/customization \'+str(p))\nfor x in sys.path:\n p=pathlib.Path(x)\n assert p.is_absolute()\n assert x in (str(B/\'lib/python312.zip\'),str(B/\'lib/python3.12\'),str(B/\'lib/python3.12/lib-dynload\'),str(S))\nfeatures={n:hasattr(os,n) for n in (\'pidfd_open\',\'P_PIDFD\',\'waitid\',\'fork\',\'pipe2\',\'WNOWAIT\',\'P_PID\',\'WEXITED\',\'WNOHANG\',\'CLD_EXITED\')}\nassert all(features.values())\nfd=os.pidfd_open(os.getpid())\ntry: assert fd>=0\nfinally: os.close(fd)\norigins={}\nfor name,m in tuple(sys.modules.items()):\n for attr in (\'__file__\',\'__cached__\'):\n  value=getattr(m,attr,None)\n  if value and not value.startswith(\'<\'):\n   p=pathlib.Path(value).resolve()\n   assert p.is_relative_to(B/\'lib/python3.12\') and not p.is_relative_to(B/\'lib/python3.12/site-packages\'),(name,value)\n   if p.is_file(): origins[str(p)]={\'bytes\':p.stat().st_size,\'sha256\':hashlib.sha256(p.read_bytes()).hexdigest()}\nmaps={}\nfor line in pathlib.Path(\'/proc/self/maps\').read_text().splitlines():\n a=line.split(maxsplit=5)\n if len(a)==6 and a[5].startswith(\'/\'):\n  p=pathlib.Path(a[5]).resolve()\n  if p.is_file(): maps[str(p)]={\'bytes\':p.stat().st_size,\'sha256\':hashlib.sha256(p.read_bytes()).hexdigest()}\nprint(json.dumps(dict(version=sys.version,executable=sys.executable,prefix=sys.prefix,base_prefix=sys.base_prefix,flags=str(sys.flags),pyvenv=cfg,sys_path=sys.path,features=features,self_pidfd=\'OPEN/CLOSE ONLY OWN SELF: success\',module_origins=origins,mapped_files=maps)))\n'

_PROBE_COMMON = '''import sys,os,json,pathlib,hashlib,stat,importlib
for name in STDLIB: importlib.import_module(name)
features={n:hasattr(os,n) for n in FEATURES}
features.update({'socket.'+n:hasattr(importlib.import_module('socket'),n) for n in ('AF_UNIX','SOL_SOCKET','SO_PEERCRED','SO_ERROR')})
features.update({'select.'+n:hasattr(importlib.import_module('select'),n) for n in ('poll','POLLHUP','POLLERR')})
assert all(features.values()),features
fd=os.pidfd_open(os.getpid())
try: assert fd>=0
finally: os.close(fd)
'''
_PROBE_OBSERVE = '''
flag_names=('debug','inspect','interactive','optimize','dont_write_bytecode','no_user_site','no_site','ignore_environment','verbose','bytes_warning','quiet','hash_randomization','isolated','dev_mode','utf8_mode','warn_default_encoding','safe_path','int_max_str_digits')
origins={}
for name,m in tuple(sys.modules.items()):
 fields={}
 for key in ('__file__','__cached__'):
  value=getattr(m,key,None)
  if value and not value.startswith('<'):
   p=pathlib.Path(value).resolve()
   fields[key]={'path':str(p),'exists':p.is_file()}
   if p.is_file():fields[key].update(size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 if fields:origins[name]=fields
maps={}
for line in pathlib.Path('/proc/self/maps').read_text().splitlines():
 a=line.split(maxsplit=5)
 if len(a)==6 and a[5].startswith('/'):
  p=pathlib.Path(a[5]).resolve()
  if p.is_file():maps[str(p)]={'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
print(json.dumps(dict(version=list(sys.version_info[:3]),version_string=sys.version,executable=sys.executable,prefix=sys.prefix,exec_prefix=sys.exec_prefix,base_prefix=sys.base_prefix,base_exec_prefix=sys.base_exec_prefix,
 flags={n:getattr(sys.flags,n) for n in flag_names},default_excepthook=sys.excepthook is sys.__excepthook__,
 customize={n:n in sys.modules for n in ('sitecustomize','usercustomize','_distutils_hack')},sys_path=list(sys.path),features=features,modules=origins,maps=maps,project=project)))
'''
_PROJECT = '''
from reference_controller.bootstrap import load_policy,validate_provider,SOURCE_FILES
s=load_policy();p=validate_provider(s)
import reference_controller.controller,reference_controller.protocol,reference_controller.publisher
import reference_controller.account,reference_controller.ownership,reference_controller.records
import reference_controller.issuance,reference_controller.cli,peer,boundaries,qmp
classes={n:dict(module=getattr(p,n).__module__,origin=sys.modules[getattr(p,n).__module__].__file__) for n in ('Session','ProcessLease','SharedEnvelopePolicy','DerivationSpec','DerivedArtifactLease','ArtifactChunk')}
project=dict(source_files=list(SOURCE_FILES),provider=p.source_binding(),classes=classes,aliases=sorted(n for n in sys.modules if n=='wordling_reference_startup_v1' or n.startswith('wordling_reference_startup_v1.')))
'''

def probe(project=False):
    return ('STDLIB='+repr(STDLIB)+'\nFEATURES='+repr(FEATURES)+'\n'+
            _PROBE_COMMON+(_PROJECT if project else 'project=None\n')+_PROBE_OBSERVE)


TRACE_SURFACE='open,openat,openat2,execve,execveat,chdir,fchdir,clone,clone3,fork,vfork,setsid,setpgid,memfd_create'

# Prospective WP70 amendment: construction-only raw bound and fixed evidence classes.
CONSTRUCTION_RAW_LIMIT=4194304
EVIDENCE_LIMIT=4294967296
EVIDENCE_FILES=10240
JSON_CHUNK=16384
JSON_ESCAPE_PEAK=12*16384+2  # ensure_ascii=True, non-BMP surrogate pairs.
OWNED_MEMORY_LIMIT=167772160
CLASS_LIMITS={
 'construction_raw':(402653184,288),'functional_raw':(115343360,238),
 'pair':(28180480,430),'origin':(805306368,48),'transient':(50331648,48),
 'inventory':(50331648,12),'deployment':(3145728,12),'build':(3145728,12),
 'compiled':(196608,12),'custody':(12582912,120),'aggregate':(16777216,2),
 'misc':(2097152,16),'input':(2097152,16),'catalog':(159383552,3328),
 'review':(37748736,1344),'control':(4194304,135),'failure':(136314880,445)}
# Legacy/default class limits above remain exact; only fixed R4 campaign
# writers use these adopted funded limits and irrecoverable old held charges.
R4_CLASS_LIMITS={**CLASS_LIMITS,'catalog':(184549376,3456),'review':(41943040,1408),
 'control':(4194304,167),'misc':(3538944,20),'custody':(12910592,124),
 'aggregate':(33554432,4)}
R4_BLOCKED_HOLDS={'misc':(1441792,4),'custody':(327680,4),'aggregate':(16777216,2)}
R5_CLASS_LIMITS={**R4_CLASS_LIMITS,'catalog':(189546496,3478),'review':(41943040,1440),'control':(4194304,183),
 'functional_raw':(117440512,242),'aggregate':(50331648,6),'misc':(4718592,20)}
R5_HELD={'misc':(2949120,9),'custody':(819200,12),'aggregate':(33554432,4),'functional_raw':(2097152,4),
 'pair':(1310720,20),'construction_raw':(33554432,24),'origin':(67108864,4),'transient':(4194304,4),
 'inventory':(4194304,1),'deployment':(262144,1),'build':(262144,1),'compiled':(16384,1)}

# R11 active profile plus R12/R13 metadata allocations. Historical tables above
# remain literal; every old unused campaign tail stays in this full held book.
R11_LIVE_SOURCE_GROWTH=160097  # zero files, from ROOT-ratified remaining held bytes
R11_CLASS_LIMITS={'construction_raw': (771751936, 552), 'functional_raw': (232783872, 480), 'pair': (55312384, 844), 'origin': (1543503872, 92), 'transient': (96468992, 92), 'inventory': (96468992, 23), 'deployment': (6029312, 23), 'build': (6029312, 23), 'compiled': (376832, 23), 'custody': (13434880, 132), 'aggregate': (67108864, 8), 'misc': (6291520, 27), 'input': (2097152, 16), 'catalog': (271286272, 3873), 'review': (50855936, 1559), 'control': (4644864, 198), 'failure': (144703488, 573)}
R11_HELD={'construction_raw': (436207616, 312), 'functional_raw': (117440512, 242), 'pair': (29229056, 446), 'origin': (872415232, 52), 'transient': (54525952, 52), 'inventory': (54525952, 13), 'deployment': (3407872, 13), 'build': (3407872, 13), 'compiled': (212992, 13), 'custody': (13107200, 128), 'aggregate': (50331648, 6), 'misc': (4784128, 21), 'input': (2097152, 16), 'catalog': (271286272, 3873), 'review': (50855936, 1559), 'control': (4644864, 198), 'failure': (144703488, 573)}
R14_CLASS_LIMITS={'construction_raw': (805306368, 576), 'functional_raw': (232783872, 480), 'pair': (56360960, 860), 'origin': (1610612736, 96), 'transient': (100663296, 96), 'inventory': (100663296, 24), 'deployment': (6291456, 24), 'build': (6291456, 24), 'compiled': (393216, 24), 'custody': (13434880, 132), 'aggregate': (67108864, 8), 'misc': (6357056, 28), 'input': (2097152, 16), 'catalog': (299024384, 3934), 'review': (51642368, 1583), 'control': (4644864, 198), 'failure': (144703488, 573)}
R14_HELD={'construction_raw': (469762048, 336), 'functional_raw': (117440512, 242), 'pair': (30277632, 462), 'origin': (939524096, 56), 'transient': (58720256, 56), 'inventory': (58720256, 14), 'deployment': (3670016, 14), 'build': (3670016, 14), 'compiled': (229376, 14), 'custody': (13107200, 128), 'aggregate': (50331648, 6), 'misc': (4849664, 22), 'input': (2097152, 16), 'catalog': (299024384, 3934), 'review': (51642368, 1583), 'control': (4644864, 198), 'failure': (144703488, 573)}
# R16 active programme-only limits; all earlier/default tables remain literal.
R16_EVIDENCE_LIMIT=8589934592
R16_EVIDENCE_FILES=16384
R16_CLASS_LIMITS={'construction_raw': (1140850688, 816), 'functional_raw': (348127232, 718), 'pair': (82444288, 1258), 'origin': (2281701376, 136), 'transient': (142606336, 136), 'inventory': (142606336, 34), 'deployment': (8912896, 34), 'build': (8912896, 34), 'compiled': (557056, 34), 'custody': (13762560, 136), 'aggregate': (83886080, 10), 'misc': (7864448, 34), 'input': (2097152, 16), 'catalog': (338378755, 4123), 'review': (54788096, 1639), 'control': (4644864, 198), 'failure': (144703488, 573)}
R16_HELD={'construction_raw': (805306368, 576), 'functional_raw': (232783872, 480), 'pair': (56360960, 860), 'origin': (1610612736, 96), 'transient': (100663296, 96), 'inventory': (100663296, 24), 'deployment': (6291456, 24), 'build': (6291456, 24), 'compiled': (393216, 24), 'custody': (13434880, 132), 'aggregate': (67108864, 8), 'misc': (6357056, 28), 'input': (2097152, 16), 'catalog': (338378755, 4123), 'review': (54788096, 1639), 'control': (4644864, 198), 'failure': (144703488, 573)}
DOCUMENT_LIMITS={'pair':65536,'origin':16777216,'transient':1048576,
 'inventory':4194304,'deployment':262144,'build':262144,'compiled':16384,
 'custody':65536,'aggregate':8388608,'misc':1048576,'input':1572864,
 'catalog':524288,'review':16777216,'control':1048576,'failure':65536}
_ACTIVE_BUDGET=None
_CAMPAIGN_CURRENT=None


def _actual_campaign(value):
    return value is not None and value is _CAMPAIGN_CURRENT and type(value) is _CampaignAdmission


def current_campaign():
    if not _actual_campaign(_CAMPAIGN_CURRENT):raise RuntimeError('ActualCampaignBootstrapRequired')
    if _CAMPAIGN_CURRENT.aborted:raise RuntimeError('CampaignAbortedNoFurtherEffects')
    return _CAMPAIGN_CURRENT


def generated_diagnostic(error,maximum=4096):
    """Bounded GENERATION: never formats a traceback or arbitrary exception."""
    if type(maximum) is not int or not 256<=maximum<=8192:raise RuntimeError('DiagnosticEarlierBound')
    marker=b' [OMITTED; original traceback UNKNOWN]'
    name=type(error).__name__;name_bytes=bytearray();name_omitted=False
    for char in name:
        piece=char.encode('utf8','backslashreplace')
        if len(name_bytes)+len(piece)>128:name_omitted=True;break
        name_bytes.extend(piece)
    prefix=b'GENERATED_DIAGNOSTIC '+bytes(name_bytes)+b'; original_traceback=UNKNOWN; message='
    available=maximum-len(prefix)-len(marker)
    if available<0:raise RuntimeError('DiagnosticHeaderBound')
    args=BaseException.args.__get__(error)
    known=type(args) is tuple and len(args)==1 and type(args[0]) is str
    message=args[0] if known else 'DETAIL_UNKNOWN_NONSTRING_OR_MULTIPLE_ARGS'
    body=bytearray();omitted=name_omitted or not known;consumed=0
    for char in message:
        number=ord(char)
        piece=('\\u%04x'%number).encode('ascii') if number<32 or number==127 else char.encode('utf8','backslashreplace')
        if len(body)+len(piece)>available:omitted=True;break
        body.extend(piece);consumed+=1
    result=prefix+bytes(body)+(marker if omitted else b'')
    if len(result)>maximum:raise RuntimeError('DiagnosticEncodedBound')
    return dict(text=result.decode('utf8'),bytes=len(result),omitted=omitted,original_traceback='UNKNOWN',kind='GENERATED_DIAGNOSTIC',content_capacity=available,source_characters_consumed=consumed)


def error_tag(error):
    return generated_diagnostic(error)['text']


def emit_diagnostic(error,fd=2,maximum=4096):
    diagnostic=generated_diagnostic(error,maximum);data=diagnostic['text'].encode('utf8');offset=0
    while offset<len(data):
        n=os.write(fd,data[offset:])
        if n<=0:break
        offset+=n
    return diagnostic


def immutable_metadata_ref(path,root):
    path=Path(path);root=Path(root)
    if not path.is_relative_to(root):raise RuntimeError('MetadataReferenceScope')
    return dict(path=str(path),relative=str(path.relative_to(root)),root=str(root),**pin(path),**rights(path),membership='exact source-owned write-once stage whole; full actual closure inventoried externally')


def _text_bound(value,maximum=16384):
    if type(value) is not str or len(value)>maximum:raise RuntimeError('MetadataStringBound')
    if any(0xd800<=ord(c)<=0xdfff for c in value):raise RuntimeError('MetadataLoneSurrogate')
    return value


def _json_parts(value,depth=0):
    # No arbitrary repr/default hooks; every emitted scalar has a preallocation bound.
    if depth>16:raise RuntimeError('MetadataDepthBound')
    if value is None:yield 'null'
    elif value is True:yield 'true'
    elif value is False:yield 'false'
    elif type(value) is int:
        if value.bit_length()>64:raise RuntimeError('MetadataIntegerBound')
        yield str(value)
    elif type(value) is float:
        if not math.isfinite(value):raise RuntimeError('MetadataNonfinite')
        yield repr(value)
    elif type(value) is str:
        _text_bound(value)
        encoded=json.encoder.encode_basestring_ascii(value)
        if len(encoded)>JSON_ESCAPE_PEAK:raise RuntimeError('MetadataEscapeBound')
        for i in range(0,len(encoded),JSON_CHUNK):yield encoded[i:i+JSON_CHUNK]
    elif type(value) in (list,tuple):
        if len(value)>32768:raise RuntimeError('MetadataCardinalityBound')
        yield '['
        for i,item in enumerate(value):
            if i:yield ','
            yield from _json_parts(item,depth+1)
        yield ']'
    elif type(value) is dict:
        if len(value)>32768:raise RuntimeError('MetadataCardinalityBound')
        yield '{'
        for i,(key,item) in enumerate(value.items()):
            if type(key) is not str:raise RuntimeError('MetadataKeyType')
            if i:yield ','
            yield from _json_parts(key,depth+1);yield ':'
            yield from _json_parts(item,depth+1)
        yield '}'
    else:raise RuntimeError('MetadataType')


def _json_prepared(raw,maximum=1048576,expected=False):
    if type(raw) is bytes:
        if len(raw)>maximum:raise RuntimeError('JSONInputBound')
        text=raw.decode('utf8')
    elif type(raw) is str:
        if len(raw)>maximum or len(raw.encode('utf8'))>maximum:raise RuntimeError('JSONInputBound')
        text=raw
    else:raise RuntimeError('JSONInputType')
    depth=0;tokens=0;nodes=0;quoted=False;escape=False;string_size=0;atom=False;atom_size=0;stack=[]
    token_limit=2097152 if expected else 65536;node_limit=524288 if expected else 65536
    for char in text:
        if quoted:
            string_size+=1
            if string_size>8192:raise RuntimeError('JSONStringBound')
            if escape:escape=False
            elif char=='\\':escape=True
            elif char=='"':quoted=False
            continue
        if char=='"':quoted=True;string_size=0;tokens+=1;nodes+=1;atom=False
        elif char in '{[':depth+=1;tokens+=1;nodes+=1;stack.append([char,0]);atom=False
        elif char in '}]':
            depth-=1;tokens+=1;atom=False
            if not stack:raise RuntimeError('JSONDepthBound')
            stack.pop()
        elif char in ',:':
            tokens+=1;atom=False
            if char==':' and stack:
                stack[-1][1]+=1
                if stack[-1][1]>(32768 if expected else 4096):raise RuntimeError('JSONMemberBound')
        elif char.isspace():atom=False
        else:
            if not atom:nodes+=1;tokens+=1;atom=True;atom_size=0
            atom_size+=1
            if atom_size>32:raise RuntimeError('JSONScalarBound')
        if depth>16 or depth<0:raise RuntimeError('JSONDepthBound')
        if tokens>token_limit:raise RuntimeError('JSONTokenBound')
        if nodes>node_limit:raise RuntimeError('JSONNodeBound')
    if quoted or depth:raise RuntimeError('JSONIncomplete')
    if expected and (not text.isascii() or '\\u' in text):raise RuntimeError('ExpectedMetadataAsciiShape')
    charge=len(text)*(2 if expected else 8)+nodes*96
    if charge>(46137344 if expected else 8388608):raise RuntimeError('JSONPreparedMemoryCharge')
    return text,charge


def bounded_json_loads(raw,maximum=1048576,expected=False):
    text,charge=_json_prepared(raw,maximum,expected)
    return json.loads(text,parse_constant=lambda s:(_ for _ in ()).throw(RuntimeError('JSONNonfinite')))


def bounded_gzip(path,maximum=8388608):
    result=bytearray()
    with gzip.open(path,'rb') as stream:
        while True:
            piece=stream.read(min(16384,maximum-len(result)+1))
            if not piece:break
            if len(result)+len(piece)>maximum:raise RuntimeError('MetadataExpansionBound')
            result.extend(piece)
    return bytes(result)


def _document_class(path):
    n=Path(path).name
    if n.endswith(('.command.json','.whole.json')):return 'pair'
    if n.endswith('.origins.json'):return 'origin'
    if n.endswith('.transient-data.json'):return 'transient'
    table={'deployment-inventory.json':'inventory','deployment.json':'deployment',
      'build-freeze.json':'build','compiled-data-before-wheel.json':'compiled',
      'functional-results.json':'aggregate','mutant-results.json':'aggregate',
      'frozen-input.json':'misc','runtime-before-first-P.json':'misc',
      'configured-results.json':'misc','whole.json':'misc','coordinator.stderr':'misc'}
    if n not in table:raise RuntimeError('UnclassifiedEvidenceWriter:'+n)
    return table[n]


def measure_json(value,maximum):
    encoded=0;nodes=0
    for part in _json_parts(value):
        nodes+=1;encoded+=len(part)
        if nodes>1048576 or encoded+1>maximum:raise RuntimeError('MetadataEncodedBound')
    return encoded


class EvidenceBudget:
    """Narrow fixed-source evidence allocation, never product/issuer authority."""
    def __init__(self,roots,baseline_bytes=0,baseline_files=0,earlier_document_cap=None,campaign=None,qualification=None):
        if earlier_document_cap is not None and (type(earlier_document_cap) is not int or not 0<earlier_document_cap<=65536):raise RuntimeError('EarlierMetadataLimitOnly')
        self.earlier_document_cap=earlier_document_cap
        self.roots=tuple(Path(p).absolute() for p in roots)
        self.base_bytes=baseline_bytes;self.base_files=baseline_files
        self.classes={k:[0,0] for k in CLASS_LIMITS};self.slots={};self.groups={}
        self._campaign_book=None;self._qualification_book=None
        if qualification is not None:
            if campaign is not None or not _actual_cold_r11(qualification):raise RuntimeError('R11QualificationBudgetIdentity')
            qualification.install(self)
            self._qualification_book=qualification
        if campaign is not None:
            if not _actual_campaign(campaign) or self.roots!=(Path(campaign.descriptor['evidence']).absolute(),):raise RuntimeError('CampaignBudgetConstructor')
            self._campaign_book=_CampaignBook(campaign,campaign.role)
            self._campaign_book.install(self)
    def _path(self,path):
        p=Path(path).absolute()
        if '..' in p.parts or not any(p.is_relative_to(r) for r in self.roots):raise RuntimeError('EvidencePathScope')
        return p
    def reserve(self,paths,kind,maximum):
        paths=tuple(self._path(p) for p in paths)
        if self._campaign_book is not None:return self._campaign_book.claim(paths,kind,maximum)
        if self._qualification_book is not None:return self._qualification_book.claim(self,paths,kind,maximum)
        if kind not in CLASS_LIMITS or type(maximum) is not int or maximum<0:raise RuntimeError('EvidenceReservation')
        if len(set(paths))!=len(paths) or any(p in self.slots for p in paths):raise RuntimeError('EvidenceNoClobberReservation')
        if _R5_REG_CURRENT is not None:return _r5_reg_module()._claim_owner(self,paths,kind,maximum)
        used=self.classes[kind];limits=CLASS_LIMITS[kind]
        if used[0]+maximum>limits[0] or used[1]+len(paths)>limits[1]:raise RuntimeError('EvidenceClassCapacity')
        if self.base_bytes+sum(v[0] for v in self.classes.values())+maximum>EVIDENCE_LIMIT or self.base_files+sum(v[1] for v in self.classes.values())+len(paths)>EVIDENCE_FILES:raise RuntimeError('EvidenceTotalCapacity')
        for p in paths:
            if p.exists() or p.is_symlink():raise RuntimeError('EvidenceNoClobber')
        group=dict(kind=kind,maximum=maximum,used=0,paths=paths)
        used[0]+=maximum;used[1]+=len(paths)
        for p in paths:self.slots[p]=group
        return group
    def document(self,path,value,kind=None,pre_reserved=False):
        p=self._path(path);kind=kind or _document_class(p);maximum=DOCUMENT_LIMITS[kind]
        if p.name in ('whole.json','configured-results.json'):maximum=min(maximum,65536)
        if p.name=='runtime-before-first-P.json':maximum=min(maximum,262144)
        if self.earlier_document_cap is not None:maximum=min(maximum,self.earlier_document_cap)
        encoded=measure_json(value,maximum)
        pre_reserved=pre_reserved or p in self.slots
        if pre_reserved:
            allocation=self.slots.get(p)
            if allocation is None or allocation['kind']!=kind or encoded+1>allocation['maximum']:raise RuntimeError('MissingMetadataReservation')
        else:allocation=self.reserve([p],kind,encoded+1)
        fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o644)
        written=0
        try:
            for part in _json_parts(value):
                data=part.encode('ascii')
                if written+len(data)+1>encoded+1:raise RuntimeError('MetadataChangedDuringEncode')
                offset=0
                while offset<len(data):
                    n=os.write(fd,data[offset:]);
                    if n<=0:raise RuntimeError('MetadataWriteProgress')
                    offset+=n
                written+=len(data)
            if written!=encoded:raise RuntimeError('MetadataChangedDuringEncode')
            if os.write(fd,b'\n')!=1:raise RuntimeError('MetadataWriteProgress')
            os.fsync(fd)
        finally:os.close(fd)
        allocation['used']+=written+1
        if self._campaign_book is not None:self._campaign_book.document_done(p)
    def raw_group(self,paths,kind,maximum,shared=None):
        if _R5_REG_CURRENT is not None and shared is not None:raise RuntimeError('FixedReviewOwnerNoSharedAugmentation')
        if self._campaign_book is not None:
            return self._campaign_book.raw(tuple(self._path(p) for p in paths),kind,maximum,shared)
        if shared is None or shared not in self.groups:
            allocation=self.reserve(paths,kind,maximum)
            if shared is not None:self.groups[shared]=allocation
        else:
            allocation=self.groups[shared]
            if allocation['kind']!=kind or allocation['maximum']!=maximum:raise RuntimeError('RawGroupChanged')
            extra=tuple(self._path(p) for p in paths)
            if any(p in self.slots or p.exists() or p.is_symlink() for p in extra):raise RuntimeError('EvidenceNoClobber')
            if self.classes[kind][1]+len(extra)>CLASS_LIMITS[kind][1] or self.base_files+sum(v[1] for v in self.classes.values())+len(extra)>EVIDENCE_FILES:raise RuntimeError('EvidenceFileCapacity')
            self.classes[kind][1]+=len(extra)
            allocation['paths']=extra
            for p in extra:self.slots[p]=allocation
        handles={}
        try:
            for p in allocation['paths']:handles[p]=open(p,'xb',buffering=0)
        except BaseException:
            for f in handles.values():f.close()
            raise
        return allocation,handles
    @staticmethod
    def retain(allocation,buffer,handle,raw):
        remaining=allocation['maximum']-allocation['used'];kept=raw[:remaining]
        allocation['used']+=len(kept)  # reserve BEFORE RAM and durable prefix.
        buffer.extend(kept)
        offset=0
        while offset<len(kept):
            n=handle.write(kept[offset:])
            if n is None or n<=0:raise RuntimeError('RawWriteProgress')
            offset+=n
        if len(raw)>remaining:raise RuntimeError('PreparationLiveOutputBound')


    def literal(self,path,data,kind='misc'):
        if type(data) is not bytes or len(data)>DOCUMENT_LIMITS[kind]:raise RuntimeError('LiteralEvidenceBound')
        allocation,handles=self.raw_group([path],kind,len(data))
        try:self.retain(allocation,bytearray(),next(iter(handles.values())),data)
        finally:
            for f in handles.values():f.close()


def evidence_budget(root=None):
    global _ACTIVE_BUDGET
    if _ACTIVE_BUDGET is None:
        if root is None:raise RuntimeError('EvidenceBudgetNotAdmitted')
        _ACTIVE_BUDGET=EvidenceBudget([Path(root)])
    elif root is not None and Path(root).absolute() not in _ACTIVE_BUDGET.roots:
        _ACTIVE_BUDGET.roots+= (Path(root).absolute(),)
    return _ACTIVE_BUDGET


def write_json(path,value,kind=None):
    evidence_budget().document(path,value,kind)


def _r5_historical_selection(expected):
    active=_actual_campaign(_CAMPAIGN_CURRENT)and expected is _CAMPAIGN_CURRENT.expected
    cold=_actual_cold_r11(_COLD_R11_CURRENT) and expected is _COLD_R11_CURRENT.expected
    if not active and not cold and _R5_REG_CURRENT is None:return expected
    if not active and not cold and expected is not _r5_reg_module()._STATE['expected']:raise RuntimeError('R5PublicExpectedIdentity')
    carrier=_r11_carrier();p=carrier['provider']
    if str(_R5_PROVIDER)!=p['path']or expected['files'][p['path']]!=p['current']or expected['approved_providers'][p['only_approved_provider_change']]!=_R5_COMMIT:raise RuntimeError('R5HistoricalProjectionIdentity')
    if expected['files'].get('/etc/ld.so.cache')!={'size':150747,'sha256':'c1dbbf1efb0a2e4e39124d1c6b296f25bb11008095945378714188dff359f320','mode':420,'uid':0,'gid':0}:raise RuntimeError('R9CacheCurrentPin')
    value=dict(expected);value['files']=dict(expected['files']);value['files'][p['path']]=p['old'];value['files']['/etc/ld.so.cache']={'size':150747,'sha256':'19dd529344d1014725201b8ae91124751cbfca72c1ab989ccd7f91eb9c6d33f8','mode':420,'uid':0,'gid':0}
    value['approved_providers']=dict(expected['approved_providers']);value['approved_providers'][p['only_approved_provider_change']]=p['old_commit']
    return value


def check_selection_records(expected,selection):
    historical=_r5_historical_selection(expected)
    newpaths={r['path'] for r in selection['new_tool_records']}
    source=Path(__file__).parent.parent
    legacy={n:v for n,v in historical['files'].items() if not Path(n).is_relative_to(source) and n not in newpaths}
    hasher=hashlib.sha256()
    for part in json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True).iterencode(legacy):
        if len(part)>JSON_ESCAPE_PEAK:raise RuntimeError('LegacyMetadataChunk')
        hasher.update(part.encode('ascii'))
    if len(legacy)!=20279 or hasher.hexdigest()!=selection['old_external_sha256']:raise RuntimeError('LegacyExternalSubsetChanged')
    for field,key in [('runtime_elf','old_runtime_elf'),('runtime_mapped_data','old_runtime_mapped_data'),('approved_providers','old_providers'),('closed_roots','old_closed_roots')]:
        if historical[field]!=selection[key]:raise RuntimeError('ToolRuntimeRoleGrowth')
    graph=selection['tool_ELF_graphs']
    if len(graph)!=5:raise RuntimeError('ToolGraphMismatch')
    graph_hash=hashlib.sha256()
    for part in json.JSONEncoder(sort_keys=True,separators=(',',':')).iterencode(graph):
        if len(part)>JSON_ESCAPE_PEAK:raise RuntimeError('ToolGraphMismatch')
        graph_hash.update(part.encode('ascii'))
    if graph_hash.hexdigest()!='4c744b472c49184cc1304971bb751b94b4f93fe7ba7102b4f0f36c408f399b93':raise RuntimeError('ToolGraphMismatch')
    rows=selection['new_tool_records']
    if len(rows)!=200 or len({r['path'] for r in rows})!=200:raise RuntimeError('Exact200ToolRecords')
    for row in rows:
        if expected['files'].get(row['path'])!={k:row[k] for k in ('size','sha256','mode','uid','gid')}:raise RuntimeError('ToolRecordMismatch')
    if len(selection['opaque_cache_pairs'])!=54:raise RuntimeError('Exact54ToolCachePairs')
    return True


def verify_tool_selection(expected):
    selection_path=Path(__file__).with_name('runtime_tool_selection.json')
    same(selection_path,expected['files'][str(selection_path)])
    selection=bounded_json_loads(selection_path.read_bytes(),1048576,True)
    if selection['schema']!='wordling.tool-selection/v1':raise RuntimeError('ToolSelectionSchema')
    check_selection_records(expected,selection)
    for alias in selection['shell_aliases']:
        if os.readlink(alias['logical'])!=alias['text']:raise RuntimeError('ToolShellAlias')
    rows=selection['new_tool_records']
    if len(rows)!=200 or len({r['path'] for r in rows})!=200:raise RuntimeError('Exact200ToolRecords')
    for row in rows:
        wanted={k:row[k] for k in ('size','sha256','mode','uid','gid')}
        if expected['files'].get(row['path'])!=wanted:raise RuntimeError('ToolRecordMismatch')
        if row['path'] in expected['runtime_elf'] or row['path'] in expected['runtime_mapped_data']:raise RuntimeError('ToolRuntimeRoleGrowth')
        same(row['path'],wanted)
    if len(selection['opaque_cache_pairs'])!=54:raise RuntimeError('Exact54ToolCachePairs')
    for pair in selection['opaque_cache_pairs']:
        p=Path(pair['cache']);source=Path(pair['source']);st=source.stat()
        same(p,expected['files'][str(p)]);same(source,expected['files'][str(source)])
        with p.open('rb') as f:header=f.read(16)
        check_tool_pair(header,dict(size=st.st_size,mtime_ns=st.st_mtime_ns),pair)
    # Explicit opaque TOOL bytes. Header metadata NEVER proves compiled-body/source equivalence.
    return selection


def check_tool_pair(header,source,pair):
    if len(header)!=16 or header[:4].hex()!=pair['magic_hex'] or header[:4].hex()!='cb0d0d0a' or int.from_bytes(header[4:8],'little')!=0:raise RuntimeError('ToolCacheHeader')
    stamp=int.from_bytes(header[8:12],'little');size=int.from_bytes(header[12:16],'little')
    if stamp!=pair['header_mtime'] or size!=pair['header_size'] or stamp!=((source['mtime_ns']//1000000000)&0xffffffff) or size!=(source['size']&0xffffffff):raise RuntimeError('ToolCacheMetadata')


def check_reference_shape(data,campaign=None):
    roots=data['canonical_reference_roots'];maximum=64
    if campaign is not None:
        if not _actual_campaign(campaign):raise RuntimeError('ActualR5ReferenceIdentity')
        path=_R11_FREEZE/'reference-roots.json';same(path,campaign.manifest['members']['reference-roots.json'])
        profile=_campaign_small(path,65536)
        if set(profile)!={'schema','roots','policies'}or profile['schema']!='wordling.controller-campaign-r5-reference-profile/v1':raise RuntimeError('R5ReferenceProfile')
        names=profile['roots'];policies=profile['policies']
        if type(names)is not list or not 91<=len(names)<=128 or any(type(r)is not str or not r.isascii()or not 0<len(r)<=192 or not Path(r).is_absolute()for r in names)or names!=sorted(set(names)):raise RuntimeError('R5ReferenceRootShape')
        if type(policies)is not dict or set(policies)!=set(names)or any(type(v)is not str or not v.isascii()or not 0<len(v)<=512 for v in policies.values()):raise RuntimeError('R5ReferencePolicyShape')
        # Exact3-field shape bounds key-inclusive nodes to391 (ceiling394).
        # The externally anchored SOURCE profile alone fixes the adopted roots.

        m=_r11_carrier()['reference_grammar']['mandatory91']
        packed=base64.b64decode(m['base64'],validate=True);z=zlib.decompressobj(31);raw=z.decompress(packed,16385)
        if not z.eof or z.unused_data or z.unconsumed_tail or len(raw)!=m['raw']or hashlib.sha256(raw).hexdigest()!=m['raw_sha256']:raise RuntimeError('R5MandatoryRootsCodec')
        mandatory=bounded_json_loads(raw,16384,True)
        if len(mandatory)!=91 or not set(mandatory)<=set(profile['roots'])or sorted(r['root']for r in roots)!=profile['roots']:raise RuntimeError('ExactR5ReferenceRoots')
        if any(profile['policies'][r['root']]!=r['policy']for r in roots):raise RuntimeError('ExactR5ReferencePolicy')
        maximum=len(profile['roots'])
    if type(roots)is not list or len(roots)>maximum:raise RuntimeError('ReferenceCardinality')
    names=set();total=0
    for ref in roots:
        if set(ref)!={'root','count','bytes','members','policy'}or ref['root']in names:raise RuntimeError('ReferenceSchema')
        names.add(ref['root']);members=ref['members'];total+=len(members)
        if ref['count']!=len(members)or total>32768:raise RuntimeError('ReferenceCardinality')
        seen=set()
        for row in members:
            if set(row)!={'relative','path','bytes','mode','uid','gid','sha256'}:raise RuntimeError('ReferenceSchema')
            name=row['relative']
            if not name or Path(name).is_absolute()or'..'in Path(name).parts or name in seen:raise RuntimeError('ReferenceAmbiguous')
            seen.add(name)
            if row['path']!=str(Path(ref['root'])/name)or len(row['sha256'])!=64:raise RuntimeError('ReferencePinShape')
    return True


def admit_capacity(expected,root,campaign=None,slot=None,*,qualification=None):
    """Resolve exact immutable baseline/references BEFORE allocation/child effects."""
    if qualification is not None:
        if campaign is not None or slot is not None or not _actual_cold_r11(qualification):raise RuntimeError('R11QualificationIdentity')
        return qualification.admit(expected,root)
    if _R5_REG_CURRENT is not None:
        if campaign is not None or slot is not None:raise RuntimeError('PublicRegressionNotCampaign')
        return _r5_reg_module()._admit_owner(expected,root)
    if campaign is not None:
        if not _actual_campaign(campaign) or expected is not campaign.expected:raise RuntimeError('ActualCampaignCapacityIdentity')
        return campaign.admit(root,slot)
    baseline_path=FREEZE/'capacity-baseline.json.gz'
    expected_pin=expected['evidence_baseline']
    same(baseline_path,expected_pin)
    data=bounded_json_loads(bounded_gzip(baseline_path),8388608,True)
    check_reference_shape(data)
    rows=data['E_inventory'];base=Path(data['evidence_root'])
    actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
    admitted=set() if _ACTIVE_BUDGET is None else {str(p.relative_to(base)) for p in _ACTIVE_BUDGET.slots if p.is_relative_to(base) and p.is_file()}
    if actual!={r['relative'] for r in rows}|admitted:raise RuntimeError('EvidenceBaselineNameSet')
    for row in rows:
        p=base/row['relative'];same(p,dict(size=row['bytes'],sha256=row['sha256'],mode=row['mode'],uid=row['uid'],gid=row['gid']))
    if len(rows)!=data['E_files'] or sum(r['bytes'] for r in rows)!=data['E_bytes']:raise RuntimeError('EvidenceBaselineTotals')
    for ref in data['canonical_reference_roots']:
        directory=Path(ref['root']);members=ref['members']
        if len(members)!=ref['count'] or {str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file()}!={r['relative'] for r in members}:raise RuntimeError('ImmutableReferenceMembers')
        for row in members:same(directory/row['relative'],dict(size=row['bytes'],sha256=row['sha256'],mode=row['mode'],uid=row['uid'],gid=row['gid']))
    if data['E_bytes']+sum(r[0] for r in CLASS_LIMITS.values())>EVIDENCE_LIMIT or data['E_files']+sum(r[1] for r in CLASS_LIMITS.values())>EVIDENCE_FILES:raise RuntimeError('EvidenceFutureEnvelopeFit')
    budget=evidence_budget(root)
    if budget.base_files not in (0,data['E_files']) or budget.base_bytes not in (0,data['E_bytes']):raise RuntimeError('EvidenceBaselineChanged')
    budget.base_files=data['E_files'];budget.base_bytes=data['E_bytes']
    return budget


def _trace_allocation_bound(raw):
    size=len(raw.encode('utf8'));n=min(16384,raw.count('\n'))
    charge=size+2048*n+8*size+16*(size//3)+524288+46137344+8388608+16777216+1048576
    if charge>OWNED_MEMORY_LIMIT:raise RuntimeError('PreparedMemoryCharge')
    return charge


def _qualification_literal_render(target):
    # Pure fixed-template rendering only; this grants no execution authority.
    old='V=pathlib.Path('+repr(str(TARGET/'venv')).replace("'",'"')+')'
    if QUALIFY_LITERAL.count(old)!=1:raise RuntimeError('QualificationTemplateBinding')
    replacement='V=pathlib.Path('+repr(str(Path(target)/'venv'))+')'
    return QUALIFY_LITERAL.replace(old,replacement,1)


def qualification_literal(target):
    target=Path(target)
    spelling=str(target)
    if not target.is_absolute() or '..' in target.parts or not spelling.startswith('/tmp/wordling-WP70-') or len(spelling.encode('utf8'))>4096:raise RuntimeError('QualificationTargetBinding')
    return _qualification_literal_render(target)


def supervisor_notice(event,**facts):
    value=os.environ.get('WORDLING_PREPARATION_CONTROL_FD')
    if value is None:return  # Harmless direct helper controls only, never main.
    raw=(json.dumps(dict(event=event,**facts))+'\n').encode('ascii')
    if len(raw)>256 or os.write(int(value),raw)!=len(raw):raise RuntimeError('SupervisorControlLost')


class _RunCapture:
    """Identity token; caller construction alone is never a genuine capture."""
    __slots__=()

_CAPTURES={}


def _quoted_argument(text):
    q=re.search(r'("(?:[^"\\]|\\.)*")',text)
    if q is None:raise RuntimeError('MissingLexicalPath')
    if len(q[1])>8192:raise RuntimeError('QuotedPathBound')
    value=ast.literal_eval(q[1])
    if type(value) is not str or len(value.encode('utf8'))>4096 or text[q.end():].lstrip().startswith('...'):raise RuntimeError('TruncatedLexicalPath')
    return value,q.end()


def _exec_argv(text,start):
    suffix=text[start:].lstrip()
    if not suffix.startswith(','):raise RuntimeError('MissingExecArgv')
    suffix=suffix[1:].lstrip()
    if not suffix.startswith('['):raise RuntimeError('UnknownExecArgv')
    quoted=False;escaped=False;depth=0;end=None
    for i,char in enumerate(suffix):
        if escaped:escaped=False;continue
        if quoted and char=='\\':escaped=True;continue
        if char=='"':quoted=not quoted;continue
        if quoted:continue
        if char=='[':
            depth+=1
            if depth>1:raise RuntimeError('ExecArgvNesting')
        if char==']':
            depth-=1
            if depth==0:end=i+1;break
    if end is None:raise RuntimeError('TruncatedExecArgv')
    token=suffix[:end]
    if len(token.encode('utf8'))>8192 or token.count(',')>255:raise RuntimeError('ExecArgvBound')
    if depth!=0:raise RuntimeError('ExecArgvNesting')
    value=ast.literal_eval(token)
    if type(value) is not list or any(type(x) is not str for x in value):raise RuntimeError('UnknownExecArgv')
    if len(value)>256 or any(len(x.encode('utf8'))>4096 for x in value):raise RuntimeError('ExecArgvBound')
    return value


_RESTART_RESULT='? ERESTARTNOINTR (To be restarted)'


def _restart_tokens(text):
    """Bounded token spans into existing args; never retain normalized copies."""
    width=0
    for char in text:
        number=ord(char)
        if 0xd800<=number<=0xdfff:raise RuntimeError('RestartArgsLexicalBound')
        width+=1 if number<128 else 2 if number<2048 else 3 if number<65536 else 4
        if width>1024:raise RuntimeError('TraceRestartArgsBound')
    index=0;tokens=0;stack=0;depth=0
    while index<len(text):
        char=text[index]
        if char in ' \t':index+=1;continue
        first=index;index+=1;kind='punctuation'
        if char in '\"\'':
            kind='quoted';quote=char;escaped=False;closed=False
            while index<len(text):
                current=text[index];index+=1
                if escaped:escaped=False
                elif current=='\\':escaped=True
                elif current==quote:closed=True;break
            if not closed:raise RuntimeError('RestartArgsLexicalBound')
        elif char=='<':
            kind='descriptor'
            while index<len(text) and text[index]!='>':index+=1
            if index==len(text):raise RuntimeError('RestartArgsLexicalBound')
            index+=1
        elif char=='>':raise RuntimeError('RestartArgsLexicalBound')
        elif char.isalnum() or char=='_':
            kind='word'
            while index<len(text) and (text[index].isalnum() or text[index]=='_'):index+=1
        elif char in '([{':
            stack=(stack<<2)|('([{'.index(char)+1);depth+=1
        elif char in ')]}':
            if not depth or stack&3!=')]}'.index(char)+1:raise RuntimeError('RestartArgsLexicalBound')
            stack>>=2;depth-=1
        elif char.isspace():raise RuntimeError('RestartArgsLexicalBound')
        tokens+=1
        if tokens>1024:raise RuntimeError('TraceRestartTokenBound')
        yield kind,first,index
    if depth:raise RuntimeError('RestartArgsLexicalBound')


def _restart_equal(left,right):
    a=_restart_tokens(left);b=_restart_tokens(right)
    while True:
        x=next(a,None);y=next(b,None)
        if x is None or y is None:return x is None and y is None
        if x[0]!=y[0] or x[2]-x[1]!=y[2]-y[1]:return False
        for offset in range(x[2]-x[1]):
            if left[x[1]+offset]!=right[y[1]+offset]:return False


def parse_trace(raw):
    """Lexical DATA parser. NEVER queries/normalizes any filesystem path."""
    if raw and not raw.endswith('\n'):raise RuntimeError('TruncatedTraceTail')
    if len(raw.encode('utf8'))>CONSTRUCTION_RAW_LIMIT or raw.count('\n')>32768:raise RuntimeError('TraceInputBound')
    _trace_allocation_bound(raw)
    pending={};records=[];surface=set(TRACE_SURFACE.split(','));actors=set()
    lifecycle={};restarts={};interrupted=0
    for lineno,line in enumerate(raw.splitlines(),1):
        match=re.fullmatch(r'(?:\[pid\s+(\d+)\]|(\d+))\s+(.*)',line)
        if not match:raise RuntimeError('UnknownTraceActorOrFraming:'+line[:100])
        digits=match[1] or match[2]
        if len(digits)>12 or len(line.encode('utf8'))>16384:raise RuntimeError('TraceLexemeBound')
        actor=int(digits)
        if actor not in actors:
            actors.add(actor)
            if len(actors)>256:raise RuntimeError('TraceActorCardinality')
            lifecycle[actor]=[0,False]  # Fixed per-actor exec epoch/dead flags only.
        life=lifecycle[actor]
        text=match[3];firstline=lineno
        if text.startswith(('--- ','+++ ')):
            if text.startswith('+++ '):
                life[1]=True
                if actor in restarts:raise RuntimeError('InterruptedCloneActorExit')
            continue
        resumed=re.match(r'<\.\.\. (\w+) resumed>(.*)',text)
        if resumed:
            if actor not in pending or pending[actor][0]!=resumed[1]:raise RuntimeError('UnmatchedResumedTrace')
            _,first,firstline=pending.pop(actor);text=first+resumed[2]
        if '<unfinished ...>' in text:
            if actor in pending:raise RuntimeError('DuplicateUnfinishedTrace')
            first=text.removesuffix('<unfinished ...>');call=re.match(r'(\w+)\(',first)
            if call is None or call[1] not in surface:raise RuntimeError('UnknownUnfinishedTrace')
            if len(pending)>=32:raise RuntimeError('TracePendingBound')
            pending[actor]=(call[1],first,firstline);continue
        complete=re.fullmatch(r'(\w+)\((.*)\)\s+=\s+(.+)',text)
        if not complete or complete[1] not in surface:raise RuntimeError('UnsupportedTraceRecord:'+text[:100])
        call,args,result=complete.groups()
        run=0
        for char in result:
            run=run+1 if '0'<=char<='9' else 0
            if run>20:raise RuntimeError('TraceIntegerBound')
        restart=result==_RESTART_RESULT
        if restart and call!='clone':raise RuntimeError('UnsupportedRestartSyscall')
        prior=restarts.get(actor)
        if (restart or prior is not None) and actor in pending:raise RuntimeError('RestartFollowupMismatch')
        if prior is not None:
            if life[1]:raise RuntimeError('TraceActorReuse')
            if life[0]!=prior[2] or (call in ('execve','execveat') and not result.startswith('-1 ')):
                raise RuntimeError('RestartActorEpochChanged')
            if call!='clone' or not _restart_equal(records[prior[0]]['args'],args):
                raise RuntimeError('RestartFollowupMismatch')
            if not restart:
                if re.fullmatch(r'[0-9]{1,12}',result):
                    child=int(result)
                    if child==0 or child==actor:raise RuntimeError('UnknownTraceResult')
                elif not re.fullmatch(r'-1 [A-Z][A-Z0-9_]* \(.*\)',result):
                    raise RuntimeError('UnknownTraceResult')
        if restart:
            if life[1]:raise RuntimeError('TraceActorReuse')
            for _ in _restart_tokens(args):pass
            if interrupted>=64:raise RuntimeError('TraceRestartTotalBound')
            if prior is not None and prior[3]>=8:raise RuntimeError('TraceRestartChainBound')
            if prior is None and len(restarts)>=32:raise RuntimeError('TraceRestartPendingBound')
        success=not restart and not result.startswith('-1 ')
        event=dict(actor=actor,syscall=call,success=success,event=len(records)+1,lines=[firstline,lineno],raw=text,args=args,result=result,kind='control',path=None,requested=None,flags=None,argv=None)
        if call in ('open','openat','openat2','execve','execveat'):
            requested,end=_quoted_argument(args);event['requested']=requested
            if call in ('execve','execveat'):
                event['kind']='exec';event['argv']=_exec_argv(args,end);event['path']=requested
                if success and (not requested.startswith('/') or result!='0'):raise RuntimeError('UnsupportedRelativeOrUnknownExec')
            else:
                event['kind']='open'
                left=end
                while left<len(args) and args[left].isspace():left+=1
                if left<len(args) and args[left]==',':left+=1
                while left<len(args) and args[left].isspace():left+=1
                right=len(args)
                while right>left and args[right-1].isspace():right-=1
                flags_bytes=0
                for index in range(left,right):
                    flags_bytes+=len(args[index].encode('utf8','strict'))
                    if flags_bytes>1024:raise RuntimeError('TraceFlagsBound')
                event['flags']=args[left:right]
                if success:
                    fd=re.fullmatch(r'\d+<(/[^>]+)>',result)
                    if fd is None:raise RuntimeError('MissingKernelResolvedOpenOrigin')
                    event['path']=fd[1]  # Preserve EXACT captured descriptor spelling.
        elif success:
            if not re.match(r'\d+(?:<[^>]+>)?(?:\s|$)',result):raise RuntimeError('UnknownTraceResult')
            if call in ('setsid','setpgid','memfd_create'):raise RuntimeError('UnsupportedToolContainmentOrOrigin:'+call)
        if len(records)>=16384:raise RuntimeError('TraceRecordCardinality')
        if prior is not None:
            records[prior[1]]['lexical_followup']={'kind':'OBSERVED_LEXICAL_FOLLOWUP','event':event['event']}
        if restart:
            event['outcome']='INTERRUPTED_RESTARTABLE';event['child_pid']=None;event['lexical_followup']=None
            interrupted+=1
            restarts[actor]=(len(records) if prior is None else prior[0],len(records),life[0],1 if prior is None else prior[3]+1)
        elif prior is not None:del restarts[actor]
        if event['kind']=='exec' and success:life[0]+=1
        records.append(event)
    if pending:raise RuntimeError('UnfinishedTraceAtEOF')
    if restarts:raise RuntimeError('InterruptedCloneAtEOF')
    return records


def _transient_maps_events(records,launch_argv):
    """Pure lexical predicate; result is DATA, not production capture authority."""
    if not records:raise RuntimeError('MissingInitialExec')
    first=records[0]
    if (first['kind']!='exec' or not first['success'] or first['syscall']!='execve' or
            first['requested']!=launch_argv[0] or first['argv']!=list(launch_argv)):
        raise RuntimeError('WrongOrFailedInitialPinnedExec')
    initial=first['actor'];epoch=0;events=[]
    for record in records:
        if record['actor']==initial and record['kind']=='exec' and record['success']:epoch+=1
        path=record['path'] or '';request=record['requested'] or ''
        if not record['success']:continue
        if not (path.startswith('/proc/') or request.startswith('/proc/')):continue
        if not (record['kind']=='open' and record['syscall']=='openat' and
                request=='/proc/self/maps' and record['flags']=='O_RDONLY' and
                record['actor']==initial and epoch==1 and
                path=='/proc/'+str(initial)+'/maps' and
                re.fullmatch(r'[0-9]+</proc/'+str(initial)+r'/maps>',record['result']) is not None):
            raise RuntimeError('UnapprovedProcOrigin')
        events.append(dict(event=record['event'],lines=record['lines'],actor=initial,initial_exec_epoch=1,
            syscall='openat',requested=request,flags=record['flags'],kernel_fd_path=path,raw_record=record['raw'],kernel_result=record['result'],
            contents='UNKNOWN/not captured',classification='TRANSIENT_KERNEL_DATA_NOT_CODE'))
    return events


def historical_data_review(raw,launch_argv,known_stable_paths=None):
    """Explicit historical/synthetic DATA only; cannot mint _RunCapture."""
    records=parse_trace(raw);transient=_transient_maps_events(records,launch_argv)
    excluded={x['event'] for x in transient};stable=[]
    for record in records:
        if not record['success'] or record['kind'] not in ('open','exec') or record['event'] in excluded:continue
        path=record['path'];stable.append(path)
        if known_stable_paths is not None and path not in known_stable_paths:raise RuntimeError('HistoricalUnknownStableOrigin:'+path)
    return dict(evidence_kind='HISTORICAL_OR_SYNTHETIC_DATA_ONLY',production_authority=False,transient=transient,stable_paths=stable)


def pin(path):
    path=Path(path);before=path.stat()
    if not stat.S_ISREG(before.st_mode):raise RuntimeError('PinRegularFile')
    digest=hashlib.sha256();size=0
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    try:
        opened=os.fstat(fd)
        if (opened.st_dev,opened.st_ino,opened.st_size,opened.st_mtime_ns,opened.st_ctime_ns)!=(before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns):raise RuntimeError('PinIdentityChanged')
        while True:
            raw=os.read(fd,65536)
            if not raw:break
            size+=len(raw)
            if size>before.st_size:raise RuntimeError('PinSizeChanged')
            digest.update(raw)
        after=os.fstat(fd);current=path.stat()
        fields=lambda st:(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
        if size!=before.st_size or fields(after)!=fields(before) or fields(current)!=fields(before):raise RuntimeError('PinIdentityChanged')
    finally:os.close(fd)
    return dict(size=size,sha256=digest.hexdigest())


def rights(path):
    s=Path(path).lstat()
    return dict(mode=stat.S_IMODE(s.st_mode),uid=s.st_uid,gid=s.st_gid)


def load_expected():
    # Trusted frozen metadata supplied as the exact reviewed input. Neither
    # newly observed imports nor caller callbacks can append to this set.
    if (FREEZE/'expected-inputs.json.gz').stat().st_size>1572864:raise RuntimeError('ExpectedCompressedBound')
    obj=bounded_json_loads(bounded_gzip(FREEZE/'expected-inputs.json.gz'),8388608,True)
    if obj['schema']!='wordling.runtime-qualification-expected/v1':raise RuntimeError('ExpectedSchema')
    return obj


def same(path,expected):
    p=Path(path)
    if p.is_symlink() or not p.is_file() or pin(p)!=dict(size=expected['size'],sha256=expected['sha256']):
        raise RuntimeError('ChangedInput:'+str(p))
    if rights(p)!={k:expected[k] for k in ('mode','uid','gid')}:raise RuntimeError('ChangedRights:'+str(p))


class _CampaignArena:
    """One shared nonexpected arena; retained trees have explicit lifetimes."""
    __slots__=('used','holds')
    def __init__(self):self.used=0;self.holds={}
    def hold(self,name,charge):
        if type(name) is not str or name in self.holds or len(self.holds)>=32 or type(charge) is not int or charge<0 or self.used+charge>8388608:raise RuntimeError('CampaignSharedArena')
        self.holds[name]=charge;self.used+=charge
    def release(self,name):
        self.used-=self.holds.pop(name)
    def shrink(self,name,charge):
        old=self.holds[name]
        if type(charge) is not int or not 0<=charge<=old:raise RuntimeError('CampaignArenaShrink')
        self.used-=old-charge;self.holds[name]=charge
    def decode(self,name,raw,maximum,earlier_nodes=None):
        # Account the original bytes/bytearray elsewhere before entering.
        # UTF8 text is bounded BEFORE it is allocated, including refusal paths.
        if type(raw) not in (bytes,str) or len(raw)>maximum:raise RuntimeError('JSONInputBound')
        # Includes UTF8 scanner text and unescape scratch; the original raw
        # capture/caller line copies have their OWN live scope reservation.
        self.hold(name,12*len(raw)+4096)
        try:
            text,charge=_json_prepared(raw,maximum)
            if earlier_nodes is not None:
                if type(earlier_nodes) is not int or not 1<=earlier_nodes<=65536 or (charge-8*len(text))//96>earlier_nodes:raise RuntimeError('CampaignEarlierJSONNodeBound')
            additional=max(0,charge+4*len(raw)-self.holds[name])
            if self.used+additional>8388608:raise RuntimeError('CampaignSharedArena')
            self.used+=additional;self.holds[name]+=additional
            value=json.loads(text,parse_constant=lambda s:(_ for _ in ()).throw(RuntimeError('JSONNonfinite')))
            del text
            self.used-=self.holds[name]-charge;self.holds[name]=charge
            return value
        except BaseException:
            # The escaping traceback may still retain text/decoder locals.
            # The real caller scope owns this reservation until those frames
            # have actually returned; failure is never refunded here.
            raise


class _CaseScope:
    """Conservative explicit leases; close only AFTER exercise frame returns.

    Ordinary bytes/JSON primitives escape run/decode unchanged. Charges do not
    escape: every returned raw/tree remains charged through the caller frame.
    Only compact whole refs and bounded status facts can leave that frame.
    """
    __slots__=('campaign','arena','names','serial','number','closed')
    def __init__(self,campaign,number):
        self.campaign=campaign;self.arena=campaign.arena;self.names=[];self.serial=0;self.number=number;self.closed=False
    def tag(self):
        if self.closed:raise RuntimeError('CaseScopeClosed')
        self.serial+=1
        if self.serial>2147483647:raise RuntimeError('CaseScopeSerialBound')
        return 'case-'+str(self.number)+'-'+str(self.serial)
    def hold(self,charge):
        name=self.tag()
        try:self.arena.hold(name,charge)
        except BaseException:self.campaign.fatal('CaseSharedArena');raise
        self.names.append(name);return name
    def begin_capture(self,remaining):
        if type(remaining) is not int or not 0<=remaining<=2097152:raise RuntimeError('CaseRawRemaining')
        # CPython bytearray <=9/8 payload +small constant, returned bytes, two
        # 64KiB I/O pieces and tuple/receipt tails. Prior calls stay charged.
        return self.hold((5*remaining+1)//2+262144)
    def end_capture(self,name,result):
        raw=len(result[1])+len(result[2])
        self.arena.shrink(name,raw+256)
        # Caller assertions retain the original bytes.splitlines semantics.
        # Account its worst live list/line copies before the caller can create
        # them; do not silently replace bytes with proxy/view objects.
        out=result[1];lines=out.count(b'\n')+out.count(b'\r')+1
        self.hold(2*len(out)+64*lines+512)
    def decode(self,raw,maximum=2097152,temporary=False):
        name=self.tag()
        try:value=self.arena.decode(name,raw,maximum)
        except (ValueError,UnicodeError):
            if name in self.arena.holds:self.names.append(name)
            raise
        except BaseException:
            if name in self.arena.holds:self.names.append(name)
            self.campaign.fatal('CaseJSONArenaOrShape');raise
        self.names.append(name)
        return value,name
    def release_temporary(self,name):
        # Caller must delete the decoded tree and every derived reference first.
        self.arena.release(name);self.names.remove(name)
    def close_after_frame(self):
        if self.closed:raise RuntimeError('CaseScopeDoubleClose')
        for name in self.names:self.arena.release(name)
        self.names.clear();self.closed=True


def _campaign_features():
    for module,names in ((os,('pidfd_open','P_PIDFD','waitid','WNOWAIT','WEXITED','WNOHANG')),
                         (signal,('pidfd_send_signal',)),
                         (socket,('AF_UNIX','SOCK_SEQPACKET','SO_PASSCRED','SCM_CREDENTIALS','SCM_RIGHTS','MSG_CMSG_CLOEXEC','MSG_TRUNC','MSG_CTRUNC'))):
        if any(not hasattr(module,name) for name in names):raise RuntimeError('CampaignKernelFeatureUnavailable')


def _campaign_clock(end):
    if type(end) is not int or end<=0 or time.monotonic_ns()>=end:raise RuntimeError('CampaignDeadline')


def _campaign_digest(value):
    h=hashlib.sha256()
    # Canonical predecessor encoder is deliberately distinct from streaming
    # writer insertion order. Keys are finite frozen metadata, not observations.
    for piece in json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True).iterencode(value):h.update(piece.encode('ascii'))
    return h.hexdigest()


def _campaign_small(path,maximum=32768):
    p=Path(path)
    if p.is_symlink() or not p.is_file() or p.stat().st_size>maximum:raise RuntimeError('CampaignMetadataBound')
    with p.open('rb') as stream:raw=stream.read(maximum+1)
    if len(raw)>maximum:raise RuntimeError('CampaignMetadataBound')
    return bounded_json_loads(raw,maximum,True)


def _r11_carrier():
    # Immutable predecessor supplies original20519 pins/roles; this fixed tiny
    # successor supplies only the explicit source5/controller and custody delta.
    same(_R11_ADMISSION,_R11_CARRIER)
    delta=_campaign_small(_R11_ADMISSION)
    if set(delta)!={'schema','predecessor','old5','owned35_sha256','source6_before','future_source','qualification','exclusions','live_growth_basis','recovery_custody'} or delta['schema']!='wordling.controller-campaign-r11-admission/v1':raise RuntimeError('R11CarrierSchema')
    if delta['predecessor']!=dict(path=str(_R5_ADMISSION),**_R5_CARRIER):raise RuntimeError('R11PredecessorBinding')
    same(_R5_ADMISSION,_R5_CARRIER)
    carrier=_campaign_small(_R5_ADMISSION)
    if carrier['schema']!='wordling.controller-campaign-r5-admission/v1':raise RuntimeError('R11PredecessorSchema')
    controller=str(Path(__file__).resolve().parent.parent/'controller.py')
    if set(delta['old5'])!=set(carrier['old4'])|{controller} or any(delta['old5'][k]!=v for k,v in carrier['old4'].items()):raise RuntimeError('R11OnlyControllerBasisExtension')
    if set(delta['source6_before'])!=set(delta['old5'])|{str(_R5_PROVIDER)} or delta['source6_before'][str(_R5_PROVIDER)]!=carrier['provider']['current']:raise RuntimeError('R11ProtectedLifetime')
    if delta['future_source']['root']!=str(_R11_FREEZE) or delta['future_source']['files']!=34 or delta['future_source']['manifest_members']!=32:raise RuntimeError('R11Source34')
    carrier['old4']=delta['old5'];carrier['owned36_sha256']=delta['owned35_sha256']
    carrier['future_source']=delta['future_source'];carrier['exclusions']=delta['exclusions']
    carrier['r11']=delta
    return carrier


def _r11_source_roles(sources,carrier):
    before=carrier['r11']['live_growth_basis']
    if set(sources)!=set(before):raise RuntimeError('R11FixedSourceSix')
    names=('controller.py','controller_deployment.py','run_controller_acceptance.py','runtime_qualification.py','runtime_qualification_supervisor.py')
    caps=(26867,65536,65536,262144,65536);growth=0
    for path,prior in before.items():
        row=sources[path]
        if set(row)!=set(prior)or any(row[k]!=prior[k]for k in row if k not in ('size','sha256')):raise RuntimeError('R11LiveSourceRoleDrift')
        if path==str(_R5_PROVIDER):
            if row!=prior:raise RuntimeError('R11ProtectedProviderBytes')
        else:
            name=Path(path).name
            if name not in names or row['size']>caps[names.index(name)]:raise RuntimeError('R11LiveSourceCap')
            if name=='controller.py'and (row['size']!=26867 or row['sha256']!='8c4f7de700ff3c236f1db93fdbcb4ffe02b298646286f0659bfbf6f6a68c142c'):raise RuntimeError('R11OnlyLocalIOCorrection')
            growth+=max(0,row['size']-prior['size'])
        same(path,row)
    if growth>R11_LIVE_SOURCE_GROWTH:raise RuntimeError('R11LiveSourceGrowthFit')
    return growth


def _campaign_manifest(source_sha):
    """The sole fixed-location externally anchored source boundary.

    ROOT independently checks this exact checksum and the owner source before
    launch. It selects no path, role, recipe, expected mapping or TEST grant.
    The final seal/review/grant are EXTERNAL anchors, never cyclic self-pins.
    """
    if type(source_sha) is not str or re.fullmatch('[0-9a-f]{64}',source_sha) is None:raise RuntimeError('CampaignExternalAnchor')
    carrier=_r11_carrier()
    if carrier['schema']!='wordling.controller-campaign-r5-admission/v1':raise RuntimeError('CampaignCarrierSchema')
    path=_R11_FREEZE/'source-bindings.json';p=pin(path)
    if p['size']>65536 or p['sha256']!=source_sha or rights(path)!=dict(mode=384,uid=1000,gid=1000):raise RuntimeError('CampaignExternalAnchor')
    manifest=_campaign_small(path,65536)
    if set(manifest)!={'schema','stage','nonce','members','sources','expected','capacity','descriptor','slots','baseline','control','reviews','exclusions'} or manifest['schema']!='wordling.controller-campaign-source/v1' or manifest['stage']!='FINAL_SAME_TESTED_SOURCE':raise RuntimeError('CampaignSourceManifest')
    if type(manifest['nonce']) is not str or re.fullmatch('[0-9a-f]{64}',manifest['nonce']) is None:raise RuntimeError('CampaignNonce')
    if manifest['exclusions']!=carrier['exclusions']:raise RuntimeError('CampaignExternalCoverage')
    sources=manifest['sources']
    _r11_source_roles(sources,carrier)
    if type(sources) is not dict or set(sources)!=set(carrier['old4'])|{str(_R5_PROVIDER)}:raise RuntimeError('CampaignFourSourceScope')
    for name,value in sources.items():
        old=carrier['old4'].get(name,carrier['provider']['old'])
        if set(value)!=set(old)or any(value[k]!=old[k]for k in value if k not in ('size','sha256')):raise RuntimeError('CampaignSourceRoleDrift')
        same(name,value)
    members=manifest['members'];caps=carrier['future_source']['caps']
    if type(members)is not dict or set(members)!=set(caps)-{'source-bindings.json','seal.json'}or len(members)!=32:raise RuntimeError('CampaignFreezeMembership')
    actual={str(p.relative_to(_R11_FREEZE)) for p in _R11_FREEZE.rglob('*') if p.is_file()}
    if actual!=set(members)|{'source-bindings.json','seal.json'}:raise RuntimeError('CampaignFreezeMembership')
    for name,value in members.items():
        if value['size']>caps[name]:raise RuntimeError('CampaignFreezeMemberBound')
        same(_R11_FREEZE/name,value)
    if sum((_R11_FREEZE/n).stat().st_size for n in actual)>4194304:raise RuntimeError('CampaignFreezeAggregate')
    # These are exact frozen metadata pins, not caller-selected filenames.
    for key,name in (('expected','expected-inputs.json.gz'),('capacity','capacity-baseline.json.gz'),('descriptor','campaign-descriptor.json'),('slots','writer-ledger.json'),('baseline','baseline-v17-binding.json')):
        if manifest[key]!=members[name]:raise RuntimeError('CampaignFixedMetadataBinding')
    for document in carrier['documents']:
        same(document['path'],document)
    for root in carrier['roots']:
        directory=Path(root['root'])
        if {str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file()}!=set(root['members']):raise RuntimeError('CampaignPredecessorMembership')
        same(root['seal']['path'],root['seal'])
    return manifest


def _campaign_plan(manifest):
    d=_campaign_small(_R11_FREEZE/'campaign-descriptor.json')
    if set(d)!={'schema','nonce','root','evidence','label','E_files','E_bytes'}or d['schema']!='wordling.controller-campaign-descriptor/v1'or d['nonce']!=manifest['nonce']or type(d['label'])is not str or re.fullmatch('WP70-controller-campaign[0-9]{2}-r11',d['label'])is None:raise RuntimeError('CampaignDescriptorSchema')
    source=Path(__file__).resolve().parent.parent
    if d['root']!='/tmp/'+d['label']+'-'+d['nonce'][:16]or d['evidence']!=str(source/'evidence'/d['label']):raise RuntimeError('CampaignFixedRoots')
    return d


def _campaign_expected(manifest):
    carrier=_r11_carrier();path=_R11_FREEZE/'expected-inputs.json.gz'
    if path.stat().st_size>1572864:raise RuntimeError('ExpectedCompressedBound')
    raw=bounded_gzip(path);text,charge=_json_prepared(raw,8388608,True)
    expected=json.loads(text,parse_constant=lambda s:(_ for _ in ()).throw(RuntimeError('JSONNonfinite')))
    del text,raw
    p=carrier['provider'];key=p['only_approved_provider_change']
    if p['path']!=str(_R5_PROVIDER)or expected['approved_providers'][key]!=_R5_COMMIT:raise RuntimeError('R5ProviderCommit')
    invariant={k:v for k,v in expected.items()if k not in ('files','evidence_baseline','payload_bytes')}
    invariant['approved_providers']=dict(expected['approved_providers']);invariant['approved_providers'][key]=p['old_commit']
    if _campaign_digest(invariant)!=carrier['expected_invariant_sha256']:raise RuntimeError('CampaignExpectedInvariant')
    if expected['files'].get('/etc/ld.so.cache')!={'size':150747,'sha256':'c1dbbf1efb0a2e4e39124d1c6b296f25bb11008095945378714188dff359f320','mode':420,'uid':0,'gid':0}:raise RuntimeError('R9CacheCurrentPin')
    restored=dict(expected['files']);restored.update(carrier['old4']);restored[p['path']]=p['old'];restored['/etc/ld.so.cache']={'size':150747,'sha256':'19dd529344d1014725201b8ae91124751cbfca72c1ab989ccd7f91eb9c6d33f8','mode':420,'uid':0,'gid':0}
    if _campaign_digest(restored)!=carrier['old_files_digest']['sha256']:raise RuntimeError('R5Other20514Changed')
    del restored,invariant
    source=Path(__file__).resolve().parent.parent;owned={n:v for n,v in expected['files'].items()if Path(n).is_relative_to(source)}
    four=set(carrier['old4']);five=four|{p['path']}
    if len(expected['files'])!=20519 or len(owned)!=40 or len(four)!=5 or not four<=set(owned)or p['path']in owned:raise RuntimeError('CampaignExpectedNamespace')
    if {str(x)for x in source.rglob('*')if x.is_file()and'evidence'not in x.relative_to(source).parts}!=set(owned):raise RuntimeError('CampaignActualOwnedNamespace')
    if _campaign_digest({n:v for n,v in owned.items()if n not in four})!=carrier['owned36_sha256']:raise RuntimeError('CampaignOwned36Changed')
    if set(manifest['sources'])!=five or any(expected['files'][n]!=manifest['sources'][n]for n in five):raise RuntimeError('R5FivePostimages')
    delta=sum(expected['files'][n]['size']-v['size']for n,v in carrier['old4'].items())+expected['files'][p['path']]['size']-p['old']['size']
    if expected['payload_bytes']!=carrier['old_payload_bytes']+delta or expected['evidence_baseline']!=manifest['capacity']:raise RuntimeError('CampaignExpectedPayloadAccounting')
    return expected,charge


def _campaign_input_guard(campaign):
    if not _actual_campaign(campaign):raise RuntimeError('ActualCampaignAdmissionRequired')
    expected=campaign.expected
    allnames=set(expected['files'])|set(expected['links'])|set(expected['directories'])
    for root in expected['closed_roots']:
        r=Path(root)
        if {str(p) for p in r.rglob('*')}!={n for n in allnames if Path(n).is_relative_to(r) and n!=root}:raise RuntimeError('ClosedInputSet:'+root)
        _campaign_clock(campaign.end)
    for root,names in expected['tool_startup_hook_sets'].items():
        if sorted(str(p) for p in Path(root).glob('*.pth'))!=names:raise RuntimeError('ToolStartupHookSet')
    for name,value in expected['files'].items():
        same(name,value);_campaign_clock(campaign.end)
    for name,value in expected['links'].items():
        p=Path(name)
        if not p.is_symlink() or os.readlink(p)!=value['target'] or str(p.resolve())!=value['resolved'] or rights(p)!=value['rights']:raise RuntimeError('ChangedLink:'+name)
        _campaign_clock(campaign.end)
    for name,value in expected['directories'].items():
        p=Path(name)
        if p.is_symlink() or not p.is_dir() or rights(p)!=value:raise RuntimeError('ChangedDirectory:'+name)
        _campaign_clock(campaign.end)
    # Existing exact200/54/four-role/20279 guard, not newly observed inputs.
    verify_tool_selection(expected);_campaign_clock(campaign.end)


def _campaign_rows():
    """Source-owned closed Case grammar, streamed; no argv recipes in JSON."""
    source=Path(__file__).resolve().parent.parent
    roster=_campaign_small(source/'tests/controller_roster.json',4096)
    names=roster['functional'];mutants=roster['mutants']
    if len(names)!=44 or tuple(mutants)!=tuple(CAMPAIGN_MUTANTS) or names[:2]!=['healthy','healthy-b']:raise RuntimeError('CampaignRoster')
    for variant,name in [(0,n) for n in names]+[(i+1,CAMPAIGN_MUTANTS[n][3]) for i,n in enumerate(mutants)]:
        yield variant,name,'admin','admin',''
        if name=='original-disabled':yield variant,name,'disabled','original',''
        elif name=='api-contract':yield variant,name,'api','api',''
        elif name=='foundation-contract':
            for sub in ('copied-permit','wrong-issuer-permit','consumed-permit','full-phase-book'):yield variant,name,'foundation-'+sub,'foundation',sub
        elif name=='deployment-foreign':continue
        elif name=='deployment-cached':yield variant,name,'make-real-cache','cache',''
        else:
            yield variant,name,'leaf','leaf',''
            if name in ('permanent-replay','changed-plan-same-id') or name.startswith('loss-'):yield variant,name,'replay','leaf','replay'
    for name,argv in CAMPAIGN_CONFIGURED:yield 0,name,'command','configured',name


def _campaign_case_row(index):
    if type(index) is not int or not 1<=index<=119:raise RuntimeError('CampaignCaseSlot')
    for ordinal,row in enumerate(_campaign_rows(),1):
        if ordinal==index:return row
    raise RuntimeError('CampaignCaseSlot')


def _campaign_slot_order(seq):
    if type(seq) is not int or not 1<=seq<=199:raise RuntimeError('CampaignLaunchSequence')
    ordinal=0
    for case_index,(variant,name,label,operation,argument) in enumerate(_campaign_rows(),1):
        number=None
        if label=='admin':
            if variant:number=variant+1
            elif name=='deployment-cached':number=0
            elif name=='deployment-foreign':number=1
        if number is not None:
            for stage in range(8):
                ordinal+=1
                if ordinal==seq:return 120+8*number+stage
        ordinal+=1
        if ordinal==seq:return case_index
    raise RuntimeError('CampaignLaunchSequence')


def _campaign_runtime(d,variant=0,poison=None):
    t=Path(d['root']);source=Path(__file__).resolve().parent.parent
    if poison not in (None,'deployment-cached','deployment-foreign'):raise RuntimeError('CampaignPoisonScope')
    if variant:
        if type(variant) is not int or not 1<=variant<=8 or poison is not None:raise RuntimeError('CampaignVariantScope')
        name=tuple(CAMPAIGN_MUTANTS)[variant-1]
        return t/'mutants'/name/'runtime',t/'mutants'/name/'source',Path(d['evidence'])/'mutants'/name/'deployment'
    if poison:return t/(poison+'-deployment'),source,Path(d['evidence'])/(poison+'-deployment')
    return _R11_TARGET,source,_R11_TARGET/'receipts/deployment'


def _campaign_case_root(d,variant,name):
    source=Path(__file__).resolve().parent.parent
    names=_campaign_small(source/'tests/controller_roster.json',4096)['functional']
    number=(44+variant-1) if variant else names.index('healthy' if name in dict(CAMPAIGN_CONFIGURED) else name)
    return '/tmp/wordling-reference-TEST-'+d['nonce'][:16]+'-'+str(number)


def _campaign_stage(number):
    if type(number) is not int or not 0<=number<10:raise RuntimeError('CampaignPreparationSlot')
    return (0,'deployment-cached') if number==0 else (0,'deployment-foreign') if number==1 else (number-1,None)


def _campaign_variant_bytes(raw,old,new,expected_postimage):
    """Pure closed substitution validation; creates no runtime authority."""
    if type(raw) is not bytes or len(raw)>262144 or type(old) is not str or type(new) is not str or not old:raise RuntimeError('CampaignVariantInputBound')
    text=raw.decode('utf8')
    if text.count(old)!=1:raise RuntimeError('CampaignUniqueVariantSubstitution')
    result=text.replace(old,new).encode('utf8')
    if dict(size=len(result),sha256=hashlib.sha256(result).hexdigest())!={k:expected_postimage[k] for k in ('size','sha256')}:raise RuntimeError('CampaignFrozenVariantPostimage')
    return result


def _campaign_command(manifest,role,index,trace=-1):
    d=_campaign_plan(manifest);t=Path(d['root']);s=Path(__file__).resolve().parent.parent
    ordinary=dict(PATH='/usr/bin:/bin',HOME=str(t/'home'),LANG='C.UTF-8',LC_ALL='C.UTF-8')
    if role=='root':
        if index!=0 or trace!=-1:raise RuntimeError('CampaignRootSlot')
        return dict(argv=[str(BASE),'-B',str(s/'tests/run_controller_acceptance.py'),d['label']],cwd=str(t),env={**ordinary,'SETUPTOOLS_USE_DISTUTILS':'stdlib'},fsize=2097152,logical=None,tool=False)
    if role!='slot' or type(index) is not int or not 1<=index<=199:raise RuntimeError('CampaignSlot')
    if index<=119:
        variant,name,label,operation,argument=_campaign_case_row(index)
        target,source,evidence=_campaign_runtime(d,variant,name if name.startswith('deployment-') else None)
        interpreter=target/'venv/bin/python';root=_campaign_case_root(d,variant,name)
        base=[str(interpreter),'-I','-B','-m','reference_controller']
        cwd=t
        if operation=='admin':argv=base+['test-admin','--root',root,'--generation','wp68-v1' if name=='foundation-contract' else 'wp70-v1']
        elif operation=='original':argv=base+['original','--grant-file','/tmp/never-inspect-Original-path']
        elif operation=='api':argv=[str(interpreter),'-I','-B',str(s/'tests/controller_api_probe.py'),root]
        elif operation=='foundation':argv=[str(interpreter),'-I','-B',str(s/'tests/api_cases.py'),argument,root]
        elif operation=='configured':argv=list(dict(CAMPAIGN_CONFIGURED)[name]);cwd=s.parents[3]
        elif operation=='cache':
            site=target/'venv/lib/python3.12/site-packages'
            argv=[str(interpreter),'-I','-B','-c','import py_compile;py_compile.compile('+repr(str(site/'reference_controller/controller.py'))+',doraise=True)']
        elif operation=='leaf':
            special=name.startswith(('issuer-','loss-','kernel-publication-')) or name in ('permanent-replay','changed-plan-same-id','release-order','publisher-no-clobber','hostile-path-cwd')
            scenario=('bad-stage' if name=='changed-plan-same-id' and argument=='replay' else 'healthy') if special or name=='healthy-b' else name
            argv=base+['test-leaf','--root',root,'--generation','wp70-v1','--grant-id',name,'--scenario',scenario]
            if not argument and name.startswith('loss-'):argv+=['--leaf-checkpoint',name[5:]]
            if name=='release-order':argv+=['--leaf-checkpoint','audited']
            if name=='issuer-one-write-partial':argv=['/usr/bin/strace','-qq','-yy','-e','trace=write']+argv
            if name.startswith('kernel-publication-'):
                inject={'zero':'pwrite64:retval=0:when=6','fsync':'fsync:error=EIO:when=17','readback':'pread64:retval=0:when=15'}[name[len('kernel-publication-'):]]
                argv=['/usr/bin/strace','-qq','-yy','-e','trace='+inject.split(':')[0],'-e','inject='+inject]+argv
            if name=='hostile-path-cwd':
                cwd=Path(d['evidence'])/'functional'/name/'hostile';ordinary['PYTHONPATH']=str(cwd)
        else:raise RuntimeError('CampaignOperation')
        if trace!=-1:raise RuntimeError('CampaignCaseTraceFd')
        return dict(argv=argv,cwd=str(cwd),env=ordinary,fsize=1 if operation=='leaf'and name=='issuer-one-write-partial'else 2097152,logical=None,tool=False)
    number,stage=divmod(index-120,8);variant,poison=_campaign_stage(number)
    target,source,evidence=_campaign_runtime(d,variant,poison)
    environment=target/'venv';build=target/'build-input';data=build/'reference_controller/testdata';wheels=target/'wheels'
    env=dict(PATH='/usr/bin:/bin',HOME=str(target/'home'),LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1',PIP_DISABLE_PIP_VERSION_CHECK='1',PIP_NO_CACHE_DIR='1',PIP_CONFIG_FILE='/dev/null',TMPDIR=str(target/'tmp'))
    interpreter=environment/'bin/python';tool=stage in (0,3,4,5)
    if stage==0:argv=[str(BASE),'-I','-B','-m','venv','--copies','--without-pip',str(environment)]
    elif stage in (1,6):argv=[str(interpreter),'-I','-B','-c',_campaign_qualification_literal(manifest,index)]
    elif stage in (2,7):argv=[str(interpreter),'-I','-B','-c',probe(stage==7)]
    elif stage==3:argv=['/usr/bin/cc','-std=c11','-O2','-static','-Wall','-Wextra','-Werror','-o',str(data/'fixture'),str(build/'fixture.c')]
    elif stage==4:argv=['/usr/bin/python','-B','-m','pip','wheel','--no-deps','--no-index','--no-build-isolation','--no-cache-dir','--config-settings=--build-option=--keep-temp','--wheel-dir',str(wheels),str(build)]
    elif stage==5:
        argv=['/usr/bin/python','-s','-B','-m','pip','install','--user','--root=/','--ignore-installed','--no-index','--no-deps','--no-compile','--no-cache-dir',str(wheels/'wordling_reference_controller_test-0.2.0-py3-none-any.whl')];env['PYTHONUSERBASE']=str(environment)
    logical=argv
    if tool:
        if type(trace) is not int or trace<0:raise RuntimeError('CampaignToolTraceFd')
        argv=['/usr/bin/strace','-f','-qq','-y','-s','4096','-e','trace='+TRACE_SURFACE,'-o','/proc/self/fd/'+str(trace)]+argv
    elif trace!=-1:raise RuntimeError('CampaignUnexpectedTraceFd')
    return dict(argv=argv,cwd=str(target),env=env,fsize=33554432 if stage==0 else 2097152,logical=logical,tool=tool)


def _campaign_qualification_literal(manifest,index):
    # The gate has no coordinator object: derive only from its independently
    # SHA-approved fixed manifest and finite source-selected preparation stage.
    if type(index)is not int or not 120<=index<=199:raise RuntimeError('CampaignQualificationStage')
    number,stage=divmod(index-120,8)
    if stage not in (1,6):raise RuntimeError('CampaignQualificationStage')
    variant,poison=_campaign_stage(number)
    target,source,evidence=_campaign_runtime(_campaign_plan(manifest),variant,poison)
    return _qualification_literal_render(target)


def _campaign_case_folder(d,variant,name):
    e=Path(d['evidence'])
    if variant:return e/'mutants'/tuple(CAMPAIGN_MUTANTS)[variant-1]/'case'
    return e/('configured' if name in dict(CAMPAIGN_CONFIGURED) else 'functional')/name


def _campaign_writer_groups(d):
    """Finite source grammar. Yield at most one small group, not a path book.

    IDs are the ordinal here, including every unreached/failure-prefix slot.
    Adding any writer changes this reviewed grammar and all its accounting.
    """
    current=None;raw=[];folder=None
    for variant,name,label,operation,argument in _campaign_rows():
        key=(variant,name)
        if current is not None and key!=current:
            yield 'coordinator','functional_raw',2097152,tuple(raw),str(folder)
            raw=[]
        current=key;folder=_campaign_case_folder(d,variant,name);base=folder/label
        yield 'coordinator','pair',131072,(base.with_suffix('.command.json'),base.with_suffix('.whole.json')),None
        raw.extend((base.with_suffix('.stdout'),base.with_suffix('.stderr')))
    if raw:yield 'coordinator','functional_raw',2097152,tuple(raw),str(folder)
    stages=('venv','qualify-literal-before','stdlib-before','compile','wheel','install','qualify-literal-after','origins')
    for number in range(10):
        variant,poison=_campaign_stage(number);target,source,evidence=_campaign_runtime(d,variant,poison)
        for stage,label in enumerate(stages):
            base=evidence/label
            yield 'coordinator','pair',131072,(base.with_suffix('.command.json'),base.with_suffix('.whole.json')),None
            yield 'coordinator','construction_raw',4194304,tuple(base.with_suffix(s) for s in ('.stdout','.stderr','.trace')),None
            if stage in (0,3,4,5):
                yield 'coordinator','origin',16777216,(base.with_suffix('.origins.json'),),None
                yield 'coordinator','transient',1048576,(base.with_suffix('.transient-data.json'),),None
        for name,kind,cap in (('build-freeze.json','build',262144),('compiled-data-before-wheel.json','compiled',16384),('deployment-inventory.json','inventory',4194304),('deployment.json','deployment',262144)):
            yield 'coordinator',kind,cap,(evidence/name,),None
    e=Path(d['evidence'])
    for name,kind,cap in (('frozen-input.json','misc',1048576),('runtime-before-first-P.json','misc',262144),('configured-results.json','misc',65536),('whole.json','misc',65536),('coordinator.stderr','misc',65536),('functional-results.json','aggregate',8388608),('mutant-results.json','aggregate',8388608)):
        yield 'coordinator',kind,cap,(e/name,),None
    yield 'coordinator','misc',64,(e/'functional/hostile-path-cwd/hostile/startup_transport.py',),None
    yield 'owner','custody',262144,tuple(e/'owner'/n for n in ('stdout.raw','stderr.raw','control.raw')),None
    yield 'owner','custody',65536,(e/'owner/whole.json',),None


def _campaign_writer_install_totals(rows,root,base_bytes,base_files,*,r5=False):
    """Pure precharge boundary, shared with DATA controls; mints nothing."""
    if type(base_bytes) is not int or type(base_files) is not int or min(base_bytes,base_files)<0:raise RuntimeError('CampaignClosedWriterBaseline')
    if type(r5)is not bool:raise RuntimeError('CampaignWriterProfile')
    limits=R14_CLASS_LIMITS if r5 else R4_CLASS_LIMITS;held=R14_HELD if r5 else R4_BLOCKED_HOLDS
    totals={k:[0,0] for k in limits};paths=0;count=0
    for identity,(role,kind,maximum,members,shared) in enumerate(rows):
        if identity>=768 or role not in ('owner','coordinator') or kind not in totals or type(maximum) is not int or maximum<0 or not 1<=len(members)<=10 or len(set(members))!=len(members) or any(not p.is_relative_to(root) or len(str(p).encode('ascii'))>512 for p in members):raise RuntimeError('CampaignClosedWriterShape')
        totals[kind][0]+=maximum;totals[kind][1]+=len(members);paths+=len(members);count=identity+1
    for kind,(held_bytes,held_files) in held.items():totals[kind][0]+=held_bytes;totals[kind][1]+=held_files
    if paths>1100 or any(totals[k][0]>limits[k][0] or totals[k][1]>limits[k][1] for k in totals):raise RuntimeError('CampaignClosedWriterCapacity')
    if base_bytes+sum(v[0] for v in totals.values())+(R11_LIVE_SOURCE_GROWTH if r5 else 0)>EVIDENCE_LIMIT or base_files+paths+sum(v[1]for v in held.values())>EVIDENCE_FILES:raise RuntimeError('CampaignClosedWriterGlobalCapacity')
    return totals,paths,count


R17_CLASS_LIMITS={'construction_raw': (1476395008, 1056), 'functional_raw': (463470592, 956), 'pair': (108527616, 1656), 'origin': (2952790016, 176), 'transient': (184549376, 176), 'inventory': (184549376, 44), 'deployment': (11534336, 44), 'build': (11534336, 44), 'compiled': (720896, 44), 'custody': (14090240, 140), 'aggregate': (100663296, 12), 'misc': (9371840, 40), 'input': (2097152, 16), 'catalog': (369049603, 4331), 'review': (57671680, 1687), 'control': (4644864, 198), 'failure': (144703488, 573)}
R17_HELD={'construction_raw': (1140850688, 816), 'functional_raw': (348127232, 718), 'pair': (82444288, 1258), 'origin': (2281701376, 136), 'transient': (142606336, 136), 'inventory': (142606336, 34), 'deployment': (8912896, 34), 'build': (8912896, 34), 'compiled': (557056, 34), 'custody': (13762560, 136), 'aggregate': (83886080, 10), 'misc': (7864448, 34), 'input': (2097152, 16), 'catalog': (369049603, 4331), 'review': (57671680, 1687), 'control': (4644864, 198), 'failure': (144703488, 573)}

def _r16_campaign_writer_install_totals(rows,root,base_bytes,base_files):
    """Fixed R16 campaign-only precharge arithmetic; mints nothing."""
    if type(base_bytes) is not int or type(base_files) is not int or min(base_bytes,base_files)<0:raise RuntimeError('CampaignClosedWriterBaseline')
    limits=R16_CLASS_LIMITS;held=R16_HELD
    totals={k:[0,0] for k in limits};paths=0;count=0
    for identity,(role,kind,maximum,members,shared) in enumerate(rows):
        if identity>=768 or role not in ('owner','coordinator') or kind not in totals or type(maximum) is not int or maximum<0 or not 1<=len(members)<=10 or len(set(members))!=len(members) or any(not p.is_relative_to(root) or len(str(p).encode('ascii'))>512 for p in members):raise RuntimeError('CampaignClosedWriterShape')
        totals[kind][0]+=maximum;totals[kind][1]+=len(members);paths+=len(members);count=identity+1
    for kind,(held_bytes,held_files) in held.items():totals[kind][0]+=held_bytes;totals[kind][1]+=held_files
    if paths>1100 or any(totals[k][0]>limits[k][0] or totals[k][1]>limits[k][1] for k in totals):raise RuntimeError('CampaignClosedWriterCapacity')
    if base_bytes+sum(v[0] for v in totals.values())+R11_LIVE_SOURCE_GROWTH>R16_EVIDENCE_LIMIT or base_files+paths+sum(v[1]for v in held.values())>R16_EVIDENCE_FILES:raise RuntimeError('CampaignClosedWriterGlobalCapacity')
    return totals,paths,count


def _campaign_writer_claim_fields(role,row,kind,maximum,retired,paths):
    """Pure role/path/retirement/max boundary; never a budget/lease/grant."""
    wanted_role,wanted_kind,cap,members,shared=row
    if type(retired) is not bool or retired or role!=wanted_role or kind!=wanted_kind or type(maximum) is not int or not 0<=maximum<=cap or not paths or len(set(paths))!=len(paths) or any(p not in members for p in paths):raise RuntimeError('CampaignWriterReusedOrRole')


def _r17_campaign_writer_install_totals(rows,root,base_bytes,base_files):
    """Fixed R16 campaign-only precharge arithmetic; mints nothing."""
    if type(base_bytes) is not int or type(base_files) is not int or min(base_bytes,base_files)<0:raise RuntimeError('CampaignClosedWriterBaseline')
    limits=R17_CLASS_LIMITS;held=R17_HELD
    totals={k:[0,0] for k in limits};paths=0;count=0
    for identity,(role,kind,maximum,members,shared) in enumerate(rows):
        if identity>=768 or role not in ('owner','coordinator') or kind not in totals or type(maximum) is not int or maximum<0 or not 1<=len(members)<=10 or len(set(members))!=len(members) or any(not p.is_relative_to(root) or len(str(p).encode('ascii'))>512 for p in members):raise RuntimeError('CampaignClosedWriterShape')
        totals[kind][0]+=maximum;totals[kind][1]+=len(members);paths+=len(members);count=identity+1
    for kind,(held_bytes,held_files) in held.items():totals[kind][0]+=held_bytes;totals[kind][1]+=held_files
    if paths>1100 or any(totals[k][0]>limits[k][0] or totals[k][1]>limits[k][1] for k in totals):raise RuntimeError('CampaignClosedWriterCapacity')
    if base_bytes+sum(v[0] for v in totals.values())+R11_LIVE_SOURCE_GROWTH>R16_EVIDENCE_LIMIT or base_files+paths+sum(v[1]for v in held.values())>R16_EVIDENCE_FILES:raise RuntimeError('CampaignClosedWriterGlobalCapacity')
    return totals,paths,count

R18_CLASS_LIMITS={'construction_raw': (1811939328, 1296), 'functional_raw': (578813952, 1194), 'pair': (134610944, 2054), 'origin': (3623878656, 216), 'transient': (226492416, 216), 'inventory': (226492416, 54), 'deployment': (14155776, 54), 'build': (14155776, 54), 'compiled': (884736, 54), 'custody': (14417920, 144), 'aggregate': (117440512, 14), 'misc': (10879232, 46), 'input': (2097152, 16), 'catalog': (399720451, 4539), 'review': (60555264, 1735), 'control': (4644864, 198), 'failure': (144703488, 573)}
R18_HELD={'construction_raw': (1476395008, 1056), 'functional_raw': (463470592, 956), 'pair': (108527616, 1656), 'origin': (2952790016, 176), 'transient': (184549376, 176), 'inventory': (184549376, 44), 'deployment': (11534336, 44), 'build': (11534336, 44), 'compiled': (720896, 44), 'custody': (14090240, 140), 'aggregate': (100663296, 12), 'misc': (9371840, 40), 'input': (2097152, 16), 'catalog': (399720451, 4539), 'review': (60555264, 1735), 'control': (4644864, 198), 'failure': (144703488, 573)}

def _r18_campaign_writer_install_totals(rows,root,base_bytes,base_files):
    """Fixed R18 campaign-only precharge arithmetic; mints nothing."""
    if type(base_bytes) is not int or type(base_files) is not int or min(base_bytes,base_files)<0:raise RuntimeError('CampaignClosedWriterBaseline')
    limits=R18_CLASS_LIMITS;held=R18_HELD
    totals={k:[0,0] for k in limits};paths=0;count=0
    for identity,(role,kind,maximum,members,shared) in enumerate(rows):
        if identity>=768 or role not in ('owner','coordinator') or kind not in totals or type(maximum) is not int or maximum<0 or not 1<=len(members)<=10 or len(set(members))!=len(members) or any(not p.is_relative_to(root) or len(str(p).encode('ascii'))>512 for p in members):raise RuntimeError('CampaignClosedWriterShape')
        totals[kind][0]+=maximum;totals[kind][1]+=len(members);paths+=len(members);count=identity+1
    for kind,(held_bytes,held_files) in held.items():totals[kind][0]+=held_bytes;totals[kind][1]+=held_files
    if paths>1100 or any(totals[k][0]>limits[k][0] or totals[k][1]>limits[k][1] for k in totals):raise RuntimeError('CampaignClosedWriterCapacity')
    if base_bytes+sum(v[0] for v in totals.values())+R11_LIVE_SOURCE_GROWTH>R16_EVIDENCE_LIMIT or base_files+paths+sum(v[1]for v in held.values())>R16_EVIDENCE_FILES:raise RuntimeError('CampaignClosedWriterGlobalCapacity')
    return totals,paths,count

R19_EVIDENCE_LIMIT=9663676416
R19_EVIDENCE_FILES=18432
R19_CLASS_LIMITS={'construction_raw': (2147483648, 1536), 'functional_raw': (694157312, 1432), 'pair': (160694272, 2452), 'origin': (4294967296, 256), 'transient': (268435456, 256), 'inventory': (268435456, 64), 'deployment': (16777216, 64), 'build': (16777216, 64), 'compiled': (1048576, 64), 'custody': (14745600, 148), 'aggregate': (134217728, 16), 'misc': (12386624, 52), 'input': (2097152, 16), 'catalog': (430391299, 4747), 'review': (63438848, 1783), 'control': (4644864, 198), 'failure': (144703488, 573)}
R19_HELD={'construction_raw': (1811939328, 1296), 'functional_raw': (578813952, 1194), 'pair': (134610944, 2054), 'origin': (3623878656, 216), 'transient': (226492416, 216), 'inventory': (226492416, 54), 'deployment': (14155776, 54), 'build': (14155776, 54), 'compiled': (884736, 54), 'custody': (14417920, 144), 'aggregate': (117440512, 14), 'misc': (10879232, 46), 'input': (2097152, 16), 'catalog': (430391299, 4747), 'review': (63438848, 1783), 'control': (4644864, 198), 'failure': (144703488, 573)}

def _r19_campaign_writer_install_totals(rows,root,base_bytes,base_files):
    """Fixed R19 campaign-only precharge arithmetic; mints nothing."""
    if type(base_bytes) is not int or type(base_files) is not int or min(base_bytes,base_files)<0:raise RuntimeError('CampaignClosedWriterBaseline')
    limits=R19_CLASS_LIMITS;held=R19_HELD
    totals={k:[0,0] for k in limits};paths=0;count=0
    for identity,(role,kind,maximum,members,shared) in enumerate(rows):
        if identity>=768 or role not in ('owner','coordinator') or kind not in totals or type(maximum) is not int or maximum<0 or not 1<=len(members)<=10 or len(set(members))!=len(members) or any(not p.is_relative_to(root) or len(str(p).encode('ascii'))>512 for p in members):raise RuntimeError('CampaignClosedWriterShape')
        totals[kind][0]+=maximum;totals[kind][1]+=len(members);paths+=len(members);count=identity+1
    for kind,(held_bytes,held_files) in held.items():totals[kind][0]+=held_bytes;totals[kind][1]+=held_files
    if paths>1100 or any(totals[k][0]>limits[k][0] or totals[k][1]>limits[k][1] for k in totals):raise RuntimeError('CampaignClosedWriterCapacity')
    if base_bytes+sum(v[0] for v in totals.values())+R11_LIVE_SOURCE_GROWTH>R19_EVIDENCE_LIMIT or base_files+paths+sum(v[1]for v in held.values())>R19_EVIDENCE_FILES:raise RuntimeError('CampaignClosedWriterGlobalCapacity')
    return totals,paths,count

class _CampaignBook:
    """Precharged closed writers; only active paths are retained in memory."""
    __slots__=('campaign','role','budget','retired','active','count')
    def __init__(self,campaign,role):
        if role not in ('owner','coordinator'):raise RuntimeError('CampaignWriterRole')
        self.campaign=campaign;self.role=role;self.budget=None;self.retired=0;self.active={};self.count=0
    def install(self,budget):
        if self.budget is not None:raise RuntimeError('CampaignBookDoubleInstall')
        # Injection proof is checked without retaining a thousand Path keys:
        # each fixed family has disjoint directories/suffixes and each group's
        # members are unique. Cross-family membership is also checked by the
        # independent metadata verifier before SOURCE can be approved.
        totals,paths,self.count=_r19_campaign_writer_install_totals(_campaign_writer_groups(self.campaign.descriptor),Path(self.campaign.descriptor['evidence']),budget.base_bytes,budget.base_files)
        if 26022808+sum(v[0]for v in totals.values())+R11_LIVE_SOURCE_GROWTH>R19_EVIDENCE_LIMIT or 1376+sum(v[1]for v in totals.values())>R19_EVIDENCE_FILES:raise RuntimeError('R11ColdFullEnvelopeFit')
        budget.classes=totals;self.budget=budget
    def resolve(self,path):
        path=Path(path).absolute();match=None
        for identity,row in enumerate(_campaign_writer_groups(self.campaign.descriptor)):
            if path in row[3]:
                if match is not None:raise RuntimeError('CampaignWriterAlias')
                match=(identity,row)
        if match is None:raise RuntimeError('CampaignUnclassifiedWriter')
        return match
    def claim(self,paths,kind,maximum):
        if not paths:raise RuntimeError('CampaignWriterEmpty')
        resolved=[self.resolve(p) for p in paths]
        identity,row=resolved[0]
        if any(i!=identity for i,_ in resolved) or len(set(paths))!=len(paths):raise RuntimeError('CampaignWriterGroupMismatch')
        role,wanted,cap,members,shared=row
        _campaign_writer_claim_fields(self.role,row,kind,maximum,bool(self.retired&(1<<identity)),paths)
        group=self.active.get(identity)
        if group is None:
            if len(self.active)>=8:raise RuntimeError('CampaignActiveWriterBound')
            group=dict(kind=kind,maximum=cap,used=0,paths=members,identity=identity,opened=0,written=0,shared=shared)
            self.active[identity]=group
            for p in members:self.budget.slots[p]=group
        for p in paths:
            bit=1<<members.index(p)
            if group['written']&bit:raise RuntimeError('CampaignWriterReused')
            if p.exists() or p.is_symlink():raise RuntimeError('EvidenceNoClobber')
        return group
    def raw(self,paths,kind,maximum,shared):
        group=self.claim(paths,kind,maximum)
        if group['shared']!=shared or (shared is not None and maximum!=group['maximum']):raise RuntimeError('CampaignRawGroupBinding')
        handles={}
        try:
            for p in paths:
                bit=1<<group['paths'].index(p)
                if group['opened']&bit:raise RuntimeError('CampaignRawReopen')
                group['opened']|=bit
                handles[p]=open(p,'xb',buffering=0)
            return group,handles
        except BaseException:
            for handle in handles.values():handle.close()
            self.campaign.fatal('CampaignRawWriterFailure');raise
    def document_done(self,path):
        group=self.budget.slots[path];bit=1<<group['paths'].index(path)
        if group['written']&bit:raise RuntimeError('CampaignDocumentRewrite')
        group['written']|=bit
        if group['written']==(1<<len(group['paths']))-1:self.retire(group)
    def retire(self,group):
        identity=group['identity']
        if self.active.get(identity) is not group or self.retired&(1<<identity):raise RuntimeError('CampaignWriterRetireIdentity')
        self.retired|=1<<identity
        for path in group['paths']:self.budget.slots.pop(path,None)
        del self.active[identity]
        # No class/file/byte reservation is reduced or reusable.
    def close_case(self,folder):
        for group in tuple(self.active.values()):
            if group['shared']==str(folder):self.retire(group)


def _campaign_gate_environment(logical):
    # Harness startup ONLY; same-PID finalexec selects the ORIGINAL logical env.
    return {**logical,'SETUPTOOLS_USE_DISTUTILS':'stdlib'}


def _campaign_pair():
    _campaign_features()
    a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET|socket.SOCK_CLOEXEC)
    try:
        for s in (a,b):s.setblocking(False);s.set_inheritable(False);s.setsockopt(socket.SOL_SOCKET,socket.SO_PASSCRED,1)
        return a,b
    except BaseException:a.close();b.close();raise


def _campaign_live(fd):
    if type(fd) is not int or fd<0 or os.get_inheritable(fd):raise RuntimeError('CampaignPidfdBinding')
    signal.pidfd_send_signal(fd,0)


def _campaign_wait_socket(s,event,end):
    _campaign_clock(end)
    with selectors.DefaultSelector() as selector:
        selector.register(s,event)
        selector.select(max(0,min(.01,(end-time.monotonic_ns())/1000000000)))
    _campaign_clock(end)


def _campaign_send(s,value,end,fd=None,maximum=256):
    # Tiny exact-source packets only; no repr/default callback or raw recipe.
    raw=bytearray()
    for part in _json_parts(value):
        b=part.encode('ascii')
        if len(raw)+len(b)>maximum:raise RuntimeError('CampaignPacketBound')
        raw.extend(b)
    ancillary=[] if fd is None else [(socket.SOL_SOCKET,socket.SCM_RIGHTS,struct.pack('i',fd))]
    while True:
        _campaign_clock(end)
        try:
            if s.sendmsg([raw],ancillary)!=len(raw):raise RuntimeError('CampaignPacketShortWrite')
            return bytes(raw)
        except BlockingIOError:_campaign_wait_socket(s,selectors.EVENT_WRITE,end)


class _CampaignFrameError(RuntimeError):
    """Bounded literal failed frame DATA; never a retained FD/capability."""
    __slots__=('raw','flags','credentials_count','fds_count','ancillary_empty')
    def __init__(self,raw,flags,credentials_count,fds_count,*,ancillary_empty=False):
        super().__init__('CampaignAuthenticatedFrame')
        self.raw=raw;self.flags=flags;self.credentials_count=credentials_count;self.fds_count=fds_count;self.ancillary_empty=ancillary_empty


def _campaign_recv(s,peer,end,with_fd=False,maximum=256):
    """Authenticate each actual sender; close every received FD on refusal."""
    while True:
        _campaign_clock(end)
        try:
            raw,ancillary,flags,address=s.recvmsg(maximum+1,socket.CMSG_SPACE(12)+socket.CMSG_SPACE(4),socket.MSG_CMSG_CLOEXEC)
            break
        except BlockingIOError:_campaign_wait_socket(s,selectors.EVENT_READ,end)
    received=[];credentials=[];bad=False
    try:
        for level,kind,data in ancillary:
            if level!=socket.SOL_SOCKET:bad=True;continue
            if kind==socket.SCM_RIGHTS:
                if len(data)%4:bad=True
                for offset in range(0,len(data)-len(data)%4,4):received.append(struct.unpack_from('i',data,offset)[0])
            elif kind==socket.SCM_CREDENTIALS:
                if len(data)!=12:bad=True
                else:credentials.append(struct.unpack('3i',data))
            else:bad=True
        fd_count_ok=(len(received) in (0,1)) if with_fd is None else (len(received)==(1 if with_fd else 0))
        if not raw or len(raw)>maximum or flags&(socket.MSG_TRUNC|socket.MSG_CTRUNC) or bad or credentials!=[peer] or not fd_count_ok:raise RuntimeError('CampaignAuthenticatedFrame')
        for fd in received:
            if os.get_inheritable(fd):raise RuntimeError('CampaignReceivedFdCloexec')
            os.set_inheritable(fd,False);_campaign_live(fd)
        value=bounded_json_loads(raw,maximum)
        if type(value) is not dict:raise RuntimeError('CampaignPacketType')
        _campaign_clock(end)
        return value,(received.pop() if received else None),raw
    except BaseException as error:
        # Close all ancillary capabilities in finally before this bounded raw
        # diagnostic reaches its source-owned transcript writer.
        raise _CampaignFrameError(raw,flags,len(credentials),len(received),ancillary_empty=not ancillary) from error
    finally:
        for fd in received:os.close(fd)


def _campaign_signal(fd,sig,process):
    # Only the producer's genuine retained, unreaped Popen child can reach here.
    # WNOWAIT observes exit without releasing the identity used for signaling.
    if process.returncode is not None:raise RuntimeError('CampaignSignalAfterReap')
    if os.waitid(os.P_PID,process.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT) is not None:return False
    _campaign_live(fd);signal.pidfd_send_signal(fd,sig);return True


def _campaign_open_child(process):
    if type(process) is not subprocess.Popen or process.returncode is not None:raise RuntimeError('CampaignActualPopenRequired')
    fd=os.pidfd_open(process.pid,0)
    try:
        os.set_inheritable(fd,False)
        # Do not poll/wait/reap the child before binding. A fast failed helper
        # can be a retained zombie; signal(0) alone cannot prove it is waiting.
        if os.waitid(os.P_PID,process.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT) is not None:raise RuntimeError('CampaignGateExitedBeforeBinding')
        _campaign_live(fd)
        return fd
    except BaseException:os.close(fd);raise


class _CampaignChild:
    __slots__=('process','pidfd','seq','index','end','signal_open','whole','gate_env')


class _PreparationSlot:
    __slots__=('number','target','source','evidence','origin','hard_end','traffic_end','preparation','state')
    def __init__(self):raise TypeError('GenuineCampaignPreparationSlotOnly')


class _QualifiedRuntime:
    __slots__=('campaign','key','interpreter','inventory_path','inventory_pin','source_hash')
    def __init__(self):raise TypeError('GenuineQualifiedRuntimeOnly')


def _runtime_validation_refusal(error):
    # Pure classification DATA, shared by actual verification and affected controls.
    args=BaseException.args.__get__(error)
    message=args[0] if len(args)==1 and type(args[0])is str else None
    return type(error)is RuntimeError and message is not None and (message in ('VenvRoot','ExactVenvConfig','ExactCopiedAliasAndScriptSet','VenvConfig','VenvConfigExact','VenvExtraRoot','VenvForeignOwner','VenvWritableByOther','VenvSymlink')or message.startswith(('CopiedAlias:','VenvCacheOrCustomization:','VenvUnexpectedFile:','ChangedInput:','ChangedRights:')))


class _CampaignAdmission:
    """Real private resource admission, NEVER a TEST/P permit or stop token."""
    __slots__=('role','source_sha','manifest','descriptor','expected','expected_charge','start','end','traffic_end','nonce','arena','budget','socket','parentfd','peer','seq','active','retired','slot','case','case_number','case_index','qualified','aborted','abort_sent','reason','first_fault','cleanup_end','bootstrap_facts','binding','disk_facts')
    def __init__(self):raise TypeError('FixedSourceCampaignProducerOnly')
    @classmethod
    def _mint(cls,role,source_sha,start,end):
        global _CAMPAIGN_CURRENT
        if _R5_REG_CURRENT is not None or _ENTRY_DATA_CURRENT is not None or _CAMPAIGN_CURRENT is not None or role not in ('owner','coordinator') or type(start) is not int or type(end) is not int or end-start!=600000000000:raise RuntimeError('CampaignSingleProducer')
        arena=_CampaignArena();arena.hold('fixed-coordinator-state' if role=='coordinator' else 'joint-owner-source-live',2097152 if role=='coordinator' else 1572864)
        manifest=_campaign_manifest(source_sha);descriptor=_campaign_plan(manifest)
        expected,charge=_campaign_expected(manifest)
        value=object.__new__(cls)
        value.role=role;value.source_sha=source_sha;value.manifest=manifest;value.descriptor=descriptor;value.expected=expected;value.expected_charge=charge
        value.start=start;value.end=end;value.traffic_end=end-2000000000;value.nonce=manifest['nonce']
        value.arena=arena
        value.budget=None;value.socket=None;value.parentfd=None;value.peer=None;value.seq=0;value.active=None;value.retired=[];value.slot=None;value.case=None;value.case_number=0;value.case_index=0;value.qualified={}
        value.aborted=False;value.abort_sent=False;value.reason=None;value.first_fault=None;value.cleanup_end=None;value.bootstrap_facts=None;value.binding=None;value.disk_facts=None
        _CAMPAIGN_CURRENT=value
        try:
            _campaign_input_guard(value)
            value.budget=value.admit(Path(descriptor['evidence']))
            value.qualify_baseline()
            value.disk_guard()
            _campaign_clock(value.traffic_end)
            return value
        except BaseException:
            value.fatal('CampaignAdmissionFailure');raise
    def check(self,end=None):
        if not _actual_campaign(self) or self.aborted:raise RuntimeError('CampaignAbortedNoFurtherEffects')
        _campaign_clock(self.traffic_end if end is None else min(end,self.traffic_end))
    def disk_guard(self):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        self.disk_facts=_r19_physical_guard(self)
    def fatal(self,reason):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        if self.aborted:return
        self.aborted=True;self.reason=reason if type(reason) is str and len(reason)<=128 else 'CampaignFatal'
        self.first_fault=time.monotonic_ns()
        active_end=self.active.end if self.active is not None else self.traffic_end
        self.cleanup_end=min(self.first_fault+2000000000,active_end+2000000000,self.end)
        if self.role=='coordinator' and self.socket is not None and not self.abort_sent:
            self.abort_sent=True
            try:
                _campaign_send(self.socket,dict(k='B',n=self.nonce,s=self.seq,i=self.active.index if self.active is not None else 0),self.cleanup_end,maximum=128)
            except BaseException:pass  # Actual owner EOF/fault path owns settlement.
    def admit(self,root,slot=None):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        self.check()
        root=Path(root)
        if slot is None:
            if root!=Path(self.descriptor['evidence']):raise RuntimeError('CampaignAdmissionRoot')
        elif slot is not self.slot or type(slot) is not _PreparationSlot or slot.preparation is None or root!=slot.evidence:raise RuntimeError('CampaignClosedPreparationSlot')
        _r11_verify_capacity(self)
        if 26022808+sum(v[0]for v in R19_CLASS_LIMITS.values())+R11_LIVE_SOURCE_GROWTH>R19_EVIDENCE_LIMIT or 1376+sum(v[1]for v in R19_CLASS_LIMITS.values())>R19_EVIDENCE_FILES:raise RuntimeError('EvidenceFutureEnvelopeFit')
        if self.budget is None:
            if self.role=='owner':
                t=Path(self.descriptor['root']);e=Path(self.descriptor['evidence'])
                if any(p.exists() or p.is_symlink() for p in (t,e)):raise RuntimeError('CampaignNoClobberRoot')
                for variant,name,_,_,_ in _campaign_rows():
                    if name in dict(CAMPAIGN_CONFIGURED):continue
                    case_root=Path(_campaign_case_root(self.descriptor,variant,name))
                    if any(p.exists() or p.is_symlink() for p in (case_root,Path(str(case_root)+'-ledger'))):raise RuntimeError('CampaignNoClobberCase')
            budget=EvidenceBudget([Path(self.descriptor['evidence'])],26022808,1376,campaign=self)
            global _ACTIVE_BUDGET
            if _ACTIVE_BUDGET is not None:raise RuntimeError('CampaignSingleBudget')
            _ACTIVE_BUDGET=budget
            return budget
        return self.budget
    def begin_case(self,name,folder,interpreter,inventory,root,origin):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        self.check()
        if self.role!='coordinator' or self.case is not None or self.slot is not None or self.active is not None:raise RuntimeError('CampaignCaseOverlap')
        variant,wanted,label,op,arg=_campaign_case_row(self.case_index+1)
        if name!=wanted or Path(folder)!=_campaign_case_folder(self.descriptor,variant,name) or root!=_campaign_case_root(self.descriptor,variant,name):raise RuntimeError('CampaignCaseBinding')
        runtime=self.qualified.get(('variant',variant) if variant else ('poison',name) if name.startswith('deployment-') else ('baseline',0))
        if runtime is None or inventory is not runtime or interpreter!=runtime.interpreter:raise RuntimeError('CampaignActualQualifiedRuntime')
        self.case_number+=1
        if self.case_number>55:raise RuntimeError('CampaignCaseCardinality')
        scope=_CaseScope(self,self.case_number);self.case=(scope,Path(folder),name,variant)
        return scope
    def baseline(self):
        self.check()
        record=self.qualified[('baseline',0)]
        self.verify_runtime(record.interpreter,record)
        return record.interpreter,record
    def prepare(self,number):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        origin=time.monotonic_ns();self.check()
        if self.role!='coordinator' or self.case is not None or self.slot is not None or self.active is not None:raise RuntimeError('CampaignPreparationOverlap')
        variant,poison=_campaign_stage(number)
        if _campaign_slot_order(self.seq+1)!=120+8*number:raise RuntimeError('CampaignPreparationOrder')
        target,source,evidence=_campaign_runtime(self.descriptor,variant,poison)
        key=('variant',variant) if variant else ('poison',poison)
        if key in self.qualified:raise RuntimeError('CampaignPreparationReused')
        slot=object.__new__(_PreparationSlot)
        slot.number=number;slot.target=target;slot.source=source;slot.evidence=evidence;slot.origin=origin
        slot.hard_end=min(origin+120000000000,self.end);slot.traffic_end=min(slot.hard_end-2000000000,self.traffic_end)
        slot.preparation=None;slot.state='CREATING';self.slot=slot
        try:
            context=Preparation(target,evidence,self.expected,origin=origin/1000000000,earlier_end=slot.traffic_end/1000000000,campaign=self,slot=slot)
            if variant:context.stage_variant()
            slot.state='PREPARING'
            return context
        except BaseException:self.fatal('CampaignPreparationSetupFailure');raise
    def finish_preparation(self,context):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        self.check()
        slot=self.slot
        if slot is None or type(context) is not Preparation or slot.preparation is not context or context.campaign is not self or slot.state!='PREPARING' or self.active is not None:raise RuntimeError('ActualPreparationCompletion')
        # Canonical caller invokes this only AFTER deploy's frame (and every
        # borrowed map/tree) returned. Failure frames never refund these holds.
        context._release_metadata_after_deploy_frame()
        context.check()
        if len(context.calls)!=8 or len(context.call_paths)!=8 or len(_CAPTURES):raise RuntimeError('CampaignEightSettledCalls')
        for index,reference in enumerate(context.calls):
            if reference['exit']!=0 or reference['failure'] is not None or reference['partial_prefix'] or reference['slot']!=120+8*slot.number+index:raise RuntimeError('CampaignPreparationActualReceipt')
            same(reference['path'],reference['pin'])
        context.preflight_inputs()
        binding=self.load_binding();variant,poison=_campaign_stage(slot.number)
        deployment=slot.evidence/'deployment.json';inventory_path=slot.evidence/'deployment-inventory.json'
        if deployment.stat().st_size>262144 or inventory_path.stat().st_size>65536:raise RuntimeError('CampaignQualifiedMetadataBound')
        deployment_pin=pin(deployment)
        raw=deployment.read_bytes();facts=self.arena.decode('prepared-deployment',raw,262144);del raw
        wanted_hash=hashlib.sha256()
        for name in SOURCE_NAMES:
            value=context.source_pin(context.source/name.removeprefix('reference_controller/')) if name.startswith('reference_controller/') else context.source_pin(context.repository/PROVIDERS[name][0])
            wanted_hash.update(name.encode('ascii')+b'\0'+bytes.fromhex(value['sha256']))
        source_hash=wanted_hash.hexdigest();interpreter=slot.target/'venv/bin/python'
        if facts['source_hash']!=source_hash or facts['interpreter']!=str(interpreter) or facts['interpreter_pin']!=pin(interpreter) or facts['master']!=binding['master'] or facts['static_fixture']!=binding['fixture']:raise RuntimeError('CampaignPreparedSourceLineage')
        same(deployment,dict(**deployment_pin,**rights(deployment)))
        del facts;self.arena.release('prepared-deployment')
        record=object.__new__(_QualifiedRuntime);record.campaign=self;record.key=('variant',variant) if variant else ('poison',poison)
        record.interpreter=interpreter;record.inventory_path=inventory_path;record.inventory_pin=dict(**pin(inventory_path),**rights(inventory_path));record.source_hash=source_hash
        self.qualified[record.key]=record
        self.verify_runtime(interpreter,record)
        # No Preparation/calls/argv/origin/CompletedProcess tree is retained in
        # the registry. The remaining qualified record is a compact identity
        # latch and fixed immutable inventory pin, never recreated authority.
        context.calls.clear();context.call_paths.clear();context.expected=None;context.env.clear();context.finished=True
        slot.state='QUALIFIED';slot.preparation=None;context.slot=None;self.slot=None
        return interpreter,record
    def load_binding(self):
        if self.binding is not None:return self.binding
        path=_R11_FREEZE/'baseline-v17-binding.json'
        if _entry_data_actual(self):
            if type(self.baseline_sha)is not str or re.fullmatch('[0-9a-f]{64}',self.baseline_sha)is None or pin(path)['sha256']!=self.baseline_sha or rights(path)!=dict(mode=384,uid=1000,gid=1000):raise RuntimeError('R11ExternalBaselineAnchor')
        elif not _actual_campaign(self):raise RuntimeError('R11GenuineBaselineConsumer')
        if path.stat().st_size>32768:raise RuntimeError('R11BaselineBound')
        raw=path.read_bytes()
        if _entry_data_actual(self):
            text,expected_charge=_json_prepared(raw,32768)
            del text
            self.baseline_expected_charge=expected_charge
        value=self.arena.decode('frozen-baseline-binding',raw,32768)
        if set(value)!={'schema','inventory','typed_inventory','deployment','marker','code','variants','source_hash','plan_hash','fixture','master','external_ROOT_review','qualification'} or value['schema']!='wordling.controller-campaign-v17-binding/v1':raise RuntimeError('CampaignBaselineSchema')
        if set(value['code'])!=set(SOURCE_NAMES) or set(value['variants'])!=set(CAMPAIGN_MUTANTS):raise RuntimeError('Campaign20SourceBindings')
        source=Path(__file__).resolve().parent.parent;repository=source.parents[3];digest=hashlib.sha256()
        for name in SOURCE_NAMES:
            original=source/name.removeprefix('reference_controller/') if name.startswith('reference_controller/') else repository/PROVIDERS[name][0]
            wanted={k:self.expected['files'][str(original)][k] for k in ('size','sha256')}
            if value['code'][name]!=wanted:raise RuntimeError('CampaignBaselineNotIndependentSource')
            digest.update(name.encode('ascii')+b'\0'+bytes.fromhex(wanted['sha256']))
        if digest.hexdigest()!=value['source_hash'] or value['source_hash']!='d734ebc970109410f2ea829773a2aa3292c4717d0ac331fc926d70eead9a3b32' or value['plan_hash']!='f4184623a3334cde4e981ae6998b9c6e578c2201660e6e57f8b17e8a50c445cb':raise RuntimeError('CampaignBaselineLineage')
        for name,(file,old,new,target,marker) in CAMPAIGN_MUTANTS.items():
            raw=(source/file).read_bytes();text=raw.decode('utf8')
            if text.count(old)!=1:raise RuntimeError('CampaignUniqueMutantPreimage')
            post=text.replace(old,new).encode('utf8')
            if value['variants'][name]!=dict(file=file,size=len(post),sha256=hashlib.sha256(post).hexdigest()):raise RuntimeError('CampaignFrozenMutantPostimage')
        if _entry_data_actual(self):
            inventory=value['inventory'];path=_R11_TARGET/'receipts/deployment/deployment-inventory.json'
            if inventory['path']!=str(path)or inventory['size']>65536:raise RuntimeError('R11EntryInventoryInput')
            same(path,inventory);raw=path.read_bytes();text,charge=_json_prepared(raw,65536)
            self.inventory_expected_initial=12*len(raw)+4096
            self.inventory_expected_additional=max(0,charge+4*len(raw)-self.inventory_expected_initial)
            del raw,text
        self.binding=value
        return value
    def _baseline200(self,typed):
        wanted=self.load_binding()['typed_inventory'] if _entry_data_actual(self)else dict(path=str(_R11_FREEZE/'input-custody.json'),**self.manifest['members']['input-custody.json'])
        if typed!=wanted or typed['path']!=str(_R11_FREEZE/'input-custody.json')or typed['size']>65536:raise RuntimeError('R11TypedFixedInput')
        same(typed['path'],typed)
        self.arena.hold('baseline-typed200-raw',typed['size']+8192)
        with Path(typed['path']).open('rb')as stream:raw=stream.read(typed['size']+1)
        if len(raw)!=typed['size']:raise RuntimeError('R5TypedBound')
        data=self.arena.decode('baseline-typed200',raw,65536);rows=data['entries']
        if data['schema']!='wordling.wp70.r11-qualified-v17-input-custody/v1'or len(rows)!=200 or any(r['root']!='runtime'for r in rows):raise RuntimeError('R5ExactTypedRoot')
        if sum(r['type']=='file'for r in rows)!=167 or sum(r['type']=='directory'for r in rows)!=32 or sum(r['type']=='symlink'for r in rows)!=1:raise RuntimeError('CampaignBaseline200Types')
        if {str(p.relative_to(_R11_TARGET))for p in _R11_TARGET.rglob('*')}!={r['relative']for r in rows}:raise RuntimeError('CampaignBaselineClosedRuntime')
        for row in rows:
            p=_R11_TARGET/row['relative']
            if rights(p)!={k:row[k]for k in ('mode','uid','gid')}:raise RuntimeError('CampaignBaselineRights')
            if row['type']=='file':same(p,dict(size=row['bytes'],sha256=row['sha256'],mode=row['mode'],uid=row['uid'],gid=row['gid']))
            elif row['type']=='directory':
                if p.is_symlink()or not p.is_dir():raise RuntimeError('CampaignBaselineDirectory')
            elif p!=_R11_TARGET/'venv/lib64'or not p.is_symlink()or os.readlink(p)!='lib'or p.resolve()!=_R11_TARGET/'venv/lib':raise RuntimeError('CampaignBaselineAlias')
            self.check()
    def qualify_baseline(self):
        binding=self.load_binding();inventory_path=_R11_TARGET/'receipts/deployment/deployment-inventory.json'
        if binding['inventory']['path']!=str(inventory_path)or binding['inventory']['size']>65536:raise RuntimeError('R11Fixed188Inventory')
        review=binding['external_ROOT_review']
        if set(review)!={'root','seal_size','seal_sha256','files','bytes','ROOT_only','kind'}or review['root']!=str(_R11_QUAL_ROOT/'review')or review['files']!=8 or not 0<review['bytes']<=262144 or not 0<review['seal_size']<=65536 or re.fullmatch('[0-9a-f]{64}',review['seal_sha256'])is None or review['ROOT_only']is not True or review['kind']!='ACCEPTED_READONLY_V16_BASELINE_SEPARATE_GATES':raise RuntimeError('R11ExternalQualificationReviewBinding')
        qualification=binding['qualification']
        labels=('venv','qualify-literal-before','stdlib-before','compile','wheel','install','qualify-literal-after','origins')
        if set(qualification)!={'owner','stages'}or set(qualification['stages'])!=set(labels):raise RuntimeError('R11ActualEightQualificationReceipts')
        for label,row in [('owner',qualification['owner']),*qualification['stages'].items()]:
            path=_R11_QUAL_ROOT/'owner/whole.json'if label=='owner'else _R11_TARGET/'receipts/deployment'/(label+'.whole.json')
            if set(row)!={'path','size','sha256','mode','uid','gid'}or row['path']!=str(path)or row['size']>65536:raise RuntimeError('R11QualificationReceiptPin')
            same(path,row);raw=path.read_bytes();facts=self.arena.decode('qualification-receipt',raw,65536);del raw
            if facts['exit']!=0:raise RuntimeError('R11QualificationStageNotSuccessful')
            if label=='owner':
                if not facts['cleanup_qualified']or facts['unknown_cleanup_hold']or facts['partial_prefix']or not facts['coordinator_reaped_last']:raise RuntimeError('R11QualificationOwnerUNKNOWN')
            elif facts['failure']is not None or facts['partial_prefix']:raise RuntimeError('R11QualificationStagePartial')
            del facts;self.arena.release('qualification-receipt')
        self._baseline200(binding['typed_inventory'])
        self.arena.release('baseline-typed200');self.arena.release('baseline-typed200-raw')
        for field,path in (('deployment',_R11_TARGET/'receipts/deployment/deployment.json'),('marker',_R11_TARGET/'venv/wordling-test-deployment.json')):
            if binding[field]['path']!=str(path):raise RuntimeError('CampaignBaselineFixedArtifact')
            same(path,binding[field])
        record=object.__new__(_QualifiedRuntime);record.campaign=self;record.key=('baseline',0);record.interpreter=_R11_TARGET/'venv/bin/python';record.inventory_path=inventory_path;record.inventory_pin={k:binding['inventory'][k]for k in ('size','sha256','mode','uid','gid')};record.source_hash=binding['source_hash']
        self.qualified[record.key]=record;self.verify_runtime(record.interpreter,record)
    def verify_runtime(self,interpreter,record):
        name='active-runtime188';already=name in self.arena.holds
        try:
            self.check()
            if type(record) is not _QualifiedRuntime or record.campaign is not self or self.qualified.get(record.key) is not record or interpreter!=record.interpreter:raise RuntimeError('ActualQualifiedRuntimeIdentity')
            same(record.inventory_path,record.inventory_pin)
            raw=record.inventory_path.read_bytes();inventory=self.arena.decode(name,raw,65536);del raw
            if len(inventory)!=188:raise RuntimeError('Campaign188InventoryCardinality')
        except BaseException:
            if not already and name in self.arena.holds and self.case is not None and name not in self.case[0].names:self.case[0].names.append(name)
            self.fatal('RuntimeInventoryAcquisitionFailure');raise
        try:
            strict_layout(interpreter,inventory)
            for path,wanted in inventory.items():
                same(path,wanted)
                try:self.check()
                except BaseException:self.fatal('RuntimeInventoryClockOrIdentity');raise
        except BaseException as error:
            if self.case is not None and name not in self.case[0].names:self.case[0].names.append(name)
            if not _runtime_validation_refusal(error):self.fatal('RuntimeInventoryValidationFailure')
            raise
        else:
            del inventory
            self.arena.release(name)
    def end_case(self,scope):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        if self.case is None or self.case[0] is not scope:raise RuntimeError('CampaignCaseScopeIdentity')
        self.budget._campaign_book.close_case(self.case[1]);self.case=None
    def case_slot(self,label):
        self.check()
        if self.case is None:raise RuntimeError('ActualCaseRequired')
        index=self.case_index+1;variant,name,wanted,op,arg=_campaign_case_row(index)
        if (name,variant)!=(self.case[2],self.case[3]) or label!=wanted:raise RuntimeError('CampaignCaseCommandOrder')
        return index
    def launch(self,index,argv,cwd,env,end,trace=-1,*,fsize=None):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        self.check(end)
        if self.role!='coordinator' or self.active is not None or self.socket is None or self.seq>=199 or index!=_campaign_slot_order(self.seq+1):raise RuntimeError('CampaignActualLaunchOrder')
        command=_campaign_command(self.manifest,'slot',index,trace)
        if fsize is not None and(type(fsize)is not int or fsize!=command['fsize']):raise RuntimeError('CampaignClosedFileCeiling')
        if argv!=command['argv'] or str(cwd)!=command['cwd'] or env!=command['env']:raise RuntimeError('CampaignClosedCommandPostimage')
        if index<=119:
            if self.case is None or index!=self.case_index+1:raise RuntimeError('CampaignCaseProducer')
        elif self.slot is None or self.slot.preparation is None or index!=120+8*self.slot.number+len(self.slot.preparation.calls):raise RuntimeError('CampaignPreparationProducer')
        self.seq+=1;release,child_release=_campaign_pair();process=None;pidfd=None
        gated=_campaign_gate_args(self.source_sha,'slot',index,self.seq,child_release.fileno(),self.nonce,end,trace=trace)
        try:
            self.check(end)
            gate_env=_campaign_gate_environment(env)
            process=subprocess.Popen(gated,cwd=cwd,env=gate_env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True,pass_fds=(child_release.fileno(),)+( (trace,) if trace!=-1 else ()),start_new_session=False)
            child_release.close()
            pidfd=_campaign_open_child(process)
            child=object.__new__(_CampaignChild);child.process=process;child.pidfd=pidfd;child.seq=self.seq;child.index=index;child.end=end;child.signal_open=True;child.whole=None;child.gate_env=gate_env
            self.active=child
            _campaign_send(self.socket,dict(k='R',v=1,n=self.nonce,s=self.seq,i=index,e=end,c=True),end,fd=pidfd)
            ack,received,raw=_campaign_recv(self.socket,self.peer,end,False,128)
            wanted=dict(k='A',n=self.nonce,s=self.seq,i=index,e=end)
            if received is not None or ack!=wanted:raise RuntimeError('CampaignRegistrationACK')
            self.check(end);_campaign_send(release,wanted,end,maximum=128);release.close()
            if index<=119:self.case_index=index
            return process
        except BaseException:
            # Never fabricate a registered child/FD if Popen/binding failed.
            # Absence of a returned Popen object is NOT proof no kernel prefix.
            if process is None:
                try:_campaign_send(self.socket,dict(k='R',v=1,n=self.nonce,s=self.seq,i=index,e=end,c=False),min(self.end,time.monotonic_ns()+2000000000))
                except BaseException:pass
            self.fatal('CampaignLaunchOrGateFailure')
            raise
        finally:
            release.close();child_release.close()
            if pidfd is not None and (self.active is None or self.active.pidfd!=pidfd):os.close(pidfd)
    def signal_child(self,process,sig):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        child=self.active
        if child is None or child.process is not process or not child.signal_open:raise RuntimeError('ActualRetainedCampaignChild')
        return _campaign_signal(child.pidfd,sig,process)
    def child_facts(self,process):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        child=self.active
        if child is None or child.process is not process:raise RuntimeError('ActualCampaignChildFacts')
        return dict(gated_initial_argv=list(process.args),requested_final_argv=_campaign_command(self.manifest,'slot',child.index)['argv'] if child.index<=119 else None,
            gated_startup_env=child.gate_env,final_logical_env='exact separately source-selected command env; startup overlay is discarded before final exec',
            gate_helper=dict(path=str(Path(__file__).resolve()),**pin(Path(__file__).resolve())),
            gate_interpreter=dict(path=str(BASE),**pin(BASE)),registered_actual_child=True,
            registration_ACK_received=True,release_ACK_sent=True,final_exec='UNKNOWN/not inferred from ACK',seq=child.seq,slot=child.index,
            end_ns=child.end,pidfd_signal_lifecycle_open=child.signal_open)
    def complete_child(self,process,whole):
        if not _actual_campaign(self):raise RuntimeError('ProductionAdmissionIdentityRequired')
        child=self.active
        if child is None or child.process is not process or process.returncode is None:raise RuntimeError('CampaignActualExitedChild')
        self.check(child.end);child.signal_open=False;child.whole=Path(whole)
        if len(self.retired)>=199:raise RuntimeError('CampaignRetiredBound')
        _campaign_send(self.socket,dict(k='I',n=self.nonce,s=child.seq,i=child.index,r=process.returncode),child.end,maximum=128)
        barrier_end=min(child.end,self.end,time.monotonic_ns()+2000000000)
        try:
            ack,fd,raw=_campaign_recv(self.socket,self.peer,barrier_end,False,128)
            if fd is not None or ack!=dict(k='i',n=self.nonce,s=child.seq,i=child.index,e=child.end):raise RuntimeError('CampaignIdleBarrierACK')
            self.check(child.end)
        except BaseException:
            self.fatal('CampaignIdleBarrierFailure');self.cleanup_end=min(self.cleanup_end,barrier_end);raise
        os.close(child.pidfd)
        self.retired.append((child.seq,child.index,process.returncode,str(whole),pin(whole)['sha256']))
        self.active=None


_ENTRY_DATA_CURRENT=None
_ENTRY_DATA_USED=False


class _EntryDataBoundary(RuntimeError):
    pass


def _entry_data_actual(value):
    return type(value)is _EntryData and value is _ENTRY_DATA_CURRENT


class _EntryData:
    """One checksum-bound readonly DATA context, never production admission."""
    __slots__=('arena','expected','binding','qualified','case','aborted','reason','traffic_end','vector','boundary','baseline_sha','baseline_expected_charge','inventory_expected_initial','inventory_expected_additional')
    def __init__(self):raise TypeError('PrivateEntryDataFactoryOnly')
    _baseline200=_CampaignAdmission._baseline200
    load_binding=_CampaignAdmission.load_binding
    qualify_baseline=_CampaignAdmission.qualify_baseline
    verify_runtime=_CampaignAdmission.verify_runtime
    def check(self):
        if not _entry_data_actual(self)or self.aborted:raise RuntimeError('EntryDataIdentityOrFatal')
        _campaign_clock(self.traffic_end)
    def fatal(self,reason):
        if not self.aborted:self.aborted=True;self.reason=reason
    def begin_case(self,name,folder,interpreter,inventory,root,origin):
        self.check()
        record=self.qualified[('baseline',0)]
        if self.case is not None or name!='DATA-entry-'+str(self.vector)or folder!=Path('/tmp/wordling-WP70-helper-io-controls-r11')or root!=str(folder)or inventory is not record or interpreter!=record.interpreter:raise RuntimeError('EntryDataActualCaseBinding')
        scope=_CaseScope(self,self.vector);self.case=(scope,folder,name,0);return scope
    def end_case(self,scope):
        if not _entry_data_actual(self)or self.case is None or self.case[0]is not scope:raise RuntimeError('EntryDataCaseIdentity')
        self.case=None


def _entry_data_initialize(vector,qsha,rsha,end,*,baseline_sha=None):
    global _ENTRY_DATA_CURRENT,_ENTRY_DATA_USED
    if _ENTRY_DATA_USED:raise RuntimeError('EntryDataFactorySpent')
    _ENTRY_DATA_USED=True
    runner=sys.modules.get('__main__');path=Path(__file__).with_name('run_controller_acceptance.py')
    if type(vector)is not int or vector not in (1,2,3)or type(end)is not int or not 0<end-time.monotonic_ns()<=10000000000:raise RuntimeError('EntryDataClosedVectorClock')
    if _R5_REG_CURRENT is not None or _CAMPAIGN_CURRENT is not None or _ACTIVE_BUDGET is not None or _CAPTURES or runner is None or Path(runner.__file__).resolve()!=path.resolve():raise RuntimeError('EntryDataNoProductionOrAlias')
    for source,sha in ((Path(__file__),qsha),(path,rsha)):
        if type(sha)is not str or re.fullmatch('[0-9a-f]{64}',sha)is None or pin(source)['sha256']!=sha:raise RuntimeError('EntryDataExactSource')
    if str(Path(sys.executable).resolve())!=str(BASE.resolve())or not sys.flags.dont_write_bytecode:raise RuntimeError('EntryDataPinnedBASEFlags')
    same(_R5_ADMISSION,_R5_CARRIER);carrier=_r11_carrier()
    same(FREEZE/'expected-inputs.json.gz',carrier['expected_base'])
    if type(baseline_sha)is not str or re.fullmatch('[0-9a-f]{64}',baseline_sha)is None:raise RuntimeError('R11ExternalBaselineChecksumRequired')
    baseline_path=_R11_FREEZE/'baseline-v17-binding.json'
    if pin(baseline_path)['sha256']!=baseline_sha or rights(baseline_path)!=dict(mode=384,uid=1000,gid=1000):raise RuntimeError('R11ExternalBaselineAnchor')
    value=object.__new__(_EntryData);value.arena=_CampaignArena();value.arena.hold('fixed-coordinator-state',2097152)
    value.expected=load_expected();value.expected['files'][str(_R5_PROVIDER)]=dict(carrier['provider']['current']);value.expected['files'][str(Path(__file__).resolve().parent.parent/'controller.py')]=dict(size=26867,sha256='8c4f7de700ff3c236f1db93fdbcb4ffe02b298646286f0659bfbf6f6a68c142c',mode=436,uid=1000,gid=1000);value.expected['approved_providers']=dict(value.expected['approved_providers']);value.expected['approved_providers']['scripts/reference/startup_family/lifetime.py']=_R5_COMMIT;value.binding=None;value.qualified={};value.case=None;value.aborted=False;value.reason=None;value.traffic_end=end;value.vector=vector;value.boundary=None;value.baseline_sha=baseline_sha;value.baseline_expected_charge=None;value.inventory_expected_initial=None;value.inventory_expected_additional=None
    value.expected['files']['/etc/ld.so.cache']={'size':150747,'sha256':'c1dbbf1efb0a2e4e39124d1c6b296f25bb11008095945378714188dff359f320','mode':420,'uid':0,'gid':0}
    _ENTRY_DATA_CURRENT=value
    # This is the real readonly qualification path and genuine runtime registry;
    # no fake Preparation, CampaignAdmission, P permit, budget or launch exists.
    value.qualify_baseline();value.check()
    return value


def _entry_data_boundary(case):
    host=case.campaign
    if _actual_campaign(host):return
    if not _entry_data_actual(host)or host.case is None or host.case[0]is not case.scope:raise RuntimeError('EntryDataBoundaryIdentity')
    host.check();host.boundary=dict(arena_used=host.arena.used,inventory_live='active-runtime188'in host.arena.holds,capture_live=5505024 in host.arena.holds.values(),scope_holds=len(case.scope.names))
    raise _EntryDataBoundary('EXPECTED_DATA_CAPTURE_BOUNDARY_NO_CHILD')


def _campaign_owner_admission(source_sha):
    origin=time.monotonic_ns()
    return _CampaignAdmission._mint('owner',source_sha,origin,origin+600000000000)


def campaign_bootstrap():
    channel,parentfd,parent,end,source_sha=_campaign_bootstrap_descriptors()
    campaign=_CampaignAdmission._mint('coordinator',source_sha,end-600000000000,end)
    campaign.socket=channel;campaign.parentfd=parentfd;campaign.peer=(parent,os.getuid(),os.getgid())
    campaign.bootstrap_facts=dict(control_fd=channel.fileno(),owner_pidfd=parentfd,actual_parent=parent,cloexec_restored_before_child_paths=True,source_sha256=source_sha,whole_end_ns=end,execution_parent_end_ns=campaign.traffic_end)
    try:
        _campaign_hello(channel,campaign.peer,campaign.nonce,source_sha,campaign.manifest['sources'][str(Path(__file__).resolve())]['sha256'],end,campaign.traffic_end)
        campaign.check()
        return campaign
    except BaseException:campaign.fatal('CampaignBootstrapFailure');raise


def _campaign_bootstrap_descriptors():
    # Restore CLOEXEC FIRST, before any child-capable path. Fixed fd roles were
    # created by the authentic same-PID rootgate; no caller recipe is accepted.
    names=('WORDLING_CAMPAIGN_CONTROL_FD','WORDLING_CAMPAIGN_OWNER_PIDFD','WORDLING_CAMPAIGN_OWNER','WORDLING_CAMPAIGN_END','WORDLING_CAMPAIGN_SOURCE')
    if any(n not in os.environ for n in names):raise RuntimeError('ActualCampaignRootGateRequired')
    control,parentfd,parent,end,source_sha=(os.environ.pop(n) for n in names)
    control=int(control);parentfd=int(parentfd);parent=int(parent);end=int(end)
    os.set_inheritable(control,False);os.set_inheritable(parentfd,False)
    if os.getppid()!=parent or control==parentfd:raise RuntimeError('CampaignActualOwnerParent')
    _campaign_live(parentfd)
    channel=socket.socket(fileno=control);channel.setblocking(False)
    if channel.family!=socket.AF_UNIX or channel.type!=socket.SOCK_SEQPACKET or not channel.getsockopt(socket.SOL_SOCKET,socket.SO_PASSCRED):raise RuntimeError('CampaignActualOwnerChannel')
    return channel,parentfd,parent,end,source_sha


def _campaign_hello(channel,peer,nonce,source_sha,qsha,end,traffic_end):
    _campaign_send(channel,dict(k='H',v=1,n=nonce,q=qsha,m=source_sha),traffic_end)
    ack,fd,raw=_campaign_recv(channel,peer,traffic_end,False,128)
    if fd is not None or ack!=dict(k='h',n=nonce,e=end):raise RuntimeError('CampaignHelloACK')
    _campaign_clock(traffic_end)


def _campaign_frame_count(count):
    if type(count) is not int or not 0<=count<400:raise RuntimeError('CampaignDirectionalFrameBound')
    return count+1


def _campaign_registration_fields(value,nonce,last_seq,wanted_slot,current,traffic_end):
    """The shared finite REGISTER grammar; validation creates no authority."""
    if type(value) is not dict or set(value)!={'k','v','n','s','i','e','c'} or value['k']!='R' or value['n']!=nonce:raise RuntimeError('CampaignREGISTERShape')
    seq,slot,end=value['s'],value['i'],value['e']
    if type(value['v']) is not int or value['v']!=1 or type(seq) is not int or seq!=last_seq+1 or not 1<=seq<=199 or type(slot) is not int or slot!=wanted_slot or type(end) is not int or not current<end<=traffic_end or end-current>30000000000 or type(value['c']) is not bool:raise RuntimeError('CampaignREGISTERBinding')
    return seq,slot,end


def _campaign_gate_args(source_sha,role,index,seq,release,nonce,end,control=-1,trace=-1):
    if role not in ('root','slot') or type(index) is not int or not 0<=index<=199 or type(seq) is not int or not 0<=seq<=199:raise RuntimeError('CampaignGateScope')
    return [str(BASE),'-I','-B',str(Path(__file__).resolve()),'--campaign-gate',source_sha,role,str(index),str(seq),str(release),nonce,str(end),str(control),str(trace),'CLOSED']


def _campaign_gate(values,harmless_group=None):
    """Fixed source-owned SAME-PID gate. Never accepts an exec recipe."""
    if len(values)!=10:raise RuntimeError('CampaignGateArguments')
    source_sha,role,index,seq,release,nonce,end,control,trace=values[0],values[1],int(values[2]),int(values[3]),int(values[4]),values[5],int(values[6]),int(values[7]),int(values[8])
    if values[9]!='CLOSED':raise RuntimeError('CampaignGateArguments')
    _campaign_features();_campaign_clock(end)
    parent=os.getppid();parentfd=os.pidfd_open(parent,0);os.set_inheritable(parentfd,False)
    channel=socket.socket(fileno=release)
    try:
        if channel.family!=socket.AF_UNIX or channel.type!=socket.SOCK_SEQPACKET or not channel.getsockopt(socket.SOL_SOCKET,socket.SO_PASSCRED):raise RuntimeError('CampaignGateSocketType')
        channel.setblocking(False);channel.set_inheritable(False)
        _campaign_live(parentfd)
        manifest=_campaign_manifest(source_sha) if harmless_group is None else _harmless_manifest(harmless_group,source_sha)
        command=_campaign_command(manifest,role,index,trace) if harmless_group is None else _harmless_command(manifest,role,index,trace,end)
        if nonce!=manifest['nonce']:raise RuntimeError('CampaignNonce')
        value,fd,raw=_campaign_recv(channel,(parent,os.getuid(),os.getgid()),end,False,128)
        if fd is not None or value!={'k':'A','n':nonce,'s':seq,'i':index,'e':end}:raise RuntimeError('CampaignGateRelease')
        _campaign_live(parentfd);_campaign_clock(end)
        if role=='root':
            if control<0 or trace!=-1:raise RuntimeError('CampaignRootDescriptors')
            retained=socket.socket(fileno=control)
            if retained.family!=socket.AF_UNIX or retained.type!=socket.SOCK_SEQPACKET or not retained.getsockopt(socket.SOL_SOCKET,socket.SO_PASSCRED):raise RuntimeError('CampaignRootDescriptors')
            retained.detach();os.set_inheritable(control,True);os.set_inheritable(parentfd,True)
            command['env'].update(WORDLING_CAMPAIGN_CONTROL_FD=str(control),WORDLING_CAMPAIGN_OWNER_PIDFD=str(parentfd),WORDLING_CAMPAIGN_OWNER=str(parent),WORDLING_CAMPAIGN_END=str(end+2000000000),WORDLING_CAMPAIGN_SOURCE=source_sha)
        elif role=='slot':
            if control!=-1:raise RuntimeError('CampaignSlotDescriptors')
            os.close(parentfd);parentfd=None
            if trace!=-1:
                if not stat.S_ISFIFO(os.fstat(trace).st_mode):raise RuntimeError('CampaignTracePipe')
                os.set_inheritable(trace,True)
            resource.setrlimit(resource.RLIMIT_FSIZE,(command['fsize'],command['fsize']))
        else:raise RuntimeError('CampaignGateRole')
        channel.close();os.chdir(command['cwd']);_campaign_clock(end)
        os.execve(command['argv'][0],command['argv'],command['env'])
    finally:
        channel.close()
        if parentfd is not None:os.close(parentfd)


_HARMLESS_OWNER=None


class _HarmlessOwner:
    """Closed DATA-control lifetime only; never production admission/authority."""
    __slots__=('group','start','end','traffic_end','manifest','descriptor','arena','aborted')
    def __init__(self):raise TypeError('SourceOwnedHarmlessProducerOnly')
    def fatal(self,reason):self.aborted=True


def _harmless_manifest(group,source_sha):
    if type(group) is not int or not 1<=group<=8 or type(source_sha) is not str or re.fullmatch('[0-9a-f]{64}',source_sha) is None:raise RuntimeError('ClosedHarmlessGroup')
    if pin(Path(__file__).resolve())['sha256']!=source_sha:raise RuntimeError('HarmlessReviewedSourcePin')
    return dict(group=group,nonce=hashlib.sha256(('wordling.wp70.harmless/v1:'+source_sha+':'+str(group)).encode('ascii')).hexdigest(),sources={str(Path(__file__).resolve()):dict(sha256=source_sha)},source_sha=source_sha)


def _harmless_owner_admission(group,source_sha,earlier_end):
    global _HARMLESS_OWNER
    origin=time.monotonic_ns()
    if _HARMLESS_OWNER is not None or type(earlier_end) is not int or not origin<earlier_end<=origin+30000000000:raise RuntimeError('HarmlessAggregateClock')
    manifest=_harmless_manifest(group,source_sha)
    value=object.__new__(_HarmlessOwner);value.group=group;value.start=origin;value.end=min(earlier_end,origin+4000000000);value.traffic_end=value.end-2000000000
    if value.traffic_end<=origin:raise RuntimeError('HarmlessCleanupReservation')
    value.manifest=manifest;value.descriptor=dict(nonce=manifest['nonce'],root='/tmp/wordling-WP70-controller-campaign-controls-21',evidence='/tmp/wordling-WP70-controller-campaign-controls-21')
    value.arena=_CampaignArena();value.aborted=False;_HARMLESS_OWNER=value
    return value


def _actual_harmless_owner(value):return value is _HARMLESS_OWNER and type(value) is _HarmlessOwner


def _harmless_command(manifest,role,index,trace=-1,end=-1):
    # No argv, path, callback, expected-input mapping or TEST/P object comes
    # from ingress. Source selects this finite harmless program exclusively.
    checked=_harmless_manifest(manifest['group'],manifest['source_sha'])
    checkpoint=manifest['group']==1 and role=='slot' and index==2 and type(trace) is int and trace>=0
    readiness=manifest['group']==8 and role=='slot' and index==1 and type(trace) is int and trace>=0 and type(end) is int and end>0
    if manifest!=checked or (trace!=-1 and not (checkpoint or readiness)) or role not in ('root','slot') or type(index) is not int or index not in ((0,) if role=='root' else (1,2)):raise RuntimeError('HarmlessClosedCommand')
    root='/tmp/wordling-WP70-controller-campaign-controls-21'
    argv=[str(BASE),'-I','-B',str(Path(__file__).resolve()),'--harmless-coordinator' if role=='root' else '--harmless-executable',str(manifest['group']),manifest['source_sha']]
    if role=='slot':argv.append(str(index))
    if checkpoint:argv.append(str(trace))
    if readiness:argv.extend((str(trace),str(end)))
    return dict(argv=argv,cwd=root,env=dict(PATH='/usr/bin:/bin',HOME=root,LANG='C.UTF-8',LC_ALL='C.UTF-8',SETUPTOOLS_USE_DISTUTILS='stdlib'),fsize=1048576,logical=None,tool=False)


def _harmless_gate_args(group,source_sha,role,index,seq,release,nonce,end,control=-1,trace=-1):
    argv=_campaign_gate_args(source_sha,role,index,seq,release,nonce,end,control,trace)
    position=argv.index('--campaign-gate');argv[position:position+1]=['--harmless-gate',str(group)]
    return argv


def _harmless_print(value):
    raw=(json.dumps(value,ensure_ascii=True,separators=(',',':'))+'\n').encode('ascii')
    if len(raw)>4096:raise RuntimeError('HarmlessReportBound')
    offset=0
    while offset<len(raw):offset+=os.write(1,raw[offset:])


def _harmless_executable(group,source_sha,index,checkpoint_fd=-1,earlier_end=-1):
    _harmless_manifest(group,source_sha)
    # Only OS8slot1 has this timing witness; restore CLOEXEC immediately.
    readiness=group==8 and index==1 and checkpoint_fd>=0 and type(earlier_end) is int and earlier_end>0
    if readiness:os.set_inheritable(checkpoint_fd,False);_campaign_clock(earlier_end)
    # Root capability descriptors/env must have ceased before final slot exec.
    names=os.listdir('/proc/self/fd')
    if len(names)>64:raise RuntimeError('HarmlessFDTableBound')
    live=[]
    for name in names:
        try:os.fstat(int(name))
        except OSError:continue
        live.append(int(name))
    if checkpoint_fd!=-1 and ((not readiness and (group!=1 or index!=2)) or not stat.S_ISFIFO(os.fstat(checkpoint_fd).st_mode)):raise RuntimeError('HarmlessCheckpointFd')
    _harmless_print(dict(event='slot_exec',index=index,pid=os.getpid(),root_capability_fds=[fd for fd in live if fd>2 and fd!=checkpoint_fd],root_role_env=any(n.startswith('WORDLING_CAMPAIGN_') for n in os.environ)))
    if checkpoint_fd!=-1 and not readiness:os.write(checkpoint_fd,b'CHECKPOINT');os.close(checkpoint_fd)
    if group==8:
        if not readiness:raise RuntimeError('HarmlessOS8ReadinessRequired')
        coordinator=os.getppid();deathfd=os.pidfd_open(coordinator,0);os.set_inheritable(deathfd,False)
        _campaign_live(deathfd);_campaign_clock(earlier_end)
        if os.getppid()!=coordinator:raise RuntimeError('HarmlessOS8StaleParent')
        worker=os.fork()
        if worker==0:
            try:
                _campaign_live(deathfd);_campaign_clock(earlier_end)
                token=b'WORDLING_OS8_WORKER_READY\n'
                if os.write(checkpoint_fd,token)!=len(token):raise RuntimeError('HarmlessOS8ReadinessWrite')
                os.close(checkpoint_fd);checkpoint_fd=-1
                with selectors.DefaultSelector() as death:
                    death.register(deathfd,selectors.EVENT_READ)
                    if not death.select(max(0,(earlier_end-time.monotonic_ns())/1000000000)):raise RuntimeError('HarmlessOS8ParentDeathMissing')
                _campaign_clock(earlier_end)
                os.close(deathfd);deathfd=-1
                os.write(2,b'HARMLESS_OS8_PARENT_DEATH\n')
                os.write(2,b'HARMLESS_PROTECTED_SELF_CLEANUP\n')
                os._exit(0)
            except BaseException:
                if checkpoint_fd!=-1:os.close(checkpoint_fd)
                if deathfd!=-1:os.close(deathfd)
                os._exit(2)
        os.close(checkpoint_fd);os.close(deathfd)
        # Registered executable waits; the actual owner terminates only its
        # retained pidfd. This is not a readiness/death witness.
        time.sleep(max(0,(earlier_end-time.monotonic_ns())/1000000000))
        return 0
    if group in (7,8):
        worker=os.fork()
        if worker==0:
            # Genuine inherited-group worker: no setsid/setpgid and no numeric
            # signal handler. It must survive owner abort and self-contain.
            time.sleep(.2)
            os.write(2,b'HARMLESS_PROTECTED_SELF_CLEANUP\n');os._exit(0)
        if group==7:
            for _ in range(9):os.write(1,b'x'*4096)
        else:time.sleep(10)
    elif group==1 and index==2:time.sleep(10)
    return 0


def _harmless_coordinator(group,source_sha):
    manifest=_harmless_manifest(group,source_sha)
    channel,parentfd,parent,end,actual_sha=_campaign_bootstrap_descriptors()
    if actual_sha!=source_sha:raise RuntimeError('HarmlessBootstrapSource')
    peer=(parent,os.getuid(),os.getgid());traffic_end=end-2000000000
    _campaign_hello(channel,peer,manifest['nonce'],source_sha,source_sha,end,traffic_end)
    _harmless_print(dict(event='bootstrap',pid=os.getpid(),control_cloexec=not os.get_inheritable(channel.fileno()),owner_cloexec=not os.get_inheritable(parentfd),actual_parent=parent))
    if group==1:
        returned=False;failure=None
        try:
            missing=subprocess.Popen(['/__wordling_harmless_missing_executable__'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True)
            returned=True
        except OSError as error:failure=type(error).__name__
        _harmless_print(dict(event='Popen_failure',returned_handle=returned,exception=failure,constructor_prefix='UNKNOWN'))
        if returned:raise RuntimeError('HarmlessMissingExecutableUnexpectedHandle')
    try:
        count=2 if group==1 else 1
        for seq in range(1,count+1):
            release,child=_campaign_pair();p=None;fd=None;checkpoint_read=checkpoint_write=-1
            if group==1 and seq==2:checkpoint_read,checkpoint_write=os.pipe2(os.O_CLOEXEC)
            if group==8 and seq==1:checkpoint_read,checkpoint_write=os.pipe2(os.O_CLOEXEC|os.O_NONBLOCK)
            if group==8:
                slot_end=min(traffic_end,time.monotonic_ns()+1000000000)
                command=_harmless_command(manifest,'slot',seq,checkpoint_write,slot_end)
            else:
                command=_harmless_command(manifest,'slot',seq,checkpoint_write)
                slot_end=min(traffic_end,time.monotonic_ns()+(80000000 if group==6 else 1000000000))
            argv=_harmless_gate_args(group,source_sha,'slot',seq,seq,child.fileno(),manifest['nonce'],slot_end,trace=checkpoint_write)
            try:
                p=subprocess.Popen(argv,cwd=command['cwd'],env=command['env'],stdin=subprocess.DEVNULL,close_fds=True,pass_fds=(child.fileno(),)+((checkpoint_write,) if checkpoint_write!=-1 else ()),start_new_session=False)
                if checkpoint_write!=-1:os.close(checkpoint_write);checkpoint_write=-1
                child.close();fd=_campaign_open_child(p)
                register=dict(k='R',v=1,n=manifest['nonce'],s=seq,i=seq,e=slot_end,c=True)
                if group==2:
                    sender=os.fork()
                    if sender==0:
                        try:_campaign_send(channel,register,slot_end,fd=fd)
                        finally:os._exit(0)
                    os.waitpid(sender,0);time.sleep(10)
                if group==3:
                    wrong=os.open('/dev/null',os.O_RDONLY|os.O_CLOEXEC)
                    try:_campaign_send(channel,register,slot_end,fd=wrong)
                    finally:os.close(wrong)
                    time.sleep(10)
                if group==4:register['n']='0'*64
                _campaign_send(channel,register,slot_end,fd=fd)
                if group==5:
                    _harmless_print(dict(event='death_before_gate_ACK',release_sent=False))
                    release.close();signal.raise_signal(signal.SIGKILL)
                ack,received,raw=_campaign_recv(channel,peer,slot_end,False,128)
                if received is not None or ack!=dict(k='A',n=manifest['nonce'],s=seq,i=seq,e=slot_end):raise RuntimeError('HarmlessActualRegistrationACK')
                if group==6:time.sleep(.12)
                _campaign_clock(slot_end);_campaign_send(release,ack,slot_end,maximum=128);release.close()
                if group==8:
                    ready=bytearray()
                    with selectors.DefaultSelector() as witness:
                        witness.register(checkpoint_read,selectors.EVENT_READ)
                        while True:
                            _campaign_clock(slot_end)
                            if not witness.select(max(0,(slot_end-time.monotonic_ns())/1000000000)):raise RuntimeError('HarmlessOS8ReadinessTimeout')
                            try:part=os.read(checkpoint_read,33-len(ready))
                            except BlockingIOError:continue
                            if not part:break
                            ready.extend(part)
                            if len(ready)>32:raise RuntimeError('HarmlessOS8ReadinessBound')
                    _campaign_clock(slot_end)
                    if ready!=b'WORDLING_OS8_WORKER_READY\n':raise RuntimeError('HarmlessOS8ReadinessToken')
                    os.close(checkpoint_read);checkpoint_read=-1
                    _harmless_print(dict(event='worker_ready_before_death',token='WORDLING_OS8_WORKER_READY',eof=True))
                    signal.raise_signal(signal.SIGKILL)
                if group==1 and seq==2:
                    with selectors.DefaultSelector() as checkpoint:
                        checkpoint.register(checkpoint_read,selectors.EVENT_READ)
                        if not checkpoint.select(max(0,(slot_end-time.monotonic_ns())/1000000000)) or os.read(checkpoint_read,11)!=b'CHECKPOINT':raise RuntimeError('HarmlessActualCheckpointMissing')
                    _campaign_clock(slot_end);_campaign_signal(fd,signal.SIGKILL,p)
                    _harmless_print(dict(event='direct_pidfd_checkpoint',actual_pipe_token='CHECKPOINT',signal='SIGKILL'))
                p.wait(timeout=max(.001,(slot_end-time.monotonic_ns())/1000000000))
                _harmless_print(dict(event='slot_exit',index=seq,exit=p.returncode))
                _campaign_send(channel,dict(k='I',n=manifest['nonce'],s=seq,i=seq,r=p.returncode),slot_end,maximum=128)
                idle,received,raw=_campaign_recv(channel,peer,slot_end,False,128)
                if received is not None or idle!=dict(k='i',n=manifest['nonce'],s=seq,i=seq,e=slot_end):raise RuntimeError('HarmlessActualIdleACK')
            finally:
                release.close();child.close()
                if fd is not None:os.close(fd)
                for checkpoint_fd in (checkpoint_read,checkpoint_write):
                    if checkpoint_fd!=-1:os.close(checkpoint_fd)
        return 0
    finally:channel.close();os.close(parentfd)






_R5_REG_CURRENT=None
_R5_REG_HELPER=None
def _r5_reg_module():
    if _R5_REG_CURRENT is None or _R5_REG_HELPER is None:raise RuntimeError('ActualPublicOwnerProducer')
    return _R5_REG_HELPER


def _begin_r5_public_owner():
    raise RuntimeError('RetiredR8PublicOwnerRole')

def _begin_tcb15():
    raise RuntimeError('RetiredColdQualificationRole')


# New standalone qualification purpose. Retired TCB15/default hooks stay closed.
_COLD_R11_CURRENT=None
_R11_QUAL_ROOT=Path('/tmp/wordling-WP70-helper-io-qualification-r14')


def _actual_cold_r11(value):
    return value is not None and value is _COLD_R11_CURRENT and type(value) is _ColdR11


def _r11_qualification_groups(mode):
    if mode=='owner':
        yield 'custody',98304,tuple(_R11_QUAL_ROOT/'owner'/n for n in ('stdout.raw','stderr.raw','control.raw'))
        yield 'custody',65536,(_R11_QUAL_ROOT/'owner/whole.json',)
        return
    root=_R11_TARGET/'receipts';deployment=root/'deployment'
    for number,label in enumerate(('venv','qualify-literal-before','stdlib-before','compile','wheel','install','qualify-literal-after','origins')):
        base=deployment/label
        yield 'pair',65536,(base.with_suffix('.command.json'),)
        yield 'pair',65536,(base.with_suffix('.whole.json'),)
        yield 'construction_raw',4194304,tuple(base.with_suffix(x)for x in ('.stdout','.stderr','.trace'))
        if number in (0,3,4,5):
            yield 'origin',16777216,(base.with_suffix('.origins.json'),)
            yield 'transient',1048576,(base.with_suffix('.transient-data.json'),)
    for name,kind,cap in (('build-freeze.json','build',262144),('compiled-data-before-wheel.json','compiled',16384),('deployment.json','deployment',262144),('deployment-inventory.json','inventory',4194304)):
        yield kind,cap,(deployment/name,)
    yield 'misc',65536,(root/'whole.json',)


def _r11_physical_guard(owner):
    # Canonical full old ordinary hold includes every older UNKNOWN, not only
    # the latest ten runtime trees. Newordinary already includes freshqual once.
    if not (_actual_campaign(owner)or _actual_cold_r11(owner)):raise RuntimeError('R11PhysicalActualProducer')
    owner.check();facts=[]
    for path in (Path('/tmp'),Path(__file__).resolve().parent.parent/'evidence'):
        owner.check()
        if path.is_symlink()or not path.is_dir():raise RuntimeError('R11PhysicalParent')
        observed=os.statvfs(path);device=path.stat().st_dev;fragment=observed.f_frsize
        if fragment<=0 or observed.f_bavail<=0 or observed.f_favail<=0:raise RuntimeError('R11PhysicalUnknown')
        rounding=max(2147483648,555808*fragment)
        required=34313605120+6681526272+4294967296+rounding
        entries=742961+316128+10240+(10240*16+64)+65536
        available=fragment*observed.f_bavail
        if available<required or observed.f_favail<entries:raise RuntimeError('R11PhysicalFullHoldFit')
        facts.append(dict(path=str(path),device=device,fragment=fragment,available_bytes=available,available_entries=observed.f_favail,required_bytes=required,required_entries=entries,old_full_bytes=34313605120,old_full_entries=742961,newordinary_bytes=6681526272,newordinary_entries=316128,evidence_bytes=4294967296,evidence_files=10240,rounding_bytes=rounding,new_family_depth=16,new_family_roots=64,no_old_hold_refunds=True))
    return facts


def _r16_physical_guard(owner):
    # Canonical full old ordinary hold includes every older UNKNOWN, not only
    # the latest ten runtime trees. R16 adds only a new55 ordinary hold; no new qualification.
    if not _actual_campaign(owner):raise RuntimeError('R11PhysicalActualProducer')
    owner.check();facts=[]
    for path in (Path('/tmp'),Path(__file__).resolve().parent.parent/'evidence'):
        owner.check()
        if path.is_symlink()or not path.is_dir():raise RuntimeError('R11PhysicalParent')
        observed=os.statvfs(path);device=path.stat().st_dev;fragment=observed.f_frsize
        if fragment<=0 or observed.f_bavail<=0 or observed.f_favail<=0:raise RuntimeError('R11PhysicalUnknown')
        rounding=max(2147483648,776384*fragment)
        required=34313605120+12289310720+8589934592+rounding
        entries=742961+432256+16384+(16384*16+64)+65536
        available=fragment*observed.f_bavail
        if available<required or observed.f_favail<entries:raise RuntimeError('R11PhysicalFullHoldFit')
        facts.append(dict(path=str(path),device=device,fragment=fragment,available_bytes=available,available_entries=observed.f_favail,required_bytes=required,required_entries=entries,old_full_bytes=34313605120,old_full_entries=742961,newordinary_bytes=12289310720,newordinary_entries=432256,evidence_bytes=8589934592,evidence_files=16384,rounding_bytes=rounding,new_family_depth=16,new_family_roots=64,no_old_hold_refunds=True))
    return facts


def _r17_physical_guard(owner):
    # Canonical full old ordinary hold includes every older UNKNOWN, not only
    # the latest ten runtime trees. R16 adds only a new55 ordinary hold; no new qualification.
    if not _actual_campaign(owner):raise RuntimeError('R11PhysicalActualProducer')
    owner.check();facts=[]
    for path in (Path('/tmp'),Path(__file__).resolve().parent.parent/'evidence'):
        owner.check()
        if path.is_symlink()or not path.is_dir():raise RuntimeError('R11PhysicalParent')
        observed=os.statvfs(path);device=path.stat().st_dev;fragment=observed.f_frsize
        if fragment<=0 or observed.f_bavail<=0 or observed.f_favail<=0:raise RuntimeError('R11PhysicalUnknown')
        rounding=max(2147483648,892512*fragment)
        required=34313605120+17897095168+8589934592+rounding
        entries=742961+548384+16384+(16384*16+64)+65536
        available=fragment*observed.f_bavail
        if available<required or observed.f_favail<entries:raise RuntimeError('R11PhysicalFullHoldFit')
        facts.append(dict(path=str(path),device=device,fragment=fragment,available_bytes=available,available_entries=observed.f_favail,required_bytes=required,required_entries=entries,old_full_bytes=34313605120,old_full_entries=742961,newordinary_bytes=17897095168,newordinary_entries=548384,evidence_bytes=8589934592,evidence_files=16384,rounding_bytes=rounding,new_family_depth=16,new_family_roots=64,no_old_hold_refunds=True))
    return facts

def _r18_physical_guard(owner):
    # Canonical full old ordinary hold includes every older UNKNOWN, not only
    # the latest ten runtime trees. R16 adds only a new55 ordinary hold; no new qualification.
    if not _actual_campaign(owner):raise RuntimeError('R11PhysicalActualProducer')
    owner.check();facts=[]
    for path in (Path('/tmp'),Path(__file__).resolve().parent.parent/'evidence'):
        owner.check()
        if path.is_symlink()or not path.is_dir():raise RuntimeError('R11PhysicalParent')
        observed=os.statvfs(path);device=path.stat().st_dev;fragment=observed.f_frsize
        if fragment<=0 or observed.f_bavail<=0 or observed.f_favail<=0:raise RuntimeError('R11PhysicalUnknown')
        rounding=max(2147483648,1008640*fragment)
        required=34313605120+23504879616+8589934592+rounding
        entries=742961+664512+16384+(16384*16+64)+65536
        available=fragment*observed.f_bavail
        if available<required or observed.f_favail<entries:raise RuntimeError('R11PhysicalFullHoldFit')
        facts.append(dict(path=str(path),device=device,fragment=fragment,available_bytes=available,available_entries=observed.f_favail,required_bytes=required,required_entries=entries,old_full_bytes=34313605120,old_full_entries=742961,newordinary_bytes=23504879616,newordinary_entries=664512,evidence_bytes=8589934592,evidence_files=16384,rounding_bytes=rounding,new_family_depth=16,new_family_roots=64,no_old_hold_refunds=True))
    return facts

def _r19_physical_guard(owner):
    # Canonical full old ordinary hold includes every older UNKNOWN, not only
    # the latest ten runtime trees. R19 adds only a new55 ordinary hold; no new qualification.
    if not _actual_campaign(owner):raise RuntimeError('R11PhysicalActualProducer')
    owner.check();facts=[]
    for path in (Path('/tmp'),Path(__file__).resolve().parent.parent/'evidence'):
        owner.check()
        if path.is_symlink()or not path.is_dir():raise RuntimeError('R11PhysicalParent')
        observed=os.statvfs(path);device=path.stat().st_dev;fragment=observed.f_frsize
        if fragment<=0 or observed.f_bavail<=0 or observed.f_favail<=0:raise RuntimeError('R11PhysicalUnknown')
        rounding=max(2147483648,1159584*fragment)
        required=34313605120+29112664064+9663676416+rounding
        entries=742961+780640+18432+(18432*16+64)+65536
        available=fragment*observed.f_bavail
        if available<required or observed.f_favail<entries:raise RuntimeError('R11PhysicalFullHoldFit')
        facts.append(dict(path=str(path),device=device,fragment=fragment,available_bytes=available,available_entries=observed.f_favail,required_bytes=required,required_entries=entries,old_full_bytes=34313605120,old_full_entries=742961,newordinary_bytes=29112664064,newordinary_entries=780640,evidence_bytes=9663676416,evidence_files=18432,rounding_bytes=rounding,new_family_depth=16,new_family_roots=64,no_old_hold_refunds=True))
    return facts

class _R11Capacity:
    """Pinned ASCII JSON, standard per-value decoder, no full capacity graph.

    All generations stay charged until this admission frame returns. TWO512KiB
    item generations cover caller/generator overlap and JSON decoder temporaries;
    names3MiB and original fixed1MiB are separate paired44MiB reservations.
    """
    __slots__=('owner','text','spans','decoder','raw_bytes','raw_limit')
    _arrays=('E_inventory','canonical_reference_roots')
    def __init__(self,owner):
        if _actual_campaign(owner):
            path=_R11_FREEZE/'capacity-baseline.json.gz';wanted=owner.manifest['capacity']
        elif _actual_cold_r11(owner):
            path=_R11_FREEZE/'qualification-capacity.json.gz';wanted=owner.prefix['members']['qualification-capacity.json.gz']
        else:raise RuntimeError('R11CapacityActualProducer')
        self.owner=owner;self.spans={}
        if _actual_campaign(owner):
            remaining=46137344-owner.expected_charge-1048576-1048576
            self.raw_limit=min(8388608,remaining//2,remaining-3145728)
        else:
            self.raw_limit=min(8388608,(46137344-owner.expected_charge-1048576-3145728-1048576)//2)
        if self.raw_limit<=0:raise RuntimeError('R11CapacityRemainingArena')
        same(path,wanted)
        raw=bounded_gzip(path,self.raw_limit)
        if not raw.isascii():raise RuntimeError('R11CapacityWriterASCII')
        self.raw_bytes=len(raw)
        self.text,_=_json_prepared(raw,self.raw_limit,True)
        del raw
        self.decoder=json.JSONDecoder(parse_constant=lambda x:(_ for _ in ()).throw(RuntimeError('JSONNonfinite')))
        t=self.text;pos=self.ws(0)
        if pos>=len(t)or t[pos]!='{':raise RuntimeError('R11CapacityObject')
        pos=self.ws(pos+1);count=0
        if pos<len(t)and t[pos]=='}':raise RuntimeError('R11CapacityEmpty')
        while True:
            owner.check()
            if pos>=len(t)or t[pos]!='"':raise RuntimeError('R11CapacityHeaderString')
            stop=pos+1;escaped=False
            while stop<len(t):
                if stop-pos>256:raise RuntimeError('R11CapacityHeaderWidth')
                char=t[stop]
                if escaped:escaped=False
                elif char=='\\':escaped=True
                elif char=='"':break
                stop+=1
            if stop>=len(t):raise RuntimeError('R11CapacityHeaderStringEnd')
            key,after=self.decoder.raw_decode(t,pos)
            if after!=stop+1:raise RuntimeError('R11CapacityHeaderFraming')
            if type(key)is not str or not key.isascii()or len(key)>64:raise RuntimeError('R11CapacityHeaderKey')
            pos=self.ws(after)
            if pos>=len(t)or t[pos]!=':':raise RuntimeError('R11CapacityColon')
            start=self.ws(pos+1);end=self.value_end(start)
            # Last duplicate wins, as in the unchanged default JSON decoder.
            # Every earlier value is nevertheless syntax-checked in full.
            if key in self._arrays:
                if t[start]!='[':raise RuntimeError('R11CapacityArray')
                for value in self.values(start,end):del value
            else:
                value=self.item(start,end);del value
            self.spans[key]=(start,end);count+=1
            if len(self.spans)>32 or count>32768:raise RuntimeError('R11CapacityHeaderBound')
            pos=self.ws(end)
            if pos<len(t)and t[pos]==',':
                pos=self.ws(pos+1)
                if pos>=len(t)or t[pos]=='}':raise RuntimeError('R11CapacityTrailingComma')
                continue
            if pos>=len(t)or t[pos]!='}':raise RuntimeError('R11CapacityObjectEnd')
            if self.ws(pos+1)!=len(t):raise RuntimeError('R11CapacityTrailingData')
            break
        if not {'E_bytes','E_files','E_inventory','evidence_root','canonical_reference_roots'}<=set(self.spans):raise RuntimeError('R11CapacityRequiredFields')
    def ws(self,pos):
        t=self.text
        while pos<len(t)and t[pos]in ' \t\r\n':pos+=1
        return pos
    def value_end(self,start):
        t=self.text;depth=0;quoted=False;escape=False;pos=start
        while pos<len(t):
            char=t[pos]
            if quoted:
                if escape:escape=False
                elif char=='\\':escape=True
                elif char=='"':quoted=False
            elif char=='"':quoted=True
            elif char in '[{':depth+=1
            elif char in ']}':
                if depth==0:break
                depth-=1
                if depth==0:return pos+1
            elif char==','and depth==0:break
            pos+=1
        if quoted or depth or pos==start:raise RuntimeError('R11CapacityValueFraming')
        end=pos
        while end>start and t[end-1]in ' \t\r\n':end-=1
        return end
    def item(self,start,end):
        self.owner.check()
        if not 0<=start<end<=len(self.text)or end-start>65536:raise RuntimeError('R11CapacityItemWidth')
        # Bound the derived slice and graph before default raw_decode. No tail
        # copy, object_pairs_hook or alternative JSON acceptance algorithm.
        part=self.text[start:end];_,charge=_json_prepared(part,65536,True)
        if charge>524288:raise RuntimeError('R11CapacityItemPrepared')
        del part
        value,actual_end=self.decoder.raw_decode(self.text,start)
        if actual_end!=end:raise RuntimeError('R11CapacityValueEnd')
        return value
    def values(self,start,end):
        t=self.text;pos=self.ws(start+1);count=0
        if pos<end and t[pos]==']':
            if pos+1!=end:raise RuntimeError('R11CapacityArrayEnd')
            return
        while True:
            stop=self.value_end(pos)
            if stop>=end:raise RuntimeError('R11CapacityArrayFraming')
            value=self.item(pos,stop);count+=1
            if count>32768:raise RuntimeError('R11CapacityArrayCount')
            yield value
            del value
            pos=self.ws(stop)
            if pos<end and t[pos]==',':
                pos=self.ws(pos+1)
                if pos>=end or t[pos]==']':raise RuntimeError('R11CapacityArrayTrailingComma')
                continue
            if pos>=end or t[pos]!=']'or pos+1!=end:raise RuntimeError('R11CapacityArrayEnd')
            return
    def scalar(self,name):return self.item(*self.spans[name])
    def rows(self,name):return self.values(*self.spans[name])


def _r11_reference_profile(owner):
    path=_R11_FREEZE/'reference-roots.json'
    wanted=owner.manifest['members']['reference-roots.json']if _actual_campaign(owner)else owner.prefix['members']['reference-roots.json']
    same(path,wanted);document=_campaign_small(path,65536)
    if set(document)!={'schema','qualification','campaign'}or document['schema']!='wordling.controller-campaign-r11-reference-profile/v1':raise RuntimeError('R11ReferenceProfile')
    profile=document['campaign'if _actual_campaign(owner)else'qualification']
    del document
    if set(profile)!={'roots','policies'}:raise RuntimeError('R11ReferenceFields')
    names=profile['roots'];policies=profile['policies']
    if type(names)is not list or not 91<=len(names)<=(162 if _actual_campaign(owner) else 143) or names!=sorted(set(names))or any(type(n)is not str or not n.isascii()or not 0<len(n)<=192 or not Path(n).is_absolute()for n in names):raise RuntimeError('R11ReferenceRootGrammar')
    if type(policies)is not dict or set(policies)!=set(names)or any(type(v)is not str or not v.isascii()or len(v)>512 for v in policies.values()):raise RuntimeError('R11ReferencePolicyGrammar')
    carrier=_r11_carrier();m=carrier['reference_grammar']['mandatory91']
    packed=base64.b64decode(m['base64'],validate=True);z=zlib.decompressobj(31);raw=z.decompress(packed,16385)
    if not z.eof or z.unused_data or z.unconsumed_tail or len(raw)!=m['raw']or hashlib.sha256(raw).hexdigest()!=m['raw_sha256']:raise RuntimeError('R11MandatoryRootsCodec')
    mandatory=bounded_json_loads(raw,16384,True)
    if len(mandatory)!=91 or not set(mandatory)<=set(names):raise RuntimeError('R11MandatoryRoots')
    return profile


def _r11_verify_capacity(owner):
    """Consume every frozen row/header with one bounded standard decoder.

    On failure no frame/traceback credit is released and no next launch occurs.
    On return cursor, row dictionaries and names sets all die with this frame.
    """
    cursor=_R11Capacity(owner);profile=_r11_reference_profile(owner)
    root=cursor.scalar('evidence_root');files=cursor.scalar('E_files');total=cursor.scalar('E_bytes')
    if root!=str(Path(__file__).resolve().parent.parent/'evidence')or type(files)is not int or not 0<files<=(3815 if _actual_campaign(owner) else 1390) or type(total)is not int or total<0:raise RuntimeError('R11CapacityBaselineScope')
    base=Path(root);baseline=set();measured=0
    for row in cursor.rows('E_inventory'):
        owner.check()
        if type(row)is not dict or not {'relative','path','bytes','sha256','mode','uid','gid','classification'}<=set(row):raise RuntimeError('R11EvidenceRow')
        name=row['relative']
        if type(name)is not str or not name.isascii()or not 0<len(name)<=256 or Path(name).is_absolute()or'..'in Path(name).parts or name in baseline or len(baseline)>=files or row['path']!=str(base/name)or type(row['classification'])is not str or len(row['classification'])>512:raise RuntimeError('R11EvidenceRowScope')
        same(base/name,dict(size=row['bytes'],**{k:row[k]for k in ('sha256','mode','uid','gid')}));measured+=row['bytes'];baseline.add(name)
        del row
    if len(baseline)!=files or measured!=total:raise RuntimeError('EvidenceBaselineTotals')
    if _actual_campaign(owner):
        # Consume only verified baseline names. Retain at most 1008 extras,
        # never a second complete E-name set or its difference.
        actual=set();observed=0
        for p in base.rglob('*'):
            owner.check()
            if not p.is_file():continue
            name=str(p.relative_to(base))
            if p.is_symlink()or not name.isascii()or len(name)>256 or observed>=files+1008:raise RuntimeError('R11EvidenceCensusBound')
            observed+=1
            if name in baseline:baseline.remove(name)
            else:
                if name in actual or len(actual)>=1008:raise RuntimeError('R11EvidenceCensusBound')
                actual.add(name)
        if baseline or observed!=files+len(actual):raise RuntimeError('EvidenceBaselineNameSet')
    else:
        actual=set()
        for p in base.rglob('*'):
            owner.check()
            if not p.is_file():continue
            name=str(p.relative_to(base))
            if p.is_symlink()or not name.isascii()or len(name)>256 or len(actual)>=files+1008:raise RuntimeError('R11EvidenceCensusBound')
            actual.add(name)
        if not baseline<=actual:raise RuntimeError('EvidenceBaselineNameSet')
    if _actual_cold_r11(owner):
        if actual!=baseline:raise RuntimeError('R11ColdNotAResume')
    else:
        for name in actual:
            p=base/name;found=None
            for identity,writer in enumerate(_campaign_writer_groups(owner.descriptor)):
                if p in writer[3]:
                    if found is not None:raise RuntimeError('CampaignWriterAlias')
                    found=writer
            if found is None or p.stat().st_size>found[2]:raise RuntimeError('CampaignUnadmittedEvidence')
            if owner.budget is None and owner.role=='coordinator'and found[0]!='owner':raise RuntimeError('CampaignNotAResume')
    if _actual_campaign(owner):del baseline,actual
    seen=set();member_total=0
    for ref in cursor.rows('canonical_reference_roots'):
        owner.check()
        if type(ref)is not dict or set(ref)!={'root','count','bytes','members','policy'}:raise RuntimeError('ReferenceSchema')
        name=ref['root'];members=ref['members']
        if name not in profile['policies']or name in seen or len(seen)>=(162 if _actual_campaign(owner) else 143) or ref['policy']!=profile['policies'][name]or type(members)is not list or len(members)!=ref['count']or len(members)>153 or sum(r['bytes']for r in members)!=ref['bytes']:raise RuntimeError('R11ReferenceRootBinding')
        seen.add(name);member_total+=len(members)
        if member_total>32768:raise RuntimeError('ReferenceCardinality')
        directory=Path(name);wanted=set()
        for row in members:
            relative=row['relative']
            if set(row)!={'relative','path','bytes','mode','uid','gid','sha256'}or type(relative)is not str or not relative.isascii()or not 0<len(relative)<=256 or Path(relative).is_absolute()or'..'in Path(relative).parts or relative in wanted or row['path']!=str(directory/relative):raise RuntimeError('R11ReferenceRowScope')
            wanted.add(relative);same(directory/relative,dict(size=row['bytes'],**{k:row[k]for k in ('sha256','mode','uid','gid')}));owner.check()
        observed=set()
        for p in directory.rglob('*'):
            owner.check()
            if not p.is_file():continue
            relative=str(p.relative_to(directory))
            if p.is_symlink()or not relative.isascii()or len(relative)>256 or len(observed)>=155:raise RuntimeError('R11ReferenceCensusBound')
            observed.add(relative)
        if directory==_R11_FREEZE and _actual_campaign(owner):
            if wanted!=set(owner.manifest['members'])-{'expected-inputs.json.gz','capacity-baseline.json.gz'}or observed!=set(owner.manifest['members'])|{'source-bindings.json','seal.json'}:raise RuntimeError('CampaignSelfReferencePartition')
        elif wanted!=observed:raise RuntimeError('ImmutableReferenceMembers')
        del ref,members,wanted,observed
    if sorted(seen)!=profile['roots']:raise RuntimeError('R11ExactReferenceRoots')
    return files,total


class _ColdR11:
    __slots__=('mode','arena','source_sha','prefix','expected','expected_charge','start','end','budget','context_value','claimed','groups','aborted')
    def __init__(self):raise TypeError('R11FixedColdProducerOnly')
    def check(self,context=None):
        if not _actual_cold_r11(self) or self.aborted:raise RuntimeError('R11ColdIdentity')
        if time.monotonic()>=self.end:raise RuntimeError('R11ColdSharedDeadline')
        if context is not None and (context is not self.context_value or type(context)is not Preparation or context.qualification is not self or context.expected is not self.expected or context.target!=_R11_TARGET or context.evidence!=_R11_TARGET/'receipts'):raise RuntimeError('R11GenuinePreparationIdentity')
    def context(self,target,evidence,expected,origin,end):
        self.check()
        if self.mode!='inner' or self.context_value is not None or Path(target)!=_R11_TARGET or Path(evidence)!=_R11_TARGET/'receipts' or expected is not self.expected or origin!=self.start or end!=self.end:raise RuntimeError('R11ColdConstructor')
        # Preparation registers itself only after its real constructor binds it.
    def install(self,budget):
        self.check()
        if self.budget is not None or type(budget)is not EvidenceBudget:raise RuntimeError('R11ColdBudgetOnce')
        root=_R11_QUAL_ROOT/'owner'if self.mode=='owner'else _R11_TARGET/'receipts'
        if budget.roots!=(root.absolute(),):raise RuntimeError('R11ColdBudgetRoot')
        totals={k:[v[0],v[1]]for k,v in R14_CLASS_LIMITS.items()}
        # The whole adopted envelope is held; own finite groups are a subset,
        # not extra grants and not a replacement for any old campaign tails.
        for kind,cap,paths in _r11_qualification_groups(self.mode):
            if cap>totals[kind][0]or len(paths)>totals[kind][1]:raise RuntimeError('R11ColdWriterEnvelope')
        if 26022808+sum(v[0]for v in totals.values())+R11_LIVE_SOURCE_GROWTH>EVIDENCE_LIMIT or 1376+sum(v[1]for v in totals.values())>EVIDENCE_FILES:raise RuntimeError('R11ColdFullEnvelopeFit')
        budget.classes=totals;self.budget=budget
    def claim(self,budget,paths,kind,maximum):
        self.check()
        if budget is not self.budget:raise RuntimeError('R11ColdBudgetIdentity')
        found=[(i,k,c,m)for i,(k,c,m)in enumerate(_r11_qualification_groups(self.mode))if paths==m]
        if len(found)!=1:raise RuntimeError('R11ClosedQualificationWriter')
        identity,wanted,cap,members=found[0]
        if kind!=wanted or maximum>cap or self.claimed&(1<<identity):raise RuntimeError('R11QualificationWriterSpent')
        if any(p.exists()or p.is_symlink()for p in paths):raise RuntimeError('R11QualificationNoClobber')
        self.claimed|=1<<identity
        group=dict(kind=kind,maximum=cap,used=0,paths=members)
        for p in paths:budget.slots[p]=group
        return group
    def admit(self,expected,root):
        self.check()
        wanted=_R11_QUAL_ROOT/'owner'if self.mode=='owner'else _R11_TARGET/'receipts'
        if expected is not self.expected or Path(root)!=wanted:raise RuntimeError('R11ColdAdmissionIdentity')
        if self.budget is not None:return self.budget
        _r11_verify_capacity(self)
        _r11_physical_guard(self)
        global _ACTIVE_BUDGET
        if _ACTIVE_BUDGET is not None:raise RuntimeError('R11ColdBudgetNotFresh')
        budget=EvidenceBudget([wanted],26022808,1376,qualification=self)
        _ACTIVE_BUDGET=budget
        return budget


def _begin_r11_cold(source_sha,mode,start,end):
    global _COLD_R11_CURRENT
    if mode not in ('owner','inner')or _COLD_R11_CURRENT is not None or _CAMPAIGN_CURRENT is not None or _R5_REG_CURRENT is not None or _ACTIVE_BUDGET is not None or _CAPTURES:raise RuntimeError('R11ColdSinglePurpose')
    if type(start)is not float or type(end)is not float or not math.isfinite(start)or not math.isfinite(end)or not 0<end-start<=120 or time.monotonic()>=end:raise RuntimeError('R11ColdClock')
    if type(source_sha)is not str or re.fullmatch('[0-9a-f]{64}',source_sha)is None:raise RuntimeError('R11ExternalPrefixAnchor')
    carrier=_r11_carrier();path=_R11_FREEZE/'prefix-seal.json'
    if pin(path)['sha256']!=source_sha or path.stat().st_size>32768 or rights(path)!=dict(mode=384,uid=1000,gid=1000):raise RuntimeError('R11ExternalPrefixAnchor')
    prefix=_campaign_small(path)
    if set(prefix)!={'schema','stage','members','sources','qualification'}or prefix['schema']!='wordling.r11.qualification-source-prefix/v1'or prefix['stage']!='SOURCE_CONTROL_REVIEWED':raise RuntimeError('R11ColdPrefixSchema')
    if prefix['qualification']!=carrier['r11']['qualification']or set(prefix['sources'])!=set(carrier['r11']['source6_before']):raise RuntimeError('R11ColdSourceSix')
    _r11_source_roles(prefix['sources'],carrier)
    if prefix['sources'][str(_R5_PROVIDER)]!=carrier['provider']['current']:raise RuntimeError('R11ColdProtectedProvider')
    caps=carrier['future_source']['caps'];members=prefix['members']
    if not set(members)<=set(caps)-{'prefix-seal.json','expected-inputs.json.gz','capacity-baseline.json.gz','source-bindings.json','seal.json','baseline-v17-binding.json','input-custody.json'}or 'qualification-capacity.json.gz'not in members:raise RuntimeError('R11ColdPrefixMembership')
    if {str(p.relative_to(_R11_FREEZE))for p in _R11_FREEZE.rglob('*')if p.is_file()}!=set(members)|{'prefix-seal.json'}:raise RuntimeError('R11ColdClosedPrefix')
    for name,row in members.items():
        if set(row)!={'size','sha256','mode','uid','gid'}or row['size']>caps[name]:raise RuntimeError('R11ColdPrefixBound')
        same(_R11_FREEZE/name,row)
    for name,row in prefix['sources'].items():
        before=carrier['r11']['source6_before'][name]
        if set(row)!=set(before)or any(row[k]!=before[k]for k in row if k not in ('size','sha256')):raise RuntimeError('R11ColdSourceRoles')
        same(name,row)
    if mode=='inner':
        fd_text=os.environ.get('WORDLING_PREPARATION_CONTROL_FD','')
        if not fd_text.isascii()or not fd_text.isdigit()or len(fd_text)>7:raise RuntimeError('R11SurvivingOwnerRequired')
        control=int(fd_text)
        if control<3 or not stat.S_ISFIFO(os.fstat(control).st_mode)or os.environ.get('WORDLING_R11_OWNER_PID')!=str(os.getppid())or os.environ.get('WORDLING_PREPARATION_ORIGIN')!=repr(start)or os.environ.get('WORDLING_PREPARATION_END')!=repr(end):raise RuntimeError('R11ActualOwnerClockPipe')
    same(FREEZE/'expected-inputs.json.gz',carrier['expected_base'])
    raw=bounded_gzip(FREEZE/'expected-inputs.json.gz');text,expected_charge=_json_prepared(raw,8388608,True)
    expected=json.loads(text,parse_constant=lambda x:(_ for _ in ()).throw(RuntimeError('JSONNonfinite')))
    del raw,text
    expected_charge+=8192  # fixed six-pin numerical-width updates, no new key/node/path
    expected['files'].update(prefix['sources']);expected['files']['/etc/ld.so.cache']={'size':150747,'sha256':'c1dbbf1efb0a2e4e39124d1c6b296f25bb11008095945378714188dff359f320','mode':420,'uid':0,'gid':0}
    expected['approved_providers']=dict(expected['approved_providers']);expected['approved_providers']['scripts/reference/startup_family/lifetime.py']=_R5_COMMIT
    delta=sum(row['size']-carrier['old4'].get(name,carrier['provider']['old'])['size']for name,row in prefix['sources'].items())
    expected['payload_bytes']=carrier['old_payload_bytes']+delta;expected['evidence_baseline']=members['qualification-capacity.json.gz']
    # All protected files/roles are checked by the ordinary preflight against
    # the immutable V19 basis; only the six explicit postimages are replaced.
    value=object.__new__(_ColdR11);value.mode=mode;value.source_sha=source_sha;value.prefix=prefix;value.expected=expected;value.expected_charge=expected_charge;value.start=start;value.end=end;value.budget=None;value.context_value=None;value.claimed=0;value.groups=None;value.aborted=False
    value.arena=_CampaignArena();value.arena.hold('fixed-coordinator-state',2097152)
    _COLD_R11_CURRENT=value
    return value


def _r11_child_argv(source_sha):
    if type(source_sha)is not str or re.fullmatch('[0-9a-f]{64}',source_sha)is None:raise RuntimeError('R11QualificationSourceSHA')
    # Fixed canonical names/default source loaders, no sys.path mutation or
    # caller-selected module/root/recipe. ROOT checks exact source/argv first.
    directory=Path(__file__).resolve().parent
    body="import importlib.util,sys,pathlib\nD=pathlib.Path("+repr(str(directory))+")\nfor name in ('runtime_qualification','controller_deployment'):\n p=D/(name+'.py')\n if any((D/'__pycache__').glob(name+'.*.pyc')):raise RuntimeError('R11CachedSourceExcluded')\n s=importlib.util.spec_from_file_location(name,p)\n if s.name!=name or s.origin!=str(p)or type(s.loader).__name__!='SourceFileLoader':raise RuntimeError('R11CanonicalSourceLoader')\n m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m)\nraise SystemExit(sys.modules['runtime_qualification']._r11_qualification_inner("+repr(source_sha)+"))\n"
    return [str(BASE),'-I','-B','-c',body]


def _r11_qualification_inner(source_sha):
    # Only the fixed surviving-owner launcher may supply these inherited ends.
    start=float(os.environ['WORDLING_PREPARATION_ORIGIN']);end=float(os.environ['WORDLING_PREPARATION_END'])
    record=_begin_r11_cold(source_sha,'inner',start,end)
    from controller_deployment import deploy
    context=Preparation(_R11_TARGET,_R11_TARGET/'receipts',record.expected,origin=start,earlier_end=end,qualification=record)
    code=2;error=None
    try:
        interpreter,inventory=deploy(context.source,context.repository,context.target,context.evidence/'deployment',context=context)
        if len(inventory)!=188 or len(context.calls)!=8:raise RuntimeError('R11EightStages188Required')
        context._release_metadata_after_deploy_frame()
        preflight(interpreter,inventory);code=0
        print(json.dumps(dict(status='R11_STANDALONE_QUALIFICATION_OBSERVED_ONLY',stages=8,inventory=188,P=False,TEST=False,CODE=False)))
    except BaseException as failure:
        error=generated_diagnostic(failure,1024);raise
    finally:
        context.budget.document(context.evidence/'whole.json',dict(exit=code,error=error,calls=[immutable_metadata_ref(p,context.evidence)for p in context.call_paths],P=False,TEST=False,CODE=False,partial=code!=0,runtime='UNKNOWN_UNTIL_ACTUAL_REVIEW'if code else'OBSERVED_NOT_ADOPTED'),'misc')
    return code


class Preparation:
    def __init__(self,target,evidence,expected,origin=None,internal_earlier_output_cap=CONSTRUCTION_RAW_LIMIT,earlier_end=None,campaign=None,slot=None,*,qualification=None):
        self.campaign=campaign;self.slot=slot;self.finished=False;self.qualification=qualification
        if qualification is not None:
            if campaign is not None or slot is not None or not _actual_cold_r11(qualification):raise RuntimeError('R11ColdPreparationIdentity')
            qualification.context(target,evidence,expected,origin,earlier_end)
        self.source=Path(__file__).resolve().parent.parent;self.repository=self.source.parents[3]
        if campaign is not None:
            if not _actual_campaign(campaign) or type(slot) is not _PreparationSlot or campaign.slot is not slot or slot.preparation is not None or slot.state!='CREATING' or expected is not campaign.expected or Path(target)!=slot.target or Path(evidence)!=slot.evidence or origin!=slot.origin/1000000000 or earlier_end!=slot.traffic_end/1000000000:raise RuntimeError('ActualPreparationConstructor')
            self.source=slot.source;slot.preparation=self
        inherited_origin=qualification.start if qualification is not None else float(os.environ.get('WORDLING_PREPARATION_ORIGIN',time.monotonic()))
        inherited_end=float(os.environ.get('WORDLING_PREPARATION_END',inherited_origin+120))
        self.start=inherited_origin if origin is None else min(origin,inherited_origin);self.end=min(self.start+120,inherited_end)
        if campaign is not None:self.start=slot.origin/1000000000;self.end=slot.traffic_end/1000000000
        if earlier_end is not None:
            if type(earlier_end) not in (int,float) or not math.isfinite(earlier_end):raise RuntimeError('EarlierClockOnly')
            self.end=min(self.end,earlier_end)
        if time.monotonic()>=self.end:raise RuntimeError('PreparationSharedDeadline')
        if not 0<internal_earlier_output_cap<=CONSTRUCTION_RAW_LIMIT:raise ValueError('EarlierOutputCapOnly')
        self.output_cap=internal_earlier_output_cap
        os.umask(0o022)  # Own preparation process only; normal copied-tree rights.
        self.target=Path(target);self.evidence=Path(evidence);self.expected=expected
        if qualification is not None:qualification.context_value=self
        self.budget=admit_capacity(expected,self.evidence,campaign=campaign,slot=slot,qualification=qualification)

        self.calls=[];self.call_paths=[]
        self._metadata_json=set();self._metadata_seen=set();self._metadata_maps=False;self._metadata_wheel=None
        if self.target.exists() or self.target.is_symlink():raise RuntimeError('NoClobberRoot')
        self.preflight_inputs()
        verify_tool_selection(self.expected)
        if campaign is not None:self.target.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
        self.target.mkdir(mode=0o700);(self.target/'home').mkdir(mode=0o700);(self.target/'tmp').mkdir(mode=0o700)
        self.evidence.mkdir(parents=True,exist_ok=False)
        self.env=dict(PATH='/usr/bin:/bin',HOME=str(self.target/'home'),LANG='C.UTF-8',LC_ALL='C.UTF-8',
            PYTHONDONTWRITEBYTECODE='1',PIP_DISABLE_PIP_VERSION_CHECK='1',PIP_NO_CACHE_DIR='1',PIP_CONFIG_FILE='/dev/null',TMPDIR=str(self.target/'tmp'))
        self.check()

    def qualification_literal(self):
        self.check(clock_only=True)
        if self.campaign is None:return qualification_literal(self.target)
        campaign=self.campaign;slot=self.slot;stage=len(self.calls)
        if not _actual_campaign(campaign)or type(slot)is not _PreparationSlot or campaign.slot is not slot or slot.preparation is not self or slot.state!='PREPARING'or stage not in(1,6):raise RuntimeError('CampaignQualificationIdentity')
        variant,poison=_campaign_stage(slot.number)
        target,source,evidence=_campaign_runtime(_campaign_plan(campaign.manifest),variant,poison)
        if(self.target,self.source,self.evidence)!=(target,source,evidence):raise RuntimeError('CampaignQualificationTarget')
        return _campaign_qualification_literal(campaign.manifest,120+8*slot.number+stage)

    def _metadata_arena(self):
        if self.qualification is not None:
            self.qualification.check(self);return self.qualification.arena
        return self.campaign.arena

    def _metadata_identity(self):
        if self.campaign is None and self.qualification is None:return None
        self.check(clock_only=True)
        if self.qualification is not None:
            self.qualification.check(self);return 'cold-r11-'
        if not _actual_campaign(self.campaign) or type(self.slot) is not _PreparationSlot or self.slot.preparation is not self:raise RuntimeError('ActualPreparationMetadata')
        return 'prep-'+str(self.slot.number)+'-'

    def decode_metadata(self,raw,label,maximum=65536):
        if self.campaign is None and self.qualification is None:return bounded_json_loads(raw)
        prefix=self._metadata_identity()
        if label not in ('stdlib-before','direct-url','origins') or label in self._metadata_seen or self._metadata_wheel is not None or type(maximum) is not int or not 0<maximum<=65536:raise RuntimeError('PreparationClosedJSONLease')
        self._metadata_seen.add(label);self._metadata_json.add(label)
        # On any refusal the actual arena lease stays charged with the
        # escaping traceback; no exception-time credit can authorize more work.
        return self._metadata_arena().decode(prefix+'json-'+label,raw,maximum,earlier_nodes=32768)

    def release_metadata(self,label):
        if self.campaign is None and self.qualification is None:return
        prefix=self._metadata_identity()
        if label not in self._metadata_json:raise RuntimeError('PreparationJSONLeaseIdentity')
        self._metadata_arena().release(prefix+'json-'+label);self._metadata_json.remove(label)

    def begin_metadata_maps(self):
        if self.campaign is None and self.qualification is None:return
        prefix=self._metadata_identity()
        if self._metadata_maps or self._metadata_json or self._metadata_seen!={'stdlib-before'}:raise RuntimeError('PreparationMapPhase')
        self._metadata_arena().hold(prefix+'direct-maps',2097152);self._metadata_maps=True

    def begin_wheel_copy(self,label):
        if self.campaign is None and self.qualification is None:return
        prefix=self._metadata_identity()
        if label not in ('fixture-elf','review-wheel','installed-wheel') or self._metadata_wheel is not None or self._metadata_json or not self._metadata_maps:raise RuntimeError('PreparationWheelPhase')
        self._metadata_arena().hold(prefix+'wheel-copy',3145728);self._metadata_wheel=label

    def end_wheel_copy(self,label):
        if self.campaign is None and self.qualification is None:return
        prefix=self._metadata_identity()
        if self._metadata_wheel!=label:raise RuntimeError('PreparationWheelLeaseIdentity')
        self._metadata_arena().release(prefix+'wheel-copy');self._metadata_wheel=None

    def _release_metadata_after_deploy_frame(self):
        prefix=self._metadata_identity()
        if not self._metadata_maps or self._metadata_json or self._metadata_wheel is not None or self._metadata_seen!={'stdlib-before','direct-url','origins'}:raise RuntimeError('PreparationMetadataNotSettled')
        self._metadata_arena().release(prefix+'direct-maps');self._metadata_maps=False

    def guard_wheel(self,path):
        if self.campaign is None and self.qualification is None:return
        self._metadata_identity()
        if self._metadata_wheel is None:raise RuntimeError('PreparationWheelCopyLeaseRequired')
        path=Path(path)
        if path!=self.target/'wheels/wordling_reference_controller_test-0.2.0-py3-none-any.whl' or path.is_symlink():raise RuntimeError('PreparationClosedWheelPath')
        size=path.stat().st_size
        if not 22<=size<=2097152:raise RuntimeError('PreparationWheelByteBound')
        with path.open('rb') as stream:stream.seek(-22,os.SEEK_END);footer=stream.read(22)
        signature,disk,central_disk,disk_count,count,central_bytes,central_offset,comment=struct.unpack('<4s4H2LH',footer)
        if signature!=b'PK\x05\x06' or disk or central_disk or count!=disk_count or not 1<=count<=32 or central_bytes>65536 or central_offset+central_bytes!=size-22 or comment:raise RuntimeError('PreparationWheelCentralDirectoryBound')
        # ZipFile iterates the physical directory, so an EOCD count alone is
        # insufficient. Bound every actual record BEFORE ZipInfo allocation.
        with path.open('rb') as stream:stream.seek(central_offset);central=stream.read(central_bytes+1)
        if len(central)!=central_bytes+1:raise RuntimeError('PreparationWheelCentralRead')
        central=central[:central_bytes];offset=0;actual=0
        while offset<len(central):
            if offset+46>len(central) or central[offset:offset+4]!=b'PK\x01\x02':raise RuntimeError('PreparationWheelCentralFraming')
            name_size,extra_size,comment_size,disk_start=struct.unpack_from('<4H',central,offset+28)
            compressed,plain=struct.unpack_from('<2L',central,offset+20)
            stop=offset+46+name_size+extra_size+comment_size
            if actual>=32 or not 1<=name_size<=256 or extra_size>4096 or comment_size or disk_start or plain>1048576 or compressed>2097152 or stop>len(central):raise RuntimeError('PreparationWheelCentralRecordBound')
            if any(b>127 for b in central[offset+46:offset+46+name_size]):raise RuntimeError('PreparationWheelMemberNameASCII')
            extra=central[offset+46+name_size:stop];position=0
            while position<len(extra):
                if position+4>len(extra):raise RuntimeError('PreparationWheelExtraFraming')
                kind,length=struct.unpack_from('<HH',extra,position);position+=4
                if kind==1 or position+length>len(extra):raise RuntimeError('PreparationWheelZIP64OrExtra')
                position+=length
            actual+=1;offset=stop
        if actual!=count:raise RuntimeError('PreparationWheelCentralCount')
        del central
        self.check(clock_only=True)

    def guard_wheel_member(self,info,record=False):
        if self.campaign is None and self.qualification is None:return
        self._metadata_identity()
        if self._metadata_wheel is None or len(info.filename)>256 or not info.filename.isascii() or info.file_size>(65536 if record else 1048576) or info.file_size<0 or len(info.extra)>4096:raise RuntimeError('PreparationWheelMemberBound')
        offset=0
        while offset<len(info.extra):
            if offset+4>len(info.extra):raise RuntimeError('PreparationWheelExtraFraming')
            kind,size=struct.unpack_from('<HH',info.extra,offset);offset+=4
            if kind==1 or offset+size>len(info.extra):raise RuntimeError('PreparationWheelZIP64OrExtra')
            offset+=size

    def add_inventory_path(self,paths,path):
        if self.campaign is None and self.qualification is None:paths.add(path);return
        self._metadata_identity()
        if not self._metadata_maps:raise RuntimeError('PreparationInventoryMapLease')
        text=str(path)
        if len(text)>512 or not text.isascii():raise RuntimeError('PreparationInventoryPathBound')
        if path in paths:return
        if len(paths)>=192 or sum(len(str(p)) for p in paths)+len(text)>32768:raise RuntimeError('PreparationInventoryCardinalityBound')
        paths.add(path)

    def source_pin(self,path):
        """Select only frozen original inputs or the one frozen postimage."""
        if self.campaign is None:
            return {k:self.expected['files'][str(path)][k] for k in ('size','sha256')}
        self.check(clock_only=True);path=Path(path)
        original=Path(__file__).resolve().parent.parent
        if path.is_relative_to(self.source):
            relative=str(path.relative_to(self.source))
            if relative not in E_FILES+('pyproject.toml','tests/harmless_fixture.c','tests/controller_roster.json'):raise RuntimeError('CampaignClosedStagingInput')
            canonical=original/relative
            wanted={k:self.expected['files'][str(canonical)][k] for k in ('size','sha256')}
            variant,_=_campaign_stage(self.slot.number)
            if variant:
                binding=self.campaign.load_binding();name=tuple(CAMPAIGN_MUTANTS)[variant-1]
                post=binding['variants'][name]
                if relative==post['file']:wanted={k:post[k] for k in ('size','sha256')}
        elif path.is_relative_to(self.repository):
            relative=str(path.relative_to(self.repository))
            if relative not in {v[0] for v in PROVIDERS.values()}:raise RuntimeError('CampaignClosedProviderInput')
            wanted={k:self.expected['files'][str(path)][k] for k in ('size','sha256')}
        else:raise RuntimeError('CampaignClosedStagingPath')
        if path.is_symlink() or pin(path)!=wanted:raise RuntimeError('CampaignStagingPostimageMismatch')
        return wanted

    def stage_variant(self):
        if self.campaign is None or self.slot is None or self.slot.preparation is not self or self.slot.state!='CREATING':raise RuntimeError('ActualVariantStaging')
        variant,poison=_campaign_stage(self.slot.number)
        if not variant or poison is not None or self.source.exists() or self.source.is_symlink():raise RuntimeError('CampaignVariantNoClobber')
        original=Path(__file__).resolve().parent.parent
        name=tuple(CAMPAIGN_MUTANTS)[variant-1];file,old,new,_,_=CAMPAIGN_MUTANTS[name]
        post=self.campaign.load_binding()['variants'][name]
        # Finite14-source copy set; no recursive copy, executable hook, newly
        # discovered input, or observed postimage is adopted as an expectation.
        names=E_FILES+('pyproject.toml','tests/harmless_fixture.c','tests/controller_roster.json')
        total=sum(self.expected['files'][str(original/n)]['size'] for n in names)
        total+=max(0,post['size']-self.expected['files'][str(original/file)]['size'])
        if total>1048576:raise RuntimeError('CampaignVariantSourceEnvelope')
        self.source.mkdir(mode=0o700)
        for relative in names:
            self.check();source=original/relative;same(source,self.expected['files'][str(source)])
            if source.stat().st_size>262144:raise RuntimeError('CampaignVariantSourceFileBound')
            raw=source.read_bytes()
            if relative==file:
                raw=_campaign_variant_bytes(raw,old,new,post)
            destination=self.source/relative;destination.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            fd=os.open(destination,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o644)
            try:
                offset=0
                while offset<len(raw):
                    count=os.write(fd,raw[offset:offset+16384])
                    if count<=0:raise RuntimeError('CampaignVariantCopyProgress')
                    offset+=count
                os.fsync(fd)
            finally:os.close(fd)
            del raw;self.source_pin(destination)
        if {str(p.relative_to(self.source)) for p in self.source.rglob('*') if p.is_file()}!=set(names):raise RuntimeError('CampaignVariantClosedCopy')

    def payload_document(self,path,value):
        path=Path(path)
        if path!=self.target/'venv/wordling-test-deployment.json' or getattr(self,'_marker_reserved',False):raise RuntimeError('ConstructionMarkerScope')
        size=0
        for part in _json_parts(value):
            size+=len(part)
            if size+1>262144:raise RuntimeError('ConstructionMarkerBound')
        self.check()
        # Exactly one256KiB/one-file suballocation within frozen4MiB other
        # construction metadata, not an E deployment-class file or raw sink.
        self._marker_reserved=True;self._marker_highwater=262144
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o644)
        wrote=0
        try:
            for part in _json_parts(value):
                data=part.encode('ascii')
                if wrote+len(data)>size:raise RuntimeError('ConstructionMarkerChanged')
                offset=0
                while offset<len(data):
                    n=os.write(fd,data[offset:])
                    if n<=0:raise RuntimeError('ConstructionMarkerWrite')
                    offset+=n
                wrote+=len(data)
            if wrote!=size or os.write(fd,b'\n')!=1:raise RuntimeError('ConstructionMarkerWrite')
            os.fsync(fd)
        finally:os.close(fd)

    def preflight_inputs(self):
        allnames=set(self.expected['files'])|set(self.expected['links'])|set(self.expected['directories'])
        for root in self.expected['closed_roots']:
            r=Path(root)
            if {str(p) for p in r.rglob('*')} != {n for n in allnames if Path(n).is_relative_to(r) and n!=root}:raise RuntimeError('ClosedInputSet:'+root)
        for root,names in self.expected['tool_startup_hook_sets'].items():
            if sorted(str(p) for p in Path(root).glob('*.pth'))!=names:raise RuntimeError('ToolStartupHookSet')
        for name,x in self.expected['files'].items():
            same(name,x)
            self.check(clock_only=True)
        for name,x in self.expected['links'].items():
            p=Path(name)
            if not p.is_symlink() or os.readlink(p)!=x['target'] or str(p.resolve())!=x['resolved'] or rights(p)!=x['rights']:
                raise RuntimeError('ChangedLink:'+name)
        for name,x in self.expected['directories'].items():
            p=Path(name)
            if p.is_symlink() or not p.is_dir() or rights(p)!=x:raise RuntimeError('ChangedDirectory:'+name)
        self.check(clock_only=True)

    def provider_rows(self):
        if self.qualification is not None:
            self.qualification.check(self)
            rows=dict(PROVIDERS);rows['startup_family/lifetime.py']=('scripts/reference/startup_family/lifetime.py',_R5_COMMIT)
            return rows
        if self.campaign is None:return PROVIDERS
        if not _actual_campaign(self.campaign):raise RuntimeError('ActualR5ProviderProjection')
        rows=dict(PROVIDERS);rows['startup_family/lifetime.py']=('scripts/reference/startup_family/lifetime.py',_R5_COMMIT)
        return rows

    def check(self,clock_only=False):
        if self.qualification is not None:self.qualification.check(self)
        if self.finished:raise RuntimeError('FinishedPreparationNotReusable')
        if self.campaign is not None:
            if self.slot is None or self.campaign.slot is not self.slot or self.slot.preparation is not self:raise RuntimeError('ActualPreparationIdentity')
            self.campaign.check(self.slot.traffic_end)
        if time.monotonic()>=self.end:raise RuntimeError('PreparationSharedDeadline')
        if clock_only or not self.target.exists():return
        # Defensive observation only. Prevention premise is the reviewed closed
        # normal-tool output construction proof plus inherited per-file FSIZE,
        # NOT this periodic tree scan.
        count=0;total=0
        for p in self.target.rglob('*'):
            count+=1
            if p.is_file():total+=p.stat().st_size
            if count>10000 or total>536870912:raise RuntimeError('PreparationCreatedFileBound')
        if time.monotonic()>=self.end:raise RuntimeError('PreparationSharedDeadline')

    def run(self,argv,label,tool=False):
        if self.campaign is not None:return self._run_campaign(argv,label,tool)
        self.check();base=self.evidence/label;base.parent.mkdir(parents=True,exist_ok=True)
        trace_read=trace_write=None
        actual=list(argv);pass_fds=()
        if tool:
            trace_read,trace_write=os.pipe2(os.O_CLOEXEC);pass_fds=(trace_write,)
            pipe_stat=os.fstat(trace_read);trace_identity=(pipe_stat.st_dev,pipe_stat.st_ino,pipe_stat.st_mode)
            actual=['/usr/bin/strace','-f','-qq','-y','-s','4096','-e','trace='+TRACE_SURFACE,'-o','/proc/self/fd/'+str(trace_write)]+actual
        end=min(self.end,time.monotonic()+30)
        supervisor_notice('command',end=end)
        spec=dict(argv=actual,logical_argv=argv,cwd=str(self.target),env=self.env,command_end=end,cleanup=2,live_combined_output=self.output_cap,shared_origin=self.start,shared_end=self.end,tool_origin_trace=tool,trace_capture='OWN PIPE; never uncontrolled regular file')
        write_json(base.with_suffix('.command.json'),spec)
        self.budget.reserve([base.with_suffix('.whole.json')],'pair',65536)
        if tool:
            self.budget.reserve([base.with_suffix('.origins.json')],'origin',16777216)
            self.budget.reserve([base.with_suffix('.transient-data.json')],'transient',1048576)
        out=bytearray();err=bytearray();trace=bytearray();failure=None;partial=False;total=0
        rawpaths=[base.with_suffix(suffix) for suffix in ('.stdout','.stderr','.trace')]
        allocation,handles=self.budget.raw_group(rawpaths,'construction_raw',self.output_cap)
        rawfiles={id(buf):handles[base.with_suffix(suffix)] for buf,suffix in ((out,'.stdout'),(err,'.stderr'),(trace,'.trace'))}
        file_limit=33554432 if label.endswith('venv') else 2097152
        def file_ceiling():resource.setrlimit(resource.RLIMIT_FSIZE,(file_limit,file_limit))
        try:
            p=subprocess.Popen(actual,cwd=self.target,env=self.env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,pass_fds=pass_fds,start_new_session=False,preexec_fn=file_ceiling)
        except BaseException as error:
            if trace_write is not None:os.close(trace_write)
            if trace_read is not None:os.close(trace_read)
            for handle in rawfiles.values():handle.close()
            receipt=dict(**spec,exit=None,failure='PopenFailure:'+type(error).__name__,combined_retained_bytes=0,partial_prefix=False,unretained_suffix=None,child_started=False)
            self.budget.document(base.with_suffix('.whole.json'),receipt,'pair',pre_reserved=True);self.calls.append(receipt);self.call_paths.append(base.with_suffix('.whole.json'))
            supervisor_notice('abort')
            raise RuntimeError('PreparationPopenFailure') from None
        if trace_write is not None:os.close(trace_write)
        sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,out);sel.register(p.stderr,selectors.EVENT_READ,err)
        if trace_read is not None:sel.register(trace_read,selectors.EVENT_READ,trace)
        try:
            while sel.get_map() or p.poll() is None:
                if time.monotonic()>=end:raise RuntimeError('PreparationCommandDeadline')
                self.check()
                for key,_ in sel.select(.01):
                    remaining=self.output_cap-total
                    fd=key.fileobj if isinstance(key.fileobj,int) else key.fileobj.fileno()
                    raw=os.read(fd,min(4096,remaining+1))
                    if not raw:sel.unregister(key.fileobj);continue
                    kept=raw[:remaining]
                    # Reserve shared remaining BEFORE retaining in either RAM or
                    # durable raw prefix. The extra detection byte is not kept.
                    self.budget.retain(allocation,key.data,rawfiles[id(key.data)],raw)
                    total=allocation['used']
                    if len(raw)>remaining:
                        partial=True;raise RuntimeError('PreparationLiveOutputBound')
            p.wait(timeout=max(.001,min(1,end-time.monotonic())))
        except BaseException as e:failure=error_tag(e)
        finally:
            if p.poll() is None:
                p.terminate()
                try:p.wait(timeout=.25)
                except subprocess.TimeoutExpired:p.kill();p.wait(timeout=.25)
            sel.close();p.stdout.close();p.stderr.close()
            if trace_read is not None:os.close(trace_read)
            for f in rawfiles.values():f.close()
            total=allocation['used']
            receipt=dict(**spec,exit=p.returncode,failure=failure,combined_retained_bytes=total,partial_prefix=partial or failure is not None,unretained_suffix='UNKNOWN' if partial or failure else None)
            self.budget.document(base.with_suffix('.whole.json'),receipt,'pair',pre_reserved=True);self.calls.append(receipt);self.call_paths.append(base.with_suffix('.whole.json'))
        if failure or p.returncode:
            supervisor_notice('abort')
            raise RuntimeError(failure or 'PreparationCommandFailed:'+label)
        supervisor_notice('idle')
        if tool:
            capture=object.__new__(_RunCapture)
            launch=Path(argv[0]).resolve()
            same(launch,self.expected['files'][str(launch)])
            same('/usr/bin/strace',self.expected['files']['/usr/bin/strace'])
            _CAPTURES[capture]=dict(owner=self,trace_path=str(base.with_suffix('.trace')),trace_sha256=hashlib.sha256(trace).hexdigest(),launch_argv=tuple(argv),launch_executable_pin=self.expected['files'][str(launch)],env=tuple(sorted(self.env.items())),cwd=str(self.target),tracer_pin=self.expected['files']['/usr/bin/strace'],tracer_pid=p.pid,pipe_identity=trace_identity,source_helper_sha256=self.expected['files'][str(Path(__file__).resolve())]['sha256'])
            self.tool_origins(base.with_suffix('.trace'),label,capture)
        self.check()
        return subprocess.CompletedProcess(actual,p.returncode,bytes(out),bytes(err))

    def _run_campaign(self,argv,label,tool):
        origin=time.monotonic_ns();self.check()
        stages=('venv','qualify-literal-before','stdlib-before','compile','wheel','install','qualify-literal-after','origins')
        stage=len(self.calls)
        if stage>=8 or label!=stages[stage] or tool!=(stage in (0,3,4,5)):raise RuntimeError('CampaignPreparationStage')
        campaign=self.campaign;index=120+8*self.slot.number+stage
        end=min(origin+30000000000,self.slot.traffic_end,campaign.traffic_end)
        base=self.evidence/label;trace_read=trace_write=None;p=None
        actual=list(argv)
        if tool:
            trace_read,trace_write=os.pipe2(os.O_CLOEXEC)
            pipe_stat=os.fstat(trace_read);trace_identity=(pipe_stat.st_dev,pipe_stat.st_ino,pipe_stat.st_mode)
            actual=['/usr/bin/strace','-f','-qq','-y','-s','4096','-e','trace='+TRACE_SURFACE,'-o','/proc/self/fd/'+str(trace_write)]+actual
        command=_campaign_command(campaign.manifest,'slot',index,trace_write if tool else -1)
        if actual!=command['argv'] or self.env!=command['env'] or str(self.target)!=command['cwd']:raise RuntimeError('CampaignPreparationClosedRecipe')
        spec=dict(argv=actual,logical_argv=argv,cwd=str(self.target),env=self.env,command_end=end/1000000000,cleanup=2,
            live_combined_output=self.output_cap,shared_origin=self.start,shared_end=self.end,tool_origin_trace=tool,
            trace_capture='OWN PIPE; never uncontrolled regular file',campaign_slot=index,registration='ACTUAL SAME-PID GATE; source-owned exact command')
        self.budget.document(base.with_suffix('.command.json'),spec)
        self.budget.reserve([base.with_suffix('.whole.json')],'pair',65536)
        if tool:
            self.budget.reserve([base.with_suffix('.origins.json')],'origin',16777216)
            self.budget.reserve([base.with_suffix('.transient-data.json')],'transient',1048576)
        # Original preparation raw-construction reservation (16MiB in the
        # trace model) covers the <=4MiB bytearrays, returned stdout/stderr
        # copies and trace decoder source. Never charged again as spare arena.
        out=bytearray();err=bytearray();trace=bytearray();failure=None;partial=False
        rawpaths=[base.with_suffix(s) for s in ('.stdout','.stderr','.trace')]
        allocation,handles=self.budget.raw_group(rawpaths,'construction_raw',self.output_cap)
        rawfiles={id(buf):handles[base.with_suffix(s)] for buf,s in ((out,'.stdout'),(err,'.stderr'),(trace,'.trace'))}
        sel=selectors.DefaultSelector();cleanup_end=None;tracer_pid=None
        try:
            campaign.check(end)
            p=campaign.launch(index,actual,self.target,self.env,end,trace_write if tool else -1);tracer_pid=p.pid
            if trace_write is not None:os.close(trace_write);trace_write=None
            sel.register(p.stdout,selectors.EVENT_READ,out);sel.register(p.stderr,selectors.EVENT_READ,err)
            if trace_read is not None:sel.register(trace_read,selectors.EVENT_READ,trace)
            while sel.get_map() or p.poll() is None:
                campaign.check(end);self.check(clock_only=True)
                for key,_ in sel.select(min(.01,max(0,(end-time.monotonic_ns())/1000000000))):
                    campaign.check(end)
                    fd=key.fileobj if isinstance(key.fileobj,int) else key.fileobj.fileno()
                    remaining=self.output_cap-allocation['used'];raw=os.read(fd,min(4096,remaining+1))
                    if not raw:sel.unregister(key.fileobj);continue
                    try:self.budget.retain(allocation,key.data,rawfiles[id(key.data)],raw)
                    except RuntimeError:partial=True;raise
            p.wait(timeout=max(.001,(end-time.monotonic_ns())/1000000000));campaign.check(end)
            if p.returncode:raise RuntimeError('PreparationCommandFailed:'+label)
        except BaseException as error:
            failure=error_tag(error);partial=True;campaign.fatal('PreparationCommandFailure')
            cleanup_end=min(campaign.cleanup_end,self.slot.hard_end)
            if p is not None and p.returncode is None:
                try:campaign.signal_child(p,signal.SIGTERM)
                except BaseException:pass
                term_end=min(cleanup_end,time.monotonic_ns()+250000000)
                while p.poll() is None and time.monotonic_ns()<term_end:time.sleep(min(.01,max(0,(term_end-time.monotonic_ns())/1000000000)))
                if p.returncode is None and time.monotonic_ns()<cleanup_end:
                    try:campaign.signal_child(p,signal.SIGKILL)
                    except BaseException:pass
            # Drain only this command's already-open streams until the SAME
            # cleanup deadline. Excess bytes are discarded and remain UNKNOWN.
            while sel.get_map() and time.monotonic_ns()<cleanup_end:
                for key,_ in sel.select(min(.01,max(0,(cleanup_end-time.monotonic_ns())/1000000000))):
                    fd=key.fileobj if isinstance(key.fileobj,int) else key.fileobj.fileno();raw=os.read(fd,4096)
                    if not raw:sel.unregister(key.fileobj);continue
                    if allocation['used']<allocation['maximum']:
                        kept=raw[:allocation['maximum']-allocation['used']]
                        self.budget.retain(allocation,key.data,rawfiles[id(key.data)],kept)
            if p is not None and p.returncode is None and time.monotonic_ns()<cleanup_end:
                try:p.wait(timeout=(cleanup_end-time.monotonic_ns())/1000000000)
                except subprocess.TimeoutExpired:pass
        finally:
            sel.close()
            if trace_write is not None:os.close(trace_write)
            if trace_read is not None:os.close(trace_read)
            if p is not None:
                p.stdout.close();p.stderr.close()
            for handle in rawfiles.values():handle.close()
            # No new effects or controls are launched after this retirement;
            # its complete future reservation remains permanently spent.
            self.budget._campaign_book.retire(allocation)
            code=p.returncode if p is not None else None
            receipt=dict(**spec,exit=code,failure=failure,combined_retained_bytes=allocation['used'],partial_prefix=partial,
                unretained_suffix='UNKNOWN' if partial else None,child_started='UNKNOWN' if p is None else True,
                gated_initial_argv=list(p.args) if p is not None else None,
                gate_descriptor_numbers='actual Popen argv when returned; launch prefix UNKNOWN otherwise')
            self.budget.document(base.with_suffix('.whole.json'),receipt,'pair',pre_reserved=True)
            whole=base.with_suffix('.whole.json')
            self.calls.append(dict(path=str(whole),pin=dict(**pin(whole),**rights(whole)),exit=code,failure=failure,partial_prefix=partial,slot=index))
            self.call_paths.append(whole)
        if failure is not None or code!=0:raise RuntimeError(failure or 'PreparationUnsettledChild')
        campaign.complete_child(p,whole)
        if tool:
            digest=hashlib.sha256(trace).hexdigest();trace.clear()
            capture=object.__new__(_RunCapture);launch=Path(argv[0]).resolve()
            same(launch,self.expected['files'][str(launch)]);same('/usr/bin/strace',self.expected['files']['/usr/bin/strace'])
            _CAPTURES[capture]=dict(owner=self,trace_path=str(base.with_suffix('.trace')),trace_sha256=digest,launch_argv=tuple(argv),launch_executable_pin=self.expected['files'][str(launch)],env=tuple(sorted(self.env.items())),cwd=str(self.target),tracer_pin=self.expected['files']['/usr/bin/strace'],tracer_pid=tracer_pid,pipe_identity=trace_identity,source_helper_sha256=self.expected['files'][str(Path(__file__).resolve())]['sha256'])
            self.tool_origins(base.with_suffix('.trace'),label,capture)
        self.check()
        return subprocess.CompletedProcess(actual,code,bytes(out),bytes(err))

    def tool_origins(self,path,label,capture=None):
        # No JSON/PID/bool/reconstructed record can select the production exception.
        facts=_CAPTURES.pop(capture,None) if type(capture) is _RunCapture else None
        if facts is None or facts['owner'] is not self or str(path)!=facts['trace_path']:raise RuntimeError('MissingGenuineOwnedCapture')
        raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=facts['trace_sha256']:raise RuntimeError('CaptureChanged')
        records=parse_trace(raw.decode('utf-8'))
        transient=_transient_maps_events(records,facts['launch_argv']);excluded={r['event'] for r in transient}
        receipt=dict(classification='BOUNDED_TRANSIENT_DATA_ONLY',capture={k:v for k,v in facts.items() if k!='owner'},events=transient,contents='UNKNOWN/not captured',not_source_or_permission=True)
        write_json(self.evidence/(label+'.transient-data.json'),receipt,'transient')
        observed={};executed=[]
        for record in records:
            if not record['success'] or record['kind'] not in ('open','exec') or record['event'] in excluded:continue
            # Eligible transient records were consumed LEXICALLY above, before
            # even constructing/resolving/looking up their proc pathname.
            name=str(Path(record['path'].removesuffix(' (deleted)')).resolve());p=Path(name)
            if not p.exists():
                # Successful unavailable external exec/open NEVER disappears.
                # Unavailable owned metadata may not establish code authority.
                if record['kind']=='exec' or not p.is_relative_to(self.target) or p.suffix in ('.py','.pyc','.so'):
                    raise RuntimeError('UnavailableToolOrigin:'+name)
                observed[name]=dict(classification='OWNED_TRANSIENT_NONCODE_UNKNOWN_BYTES');continue
            if not p.is_file():continue
            if p.is_relative_to(self.target):observed[name]=dict(**pin(p),classification='NEW_OWNED_BUILD_OUTPUT')
            elif name in self.expected['files']:
                same(p,self.expected['files'][name]);observed[name]=dict(**pin(p),classification='FROZEN_TOOL_INPUT')
            else:raise RuntimeError('UnclassifiedToolInput:'+name)
            if record['kind']=='exec':executed.append(name)
        write_json(self.evidence/(label+'.origins.json'),dict(records=records,files=observed,executed=executed,semantics='Complete selected open/exec trace framing; unsupported/relative exec/truncated/unavailable code refuses, never silently accepted'))
        if not executed:raise RuntimeError('MissingToolProcessTrace')
        self.check()


def strict_layout(interpreter,expected_files=None):
    interpreter=Path(interpreter);v=interpreter.parent.parent
    if v.is_symlink() or not v.is_dir() or rights(v)['mode'] & 0o022:raise RuntimeError('VenvRoot')
    for name in ('python','python3','python3.12'):
        p=v/'bin'/name
        if (p.is_symlink() or not p.is_file() or p.stat().st_nlink!=1 or
                (p.stat().st_dev,p.stat().st_ino)==(BASE.stat().st_dev,BASE.stat().st_ino) or
                pin(p)!=pin(BASE) or rights(p)['mode']!=rights(BASE)['mode']):
            raise RuntimeError('CopiedAlias:'+str(p))
    cfg=(v/'pyvenv.cfg').read_text()
    expected_cfg='home = '+str(BASE.parent)+'\ninclude-system-site-packages = false\nversion = 3.12.14\nexecutable = '+str(BASE)+'\ncommand = '+str(BASE)+' -m venv --copies --without-pip '+str(v)+'\n'
    if cfg!=expected_cfg:raise RuntimeError('ExactVenvConfig')
    if {p.name for p in (v/'bin').iterdir()}!={'python','python3','python3.12','activate','activate.csh','activate.fish','Activate.ps1'}:raise RuntimeError('ExactCopiedAliasAndScriptSet')
    rows=dict(line.split(' = ',1) for line in cfg.splitlines() if ' = ' in line)
    if rows.get('include-system-site-packages')!='false' or rows.get('home')!=str(BASE.parent) or rows.get('version')!='3.12.14':raise RuntimeError('VenvConfig')
    if rows.get('executable')!=str(BASE) or rows.get('command')!=str(BASE)+' -m venv --copies --without-pip '+str(v):raise RuntimeError('VenvConfigExact')
    allowed={'bin','include','lib','lib64','pyvenv.cfg','wordling-test-deployment.json'}
    if any(p.name not in allowed for p in v.iterdir()):raise RuntimeError('VenvExtraRoot')
    for p in v.rglob('*'):
        if p.name=='__pycache__' or p.name.endswith(('.pyc','.pth','._pth')):raise RuntimeError('VenvCacheOrCustomization:'+str(p))
        if rights(p)['uid']!=os.geteuid():raise RuntimeError('VenvForeignOwner')
        if not p.is_symlink() and rights(p)['mode'] & 0o022:raise RuntimeError('VenvWritableByOther')
        if p.is_symlink() and not (p==v/'lib64' and p.resolve()==v/'lib'):raise RuntimeError('VenvSymlink')
        if expected_files is not None and p.is_file() and str(p) not in expected_files:raise RuntimeError('VenvUnexpectedFile:'+str(p))
    return rows


def compare_observation(observation,interpreter,expected,installed,project=False):
    if type(observation) is not dict or len(observation.get('modules',{}))>2048 or len(observation.get('maps',{}))>512:raise RuntimeError('ObservationCardinality')
    v=Path(interpreter).parent.parent;site=v/'lib/python3.12/site-packages'
    wanted_path=[str(PREFIX/'lib/python312.zip'),str(PREFIX/'lib/python3.12'),str(PREFIX/'lib/python3.12/lib-dynload'),str(site)]
    if observation['sys_path']!=wanted_path:raise RuntimeError('ExactOrderedSysPath')
    if observation['version']!=[3,12,14] or observation['executable']!=str(interpreter) or observation['prefix']!=str(v) or observation['exec_prefix']!=str(v) or observation['base_prefix']!=str(PREFIX) or observation['base_exec_prefix']!=str(PREFIX):raise RuntimeError('RuntimePrefix')
    expected_flags=dict(debug=0,inspect=0,interactive=0,optimize=0,dont_write_bytecode=1,no_user_site=1,no_site=0,ignore_environment=1,verbose=0,bytes_warning=0,quiet=0,hash_randomization=1,isolated=1,dev_mode=False,utf8_mode=0,warn_default_encoding=0,safe_path=True,int_max_str_digits=4300)
    if observation['flags']!=expected_flags or not observation['default_excepthook'] or any(observation['customize'].values()) or not all(observation['features'].values()):raise RuntimeError('RuntimeStartup')
    for module,fields in observation['modules'].items():
        for key,x in fields.items():
            if not x['exists']:continue
            name=x['path']
            if name in installed:same(name,installed[name])
            elif name in expected['files'] and Path(name).is_relative_to(PREFIX/'lib/python3.12') and not Path(name).is_relative_to(PREFIX/'lib/python3.12/site-packages'):same(name,expected['files'][name])
            else:raise RuntimeError('UnexpectedModuleOrigin:'+module+':'+name)
            target=installed.get(name,expected['files'].get(name))
            if dict(size=x['size'],sha256=x['sha256'])!={k:target[k] for k in ('size','sha256')}:raise RuntimeError('ObservedSourceMismatch')
    for name,x in observation['maps'].items():
        if name==str(interpreter.resolve()):
            if x!=pin(BASE):raise RuntimeError('CopiedMappedInterpreter')
        elif name in expected['runtime_elf'] or name in expected['runtime_mapped_data']:
            same(name,expected['files'][name])
            if x!=pin(name):raise RuntimeError('MappedELFMismatch')
        else:raise RuntimeError('UnexpectedMappedELF:'+name)
    if project:
        facts=observation['project'];site_files=set(installed)
        if facts is None or set(str(site/n) for n in facts['source_files'])!={n for n in site_files if n.endswith('.py')}:raise RuntimeError('Exact20SourceSet')
        if facts['aliases']!=['wordling_reference_startup_v1','wordling_reference_startup_v1.artifacts','wordling_reference_startup_v1.engine','wordling_reference_startup_v1.lifetime']:raise RuntimeError('FacadeAliasSet')
        if facts['provider']['root']!=str(site/'startup_family') or facts['provider']['version']!=1:raise RuntimeError('ProviderRoot')
        for name,x in facts['provider']['sha256'].items():
            if installed[str(site/'startup_family'/name)]['sha256']!=x:raise RuntimeError('ProviderSourceRoot')
        for x in facts['classes'].values():
            if x['module'] not in facts['aliases'] or str(Path(x['origin'])) not in installed:raise RuntimeError('ProviderClassOrigin')
    elif observation['project'] is not None:raise RuntimeError('UnexpectedProjectImport')


def preflight(interpreter,inventory):
    """New integrated deployment only; no legacy3.13 qualification inference."""
    if type(inventory) is _QualifiedRuntime:
        if _entry_data_actual(inventory.campaign):return inventory.campaign.verify_runtime(interpreter,inventory)
        return current_campaign().verify_runtime(interpreter,inventory)
    strict_layout(interpreter,inventory)
    for name,x in inventory.items():same(name,x)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');args=parser.parse_args()
    if not args.prepare:raise SystemExit('DISABLED: exact source/manifest ROOT grant required before --prepare')
    from controller_deployment import deploy
    source=Path(__file__).resolve().parent.parent;repository=source.parents[3]
    if 'WORDLING_PREPARATION_CONTROL_FD' not in os.environ:raise RuntimeError('SurvivingSupervisorRequired')
    origin=float(os.environ['WORDLING_PREPARATION_ORIGIN'])
    expected=load_expected();context=Preparation(TARGET,TARGET/'receipts',expected,origin=origin)
    code=1
    try:
        interpreter,inventory=deploy(source,repository,TARGET,TARGET/'receipts/deployment',context=context)
        code=0
        print(json.dumps(dict(status='TCB_QUALIFICATION_OBSERVED_ONLY',interpreter=str(interpreter),inventory=pin(TARGET/'receipts/deployment/deployment-inventory.json'),P_effects=False,grants=False,root_and_independent_review_required=True)))
    finally:
        write_json(TARGET/'receipts/whole.json',dict(exit=code,elapsed=time.monotonic()-context.start,calls=[immutable_metadata_ref(p,context.evidence) for p in context.call_paths],P_effects=False,grants=False))
    return code

if __name__=='__main__':
    # Preserve raw failures without invoking the OS packaging tool's apport
    # exception hook or creating a host crash report. No hook is changed.
    try:
        if sys.argv[1:2]==['--harmless-gate']:result=_campaign_gate(sys.argv[3:],int(sys.argv[2]))
        elif sys.argv[1:2]==['--harmless-coordinator'] and len(sys.argv)==4:result=_harmless_coordinator(int(sys.argv[2]),sys.argv[3])
        elif sys.argv[1:2]==['--harmless-executable'] and len(sys.argv) in (5,6,7):result=_harmless_executable(int(sys.argv[2]),sys.argv[3],int(sys.argv[4]),int(sys.argv[5]) if len(sys.argv)>=6 else -1,int(sys.argv[6]) if len(sys.argv)==7 else -1)
        elif sys.argv[1:2]==['--campaign-gate']:result=_campaign_gate(sys.argv[2:])
        else:result=main()
    except SystemExit as exc: result=exc.code
    except BaseException as error:
        emit_diagnostic(error);result=2
    raise SystemExit(result)
