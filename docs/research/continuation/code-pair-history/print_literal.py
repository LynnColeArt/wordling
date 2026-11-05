"""Exact measured Standard Printer families, not a formatter or generic bold rule."""
import hashlib

ON=bytes.fromhex('c30cc3');OFF=bytes.fromhex('c40cc4')
PREFIX=b'\r'+b'\r\n'*6
SUFFIX=b'\r'+b'\r\n'*60
CLOSING=b'A'+ON+b'BC'+OFF+ON+OFF+b'XDZ'


class PrintRefusal(ValueError):pass


def audit(case,body,stream):
    if case=='closing-block-repair-yes':
        if body!=CLOSING:raise PrintRefusal('Outside exact balanced two-pair/empty-second literal source')
        plain=b'ABCXDZ';overstrike=b' '*11+b'BC'
        expected=PREFIX+b' '*10+plain+b'\r'+overstrike+SUFFIX
        spans=[{'start':1,'literal_hex':'4243'},{'start':3,'literal_hex':'','empty_second_pair':True}]
    elif case.startswith('direct-')and case.endswith('-on'):
        if body!=b'ASXBCDZ':raise PrintRefusal('Outside exact direct On/S/X/Z literal source')
        plain=body;overstrike=b'';expected=PREFIX+b' '*10+plain+SUFFIX;spans=[]
    elif case.startswith('direct-')and case.endswith('-off'):
        if body!=b'ABCSXDZ':raise PrintRefusal('Outside exact direct Off/S/X/Z literal source')
        plain=body;overstrike=b'';expected=PREFIX+b' '*10+plain+SUFFIX;spans=[]
    else:raise PrintRefusal('Unknown literal family')
    if len(stream)>2048 or stream!=expected:raise PrintRefusal('Complete control/ink/overstrike stream differs; no whitespace/control normalization')
    return {'case':case,'stream_bytes':len(stream),'sha256':hashlib.sha256(stream).hexdigest(),
            'prefix_hex':PREFIX.hex(),'suffix_hex':SUFFIX.hex(),'first_ink_hex':(b' '*10+plain).hex(),
            'overstrike_hex':overstrike.hex(),'known_literal_spans':spans,
            'scope':'exact measured one-line selected Standard Printer families only; no physical metrics, arbitrary spans or formatter permission'}
