# Independent WP93 review, cycle 1

**Approve** source `2df0dd6d2be20fed5274abc754cd1393a7fabb71`, issued base
`c2443182`. Only the three owned layout files changed. Approved WP81
`453b9219` and WP92 `bfea5e24` are actual ancestors. Layout and native
formatter ownership remain distinct.

## Verified behavior

- `FromDocument` and `Project` retain native-owner order, a single placement
  for every owner, zero-width owners, final rows, and exact native source bytes.
  They use physical profile dimensions without viewport inputs. Qualified
  caret gaps, nearest real gaps, desired-column vertical movement, line
  boundaries and printed-page movement are exposed to WP94/WP84.
- Tests against pinned `FLOW.WP` verify 116 rows, transitions at rows 54 and
  108, final Pg3 Ln2.17 Pos3.5, a tab occupying half an inch, and the original
  vertical sequence at requested column 63. Compound page interiors are not
  returned as editable gaps.
- An independent public probe loaded the actual stopped-original
  `TABONE.WP.native` and `TABTWO.WP.native` with SHA-256
  `3cc560107f0a21acfce87f06488fae08828331c438a286ebd7f9824d99f150f5`
  and `d51edebd6fff93230299874e377f6468b50e2d57282cf5ed8a9dc29515a63bb9`.
  End positions were columns 8 and 13, respectively, and projection retained
  the input bytes. The same probe generated 300 independent multi-page ASCII
  fixtures with spaces and hard returns. Typed WP92 plan adoption converged
  to the exact same revision on the second pass for every fixture. Probe
  source remains under the path recorded in `/tmp/wordling-WP93-review-path`.
- The original native wrap, tab-edge, hard return page, soft-space page and
  unbroken-word page fixtures exercise exact bytes through WP92. Planning
  returns a revision-owned operation. Layout never adopts it and never uses
  renderer text as native content.

Full Go build, tests and vet passed, along with fresh layout/document race
tests, formatting and scoped diff checks.

## Qualification limits

The 564-byte FastSave family remains read-only under the separately reviewed
document admission boundary. WP93 can still project its qualified owners. The
layout computes live tab geometry from the matched profile. Native Tab cache
refresh after a semantic change remains a document-owned operation and has a
separate original witness. These limits do not alter WP93's pure projection
contract. Live reducer use, terminal paths, and the complete acceptance journey
remain assigned to WP94, WP84 and WP86.
