from pathlib import Path
import sys,json,unittest
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-t');O=R/'docs/research/continuation/native-genesis';sys.path[:0]=[str(R/'scripts/reference'),str(O/'analysis')];import test_postrun as t
class Extra(unittest.TestCase):
 def test_rehashed_real_empty_native_truncation_is_not_no_file(self):
  def change(base,run):
   p=base/'r1/G43EMPTY.WP5';self.assertEqual(p.stat().st_size,324);p.write_bytes(b'')
  t.Postrun().replay(change,'ExportFailed',case='empty-first-save')
 def test_rehashed_filename_cursor_claim_must_match_raw_CRTC(self):
  def change(base,run):
   p=base/'r1/first-save-typed-name/cursor.json';x=json.loads(p.read_text());x['column']=(x['column']+1)%80;p.write_text(json.dumps(x))
  t.Postrun().replay(change,'CursorChanged',case='empty-first-save')
r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Extra));assert r.wasSuccessful();Path('/tmp/wordling-wp43-independent/extra-negatives.json').write_text(json.dumps({'tests':2,'passes':2,'controls':['rehashed actual324B empty native ->0B rejects ExportFailed','rehashed filename cursor claim rejects CursorChanged'],'new_VM':False},indent=2)+'\n')
