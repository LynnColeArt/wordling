"""Read-only inspectors for the authored native document fixtures, not a WP codec."""
import hashlib
import struct


def prefix(data):
    if data[:4]!=bytes.fromhex('ff575043') or data[8:10]!=bytes([1,10]):
        raise ValueError('Expected original native document')
    body=struct.unpack_from('<I',data,4)[0]
    if not 16<=body<=len(data):raise ValueError('Invalid document offset')
    packets=[];offset=16;seen=set()
    while offset:
        if offset in seen or not 16<=offset<=body-10:raise ValueError('Invalid prefix index')
        seen.add(offset)
        kind,count,size,nxt=struct.unpack_from('<HHHI',data,offset)
        if kind!=0xfffb or size!=count*10 or offset+size>body:raise ValueError('Invalid prefix index size')
        for i in range(1,count):
            kind,length,start=struct.unpack_from('<HII',data,offset+i*10)
            if not kind:continue
            if start+length>body:raise ValueError('Packet outside prefix')
            packets.append({'type':kind,'offset':start,'length':length})
        offset=nxt
    flag=next(p for p in packets if p['type']==6)
    return {'document_offset':body,'packets':packets,'document_flags':{
        'offset':flag['offset'],'value':data[flag['offset']],
        'must_be_formatted':bool(data[flag['offset']]&8)}}


def plain_merge(data):
    """Accept only ASCII/control bytes and validated D4/00 formatter functions.

    SDK51 WP-55 describes the length and page number fields. Unknown structures
    fail explicitly; this deliberately does not parse arbitrary WP documents.
    """
    info=prefix(data);body=data[info['document_offset']:];text=bytearray();pages=[];hard=0;i=0
    while i<len(body):
        c=body[i]
        if c==0xd4:
            if i+4>len(body) or body[i+1]!=0:raise ValueError('Unsupported formatter function')
            length=struct.unpack_from('<H',body,i+2)[0]
            if length<10 or i+length+4>len(body):raise ValueError('Invalid formatter length')
            if body[i+length:i+length+4]!=struct.pack('<HBB',length,0,0xd4):
                raise ValueError('Formatter trailer mismatch')
            pages.append(struct.unpack_from('<H',body,i+8)[0]);i+=length+4
        elif 32<=c<127 or c in [9,10,12,13]:
            if c==12:hard+=1
            text.append(c);i+=1
        else:raise ValueError(f'Unsupported fixture byte {c:02x} at body offset {i}')
    return {**info,'hard_page_count':hard,'formatter_page_numbers':pages,
            'ascii_text':text.decode('ascii'),'body_sha256':hashlib.sha256(body).hexdigest()}
