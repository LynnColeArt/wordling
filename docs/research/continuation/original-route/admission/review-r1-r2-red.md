# WP104 R1/R2 genuine RED checkpoint

Review frozen source f0d990eeca478b4a6f9635b1a354eb0f0b8fb3e2.
Command: `/usr/bin/python -B -m unittest discover -s internal/document/evidence/reference_controller/tests -p test_original_foreground.py -v`.

Actual ordinary installed managed Python3.12 candidate: five tests, two failures, three passes. The failures identify missing OriginalLeaf methods and both invalid canonical ledger states, independently of authority construction. Raw stdout/stderr are retained beside this record. No grant, ROOT/admin, CONTROL/P session, private guard/image, VM or Mac action was invoked. This is a source compatibility regression, not positive OS evidence. The original failure remains preserved at its commit and candidate.
