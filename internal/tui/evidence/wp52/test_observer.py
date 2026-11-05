"""Offline VT/style falsifiers for the observer, never product proof."""
import unittest
from run_pty import Styled
class Observer(unittest.TestCase):
 def test_roles_reset_and_intensity(self):
  t=Styled();t.feed(b'\x1b[1mX\x1b[m\x1b[37;41mA\x1b[97;44m[BOLD]\x1b[37mBC\x1b[97m[bold]\x1b[37mD\x1b[mQ')
  self.assertEqual(t.roles(0)[:18],[0,71]+[31]*6+[23]*2+[31]*6+[23,0]);self.assertFalse(t.style[2])
 def test_private_sgr_queries_and_tabs_no_visible_cells(self):
  t=Styled();t.feed(b'\x1b[?2026$p\x1b[>4m\x1b[?5W');self.assertEqual(t.unknown,[]);self.assertEqual(t.x,0)
 def test_line_insert_delete_and_erase_copy_styles(self):
  t=Styled();t.feed(b'\x1b[37;41mA\x1b[2;1H\x1b[97;44mB\x1b[H\x1b[L')
  self.assertEqual(t.roles(1)[0],71);self.assertEqual(t.rows()[1][0],'A')
  t.feed(b'\x1b[M');self.assertEqual(t.roles(0)[0],71);self.assertEqual(t.rows()[0][0],'A')
  t.feed(b'\x1b[m\x1b[2K');self.assertEqual(t.roles(0),[0]*80)
 def test_unknown_control_remains_unknown(self):
  t=Styled();t.feed(b'\x1b[999z');self.assertEqual(t.unknown,['CSI999z'])
if __name__=='__main__':unittest.main()

class CapturedAlias(unittest.TestCase):
 def test_actual_old_alias_red_immutable_prefix_green(self):
  import json
  from pathlib import Path
  here=Path(__file__).resolve().parent
  receipt=json.loads((here/'pty-07/result.json').read_bytes())
  frozen=json.loads((here/'raw-replay.json').read_bytes());mismatches=0
  for row in receipt['results']:
   wire=(here/'pty-07'/('native-r'+str(row['repeat']))/'wire-output.bin').read_bytes()
   for index,w in enumerate(row['witnesses']):
    t=Styled();t.feed(wire[:w['wire_bytes']]);self.assertEqual(t.pending,bytearray())
    independent=json.loads(json.dumps(t.styles));self.assertEqual(independent,frozen['processes'][str(row['repeat'])][index]['styles'])
    if independent!=w['styles']:mismatches+=1
    # Later output must never retarget a frozen receipt at an earlier offset.
    t.feed(wire[w['wire_bytes']:]);self.assertEqual(independent,frozen['processes'][str(row['repeat'])][index]['styles'])
  self.assertGreater(mismatches,0,'old defect must reproduce against actual raw prefixes')
