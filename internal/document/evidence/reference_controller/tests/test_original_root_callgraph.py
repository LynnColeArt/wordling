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


class RootCallGraph(unittest.TestCase):
    def setUp(self):
        self.sources = {n:(SOURCE/'tests'/n if n=='original_control_admin.py' else SOURCE/n).read_text() for n in NAMES}

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
