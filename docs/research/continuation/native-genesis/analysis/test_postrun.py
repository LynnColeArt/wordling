"""Actual original replays and rehashed semantic controls, all post-run/offline."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import probe_audit as a
import native_genesis as g
BASE=a.OUT/'runs/wp43-genesis-01-ascii-first-retrieve'


class Postrun(unittest.TestCase):
    def test_all_ten_original_twenty_reader_six_print_and_git_witnesses(self):
        x=a.audit();self.assertEqual(x['Git_raw_files_verified'],2862);self.assertEqual(x['reader_paths'],20)
        self.assertIs(x['constructor_ready'],False)

    def replay(self,change,expected,case='ascii-first-retrieve'):
        source=a.OUT/'runs'/('wp43-genesis-01-'+case)
        with tempfile.TemporaryDirectory(prefix='wp43-rehashed-')as tmp:
            base=Path(tmp)/source.name;shutil.copytree(source,base)
            report=json.loads((base/'run.json').read_text());change(base,report)
            # Recompute every local artifact hash, so a rejection is semantic, not a stale checksum.
            for row in report['results']:
                for item in row['artifacts']:
                    f=base/item['path'];item['size']=f.stat().st_size;item['sha256']=g.sha(f)
                for item in row.get('exports',[]):
                    f=base/('r'+str(row['repetition']))/item['host']
                    if f.exists():item.update(size=f.stat().st_size,sha256=g.sha(f))
            (base/'run.json').write_text(json.dumps(report))
            with self.assertRaises(g.Refusal)as e:g.result(base/'run.json')
            self.assertEqual(e.exception.code,expected)

    def test_rehashed_nonexecuted_filename_substitution_refused(self):
        def change(base,r):
            d=base/'r1/first-save-typed-name';raw=bytearray((d/'vram.bin').read_bytes());chars=bytes(raw[::2]);self.assertIn(b'G43TEXT',chars)
            changed=chars.replace(b'G43TEXT',b'G43WRNG');raw[::2]=changed;(d/'vram.bin').write_bytes(raw)
            text='\n'.join(bytes(raw[i:i+160:2]).replace(b'\0',b' ').decode('cp437').rstrip()for i in range(0,4000,160))+'\n';(d/'screen.txt').write_text(text)
        self.replay(change,'WrongFilename')

    def test_rehashed_hidden_actual_wire_save_refused(self):
        def change(base,r):
            p=base/'r1/qmp-wire.jsonl';msg={'execute':'human-monitor-command','arguments':{'command-line':'sendkey f10 80'}}
            with p.open('a')as f:f.write(json.dumps({'direction':'tx-buffer','raw_hex':json.dumps(msg).encode().hex()})+'\n')
        self.replay(change,'WireCommandChanged')

    def test_rehashed_swapped_dirty_cancel_branch_refused(self):
        def change(base,r):
            self.assertIn('G43DIRTY.WP5',{x['host']for x in r['results'][0]['exports']})
            self.assertNotIn('G43RETRY.WP5',{x['host']for x in r['results'][0]['exports']})
            r['case']='ascii-name-cancel'
        self.replay(change,'RequiredExportMissing',case='ascii-dirty-exit-return')

    def test_rehashed_fabricated_zero_empty_native_refused(self):
        def change(base,r):
            d=base/'r1';(d/'EMPTY.WP5').write_bytes(b'');r['results'][0]['exports'].append({'name':'EMPTY','host':'EMPTY.WP5','exit':0,'size':0,'sha256':g.sha(d/'EMPTY.WP5')})
        self.replay(change,'RequiredExportMissing',case='empty-f10-cancel')

    def test_rehashed_initial_profile_default_source_refused(self):
        def change(base,r):
            r['preparation']['private_sources'][0]['sha256']='0'*64
            (base/'prelaunch.json').write_text(json.dumps(r['preparation']))
        self.replay(change,'SourceChanged')

    def test_rehashed_owned_pid_termination_cannot_be_fabricated(self):
        def change(base,r):
            r['results'][0]['owned_process']['pid']=0
            (base/'r1/owned-process.json').write_text(json.dumps(r['results'][0]['owned_process']))
        self.replay(change,'UnprovenPID')

    def test_rehashed_fake_final_dos_refused(self):
        self.replay(lambda b,r:(b/'r1/clean-exit/screen.txt').write_text('C:\\WP51>\nDoc 1 Pg 1 Ln 1" Pos 1"\n'),'FakeExit')

    def test_postrun_public_plan_preserves_every_raw_git_witness(self):
        import subprocess
        ledger=json.loads((a.OUT/'analysis/genesis-ledger.json').read_text())
        before={r['path']:g.sha(a.OUT/r['path'])for r in ledger['raw_files']}
        r=subprocess.run([sys.executable,str(a.ROOT/'scripts/reference/native_genesis.py'),'plan'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout)
        self.assertEqual(before,{r['path']:g.sha(a.OUT/r['path'])for r in ledger['raw_files']})
        self.assertEqual(a.git_seals(ledger['raw_files']),2862)

    def test_full_control_ink_print_mutations_refused(self):
        self.assertEqual(a.print_audit(a.PRINT)['bytes'],153)
        for bad in [a.PRINT[:-1],a.PRINT+b'\n',a.PRINT.replace(b'G43ASCIIZ',b'G43ASCIJZ'),a.PRINT.replace(b'\r\n',b'\n',1),a.PRINT.replace(b' '*10,b' '*9,1)]:
            with self.assertRaises(g.Refusal)as e:a.print_audit(bad)
            self.assertEqual(e.exception.code,'PrintChanged')

    def test_changed_raw_git_blob_refused(self):
        ledger=json.loads((a.OUT/'analysis/genesis-ledger.json').read_text());row=ledger['raw_files'][0]
        with tempfile.TemporaryDirectory()as tmp:
            root=Path(tmp);p=root/row['path'];p.parent.mkdir(parents=True);p.write_bytes(b'changed committed witness')
            with self.assertRaises(g.Refusal)as e:a.git_seals(ledger['raw_files'],root)
            self.assertEqual(e.exception.code,'RawGitChanged')

    def test_raw_inventory_cannot_drop_a_file(self):
        ledger=json.loads((a.OUT/'analysis/genesis-ledger.json').read_text())
        with self.assertRaises(g.Refusal)as e:a.git_seals(ledger['raw_files'][:-1])
        self.assertEqual(e.exception.code,'RawInventoryChanged')


if __name__=='__main__':unittest.main()
