# WP58 current handoff: cycle2

Read report.md, CONTRACT.md and cycle-2/acceptance-inputs.json first. Current source
corrects I1P2 readiness supervision; independent cycle2 review remains required.
Current results are under cycle-2:57 tests,10 mutants, configured4PASS/3 legitimate
SKIP,8 CLI captures and exact red/green reviewer probes. Root-level prior47-test,
CLI/mutant/resource results and cycle-2/history are OLD evidence, not current runs.

Public entry remains `python -B scripts/reference/startup_transport.py fixture readiness`.
Run `python -B tests/reference/startup-seam/run_suite.py --junit /tmp/startup-suite.xml`
for public tests. `mutate.py` and `capture_cli.py` now write cycle-2 evidence.
The component is generic Linux-only: no legacy delegation, E import, original
resources/VM, grant/native interpretation or M1 closure. Full scope remains open.
