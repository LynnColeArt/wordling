"""Artifact-observer controls; these never stand in for executable/native proof."""
import unittest
from terminal import Terminal
class Observation(unittest.TestCase):
    def test_split_csi_and_trailing_cells(self):
        t=Terminal(20,4);t.feed(b'\x1b[2');t.feed(b'J\x1b[HMacro:');self.assertTrue(t.text().startswith('Macro: '));self.assertEqual((t.x,t.y),(6,0))
    def test_cursor_diffs_and_erase(self):
        t=Terminal(20,4);t.feed(b'Macro queued\x1b[1;7Hcomplete\x1b[K');self.assertTrue(t.rows()[0].startswith('Macro complete '));t.feed(b'\r\x1b[2P');self.assertTrue(t.rows()[0].startswith('cro complete'))
    def test_reverse_index_and_lines(self):
        t=Terminal(20,4);t.feed(b'A\r\nB\r\nC\r\x1bMD');self.assertTrue(t.rows()[1].startswith('D'));t.feed(b'\x1b[1;1H\x1b[M');self.assertTrue(t.rows()[0].startswith('D'))
    def test_modes_and_osc_are_not_body_text(self):
        t=Terminal(20,4);t.feed(b'\x1b[?1049h\x1b[>31u\x1b]11;?\x1b\\ABC\x1b[0m');self.assertTrue(t.text().startswith('ABC'));self.assertEqual(t.unknown,[])
if __name__=='__main__':unittest.main()
