#!/usr/bin/env python3
"""Selected assertion-quality probes; restore exact production bytes on every path."""
from pathlib import Path
import hashlib
import subprocess

root = Path(__file__).resolve().parents[3]
source = root / 'internal/document/document.go'
original = source.read_bytes()
mutations = [
 ('gap-step', 'target := c.gap + direction', 'target := c.gap + 2*direction', 'TestOriginalGapsAndSharedViews'),
 ('opaque-crossing', 'if token.Kind == Opaque {', 'if false && token.Kind == Opaque {', 'TestOpaqueIdentitiesArePreservedButNotTraversedOrRendered'),
 ('reveal-identity', 'text = "[bold]"', 'text = "[BOLD]"', 'TestOriginalGapsAndSharedViews'),
 ('token-limit-boundary', 'if info.OuterTokenCount > MaxTokens {', 'if info.OuterTokenCount >= MaxTokens {', 'TestTokenAndWindowBudgets'),
]
try:
    print('production SHA256', hashlib.sha256(original).hexdigest(), flush=True)
    for name, old, new, target in mutations:
        text = original.decode()
        assert text.count(old) == 1, name
        source.write_text(text.replace(old, new))
        command = ['go', 'test', './internal/document', '-run', '^'+target+'$', '-count=1']
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=90)
        print('\nMUTATION', name, '\nCOMMAND', ' '.join(command), '\nEXIT', result.returncode)
        print(result.stdout, result.stderr, flush=True)
        assert result.returncode != 0 and '--- FAIL:' in result.stdout and '[build failed]' not in result.stdout, name
        source.write_bytes(original)
finally:
    source.write_bytes(original)
assert source.read_bytes() == original
print('All four selected mutations compiled and were killed by test assertions; production restored byte-exactly.')
