#!/usr/bin/env python3
"""Create a disclosed private CTMouse variant; never modify the reference master."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile
from run import ROOT, digest

base = ROOT / 'research/cache/reference/master'
profile = json.loads((ROOT / 'docs/research/reference-environment/environment.json').read_text())
assert digest(base / 'harddisk.img') == profile['master_disk_sha256']
assert digest(base / 'boot.img') == profile['master_boot_sha256']
archive = Path('/tmp/wp78-ctmouse.zip')
assert digest(archive) == 'f5d00e98e81d06060db0d1f36e4f51d44447fd0c794dc2cedd9a1cc696e3bee2'
private = ROOT / 'research/cache/reference/wp78-mouse-master'
private.mkdir(exist_ok=False)
for name in ['harddisk.img', 'boot.img']:
    shutil.copyfile(base / name, private / name)
with zipfile.ZipFile(archive) as z:
    driver = private / 'CTMOUSE.EXE'
    driver.write_bytes(z.read('BIN/CTMOUSE.EXE'))
    (private / 'CTMOUSE.LSM').write_bytes(z.read('APPINFO/CTMOUSE.LSM'))
subprocess.run(['mcopy', '-i', str(private / 'harddisk.img') + '@@1048576', str(driver), '::/CTMOUSE.EXE'], check=True)
startup = private / 'FDAUTO.BAT'
subprocess.run(['mcopy', '-i', str(private / 'boot.img'), '::/FDAUTO.BAT', str(startup)], check=True)
original_startup = startup.read_bytes()
startup.write_bytes(original_startup.replace(b'WP\r\n', b'C:\\CTMOUSE.EXE\r\nWP\r\n'))
subprocess.run(['mcopy', '-o', '-i', str(private / 'boot.img'), str(startup), '::/FDAUTO.BAT'], check=True)
profile['parent_profile_id'] = profile['profile_id']
profile['profile_id'] += '-ctmouse-2.1b4-private'
profile['master_disk_sha256'] = digest(private / 'harddisk.img')
profile['master_boot_sha256'] = digest(private / 'boot.img')
profile['mouse_driver'] = {
    'path': 'C:\\CTMOUSE.EXE', 'sha256': digest(driver), 'bytes': driver.stat().st_size,
    'package_sha256': digest(archive), 'package_sha1': hashlib.sha1(archive.read_bytes()).hexdigest(),
    'source': 'https://ibiblio.org/pub/micro/pc-stuff/freedos/files/repositories/latest/base/ctmouse.zip',
    'metadata': 'https://ibiblio.org/pub/micro/pc-stuff/freedos/files/repositories/latest/html/en/base/ctmouse/20250409.8/index.html',
    'license': 'GPL-2.0, external resource retained only in ignored private cache',
    'change': 'Add driver before WP in private FDAUTO.BAT; original master unchanged',
    'parent_startup_sha256': hashlib.sha256(original_startup).hexdigest(),
    'derived_startup_sha256': digest(startup),
}
(private / 'profile.json').write_text(json.dumps(profile, indent=2) + '\n')
print(private)
