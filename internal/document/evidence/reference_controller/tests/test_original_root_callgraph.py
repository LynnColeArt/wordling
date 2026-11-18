"""Non-vacuous reviewed-code call-site gate, not authentication of a hostile host."""
import ast
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1]
NAMES = ('__init__.py','__main__.py','bootstrap.py','errors.py','account.py','ownership.py',
         'records.py','issuance.py','cli.py','controller.py','protocol.py','publisher.py',
         'original.py','original_release.py','original_control_admin.py')
EXPECTED = {('_mint_registered_decision','original_release.py','coordinate_one'),
            ('RootDecision','original_release.py','_mint_registered_decision')}


def check_sources(sources):
    if set(sources) != set(NAMES):
        raise AssertionError('source-floor')
    found = []
    for filename, text in sources.items():
        aliases = {}
        tree = ast.parse(text,filename=filename)
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom):
                for item in node.names:
                    aliases[item.asname or item.name] = item.name
        def visit(node, function='<module>'):
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
                function = node.name
            if isinstance(node,ast.Call):
                name = node.func.id if isinstance(node.func,ast.Name) else node.func.attr if isinstance(node.func,ast.Attribute) else None
                name = aliases.get(name,name)
                if name == 'coordinate_one':
                    raise AssertionError('ordinary-code-calls-ROOT')
                if name in ('_mint_registered_decision','RootDecision'):
                    found.append((name,filename,function))
                if name in ('getattr','setattr','eval','exec'):
                    for arg in node.args:
                        if isinstance(arg,ast.Constant) and arg.value in ('coordinate_one','_mint_registered_decision','RootDecision'):
                            raise AssertionError('dynamic-ROOT-selector')
            for child in ast.iter_child_nodes(node):
                visit(child,function)
        visit(tree)
    if len(found) != 2 or set(found) != EXPECTED:
        raise AssertionError('sole-mint-floor-or-callsite')


def check_admin_phases(text):
    tree=ast.parse(text)
    admin=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='administer_one')
    functions={n.name:n for n in admin.body if isinstance(n,ast.FunctionDef)}
    def calls(node,name):
        return [n for n in ast.walk(node) if isinstance(n,ast.Call) and
                ((isinstance(n.func,ast.Name) and n.func.id==name) or
                 (isinstance(n.func,ast.Attribute) and n.func.attr==name))]
    assert len(calls(functions['source_phase'],'verify_administration'))==1,'live-source-check-floor'
    assert len(calls(functions['file'],'source_phase'))==1,'file-phase-source-check'
    assert len(calls(functions['read'],'source_phase'))==1,'input-phase-source-check'
    direct=[n for n in admin.body if isinstance(n,ast.Expr) and calls(n,'source_phase')]
    effect_try=next(n for n in admin.body if isinstance(n,ast.Try))
    assert len(direct)>=2 and min(n.lineno for n in direct)<effect_try.lineno,'pre-create-source-check'
    group=next(n for n in effect_try.body if isinstance(n,ast.For))
    assert calls(group,'source_phase'),'group-phase-source-check'
    assert calls(effect_try,'source_phase'),'pre-receipt-source-check'


class RootCallGraph(unittest.TestCase):
    def setUp(self):
        self.sources = {n:(SOURCE/'tests'/n if n=='original_control_admin.py' else SOURCE/n).read_text() for n in NAMES}

    def test_admin_live_source_phases(self):
        check_admin_phases(self.sources['original_control_admin.py'])

    def test_admin_identity_bypass_is_rejected_by_gate(self):
        changed=self.sources['original_control_admin.py'].replace('source.verify_administration(end,used)','pass')
        with self.assertRaisesRegex(AssertionError,'live-source-check-floor'):
            check_admin_phases(changed)

    def test_exact_live_gate(self):
        check_sources(self.sources)

    def test_missing_mint_is_not_a_vacuous_pass(self):
        changed = dict(self.sources)
        changed['original_release.py'] = changed['original_release.py'].replace(
            'decision = _mint_registered_decision(invocation, source, plan,',
            'decision = unavailable(invocation, source, plan,')
        with self.assertRaisesRegex(AssertionError,'floor'):
            check_sources(changed)

    def test_leaf_call_mutant_is_rejected(self):
        changed = dict(self.sources)
        changed['original.py'] += '\ndef unauthorized():\n    return coordinate_one("row", "bundle", "note")\n'
        with self.assertRaisesRegex(AssertionError,'ordinary-code'):
            check_sources(changed)

    def test_alias_mint_mutant_is_rejected(self):
        changed = dict(self.sources)
        changed['original.py'] += '\nfrom .original_release import _mint_registered_decision as alternate\ndef unauthorized():\n    return alternate(None,None,None,None)\n'
        with self.assertRaisesRegex(AssertionError,'callsite'):
            check_sources(changed)


if __name__ == '__main__':
    unittest.main()
