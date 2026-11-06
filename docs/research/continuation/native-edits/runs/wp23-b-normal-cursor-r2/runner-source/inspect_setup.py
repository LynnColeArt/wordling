#!/usr/bin/env python3
"""Read SET packet 54h and independently compare its timestamp to FAT16 metadata."""

import argparse
import hashlib
import json
from pathlib import Path
import struct

PARTITION = 1048576


def dos_stamp(date, time):
    return {"date_word": date, "time_word": time,
            "date": f"{1980+(date>>9):04}-{(date>>5)&15:02}-{date&31:02}",
            "time": f"{time>>11:02}:{(time>>5)&63:02}:{(time&31)*2:02}"}


class FAT16:
    def __init__(self, image):
        self.image = Path(image)
        self.data = self.image.read_bytes()
        boot = self.data[PARTITION:PARTITION+512]
        self.bps = struct.unpack_from("<H", boot, 11)[0]
        self.spc = boot[13]
        self.reserved = struct.unpack_from("<H", boot, 14)[0]
        self.nfat = boot[16]
        self.root_count = struct.unpack_from("<H", boot, 17)[0]
        self.fat_sectors = struct.unpack_from("<H", boot, 22)[0]
        if self.bps != 512 or not self.spc or not self.fat_sectors:
            raise ValueError("Unexpected reference volume geometry")
        self.fat_start = PARTITION + self.reserved * self.bps
        self.root_start = self.fat_start + self.nfat * self.fat_sectors * self.bps
        root_sectors = (self.root_count*32+self.bps-1)//self.bps
        self.data_start = self.root_start + root_sectors * self.bps

    def chain(self, cluster):
        seen = set()
        while cluster < 0xFFF8:
            if cluster < 2 or cluster in seen:
                raise ValueError("Invalid/cyclic FAT chain")
            seen.add(cluster)
            start = self.data_start + (cluster-2)*self.spc*self.bps
            if start + self.spc*self.bps > len(self.data):
                raise ValueError("Cluster outside image")
            yield start, self.spc*self.bps
            cluster = struct.unpack_from("<H", self.data, self.fat_start+cluster*2)[0]

    def entry(self, path):
        extents = [(self.root_start, self.root_count*32)]
        components = path.replace("\\", "/").strip("/").upper().split("/")
        for index, component in enumerate(components):
            stem, _, extension = component.partition(".")
            key = (stem.ljust(8)+extension.ljust(3)).encode("ascii")
            found = None
            for start, length in extents:
                for offset in range(start, start+length, 32):
                    entry = self.data[offset:offset+32]
                    if entry[0] in [0, 0xE5] or entry[11] == 0x0F:
                        continue
                    if entry[:11] == key:
                        found = (offset, entry)
                        break
                if found:
                    break
            if found is None:
                raise FileNotFoundError(path)
            offset, entry = found
            if index < len(components)-1:
                if not entry[11] & 16:
                    raise ValueError("Non-directory component")
                extents = list(self.chain(struct.unpack_from("<H", entry, 26)[0]))
        return offset, entry

    def read_file(self, path):
        _, entry = self.entry(path)
        size = struct.unpack_from("<I", entry, 28)[0]
        pieces = [self.data[a:a+n] for a,n in self.chain(struct.unpack_from("<H", entry, 26)[0])]
        return b"".join(pieces)[:size]


def inspect(image):
    fs = FAT16(image)
    data = fs.read_file("WP51/WP{WP}.SET")
    if data[:4] != bytes.fromhex("ff575043") or data[9] != 0x11:
        raise ValueError("Not the original SET format")
    packets, seen, offset = [], set(), 16
    while offset:
        if offset in seen or not 16 <= offset <= len(data)-10:
            raise ValueError("Invalid/cyclic SET index")
        seen.add(offset)
        kind,count,size,next_block = struct.unpack_from("<HHHI",data,offset)
        if kind != 0xFFFB or size != count*10 or offset+size>len(data):
            raise ValueError("Invalid SET index shape")
        for i in range(1,count):
            kind,length,start = struct.unpack_from("<HII",data,offset+i*10)
            if start+length>len(data):
                raise ValueError("SET packet outside file")
            packets.append({"type":kind,"offset":start,"length":length})
        offset = next_block
    default = next(p for p in packets if p["type"] == 0x54)
    packet = data[default["offset"]:default["offset"]+default["length"]]
    printer = packet[37:50].split(b"\0")[0].decode("ascii")
    cached_date,cached_time=struct.unpack_from("<HH",packet,237)
    file_offset,entry=fs.entry("WP51/"+printer)
    fat_time,fat_date=struct.unpack_from("<HH",entry,22)
    return {"image_sha256":hashlib.sha256(fs.data).hexdigest(),"setup_sha256":hashlib.sha256(data).hexdigest(),
            "setup_size":len(data),"packets":packets,"default_printer":printer,
            "packet_54_offset":default["offset"],"cached_time_offset":default["offset"]+239,
            "cached_timestamp":dos_stamp(cached_date,cached_time),"printer_fat_timestamp":dos_stamp(fat_date,fat_time),
            "printer_directory_entry_offset":file_offset,"printer_sha256":hashlib.sha256(fs.read_file("WP51/"+printer)).hexdigest(),
            "cached_matches_printer_timestamp":(cached_date,cached_time)==(fat_date,fat_time)}


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("image",type=Path);a=p.parse_args()
    print(json.dumps(inspect(a.image),indent=2))
