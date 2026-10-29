#!/usr/bin/env python3
"""Fetch the pinned external references into an ignored local research cache."""

import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "research/cache"
TEXT_NAMES = {"REF51": "reference.txt", "WB51": "workbook.txt", "SDK51": "toolkit.txt"}


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    sources = json.loads((ROOT / "docs/research/sources.json").read_text())
    for source in sources:
        destination = CACHE / source["filename"]
        if not destination.exists():
            temporary = destination.with_suffix(".download")
            try:
                request = urllib.request.Request(source["url"], headers={"User-Agent": "Wordling-reference-research/0.1"})
                with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as out:
                    while chunk := response.read(1024 * 1024):
                        out.write(chunk)
                with temporary.open("rb") as stream:
                    digest = hashlib.file_digest(stream, "sha256").hexdigest()
                if digest != source["sha256"]:
                    raise ValueError(f"Source changed: {source['id']}; investigate edition before updating registry")
                temporary.replace(destination)
            finally:
                temporary.unlink(missing_ok=True)
        with destination.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != source["sha256"]:
            raise ValueError(f"Cached source checksum mismatch: {source['id']}")
        subprocess.run(["pdftotext", "-layout", str(destination), str(CACHE / TEXT_NAMES[source["id"]])], check=True)
        print(f"Verified and extracted {source['id']}")


if __name__ == "__main__":
    main()
