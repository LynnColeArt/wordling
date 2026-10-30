"""Negative audits use copies; original probe evidence is never edited."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT/'scripts/reference'))
import session1
import audit_states
import audit_catalogue
import struct


class EvidenceBoundaries(unittest.TestCase):
    def test_corrupt_original_input_is_refused(self):
        original = session1.FIXTURE
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base/'CMD51-204'/'ORIGIN.WP5'
            target.parent.mkdir()
            data = bytearray(original.read_bytes());data[-1] ^= 1
            target.write_bytes(data)
            shutil.copyfile(original.parent.parent/'run.json',base/'run.json')
            with patch.object(session1,'FIXTURE',target),self.assertRaisesRegex(ValueError,'fixture differs'):
                session1.fixture()

    def test_malformed_captured_offset_is_refused(self):
        original=bytearray(session1.FIXTURE.read_bytes())
        for offset in (0,15,len(original)+1,0xffffffff):
            struct.pack_into('<I',original,4,offset)
            with self.assertRaises(ValueError):audit_states.body(original)
        with self.assertRaises(struct.error):audit_states.body(b'bad')

    def test_same_feature_wrong_cursor_state_is_refused(self):
        cases=json.loads((ROOT/'docs/research/command-scenarios.json').read_text())
        features=json.loads((ROOT/'docs/research/feature-inventory.json').read_text())
        index=json.loads((session1.OUT/'state-index.json').read_text())
        case=next(c for c in cases if c['id']=='CMD51-019')
        sub=next(s for s in case['session1_subcases'] if s['branch']=='cursor')
        sub['accepted_state_labels']=['codes-before-initial']
        with self.assertRaisesRegex(AssertionError,'After-initial case linked to wrong state'):
            audit_catalogue.check(cases,features,index)

    def altered_manifest(self, alteration, message):
        source = next((session1.OUT/'runs').glob('*/run.json'))
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary)
            target = out/'runs'/'negative'
            shutil.copytree(source.parent,target)
            manifest = json.loads((target/'run.json').read_text())
            (out/'accepted-branches.json').write_text(json.dumps({'accepted_run_ids':[manifest['run_id']]}))
            alteration(manifest)
            (target/'run.json').write_text(json.dumps(manifest))
            with patch.object(session1,'OUT',out),contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(ValueError,message):session1.verify('negative')

    def test_valid_unrelated_case_cannot_label_retrieval(self):
        self.altered_manifest(lambda r:r['results'][0].update(case_id='CMD51-001'),'Case-feature mismatch')

    def test_changed_capture_checksum_is_refused(self):
        self.altered_manifest(lambda r:r['results'][0]['evidence'][0].update(sha256='0'*64),'Evidence checksum mismatch')


if __name__=='__main__':unittest.main()
