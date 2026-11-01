"""Exact finite LedgerRecordV1 validation then bounded ASCII encoding, no user hooks."""
from typing import TypedDict
from .errors import Refusal
from .account import LedgerOperationPermit

SCHEMA = 'wordling.reference-controller.ledger/v1'
STATES = ('AUTHORIZED', 'CHARGED', 'SETUP', 'RUNNING', 'STOP_COLLECTING',
          'STOPPED_ISSUED', 'EXPORTING', 'PHYSICAL_RELEASED', 'AUDITING', 'COMPLETE', 'HALTED')


class LedgerRecordV1(TypedDict):
    schema: str
    leaf: str
    sequence: int
    state: str
    source: dict
    observed_ns: int
    facts: dict


def _hex(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def encode(record, permit):
    if type(permit) is not LedgerOperationPermit or not permit._consumed:
        raise Refusal('InvalidPermit')
    book, meter, limit = permit._book, permit._meter, permit._limits.max_record_bytes
    owner = meter._owner
    if (type(record) is not dict or len(record) != 7 or
            any(type(k) is not str for k in record) or set(record) !=
            {'schema', 'leaf', 'sequence', 'state', 'source', 'observed_ns', 'facts'}):
        raise Refusal('RecordSchema')
    if (type(record['schema']) is not str or record['schema'] != SCHEMA or
            type(record['leaf']) is not str or not 0 < len(record['leaf']) <= 128 or
            not record['leaf'].isascii() or record['leaf'] != book.leaf or
            type(record['sequence']) is not int or record['sequence'] != permit.record_sequence or
            not 0 <= record['sequence'] < 2**63 or type(record['state']) is not str or
            record['state'] not in STATES or type(record['observed_ns']) is not int or
            not 0 <= record['observed_ns'] < 2**63 or type(record['facts']) is not dict):
        raise Refusal('RecordSchema')
    source = record['source']
    if (type(source) is not dict or len(source) != 2 or
            any(type(k) is not str for k in source) or set(source) != {'binding', 'plan'} or
            not _hex(source.get('binding')) or not _hex(source.get('plan')) or
            source['binding'] != book._source or source['plan'] != book._plan):
        raise Refusal('RecordSource')
    seen = set()
    nodes = characters = 0

    def charge(n=1):
        meter.charge(owner, work=n)

    def string_bound(value, key=False):
        nonlocal characters
        if type(value) is not str or len(value) > (64 if key else 4096):
            raise Refusal('RecordString')
        if key and (not value or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-' for c in value)):
            raise Refusal('RecordKey')
        characters += len(value)
        if characters > 32768:
            raise Refusal('RecordCharacters')
        charge(len(value) + 1)
        if any(0xd800 <= ord(c) <= 0xdfff for c in value):
            raise Refusal('RecordUnicode')
        return 2 + 12 * len(value)

    def preflight(value, depth):
        nonlocal nodes
        charge()
        nodes += 1
        if nodes > 4096 or depth > 8:
            raise Refusal('RecordStructure')
        t = type(value)
        if t is str:
            return string_bound(value)
        if t is int:
            if value.bit_length() > 64 or not -(2**63) <= value < 2**63:
                raise Refusal('RecordInteger')
            return len(str(value))
        if value is None:
            return 4
        if t is bool:
            return 4 if value else 5
        if t not in (dict, list):
            raise Refusal('RecordType')
        if len(value) > 256:
            raise Refusal('RecordEntries')
        if id(value) in seen:
            raise Refusal('RecordAlias')
        seen.add(id(value))
        total = 2
        if value:
            total += 2 + 2 * (depth - 1)
        for k in value if t is dict else range(len(value)):
            charge()
            total += 2 * depth + 2
            if t is dict:
                nodes += 1
                if nodes > 4096:
                    raise Refusal('RecordStructure')
                total += string_bound(k, True) + 2
                child = value[k]
            else:
                child = value[k]
            total += preflight(child, depth + 1)
            if total > limit:
                raise Refusal('RecordBytes')
        return total

    if preflight(record, 1) + 1 > limit:
        raise Refusal('RecordBytes')
    out = bytearray()
    pieces = 0

    def emit(text):
        nonlocal pieces
        pieces += 1
        if pieces > 4096:
            raise Refusal('RecordPieces')
        charge()
        raw = text.encode('ascii')
        if len(raw) > 4096 or len(out) + len(raw) > limit:
            raise Refusal('RecordBytes')
        out.extend(raw)

    def quoted(value):
        if type(value) is not str or len(value) > 4096 or any(0xd800 <= ord(c) <= 0xdfff for c in value):
            raise Refusal('RecordMutation')
        emit('"')
        for c in value:
            charge()
            n = ord(c)
            if c in ('"', '\\'):
                emit('\\' + c)
            elif c in '\b\f\n\r\t':
                emit({'\b': '\\b', '\f': '\\f', '\n': '\\n', '\r': '\\r', '\t': '\\t'}[c])
            elif n < 32 or n >= 127:
                if n <= 0xffff:
                    emit('\\u%04x' % n)
                else:
                    n -= 0x10000
                    emit('\\u%04x\\u%04x' % (0xd800 + (n >> 10), 0xdc00 + (n & 1023)))
            else:
                emit(c)
        emit('"')

    def write(value, depth):
        charge()
        t = type(value)
        if depth >= 8 or (t in (dict, list) and len(value) > 256):
            raise Refusal('RecordMutation')
        if t is str:
            quoted(value)
        elif value is None:
            emit('null')
        elif t is bool:
            emit('true' if value else 'false')
        elif t is int:
            if value.bit_length() > 64 or not -(2**63) <= value < 2**63:
                raise Refusal('RecordMutation')
            emit(str(value))
        elif t in (list, dict):
            emit('{' if t is dict else '[')
            if value:
                emit('\n')
            for i, k in enumerate(value if t is dict else range(len(value))):
                emit('  ' * (depth + 1))
                if t is dict:
                    quoted(k)
                    emit(': ')
                write(value[k], depth + 1)
                emit(',\n' if i + 1 < len(value) else '\n')
            if value:
                emit('  ' * depth)
            emit('}' if t is dict else ']')
        else:
            raise Refusal('RecordMutation')
    write(record, 0)
    emit('\n')
    meter.check(owner)
    return bytes(out)
