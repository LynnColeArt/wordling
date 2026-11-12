import importlib.util,sys,unittest,io
from pathlib import Path
sys.path.insert(0,str(Path('scripts/reference').resolve()));sys.path.insert(0,str(Path('docs/research/continuation/text-layout').resolve()))
import text_layout,analyze,test_analysis
source=Path('scripts/reference/text_layout.py').read_text()
mutant=source.replace("0x99:'dormant-hard-return'","0x99:'hard-return'")
assert mutant!=source
namespace={'__file__':text_layout.__file__,'__name__':'mutated_text_layout'};exec(compile(mutant,'mutant.py','exec'),namespace)
result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(namespace['Tests']))
assert not result.wasSuccessful();print('Mutant dormant99-as-normal-return rejected:',len(result.failures),'failures',len(result.errors),'errors')
source=Path(analyze.__file__).read_text();mutant=source.replace('new_values=[u16(8),u16(10)]','new_values=[u16(6),u16(8)]');assert mutant!=source
namespace={'__file__':analyze.__file__,'__name__':'mutated_analysis'};exec(compile(mutant,'mutant-analysis.py','exec'),namespace)
test_analysis.format_fields=namespace['format_fields']
result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(test_analysis.AnalysisTests))
assert not result.wasSuccessful();print('Mutant documented margin offsets shifted rejected:',len(result.failures),'failures',len(result.errors),'errors')
print('No production/evidence files modified; no VM execution.')
