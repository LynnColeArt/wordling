"""Bounded Standard Printer literal ink/overstrike audit, no physical metrics."""
from pathlib import Path
import native_edits as n

def audit(native,stream):
 raw=Path(native).read_bytes();tokens=n.body_tokens(raw[int.from_bytes(raw[4:8],'little'):]);plain=b'';bold=b'';active=False;start=None
 for token in tokens:
  if token['kind']=='BoldOn':active=True;start=len(plain)
  elif token['kind']=='BoldOff':active=False
  else:
   char=bytes.fromhex(token['hex']);plain+=char
   if active:bold+=char
 printed=Path(stream).read_bytes()
 if any(c not in (10,13) and not 32<=c<=126 for c in printed):raise ValueError('Unsupported printer language for literal text audit')
 raw_parts=[part for part in printed.split(b'\r') if part.strip(b'\n ')]
 parts=[part.removeprefix(b'\n') for part in raw_parts]
 if not parts or parts[0]!=b' '*10+plain:raise ValueError('Original first ink pass differs from exact native ASCII')
 expected=[b' '*10+plain]
 if bold.strip(b' '):expected.append(b' '*(10+start)+bold)
 if parts!=expected:raise ValueError('Original bold overstrike differs from exact native selected span')
 return {'first_ink_pass_hex':parts[0].hex(),'remaining_ink_pass_hex':[x.hex() for x in parts[1:]],'leading_space_bytes':10,'scope':'literal bytes of selected original Standard Printer on these short one-line fixtures only; no pitch/origin/height/tolerance claim','stream_bytes':len(printed),'sha256':n.sha(stream)}
