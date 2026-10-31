import unittest
from terminal import Screen,TerminalFailure
class Decoder(unittest.TestCase):
 def test_incremental_and_cells(self):
  s=Screen(10,4);s.feed(b'abc\x1b[')
  with self.assertRaises(TerminalFailure):s.snapshot()
  s.feed(b'2D\x1b[PZ');self.assertEqual(s.snapshot()['rows'][0],'aZ        ')
 def test_lines_and_reverse(self):
  s=Screen(5,3);s.feed(b'A\x1b[2;1HB\x1b[3;1HC\x1b[2;1H\x1b[L');self.assertEqual(s.snapshot()['rows'],['A    ','     ','B    '])
  s.feed(b'\x1b[M');self.assertEqual(s.snapshot()['rows'],['A    ','B    ','     '])
  s.feed(b'\x1b[H\x1bM');self.assertEqual(s.snapshot()['rows'],['     ','A    ','B    '])
 def test_unknown_refused(self):
  for b in [b'\x1b[8z',b'\x1bX',b'\x1b[?999p',b'\x1b[?3h',b'\x1b[3J',b'\xff']:
   with self.assertRaises(TerminalFailure):Screen().feed(b)
 def test_insert_count_bounded(self):
  s=Screen(10,4);s.feed(b"abc\x1b[H\x1b[999999999999999999999999999999999999@")
  self.assertEqual(s.snapshot()["rows"][0]," "*10)
 def test_no_fake_model(self):
  s=Screen();s.feed(b'Editing | ORIGIN | gap 2 | NotSaved\r\nDirty=true Block=false revision=3 history=unknown qualified=false')
  self.assertEqual(s.state()['gap'],2);self.assertIsNone(s.state()['history_count']);self.assertTrue(s.state()['dirty'])
  s.feed(b'\x1b[2J')
  with self.assertRaises(TerminalFailure):s.state()
if __name__=='__main__':unittest.main()
