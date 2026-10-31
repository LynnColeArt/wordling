"""Derived evidence checks; no original guest launch or native writer."""
import copy
import json
from pathlib import Path
import unittest

from analyze import difference,format_fields,membership


HERE=Path(__file__).resolve().parent


class AnalysisTests(unittest.TestCase):
    def test_original_margin_inputs_have_documentary_units(self):
        a=json.loads((HERE/'runs/wp14-r01-L1-WRAP-L3-LR/CHANGEA.WP5.annotation.json').read_text())
        before=copy.deepcopy(a)
        fields=format_fields(a)
        margins=[x for x in fields if x.get('name')=='Left/Right Margins']
        self.assertEqual(margins[-1]['new_values'],[1500,1800])
        self.assertEqual(margins[-1]['old_values'],[1200,1200])
        self.assertEqual(next(x for x in fields if x.get('name')=='Line Height')['new_value'],240)
        self.assertEqual(next(x for x in fields if x.get('name')=='Line Spacing')['new_value'],256)
        self.assertEqual(next(x for x in fields if x.get('name')=='Page Number Position')['new_position_code'],6)
        self.assertEqual(a,before)

    def test_original_hard_page_membership(self):
        a=json.loads((HERE/'runs/wp14-r01-L2-HP/BASEA.WP5.annotation.json').read_text())
        m=membership(a)
        self.assertEqual(m['native_page_ordinals'],2)
        self.assertEqual([(x['text'],x['native_page_ordinal']) for x in m['rows']],[('BEFORE',1),('AFTER',2)])

    def test_unknown_width_is_not_silently_read_as_margin(self):
        a=json.loads((HERE/'runs/wp14-r01-L1-WRAP-L3-LR/CHANGEA.WP5.annotation.json').read_text())
        bad=copy.deepcopy(a)
        for t in bad['tokens']:
            raw=bytes.fromhex(t['hex'])
            if raw[:2]==bytes.fromhex('d001'):t['hex']=raw[:8].hex()
        self.assertFalse(any(x.get('name')=='Left/Right Margins' for x in format_fields(bad)))

    def test_comparison_retains_control_and_space_differences(self):
        self.assertFalse(difference(b'A  \r\n',b'A \n')['equal'])
        d=difference(b'A  \r\n',b'A \n')
        self.assertEqual(d['bytes'],[5,3])
        self.assertFalse(d['normalized'])

    def test_original_dormant_return_preserves_print_until_boundary_moves(self):
        root=HERE/'runs/wp14-r01-L2-DORMANT'
        base=json.loads((root/'BASEA.WP5.annotation.json').read_text())
        dormant=json.loads((root/'DORMANTA.WP5.annotation.json').read_text())
        changed=json.loads((root/'CHANGEA.WP5.annotation.json').read_text())
        self.assertEqual(dormant['counts'].get('dormant-hard-return'),1)
        self.assertNotIn('dormant-hard-return',base['counts'])
        self.assertNotIn('dormant-hard-return',changed['counts'])
        self.assertEqual(changed['counts']['hard-return'],dormant['counts']['hard-return']+1)
        self.assertEqual((root/'BASE.PRN').read_bytes(),(root/'DORMANT.PRN').read_bytes())
        self.assertNotEqual((root/'DORMANT.PRN').read_bytes(),(root/'CHANGE.PRN').read_bytes())

    def test_original_absolute_and_relative_tab_fields(self):
        for mode,margin,positions in [('ABS',65535,[2400,3600,2400,3600]),('REL',1200,[2700,3900,2700,3900])]:
            p=HERE/('runs/wp14-r01-L4-'+mode)/'CHANGEA.WP5.annotation.json'
            fields=format_fields(json.loads(p.read_text()))
            tabs=next(x for x in fields if x['name']=='Tab Set')
            self.assertEqual(tabs['new_left_margin_word'],margin)
            self.assertEqual([p for p in tabs['new_position_words'] if p!=65535],[2400,3600])
            self.assertEqual([x['absolute_tab_align_wpu'] for x in fields if x['name']=='Center/Align/Tab/Left Margin Release'],positions)


if __name__=='__main__':unittest.main()
