"""Create a small Lotus 1-2-3 worksheet for DOS range probes."""
from pathlib import Path
from struct import pack
import sys


def record(kind, payload=b""):
    return pack("<HH", kind, len(payload)) + payload


count = int(sys.argv[2]) if len(sys.argv) > 2 else 7
worksheet = record(0, pack("<H", 0x0406))
worksheet += record(6, pack("<HHHH", 0, 0, 2, 2))
for row, values in enumerate((("Name", "Count", "Outside"), ("Amber", count, 91), ("Outside", 25, 42))):
    for column, value in enumerate(values):
        header = pack("<BHH", 0xff, column, row)
        if isinstance(value, int):
            worksheet += record(13, header + pack("<h", value))
        else:
            worksheet += record(15, header + b"'" + value.encode("ascii") + b"\0")
worksheet += record(1)
Path(sys.argv[1]).write_bytes(worksheet)
